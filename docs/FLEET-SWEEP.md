# Fleet Sweep and the Waiver Ledger

You ship more than one app. Fleet Sweep runs the guard over every one of them and gives you one release verdict, so a blocker in the app you forgot about cannot slip through. The Waiver Ledger lets a reviewed false positive step aside, with evidence, until a date you choose, after which it comes back on its own.

## What you get

- One verdict for the whole fleet. `READY`, `READY_WITH_ACTIONS`, `NOT_CHECKED`, or `BLOCKED`, worst app wins. Exit codes 0, 3, 1 and 2, so only a truly ready fleet exits 0.
- No silent passes. The guard prints a `Coverage.` line before every exit naming what it scanned. A partial scan, a platform you declared but the guard did not find, a timeout, a missing or doubled summary, counts that do not match the findings, or an exit code that contradicts them is `NOT_CHECKED`, never `READY`. A waiver can never turn a partial scan into a pass.
- Owner actions in the same report. Account and console steps the scan cannot see (agreements, privacy answers, Data Safety, a test on a real device) sit beside the code findings. A step set to `false`, or no readiness list at all, stays open.
- Waivers that expire and cover one occurrence. A waiver names the app, the finding ID, its severity and its file, so it never hides the same rule firing somewhere new or at a higher severity. It needs a reason, evidence, a reviewer, and an expiry no more than 180 days out. Two waivers for the same occurrence cancel each other. An expired, incomplete, duplicated, or stale waiver is named in the report and the finding returns.
- The release rules a scan cannot see. Each app declares its `regions` and `features`, and every verified, in-force [Ruling Register](RULING-REGISTER.md) requirement that applies blocks the app until you attest to it.
- A GitHub code-scanning file. `--scanning-export` writes findings in the SARIF 2.1.0 format GitHub requires, so they show in the Security tab and on pull requests.

## From install to first verdict

1. Copy the fleet template and list your apps.

   ```bash
   cp templates/fleet.example.json fleet.json
   ```

   Each `name` must be unique. `path` may use `~` and environment variables. `platforms` lists what you ship (`ios`, `android`, `web`), and the sweep checks the guard actually found each one. `readiness` maps each account step to `true` or `false`. Leave it out and the app reports it as an open owner action.
2. Run the sweep.

   ```bash
   python3 scripts/fleet-sweep.py fleet.json
   ```

3. Read the verdict line at the bottom. Exit code 0 is ready, 3 is ready with open actions, 2 is blocked, 1 is not checked or bad input.

## Waive a reviewed false positive

```bash
cp templates/waivers.example.json waivers.json
python3 scripts/fleet-sweep.py fleet.json --waivers waivers.json
```

Each waiver copies the `app` name from the fleet file and the `finding_id`, `severity` and `file` exactly as the guard prints them. Leave `file` out only for a finding the guard prints without one. A waiver never applies to a different app, and one that matches nothing is reported so you can retire it.

## Outputs for CI

```bash
python3 scripts/fleet-sweep.py fleet.json --json fleet-result.json --scanning-export fleet.sarif
```

Upload `fleet.sarif` with `github/codeql-action/upload-sarif` to see findings in code scanning. Paths carry the app name, waived findings stay in the file marked as suppressed with their evidence, and an app that was not checked marks the run unsuccessful. The JSON holds every app, its findings, the waived items with their evidence, waiver problems, and owner actions.

## What it does not do

It does not change a single guard rule. The guard decides what is a finding. Fleet Sweep only gathers, applies waivers you signed, and refuses to call anything ready that it did not see checked.
