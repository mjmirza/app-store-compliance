#!/usr/bin/env bash
# App Store Compliance Guard. Native and cross-platform (Flutter, RN/Expo, Ionic/Capacitor).
# Standalone or PreToolUse Bash hook on a submit command. See docs/CROSS-PLATFORM-FRAMEWORKS.md.
# @event: PreToolUse
# @matcher: Bash
set -uo pipefail

HOOK_LOG="$HOME/.claude/hooks/hook-log.sh"
# shellcheck disable=SC1090
[ -f "$HOOK_LOG" ] && source "$HOOK_LOG" 2>/dev/null || true
log_err() { if type hlog_error >/dev/null 2>&1; then hlog_error "app-store-compliance-guard" "$@"; else echo "app-store-compliance-guard: $*" >&2; fi; }

CRIT=0; HIGH=0; MED=0
FILELIST=""
cleanup() { [ -n "$FILELIST" ] && rm -f "$FILELIST" 2>/dev/null || true; }
trap cleanup EXIT

# ----- resolve mode and project dir -----
DIR=""
STDIN_JSON=""
CMD=""
if [ "$#" -ge 1 ] && [ -d "$1" ]; then
  DIR="$1"                                   # standalone with explicit path
elif [ ! -t 0 ]; then
  STDIN_JSON="$(cat 2>/dev/null || true)"    # hook mode, payload on stdin
fi

if [ -n "$STDIN_JSON" ]; then
  CMD="$(printf '%s' "$STDIN_JSON" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"//; s/"$//')"
  # Only act on submission style commands. Otherwise stay silent.
  if ! printf '%s' "$CMD" | grep -qiE 'fastlane[[:space:]]+(deliver|pilot|supply|submit)|eas[[:space:]]+(submit|build)|xcrun[[:space:]]+(altool|notarytool)|transporter|gradlew?[^&|;]*(bundleRelease|assembleRelease)|bundletool|xcodebuild[^&|;]*archive|flutter[[:space:]]+build[[:space:]]+(ipa|appbundle|apk|ios)|(npx[[:space:]]+)?(expo[[:space:]]+(prebuild|run:ios|run:android)|cap[[:space:]]+(sync|build|run|copy|open)|react-native[[:space:]]+run-(ios|android))|ionic[[:space:]]+capacitor[[:space:]]+(build|run)|cordova[[:space:]]+build'; then
    exit 0
  fi
  DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
fi

# See docs/CROSS-PLATFORM-FRAMEWORKS.md: an Android-only command beats a committed ios/
# folder for the Apple-only checks below (standalone mode has no CMD, unaffected).
CMD_TARGET_ANDROID_ONLY=0
if [ -n "$CMD" ] \
  && printf '%s' "$CMD" | grep -qiE 'build[[:space:]]+(apk|appbundle)\b|assembleRelease|bundleRelease|run-android|run:android|--platform[[:space:]]+android\b|capacitor[[:space:]]+android\b' \
  && ! printf '%s' "$CMD" | grep -qiE '\bios\b|\bipa\b|xcodebuild|altool|notarytool'; then
  CMD_TARGET_ANDROID_ONLY=1
fi

[ -z "$DIR" ] && DIR="$PWD"
[ -d "$DIR" ] || { log_err "project dir not found. $DIR"; exit 0; }

# ----- build a source file list, excluding vendor dirs -----
FILELIST="$(mktemp 2>/dev/null || echo /tmp/ascg.$$)"
find "$DIR" -type f \( \
  -name '*.swift' -o -name '*.m' -o -name '*.h' -o -name '*.kt' -o -name '*.java' \
  -o -name '*.xml' -o -name '*.plist' -o -name '*.gradle' -o -name '*.kts' \
  -o -name '*.json' -o -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \
  -o -name '*.dart' -o -name '*.xcconfig' -o -name '*.yaml' -o -name '*.yml' \
  -o -name '*.pbxproj' -o -name '*.entitlements' -o -name '*.html' \
  \) 2>/dev/null \
  | grep -vE '/(node_modules|Pods|\.git|build|DerivedData|vendor|\.dart_tool|Carthage|[A-Za-z0-9_]*Tests|androidTest|__tests__)/' \
  > "$FILELIST"

