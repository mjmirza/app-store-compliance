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
# A privacy manifest is a plist. The validator rejects anything it cannot parse, so fixtures carry a real one.
PLIST_EMPTY='<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict/></plist>'

mk_ios_bad() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App"
  printf '<plist><dict></dict></plist>' > "$d/App/Info.plist"
  printf 'import CoreLocation\nclass A { func signIn(){} func createAccount(){} }\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\nimport Stripe\n' > "$d/App/X.swift"
  echo "$d"
}
mk_ios_clean() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/App"
  printf '<plist><dict><key>NSCameraUsageDescription</key><string>Scan receipts to log expenses</string><key>NSLocationWhenInUseUsageDescription</key><string>Show nearby stores on the map</string><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$d/App/Info.plist"
  printf '%s' "$PLIST_EMPTY" > "$d/App/PrivacyInfo.xcprivacy"
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
  printf '%s' "$PLIST_EMPTY" > "$d/App/PrivacyInfo.xcprivacy"
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
  printf '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="com.google.android.gms.permission.AD_ID"/><uses-permission android:name="android.permission.READ_STEPS"/><uses-permission android:name="android.permission.READ_CONTACTS"/></manifest>' > "$d/app/src/main/AndroidManifest.xml"
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

# Flutter, Android-only (no ios/ folder at all). The iOS-only privacy-manifest check must
# NOT fire, since flutter build appbundle/apk never touches Info.plist or PrivacyInfo.xcprivacy.
mk_flutter_android_only() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/android/app/src/main" "$d/lib"
  printf 'name: t\ndependencies:\n  permission_handler: ^11.0.0\n' > "$d/pubspec.yaml"
  printf "import 'package:permission_handler/permission_handler.dart';\nvoid main(){Permission.camera.request();}\n" > "$d/lib/main.dart"
  printf '<manifest xmlns:android="http://schemas.android.com/apk/res/android"></manifest>' > "$d/android/app/src/main/AndroidManifest.xml"
  echo "$d"
}

# Monorepo layout: root package.json is tooling-only, the real RN app lives at apps/mobile/.
mk_rn_monorepo() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/apps/mobile/ios/App"
  printf '{"name":"tooling-root","private":true}' > "$d/package.json"
  printf '{"dependencies":{"react-native":"0.74.0"}}' > "$d/apps/mobile/package.json"
  printf '<plist><dict></dict></plist>' > "$d/apps/mobile/ios/App/Info.plist"
  echo "$d"
}

# A config.xml that is NOT Cordova (no <widget>/xmlns:cdv marker). Must not flip IS_IONIC.
mk_unrelated_config_xml() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/App"
  printf '<configuration><appSettings></appSettings></configuration>' > "$d/config.xml"
  printf '<plist><dict></dict></plist>' > "$d/ios/App/Info.plist"
  echo "$d"
}

# The real-world Codex-found scenario: a full cross-platform Flutter repo with BOTH ios/ and
# android/ folders committed (the normal case), building only for Android.
mk_flutter_both_platforms() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/Runner" "$d/android/app/src/main" "$d/lib"
  printf 'name: t\ndependencies:\n  permission_handler: ^11.0.0\n' > "$d/pubspec.yaml"
  printf "import 'package:permission_handler/permission_handler.dart';\nvoid main(){Permission.camera.request();}\n" > "$d/lib/main.dart"
  printf '<plist><dict></dict></plist>' > "$d/ios/Runner/Info.plist"
  printf '<manifest xmlns:android="http://schemas.android.com/apk/res/android"></manifest>' > "$d/android/app/src/main/AndroidManifest.xml"
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

# 9b fail-open. Hook mode with an empty payload must not fall back to scanning the working directory
D="$(mk_ios_bad)"; OUT="$(cd "$D" && printf '' | bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && [ -z "$OUT" ] && ok "Empty hook payload exits 0 without scanning cwd" || bad "Empty hook payload scanned cwd (rc=$RC)"
rm -rf "$D"

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

# 20 Ionic thin wrapper (WebView, <2 native plugins) fires as HIGH (advisory heuristic, not a
# hard blocker per council review, since plugin-count is a proxy, not the real Apple 4.2 test)
D="$(mk_ionic_thin_wrapper)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
if echo "$OUT" | grep -q 'Ionic/Capacitor/Cordova=1' && echo "$OUT" | grep -q 'IONIC-4.2-THIN-WRAPPER'; then
  ok "Ionic thin wrapper fires as high-severity advisory on 4.2 minimum functionality"
else
  bad "Ionic thin wrapper fires as high-severity advisory on 4.2 minimum functionality"
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

# 23 Council-found bug fix: Flutter Android-only build must NOT trigger the iOS-only privacy check
D="$(mk_flutter_android_only)"; OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
if ! echo "$OUT" | grep -q 'FLUTTER-PRIVACY-MANIFEST-MISSING'; then
  ok "Flutter Android-only build stays silent on iOS-only privacy check"
else
  bad "Flutter Android-only build wrongly fired the iOS-only privacy check (rc=$RC)"
fi
rm -rf "$D"

# 24 Council-found bug fix: monorepo detection scans every package.json, not just the first
D="$(mk_rn_monorepo)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
if echo "$OUT" | grep -q 'ReactNative/Expo=1'; then
  ok "Monorepo React Native detected via nested apps/mobile/package.json"
else
  bad "Monorepo React Native detected via nested apps/mobile/package.json"
fi
rm -rf "$D"

# 25 Council-found bug fix: an unrelated config.xml (no Cordova widget marker) must not flip IS_IONIC
D="$(mk_unrelated_config_xml)"; OUT="$(bash "$GUARD" "$D" 2>&1)"
if echo "$OUT" | grep -q 'Ionic/Capacitor/Cordova=0'; then
  ok "Unrelated config.xml (no widget marker) stays silent on Ionic detection"
else
  bad "Unrelated config.xml (no widget marker) stays silent on Ionic detection"
fi
rm -rf "$D"

# 26 Command overrides file-tree presence for a both-platforms repo (docs/CROSS-PLATFORM-FRAMEWORKS.md)
D="$(mk_flutter_both_platforms)"
OUT_APK="$(printf '{"tool_input":{"command":"flutter build apk --release"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"
OUT_IPA="$(printf '{"tool_input":{"command":"flutter build ipa --release"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"
if ! echo "$OUT_APK" | grep -q 'FLUTTER-PRIVACY-MANIFEST-MISSING' && echo "$OUT_IPA" | grep -q 'FLUTTER-PRIVACY-MANIFEST-MISSING'; then
  ok "Command-aware gate: apk build silent, ipa build fires, on the SAME both-platforms repo"
else
  bad "Command-aware gate: apk build silent, ipa build fires, on the SAME both-platforms repo"
fi
rm -rf "$D"

# 27 Donation link to a funding platform fires the Payments-policy finding on an Android tree
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } }\n' > "$D/app/build.gradle"
printf 'val donate = "https://opencollective.com/example/donate"\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PAYMENTS-DONATION-LINK' && ok "Open Collective donate link fires the Payments finding" || bad "Open Collective donate link fires the Payments finding"
rm -rf "$D"

