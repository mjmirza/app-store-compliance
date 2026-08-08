#!/usr/bin/env bash
# Test suite for Apple Developer Requirements Monitor (scripts/monitor.py)
# Verifies mock news/simulation input, codebase scanning, file generation,
# presence of exactly 15 required compliance sections in the PR draft,
# and adherence to the strict emoji-free policy.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

cleanup() {
  rm -f "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Apple Developer Requirements Monitor Test Suite =="

# 1. Execute monitor.py in simulation mode to generate documentation and PR drafts
python3 scripts/monitor.py --simulate "Privacy Manifests" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/apple_monitor_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py failed to execute. Log:"
  cat /tmp/apple_monitor_run.log
  exit 1
fi
ok "monitor.py executed successfully in simulation mode"

# 2. Check that the documentation migration report was generated correctly
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Privacy Manifests" "$OUT_DOCS"; then
    ok "Documentation contains details of matched Privacy Manifests update"
  else
    bad "Documentation is missing matched details"
  fi
else
  bad "Documentation file was not created"
fi

# 3. Check that the PR draft was generated and contains exactly 15 required sections
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

# 4. Verify strict emoji-free policy on output files
EMOJI_CHECK=$(python3 -c "
import sys
for path in ['$OUT_DOCS', '$OUT_PR']:
    with open(path, encoding='utf-8') as f:
        text = f.read()
        emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
        if emojis:
            print('Found emojis:', emojis)
            sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  bad "Emojis detected in generated output files!"
  exit 1
fi
ok "All generated Apple compliance files are 100% emoji-free"

# 5. Verify that running monitor.py with --json has suppressed console messages but generated files
rm -f "$OUT_DOCS" "$OUT_PR"
JSON_OUT=$(python3 scripts/monitor.py --simulate "Required Reason APIs" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" --json 2>&1)

if echo "$JSON_OUT" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
  ok "Output is valid JSON when running with --json"
else
  bad "Output is not valid JSON or contains extra log messages when running with --json. Output: $JSON_OUT"
fi

if [ -f "$OUT_DOCS" ] && [ -f "$OUT_PR" ]; then
  ok "Documentation and PR draft were successfully generated in the background when running with --json"
else
  bad "Files were not generated when running with --json"
fi

echo ""
echo "Apple Monitor test suite: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
