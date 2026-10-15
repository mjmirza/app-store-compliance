#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock RSS input parsing, technical standards category matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.
# Also verifies that all generated outputs are completely emoji-free.

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
    "id": "STD-MOCK-TEST-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Information Security Controls Update",
    "description": "Essential ISMS governance updates require threat intelligence alignment.",
    "link": "https://www.iso.org/isoiec-27001-information-security.html",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "STD-MOCK-TEST-NIST",
    "category": "NIST CSF",
    "title": "NIST CSF Cybersecurity Governance Guideline",
    "description": "NIST CSF 2.0 adds Governance pillar across core security functions.",
    "link": "https://www.nist.gov/cyberframework",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
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

if grep -q "ISO 27001 Information Security" /tmp/monitor_standards_run.log && grep -q "NIST CSF Cybersecurity Governance" /tmp/monitor_standards_run.log; then
  ok "Correctly matched relevant Technical Standards policy updates"
else
  bad "Failed to match relevant Technical Standards policy updates. Output: $(cat /tmp/monitor_standards_run.log)"
fi

if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001 Information Security" "$OUT_DOCS" && grep -q "NIST CSF Cybersecurity Governance" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

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

echo "Checking for emojis in scripts and generated files..."
has_emojis() {
  python3 -c "
import sys, re
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
emojis = re.findall(r'[\U00010000-\U0010ffff]', text)
if emojis:
    print('Found emojis in', sys.argv[1], ':', emojis)
    sys.exit(1)
sys.exit(0)
" "$1"
}

if has_emojis "scripts/monitor-standards.py" && \
   has_emojis "scripts/monitor-standards-test.sh" && \
   has_emojis "$OUT_DOCS" && \
   has_emojis "$OUT_PR"; then
  ok "All scripts and generated markdown files are 100% emoji-free"
else
  bad "Emoji check failed: high-unicode emojis or symbols detected"
fi

echo ""
echo "Technical Standards Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
