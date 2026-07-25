#!/usr/bin/env bash
# Test verification script for Apple Developer Requirement Monitor
# Runs the monitor in mock mode, verifies the generation of migration logs and draft PRs,
# and checks that no emojis or graphical symbols are present in any generated assets.

set -euo pipefail

echo "=== Running Apple Monitor Test Runner ==="

# Clean any existing generated draft PRs and logs to ensure a clean test
rm -f data/apple-policy-history.json
rm -f docs/APPLE-POLICY-MIGRATION.md
rm -f docs/APPLE_COMPLIANCE_PR_DRAFT.md
rm -f docs/apple_pr_draft_*.md

# Execute the monitor python script with mock updates
echo "Running monitor-apple.py with mock updates..."
python3 scripts/monitor-apple.py --mock --verbose

# Verify file creation
echo "Verifying file creations..."
if [ ! -f "data/apple-policy-history.json" ]; then
    echo "FAILED: data/apple-policy-history.json was not created"
    exit 1
fi

if [ ! -f "docs/APPLE-POLICY-MIGRATION.md" ]; then
    echo "FAILED: docs/APPLE-POLICY-MIGRATION.md was not created"
    exit 1
fi

if [ ! -f "docs/APPLE_COMPLIANCE_PR_DRAFT.md" ]; then
    echo "FAILED: docs/APPLE_COMPLIANCE_PR_DRAFT.md was not created"
    exit 1
fi

# Verify individal PR drafts exist
INDIVIDUAL_DRAFT="docs/apple_pr_draft_enforcing_privacy_manifests_and_required_reason_apis.md"
if [ ! -f "$INDIVIDUAL_DRAFT" ]; then
    echo "FAILED: Individual draft PR $INDIVIDUAL_DRAFT was not created"
    exit 1
fi

# Verify the PR contains exactly 15 required sections
echo "Verifying 15 required sections exist in the draft PR..."
REQUIRED_SECTIONS=(
    "## Summary"
    "## Background"
    "## Regulatory change"
    "## Official citations"
    "## Affected files"
    "## Risk assessment"
    "## Migration steps"
    "## Backward compatibility"
    "## Implementation checklist"
    "## Testing checklist"
    "## Documentation checklist"
    "## Compliance impact"
    "## Breaking changes"
    "## Review checklist"
    "## Approver recommendations"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -Fq "$section" "$INDIVIDUAL_DRAFT"; then
        echo "FAILED: Section '$section' is missing in $INDIVIDUAL_DRAFT"
        exit 1
    fi
done

# Verify no emojis, emoticons, or graphical symbols are present in the generated files.
echo "Checking for emojis, emoticons, or graphical symbols in generated files..."
python3 -c '
import re, sys

files_to_check = [
    "docs/APPLE-POLICY-MIGRATION.md",
    "docs/APPLE_COMPLIANCE_PR_DRAFT.md",
    "scripts/monitor-apple.py"
]

# Regex for common emoticons (e.g. :-), :-D, :), :D), and emojis/symbols using proper 8-character escapes for high code points
emoji_pattern = re.compile(
    "[\u2600-\u27BF]"
    "|[\U0001F300-\U0001F6FF]"
    "|[\U0001F900-\U0001F9FF]"
    "|[\u2190-\u21FF]"
    "|:-?\\)"
    "|:-?D"
    "|✓|✗|➔|➜"
)

failed = False
for path in files_to_check:
    try:
        with open(path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                # Check for explicit emojis/symbols in line
                matches = emoji_pattern.findall(line)
                if matches:
                    print("FAILED: Found potential emoji/emoticon/graphical symbol {} in {} at line {}: {}".format(
                        matches, path, idx, line.strip()
                    ))
                    failed = True
    except Exception as e:
        print("Error checking {}: {}".format(path, e))
        failed = True

if failed:
    sys.exit(1)
'

echo "SUCCESS: All tests passed cleanly. Generated files conform to strict non-emoji requirements."
exit 0
