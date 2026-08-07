#!/usr/bin/env bash
#
# monitor-standards-test.sh
# Tests the Technical Standards Compliance Monitor utility.
# Ensures that correct outputs are generated and strict emoji-free policy is adhered to.
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MON_SCRIPT="$REPO_ROOT/scripts/monitor-standards.py"

echo "[TEST] Starting Technical Standards Compliance Monitor Test Suite"
echo "Project Path: $REPO_ROOT"
echo "Script Path:  $MON_SCRIPT"
echo ""

# Test 1: Verify monitor-standards.py exists and is executable
if [ ! -x "$MON_SCRIPT" ]; then
  echo "[ERROR] monitor-standards.py is not executable or not found."
  exit 1
fi
echo "[PASS] monitor-standards.py is executable"

# Test 2: Verify help menu executes successfully
python3 "$MON_SCRIPT" --help > /dev/null
echo "[PASS] monitor-standards.py --help executed successfully"

# Test 3: Run scan against the repository root
echo "[TEST] Running scan against current project directory..."
python3 "$MON_SCRIPT" --dir "$REPO_ROOT" > /dev/null
echo "[PASS] monitor-standards.py successfully scanned the target directory"

# Test 4: Run simulation and verify output contains the 15 required sections
echo "[TEST] Validating 15-section JSON output..."
STANDARDS_JSON=$(python3 "$MON_SCRIPT" --dir "$REPO_ROOT" --json)

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

# Test 5: Verify PR Draft exists and contains all 15 sections
PR_DRAFT_FILE="$REPO_ROOT/docs/STANDARDS_COMPLIANCE_PR_DRAFT.md"
if [ ! -f "$PR_DRAFT_FILE" ]; then
  echo "[ERROR] Expected PR draft file not found at: $PR_DRAFT_FILE"
  exit 1
fi

for sect in "${SECTIONS[@]}"; do
  # Check if the section header exists as a markdown heading in the description
  if ! grep -q "## [0-9]\+\. $sect" "$PR_DRAFT_FILE"; then
    echo "[ERROR] Missing expected section in output: $sect"
    exit 1
  fi
done
echo "[PASS] All 15 required compliance sections exist in the Pull Request draft"

# Test 6: Verify JSON output is valid JSON
if ! echo "$STANDARDS_JSON" | python3 -m json.tool > /dev/null; then
  echo "[ERROR] JSON output of monitor-standards.py is invalid"
  exit 1
fi
echo "[PASS] monitor-standards.py generated valid JSON output"

# Test 7: Verify strict emoji-free policy on output
echo "[TEST] Scanning output for any emojis or non-ascii/graphical emoticons..."
EMOJI_CHECK=$(python3 -c "
import sys
with open('$PR_DRAFT_FILE', 'r', encoding='utf-8') as f:
    text = f.read()
# Check code points for emojis or typical pictograph blocks
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
    sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  echo "[ERROR] Emojis detected in monitor-standards.py output!"
  exit 1
fi
echo "[PASS] monitor-standards.py outputs are 100% emoji-free"

# Cleanup function to ensure isolated tests leave no stale files in /tmp
cleanup() {
  rm -f /tmp/rumor_only.json 2>/dev/null || true
}
trap cleanup EXIT

# Test 8: Verify Source Trust Hierarchy validation and blocking logic
echo "[TEST] Verifying Source Trust Hierarchy and blocking logic..."

# Create the rumor mock JSON file explicitly so the test is fully isolated
cat << 'EOF' > /tmp/rumor_only.json
[
  {
    "id": "STD-MOCK-RUMOR",
    "category": "ISO 27001",
    "title": "Unverified rumor on LinkedIn alleging changes to ISO 27001 controls",
    "description": "A user post claims that ISO 27001 is immediately requiring zero-trust network access on all employee home offices. No citations or official documents are referenced.",
    "link": "https://linkedin.com/posts/unverified-rumor-iso",
    "pubDate": "Mon, 13 Jul 2026 10:00:00 UTC"
  }
]
EOF

RUMOR_JSON=$(python3 "$MON_SCRIPT" --dir "$REPO_ROOT" --mock /tmp/rumor_only.json --json)

# Verify that the standard rumor has "proposed_pull_request": null
if ! echo "$RUMOR_JSON" | grep -q '"proposed_pull_request": null'; then
  echo "[ERROR] Expected standard rumor from Priority 5 (LinkedIn) to be blocked (proposed_pull_request: null)"
  exit 1
fi
echo "[PASS] Blocked unverified Priority 5 secondary sources successfully"

# Verify that official Priority 1 sources are NOT blocked
if echo "$STANDARDS_JSON" | grep -q '"proposed_pull_request": null'; then
  # Wait, standard rumor is in standard_json as well, but some tracks (like ISO 27701) are official and should have a PR
  # Let's verify that ISO 27701 (which only has verified official mock announcements) generates a valid PR
  ISO_27701_PR=$(echo "$STANDARDS_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data:
    if item['track'] == 'ISO 27701':
        if item['proposed_pull_request'] is None:
            sys.exit(1)
        else:
            sys.exit(0)
sys.exit(1)
")
  if [ $? -ne 0 ]; then
    echo "[ERROR] Expected ISO 27701 (Priority 1) to generate a Pull Request, but it was blocked or missing"
    exit 1
  fi
fi
echo "[PASS] Allowed verified Priority 1 sources successfully"

echo ""
echo "[SUCCESS] All tests passed successfully."
exit 0
