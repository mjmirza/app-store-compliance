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
grep -q 'CROSS-PLATFORM-REFERENCE' <<<"$OUT" && ok "flags other-platform mention" || bad "other-platform"

# 2 over-limit name flagged
OUT="$($AUDIT --name "This App Name Is Definitely Way Too Long For The Store" 2>&1)"
grep -q 'over the 30 limit' <<<"$OUT" && ok "flags name over 30 chars" || bad "name limit"

# 3 future functionality flagged
OUT="$($AUDIT --description "Coming soon, dark mode" 2>&1)"
grep -q 'FUTURE-FUNCTIONALITY' <<<"$OUT" && ok "flags future functionality" || bad "future func"

# 4 clean dir has no high or medium
T=$(mktemp -d); mkdir -p "$T/en-US"
printf 'Lumina Studio' > "$T/en-US/name.txt"
printf 'photo,editor,filters' > "$T/en-US/keywords.txt"
printf 'A focused editor with layers and presets.' > "$T/en-US/description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$T/m.json"
OUT="$($AUDIT "$T" 2>&1)"; RC=$?
if grep -qE '\[(HIGH|MEDIUM)\]' <<<"$OUT"; then bad "clean dir flagged high/medium"; else ok "clean dir passes"; fi
# 5 propose writes the fixes file
$AUDIT "$T" --propose >/dev/null 2>&1
[ -f "$T/.metadata-fixes.md" ] && ok "propose writes fixes file" || bad "propose file"
rm -rf "$T"

# 6 missing privacy policy flagged
OUT="$($AUDIT --name "App" 2>&1)"
grep -q 'MISSING-PRIVACY-POLICY' <<<"$OUT" && ok "flags missing privacy policy" || bad "missing pp"

# 7 empty input does not crash
OUT="$($AUDIT 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "empty input exits 0" || bad "empty input rc=$RC"

# 8 subscription without terms flagged
OUT="$($AUDIT --description "Subscribe for premium, auto-renew monthly" 2>&1)"
grep -q 'MISLEADING-PRICING\|Terms' <<<"$OUT" && ok "flags subscription without terms" || bad "subscription terms"

# Google Play has its own limits and rules. Short description is 80 chars, not Apple's 170 promotional text.
LONG80="$(python3 -c 'print("x"*100)')"
OUT="$($AUDIT --platform google --title "Lumina" --short_description "$LONG80" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
grep -q 'over the 80 limit' <<<"$OUT" && ok "google short description is held to 80 chars" || bad "google short description is held to 80 chars"
OK70="$(python3 -c 'print("x"*70)')"
OUT="$($AUDIT --platform google --title "Lumina" --short_description "$OK70" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
grep -q 'over the' <<<"$OUT" && bad "a 70 char google short description passes" || ok "a 70 char google short description passes"
OUT="$($AUDIT --platform google --title "Lumina" --full_description "Get the Android app today" --privacy_url https://lumina.app/p --contact_email hi@lumina.app 2>&1)"
grep -q 'CROSS-PLATFORM-REFERENCE' <<<"$OUT" && bad "an Android listing saying Android is not an Apple violation" || ok "an Android listing saying Android is not an Apple violation"
OUT="$($AUDIT --platform google --title "Lumina" --privacy_url https://lumina.app/p 2>&1)"
grep -q 'MISSING-CONTACT-EMAIL' <<<"$OUT" && ok "google listing without a contact email is flagged" || bad "google listing without a contact email is flagged"
OUT="$($AUDIT --platform windows --name "Lumina" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && grep -q 'apple or google' <<<"$OUT" && ok "an unknown platform exits 1" || bad "an unknown platform exits 1 (rc=$RC)"

# URLs must be real http or https URLs before any network check.
OUT="$($AUDIT --name 'Real App' --privacy_url nonsense --support_url https://real.app/help --check-urls 2>&1)"
grep -q 'INVALID-METADATA-URL' <<<"$OUT" && ! grep -q '^Clean' <<<"$OUT" && ok "a privacy url that is not a url is flagged" || bad "a privacy url that is not a url is flagged"
OUT="$($AUDIT --name 'Real App' --privacy_url ftp://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'INVALID-METADATA-URL' <<<"$OUT" && ok "a non http privacy url is flagged" || bad "a non http privacy url is flagged"
OUT="$($AUDIT --name 'Real App' --privacy_url https://real.app/p 2>&1)"
grep -q 'MISSING-SUPPORT-URL' <<<"$OUT" && ok "apple listing without a support url is flagged" || bad "apple listing without a support url is flagged"

