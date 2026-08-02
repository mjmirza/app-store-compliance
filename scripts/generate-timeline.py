#!/usr/bin/env python3
"""Timeline compiler utility.
Loads data/regulatory-deadlines.json, sorts deadlines chronologically, and
compiles them into a clean, emoji-free compliance timeline markdown document
at docs/REGULATORY-TIMELINE.md.
Evaluates active/overdue and approaching deadlines within 90 days relative
to today's date, outputs automatic console warnings on stderr, and embeds
an active and approaching compliance warnings section at the top of the
generated timeline.
"""

import os
import sys
import json
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
TIMELINE_OUT_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


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


def format_sections(sections):
    if isinstance(sections, list):
        return ", ".join(sections)
    return str(sections)


def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines found to compile.", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)

    # Chronologically sort by mandatory_date ascending
    sorted_deadlines = []
    for d in deadlines:
        try:
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            sorted_deadlines.append((mand_dt, d))
        except Exception as e:
            print(f"Error parsing mandatory_date for ID {d.get('id')}: {e}", file=sys.stderr)
            # Fallback sort date in the far future if unparseable
            sorted_deadlines.append((datetime.max.replace(tzinfo=timezone.utc), d))

    sorted_deadlines.sort(key=lambda x: x[0])

    passed_warnings = []
    approaching_warnings = []

    for mand_dt, d in sorted_deadlines:
        if mand_dt == datetime.max.replace(tzinfo=timezone.utc):
            continue
        remaining_days = (mand_dt - now).days
        item = {
            "id": d.get("id", "UNKNOWN"),
            "jurisdiction": d.get("jurisdiction", "Unknown"),
            "law": d.get("law", "Unknown"),
            "requirement": d.get("requirement", "Unknown"),
            "mandatory_date": d.get("mandatory_date"),
            "priority": d.get("priority", "medium"),
            "sections": format_sections(d.get("affected_repository_sections", "")),
            "remaining_days": remaining_days,
            "effective_date": d.get("effective_date"),
            "grace_period": d.get("grace_period"),
            "enforcement_date": d.get("enforcement_date"),
        }
        if remaining_days < 0:
            passed_warnings.append(item)
        elif remaining_days <= 90:
            approaching_warnings.append(item)

    # 1. Output warnings to stderr if there are any active or approaching deadlines
    if passed_warnings:
        print("WARNING: ACTIVE / OVERDUE COMPLIANCE DEADLINES DETECTED", file=sys.stderr)
        for item in passed_warnings:
            overdue = abs(item["remaining_days"])
            print(f"[{item['priority'].upper()}] {item['jurisdiction']} - {item['law']}: Overdue by {overdue} days (Mandatory: {item['mandatory_date']})", file=sys.stderr)

    if approaching_warnings:
        print("WARNING: APPROACHING COMPLIANCE DEADLINES DETECTED (WITHIN 90 DAYS)", file=sys.stderr)
        for item in approaching_warnings:
            print(f"[{item['priority'].upper()}] {item['jurisdiction']} - {item['law']}: Due in {item['remaining_days']} days (Mandatory: {item['mandatory_date']})", file=sys.stderr)

    # 2. Build the REGULATORY-TIMELINE.md document (completely emoji-free)
    md_lines = []
    md_lines.append("# Regulatory Compliance Timeline")
    md_lines.append("")
    md_lines.append("This document maintains a chronological timeline of global regional, national, and platform regulatory deadlines.")
    md_lines.append(f"Last compiled: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    md_lines.append("")

    # Embed Warnings Section at the top
    md_lines.append("## Active and Approaching Compliance Warnings")
    md_lines.append("")
    if not passed_warnings and not approaching_warnings:
        md_lines.append("No active or approaching deadlines within the 90-day warning window.")
        md_lines.append("")
    else:
        if passed_warnings:
            md_lines.append("### Active / Overdue Deadlines")
            md_lines.append("")
            md_lines.append("| Priority | Jurisdiction | Law / Requirement | Mandatory Date | Status |")
            md_lines.append("|---|---|---|---|---|")
            for item in passed_warnings:
                overdue = abs(item["remaining_days"])
                md_lines.append(f"| {item['priority'].upper()} | {item['jurisdiction']} | **{item['law']}**: {item['requirement']} | {item['mandatory_date']} | Overdue by {overdue} days |")
            md_lines.append("")

        if approaching_warnings:
            md_lines.append("### Approaching Deadlines (Within 90 Days)")
            md_lines.append("")
            md_lines.append("| Priority | Jurisdiction | Law / Requirement | Mandatory Date | Status |")
            md_lines.append("|---|---|---|---|---|")
            for item in approaching_warnings:
                md_lines.append(f"| {item['priority'].upper()} | {item['jurisdiction']} | **{item['law']}**: {item['requirement']} | {item['mandatory_date']} | In {item['remaining_days']} days |")
            md_lines.append("")

    # Full Chronological Timeline
    md_lines.append("## Chronological Regulatory Timeline")
    md_lines.append("")
    md_lines.append("Below is the complete list of all registered regulatory and platform deadlines, sorted chronologically by mandatory compliance date.")
    md_lines.append("")

    for mand_dt, d in sorted_deadlines:
        sections_str = format_sections(d.get("affected_repository_sections", ""))
        md_lines.append(f"### {d.get('mandatory_date')} - {d.get('jurisdiction')}: {d.get('law')}")
        md_lines.append("")
        md_lines.append(f"- **ID:** {d.get('id')}")
        md_lines.append(f"- **Law:** {d.get('law')}")
        md_lines.append(f"- **Requirement:** {d.get('requirement')}")
        md_lines.append(f"- **Effective Date:** {d.get('effective_date')}")
        md_lines.append(f"- **Grace Period:** {d.get('grace_period')}")
        md_lines.append(f"- **Mandatory Date:** {d.get('mandatory_date')}")
        md_lines.append(f"- **Enforcement Date:** {d.get('enforcement_date')}")
        md_lines.append(f"- **Affected Repository Sections:** {sections_str}")
        md_lines.append(f"- **Priority:** {d.get('priority', 'medium').upper()}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    try:
        # Write clean markdown
        os.makedirs(os.path.dirname(TIMELINE_OUT_FILE), exist_ok=True)
        with open(TIMELINE_OUT_FILE, "w") as f:
            f.write("\n".join(md_lines))
        print(f"Timeline successfully compiled and written to {TIMELINE_OUT_FILE}")
    except Exception as e:
        print(f"Error writing timeline markdown: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
