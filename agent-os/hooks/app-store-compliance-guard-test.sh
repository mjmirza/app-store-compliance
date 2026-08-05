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

# The four known FALSE-POSITIVE scenarios, which must all stay SILENT: a localhost only inside
# #if DEBUG (never shipped), a location usage description in the modern INFOPLIST_KEY build-setting
# form, example.com used as test input inside a Tests dir (never shipped), and the bare word "Adjust".
mk_ios_precision_safe() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App.xcodeproj" "$d/App" "$d/AppTests"
  printf 'INFOPLIST_KEY_NSLocationWhenInUseUsageDescription = "for prayer times";\nITSAppUsesNonExemptEncryption = NO;\n' > "$d/App.xcodeproj/project.pbxproj"
  printf '{}' > "$d/App/PrivacyInfo.xcprivacy"
  printf 'import CoreLocation\nimport SwiftUI\nlet m = CLLocationManager()\nlet policy = "https://app.com/privacy-policy"\nvar base: String {\n#if DEBUG\nreturn "http://localhost:8787"\n#else\nreturn "https://prod.app.com"\n#endif\n}\nstruct V: View { var body: some View { TextField("Search", text: .constant("")) } }\nlet label = "Adjust times"\n' > "$d/App/Main.swift"
  printf 'let testURL = "https://example.com/x"\n' > "$d/AppTests/T.swift"
  echo "$d"
}

# The SAME four categories as REAL shipped violations, which must all FIRE (no blind spot): a
# release-reachable localhost string, CLLocationManager with no usage description, a real tracking
# SDK (AdjustConfig), and lorem ipsum in shipped (non-test) source.
mk_ios_precision_real() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App.xcodeproj" "$d/App"
  printf 'X=1;\n' > "$d/App.xcodeproj/project.pbxproj"
  printf 'import CoreLocation\nimport AdjustSdk\nlet m = CLLocationManager()\nlet staging = "http://localhost:9000"\nlet cfg = AdjustConfig(appToken:"x")\nlet copy = "lorem ipsum dolor sit"\n' > "$d/App/Main.swift"
  echo "$d"
}

mk_ios_bad_nutrition() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App"
  printf '<plist><dict></dict></plist>' > "$d/App/Info.plist"
  printf 'import Foundation\nlet email = "test@example.com"\n' > "$d/App/X.swift"
  echo "$d"
}

mk_android_bad_privacy() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/app/src/main"
  printf '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="com.google.android.gms.permission.AD_ID"/><uses-permission android:name="android.permission.READ_STEPS"/></manifest>' > "$d/app/src/main/AndroidManifest.xml"
  printf 'android { defaultConfig { targetSdkVersion 34 } }\n' > "$d/app/build.gradle"
  printf 'class MyActivity { void test() { requestPermissions(new String[]{"camera"}, 1); HealthConnectClient client = null; contacts = "john"; } }\n' > "$d/app/src/main/MyActivity.java"
  echo "$d"
}

mk_web_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d"
  printf '{"name": "test-web"}' > "$d/package.json"
  printf '<html><body><script>localStorage.setItem("token", "secret"); sessionStorage.setItem("session", "xyz"); indexedDB.open("db"); gtag("event", "test"); document.cookie = "user=john"; processData("sensitivedata");</script></body></html>' > "$d/index.html"
  echo "$d"
}

mk_web_clean() {
  local d; d="$(mktemp -d)"; mkdir -p "$d"
  printf '{"name": "test-web"}' > "$d/package.json"
  printf '<html><body><script>encryptedStorage("token"); clearSessionStorage(); encryptDatabase(); consentTracking(); cookieBanner(); GDPR();</script></body></html>' > "$d/index.html"
  echo "$d"
}

# Flutter with a required-reason plugin and no PrivacyInfo.xcprivacy anywhere.
mk_flutter_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/Runner" "$d/lib"
  printf 'name: t\ndependencies:\n  permission_handler: ^11.0.0\n' > "$d/pubspec.yaml"
  printf "import 'package:permission_handler/permission_handler.dart';\nvoid main(){Permission.camera.request();}\n" > "$d/lib/main.dart"
  printf '<plist><dict></dict></plist>' > "$d/ios/Runner/Info.plist"
  echo "$d"
}

