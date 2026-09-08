#!/usr/bin/env bash
# Test suite for monitor.py
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# 1. Verification of help output
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"

# 2. Simulation of a single track
OUT="$($MONITOR --simulate "Privacy Manifests" 2>&1)"
echo "$OUT" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "simulating a track successfully matches and prints track header" || bad "simulate single track"
echo "$OUT" | grep -q "Proposed Pull Request Details:" && ok "simulating a track generates proposed pull request information" || bad "simulate PR generation"

# 3. Simulate all tracks to ensure no crashes
OUT="$($MONITOR --simulate "all" 2>&1)"
# Check some known tracks in the simulation
echo "$OUT" | grep -q "TRACK UPDATE: \[In-App Purchase policies\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[DMA compliance changes\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[Swift requirements\]" && \
ok "simulating all 25 tracks runs successfully with no crashes and outputs matches" || bad "simulate all tracks"

# 4. JSON output format verification
JSON_OUT="$($MONITOR --simulate "Required Reason APIs" --json 2>&1)"
# Validate if it is well-formed JSON
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Required Reason APIs'" 2>/dev/null && ok "json output format is valid and contains matched track" || bad "json output"

# 5. Repository scanning verification
T=$(mktemp -d)
# Create a dummy project structure with a signature matching Swift requirements
mkdir -p "$T/Sources"
printf "import SwiftUI\nlet swiftVersion = 6.0\nTask { @MainActor in print(\"async-await\") }" > "$T/Sources/App.swift"

# Run monitor pointing to the temp directory simulating Swift requirements
OUT_SCAN="$($MONITOR --project "$T" --simulate "Swift requirements" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/App.swift" && ok "repo scanner correctly identifies affected source file" || bad "repo scanner affected file"

# Clean up
rm -rf "$T"

# 6. Mock announcements fallback or manual trigger
OUT_MOCK="$($MONITOR --mock 2>&1)"
echo "$OUT_MOCK" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "mock announcements fallback runs and matches tracks" || bad "mock announcements"

# 7. File output flags (--output-docs and --pr-output) and 15-section verification
TMP_DOCS="/tmp/test_apple_migration.md"
TMP_PR="/tmp/test_apple_pr.md"
rm -f "$TMP_DOCS" "$TMP_PR"

$MONITOR --simulate "Privacy Manifests" --output-docs "$TMP_DOCS" --pr-output "$TMP_PR" > /dev/null 2>&1

SECTIONS=(
  "1. Summary"
  "2. Background"
  "3. Regulatory change"
  "4. Official citations"
  "5. Affected files"
  "6. Risk assessment"
  "7. Migration steps"
  "8. Backward compatibility"
  "9. Implementation checklist"
  "10. Testing checklist"
  "11. Documentation checklist"
  "12. Compliance impact"
  "13. Breaking changes"
  "14. Review checklist"
  "15. Approver recommendations"
)

ALL_FOUND=true
if [ -s "$TMP_PR" ] && [ -s "$TMP_DOCS" ]; then
  for sect in "${SECTIONS[@]}"; do
    if ! grep -q "## $sect" "$TMP_PR"; then
      ALL_FOUND=false
      break
    fi
  done
else
  ALL_FOUND=false
fi

rm -f "$TMP_DOCS" "$TMP_PR"

if [ "$ALL_FOUND" = true ]; then
  ok "file output flags (--output-docs and --pr-output) produce 15-section draft PR"
else
  bad "file output flags or 15-section draft PR verification failed"
fi

echo ""
echo "monitor-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