grep_has() {  # 0 if regex found in any source file
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

# True only if a STRING LITERAL containing the regex appears in RELEASE-reachable source. For
# Swift, `#if DEBUG` / `#if !RELEASE` debug-only regions are stripped first, so a URL only a debug
# build compiles is not flagged. The string-literal requirement (the match must sit inside "...")
# skips comments and identifiers. This is what makes the backend check precise instead of matching
# a localhost mentioned in a comment or guarded behind DEBUG. Without it the check cries wolf.
release_string_has() {
  [ -s "$FILELIST" ] || return 1
  local f
  while IFS= read -r f; do
    case "$f" in
      *.swift)
        awk '
          /^[ \t]*#if/    { d++; if ($0 ~ /#if[ \t]+DEBUG/ || $0 ~ /#if[ \t]+!RELEASE/) { dbg=d; skip=1 } next }
          /^[ \t]*#else/  { if (skip && d==dbg) skip=0; next }
          /^[ \t]*#elseif/ { next }
          /^[ \t]*#endif/ { if (skip && d==dbg) { skip=0; dbg=0 } d--; next }
          !skip { print }
        ' "$f" 2>/dev/null ;;
      *) cat "$f" 2>/dev/null ;;
    esac
  done < "$FILELIST" \
    | LC_ALL=C grep -E "\"[^\"]*($1)[^\"]*\"" >/dev/null 2>&1
  # NOTE. no `grep -q`. With `set -o pipefail`, `grep -q` exits on the first match and
  # closes the pipe, so the still-writing awk/cat producer gets SIGPIPE (141) and pipefail
  # then reports the whole pipeline non-zero even though grep matched. That made this check
  # silently miss on the CI runner (GNU grep, timing-dependent) while passing on a fast local
  # machine. Draining all input with plain grep and returning its status is deterministic.
}

finding() {  # severity id title fix
  case "$1" in
    critical) CRIT=$((CRIT+1)); printf '  [CRITICAL] %s  %s\n' "$2" "$3" ;;
    high)     HIGH=$((HIGH+1)); printf '  [HIGH]     %s  %s\n' "$2" "$3" ;;
    *)        MED=$((MED+1));   printf '  [MEDIUM]   %s  %s\n' "$2" "$3" ;;
  esac
  printf '      fix. %s\n' "$4"
}

# ----- platform detection -----
IS_IOS=0; IS_AND=0; IS_WEB=0
find "$DIR" -maxdepth 4 \( -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'Package.swift' -o -name 'Podfile' \) 2>/dev/null | grep -q . && IS_IOS=1
find "$DIR" -maxdepth 4 -name 'Info.plist' 2>/dev/null | grep -q . && IS_IOS=1
find "$DIR" -maxdepth 5 \( -name 'AndroidManifest.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' \) 2>/dev/null | grep -q . && IS_AND=1
find "$DIR" -maxdepth 4 \( -name 'package.json' -o -name 'index.html' -o -name 'webpack.config.js' -o -name 'next.config.js' \) 2>/dev/null | grep -q . && IS_WEB=1

# ----- cross-platform framework detection -----
# IS_IOS/IS_AND above still fire on the built artifact. This adds framework-specific checks.
IS_FLUTTER=0; IS_RN=0; IS_IONIC=0
find "$DIR" -maxdepth 4 -name 'pubspec.yaml' 2>/dev/null | grep -q . && IS_FLUTTER=1
# Scan EVERY package.json within depth (not just the first), so a monorepo root's tooling
# package.json never shadows a real apps/mobile/package.json deeper in the tree.
while IFS= read -r pkg; do
  grep -qE '"react-native"|"expo"' "$pkg" 2>/dev/null && IS_RN=1
  grep -qE '"@capacitor/core"|"@capacitor/ios"|"@capacitor/android"|"@ionic/(angular|react|vue)"|"cordova-android"|"cordova-ios"' "$pkg" 2>/dev/null && IS_IONIC=1
done < <(find "$DIR" -maxdepth 4 -name 'package.json' 2>/dev/null | grep -vE '/(node_modules|ios/Pods)/')
find "$DIR" -maxdepth 4 -name 'capacitor.config.*' 2>/dev/null | grep -q . && IS_IONIC=1
# config.xml alone is ambiguous (Maven/NuGet/tooling also use that filename), so require the
# Cordova widget marker before it counts as a signal.
while IFS= read -r cfg; do
  grep -qE '<widget|xmlns:cdv' "$cfg" 2>/dev/null && IS_IONIC=1
done < <(find "$DIR" -maxdepth 4 -name 'config.xml' 2>/dev/null)

# The actual gate the framework checks below use: a committed ios/ folder AND the
# invoking command (when known) does not explicitly target Android-only.
IOS_TARGET_ACTIVE=0
[ "$IS_IOS" -eq 1 ] && [ "$CMD_TARGET_ANDROID_ONLY" -eq 0 ] && IOS_TARGET_ACTIVE=1

echo "== App Store Compliance Guard =="
echo "Project. $DIR"
echo "Platforms. iOS=$IS_IOS Android=$IS_AND Web=$IS_WEB"
echo "Frameworks. Flutter=$IS_FLUTTER ReactNative/Expo=$IS_RN Ionic/Capacitor/Cordova=$IS_IONIC"
[ "$CMD_TARGET_ANDROID_ONLY" -eq 1 ] && echo "Command targets Android only. Apple-only framework checks suppressed for this run."
echo ""

