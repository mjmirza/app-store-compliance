#!/usr/bin/env python3
"""Timeline Compiler Utility.
Loads data/regulatory-deadlines.json, sorts deadlines chronologically,
and compiles them into a clean, emoji-free compliance timeline markdown document
at docs/REGULATORY-TIMELINE.md.
"""

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
TIMELINE_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


def load_deadlines():
    if not os.path.exists(DEADLINES_FILE):
        sys.stderr.write(f"Error: Deadlines database not found at {DEADLINES_FILE}\n")
        return []
    try:
        with open(DEADLINES_FILE, "r") as f:
            data = json.load(f)
            return data.get("deadlines", [])
    except Exception as e:
        sys.stderr.write(f"Error loading deadlines: {e}\n")
        return []


def main():
    deadlines = load_deadlines()
    if not deadlines:
        sys.stderr.write("No deadlines loaded.\n")
        return 0

    now = datetime.now(timezone.utc)

    parsed_deadlines = []
    for d in deadlines:
        try:
            eff_dt = datetime.strptime(d["effective_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            enf_dt = datetime.strptime(d["enforcement_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except Exception as e:
            sys.stderr.write(
                f"Error parsing dates for {d.get('id', 'Unknown')}: {e}\n"
            )
            continue

        remaining_days = (mand_dt - now).days

        raw_sections = d.get("affected_repository_sections", "")
        if isinstance(raw_sections, list):
            sections_str = ", ".join(raw_sections)
        else:
            sections_str = str(raw_sections)

        parsed_deadlines.append(
            {
                "id": d.get("id"),
                "jurisdiction": d.get("jurisdiction"),
                "law": d.get("law"),
                "requirement": d.get("requirement"),
                "effective_date": d.get("effective_date"),
                "grace_period": d.get("grace_period"),
                "mandatory_date": d.get("mandatory_date"),
                "enforcement_date": d.get("enforcement_date"),
                "affected_repository_sections": sections_str,
                "priority": d.get("priority"),
                "remaining_days": remaining_days,
                "mand_dt": mand_dt,
            }
        )

    # Sort deadlines chronologically by mandatory_date
    parsed_deadlines.sort(key=lambda x: x["mand_dt"])

    # Evaluate active/overdue and approaching deadlines
    passed_deadlines = []
    upcoming_deadlines = []
    for d in parsed_deadlines:
        if d["remaining_days"] < 0:
            passed_deadlines.append(d)
        elif d["remaining_days"] <= 90:
            upcoming_deadlines.append(d)

    # Print automatic console warnings on stderr
    if passed_deadlines or upcoming_deadlines:
        sys.stderr.write("== Regulatory Compliance Deadline Warnings ==\n\n")
        if passed_deadlines:
            sys.stderr.write("ACTIVE / PASSED COMPLIANCE DEADLINES (Action Required):\n")
            sys.stderr.write("-" * 80 + "\n")
            for d in passed_deadlines:
                overdue_days = abs(d["remaining_days"])
                sys.stderr.write(f"[{d['priority'].upper()}] Jurisdiction: {d['jurisdiction']}\n")
                sys.stderr.write(f"  Law:         {d['law']}\n")
                sys.stderr.write(f"  Requirement: {d['requirement']}\n")
                sys.stderr.write(f"  Passed Date: {d['mandatory_date']} ({overdue_days} days overdue)\n")
                sys.stderr.write(f"  Impacted:    {d['affected_repository_sections']}\n\n")
        if upcoming_deadlines:
            sys.stderr.write("UPCOMING COMPLIANCE DEADLINES (Action Required Soon):\n")
            sys.stderr.write("-" * 80 + "\n")
            for d in upcoming_deadlines:
                sys.stderr.write(f"[{d['priority'].upper()}] Jurisdiction: {d['jurisdiction']}\n")
                sys.stderr.write(f"  Law:         {d['law']}\n")
                sys.stderr.write(f"  Requirement: {d['requirement']}\n")
                sys.stderr.write(f"  Due Date:    {d['mandatory_date']} (in {d['remaining_days']} days)\n")
                sys.stderr.write(f"  Impacted:    {d['affected_repository_sections']}\n\n")

    # Generate docs/REGULATORY-TIMELINE.md
    os.makedirs(os.path.dirname(TIMELINE_FILE), exist_ok=True)
    with open(TIMELINE_FILE, "w") as f:
        f.write("# Regulatory Compliance Timeline\n\n")
        f.write("This document maintains a timeline of every regulatory deadline.\n\n")

        # Warnings Section
        f.write("## Active and Approaching Compliance Warnings\n\n")
        if passed_deadlines or upcoming_deadlines:
            if passed_deadlines:
                f.write("### Active / Passed Compliance Deadlines (Action Required)\n\n")
                for d in passed_deadlines:
                    overdue_days = abs(d["remaining_days"])
                    f.write(f"- **[{d['priority'].upper()}] {d['jurisdiction']}: {d['law']}**\n")
                    f.write(f"  - Requirement: {d['requirement']}\n")
                    f.write(f"  - Passed Date: {d['mandatory_date']} ({overdue_days} days overdue)\n")
                    f.write(f"  - Impacted Sections: `{d['affected_repository_sections']}`\n\n")
            if upcoming_deadlines:
                f.write("### Upcoming Compliance Deadlines (Action Required Soon)\n\n")
                for d in upcoming_deadlines:
                    f.write(f"- **[{d['priority'].upper()}] {d['jurisdiction']}: {d['law']}**\n")
                    f.write(f"  - Requirement: {d['requirement']}\n")
                    f.write(f"  - Due Date: {d['mandatory_date']} (in {d['remaining_days']} days)\n")
                    f.write(f"  - Impacted Sections: `{d['affected_repository_sections']}`\n\n")
        else:
            f.write("There are no active or approaching deadlines within 90 days.\n\n")

        # Chronological list of every regulatory deadline
        f.write("## Complete Chronological Timeline\n\n")
        f.write("Below is the complete chronological timeline of all registered regulatory deadlines.\n\n")

        for d in parsed_deadlines:
            f.write(f"### {d['mandatory_date']} - {d['jurisdiction']}: {d['law']}\n\n")
            f.write(f"- **Law:** {d['law']}\n")
            f.write(f"- **Requirement:** {d['requirement']}\n")
            f.write(f"- **Effective date:** {d['effective_date']}\n")
            f.write(f"- **Grace period:** {d['grace_period']}\n")
            f.write(f"- **Mandatory date:** {d['mandatory_date']}\n")
            f.write(f"- **Enforcement date:** {d['enforcement_date']}\n")
            f.write(f"- **Affected repository sections:** `{d['affected_repository_sections']}`\n")
            f.write(f"- **Priority:** {d['priority']}\n\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