# 28 Play billing with no refund-review handling surfaces the chargeback-liability finding
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } }\n' > "$D/app/build.gradle"
printf 'import com.android.billingclient.api.BillingClient\nval c = BillingClient.newBuilder(ctx)\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PLAY-CHARGEBACK-LIABILITY' && ok "Play billing without ReviewRefund handling surfaces chargeback liability" || bad "Play billing without ReviewRefund handling surfaces chargeback liability"
rm -rf "$D"

# 29 Play billing WITH refund-review handling stays silent on the chargeback finding
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } }\n' > "$D/app/build.gradle"
printf 'import com.android.billingclient.api.BillingClient\nfun onRtdn(n: PendingRefundReviewNotification) { reviewRefund(n) }\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +GOOGLE-PLAY-CHARGEBACK-LIABILITY ' && bad "Play billing with ReviewRefund handling stays silent" || ok "Play billing with ReviewRefund handling stays silent"
rm -rf "$D"

# 30 SIWA relay allowlist with only the old domain fires
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'let ok = email.hasSuffix("privaterelay.appleid.com")\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-4.0-SIWA-RELAY-DOMAIN' && ok "SIWA relay allowlist missing private.icloud.com fires" || bad "SIWA relay allowlist missing private.icloud.com fires"
rm -rf "$D"

# 31 SIWA relay allowlist with both domains stays silent
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'let ok = email.hasSuffix("privaterelay.appleid.com") || email.hasSuffix("private.icloud.com")\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +APPLE-4\.0-SIWA-RELAY-DOMAIN ' && bad "SIWA relay allowlist with both domains stays silent" || ok "SIWA relay allowlist with both domains stays silent"
rm -rf "$D"

# 32 External purchase link with no storefront gating fires
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'ExternalPurchaseLink.open()\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING' && ok "External purchase link without storefront gating fires" || bad "External purchase link without storefront gating fires"
rm -rf "$D"

# 33 External purchase link gated on the storefront stays silent
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'if Storefront.current?.countryCode == "USA" { ExternalPurchaseLink.open() }\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +APPLE-3\.1\.1-EXTERNAL-LINK-REGION-GATING ' && bad "External purchase link gated on storefront stays silent" || ok "External purchase link gated on storefront stays silent"
rm -rf "$D"

# 34 Declared Age Range without RESCIND_CONSENT fires
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'let r = DeclaredAgeRange.request()\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-5.1.1-RESCIND-CONSENT-UNHANDLED' && ok "Declared Age Range without RESCIND_CONSENT fires" || bad "Declared Age Range without RESCIND_CONSENT fires"
rm -rf "$D"

# 35 On-Demand Resources usage fires the deprecation finding
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf 'let req = NSBundleResourceRequest(tags: ["level2"])\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-ODR-DEPRECATED-27' && ok "On-Demand Resources usage fires" || bad "On-Demand Resources usage fires"
rm -rf "$D"

# 36 READ_CONTACTS on an API 37 target fires the contact-picker finding
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 37 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val p = "android.permission.READ_CONTACTS"\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-CONTACTS-PICKER-REQUIRED' && ok "READ_CONTACTS at API 37 fires contact-picker finding" || bad "READ_CONTACTS at API 37 fires contact-picker finding"
rm -rf "$D"

# 37 READ_CONTACTS on an API 36 target stays silent on the API 37 finding
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val p = "android.permission.READ_CONTACTS"\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +GOOGLE-CONTACTS-PICKER-REQUIRED ' && bad "READ_CONTACTS at API 36 stays silent on the API 37 finding" || ok "READ_CONTACTS at API 36 stays silent on the API 37 finding"
rm -rf "$D"

# 38 Local network discovery on API 37 without ACCESS_LOCAL_NETWORK fires
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 37 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val nsd = getSystemService(NsdManager::class.java)\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'ANDROID-LOCAL-NETWORK-PERMISSION' && ok "NsdManager at API 37 without ACCESS_LOCAL_NETWORK fires" || bad "NsdManager at API 37 without ACCESS_LOCAL_NETWORK fires"
rm -rf "$D"

# 39 Foreground service used for geofencing fires
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val perm = "android.permission.FOREGROUND_SERVICE_LOCATION"; fun geofenceLoop() {}\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-FGS-GEOFENCE-REMOVED' && ok "FGS geofencing fires" || bad "FGS geofencing fires"
rm -rf "$D"

# 40 Random chat app without minor blocking fires critical
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val tagline = "random chat with strangers"\n' > "$D/app/src/main/java/t/Src.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-ANON-CHAT-MINOR-BLOCK' && ok "Random chat without minor blocking fires" || bad "Random chat without minor blocking fires"
rm -rf "$D"

# 41 Release build without minifyEnabled true fires the R8 finding
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'val x = 1\n' > "$D/app/src/main/java/t/Src.kt"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled false } } }\n' > "$D/app/build.gradle"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'ANDROID-R8-OPTIMIZATION-MISSING' && ok "Missing R8 minify fires" || bad "Missing R8 minify fires"
rm -rf "$D"

# 42 Pipeline script calling the removed ASC age-rating endpoint fires critical
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist/>' > "$D/App/Info.plist"
printf '// curl https://api.appstoreconnect.apple.com/v1/appStoreVersions/123/ageRatingDeclaration\n' > "$D/App/A.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED' && ok "Removed ASC age-rating endpoint in a script fires" || bad "Removed ASC age-rating endpoint in a script fires"
rm -rf "$D"

# 43 A vendored build.gradle.kts under node_modules must not switch the Android section on for an iOS-only app
D="$(mktemp -d)"; mkdir -p "$D/node_modules/react-native" "$D/ios"
printf '{"name":"x"}' > "$D/package.json"
touch "$D/node_modules/react-native/build.gradle.kts" "$D/ios/Podfile"
OUT="$(bash "$GUARD" "$D" 2>&1)"
if echo "$OUT" | grep -q 'Android=0' && ! echo "$OUT" | grep -Eq '^\s+\[(CRITICAL|HIGH|MEDIUM)\]\s+(ANDROID|GOOGLE)-'; then ok "Vendored gradle file does not flip Android on"; else bad "Vendored gradle file does not flip Android on"; fi
rm -rf "$D"

# 44 NSPrivacyTracking true with no NSPrivacyTrackingDomains is the ITMS-91064 upload rejection and must block
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist><dict><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$D/App/Info.plist"
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSPrivacyTracking</key><true/><key>NSPrivacyTrackingDomains</key><array/></dict></plist>' > "$D/App/PrivacyInfo.xcprivacy"
OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-ITMS-91064-TRACKING-NO-DOMAINS' && [ "$RC" -eq 2 ] && ok "Tracking true with empty domains blocks" || bad "Tracking true with empty domains blocks (rc=$RC)"
rm -rf "$D"

# 45 A manifest that is not a plist cannot be compiled by Xcode, so it is a finding, never a silent pass
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist><dict><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$D/App/Info.plist"
printf '{}' > "$D/App/PrivacyInfo.xcprivacy"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-MANIFEST-UNREADABLE' && ok "Malformed manifest fires" || bad "Malformed manifest fires"
rm -rf "$D"