# ----- run regulatory deadlines check -----
# Tries both ship shapes. nested repo (agent-os/hooks/) and flat ~/.claude.
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEADLINE_PY=""
for candidate in \
  "$HOOK_DIR/../../scripts/deadline-checker.py" \
  "$HOOK_DIR/../skills/app-store-compliance/scripts/deadline-checker.py"; do
  if [ -f "$candidate" ]; then DEADLINE_PY="$candidate"; break; fi
done
if [ -n "$DEADLINE_PY" ]; then
  python3 "$DEADLINE_PY"
  echo ""
fi

# ===== shared checks =====
# Genuine placeholder CONTENT only. the bare word "placeholder" matches every SwiftUI
# `placeholder:` parameter and a "TODO"/"FIXME" matches normal dev comments, neither of which is a
# rejection cause, so match real placeholder markers a reviewer would actually see.
if grep_has 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'; then
  finding high "BOTH-PLACEHOLDER" "Placeholder content (lorem ipsum, example.com, dummy text) found in sources" "Replace placeholder text and assets with real content."
fi
# ROSCA and CA/NY/MA negative-option laws bind regardless of the vacated federal rule.
if grep_has 'subscri(be|ption)|auto.renew|membership' && grep_has '[Cc]all.{0,25}[Cc]ancel|[Cc]ancel.{0,25}[Cc]all|[Mm]ail.{0,25}[Cc]ancel|[Ww]rite.{0,25}[Cc]ancel|[Cc]ancel.{0,15}(in.person|by.phone|by.mail)'; then
  finding high "BOTH-SUBSCRIPTION-HARD-CANCEL" "Subscription cancellation appears to require a phone call, mail, or an in-person visit" "Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws)."
fi
# fastlane precheck derived metadata checks
if grep_has 'coming soon|coming-soon|will be available|in a future update|stay tuned'; then
  finding medium "APPLE-2.3-FUTURE-FUNCTIONALITY" "Future functionality language found (coming soon, beta)" "Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1)."
fi
if grep_has 'iOS bug|apple bug|broken on iOS'; then
  finding medium "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT" "Negative Apple or iOS bug reference in copy" "Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment)."
fi
if grep_has 'loot ?box|gacha|mystery box|random reward'; then
  finding high "BOTH-LOOTBOX-ODDS" "Random reward mechanic present" "Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling)."
fi

# ===== Flutter checks =====
# iOS-only Apple requirement, gated on IS_IOS so an Android-only build is never blocked for it.
if [ "$IS_FLUTTER" -eq 1 ]; then
  if [ "$IOS_TARGET_ACTIVE" -eq 1 ] && grep_has 'permission_handler|image_picker|geolocator|device_info_plus|package_info_plus|shared_preferences|sqflite|firebase_'; then
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep -q .; then
      finding critical "FLUTTER-PRIVACY-MANIFEST-MISSING" "Flutter plugins that touch required-reason APIs but no PrivacyInfo.xcprivacy anywhere in the project" "Add an app-level PrivacyInfo.xcprivacy AND confirm each Flutter plugin ships its own (permission_handler, image_picker, and most first-party plugins added theirs from Flutter 3.19+). A missing plugin-level manifest is invisible to Apple's aggregator unless the app manifest also declares that plugin's reason codes. This check only runs against an iOS target."
    fi
  fi
  if [ "$IS_IOS" -eq 0 ]; then
    finding medium "FLUTTER-NO-IOS-RUNNER-FOUND" "No ios/Runner target detected next to pubspec.yaml" "If this is an iOS submission, run flutter create . or confirm the ios/ platform folder exists. A pure Android build never needs one."
  fi
fi

# ===== React Native / Expo checks =====
# Both findings are Apple-specific (3.3.2/2.5.2 disclosure, iOS privacy manifest), IS_IOS-gated.
if [ "$IS_RN" -eq 1 ] && [ "$IOS_TARGET_ACTIVE" -eq 1 ]; then
  if grep_has 'react-native-code-push|CodePush\.|expo-updates|Updates\.checkForUpdate|react-native-ota-hot-update|@stallion-js|Stallion\.'; then
    if ! grep_has 'reviewNotes|App Review|bug.fix.only|bugfix.only'; then
      finding high "RN-OTA-UNDECLARED" "An over-the-air JS bundle updater (CodePush, Expo Updates, or similar) is present" "Disclose the OTA mechanism by name in App Review notes, restrict its use to bug fixes that do not change the app's purpose, UI, or add features beyond what was reviewed (Apple 3.3.2, 2.5.2)."
    fi
  fi
  if grep_has 'Firebase|@react-native-firebase|expo-file-system|expo-application|AsyncStorage|@react-native-async-storage'; then
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep -q .; then
      finding critical "RN-PRIVACY-MANIFEST-MISSING" "React Native native modules that touch required-reason APIs but no PrivacyInfo.xcprivacy anywhere" "Add an app-level PrivacyInfo.xcprivacy. Native modules bundled transitively via JS deps (analytics, storage, device-info libraries) each need their own manifest aggregated in the final IPA; this is easy to miss because the dependency is JS-side."
    fi
  fi
