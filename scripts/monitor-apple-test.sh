#!/usr/bin/env bash
# Test suite for scripts/monitor.py (Apple Developer Requirements Monitor)
# Verifies options, track simulation, codebase scanning, documentation generation,
# presence of exactly 15 required numbered sections in PR draft, and strict emoji-free policy.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

TMP_DIR="$(mktemp -d)"
OUT_DOCS="$TMP_DIR/APPLE-POLICY-MIGRATION.md"
OUT_PR="$TMP_DIR/APPLE_COMPLIANCE_PR_DRAFT.md"

cleanup() {
  rm -rf "$TMP_DIR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Apple Developer Requirements Monitor Test Suite =="

# 1. Verification of help output
OUT="$(python3 scripts/monitor.py --help 2>&1)"
if echo "$OUT" | grep -q -- "--output-docs" && echo "$OUT" | grep -q -- "--pr-output"; then
  ok "help output contains --output-docs and --pr-output CLI flags"
else
  bad "help output missing expected flags"
fi

# 2. Simulation of all 25 tracks with documentation and PR generation
python3 scripts/monitor.py --simulate "all" --output-docs "$OUT_DOCS" --pr-output "$OUT_PR" > "$TMP_DIR/run_all.log" 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "monitor.py --simulate all failed with exit code $RC. Log:"
  cat "$TMP_DIR/run_all.log"
  exit 1
fi
ok "monitor.py ran successfully for all 25 tracks with exit code 0"

# 3. Assert documentation report was generated and contains tracked entries
if [ -f "$OUT_DOCS" ]; then
  ok "Documentation output file created at $OUT_DOCS"
  if grep -q "Privacy Manifests" "$OUT_DOCS" && grep -q "App Store Review Guidelines" "$OUT_DOCS"; then
    ok "Documentation contains details for monitored Apple requirement tracks"
  else
    bad "Documentation is missing expected requirement tracks"
  fi
else
  bad "Documentation file was not created"
fi

# 4. Assert PR draft contains EXACTLY 15 required numbered sections
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
    ok "PR Draft contains exactly the 15 required numbered compliance sections"
  else
    bad "PR Draft is missing $MISSING of the 15 required compliance sections"
  fi
else
  bad "PR Draft file was not created"
fi

# 5. Verify JSON output format
JSON_OUT="$(python3 scripts/monitor.py --simulate "Privacy Manifests" --json 2>&1)"
if echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Privacy Manifests'" 2>/dev/null; then
  ok "JSON output format is valid and contains matched track"
else
  bad "JSON output verification failed"
fi

# 6. Assert no emojis are present in scripts or generated outputs
has_emojis() {
  python3 -c "
import sys, re
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    text = f.read()
emojis = re.findall(r'[\U00010000-\U0010ffff]', text)
if emojis:
    print('Found emojis in', sys.argv[1], ':', emojis)
    sys.exit(1)
sys.exit(0)
" "$1"
}

if has_emojis "scripts/monitor.py" && \
   has_emojis "$OUT_DOCS" && \
   has_emojis "$OUT_PR"; then
  ok "All scripts and generated markdown files are 100% emoji-free"
else
  bad "Emoji check failed: high-unicode emojis or symbols detected"
fi

echo ""
echo "Apple Monitor test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
