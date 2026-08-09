# Mobile Security Compliance Audit and Best Practices Review (2026)

This compliance audit and best practices review provides a rigorous, comprehensive assessment of this repository and mobile applications using this security playbook against seventeen core mobile security domains. Directed by the Senior Compliance Officer, this audit aligns with the OWASP Mobile Application Security Verification Standard (MASVS) L1 and L2 guidelines, App Store Review Guidelines, and Google Play Developer Policies.

All analysis, guidelines, recommendations, and checklists in this document are strictly emoji-free and free of graphical symbols to comply with repository coding rules.

---

## Executive Summary

As mobile applications process increasingly sensitive personal, financial, and authentication data, securing client-side boundaries is paramount. This review systematically analyzes seventeen critical mobile security areas across iOS (Apple) and Android (Google) ecosystems. The objective is twofold:
1. Verify how security requirements are tracked, scanned, and enforced statically within this repository.
2. Outline platform-specific mechanisms, potential vulnerabilities, and concrete implementation rules to guide development teams toward secure releases.

Through utilities like the automated pre-submission compliance guard and platform-specific monitors, this repository actively mitigates common pitfalls before binaries are uploaded to the stores. This report serves as the definitive reference for continuous security auditing and release readiness certification.

---

## Core Audit of the 17 Mobile Security Domains

### 1. Secure Storage

#### 1.1 Technical Mechanics
- **iOS:** Standard sandboxed files are unencrypted on disk unless Explicit Data Protection is enabled. The `UserDefaults` API writes directly to unencrypted Plist files within the sandbox. The proper standard is utilizing the Keychain Services API or SQLCipher.
- **Android:** Standard `SharedPreferences` write key-value pairs in plaintext XML files. Internal and external files are accessible on rooted devices. The standard is using the Jetpack Security library components (`EncryptedSharedPreferences` and `EncryptedFile`) which employ AES-256-GCM.

#### 1.2 Audit Methodology & Repository Status
- **Detection Signals:** Scanning for `UserDefaults.standard.set`, `getSharedPreferences`, and standard plain SQLite/Room database initializations.
- **Rejection Risks:** Storing sensitive session credentials or personal data in plaintext triggers severe privacy and security rejections under Apple Guideline 5.1.1 and Google Play User Data policies.
- **Recommendations:**
  - Enforce a strict compile-time ban on writing authorization credentials to plain `UserDefaults` or standard `SharedPreferences`.
  - Encrypt all local structured data via SQLCipher.
  - Utilize `EncryptedSharedPreferences` for Android configurations containing metadata or non-token identity markers.

---

### 2. Keychain (iOS Specific)

#### 2.1 Technical Mechanics
- The iOS Keychain is a secure, hardware-accelerated enclave database operated by the iOS Security Daemon.
- High-security items must declare appropriate Accessibility Constants (`kSecAttrAccessible`) to restrict when the data can be decrypted:
  - `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`: Restricts decryption until the user unlocks the device once after booting. This is highly recommended for apps with background processing.
  - `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`: Restricts decryption to when the screen is active and unlocked.
  - Non-`ThisDeviceOnly` attributes allow the keychain items to migrate to other devices via backups, creating a physical boundary leak risk.

#### 2.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `kSecAttrAccessible`, `SecItemAdd`, and custom Keychain wrappers.
- **Rejection Risks:** Storing critical access tokens without the `ThisDeviceOnly` protection class allows unauthorized extraction when physical backups are restored on secondary hardware.
- **Recommendations:**
  - Set `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` as the default keychain insertion configuration.
  - Disable `kSecAttrSynchronizable` unless explicit iCloud syncing is mandated and documented.
  - Conduct periodic audits of any third-party wrappers (such as SwiftKeychain) to confirm they do not default to insecure classes.

---

### 3. Android Keystore (Android Specific)

#### 3.1 Technical Mechanics
- The Android Keystore system allows cryptographic keys to be generated and stored in hardware-backed secure storage: the Trusted Execution Environment (TEE) or StrongBox Security Chip (introduced in Android 9, API 28).
- Hardware-backed keys ensure that key material cannot be extracted from the device memory even if the OS is fully rooted.

#### 3.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `AndroidKeyStore`, `KeyGenParameterSpec.Builder`, `setIsStrongBoxBacked`, and `isInsideSecureHardware`.
- **Rejection Risks:** Failure to protect signing keys or decryption keys via hardware containers allows key extraction in compromised client environments, failing Google Play Device and Network Abuse policies.
- **Recommendations:**
  - Require keys used for high-value signatures (e.g., payment payloads, health records) to enforce StrongBox backing via `setIsStrongBoxBacked(true)`.
  - Validate hardware isolation at runtime by verifying `KeyInfo.isInsideSecureHardware()` returns true.
  - Strictly limit key operations to required cryptographic purposes (e.g., `PURPOSE_DECRYPT` only, disabling sign/verify on the same key alias).

