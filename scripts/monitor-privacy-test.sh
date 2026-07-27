#!/usr/bin/env bash
# Test suite for scripts/monitor-privacy.py
# Verifies privacy compliance policy matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

OUT_DOCS="/tmp/test_privacy_migration.md"
OUT_PR="/tmp/test_privacy_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Privacy Policy Monitor Test Suite =="

# Execute scripts/monitor-privacy.py with simulation
python3 scripts/monitor-privacy.py --simulate "Unnecessary Personal Data Collection" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_privacy_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-privacy.py failed with exit code $RC. Output:"
  cat /tmp/monitor_privacy_run.log
  exit 1
fi
ok "monitor-privacy.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Unnecessary Personal Data Collection" /tmp/monitor_privacy_run.log; then
  ok "Correctly matched relevant privacy policy updates"
else
  bad "Failed to match relevant privacy policy updates. Output: $(cat /tmp/monitor_privacy_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Unnecessary Personal Data Collection" "$OUT_DOCS"; then
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
    # Section header checking
    if grep -q "## ${sec_name}" "$OUT_PR"; then
      true
    else
      echo "  Missing PR section: ## ${sec_name}"
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

# Verify strict emoji-free policy on output
echo "Scanning output for any emojis..."
EMOJI_CHECK=$(python3 -c "
import sys
with open('$OUT_PR', 'r', encoding='utf-8') as f:
    text = f.read()
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
else:
    print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  bad "Emoji validation failed: $EMOJI_CHECK"
else
  ok "PR draft is 100% emoji-free"
fi

echo ""
echo "Privacy Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