# React Native + an undisclosed OTA updater (CodePush).
mk_rn_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/App"
  printf '{"dependencies":{"react-native":"0.74.0","react-native-code-push":"^8.0.0"}}' > "$d/package.json"
  printf 'import codePush from "react-native-code-push";\ncodePush.sync();\n' > "$d/App.tsx"
  printf '<plist><dict></dict></plist>' > "$d/ios/App/Info.plist"
  echo "$d"
}

# Ionic/Capacitor thin wrapper. WebView present, fewer than 2 native-feel plugins.
mk_ionic_thin_wrapper() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/App" "$d/src"
  printf '{"dependencies":{"@capacitor/core":"^6.0.0","@ionic/angular":"^8.0.0"}}' > "$d/package.json"
  printf 'export default {};' > "$d/capacitor.config.ts"
  printf "import { Capacitor } from '@capacitor/core';\nconst wv = new WKWebView();\n" > "$d/src/app.ts"
  printf '<plist><dict></dict></plist>' > "$d/ios/App/Info.plist"
  echo "$d"
}

# Same shape but with 3 distinct native-feel plugins. Thin-wrapper must NOT fire.
mk_ionic_native_shell() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/App" "$d/src"
  printf '{"dependencies":{"@capacitor/core":"^6.0.0","@ionic/angular":"^8.0.0"}}' > "$d/package.json"
  printf 'export default {};' > "$d/capacitor.config.ts"
  printf "import { Capacitor } from '@capacitor/core';\nimport '@capacitor/status-bar';\nimport '@capacitor/splash-screen';\nimport '@capacitor/push-notifications';\nconst wv = new WKWebView();\n" > "$d/src/app.ts"
  printf '<plist><dict></dict></plist>' > "$d/ios/App/Info.plist"
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

# 10 precision. The four known false-positive scenarios must NOT fire (no false alarms).
D="$(mk_ios_precision_safe)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if echo "$OUT" | grep -Eq 'STAGING-BACKEND|MISSING-USAGE-DESCRIPTION|BOTH-PLACEHOLDER|MISSING-ATT' || [ "$RC" -ne 0 ]; then
  bad "Precision: false positives silent (rc=$RC, leaked: $(echo "$OUT" | grep -Eo 'STAGING-BACKEND|MISSING-USAGE-DESCRIPTION|BOTH-PLACEHOLDER|MISSING-ATT' | paste -sd, -))"
else ok "Precision: #if-DEBUG localhost, INFOPLIST_KEY location, example.com-in-Tests, word Adjust all stay silent"; fi
rm -rf "$D"

# 11 no blind spot. The SAME four categories as real shipped violations must STILL fire.
D="$(mk_ios_precision_real)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
MISS=""
for pat in STAGING-BACKEND MISSING-USAGE-DESCRIPTION BOTH-PLACEHOLDER MISSING-ATT; do
  echo "$OUT" | grep -q "$pat" || MISS="$MISS $pat"
done
[ -z "$MISS" ] && ok "No blind spot: release localhost, no-usage location, AdjustConfig, lorem ipsum all still fire" || bad "No blind spot: missed$MISS"
rm -rf "$D"

# 12 Apple Privacy Nutrition Labels violation blocks
D="$(mk_ios_bad_nutrition)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-PRIVACY-NUTRITION-LABELS' && ok "Apple missing nutrition labels blocks" || bad "Apple missing nutrition labels blocks"
rm -rf "$D"

# 13 Android user disclosures, AD_ID, runtime permission checks, health permissions block
D="$(mk_android_bad_privacy)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
MISS_AND=""
for pat in ANDROID-USER-DATA-DISCLOSURE ANDROID-ADVERTISING-ID ANDROID-RUNTIME-PERMISSIONS ANDROID-HEALTH-PERMISSIONS; do
  echo "$OUT" | grep -q "$pat" || MISS_AND="$MISS_AND $pat"
done
[ -z "$MISS_AND" ] && ok "Android bad privacy checks all fire" || bad "Android bad privacy checks missed:$MISS_AND"
rm -rf "$D"

# 14 Web bad privacy checks (GDPR, cookie, localStorage, sessionStorage, IndexedDB, tracking)
D="$(mk_web_bad)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
MISS_WEB=""
for pat in WEB-GDPR-COMPLIANCE WEB-COOKIE-CONSENT WEB-LOCAL-STORAGE WEB-SESSION-STORAGE WEB-INDEXEDDB WEB-TRACKING-TECHNOLOGIES; do
  echo "$OUT" | grep -q "$pat" || MISS_WEB="$MISS_WEB $pat"
