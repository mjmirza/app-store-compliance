# Mobile Security Compliance Audit and Best Practices Review (2026)

This document provides a comprehensive, rigorous security audit and best practices review across seventeen critical mobile security domains. Prepared by the Senior Compliance Officer, this audit evaluates native platform architectures (iOS and Android) against industry security baselines (such as OWASP MASVS - Mobile Application Security Verification Standard), international standards, and platform-specific requirements (Apple App Store Review Guidelines and Google Play Developer Policies).

---

## Executive Summary

To ensure complete organizational integrity and robust client-side protection, this audit establishes technical security baselines for all applications maintained under this repository. Implementing these controls is mandatory for mitigating risk vectors such as dynamic instrumentation, static reverse engineering, token theft, and transport interception.

---

## 1. Secure Storage

### 1.1 Overview and Platform Mechanics
Sensitive data stored locally on physical devices must be encrypted to prevent unauthorized extraction. Standard sandbox structures—such as iOS `UserDefaults` or standard Android `SharedPreferences`—persist data in plaintext XML/plist formats within the application data sandbox. While sandboxing prevents cross-app access on non-compromised devices, these files are fully exposed on rooted/jailbroken devices or via system backup extractions.

- **iOS Mechanics**: The system employs Data Protection APIs mapped to the hardware-backed Secure Enclave. Developers must enforce File Protection classes when writing data directly to disk.
- **Android Mechanics**: Standard Android uses the ext4/f2fs filesystem with file-based encryption (FBE). However, local shared preference XML files remain decrypted while the device is in an unlocked state.

### 1.2 Identified Gaps and Risks
- Writing tokens, user profiles, or credentials in standard plist/xml databases.
- Relying on offline client-side databases (e.g. SQLite, Realm, Room) without active cryptographic page-level encryption.

