#!/usr/bin/env python3
"""Verifies that PR markdown files or templates contain all 15 required numbered
compliance section headings in exact sequential order.
Exit 0 on success, exit 1 on missing/misordered sections."""

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


def verify_file(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    errors = []
    last_pos = -1

    for idx, sec_name in enumerate(REQUIRED_SECTIONS, 1):
        # Match pattern like "## 1. Summary" or "## 15. Approver recommendations"
        pattern = re.compile(rf"^##\s+{idx}\.\s+{re.escape(sec_name)}\b", re.MULTILINE | re.IGNORECASE)
        match = pattern.search(content)

        if not match:
            # Fallback check for unnumbered or slightly formatted section heading
            fallback_pattern = re.compile(rf"^##\s+(?:\d+\.\s+)?{re.escape(sec_name)}\b", re.MULTILINE | re.IGNORECASE)
            fallback_match = fallback_pattern.search(content)

            if not fallback_match:
                errors.append(f"Missing required section: '## {idx}. {sec_name}'")
            else:
                pos = fallback_match.start()
                if pos < last_pos:
                    errors.append(f"Section out of order: '## {idx}. {sec_name}' appears before previous sections")
                last_pos = pos
        else:
            pos = match.start()
            if pos < last_pos:
                errors.append(f"Section out of order: '## {idx}. {sec_name}' appears before previous sections")
            last_pos = pos

    if errors:
        print(f"[FAIL] {filepath} failed compliance PR section verification:")
        for err in errors:
            print(f"  - {err}")
        return False

    print(f"[PASS] {filepath} contains all 15 required compliance PR sections in exact sequential order.")
    return True


def main():
    if len(sys.argv) > 1:
        files_to_check = sys.argv[1:]
    else:
        # Default to .github/PULL_REQUEST_TEMPLATE.md
        default_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".github", "PULL_REQUEST_TEMPLATE.md")
        files_to_check = [default_file]

    all_passed = True
    for f in files_to_check:
        if not verify_file(f):
            all_passed = False

    if not all_passed:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