done
[ -z "$MISS_WEB" ] && [ "$RC" -eq 2 ] && ok "Web bad privacy checks all fire (exit 2)" || bad "Web bad privacy checks missed:$MISS_WEB or wrong exit code ($RC)"
rm -rf "$D"

# 15 Web clean privacy checks pass
D="$(mk_web_clean)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if [ "$RC" -eq 0 ] && ! echo "$OUT" | grep -q 'WEB-'; then
  ok "Web clean privacy passes (exit 0)"
else
  bad "Web clean privacy passes (got $RC) :: $(echo "$OUT" | grep -E 'WEB-')"
fi
rm -rf "$D"

# 16 Subscription hard-cancel block (phone/mail/in-person only)
D="$(mktemp -d)"; mkdir -p "$D"
printf '{"name":"t"}' > "$D/package.json"
printf '<html><body>Your subscription auto-renews monthly. Call us to cancel at 1-800-555-0100.</body></html>' > "$D/index.html"
OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'BOTH-SUBSCRIPTION-HARD-CANCEL' && ok "Subscription phone-only cancel blocks" || bad "Subscription phone-only cancel blocks"
rm -rf "$D"

# 17 Subscription self-service cancel stays silent
D="$(mktemp -d)"; mkdir -p "$D"
printf '{"name":"t"}' > "$D/package.json"
printf '<html><body>Your membership auto-renews monthly. Cancel any time from Account Settings.</body></html>' > "$D/index.html"
OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if ! echo "$OUT" | grep -q 'BOTH-SUBSCRIPTION-HARD-CANCEL'; then
  ok "Subscription self-service cancel stays silent"
else
  bad "Subscription self-service cancel stays silent"
fi
rm -rf "$D"

# 18 Flutter framework detected + privacy manifest gap blocks
D="$(mk_flutter_bad)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if echo "$OUT" | grep -q 'Flutter=1' && echo "$OUT" | grep -q 'FLUTTER-PRIVACY-MANIFEST-MISSING' && [ "$RC" -eq 2 ]; then
  ok "Flutter detected, missing privacy manifest blocks"
else
  bad "Flutter detected, missing privacy manifest blocks (rc=$RC)"
fi
rm -rf "$D"

# 19 React Native + undisclosed CodePush OTA fires (non-critical, does not block alone)
D="$(mk_rn_bad)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
if echo "$OUT" | grep -q 'ReactNative/Expo=1' && echo "$OUT" | grep -q 'RN-OTA-UNDECLARED'; then
  ok "React Native detected, undisclosed CodePush OTA fires"
else
  bad "React Native detected, undisclosed CodePush OTA fires"
fi
rm -rf "$D"

# 20 Ionic thin wrapper (WebView, <2 native plugins) blocks on 4.2
D="$(mk_ionic_thin_wrapper)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if echo "$OUT" | grep -q 'Ionic/Capacitor/Cordova=1' && echo "$OUT" | grep -q 'IONIC-4.2-THIN-WRAPPER' && [ "$RC" -eq 2 ]; then
  ok "Ionic thin wrapper blocks on 4.2 minimum functionality"
else
  bad "Ionic thin wrapper blocks on 4.2 minimum functionality (rc=$RC)"
fi
rm -rf "$D"

# 21 Ionic with 3 distinct native-feel plugins does NOT trip the thin-wrapper false positive
D="$(mk_ionic_native_shell)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
if ! echo "$OUT" | grep -q 'IONIC-4.2-THIN-WRAPPER'; then
  ok "Ionic with real native plugin shell stays silent on thin-wrapper"
else
  bad "Ionic with real native plugin shell stays silent on thin-wrapper (false positive)"
fi
rm -rf "$D"

# 22 Submission-command regex now catches Flutter, Capacitor, Ionic, EAS, Cordova build commands
MISS_CMD=""
for cmd in "flutter build ipa --release" "npx cap sync ios" "ionic capacitor build ios --prod" "eas build --platform ios" "cordova build ios --release"; do
  OUT="$(printf '{"tool_input":{"command":"%s"}}' "$cmd" | bash "$GUARD" 2>&1)"
  echo "$OUT" | grep -q 'App Store Compliance Guard' || MISS_CMD="$MISS_CMD [$cmd]"
done
[ -z "$MISS_CMD" ] && ok "Submission regex catches flutter/cap/ionic/eas/cordova build commands" || bad "Submission regex missed:$MISS_CMD"

echo ""
echo "app-store-compliance-guard-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
