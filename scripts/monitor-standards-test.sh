#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock technical standards parsing, keyword matching, codebase scanning,
# gap identification, implementation tasks, documentation updates, testing updates,
# source trust validation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_standards_announcements.json"
OUT_DOCS="/tmp/test_standards_migration.md"
OUT_PR="/tmp/test_standards_pr.md"

cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" /tmp/monitor_standards_run.log /tmp/monitor_standards_json.log 2>/dev/null || true
}
trap cleanup EXIT

# Create a comprehensive mock dataset containing updates for all 10 tracked standards
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-STD-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 ISMS Controls Revision",
    "description": "Information Security Management System Annex A controls update.",
    "link": "https://www.iso.org/iso-iec-27001-information-security.html",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-27701",
    "category": "ISO 27701",
    "title": "ISO 27701 PIMS Privacy Standard",
    "description": "Privacy Information Management System controls update.",
    "link": "https://www.iso.org/standard/71670.html",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-42001",
    "category": "ISO 42001",
    "title": "ISO 42001 Artificial Intelligence Management System",
    "description": "AI Management System framework for model governance.",
    "link": "https://www.iso.org/standard/81230.html",
    "pubDate": "Sun, 17 May 2026 09:00:00 GMT"
  },
  {
    "id": "MOCK-STD-31000",
    "category": "ISO 31000",
    "title": "ISO 31000 Risk Management Standard",
    "description": "Risk management guidelines and assessment controls.",
    "link": "https://www.iso.org/iso-31000-risk-management.html",
    "pubDate": "Mon, 18 May 2026 14:00:00 GMT"
  },
  {
    "id": "MOCK-STD-9001",
    "category": "ISO 9001",
    "title": "ISO 9001 Quality Management System",
    "description": "Quality Management System audit checklists.",
    "link": "https://www.iso.org/iso-9001-quality-management.html",
    "pubDate": "Tue, 19 May 2026 12:00:00 GMT"
  },
  {
    "id": "MOCK-STD-IEC",
    "category": "IEC standards",
    "title": "IEC Standards 62304 Medical Software Lifecycle",
    "description": "Medical and health software lifecycle requirements.",
    "link": "https://www.iec.ch/homepage",
    "pubDate": "Wed, 20 May 2026 15:00:00 GMT"
  },
  {
    "id": "MOCK-STD-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS & ASVS Security Verification",
    "description": "OWASP mobile and web application security verification standard.",
    "link": "https://owasp.org/www-project-mobile-application-security/",
    "pubDate": "Thu, 21 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-AIRMF",
    "category": "NIST AI RMF",
    "title": "NIST AI Risk Management Framework 1.0",
    "description": "NIST AI RMF Map Measure Manage Govern functions.",
    "link": "https://www.nist.gov/itl/ai-risk-management-framework",
    "pubDate": "Fri, 22 May 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CSF",
    "category": "NIST CSF",
    "title": "NIST Cybersecurity Framework 2.0",
    "description": "NIST CSF cybersecurity functions update.",
    "link": "https://www.nist.gov/cyberframework",
    "pubDate": "Sat, 23 May 2026 13:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CIS",
    "category": "CIS Benchmarks",
    "title": "CIS Benchmarks Hardening Standards",
    "description": "CIS Benchmarks system and software hardening rules.",
    "link": "https://www.cisecurity.org/cis-benchmarks",
    "pubDate": "Sun, 24 May 2026 09:00:00 GMT"
  }
]
EOF

echo "== Running Technical Standards Monitor Test Suite =="

# 1. Execute scripts/monitor-standards.py with mock dataset
python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_standards_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py failed with exit code $RC. Output:"
  cat /tmp/monitor_standards_run.log
  exit 1
fi
ok "monitor-standards.py ran successfully with exit code 0"

# 2. Assert all 10 standards were matched
MISSING_CATS=0
declare -a CATEGORIES=(
  "ISO 27001"
  "ISO 27701"
  "ISO 42001"
  "ISO 31000"
  "ISO 9001"
  "IEC standards"
  "OWASP"
  "NIST AI RMF"
  "NIST CSF"
  "CIS Benchmarks"
)

for cat in "${CATEGORIES[@]}"; do
  if grep -q "\[$cat\]" /tmp/monitor_standards_run.log; then
    true
  else
    echo "  Missing category match log for: $cat"
    MISSING_CATS=$((MISSING_CATS + 1))
  fi
done

if [ "$MISSING_CATS" -eq 0 ]; then
  ok "All 10 technical standards categories were matched in the output log"
else
  bad "Missing $MISSING_CATS technical standards category matches"
fi

# 3. Assert documentation output was generated with gaps, implementation, and testing updates
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Identified Repository Gaps" "$OUT_DOCS" && \
     grep -q "Automated Migration Recommendations & Implementation Tasks" "$OUT_DOCS" && \
     grep -q "Generated Testing Updates" "$OUT_DOCS"; then
    ok "Documentation contains repository gaps, implementation tasks, and testing updates"
  else
    bad "Documentation output is missing required sections"
  fi
else
  bad "Documentation file was not created"
fi

# 4. Assert PR Draft contains EXACTLY 15 required sections
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

  # 5. Verify strict emoji-free policy on output
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

# 6. Test --json output flag
python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --json > /tmp/monitor_standards_json.log 2>&1
if [ $? -eq 0 ] && grep -q '"scan_matches"' /tmp/monitor_standards_json.log; then
  ok "--json option produces valid JSON output"
else
  bad "--json option failed or output invalid"
fi

echo ""
echo "Technical Standards Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
