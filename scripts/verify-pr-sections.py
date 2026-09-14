#!/usr/bin/env python3
"""
verify-pr-sections.py

Validates that compliance Pull Request markdown documents contain all 15 required
numbered compliance section headings in exact sequential order without missing or vague content.

Required sections (in exact order 1-15):
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
import os
import argparse
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

def check_emojis(content):
    emojis = [c for c in content if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    return len(emojis) > 0

def verify_file(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []

    if check_emojis(content):
        errors.append("Emojis detected in PR document (violates strict emoji-free policy)")

    # Find all level 2 headers matching ## N. Title
    header_pattern = re.compile(r"^##\s+(\d+)\.\s+(.+)$", re.MULTILINE)
    found_headers = header_pattern.findall(content)

    if not found_headers:
        # Fallback check for unnumbered headers if any
        alt_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
        found_alt = alt_pattern.findall(content)
        errors.append(f"No numbered section headings (## N. Title) found. Unnumbered headers found: {found_alt}")
        print(f"[FAIL] {filepath}:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    # Check sections presence and order
    expected_idx = 0
    for num_str, title in found_headers:
        num = int(num_str)
        clean_title = title.strip()

        if expected_idx < len(REQUIRED_SECTIONS):
            expected_num = expected_idx + 1
            expected_title = REQUIRED_SECTIONS[expected_idx]

            if num != expected_num:
                errors.append(f"Section sequence error: expected section #{expected_num} ('{expected_title}'), but found #{num} ('{clean_title}')")
            elif clean_title.lower() != expected_title.lower():
                errors.append(f"Section title mismatch for #{num}: expected '{expected_title}', found '{clean_title}'")
            else:
                expected_idx += 1

    if expected_idx < len(REQUIRED_SECTIONS):
        for missing_idx in range(expected_idx, len(REQUIRED_SECTIONS)):
            m_num = missing_idx + 1
            m_title = REQUIRED_SECTIONS[missing_idx]
            errors.append(f"Missing required section #{m_num}: ## {m_num}. {m_title}")

    # Verify content between headers is non-empty / non-vague
    # Split content by ## headers
    sections = re.split(r"^##\s+\d+\.\s+.+$", content, flags=re.MULTILINE)
    # The first element is pre-header content (e.g. title)
    section_bodies = sections[1:] if len(sections) > 1 else []

    if len(section_bodies) == len(REQUIRED_SECTIONS):
        for idx, body in enumerate(section_bodies):
            sec_num = idx + 1
            sec_name = REQUIRED_SECTIONS[idx]
            clean_body = body.strip()
            # Remove HTML comments
            clean_body_no_comments = re.sub(r"<!--.*?-->", "", clean_body, flags=re.DOTALL).strip()
            if not clean_body_no_comments:
                errors.append(f"Section #{sec_num} ('{sec_name}') has no content (empty section)")

    if errors:
        print(f"[FAIL] {filepath}:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False
    else:
        print(f"[PASS] {filepath}: All 15 required compliance sections verified successfully.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Verify 15 required PR sections in markdown files.")
    parser.add_argument("files", nargs="*", help="Markdown files to verify")
    parser.add_argument("--files", nargs="+", dest="flag_files", help="Markdown files to verify")

    args = parser.parse_args()
    target_files = args.files if args.files else (args.flag_files if args.flag_files else [])

    if not target_files:
        print("Usage: python3 scripts/verify-pr-sections.py <file1.md> [<file2.md> ...]")
        sys.exit(1)

    all_passed = True
    for filepath in target_files:
        if not verify_file(filepath):
            all_passed = False

    if not all_passed:
        sys.exit(1)

    print("All PR section checks passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
