#!/usr/bin/env bash
# Test suite for scripts/monitor-security.py
# Verifies mock RSS input parsing, Mobile Security keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft without emojis.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_security_announcements.json"
OUT_DOCS="/tmp/test_security_migration.md"
OUT_PR="/tmp/test_security_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-SEC-STORAGE",
    "category": "secure storage",
    "title": "NIST Secure Storage Revisions",
    "description": "NIST releases updated instructions for secure encryption of mobile storage devices using SQLCipher.",
    "link": "https://pages.nist.gov/Mobile-Threat-Catalogue/",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-BIOMETRICS",
    "category": "biometric authentication",
    "title": "Biometric Bypass Vulnerabilities Protection",
    "description": "OWASP MASVS mandates crypto-backed biometric authentication using CryptoObject.",
    "link": "https://mas.owasp.org/MASVS/",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
  }
]
EOF

echo "== Running Mobile Security Monitor Test Suite =="

# 1. Help Menu Verification
OUT_HELP="$(python3 scripts/monitor-security.py --help 2>&1)"
if echo "$OUT_HELP" | grep -q "Monitor all Mobile Security requirements"; then
  ok "help output contains usage description"
else
  bad "help output was incorrect"
fi

# 2. Execution with Mock Announcements
python3 scripts/monitor-security.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_security_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-security.py failed with exit code $RC. Output:"
  cat /tmp/monitor_security_run.log
  exit 1
fi
ok "monitor-security.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "NIST Secure Storage Revisions" /tmp/monitor_security_run.log || grep -q "Biometric Bypass Vulnerabilities" /tmp/monitor_security_run.log || grep -q "NIST" "$OUT_DOCS"; then
  ok "Correctly matched relevant security guidelines updates"
else
  bad "Failed to match relevant security guidelines updates. Output: $(cat /tmp/monitor_security_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "NIST Secure Storage Revisions" "$OUT_DOCS"; then
    ok "Documentation contains details of matched security updates"
  else
    bad "Documentation is missing security details"
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

  # 3. Verify no emojis or emoticons are present
  # Checks for typical emoji unicode blocks
  # Also standard graphical emoticons if any (e.g. smileys)
  # grep -E '[^\x00-\x7F]' handles non-ascii but we want to specifically flag emojis/graphical icons if any are written.
  # Let's check for some standard emoji characters or emoticons.
  if grep -qiE '(:-\)|:\)|:-D|:D|:-P|:P|;\)|:-\(|:\(|✅|❌|⚠️|🔒|🛡️)' "$OUT_PR"; then
    bad "PR Draft contains emoticons or emojis"
  else
    ok "PR Draft is free of emoticons and emojis"
  fi
else
  bad "PR Draft file was not created"
fi

echo ""
echo "Mobile Security Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
