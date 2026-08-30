#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies mock RSS input parsing, 25 Apple developer requirement category keyword matching,
# codebase scanning, documentation generation, exact 15 required PR draft sections, and emoji-free compliance.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"

OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

cleanup() {
  rm -f "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Apple Developer Requirements Monitor Test Suite =="

# 1. Verification of help output
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"

# 2. Execution of monitor with mock dataset
$MONITOR --mock --project . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py --mock failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor.py --mock ran successfully with exit code 0"

# 3. Verify documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Apple Developer Requirements Policy Migration" "$OUT_DOCS"; then
    ok "Documentation contains header and matched requirements"
  else
    bad "Documentation is missing header"
  fi
else
  bad "Documentation file was not created"
fi

# 4. Verify PR Draft contains EXACTLY 15 required sections
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

# 5. Simulate all 25 tracks to verify full coverage
OUT_SIM="$($MONITOR --simulate "all" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" 2>&1)"
TRACK_COUNT=$(echo "$OUT_SIM" | grep -c "TRACK UPDATE:" || true)
if [ "$TRACK_COUNT" -eq 25 ]; then
  ok "Simulating all 25 Apple developer requirement tracks matches all 25 categories"
else
  bad "Simulating all tracks matched $TRACK_COUNT tracks instead of 25"
fi

# 6. JSON output format verification
JSON_OUT="$($MONITOR --simulate "Privacy Manifests" --json 2>&1)"
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Privacy Manifests'" 2>/dev/null && ok "json output format is valid JSON and contains matched track" || bad "json output"

# 7. Repository scanning verification
T=$(mktemp -d)
mkdir -p "$T/Sources"
printf "import StoreKit\nlet p = Product.purchase()" > "$T/Sources/IAPService.swift"

OUT_SCAN="$($MONITOR --project "$T" --simulate "In-App Purchase policies" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/IAPService.swift" && ok "repo scanner correctly identifies affected source file" || bad "repo scanner affected file"
rm -rf "$T"

# 8. Assert no emojis are present in outputs or scripts
echo "Checking for emojis in scripts and generated files..."
has_emojis() {
  python3 -c "
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
import re
emojis = re.findall(r'[\U00010000-\U0010ffff]', text)
if emojis:
    print('Found emojis in', sys.argv[1], ':', emojis)
    sys.exit(1)
sys.exit(0)
" "$1"
}

if has_emojis "$HERE/monitor.py" && \
   has_emojis "$OUT_DOCS" && \
   has_emojis "$OUT_PR"; then
  ok "All scripts and generated markdown files are 100% emoji-free"
else
  bad "Emoji check failed: high-unicode emojis or symbols detected"
fi

echo ""
echo "Apple Developer Requirements Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
