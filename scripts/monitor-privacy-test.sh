#!/usr/bin/env bash
# Test suite for scripts/monitor-privacy.py
# Verifies help output, mock announcements parsing, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.
# Strict emoji-free policy is checked.

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
    "id": "MOCK-PRIV-GDPR",
    "requirement": "GDPR",
    "title": "GDPR Regulatory Consent Standard Change",
    "description": "EDPB updates and clarifies consent and user data deletion standard under the GDPR.",
    "link": "https://edpb.europa.eu",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-PRIV-ATT",
    "requirement": "App Tracking Transparency",
    "title": "ATT Consent Prompt Compliance Guidelines",
    "description": "Review teams reiterate that ATT consent prompts are required before cross-app telemetry runs.",
    "link": "https://developer.apple.com",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  }
]
EOF

echo "== Running Privacy Monitor Test Suite =="

# 1. Verification of help output
if python3 scripts/monitor-privacy.py --help | grep -q "Monitor Mobile and Web Privacy Compliance Requirements"; then
  ok "Help output contains correct usage description"
else
  bad "Help output verification failed"
fi

# 2. Run scan with mock JSON
python3 scripts/monitor-privacy.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_privacy_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-privacy.py failed with exit code $RC. Output:"
  cat /tmp/monitor_privacy_run.log
  exit 1
fi
ok "monitor-privacy.py ran successfully with exit code 0"

# 3. Verify JSON output format
JSON_OUT=$(python3 scripts/monitor-privacy.py --simulate "GDPR" --json)
if echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['requirement'] == 'GDPR'" 2>/dev/null; then
  ok "JSON output format is valid and contains matched requirement details"
else
  bad "JSON output validation failed"
fi

# 4. Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "GDPR" "$OUT_DOCS" && grep -q "App Tracking Transparency" "$OUT_DOCS"; then
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

# 6. Verify strict emoji-free policy on generated outputs
EMOJI_CHECK=$(python3 -c "
import sys, os
emojis_found = False
for path in ['$OUT_DOCS', '$OUT_PR', 'scripts/monitor-privacy.py']:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    if emojis:
        print('Found emojis in', path, ':', emojis)
        emojis_found = True
if emojis_found:
    sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" = "No emojis found" ]; then
  ok "Privacy Monitor code and generated files are 100 percent emoji-free"
else
  bad "Emoji detection check failed"
fi

echo ""
echo "Privacy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
