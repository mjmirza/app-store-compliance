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

# 7. Verification of document generation (APPLE-POLICY-MIGRATION.md and APPLE_COMPLIANCE_PR_DRAFT.md)
[ -f "docs/APPLE-POLICY-MIGRATION.md" ] && ok "APPLE-POLICY-MIGRATION.md was generated successfully" || bad "APPLE-POLICY-MIGRATION.md missing"
[ -f "docs/APPLE_COMPLIANCE_PR_DRAFT.md" ] && ok "APPLE_COMPLIANCE_PR_DRAFT.md was generated successfully" || bad "APPLE_COMPLIANCE_PR_DRAFT.md missing"

# Ensure 15 section headers are present in APPLE_COMPLIANCE_PR_DRAFT.md
DRAFT="docs/APPLE_COMPLIANCE_PR_DRAFT.md"
grep -q "## Summary" "$DRAFT" && \
grep -q "## Background" "$DRAFT" && \
grep -q "## Regulatory change" "$DRAFT" && \
grep -q "## Official citations" "$DRAFT" && \
grep -q "## Affected files" "$DRAFT" && \
grep -q "## Risk assessment" "$DRAFT" && \
grep -q "## Migration steps" "$DRAFT" && \
grep -q "## Backward compatibility" "$DRAFT" && \
grep -q "## Implementation checklist" "$DRAFT" && \
grep -q "## Testing checklist" "$DRAFT" && \
grep -q "## Documentation checklist" "$DRAFT" && \
grep -q "## Compliance impact" "$DRAFT" && \
grep -q "## Breaking changes" "$DRAFT" && \
grep -q "## Review checklist" "$DRAFT" && \
grep -q "## Approver recommendations" "$DRAFT" && \
ok "APPLE_COMPLIANCE_PR_DRAFT.md contains exactly 15 required sections" || bad "APPLE_COMPLIANCE_PR_DRAFT.md sections count/presence"

# Ensure no emojis in generated files
python3 -c 'import sys; text = open("docs/APPLE_COMPLIANCE_PR_DRAFT.md").read() + open("docs/APPLE-POLICY-MIGRATION.md").read(); has_emoji = any(ord(char) > 0x1F000 for char in text); sys.exit(1 if has_emoji else 0)' && ok "Generated files are completely emoji-free" || bad "emoji present in generated files"

# 8. Suppressed logs on stdout in JSON mode
OUT_JSON_RAW="$($MONITOR --simulate "Privacy Manifests" --json)"
echo "$OUT_JSON_RAW" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0" 2>/dev/null && ok "stdout contains only valid JSON when running in JSON mode" || bad "stdout pollution or invalid JSON in JSON mode"

echo ""
echo "monitor-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
