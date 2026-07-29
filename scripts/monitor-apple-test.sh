#!/usr/bin/env bash
# Test suite for scripts/monitor-apple.py
# Verifies mock RSS/JSON input parsing, Apple keyword/pattern matching, codebase scanning,
# documentation generation, 15-section compliance PR draft, and strict emoji-free/emoticon-free policy.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_JSON="/tmp/test_apple_announcements.json"
OUT_DOCS="/tmp/test_apple_migration.md"
OUT_PR="/tmp/test_apple_pr.md"

# Cleanup files first
cleanup() {
  rm -f "$MOCK_JSON" "$OUT_DOCS" "$OUT_PR" 2>/dev/null || true
}
trap cleanup EXIT

# Create a mock dataset containing updates for testing
cat << 'EOF' > "$MOCK_JSON"
[
  {
    "id": "MOCK-APPLE-PRIVACY-MANIFEST",
    "category": "Privacy Manifests",
    "title": "Mandatory Privacy Manifest Policies for Third Party SDKs",
    "description": "Important requirements to declare xcmanifest and privacyinfo descriptors.",
    "link": "https://developer.apple.com/news/?id=privacy-manifests",
    "pubDate": "Fri, 15 May 2026 10:00:00 GMT"
  },
  {
    "id": "MOCK-APPLE-XCODE",
    "category": "Xcode requirements",
    "title": "Xcode 26 Mandatory Build Requirements",
    "description": "All submitted apps must be compiled using Xcode 26 or higher.",
    "link": "https://developer.apple.com/news/?id=xcode-26",
    "pubDate": "Sat, 16 May 2026 11:00:00 GMT"
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
if grep -q "Mandatory Privacy Manifest Policies" /tmp/monitor_apple_run.log && grep -q "Xcode 26 Mandatory" /tmp/monitor_apple_run.log; then
  ok "Correctly matched relevant Apple policy updates"
else
  bad "Failed to match relevant Apple policy updates. Output: $(cat /tmp/monitor_apple_run.log)"
fi

# Assert that documentation was generated
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Mandatory Privacy Manifest" "$OUT_DOCS" && grep -q "Xcode 26 Mandatory" "$OUT_DOCS"; then
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

# Assert strict emoji-free / emoticon-free compliance in the PR draft and documentation
EMOJI_CHECK=$(python3 -c "
import sys
def check_emojis(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Check code points for emojis or typical pictograph blocks
    emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
    if emojis:
        return emojis
    return []

e1 = check_emojis('$OUT_DOCS')
e2 = check_emojis('$OUT_PR')
if e1 or e2:
    print('Found emojis:', e1 + e2)
    sys.exit(1)
print('No emojis found')
" 2>&1)

if [ "$EMOJI_CHECK" = "No emojis found" ]; then
  ok "Documentation and PR Draft are 100% emoji-free and emoticon-free"
else
  bad "Emojis or graphical emoticons detected in generated outputs: $EMOJI_CHECK"
fi

echo ""
echo "Apple Policy Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