# 46 A manifest inside a Tests dir is a fixture, not a shipped manifest, and is not validated
D="$(mktemp -d)"; mkdir -p "$D/App" "$D/AppTests/Fixtures"
printf '<plist><dict><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$D/App/Info.plist"
printf '%s' "$PLIST_EMPTY" > "$D/App/PrivacyInfo.xcprivacy"
printf '{}' > "$D/AppTests/Fixtures/PrivacyInfo.xcprivacy"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'APPLE-MANIFEST-UNREADABLE' && bad "Manifest fixture under Tests is skipped" || ok "Manifest fixture under Tests is skipped"

# 47 A Python virtualenv inside the project is not app source. Its vendored JSON mentions betting,
# background location, and localhost, none of which the app ships.
D="$(mktemp -d)"; mkdir -p "$D/App" "$D/app/src/main" "$D/tool/.venv/lib/python3.12/site-packages/api"
printf '<plist/>' > "$D/App/Info.plist"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf '{"a": "fixed-odds betting", "b": "ACCESS_BACKGROUND_LOCATION", "c": "http://localhost:8080"}\n' > "$D/tool/.venv/lib/python3.12/site-packages/api/discovery.json"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +(APPLE-GAMBLING-BRAZIL-LICENSE|APPLE-2\.1-STAGING-BACKEND|GOOGLE-PERM-BACKGROUND-LOCATION) ' && bad "Virtualenv contents are not scanned as app source" || ok "Virtualenv contents are not scanned as app source"
rm -rf "$D"

# 48 Many privacy manifests, as every CocoaPods or SPM project has. `find | grep -q .` exited 141
# under pipefail once grep stopped reading, and reported the app's own manifest missing.
D="$(mktemp -d)"; mkdir -p "$D/ios/Runner" "$D/lib"
printf 'name: t\ndependencies:\n  permission_handler: ^11.0.0\n' > "$D/pubspec.yaml"
printf "import 'package:permission_handler/permission_handler.dart';\n" > "$D/lib/main.dart"
printf '<plist><dict></dict></plist>' > "$D/ios/Runner/Info.plist"
printf '{}' > "$D/ios/Runner/PrivacyInfo.xcprivacy"
for i in $(seq 1 1500); do mkdir -p "$D/ios/Pods/SomeVendoredPod$i/Resources"; printf '{}' > "$D/ios/Pods/SomeVendoredPod$i/Resources/PrivacyInfo.xcprivacy"; done
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +(FLUTTER|APPLE)-PRIVACY-MANIFEST-MISSING ' && bad "Existing privacy manifest is found among many (no SIGPIPE under pipefail)" || ok "Existing privacy manifest is found among many (no SIGPIPE under pipefail)"
rm -rf "$D"

# 49 A project that itself sits under folders named build and test is still scanned. Exclusions
# apply only below the project root.
P="$(mktemp -d)"; D="$P/build/test/app"; mkdir -p "$D"
S="$(mk_ios_bad)"; cp -R "$S/." "$D/"; rm -rf "$S"
OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-3.1.1-EXTERNAL-PAYMENT' && [ "$RC" -eq 2 ] && ok "Project under build/ and test/ parent folders is still scanned" || bad "Project under build/ and test/ parent folders is still scanned (rc=$RC)"
rm -rf "$P"

# 50 NSPrivacyCollectedDataTypes lives in PrivacyInfo.xcprivacy, so declaring it there satisfies the check.
D="$(mk_ios_bad_nutrition)"
printf '<plist><dict><key>NSPrivacyCollectedDataTypes</key><array/></dict></plist>' > "$D/App/PrivacyInfo.xcprivacy"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +APPLE-PRIVACY-NUTRITION-LABELS ' && bad "Privacy manifest declaring collected data types satisfies nutrition labels" || ok "Privacy manifest declaring collected data types satisfies nutrition labels"
rm -rf "$D"

# 51 Lowercase test folders (Flutter test/ and integration_test/, JS tests/) never ship either.
D="$(mktemp -d)"; mkdir -p "$D/App" "$D/test"
printf '<plist/>' > "$D/App/Info.plist"
printf 'func deleteAccount() { api.delete("/users/me") }\n' > "$D/App/A.swift"
printf '// the outgoing page must finish sliding after it is deactivated\n' > "$D/test/T.swift"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +APPLE-ACCOUNT-DELETION-WEAK ' && bad "Words in a lowercase test/ folder are not app source" || ok "Words in a lowercase test/ folder are not app source"
rm -rf "$D"

# 52 A cross-platform app selling digital goods through a store plugin, and physical goods through a
# payment SDK, is not an external-payment violation. Without the plugin it still is.
mk_flutter_pay() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/ios/Runner" "$d/android/app/src/main" "$d/lib"
  printf 'name: t\ndependencies:\n  razorpay_flutter: ^1.3.0\n%b' "$1" > "$d/pubspec.yaml"
  printf '<plist><dict></dict></plist>' > "$d/ios/Runner/Info.plist"
  printf '{}' > "$d/ios/Runner/PrivacyInfo.xcprivacy"
  printf '<manifest package="t"/>' > "$d/android/app/src/main/AndroidManifest.xml"
  echo "$d"
}
D="$(mk_flutter_pay '  in_app_purchase: ^3.2.0\n')"; OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +(GOOGLE-PLAY-BILLING|APPLE-3\.1\.1-EXTERNAL-PAYMENT) ' && bad "Store purchase plugin satisfies both IAP checks" || ok "Store purchase plugin satisfies both IAP checks"
rm -rf "$D"
D="$(mk_flutter_pay '')"; OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PLAY-BILLING' && echo "$OUT" | grep -q 'APPLE-3.1.1-EXTERNAL-PAYMENT' && ok "Payment SDK with no store plugin still fires both IAP checks" || bad "Payment SDK with no store plugin still fires both IAP checks"
rm -rf "$D"

# 53 "renew automatically until cancelled" is a renewal notice, not an instruction to call.
D="$(mktemp -d)"
printf '{"name":"t"}' > "$D/package.json"
printf '<html><body>Your subscription renews automatically until cancelled in your store account settings.</body></html>' > "$D/index.html"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +BOTH-SUBSCRIPTION-HARD-CANCEL ' && bad "Call inside automatically does not read as call to cancel" || ok "Call inside automatically does not read as call to cancel"
rm -rf "$D"

# 54 and 51, the two fixtures from #542. Prose about files is not a sensitive permission. READ_CONTACTS is.
mk_android_perm() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/android/app/src/main"
  printf '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET"/>%s</manifest>' "$1" > "$d/android/app/src/main/AndroidManifest.xml"
  printf 'android { compileSdk 36 }\n' > "$d/android/app/build.gradle"
  echo "$d"
}
D="$(mk_android_perm '')"
printf '<html><body>%s</body></html>' "$(for i in $(seq 1 20); do printf 'Export the files. '; done)" > "$D/notes.html"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +ANDROID-USER-DATA-DISCLOSURE ' && bad "#542 fixture A: prose about files stays silent" || ok "#542 fixture A: prose about files stays silent"
rm -rf "$D"
D="$(mk_android_perm '<uses-permission android:name="android.permission.READ_CONTACTS"/>')"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'ANDROID-USER-DATA-DISCLOSURE' && ok "#542 fixture B: READ_CONTACTS without disclosure fires" || bad "#542 fixture B: READ_CONTACTS without disclosure fires"
rm -rf "$D"

