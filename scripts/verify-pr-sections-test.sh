#!/usr/bin/env bash
# verify-pr-sections-test.sh
# Tests scripts/verify-pr-sections.py against valid and invalid markdown files.

set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

VALID_MD="$TMP_DIR/valid_pr.md"
MISSING_SECTION_MD="$TMP_DIR/missing_section.md"
EMOJI_MD="$TMP_DIR/emoji.md"
EMPTY_SECTION_MD="$TMP_DIR/empty_section.md"

cat << 'EOF' > "$VALID_MD"
## 1. Summary
Summary text goes here.

## 2. Background
Background text goes here.

## 3. Regulatory change
Regulatory change details.

## 4. Official citations
- Official Citation 1

## 5. Affected files
- file1.py

## 6. Risk assessment
Risk assessment details.

## 7. Migration steps
1. Migration step 1

## 8. Backward compatibility
Backward compatibility details.

## 9. Implementation checklist
- [ ] Task 1

## 10. Testing checklist
- [ ] Test 1

## 11. Documentation checklist
- [ ] Doc 1

## 12. Compliance impact
Compliance impact details.

## 13. Breaking changes
None.

## 14. Review checklist
- [ ] Reviewed

## 15. Approver recommendations
Approved.
EOF

cat << 'EOF' > "$MISSING_SECTION_MD"
## 1. Summary
Summary text.

## 2. Background
Background text.
EOF

cat << 'EOF' > "$EMOJI_MD"
## 1. Summary
Summary text. 😊

## 2. Background
Background text.

## 3. Regulatory change
Change.

## 4. Official citations
Citations.

## 5. Affected files
Files.

## 6. Risk assessment
Risk.

## 7. Migration steps
Steps.

## 8. Backward compatibility
Compat.

## 9. Implementation checklist
Tasks.

## 10. Testing checklist
Tests.

## 11. Documentation checklist
Docs.

## 12. Compliance impact
Impact.

## 13. Breaking changes
None.

## 14. Review checklist
Check.

## 15. Approver recommendations
Recs.
EOF

cat << 'EOF' > "$EMPTY_SECTION_MD"
## 1. Summary

## 2. Background
Background text.

## 3. Regulatory change
Change.

## 4. Official citations
Citations.

## 5. Affected files
Files.

## 6. Risk assessment
Risk.

## 7. Migration steps
Steps.

## 8. Backward compatibility
Compat.

## 9. Implementation checklist
Tasks.

## 10. Testing checklist
Tests.

## 11. Documentation checklist
Docs.

## 12. Compliance impact
Impact.

## 13. Breaking changes
None.

## 14. Review checklist
Check.

## 15. Approver recommendations
Recs.
EOF

echo "== Running verify-pr-sections Test Suite =="

# 1. Valid file should pass
if python3 scripts/verify-pr-sections.py "$VALID_MD" > /dev/null; then
    echo "PASS: Valid PR markdown passed"
else
    echo "FAIL: Valid PR markdown failed"
    exit 1
fi

# 2. Missing sections should fail
if python3 scripts/verify-pr-sections.py "$MISSING_SECTION_MD" > /dev/null 2>&1; then
    echo "FAIL: Missing section markdown passed unexpectedly"
    exit 1
else
    echo "PASS: Missing section markdown caught successfully"
fi

# 3. Emoji markdown should fail
if python3 scripts/verify-pr-sections.py "$EMOJI_MD" > /dev/null 2>&1; then
    echo "FAIL: Emoji markdown passed unexpectedly"
    exit 1
else
    echo "PASS: Emoji markdown caught successfully"
fi

# 4. Empty section markdown should fail
if python3 scripts/verify-pr-sections.py "$EMPTY_SECTION_MD" > /dev/null 2>&1; then
    echo "FAIL: Empty section markdown passed unexpectedly"
    exit 1
else
    echo "PASS: Empty section markdown caught successfully"
fi

# 5. Check repo's PULL_REQUEST_TEMPLATE.md
if python3 scripts/verify-pr-sections.py .github/PULL_REQUEST_TEMPLATE.md > /dev/null; then
    echo "PASS: .github/PULL_REQUEST_TEMPLATE.md passed verification"
else
    echo "FAIL: .github/PULL_REQUEST_TEMPLATE.md failed verification"
    exit 1
fi

echo "verify-pr-sections test suite: ALL PASSED"
