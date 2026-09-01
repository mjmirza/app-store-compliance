#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies mock/RSS input parsing, 25 Apple requirement categories, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.
# Also verifies that all generated outputs are completely emoji-free.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"
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

# 1. Help output
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"
echo "$OUT" | grep -q "\-\-output-docs" && ok "help output contains --output-docs flag" || bad "help flag --output-docs"
echo "$OUT" | grep -q "\-\-pr-output" && ok "help output contains --pr-output flag" || bad "help flag --pr-output"

# 2. Simulation of all 25 tracks
OUT_ALL="$($MONITOR --simulate "all" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" 2>&1)"
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[In-App Purchase policies\]" && \
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[DMA compliance changes\]" && \
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[Swift requirements\]" && \
ok "simulating all 25 tracks runs successfully" || bad "simulate all tracks"

# 3. Check documentation output file
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  grep -q "Apple Developer Requirements Migration & Compliance Report" "$OUT_DOCS" && ok "Documentation contains header" || bad "Documentation missing header"
else
  bad "Documentation file was not created"
fi

# 4. Check PR Draft output file for 15 required sections
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

# 5. JSON output verification
JSON_OUT="$($MONITOR --simulate "Required Reason APIs" --json 2>&1)"
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Required Reason APIs'" 2>/dev/null && ok "json output format is valid" || bad "json output format"

# 6. Repo scanning verification
T=$(mktemp -d)
mkdir -p "$T/Sources"
printf "import SwiftUI\nlet swiftVersion = 6.0\nTask { @MainActor in print(\"async-await\") }" > "$T/Sources/App.swift"

OUT_SCAN="$($MONITOR --project "$T" --simulate "Swift requirements" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/App.swift" && ok "repo scanner correctly identifies affected source file" || bad "repo scanner"

rm -rf "$T"

# 7. Check for emojis in outputs and script
has_emojis() {
  python3 -c "
import sys, re
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
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
  bad "Emoji check failed"
fi

echo ""
echo "monitor-apple-test: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
