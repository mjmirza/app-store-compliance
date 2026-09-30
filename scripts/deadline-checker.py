#!/usr/bin/env python3
"""Checks data/regulatory-deadlines.json against today's UTC date.
Prints active/passed deadlines and upcoming ones within 90 days.
This script implements the automatic warning system for regulatory deadlines."""

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.environ.get(
    "DEADLINES_FILE", os.path.join(ROOT, "data", "regulatory-deadlines.json")
)


def load_deadlines():
    if not os.path.exists(DEADLINES_FILE):
        print(
            f"Error: Deadlines database not found at {DEADLINES_FILE}", file=sys.stderr
        )
        return []
    try:
        with open(DEADLINES_FILE, "r") as f:
            data = json.load(f)
            return data.get("deadlines", [])
    except Exception as e:
        print(f"Error loading deadlines: {e}", file=sys.stderr)
        return []


def print_brief(passed, upcoming, absorbed):
    """One line per deadline, for the guard report. The full blocks stay the default."""
    print("== Regulatory Compliance Deadline Status ==")
    for item in passed:
        print(
            f"[{item['priority'].upper()}] OVERDUE {abs(item['remaining_days'])} days. "
            f"{item['jurisdiction']}. {item['law']} (mandatory {item['mandatory_date']})"
        )
    for item in sorted(upcoming, key=lambda x: x["remaining_days"]):
        days = item["remaining_days"]
        when = "due today" if days == 0 else f"in {days} day" + ("" if days == 1 else "s")
        print(
            f"[{item['priority'].upper()}] {when}. "
            f"{item['jurisdiction']}. {item['law']} (mandatory {item['mandatory_date']})"
        )
    if not passed and not upcoming:
        print("No deadline is overdue or due within 90 days.")
    if absorbed:
        print(f"{len(absorbed)} passed deadline(s) already carried by the playbook, not listed.")
    print(f"Full detail. python3 {os.path.abspath(__file__)}")
    return 0


def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines loaded.")
        return 0

    now = datetime.now(timezone.utc)
    warnings_found = False

    passed_deadlines = []
    upcoming_deadlines = []
    absorbed_deadlines = []

    for d in deadlines:
        try:
            # validated for well-formed-ness; only mandatory_date drives the window below
            _ = datetime.strptime(d["effective_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            _ = datetime.strptime(d["enforcement_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except Exception as e:
            print(
                f"Error parsing dates for {d.get('law', 'Unknown')}: {e}",
                file=sys.stderr,
            )
            continue

        # Check against the mandatory date or enforcement date (whichever is earlier/relevant, let's use mandatory_date)
        # We calculate remaining days based on the mandatory date
        # whole calendar days in UTC, so a deadline is due on its own date and not a day early
        remaining_days = (mand_dt.date() - now.date()).days

        raw_sections = d.get("affected_repository_sections", "")
        if isinstance(raw_sections, list):
            sections_str = ", ".join(raw_sections)
        else:
            sections_str = str(raw_sections)

        item = {
            "jurisdiction": d.get("jurisdiction", "Unknown"),
            "law": d.get("law", "Unknown"),
            "requirement": d.get("requirement", "Unknown"),
            "effective_date": d.get("effective_date", "Unknown"),
            "grace_period": d.get("grace_period", "Unknown"),
            "mandatory_date": d.get("mandatory_date", "Unknown"),
            "enforcement_date": d.get("enforcement_date", "Unknown"),
            "priority": d.get("priority", "Medium"),
            "sections": sections_str,
            "remaining_days": remaining_days,
            "absorbed_into": d.get("absorbed_into", ""),
        }

        if remaining_days < 0 and item["absorbed_into"]:
            absorbed_deadlines.append(item)
        elif remaining_days < 0:
            passed_deadlines.append(item)
        elif remaining_days <= 90:
            upcoming_deadlines.append(item)

    if "--brief" in sys.argv[1:]:
        return print_brief(passed_deadlines, upcoming_deadlines, absorbed_deadlines)

    if passed_deadlines or upcoming_deadlines:
        print("== Regulatory Compliance Deadline Status ==\n")

    if passed_deadlines:
        warnings_found = True
        print("ACTIVE / PASSED COMPLIANCE DEADLINES (Action Required):")
        print("-" * 80)
        for item in passed_deadlines:
            overdue = abs(item["remaining_days"])
            print(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}")
            print(f"  Law:                          {item['law']}")
            print(f"  Requirement:                  {item['requirement']}")
            print(f"  Effective date:               {item['effective_date']}")
            print(f"  Grace period:                 {item['grace_period']}")
            print(f"  Mandatory date:               {item['mandatory_date']} ({overdue} days overdue)")
            print(f"  Enforcement date:             {item['enforcement_date']}")
            print(f"  Affected repository sections: {item['sections']}")
            print(f"  Priority:                     {item['priority'].upper()}")
            print()

    if upcoming_deadlines:
        warnings_found = True
        print("UPCOMING COMPLIANCE DEADLINES (Action Required Soon):")
        print("-" * 80)
        # Sort upcoming by closest date first
        upcoming_deadlines.sort(key=lambda x: x["remaining_days"])
        for item in upcoming_deadlines:
            print(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}")
            print(f"  Law:                          {item['law']}")
            print(f"  Requirement:                  {item['requirement']}")
            print(f"  Effective date:               {item['effective_date']}")
            print(f"  Grace period:                 {item['grace_period']}")
            print(f"  Mandatory date:               {item['mandatory_date']} (in {item['remaining_days']} days)")
            print(f"  Enforcement date:             {item['enforcement_date']}")
            print(f"  Affected repository sections: {item['sections']}")
            print(f"  Priority:                     {item['priority'].upper()}")
            print()

    if absorbed_deadlines:
        print("PASSED DEADLINES ABSORBED INTO THE PLAYBOOK (no action needed):")
        print("-" * 80)
        for item in absorbed_deadlines:
            print(
                f"[{item['priority'].upper()}] {item['law']} "
                f"(mandatory {item['mandatory_date']}) absorbed into {item['absorbed_into']}"
            )
        print()

    if not warnings_found:
        print(
            "All registered regulatory deadlines are in the future (> 90 days). No immediate warnings."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
