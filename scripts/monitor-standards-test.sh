#!/usr/bin/env bash
# Test suite for scripts/monitor-standards.py
# Verifies CLI execution, technical standards classification (ISO 27001, ISO 27701, ISO 42001,
# ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks), codebase scanning,
# documentation generation, exact 15 required PR draft sections, JSON output,
# Source Trust Hierarchy blocking, and strict emoji-free compliance.

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

cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "STD-MOCK-TEST-ISO27001",
    "category": "ISO 27001",
    "title": "ISO 27001 ISMS Controls Guidelines Update",
    "description": "Essential ISMS update requiring enhanced access control and data protection.",
    "link": "https://www.iso.org/standard/27001",
    "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "STD-MOCK-TEST-OWASP",
    "category": "OWASP",
    "title": "OWASP MASVS and Top 10 Verification Standards Update",
    "description": "Updated OWASP standards requiring input validation and secure authentication.",
    "link": "https://owasp.org/www-project-top-ten/",
    "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
  },
  {
    "id": "STD-MOCK-TEST-UNVERIFIED",
    "category": "ISO 27001",
    "title": "Unverified Blog Rumor on ISO Changes",
    "description": "Unverified blog claims ISO changes are happening tomorrow.",
    "link": "https://randomblogsite.com/iso-rumor",
    "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
  }
]
EOF

echo "== Running Technical Standards Policy Monitor Test Suite =="

# 1. Verify script exists
if [ -x "scripts/monitor-standards.py" ]; then
  ok "scripts/monitor-standards.py is executable"
else
  bad "scripts/monitor-standards.py is missing or not executable"
  exit 1
fi

# 2. Help menu execution
if python3 scripts/monitor-standards.py --help > /dev/null; then
  ok "monitor-standards.py --help executed successfully"
else
  bad "monitor-standards.py --help failed"
fi

# 3. Execute monitor with mock dataset
python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_standards_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-standards.py failed with exit code $RC. Output:"
  cat /tmp/monitor_standards_run.log
  exit 1
fi
ok "monitor-standards.py ran successfully with exit code 0"

# 4. Assert relevant policies were matched
if grep -q "ISO 27001 ISMS Controls" /tmp/monitor_standards_run.log && grep -q "OWASP MASVS" /tmp/monitor_standards_run.log; then
  ok "Correctly matched technical standards policy updates"
else
  bad "Failed to match technical standards policy updates. Output: $(cat /tmp/monitor_standards_run.log)"
fi

# 5. Assert documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "ISO 27001 ISMS Controls" "$OUT_DOCS" && grep -q "OWASP MASVS" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# 6. Assert PR Draft contains EXACTLY 15 required sections
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

# 7. Test JSON output
JSON_OUT=$(python3 scripts/monitor-standards.py --mock "$MOCK_JSON" --json)
if echo "$JSON_OUT" | python3 -m json.tool > /dev/null; then
  ok "monitor-standards.py generated valid JSON output"
else
  bad "JSON output of monitor-standards.py is invalid"
fi

# 8. Test Source Trust Hierarchy blocking
UNVERIFIED_MOCK="/tmp/test_unverified_only.json"
cat << 'EOF' > "$UNVERIFIED_MOCK"
[
  {
    "id": "STD-MOCK-UNVERIFIED-ONLY",
    "category": "ISO 27001",
    "title": "Unverified Industry Rumor Post",
    "description": "Unverified post on twitter with fake news.",
    "link": "https://twitter.com/rumor",
    "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
  }
]
EOF

UNVERIFIED_JSON=$(python3 scripts/monitor-standards.py --mock "$UNVERIFIED_MOCK" --json)
if echo "$UNVERIFIED_JSON" | grep -q '"proposed_pull_request": null'; then
  ok "Blocked unverified Priority 5 secondary sources successfully"
else
  bad "Failed to block unverified Priority 5 secondary sources"
fi

rm -f "$UNVERIFIED_MOCK" 2>/dev/null || true

# 9. Verify strict emoji-free policy on outputs and scripts
has_emojis() {
  python3 -c "
import sys, re
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis in', sys.argv[1], ':', emojis)
    sys.exit(1)
sys.exit(0)
" "$1"
}

if has_emojis "scripts/monitor-standards.py" && \
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
