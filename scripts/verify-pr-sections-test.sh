#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VERIFY_SCRIPT="${REPO_ROOT}/scripts/verify-pr-sections.py"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "${TEMP_DIR}"' EXIT

PASSED_TESTS=0
FAILED_TESTS=0

assert_pass() {
    local test_name="$1"
    local file_path="$2"
    if python3 "${VERIFY_SCRIPT}" "${file_path}" >/dev/null 2>&1; then
        echo "PASS  ${test_name}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "FAIL  ${test_name} (expected pass, got fail)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

assert_fail() {
    local test_name="$1"
    local file_path="$2"
    if python3 "${VERIFY_SCRIPT}" "${file_path}" >/dev/null 2>&1; then
        echo "FAIL  ${test_name} (expected fail, got pass)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    else
        echo "PASS  ${test_name}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
}

# Test 1: Valid 15-section PR draft
VALID_FILE="${TEMP_DIR}/valid.md"
cat <<'EOF' > "${VALID_FILE}"
## 1. Summary
Summary text goes here.

## 2. Background
Background text goes here.

## 3. Regulatory change
Regulatory change details.

## 4. Official citations
- https://eur-lex.europa.eu

## 5. Affected files
- src/app.ts

## 6. Risk assessment
High risk details.

## 7. Migration steps
1. Do this.

## 8. Backward compatibility
Compatible.

## 9. Implementation checklist
- [x] Implemented

## 10. Testing checklist
- [x] Tested

## 11. Documentation checklist
- [x] Documented

## 12. Compliance impact
Positive impact.

## 13. Breaking changes
None.

## 14. Review checklist
- [x] Reviewed

## 15. Approver recommendations
Recommended.
EOF

assert_pass "Valid 15-section PR draft" "${VALID_FILE}"

# Test 2: Missing section
MISSING_FILE="${TEMP_DIR}/missing.md"
cat <<'EOF' > "${MISSING_FILE}"
## 1. Summary
Summary text.

## 2. Background
Background text.
EOF

assert_fail "Missing required sections" "${MISSING_FILE}"

# Test 3: Out of order sections
ORDER_FILE="${TEMP_DIR}/out_of_order.md"
cat <<'EOF' > "${ORDER_FILE}"
## 2. Background
Background text.

## 1. Summary
Summary text.
EOF

assert_fail "Out of order sections" "${ORDER_FILE}"

# Test 4: Empty section
EMPTY_FILE="${TEMP_DIR}/empty.md"
cat <<'EOF' > "${EMPTY_FILE}"
## 1. Summary
<!-- Comment only, no text -->

## 2. Background
Background text.
EOF

assert_fail "Empty section (comment only)" "${EMPTY_FILE}"

# Test 5: Emoji presence
EMOJI_FILE="${TEMP_DIR}/emoji.md"
cat <<'EOF' > "${EMOJI_FILE}"
## 1. Summary
Summary text 😀.

## 2. Background
Background text.
EOF

assert_fail "Emoji in content" "${EMOJI_FILE}"

# Test 6: Repository default PR template
assert_pass "Repository PULL_REQUEST_TEMPLATE.md" "${REPO_ROOT}/.github/PULL_REQUEST_TEMPLATE.md"

echo ""
echo "Verify PR Sections Test Results: ${PASSED_TESTS} passed, ${FAILED_TESTS} failed"
if [ "${FAILED_TESTS}" -ne 0 ]; then
    exit 1
fi
