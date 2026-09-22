#!/usr/bin/env python3
"""
verify-pr-sections.py

Validates that compliance Pull Request markdown documents (such as PR templates or PR drafts)
contain all 15 required numbered compliance section headings in exact sequential order:
  ## 1. Summary
  ## 2. Background
  ## 3. Regulatory change
  ## 4. Official citations
  ## 5. Affected files
  ## 6. Risk assessment
  ## 7. Migration steps
  ## 8. Backward compatibility
  ## 9. Implementation checklist
  ## 10. Testing checklist
  ## 11. Documentation checklist
  ## 12. Compliance impact
  ## 13. Breaking changes
  ## 14. Review checklist
  ## 15. Approver recommendations

Also verifies that no section is completely empty and that no emojis or graphical emoticons are present.
"""

import sys
import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. Summary",
    "## 2. Background",
    "## 3. Regulatory change",
    "## 4. Official citations",
    "## 5. Affected files",
    "## 6. Risk assessment",
    "## 7. Migration steps",
    "## 8. Backward compatibility",
    "## 9. Implementation checklist",
    "## 10. Testing checklist",
    "## 11. Documentation checklist",
    "## 12. Compliance impact",
    "## 13. Breaking changes",
    "## 14. Review checklist",
    "## 15. Approver recommendations",
]

# Regex for detecting common emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Misc Symbols & Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport & Map
    r"\U0001F1E0-\U0001F1FF"  # Flags
    r"\U00002702-\U000027B0"  # Dingbats
    r"\U0001F900-\U0001F9FF"  # Supplemental Symbols
    r"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    r"\U00002600-\U000026FF]" # Misc Symbols
)


def verify_file(filepath: Path) -> bool:
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return False

    content = filepath.read_text(encoding="utf-8")

    # Check for emojis
    if EMOJI_PATTERN.search(content):
        print(f"ERROR: Emojis detected in {filepath}", file=sys.stderr)
        return False

    # Extract all lines matching section headers
    lines = content.splitlines()
    found_headers = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            found_headers.append(stripped)

    # Validate that all required sections exist in order
    idx = 0
    for req in REQUIRED_SECTIONS:
        while idx < len(found_headers) and found_headers[idx] != req:
            idx += 1
        if idx >= len(found_headers):
            print(f"ERROR: Missing required section heading '{req}' in {filepath}", file=sys.stderr)
            return False
        idx += 1

    # Validate non-empty section bodies
    for i, req in enumerate(REQUIRED_SECTIONS):
        next_req = REQUIRED_SECTIONS[i + 1] if i + 1 < len(REQUIRED_SECTIONS) else None
        pos_req = content.find(req)
        if pos_req == -1:
            print(f"ERROR: Section heading '{req}' not found in content.", file=sys.stderr)
            return False

        if next_req:
            pos_next = content.find(next_req, pos_req)
            section_body = content[pos_req + len(req):pos_next].strip()
        else:
            section_body = content[pos_req + len(req):].strip()

        if not section_body:
            print(f"ERROR: Empty section body for '{req}' in {filepath}", file=sys.stderr)
            return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/verify-pr-sections.py <file1.md> [file2.md ...]")
        sys.exit(1)

    all_valid = True
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not verify_file(p):
            all_valid = False

    if not all_valid:
        sys.exit(1)

    print("PASS: All PR markdown files contain all 15 required compliance sections in order, non-empty, and emoji-free.")
    sys.exit(0)


if __name__ == "__main__":
    main()