---

### 4. Biometric Authentication

#### 4.1 Technical Mechanics
- Biometric authentication (FaceID/TouchID on iOS, BiometricPrompt on Android) must be tightly integrated with the platform's cryptographic keystore.
- Treating biometrics as an offline boolean return check (e.g., running `LAContext.evaluatePolicy` and simply routing the user to the main screen on success) is a major flaw. Attackers easily bypass this check using dynamic hooking engines like Frida.

#### 4.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `LAContext`, `evaluatePolicy`, `BiometricPrompt`, and `CryptoObject`.
- **Rejection Risks:** Bypasseable local biometric checks expose apps to unauthorized client-side access, violating core security expectations of both major stores.
- **Recommendations:**
  - Enforce **Crypto-Backed Biometrics**. The app must request biometrics to unlock a cryptographic key stored in the Keychain or Keystore.
  - On iOS, insert the access token with `SecAccessControl` constraints. The OS then prompts the user and releases the token only if biometrics match.
  - On Android, initialize a `BiometricPrompt.CryptoObject` wrapping a Keystore-backed cipher. The Keystore key must require user authentication on creation.

---

### 5. Certificate Pinning

#### 5.1 Technical Mechanics
- Certificate pinning prevents Man-in-the-Middle (MITM) attacks by specifying which public keys or certificate authorities (CAs) are trusted.
- Pinning the leaf certificate directly is discouraged because standard certificate rotations will break the application, leading to bricked installs. The best practice is pinning the Subject Public Key Info (SPKI) hashes of the root or intermediate CAs.

#### 5.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `NSPinnedDomains` in `Info.plist`, `network_security_config` XML, and `CertificatePinner` objects.
- **Rejection Risks:** Lack of transport-level protection allows MITM traffic interception, exposing user credentials and violating privacy standards under Apple Guideline 5.1.1 and Google Play data protection rules.
- **Recommendations:**
  - Utilize declarative platform pinning: `NSPinnedDomains` for iOS 14+ and `<pin-set>` inside Android's `network_security_config.xml`.
  - Always include at least one backup SPKI pin representing a secondary or emergency backup CA.
  - Implement certificate pinning expiration dates to gracefully fall back to standard system trust anchors rather than bricking the application permanently.

---

### 6. Jailbreak Detection (iOS)

#### 6.1 Technical Mechanics
- iOS applications running on jailbroken devices lose standard sandbox protections. Attackers can modify runtime binaries and access local storage directly.
- Jailbreak detection must use a multi-layered heuristic approach rather than relying on a single check.

#### 6.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for file existence paths (`/Applications/Cydia.app`, `/private/var/lib/apt`), sandbox write attempts, and dyld dynamic library iterations.
- **Rejection Risks:** Executing high-security apps on jailbroken environments without proper degradation or warning violates OWASP MASVS compliance and risks account integrity.
- **Recommendations:**
  - Combine multiple detection routines: path checking, attempting to write outside the sandbox directory, symlink integrity checking, and checking for loaded dynamic libraries (like MobileSubstrate).
  - Clear all localized tokens and cache databases immediately upon detecting device compromise.
  - Gracefully degrade or safely terminate the application to prevent exploitation.

---

### 7. Root Detection (Android)

#### 7.1 Technical Mechanics
- Rooted Android devices allow superuser access, letting malicious tools hook runtime methods, bypass sandbox constraints, and extract files.
- Local heuristic root checks are easily bypassed by advanced rooting masking frameworks (such as Magisk or Zygisk).

#### 7.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `/system/bin/su`, `"test-keys"` ROM tags, superuser packages, and the Google Play Integrity API.
- **Rejection Risks:** Inadequate root detection in financial or data-sensitive apps exposes them to credential cloning, violating Google Play's Device and Network Abuse policies.
- **Recommendations:**
  - Use local heuristic checks (binary search, package checking, Build.TAGS verification) for basic defense.
  - Implement the hardware-backed **Google Play Integrity API**. Call the API from the client and verify the signed integrity verdict securely on the backend server.
  - Block high-risk operations (such as offline credential caching) if the integrity verdict indicates a compromised device.

---

### 8. SSL Configuration

#### 8.1 Technical Mechanics
- Modern mobile platforms enforce secure connections by default. Disabling secure network protections or allowing cleartext traffic exposes apps to transport-level data harvesting.

