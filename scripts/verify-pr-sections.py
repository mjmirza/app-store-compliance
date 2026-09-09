#!/usr/bin/env python3
"""Verify PR Sections Utility: Validates that a markdown file or PR draft text
contains all 15 required numbered compliance sections in exact sequential order."""

import sys
import os
import re

REQUIRED_SECTIONS = [
    "Summary",
    "Background",
    "Regulatory change",
    "Official citations",
    "Affected files",
    "Risk assessment",
    "Migration steps",
    "Backward compatibility",
    "Implementation checklist",
    "Testing checklist",
    "Documentation checklist",
    "Compliance impact",
    "Breaking changes",
    "Review checklist",
    "Approver recommendations",
]


def verify_content(content):
    missing = []
    out_of_order = []
    last_found_idx = -1

    for idx, sec_name in enumerate(REQUIRED_SECTIONS, 1):
        pattern = re.compile(rf"^##\s+{idx}\.\s+{re.escape(sec_name)}", re.MULTILINE | re.IGNORECASE)
        match = pattern.search(content)
        if not match:
            missing.append(f"## {idx}. {sec_name}")
        else:
            found_idx = match.start()
            if found_idx < last_found_idx:
                out_of_order.append(f"## {idx}. {sec_name}")
            last_found_idx = found_idx

    return missing, out_of_order


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/verify-pr-sections.py <filepath_or_markdown_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    missing, out_of_order = verify_content(content)

    if missing or out_of_order:
        print(f"FAILED: Compliance PR validation failed for {filepath}")
        if missing:
            print("Missing required section(s):")
            for m in missing:
                print(f"  - {m}")
        if out_of_order:
            print("Out-of-order section(s):")
            for o in out_of_order:
                print(f"  - {o}")
        sys.exit(1)

    print(f"PASS: {filepath} contains all 15 required numbered compliance sections in sequential order.")
    sys.exit(0)


if __name__ == "__main__":
    main()
