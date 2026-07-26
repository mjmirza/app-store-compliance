#!/usr/bin/env python3
"""
Checks global regional, national, and store platform regulatory deadlines.
Warns developers about approaching or already active (enforced) deadlines.
"""

import json
import os
import sys
from datetime import datetime, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")

def load_deadlines():
    try:
        with open(DEADLINES_FILE, "r") as f:
            return json.load(f).get("deadlines", [])
    except Exception as e:
        print(f"Error loading deadlines database: {e}", file=sys.stderr)
        return []

def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No regulatory deadlines found to evaluate.", file=sys.stderr)
        return 0

    today = date.today()
    print("== App Store Compliance: Regulatory Deadlines Check ==")
    print(f"Evaluation Date: {today.isoformat()}\n")

    approaching = []
    enforced = []

    for d in deadlines:
        mdate_str = d.get("mandatory_date")
        if not mdate_str:
            continue

        try:
            mdate = datetime.strptime(mdate_str, "%Y-%m-%d").date()
        except ValueError:
            if len(mdate_str) == 4 and mdate_str.isdigit():
                mdate = date(int(mdate_str), 1, 1)
            else:
                continue

        days_left = (mdate - today).days

        if days_left < 0:
            enforced.append((d, days_left))
        else:
            approaching.append((d, days_left))

    # Sort approaching deadlines by closest first
    approaching.sort(key=lambda x: x[1])

    # Sort enforced deadlines by priority (critical first) then most recent
    enforced.sort(key=lambda x: (
        0 if x[0].get("priority") == "critical" else 1,
        -x[1]
    ))

    # Print Approaching Deadlines
    if approaching:
        print(f"WARNING: APPROACHING REGULATORY DEADLINES (Active soon):")
        print("=" * 80)
        for d, days in approaching:
            priority_str = d.get("priority", "medium").upper()
            time_str = f"IN {days} DAYS" if days > 0 else "TODAY"
            print(f"  [{priority_str}] {d.get('law')} ({d.get('jurisdiction')})")
            print(f"    Requirement : {d.get('requirement')}")
            print(f"    Mandatory   : {d.get('mandatory_date')} ({time_str})")
            print(f"    Grace Period: {d.get('grace_period')}")
            print(f"    Affected Sec: {d.get('affected_repository_sections')}")
            print("-" * 80)
        print()
    else:
        print("SUCCESS: No new regulatory deadlines approaching within the next 90 days.\n")

    # Print Enforced/Active Checklist Summary
    if enforced:
        print(f"ACTIVE AND ENFORCED REGULATORY REQUIREMENTS:")
        print("=" * 80)
        print(f"  {'Jurisdiction':<28} | {'Law/Requirement':<34} | {'Priority':<8}")
        print("-" * 80)
        for d, days in enforced:
            priority_str = d.get("priority", "medium").upper()
            law_short = d.get('law')
            if len(law_short) > 34:
                law_short = law_short[:31] + "..."
            jur_short = d.get('jurisdiction')
            if len(jur_short) > 28:
                jur_short = jur_short[:25] + "..."
            print(f"  {jur_short:<28} | {law_short:<34} | {priority_str:<8}")
        print("=" * 80)
        print("  Note: Run a full compliance audit to ensure your app satisfies these active laws.")
        print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
