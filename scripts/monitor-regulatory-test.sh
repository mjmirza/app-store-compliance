#!/usr/bin/env bash
#
# monitor-regulatory-test.sh
# Tests the Regulatory Intelligence Agent Monitor utility.
# Ensures that correct outputs are generated and strict emoji-free policy is adhered to.
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MON_SCRIPT="$REPO_ROOT/scripts/monitor-regulatory.py"

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

# Test 3: Run scan against the repository root
echo "[TEST] Running scan against current project directory..."
python3 "$MON_SCRIPT" --project "$REPO_ROOT" > /dev/null
echo "[PASS] monitor-regulatory.py successfully scanned the target directory"

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
EMOJI_CHECK=$(echo "$EU_JSON" | python3 -c "
import sys
text = sys.stdin.read()
# Check code points for emojis or typical pictograph blocks
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
    sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  echo "[ERROR] Emojis detected in monitor-regulatory.py output!"
  exit 1
fi
echo "[PASS] monitor-regulatory.py is 100% emoji-free"

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

# Test 8: Verify file-writing capabilities and 15-section check in output files
echo "[TEST] Verifying output file creation and contents..."
TEST_MIG="/tmp/test_migration.md"
TEST_PR="/tmp/test_pr_draft.md"
rm -f "$TEST_MIG" "$TEST_PR"

python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "EU AI Act" --output-docs "$TEST_MIG" --pr-output "$TEST_PR" > /dev/null

if [ ! -f "$TEST_MIG" ] || [ ! -s "$TEST_MIG" ]; then
  echo "[ERROR] Failed to create or write to $TEST_MIG"
  exit 1
fi
echo "[PASS] Successfully created and wrote documentation to $TEST_MIG"

if [ ! -f "$TEST_PR" ] || [ ! -s "$TEST_PR" ]; then
  echo "[ERROR] Failed to create or write to $TEST_PR"
  exit 1
fi
echo "[PASS] Successfully created and wrote PR draft to $TEST_PR"

for sect in "${SECTIONS[@]}"; do
  if ! grep -q "## $sect" "$TEST_PR"; then
    echo "[ERROR] Missing expected section $sect in written file: $TEST_PR"
    exit 1
  fi
done
echo "[PASS] All 15 required sections verified inside the written PR draft file"

rm -f "$TEST_MIG" "$TEST_PR"

echo ""
echo "[SUCCESS] All tests passed successfully."
exit 0
