# Mobile Security Compliance Audit and Best Practices Review (2026)

This document provides a comprehensive compliance audit and best practices review covering seventeen critical mobile security domains. It outlines iOS and Android platform-specific security mechanics, risks, and recommendations aligned with modern security frameworks (such as OWASP MASVS).

---

## 1. Secure Storage

### 1.1 Description & Compliance Risk
Storing sensitive data (such as access tokens, personally identifiable information, session keys, and database passwords) in plaintext within the application sandbox is a critical security vulnerability. On jailbroken/rooted devices, or via backup extraction, standard files like iOS `UserDefaults` plists or Android standard `SharedPreferences` XML files can be read directly by unauthorized parties or malware.

### 1.2 Platform-Specific Mechanics
- **iOS**: Standard sandboxed files are readable if the device is compromised. Apple provides Keychain Services and Data Protection APIs. Larger local databases (SQLite or CoreData) are vulnerable to cold boot attacks unless encrypted.
- **Android**: Default sandbox files under `/data/data/<package>/` are protected by Unix permissions but accessible to root users. The Jetpack Security library offers wrappers for encrypting SharedPreferences and raw files.

### 1.3 Best Practices & Recommendations
- **For Small Assets**: Utilize platform-specific secure enclaves. Use iOS Keychain Services and Android EncryptedSharedPreferences (AES-256-SIV).
- **For Large Databases**: Encrypt local SQLite/Room databases using SQLCipher with a hardware-backed master key generated dynamically.
- **For File Protection**: Use `Data.WritingOptions.completeFileProtection` on iOS to ensure files are encrypted on disk when the device is locked, and use `EncryptedFile` from Jetpack Security on Android.

---

## 2. Keychain (iOS Specific)

### 2.1 Description & Compliance Risk
The iOS Keychain provides a secure container for storing small pieces of sensitive data. Storing keys with weak accessibility settings can expose data during background processing or allow migration across unauthorized devices during cloud backup restorations.

### 2.2 Platform-Specific Mechanics
- **Accessibility Attributes**: Controlled via `kSecAttrAccessible`. Some settings allow the data to be accessible even when locked, or allow the data to migrate via iCloud/iTunes backups to secondary physical hardware.
- **Access Group Sharing**: Controlled by the `kSecAttrAccessGroup` attribute, which shares credentials across applications with the same App Group entitlement.

