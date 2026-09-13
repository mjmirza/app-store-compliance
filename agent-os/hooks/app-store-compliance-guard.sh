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
REPORT=""; REPORT_DEGRADED=0
cleanup() { [ -n "$FILELIST" ] && rm -f "$FILELIST" 2>/dev/null; [ -n "$REPORT" ] && rm -f "$REPORT" 2>/dev/null; true; }
trap cleanup EXIT

# ----- resolve mode and project dir -----
DIR=""
STDIN_JSON=""
CMD=""
if [ "$#" -ge 1 ] && [ -d "$1" ]; then
  DIR="$1"                                   # standalone with explicit path
elif [ "$#" -ge 1 ] && [ ! -d "$1" ]; then
  # An explicit path that does not exist must fail open, never fall back to scanning the working directory.
  log_err "project dir not found. $1"; exit 0
elif [ ! -t 0 ]; then
  STDIN_JSON="$(cat 2>/dev/null || true)"    # hook mode, payload on stdin
  # An empty hook payload has no command to judge; falling back to scanning the working directory can take minutes.
  [ -z "$STDIN_JSON" ] && exit 0
fi

# Read .tool_input.command as JSON (issue #610). The best installed parser decides. jq, else python3,
# else a backslash-aware regex. A payload the chosen parser rejects yields no command, so the guard stays silent.
tool_ok() { command -v "$1" >/dev/null 2>&1 && "$@" >/dev/null 2>&1; }   # present AND able to run
payload_command() {
  local out
  if tool_ok jq -n true; then
    out="$(printf '%s' "$STDIN_JSON" | jq -rs 'if length != 1 then empty else .[0] | if ((.tool_name? // "Bash") != "Bash") then empty else ((.tool_input.command? | strings) // (.command? | strings) // empty) end end' 2>/dev/null)" && { printf '%s' "$out"; return 0; }
  fi
  if tool_ok python3 -c pass; then
    out="$(printf '%s' "$STDIN_JSON" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
except Exception:
    sys.exit(4)
c = None
if isinstance(d, dict) and d.get("tool_name", "Bash") == "Bash":
    ti = d.get("tool_input")
    if isinstance(ti, dict) and isinstance(ti.get("command"), str):
        c = ti["command"]
    elif isinstance(d.get("command"), str):
        c = d["command"]
sys.stdout.buffer.write((c or "").encode("utf-8"))' 2>/dev/null)"; rc=$?
    [ "$rc" -eq 0 ] && { printf '%s' "$out"; return 0; }
    [ "$rc" -eq 4 ] && return 0
  fi
  # No working tool. Prefer the command inside tool_input, else the first command key, then unescape it.
  local body
  body="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"tool_input"[[:space:]]*:[[:space:]]*\{([^{}]|\{[^{}]*\})*"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1)"
  [ -z "$body" ] && body="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1)"
  [ -z "$body" ] && return 0
  printf '%s' "$body" | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"//; s/"$//' \
    | awk 'BEGIN { hx="0123456789abcdef" }
      { n=split($0, part, /\\/); o=part[1]; lit=0
        for (i=2; i<=n; i++) { p=part[i]
          if (lit) { o=o p; lit=0; continue }
          if (p=="") { o=o "\\"; lit=1; continue }
          d=substr(p,1,1); rest=substr(p,2)
          if (d=="n") o=o "\n" rest; else if (d=="t") o=o "\t" rest; else if (d=="r") o=o "\r" rest
          else if (d=="\"") o=o "\"" rest; else if (d=="/") o=o "/" rest
          else if (d=="f") o=o sprintf("%c", 12) rest; else if (d=="b") o=o sprintf("%c", 8) rest
          else if (d=="u" && length(p)>=5) { h=tolower(substr(p,2,4)); v=0; ok=1
            for (j=1;j<=4;j++) { q=index(hx,substr(h,j,1)); if (q==0) {ok=0; break}; v=v*16+q-1 }
            if (ok && v>0 && v<128) o=o sprintf("%c", v) substr(p,6); else o=o "\\" p }
          else o=o "\\" p }
        printf "%s", o }'
}

