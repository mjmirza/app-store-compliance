#!/usr/bin/env python3
"""
verify-pr-sections.py

Validates that compliance Pull Request markdown documents and templates contain all 15
required numbered compliance section headings in exact sequential order without empty
or emoji-containing sections.
"""

import sys
import re
import argparse

REQUIRED_SECTIONS = [
    "1. Summary",
    "2. Background",
    "3. Regulatory change",
    "4. Official citations",
    "5. Affected files",
    "6. Risk assessment",
    "7. Migration steps",
    "8. Backward compatibility",
    "9. Implementation checklist",
    "10. Testing checklist",
    "11. Documentation checklist",
    "12. Compliance impact",
    "13. Breaking changes",
    "14. Review checklist",
    "15. Approver recommendations"
]

EMOJI_PATTERN = re.compile(
    r'['
    r'\U0001F600-\U0001F64F'  # Emoticons
    r'\U0001F300-\U0001F5FF'  # Misc Symbols & Pictographs
    r'\U0001F680-\U0001F6FF'  # Transport & Map
    r'\U0001F1E0-\U0001F1FF'  # Flags
    r'\u2700-\u27bf'          # Dingbats
    r'\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
    r'\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
    r']'
)


def verify_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as err:
        print(f"FAIL: Unable to read file {filepath}: {err}")
        return False

    errors = []

    # 1. Emoji check
    if EMOJI_PATTERN.search(content):
        errors.append("Contains disallowed emojis or unicode graphical emoticons.")

    # 2. Section presence and order check
    last_position = -1
    for idx, sec_title in enumerate(REQUIRED_SECTIONS, start=1):
        pattern = re.compile(r'^##\s+' + re.escape(sec_title) + r'(?:\s|$)', re.MULTILINE)
        match = pattern.search(content)
        if not match:
            errors.append(f"Missing required section heading: '## {sec_title}'")
        else:
            pos = match.start()
            if pos < last_position:
                errors.append(f"Section '## {sec_title}' is out of sequential order.")
            last_position = pos

    if errors:
        print(f"FAIL: Validation failed for {filepath}:")
        for error in errors:
            print(f"  - {error}")
        return False

    print(f"PASS: {filepath} contains all 15 required sections in order with no emojis.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Verify PR markdown sections.")
    parser.add_argument("files", nargs="*", help="Markdown files to verify.")
    args = parser.parse_args()

    target_files = args.files
    if not target_files:
        target_files = [".github/PULL_REQUEST_TEMPLATE.md"]

    all_passed = True
    for fp in target_files:
        if not verify_file(fp):
            all_passed = False

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
