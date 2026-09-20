#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_SCRIPT="${SCRIPT_DIR}/verify-pr-sections.py"

PASS_COUNT=0
FAIL_COUNT=0

pass() {
  echo "PASS  $1"
  PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
  echo "FAIL  $1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

# Test 1: Default PR template
if python3 "${VERIFY_SCRIPT}" "${SCRIPT_DIR}/../.github/PULL_REQUEST_TEMPLATE.md" >/dev/null 2>&1; then
  pass "Default .github/PULL_REQUEST_TEMPLATE.md passes verification"
else
  fail "Default .github/PULL_REQUEST_TEMPLATE.md failed verification"
fi

# Test 2: Valid generated markdown file
VALID_MD="${TMP_DIR}/valid.md"
cat << 'EOF' > "${VALID_MD}"
## 1. Summary
Summary text.

## 2. Background
Background details.

## 3. Regulatory change
Details.

## 4. Official citations
Citations.

## 5. Affected files
Files.

## 6. Risk assessment
Risks.

## 7. Migration steps
Steps.

## 8. Backward compatibility
Details.

## 9. Implementation checklist
Checklist.

## 10. Testing checklist
Tests.

## 11. Documentation checklist
Docs.

## 12. Compliance impact
Impact.

## 13. Breaking changes
None.

## 14. Review checklist
Review.

## 15. Approver recommendations
Recommendations.
EOF

if python3 "${VERIFY_SCRIPT}" "${VALID_MD}" >/dev/null 2>&1; then
  pass "Valid PR markdown passes verification"
else
  fail "Valid PR markdown failed verification"
fi

# Test 3: Missing section heading
MISSING_MD="${TMP_DIR}/missing.md"
cat << 'EOF' > "${MISSING_MD}"
## 1. Summary
Summary text.

## 3. Regulatory change
Details.
EOF

if ! python3 "${VERIFY_SCRIPT}" "${MISSING_MD}" >/dev/null 2>&1; then
  pass "Fails on missing sections"
else
  fail "Should have failed on missing sections"
fi

# Test 4: Emoji containing file
EMOJI_MD="${TMP_DIR}/emoji.md"
cat << 'EOF' > "${EMOJI_MD}"
## 1. Summary 🚀
Summary text.

## 2. Background
Background details.

## 3. Regulatory change
Details.

## 4. Official citations
Citations.

## 5. Affected files
Files.

## 6. Risk assessment
Risks.

## 7. Migration steps
Steps.

## 8. Backward compatibility
Details.

## 9. Implementation checklist
Checklist.

## 10. Testing checklist
Tests.

## 11. Documentation checklist
Docs.

## 12. Compliance impact
Impact.

## 13. Breaking changes
None.

## 14. Review checklist
Review.

## 15. Approver recommendations
Recommendations.
EOF

if ! python3 "${VERIFY_SCRIPT}" "${EMOJI_MD}" >/dev/null 2>&1; then
  pass "Fails on emoji presence"
else
  fail "Should have failed on emoji presence"
fi

# Test 5: Out of order sections
ORDER_MD="${TMP_DIR}/order.md"
cat << 'EOF' > "${ORDER_MD}"
## 2. Background
Background details.

## 1. Summary
Summary text.

## 3. Regulatory change
Details.

## 4. Official citations
Citations.

## 5. Affected files
Files.

## 6. Risk assessment
Risks.

## 7. Migration steps
Steps.

## 8. Backward compatibility
Details.

## 9. Implementation checklist
Checklist.

## 10. Testing checklist
Tests.

## 11. Documentation checklist
Docs.

## 12. Compliance impact
Impact.

## 13. Breaking changes
None.

## 14. Review checklist
Review.

## 15. Approver recommendations
Recommendations.
EOF

if ! python3 "${VERIFY_SCRIPT}" "${ORDER_MD}" >/dev/null 2>&1; then
  pass "Fails on out-of-order sections"
else
  fail "Should have failed on out-of-order sections"
fi

echo "verify-pr-sections test suite: ${PASS_COUNT} passed, ${FAIL_COUNT} failed"

if [ "${FAIL_COUNT}" -gt 0 ]; then
  exit 1
fi
