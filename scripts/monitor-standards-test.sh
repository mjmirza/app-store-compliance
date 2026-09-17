#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies technical standards updates across all 10 categories, codebase scanning,
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
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" /tmp/monitor_standards_run.log 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset covering all 10 technical standards
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-STD-27001",
    "category": "ISO 27001",
    "title": "ISO 27001 Information Security Update",
    "description": "Mandates access control and encryption at rest controls.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 18 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-27701",
    "category": "ISO 27701",
    "title": "ISO 27701 Privacy Information Management Update",
    "description": "Requires automated PII data mapping and consent controls.",
    "link": "https://www.iso.org/standard/27701",
    "pubDate": "Wed, 20 May 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-42001",
    "category": "ISO 42001",
    "title": "ISO 42001 AI Management System Update",
    "description": "Establishes AI impact assessment and model monitoring guidelines.",
    "link": "https://www.iso.org/standard/42001",
    "pubDate": "Fri, 22 May 2026 12:00:00 GMT"
  },
  {
    "id": "MOCK-STD-31000",
    "category": "ISO 31000",
    "title": "ISO 31000 Risk Management Guidelines Update",
    "description": "Requires formal risk matrices and risk treatment plans.",
    "link": "https://www.iso.org/standard/31000",
    "pubDate": "Mon, 25 May 2026 09:00:00 GMT"
  },
  {
    "id": "MOCK-STD-9001",
    "category": "ISO 9001",
    "title": "ISO 9001 Quality Management System Update",
    "description": "Mandates automated release audits and quality gates.",
    "link": "https://www.iso.org/standard/9001",
    "pubDate": "Wed, 27 May 2026 14:00:00 GMT"
  },
  {
    "id": "MOCK-STD-IEC",
    "category": "IEC standards",
    "title": "IEC 62304 / IEC 82304 Lifecycle Standards Update",
    "description": "Software lifecycle hazard analysis and safety class requirements.",
    "link": "https://www.iec.ch/",
    "pubDate": "Fri, 29 May 2026 15:00:00 GMT"
  },
  {
    "id": "MOCK-STD-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS and LLM Top 10 Security Update",
    "description": "OWASP mobile and generative AI safety guidelines.",
    "link": "https://owasp.org/",
    "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-STD-NISTAIRMF",
    "category": "NIST AI RMF",
    "title": "NIST AI Risk Management Framework 1.0 Update",
    "description": "NIST AI RMF core functions: Govern, Map, Measure, Manage.",
    "link": "https://www.nist.gov/itl/ai-risk-management-framework",
    "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT"
  },
  {
    "id": "MOCK-STD-NISTCSF",
    "category": "NIST CSF",
    "title": "NIST Cybersecurity Framework CSF 2.0 Update",
    "description": "NIST CSF 2.0 Govern function and supply chain security.",
    "link": "https://www.nist.gov/cyberframework",
    "pubDate": "Fri, 05 Jun 2026 13:00:00 GMT"
  },
  {
    "id": "MOCK-STD-CIS",
    "category": "CIS Benchmarks",
    "title": "CIS Benchmarks Hardening Standards Update",
    "description": "CIS Controls and Level 1/2 hardening profiles.",
    "link": "https://www.cisecurity.org/",
    "pubDate": "Mon, 08 Jun 2026 14:00:00 GMT"
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

# Assert all 10 standards were matched
STANDARDS_MATCHED=0
for std in "ISO 27001" "ISO 27701" "ISO 42001" "ISO 31000" "ISO 9001" "IEC standards" "OWASP" "NIST AI RMF" "NIST CSF" "CIS Benchmarks"; do
  if grep -q "$std" /tmp/monitor_standards_run.log; then
    STANDARDS_MATCHED=$((STANDARDS_MATCHED + 1))
  else
    echo "  Missing standard match: $std"
  fi
done

if [ "$STANDARDS_MATCHED" -eq 10 ]; then
  ok "Matched all 10 tracked technical standards"
else
  bad "Matched only $STANDARDS_MATCHED of 10 tracked technical standards"
fi

# Assert documentation was generated and contains tasks/updates
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Implementation Tasks" "$OUT_DOCS" && grep -q "Documentation Updates" "$OUT_DOCS" && grep -q "Testing Updates" "$OUT_DOCS"; then
    ok "Documentation contains implementation, documentation, and testing updates"
  else
    bad "Documentation is missing task breakdown sections"
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