#### 8.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `NSAllowsArbitraryLoads` in plist files, and `usesCleartextTraffic` or `cleartextTrafficPermitted` in Android configurations.
- **Rejection Risks:** Allowing arbitrary cleartext HTTP traffic without documented, strict domain exceptions triggers automated rejections on both store pipelines.
- **Recommendations:**
  - Set `android:usesCleartextTraffic="false"` in the AndroidManifest or enforce cleartext constraints globally in `network_security_config.xml`.
  - Maintain App Transport Security (ATS) fully active on iOS. Never configure `NSAllowsArbitraryLoads` to true in production. Use domain-specific exceptions only if absolutely required and documented.
  - Enforce TLS 1.2 or TLS 1.3 as the minimum transport protocol version.

---

### 9. Backup Rules

#### 9.1 Technical Mechanics
- Automated OS backups (iCloud/iTunes on iOS, cloud/ADB backups on Android) copy local sandbox files. If credentials or local databases are stored without explicit exclusion rules, they leak to external cloud folders or local developer machines.

#### 9.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `isExcludedFromBackup` URL resource attributes on iOS, and `allowBackup` or `dataExtractionRules` in Android configurations.
- **Rejection Risks:** Backing up plain database configurations or plain preference files containing sensitive user identifiers violates basic data safety requirements.
- **Recommendations:**
  - For high-security applications, disable backups completely on Android via `android:allowBackup="false"`.
  - If backups are required, configure a comprehensive `data_extraction_rules.xml` file to explicitly exclude `sharedpref` and `database` domains.
  - On iOS, apply the `.isExcludedFromBackup = true` resource attribute to any local SQLite, SQLCipher, or cache files created in the application documents directory.

---

### 10. Exported Activities (Android Specific)

#### 10.1 Technical Mechanics
- Android activities, services, or receivers declared in `AndroidManifest.xml` with `android:exported="true"` are accessible to all other applications on the device.
- Unintentionally exported components allow malicious apps to launch internal views or bypass authorization flows.

#### 10.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `android:exported="true"` in AndroidManifest.xml files.
- **Rejection Risks:** Exposing core internal activities to the system violates Google's security rules and can act as an injection vector for system-wide privilege exploits.
- **Recommendations:**
  - Enforce a strict default of `android:exported="false"` for all internal activities.
  - Under Android 12+, components with intent filters must explicitly declare their exported status; ensure this is handled correctly.
  - For components that must be exported (e.g., launchers or deep-link handlers), protect them with custom signature-level permissions (`android:protectionLevel="signature"`) to ensure only your apps can launch them.

---

### 11. Intent Filters (Android Specific)

#### 11.1 Technical Mechanics
- Intent filters declare which implicit intents an application component responds to. Adding intent filters automatically exports the component on legacy API levels, creating implicit security boundaries.

#### 11.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `intent-filter` elements, `getCallingPackage()`, and `getCallingActivity()`.
- **Rejection Risks:** Implicit components can be spoofed or hijacked by other applications on the device if no verification of the caller is performed.
- **Recommendations:**
  - Always utilize explicit class intents when launching internal activities to guarantee compile-time and runtime target verification.
  - If an exported intent filter must be used, verify the caller's package identity via `getCallingPackage()` and cross-reference its certificate fingerprint against trusted values.
  - Apply custom signature-level permissions to protect custom broadcast receivers and services.

---

### 12. Deep Links

#### 12.1 Technical Mechanics
- Custom URL schemes (e.g., `myapp://action`) are inherently insecure because any application on the device can register the exact same scheme. If multiple apps register a scheme, the operating system's routing behavior is undefined, leading to custom scheme hijacking.

#### 12.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for custom scheme declarations under `CFBundleURLSchemes` or `android:scheme` without matching secure domain verification markers.
- **Rejection Risks:** Transmitting sensitive credentials, verification tokens, or direct session states over custom URL schemes is a critical security vulnerability and violates store security rules.
- **Recommendations:**
  - Treat all parameters parsed from incoming deep links as untrusted external inputs. Implement rigorous input sanitization and verification.
  - Never transmit authentication tokens, passwords, or session IDs within deep link parameters.
  - Restrict custom URL schemes to basic marketing routing and migrate all core application navigation to secure, domain-validated links.

---

### 13. Universal Links (iOS Specific)

#### 13.1 Technical Mechanics
- Universal Links use standard HTTPS connections. Because they require domain validation via an `apple-app-site-association` (AASA) file hosted on the target domain, they cannot be hijacked or duplicated by other applications.

#### 13.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for the `apple-app-site-association` file reference and associated domain entitlements (`applinks:`).
- **Rejection Risks:** Custom scheme fallbacks that transmit sensitive data trigger severe review warnings and potential rejections under Apple Guideline 5.1.1.
- **Recommendations:**
  - Publish a valid, minified AASA file in JSON format under the `.well-known` directory of your web server (`https://yourdomain.com/.well-known/apple-app-site-association`).
  - Serve the AASA file with `Content-Type: application/json` and ensure it is delivered over valid, secure HTTPS without redirects.
  - Enable the Associated Domains capability in the iOS app configuration and verify that the target domain matches the bundle identifier.

