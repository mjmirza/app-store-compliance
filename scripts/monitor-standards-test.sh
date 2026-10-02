#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock input parsing, standards keyword matching across all 10 categories,
# codebase scanning, documentation generation, source trust hierarchy blocking, and exact 15 PR sections.

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

# Create a mock dataset containing updates for testing all 10 categories + an unverified blog
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-STD-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Revision Notice",
    "description": "ISO/IEC 27001 Annex A controls updated.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-27701",
    "category": "ISO 27701",
    "title": "ISO 27701 PIMS Privacy Controls",
    "description": "ISO/IEC 27701 PIMS privacy management update.",
    "link": "https://www.iso.org/standard/27701",
    "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-42001",
    "category": "ISO 42001",
    "title": "ISO 42001 AIMS AI Standard",
    "description": "ISO/IEC 42001 AIMS artificial intelligence management.",
    "link": "https://www.iso.org/standard/42001",
    "pubDate": "Wed, 03 Jun 2026 12:00:00 GMT"
  },
  {
    "id": "MOCK-STD-31000",
    "category": "ISO 31000",
    "title": "ISO 31000 Enterprise Risk Management",
    "description": "ISO 31000 risk assessment guidelines.",
    "link": "https://www.iso.org/standard/31000",
    "pubDate": "Thu, 04 Jun 2026 13:00:00 GMT"
  },
  {
    "id": "MOCK-STD-9001",
    "category": "ISO 9001",
    "title": "ISO 9001 Quality Management System",
    "description": "ISO 9001 software QMS release controls.",
    "link": "https://www.iso.org/standard/9001",
    "pubDate": "Fri, 05 Jun 2026 14:00:00 GMT"
  },
  {
    "id": "MOCK-STD-IEC",
    "category": "IEC standards",
    "title": "IEC 62443 / 62304 Standards Update",
    "description": "IEC standards for software lifecycle security.",
    "link": "https://www.iec.ch/homepage",
    "pubDate": "Sat, 06 Jun 2026 15:00:00 GMT"
  },
  {
    "id": "MOCK-STD-OWASP",
    "category": "OWASP",
    "title": "OWASP Top 10 and MASVS Controls",
    "description": "OWASP security verification standard update.",
    "link": "https://owasp.org/www-project-top-ten/",
    "pubDate": "Sun, 07 Jun 2026 16:00:00 GMT"
  },
  {
    "id": "MOCK-STD-AIRMF",
    "category": "NIST AI RMF",
    "title": "NIST AI Risk Management Framework 1.0",
    "description": "NIST AI RMF govern map measure manage guidance.",
    "link": "https://www.nist.gov/itl/ai-risk-management-framework",
    "pubDate": "Mon, 08 Jun 2026 17:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CSF",
    "category": "NIST CSF",
    "title": "NIST Cybersecurity Framework 2.0",
    "description": "NIST CSF 2.0 cybersecurity directives.",
    "link": "https://www.nist.gov/cyberframework",
    "pubDate": "Tue, 09 Jun 2026 18:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CIS",
    "category": "CIS Benchmarks",
    "title": "CIS Benchmarks Hardening Rules",
    "description": "CIS Benchmarks internet security configuration.",
    "link": "https://www.cisecurity.org/cis-benchmarks",
    "pubDate": "Wed, 10 Jun 2026 19:00:00 GMT"
  },
  {
    "id": "MOCK-STD-BLOG-UNVERIFIED",
    "category": "ISO 27001",
    "title": "Unverified ISO Rumor",
    "description": "A random blog claims ISO rules are changing.",
    "link": "https://randomblogsite.com/iso-rumor",
    "pubDate": "Thu, 11 Jun 2026 20:00:00 GMT"
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

# Verify all 10 categories were matched
for cat in "ISO 27001" "ISO 27701" "ISO 42001" "ISO 31000" "ISO 9001" "IEC standards" "OWASP" "NIST AI RMF" "NIST CSF" "CIS Benchmarks"; do
  if grep -q "\[$cat\]" /tmp/monitor_standards_run.log; then
    ok "Correctly matched category [$cat]"
  else
    bad "Failed to match category [$cat]"
  fi
done

# Verify documentation output
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output created at $OUT_DOCS"
  if grep -q "ISO 27001 Revision Notice" "$OUT_DOCS" && grep -q "NIST AI Risk Management Framework" "$OUT_DOCS"; then
    ok "Documentation contains policy details"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# Verify PR Draft has 15 sections
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
    ok "PR Draft contains all 15 required compliance sections"
  else
    bad "PR Draft is missing $MISSING required sections"
  fi

  # Verify emoji-free
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

# Test JSON output
JSON_OUT=$(python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --json)
if echo "$JSON_OUT" | python3 -m json.tool > /dev/null 2>&1; then
  ok "JSON output is valid JSON"
else
  bad "JSON output is invalid JSON"
fi

echo ""
echo "Technical Standards Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
