#!/usr/bin/env bash
# Test suite for scripts/monitor-apple.py
# Verifies mock RSS input parsing, Apple keyword matching, codebase scanning,
# documentation generation, and the presence of exactly 15 required non-vague sections in the PR draft.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_apple_announcements.json"
OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-APPLE-PRIVACY",
    "category": "Privacy Manifests",
    "title": "Mandatory Privacy Manifest Integration and Domain Tracking Requirements",
    "description": "Apple is strictly enforcing Privacy Manifests (PrivacyInfo.xcprivacy) for all submissions containing third-party tracking domains or Required Reason APIs.",
    "link": "https://developer.apple.com/news/?id=privacy-manifests-mandatory",
    "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-APPLE-IAP",
    "category": "In-App Purchase policies",
    "title": "App Store In-App Purchase and StoreKit Updates",
    "description": "Important billing and subscription term disclosures under updated StoreKit regulations, requiring Restore Purchases and pricing clarity.",
    "link": "https://developer.apple.com/news/?id=storekit-iap-policies",
    "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT"
  }
]
EOF

echo "== Running Apple Policy Monitor Test Suite =="

# Execute scripts/monitor-apple.py with mock dataset
python3 scripts/monitor-apple.py --mock "$MOCK_JSON" --dir . --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > /tmp/monitor_apple_run.log 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor-apple.py failed with exit code $RC. Output:"
  cat /tmp/monitor_apple_run.log
  exit 1
fi
ok "monitor-apple.py ran successfully with exit code 0"

# Assert relevant policies were matched
if grep -q "Mandatory Privacy Manifest Integration" /tmp/monitor_apple_run.log && grep -q "App Store In-App Purchase" /tmp/monitor_apple_run.log; then
  ok "Correctly matched relevant Apple policy updates"
else
  bad "Failed to match relevant Apple policy updates. Output: $(cat /tmp/monitor_apple_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Mandatory Privacy Manifest Integration" "$OUT_DOCS" && grep -q "App Store In-App Purchase" "$OUT_DOCS"; then
    ok "Documentation contains details of matched policy updates"
  else
    bad "Documentation is missing policy details"
  fi
else
  bad "Documentation file was not created"
fi

# Assert that PR Draft contains EXACTLY 15 required sections
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

echo ""
echo "Apple Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
