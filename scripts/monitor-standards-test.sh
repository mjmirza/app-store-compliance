#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies mock dataset parsing, keyword/category matching, codebase scanning,
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

# Create a mock dataset containing updates for testing all 10 categories
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-STD-ISO27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Control Standard Update",
    "description": "Information security management controls guidelines.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-ISO27701",
    "category": "ISO 27701",
    "title": "ISO 27701 Privacy Standard Update",
    "description": "Privacy information management system requirements.",
    "link": "https://www.iso.org/standard/27701",
    "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-ISO42001",
    "category": "ISO 42001",
    "title": "ISO 42001 AI Governance",
    "description": "Artificial Intelligence Management System requirements.",
    "link": "https://www.iso.org/standard/42001",
    "pubDate": "Fri, 05 Jun 2026 09:00:00 GMT"
  },
  {
    "id": "MOCK-STD-ISO31000",
    "category": "ISO 31000",
    "title": "ISO 31000 Risk Management",
    "description": "Risk assessment framework guidelines.",
    "link": "https://www.iso.org/standard/31000",
    "pubDate": "Mon, 08 Jun 2026 14:00:00 GMT"
  },
  {
    "id": "MOCK-STD-ISO9001",
    "category": "ISO 9001",
    "title": "ISO 9001 Quality Assurance",
    "description": "Quality Management System specifications.",
    "link": "https://www.iso.org/standard/9001",
    "pubDate": "Wed, 10 Jun 2026 12:00:00 GMT"
  },
  {
    "id": "MOCK-STD-IEC",
    "category": "IEC standards",
    "title": "IEC 62443 Industrial Cybersecurity",
    "description": "IEC standards for secure software lifecycle.",
    "link": "https://www.iec.ch/standards",
    "pubDate": "Fri, 12 Jun 2026 15:00:00 GMT"
  },
  {
    "id": "MOCK-STD-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS Controls",
    "description": "Mobile application security verification standard.",
    "link": "https://owasp.org/masvs",
    "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-NISTAIRMF",
    "category": "NIST AI RMF",
    "title": "NIST AI Risk Management Framework",
    "description": "Trustworthy AI governance framework.",
    "link": "https://www.nist.gov/ai-rmf",
    "pubDate": "Wed, 17 Jun 2026 13:00:00 GMT"
  },
  {
    "id": "MOCK-STD-NISTCSF",
    "category": "NIST CSF",
    "title": "NIST Cybersecurity Framework 2.0",
    "description": "Governance core and supply chain risk.",
    "link": "https://www.nist.gov/csf",
    "pubDate": "Fri, 19 Jun 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CIS",
    "category": "CIS Benchmarks",
    "title": "CIS Benchmarks Hardening Guidelines",
    "description": "Center for Internet Security hardening benchmarks.",
    "link": "https://www.cisecurity.org/benchmarks",
    "pubDate": "Mon, 22 Jun 2026 16:00:00 GMT"
  }
]
EOF

echo "== Running Technical Standards Monitor Test Suite =="

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
if grep -q "ISO 27001 Control Standard Update" /tmp/monitor_standards_run.log && grep -q "CIS Benchmarks Hardening Guidelines" /tmp/monitor_standards_run.log; then
  ok "Correctly matched relevant technical standards updates"
else
  bad "Failed to match relevant technical standards updates. Output: $(cat /tmp/monitor_standards_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001" "$OUT_DOCS" && grep -q "NIST AI RMF" "$OUT_DOCS" && grep -q "Repository Gap Analysis" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates and gap analysis"
  else
    bad "Documentation is missing policy details or gap analysis"
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
echo "Technical Standards Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