# A subscription needs a real Terms or EULA link, not the word terms.
OUT="$($AUDIT --description "Subscription. Terms apply." --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "the word terms without a link is flagged" || bad "the word terms without a link is flagged"
OUT="$($AUDIT --description "Subscription renews monthly. Terms of Use https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && bad "the Apple standard EULA link satisfies the terms check" || ok "the Apple standard EULA link satisfies the terms check"
OUT="$($AUDIT --description "Subscription renews monthly. Terms https://real.app/terms" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && bad "an own terms link satisfies the terms check" || ok "an own terms link satisfies the terms check"
OUT="$($AUDIT --description "Monthly subscription for journaling." --terms_url https://journal.test/terms --privacy_url https://journal.test/p --support_url https://journal.test/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a separate terms_url field does not replace the link in the description" || bad "a separate terms_url field does not replace the link in the description"
OUT="$($AUDIT --name Photos --description "Monthly subscription. Privacy policy https://photos.app/privacy" --privacy_url https://photos.app/privacy --support_url https://photos.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a privacy link on a host named photos is not a Terms link" || bad "a privacy link on a host named photos is not a Terms link"
OUT="$($AUDIT --description "Monthly subscription. More at https://legal.example.app/x" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a legal-looking link without the word terms or EULA is still flagged" || bad "a legal-looking link without the word terms or EULA is still flagged"
OUT="$($AUDIT --description "Read our policy at https:///privacy" --privacy_url https://real.app/p --support_url https://real.app/help --check-urls 2>&1)"
grep -q 'BOTH-UNREACHABLE-METADATA-URL' <<<"$OUT" && ok "a malformed URL in the description is reported with --check-urls" || bad "a malformed URL in the description is reported with --check-urls"
OUT="$($AUDIT --description "Monthly subscription." --promotional_text "Terms of Use https://journal.test/terms" --privacy_url https://journal.test/p --support_url https://journal.test/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a Terms link only in the promotional text is flagged" || bad "a Terms link only in the promotional text is flagged"
OUT="$($AUDIT --description "Monthly subscription. Terms apply. Privacy https://tos.example/privacy" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a privacy link on a tos host is not a Terms link" || bad "a privacy link on a tos host is not a Terms link"
for u in https://journal.test/legal/privacy https://journal.test/tostadas; do
  OUT="$($AUDIT --description "Monthly subscription. Terms apply. Privacy $u" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
  grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "$u is not a Terms link" || bad "$u is not a Terms link"
done
OUT="$($AUDIT --description "Monthly subscription. Terms apply. Privacy https://journal.test/privacy?next=apple.com/legal/internet-services/itunes/dev/stdeula" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "the Apple EULA path in a query string is not a Terms link" || bad "the Apple EULA path in a query string is not a Terms link"
OUT="$($AUDIT --description "Monthly subscription. Terms of Use https://journal.test/termsofuse" --privacy_url https://real.app/p --support_url https://real.app/help 2>&1)"
! grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "a termsofuse path is a Terms link" || bad "a termsofuse path is a Terms link"

# Every locale is audited on its own, and each finding says which locale.
L="$(mktemp -d)"; mkdir -p "$L/en-US" "$L/de-DE"
printf 'Lumina Studio Photo Editor' > "$L/en-US/name.txt"
printf 'App fuer Android' > "$L/de-DE/name.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$L/m.json"
OUT="$($AUDIT "$L" 2>&1)"
grep -q 'de-DE' <<<"$(grep 'CROSS-PLATFORM-REFERENCE' <<<"$OUT")" && ok "a short German name with a violation is audited and named" || bad "a short German name with a violation is audited and named"
grep -q 'en-US' <<<"$(grep 'CROSS-PLATFORM-REFERENCE' <<<"$OUT")" && bad "the clean English name is not blamed" || ok "the clean English name is not blamed"
rm -rf "$L"

