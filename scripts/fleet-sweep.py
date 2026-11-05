#!/usr/bin/env python3
"""Fleet Sweep. Runs the guard across every app and returns one release verdict. See docs/FLEET-SWEEP.md."""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_GUARD = REPO / "agent-os" / "hooks" / "app-store-compliance-guard.sh"
DEFAULT_REGISTER = REPO / "data" / "ruling-register.json"
STORE_OF = {"ios": "apple", "android": "google"}
MAX_WAIVER_DAYS = 180
LINE = re.compile(r"^\s+\[(CRITICAL|HIGH|MEDIUM)\]\s+(\S+)\s+(.*)$")
SUMMARY = re.compile(r"^Summary\. critical=(\d+) high=(\d+) medium=(\d+)$")
COVERAGE = re.compile(
    r"^Coverage\. (complete|incomplete) ios=([01]) android=([01]) web=([01])(?: reason=(.*))?$"
)
RANK = {"READY": 0, "READY_WITH_ACTIONS": 1, "NOT_CHECKED": 2, "BLOCKED": 3}
EXIT = {"READY": 0, "BLOCKED": 2, "NOT_CHECKED": 1, "READY_WITH_ACTIONS": 3}
LEVEL = {"critical": "error", "high": "warning", "medium": "note"}
PLATFORMS = ("ios", "android", "web")
WAIVER_TEXT = (
    "app",
    "finding_id",
    "severity",
    "reason",
    "evidence",
    "reviewed_by",
    "expires",
)


class InputError(Exception):
    pass


