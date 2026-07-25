#!/usr/bin/env python3
"""
Regulatory Deadline Checker Utility.
Loads the machine-readable database of deadlines from data/regulatory-deadlines.json,
calculates days remaining to each deadline using timezone-aware UTC datetimes,
and prints clear, structured warnings for:
  - Active/passed deadlines
  - Upcoming deadlines (occurring within 90 days)
Adheres strictly to the zero-emoji guideline.
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")

def load_deadlines():
    if not os.path.exists(DEADLINES_FILE):
        print(f"Error: Deadlines database not found at {DEADLINES_FILE}", file=sys.stderr)
        return []
    try:
        with open(DEADLINES_FILE, "r") as f:
            data = json.load(f)
            return data.get("deadlines", [])
    except Exception as e:
        print(f"Error loading deadlines: {e}", file=sys.stderr)
        return []

def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines loaded.")
        return 0

    now = datetime.now(timezone.utc)
    warnings_found = False

    passed_deadlines = []
    upcoming_deadlines = []

    for d in deadlines:
        try:
            # Parse dates as UTC timezone-aware datetimes
            eff_dt = datetime.strptime(d["effective_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            enf_dt = datetime.strptime(d["enforcement_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception as e:
            print(f"Error parsing dates for {d.get('law', 'Unknown')}: {e}", file=sys.stderr)
            continue

        # Check against the mandatory date or enforcement date (whichever is earlier/relevant, let's use mandatory_date)
        # We calculate remaining days based on the mandatory date
        remaining_days = (mand_dt - now).days

        item = {
            "jurisdiction": d.get("jurisdiction", "Unknown"),
            "law": d.get("law", "Unknown"),
            "requirement": d.get("requirement", "Unknown"),
            "mandatory_date": d.get("mandatory_date"),
            "priority": d.get("priority", "Medium"),
            "sections": ", ".join(d.get("affected_repository_sections", [])),
            "remaining_days": remaining_days
        }

        if remaining_days < 0:
            passed_deadlines.append(item)
        elif remaining_days <= 90:
            upcoming_deadlines.append(item)

    if passed_deadlines or upcoming_deadlines:
        print("== Regulatory Compliance Deadline Status ==\n")

    if passed_deadlines:
        warnings_found = True
        print("ACTIVE / PASSED COMPLIANCE DEADLINES (Action Required):")
        print("-" * 80)
        for item in passed_deadlines:
            overdue = abs(item["remaining_days"])
            print(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}")
            print(f"  Law:         {item['law']}")
            print(f"  Requirement: {item['requirement']}")
            print(f"  Passed Date: {item['mandatory_date']} ({overdue} days overdue)")
            print(f"  Impacted:    {item['sections']}")
            print()

    if upcoming_deadlines:
        warnings_found = True
        print("UPCOMING COMPLIANCE DEADLINES (Action Required Soon):")
        print("-" * 80)
        # Sort upcoming by closest date first
        upcoming_deadlines.sort(key=lambda x: x["remaining_days"])
        for item in upcoming_deadlines:
            print(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}")
            print(f"  Law:         {item['law']}")
            print(f"  Requirement: {item['requirement']}")
            print(f"  Due Date:    {item['mandatory_date']} (in {item['remaining_days']} days)")
            print(f"  Impacted:    {item['sections']}")
            print()

    if not warnings_found:
        print("All registered regulatory deadlines are in the future (> 90 days). No immediate warnings.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
