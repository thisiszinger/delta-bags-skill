#!/usr/bin/env python3
"""Manage Delta Bags fallback Traveler Profiles and duplicate ledger."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = 1
RETENTION_DAYS = 30
OUTCOMES = {"approved", "rejected", "duplicate", "expired", "failed", "unknown"}
SKYMILES_PATTERN = re.compile(r"^[0-9]{10}$")
AIRPORT_PATTERN = re.compile(r"^[A-Z]{3}$")
DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


class StateError(ValueError):
    """Raised when fallback state or command input is invalid."""


def _clean_text(value: str, field: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise StateError(f"{field} must not be empty")
    return cleaned


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_timestamp(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise StateError("submittedAt must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise StateError("submittedAt must include a timezone")
    return parsed.astimezone(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _path_environment() -> dict[str, str]:
    """Read only the non-secret environment variables used for state paths."""
    values = {
        "APPDATA": os.environ.get("APPDATA"),
        "LOCALAPPDATA": os.environ.get("LOCALAPPDATA"),
        "XDG_CONFIG_HOME": os.environ.get("XDG_CONFIG_HOME"),
        "XDG_STATE_HOME": os.environ.get("XDG_STATE_HOME"),
    }
    return {key: value for key, value in values.items() if value is not None}


def resolve_paths(
    *,
    config_dir: str | None = None,
    state_dir: str | None = None,
    platform: str | None = None,
    home: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> tuple[Path, Path]:
    """Return the platform-native profile and ledger paths."""
    current_platform = platform or sys.platform
    current_home = home or Path.home()
    current_environment = environment if environment is not None else _path_environment()

    if config_dir:
        config_base = Path(config_dir).expanduser()
    elif current_platform == "win32":
        config_base = Path(
            current_environment.get("APPDATA", current_home / "AppData" / "Roaming")
        )
    elif current_platform == "darwin":
        config_base = current_home / "Library" / "Application Support"
    else:
        config_base = Path(
            current_environment.get("XDG_CONFIG_HOME", current_home / ".config")
        )

    if state_dir:
        state_base = Path(state_dir).expanduser()
    elif current_platform == "win32":
        state_base = Path(
            current_environment.get("LOCALAPPDATA", current_home / "AppData" / "Local")
        )
    elif current_platform == "darwin":
        state_base = current_home / "Library" / "Application Support"
    else:
        state_base = Path(
            current_environment.get("XDG_STATE_HOME", current_home / ".local" / "state")
        )

    return (
        config_base / "delta-bags" / "profiles.json",
        state_base / "delta-bags" / "submissions.json",
    )


def _read_json(path: Path, empty: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return empty
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise StateError(f"cannot read valid JSON from {path}") from error
    if not isinstance(data, dict):
        raise StateError(f"state at {path} must be a JSON object")
    return data


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        path.parent.chmod(0o700)

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            json.dump(data, temporary, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        if os.name == "posix":
            os.chmod(temporary_name, 0o600)
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def _validate_profiles_document(data: dict[str, Any]) -> list[dict[str, str]]:
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise StateError("profiles.json has an unsupported schemaVersion")
    raw_profiles = data.get("profiles")
    if not isinstance(raw_profiles, list):
        raise StateError("profiles.json profiles must be an array")

    profiles: list[dict[str, str]] = []
    default_count = 0
    seen_ids: set[str] = set()
    required_keys = {
        "id",
        "type",
        "friendlyName",
        "firstName",
        "lastName",
        "skymilesNumber",
    }

    for raw in raw_profiles:
        if not isinstance(raw, dict) or set(raw) != required_keys:
            raise StateError("each Traveler Profile must contain exactly the documented fields")
        if not all(isinstance(raw[key], str) for key in required_keys):
            raise StateError("Traveler Profile values must be strings")

        profile = {key: raw[key] for key in required_keys}
        profile["id"] = _clean_text(profile["id"], "profile id")
        profile["friendlyName"] = _clean_text(profile["friendlyName"], "friendly name")
        profile["firstName"] = _clean_text(profile["firstName"], "first name")
        profile["lastName"] = _clean_text(profile["lastName"], "last name")
        if profile["type"] not in {"default", "companion"}:
            raise StateError("Traveler Profile type must be default or companion")
        if not SKYMILES_PATTERN.fullmatch(profile["skymilesNumber"]):
            raise StateError("SkyMiles number must contain exactly 10 digits")
        if profile["id"] in seen_ids:
            raise StateError("Traveler Profile ids must be unique")
        seen_ids.add(profile["id"])
        if profile["type"] == "default":
            default_count += 1
        profiles.append(profile)

    if default_count > 1:
        raise StateError("only one Default Traveler is allowed")
    return profiles


def load_profiles(path: Path) -> list[dict[str, str]]:
    data = _read_json(path, {"schemaVersion": SCHEMA_VERSION, "profiles": []})
    return _validate_profiles_document(data)


def save_profiles(path: Path, profiles: Sequence[dict[str, str]]) -> None:
    document = {"schemaVersion": SCHEMA_VERSION, "profiles": list(profiles)}
    _validate_profiles_document(document)
    _write_json(path, document)


def upsert_profile(
    path: Path,
    *,
    profile_id: str | None,
    profile_type: str,
    friendly_name: str,
    first_name: str,
    last_name: str,
    skymiles_number: str,
    confirmed: bool,
) -> tuple[dict[str, str], bool]:
    profiles = load_profiles(path)
    requested = {
        "id": _clean_text(profile_id, "profile id") if profile_id else str(uuid.uuid4()),
        "type": profile_type,
        "friendlyName": _clean_text(friendly_name, "friendly name"),
        "firstName": _clean_text(first_name, "first name"),
        "lastName": _clean_text(last_name, "last name"),
        "skymilesNumber": skymiles_number,
    }
    _validate_profiles_document({"schemaVersion": SCHEMA_VERSION, "profiles": [requested]})

    existing_index = next(
        (index for index, profile in enumerate(profiles) if profile["id"] == requested["id"]),
        None,
    )
    if existing_index is None:
        identical = next(
            (
                profile
                for profile in profiles
                if all(profile[key] == requested[key] for key in requested if key != "id")
            ),
            None,
        )
        if identical:
            return identical, False
    else:
        existing = profiles[existing_index]
        protected_fields = {"type", "firstName", "lastName", "skymilesNumber"}
        protected_change = any(existing[key] != requested[key] for key in protected_fields)
        if existing["type"] == "default" and protected_change and not confirmed:
            raise StateError("changing the Default Traveler requires --confirmed")

    other_default = next(
        (
            profile
            for profile in profiles
            if profile["type"] == "default" and profile["id"] != requested["id"]
        ),
        None,
    )
    if requested["type"] == "default" and other_default:
        if not confirmed:
            raise StateError("replacing the Default Traveler requires --confirmed")
        other_default["type"] = "companion"

    created = existing_index is None
    if created:
        profiles.append(requested)
    else:
        profiles[existing_index] = requested
    save_profiles(path, profiles)
    return requested, created


def delete_profile(path: Path, profile_id: str, *, confirmed: bool) -> dict[str, str]:
    profiles = load_profiles(path)
    existing = next((profile for profile in profiles if profile["id"] == profile_id), None)
    if existing is None:
        raise StateError(f"Traveler Profile {profile_id!r} was not found")
    if existing["type"] == "default" and not confirmed:
        raise StateError("deleting the Default Traveler requires --confirmed")
    save_profiles(path, [profile for profile in profiles if profile["id"] != profile_id])
    return existing


def _validate_submission(raw: Any) -> dict[str, str]:
    required_keys = {
        "id",
        "flightDate",
        "departureAirport",
        "arrivalAirport",
        "profileId",
        "submittedAt",
        "outcome",
    }
    if not isinstance(raw, dict) or set(raw) != required_keys:
        raise StateError("each submission must contain exactly the documented fields")
    if not all(isinstance(raw[key], str) for key in required_keys):
        raise StateError("submission values must be strings")

    submission = {key: raw[key] for key in required_keys}
    submission["id"] = _clean_text(submission["id"], "submission id")
    submission["profileId"] = _clean_text(submission["profileId"], "profile id")
    if not DATE_PATTERN.fullmatch(submission["flightDate"]):
        raise StateError("flight date must use YYYY-MM-DD")
    try:
        datetime.strptime(submission["flightDate"], "%Y-%m-%d")
    except ValueError as error:
        raise StateError("flight date must be a real calendar date") from error
    for key in ("departureAirport", "arrivalAirport"):
        if not AIRPORT_PATTERN.fullmatch(submission[key]):
            raise StateError(f"{key} must be a three-letter uppercase airport code")
    if submission["departureAirport"] == submission["arrivalAirport"]:
        raise StateError("departure and arrival airports must differ")
    _parse_timestamp(submission["submittedAt"])
    if submission["outcome"] not in OUTCOMES:
        raise StateError(f"outcome must be one of: {', '.join(sorted(OUTCOMES))}")
    return submission


def load_submissions(path: Path) -> list[dict[str, str]]:
    data = _read_json(path, {"schemaVersion": SCHEMA_VERSION, "submissions": []})
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise StateError("submissions.json has an unsupported schemaVersion")
    raw_submissions = data.get("submissions")
    if not isinstance(raw_submissions, list):
        raise StateError("submissions.json submissions must be an array")
    submissions = [_validate_submission(raw) for raw in raw_submissions]
    ids = [submission["id"] for submission in submissions]
    if len(ids) != len(set(ids)):
        raise StateError("submission ids must be unique")
    return submissions


def save_submissions(path: Path, submissions: Sequence[dict[str, str]]) -> None:
    validated = [_validate_submission(submission) for submission in submissions]
    _write_json(path, {"schemaVersion": SCHEMA_VERSION, "submissions": validated})


def prune_submissions(
    submissions: Sequence[dict[str, str]], *, now: datetime | None = None
) -> tuple[list[dict[str, str]], int]:
    current = (now or _utc_now()).astimezone(timezone.utc)
    cutoff = current - timedelta(days=RETENTION_DAYS)
    retained = [
        submission
        for submission in submissions
        if _parse_timestamp(submission["submittedAt"]) >= cutoff
    ]
    return retained, len(submissions) - len(retained)


def find_duplicates(
    submissions: Sequence[dict[str, str]],
    *,
    flight_date: str,
    departure: str,
    arrival: str,
    profile_id: str,
) -> list[dict[str, str]]:
    return [
        submission
        for submission in submissions
        if submission["flightDate"] == flight_date
        and submission["departureAirport"] == departure
        and submission["arrivalAirport"] == arrival
        and submission["profileId"] == profile_id
    ]


def _flight_values(args: argparse.Namespace) -> tuple[str, str, str, str]:
    departure = args.departure.upper()
    arrival = args.arrival.upper()
    candidate = {
        "id": "validation",
        "flightDate": args.flight_date,
        "departureAirport": departure,
        "arrivalAirport": arrival,
        "profileId": args.profile_id,
        "submittedAt": "2000-01-01T00:00:00Z",
        "outcome": "unknown",
    }
    _validate_submission(candidate)
    return args.flight_date, departure, arrival, args.profile_id


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage optional plaintext fallback state for the Delta Bags skill."
    )
    parser.add_argument("--config-dir", help="override the platform config base directory")
    parser.add_argument("--state-dir", help="override the platform state base directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("paths", help="show resolved fallback file paths")
    subparsers.add_parser("list-profiles", help="list saved Traveler Profiles")

    get_profile = subparsers.add_parser("get-profile", help="get one Traveler Profile")
    get_profile.add_argument("--id", required=True)

    upsert = subparsers.add_parser("upsert-profile", help="add or update a Traveler Profile")
    upsert.add_argument("--id")
    upsert.add_argument("--type", choices=("default", "companion"), required=True)
    upsert.add_argument("--friendly-name", required=True)
    upsert.add_argument("--first-name", required=True)
    upsert.add_argument("--last-name", required=True)
    upsert.add_argument("--skymiles-number", required=True)
    upsert.add_argument(
        "--confirmed",
        action="store_true",
        help="confirm a protected Default Traveler change",
    )

    delete = subparsers.add_parser("delete-profile", help="delete a Traveler Profile")
    delete.add_argument("--id", required=True)
    delete.add_argument(
        "--confirmed",
        action="store_true",
        help="confirm deletion of the Default Traveler",
    )

    def add_flight_arguments(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument("--flight-date", required=True)
        command_parser.add_argument("--departure", required=True)
        command_parser.add_argument("--arrival", required=True)
        command_parser.add_argument("--profile-id", required=True)

    duplicate = subparsers.add_parser("find-duplicate", help="check for a recent attempt")
    add_flight_arguments(duplicate)

    record = subparsers.add_parser("record-submission", help="record one Request Outcome")
    add_flight_arguments(record)
    record.add_argument("--outcome", choices=sorted(OUTCOMES), required=True)
    record.add_argument("--submitted-at", help="ISO-8601 timestamp; defaults to now")
    record.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="record despite a matching recent attempt after explicit approval",
    )

    subparsers.add_parser("prune-ledger", help="remove attempts older than 30 days")
    return parser


def run(args: argparse.Namespace) -> None:
    profiles_path, submissions_path = resolve_paths(
        config_dir=args.config_dir, state_dir=args.state_dir
    )

    if args.command == "paths":
        _print_json(
            {"profilesPath": str(profiles_path), "submissionsPath": str(submissions_path)}
        )
        return

    if args.command == "list-profiles":
        _print_json({"profiles": load_profiles(profiles_path)})
        return

    if args.command == "get-profile":
        profile = next(
            (profile for profile in load_profiles(profiles_path) if profile["id"] == args.id),
            None,
        )
        if profile is None:
            raise StateError(f"Traveler Profile {args.id!r} was not found")
        _print_json({"profile": profile})
        return

    if args.command == "upsert-profile":
        profile, created = upsert_profile(
            profiles_path,
            profile_id=args.id,
            profile_type=args.type,
            friendly_name=args.friendly_name,
            first_name=args.first_name,
            last_name=args.last_name,
            skymiles_number=args.skymiles_number,
            confirmed=args.confirmed,
        )
        _print_json({"created": created, "profile": profile})
        return

    if args.command == "delete-profile":
        deleted = delete_profile(profiles_path, args.id, confirmed=args.confirmed)
        _print_json({"deleted": deleted})
        return

    if args.command == "find-duplicate":
        flight_date, departure, arrival, profile_id = _flight_values(args)
        submissions = load_submissions(submissions_path)
        retained, pruned = prune_submissions(submissions)
        if pruned:
            save_submissions(submissions_path, retained)
        matches = find_duplicates(
            retained,
            flight_date=flight_date,
            departure=departure,
            arrival=arrival,
            profile_id=profile_id,
        )
        _print_json({"duplicate": bool(matches), "matches": matches, "pruned": pruned})
        return

    if args.command == "record-submission":
        flight_date, departure, arrival, profile_id = _flight_values(args)
        submissions = load_submissions(submissions_path)
        retained, _ = prune_submissions(submissions)
        matches = find_duplicates(
            retained,
            flight_date=flight_date,
            departure=departure,
            arrival=arrival,
            profile_id=profile_id,
        )
        if matches and not args.allow_duplicate:
            raise StateError(
                "a matching attempt exists; require explicit approval before using --allow-duplicate"
            )
        timestamp = _parse_timestamp(args.submitted_at) if args.submitted_at else _utc_now()
        submission = {
            "id": str(uuid.uuid4()),
            "flightDate": flight_date,
            "departureAirport": departure,
            "arrivalAirport": arrival,
            "profileId": profile_id,
            "submittedAt": _format_timestamp(timestamp),
            "outcome": args.outcome,
        }
        retained.append(_validate_submission(submission))
        save_submissions(submissions_path, retained)
        _print_json({"submission": submission})
        return

    if args.command == "prune-ledger":
        submissions = load_submissions(submissions_path)
        retained, pruned = prune_submissions(submissions)
        if pruned or not submissions_path.exists():
            save_submissions(submissions_path, retained)
        _print_json({"pruned": pruned, "retained": len(retained)})
        return

    raise StateError(f"unsupported command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args)
    except StateError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