def load_register_module():
    spec = importlib.util.spec_from_file_location("ruling_register", REPO / "scripts" / "ruling-register.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RR = load_register_module()


def expand(path):
    return Path(os.path.expandvars(os.path.expanduser(path)))


def is_text(value):
    return isinstance(value, str) and value.strip() != ""


def run_guard(guard, app_path, timeout):
    """Returns (exit_code, stdout). exit_code None means the guard did not finish."""
    try:
        done = subprocess.run(
            ["bash", str(guard), str(app_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "APP_STORE_GUARD_OK": "0"},
        )
        return done.returncode, done.stdout
    except subprocess.TimeoutExpired as exc:
        out = (
            exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        )
        return None, out
    except OSError as exc:
        return None, f"could not start the guard. {exc}"


def parse_report(stdout):
    """Reads findings, every Summary line, and every Coverage line, strictly."""
    findings, current, summaries, coverages = [], None, [], []
    for raw in stdout.splitlines():
        m = LINE.match(raw)
        if m:
            current = {
                "severity": m.group(1).lower(),
                "id": m.group(2),
                "title": m.group(3).strip(),
                "file": "",
                "fix": "",
            }
            findings.append(current)
            continue
        text = raw.strip()
        if text.startswith("Summary."):
            s = SUMMARY.match(text)
            summaries.append(tuple(int(x) for x in s.groups()) if s else None)
            current = None
            continue
        if text.startswith("Coverage."):
            c = COVERAGE.match(text)
            coverages.append(c.groups() if c else None)
            current = None
            continue
        if current is not None and text.startswith("file. "):
            current["file"] = text[6:]
        elif current is not None and text.startswith("fix. "):
            current["fix"] = text[5:]
    return findings, summaries, coverages


def integrity_problem(code, findings, summaries, coverages):
    """Any reason this report cannot be trusted, or empty when it can."""
    if code is None:
        return "the guard did not finish (timeout or start failure)"
    if code not in (0, 2):
        return f"the guard exited {code}, which is not a complete verdict"
    if len(summaries) != 1 or summaries[0] is None:
        return "the guard report needs exactly one well formed Summary line"
    if len(coverages) != 1 or coverages[0] is None:
        return "the guard report needs exactly one well formed Coverage line"
    counted = tuple(
        sum(1 for f in findings if f["severity"] == s)
        for s in ("critical", "high", "medium")
    )
    if summaries[0] != counted:
        return f"the Summary counts {summaries[0]} do not match the findings read {counted}"
    if (code == 2) != (counted[0] > 0):
        return "the guard exit code contradicts its critical count"
    return ""


def validate_inputs(fleet, ledger):
    """Checks every shape before any guard runs, so a typo never aborts a half-done sweep."""
    if (
        not isinstance(fleet, dict)
        or not isinstance(fleet.get("apps"), list)
        or not fleet["apps"]
    ):
        raise InputError("the fleet file lists no apps")
    names = []
    for i, app in enumerate(fleet["apps"]):
        if not isinstance(app, dict):
            raise InputError(f"apps[{i}] is not an object")
        if not is_text(app.get("name")) or not is_text(app.get("path")):
            raise InputError(f"apps[{i}] needs a non-empty name and path")
        plats = app.get("platforms", [])
        if not isinstance(plats, list) or any(p not in PLATFORMS for p in plats):
            raise InputError(
                f"apps[{i}] platforms must be a list drawn from {', '.join(PLATFORMS)}"
            )
        ready = app.get("readiness")
        if ready is not None and not (
            isinstance(ready, dict) and all(isinstance(v, bool) for v in ready.values())
        ):
            raise InputError(f"apps[{i}] readiness must map each step to true or false")
        feats = app.get("features", [])
        if not isinstance(feats, list) or any(f not in RR.FEATURES for f in feats):
            raise InputError(f"apps[{i}] features must be a list drawn from {', '.join(RR.FEATURES)}")
        regions = app.get("regions", [])
        if not isinstance(regions, list) or not all(is_text(r) for r in regions):
            raise InputError(f"apps[{i}] regions must be a list of country codes")
        if not isinstance(app.get("attestations", {}), dict):
            raise InputError(f"apps[{i}] attestations must map a requirement id to its attestation")
        names.append(app["name"])
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise InputError(f"app names must be unique, repeated: {', '.join(dupes)}")
    if ledger is None:
        return []
    if not isinstance(ledger, dict) or not isinstance(ledger.get("waivers"), list):
        raise InputError("the waiver ledger needs a waivers list")
    for i, w in enumerate(ledger["waivers"]):
        if not isinstance(w, dict):
            raise InputError(f"waivers[{i}] is not an object")
    return ledger["waivers"]


def check_waiver(w, today):
    """Returns (usable, problem). A waiver is honoured only when complete, typed, and in date."""
    for key in WAIVER_TEXT:
        if not is_text(w.get(key)):
            return False, f"missing {key}"
    if w["severity"] not in ("critical", "high", "medium"):
        return False, "severity must be critical, high or medium"
    if "file" in w and not isinstance(w["file"], str):
        return False, "file must be text"
    try:
        expires = dt.date.fromisoformat(w["expires"])
    except ValueError:
        return False, "expires is not a YYYY-MM-DD date"
    if expires < today:
        return False, f"expired on {expires}"
    if (expires - today).days > MAX_WAIVER_DAYS:
        return (
            False,
            f"expiry is more than {MAX_WAIVER_DAYS} days out, review it sooner",
        )
    return True, ""


def attestation_problem(a, today):
    """Returns why an attestation cannot be accepted, or empty when it can."""
    if not isinstance(a, dict):
        return "is not an object"
    for key in ("attested_by", "attested_on", "evidence"):
        if not is_text(a.get(key)):
            return f"is missing {key}"
    try:
        on = dt.date.fromisoformat(a["attested_on"])
    except ValueError:
        return "attested_on is not a YYYY-MM-DD date"
    if on > today:
        return "attested_on is in the future"
    if (today - on).days > 365:
        return "is more than a year old, attest again"
    return ""


def register_actions(app, register, today):
    """Owner actions from every Ruling Register requirement that applies to this app."""
    if register is None:
        return []
    stores = {STORE_OF[p] for p in app.get("platforms", []) if p in STORE_OF}
    rows = RR.due(register, {r.upper() for r in app.get("regions", [])}, stores,
                  set(app.get("features", [])), today)
    attested = app.get("attestations", {})
    actions = []
    for row in rows:
        if not row["source_verified"]:
            actions.append(f"{row['id']} applies but its source is unconfirmed, check it before relying on it")
        elif row["blocks_release"] and row["needs_attestation"]:
            problem = attestation_problem(attested[row["id"]], today) if row["id"] in attested else "is missing"
            if problem:
                actions.append(f"{row['id']} needs your attestation, which {problem}. {row['title']}")
    return actions


def fingerprint(app, finding_id, severity, file):
    return (app, finding_id, severity, file or "")


def sweep_app(app, guard, waivers, today, timeout, register=None):
    name, path = app["name"], expand(app["path"])
    result = {
        "name": name,
        "path": str(path),
        "platforms": app.get("platforms", []),
        "regions": app.get("regions", []),
        "findings": [],
        "waived": [],
        "waiver_problems": [],
        "owner_actions": [],
        "coverage": None,
        "guard_exit": None,
        "note": "",
    }

    # Waivers are judged first. Two records for one occurrence cancel each other out.
    usable, seen = {}, {}
    for w in (w for w in waivers if w.get("app") == name):
        ok, problem = check_waiver(w, today)
        key = fingerprint(
            name, w.get("finding_id"), w.get("severity"), w.get("file", "")
        )
        seen[key] = seen.get(key, 0) + 1
        if ok:
            usable[key] = w
        else:
            result["waiver_problems"].append(f"{w.get('finding_id', '?')}. {problem}")
    for key, count in seen.items():
        if count > 1:
            usable.pop(key, None)
            result["waiver_problems"].append(
                f"{key[1]}. {count} waivers name the same finding, none applied"
            )

    ready = app.get("readiness")
    if not ready:
        result["owner_actions"].append(
            "readiness not tracked, list the account and console steps in the fleet file"
        )
    else:
        result["owner_actions"] += [k for k, v in ready.items() if v is not True]
    result["owner_actions"] += register_actions(app, register, today)

    if not path.is_dir():
        result.update(verdict="NOT_CHECKED", note=f"path {path} is not a folder")
        return result

    code, stdout = run_guard(guard, path, timeout)
    findings, summaries, coverages = parse_report(stdout)
    result["guard_exit"] = code
    problem = integrity_problem(code, findings, summaries, coverages)
    if problem:
        result["findings"] = findings
        result.update(verdict="NOT_CHECKED", note=problem)
        return result

    state, ios, android, web, why = coverages[0]
    covered = {"ios": ios == "1", "android": android == "1", "web": web == "1"}
    result["coverage"] = {"state": state, **covered, "reason": why or ""}

    present = set()
    for f in findings:
        key = fingerprint(name, f["id"], f["severity"], f["file"])
        present.add(key)
        w = usable.get(key)
        if w:
            result["waived"].append(
                {
                    **f,
                    "reason": w["reason"],
                    "evidence": w["evidence"],
                    "reviewed_by": w["reviewed_by"],
                    "expires": w["expires"],
                }
            )
        else:
            result["findings"].append(f)
    for key in sorted(set(usable) - present):
        result["waiver_problems"].append(
            f"{key[1]}. no longer reported at {key[3] or 'app level'}, retire this waiver"
        )

    missing = [p for p in result["platforms"] if not covered[p]]
    blocked = any(f["severity"] == "critical" for f in result["findings"])
    if blocked:
        result["verdict"] = "BLOCKED"
    elif state != "complete":
        result.update(
            verdict="NOT_CHECKED",
            note=f"the scan was incomplete. {why or 'no reason given'}",
        )
    elif missing:
        result.update(
            verdict="NOT_CHECKED",
            note=f"declared {', '.join(missing)} but the guard found no such project",
        )
    elif result["findings"] or result["owner_actions"] or result["waiver_problems"]:
        result["verdict"] = "READY_WITH_ACTIONS"
    else:
        result["verdict"] = "READY"
    if blocked and state != "complete":
        result["note"] = f"also, the scan was incomplete. {why or 'no reason given'}"
    return result


def scanning_export(results):
    """Code-scanning export in SARIF 2.1.0, the one format GitHub code scanning accepts."""
    rules, seen, items, notes = [], set(), [], []

    def add(app, f, suppressed):
        if f["id"] not in seen:
            seen.add(f["id"])
            rules.append(
                {
                    "id": f["id"],
                    "shortDescription": {"text": f["title"]},
                    "help": {"text": f["fix"] or f["title"]},
                }
            )
        uri = f"{app['name']}/{f['file']}" if f["file"] else app["name"]
        item = {
            "ruleId": f["id"],
            "level": LEVEL[f["severity"]],
            "message": {
                "text": f"{app['name']}. {f['title']}. Fix. {f['fix']}".strip()
            },
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}}}],
        }
        if suppressed:
            item["suppressions"] = [
                {
                    "kind": "external",
                    "status": "accepted",
                    "justification": f"{f['reason']} Evidence. {f['evidence']} "
                    f"Reviewed by {f['reviewed_by']}, expires {f['expires']}.",
                }
            ]
        items.append(item)

    for app in results:
        for f in app["findings"]:
            add(app, f, False)
        for f in app["waived"]:
            add(app, f, True)
        if app["verdict"] == "NOT_CHECKED":
            notes.append(
                {
                    "level": "error",
                    "message": {
                        "text": f"{app['name']} was not checked. {app['note']}"
                    },
                }
            )
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "app-store-compliance",
                        "informationUri": "https://github.com/mjmirza/app-store-compliance",
                        "rules": rules,
                    }
                },
                "invocations": [
                    {
                        "executionSuccessful": not notes,
                        "toolExecutionNotifications": notes,
                    }
                ],
                "results": items,
            }
        ],
    }


