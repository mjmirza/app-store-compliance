#!/usr/bin/env python3
"""Timeline compiler utility.
Loads data/regulatory-deadlines.json, sorts deadlines chronologically,
and compiles them into a clean, emoji-free compliance timeline markdown document
at docs/REGULATORY-TIMELINE.md.
Evaluates active/overdue and approaching deadlines within 90 days relative to
today's UTC date, outputs automatic console warnings on stderr, and embeds
an active and approaching compliance warnings section at the top of the timeline.
"""

import os
import sys
import json
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
OUTPUT_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


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


def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def main():
    deadlines = load_deadlines()
    if not deadlines:
        sys.stderr.write("No deadlines loaded.\n")
        return 1

    now = datetime.now(timezone.utc)

    # Process and evaluate deadlines
    processed = []
    for d in deadlines:
        mand_date_str = d.get("mandatory_date")
        mand_dt = parse_date(mand_date_str)
        if not mand_dt:
            # Skip or handle invalid date gracefully
            continue

        remaining_days = (mand_dt - now).days

        raw_sections = d.get("affected_repository_sections", "")
        if isinstance(raw_sections, list):
            sections_str = ", ".join(raw_sections)
        else:
            sections_str = str(raw_sections)

        processed.append({
            "id": d.get("id", "Unknown"),
            "jurisdiction": d.get("jurisdiction", "Unknown"),
            "law": d.get("law", "Unknown"),
            "requirement": d.get("requirement", "Unknown"),
            "effective_date": d.get("effective_date", "Unknown"),
            "grace_period": d.get("grace_period", "Unknown"),
            "mandatory_date": mand_date_str,
            "enforcement_date": d.get("enforcement_date", "Unknown"),
            "sections": sections_str,
            "priority": d.get("priority", "medium"),
            "remaining_days": remaining_days,
            "mandatory_datetime": mand_dt
        })

    # Sort deadlines chronologically by mandatory date
    processed.sort(key=lambda x: x["mandatory_datetime"])

    # Split into passed, upcoming (<= 90 days), and far future (> 90 days)
    passed_deadlines = []
    upcoming_deadlines = []
    for p in processed:
        if p["remaining_days"] < 0:
            passed_deadlines.append(p)
        elif p["remaining_days"] <= 90:
            upcoming_deadlines.append(p)

    # Output console warnings on sys.stderr
    if passed_deadlines or upcoming_deadlines:
        sys.stderr.write("== Regulatory Compliance Deadline Status ==\n\n")

    if passed_deadlines:
        sys.stderr.write("ACTIVE / PASSED COMPLIANCE DEADLINES (Action Required):\n")
        sys.stderr.write("-" * 80 + "\n")
        for item in passed_deadlines:
            overdue = abs(item["remaining_days"])
            sys.stderr.write(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}\n")
            sys.stderr.write(f"  Law:         {item['law']}\n")
            sys.stderr.write(f"  Requirement: {item['requirement']}\n")
            sys.stderr.write(f"  Passed Date: {item['mandatory_date']} ({overdue} days overdue)\n")
            sys.stderr.write(f"  Impacted:    {item['sections']}\n\n")

    if upcoming_deadlines:
        sys.stderr.write("UPCOMING COMPLIANCE DEADLINES (Action Required Soon):\n")
        sys.stderr.write("-" * 80 + "\n")
        for item in upcoming_deadlines:
            sys.stderr.write(f"[{item['priority'].upper()}] Jurisdiction: {item['jurisdiction']}\n")
            sys.stderr.write(f"  Law:         {item['law']}\n")
            sys.stderr.write(f"  Requirement: {item['requirement']}\n")
            sys.stderr.write(f"  Due Date:    {item['mandatory_date']} (in {item['remaining_days']} days)\n")
            sys.stderr.write(f"  Impacted:    {item['sections']}\n\n")

    if not passed_deadlines and not upcoming_deadlines:
        sys.stderr.write("All registered regulatory deadlines are in the future (> 90 days). No immediate warnings.\n")

    # Build markdown contents
    md = []
    md.append("# Regulatory Compliance Timeline")
    md.append("")
    md.append("This document tracks every regulatory compliance deadline chronologically, compiling upcoming deadlines and active/passed requirements from the App Store Compliance Playbook.")
    md.append("")
    md.append("## Active and Approaching Compliance Warnings")
    md.append("")

    if not passed_deadlines and not upcoming_deadlines:
        md.append("All registered regulatory deadlines are currently in the future (greater than 90 days). No immediate warnings are active.")
        md.append("")
    else:
        if passed_deadlines:
            md.append("### Active / Overdue Deadlines (Immediate Action Required)")
            md.append("")
            md.append("| Priority | Jurisdiction | Law | Requirement | Passed Date | Overdue Status | Affected Sections |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for item in passed_deadlines:
                overdue = abs(item["remaining_days"])
                md.append(f"| {item['priority'].upper()} | {item['jurisdiction']} | {item['law']} | {item['requirement']} | {item['mandatory_date']} | {overdue} days overdue | {item['sections']} |")
            md.append("")

        if upcoming_deadlines:
            md.append("### Approaching Deadlines (Within 90 Days)")
            md.append("")
            md.append("| Priority | Jurisdiction | Law | Requirement | Due Date | Time Remaining | Affected Sections |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for item in upcoming_deadlines:
                md.append(f"| {item['priority'].upper()} | {item['jurisdiction']} | {item['law']} | {item['requirement']} | {item['mandatory_date']} | in {item['remaining_days']} days | {item['sections']} |")
            md.append("")

    md.append("## Complete Chronological Timeline Summary")
    md.append("")
    md.append("| Mandatory Date | Jurisdiction | Law | Requirement | Grace Period | Priority |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for item in processed:
        md.append(f"| {item['mandatory_date']} | {item['jurisdiction']} | {item['law']} | {item['requirement']} | {item['grace_period']} | {item['priority'].upper()} |")
    md.append("")

    md.append("## Detailed Compliance Breakdown")
    md.append("")
    for item in processed:
        md.append(f"### [{item['mandatory_date']}] {item['id']}: {item['law']}")
        md.append("")
        md.append(f"- **Jurisdiction**: {item['jurisdiction']}")
        md.append(f"- **Law**: {item['law']}")
        md.append(f"- **Requirement**: {item['requirement']}")
        md.append(f"- **Effective Date**: {item['effective_date']}")
        md.append(f"- **Grace Period**: {item['grace_period']}")
        md.append(f"- **Mandatory Date**: {item['mandatory_date']}")
        md.append(f"- **Enforcement Date**: {item['enforcement_date']}")
        md.append(f"- **Affected Repository Sections**: {item['sections']}")
        md.append(f"- **Priority**: {item['priority']}")
        md.append("")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Write emoji-free markdown
    content = "\n".join(md)
    # Double-check for emojis
    for char in content:
        if ord(char) >= 0x1F600:
            sys.stderr.write("Internal Warning: Generated content contains high Unicode characters / potential emojis!\n")
            break

    with open(OUTPUT_FILE, "w") as f:
        f.write(content)

    print(f"Regulatory timeline successfully generated at {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
