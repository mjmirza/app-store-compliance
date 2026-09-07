#!/usr/bin/env python3
"""
verify-pr-sections.py

Verifies that a given compliance Pull Request markdown document contains all 15
required numbered compliance section headings in exact order:
  1. Summary
  2. Background
  3. Regulatory change
  4. Official citations
  5. Affected files
  6. Risk assessment
  7. Migration steps
  8. Backward compatibility
  9. Implementation checklist
 10. Testing checklist
 11. Documentation checklist
 12. Compliance impact
 13. Breaking changes
 14. Review checklist
 15. Approver recommendations
"""

import sys
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


def check_pr_sections(content):
    missing = []
    for idx, name in enumerate(REQUIRED_SECTIONS, 1):
        pattern = rf"^##\s+{idx}\.\s+{re.escape(name)}"
        if not re.search(pattern, content, re.MULTILINE):
            missing.append(f"## {idx}. {name}")
    return missing


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()

    missing = check_pr_sections(content)
    if missing:
        print(f"FAILED: PR draft is missing {len(missing)} section(s):")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print("PASS: PR draft contains all 15 required numbered compliance sections.")
        sys.exit(0)


if __name__ == "__main__":
    main()
