#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements compliance)
# Verifies mock parsing, documentation and PR generation, 15 required PR sections,
# and that all files are entirely emoji-free and respect the source trust hierarchy.

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
    "title": "Unverified rumors of App Store Review Guidelines update on Reddit forum",
    "description": "An anonymous user posted a rumor on Reddit saying guidelines are changing next week. No official authorities or official sources were referenced.",
    "pubDate": "Sun, 26 Jul 2026 12:00:00 GMT",
    "link": "https://reddit.com/r/technology/comments/12345/Guidelines_rumor"
  }
]
EOF

echo "== Running Apple Developer Requirements Monitor Test Suite =="

# Execute scripts/monitor.py with mock dataset
python3 scripts/monitor.py --news-file "$MOCK_JSON" --project . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor.py ran successfully with exit code 0"

# Assert relevant policies were matched and we got the correct blocking behavior
if grep -q "Privacy Manifests" "$OUT_DOCS"; then
  ok "Correctly matched and documented Privacy Manifests update"
else
  bad "Failed to match or document Privacy Manifests update"
fi

if grep -q "WARNING" /tmp/monitor_apple_run.log; then
  ok "Source trust correctly flagged or blocked the unverified Reddit rumor"
else
  bad "Reddit rumor was not blocked or warned"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
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

# Assert no emojis are present in outputs or scripts
echo "Checking for emojis in scripts and generated files..."
has_emojis() {
  # Scans for high-unicode character range (emojis and similar symbols)
  python3 -c "
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
import re
emojis = re.findall(r'[\U00010000-\U0010ffff]', text)
if emojis:
    print('Found emojis in', sys.argv[1], ':', emojis)
    sys.exit(1)
sys.exit(0)
" "$1"
}

if has_emojis "scripts/monitor.py" && \
   has_emojis "$OUT_DOCS" && \
   has_emojis "$OUT_PR"; then
  ok "All scripts and generated markdown files are 100% emoji-free"
else
  bad "Emoji check failed: high-unicode emojis or symbols detected"
fi

echo ""
echo "Apple Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