---

### 14. App Links (Android Specific)

#### 14.1 Technical Mechanics
- Android App Links are HTTPS links verified against a hosted Digital Asset Links JSON file. This allows the app to handle web URLs directly, avoiding the user disambiguation prompt.

#### 14.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `assetlinks.json` and intent filters with `android:autoVerify="true"`.
- **Rejection Risks:** Failing to configure secure verification triggers user choice prompts, opening the door for spoofing or parameter injection.
- **Recommendations:**
  - Include `android:autoVerify="true"` on any web-based intent-filter in `AndroidManifest.xml` to force installation-time verification.
  - Publish the Digital Asset Links JSON file at `https://yourdomain.com/.well-known/assetlinks.json` containing the application package name and the SHA-256 certificate fingerprints of your production signing key.
  - Gracefully degrade routing if the domain verification fails.

---

### 15. Authentication Flows

#### 15.1 Technical Mechanics
- Standard mobile authentication flows must handle credentials securely and prevent local storage of secrets. Hardcoding client secrets inside mobile binaries is a critical vulnerability because binaries can be easily decompiled.

#### 15.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `ASWebAuthenticationSession`, `CustomTabs`, and references to PKCE (Proof Key for Code Exchange) or OAuth libraries.
- **Rejection Risks:** Hardcoded client secrets or utilizing insecure, embedded web view wrappers (e.g., plain `WebView` or `WKWebView`) for user login screens is a severe security violation that triggers automated store rejections.
- **Recommendations:**
  - Implement **OAuth 2.1 / OIDC with PKCE (RFC 7636)** for all authentication flows to eliminate the need for client secrets in the binary.
  - Perform user login transitions within a secure system browser window: `ASWebAuthenticationSession` on iOS and Android `CustomTabs`.
  - Validate State and Nonce parameters on the client and server to prevent replay or cross-site request forgery attacks.

---

### 16. Session Handling

#### 16.1 Technical Mechanics
- Session tokens must have secure, well-defined lifecycles. Relying purely on client-side state is insecure; the backend must maintain ultimate authority over session validity.
- Sensitive information displayed on screens must be shielded from system multitasking snapshot mechanisms.

#### 16.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for background notifications, logout functions, and window blurring code.
- **Rejection Risks:** Retaining active session configurations after a logout request or leaving sensitive user information visible in the multitasking viewer violates user privacy and store policies.
- **Recommendations:**
  - Enforce server-side session invalidation immediately upon receiving a logout request.
  - Clear all local secure storage cache, keychain tokens, and cookies on logout.
  - Prevent data leakage by blurring the application multitasking screen snapshot. On iOS, add a blurring overlay view inside the `applicationWillResignActive` delegate. On Android, set `WindowManager.LayoutParams.FLAG_SECURE` in secure activities:
    ```kotlin
    window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)
    ```

---

### 17. Token Storage

#### 17.1 Technical Mechanics
- Authentication and authorization tokens (Access Tokens, Refresh Tokens) are target-rich assets.
- If tokens leak, attackers gain immediate account control. They must never be written to plaintext storage or standard logging outputs.

#### 17.2 Audit Methodology & Repository Status
- **Detection Signals:** Scans for `accessToken`, `refreshToken`, and logging frameworks (`Log.d`, `NSLog`, `print`) processing these variables.
- **Rejection Risks:** Exposing active token sets in device log buffers or unencrypted caches violates standard OWASP MASVS rules and store data safety guidelines.
- **Recommendations:**
  - Store tokens strictly inside the **iOS Keychain** or **Android EncryptedSharedPreferences**.
  - Keep access tokens short-lived (e.g., 15 minutes) and require a secure, long-lived refresh token stored with strict access constraints (such as `ThisDeviceOnly` or requiring biometrics) to rotate access tokens.
  - Ensure that diagnostic loggers completely scrub authorization header values or token vectors before printing.

---

## Continuous Security Auditing and Verification

### 1. Pre-Submission Compliance Guard
The continuous security stance of this repository is protected by the pre-submission guard located at `agent-os/hooks/app-store-compliance-guard.sh`.
This script performs key security verifications:
- Scans files for unencrypted storage patterns (e.g., plain `getSharedPreferences`).
- Audits network files for cleartext traffic permission or insecure SSL exceptions.
- Verifies that sensitive native permissions match valid, non-vague purpose strings in `Info.plist` and `AndroidManifest.xml`.
- Checks for active, overdue, or approaching regulatory deadlines.

### 2. Integration & Release Auditing
Before any production release is authorized, developers must execute the automated release audit:
```bash
python3 scripts/release-audit.py
```
This runs validation checks, scans for metadata deviations, and updates the release readiness report. High-priority or critical violations block the publishing pipeline, guaranteeing that no insecure build is uploaded to App Store Connect or Google Play Console.
