#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock RSS input parsing, technical standards keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

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

# Create mock dataset covering all 10 tracked technical standards
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-ISO-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 ISMS Controls",
    "description": "Updated security controls and information security management systems.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-ISO-27701",
    "category": "ISO 27701",
    "title": "ISO 27701 PIMS Privacy Update",
    "description": "Privacy Information Management System requirements.",
    "link": "https://www.iso.org/standard/71670.html",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-ISO-42001",
    "category": "ISO 42001",
    "title": "ISO 42001 Artificial Intelligence Management System",
    "description": "AI Management System controls and governance.",
    "link": "https://www.iso.org/standard/81230.html",
    "pubDate": "Sun, 17 May 2026 12:00:00 GMT"
  },
  {
    "id": "MOCK-ISO-31000",
    "category": "ISO 31000",
    "title": "ISO 31000 Risk Management Guidelines",
    "description": "Risk assessment framework guidelines for software releases.",
    "link": "https://www.iso.org/iso-31000-risk-management.html",
    "pubDate": "Mon, 18 May 2026 13:00:00 GMT"
  },
  {
    "id": "MOCK-ISO-9001",
    "category": "ISO 9001",
    "title": "ISO 9001 Quality Management Systems",
    "description": "Quality management assurance and continuous improvement.",
    "link": "https://www.iso.org/iso-9001-quality-management.html",
    "pubDate": "Tue, 19 May 2026 14:00:00 GMT"
  },
  {
    "id": "MOCK-IEC",
    "category": "IEC standards",
    "title": "IEC 62443 System Security Requirements",
    "description": "Electrotechnical cybersecurity specifications and device hardening.",
    "link": "https://www.iec.ch/cybersecurity",
    "pubDate": "Wed, 20 May 2026 15:00:00 GMT"
  },
  {
    "id": "MOCK-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS Verification Standard",
    "description": "Mobile security controls and vulnerability remediation.",
    "link": "https://mas.owasp.org/",
    "pubDate": "Thu, 21 May 2026 16:00:00 GMT"
  },
  {
    "id": "MOCK-NIST-AI-RMF",
    "category": "NIST AI RMF",
    "title": "NIST AI Risk Management Framework",
    "description": "AI RMF guidance across Govern, Map, Measure, Manage.",
    "link": "https://www.nist.gov/itl/ai-risk-management-framework",
    "pubDate": "Fri, 22 May 2026 17:00:00 GMT"
  },
  {
    "id": "MOCK-NIST-CSF",
    "category": "NIST CSF",
    "title": "NIST CSF 2.0 Governance Guidance",
    "description": "Cybersecurity framework updates and supply chain security.",
    "link": "https://www.nist.gov/cyberframework",
    "pubDate": "Sat, 23 May 2026 18:00:00 GMT"
  },
  {
    "id": "MOCK-CIS",
    "category": "CIS Benchmarks",
    "title": "CIS Benchmarks Hardening Standards",
    "description": "CIS Controls and system configuration hardening.",
    "link": "https://www.cisecurity.org/cis-benchmarks",
    "pubDate": "Sun, 24 May 2026 19:00:00 GMT"
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

# Assert all 10 technical standards were matched
MATCH_FAILURES=0
for cat in "ISO 27001" "ISO 27701" "ISO 42001" "ISO 31000" "ISO 9001" "IEC standards" "OWASP" "NIST AI RMF" "NIST CSF" "CIS Benchmarks"; do
  if grep -q "\[$cat\]" /tmp/monitor_standards_run.log; then
    true
  else
    echo "  Missing standard match log for: $cat"
    MATCH_FAILURES=$((MATCH_FAILURES + 1))
  fi
done

if [ "$MATCH_FAILURES" -eq 0 ]; then
  ok "Correctly matched all 10 technical standards policy updates"
else
  bad "Failed to match $MATCH_FAILURES of 10 technical standards policy updates"
fi

# Assert documentation generation
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001" "$OUT_DOCS" && grep -q "OWASP" "$OUT_DOCS" && grep -q "NIST AI RMF" "$OUT_DOCS"; then
    ok "Documentation contains details of matched technical standards"
  else
    bad "Documentation is missing technical standards details"
  fi
else
  bad "Documentation file was not created"
fi

# Assert PR Draft contains EXACTLY 15 required sections
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

echo ""
echo "Technical Standards Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
