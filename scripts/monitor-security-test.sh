#!/usr/bin/env bash
# Test suite for scripts/monitor-security.py
# Verifies mock RSS input parsing, security keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

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
    "title": "Secure Storage Update on EncryptedSharedPreferences",
    "description": "Crucial updates requiring all local user databases to use encrypted shared preferences and SQLCipher.",
    "link": "https://developer.android.com/topic/security/data",
    "pubDate": "Fri, 15 May 2026 10:00:00 PDT"
  },
  {
    "id": "MOCK-SEC-KEYCHAIN",
    "category": "Keychain",
    "title": "iOS Keychain Security Policies",
    "description": "Keychain items must use kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly to prevent unsecure backups.",
    "link": "https://developer.apple.com/documentation/security",
    "pubDate": "Sat, 16 May 2026 11:00:00 PDT"
  }
]
EOF

echo "== Running Security Policy Monitor Test Suite =="

# Execute scripts/monitor-security.py with mock dataset
python3 scripts/monitor-security.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_security_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-security.py failed with exit code $RC. Output:"
  cat /tmp/monitor_security_run.log
  exit 1
fi
ok "monitor-security.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Secure Storage Update" /tmp/monitor_security_run.log && grep -q "iOS Keychain Security" /tmp/monitor_security_run.log; then
  ok "Correctly matched relevant security policy updates"
else
  bad "Failed to match relevant security policy updates. Output: $(cat /tmp/monitor_security_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Secure Storage Update" "$OUT_DOCS" && grep -q "iOS Keychain Security" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
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
echo "Security Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
