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
`cordova build` (with or without `--release`), `Unity ... -buildTarget iOS/Android`,
`dotnet publish -f net8.0-ios/android`, `tauri ios/android build`.

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

## Unity, .NET MAUI, Tauri mobile, and Kotlin Multiplatform

Added for issue 837. Each one is detected, named on the `Frameworks.` line, and has a bad and a clean project in the test suite.

| Framework | Detected by | Source now read | Submit command that runs the scan |
|---|---|---|---|
| Unity | `ProjectSettings/ProjectVersion.txt` | `.cs` | `Unity -batchmode ... -buildTarget iOS` or `Android` |
| .NET MAUI | a `.csproj` with `UseMaui` or a `net8.0-ios` style target | `.cs`, `.xaml`, `.csproj` | `dotnet publish -f net8.0-ios` or `net8.0-android` |
| Tauri mobile | `tauri.conf.json`, `tauri.conf.json5` or `Tauri.toml` | `.rs`, `.toml` | `tauri ios build`, `tauri android build`, with or without `cargo` or `npx` |
| Kotlin Multiplatform | the multiplatform plugin in a Gradle file | `commonMain` Kotlin, as before | the Gradle and `xcodebuild archive` commands already covered |

Three behaviours to know.

- A Unity project is scanned for both stores when it is run by hand. As a hook the `-buildTarget` value picks the store.
- A Unity project holds no Xcode or Gradle project until it is exported, so the export compliance check and the R8 check stay silent and the report says so. Scan the exported project too.
- A Kotlin Multiplatform project is scanned as one app, so shared code in `commonMain` counts for both the iOS and the Android checks.

## What stays out of reach

These are limits, not bugs waiting for a fix. Plan around them.

- **Anything that runs on a CI server.** `gh workflow run`, a release started from a CI dashboard, and a fastlane lane run by a runner are never seen by a hook on your machine.
- **Uploads from an app window.** Xcode Organizer, the Transporter app, the Unity Editor build window and Android Studio's Generate Signed Bundle do not run a shell command.
- **A Unity build whose target is chosen in code.** `-executeMethod` with no `-buildTarget iOS` or `Android` on the command line is not treated as a submit.
- **Unity and .NET MAUI build settings.** Info.plist keys and Gradle settings that the tool generates at build time are not read. For .NET MAUI the linker and target API settings in the `.csproj` are not checked, and `dotnet build -t:Publish` is not matched. A Mac Catalyst publish is not treated as a submit.
- **Tauri before init.** With no `src-tauri/gen/apple` or `src-tauri/gen/android` folder there is nothing native to scan. The report names the command to run.
- **A Tauri app beside a native app.** In a monorepo a Tauri folder with no `gen/apple` or `gen/android` is treated as a desktop app, so it does not stop a `CLEAR` for the native app next to it.
- **Rust naming.** The sign-in and account-deletion patterns look for camelCase names such as `signIn`. A Rust function named `sign_in` does not trigger them.
- **Frameworks not detected.** NativeScript and legacy Xamarin.Forms projects.
- **More than one Xcode target.** Targets are read as one body of source, so an app extension can satisfy, or trigger, a finding for the main app. A watchOS-only or visionOS-only workspace is treated as iOS.
- **Store console state.** The guard cannot see App Store Connect or Play Console, so the age rating, social media declaration, and closed testing items are reminders, not proof of a problem.

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
- **Two frameworks have no coverage.** NativeScript and legacy Xamarin.Forms
  are not detected. Unity, .NET MAUI, Tauri mobile, and Kotlin Multiplatform
  are, see the section above for what each one still cannot see.
- **The submission regex still misses a few real commands**
  (`eas build` with no platform flag, ambiguous local `cap run` without a
  release intent) and can overfire on non-release local dev commands.

These are logged, not hidden. Track them before treating this guard as complete
coverage for a cross-platform team; the checks that exist are a real
improvement over native-only, not a finished answer.

## The honest limit

The guard reads Swift, Kotlin, XML, Gradle, Plist, Dart, JS, TS, C#, and Rust source text.
It does not execute the app, does not parse the Dart or JS AST, and cannot see
runtime behavior (whether an OTA update actually changes the UI, for example).
Treat every finding as a lead to verify, not a guaranteed defect, and treat a
clean run as "nothing detectable from source text", not a guarantee of approval.