### 1.3 Best Practice Recommendations
- **iOS Implementation**: Force page-level database encryption using SQLCipher for local storage. For small values, utilize the iOS Keychain. When saving files directly, append the `Data.WritingOptions.completeFileProtection` option.
- **Android Implementation**: Utilize Jetpack Security's `EncryptedSharedPreferences` and `EncryptedFile`, which automatically apply AES-256-SIV for keys and AES-256-GCM for values, with keys wrapped in the Android Keystore.
- **Citations**: [Android Developer Guide on Data Security](https://developer.android.com/topic/security/data), [Apple Developer Documentation on File Protection](https://developer.apple.com/documentation/uikit/protecting_the_user_s_privacy/encrypting_your_app_s_files_with_data_protection).

---

## 2. Keychain

### 2.1 Overview and Platform Mechanics
The iOS Keychain provides a secure container for small quantities of sensitive data, such as API keys, access tokens, and passwords. It operates as a SQLite database managed directly by the `securityd` daemon, isolated from individual apps except through explicit access entitlements.

### 2.2 Identified Gaps and Risks
- Using overly permissive accessibility attributes (such as `kSecAttrAccessibleAlways` or `kSecAttrAccessibleAlwaysThisDeviceOnly`), which expose items to background processes when the device is locked.
- Allowing keys to be synchronized with iCloud Backups when they are meant to be restricted to the physical device.

### 2.3 Best Practice Recommendations
- Apply the strict `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` protection class for items that must be accessed by background tasks, or `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for foreground-only operations.
- Avoid using `kSecAttrSynchronizable` unless cross-device synchronization is a verified product requirement.
- Explicitly partition keychain access groups to prevent access outside defined application suites.
- **Citations**: [Apple Developer Documentation on Keychain Services](https://developer.apple.com/documentation/security/keychain_services).

---

## 3. Android Keystore

### 3.1 Overview and Platform Mechanics
The Android Keystore system lets applications store cryptographic keys in hardware-backed storage to prevent extraction from the device. This system runs within the Trusted Execution Environment (TEE) or an isolated hardware security module (HSM) such as StrongBox.

### 3.2 Identified Gaps and Risks
- Generating keys using software-based providers without asserting hardware backing.
- Leaving keys unrestricted, allowing them to be used for arbitrary algorithms or operations without user authentication constraints.

### 3.3 Best Practice Recommendations
- Enforce the use of hardware-backed keys by checking `KeyInfo.isInsideSecureHardware()` after generation.
- For devices running Android 9 (API 28) or higher, call `setIsStrongBoxBacked(true)` during `KeyGenParameterSpec` initialization to isolate keys in physical StrongBox hardware.
- Limit key purposes specifically (e.g., restrict exclusively to `PURPOSE_DECRYPT` or `PURPOSE_SIGN`).
- **Citations**: [Android Developer Guide on Keystore](https://developer.android.com/training/articles/keystore).

---

## 4. Biometric Authentication

### 4.1 Overview and Platform Mechanics
Biometric authentication (FaceID/TouchID on iOS, BiometricPrompt on Android) verifies the user's physical presence. A common vulnerability is implementing "offline biometrics" that merely evaluate a boolean callback (such as a success block), which can be bypassed using runtime hooking libraries (e.g. Frida) to force the boolean return value to true.

### 4.2 Identified Gaps and Risks
- Relying on non-cryptographic biometric evaluations where runtime instrumentation can bypass the verification.
- Storing access tokens in plaintext and releasing them upon a simple boolean callback.

### 4.3 Best Practice Recommendations
- **iOS Implementation**: Wrap sensitive tokens inside a Keychain item configured with a `SecAccessControl` reference. Set the access control flag to `.biometryAny` or `.biometryCurrentSet`. The OS will prompt the user for biometrics and will decrypt and release the item only if biometrics succeed.
- **Android Implementation**: Initialize a cryptographic cipher from the Keystore (configured with `.setUserAuthenticationRequired(true)`) and wrap it in a `BiometricPrompt.CryptoObject`. Pass this object to the `authenticate()` call. The cipher can only be unlocked if the biometric challenge succeeds.
- **Citations**: [Android Developer Guide on Biometric Prompt](https://developer.android.com/training/sign-in/biometric-auth), [Apple Developer Documentation on SecAccessControl](https://developer.apple.com/documentation/security/secaccesscontrol).

---

## 5. Certificate Pinning

### 5.1 Overview and Platform Mechanics
Certificate Pinning secures HTTP traffic against Man-in-the-Middle (MITM) attacks by binding a client application to trusted server public keys. This mitigates risks associated with rogue certificate authorities (CAs) or user-installed root profiles.

### 5.2 Identified Gaps and Risks
- Pinning the leaf certificate directly, which causes application downtime when certificates expire and are rotated.
- Failing to include backup pins, resulting in application lockouts during emergency key rollovers.

### 5.3 Best Practice Recommendations
- Pin the Subject Public Key Info (SPKI) rather than the leaf certificate.
- Ensure at least one backup pin represents a different certificate authority or root backup.
- **iOS Implementation**: Configure native declarative Network Session Pinning in `Info.plist` using `NSPinnedDomains`.
- **Android Implementation**: Declare SPKI hashes in `res/xml/network_security_config.xml` under the `<pin-set>` element.
- **Citations**: [OWASP Certificate Pinning Cheat Sheet](https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning).

---

## 6. Jailbreak Detection

### 6.1 Overview and Platform Mechanics
Jailbreaking circumvents iOS sandbox restrictions, exposing secure resources, enabling dynamic library injection, and compromising client-side trust boundaries.

### 6.2 Identified Gaps and Risks
- Relying on a single file check (e.g. looking for Cydia.app), which is easily bypassed by jailbreak masking tools.
- Failing to clear memory-cached credentials when a jailbroken environment is identified.

### 6.3 Best Practice Recommendations
- Combine multiple independent client-side heuristics:
  1. Check for jailbreak-specific files and executables (e.g., `/Applications/Cydia.app`, `/bin/bash`, `/usr/sbin/sshd`).
  2. Attempt to write to folders outside the application sandbox directory (such as writing to `/private/jailbreak.txt`).
  3. Analyze loaded dynamic libraries using the `dyld` API to detect hooking frameworks like MobileSubstrate or Frida.
  4. Perform symlink detection on system directories (e.g., `/Applications`).
- Programmatically purge access tokens and terminate the application session when compromise is detected.
- **Citations**: [OWASP MASVS Resilience Requirements](https://mas.owasp.org/MASVS/).

---

## 7. Root Detection

### 7.1 Overview and Platform Mechanics
Rooting an Android device provides superuser access, which compromises the integrity of the operating system sandbox and exposes raw application memory.

### 7.2 Identified Gaps and Risks
- Using easily bypassed client-side checks like searching for `su` binaries or `test-keys`.
- Not utilizing server-side validation for device integrity checks.

### 7.3 Best Practice Recommendations
- Implement a two-tiered root detection strategy. Combine local heuristic checks with native Google Play Integrity API attestation.
- **Local Heuristics**: Search standard binary search paths for administrative indicators (`/system/bin/su`, `/system/xbin/su`, `/sbin/su`, `/system/sd/xbin/su`). Monitor `android.os.Build.TAGS` for `test-keys`.
- **Hardware Attestation**: Request an integrity token using the Play Integrity API, pass the token to your secure backend, and verify the attestation verdict on the server-side to ensure the device runs a certified Android environment.
- **Citations**: [Android Developer Guide on Google Play Integrity API](https://developer.android.com/google/play/integrity).

---

## 8. SSL Configuration

### 8.1 Overview and Platform Mechanics
Secure communication is the first line of defense for application payloads. Unsecure configurations, such as allowing cleartext traffic (HTTP), permit active network sniffing.

### 8.2 Identified Gaps and Risks
- Allowing arbitrary HTTP cleartext traffic globally in production.
- Permitting trust anchors for user-installed root certificates in production configurations.

### 8.3 Best Practice Recommendations
- Enforce TLS 1.2 or TLS 1.3 as the absolute minimum protocol version.
- **iOS Implementation**: Maintain App Transport Security (ATS) active. Ensure `NSAllowsArbitraryLoads` is set to `false`. Explicitly declare exception domains in `NSExceptionDomains` only when strictly required for non-production domains.
- **Android Implementation**: Configure `android:usesCleartextTraffic="false"` in the application manifest, and enforce this via `network_security_config.xml` to limit trust anchors exclusively to system-trusted CAs:
  ```xml
  <network-security-config>
      <base-config cleartextTrafficPermitted="false">
          <trust-anchors>
              <certificates src="system" />
          </trust-anchors>
      </base-config>
  </network-security-config>
  ```
- **Citations**: [Android Developer Guide on Network Security Configuration](https://developer.android.com/training/articles/security-config), [Apple Developer Documentation on App Transport Security](https://developer.apple.com/documentation/security/preventing_insecure_network_connections).

---

## 9. Backup Rules

### 9.1 Overview and Platform Mechanics
Standard mobile backups copy application databases, shared preferences, and files from the sandbox directory to cloud or desktop storage. If backups are not restricted, a physical extraction or compromised cloud account can retrieve sensitive application state.

### 9.2 Identified Gaps and Risks
- Allowing full backups of SQLite databases containing personal information or authentication credentials.
- Leaving `android:allowBackup` set to `true` without specific exclusions.

### 9.3 Best Practice Recommendations
- **iOS Implementation**: Programmatically exclude sensitive application files, local databases, and temporary resources from iCloud and iTunes backups by adding the `.isExcludedFromBackup` attribute to the file URL.
- **Android Implementation**: For high-security applications, disable backups completely by declaring `android:allowBackup="false"` in the manifest. If backup is required, configure exact inclusions and exclusions via `android:dataExtractionRules` (for Android 12+) and `android:fullBackupContent` (for legacy Android versions) to exclude specific directories (e.g. database and shared preference files holding session data).
- **Citations**: [Android Developer Guide on Auto Backup](https://developer.android.com/guide/topics/data/autobackup), [Apple Developer Documentation on Preventing Files From Being Backed Up](https://developer.apple.com/library/archive/qa/qa1719/_index.html).

---

## 10. Exported Activities

### 10.1 Overview and Platform Mechanics
Android activities, services, or broadcast receivers marked as exported (`android:exported="true"`) are accessible to all other applications on the device. Malicious apps can launch these components to bypass internal authentication states or inject malicious intents.

### 10.2 Identified Gaps and Risks
- Unintentionally exporting internal activities containing sensitive details or private state transitions.
- Failing to declare the `android:exported` attribute on Android 12+, which causes compiler or installer rejections.

### 10.3 Best Practice Recommendations
- Enforce a strict default policy of `android:exported="false"` for all activities, services, and receivers unless they explicitly require external invocation (e.g., the launcher activity).
- For components that must be exported, enforce signature-level custom permissions (`android:protectionLevel="signature"`) to ensure that only applications signed with your exact developer certificate can interact with them.
- **Citations**: [Android Developer Guide on Activities](https://developer.android.com/guide/components/activities/intro-activities).

---

## 11. Intent Filters

### 11.1 Overview and Platform Mechanics
Intent filters define the types of intents that a component can receive. Registering an intent filter automatically marks the component as exported in older Android API levels.

### 11.2 Identified Gaps and Risks
- Relying on implicit intents for internal communication, which can be intercepted by malicious listener applications.
- Failing to validate data received from an external intent filter.

### 11.3 Best Practice Recommendations
- Use explicit class intents for all internal application communication.
- When handling external intents, validate the calling package using `getCallingActivity()` or `getCallingPackage()` before executing any actions or processing data.
- **Citations**: [Android Developer Guide on Intents and Intent Filters](https://developer.android.com/guide/components/intents-filters).

---

## 12. Deep Links

### 12.1 Overview and Platform Mechanics
Deep links trigger internal routes based on custom URL schemes (e.g. `myapp://path`). These schemes are inherently unverified, allowing multiple applications to register the same scheme.

### 12.2 Identified Gaps and Risks
- Transmitting sensitive credentials (such as access tokens or recovery keys) directly within custom URL parameters.
- Executing privileged local actions or database mutations based solely on deep link commands without additional authentication checks.

### 12.3 Best Practice Recommendations
- Treat all incoming deep link parameters as untrusted inputs. Implement rigorous validation and sanitization.
- Do not transmit sensitive tokens in deep links. If authentication is required via link, pass a short-lived, single-use, cryptographically random reference code that must be exchanged via a secure HTTPS POST request.
- **Citations**: [Android Developer Guide on Deep Linking](https://developer.android.com/training/app-links/deep-linking).

---

## 13. Universal Links

### 13.1 Overview and Platform Mechanics
Universal Links utilize secure HTTPS URLs to route traffic directly to iOS applications, bypassing custom scheme routing and eliminating custom URL scheme hijacking.

### 13.2 Identified Gaps and Risks
- Misconfigured association files or unencrypted web connections to the hosting domain, which disable secure domain association verification on iOS.

### 13.3 Best Practice Recommendations
- Host a valid `apple-app-site-association` (AASA) JSON file at your target domain's `.well-known/apple-app-site-association` endpoint.
- Serve the file over HTTPS, with `Content-Type: application/json`, and without any HTTP redirects.
- Enable the Associated Domains capability in Xcode, declaring domains in the exact `applinks:yourdomain.com` format.
- **Citations**: [Apple Developer Documentation on Universal Links](https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html).

---

## 14. App Links

### 14.1 Overview and Platform Mechanics
Android App Links use HTTPS URLs to deep link directly into Android applications, verifying domain ownership to prevent the platform disambiguation dialog.

### 14.2 Identified Gaps and Risks
- Missing or malformed Digital Asset Links files on the hosting domain.
- Missing `android:autoVerify="true"` attributes in the manifest.

### 14.3 Best Practice Recommendations
- Host a valid `assetlinks.json` file on your domain at `https://yourdomain.com/.well-known/assetlinks.json`.
- Declare the digital certificate SHA-256 fingerprint of the production signing key in the `sha256_cert_fingerprints` field.
- Configure `<intent-filter android:autoVerify="true">` in the `AndroidManifest.xml` file.
- **Citations**: [Android Developer Guide on App Links Verification](https://developer.android.com/training/app-links/verify-site-associations).

---

## 15. Authentication Flows

### 15.1 Overview and Platform Mechanics
Mobile authentication must ensure that user credentials are securely transmitted and verified, and that backend client secrets are not exposed within the mobile package.

### 15.2 Identified Gaps and Risks
- Hardcoding OAuth client secrets in application binaries, which can be extracted via static analysis.
- Utilizing insecure embedded web views (e.g., standard `WKWebView` or standard `WebView`) for login screens, which allow the host app to capture passwords.

### 15.3 Best Practice Recommendations
- Implement OAuth 2.1 or OpenID Connect (OIDC) protocols with Proof Key for Code Exchange (PKCE) (RFC 7636).
- Perform authentication using secure system browsers, such as `ASWebAuthenticationSession` on iOS and Custom Tabs on Android. These operate in isolated memory processes separate from the host application.
- **Citations**: [IETF RFC 7636 - Proof Key for Code Exchange](https://oauth.net/2/pkce/).

---

## 16. Session Handling

### 16.1 Overview and Platform Mechanics
Session state must be tracked and invalidated securely on both the client and server.

### 16.2 Identified Gaps and Risks
- Relying on local client-side state to determine session validity without server-side validation.
- Failing to blur multitasking window previews, exposing sensitive screen content in background snapshots.

### 16.3 Best Practice Recommendations
- Enforce strict server-side session validation for every critical API request.
- Blur or mask the application window during background transitions (e.g., covering the window with a splash screen on iOS inside `applicationWillResignActive` or using `WindowManager.LayoutParams.FLAG_SECURE` on Android).
- Implement server-side session invalidation upon user logout, and simultaneously purge all cached data and local credentials.
- **Citations**: [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

---

## 17. Token Storage

### 17.1 Overview and Platform Mechanics
Tokens (access and refresh tokens) represent active authorization sessions and must be protected as high-value secrets.

### 17.2 Identified Gaps and Risks
- Storing long-lived refresh tokens in plain, unencrypted storage (like standard plist files or Shared Preferences).
- Printing tokens to console output or diagnostic loggers.

### 17.3 Best Practice Recommendations
- Always isolate access and refresh tokens within the iOS Keychain or Android `EncryptedSharedPreferences`.
- Utilize short-lived access tokens (e.g., 15 minutes) and implement sliding sessions with token rotation on refresh.
- Enforce hardware-backed security classes on refresh tokens (such as requiring biometric authorization or restricting access to `ThisDeviceOnly`).
- **Citations**: [OWASP MASVS Cryptographic Verification](https://mas.owasp.org/MASVS/).