if [ -n "$STDIN_JSON" ]; then
  # Only a Bash tool call carries a shell command. The jq and python3 tiers check the top-level tool_name.
  # The no-tools tier cannot tell a top-level key from a nested one, so it scans rather than skips.
  CMD="$(payload_command 2>/dev/null | tr -d '\000')"
  # Fold a backslash-newline continuation (odd trailing backslashes) into one space. Bare newlines stay,
  # and grep matches per line, so a trigger split across two commands is never invented.
  CMD="$(printf '%s' "$CMD" | tr -d '\r' | awk '
    { l=$0; if (cont) { sub(/^[ \t]*/, "", l); cont=0 }
      n=length(l); k=0; while (k<n && substr(l,n-k,1)=="\\") k++
      if (k%2==1) { acc=acc substr(l,1,n-1) " "; cont=1 } else { printf "%s%s\n", acc, l; acc="" } }
    END { if (cont) printf "%s\n", acc }' 2>/dev/null)"
  [ -z "$CMD" ] && exit 0
  # Match raw with quotes and letter escapes stripped. Only a single simple line led by an inert text command
  # (echo, grep, cat) has quoted spans blanked, and a heredoc body is blanked unless an interpreter consumes it.
  CMD_MATCH="$(printf '%s' "$CMD" | awk 'BEGIN { sq=sprintf("%c", 39); dq="\""; bt=sprintf("%c", 96); hd=0 }
    { l=$0
      if (hd) { t=l; sub(/^\t+/, "", t); if (t == hd_end) { hd=0 } else if (!hd_keep) { l="" } ; print l; next }
      if (match(l, /<<-?[ \t]*[\047"]?[A-Za-z_][A-Za-z0-9_]*[\047"]?/) && substr(l, RSTART+2, 1) != "<") {
        tag=substr(l, RSTART, RLENGTH); sub(/^<<-?[ \t]*/, "", tag); gsub(/[\047"]/, "", tag); hd=1; hd_end=tag
        hd_keep = (l ~ /(^|[^A-Za-z0-9_\/-])((ba|z|da|k)?sh|eval|ssh|sudo|su|xargs|python[0-9.]*|node|ruby|perl|docker|kubectl|source)([^A-Za-z0-9_-]|$)/) }
      f=l; sub(/^[ \t]*/, "", f)
      while (f ~ /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/) sub(/^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/, "", f)
      split(f, w, /[ \t]+/); c=w[1]
      simple = (index(l, "$(") == 0 && index(l, bt) == 0 && l !~ /[|;&<>]/)
      if (simple && c ~ /^(echo|printf|grep|egrep|fgrep|cat|head|tail|wc|sort|uniq|tee)$/) {
        gsub(sq "[^" sq "]*" sq, sq sq, l); gsub(dq "[^" dq "]*" dq, dq dq, l); sub(/(^|[ \t])#.*$/, "", l) }
      else { gsub(sq, "", l); gsub(dq, "", l) }
      print l }' 2>/dev/null | sed -E 's/\\([A-Za-z0-9])/\1/g')"
  # Only act on submission style commands. Otherwise stay silent.
  if ! printf '%s' "$CMD_MATCH" | grep -qiE 'fastlane[[:space:]]+(deliver|pilot|supply|submit)|eas[[:space:]]+(submit|build)|xcrun[[:space:]]+(altool|notarytool)|transporter|gradlew?[^&|;]*(bundleRelease|assembleRelease)|bundletool|xcodebuild[^&|;]*archive|flutter[[:space:]]+build[[:space:]]+(ipa|appbundle|apk|ios)|(npx[[:space:]]+)?(expo[[:space:]]+(prebuild|run:ios|run:android)|cap[[:space:]]+(sync|build|run|copy|open)|react-native[[:space:]]+run-(ios|android))|ionic[[:space:]]+capacitor[[:space:]]+(build|run)|cordova[[:space:]]+build([[:space:]]+--release)?'; then
    exit 0
  fi
  DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
  # A leading "cd <dir> &&" scopes the scan to that app (an EAS monorepo submits from apps/<app>).
  # The target must resolve inside the project root, otherwise the root is scanned as before.
  FIRST="$(printf '%s' "$CMD" | head -1)"
  CD_COUNT="$(printf '%s' "$CMD" | grep -oE '(^|[;&|(][[:space:]]*)(cd|pushd|popd|source|\.)[[:space:]]' | wc -l | tr -d ' ')"
  if [ "$CD_COUNT" -eq 1 ] && printf '%s' "$FIRST" | grep -qE '^[[:space:]]*cd[[:space:]]+[^&|;]+(&&|;)'; then
    TARGET="$(printf '%s' "$FIRST" | sed -E 's/^[[:space:]]*cd[[:space:]]+//; s/[[:space:]]*(&&|;).*$//; s/^"(.*)"$/\1/; s/^'"'"'(.*)'"'"'$/\1/')"
    TARGET="${TARGET//\$\{CLAUDE_PROJECT_DIR\}/$DIR}"; TARGET="${TARGET//\$CLAUDE_PROJECT_DIR/$DIR}"
    case "$TARGET" in /*) ;; '~'*) TARGET="$HOME${TARGET#\~}" ;; *) TARGET="$DIR/$TARGET" ;; esac
    if [ -d "$TARGET" ]; then
      REAL_T="$(cd "$TARGET" 2>/dev/null && pwd -P)"; REAL_R="$(cd "$DIR" 2>/dev/null && pwd -P)"
      case "$REAL_T/" in "$REAL_R"/*) DIR="$REAL_T" ;; esac
    fi
  fi
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
# Directories are pruned by name, and only below the project root (-mindepth 1). The old full-path
# match also hit the folders ABOVE the root, so a project sitting under a folder named build was
# scanned as empty, and it still walked every excluded tree. Test code, Python virtualenvs, and
# bundled web output (dist) never ship in the binary, and a virtualenv's vendored JSON otherwise
# reads as app source. .xcprivacy is scanned because NSPrivacyCollectedDataTypes lives there.
FILELIST="$(mktemp 2>/dev/null || echo /tmp/ascg.$$)"
find "$DIR" -mindepth 1 \
  \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
    -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage \
    -o -name '*Tests' -o -name androidTest -o -name __tests__ -o -name test -o -name tests \
    -o -name integration_test -o -name .venv -o -name venv -o -name site-packages -o -name .pub-cache \) -prune \) \
  -o -type f \( \
  -name '*.swift' -o -name '*.m' -o -name '*.h' -o -name '*.kt' -o -name '*.java' \
  -o -name '*.xml' -o -name '*.plist' -o -name '*.gradle' -o -name '*.kts' \
  -o -name '*.json' -o -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \
  -o -name '*.dart' -o -name '*.xcconfig' -o -name '*.yaml' -o -name '*.yml' \
  -o -name '*.pbxproj' -o -name '*.entitlements' -o -name '*.html' -o -name '*.xcprivacy' \
  \) -print 2>/dev/null \
  > "$FILELIST"

grep_has() {  # 0 if regex found in any source file
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

manifest_has() {  # 0 if regex found in any AndroidManifest.xml in the source list
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(grep '/AndroidManifest\.xml$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
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

# Cross-platform apps reach StoreKit and Play Billing through a plugin, so the native symbols never
# appear in their source. These are the plugins' own package names.
XPLAT_IAP='in_app_purchase|purchases_flutter|flutter_inapp_purchase|react-native-iap|react-native-purchases|expo-iap|cordova-plugin-purchase|@revenuecat/purchases-capacitor'

# Vendored trees never decide the platform, and the prune applies only below the project root, so a project
# that itself sits under a folder named build or test is still detected. Same SIGPIPE-safe grep as the source scan.
find_app() {  # find_app <maxdepth> <find name expression...>
  local depth="$1"; shift
  find "$DIR" -mindepth 1 -maxdepth "$depth" \
    \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
      -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage -o -name .pub-cache \) -prune \) \
    -o \( "$@" \) -print 2>/dev/null
}

# ----- platform detection -----
# Every find below pipes into `grep .`, never `grep -q .`, for the reason in release_string_has:
# grep -q exits on the first match, find dies of SIGPIPE, and pipefail turns "found" into "missing".
IS_IOS=0; IS_AND=0; IS_WEB=0
find_app 4 -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'Package.swift' -o -name 'Podfile' | grep . >/dev/null && IS_IOS=1
find_app 4 -name 'Info.plist' | grep . >/dev/null && IS_IOS=1
find_app 5 -name 'AndroidManifest.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' | grep . >/dev/null && IS_AND=1
find_app 4 -name 'package.json' -o -name 'index.html' -o -name 'webpack.config.js' -o -name 'next.config.js' | grep . >/dev/null && IS_WEB=1

# ----- cross-platform framework detection -----
# IS_IOS/IS_AND above still fire on the built artifact. This adds framework-specific checks.
IS_FLUTTER=0; IS_RN=0; IS_IONIC=0
find_app 4 -name 'pubspec.yaml' | grep . >/dev/null && IS_FLUTTER=1
# Scan EVERY package.json within depth (not just the first), so a monorepo root's tooling
# package.json never shadows a real apps/mobile/package.json deeper in the tree.
while IFS= read -r pkg; do
  grep -qE '"react-native"|"expo"' "$pkg" 2>/dev/null && IS_RN=1
  grep -qE '"@capacitor/core"|"@capacitor/ios"|"@capacitor/android"|"@ionic/(angular|react|vue)"|"cordova-android"|"cordova-ios"' "$pkg" 2>/dev/null && IS_IONIC=1
done < <(find "$DIR" -maxdepth 4 -name 'package.json' 2>/dev/null | grep -vE '/(node_modules|ios/Pods)/')
find_app 4 -name 'capacitor.config.*' | grep . >/dev/null && IS_IONIC=1
# config.xml alone is ambiguous (Maven/NuGet/tooling also use that filename), so require the
# Cordova widget marker before it counts as a signal.
while IFS= read -r cfg; do
  grep -qE '<widget|xmlns:cdv' "$cfg" 2>/dev/null && IS_IONIC=1
done < <(find "$DIR" -maxdepth 4 -name 'config.xml' 2>/dev/null)

# The actual gate the framework checks below use: a committed ios/ folder AND the
# invoking command (when known) does not explicitly target Android-only.
IOS_TARGET_ACTIVE=0
[ "$IS_IOS" -eq 1 ] && [ "$CMD_TARGET_ANDROID_ONLY" -eq 0 ] && IOS_TARGET_ACTIVE=1

# ----- report routing (issue #610). Hook mode buffers the report. A block goes to stderr, the only
# stream Claude Code shows on exit 2. A pass stays on stdout. Standalone mode prints straight to stdout.
emit_report() {  # $1 is the exit code about to be returned
  [ -n "$REPORT" ] || return 0
  exec 1>&3 3>&-
  if [ "$1" -eq 2 ]; then cat "$REPORT" >&2; else cat "$REPORT"; fi
  rm -f "$REPORT" 2>/dev/null; REPORT=""
}
# A hook timeout sends TERM. Flush what was buffered to stderr so the partial report is not lost.
trap 'emit_report 2; exit 143' INT TERM HUP
if [ -n "$STDIN_JSON" ]; then
  REPORT="$(mktemp 2>/dev/null)" || REPORT=""
  if [ -n "$REPORT" ] && : >"$REPORT" 2>/dev/null; then exec 3>&1; exec >"$REPORT"; else REPORT=""; REPORT_DEGRADED=1; fi
fi

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
# App Store Connect API 4.3 and 4.4 removed the old age-rating declaration endpoints. a pipeline that still calls them stops the release.
if grep_has 'appStoreVersions/[^ "]*/ageRatingDeclaration|relationships/ageRatingDeclaration'; then
  finding critical "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED" "Pipeline calls a removed App Store Connect API age-rating endpoint" "Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes)."
fi
# Genuine placeholder CONTENT only. the bare word "placeholder" matches every SwiftUI
# `placeholder:` parameter and a "TODO"/"FIXME" matches normal dev comments, neither of which is a
# rejection cause, so match real placeholder markers a reviewer would actually see.
if grep_has 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'; then
  finding high "BOTH-PLACEHOLDER" "Placeholder content (lorem ipsum, example.com, dummy text) found in sources" "Replace placeholder text and assets with real content."
fi
# ROSCA and CA/NY/MA negative-option laws bind regardless of the vacated federal rule.
# "call" and "write" match as whole words only, or "renews automatically until cancelled" and
# "overwrite ... cancel" read as an instruction to call or write in.
if grep_has 'subscri(be|ption)|auto.renew|membership' && grep_has '(^|[^A-Za-z])[Cc]all[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,25}[^A-Za-z][Cc]all([^A-Za-z]|$)|[Mm]ail.{0,25}[Cc]ancel|(^|[^A-Za-z])[Ww]rite[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,15}(in.person|by.phone|by.mail)'; then
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
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep . >/dev/null; then
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
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep . >/dev/null; then
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
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep . >/dev/null; then
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
  # Hide My Email relay addresses now also come from private.icloud.com (Apple news 1ptvdtcm, corrected 24 Aug 2026).
  if grep_has 'privaterelay\.appleid\.com' && ! grep_has 'private\.icloud\.com'; then
    finding critical "APPLE-4.0-SIWA-RELAY-DOMAIN" "Sign in with Apple relay allowlist accepts only privaterelay.appleid.com" "Accept private.icloud.com as well, everywhere relay addresses are validated or allowlisted."
  fi
  # Age assurance. a parent can withdraw consent, Apple then blocks launch. the app must handle RESCIND_CONSENT.
  if grep_has 'DeclaredAgeRange|AgeRangeService' && ! grep_has 'RESCIND_CONSENT|rescindConsent'; then
    finding high "APPLE-5.1.1-RESCIND-CONSENT-UNHANDLED" "Declared Age Range used without RESCIND_CONSENT handling" "Handle the RESCIND_CONSENT server notification, revoke the minor session and consent-scoped data, and build with the iOS 26.2 SDK or later."
  fi
  # The no-entitlement external purchase link is a US-storefront carve-out only. everywhere else it is still 3.1.1.
  if grep_has 'ExternalPurchaseLink|external-purchase-link|openExternalPurchaseLink' && ! grep_has 'Storefront|storefront|countryCode'; then
    finding high "APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING" "External purchase link is not gated on the storefront" "Show the link only on the US storefront (or where you hold the entitlement). gate on Storefront.current or countryCode."
  fi
  # On-Demand Resources are deprecated from the 27 OS family (WWDC26).
  if grep_has 'NSBundleResourceRequest|OnDemandResources|on-demand-resource'; then
    finding high "APPLE-ODR-DEPRECATED-27" "On-Demand Resources in use, deprecated starting iOS 27" "Migrate tagged resources to the Background Assets framework."
  fi
  # Since September 2026 the social media capability question gates every submission (Apple news 0d2gpmml).
  if grep_has 'newsFeed|NewsFeed|followers|chatRoom|ChatRoom|DirectMessage|liveStream|LiveStream'; then
    finding medium "APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION" "Social features detected, confirm the social media capability declaration in App Store Connect" "Answer the social media question before submitting. it sets a 13+ minimum and requires Declared Age Range for under-13 users."
  fi
  # Match the tracking SDKs by their own type names / imports, never the bare words "Adjust" or
  # "Branch", which collide with ordinary English ("Adjust times", a git branch) and false-flag a
  # tracking SDK that is not present.
  if grep_has 'AppsFlyerLib|import AppsFlyer|AdjustConfig|AdjustEvent|import Adjust[^A-Za-z]|BranchEvent|BranchUniversalObject|import Branch[^A-Za-z]|FBSDKCoreKit|FBSDKLogin|ASIdentifierManager|advertisingIdentifier'; then
    grep_has 'ATTrackingManager|NSUserTrackingUsageDescription' || finding high "APPLE-5.1.2-MISSING-ATT" "Tracking SDK without App Tracking Transparency" "Call the ATT prompt and add NSUserTrackingUsageDescription (Apple 5.1.2)."
  fi
  if grep_has 'Stripe|PayPalCheckout|braintree|razorpay'; then
    grep_has "StoreKit|SKProduct|Product\.purchase|$XPLAT_IAP" || finding critical "APPLE-3.1.1-EXTERNAL-PAYMENT" "External payment SDK without StoreKit" "Route digital goods through in app purchase unless the app is a documented exempt category (Apple 3.1.1)."
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
    if ! find "$DIR" -name 'PrivacyInfo.xcprivacy' 2>/dev/null | grep . >/dev/null; then
      finding critical "APPLE-PRIVACY-MANIFEST-MISSING" "Required reason APIs or SDKs present but no PrivacyInfo.xcprivacy" "Add a privacy manifest with approved reason codes and tracking domains, and confirm each SDK ships its signed manifest."
    fi
  fi

  # A manifest that exists can still be internally inconsistent. Apple validates
  # these keys at upload and rejects by email (ITMS-91xxx) after processing, so
  # the binary installs from TestFlight and is still barred from review.
  MANIFEST_VALIDATOR=""
  for candidate in \
    "$(dirname "$0")/../../scripts/validate-privacy-manifest.py" \
    "$HOME/.claude/skills/app-store-compliance/scripts/validate-privacy-manifest.py"; do
    [ -f "$candidate" ] && { MANIFEST_VALIDATOR="$candidate"; break; }
  done
  if [ -n "$MANIFEST_VALIDATOR" ] && command -v python3 >/dev/null 2>&1; then
    # Same exclusions as the source file list. A pod's manifest is the vendor's job, a Tests fixture never ships.
    find "$DIR" -mindepth 1 \
      \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
        -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage \
        -o -name '*Tests' -o -name androidTest -o -name __tests__ -o -name test -o -name tests \
        -o -name integration_test -o -name .venv -o -name venv -o -name site-packages -o -name .pub-cache \) -prune \) \
      -o -name 'PrivacyInfo.xcprivacy' -print 2>/dev/null \
      | while IFS= read -r manifest; do
          python3 "$MANIFEST_VALIDATOR" "$manifest" 2>/dev/null
        done > "$FILELIST.manifest" 2>/dev/null || true
    if [ -s "$FILELIST.manifest" ]; then
      while IFS="$(printf '\t')" read -r sev id msg; do
        [ -n "$id" ] || continue
        finding "$sev" "$id" "$msg" "Correct the privacy manifest so its keys agree, then rebuild. Reference. https://developer.apple.com/documentation/bundleresources/privacy_manifest_files"
      done < "$FILELIST.manifest"
    fi
    rm -f "$FILELIST.manifest" 2>/dev/null || true
  elif find_app 12 -name 'PrivacyInfo.xcprivacy' | grep . >/dev/null; then
    finding medium "APPLE-MANIFEST-VALIDATOR-UNAVAILABLE" "Privacy manifests present but python3 or scripts/validate-privacy-manifest.py is missing, so their internals were not validated" "Install python3 and keep scripts/validate-privacy-manifest.py next to the guard, or run plutil -lint on each manifest by hand."
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
    grep_has "BillingClient|com\.android\.billingclient|$XPLAT_IAP" || finding critical "GOOGLE-PLAY-BILLING" "External payment without Play Billing" "Use Play Billing for in app digital goods."
  fi
  # Payments policy exception is literal. only a tax-exempt charity may take donations outside Play
  # billing (AnkiDroid, August 2026). A donate link to a funding platform is a Payments violation.
  if grep_has 'opencollective\.com|ko-fi\.com|patreon\.com|buymeacoffee\.com|github\.com/sponsors|liberapay\.com|paypal\.com/donate'; then
    finding high "GOOGLE-PAYMENTS-DONATION-LINK" "In-app donation link to a payment page outside Play billing" "Remove the donation entry point from the Play build or sell it through Play billing. Only a tax-exempt charity (501(c)(3)-class) may bypass Play billing, Google rejects 501(c)(6) and unincorporated projects (Payments policy)."
  fi
  # Since 3 August 2026 the developer bears chargeback costs. An app on Play billing that never
  # handles the refund-review notification loses every fraudulent dispute by default.
  # New apps and updates need Play Billing Library 8 or later since 31 August 2026 (deprecation ladder, extension to 1 November 2026).
  BILLING_MAJOR="$(grep -E '/build\.gradle(\.kts)?$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -hoE 'com\.android\.billingclient:billing(-ktx)?:[0-9]+' 2>/dev/null | grep -oE '[0-9]+$' | sort -n | tail -1)"
  if [ -n "$BILLING_MAJOR" ] && [ "$BILLING_MAJOR" -lt 8 ]; then
    finding critical "GOOGLE-PLAY-BILLING-V8-REQUIRED" "Play Billing Library $BILLING_MAJOR.x, new apps and updates need version 8 or later since 31 August 2026" "Upgrade com.android.billingclient:billing to 8.x, or request the Play Console extension available until 1 November 2026."
  fi
  if grep_has 'BillingClient|com\.android\.billingclient'; then
    grep_has 'PendingRefundReviewNotification|[Rr]eview[Rr]efund' || finding medium "GOOGLE-PLAY-CHARGEBACK-LIABILITY" "Play billing without chargeback dispute handling" "Handle PendingRefundReviewNotification and call the Review Refund API within 24 hours with the refund preference and usage evidence (Play Console Help answer 17068375)."
  fi
  # From 30 September 2026 regulated categories must publish from an organization account with a D-U-N-S number.
  if grep_has 'VpnService|HealthConnect|health\.connect|BankAccount|cryptocurrency'; then
    finding high "GOOGLE-ORG-REGISTRATION-REQUIRED" "Regulated-category signals (VPN, health, finance), organization account required from 30 Sep 2026" "Publish from an organization account with a D-U-N-S number matching the Dun and Bradstreet profile (Play Console Help 10788890)."
  fi
  # Geofencing is no longer an approved foreground-service use case for API 37 targets (Play Console Help 16965181).
  if grep_has 'FOREGROUND_SERVICE_LOCATION' && grep_has '[Gg]eofenc'; then
    finding high "GOOGLE-FGS-GEOFENCE-REMOVED" "Foreground service used for geofencing" "Move to the Geofence API (GeofencingClient) and drop FOREGROUND_SERVICE_LOCATION if geofencing was its only use."
  fi
  # Random or anonymous chat is now in scope of Age-Restricted, Families, and Child Safety Standards (26 Aug 2026).
  if grep_has '[Rr]andom chat|[Aa]nonymous chat|chat with strangers|Omegle' && ! grep_has 'ageGate|minorBlock|csae'; then
    finding critical "GOOGLE-ANON-CHAT-MINOR-BLOCK" "Random or anonymous chat without minor blocking and child-safety standards" "Enable Play Console minor blocking, exclude children from the target audience, publish CSAE standards, add in-app reporting and a child-safety contact."
  fi
  # Generative image or video apps need NCII controls and a full-access test account (Android Developers Blog, 25 Aug 2026).
  if grep_has 'generateImage|imageGeneration|text-to-image|faceSwap|stable-diffusion' && ! grep_has '[Mm]oderation|safetyClassifier|contentFilter'; then
    finding high "GOOGLE-GENAI-NCII-CONTROLS" "Generative image or video feature without moderation controls" "Add input and output moderation for intimate and deepfake content, document tested safety prompts, and give the reviewer a full-access test account."
  fi
  # From February 2027 release builds must be R8-optimized (25 percent minimum coverage, Play Console Help 17492799).
  if ! grep -rqE '(isMinifyEnabled|minifyEnabled)[[:space:]=]+true' "$DIR" --include='*.gradle' --include='*.kts' 2>/dev/null; then
    finding high "ANDROID-R8-OPTIMIZATION-MISSING" "No release build type with minifyEnabled true" "Enable R8 (isMinifyEnabled = true, isShrinkResources = true) in the release build type before February 2027."
  fi
  # From April 2027 sign-in apps must restore sign-in state on a new device (Restore Credentials API).
  if grep_has 'signInWith|CredentialManager|FirebaseAuth|LoginActivity' && ! grep_has 'RestoreCredential'; then
    finding medium "ANDROID-RESTORE-CREDENTIALS-REQUIRED" "Sign-in present without Restore Credentials integration" "Create a restore credential on sign-in and restore it after device transfer (Play technical quality requirement, April 2027)."
  fi
  if grep_has 'firebase-analytics|com\.google\.android\.gms\.ads|appsflyer|com\.adjust|com\.facebook'; then
    finding high "GOOGLE-DATASAFETY-MISMATCH" "Analytics or ad SDK present. Verify the Data Safety form" "Declare every collection and sharing accurately. Data Safety mismatch is the top Google rejection."
  fi
  if ! grep_has 'privacyPolicy|privacy-policy'; then
    finding high "GOOGLE-MISSING-PRIVACY-POLICY" "No privacy policy reference found" "Publish a privacy policy and set its URL in the Play Console store listing."
  fi
  # Every build.gradle in the source list. A bare ** glob without globstar only saw one directory level, so
  # android/app/build.gradle was never read. Play rejects new apps and updates below API 36 since 31 August 2026.
  TSDK="$(grep -E '/build\.gradle(\.kts)?$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -hoE 'targetSdk(Version)?[[:space:]=]+[0-9]+' 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)"
  if [ -n "$TSDK" ] && [ "$TSDK" -lt 36 ]; then
    finding critical "GOOGLE-TARGET-API" "targetSdk is $TSDK, below the API 36 floor Play enforces for new apps and updates since 31 August 2026" "Target API 36 or higher (Wear OS and Automotive 35, TV and XR 34), or request the Play Console extension available until 1 November 2026."
  fi
  # Android 17 (API 37) targets. contacts picker, location button scope, and local network permission (27 Jan 2027).
  if [ -n "$TSDK" ] && [ "$TSDK" -ge 37 ] 2>/dev/null; then
    if grep_has 'READ_CONTACTS' && ! grep_has 'ACTION_PICK|ContactPicker'; then
      finding high "GOOGLE-CONTACTS-PICKER-REQUIRED" "READ_CONTACTS on an API 37 target where the Contact Picker may suffice" "Use the Android Contact Picker for one-off selection and keep READ_CONTACTS only for a declared core use (Play Console Help 16909972)."
    fi
    if grep_has 'ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION' && ! grep_has 'onlyForLocationButton'; then
      finding high "GOOGLE-LOCATION-BUTTON-SCOPE" "Location requested on an API 37 target without the location button scope" "Scope one-shot location to the Android location button with the onlyForLocationButton manifest flag (Play Console Help 16909972)."
    fi
    if grep_has 'NsdManager|MulticastSocket|_tcp\.local|mDNS' && ! grep_has 'ACCESS_LOCAL_NETWORK'; then
      finding high "ANDROID-LOCAL-NETWORK-PERMISSION" "Local network discovery on an API 37 target without ACCESS_LOCAL_NETWORK" "Declare and request android.permission.ACCESS_LOCAL_NETWORK before any LAN discovery or connection (Android 17 behavior changes)."
    fi
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
  # Play only allows READ_MEDIA_IMAGES and READ_MEDIA_VIDEO on API 33+ when the system picker cannot serve the core
  # feature, and a Play Console declaration is required either way (Photo and Video Permissions policy).
  if manifest_has 'android\.permission\.READ_MEDIA_(IMAGES|VIDEO)'; then
    if ! grep_has 'PickVisualMedia|ACTION_PICK_IMAGES|PhotoPicker|photo_picker'; then
      finding high "GOOGLE-PHOTO-VIDEO-PERMISSIONS-DECLARATION" "READ_MEDIA_IMAGES or READ_MEDIA_VIDEO declared without the Android photo picker" "Use the Android photo picker for one-off selection. Keep broad access only for a core gallery-style feature and complete the Photo and Video Permissions declaration in Play Console."
    fi
  fi
  # Declared permissions in AndroidManifest.xml, the surface Play enforces on (#542). English words matched prose,
  # and bare API symbols match imports, comments and vendored SDKs. READ_MEDIA_* has its own check below.
  if manifest_has 'android\.permission\.(READ_CONTACTS|WRITE_CONTACTS|READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG|GET_ACCOUNTS|MANAGE_EXTERNAL_STORAGE)'; then
    if ! grep_has 'prominent disclosure|user consent|privacy consent|accept policy|[Pp]rominentDisclosure|[Dd]isclosureDialog|[Cc]onsentDialog|showDisclosure|requestConsent'; then
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
    emit_report 0; exit 0
  fi
  echo ""
  echo "BLOCKED. $CRIT critical rejection risk(s) above. Fix them, or set APP_STORE_GUARD_OK=1 to override."
  [ "${REPORT_DEGRADED:-0}" = "1" ] && echo "BLOCKED. $CRIT critical rejection risk(s). Full report on stdout (no temp file available for buffering)." >&2
  emit_report 2; exit 2
fi
emit_report 0; exit 0