### 2.3 Best Practices & Recommendations
- Always declare strict accessibility classes. Use `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` for background operations or `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for foreground-only apps.
- Prevent migration across devices during cloud backups by using `ThisDeviceOnly` protection attributes.
- Set `kSecAttrSynchronizable` to `false` unless explicit iCloud Keychain synchronization is required.
- Isolate group-shared items strictly using verified App Groups under the same provisioning profiles.

---

## 3. Android Keystore (Android Specific)

### 3.1 Description & Compliance Risk
The Android Keystore system protects cryptographic keys, preventing their extraction from the device's RAM or storage. Failing to enforce hardware backing means cryptographic keys are stored in software, making them vulnerable to extraction if the operating system kernel is compromised.

### 3.2 Platform-Specific Mechanics
- **TEE (Trusted Execution Environment)**: A secure area of the main processor that runs isolated from the standard Android OS.
- **StrongBox**: A dedicated hardware security module (HSM) chip introduced in Android 9 (API 28) providing physical tampering resistance.
- **KeyGenParameterSpec**: Defines the cryptographic parameters and constraints under which the key is generated and used.

### 3.3 Best Practices & Recommendations
- Enforce hardware-backed key generation by specifying `setIsStrongBoxBacked(true)` when initializing keys on supported hardware.
- Programmatically verify that keys are hardware-isolated by checking `KeyInfo.isInsideSecureHardware()`.
- Explicitly restrict key authorization purposes (e.g., limit to `PURPOSE_ENCRYPT` and `PURPOSE_DECRYPT` only, and disable insecure padding/block modes).
- Require user authentication for high-value key operations using `.setUserAuthenticationRequired(true)` with a non-zero timeout or biometric prompt association.

---

## 4. Biometric Authentication

### 4.1 Description & Compliance Risk
Biometric authentication (such as Face ID, Touch ID, or Android BiometricPrompt) must securely authenticate the user. A common anti-pattern is implementing biometric prompts as a simple UI overlay that returns a boolean success value. Attackers can bypass this return value at runtime using instrumentation tools like Frida.

### 4.2 Platform-Specific Mechanics
- **iOS**: `LAContext` handles local authentication but is vulnerable to runtime return-value hooking if used in isolation.
- **Android**: `BiometricPrompt` can operate in credential-free mode or wrapped with a cryptographic object.

### 4.3 Best Practices & Recommendations
- **Crypto-Backed Biometrics**: Tie biometric verification directly to a cryptographic operation.
- **On iOS**: Save the sensitive target token in the Keychain, protected with `SecAccessControl` constraints that require biometric authentication (`.biometryAny` or `.biometryCurrentSet`) to decrypt. The OS will release the token only upon a successful biometric match.
- **On Android**: Generate a Keystore key requiring biometric authorization, and wrap it inside a `BiometricPrompt.CryptoObject` (using a Cipher or Signature) passed directly to `biometricPrompt.authenticate()`. The key is cryptographically unusable unless authorized by the secure biometric processor.

---

## 5. Certificate Pinning

### 5.1 Description & Compliance Risk
Certificate pinning mitigates Man-in-the-Middle (MITM) attacks by restricting acceptable connection targets to servers presenting specific, trusted cryptographic keys. Relying solely on default OS trust anchors leaves the app vulnerable if a malicious CA certificate is installed on the user's device (e.g., via enterprise MDMs or proxy utilities).

### 5.2 Platform-Specific Mechanics
- **iOS NSPinnedDomains**: A declarative native pinning mechanism configured in `Info.plist` since iOS 14.
- **Android Network Security Configuration**: A declarative XML-based configuration (`res/xml/network_security_config.xml`) enforced natively by the system networking stack.

### 5.3 Best Practices & Recommendations
- Pin the **Subject Public Key Info (SPKI)** hash rather than the leaf certificate itself. This avoids application outages during routine leaf certificate rotations.
- Always include at least one backup/backup-standby SPKI pin from an independent Certificate Authority to prevent bricking the application during an emergency certificate migration.
- Utilize declarative native frameworks (`NSPinnedDomains` on iOS and `network_security_config.xml` on Android) to minimize human error in custom delegate socket validation code.

---

## 6. Jailbreak Detection (iOS)

### 6.1 Description & Compliance Risk
A jailbroken iOS device compromises standard kernel-level security guarantees, permitting sandbox escapes, custom library injections (using dyld), and memory scanning. Apps operating in highly sensitive areas (finance, identity, health) must detect and respond to device compromise.

### 6.2 Platform-Specific Mechanics
- **Sandbox Checks**: Checking directory write capabilities outside the standard app container.
- **File System Inspection**: Verifying the presence of jailbreak tools, directory layouts, and symlinks.
- **Dynamic Linker Inspection**: Looking for injected dylibs.

### 6.3 Best Practices & Recommendations
- Implement a multi-layered detection strategy:
  1. **File System Auditing**: Search for common jailbreak files and directories (e.g., `/Applications/Cydia.app`, `/private/var/lib/apt`).
  2. **Sandbox Violations**: Attempt to write to directories outside the sandboxed path (e.g., `/private/jailbreak.txt`).
  3. **Symlink Verification**: Verify that folders like `/Library/Ringtones` or `/Applications` are not symlinks.
  4. **Dynamic Library Verification**: Inspect the loaded dylibs list via `_dyld_get_image_name` to detect hooking runtimes.
- Upon positive detection, clean all local access tokens and databases, notify backend security monitors, and perform a graceful terminate or feature degradation.

---

## 7. Root Detection (Android)

### 7.1 Description & Compliance Risk
Android root access allows users and malicious apps to bypass Android's sandboxing mechanism, inspect application memory, and manipulate files. Basic local root detection heuristics are easily bypassed by masking tools like Magisk or Zygisk.

### 7.2 Platform-Specific Mechanics
- **Local Heuristics**: Scanning for binaries, packages, and system build signatures.
- **Hardware-Backed Attestation**: Google Play Integrity API provides cryptographically signed statements about the integrity of the device and environment.

### 7.3 Best Practices & Recommendations
- Combine basic local heuristic checks (such as searching for `su` binaries, `test-keys` in `Build.TAGS`, and superuser manager apps) with robust hardware attestation.
- Integrate the **Google Play Integrity API** (or hardware-backed SafetyNet fallback) as the primary root verification mechanism in production.
- Send the signed attestation token directly to a secure backend server for decryption and cryptographic verification. Never perform the validation logic entirely on the client.

---

## 8. SSL Configuration

### 8.1 Description & Compliance Risk
Improper SSL/TLS configurations can allow cleartext (HTTP) traffic or weak cipher usage, exposing application APIs to sniffing, credentials theft, and MITM interception.

### 8.2 Platform-Specific Mechanics
- **iOS App Transport Security (ATS)**: Enforces HTTPS connections by default.
- **Android Cleartext Traffic Policy**: Configured in `AndroidManifest.xml` or XML network configs.

### 8.3 Best Practices & Recommendations
- Completely disable cleartext HTTP traffic globally.
  - On iOS: Keep App Transport Security active. Avoid setting `NSAllowsArbitraryLoads` to `true`.
  - On Android: Set `android:usesCleartextTraffic="false"` in the application manifest, or enforce `cleartextTrafficPermitted="false"` inside the network security configuration file.
- Enforce TLS 1.2 or TLS 1.3 as the absolute minimum communication standard, disabling older, vulnerable protocols (such as TLS 1.0, TLS 1.1, and SSL v3).

---

## 9. Backup Rules

### 9.1 Description & Compliance Risk
By default, standard system backup systems (iCloud/iTunes on iOS, ADB/Google Drive backups on Android) copy local sandbox databases, preferences, and files. If private keys or session tokens are stored insecurely in the sandboxed folder, they are written to cloud storage or can be extracted via physical USB interfaces.

### 9.2 Platform-Specific Mechanics
- **iOS iCloud Backups**: Backs up standard application directories unless files are marked for exclusion.
- **Android Auto Backup**: ADB-based file extraction commands can pull raw files unless `allowBackup` is disabled or configured with precise filters.

### 9.3 Best Practices & Recommendations
- **On iOS**: Exclude sensitive database files, preferences, and localized caches from iCloud and iTunes backups by programmatically setting the `.isExcludedFromBackup` URL resource attribute on the target files.
- **On Android**: Set `android:allowBackup="false"` in the application manifest for high-security applications.
- If backup is required, configure strict `android:dataExtractionRules` (for Android 12+) and `android:fullBackupContent` rules to explicitly exclude folders containing credentials, token databases, and secure caches.

---

## 10. Exported Activities (Android Specific)

### 10.1 Description & Compliance Risk
Exported activities in Android can be launched by any other application on the device. An exported activity that handles sensitive state or processes intent data without validation can lead to intent injection, authorization bypass, and tapjacking.

### 10.2 Platform-Specific Mechanics
- **android:exported**: A manifest attribute that defines whether an application component can be launched by other apps.
- **Android 12 Restrictions**: Enforces explicit declaration of `android:exported` on any component declaring an intent filter.

### 10.3 Best Practices & Recommendations
- Enforce a strict "closed-by-default" policy. Set `android:exported="false"` for all internal activities, services, and receivers.
- If an activity must be exported, protect it with custom signature-level permissions (`android:protectionLevel="signature"`), ensuring only applications signed with your exact developer certificate can launch it.
- Thoroughly validate, sanitize, and authorize all parameters received within any exported component before executing business actions.

---

## 11. Intent Filters (Android Specific)

### 11.1 Description & Compliance Risk
Declaring an intent filter on a component automatically exports it, exposing it to external apps. Malicious applications can exploit this to intercept implicit intents, spoof transitions, or hijack communication channels.

### 11.2 Platform-Specific Mechanics
- **Implicit Intents**: Intents that specify an action without defining a target class.
- **Explicit Intents**: Intents that define the exact package name or class to resolve.

### 11.3 Best Practices & Recommendations
- Never use implicit intents for internal communication. Always use explicit class-based intents when launching components or starting services inside your own application package boundaries.
- Inspect and restrict exported intent receivers by validating the sender's identity using `getCallingActivity()` or `getCallingPackage()`, verifying their package signing certificate.
- Enforce custom signature permissions on the receiver manifest tags if communication is limited to an approved family of apps.

---

## 12. Deep Links

### 12.1 Description & Compliance Risk
Deep links invoke specific routes inside the application from external sources. Custom URL schemes (e.g., `myapp://login`) are insecure and can be registered by any other application, enabling deep-link hijacking, parameter manipulation, and authorization bypasses.

