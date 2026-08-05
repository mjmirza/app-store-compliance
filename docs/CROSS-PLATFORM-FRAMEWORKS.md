# Cross-Platform Framework Coverage

The guard scans the app's built artifact surface (Info.plist, AndroidManifest.xml,
entitlements, gradle, PrivacyInfo.xcprivacy) which store review inspects regardless of
what generated it. This page documents the checks specific to the framework that
generated the app, on top of the native checks.

## Detection

| Framework | Detected by |
|---|---|
| Flutter | `pubspec.yaml` present within 3 levels of the project root |
| React Native / Expo | `package.json` dependency on `react-native` or `expo` |
| Ionic / Capacitor / Cordova | `package.json` dependency on `@capacitor/*`, `@ionic/*`, or `cordova-*`, OR a `capacitor.config.*` / `config.xml` file |

A project can match more than one framework flag (a Capacitor app that also
imports `expo` polyfills, for example); every matching check runs. Detection scans
EVERY `package.json`/`config.xml` within depth, not only the first, so a monorepo
whose root `package.json` is tooling-only still finds the real app deeper in the
tree. A `config.xml` only counts as Cordova evidence when it carries a `<widget>`
or `xmlns:cdv` marker, since that filename collides with unrelated tooling configs.

Every framework-specific finding below is gated on `IOS_TARGET_ACTIVE`, not raw
file-tree presence. A committed `ios/` folder is common in a real cross-platform
repo even when the current build is Android-only, so file presence alone cannot
tell `flutter build apk` apart from an iOS build. When the invoking command is
known (hook mode) and clearly targets Android only (`build apk/appbundle`,
`assembleRelease`, `bundleRelease`, `run-android`, `run:android`,
`--platform android`, `capacitor android`, with no `ios`/`ipa`/`xcodebuild`
token present), the command overrides the file-tree signal and these Apple-only
checks stay silent. Standalone mode (no command context) falls back to plain
file-tree detection.

## Submission commands the guard recognizes

`fastlane deliver/pilot/supply/submit`, `eas submit`, `eas build`, `xcrun altool`,
`xcrun notarytool`, `transporter`, `gradlew bundleRelease/assembleRelease`,
`bundletool`, `xcodebuild archive`, `flutter build ipa/appbundle/apk`,
`cap sync/build/run` (with or without `npx`), `ionic capacitor build/run`,
`cordova build` (with or without `--release`).

## Flutter checks

- `FLUTTER-PRIVACY-MANIFEST-MISSING` (critical). A required-reason-API plugin
  (permission_handler, image_picker, geolocator, device_info_plus,
  package_info_plus, shared_preferences, sqflite, firebase_*) is a dependency and
  no `PrivacyInfo.xcprivacy` exists anywhere in the project. Since Flutter 3.19
  most first-party plugins ship their own manifest, but the aggregation only
  works when the app also ships one.
- `FLUTTER-NO-IOS-RUNNER-FOUND` (medium, advisory). No `Info.plist` was found, so
  every iOS-specific check in this guard was skipped. Run `flutter create .` or
  confirm the `ios/` platform folder exists before an iOS submission.

Known limitation. The guard cannot see whether a purpose-string value that
exists only in a localized `InfoPlist.strings` file was also copied into the
real `Info.plist` shipped in the archive (ITMS-90683). Check this by hand
before submitting.

## React Native / Expo checks

- `RN-OTA-UNDECLARED` (high). An over-the-air JS bundle updater
  (`react-native-code-push`, `expo-updates`, `react-native-ota-hot-update`,
  Stallion) is present with no App Review disclosure. Apple 3.3.2/2.5.2 allow
  bug-fix-only OTA updates when disclosed by name in the review notes; an
  undeclared swappable bundle reads as dormant functionality.