# A fastlane android folder is audited with the Google rules even without --platform.
A="$(mktemp -d)"; mkdir -p "$A/android/en-US"
printf 'Lumina' > "$A/android/en-US/title.txt"
printf '%s' "$LONG80" > "$A/android/en-US/short_description.txt"
printf 'Get the Android app today' > "$A/android/en-US/full_description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","contact_email":"hi@lumina.app"}' > "$A/android/m.json"
OUT="$($AUDIT "$A" 2>&1)"
grep -q 'over the 80 limit' <<<"$OUT" && ! grep -q 'CROSS-PLATFORM-REFERENCE' <<<"$OUT" && ok "a fastlane android folder uses the Google rules" || bad "a fastlane android folder uses the Google rules"
# Pointing at metadata/android itself, or at one of its locale folders, keeps the Google rules.
OUT="$($AUDIT "$A/android" 2>&1)"
grep -q 'over the 80 limit' <<<"$OUT" && ! grep -q 'CROSS-PLATFORM-REFERENCE' <<<"$OUT" && ok "the android folder given directly uses the Google rules" || bad "the android folder given directly uses the Google rules"
OUT="$($AUDIT "$A/android/en-US" 2>&1)"
grep -q 'over the 80 limit' <<<"$OUT" && ok "an android locale folder given directly uses the Google rules" || bad "an android locale folder given directly uses the Google rules"
rm -rf "$A"

# Two files that both supply one field never hide the overlong one, and the conflict is named (origin/main kept the longest).
for pair in "name.txt title.txt" "Name.txt title.txt" "name.txt m.json"; do
  C="$(mktemp -d)"; mkdir -p "$C/en-US"; set -- $pair
  printf 'This App Name Is Definitely Way Too Long For The Store' > "$C/en-US/$1"
  if [ "$2" = "m.json" ]; then printf '{"title":"Short"}' > "$C/en-US/m.json"; else printf 'Short' > "$C/en-US/$2"; fi
  printf '{"privacy_url":"https://a.io/p","support_url":"https://a.io/s"}' > "$C/u.json"
  OUT="$($AUDIT "$C" 2>&1)"
  grep -q 'over the 30 limit' <<<"$OUT" && grep -q 'conflicting values' <<<"$OUT" && ok "conflicting name files keep the overlong value and flag the conflict. $pair" || bad "conflicting name files keep the overlong value and flag the conflict. $pair"
  rm -rf "$C"
done

echo ""
# A folder with no listing files was not audited. That is exit 1 with the file names to add, never a pass.
E="$(mktemp -d)"
OUT="$($AUDIT "$E" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && grep -q "name.txt" <<<"$OUT" && grep -q "Nothing was audited" <<<"$OUT" && ok "an empty metadata folder exits 1 and names the files to add" || bad "an empty metadata folder exits 1 and names the files to add (rc=$RC)"
OUT="$($AUDIT "$E/missing" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && grep -q "not a directory" <<<"$OUT" && ok "a missing metadata folder exits 1" || bad "a missing metadata folder exits 1 (rc=$RC)"
rm -rf "$E"

# two equal-length names, the risky one still audited
EQ="$(mktemp -d)"; mkdir -p "$EQ/en-US"
printf 'Android' > "$EQ/en-US/title.txt"; printf 'Journal' > "$EQ/en-US/name.txt"
printf 'https://journal.test/privacy' > "$EQ/en-US/privacy_url.txt"; printf 'https://journal.test/help' > "$EQ/en-US/support_url.txt"
OUT="$($AUDIT "$EQ" 2>&1)"
grep -q 'CROSS-PLATFORM' <<<"$OUT" && ok "an equal-length conflicting name is audited too" || bad "an equal-length conflicting name is audited too"
rm -rf "$EQ"

# two fields in conflict at once, the risky pairing across them is still audited
XC="$(mktemp -d)"; mkdir -p "$XC/en-US"
printf 'Notes xxxxxxxxxxxxxxxxxxxx' > "$XC/en-US/full_description.txt"
printf 'Subscribe' > "$XC/en-US/short_description.txt"
printf 'Terms https://j.test/terms' > "$XC/en-US/description.txt"
printf 'Notebooks' > "$XC/en-US/promo_text.txt"
printf 'Journal' > "$XC/en-US/name.txt"
printf 'https://j.test/privacy' > "$XC/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$XC/en-US/support_url.txt"
OUT="$($AUDIT "$XC" 2>&1)"
grep -q 'APPLE-3.1.2-MISLEADING-PRICING' <<<"$OUT" && ok "a risky pairing across two conflicting fields is audited" || bad "a risky pairing across two conflicting fields is audited"
rm -rf "$XC"
# a repeated command line field wins over an older alias for the same field, as on origin/main
OUT="$($AUDIT --name Android --title Journal --name Android --privacy_url https://j.test/p --support_url https://j.test/help 2>&1)"
grep -q 'CROSS-PLATFORM' <<<"$OUT" && ok "the last --name wins over an older --title alias" || bad "the last --name wins over an older --title alias"