### 12.2 Platform-Specific Mechanics
- **URL Schemes**: Global custom handlers registered on the OS level.
- **Input Sanitization**: Processing external parameters before parsing.

### 12.3 Best Practices & Recommendations
- Treat all incoming deep links as untrusted input. Validate, sanitize, and escape all URL parameters before routing or rendering inside WebViews to prevent SQL injection, path traversals, or cross-site scripting (XSS).
- Never transmit sensitive credentials, access tokens, or personal identifiers inside deep link URLs.
- For authentication-oriented deep links (such as email magic links), pass a one-time, cryptographically strong challenge token that must be exchanged via a secure, explicit backchannel HTTPS request.

---

## 13. Universal Links (iOS Specific)

### 13.1 Description & Compliance Risk
Universal Links bind an iOS application to a verified web domain using HTTPS. If a website does not publish a verified association file, malicious apps can register matching custom protocols to capture user transitions and intercept secure flows.

### 13.2 Platform-Specific Mechanics
- **apple-app-site-association (AASA)**: A JSON file hosted at the root domain that specifies the allowed application bundle identifiers.
- **Associated Domains Entitlement**: The iOS capability that defines authorized domains.

### 13.3 Best Practices & Recommendations
- Adopt Universal Links for all external linking and routing requirements, avoiding insecure custom URL schemes.
- Host a valid `apple-app-site-association` file inside the `.well-known/` directory at the target HTTPS domain. Ensure the file is served with the `application/json` content-type, without HTTP redirects, and contains the correct Team ID and App Bundle ID.
- Enable the "Associated Domains" capability in Xcode, registering the exact matching hostnames.