fi

# ===== Ionic / Capacitor / Cordova checks =====
# All three are Apple-side (4.2, UIWebView, iOS privacy manifest), IS_IOS-gated as above.
if [ "$IS_IONIC" -eq 1 ] && [ "$IOS_TARGET_ACTIVE" -eq 1 ]; then
  WRAPPER_COUNT="$( [ -s "$FILELIST" ] && tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e 'WKWebView|loadRequest|Capacitor|Cordova' 2>/dev/null | wc -l | tr -d '[:space:]' || echo 0)"
  NATIVE_PLUGIN_COUNT="$( [ -s "$FILELIST" ] && tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIho -e '@capacitor/(push-notifications|status-bar|splash-screen|haptics|share|camera|local-notifications)|cordova-plugin-(statusbar|splashscreen|push)' 2>/dev/null | sort -u | wc -l | tr -d '[:space:]' || echo 0)"
  if [ "${WRAPPER_COUNT:-0}" -gt 0 ] && [ "${NATIVE_PLUGIN_COUNT:-0}" -lt 2 ]; then
    finding high "IONIC-4.2-THIN-WRAPPER" "WebView/Capacitor/Cordova present with fewer than 2 recognized native-feel plugins (status bar, splash screen, push, haptics)" "This is a heuristic proxy, not the actual Apple 4.2 test (features/content/UI beyond a repackaged website); review manually before treating it as a hard blocker. Add native Capacitor/Cordova plugins for status bar, splash transition, push, and haptics, or ship as an installable PWA to skip App Review entirely."
  fi
  if grep_has 'UIWebView'; then
    finding critical "IONIC-UIWEBVIEW-DEPRECATED" "Deprecated UIWebView symbol referenced (directly or via a stale plugin)" "Apple auto-rejects (ITMS-90809) any binary statically linking UIWebView. Update every Capacitor/Cordova plugin to a version using WKWebView; a stale plugin can pull this in even when app code never references it."
  fi
  if grep_has '@capacitor/|Capacitor\.'; then
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep -q .; then
      finding high "IONIC-PRIVACY-MANIFEST-MISSING" "Capacitor/Cordova plugins present but no PrivacyInfo.xcprivacy" "Capacitor plugin manifest support is less standardized than Flutter's; verify each plugin wrapping a native SDK (camera, geolocation, ads) ships PrivacyInfo.xcprivacy, and add the app-level one."
    fi
  fi
fi