# a locale value overrides a conflict between two parent files, so the overridden values raise nothing
OV="$(mktemp -d)"; mkdir -p "$OV/en-US"
printf '{"privacy_url":"broken"}' > "$OV/a.json"
printf '{"privacy_url":"https://common.test/privacy"}' > "$OV/b.json"
printf '{"name":"Journal","privacy_url":"https://j.test/privacy","support_url":"https://j.test/help"}' > "$OV/en-US/metadata.json"
OUT="$($AUDIT "$OV" 2>&1)"
! grep -q 'INVALID-METADATA-URL' <<<"$OUT" && ok "a locale value overrides a parent conflict" || bad "a locale value overrides a parent conflict"
rm -rf "$OV"

# fastlane's default folder fills every locale that lacks a field, so the name and keywords are audited together
DF="$(mktemp -d)"; mkdir -p "$DF/default" "$DF/en-US"
printf 'Journal' > "$DF/default/name.txt"
printf 'https://j.test/privacy' > "$DF/default/privacy_url.txt"; printf 'https://j.test/help' > "$DF/default/support_url.txt"
printf 'journal' > "$DF/en-US/keywords.txt"
OUT="$($AUDIT "$DF" 2>&1)"
grep -q 'KEYWORD-FORMAT' <<<"$OUT" && ! grep -q 'MISSING-PRIVACY' <<<"$OUT" && ok "a locale inherits the default folder" || bad "a locale inherits the default folder"
rm -rf "$DF"
# A URL scheme is case-insensitive, so an upper case HTTPS terms link counts
UC="$(mktemp -d)"; mkdir -p "$UC/en-US"
printf 'Journal' > "$UC/en-US/name.txt"
printf 'https://j.test/privacy' > "$UC/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$UC/en-US/support_url.txt"
printf 'Monthly subscription. Terms of Use. HTTPS://journal.test/terms' > "$UC/en-US/description.txt"
OUT="$($AUDIT "$UC" 2>&1)"
! grep -q 'MISLEADING-PRICING' <<<"$OUT" && ok "an upper case HTTPS terms link counts" || bad "an upper case HTTPS terms link counts"
rm -rf "$UC"
# fastlane review_information holds app review notes, it is not a locale needing its own URLs
RV="$(mktemp -d)"; mkdir -p "$RV/en-US" "$RV/review_information"
printf 'Journal' > "$RV/en-US/name.txt"
printf 'https://j.test/privacy' > "$RV/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$RV/en-US/support_url.txt"
printf 'Use demo account to sign in.' > "$RV/review_information/notes.txt"
OUT="$($AUDIT "$RV" 2>&1)"
! grep -q 'review_information' <<<"$OUT" && ok "review_information is not audited as a locale" || bad "review_information is not audited as a locale"
rm -rf "$RV"
# review notes are still audited for their content, once, with the first listing
RN="$(mktemp -d)"; mkdir -p "$RN/en-US" "$RN/review_information"
printf 'Journal' > "$RN/en-US/name.txt"
printf 'https://j.test/privacy' > "$RN/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$RN/en-US/support_url.txt"
printf 'TODO add a working review account.' > "$RN/review_information/notes.txt"
OUT="$($AUDIT "$RN" 2>&1)"
grep -q 'BOTH-PLACEHOLDER' <<<"$OUT" && ok "a placeholder in the review notes is still found" || bad "a placeholder in the review notes is still found"
rm -rf "$RN"
# each app's review notes are audited with that app, never overwritten by another app's notes
TA="$(mktemp -d)"
for a in app-a app-b; do mkdir -p "$TA/$a/metadata/en-US" "$TA/$a/metadata/review_information"
  printf 'Journal' > "$TA/$a/metadata/en-US/name.txt"
  printf 'https://j.test/privacy' > "$TA/$a/metadata/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$TA/$a/metadata/en-US/support_url.txt"; done
