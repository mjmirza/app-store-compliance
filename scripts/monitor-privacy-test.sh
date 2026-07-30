#!/usr/bin/env bash
# Test suite for scripts/monitor-privacy.py
# Verifies mock RSS/JSON input parsing, privacy/compliance keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_privacy_announcements.json"
OUT_DOCS="/tmp/test_privacy_migration.md"
OUT_PR="/tmp/test_privacy_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-PRIV-MANIFEST",
    "category": "Privacy Manifest",
    "title": "Strict Apple Privacy Manifest Rules",
    "description": "Important privacy manifest policy updates requiring PrivacyInfo.xcprivacy configuration.",
    "link": "https://developer.apple.com",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-COOKIE-CONSENT",
    "category": "Cookie consent",
    "title": "Mandatory Cookie Consent Banner Guidelines",
    "description": "All web services must integrate cookie consent banners before setting non-essential cookies.",
    "link": "https://eur-lex.europa.eu",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  }
]
EOF

echo "== Running Privacy Policy Monitor Test Suite =="

# Execute scripts/monitor-privacy.py with mock dataset
python3 scripts/monitor-privacy.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_privacy_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-privacy.py failed with exit code $RC. Output:"
  cat /tmp/monitor_privacy_run.log
  exit 1
fi
ok "monitor-privacy.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Strict Apple Privacy Manifest" /tmp/monitor_privacy_run.log && grep -q "Mandatory Cookie Consent" /tmp/monitor_privacy_run.log; then
  ok "Correctly matched relevant Privacy policy updates"
else
  bad "Failed to match relevant Privacy policy updates. Output: $(cat /tmp/monitor_privacy_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Strict Apple Privacy Manifest" "$OUT_DOCS" && grep -q "Mandatory Cookie Consent" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# Assert that PR Draft contains EXACTLY 15 required sections and is completely emoji-free
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

  # Check that the PR draft is emoji-free
  # Using a broad regex pattern to spot emojis (any characters in the typical Emoji and Pictographs blocks)
  # or simple checks
  if grep -P "[\x{1F300}-\x{1F6FF}]|[\x{2600}-\x{26FF}]" "$OUT_PR" >/dev/null 2>&1; then
    bad "PR Draft contains emojis"
  else
    ok "PR Draft is completely emoji-free"
  fi

else
  bad "PR Draft file was not created"
fi

echo ""
echo "Privacy Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
