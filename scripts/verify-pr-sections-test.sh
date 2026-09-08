#!/usr/bin/env bash
#
# verify-pr-sections-test.sh
# Unit tests for verify-pr-sections.py
#

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$REPO_ROOT/scripts/verify-pr-sections.py"

chmod +x "$SCRIPT"

echo "== Running PR Sections Verification Test Suite =="

PASS=0
FAIL=0

ok() { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# Test 1: Valid 15-section PR
TMP_VALID="/tmp/test_valid_pr.md"
cat << 'EOF' > "$TMP_VALID"
# Compliance Update

## 1. Summary
This pull request addresses the regulatory requirement.

## 2. Background
Historical context of policy changes.

## 3. Regulatory change
Specific statutory mandates.

## 4. Official citations
Primary sources from Official Journal.

## 5. Affected files
- `Info.plist`

## 6. Risk assessment
High risk if not addressed.

## 7. Migration steps
1. Update declarations.

## 8. Backward compatibility
Fully backward compatible.

## 9. Implementation checklist
- [x] Code updated.

## 10. Testing checklist
- [x] Unit tests passed.

## 11. Documentation checklist
- [x] Guides updated.

## 12. Compliance impact
Low residual risk.

## 13. Breaking changes
None.

## 14. Review checklist
- [x] Verified.

## 15. Approver recommendations
Lead Mobile Architect.
EOF

if python3 "$SCRIPT" "$TMP_VALID" > /dev/null 2>&1; then
  ok "Valid 15-section PR passed verification"
else
  bad "Valid 15-section PR failed verification"
fi

# Test 2: Missing Section
TMP_INVALID_MISSING="/tmp/test_invalid_missing.md"
sed '/## 3. Regulatory change/d' "$TMP_VALID" > "$TMP_INVALID_MISSING"

if ! python3 "$SCRIPT" "$TMP_INVALID_MISSING" > /dev/null 2>&1; then
  ok "Missing section correctly caught and flagged"
else
  bad "Missing section was not flagged"
fi

# Test 3: Out-of-order section
TMP_INVALID_ORDER="/tmp/test_invalid_order.md"
cat << 'EOF' > "$TMP_INVALID_ORDER"
## 2. Background
Context

## 1. Summary
Summary
EOF

if ! python3 "$SCRIPT" "$TMP_INVALID_ORDER" > /dev/null 2>&1; then
  ok "Out-of-order sections correctly caught and flagged"
else
  bad "Out-of-order sections were not flagged"
fi

# Test 4: Vague placeholder keyword
TMP_INVALID_VAGUE="/tmp/test_invalid_vague.md"
sed 's/This pull request addresses the regulatory requirement./TODO: add summary/' "$TMP_VALID" > "$TMP_INVALID_VAGUE"

if ! python3 "$SCRIPT" "$TMP_INVALID_VAGUE" > /dev/null 2>&1; then
  ok "Vague placeholder keyword correctly caught and flagged"
else
  bad "Vague placeholder keyword was not flagged"
fi

# Test 5: Emoji check
TMP_INVALID_EMOJI="/tmp/test_invalid_emoji.md"
sed 's/Low residual risk./Low residual risk. 😀/' "$TMP_VALID" > "$TMP_INVALID_EMOJI"

if ! python3 "$SCRIPT" "$TMP_INVALID_EMOJI" > /dev/null 2>&1; then
  ok "Emoji presence correctly caught and flagged"
else
  bad "Emoji presence was not flagged"
fi

rm -f "$TMP_VALID" "$TMP_INVALID_MISSING" "$TMP_INVALID_ORDER" "$TMP_INVALID_VAGUE" "$TMP_INVALID_EMOJI"

echo ""
echo "PR Sections Verification Test Suite: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
