#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock RSS input parsing, standards keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_standards_announcements.json"
OUT_DOCS="/tmp/test_standards_migration.md"
OUT_PR="/tmp/test_standards_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-STAND-ISO-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 ISMS Standard Update on Information Security Controls",
    "description": "Crucial updates requiring all local ISMS controls to align with new Annex A standards.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 15 Jun 2026 10:00:00 UTC"
  },
  {
    "id": "MOCK-STAND-ISO-27701",
    "category": "ISO 27701",
    "title": "ISO 27701 Privacy Information Management System Requirements",
    "description": "ISO/IEC 27701 specifies requirements for PIMS.",
    "link": "https://www.iso.org/standard/27701",
    "pubDate": "Tue, 16 Jun 2026 11:00:00 UTC"
  },
  {
    "id": "MOCK-STAND-UNVERIFIED-BLOG",
    "category": "ISO 27001",
    "title": "Unverified Industry Blog Rumors on ISO 27001 Fines",
    "description": "A random tech blog claims ISO 27001 rules are being changed next week. This is an unverified blog post.",
    "link": "https://randomblogsite.com/iso-rumor",
    "pubDate": "Wed, 01 Jul 2026 11:00:00 PDT"
  }
]
EOF

echo "== Running Technical Standards Policy Monitor Test Suite =="

# Execute scripts/monitor-standards.py with mock dataset
python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_standards_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py failed with exit code $RC. Output:"
  cat /tmp/monitor_standards_run.log
  exit 1
fi
ok "monitor-standards.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "ISO 27001 ISMS Standard Update" /tmp/monitor_standards_run.log && grep -q "ISO 27701 Privacy Information" /tmp/monitor_standards_run.log; then
  ok "Correctly matched relevant standards policy updates"
else
  bad "Failed to match relevant standards policy updates. Output: $(cat /tmp/monitor_standards_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001 ISMS Standard Update" "$OUT_DOCS" && grep -q "ISO 27701 Privacy Information" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# Assert that unverified blog posts are marked as BLOCKED in the documentation tasks
if grep -q "BLOCKED: Announcement source is unverified" "$OUT_DOCS"; then
  ok "Source trust check correctly marked unverified sources as BLOCKED in documentation tasks"
else
  bad "Failed to block unverified sources in documentation"
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

  # Verify that the unverified blog post is NOT included in the PR draft's Official citations or updates (it should be blocked)
  if grep -q "Unverified Industry Blog Rumors" "$OUT_PR"; then
    bad "PR Draft contains unverified secondary source information!"
  else
    ok "PR Draft successfully excluded unverified secondary sources"
  fi

  # Verify strict emoji-free policy on output
  EMOJI_CHECK=$(python3 -c "
import sys
with open('$OUT_PR', 'r', encoding='utf-8') as f:
    text = f.read()
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
    sys.exit(1)
print('No emojis found')
")

  if [ "$EMOJI_CHECK" = "No emojis found" ]; then
    ok "PR Draft is 100% emoji-free"
  else
    bad "PR Draft has emojis!"
  fi

else
  bad "PR Draft file was not created"
fi

# Test --json mode output format
JSON_OUT=$(python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --json 2>/tmp/monitor_standards_json_err.log)
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py with --json option failed with exit code $RC"
else
  # Verify if JSON_OUT is valid JSON
  VALID_JSON=$(echo "$JSON_OUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Valid JSON')
except Exception as e:
    print('Invalid:', e)
    sys.exit(1)
")
  if [ "$VALID_JSON" = "Valid JSON" ]; then
    ok "monitor-standards.py --json outputs valid JSON"
  else
    bad "monitor-standards.py --json outputs invalid JSON!"
  fi
fi

# Verify no progress logs were written to stdout when in --json mode
if [ -n "$JSON_OUT" ] && ! echo "$JSON_OUT" | grep -q "Scanning codebase"; then
  ok "No progress logs written to stdout when in --json mode"
else
  bad "Progress logs or non-JSON output leaked to stdout in --json mode"
fi

echo ""
echo "Technical Standards Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
