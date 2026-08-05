#!/usr/bin/env python3
"""Timeline Compiler Utility.
Loads regulatory deadlines from data/regulatory-deadlines.json, sorts them
chronologically, evaluates active/overdue and approaching deadlines within
90 days relative to today's UTC date, prints warnings to stderr, and writes
a clean, emoji-free markdown timeline document to docs/REGULATORY-TIMELINE.md.
This script automatically regenerates and compiles the timeline of every regulatory deadline."""

import os
import sys
import json
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
OUTPUT_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


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


def format_sections(raw_sections):
    if isinstance(raw_sections, list):
        return ", ".join(raw_sections)
    return str(raw_sections)


def main():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines to compile.", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)
    parsed_items = []

    for d in deadlines:
        try:
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except Exception as e:
            print(f"Error parsing date for {d.get('id', 'Unknown')}: {e}", file=sys.stderr)
            continue

        remaining_days = (mand_dt - now).days
        parsed_items.append({
            "id": d.get("id"),
            "jurisdiction": d.get("jurisdiction", "Unknown"),
            "law": d.get("law", "Unknown"),
            "requirement": d.get("requirement", "Unknown"),
            "effective_date": d.get("effective_date", ""),
            "grace_period": d.get("grace_period", ""),
            "mandatory_date": d.get("mandatory_date", ""),
            "enforcement_date": d.get("enforcement_date", ""),
            "affected_repository_sections": format_sections(d.get("affected_repository_sections", "")),
            "priority": d.get("priority", "medium"),
            "remaining_days": remaining_days,
            "mandatory_datetime": mand_dt
        })

    # Sort chronologically by mandatory date
    parsed_items.sort(key=lambda x: x["mandatory_datetime"])

    # Categorize warnings
    overdue_warnings = []
    approaching_warnings = []

    for item in parsed_items:
        if item["remaining_days"] < 0:
            overdue_warnings.append(item)
        elif item["remaining_days"] <= 90:
            approaching_warnings.append(item)

    # Print warnings to stderr
    if overdue_warnings:
        print("WARNING: Active / Overdue Regulatory Compliance Deadlines Detected:", file=sys.stderr)
        for item in overdue_warnings:
            overdue_days = abs(item["remaining_days"])
            print(f"  [{item['priority'].upper()}] {item['law']} ({item['jurisdiction']}) - OVERDUE by {overdue_days} days. Req: {item['requirement']}", file=sys.stderr)

    if approaching_warnings:
        print("WARNING: Approaching Regulatory Compliance Deadlines Detected (Within 90 Days):", file=sys.stderr)
        for item in approaching_warnings:
            print(f"  [{item['priority'].upper()}] {item['law']} ({item['jurisdiction']}) - Due in {item['remaining_days']} days. Req: {item['requirement']}", file=sys.stderr)

    # Generate markdown document
    md_lines = []
    md_lines.append("# Global Regulatory Compliance Timeline")
    md_lines.append("")
    md_lines.append("This document compiles every registered global regulatory deadline tracking regional, national, and platform requirements.")
    md_lines.append(f"Last compiled: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    md_lines.append("")

    # Embed warning section at the top
    md_lines.append("## Active and Approaching Compliance Warnings")
    md_lines.append("")

    if not overdue_warnings and not approaching_warnings:
        md_lines.append("No active or approaching deadlines within a rolling 90-day window.")
        md_lines.append("")
    else:
        if overdue_warnings:
            md_lines.append("### Active / Overdue Deadlines (Action Required)")
            md_lines.append("")
            md_lines.append("| Priority | Jurisdiction | Law | Requirement | Passed Date | Overdue Days | Affected Sections |")
            md_lines.append("|---|---|---|---|---|---|---|")
            for item in overdue_warnings:
                overdue_days = abs(item["remaining_days"])
                md_lines.append(
                    f"| {item['priority'].upper()} | {item['jurisdiction']} | {item['law']} | {item['requirement']} | {item['mandatory_date']} | {overdue_days} days | {item['affected_repository_sections']} |"
                )
            md_lines.append("")

        if approaching_warnings:
            md_lines.append("### Approaching Deadlines (Within 90 Days)")
            md_lines.append("")
            md_lines.append("| Priority | Jurisdiction | Law | Requirement | Due Date | Days Remaining | Affected Sections |")
            md_lines.append("|---|---|---|---|---|---|---|")
            for item in approaching_warnings:
                md_lines.append(
                    f"| {item['priority'].upper()} | {item['jurisdiction']} | {item['law']} | {item['requirement']} | {item['mandatory_date']} | {item['remaining_days']} days | {item['affected_repository_sections']} |"
                )
            md_lines.append("")

    # Full chronological timeline
    md_lines.append("## Full Chronological Timeline")
    md_lines.append("")
    md_lines.append("| Mandatory Date | Law | Requirement | Jurisdiction | Grace Period | Enforcement Date | Priority | Affected Sections |")
    md_lines.append("|---|---|---|---|---|---|---|---|")
    for item in parsed_items:
        md_lines.append(
            f"| {item['mandatory_date']} | {item['law']} | {item['requirement']} | {item['jurisdiction']} | {item['grace_period']} | {item['enforcement_date']} | {item['priority'].upper()} | {item['affected_repository_sections']} |"
        )
    md_lines.append("")

    # Detailed Records Section
    md_lines.append("## Detailed Compliance Records")
    md_lines.append("")
    for item in parsed_items:
        md_lines.append(f"### ID: {item['id']}")
        md_lines.append("")
        md_lines.append(f"- **Jurisdiction:** {item['jurisdiction']}")
        md_lines.append(f"- **Law:** {item['law']}")
        md_lines.append(f"- **Requirement:** {item['requirement']}")
        md_lines.append(f"- **Effective Date:** {item['effective_date']}")
        md_lines.append(f"- **Grace Period:** {item['grace_period']}")
        md_lines.append(f"- **Mandatory Date:** {item['mandatory_date']}")
        md_lines.append(f"- **Enforcement Date:** {item['enforcement_date']}")
        md_lines.append(f"- **Priority:** {item['priority'].upper()}")
        md_lines.append(f"- **Affected Repository Sections:** {item['affected_repository_sections']}")
        md_lines.append("")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    content_to_write = "\n".join(md_lines)

    # Sanity check: programmatically guarantee no emoji or high-unicode character is written to the markdown timeline
    for char in content_to_write:
        if ord(char) >= 0x1F600:
            print(f"CRITICAL ERROR: Emoji or high-unicode character '{char}' (code {ord(char)}) detected in timeline content!", file=sys.stderr)
            return 1

    with open(OUTPUT_FILE, "w") as f:
        f.write(content_to_write)

    print(f"Compiled {len(parsed_items)} deadlines to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
