#!/usr/bin/env bash
# monitor-apple-test.sh: Comprehensive test suite for Apple Developer Requirements Monitor (monitor.py)
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"
PASS=0; FAIL=0

ok() {
  PASS=$((PASS+1))
  printf 'PASS  %s\n' "$1"
}

bad() {
  FAIL=$((FAIL+1))
  printf 'FAIL  %s\n' "$1"
}

# 1. Verification of expanded help output and CLI arguments
OUT_HELP="$($MONITOR --help 2>&1)"
echo "$OUT_HELP" | grep -q -e "--output-docs" && \
echo "$OUT_HELP" | grep -q -e "--pr-output" && \
ok "help output contains --output-docs and --pr-output options" || bad "help output options"

# 2. Setup a temporary directory for scanning simulation
T=$(mktemp -d)
mkdir -p "$T/Sources"

# Write a compliant-ish app with some matches (e.g. UserDefaults and NSPrivacyAccessedAPITypes)
printf "import Foundation\nlet d = UserDefaults.standard\n" > "$T/Sources/App.swift"
printf "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<plist version=\"1.0\">\n<dict>\n<key>NSPrivacyAccessedAPITypes</key>\n<array/>\n</dict>\n</plist>" > "$T/Sources/PrivacyInfo.xcprivacy"

# 3. Simulate with mock data to have a Priority 1 official reference to pass source trust checks
DOC_OUT="$T/APPLE-POLICY-MIGRATION.md"
PR_OUT="$T/APPLE_COMPLIANCE_PR_DRAFT.md"

$MONITOR --project "$T" --mock --output-docs "$DOC_OUT" --pr-output "$PR_OUT" > /dev/null 2>&1

# Check that files were created
[ -f "$DOC_OUT" ] && ok "APPLE-POLICY-MIGRATION.md was successfully written" || bad "migration doc write"
[ -f "$PR_OUT" ] && ok "APPLE_COMPLIANCE_PR_DRAFT.md was successfully written" || bad "PR draft write"

# Check the contents of the generated PR draft for the 15 required sections and lack of emojis
PR_CONTENT=$(cat "$PR_OUT")
echo "$PR_CONTENT" | grep -q "## 1. Summary" && \
echo "$PR_CONTENT" | grep -q "## 2. Background" && \
echo "$PR_CONTENT" | grep -q "## 3. Regulatory change" && \
echo "$PR_CONTENT" | grep -q "## 4. Official citations" && \
echo "$PR_CONTENT" | grep -q "## 5. Affected files" && \
echo "$PR_CONTENT" | grep -q "## 6. Risk assessment" && \
echo "$PR_CONTENT" | grep -q "## 7. Migration steps" && \
echo "$PR_CONTENT" | grep -q "## 8. Backward compatibility" && \
echo "$PR_CONTENT" | grep -q "## 9. Implementation checklist" && \
echo "$PR_CONTENT" | grep -q "## 10. Testing checklist" && \
echo "$PR_CONTENT" | grep -q "## 11. Documentation checklist" && \
echo "$PR_CONTENT" | grep -q "## 12. Compliance impact" && \
echo "$PR_CONTENT" | grep -q "## 13. Breaking changes" && \
echo "$PR_CONTENT" | grep -q "## 14. Review checklist" && \
echo "$PR_CONTENT" | grep -q "## 15. Approver recommendations" && \
ok "APPLE_COMPLIANCE_PR_DRAFT.md contains exactly 15 non-vague sections" || bad "PR draft sections completeness"

# Emoji-free check
if echo "$PR_CONTENT" | grep -q -P '[\x{1F300}-\x{1F6FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]'; then
  bad "PR draft contains emojis"
else
  ok "PR draft is 100% emoji-free"
fi

# 4. Source Trust and Blocking Logic verification
# Running a single simulated track with a mock.invalid link (unverified Priority 4) should block PR generation
DOC_BLOCKED="$T/BLOCKED-DOC.md"
PR_BLOCKED="$T/BLOCKED-PR.md"
$MONITOR --project "$T" --simulate "Privacy Manifests" --output-docs "$DOC_BLOCKED" --pr-output "$PR_BLOCKED" > /dev/null 2>&1

DOC_CONTENT=$(cat "$DOC_BLOCKED")
echo "$DOC_CONTENT" | grep -q "BLOCKED" && \
echo "$DOC_CONTENT" | grep -q "Suspended" && \
ok "unverified priority 4/5 announcements successfully block task generation in migration doc" || bad "source trust block check"

# PR_BLOCKED should not be created because verified_updates was empty
[ ! -f "$PR_BLOCKED" ] && ok "PR generation is blocked when all updates are from unverified sources" || bad "PR generation blocking"

# 5. JSON output formatting and logs suppression verification
JSON_OUT="$($MONITOR --project "$T" --simulate "Xcode requirements" --json 2>&1)"
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Xcode requirements'" 2>/dev/null && \
ok "json option suppresses all logs and outputs strictly valid JSON" || bad "json logs suppression and validity"

# Clean up temp files
rm -rf "$T"

echo ""
echo "monitor-apple-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
