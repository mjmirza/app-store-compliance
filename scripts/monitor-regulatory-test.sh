#!/usr/bin/env bash
#
# monitor-regulatory-test.sh
# Tests the Regulatory Intelligence Agent Monitor utility.
# Ensures that correct outputs are generated and strict emoji-free policy is adhered to.
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MON_SCRIPT="$REPO_ROOT/scripts/monitor-regulatory.py"
TMP_DOC_OUTPUT="/tmp/test_regulatory_monitor_report.md"
TMP_PR_OUTPUT="/tmp/test_regulatory_pr_draft.md"

echo "[TEST] Starting Regulatory Intelligence Agent Monitor Test Suite"
echo "Project Path: $REPO_ROOT"
echo "Script Path:  $MON_SCRIPT"
echo ""

# Test 1: Verify monitor-regulatory.py exists and is executable
if [ ! -x "$MON_SCRIPT" ]; then
  echo "[ERROR] monitor-regulatory.py is not executable or not found."
  exit 1
fi
echo "[PASS] monitor-regulatory.py is executable"

# Test 2: Verify help menu executes successfully
python3 "$MON_SCRIPT" --help > /dev/null
echo "[PASS] monitor-regulatory.py --help executed successfully"

# Test 3: Run scan against the repository root and output docs/PR files
echo "[TEST] Running scan against current project directory and validating file creation..."
python3 "$MON_SCRIPT" --project "$REPO_ROOT" --output-docs "$TMP_DOC_OUTPUT" --pr-output "$TMP_PR_OUTPUT" > /dev/null
if [ ! -f "$TMP_DOC_OUTPUT" ]; then
  echo "[ERROR] Documentation report file $TMP_DOC_OUTPUT was not created."
  exit 1
fi
if [ ! -f "$TMP_PR_OUTPUT" ]; then
  echo "[ERROR] PR output file $TMP_PR_OUTPUT was not created."
  exit 1
fi
echo "[PASS] monitor-regulatory.py successfully scanned and created doc and PR files"

# Test 4: Run simulation for EU AI Act and verify output contains the 15 required sections in JSON
echo "[TEST] Simulating 'EU AI Act' track and validating 15-section JSON output..."
EU_JSON=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "EU AI Act" --json)

# Define expected sections
SECTIONS=(
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

for sect in "${SECTIONS[@]}"; do
  # Check if the section header exists as a markdown heading in the description field of the JSON
  if ! echo "$EU_JSON" | grep -q "## $sect"; then
    echo "[ERROR] Missing expected section in output: $sect"
    exit 1
  fi
done
echo "[PASS] All 15 required compliance sections exist in the Pull Request generator output"

# Test 5: Verify JSON output is valid JSON
echo "[TEST] Running JSON output validation..."
JSON_OUT=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "COPPA" --json)
if ! echo "$JSON_OUT" | python3 -m json.tool > /dev/null; then
  echo "[ERROR] JSON output of monitor-regulatory.py is invalid"
  exit 1
fi
echo "[PASS] monitor-regulatory.py generated valid JSON output"

# Test 6: Verify strict emoji-free policy on output
echo "[TEST] Scanning output for any emojis or non-ascii/graphical emoticons..."
EMOJI_CHECK=$(python3 -c "
import sys
for path in ['$TMP_DOC_OUTPUT', '$TMP_PR_OUTPUT']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    if emojis:
        print('Found emojis in ' + path + ':', emojis)
        sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  echo "[ERROR] Emojis detected in generated monitor output!"
  exit 1
fi
echo "[PASS] monitor-regulatory.py output files are 100% emoji-free"

# Test 7: Verify Source Trust Hierarchy validation and blocking logic
echo "[TEST] Verifying Source Trust Hierarchy and blocking logic..."
GDPR_RUMOR_JSON=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "rumors of GDPR policy changes" --json)

# Verify that GDPR_RUMOR_JSON has "proposed_pull_request": null
if ! echo "$GDPR_RUMOR_JSON" | grep -q '"proposed_pull_request": null'; then
  echo "[ERROR] Expected GDPR rumor from Priority 5 (Reddit) to be blocked (proposed_pull_request: null)"
  exit 1
fi
echo "[PASS] Blocked unverified Priority 5 secondary sources successfully"

# Verify that official Priority 1 sources are NOT blocked
if echo "$EU_JSON" | grep -q '"proposed_pull_request": null'; then
  echo "[ERROR] Expected EU AI Act (Priority 1) to generate a Pull Request, but it was blocked"
  exit 1
fi
echo "[PASS] Allowed verified Priority 1 sources successfully"

# Clean up temp files
rm -f "$TMP_DOC_OUTPUT" "$TMP_PR_OUTPUT"

echo ""
echo "[SUCCESS] All tests passed successfully."
exit 0
