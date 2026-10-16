# Cross-Platform Framework Coverage

The guard scans the app's built artifact surface (Info.plist, AndroidManifest.xml,
entitlements, gradle, PrivacyInfo.xcprivacy) which store review inspects regardless of
what generated it. This page documents the checks specific to the framework that
generated the app, on top of the native checks.

## Detection

| Framework | Detected by |
|---|---|
| Flutter | `pubspec.yaml` present within 12 levels of the project root |
| React Native / Expo | `package.json` within 12 levels with a dependency on `react-native` or `expo` |
| Ionic / Capacitor / Cordova | `package.json` within 12 levels with a dependency on `@capacitor/*`, `@ionic/*`, or `cordova-*`, OR a `capacitor.config.*` / `config.xml` file within 12 levels |

These depths come from the `find_app` calls in
`agent-os/hooks/app-store-compliance-guard.sh`. Unity, .NET MAUI, Tauri mobile,
and Kotlin Multiplatform are searched within 6 levels.

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
checks stay silent. 2.0.0 also requires every other command in the line to be a
known harmless one, so it never silences more than 1.0.0 did. Standalone mode (no command context) falls back to plain
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

Four behaviours to know.

- A Unity project is scanned for both stores when it is run by hand. As a hook the `-buildTarget` value picks the store.
- A Unity project holds no Xcode or Gradle project until it is exported, so the export compliance check and the R8 check stay silent and the report says so. Scan the exported project too.
- A Kotlin Multiplatform project is scanned as one app, so shared code in `commonMain` counts for both the iOS and the Android checks.
- A bare Xcode or Android project under a root Expo, React Native, Flutter, or Capacitor app is scanned as its own app when it has its own `Info.plist` or `AndroidManifest.xml` and no root build file names its path (`settings.gradle`, a `Podfile`, or an `.xcworkspace`). It counts as an app only with an `.xcodeproj` that builds an application (or names no product type) or an Android application module, so a library, a framework or a local native module stays with the app that uses it. A native host that embeds the root framework (React Native, Expo, Flutter, Capacitor or Cordova code in its sources, such as an `RCTAppDelegate`, or its Podfile or Gradle files) is a brownfield host and stays in the root scan, so the root's framework checks still cover it. A native app that does split off, and the root it left, both keep every framework check the pooled tree showed, so every check that ran when they were scanned as one still runs, a framework marker found only inside the split app included. The root and its split native apps are also scanned together as in 1.0.0, and any finding the separate scans missed is added once, so evidence spread across a shared file and the split app still counts. A project in a folder named exactly `demo`, `example`, `sample`, or `playground` (or the plural) is treated as a repo demo and stays part of the root scan. A nested project splits off only when the root has its own project for that platform, so a managed Expo root with no native project keeps scanning the nested project and keeps its iOS checks. A native root app never splits off a nested project (issue #656).

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
- **Pooled or split layouts that remain coarse (inherited from 1.0).** A single nested managed Expo app is read through the root's config only, shared packages and a brownfield host's source outside the scanned root are not followed, every native target in one root is pooled, and two .NET MAUI or Unity apps in one repo are scanned as one.
- **Workspace runners.** A package script is followed one level deep, so a root script that runs `turbo run build`, which in turn runs a mobile package's submit, is not seen. A pnpm graph selector (`web...`, `...web`, `{apps/web}`) is reduced to its package name, without following that package's dependencies or dependents, and a change-set selector such as `"[origin/main]"` cannot be resolved, so it reads every package, which can block a web-only build in a repo that also holds a mobile app. Run the web build without the wrapper, or set `APP_STORE_GUARD_OK=1` once.
- **Cross-platform purchase plugins.** 1.0.0 checked the restore flow only for native StoreKit apps. 2.0.0 also checks a react-native-iap, RevenueCat or Flutter purchase plugin app, where a purchase list query (`getAvailablePurchases`, `queryPastPurchases`) or the plugin's restore call counts as the restore flow. Check by hand that a visible Restore Purchases control calls it.
- **Monitor source verification.** The regulatory and privacy monitors mark a claim as corroborated when an official source shares its keywords, not when that source states the same claim. Read the official source before acting on a monitor item.
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
- **Android-side framework checks are thin.** Apart from the Android
  permissions array a managed Expo app config declares, every check in this doc is
  Apple-side. Flutter/RN/Ionic apps also ship to Google Play, where Data Safety
  disclosure for bundled SDKs, WebView-controlled data collection, cleartext
  traffic, and mixed-content/debug flags are real, framework-relevant risks this
  guard does not yet check.
- **The PrivacyInfo.xcprivacy check reads the app's own manifest only.**
  A manifest under `Pods`, `Carthage`, `node_modules`, SwiftPM `.build` or
  checkouts, `SourcePackages` or Flutter `.symlinks` does not count. A managed
  Expo app passes with `expo.ios.privacyManifests` in its app config, since EAS
  generates the native project at build time.
- **Expo Continuous Native Generation (CNG) is modeled for config only.** A
  managed Expo project with no committed `ios/` or `android/` folder has its
  `app.json` or `app.config` read for camera and location purpose strings,
  `ios.privacyManifests` and the sensitive `android.permissions` entries. Its
  native code is still NOT CHECKED until `npx expo prebuild` runs.
- **Two frameworks have no coverage.** NativeScript and legacy Xamarin.Forms
  are not detected. Unity, .NET MAUI, Tauri mobile, and Kotlin Multiplatform
  are, see the section above for what each one still cannot see.
- **The submission regex errs toward firing.** `SUBMIT_RE` in
  `agent-os/hooks/app-store-compliance-guard.sh` matches `eas build` with or
  without a `--platform` flag, also when global flags come before the
  subcommand. It also matches every `cap run` and `cap open`, so a local dev
  run with no release intent still triggers the guard.

These are logged, not hidden. Track them before treating this guard as complete
coverage for a cross-platform team; the checks that exist are a real
improvement over native-only, not a finished answer.

## The honest limit

The guard reads Swift, Kotlin, XML, Gradle, Plist, Dart, JS, TS, C#, and Rust source text.
It does not execute the app, does not parse the Dart or JS AST, and cannot see
runtime behavior (whether an OTA update actually changes the UI, for example).
Treat every finding as a lead to verify, not a guaranteed defect, and treat a
clean run as "nothing detectable from source text", not a guarantee of approval.
