# Mobile Security Requirements Reference (2026)

This reference outlines mobile security best practices, platform implementation guides, and risk assessment methodologies across 17 critical domains for iOS and Android platforms.

Following these guidelines ensures compliance with App Store and Google Play security expectations, prevents common OWASP Mobile Top 10 vulnerabilities, and secures sensitive user information from extraction or manipulation.

---

## Table of Contents
1. [Secure Storage](#1-secure-storage)
2. [Keychain (iOS)](#2-keychain-ios)
3. [Android Keystore](#3-android-keystore)
4. [Biometric Authentication](#4-biometric-authentication)
5. [Certificate Pinning](#5-certificate-pinning)
6. [Jailbreak Detection (iOS)](#6-jailbreak-detection-ios)
7. [Root Detection (Android)](#7-root-detection-android)
8. [SSL Configuration](#8-ssl-configuration)
9. [Backup Rules](#9-backup-rules)
10. [Exported Activities (Android)](#10-exported-activities-android)
11. [Intent Filters (Android)](#11-intent-filters-android)
12. [Deep Links (Custom URL Schemes)](#12-deep-links-custom-url-schemes)
13. [Universal Links (iOS)](#13-universal-links-ios)
14. [App Links (Android)](#14-app-links-android)
15. [Authentication Flows](#15-authentication-flows)
16. [Session Handling](#16-session-handling)
17. [Token Storage](#17-token-storage)

---

## 1. Secure Storage

Storing sensitive credentials, tokens, and personal data unencrypted in local storage is a primary source of credential harvesting and privilege escalation.

### Common Vulnerabilities
- Storing authentication tokens, passwords, or personal data in unencrypted containers: iOS `UserDefaults`, Android `SharedPreferences`, HTML5 `localStorage`, or React Native `AsyncStorage`.
- Keeping plain SQLite databases containing sensitive transactional history on the local filesystem.

### Best Practices and Recommendations
- **Avoid plain local files**: Never store sensitive files, tokens, or configuration keys in raw JSON/XML format within the app sandbox directory.
- **Use Encrypted SQLite**: For structured storage containing sensitive user data, compile and use SQLCipher or an equivalent SQLite library that implements 256-bit AES encryption.
- **Utilize secure wrappers**: Wrap platform secure storage engines (iOS Keychain and Android Keystore) via vetted library interfaces (e.g., `SecureStore` in Expo, `react-native-keychain`, or `flutter_secure_storage`) rather than homebrewed encryption logic.

---

## 2. Keychain (iOS)

The iOS Keychain provides a secure, hardware-accelerated repository for small pieces of sensitive data, such as passwords, cryptographic keys, and tokens.

### Common Vulnerabilities
- Setting overly permissive accessibility constants (e.g., `kSecAttrAccessibleAlways`), allowing data access even when the device is locked or before the user has authenticated.
- Sharing Keychain items across access groups without restricting access to authorized team identifiers.

### Best Practices and Recommendations
- **Strict accessibility classes**: Set explicit, restrictive access policies for every Keychain entry.
  - For standard tokens required only while the app runs: use `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`.
  - For maximum security (unlocked only while device is unlocked, never restored to new devices): use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`.
- **Avoid always-accessible settings**: Never use `kSecAttrAccessibleAlways` or `kSecAttrAccessibleAlwaysThisDeviceOnly` (both are deprecated and unsafe).
- **Access Group restrictions**: If using Keychain Sharing, specify exact access groups in the `Entitlements.plist` to prevent unauthorized cross-app data leaks.

---

## 3. Android Keystore

The Android Keystore system lets developers store cryptographic keys in a container to make them more difficult to extract from the device. Keys can be generated inside the Keystore, allowing cryptographic operations to occur in secure hardware (Trusted Execution Environment or StrongBox).

### Common Vulnerabilities
- Relying on software-backed Keystore implementations without checking if hardware-backed security (TEE or StrongBox) is active.
- Creating keys with empty or weak authorization policies.

### Best Practices and Recommendations
- **Hardware-backed key generation**: Always generate cryptographic keys inside the Keystore using `KeyGenParameterSpec.Builder`.
- **Require Hardware Security**: Query `KeyInfo.isInsideSecureHardware()` to verify that the key resides inside a TEE (Trusted Execution Environment) or StrongBox Keymaster.
- **Configure StrongBox**: For high-security applications (e.g., banking or identity), set `setIsStrongBoxBacked(true)` when generating keys to isolate them within a dedicated, hardware-secured chip.

---

## 4. Biometric Authentication

Biometric authentication (Face ID/Touch ID on iOS and BiometricPrompt on Android) must be bound to cryptographic verification to prevent client-side bypasses.

### Common Vulnerabilities
- **Boolean-only checks**: Relying solely on a success/failure callback boolean from a local API (e.g., LocalAuthentication on iOS) to unlock critical application state. Attackers with rooted or jailbroken devices can easily hook these APIs (using Frida) to force the boolean to return true.
- Failing to handle biometric changes (e.g., when a user adds a new fingerprint to their device, the app should invalidate existing keys).

### Best Practices and Recommendations
- **Crypto-backed biometrics**: Rather than a simple success callback, require a biometric prompt to unlock a Keystore/Keychain-wrapped cryptographic key that is subsequently used to sign a challenge or decrypt a session token.
- **Android key authorization**: On Android, construct the Keystore key with `setUserAuthenticationRequired(true)` and `setUserAuthenticationValidityDurationSeconds(-1)`. This guarantees the key cannot be used unless the user successfully completes biometric authentication.
- **Detect biometric enrollment changes**: On iOS, check the `evaluatedPolicyDomainState` of the `LAContext` before trusting biometric state. If the state changes (new face/fingerprint enrolled), invalidate active tokens and force a full password re-login.

---

## 5. Certificate Pinning

Certificate pinning mitigates Man-in-the-Middle (MitM) attacks by restricting which certificates or public keys are accepted for a given domain, preventing trust in malicious root CAs.

### Common Vulnerabilities
- Pinning the leaf certificate instead of the intermediate CA or public key, which causes immediate application breakage when the leaf certificate expires or is rotated.
- Failing to provide a fallback backup pin, resulting in a bricked application if the primary certificate authority is compromised.
- Disabling certificate verification entirely in staging or test environments and accidentally releasing that configuration to production.

### Best Practices and Recommendations
- **Pin the Public Key (Subject Public Key Info - SPKI)**: Pin the public key hash rather than the full certificate. Public keys remain consistent even when certificates are renewed.
- **Provide Backup Pins**: Always include at least one backup pin from a different Certificate Authority to allow seamless failover during rotation or compromise.
- **Implementation channels**:
  - **Android**: Use the native Network Security Configuration file (`network_security_config.xml`) with the `<pin-set>` element. This is managed by the OS and is highly secure.
  - **iOS**: Use native App Transport Security (ATS) pinning configurations in `Info.plist` (iOS 14 or later), or trust TrustKit for older versions.
  - **Cross-Platform / OkHttp**: For Android apps utilizing OkHttp, leverage the `CertificatePinner` class.

---

## 6. Jailbreak Detection (iOS)

Jailbreak detection identifies compromised iOS devices where sandboxing controls and platform security boundaries have been bypassed, exposing the app to runtime hooking and reverse engineering.

### Common Vulnerabilities
- Relying on a single detection check (e.g., checking only if Cydia exists).
- Performing checks synchronously at app launch in a predictable function, which can be easily identified and bypassed using Frida or Cycript.

### Best Practices and Recommendations
- **Multi-layered heuristics**: Implement multiple distinct detection techniques:
  - **File presence**: Check for common jailbreak files and directories: `/Applications/Cydia.app`, `/Library/MobileSubstrate/MobileSubstrate.dylib`, `/bin/bash`, `/usr/sbin/sshd`, `/etc/apt`.
  - **Directory write test**: Attempt to write a temporary file to system directories outside the app sandbox (e.g., `/private/jailbreak_test.txt`). If the write succeeds, the device is jailbroken.
  - **Protocol scheme check**: Check if the device can open custom schemes like `cydia://`.
  - **Sandbox integrity**: Check for dynamic linker environment variables like `DYLD_INSERT_LIBRARIES`.
- **Obfuscation and timing**: Avoid centralizing detection in a single, well-named method like `isDeviceJailbroken()`. Inline checks or scatter them across unrelated core flows (e.g., during payment initialization or authentication).
- **Graceful degradation**: Do not crash abruptly. Instead, log the risk, notify the backend, and restrict access to high-risk transactions.

---

## 7. Root Detection (Android)

Root detection identifies Android devices that have bypassed standard access controls, allowing attackers to read private app sandboxes, hook memory, and bypass client-side logic.

### Common Vulnerabilities
- Checking only for the `su` binary in standard paths, failing to detect modern root masking engines like Magisk.
- Failing to verify hardware-backed attestation, relying entirely on client-side filesystem checks that are easily masked.

### Best Practices and Recommendations
- **Multi-layered checks**:
  - **Binary scanning**: Search for binaries (`su`, `busybox`) in common paths: `/system/bin/`, `/system/xbin/`, `/sbin/`, `/vendor/bin/`, `/sys/class/`.
  - **Test execution**: Attempt to run the `su` command via `Runtime.getRuntime().exec()`.
  - **Directory write permissions**: Check if system partitions (like `/system` or `/vendor`) are mounted as read-write.
  - **Known packages**: Query the Package Manager for root applications (e.g., `com.topjohnwu.magisk`, `com.noshufou.android.su`).
- **Implement Play Integrity API**: Integrate the modern Play Integrity API to perform hardware-backed integrity attestation. Verify the integrity verdict (`MEETS_DEVICE_INTEGRITY`, `MEETS_STRONG_INTEGRITY`) on a secure backend server before permitting sensitive transactions.

---

## 8. SSL Configuration

Secure Sockets Layer (SSL) and Transport Layer Security (TLS) settings dictate how an app connects to backend resources, preventing traffic interception and decryption.

### Common Vulnerabilities
- Allowing cleartext (HTTP) connections in production.
- Accepting self-signed or invalid certificates by implementing empty trust managers (`TrustManager`) or custom hostname verifiers that return true unconditionally.
- Supporting legacy, insecure protocols (SSLv3, TLS 1.0, TLS 1.1) and weak cipher suites.

### Best Practices and Recommendations
- **Enforce TLS 1.2 or 1.3**: Configure the network stack to reject connections utilizing TLS versions below 1.2.
- **Configure Network Security Policies**:
  - **Android**: Explicitly set `android:usesCleartextTraffic="false"` in the `<application>` tag of `AndroidManifest.xml`. Create a `network_security_config.xml` to restrict cleartext traffic globally, except for specified debug-only local domains.
  - **iOS**: Ensure App Transport Security (ATS) is enabled in `Info.plist` by avoiding `NSAllowsArbitraryLoads = true` unless absolutely required and combined with rigorous justification.
- **Strict Hostname Verification**: Use the platform's default trust managers. Never bypass hostname verification or certificate validation in production builds.

---

## 9. Backup Rules

iOS and Android automatically back up application files and configuration to local machines (via ADB/iTunes) or cloud platforms (Google Drive/iCloud), which can leak local credentials and databases if not explicitly configured.

### Common Vulnerabilities
- Android apps leaving `android:allowBackup="true"` enabled in the `AndroidManifest.xml` without specifying backup rules. Attackers with physical access to an unlocked device can execute `adb backup` to extract the app's entire private database, shared preferences, and encrypted tokens.
- iOS apps storing sensitive cryptographic key material in directories that are automatically synced to iCloud backups.

### Best Practices and Recommendations
- **Android backup configurations**:
  - For high-security applications, completely disable backup by setting `android:allowBackup="false"` in the `<application>` tag of `AndroidManifest.xml`.
  - If backup is required, configure a restrictive backup rules XML file (using `android:dataExtractionRules` for API 31+ and `android:fullBackupContent` for older versions). Explicitly exclude databases, shared preferences, and files containing keys, session tokens, or sensitive user data.
- **iOS backup exclusions**:
  - Mark files containing sensitive data with the `isExcludedFromBackup` attribute (`URLResourceValues.isExcludedFromBackupKey = true`).
  - Store temporary files or transient caches inside the `Caches` or `tmp` directories, which are automatically excluded from backups.

---

## 10. Exported Activities (Android)

Android components (Activities, Services, Broadcast Receivers, Content Providers) declared in the `AndroidManifest.xml` can be marked as exported, allowing external applications to start or query them.

### Common Vulnerabilities
- **Implicitly exporting components**: Activities containing an `<intent-filter>` are automatically exported by default unless `android:exported="false"` is explicitly defined.
- Exporting sensitive activities (e.g., checkout, profile, or settings screens) without applying permission checks, allowing malicious third-party apps on the device to launch them and bypass login gates.

### Best Practices and Recommendations
- **Explicitly declare exported status**: Since Android 12, developers must explicitly declare `android:exported="true"` or `android:exported="false"` for any component containing an intent filter.
- **Minimize exported footprint**: Ensure all internal-only activities, services, and receivers are explicitly marked `android:exported="false"`.
- **Permission gating**: If a component must be exported to allow specific partner apps to access it, protect it with a custom permission using a signature-level protection level (`android:protectionLevel="signature"`), ensuring only apps signed with your certificate can communicate with it.

---

## 11. Intent Filters (Android)

Intent filters define the types of intents that a component can receive, serving as a gateway for communication with other components and applications on the device.

### Common Vulnerabilities
- Relying on implicit intents to transmit sensitive data, allowing malicious broadcast receivers on the device to register for the same action and intercept the payload.
- Executing actions received via incoming intents without verifying the authenticity or integrity of the intent parameters, leading to intent redirection vulnerabilities.

### Best Practices and Recommendations
- **Use explicit intents**: For all internal application communication, use explicit intents naming the target class directly (e.g., `Intent(context, TargetActivity::class.java)`), bypassing the intent filter system entirely.
- **Sanitize incoming intent data**: Always validate and sanitize any parameters received from an incoming intent (using `intent.getStringExtra()` or bundle parameters) before passing them to internal databases, web views, or file operations.
- **Protect against intent redirection**: If your app receives an intent that contains an nested intent to launch another component, verify that the nested intent cannot target internal, non-exported components.

---

## 12. Deep Links (Custom URL Schemes)

Custom URL schemes (e.g., `myapp://`) allow apps to launch from a web page or another app. However, because multiple apps can register the same custom scheme, they are insecure by default.

### Common Vulnerabilities
- **Scheme Hijacking**: A malicious application registers the same custom scheme as your app. When a user clicks a deep link, the OS might launch the malicious app instead, leaking sensitive parameters (such as OAuth authorization codes or session tokens) to the attacker.
- **Parameter Injection**: Acting directly on parameters parsed from a custom URL without validation, leading to arbitrary database queries, unauthorized transactions, or local file extraction.

### Best Practices and Recommendations
- **Do not trust custom schemes for authentication**: Never pass sensitive authorization codes, session tokens, reset tokens, or personal identifiers via custom URL schemes.
- **Strict sanitization**: Treat all incoming deep link URLs as untrusted input. Parse, sanitize, and validate parameters against strict allowlists before performing actions or updating state.
- **Prefer Universal Links / App Links**: Transition all deep linking to secure, validated association standards (Universal Links on iOS, App Links on Android) which guarantee domain ownership.

---

## 13. Universal Links (iOS)

Universal Links use standard HTTP or HTTPS links to launch iOS apps directly, preventing custom scheme hijacking by verifying domain ownership.

### Common Vulnerabilities
- Registering wildcard paths (e.g., `*`) for associated domains, allowing the app to handle sensitive web paths (like password-reset, payments, or administrative routes) that should remain web-only.
- Storing a malformed or unverified `apple-app-site-association` (AASA) file on the hosting server, causing Universal Links to fail silently and fall back to insecure browser behaviors.

### Best Practices and Recommendations
- **Strict path matching**: Define explicit, restrictive paths in your AASA file. Avoid broad wildcards; instead, specify precise sub-paths (e.g., `/app/profile/*`, `/app/dashboard/*`) and exclude administrative or sensitive auth paths.
- **Secure HTTPS hosting**: Host the AASA file on a secure server using HTTPS at the root level or in the `.well-known` directory (`https://example.com/.well-known/apple-app-site-association`). Ensure the server returns `application/json` content type and does not perform redirects.
- **Verify Associated Domains**: Configure the exact domain matching in the `com.apple.developer.associated-domains` entitlement within Xcode, specifying the `applinks:` prefix.

---

## 14. App Links (Android)

Android App Links are HTTP/HTTPS URLs that associate a domain with an Android application, allowing the app to open the link directly without prompting the user to select an app.

### Common Vulnerabilities
- Omitting `android:autoVerify="true"` in the `<intent-filter>` tag within `AndroidManifest.xml`, preventing the OS from verifying the domain association at install time.
- Storing a malformed or publicly writable `assetlinks.json` file on the web server, which fails the association verification process and causes the OS to fall back to standard browser choice dialogs.

### Best Practices and Recommendations
- **Configure Auto-Verification**: Always include `android:autoVerify="true"` on the `<intent-filter>` containing the App Link configuration.
- **Deploy Digital Asset Links**: Host the `assetlinks.json` file securely at `https://example.com/.well-known/assetlinks.json`. The file must contain the application package name and the SHA-256 fingerprint of the app's signing certificate.
- **Verify Association Status**: Check the verification status of App Links using ADB commands during local testing:
  ```bash
  adb shell pm get-app-links <package-name>
  ```
  Ensure the status is verified (`verified` or `legacy_verified`).

---

## 15. Authentication Flows

Mobile authentication flows must handle user credentials and authorization state securely, avoiding standard web vulnerabilities.

### Common Vulnerabilities
- **Implicit Grant Flow**: Implementing the OAuth 2.0 Implicit Grant flow, which returns access tokens directly in the redirect URL, making them vulnerable to interception via deep links.
- **Insecure embedded WebViews**: Using legacy web views (like `UIWebView` or standard `WKWebView` on iOS, or custom WebView configurations on Android) to render login screens, allowing the host app to capture user keystrokes and credentials.

### Best Practices and Recommendations
- **Enforce Authorization Code Flow with PKCE**: Always use the OAuth 2.0 Authorization Code flow combined with Proof Key for Code Exchange (PKCE, RFC 7636). This ensures that intercepted authorization codes cannot be exchanged for tokens without the client-side secret verifier.
- **Use secure system browsers**: Render external login flows using secure, isolated system browser controllers:
  - **iOS**: Use `ASWebAuthenticationSession` or `SFSafariViewController`.
  - **Android**: Use Android Custom Tabs.
  These controllers run in a separate process, preventing the host app from inspecting session cookies, injecting JavaScript, or capturing user credentials.

---

## 16. Session Handling

Secure session management ensures that user sessions are terminated, updated, and validated correctly, limiting the window of opportunity for an attacker.

### Common Vulnerabilities
- Maintaining infinite session lifetimes without enforcing idle timeouts or maximum session durations.
- Failing to mask or blank the application screen when the app transitions to the background, exposing sensitive account details in the device's multitasking app switcher.

### Best Practices and Recommendations
- **Implement short-lived access tokens**: Configure short-lived access tokens (e.g., 15 minutes) coupled with secure refresh token rotation (RTR) where a refresh token is single-use and rotated on every exchange.
- **Application screenshot masking**: Securely blank or blur the application screen during background transitions:
  - **iOS**: Overlay a secure splash screen or blurred view in `applicationWillResignActive` and remove it in `applicationDidBecomeActive`.
  - **Android**: Set `WindowManager.LayoutParams.FLAG_SECURE` in the Activity's `onCreate()` method to prevent screenshots and obscure the multitasking thumbnail.
- **Idle timeout policies**: Implement client-side idle timers that automatically log the user out and clear local cached session state after a defined duration of inactivity.

---

## 17. Token Storage

Tokens (Access, Refresh, and ID tokens) represent active authorizations and must be guarded from local extraction and leakage.

### Common Vulnerabilities
- Storing access or refresh tokens in plaintext logs (using `NSLog` or Android `Log.d`), leaking them to the device's system log buffer (Logcat) where other apps with standard permissions can read them.
- Transmitting tokens over unencrypted HTTP channels or including them as URL query parameters where they are recorded in server logs and browser histories.

### Best Practices and Recommendations
- **Never log tokens**: Strictly audit codebase logging wrappers. Ensure that authorization headers, bearer tokens, and session identifiers are redacted from all console and filesystem logs.
- **Encrypt at rest**: Store all active tokens exclusively in the platform's secure hardware-backed container (iOS Keychain or Android Keystore / EncryptedSharedPreferences).
- **Secure transmission**: Deliver tokens exclusively via HTTPS headers (e.g., `Authorization: Bearer <token>`). Avoid passing tokens in request bodies, query strings, or custom headers unless encrypted.
