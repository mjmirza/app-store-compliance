#!/usr/bin/env python3
"""
verify-pr-sections.py
Validates that compliance Pull Request markdown documents contain all 15 required
numbered compliance section headings in exact sequential order with non-vague content and zero emojis.
"""

import sys
import os
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
    "15. Approver recommendations",
]

VAGUE_KEYWORDS = [
    "todo",
    "tbd",
    "fixme",
    "n/a - vague",
    "placeholder text",
    "lorem ipsum",
]


def check_emojis(text):
    emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    return emojis


def verify_pr_content(content, filename="input"):
    errors = []

    # Check Emojis
    emojis = check_emojis(content)
    if emojis:
        errors.append(f"[{filename}] Emojis detected in PR content: {emojis}")

    # Search for section positions
    positions = []
    for idx, sec in enumerate(REQUIRED_SECTIONS, 1):
        # Match ## 1. Summary or ## 1. Summary: or similar heading variations
        pattern = re.compile(rf"^##\s*{re.escape(sec)}\b", re.IGNORECASE | re.MULTILINE)
        matches = list(pattern.finditer(content))
        if not matches:
            errors.append(f"[{filename}] Missing required section heading: '## {sec}'")
        else:
            positions.append((idx, matches[0].start(), matches[0].end()))

    # Check sequential order
    if len(positions) == len(REQUIRED_SECTIONS):
        for i in range(len(positions) - 1):
            if positions[i][1] >= positions[i + 1][1]:
                errors.append(
                    f"[{filename}] Out-of-order section: '## {REQUIRED_SECTIONS[positions[i+1][0]-1]}' appears before '## {REQUIRED_SECTIONS[positions[i][0]-1]}'"
                )

        # Check content non-emptiness and non-vagueness between sections
        for i in range(len(positions)):
            start_pos = positions[i][2]
            end_pos = positions[i + 1][1] if i + 1 < len(positions) else len(content)
            sec_body = content[start_pos:end_pos].strip()

            if not sec_body:
                errors.append(
                    f"[{filename}] Section '## {REQUIRED_SECTIONS[i]}' is empty."
                )
            else:
                for vague in VAGUE_KEYWORDS:
                    if vague in sec_body.lower():
                        errors.append(
                            f"[{filename}] Section '## {REQUIRED_SECTIONS[i]}' contains vague or placeholder keyword '{vague}'."
                        )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Verify compliance PR markdown for 15 numbered sections, non-vagueness, and emoji-free policy."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Path to PR markdown file(s) to verify (or stdin if omitted)",
    )

    args = parser.parse_args()

    all_errors = []

    if args.files:
        for fpath in args.files:
            if not os.path.exists(fpath):
                all_errors.append(f"File not found: {fpath}")
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    content = fp.read()
                errs = verify_pr_content(content, filename=fpath)
                all_errors.extend(errs)
            except Exception as e:
                all_errors.append(f"Failed to read file {fpath}: {e}")
    else:
        # Read from stdin
        content = sys.stdin.read()
        if content:
            errs = verify_pr_content(content, filename="stdin")
            all_errors.extend(errs)
        else:
            all_errors.append("No input provided via stdin or file arguments.")

    if all_errors:
        print("PR Verification Failed:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("PASS: PR markdown contains all 15 required numbered sections in sequential order with valid content.")
        sys.exit(0)


if __name__ == "__main__":
    main()
