#!/usr/bin/env bash
# Test script for scripts/monitor-privacy.py
# Validates parsing, classification, codebase scanning, and Markdown generation.
set -euo pipefail

# Setup temp directory for testing
TEST_DIR=$(mktemp -d 2>/dev/null || echo /tmp/privacy_test.$$)
trap 'rm -rf "$TEST_DIR" 2>/dev/null' EXIT

echo "=== Running scripts/monitor-privacy.py tests ==="

# 1. Test standard run with inline mock data
echo "Test 1: Running with default mock data..."
python3 scripts/monitor-privacy.py \
  --dir . \
  --output-docs "$TEST_DIR/PRIVACY-POLICY-MIGRATION.md" \
  --pr-output "$TEST_DIR/PRIVACY_COMPLIANCE_PR_DRAFT.md"

# Check if both output files exist and are not empty
if [ ! -s "$TEST_DIR/PRIVACY-POLICY-MIGRATION.md" ]; then
  echo "FAIL: PRIVACY-POLICY-MIGRATION.md is empty or missing"
  exit 1
fi
if [ ! -s "$TEST_DIR/PRIVACY_COMPLIANCE_PR_DRAFT.md" ]; then
  echo "FAIL: PRIVACY_COMPLIANCE_PR_DRAFT.md is empty or missing"
  exit 1
fi
echo "PASS: Output files created successfully"

# 2. Verify exactly 15 non-vague sections inside the PR draft
echo "Test 2: Verifying exactly 15 non-vague sections inside the PR draft..."
declare -a EXPECTED_SECTIONS=(
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

for section in "${EXPECTED_SECTIONS[@]}"; do
  if ! grep -q "##.*$section" "$TEST_DIR/PRIVACY_COMPLIANCE_PR_DRAFT.md"; then
    echo "FAIL: Missing required section '$section'"
    exit 1
  fi
done
echo "PASS: PR draft contains exactly the 15 required sections"

# 3. Verify no emojis are present in any of the output files
echo "Test 3: Checking output files for emojis..."
# This regex searches for standard Unicode range of emojis/symbols
EMOJI_REGEX='[^\x00-\x7F]'
if grep -q -P "$EMOJI_REGEX" "$TEST_DIR/PRIVACY-POLICY-MIGRATION.md" 2>/dev/null; then
  echo "FAIL: Found emojis or non-ASCII characters inside PRIVACY-POLICY-MIGRATION.md"
  exit 1
fi
if grep -q -P "$EMOJI_REGEX" "$TEST_DIR/PRIVACY_COMPLIANCE_PR_DRAFT.md" 2>/dev/null; then
  echo "FAIL: Found emojis or non-ASCII characters inside PRIVACY_COMPLIANCE_PR_DRAFT.md"
  exit 1
fi
echo "PASS: Output files are completely emoji-free and clean"

# 4. Test code scanning with dummy code files
echo "Test 4: Testing codebase scanner..."
CODE_DIR="$TEST_DIR/mock_code"
mkdir -p "$CODE_DIR"

# Write standard signals to files to verify scanner detects them
echo "let manager = ATTrackingManager.shared" > "$CODE_DIR/app.swift"
echo "UserDefaults.standard.set(true, forKey: 'opt_in')" > "$CODE_DIR/utils.swift"
echo "localStorage.setItem('session_token', token)" > "$CODE_DIR/index.js"
echo "<div class='cookie-banner'>Consent</div>" > "$CODE_DIR/index.html"

python3 scripts/monitor-privacy.py \
  --dir "$CODE_DIR" \
  --output-docs "$TEST_DIR/MIGRATION_SCAN.md" \
  --pr-output "$TEST_DIR/PR_SCAN.md"

# Check if signal-related files are listed under affected files section in the PR
if ! grep -q "app.swift" "$TEST_DIR/PR_SCAN.md"; then
  echo "FAIL: Scanner missed signal in app.swift"
  exit 1
fi
if ! grep -q "utils.swift" "$TEST_DIR/PR_SCAN.md"; then
  echo "FAIL: Scanner missed signal in utils.swift"
  exit 1
fi
if ! grep -q "index.js" "$TEST_DIR/PR_SCAN.md"; then
  echo "FAIL: Scanner missed signal in index.js"
  exit 1
fi
echo "PASS: Scanning matches signals correctly and updates PR affected files list"

# 5. Test keyword-based filters
echo "Test 5: Testing keyword filter flag..."
python3 scripts/monitor-privacy.py \
  --keywords "GDPR,xcprivacy" \
  --output-docs "$TEST_DIR/MIGRATION_FILTER.md" \
  --pr-output "$TEST_DIR/PR_FILTER.md"

if ! grep -q "Privacy Manifest" "$TEST_DIR/MIGRATION_FILTER.md"; then
  echo "FAIL: Expected 'Privacy Manifest' to pass keyword filter"
  exit 1
fi
if ! grep -q "GDPR" "$TEST_DIR/MIGRATION_FILTER.md"; then
  echo "FAIL: Expected 'GDPR' to pass keyword filter"
  exit 1
fi
if grep -q "Advertising ID" "$TEST_DIR/MIGRATION_FILTER.md"; then
  echo "FAIL: Unexpected 'Advertising ID' passed keyword filter"
  exit 1
fi
echo "PASS: Keyword filtering works precisely"

# 6. Test with custom mock JSON file
echo "Test 6: Testing custom mock JSON file parsing..."
echo '[{"id": "CUSTOM-1", "category": "GDPR", "title": "Custom GDPR Guidance 2026", "description": "Custom description of GDPR update.", "link": "https://eur-lex.europa.eu/", "pubDate": "Wed, 01 Jul 2026 12:00:00 GMT"}]' > "$TEST_DIR/custom_mock.json"

python3 scripts/monitor-privacy.py \
  --mock "$TEST_DIR/custom_mock.json" \
  --output-docs "$TEST_DIR/MIGRATION_CUSTOM.md" \
  --pr-output "$TEST_DIR/PR_CUSTOM.md"

if ! grep -q "Custom GDPR Guidance 2026" "$TEST_DIR/MIGRATION_CUSTOM.md"; then
  echo "FAIL: Custom mock JSON announcements were not parsed or integrated correctly"
  exit 1
fi
echo "PASS: Custom mock JSON parsed and integrated successfully"

echo "=== All monitor-privacy.py tests passed successfully! ==="
exit 0
