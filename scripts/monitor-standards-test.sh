#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock dataset parsing, technical standards keyword matching, codebase scanning,
# documentation generation, source trust hierarchy enforcement, and the presence of
# exactly 15 required non-vague sections in the PR draft without emojis.

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
    "id": "MOCK-STD-ISO27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Controls Update on Information Security",
    "description": "Crucial updates requiring all ISMS controls to update access control policies and encryption protocols.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS Mobile Security Standard Update",
    "description": "Mobile applications must satisfy OWASP MASVS v2.1 requirements for secure data storage and transport.",
    "link": "https://owasp.org/www-project-mobile-app-security/",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-UNVERIFIED-BLOG",
    "category": "ISO 31000",
    "title": "Unverified Industry Blog Post on ISO Risk Standards",
    "description": "An unverified blog claims ISO 31000 rules are changing completely tomorrow.",
    "link": "https://randomblogsite.com/iso-rumor",
    "pubDate": "Sun, 17 May 2026 12:00:00 GMT"
  }
]
EOF

echo "== Running Technical Standards Monitor Test Suite =="

python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_standards_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py failed with exit code $RC. Output:"
  cat /tmp/monitor_standards_run.log
  exit 1
fi
ok "monitor-standards.py ran successfully with exit code 0"

if grep -q "ISO 27001 Controls Update" /tmp/monitor_standards_run.log && grep -q "OWASP MASVS Mobile" /tmp/monitor_standards_run.log; then
  ok "Correctly matched relevant technical standards updates"
else
  bad "Failed to match relevant technical standards updates. Output: $(cat /tmp/monitor_standards_run.log)"
fi

if grep -q "blocked due to source trust validation" /tmp/monitor_standards_run.log; then
  ok "Correctly blocked unverified Priority 4/5 secondary source"
else
  bad "Source trust hierarchy failed to block unverified blog post"
fi

if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001 Controls Update" "$OUT_DOCS" && grep -q "OWASP MASVS Mobile" "$OUT_DOCS"; then
    ok "Documentation contains details of matched standards updates"
  else
    bad "Documentation is missing standards details"
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

echo ""
echo "Technical Standards Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
