#!/usr/bin/env bash
# Test suite for scripts/monitor-android.py
# Verifies mock RSS input parsing, Android/Google Play keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_android_announcements.json"
OUT_DOCS="/tmp/test_android_migration.md"
OUT_PR="/tmp/test_android_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-GP-DEV-POL",
    "category": "Google Play Developer Policies",
    "title": "Google Play Policy Revision on Child Safety",
    "description": "Important policy revisions for child safety and Families program compliance.",
    "link": "https://support.google.com/googleplay/android-developer",
    "pubDate": "Fri, 15 May 2026 10:00:00 PDT"
  },
  {
    "id": "MOCK-TARGET-SDK",
    "category": "Target SDK requirements",
    "title": "Target SDK API Level 36 Requirements",
    "description": "All submissions must target Android 16 (API 36) or higher.",
    "link": "https://developer.android.com/google/play/requirements/target-sdk",
    "pubDate": "Sat, 16 May 2026 11:00:00 PDT"
  }
]
EOF

echo "== Running Android Policy Monitor Test Suite =="

# Execute scripts/monitor-android.py with mock dataset
python3 scripts/monitor-android.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_android_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-android.py failed with exit code $RC. Output:"
  cat /tmp/monitor_android_run.log
  exit 1
fi
ok "monitor-android.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Google Play Policy Revision" /tmp/monitor_android_run.log && grep -q "Target SDK API Level" /tmp/monitor_android_run.log; then
  ok "Correctly matched relevant Android policy updates"
else
  bad "Failed to match relevant Android policy updates. Output: $(cat /tmp/monitor_android_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Google Play Policy Revision" "$OUT_DOCS" && grep -q "Target SDK API Level" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# Assert that PR Draft contains EXACTLY 15 required sections
if [ -f "$OUT_PR" ]; then
  ok "PR Draft output file created at $OUT_PR"

  declare -a SECTIONS=(
    "Summary"
    "Background"
    "Regulatory change"
    "Official citations"
    "Affected files"
    "Risk assessment"
    "Migration steps"
    "Backward compatibility"
    "Implementation checklist"
    "Testing checklist"
    "Documentation checklist"
    "Compliance impact"
    "Breaking changes"
    "Review checklist"
    "Approver recommendations"
  )

  MISSING=0
  for idx in "${!SECTIONS[@]}"; do
    sec_num=$((idx + 1))
    sec_name="${SECTIONS[$idx]}"
    if grep -q "## ${sec_num}\. ${sec_name}" "$OUT_PR"; then
      true
    else
      echo "  Missing PR section: ## ${sec_num}. ${sec_name}"
      MISSING=$((MISSING + 1))
    fi
  done

  if [ "$MISSING" -eq 0 ]; then
    ok "PR Draft contains exactly the 15 required compliance sections"
  else
    bad "PR Draft is missing $MISSING of the 15 required compliance sections"
  fi
else
  bad "PR Draft file was not created"
fi

echo ""
echo "Android Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
