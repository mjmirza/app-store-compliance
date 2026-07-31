#!/usr/bin/env python3
"""Generates docs/REGULATORY-TIMELINE.md from data/regulatory-deadlines.json.
Sorts deadlines chronologically and evaluates active/overdue or approaching deadlines.
Outputs console warnings to stderr and embeds a warnings section at the top."""

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
TIMELINE_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


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
        print("No deadlines loaded.", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)

    parsed_deadlines = []
    for d in deadlines:
        try:
            mand_dt = datetime.strptime(d["mandatory_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception as e:
            print(f"Error parsing mandatory_date for {d.get('id')}: {e}", file=sys.stderr)
            continue

        remaining_days = (mand_dt - now).days
        parsed_deadlines.append((mand_dt, remaining_days, d))

    # Sort deadlines chronologically by mandatory_date
    parsed_deadlines.sort(key=lambda x: x[0])

    passed_warnings = []
    approaching_warnings = []

    for mand_dt, remaining_days, d in parsed_deadlines:
        jurisdiction = d.get("jurisdiction", "Unknown")
        law = d.get("law", "Unknown")
        requirement = d.get("requirement", "Unknown")
        mand_date_str = d.get("mandatory_date", "Unknown")
        priority = d.get("priority", "medium")
        sections = format_sections(d.get("affected_repository_sections", ""))

        if remaining_days < 0:
            overdue_days = abs(remaining_days)
            warn_msg = f"WARNING: OVERDUE [{priority.upper()}] {law} ({jurisdiction}) - Mandatory date {mand_date_str} passed {overdue_days} days ago!"
            print(warn_msg, file=sys.stderr)
            passed_warnings.append((warn_msg, overdue_days, d))
        elif remaining_days <= 90:
            warn_msg = f"WARNING: APPROACHING [{priority.upper()}] {law} ({jurisdiction}) - Mandatory date {mand_date_str} is in {remaining_days} days!"
            print(warn_msg, file=sys.stderr)
            approaching_warnings.append((warn_msg, remaining_days, d))

    # Generate Markdown timeline
    markdown_content = []
    markdown_content.append("# Regulatory Compliance Timeline")
    markdown_content.append("")
    markdown_content.append("This document tracks regional, national, and platform regulatory deadlines and highlights active/overdue or upcoming compliance obligations.")
    markdown_content.append("")
    markdown_content.append("## Active and Approaching Compliance Warnings")
    markdown_content.append("")

    if not passed_warnings and not approaching_warnings:
        markdown_content.append("No active or approaching compliance warnings.")
        markdown_content.append("")
    else:
        if passed_warnings:
            markdown_content.append("### Active / Overdue Deadlines")
            markdown_content.append("")
            for msg, overdue, d in passed_warnings:
                markdown_content.append(f"- **[{d.get('priority').upper()}] {d.get('law')}** ({d.get('jurisdiction')}): Overdue by {overdue} days (Mandatory Date: {d.get('mandatory_date')}).")
            markdown_content.append("")

        if approaching_warnings:
            markdown_content.append("### Approaching Deadlines (Within 90 Days)")
            markdown_content.append("")
            for msg, remaining, d in approaching_warnings:
                markdown_content.append(f"- **[{d.get('priority').upper()}] {d.get('law')}** ({d.get('jurisdiction')}): Due in {remaining} days (Mandatory Date: {d.get('mandatory_date')}).")
            markdown_content.append("")

    markdown_content.append("## Chronological Compliance Timeline")
    markdown_content.append("")
    markdown_content.append("The table below details all registered regulatory deadlines sorted chronologically by mandatory compliance date.")
    markdown_content.append("")

    # Construct timeline markdown table
    headers = [
        "Jurisdiction",
        "Law",
        "Requirement",
        "Effective Date",
        "Grace Period",
        "Mandatory Date",
        "Enforcement Date",
        "Affected Repository Sections",
        "Priority"
    ]

    markdown_content.append("| " + " | ".join(headers) + " |")
    markdown_content.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for mand_dt, remaining_days, d in parsed_deadlines:
        row = [
            d.get("jurisdiction", "").replace("|", "\\|"),
            d.get("law", "").replace("|", "\\|"),
            d.get("requirement", "").replace("|", "\\|"),
            d.get("effective_date", "").replace("|", "\\|"),
            d.get("grace_period", "").replace("|", "\\|"),
            d.get("mandatory_date", "").replace("|", "\\|"),
            d.get("enforcement_date", "").replace("|", "\\|"),
            format_sections(d.get("affected_repository_sections", "")).replace("|", "\\|"),
            d.get("priority", "").upper()
        ]
        markdown_content.append("| " + " | ".join(row) + " |")

    markdown_content.append("")

    # Ensure target directory exists
    os.makedirs(os.path.dirname(TIMELINE_FILE), exist_ok=True)
    with open(TIMELINE_FILE, "w") as f:
        f.write("\n".join(markdown_content) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
