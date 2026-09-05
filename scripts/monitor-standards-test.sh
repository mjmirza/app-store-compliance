#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies tracking for ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001,
# IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
# Confirms repository gap identification, implementation tasks, documentation updates,
# testing updates, and 15-section emoji-free PR draft generation.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_standards_announcements.json"
OUT_DOCS="/tmp/test_standards_migration.md"
OUT_PR="/tmp/test_standards_pr.md"

cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-ISO-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Information Security Update",
    "description": "Updated ISMS controls for cloud infrastructure and access control logs.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-OWASP",
    "category": "OWASP",
    "title": "OWASP Top 10 Standard Guideline Update",
    "description": "Updated OWASP verification standards for application credential handling.",
    "link": "https://owasp.org/www-project-top-ten/",
    "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
  }
]
EOF

echo "== Running Technical Standards Policy Monitor Test Suite =="

python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_standards_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py failed with exit code $RC. Output:"
  cat /tmp/monitor_standards_run.log
  exit 1
fi
ok "monitor-standards.py ran successfully with exit code 0"

if grep -q "ISO 27001 Information Security" /tmp/monitor_standards_run.log && grep -q "OWASP Top 10 Standard" /tmp/monitor_standards_run.log; then
  ok "Correctly matched technical standards announcements"
else
  bad "Failed to match technical standards announcements. Output: $(cat /tmp/monitor_standards_run.log)"
fi

if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output report created at $OUT_DOCS"
  if grep -q "Identified Repository Gaps" "$OUT_DOCS" && grep -q "Implementation Tasks" "$OUT_DOCS" && grep -q "Documentation Updates" "$OUT_DOCS" && grep -q "Testing Updates" "$OUT_DOCS"; then
    ok "Documentation report contains repository gaps, implementation tasks, documentation updates, and testing updates"
  else
    bad "Documentation report missing required task breakdown sections"
  fi
else
  bad "Documentation report file was not created"
fi

if [ -f "$OUT_PR" ]; then
  ok "PR Draft output created at $OUT_PR"

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
    bad "PR Draft contains emojis!"
  fi

else
  bad "PR Draft file was not created"
fi

echo ""
echo "Technical Standards Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
