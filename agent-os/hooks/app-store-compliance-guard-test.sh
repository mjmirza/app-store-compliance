#!/usr/bin/env bash
# Test gauntlet for app-store-compliance-guard.sh
# Covers positive, negative, override, fail-open, hook-mode silence, and stress cases.
# @register: no
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
GUARD="$HERE/app-store-compliance-guard.sh"
[ -x "$GUARD" ] || GUARD="bash $HERE/app-store-compliance-guard.sh"
PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

mk_ios_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App"
  printf '<plist><dict></dict></plist>' > "$d/App/Info.plist"
  printf 'import CoreLocation\nclass A { func signIn(){} func createAccount(){} }\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\nimport Stripe\n' > "$d/App/X.swift"
  echo "$d"
}
mk_ios_clean() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App"
  printf '<plist><dict><key>NSCameraUsageDescription</key><string>Scan receipts to log expenses</string><key>NSLocationWhenInUseUsageDescription</key><string>Show nearby stores on the map</string><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$d/App/Info.plist"
  printf '{}' > "$d/App/PrivacyInfo.xcprivacy"
  printf 'import StoreKit\nimport CoreLocation\nimport AVFoundation\nclass A { func signIn(){} func createAccount(){} func deleteAccount(){} func restorePurchases(){} }\nlet dev=AVCaptureDevice.default(for:.video)\nlet m=CLLocationManager()\nlet p="https://api.realbackend.io"\nlet policy="https://realbackend.io/privacy-policy"\nlet prod:SKProduct?=nil\n' > "$d/App/X.swift"
  echo "$d"
}
mk_android_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/app/src/main"
  printf '<manifest><uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION"/></manifest>' > "$d/app/src/main/AndroidManifest.xml"
  printf 'android { defaultConfig { targetSdkVersion 30 } }\n' > "$d/app/build.gradle"
  echo "$d"
}

# 1 positive. iOS with violations blocks
D="$(mk_ios_bad)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'CRITICAL' && [ "$RC" -eq 2 ] && ok "iOS violations block (exit 2, has CRITICAL)" || bad "iOS violations block"
rm -rf "$D"

# 2 positive. Android background location blocks
D="$(mk_android_bad)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'GOOGLE-PERM-BACKGROUND-LOCATION' && [ "$RC" -eq 2 ] && ok "Android bg location blocks" || bad "Android bg location blocks"
rm -rf "$D"

# 3 negative. Clean iOS passes
D="$(mk_ios_clean)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if [ "$RC" -eq 0 ]; then ok "Clean iOS passes (exit 0)"; else bad "Clean iOS passes (got $RC) :: $(echo "$OUT" | grep CRITICAL)"; fi
rm -rf "$D"

# 4 override. APP_STORE_GUARD_OK=1 allows despite critical
D="$(mk_ios_bad)"; OUT="$(APP_STORE_GUARD_OK=1 bash "$GUARD" "$D" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "Override allows critical (exit 0)" || bad "Override allows critical (got $RC)"
rm -rf "$D"

# 5 hook mode. Non-submission command stays silent
OUT="$(printf '{"tool_input":{"command":"ls -la"}}' | bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "Hook mode silent on non-submission command" || bad "Hook mode silent (rc=$RC out=$OUT)"

# 6 hook mode. Submission command runs the scan
D="$(mk_ios_bad)"; OUT="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "Hook mode runs scan on submission command" || bad "Hook mode runs scan (rc=$RC)"
rm -rf "$D"

# 7 fail-open. Non-existent dir does not crash
OUT="$(bash "$GUARD" /no/such/dir/here 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "Fail-open on missing dir (exit 0)" || bad "Fail-open on missing dir (got $RC)"

# 8 stress. Malformed JSON stdin does not crash
OUT="$(printf '%s' '{not valid json [[[ command : oops }}}' | bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "Malformed JSON stdin fail-open" || bad "Malformed JSON stdin (got $RC)"

# 9 stress. Empty stdin does not hang or crash
OUT="$(printf '' | bash "$GUARD" /tmp 2>&1)"; RC=$?
[ "$RC" -eq 0 ] || [ "$RC" -eq 2 ] && ok "Empty stdin handled" || bad "Empty stdin handled (got $RC)"

echo ""
echo "app-store-compliance-guard-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