# ===== iOS checks =====
if [ "$IS_IOS" -eq 1 ]; then
  if release_string_has 'localhost|127\.0\.0\.1|staging\.[a-z]|ngrok\.io'; then
    finding critical "APPLE-2.1-STAGING-BACKEND" "A release-build string points at localhost or a staging host" "Point the release build at the live production backend. A localhost/staging URL inside #if DEBUG or a comment is fine. this only flags strings the release build actually compiles."
  fi
  if grep_has 'signIn|logIn|LoginView|OAuth|FirebaseAuth|createAccount|signUp'; then
    if ! grep_has 'deleteAccount|delete_account|account deletion|deleteUser'; then
      finding critical "APPLE-5.1.1-NO-ACCOUNT-DELETION" "Account creation found but no in app account deletion" "Add an in app account deletion flow (Apple 5.1.1(v))."
    fi
  fi
  if grep_has 'AVCaptureDevice|UIImagePickerController'; then
    grep_has 'NSCameraUsageDescription' || finding critical "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Camera used without NSCameraUsageDescription" "Add NSCameraUsageDescription with a specific reason."
  fi
  if grep_has 'CLLocationManager'; then
    grep_has 'NSLocation.*UsageDescription' || finding critical "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Location used without a location usage description" "Add the matching NSLocation usage description with a specific reason."
  fi
  if grep_has 'PHPhotoLibrary|PHPicker'; then
    grep_has 'NSPhotoLibrary.*UsageDescription' || finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Photos used without a photo library usage description" "Add NSPhotoLibraryUsageDescription with a specific reason."
  fi
  if grep_has 'CNContactStore'; then
    grep_has 'NSContactsUsageDescription' || finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Contacts used without NSContactsUsageDescription" "Add NSContactsUsageDescription with a specific reason."
  fi
  if grep_has 'FacebookLogin|GoogleSignIn|GIDSignIn|LoginWithFacebook'; then
    grep_has 'SignInWithApple|ASAuthorizationAppleIDProvider' || finding high "APPLE-4.8-SOCIAL-LOGIN-ONLY" "Third party social login without Sign in with Apple" "Add Sign in with Apple or an equal privacy preserving login (Apple 4.8)."
  fi
  # Match the tracking SDKs by their own type names / imports, never the bare words "Adjust" or
  # "Branch", which collide with ordinary English ("Adjust times", a git branch) and false-flag a
  # tracking SDK that is not present.
  if grep_has 'AppsFlyerLib|import AppsFlyer|AdjustConfig|AdjustEvent|import Adjust[^A-Za-z]|BranchEvent|BranchUniversalObject|import Branch[^A-Za-z]|FBSDKCoreKit|FBSDKLogin|ASIdentifierManager|advertisingIdentifier'; then
    grep_has 'ATTrackingManager|NSUserTrackingUsageDescription' || finding high "APPLE-5.1.2-MISSING-ATT" "Tracking SDK without App Tracking Transparency" "Call the ATT prompt and add NSUserTrackingUsageDescription (Apple 5.1.2)."
  fi
  if grep_has 'Stripe|PayPalCheckout|braintree|razorpay'; then
    grep_has 'StoreKit|SKProduct|Product\.purchase' || finding critical "APPLE-3.1.1-EXTERNAL-PAYMENT" "External payment SDK without StoreKit" "Route digital goods through in app purchase unless the app is a documented exempt category (Apple 3.1.1)."
  fi
  if grep_has 'api\.openai\.com|anthropic|generativelanguage|chat/completions'; then
    finding medium "APPLE-5.1.2-AI-NO-CONSENT-MODAL" "Third party AI integration detected" "If personal data is sent, show a consent modal naming the AI provider and data types (Apple 5.1.2)."
  fi
  if ! grep_has 'privacyPolicy|privacy-policy|PrivacyPolicy'; then
    finding high "APPLE-5.1.1-MISSING-PRIVACY-POLICY" "No privacy policy reference found in sources" "Publish a privacy policy, link it in App Store Connect, and reach it from inside the app."
  fi
  if grep_has 'UserDefaults\.standard'; then
    if grep_has 'token|password|credential|secret|jwt' && ! grep_has 'Keychain|SecItemAdd|SecItemUpdate'; then
      finding high "BOTH-SECURE-STORAGE" "Plain UserDefaults storage is used for sensitive credentials" "Store access tokens and sensitive credentials in iOS Keychain instead."
    fi
  fi
  if grep_has 'CFBundleURLSchemes'; then
    if ! grep_has 'apple-app-site-association'; then
      finding high "BOTH-UNSAFE-DEEPLINK" "Custom URL deep link schemes declared without Universal Links configuration" "Configure Universal Links (iOS) using apple-app-site-association verification to prevent URL hijacking."
    fi
  fi
  # Privacy manifest, the top modern Apple upload rejection since 2024
  if grep_has 'Firebase|Alamofire|UserDefaults|systemUptime|FileManager\.default|ProcessInfo'; then
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep -q .; then
      finding critical "APPLE-PRIVACY-MANIFEST-MISSING" "Required reason APIs or SDKs present but no PrivacyInfo.xcprivacy" "Add a privacy manifest with approved reason codes and tracking domains, and confirm each SDK ships its signed manifest."
    fi
  fi
  grep_has 'ITSAppUsesNonExemptEncryption' || finding high "APPLE-EXPORT-COMPLIANCE-MISSING" "ITSAppUsesNonExemptEncryption not set" "Set it in Info.plist or the build stalls in Missing Compliance and never reaches review."
  if grep_has 'SKProduct|Product\.purchase|StoreKit'; then
    grep_has 'restorePurchases|restoreCompletedTransactions|AppStore\.sync|Restore Purchases' || finding high "APPLE-RESTORE-PURCHASES-MISSING" "StoreKit purchases without a Restore Purchases control" "Add a visible Restore Purchases control. Required for non consumables."
  fi
  if grep_has 'deleteAccount|delete account'; then
    grep_has 'mailto:|deactivate' && finding high "APPLE-ACCOUNT-DELETION-WEAK" "Account removal may be deactivate or mailto only" "Provide genuine in app deletion of the account and its data, not a deactivate or external form."
  fi
  if grep_has 'fixed-odds|betting'; then
    finding critical "APPLE-GAMBLING-BRAZIL-LICENSE" "Fixed-odds or betting keyword detected in sources" "Provide a valid fixed-odds betting license from the Secretariat of Prizes and Bets (SPA) in App Review Info, set age rating to A18, and submit a new version to trigger verification (Apple policy May 8, 2026)."
  fi
  if grep_has 'Image\('; then
    if ! grep_has 'accessibilityLabel|accessibilityIdentifier|accessibilityHidden|accessibilityElement'; then
      finding medium "APPLE-ACCESSIBILITY-VOICEOVER" "SwiftUI Image or UIKit component without VoiceOver accessibility attribute" "Provide an accessibilityLabel or use decorative initializers (Apple Design - Accessibility)."
    fi
  fi
  if grep_has '\.system\(size:'; then
    finding medium "APPLE-ACCESSIBILITY-DYNAMICTYPE" "Hardcoded system font size detected" "Use relative SwiftUI font styles or preferredFont APIs to support Dynamic Type (Apple Design - Accessibility)."
  fi
  if grep_has 'withAnimation|UIView\.animate'; then
    if ! grep_has 'isReduceMotionEnabled|accessibilityReduceMotion'; then
      finding medium "APPLE-ACCESSIBILITY-REDUCEMOTION" "Animations implemented without checking Reduce Motion" "Respect the Reduce Motion accessibility setting before executing complex custom animations (Apple Design - Accessibility)."
    fi
  fi
  if grep_has 'UIColor\(\s*red:'; then
    if ! grep_has 'isDarkerSystemColorsEnabled|darkerSystemColors'; then
      finding medium "APPLE-ACCESSIBILITY-COLORCONTRAST" "Raw RGB UIColor without system dynamic color or high contrast checks" "Utilize dynamic named asset colors or check isDarkerSystemColorsEnabled (Apple Design - Accessibility)."
    fi
  fi
  if grep_has 'onTapGesture|Button'; then
    if ! grep_has 'FeedbackGenerator|CoreHaptics'; then
      finding medium "APPLE-ACCESSIBILITY-HAPTICS" "Taps or button interactions without tactile feedback" "Integrate haptic feedback generators to improve interaction accessibility (Apple Design - Accessibility)."
    fi
  fi
  if grep_has 'focusable'; then
    if ! grep_has 'FocusState|focused'; then
      finding medium "APPLE-ACCESSIBILITY-KEYBOARD" "Focusable controls declared without focus state tracking" "Support physical keyboards with FocusState tracking (Apple Design - Accessibility)."
    fi
  fi
  finding medium "APPLE-2.3-AGE-RATING-2026" "Verify the 2026 age rating questionnaire" "Answer the updated age rating questions (13 plus, 16 plus, 18 plus) in App Store Connect."
  if grep_has 'email|phoneNumber|userName|location|coordinates'; then
    if ! grep_has 'NSPrivacyCollectedDataTypes|privacyNutritionLabels|privacy-nutrition-labels'; then
      finding high "APPLE-PRIVACY-NUTRITION-LABELS" "Missing Privacy Nutrition Labels data type declarations" "Update the app privacy manifest (PrivacyInfo.xcprivacy) with NSPrivacyCollectedDataTypes and complete corresponding Nutrition Labels in App Store Connect."
    fi
  fi
