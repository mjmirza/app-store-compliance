#!/usr/bin/env python3
"""
Generates docs/REGULATORY-TIMELINE.md from data/regulatory-deadlines.json.
Sorts deadlines chronologically by mandatory_date and formats them cleanly
with all 9 required fields for each. Displays dynamic warnings for active and
approaching deadlines (within 90 days). Strictly emoji-free.
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
        print(f"Error: Deadlines file not found at {DEADLINES_FILE}", file=sys.stderr)
        return []
    with open(DEADLINES_FILE, "r") as f:
        data = json.load(f)
        return data.get("deadlines", [])

def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines loaded.")
        return 1

    now = datetime.now(timezone.utc)
    passed_deadlines = []
    upcoming_deadlines = []

    # Sort chronologically by mandatory_date, then by jurisdiction, then by id
    def get_sort_key(d):
        m_date = d.get("mandatory_date", "9999-12-31")
        # Handle cases where mandatory_date is 'none' or empty
        if not m_date or m_date.lower() == "none":
            m_date = "9999-12-31"
        return (m_date, d.get("jurisdiction", ""), d.get("id", ""))

    sorted_deadlines = sorted(deadlines, key=get_sort_key)

    for d in sorted_deadlines:
        m_date_str = d.get("mandatory_date")
        if not m_date_str or m_date_str.lower() == "none":
            continue
        try:
            mand_dt = datetime.strptime(m_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception as e:
            print(f"Error parsing date {m_date_str} for {d.get('id')}: {e}", file=sys.stderr)
            continue

        remaining_days = (mand_dt - now).days
        item_summary = {
            "id": d.get("id"),
            "jurisdiction": d.get("jurisdiction"),
            "law": d.get("law"),
            "mandatory_date": m_date_str,
            "priority": d.get("priority", "medium"),
            "remaining_days": remaining_days,
            "requirement": d.get("requirement")
        }

        if remaining_days < 0:
            passed_deadlines.append(item_summary)
        elif remaining_days <= 90:
            upcoming_deadlines.append(item_summary)

    # Output warnings to stdout/stderr to warn when a deadline approaches
    if passed_deadlines or upcoming_deadlines:
        print("=== COMPLIANCE DEADLINE WARNINGS ===", file=sys.stderr)
        if passed_deadlines:
            print("\nACTIVE / PASSED COMPLIANCE DEADLINES:", file=sys.stderr)
            for item in passed_deadlines:
                overdue = abs(item["remaining_days"])
                print(f"  [{item['priority'].upper()}] {item['id']} ({item['law']}) - Overdue by {overdue} days (Mandatory Date: {item['mandatory_date']})", file=sys.stderr)
        if upcoming_deadlines:
            print("\nUPCOMING COMPLIANCE DEADLINES (Within 90 Days):", file=sys.stderr)
            for item in upcoming_deadlines:
                print(f"  [{item['priority'].upper()}] {item['id']} ({item['law']}) - Approaching in {item['remaining_days']} days (Mandatory Date: {item['mandatory_date']})", file=sys.stderr)
        print("====================================", file=sys.stderr)

    # Build the markdown content
    lines = [
        "# Global Regulatory Compliance Timeline",
        "",
        "This document maintains a chronological timeline of global regulatory and platform compliance deadlines compiled from the App Store Compliance Playbook records.",
        ""
    ]

    # Embed warning section in the markdown
    lines.append("## Active and Approaching Compliance Warnings")
    lines.append("")
    if passed_deadlines:
        lines.append("### Overdue / Active Deadlines")
        lines.append("")
        lines.append("| Priority | ID | Jurisdiction | Law | Overdue Days |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for item in passed_deadlines:
            lines.append(f"| {item['priority'].upper()} | `{item['id']}` | {item['jurisdiction']} | {item['law']} | {abs(item['remaining_days'])} days overdue |")
        lines.append("")

    if upcoming_deadlines:
        lines.append("### Upcoming Deadlines (Within 90 Days)")
        lines.append("")
        lines.append("| Priority | ID | Jurisdiction | Law | Remaining Days |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for item in upcoming_deadlines:
            lines.append(f"| {item['priority'].upper()} | `{item['id']}` | {item['jurisdiction']} | {item['law']} | in {item['remaining_days']} days |")
        lines.append("")

    if not passed_deadlines and not upcoming_deadlines:
        lines.append("All registered regulatory deadlines are in the future (> 90 days). No immediate warnings.")
        lines.append("")

    lines.append("## Timeline Summary")
    lines.append("")
    lines.append("| Mandatory Date | Jurisdiction | Law | Priority |")
    lines.append("| :--- | :--- | :--- | :--- |")

    for d in sorted_deadlines:
        lines.append(f"| {d.get('mandatory_date')} | {d.get('jurisdiction')} | {d.get('law')} | {d.get('priority').upper()} |")

    lines.append("")
    lines.append("## Detailed Timeline Records")
    lines.append("")

    for d in sorted_deadlines:
        lines.append(f"### {d.get('id')} - {d.get('law')}")
        lines.append("")
        lines.append(f"- **Jurisdiction**: {d.get('jurisdiction')}")
        lines.append(f"- **Law**: {d.get('law')}")
        lines.append(f"- **Requirement**: {d.get('requirement')}")
        lines.append(f"- **Effective Date**: {d.get('effective_date')}")
        lines.append(f"- **Grace Period**: {d.get('grace_period')}")
        lines.append(f"- **Mandatory Date**: {d.get('mandatory_date')}")
        lines.append(f"- **Enforcement Date**: {d.get('enforcement_date')}")

        raw_sections = d.get("affected_repository_sections", "")
        if isinstance(raw_sections, list):
            sections_str = ", ".join(raw_sections)
        else:
            sections_str = str(raw_sections)
        lines.append(f"- **Affected Repository Sections**: {sections_str}")
        lines.append(f"- **Priority**: {d.get('priority').upper()}")
        lines.append("")

    # Ensure NO emoji is present in the output
    content = "\n".join(lines)
    for char in content:
        if ord(char) >= 0x1F600:
            print(f"Error: Found emoji or high unicode character in output: {char}", file=sys.stderr)
            return 1

    with open(TIMELINE_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated timeline with {len(sorted_deadlines)} records at {TIMELINE_FILE}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
