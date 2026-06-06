#!/usr/bin/env bash
# App Store Compliance Guard
# Scans a mobile app project for the rejection patterns that cause most App Store
# and Google Play rejections, before a build is uploaded.
#
# Two modes.
#   1. Standalone.  app-store-compliance-guard.sh /path/to/project
#   2. agent-os PreToolUse hook on Bash. Fires only when the command looks like an
#      app submission (fastlane, eas submit, xcrun altool, gradle bundleRelease,
#      bundletool, xcodebuild archive). Blocks on a critical finding.
#
# Exit codes. 0 clean or advisory, 2 critical finding (blocks the submission).
# Override the block with APP_STORE_GUARD_OK=1.
#
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
if [ "$#" -ge 1 ] && [ -d "$1" ]; then
  DIR="$1"                                   # standalone with explicit path
elif [ ! -t 0 ]; then
  STDIN_JSON="$(cat 2>/dev/null || true)"    # hook mode, payload on stdin
fi

if [ -n "$STDIN_JSON" ]; then
  CMD="$(printf '%s' "$STDIN_JSON" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"//; s/"$//')"
  # Only act on submission style commands. Otherwise stay silent.
  if ! printf '%s' "$CMD" | grep -qiE 'fastlane[[:space:]]+(deliver|pilot|supply|submit)|eas[[:space:]]+submit|xcrun[[:space:]]+(altool|notarytool)|transporter|gradlew?[^&|;]*(bundleRelease|assembleRelease)|bundletool|xcodebuild[^&|;]*archive'; then
    exit 0
  fi
  DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
fi

[ -z "$DIR" ] && DIR="$PWD"
[ -d "$DIR" ] || { log_err "project dir not found. $DIR"; exit 0; }

# ----- build a source file list, excluding vendor dirs -----
FILELIST="$(mktemp 2>/dev/null || echo /tmp/ascg.$$)"
find "$DIR" -type f \( \
  -name '*.swift' -o -name '*.m' -o -name '*.h' -o -name '*.kt' -o -name '*.java' \
  -o -name '*.xml' -o -name '*.plist' -o -name '*.gradle' -o -name '*.kts' \
  -o -name '*.json' -o -name '*.js' -o -name '*.ts' -o -name '*.dart' -o -name '*.xcconfig' \
  \) 2>/dev/null \
  | grep -vE '/(node_modules|Pods|\.git|build|DerivedData|vendor|\.dart_tool|Carthage)/' \
  > "$FILELIST"

grep_has() {  # 0 if regex found in any source file
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
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
IS_IOS=0; IS_AND=0
find "$DIR" -maxdepth 4 \( -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'Package.swift' -o -name 'Podfile' \) 2>/dev/null | grep -q . && IS_IOS=1
find "$DIR" -maxdepth 4 -name 'Info.plist' 2>/dev/null | grep -q . && IS_IOS=1
find "$DIR" -maxdepth 5 \( -name 'AndroidManifest.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' \) 2>/dev/null | grep -q . && IS_AND=1

echo "== App Store Compliance Guard =="
echo "Project. $DIR"
echo "Platforms. iOS=$IS_IOS Android=$IS_AND"
echo ""

# ===== shared checks =====
if grep_has 'lorem ipsum|[^a-z]TODO[^a-z]|FIXME|placeholder|example\.com'; then
  finding high "BOTH-PLACEHOLDER" "Placeholder content or example.com found in sources" "Replace all placeholder text and assets with real content."
fi
if grep_has 'loot ?box|gacha|mystery box|random reward'; then
  finding high "BOTH-LOOTBOX-ODDS" "Random reward mechanic present" "Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling)."
fi

# ===== iOS checks =====
if [ "$IS_IOS" -eq 1 ]; then
  if grep_has 'localhost|127\.0\.0\.1|staging\.|//dev\.|ngrok'; then
    finding critical "APPLE-2.1-STAGING-BACKEND" "Release sources reference localhost or staging" "Point the release build at the live production backend and keep it up during review."
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
  if grep_has 'AppsFlyer|Adjust|Branch|FBSDK|ASIdentifierManager|advertisingIdentifier'; then
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
  finding medium "APPLE-2.3-AGE-RATING-2026" "Verify the 2026 age rating questionnaire" "Answer the updated age rating questions (13 plus, 16 plus, 18 plus) in App Store Connect."
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
  if grep_has 'firebase-analytics|com\.google\.android\.gms\.ads|appsflyer|adjust|com\.facebook'; then
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
  if grep_has 'QUERY_ALL_PACKAGES'; then
    finding high "ANDROID-QUERY-ALL-PACKAGES" "QUERY_ALL_PACKAGES without a permitted use case" "Declare specific packages with a queries element, or qualify for a permitted use case."
  fi
  if grep_has 'SYSTEM_ALERT_WINDOW|TYPE_APPLICATION_OVERLAY'; then
    finding high "ANDROID-OVERLAY-TAPJACKING" "System overlay permission present" "Remove overlay abuse. The overlay plus accessibility combination is a strong malware signal."
  fi
  finding medium "GOOGLE-12-TESTER-RULE" "Verify the closed testing requirement" "A new personal account needs 12 testers over 14 consecutive days before production."
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
