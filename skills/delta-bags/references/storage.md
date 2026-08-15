# Private storage

Prefer the host's existing private store. Use `scripts/state.py` only when the host has local file access and no preferred store.

## Fallback paths

Store runtime data outside the skill, repository, `.agents`, and `.claude` directories.

| Platform | Traveler Profiles | Duplicate ledger |
| --- | --- | --- |
| Linux | `~/.config/delta-bags/profiles.json` | `~/.local/state/delta-bags/submissions.json` |
| macOS | `~/Library/Application Support/delta-bags/profiles.json` | `~/Library/Application Support/delta-bags/submissions.json` |
| Windows | `%APPDATA%\delta-bags\profiles.json` | `%LOCALAPPDATA%\delta-bags\submissions.json` |

The helper creates private directories and files where the platform supports Unix permissions. The files are plaintext; disclose that fact before first save.

## Traveler Profile schema

Store only:

```json
{
  "schemaVersion": 1,
  "profiles": [
    {
      "id": "stable-private-id",
      "type": "default",
      "friendlyName": "Me",
      "firstName": "First",
      "lastName": "Last",
      "skymilesNumber": "0123456789"
    }
  ]
}
```

Allow exactly one `default` profile. All others are `companion`. Keep the SkyMiles number as a 10-character string so leading zeroes survive. Never store a Confirmation Number, password, email body, calendar event, or payment detail.

Confirm before deleting or replacing the Default Traveler or changing its identity/SkyMiles fields. Save a companion only after explicit acceptance.

## Duplicate ledger schema

Store only:

```json
{
  "schemaVersion": 1,
  "submissions": [
    {
      "id": "attempt-id",
      "flightDate": "2026-08-15",
      "departureAirport": "ATL",
      "arrivalAirport": "LAX",
      "profileId": "stable-private-id",
      "submittedAt": "2026-08-15T12:34:56Z",
      "outcome": "approved"
    }
  ]
}
```

Retain entries for 30 days, then prune them. Use the flight date, airport pair, and profile identifier for local duplicate detection. Never add the Confirmation Number.

## Helper commands

Resolve `<skill-dir>` to the directory containing the loaded `SKILL.md`; do not assume the current working directory is the skill directory. Run `python <skill-dir>/scripts/state.py --help` for complete arguments. Common commands:

```text
python <skill-dir>/scripts/state.py paths
python <skill-dir>/scripts/state.py list-profiles
python <skill-dir>/scripts/state.py upsert-profile --type companion --friendly-name Pat --first-name Pat --last-name Lee --skymiles-number 0123456789
python <skill-dir>/scripts/state.py find-duplicate --flight-date 2026-08-15 --departure ATL --arrival LAX --profile-id <id>
python <skill-dir>/scripts/state.py record-submission --flight-date 2026-08-15 --departure ATL --arrival LAX --profile-id <id> --outcome approved
```

Use `--config-dir` and `--state-dir` only for tests or an explicitly selected private location. The skill must work without this helper by applying the same schemas to a host-private store.

For a manually adapted Grok Bot private skill, prefer directories under `/workspace/delta-bags` because xAI documents `/workspace` as durable. Tell the Agent User that every Bot on the same account shares that computer and can access those files.
