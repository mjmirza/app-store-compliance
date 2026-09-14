#!/usr/bin/env bash
#
# verify-pr-sections-test.sh
# Tests the PR section verification script (scripts/verify-pr-sections.py).
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERIFY_SCRIPT="$REPO_ROOT/scripts/verify-pr-sections.py"

echo "[TEST] Starting PR Sections Verification Test Suite"

# Test 1: Executable check
if [ ! -x "$VERIFY_SCRIPT" ]; then
  echo "[FAIL] verify-pr-sections.py is not executable"
  exit 1
fi
echo "[PASS] verify-pr-sections.py is executable"

# Test 2: Verify PULL_REQUEST_TEMPLATE.md passes
python3 "$VERIFY_SCRIPT" "$REPO_ROOT/.github/PULL_REQUEST_TEMPLATE.md" > /dev/null
echo "[PASS] .github/PULL_REQUEST_TEMPLATE.md passed 15-section verification"

# Test 3: Verify generated PR draft passes
TMP_VALID="/tmp/test_valid_pr.md"
cat << 'EOF' > "$TMP_VALID"
# Test Compliance PR

## 1. Summary
Summary content here.

## 2. Background
Background content here.

## 3. Regulatory change
Regulatory change content here.

## 4. Official citations
- https://example.com/citation

## 5. Affected files
- file1.py

## 6. Risk assessment
Low risk assessment.

## 7. Migration steps
1. Migration step 1.

## 8. Backward compatibility
100% backward compatible.

## 9. Implementation checklist
- [x] Implemented step 1

## 10. Testing checklist
- [x] Ran unit tests

## 11. Documentation checklist
- [x] Updated docs

## 12. Compliance impact
Positive compliance impact.

## 13. Breaking changes
None.

## 14. Review checklist
- [x] Verified citations

## 15. Approver recommendations
- Compliance Lead
EOF

python3 "$VERIFY_SCRIPT" "$TMP_VALID" > /dev/null
echo "[PASS] Valid 15-section PR draft passed verification"
rm -f "$TMP_VALID"

# Test 4: Verify failure on missing section
TMP_MISSING="/tmp/test_missing_pr.md"
cat << 'EOF' > "$TMP_MISSING"
## 1. Summary
Summary content here.

## 2. Background
Background content here.
EOF

if python3 "$VERIFY_SCRIPT" "$TMP_MISSING" > /dev/null 2>&1; then
  echo "[FAIL] Failed to detect missing PR sections"
  rm -f "$TMP_MISSING"
  exit 1
fi
echo "[PASS] Correctly detected missing PR sections"
rm -f "$TMP_MISSING"

# Test 5: Verify failure on wrong order
TMP_WRONG_ORDER="/tmp/test_order_pr.md"
cat << 'EOF' > "$TMP_WRONG_ORDER"
## 2. Background
Background first.

## 1. Summary
Summary second.
EOF

if python3 "$VERIFY_SCRIPT" "$TMP_WRONG_ORDER" > /dev/null 2>&1; then
  echo "[FAIL] Failed to detect out-of-order PR sections"
  rm -f "$TMP_WRONG_ORDER"
  exit 1
fi
echo "[PASS] Correctly detected out-of-order PR sections"
rm -f "$TMP_WRONG_ORDER"

# Test 6: Verify failure on emojis
TMP_EMOJI="/tmp/test_emoji_pr.md"
cat << 'EOF' > "$TMP_EMOJI"
# PR Title 🚀

## 1. Summary
Summary content here.

## 2. Background
Background content here.

## 3. Regulatory change
Regulatory change content here.

## 4. Official citations
- https://example.com/citation

## 5. Affected files
- file1.py

## 6. Risk assessment
Low risk assessment.

## 7. Migration steps
1. Migration step 1.

## 8. Backward compatibility
100% backward compatible.

## 9. Implementation checklist
- [x] Implemented step 1

## 10. Testing checklist
- [x] Ran unit tests

## 11. Documentation checklist
- [x] Updated docs

## 12. Compliance impact
Positive compliance impact.

## 13. Breaking changes
None.

## 14. Review checklist
- [x] Verified citations

## 15. Approver recommendations
- Compliance Lead
EOF

if python3 "$VERIFY_SCRIPT" "$TMP_EMOJI" > /dev/null 2>&1; then
  echo "[FAIL] Failed to detect emojis in PR draft"
  rm -f "$TMP_EMOJI"
  exit 1
fi
echo "[PASS] Correctly detected emojis in PR draft"
rm -f "$TMP_EMOJI"

echo "[SUCCESS] All verify-pr-sections tests passed."
exit 0
