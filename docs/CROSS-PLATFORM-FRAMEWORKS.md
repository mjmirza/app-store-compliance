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
imports `expo` polyfills, for example); every matching check runs.

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

- `IONIC-4.2-THIN-WRAPPER` (critical). The single most common Ionic rejection.
  A WebView/Capacitor/Cordova marker is present with fewer than 2 DISTINCT
  native-feel plugins (status bar, splash screen, push notifications, haptics,
  share, camera, local notifications). Counts distinct plugin identifiers, not
  files, so multiple plugin imports in one bootstrap file are counted correctly.
  Fix by adding native chrome plugins, or ship as an installable PWA to skip App
  Review entirely.
- `IONIC-UIWEBVIEW-DEPRECATED` (critical). The literal `UIWebView` symbol,
  usually pulled in by a stale plugin even when app code never references it
  directly. Apple auto-rejects (ITMS-90809) any binary that statically links it.
- `IONIC-PRIVACY-MANIFEST-MISSING` (high). Capacitor/Cordova plugin manifest
  support is less standardized than Flutter's. Verify each plugin wrapping a
  native SDK ships its own `PrivacyInfo.xcprivacy`.

## The honest limit

The guard reads Swift, Kotlin, XML, Gradle, Plist, Dart, JS, and TS source text.
It does not execute the app, does not parse the Dart or JS AST, and cannot see
runtime behavior (whether an OTA update actually changes the UI, for example).
Treat every finding as a lead to verify, not a guaranteed defect, and treat a
clean run as "nothing detectable from source text", not a guarantee of approval.