- `RN-PRIVACY-MANIFEST-MISSING` (critical). A native module touching
  required-reason APIs (Firebase, AsyncStorage, expo-file-system) is present
  transitively via a JS dependency and no `PrivacyInfo.xcprivacy` exists. This is
  the hardest of the three frameworks to audit by eye because the native SDK
  hides behind a JS package name.

## Ionic / Capacitor / Cordova checks

- `IONIC-4.2-THIN-WRAPPER` (high, advisory). The single most common Ionic
  rejection reason in the wild, but this check is a HEURISTIC PROXY, not the
  actual Apple 4.2 test, which is about features, content, and UI beyond a
  repackaged website, not a plugin count. A real app using unmatched plugins
  (`@capacitor/preferences`, private native plugins) can false-positive; a thin
  wrapper that imports two matched plugins for cosmetic reasons can false-negative.
  Review manually before treating this as a hard blocker. Counts distinct plugin
  identifiers, not files, so multiple plugin imports in one bootstrap file are
  counted correctly.
- `IONIC-UIWEBVIEW-DEPRECATED` (critical). The literal `UIWebView` symbol,
  usually pulled in by a stale plugin even when app code never references it
  directly. Apple auto-rejects (ITMS-90809) any binary that statically links it.
- `IONIC-PRIVACY-MANIFEST-MISSING` (high). Capacitor/Cordova plugin manifest
  support is less standardized than Flutter's. Verify each plugin wrapping a
  native SDK ships its own `PrivacyInfo.xcprivacy`.

## Known gaps (found by Codex and Qwen adversarial review, not yet fixed)

- **Newline-containing file paths.** The `package.json`/`config.xml` scan loops
  are safe against spaces and shell metacharacters (quoted `IFS= read -r`), but
  not against a literal newline inside a path, which `find`'s newline-delimited
  output cannot represent. Extremely unlikely in practice, and not proven safe.
- **`config.xml` widget-marker check is spoofable by a comment.** A commented-out
  `<!-- <widget ...> -->` or a look-alike tag like `<widgetConfig>` still counts
  as Cordova evidence. Low severity, no realistic false negative on a real
  Cordova project, though not a hard proof either.
- **Android-side framework checks are absent.** Every check in this doc is
  Apple-side. Flutter/RN/Ionic apps also ship to Google Play, where Data Safety
  disclosure for bundled SDKs, WebView-controlled data collection, cleartext
  traffic, and mixed-content/debug flags are real, framework-relevant risks this
  guard does not yet check.
- **The PrivacyInfo.xcprivacy presence check is both too loose and too strict.**
  It accepts a manifest found anywhere, including inside `node_modules` or
  `Pods`, which does not prove an APP-LEVEL manifest exists. It also has no
  Expo-managed-workflow awareness (`expo.ios.privacyManifests` in `app.json`
  can be valid with no `ios/PrivacyInfo.xcprivacy` on disk yet, since EAS
  generates the native project remotely at build time).
- **Expo Continuous Native Generation (CNG) is not modeled.** A managed Expo
  project legitimately has no committed `ios/`/`android/` folder; treating that
  as "no iOS target" is not always correct.
- **Other cross-platform frameworks have no coverage.** NativeScript,
  Xamarin/.NET MAUI, Kotlin Multiplatform, Unity (mobile export), and Tauri
  Mobile are not detected at all.
- **The submission regex still misses a few real commands**
  (`eas build` with no platform flag, ambiguous local `cap run` without a
  release intent) and can overfire on non-release local dev commands.

These are logged, not hidden. Track them before treating this guard as complete
coverage for a cross-platform team; the checks that exist are a real
improvement over native-only, not a finished answer.

## The honest limit

The guard reads Swift, Kotlin, XML, Gradle, Plist, Dart, JS, and TS source text.
It does not execute the app, does not parse the Dart or JS AST, and cannot see
runtime behavior (whether an OTA update actually changes the UI, for example).
Treat every finding as a lead to verify, not a guaranteed defect, and treat a
clean run as "nothing detectable from source text", not a guarantee of approval.