printf 'TODO add a working review account.' > "$TA/app-a/metadata/review_information/notes.txt"
printf 'Sign in with the supplied account.' > "$TA/app-b/metadata/review_information/notes.txt"
OUT="$($AUDIT "$TA" 2>&1)"
grep -q 'BOTH-PLACEHOLDER' <<<"$OUT" && ok "one app's review notes never hide another app's placeholder" || bad "one app's review notes never hide another app's placeholder"
rm -rf "$TA"
# fastlane's default folder is not a listing of its own when real locales sit beside it
DF2="$(mktemp -d)"; mkdir -p "$DF2/default" "$DF2/en-US"
printf 'writing' > "$DF2/default/keywords.txt"
printf 'Journal' > "$DF2/en-US/name.txt"
printf 'https://j.test/privacy' > "$DF2/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$DF2/en-US/support_url.txt"
OUT="$($AUDIT "$DF2" 2>&1)"
! grep -q 'MISSING-PRIVACY' <<<"$OUT" && ! grep -q 'MISSING-SUPPORT' <<<"$OUT" && ok "default/ is not audited as a listing beside real locales" || bad "default/ is not audited as a listing beside real locales"
rm -rf "$DF2"
# fastlane's default folder wins over a file further up, and the global review notes win over a locale's
DP="$(mktemp -d)"; mkdir -p "$DP/default" "$DP/en-US"
printf 'Journal' > "$DP/name.txt"; printf 'https://j.test/privacy' > "$DP/privacy_url.txt"; printf 'https://j.test/help' > "$DP/support_url.txt"
printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' > "$DP/default/name.txt"; printf 'writing' > "$DP/en-US/keywords.txt"
OUT="$($AUDIT "$DP" 2>&1)"
grep -q 'BOTH-METADATA-DECORATION' <<<"$OUT" && ok "the default folder's overlong name is audited over a root name" || bad "the default folder's overlong name is audited over a root name"
rm -rf "$DP"
GN="$(mktemp -d)"; mkdir -p "$GN/review_information" "$GN/en-US"
printf 'TODO add a working review account.' > "$GN/review_information/notes.txt"; printf 'Sign in.' > "$GN/en-US/review_notes.txt"
printf 'Journal' > "$GN/en-US/name.txt"; printf 'https://j.test/privacy' > "$GN/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$GN/en-US/support_url.txt"
OUT="$($AUDIT "$GN" 2>&1)"
grep -q 'BOTH-PLACEHOLDER' <<<"$OUT" && ok "the global review notes are audited over a locale's notes" || bad "the global review notes are audited over a locale's notes"
rm -rf "$GN"
# A rule term matches as a whole word, so Freeform, Todoist and "desktop app" are clean.
WB="$(mktemp -d)"; mkdir -p "$WB/en-US"
printf 'https://j.test/privacy' > "$WB/en-US/privacy_url.txt"; printf 'https://j.test/help' > "$WB/en-US/support_url.txt"
for word in Freeform Freelance "Freedom Journal" Todoist; do
  printf '%s' "$word" > "$WB/en-US/name.txt"
  OUT="$($AUDIT "$WB" 2>&1)"
  grep -qE '\[(HIGH|MEDIUM)\]' <<<"$OUT" && bad "a name that only contains a listed word is not a claim. $word" || ok "a name that only contains a listed word is not a claim. $word"
