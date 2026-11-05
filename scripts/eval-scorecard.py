#!/usr/bin/env python3
"""Scores Fleet Sweep, the Waiver Ledger and the Ruling Register against evals/gold-cases.json."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GOLD = REPO / "evals" / "gold-cases.json"
FEATURES = ("fleet", "waiver", "register")
VERDICTS = {"READY": 0, "READY_WITH_ACTIONS": 3, "NOT_CHECKED": 1, "BLOCKED": 2}
SAFE = {"READY", "READY_WITH_ACTIONS"}


def check_gold(gold):
    problems = []
    for i, c in enumerate(gold.get("cases", [])):
        if c.get("feature") not in FEATURES:
            problems.append(f"case {i} has unknown feature {c.get('feature')}")
        if c.get("expect") not in VERDICTS:
            problems.append(f"case {i} has unknown verdict {c.get('expect')}")
    if not gold.get("cases"):
        problems.append("no gold cases")
    return problems


def run_case(case, tmp, eval_date):
    """Returns a list of reasons the case failed, empty when it passed."""
    app_dir = tmp / "app"
    app_dir.mkdir()
    (app_dir / "report.txt").write_text(case["report"])
    (app_dir / "exit.txt").write_text(str(case["guard_exit"]))
    (tmp / "guard.sh").write_text('#!/usr/bin/env bash\ncat "$1/report.txt"\nexit "$(cat "$1/exit.txt")"\n')
    app = {k: v for k, v in case["app"].items() if v is not None}
    app.update(name="app", path=str(app_dir))
    (tmp / "fleet.json").write_text(json.dumps({"apps": [app]}))
    args = [sys.executable, str(REPO / "scripts" / "fleet-sweep.py"), str(tmp / "fleet.json"),
            "--json", str(tmp / "result.json")]
    if not case.get("register", False):
        args.append("--no-register")
    if case.get("waivers") is not None:
        (tmp / "waivers.json").write_text(json.dumps({"waivers": case["waivers"]}))
        args += ["--waivers", str(tmp / "waivers.json")]
    env = {**os.environ, "FLEET_SWEEP_GUARD": str(tmp / "guard.sh"), "FLEET_SWEEP_TESTING": "1",
           "FLEET_SWEEP_TEST_TODAY": eval_date}
    done = subprocess.run(args, env=env, capture_output=True, text=True, timeout=60)
    try:
        result = json.loads((tmp / "result.json").read_text())
    except (OSError, ValueError):
        return "NO_RESULT", [f"no result, exit {done.returncode}. {done.stderr.strip()[:200]}"]
    apps = result.get("apps", [])
    if len(apps) != 1:
        return "NO_RESULT", [f"expected one app result, got {len(apps)}"]
    got = apps[0].get("verdict")
    why = []
    if got != case["expect"]:
        why.append(f"expected {case['expect']}, got {got}")
    if result.get("verdict") != got:
        why.append(f"fleet verdict {result.get('verdict')} disagrees with the app verdict {got}")
    if done.returncode != VERDICTS.get(got, -1):
        why.append(f"exit code {done.returncode} does not match {got}")
    text = json.dumps(apps[0])
    why += [f"does not mention {m}" for m in case.get("must_mention", []) if m not in text]
    why += [f"mentions {m}, which it must not" for m in case.get("must_not_mention", []) if m in text]
    return got, why


def main():
    gold = json.loads(GOLD.read_text())
    problems = check_gold(gold)
    if problems:
        for p in problems:
            print(f"  GOLD ERROR. {p}")
        return 1
    rows = []
    for case in gold["cases"]:
        with tempfile.TemporaryDirectory() as d:
            got, why = run_case(case, Path(d), gold["eval_date"])
        rows.append((case, got, why))

    print(f"{'feature':<9} {'cases':>5} {'correct':>8} {'false pass':>11} {'false block':>12}")
    for feature in FEATURES:
        mine = [r for r in rows if r[0]["feature"] == feature]
        correct = sum(1 for r in mine if not r[2])
        false_pass = sum(1 for c, got, _ in mine if c["expect"] not in SAFE and got in SAFE)
        false_block = sum(1 for c, got, _ in mine if c["expect"] in SAFE and got not in SAFE and got != "NO_RESULT")
        print(f"{feature:<9} {len(mine):>5} {correct:>8} {false_pass:>11} {false_block:>12}")
    failed = [r for r in rows if r[2]]
    for case, _, why in failed:
        print(f"  MISS {case['feature']}. {case['name']}. {'; '.join(why)}")
    total_fp = sum(1 for c, got, _ in rows if c["expect"] not in SAFE and got in SAFE)
    accuracy = 100 * (len(rows) - len(failed)) / len(rows)
    print(f"\nScorecard. {len(rows)} cases, accuracy {accuracy:.1f}%, false passes {total_fp}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