# 56 #542. Bundled web output under dist/ is a build artifact, not source.
D="$(mktemp -d)"; mkdir -p "$D/App" "$D/web/dist/assets"
printf '<plist/>' > "$D/App/Info.plist"
printf 'const u="http://localhost:54321/auth/v1";\n' > "$D/web/dist/assets/index-abc123.js"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^  \[(CRITICAL|HIGH|MEDIUM)\] +APPLE-2\.1-STAGING-BACKEND ' && bad "Bundled dist/ output is not scanned as source" || ok "Bundled dist/ output is not scanned as source"
rm -rf "$D"

# 57 targetSdk lives two levels down in every real project. The old ** glob never read android/app/build.gradle
D="$(mktemp -d)"; mkdir -p "$D/android/app/src/main"
printf '<manifest package="t"/>' > "$D/android/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 35 } buildTypes { release { minifyEnabled true } } }\n' > "$D/android/app/build.gradle"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^ +\[CRITICAL\] +GOOGLE-TARGET-API ' && ok "targetSdk 35 two levels deep fires the API 36 floor" || bad "targetSdk 35 two levels deep fires the API 36 floor"
printf 'android { defaultConfig { targetSdk = 36 } buildTypes { release { isMinifyEnabled = true } } }\n' > "$D/android/app/build.gradle"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^ +\[CRITICAL\] +GOOGLE-TARGET-API ' && bad "targetSdk 36 stays silent" || ok "targetSdk 36 stays silent"
rm -rf "$D"

# 58 Play Billing Library 7 dependency fires the v8 floor, 8 stays silent
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\ndependencies { implementation "com.android.billingclient:billing-ktx:7.1.1" }\n' > "$D/app/build.gradle"
printf 'val c = BillingClient.newBuilder(ctx)\n' > "$D/app/src/main/java/t/Pay.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^ +\[CRITICAL\] +GOOGLE-PLAY-BILLING-V8-REQUIRED ' && ok "Billing Library 7 fires the v8 floor" || bad "Billing Library 7 fires the v8 floor"
sed -i.bak 's/billing-ktx:7.1.1/billing-ktx:8.0.0/' "$D/app/build.gradle"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -Eq '^ +\[CRITICAL\] +GOOGLE-PLAY-BILLING-V8-REQUIRED ' && bad "Billing Library 8 stays silent" || ok "Billing Library 8 stays silent"
rm -rf "$D"

# 59 READ_MEDIA_IMAGES without the photo picker surfaces the declaration, with the picker it stays silent
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest><uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/></manifest>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PHOTO-VIDEO-PERMISSIONS-DECLARATION' && ok "READ_MEDIA_IMAGES without a picker surfaces the declaration" || bad "READ_MEDIA_IMAGES without a picker surfaces the declaration"
printf 'val p = registerForActivityResult(PickVisualMedia()) {}\n' > "$D/app/src/main/java/t/Pick.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PHOTO-VIDEO-PERMISSIONS-DECLARATION' && bad "READ_MEDIA_IMAGES with the photo picker stays silent" || ok "READ_MEDIA_IMAGES with the photo picker stays silent"
rm -rf "$D"

# 60 an AccountManager import with no declared permission is not a data-collection signal
D="$(mktemp -d)"; mkdir -p "$D/app/src/main/java/t"
printf '<manifest><uses-permission android:name="android.permission.INTERNET"/></manifest>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'import android.accounts.AccountManager\n// ContactsContract is not used here\n' > "$D/app/src/main/java/t/A.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'ANDROID-USER-DATA-DISCLOSURE' && bad "Symbol in an import without a declared permission stays silent" || ok "Symbol in an import without a declared permission stays silent"
rm -rf "$D"

# 61 src/dist is an Android product-flavor source set and must be scanned, web/dist is build output and must not
D="$(mktemp -d)"; mkdir -p "$D/app/src/main" "$D/app/src/dist/java/t"
printf '<manifest package="t"/>' > "$D/app/src/main/AndroidManifest.xml"
printf 'android { defaultConfig { targetSdkVersion 36 } buildTypes { release { minifyEnabled true } } }\n' > "$D/app/build.gradle"
printf 'import com.stripe.android.Stripe\n' > "$D/app/src/dist/java/t/Pay.kt"
OUT="$(bash "$GUARD" "$D" 2>&1)"
echo "$OUT" | grep -q 'GOOGLE-PLAY-BILLING' && ok "Stripe inside a src/dist flavor tree is still seen" || bad "Stripe inside a src/dist flavor tree is still seen"
rm -rf "$D"

# 62 a privacy manifest whose root is an array fires through the guard, never a silent pass
D="$(mktemp -d)"; mkdir -p "$D/App"
printf '<plist><dict><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$D/App/Info.plist"
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><array/></plist>' > "$D/App/PrivacyInfo.xcprivacy"
OUT="$(bash "$GUARD" "$D" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-MANIFEST-UNREADABLE' && [ "$RC" -eq 2 ] && ok "Array-root manifest blocks" || bad "Array-root manifest blocks (rc=$RC)"
rm -rf "$D"

# ===== Issue #610. The hook payload parser must be JSON-aware. Real Claude Code payloads below =====
# (.tool_input.command inside JSON). The old regex truncated at an escaped quote and left \n literal.
BS='\'
P_QUOTED='{"tool_name":"Bash","tool_input":{"command":"cd '"$BS"'"$CLAUDE_PROJECT_DIR/apps/app'"$BS"'" && npx eas submit --platform ios"}}'
P_CONT='{"tool_input":{"command":"npx eas '"$BS$BS$BS"'n  submit --platform ios"}}'
P_TWOCMD='{"tool_input":{"command":"echo eas'"$BS"'nsubmit --platform ios"}}'
P_TABCRLF='{"tool_input":{"command":"npx'"$BS"'teas'"$BS"'tsubmit --platform ios'"$BS"'r'"$BS"'n"}}'
P_QUOTED_CONT='{"tool_input":{"command":"cd '"$BS"'"$CLAUDE_PROJECT_DIR/apps/app'"$BS"'" && npx eas '"$BS$BS$BS"'n submit --platform ios"}}'
P_QUOTED_TEST='{"tool_input":{"command":"cd '"$BS"'"$HOME/my app'"$BS"'" && npm test"}}'
P_COMMITMSG='{"tool_input":{"command":"git commit -m '"$BS"'"docs: note that eas submit needs a profile'"$BS"'""}}'

