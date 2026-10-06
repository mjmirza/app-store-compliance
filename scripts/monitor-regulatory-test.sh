#!/usr/bin/env bash
#
# monitor-regulatory-test.sh
# Tests the Regulatory Intelligence Agent Monitor utility.
# Ensures that correct outputs are generated and strict emoji-free policy is adhered to.
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MON_SCRIPT="$REPO_ROOT/scripts/monitor-regulatory.py"
TMP_DIR="$(mktemp -d)"

trap "rm -rf '$TMP_DIR'" EXIT

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

# Test 4: Verify full jurisdiction coverage in default run
echo "[TEST] Validating full jurisdiction coverage..."
ALL_JSON=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --json)
REQUIRED_JURISDICTIONS=(
  "European Union"
  "United Kingdom"
  "United States"
  "Canada"
  "Australia"
  "Singapore"
  "International"
)

for jur in "${REQUIRED_JURISDICTIONS[@]}"; do
  if ! echo "$ALL_JSON" | grep -q "\"jurisdiction\": \"$jur\""; then
    echo "[ERROR] Missing expected jurisdiction in default monitor output: $jur"
    exit 1
  fi
done
echo "[PASS] All 7 required global jurisdictions are covered in monitor output"

# Test 5: Run simulation for EU AI Act and verify output contains the 15 required sections in JSON
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

for idx in "${!SECTIONS[@]}"; do
  sec_num=$((idx + 1))
  sec_name="${SECTIONS[$idx]}"
  # Check if the numbered section header exists as a markdown heading in the description field of the JSON
  if ! echo "$EU_JSON" | grep -q "## ${sec_num}\. ${sec_name}"; then
    echo "[ERROR] Missing expected section in output: ## ${sec_num}. ${sec_name}"
    exit 1
  fi
done
echo "[PASS] All 15 required compliance sections exist in the Pull Request generator output"

# Test 6: Verify JSON output is valid JSON
echo "[TEST] Running JSON output validation..."
JSON_OUT=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "COPPA" --json)
if ! echo "$JSON_OUT" | python3 -m json.tool > /dev/null; then
  echo "[ERROR] JSON output of monitor-regulatory.py is invalid"
  exit 1
fi
echo "[PASS] monitor-regulatory.py generated valid JSON output"

# Test 7: Verify --output-docs and --pr-output flags
echo "[TEST] Verifying --output-docs and --pr-output file generation..."
TEST_DOCS_OUT="$TMP_DIR/TEST-MONITOR-REPORT.md"
TEST_PR_OUT="$TMP_DIR/TEST_PR_DRAFT.md"

python3 "$MON_SCRIPT" --project "$REPO_ROOT" --output-docs "$TEST_DOCS_OUT" --pr-output "$TEST_PR_OUT" > /dev/null

if [ ! -f "$TEST_DOCS_OUT" ]; then
  echo "[ERROR] --output-docs failed to create report file at $TEST_DOCS_OUT"
  exit 1
fi

if [ ! -f "$TEST_PR_OUT" ]; then
  echo "[ERROR] --pr-output failed to create PR draft file at $TEST_PR_OUT"
  exit 1
fi

# Confirm 15 sections in generated PR draft
for idx in "${!SECTIONS[@]}"; do
  sec_num=$((idx + 1))
  sec_name="${SECTIONS[$idx]}"
  if ! grep -q "## ${sec_num}\. ${sec_name}" "$TEST_PR_OUT"; then
    echo "[ERROR] Generated PR draft missing section: ## ${sec_num}. ${sec_name}"
    exit 1
  fi
done
echo "[PASS] --output-docs and --pr-output created valid files with 15 required PR sections"

# Test 8: Verify strict emoji-free policy on output and generated files
echo "[TEST] Scanning output for any emojis or non-ascii/graphical emoticons..."
EMOJI_CHECK=$(cat "$TEST_DOCS_OUT" "$TEST_PR_OUT" | python3 -c "
import sys
text = sys.stdin.read()
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
    sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  echo "[ERROR] Emojis detected in monitor-regulatory.py output files!"
  exit 1
fi
echo "[PASS] monitor-regulatory.py output is 100% emoji-free"

# Test 9: Verify Source Trust Hierarchy validation and blocking logic
echo "[TEST] Verifying Source Trust Hierarchy and blocking logic..."
GDPR_RUMOR_JSON=$(python3 "$MON_SCRIPT" --project "$REPO_ROOT" --simulate "rumors of GDPR policy changes" --json)

if ! echo "$GDPR_RUMOR_JSON" | grep -q '"proposed_pull_request": null'; then
  echo "[ERROR] Expected GDPR rumor from Priority 5 (Reddit) to be blocked (proposed_pull_request: null)"
  exit 1
fi
echo "[PASS] Blocked unverified Priority 5 secondary sources successfully"

if echo "$EU_JSON" | grep -q '"proposed_pull_request": null'; then
  echo "[ERROR] Expected EU AI Act (Priority 1) to generate a Pull Request, but it was blocked"
  exit 1
fi
echo "[PASS] Allowed verified Priority 1 sources successfully"

echo ""
echo "[SUCCESS] All tests passed successfully."
exit 0