done
printf 'Journal' > "$WB/en-US/name.txt"; printf 'Now on the desktop app too' > "$WB/en-US/subtitle.txt"
printf 'Syncs every note' > "$WB/en-US/description.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'BOTH-METADATA-DECORATION' <<<"$OUT" && bad "'top app' inside 'desktop app' is not a ranking claim" || ok "'top app' inside 'desktop app' is not a ranking claim"
printf 'Todos los usuarios pueden crear notas' > "$WB/en-US/description.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'BOTH-PLACEHOLDER' <<<"$OUT" && bad "'Todos' is not the placeholder TODO" || ok "'Todos' is not the placeholder TODO"
# The words themselves still fire, so the boundary is not a blanket off switch.
printf 'Journal Free' > "$WB/en-US/name.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'BOTH-METADATA-DECORATION' <<<"$OUT" && ok "a name that says free is still a price claim" || bad "a name that says free is still a price claim"
printf '#1 Notes' > "$WB/en-US/name.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'BOTH-METADATA-DECORATION' <<<"$OUT" && ok "a name that says #1 is still a ranking claim" || bad "a name that says #1 is still a ranking claim"
printf 'TODO add the screenshots' > "$WB/en-US/description.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'BOTH-PLACEHOLDER' <<<"$OUT" && ok "a TODO in the description is still a placeholder" || bad "a TODO in the description is still a placeholder"
printf 'Shipped from Scunthorpe' > "$WB/en-US/description.txt"
OUT="$($AUDIT "$WB" 2>&1)"
grep -q 'CURSE-WORD' <<<"$OUT" && bad "a place name is not profanity" || ok "a place name is not profanity"
# Inflections and attached versions of a real claim still fire.
for pair in "subtitle|One of the best apps|BOTH-METADATA-DECORATION" "description|Download via Google PlayStore.|APPLE-2.3-CROSS-PLATFORM-REFERENCE" "description|TODO123: replace before submission|BOTH-PLACEHOLDER" "description|Multiplayer will arrive in future releases.|APPLE-2.3-FUTURE-FUNCTIONALITY" "description|Powered by ChatGPT4|CHINA-AI-REFERENCES" "description|Replace placeholders before publishing.|BOTH-PLACEHOLDER" "description|Offline mode coming sooner than expected.|APPLE-2.3-FUTURE-FUNCTIONALITY" "description|Get our AndroidTV app.|APPLE-2.3-CROSS-PLATFORM-REFERENCE" "subtitle|Journal - FreeToUse|BOTH-METADATA-DECORATION" "description|TODOreplace before submission|BOTH-PLACEHOLDER" "description|Offline mode upcoming soon.|APPLE-2.3-FUTURE-FUNCTIONALITY" "description|Powered by ChatGPTPlus.|CHINA-AI-REFERENCES" "description|Android版も公開中です。|APPLE-2.3-CROSS-PLATFORM-REFERENCE" "description|İstanbul guide. TODO: replace this.|BOTH-PLACEHOLDER" "subtitle|İstanbul Free Guide|BOTH-METADATA-DECORATION" "description|Auch für Androidgeräte verfügbar.|APPLE-2.3-CROSS-PLATFORM-REFERENCE" "description|Saatavilla myös Androidille.|APPLE-2.3-CROSS-PLATFORM-REFERENCE" "subtitle|Memo Freeware|BOTH-METADATA-DECORATION" "description|Kirjoita nopeammin Geminin avulla.|CHINA-AI-REFERENCES" "name|Notes: #1notepad|BOTH-METADATA-DECORATION" "description|Placeholdertext|BOTH-PLACEHOLDER" "name|AIChatGPT - Writing Assistant|CHINA-AI-REFERENCES" "name|VPNfree - Secure VPN|BOTH-METADATA-DECORATION" "name|PDFfree Scanner|BOTH-METADATA-DECORATION"; do
  IFS='|' read -r fld txt id <<< "$pair"
  printf 'Journal' > "$WB/en-US/name.txt"; rm -f "$WB/en-US/subtitle.txt" "$WB/en-US/description.txt"
  printf '%s' "$txt" > "$WB/en-US/$fld.txt"
  OUT="$($AUDIT "$WB" 2>&1)"
  grep -q "$id" <<<"$OUT" && ok "still fires. $txt" || bad "still fires. $txt"
done
rm -rf "$WB"

# Cross-field combinations are bounded, but every individual conflicting value must be audited.
MC="$(mktemp -d)"
python3 - "$MC" <<'PYTHON'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
(root / "listing.json").write_text(json.dumps({
    "name": "Personal Journal",
    "privacy_url": "https://journal.test/privacy",
    "support_url": "https://journal.test/help",
    "release_notes": "A long release note describing changes",
    "review_notes": "A long note describing manual review",
    "subtitle": "A pocket notebook for everyone",
}))
(root / "title.txt").write_text("Android Diary")
for n in range(15):
    (root / f"alternate-{n}.json").write_text(json.dumps({
        "release_notes": f"Updates {n}", "review_notes": f"Review {n}", "subtitle": f"Notebook {n}"
    }))
PYTHON
OUT="$($AUDIT "$MC" 2>&1)"
if grep -q 'APPLE-2.3-CROSS-PLATFORM-REFERENCE.*(name,' <<<"$OUT" \
    && grep -q 'each value and the first 4096 of 8192 combinations' <<<"$OUT"; then
  ok "the combination limit never hides an individual conflicting value"
else
  bad "the combination limit never hides an individual conflicting value"
fi
rm -rf "$MC"

echo "metadata-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
