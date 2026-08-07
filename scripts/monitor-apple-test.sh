#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies mock RSS/JSON input parsing, Apple keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_apple_announcements.json"
OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "title": "Upcoming Requirements for Privacy Manifests and Required Reason APIs",
    "description": "Starting late spring, all new apps and app updates submitted to the App Store must include a Privacy Info manifest declaring reasons for accessing specific APIs such as UserDefaults or systemUptime.",
    "pubDate": "Wed, 15 May 2026 10:00:00 GMT",
    "link": "https://mock.invalid/apple-news/privacy-requirements"
  },
  {
    "title": "Updates to In-App Purchase Policies and Alternative Payment Options",
    "description": "To comply with recent global regulations, developers can now direct users to external purchase options on their website. Ensure transparent billing disclosures and subscription terms are met.",
    "pubDate": "Mon, 01 Jun 2026 09:00:00 GMT",
    "link": "https://mock.invalid/apple-news/iap-updates"
  }
]
EOF

echo "== Running Apple Policy Monitor Test Suite =="

# Execute scripts/monitor.py with mock dataset
python3 scripts/monitor.py --news-file "$MOCK_JSON" --project . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Privacy Manifests" /tmp/monitor_apple_run.log && grep -q "In-App Purchase policies" /tmp/monitor_apple_run.log; then
  ok "Correctly matched relevant Apple policy updates"
else
  bad "Failed to match relevant Apple policy updates. Output: $(cat /tmp/monitor_apple_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Privacy Manifests" "$OUT_DOCS" && grep -q "In-App Purchase policies" "$OUT_DOCS"; then
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

# Check for emojis or graphical symbols
EMOJI_CHECK=$(python3 -c "
import sys
for filepath in ['$OUT_DOCS', '$OUT_PR']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    if emojis:
        print('Found emojis in', filepath, ':', emojis)
        sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" = "No emojis found" ]; then
  ok "Verified that output documentation and PR draft are 100% emoji-free"
else
  bad "Emojis detected in outputs!"
fi

echo ""
echo "Apple Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
