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
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$T/m.json"
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

# Google Play has its own limits and rules. Short description is 80 chars, not Apple's 170 promotional text.
LONG80="$(python3 -c 'print("x"*100)')"
OUT="$($AUDIT --platform google --title "Lumina" --short_description "$LONG80" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
echo "$OUT" | grep -q 'over the 80 limit' && ok "google short description is held to 80 chars" || bad "google short description is held to 80 chars"
OK70="$(python3 -c 'print("x"*70)')"
OUT="$($AUDIT --platform google --title "Lumina" --short_description "$OK70" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
echo "$OUT" | grep -q 'over the' && bad "a 70 char google short description passes" || ok "a 70 char google short description passes"
OUT="$($AUDIT --platform google --title "Lumina" --full_description "Get the Android app today" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
echo "$OUT" | grep -q 'CROSS-PLATFORM-REFERENCE' && bad "an Android listing saying Android is not an Apple violation" || ok "an Android listing saying Android is not an Apple violation"
OUT="$($AUDIT --platform google --title "Lumina" --privacy_url https://lumina.app/p 2>&1)"
echo "$OUT" | grep -q 'MISSING-CONTACT-EMAIL' && ok "google listing without a contact email is flagged" || bad "google listing without a contact email is flagged"
OUT="$($AUDIT --platform windows --name "Lumina" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q 'apple or google' && ok "an unknown platform exits 1" || bad "an unknown platform exits 1 (rc=$RC)"

# URLs must be real http or https URLs before any network check.
OUT="$($AUDIT --name 'Real App' --privacy_url nonsense --support_url https://real.app/help --check-urls 2>&1)"
echo "$OUT" | grep -q 'INVALID-METADATA-URL' && ! echo "$OUT" | grep -q '^Clean' && ok "a privacy url that is not a url is flagged" || bad "a privacy url that is not a url is flagged"
OUT="$($AUDIT --name 'Real App' --privacy_url ftp://real.app/p --support_url https://real.app/help 2>&1)"
echo "$OUT" | grep -q 'INVALID-METADATA-URL' && ok "a non http privacy url is flagged" || bad "a non http privacy url is flagged"
OUT="$($AUDIT --name 'Real App' --privacy_url https://real.app/p 2>&1)"
echo "$OUT" | grep -q 'MISSING-SUPPORT-URL' && ok "apple listing without a support url is flagged" || bad "apple listing without a support url is flagged"

# A subscription needs a real Terms or EULA link, not the word terms.
OUT="$($AUDIT --description "Subscription. Terms apply." --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
echo "$OUT" | grep -q 'MISLEADING-PRICING' && ok "the word terms without a link is flagged" || bad "the word terms without a link is flagged"
OUT="$($AUDIT --description "Subscription renews monthly. Terms of Use https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
echo "$OUT" | grep -q 'MISLEADING-PRICING' && bad "the Apple standard EULA link satisfies the terms check" || ok "the Apple standard EULA link satisfies the terms check"
OUT="$($AUDIT --description "Subscription renews monthly. Terms https://real.app/terms" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
echo "$OUT" | grep -q 'MISLEADING-PRICING' && bad "an own terms link satisfies the terms check" || ok "an own terms link satisfies the terms check"
OUT="$($AUDIT --description "Monthly subscription for journaling." --terms_url https://journal.test/terms --privacy_url https://journal.test/p --support_url https://journal.test/help 2>&1)"
echo "$OUT" | grep -q 'MISLEADING-PRICING' && ok "a separate terms_url field does not replace the link in the description" || bad "a separate terms_url field does not replace the link in the description"

# Every locale is audited on its own, and each finding says which locale.
L="$(mktemp -d)"; mkdir -p "$L/en-US" "$L/de-DE"
printf 'Lumina Studio Photo Editor' > "$L/en-US/name.txt"
printf 'App fuer Android' > "$L/de-DE/name.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$L/m.json"
OUT="$($AUDIT "$L" 2>&1)"
echo "$OUT" | grep 'CROSS-PLATFORM-REFERENCE' | grep -q 'de-DE' && ok "a short German name with a violation is audited and named" || bad "a short German name with a violation is audited and named"
echo "$OUT" | grep 'CROSS-PLATFORM-REFERENCE' | grep -q 'en-US' && bad "the clean English name is not blamed" || ok "the clean English name is not blamed"
rm -rf "$L"

# A fastlane android folder is audited with the Google rules even without --platform.
A="$(mktemp -d)"; mkdir -p "$A/android/en-US"
printf 'Lumina' > "$A/android/en-US/title.txt"
printf '%s' "$LONG80" > "$A/android/en-US/short_description.txt"
printf 'Get the Android app today' > "$A/android/en-US/full_description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","contact_email":"hi@lumina.app"}' > "$A/android/m.json"
OUT="$($AUDIT "$A" 2>&1)"
echo "$OUT" | grep -q 'over the 80 limit' && ! echo "$OUT" | grep -q 'CROSS-PLATFORM-REFERENCE' && ok "a fastlane android folder uses the Google rules" || bad "a fastlane android folder uses the Google rules"
# Pointing at metadata/android itself, or at one of its locale folders, keeps the Google rules.
OUT="$($AUDIT "$A/android" 2>&1)"
echo "$OUT" | grep -q 'over the 80 limit' && ! echo "$OUT" | grep -q 'CROSS-PLATFORM-REFERENCE' && ok "the android folder given directly uses the Google rules" || bad "the android folder given directly uses the Google rules"
OUT="$($AUDIT "$A/android/en-US" 2>&1)"
echo "$OUT" | grep -q 'over the 80 limit' && ok "an android locale folder given directly uses the Google rules" || bad "an android locale folder given directly uses the Google rules"
rm -rf "$A"

# Two files that both supply one field never hide the overlong one, and the conflict is named (origin/main kept the longest).
for pair in "name.txt title.txt" "Name.txt title.txt" "name.txt m.json"; do
  C="$(mktemp -d)"; mkdir -p "$C/en-US"; set -- $pair
  printf 'This App Name Is Definitely Way Too Long For The Store' > "$C/en-US/$1"
  if [ "$2" = "m.json" ]; then printf '{"title":"Short"}' > "$C/en-US/m.json"; else printf 'Short' > "$C/en-US/$2"; fi
  printf '{"privacy_url":"https://a.io/p","support_url":"https://a.io/s"}' > "$C/u.json"
  OUT="$($AUDIT "$C" 2>&1)"
  echo "$OUT" | grep -q 'over the 30 limit' && echo "$OUT" | grep -q 'conflicting values' && ok "conflicting name files keep the overlong value and flag the conflict. $pair" || bad "conflicting name files keep the overlong value and flag the conflict. $pair"
  rm -rf "$C"
done

echo ""
# A folder with no listing files was not audited. That is exit 1 with the file names to add, never a pass.
E="$(mktemp -d)"
OUT="$($AUDIT "$E" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "name.txt" && echo "$OUT" | grep -q "Nothing was audited" && ok "an empty metadata folder exits 1 and names the files to add" || bad "an empty metadata folder exits 1 and names the files to add (rc=$RC)"
OUT="$($AUDIT "$E/missing" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "not a directory" && ok "a missing metadata folder exits 1" || bad "a missing metadata folder exits 1 (rc=$RC)"
rm -rf "$E"

echo "metadata-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
