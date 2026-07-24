#!/usr/bin/env python3
"""
Regulatory Deadline Checker Utility.
Parses data/regulatory-deadlines.json and alerts developers of approaching or
currently active/enforced regulatory deadlines.
"""
import os
import sys
import argparse
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")

def load_deadlines():
    import json
    if not os.path.exists(DEADLINES_FILE):
        print(f"[ERROR] Deadlines file not found at {DEADLINES_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(DEADLINES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def check_deadlines(days_threshold=60):
    deadlines = load_deadlines()
    today = datetime.now(timezone.utc).date()

    active_deadlines = []
    approaching_deadlines = []

    for item in deadlines:
        mandatory_date_str = item.get("mandatory_date")
        if not mandatory_date_str:
            continue

        try:
            m_date = datetime.strptime(mandatory_date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"[ERROR] Invalid date format for law '{item.get('law')}': {mandatory_date_str}", file=sys.stderr)
            continue

        days_until = (m_date - today).days

        # Classify the deadline
        if days_until < 0:
            active_deadlines.append((item, days_until))
        elif 0 <= days_until <= days_threshold:
            approaching_deadlines.append((item, days_until))

    # Print Report
    print("================================================================================")
    print("                       REGULATORY DEADLINE MONITORING SYSTEM                    ")
    print("================================================================================")
    print(f"Current Date (UTC): {today.isoformat()}")
    print(f"Checking for upcoming deadlines within {days_threshold} days.")
    print("--------------------------------------------------------------------------------")

    if active_deadlines:
        print("\n[ACTIVE / ENFORCED DEADLINES] - These are currently in effect and mandatory:")
        print("--------------------------------------------------------------------------------")
        # Sort by priority and then by how long ago they passed
        active_sorted = sorted(active_deadlines, key=lambda x: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x[0]["priority"].lower(), 4),
            x[1]
        ))
        for item, days_passed in active_sorted:
            print(f"JURISDICTION: {item['jurisdiction']}")
            print(f"LAW:          {item['law']} ({item['priority'].upper()} priority)")
            print(f"REQUIREMENT:  {item['requirement']}")
            print(f"MANDATORY AS OF: {item['mandatory_date']} ({abs(days_passed)} days ago)")
            if item.get("grace_period") and item["grace_period"] != "none":
                print(f"GRACE PERIOD: {item['grace_period']}")
            print(f"AFFECTED REPO SECTIONS:")
            for section in item.get("affected_repository_sections", []):
                print(f"  - {section}")
            print("-" * 80)

    if approaching_deadlines:
        print("\n[APPROACHING DEADLINES] - Action required soon:")
        print("--------------------------------------------------------------------------------")
        # Sort by urgency (days_until ascending)
        approaching_sorted = sorted(approaching_deadlines, key=lambda x: (
            x[1],
            {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x[0]["priority"].lower(), 4)
        ))
        for item, days_until in approaching_sorted:
            print(f"JURISDICTION: {item['jurisdiction']}")
            print(f"LAW:          {item['law']} ({item['priority'].upper()} priority)")
            print(f"REQUIREMENT:  {item['requirement']}")
            print(f"MANDATORY DATE: {item['mandatory_date']} (in {days_until} days)")
            if item.get("grace_period") and item["grace_period"] != "none":
                print(f"GRACE PERIOD: {item['grace_period']}")
            print(f"AFFECTED REPO SECTIONS:")
            for section in item.get("affected_repository_sections", []):
                print(f"  - {section}")
            print("-" * 80)

    if not active_deadlines and not approaching_deadlines:
        print("\nNo currently active or approaching deadlines found in the specified window.")
        print("-" * 80)

    print("================================================================================")

def main():
    parser = argparse.ArgumentParser(description="Audit and warn of approaching regulatory deadlines.")
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="The window of days to look ahead for approaching deadlines (default: 60)."
    )
    args = parser.parse_args()
    check_deadlines(args.days)

if __name__ == "__main__":
    main()
