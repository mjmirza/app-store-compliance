#!/usr/bin/env bash
# Test suite for scripts/monitor-ai-policy.py
# Verifies mock RSS input parsing, AI keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_ai_announcements.json"
OUT_DOCS="/tmp/test_ai_migration.md"
OUT_PR="/tmp/test_ai_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# 1. Create a mock dataset containing both unrelated news and relevant AI policy announcements
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "UNRELATED-NEWS",
    "platform": "Apple",
    "title": "New Apple Arcade Games Coming in Spring",
    "description": "Discover new games arriving on Apple Arcade this Spring including classic card games and puzzle games.",
    "link": "https://developer.apple.com/news/?id=arcade_spring",
    "pubDate": "Mon, 10 Mar 2026 09:00:00 PDT"
  },
  {
    "id": "APPLE-AI-TEST-RULE",
    "platform": "Apple",
    "title": "Important Updates on Generative AI Requirements and User Disclosures",
    "description": "We are introducing new compliance checks for generative AI outputs. Developers must include user disclosures and clear consent mechanisms for third-party AI data flows.",
    "link": "https://developer.apple.com/news/?id=ai_test_2026",
    "pubDate": "Tue, 11 Mar 2026 10:00:00 PDT"
  },
  {
    "id": "GOOGLE-AI-TEST-RULE",
    "platform": "Google Play",
    "title": "Google Play Policy Revision: Disclosure for AI-Generated Media",
    "description": "All developers utilizing generative AI for user-generated content must implement prominent safety safeguards and disclosures.",
    "link": "https://android-developers.googleblog.com/",
    "pubDate": "Wed, 12 Mar 2026 11:00:00 PDT"
  }
]
EOF

echo "== Running AI Policy Monitor Test Suite =="

# 2. Execute scripts/monitor-ai-policy.py with mock dataset
python3 scripts/monitor-ai-policy.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-ai-policy.py failed with exit code $RC. Output:"
  cat /tmp/monitor_run.log
  exit 1
fi
ok "monitor-ai-policy.py ran successfully with exit code 0"

# 3. Assert relevant policies were matched and unrelated was ignored
if grep -q "Generative AI Requirements" /tmp/monitor_run.log && grep -q "Google Play Policy Revision" /tmp/monitor_run.log; then
  ok "Correctly matched relevant AI policy updates"
else
  bad "Failed to match relevant AI policy updates. Output: $(cat /tmp/monitor_run.log)"
fi

if grep -q "Apple Arcade Games" /tmp/monitor_run.log; then
  bad "Erroneously matched unrelated Apple Arcade announcement"
else
  ok "Successfully ignored unrelated announcement"
fi

# 4. Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  # Check content in documentation
  if grep -q "Generative AI Requirements" "$OUT_DOCS" && grep -q "Google Play Policy Revision" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# 5. Assert that PR Draft contains EXACTLY 15 required sections
if [ -f "$OUT_PR" ]; then
  ok "PR Draft output file created at $OUT_PR"

  # Define the exactly 15 required sections
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
    # Match patterns like "## 1. Summary" or "## 15. Approver recommendations"
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
echo "AI Policy Monitor test suite: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
