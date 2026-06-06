#!/usr/bin/env bash
# Test suite for metadata-audit.py
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
AUDIT="python3 $HERE/metadata-audit.py"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# 1 cross-platform mention flagged
OUT="$($AUDIT --name "My App also on Android" 2>&1)"
echo "$OUT" | grep -q 'CROSS-PLATFORM-REFERENCE' && ok "flags other-platform mention" || bad "other-platform"

# 2 over-limit name flagged
OUT="$($AUDIT --name "This App Name Is Definitely Way Too Long For The Store" 2>&1)"
echo "$OUT" | grep -q 'over the 30 limit' && ok "flags name over 30 chars" || bad "name limit"

# 3 future functionality flagged
OUT="$($AUDIT --description "Coming soon, dark mode" 2>&1)"
echo "$OUT" | grep -q 'FUTURE-FUNCTIONALITY' && ok "flags future functionality" || bad "future func"

# 4 clean dir has no high or medium
T=$(mktemp -d); mkdir -p "$T/en-US"
printf 'Lumina Studio' > "$T/en-US/name.txt"
printf 'photo,editor,filters' > "$T/en-US/keywords.txt"
printf 'A focused editor with layers and presets.' > "$T/en-US/description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy"}' > "$T/m.json"
OUT="$($AUDIT "$T" 2>&1)"; RC=$?
if echo "$OUT" | grep -qE '\[(HIGH|MEDIUM)\]'; then bad "clean dir flagged high/medium"; else ok "clean dir passes"; fi
# 5 propose writes the fixes file
$AUDIT "$T" --propose >/dev/null 2>&1
[ -f "$T/.metadata-fixes.md" ] && ok "propose writes fixes file" || bad "propose file"
rm -rf "$T"

# 6 missing privacy policy flagged
OUT="$($AUDIT --name "App" 2>&1)"
echo "$OUT" | grep -q 'MISSING-PRIVACY-POLICY' && ok "flags missing privacy policy" || bad "missing pp"

# 7 empty input does not crash
OUT="$($AUDIT 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "empty input exits 0" || bad "empty input rc=$RC"

# 8 subscription without terms flagged
OUT="$($AUDIT --description "Subscribe for premium, auto-renew monthly" 2>&1)"
echo "$OUT" | grep -q 'MISLEADING-PRICING\|Terms' && ok "flags subscription without terms" || bad "subscription terms"

echo ""
echo "metadata-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
