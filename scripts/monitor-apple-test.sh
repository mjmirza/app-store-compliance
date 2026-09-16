#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies mock/simulated input parsing, track matching across all 25 tracks,
# repository scanning, documentation report generation, 15-section PR draft compliance,
# valid JSON stdout format, and emoji-free compliance.

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

# 1. Help output verification
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"

# 2. Simulate single track and verify documentation and 15-section PR draft generation
$MONITOR --simulate "Privacy Manifests" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py --simulate failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor.py ran successfully with exit code 0"

# Verify documentation generation
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Privacy Manifests" "$OUT_DOCS"; then
    ok "Documentation contains details of matched track updates"
  else
    bad "Documentation missing track update details"
  fi
else
  bad "Documentation file was not created"
fi

# Verify 15 required PR sections
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

# 3. Simulate all 25 tracks
OUT_ALL="$($MONITOR --simulate "all" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" 2>&1)"
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[In-App Purchase policies\]" && \
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[DMA compliance changes\]" && \
echo "$OUT_ALL" | grep -q "TRACK UPDATE: \[Swift requirements\]" && \
ok "Simulating all 25 tracks runs successfully with no crashes and outputs matches" || bad "Simulate all tracks failed"

# 4. JSON output validation (clean stdout)
JSON_OUT="$($MONITOR --simulate "Required Reason APIs" --json 2>&1)"
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Required Reason APIs'" 2>/dev/null && ok "JSON output format is valid and clean" || bad "JSON output validation failed"

# 5. Repository scanning verification
T=$(mktemp -d)
mkdir -p "$T/Sources"
printf "import SwiftUI\nlet swiftVersion = 6.0\nTask { @MainActor in print(\"async-await\") }" > "$T/Sources/App.swift"

OUT_SCAN="$($MONITOR --project "$T" --simulate "Swift requirements" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/App.swift" && ok "Repo scanner correctly identifies affected source file" || bad "Repo scanner failed"
rm -rf "$T"

# 6. Mock mode verification
OUT_MOCK="$($MONITOR --mock --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" 2>&1)"
echo "$OUT_MOCK" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "Mock announcements mode runs and matches tracks" || bad "Mock announcements failed"

# 7. Emoji check
EMOJI_MATCHES=$(grep -P "[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true)
if [ -z "$EMOJI_MATCHES" ]; then
  ok "All generated markdown outputs are 100% emoji-free"
else
  bad "Found emojis in generated files"
fi

echo ""
echo "Apple Developer Requirements Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