fi

# ===== Android checks =====
if [ "$IS_AND" -eq 1 ]; then
  if grep_has 'ACCESS_BACKGROUND_LOCATION'; then
    finding critical "GOOGLE-PERM-BACKGROUND-LOCATION" "Background location permission declared" "Justify with a core feature and prominent disclosure, or use foreground location."
  fi
  if grep_has 'MANAGE_EXTERNAL_STORAGE'; then
    finding critical "GOOGLE-PERM-ALL-FILES" "All files access declared" "Use scoped storage. Request all files access only for a qualifying use case."
  fi
  if grep_has 'android\.permission\.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)'; then
    finding critical "GOOGLE-PERM-SMS-CALLLOG" "SMS or Call Log permission declared" "Use the permissions declaration for an approved core use case, or drop it."
  fi
  if grep_has 'BIND_ACCESSIBILITY_SERVICE|AccessibilityService'; then
    finding critical "GOOGLE-PERM-ACCESSIBILITY-MISUSE" "AccessibilityService present" "Use it only for genuine accessibility and declare the use, or remove it."
  fi
  if grep_has 'Stripe|PayPal|braintree|razorpay'; then
    grep_has 'BillingClient|com\.android\.billingclient' || finding critical "GOOGLE-PLAY-BILLING" "External payment without Play Billing" "Use Play Billing for in app digital goods."
  fi
  if grep_has 'firebase-analytics|com\.google\.android\.gms\.ads|appsflyer|com\.adjust|com\.facebook'; then
    finding high "GOOGLE-DATASAFETY-MISMATCH" "Analytics or ad SDK present. Verify the Data Safety form" "Declare every collection and sharing accurately. Data Safety mismatch is the top Google rejection."
  fi
  if ! grep_has 'privacyPolicy|privacy-policy'; then
    finding high "GOOGLE-MISSING-PRIVACY-POLICY" "No privacy policy reference found" "Publish a privacy policy and set its URL in the Play Console store listing."
  fi
  TSDK="$(grep -hoE 'targetSdk(Version)?[[:space:]=]+[0-9]+' "$DIR"/**/build.gradle* 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)"
  if [ -n "$TSDK" ] && [ "$TSDK" -lt 34 ]; then
    finding high "GOOGLE-TARGET-API" "targetSdk is $TSDK, below the current Play requirement" "Build against the current required Android target API level and verify the current minimum."
  fi
  if grep_has 'DexClassLoader|PathClassLoader|loadDex'; then
    finding high "ANDROID-DYNAMIC-CODE-LOADING" "Dynamic code loading at runtime" "Ship all code in the package. Server changes are data, not executable code."
  fi
  if grep_has 'getSharedPreferences'; then
    if grep_has 'token|password|credential|secret|jwt' && ! grep_has 'EncryptedSharedPreferences|KeyStore|SQLCipher'; then
      finding high "BOTH-SECURE-STORAGE" "Plain SharedPreferences storage is used for sensitive credentials" "Store access tokens and sensitive credentials in Android EncryptedSharedPreferences / Keystore instead."
    fi
  fi
  if grep_has 'allowBackup="true"'; then
    if ! grep_has 'dataExtractionRules|fullBackupContent|allowBackup="false"'; then
      finding high "ANDROID-INSECURE-BACKUP" "Android allowBackup is enabled without strict filters" "Disable backups using android:allowBackup=\"false\", or restrict backup folders using dataExtractionRules."
    fi
  fi
  if grep_has 'android:scheme'; then
    if ! grep_has 'assetlinks.json'; then
      finding high "BOTH-UNSAFE-DEEPLINK" "Custom URL deep link schemes declared without App Links configuration" "Configure App Links (Android) using assetlinks.json verification to prevent URL hijacking."
    fi
  fi
  if grep_has 'QUERY_ALL_PACKAGES'; then
    finding high "ANDROID-QUERY-ALL-PACKAGES" "QUERY_ALL_PACKAGES without a permitted use case" "Declare specific packages with a queries element, or qualify for a permitted use case."
  fi
  if grep_has 'SYSTEM_ALERT_WINDOW|TYPE_APPLICATION_OVERLAY'; then
    finding high "ANDROID-OVERLAY-TAPJACKING" "System overlay permission present" "Remove overlay abuse. The overlay plus accessibility combination is a strong malware signal."
  fi
  if grep_has 'com\.google\.android\.play:age-signals|AgeSignalsManager|AgeSignalsRequest'; then
    finding critical "GOOGLE-PLAY-AGE-SIGNALS-MISUSE" "Play Age Signals API dependency found" "Ensure age signals are ONLY used to provide age-appropriate experiences. Using them for advertising, marketing, user profiling, or analytics is a direct ToS violation that can result in immediate app suspension or takedown."
  fi
  if grep_has '<ImageView|<ImageButton'; then
    if ! grep_has 'contentDescription'; then
      finding medium "ANDROID-ACCESSIBILITY-TALKBACK" "XML ImageView or ImageButton missing contentDescription" "Add an android:contentDescription attribute (Google User Experience - Accessibility)."
    fi
  fi
  if grep_has 'android:textSize=.*dp'; then
    finding medium "ANDROID-ACCESSIBILITY-FONTSCALING" "Text size defined in dp instead of sp" "Always define text size in sp to allow system font scaling to work correctly (Google User Experience - Accessibility)."
  fi
  if grep_has 'android:(textColor|background)=.*#'; then
    finding medium "ANDROID-ACCESSIBILITY-HIGHCONTRAST" "Hardcoded hex colors ignoring high contrast settings" "Use semantic theme references or color resources instead of hardcoded hex values (Google User Experience - Accessibility)."
  fi
  if grep_has 'android:(layout_width|layout_height|minWidth|minHeight)=.*dp'; then
    if grep_has 'clickable|onClick'; then
      finding medium "ANDROID-ACCESSIBILITY-SCANNER" "Interactive controls with hardcoded dimensions" "Verify touch target sizes are at least 48dp (Google User Experience - Accessibility)."
    fi
  fi
  finding medium "GOOGLE-12-TESTER-RULE" "Verify the closed testing requirement" "A new personal account needs 12 testers over 14 consecutive days before production."
  if grep_has 'contacts|SMS|device accounts|files|personalData'; then
    if ! grep_has 'prominent disclosure|user consent|privacy consent|accept policy'; then
      finding critical "ANDROID-USER-DATA-DISCLOSURE" "Missing prominent disclosure for sensitive user data" "Provide a prominent in-app disclosure before collecting sensitive personal data, and obtain explicit user consent."
    fi
  fi
  if grep_has 'com\.google\.android\.gms\.permission\.AD_ID|AD_ID|getAdvertisingIdInfo'; then
    if ! grep_has 'opt-out|reset AD_ID|advertisingIdConsent|delete AD_ID'; then
      finding high "ANDROID-ADVERTISING-ID" "Google Play Advertising ID usage without disclosure or opt-out" "Declare the AD_ID permission in AndroidManifest.xml and handle user opt-out or deletion requests in full compliance with Google Play policy."
    fi
  fi
  if grep_has 'requestPermissions|checkSelfPermission|shouldShowRequestPermissionRationale'; then
    if ! grep_has 'permission explanation|showPermissionRationale|explainPermission'; then
      finding high "ANDROID-RUNTIME-PERMISSIONS" "Sensitive runtime permissions requested without validation" "Check permissions dynamically at runtime, show a clear rationale if denied, and handle denials gracefully."
    fi
  fi
  if grep_has 'HealthConnectClient|com\.google\.android\.gms\.permission\.HealthConnect|READ_STEPS|READ_HEART_RATE'; then
    if ! grep_has 'healthConnectConsent|healthPrivacyPolicy|Health Connect'; then
      finding critical "ANDROID-HEALTH-PERMISSIONS" "Health or fitness data access without Health Connect declaration" "Declare Health Connect permissions, complete the console Health Connect form, and maintain a dedicated health privacy policy."
    fi
  fi