# 63 a quoted path before the submit command must still be scanned
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_QUOTED" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-1 quoted path before eas submit is scanned" || bad "610-1 quoted path before eas submit is scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 64 a backslash-newline continuation must not hide the trigger
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_CONT" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-2 line continuation before submit is scanned" || bad "610-2 line continuation before submit is scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 65 a bare newline separates commands. "eas" on one line and "submit" on the next is NOT a submit
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_TWOCMD" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-3 trigger split across two commands is never invented" || bad "610-3 trigger split across two commands is never invented (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 66 on a block in hook mode the report reaches stderr (the only stream Claude Code shows on exit 2)
D="$(mk_ios_bad)"
ERR="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 >/dev/null)"; RC=$?
echo "$ERR" | grep -q 'BLOCKED' && echo "$ERR" | grep -q 'CRITICAL' && [ "$RC" -eq 2 ] && ok "610-4 hook-mode block report is on stderr" || bad "610-4 hook-mode block report is on stderr (rc=$RC bytes=${#ERR})"
rm -rf "$D"

# 67 a passing hook-mode scan keeps its report on stdout, and stderr stays quiet
D="$(mk_ios_clean)"
STDOUT="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>/dev/null)"; RC=$?
ERR="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 >/dev/null)"
echo "$STDOUT" | grep -q 'Summary\.' && [ "$RC" -eq 0 ] && ! echo "$ERR" | grep -q 'Summary\.' && ok "610-5 hook-mode pass report stays on stdout" || bad "610-5 hook-mode pass report stays on stdout (rc=$RC)"
rm -rf "$D"

# 68 standalone mode is unchanged. the report is on stdout even when it blocks
D="$(mk_ios_bad)"
STDOUT="$(bash "$GUARD" "$D" 2>/dev/null)"; RC=$?
echo "$STDOUT" | grep -q 'BLOCKED' && [ "$RC" -eq 2 ] && ok "610-6 standalone block report stays on stdout" || bad "610-6 standalone block report stays on stdout (rc=$RC)"
rm -rf "$D"

# 69 CRLF inside the command and a tab between the words are folded, the trigger still matches
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_TABCRLF" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-7 tabs and CRLF inside the command still match" || bad "610-7 tabs and CRLF inside the command still match (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 70 without jq the fallback decoder still handles the quoted path (a vendored copy on a runner without jq)
D="$(mk_ios_bad)"
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil python3 xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done
OUT="$(printf '%s' "$P_QUOTED" | PATH="$NOJQ" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-8 quoted path is scanned without jq on PATH" || bad "610-8 quoted path is scanned without jq on PATH (rc=$RC bytes=${#OUT})"
rm -rf "$D" "$NOJQ"

# 71 without jq AND python3 the last-resort decoder still unescapes the quoted path and the continuation
D="$(mk_ios_bad)"
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done
OUT="$(printf '%s' "$P_QUOTED_CONT" | PATH="$NOJQ" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-9 quoted path plus continuation is scanned with neither jq nor python3" || bad "610-9 quoted path plus continuation is scanned with neither jq nor python3 (rc=$RC bytes=${#OUT})"
rm -rf "$D" "$NOJQ"

# 72 a payload with the command at the top level (older hook shape) is still read
D="$(mk_ios_bad)"
OUT="$(printf '{"command":"fastlane pilot upload"}' | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-10 top-level command key is read" || bad "610-10 top-level command key is read (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 73 malformed JSON payload fails open, silently
OUT="$(printf '{"tool_input":{"command":"fastlane deliver' | bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && [ -z "$OUT" ] && ok "610-11 malformed payload fails open silently" || bad "610-11 malformed payload fails open silently (rc=$RC out=$OUT)"

# 74 a non-string command (object) fails open, silently
OUT="$(printf '{"tool_input":{"command":{"nested":true}}}' | bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && [ -z "$OUT" ] && ok "610-12 non-string command fails open silently" || bad "610-12 non-string command fails open silently (rc=$RC out=$OUT)"

# 75 a quoted non-submit command stays silent (decoding must not widen the trigger)
OUT="$(printf '%s' "$P_QUOTED_TEST" | bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-13 quoted non-submit command stays silent" || bad "610-13 quoted non-submit command stays silent (rc=$RC out=$OUT)"

# 76 the trigger phrase inside a commit message is scanned on the conservative side, never a silent skip.
# The scan on a clean project must exit 0, so a commit message never blocks anyone.
D="$(mk_ios_clean)"
OUT="$(printf '%s' "$P_COMMITMSG" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "610-14 trigger phrase inside a commit message never blocks a clean project" || bad "610-14 trigger phrase inside a commit message never blocks a clean project (rc=$RC)"
rm -rf "$D"

# 77 a 200KB payload with the command at the end is decoded and scanned
D="$(mk_ios_bad)"
PAD="$(head -c 200000 /dev/zero | tr '\0' 'x')"
OUT="$(printf '{"tool_input":{"description":"%s","command":"npx eas submit --platform ios"}}' "$PAD" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-15 large payload is decoded and scanned" || bad "610-15 large payload is decoded and scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# ===== Issue #610, second round. Counterexamples from the adversarial review, pinned =====
NOTOOLS="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOTOOLS/$b"; done
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil python3 xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done
P_ESCBS='{"tool_input":{"command":"gradlew '"$BS$BS$BS$BS$BS"'nbundleRelease"}}'
P_BSSPACE='{"tool_input":{"command":"npx eas '"$BS$BS"' '"$BS"'nsubmit --platform ios"}}'
P_META_OK='{"meta":{"command":"eas submit"},"tool_input":{"command":"ls"}}'
P_META_BROKEN='{"meta":{"command":"eas submit"},"tool_input":{"command":"ls"},BROKEN'
P_FALSE='{"tool_input":{"command":false},"command":"fastlane pilot upload"}'
P_UESC='{"tool_input":{"command":"'"$BS"'u0065as submit --platform ios"}}'

# 78 two backslashes before a newline are an escaped backslash plus a separator, not a continuation
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_ESCBS" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-16 escaped backslash before a newline is not folded" || bad "610-16 escaped backslash before a newline is not folded (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 79 a backslash followed by a space and then a newline is not a continuation either
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_BSSPACE" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-17 backslash space newline is not folded" || bad "610-17 backslash space newline is not folded (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 80 a trigger under a sibling key never wins over tool_input.command, on every tier
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ" "$NOTOOLS"; do
  OUT="$(printf '%s' "$P_META_OK" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  [ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-18 sibling command key is ignored (tier=${tier##*/})" || bad "610-18 sibling command key is ignored (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 81 a malformed payload with a trigger under a sibling key stays silent when a real parser is installed
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ"; do
  OUT="$(printf '%s' "$P_META_BROKEN" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  [ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-19 malformed payload never scans a sibling key (tier=${tier##*/})" || bad "610-19 malformed payload never scans a sibling key (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 82 a non-string tool_input.command falls through to the top-level command identically on jq and python3
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ"; do
  OUT="$(printf '%s' "$P_FALSE" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-20 false tool_input.command falls through to top-level (tier=${tier##*/})" || bad "610-20 false tool_input.command falls through to top-level (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 83 an ASCII unicode escape in the command is read on every tier, including the no-tools fallback
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ" "$NOTOOLS"; do
  OUT="$(printf '%s' "$P_UESC" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-21 unicode-escaped trigger is read (tier=${tier##*/})" || bad "610-21 unicode-escaped trigger is read (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 84 the three tiers agree byte for byte on the two payloads from the issue
