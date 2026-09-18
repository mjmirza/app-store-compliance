#!/usr/bin/env bash
# Test suite for monitor.py and Apple developer requirement monitoring
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"
PASS=0; FAIL=0

ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# 1. Verification of help output and CLI arguments
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"
echo "$OUT" | grep -q "\-\-output-docs" && ok "help output contains --output-docs flag" || bad "help --output-docs"
echo "$OUT" | grep -q "\-\-pr-output" && ok "help output contains --pr-output flag" || bad "help --pr-output"
echo "$OUT" | grep -q "\-\-live" && ok "help output contains --live flag" || bad "help --live"

# 2. Simulation of a single track
OUT="$($MONITOR --simulate "Privacy Manifests" 2>&1)"
echo "$OUT" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "simulating a track successfully matches and prints track header" || bad "simulate single track"
echo "$OUT" | grep -q "Proposed Pull Request Details:" && ok "simulating a track generates proposed pull request information" || bad "simulate PR generation"

# 3. Simulate all 25 tracks
OUT="$($MONITOR --simulate "all" 2>&1)"
# Check key tracks in the simulation output
echo "$OUT" | grep -q "TRACK UPDATE: \[In-App Purchase policies\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[DMA compliance changes\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[Swift requirements\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[AI-related App Store policies\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[Child safety requirements\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[HealthKit policies\]" && \
ok "simulating all 25 tracks runs successfully with no crashes and outputs matches" || bad "simulate all tracks"

# 4. JSON output format verification
JSON_OUT="$($MONITOR --simulate "Required Reason APIs" --json 2>&1)"
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Required Reason APIs'" 2>/dev/null && ok "json output format is valid and contains matched track" || bad "json output"

# 5. Repository scanning verification
T=$(mktemp -d)
mkdir -p "$T/Sources"
printf "import SwiftUI\nlet swiftVersion = 6.0\nTask { @MainActor in print(\"async-await\") }" > "$T/Sources/App.swift"

OUT_SCAN="$($MONITOR --project "$T" --simulate "Swift requirements" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/App.swift" && ok "repo scanner correctly identifies affected source file" || bad "repo scanner affected file"

rm -rf "$T"

# 6. Documentation and PR draft file generation test
T_DOCS=$(mktemp)
T_PR=$(mktemp)

$MONITOR --simulate "Privacy Manifests" --output-docs "$T_DOCS" --pr-output "$T_PR" >/dev/null 2>&1

grep -q "Apple Developer Policy & Requirements Migration Report" "$T_DOCS" && ok "--output-docs writes migration report" || bad "--output-docs"
grep -q "Compliance Update: Privacy Manifests" "$T_PR" && ok "--pr-output writes draft PR markdown" || bad "--pr-output"
grep -q "## 1. Summary" "$T_PR" && grep -q "## 15. Approver recommendations" "$T_PR" && ok "PR draft contains standard 15 sections" || bad "PR draft sections"

rm -f "$T_DOCS" "$T_PR"

# 7. Mock announcements fallback or manual trigger
OUT_MOCK="$($MONITOR --mock 2>&1)"
echo "$OUT_MOCK" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "mock announcements fallback runs and matches tracks" || bad "mock announcements"

echo ""
echo "monitor-apple-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
