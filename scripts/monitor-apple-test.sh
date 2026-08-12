#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies Apple keyword matching, codebase scanning, documentation generation,
# emoji-free validation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Apple Policy Monitor Test Suite =="

# Execute scripts/monitor.py with mock dataset
python3 scripts/monitor.py --mock --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Privacy Manifests" "$OUT_DOCS" && grep -q "In-App Purchase" "$OUT_DOCS"; then
  ok "Correctly matched relevant Apple policy updates"
else
  bad "Failed to match relevant Apple policy updates."
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
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
else
  bad "PR Draft file was not created"
fi

# Check for emojis in the generated files and monitor.py
echo "Checking for emojis in scripts and generated files..."
if grep -q -P "[^\x00-\x7F]" "$OUT_DOCS" "$OUT_PR" scripts/monitor.py; then
  bad "Found non-ASCII or potential emoji characters in monitor.py or generated files"
else
  ok "All scripts and generated markdown files are 100% emoji-free"
fi

# Verify JSON output suppresses file generation status logs and remains valid JSON
JSON_OUT=$(python3 scripts/monitor.py --mock --json --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" 2>/dev/null)
if echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0" 2>/dev/null; then
  ok "JSON output mode is valid and suppresses logs to preserve clean JSON stdout"
else
  bad "JSON output is invalid or contains unexpected logs/characters"
fi

echo ""
echo "Apple Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