D="$(mk_ios_bad)"
for p in "$P_QUOTED" "$P_CONT"; do
  A="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 | grep -E '^  \[|^Summary\.|^BLOCKED')"
  B="$(printf '%s' "$p" | PATH="$NOJQ" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 | grep -E '^  \[|^Summary\.|^BLOCKED')"
  C="$(printf '%s' "$p" | PATH="$NOTOOLS" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 | grep -E '^  \[|^Summary\.|^BLOCKED')"
  [ -n "$A" ] && [ "$A" = "$B" ] && [ "$B" = "$C" ] && ok "610-22 tiers agree on an issue payload" || bad "610-22 tiers agree on an issue payload (jq=${#A} py=${#B} none=${#C})"
done
rm -rf "$D"

# 85 there is no stdin cap. a 34MB valid payload with the command up front is read and scanned
D="$(mk_ios_bad)"
BIG="$(mktemp)"; { printf '{"tool_input":{"command":"npx eas submit --platform ios","description":"'; head -c 34000000 /dev/zero | tr '\0' 'x'; printf '"}}'; } > "$BIG"
OUT="$(CLAUDE_PROJECT_DIR="$D" bash "$GUARD" < "$BIG" 2>&1)"; RC=$?; rm -f "$BIG"
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-23 34MB valid payload is read and scanned" || bad "610-23 34MB valid payload is read and scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"
rm -rf "$NOTOOLS" "$NOJQ"

# ===== Issue #610, third round. Reporter persona findings, pinned =====
P_ECHO='{"tool_input":{"command":"echo '"$BS"'"eas submit --platform ios'"$BS"'""}}'
P_GREP='{"tool_input":{"command":"grep -rn '"'"'eas submit'"'"' docs/"}}'
P_COMMENT='{"tool_input":{"command":"ls -la # then npx eas submit --platform ios"}}'
P_COMMENT_ECHO='{"tool_input":{"command":"echo hi # then npx eas submit --platform ios"}}'
P_SHC='{"tool_input":{"command":"bash -c '"$BS"'"npx eas submit --platform ios'"$BS"'""}}'
P_CD_APP='{"tool_input":{"command":"cd '"$BS"'"$CLAUDE_PROJECT_DIR/apps/app'"$BS"'" && npx eas submit --platform ios"}}'
P_CD_REL='{"tool_input":{"command":"cd apps/app; eas submit -p ios --latest"}}'
P_CD_OUT='{"tool_input":{"command":"cd /tmp && npx eas submit --platform ios"}}'
P_BOM="$(printf '\357\273\277')"'{"tool_input":{"command":"fastlane pilot upload"}}'

mk_expo_mono() {
  local d; d="$(mktemp -d)"; mkdir -p "$d/apps/app/ios/App" "$d/apps/kiosk/ios/Kiosk" "$d/node_modules/x"
  printf '{"name":"root","workspaces":["apps/*"]}' > "$d/package.json"
  printf '{"expo":{"name":"app"}}' > "$d/apps/app/app.json"
  printf '<plist><dict></dict></plist>' > "$d/apps/app/ios/App/Info.plist"
  printf 'import CoreLocation\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\n' > "$d/apps/app/ios/App/A.swift"
  printf '<plist><dict><key>NSLocationWhenInUseUsageDescription</key><string>Show stores</string><key>ITSAppUsesNonExemptEncryption</key><false/></dict></plist>' > "$d/apps/kiosk/ios/Kiosk/Info.plist"
  printf '%s' "$PLIST_EMPTY" > "$d/apps/kiosk/ios/Kiosk/PrivacyInfo.xcprivacy"
  printf 'import StoreKit\nlet policy="https://kiosk.example.io/privacy-policy"\n' > "$d/apps/kiosk/ios/Kiosk/K.swift"
  echo "$d"
}

# 86 echo of the trigger text is not a submit
OUT="$(printf '%s' "$P_ECHO" | bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-24 echo of the trigger text stays silent" || bad "610-24 echo of the trigger text stays silent (rc=$RC bytes=${#OUT})"

# 87 grep for the trigger text is not a submit
OUT="$(printf '%s' "$P_GREP" | bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-25 grep for the trigger text stays silent" || bad "610-25 grep for the trigger text stays silent (rc=$RC bytes=${#OUT})"

# 88 a trailing comment is blanked only behind a text-only command. behind anything else it scans on the
# conservative side (a comment can start inside a quoted wrapper argument) and a clean project still passes.
D="$(mk_ios_clean)"
OUT="$(printf '%s' "$P_COMMENT_ECHO" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-26 comment behind echo stays silent" || bad "610-26 comment behind echo stays silent (rc=$RC bytes=${#OUT})"
OUT="$(printf '%s' "$P_COMMENT" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "610-26 comment behind ls scans and a clean project passes" || bad "610-26 comment behind ls scans and a clean project passes (rc=$RC)"
rm -rf "$D"

# 89 a submit wrapped in bash -c "..." is still a submit and is scanned
D="$(mk_ios_bad)"
OUT="$(printf '%s' "$P_SHC" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-27 submit inside bash -c is scanned" || bad "610-27 submit inside bash -c is scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 90 a leading cd into an app inside the project scopes the scan to that app, quoted and relative forms
D="$(mk_expo_mono)"
for p in "$P_CD_APP" "$P_CD_REL"; do
  OUT="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q "^Project\. .*/apps/app$" && echo "$OUT" | grep -q 'MISSING-USAGE-DESCRIPTION' && [ "$RC" -eq 2 ] && ok "610-28 leading cd scopes the scan to the app" || bad "610-28 leading cd scopes the scan to the app (rc=$RC)"
done
rm -rf "$D"

# 91 a leading cd outside the project root is ignored and the root is scanned
D="$(mk_expo_mono)"
OUT="$(printf '%s' "$P_CD_OUT" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q "^Project\. $D$" && ok "610-29 cd outside the project root is ignored" || bad "610-29 cd outside the project root is ignored (rc=$RC)"
rm -rf "$D"

# 92 a UTF-8 BOM before the payload is read on every tier
D="$(mk_ios_bad)"
NOTOOLS="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOTOOLS/$b"; done
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil python3 xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done
for tier in "$PATH" "$NOJQ" "$NOTOOLS"; do
  OUT="$(printf '%s' "$P_BOM" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-30 BOM payload is read (tier=${tier##*/})" || bad "610-30 BOM payload is read (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D" "$NOTOOLS" "$NOJQ"

# ===== Issue #610, fourth round. Hook-contract persona findings, pinned =====
P_MCP='{"hook_event_name":"PreToolUse","tool_name":"mcp__some__runner","tool_input":{"command":"eas submit --platform ios"}}'
P_EDIT='{"hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"x.md","new_string":"run eas submit"},"command":"eas submit --platform ios"}'
P_NUL='{"tool_name":"Bash","tool_input":{"command":"./gradlew '"$BS"'u0000 bundleRelease"}}'

