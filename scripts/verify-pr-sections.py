#!/usr/bin/env python3
"""
verify-pr-sections.py
Validates that compliance Pull Request markdown files contain all 15 required
numbered sections in exact sequential order, are non-empty, and contain no emojis.
"""

import sys
import os
import re
import argparse

REQUIRED_SECTIONS = [
    (1, "Summary"),
    (2, "Background"),
    (3, "Regulatory change"),
    (4, "Official citations"),
    (5, "Affected files"),
    (6, "Risk assessment"),
    (7, "Migration steps"),
    (8, "Backward compatibility"),
    (9, "Implementation checklist"),
    (10, "Testing checklist"),
    (11, "Documentation checklist"),
    (12, "Compliance impact"),
    (13, "Breaking changes"),
    (14, "Review checklist"),
    (15, "Approver recommendations"),
]

# Regex pattern for emojis and high unicode emoticon symbols
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosure
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "]+",
    flags=re.UNICODE,
)

def strip_html_comments(text: str) -> str:
    """Removes HTML comment blocks from text."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def verify_pr_markdown(filepath: str) -> tuple[bool, list[str]]:
    """
    Verifies a PR markdown file for section headings, order, content, and emoji presence.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    if not os.path.isfile(filepath):
        return False, [f"File not found: {filepath}"]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for emojis
    emoji_matches = EMOJI_PATTERN.findall(content)
    if emoji_matches:
        errors.append(f"Emoji detected in file: {', '.join(set(emoji_matches))}")

    # Extract all h2 section headers
    # Format: "## N. Section Title" or "## Section Title"
    section_matches = []
    header_regex = re.compile(r"^##\s+(?:(\d+)\.\s+)?(.+?)$", re.MULTILINE)
    for match in header_regex.finditer(content):
        num_str, title = match.groups()
        num = int(num_str) if num_str else None
        section_matches.append((num, title.strip(), match.start(), match.end()))

    if not section_matches:
        errors.append("No '##' section headings found in file.")
        return False, errors

    # Check presence and order of all 15 required sections
    match_idx = 0
    for req_num, req_title in REQUIRED_SECTIONS:
        found = False
        while match_idx < len(section_matches):
            num, title, start, end = section_matches[match_idx]
            clean_title = title.rstrip().lower()
            expected_lower = req_title.lower()

            if clean_title == expected_lower or clean_title == f"{req_num}. {expected_lower}":
                found = True
                match_idx += 1
                break
            match_idx += 1

        if not found:
            errors.append(f"Missing or out-of-order section ## {req_num}. {req_title}")

    # Verify each section has content
    for i, (num, title, start, end) in enumerate(section_matches):
        next_start = section_matches[i + 1][2] if i + 1 < len(section_matches) else len(content)
        section_body = content[end:next_start]
        clean_body = strip_html_comments(section_body).strip()
        if not clean_body:
            section_label = f"{num}. {title}" if num else title
            errors.append(f"Section '## {section_label}' is empty.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    parser = argparse.ArgumentParser(
        description="Verify compliance PR markdown documents for 15 required sections."
    )
    parser.add_argument(
        "files", nargs="+", help="Path to markdown PR file(s) or PR template(s)"
    )
    args = parser.parse_args()

    all_valid = True
    for filepath in args.files:
        is_valid, errors = verify_pr_markdown(filepath)
        if is_valid:
            print(f"PASS  {filepath}: All 15 required compliance sections present and verified.")
        else:
            all_valid = False
            print(f"FAIL  {filepath}: Validation errors found:")
            for err in errors:
                print(f"  - {err}")

    if not all_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