def print_report(fleet_name, results, verdict):
    print(f"Fleet Sweep. {fleet_name}")
    for r in results:
        counts = {
            s: sum(1 for f in r["findings"] if f["severity"] == s)
            for s in ("critical", "high", "medium")
        }
        print(
            f"\n{r['verdict']:<19} {r['name']}  critical={counts['critical']} high={counts['high']} "
            f"medium={counts['medium']} waived={len(r['waived'])}"
        )
        if r["note"]:
            print(f"  note. {r['note']}")
        for f in r["findings"]:
            print(f"  [{f['severity'].upper()}] {f['id']}  {f['title']}")
            if f["file"]:
                print(f"      file. {f['file']}")
            if f["fix"]:
                print(f"      fix. {f['fix']}")
        for w in r["waived"]:
            print(f"  waived until {w['expires']}. {w['id']} ({w['reviewed_by']})")
        for p in r["waiver_problems"]:
            print(f"  waiver problem. {p}")
        for a in r["owner_actions"]:
            print(f"  owner action. {a}")
    print(f"\nFleet verdict. {verdict}")


def load_json(path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise InputError(f"{label} not found at {path}")
    except json.JSONDecodeError as exc:
        raise InputError(f"{label} at {path} is not valid JSON. {exc}")


def main():
    ap = argparse.ArgumentParser(
        description="Run the guard across every app and return one verdict."
    )
    ap.add_argument("fleet", help="fleet file, see templates/fleet.example.json")
    ap.add_argument(
        "--waivers", help="Waiver Ledger file, see templates/waivers.example.json"
    )
    ap.add_argument(
        "--json", dest="json_out", help="write the full result as JSON here"
    )
    ap.add_argument(
        "--scanning-export",
        dest="scan_out",
        help="write a GitHub code-scanning file here",
    )
    ap.add_argument("--timeout", type=int, default=300, help="seconds allowed per app")
    ap.add_argument("--register", default=str(DEFAULT_REGISTER), help="Ruling Register file")
    ap.add_argument("--no-register", action="store_true", help="skip the Ruling Register")
    args = ap.parse_args()

    try:
        fleet = load_json(args.fleet, "fleet file")
        ledger = load_json(args.waivers, "waiver ledger") if args.waivers else None
        waivers = validate_inputs(fleet, ledger)
        register = None if args.no_register else load_json(args.register, "ruling register")
        if register is not None:
            problems = RR.validate(register, RR.pattern_ids())
            if problems:
                raise InputError(f"the ruling register is invalid. {problems[0]}")
    except InputError as exc:
        print(f"fleet-sweep. {exc}", file=sys.stderr)
        return 1

    # The clock can only be moved in the test suite, so an expired waiver cannot be revived from the CLI.
    fake = os.environ.get("FLEET_SWEEP_TEST_TODAY")
    today = (
        dt.date.fromisoformat(fake)
        if fake and os.environ.get("FLEET_SWEEP_TESTING") == "1"
        else dt.date.today()
    )
    guard = Path(os.environ.get("FLEET_SWEEP_GUARD", DEFAULT_GUARD))

    results = [sweep_app(a, guard, waivers, today, args.timeout, register) for a in fleet["apps"]]
    verdict = max((r["verdict"] for r in results), key=RANK.get)
    print_report(fleet.get("fleet_name", "fleet"), results, verdict)

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(
                {
                    "fleet": fleet.get("fleet_name", "fleet"),
                    "date": str(today),
                    "verdict": verdict,
                    "apps": results,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if args.scan_out:
        Path(args.scan_out).write_text(
            json.dumps(scanning_export(results), indent=2) + "\n", encoding="utf-8"
        )
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