---

## 14. App Links (Android Specific)

### 14.1 Description & Compliance Risk
Android App Links bypass the platform disambiguation dialog by establishing verified ownership of a web domain. Without proper domain association, users may be prompted to choose from a list of apps, allowing custom scheme hijackers to intercept the link.

### 14.2 Platform-Specific Mechanics
- **assetlinks.json**: The digital asset verification file hosted on the target domain.
- **android:autoVerify**: Manifest flag instructing Android to perform cryptographic domain checks on installation.

### 14.3 Best Practices & Recommendations
- Securely configure Android App Links by specifying `android:autoVerify="true"` within the intent filters of `AndroidManifest.xml`.
- Host a valid, digitally signed `assetlinks.json` file inside the `.well-known/` directory at the host HTTPS domain.
- The `assetlinks.json` file must contain the exact SHA-256 certificate fingerprint of the production application signing certificate.

---

## 15. Authentication Flows

### 15.1 Description & Compliance Risk
Authentication flows handle the transmission and storage of critical credentials. Hardcoding client secrets inside mobile binaries is a severe risk, as any user or attacker can extract them via static reverse engineering. Additionally, using insecure browsers allows credential sniffing.

### 15.2 Platform-Specific Mechanics
- **Proof Key for Code Exchange (PKCE)**: Dynamic cryptographic challenges that secure authorization code exchanges on public clients.
- **Secure Web Components**: Native browser sessions that isolate credentials from the host app container.

### 15.3 Best Practices & Recommendations
- Enforce the OAuth 2.1 / OpenID Connect standard using Proof Key for Code Exchange (PKCE, RFC 7636). Do not store static client secrets inside mobile codebases.
- Do not utilize embedded WebViews (`WKWebView` on iOS or standard Android `WebView`) for login screens. These components allow the parent application to intercept keystrokes, sessions, and credentials.
- Always execute authentication flows using native, isolated browser sessions such as `ASWebAuthenticationSession` on iOS and Android **Custom Tabs**.

---

## 16. Session Handling

### 16.1 Description & Compliance Risk
Insecure session handling can leave user credentials active on the client after logout, or leak sensitive screen contents to multitasking system snapshots, violating strict data protection laws.

### 16.2 Platform-Specific Mechanics
- **Server-Side Verification**: Active validation of tokens on the host.
- **Multitasking Snapshotting**: The OS takes a screenshot of the app when backgrounded to show in the app switcher.

### 16.3 Best Practices & Recommendations
- Do not make offline assumptions regarding session validity. Perform active token verification on the server-side for all sensitive transactions.
- Implement server-side session invalidation immediately upon user logout, and simultaneously purge all local access/refresh tokens, localized database keys, cookies, and secure caches.
- Protect user privacy in public areas by applying a blur filter or splash overlay to the application window during background transitions to prevent sensitive user data from being visible in system multitasking switcher snapshots.

---

## 17. Token Storage

### 17.1 Description & Compliance Risk
Tokens (such as access tokens, refresh tokens, and JWTs) represent the active authorization state of the user. Writing tokens to public loggers, unsecured caches, or plaintext storage allows attackers to compromise account custody.

### 17.2 Platform-Specific Mechanics
- **Encrypted Storage Vaults**: Storing tokens inside hardware-protected compartments.
- **Logging Policies**: Preventing sensitive tokens from leaking to diagnostic stdout/stderr.

### 17.3 Best Practices & Recommendations
- Store all active session tokens strictly inside the **iOS Keychain** or **Android EncryptedSharedPreferences** / hardware-backed Keystore containers.
- Enforce short expiration limits on access tokens (e.g., 15 minutes) and implement secure refresh token rotation to minimize the impact of a leaked credential.
- Strictly audit codebase logging mechanisms (`print`, `NSLog`, `Log.d`, custom logger suites) to guarantee that session tokens, cryptographic vectors, and secret payloads are never outputted to device diagnostics or diagnostic logs.