fi

# ===== Web checks =====
if [ "$IS_WEB" -eq 1 ]; then
  if grep_has 'processData|personalData|submitForm|registerWeb|webForm'; then
    if ! grep_has 'GDPR|opt-in|privacyConsent|deletePersonalData|exportData'; then
      finding critical "WEB-GDPR-COMPLIANCE" "Processing web personal data without GDPR compliance controls" "Integrate standard GDPR compliance gates including explicit opt-in for data processing and a mechanism for data deletion."
    fi
  fi
  if grep_has 'document\.cookie|setCookie|cookieStore|js-cookie|cookieConsent'; then
    if ! grep_has 'cookieBanner|cookieConsentBanner|acceptCookies|cookiePreferences'; then
      finding critical "WEB-COOKIE-CONSENT" "Setting non-essential cookies without prior cookie consent" "Implement a compliant Cookie Consent banner that blocks non-essential cookies until the user gives explicit consent."
    fi
  fi
  if grep_has 'localStorage\.setItem|localStorage'; then
    if ! grep_has 'encryptedStorage|encryptToken|consentLocalStorage|clearLocalStorage'; then
      finding high "WEB-LOCAL-STORAGE" "Unencrypted sensitive personal data stored in localStorage" "Avoid storing plain sensitive personal info in localStorage, encrypt any stored tokens, and respect storage preferences."
    fi
  fi
  if grep_has 'sessionStorage\.setItem|sessionStorage'; then
    if ! grep_has 'encryptedSession|clearSessionStorage'; then
      finding high "WEB-SESSION-STORAGE" "Sensitive session details stored in sessionStorage without protection" "Limit and secure the data written to sessionStorage, apply encryption, and ensure data is deleted at session end."
    fi
  fi
  if grep_has 'indexedDB\.open|indexedDB|createObjectStore'; then
    if ! grep_has 'encryptDatabase|deleteDatabase|consentIndexedDB'; then
      finding high "WEB-INDEXEDDB" "Structured personal data stored in IndexedDB without security controls" "Use encrypted IndexedDB wrappers for structured sensitive records, check user consent, and clear databases upon logout."
    fi
  fi
  if grep_has 'gtag|fbq|google-analytics|trackingPixel|analytics\.js|hotjar'; then
    if ! grep_has 'consentTracking|disableTracking|optOutTracking|trackingPreferences'; then
      finding high "WEB-TRACKING-TECHNOLOGIES" "Third-party tracking technologies loaded without consent" "Load third-party tracking scripts and pixels conditionally only after receiving explicit user cookie consent."
    fi
  fi
fi

# ===== summary and exit =====
echo ""
echo "Summary. critical=$CRIT high=$HIGH medium=$MED"
echo "Reference. docs/ in the app-store-compliance repo, and data/rejection-patterns.json"

if [ "$CRIT" -gt 0 ]; then
  if [ "${APP_STORE_GUARD_OK:-0}" = "1" ]; then
    echo "APP_STORE_GUARD_OK set. Critical findings present but the submission is allowed."
    log_err "override used with $CRIT critical findings"
    exit 0
  fi
  echo ""
  echo "BLOCKED. $CRIT critical rejection risk(s) above. Fix them, or set APP_STORE_GUARD_OK=1 to override."
  exit 2
fi
exit 0