# 93 a payload from any tool other than Bash is never scanned, even when it carries a command key
D="$(mk_ios_bad)"
for p in "$P_MCP" "$P_EDIT"; do
  OUT="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  [ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-31 non-Bash tool payload stays silent" || bad "610-31 non-Bash tool payload stays silent (rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 94 a 5MB payload that is valid JSON with the command up front is scanned, well under the cap
D="$(mk_ios_bad)"
BIG="$(mktemp)"; { printf '{"tool_name":"Bash","tool_input":{"command":"npx eas submit --platform ios","description":"'; head -c 5000000 /dev/zero | tr '\0' 'x'; printf '"}}'; } > "$BIG"
OUT="$(bash "$GUARD" < "$BIG" 2>&1)"; RC=$?; rm -f "$BIG"
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-32 5MB valid payload is scanned" || bad "610-32 5MB valid payload is scanned (rc=$RC bytes=${#OUT})"
rm -rf "$D"

# 95 a NUL byte inside the command never leaks a bash warning to stderr on a pass
D="$(mk_ios_clean)"
ERR="$(printf '%s' "$P_NUL" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 >/dev/null)"; RC=$?
[ "$RC" -eq 0 ] && [ -z "$ERR" ] && ok "610-33 NUL byte in the command keeps stderr empty on a pass" || bad "610-33 NUL byte in the command keeps stderr empty on a pass (rc=$RC err=${ERR:0:80})"
rm -rf "$D"

# ===== Issue #610, fifth round. Second adversarial review, pinned. A submit can never hide in quotes =====
P_QSUB='{"tool_input":{"command":"eas '"$BS"'"submit'"$BS"'" --platform ios"}}'
P_SEMI_SHC='{"tool_input":{"command":"true;bash -c '"'"'eas submit --platform ios'"'"'"}}'
P_PY_OS='{"tool_input":{"command":"python3 -c '"'"'import os; os.system('"$BS"'"eas submit --platform ios'"$BS"'")'"'"'"}}'
P_SUBST='{"tool_input":{"command":"x='"$BS"'"$(bash -c '"'"'npx eas submit --platform ios'"'"')'"$BS"'""}}'
P_ABS_SH='{"tool_input":{"command":"/bin/sh -c '"'"'eas submit --platform ios'"'"'"}}'
P_TWO_CD='{"tool_input":{"command":"cd apps/app && cd ../kiosk && npx eas submit --platform ios"}}'
P_TWO_DOCS='{"tool_input":{"command":"eas submit --platform ios"}} {"tool_input":{"command":"echo"}}'
P_NESTED_TN='{"metadata":{"tool_name":"Edit"},"tool_name":"Bash","tool_input":{"command":"fastlane pilot upload"}}'
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil python3 xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done

# 96 a submit is scanned however it is quoted or wrapped
D="$(mk_ios_bad)"
for p in "$P_QSUB" "$P_SEMI_SHC" "$P_PY_OS" "$P_SUBST" "$P_ABS_SH"; do
  OUT="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-34 quoted or wrapped submit is scanned" || bad "610-34 quoted or wrapped submit is scanned (rc=$RC bytes=${#OUT} payload=${p:0:60})"
done
rm -rf "$D"

# 97 two cd's in one command never scope the scan. the root is scanned as before
D="$(mk_expo_mono)"
OUT="$(printf '%s' "$P_TWO_CD" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q "^Project\. $D$" && ok "610-35 two cd's fall back to the project root" || bad "610-35 two cd's fall back to the project root (rc=$RC)"
rm -rf "$D"

# 98 two concatenated JSON documents are not one payload. silent on jq and on python3
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ"; do
  OUT="$(printf '%s' "$P_TWO_DOCS" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  [ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-36 concatenated documents stay silent (tier=${tier##*/})" || bad "610-36 concatenated documents stay silent (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D"

# 99 a nested metadata tool_name never masks the real top-level Bash tool_name on the JSON tiers
D="$(mk_ios_bad)"
for tier in "$PATH" "$NOJQ"; do
  OUT="$(printf '%s' "$P_NESTED_TN" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-37 nested tool_name does not mask Bash (tier=${tier##*/})" || bad "610-37 nested tool_name does not mask Bash (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done
rm -rf "$D" "$NOJQ"

# ===== Issue #610, sixth round. Portability persona. the no-tools unescape must stay linear =====
# 100 a 300KB command reaches the no-tools tier and is unescaped and scanned in seconds, not minutes
D="$(mk_ios_bad)"
NOTOOLS="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOTOOLS/$b"; done
BIG="$(mktemp)"; { printf '{"tool_input":{"command":"npx eas submit --platform ios && echo '; head -c 300000 /dev/zero | tr '\0' 'x'; printf '"}}'; } > "$BIG"
T0=$(date +%s); OUT="$(PATH="$NOTOOLS" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" < "$BIG" 2>&1)"; RC=$?; T1=$(date +%s); rm -f "$BIG"
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && [ $((T1-T0)) -lt 20 ] && ok "610-38 300KB command is scanned on the no-tools tier in $((T1-T0))s" || bad "610-38 300KB command is scanned on the no-tools tier (rc=$RC secs=$((T1-T0)) bytes=${#OUT})"
rm -rf "$D" "$NOTOOLS"

# ===== Issue #610, seventh round. Fuzz persona. a present but broken parser never disables the guard =====
mk_broken_tool_path() {  # $1 = name of the tool to break, everything else real, jq and python3 otherwise absent
  local d; d="$(mktemp -d)"
  for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$d/$b"; done
  printf '#!/bin/sh\necho "xcrun: error: invalid active developer path" >&2\nexit 1\n' > "$d/$1"; chmod +x "$d/$1"
  echo "$d"
}
P_FF='{"tool_input":{"command":"eas'"$BS"'fsubmit --platform ios"}}'
P_NESTED_TI='{"command":"ls","tool_input":{"env":{"x":"y"},"command":"eas submit --platform ios"}}'

# 101 the macOS python3 stub (no Command Line Tools) or a stale pyenv shim must fall through, never silence the guard
D="$(mk_ios_bad)"
for tool in python3 jq; do
  BROKEN="$(mk_broken_tool_path "$tool")"
  OUT="$(printf '%s' "$P_QUOTED" | PATH="$BROKEN" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-39 broken $tool on PATH falls through and the submit is scanned" || bad "610-39 broken $tool on PATH falls through and the submit is scanned (rc=$RC bytes=${#OUT})"
  rm -rf "$BROKEN"
done
rm -rf "$D"

# 102 a form feed between the tool and the verb is whitespace on every tier
D="$(mk_ios_bad)"
NOTOOLS="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOTOOLS/$b"; done
for tier in "$PATH" "$NOTOOLS"; do
  OUT="$(printf '%s' "$P_FF" | PATH="$tier" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-40 form feed separator is read (tier=${tier##*/})" || bad "610-40 form feed separator is read (tier=${tier##*/} rc=$RC bytes=${#OUT})"
done

# 103 a nested object ahead of the command key inside tool_input does not fool the no-tools tier
OUT="$(printf '%s' "$P_NESTED_TI" | PATH="$NOTOOLS" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-41 nested object inside tool_input is skipped over" || bad "610-41 nested object inside tool_input is skipped over (rc=$RC bytes=${#OUT})"
rm -rf "$D" "$NOTOOLS"

# ===== Issue #610, eighth round. Third adversarial review. an inert text command cannot smuggle a submit =====
P_ECHO_SUBST='{"tool_input":{"command":"echo '"$BS"'"$(eas submit --platform ios)'"$BS"'""}}'
P_ECHO_PIPE='{"tool_input":{"command":"echo '"$BS"'"eas submit --platform ios'"$BS"'" | sh"}}'
P_GIT_ALIAS='{"tool_input":{"command":"git -c alias.ship='"'"'!npx eas submit --platform ios'"'"' ship"}}'
P_GIT_MSG='{"tool_input":{"command":"git commit -m '"$BS"'"docs: note that eas submit needs a profile'"$BS"'""}}'

# 104 a submit inside a command substitution, a pipe, or a git alias behind an inert-looking command is scanned
D="$(mk_ios_bad)"
for p in "$P_ECHO_SUBST" "$P_ECHO_PIPE" "$P_GIT_ALIAS"; do
  OUT="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-42 smuggled submit behind a text command is scanned" || bad "610-42 smuggled submit behind a text command is scanned (rc=$RC bytes=${#OUT} payload=${p:0:60})"
done
rm -rf "$D"

# 105 a plain echo of the trigger with no substitution, pipe, or separator is still silent
OUT="$(printf '%s' "$P_ECHO" | bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-43 plain echo of the trigger stays silent" || bad "610-43 plain echo of the trigger stays silent (rc=$RC bytes=${#OUT})"

# 106 git is no longer inert (aliases and exec flags run commands). a commit message scans and a clean project passes
D="$(mk_ios_clean)"
OUT="$(printf '%s' "$P_GIT_MSG" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "610-44 git commit message scans and a clean project passes" || bad "610-44 git commit message scans and a clean project passes (rc=$RC)"
rm -rf "$D"

# ===== Issue #610, ninth round. Fourth adversarial review. a parser that passes its probe but fails for real falls through =====
mk_shim_path() {  # $1 tool name to shim, $2 shim body, $3 = jq|python3|none to keep real on PATH besides the shim
  local d; d="$(mktemp -d)"
  for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$d/$b"; done
  [ "$3" = jq ] && ln -s "$(command -v jq)" "$d/jq"; [ "$3" = python3 ] && ln -s "$(command -v python3)" "$d/python3"
  printf '%s\n' "$2" > "$d/$1"; chmod +x "$d/$1"
  echo "$d"
}
P_UNI='{"tool_input":{"command":"cd apps/caf\xc3\xa9 && npx eas submit --platform ios"}}'

# 107 a jq that answers the probe but dies on real input falls through to python3 and the submit is scanned
D="$(mk_ios_bad)"
SHIM="$(mk_shim_path jq '#!/bin/sh
[ "$1" = "-n" ] && exit 0
echo "jq: error: segfault" >&2; exit 2' python3)"
OUT="$(printf '%s' "$P_QUOTED" | PATH="$SHIM" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-45 jq that fails on real input falls through" || bad "610-45 jq that fails on real input falls through (rc=$RC bytes=${#OUT})"
rm -rf "$SHIM"

# 108 a python3 that answers the probe but dies on real input falls through to the regex tier and the submit is scanned
SHIM="$(mk_shim_path python3 '#!/bin/sh
[ "$2" = "pass" ] && exit 0
echo "Fatal Python error" >&2; exit 1' none)"
OUT="$(printf '%s' "$P_QUOTED" | PATH="$SHIM" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-46 python3 that fails on real input falls through" || bad "610-46 python3 that fails on real input falls through (rc=$RC bytes=${#OUT})"
rm -rf "$SHIM"

# 109 a genuinely invalid payload rejected by python3 stays silent (rejection is authoritative, not a crash)
SHIM="$(mk_shim_path jq '#!/bin/sh
exit 2' python3)"
OUT="$(printf '{"tool_input":{"command":"fastlane deliver' | PATH="$SHIM" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
[ -z "$OUT" ] && [ "$RC" -eq 0 ] && ok "610-47 python3 rejecting invalid JSON stays silent" || bad "610-47 python3 rejecting invalid JSON stays silent (rc=$RC bytes=${#OUT})"
rm -rf "$SHIM"

# 110 PYTHONIOENCODING=ascii never drops a command with a non-ASCII path on the python3 tier
NOJQ="$(mktemp -d)"; for b in bash grep sed awk find xargs tr head mktemp cat rm printf wc sort uniq cut plutil python3 xmllint dirname basename date; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NOJQ/$b"; done
OUT="$(printf "$P_UNI" | PYTHONIOENCODING=ascii PATH="$NOJQ" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-48 non-ASCII path survives PYTHONIOENCODING=ascii" || bad "610-48 non-ASCII path survives PYTHONIOENCODING=ascii (rc=$RC bytes=${#OUT})"
rm -rf "$NOJQ"

# 111 with no temp file available the pass report stays on stdout and a block still puts its reason on stderr
SHIM="$(mk_shim_path mktemp '#!/bin/sh
exit 1' jq)"; ln -s "$(command -v python3)" "$SHIM/python3"
ERR="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | PATH="$SHIM" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1 >/dev/null)"; RC=$?
echo "$ERR" | grep -q '^BLOCKED\.' && [ "$RC" -eq 2 ] && ok "610-49 degraded routing still puts the block reason on stderr" || bad "610-49 degraded routing still puts the block reason on stderr (rc=$RC err=${ERR:0:80})"
rm -rf "$D"
D="$(mk_ios_clean)"
STDOUT="$(printf '{"tool_input":{"command":"fastlane deliver --submit"}}' | PATH="$SHIM" CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>/dev/null)"; RC=$?
echo "$STDOUT" | grep -q 'Summary\.' && [ "$RC" -eq 0 ] && ok "610-50 degraded routing keeps the pass report on stdout" || bad "610-50 degraded routing keeps the pass report on stdout (rc=$RC bytes=${#STDOUT})"
rm -rf "$D" "$SHIM"

# ===== Issue #610, tenth round. Fifth adversarial review. a backslash before a letter is the letter =====
P_LETTER_ESC='{"tool_input":{"command":"eas s'"$BS$BS"'ubmit --platform ios"}}'
P_CONT_ESC='{"tool_input":{"command":"eas '"$BS$BS$BS"'n'"$BS$BS"'submit --platform ios"}}'

# 112 eas s\ubmit and a continuation followed by \submit are both plain eas submit to the shell, and are scanned
D="$(mk_ios_bad)"
for p in "$P_LETTER_ESC" "$P_CONT_ESC"; do
  OUT="$(printf '%s' "$p" | CLAUDE_PROJECT_DIR="$D" bash "$GUARD" 2>&1)"; RC=$?
  echo "$OUT" | grep -q 'App Store Compliance Guard' && [ "$RC" -eq 2 ] && ok "610-51 letter escape inside the verb is scanned" || bad "610-51 letter escape inside the verb is scanned (rc=$RC bytes=${#OUT} payload=${p:0:60})"
done
rm -rf "$D"

echo ""
echo "app-store-compliance-guard-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
