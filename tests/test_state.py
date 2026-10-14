from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_SCRIPT = REPO_ROOT / "skills" / "delta-bags" / "scripts" / "state.py"
SPEC = importlib.util.spec_from_file_location("delta_bags_state", STATE_SCRIPT)
assert SPEC and SPEC.loader
state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(state)


class PathTests(unittest.TestCase):
    def test_linux_paths_use_xdg_defaults(self) -> None:
        profiles, submissions = state.resolve_paths(
            platform="linux", home=Path("/person"), environment={}
        )
        self.assertEqual(profiles, Path("/person/.config/delta-bags/profiles.json"))
        self.assertEqual(
            submissions, Path("/person/.local/state/delta-bags/submissions.json")
        )

    def test_platform_native_paths(self) -> None:
        mac_profiles, mac_submissions = state.resolve_paths(
            platform="darwin", home=Path("/person"), environment={}
        )
        self.assertEqual(mac_profiles, mac_submissions.parent / "profiles.json")

        windows_profiles, windows_submissions = state.resolve_paths(
            platform="win32",
            home=Path("C:/person"),
            environment={"APPDATA": "C:/roaming", "LOCALAPPDATA": "C:/local"},
        )
        self.assertEqual(windows_profiles, Path("C:/roaming/delta-bags/profiles.json"))
        self.assertEqual(windows_submissions, Path("C:/local/delta-bags/submissions.json"))

    def test_default_environment_reads_only_path_variables(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "XDG_CONFIG_HOME": "/custom/config",
                "XDG_STATE_HOME": "/custom/state",
                "OPENAI_API_KEY": "must-not-be-read",
            },
            clear=True,
        ):
            self.assertEqual(
                state._path_environment(),
                {
                    "XDG_CONFIG_HOME": "/custom/config",
                    "XDG_STATE_HOME": "/custom/state",
                },
            )


class ProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary.name) / "profiles.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def add_default(self) -> dict[str, str]:
        profile, _ = state.upsert_profile(
            self.path,
            profile_id="default-id",
            profile_type="default",
            friendly_name="Me",
            first_name="Alex",
            last_name="Rivera",
            skymiles_number="0123456789",
            confirmed=False,
        )
        return profile

    def test_round_trip_preserves_leading_zero_and_private_mode(self) -> None:
        self.add_default()
        profiles = state.load_profiles(self.path)
        self.assertEqual(profiles[0]["skymilesNumber"], "0123456789")
        self.assertNotIn("confirmationNumber", self.path.read_text(encoding="utf-8"))
        if os.name == "posix":
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(self.path.parent.stat().st_mode & 0o777, 0o700)

    def test_replacing_default_requires_confirmation(self) -> None:
        self.add_default()
        with self.assertRaisesRegex(state.StateError, "requires --confirmed"):
            state.upsert_profile(
                self.path,
                profile_id="other-id",
                profile_type="default",
                friendly_name="Pat",
                first_name="Pat",
                last_name="Lee",
                skymiles_number="1111111111",
                confirmed=False,
            )

        replacement, created = state.upsert_profile(
            self.path,
            profile_id="other-id",
            profile_type="default",
            friendly_name="Pat",
            first_name="Pat",
            last_name="Lee",
            skymiles_number="1111111111",
            confirmed=True,
        )
        self.assertTrue(created)
        self.assertEqual(replacement["type"], "default")
        profiles = state.load_profiles(self.path)
        self.assertEqual(sum(profile["type"] == "default" for profile in profiles), 1)
        self.assertEqual(
            next(profile for profile in profiles if profile["id"] == "default-id")["type"],
            "companion",
        )

    def test_changing_or_deleting_default_requires_confirmation(self) -> None:
        self.add_default()
        with self.assertRaisesRegex(state.StateError, "requires --confirmed"):
            state.upsert_profile(
                self.path,
                profile_id="default-id",
                profile_type="default",
                friendly_name="Me",
                first_name="Alex",
                last_name="Rivera",
                skymiles_number="9999999999",
                confirmed=False,
            )
        with self.assertRaisesRegex(state.StateError, "requires --confirmed"):
            state.delete_profile(self.path, "default-id", confirmed=False)

    def test_undocumented_profile_fields_are_rejected(self) -> None:
        document = {
            "schemaVersion": 1,
            "profiles": [
                {
                    "id": "traveler",
                    "type": "companion",
                    "friendlyName": "Pat",
                    "firstName": "Pat",
                    "lastName": "Lee",
                    "skymilesNumber": "0123456789",
                    "confirmationNumber": "ABC123",
                }
            ],
        }
        self.path.write_text(json.dumps(document), encoding="utf-8")
        with self.assertRaisesRegex(state.StateError, "exactly the documented fields"):
            state.load_profiles(self.path)


class LedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.ledger = self.base / "state" / "delta-bags" / "submissions.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(STATE_SCRIPT),
                "--config-dir",
                str(self.base / "config"),
                "--state-dir",
                str(self.base / "state"),
                *arguments,
            ],
            capture_output=True,
            check=False,
            text=True,
        )

    def record_arguments(self) -> list[str]:
        # Use a recent timestamp so the 30-day prune never removes the entry
        # before the duplicate check runs, regardless of today's date.
        recent = datetime.now(timezone.utc) - timedelta(hours=1)
        return [
            "record-submission",
            "--flight-date",
            recent.date().isoformat(),
            "--departure",
            "atl",
            "--arrival",
            "lax",
            "--profile-id",
            "traveler-id",
            "--outcome",
            "approved",
            "--submitted-at",
            state._format_timestamp(recent),
        ]

    def test_duplicate_requires_explicit_override_and_omits_confirmation(self) -> None:
        first = self.command(*self.record_arguments())
        self.assertEqual(first.returncode, 0, first.stderr)

        duplicate = self.command(*self.record_arguments())
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn("explicit approval", duplicate.stderr)

        override = self.command(*self.record_arguments(), "--allow-duplicate")
        self.assertEqual(override.returncode, 0, override.stderr)
        document = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(len(document["submissions"]), 2)
        self.assertNotIn("confirmationNumber", self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(document["submissions"][0]["departureAirport"], "ATL")

    def test_prunes_entries_older_than_thirty_days(self) -> None:
        now = datetime(2026, 8, 15, 12, tzinfo=timezone.utc)
        template = {
            "flightDate": "2026-07-01",
            "departureAirport": "ATL",
            "arrivalAirport": "LAX",
            "profileId": "traveler-id",
            "outcome": "unknown",
        }
        old = {
            **template,
            "id": "old",
            "submittedAt": state._format_timestamp(now - timedelta(days=30, seconds=1)),
        }
        boundary = {
            **template,
            "id": "boundary",
            "submittedAt": state._format_timestamp(now - timedelta(days=30)),
        }
        retained, pruned = state.prune_submissions([old, boundary], now=now)
        self.assertEqual(pruned, 1)
        self.assertEqual([submission["id"] for submission in retained], ["boundary"])


if __name__ == "__main__":
    unittest.main()
