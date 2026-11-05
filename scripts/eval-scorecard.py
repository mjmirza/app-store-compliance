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
SAFE = {"READY", "READY_WITH_ACTIONS"}


def run_case(case, tmp):
    app_dir = tmp / "app"
    app_dir.mkdir()
    (app_dir / "report.txt").write_text(case["report"])
    (app_dir / "exit.txt").write_text(str(case["guard_exit"]))
    app = {k: v for k, v in case["app"].items() if v is not None}
    app.update(name="app", path=str(app_dir))
    (tmp / "fleet.json").write_text(json.dumps({"apps": [app]}))
    args = [sys.executable, str(REPO / "scripts" / "fleet-sweep.py"), str(tmp / "fleet.json"),
            "--json", str(tmp / "result.json")]
    if case.get("waivers") is not None:
        (tmp / "waivers.json").write_text(json.dumps({"waivers": case["waivers"]}))
        args += ["--waivers", str(tmp / "waivers.json")]
    env = {**os.environ, "FLEET_SWEEP_GUARD": str(tmp / "guard.sh"), "FLEET_SWEEP_TESTING": "1",
           "FLEET_SWEEP_TEST_TODAY": json.loads(GOLD.read_text())["eval_date"]}
    subprocess.run(args, env=env, capture_output=True, text=True, timeout=60)
    try:
        return json.loads((tmp / "result.json").read_text())["apps"][0]["verdict"]
    except (OSError, ValueError, KeyError, IndexError):
        return "NO_RESULT"


def main():
    gold = json.loads(GOLD.read_text())
    rows = []
    for case in gold["cases"]:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            (tmp / "guard.sh").write_text('#!/usr/bin/env bash\ncat "$1/report.txt"\nexit "$(cat "$1/exit.txt")"\n')
            got = run_case(case, tmp)
        rows.append((case["feature"], case["name"], case["expect"], got))

    print(f"{'feature':<9} {'cases':>5} {'correct':>8} {'false pass':>11} {'false block':>12}")
    total_fp = total_bad = 0
    for feature in ("fleet", "waiver", "register"):
        mine = [r for r in rows if r[0] == feature]
        correct = sum(1 for r in mine if r[2] == r[3])
        false_pass = sum(1 for r in mine if r[2] not in SAFE and r[3] in SAFE)
        false_block = sum(1 for r in mine if r[2] in SAFE and r[3] not in SAFE)
        total_fp += false_pass
        total_bad += len(mine) - correct
        print(f"{feature:<9} {len(mine):>5} {correct:>8} {false_pass:>11} {false_block:>12}")
    for feature, name, expect, got in rows:
        if expect != got:
            print(f"  MISS {feature}. {name}. expected {expect}, got {got}")
    accuracy = 100 * (len(rows) - total_bad) / len(rows)
    print(f"\nScorecard. {len(rows)} cases, accuracy {accuracy:.1f}%, false passes {total_fp}")
    return 1 if total_fp or total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
