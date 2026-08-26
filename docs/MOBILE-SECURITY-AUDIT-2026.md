# Mobile Security Requirements Compliance Audit and Best Practices Review (2026)

This compliance audit and best practices review provides an exhaustive evaluation of mobile security requirements across both iOS and Android platforms. It establishes platform-specific technical standards, threat analyses, and actionable remediation guidelines for all 17 critical mobile security domains required to satisfy App Store and Google Play review policies, OWASP Mobile Application Security Verification Standards (MASVS), and global privacy/security mandates.

---

## Executive Summary and Audit Scope

Modern mobile applications operate under strict security and regulatory requirements. Insecure credential storage, improper link handling, or missing binary protections can lead to account takeover, data exfiltration, regulatory penalties, and store rejection.

This audit evaluates the repository and establishes implementation standards across 17 core domains:

1. Secure Storage
2. Keychain (iOS)
3. Android Keystore
4. Biometric Authentication
5. Certificate Pinning
6. Jailbreak Detection (iOS)
7. Root Detection (Android)
8. SSL Configuration
9. Backup Rules
10. Exported Activities (Android)
11. Intent Filters (Android)
12. Deep Links
13. Universal Links (iOS)
14. App Links (Android)
15. Authentication Flows
16. Session Handling
17. Token Storage

---

## 1. Secure Storage

### 1.1 Overview and Threat Analysis
Plaintext storage of sensitive data (passwords, auth tokens, personally identifiable information, API keys) inside standard local storage mechanisms like `UserDefaults` on iOS or standard `SharedPreferences` on Android creates severe security vulnerabilities. On jailbroken/rooted devices, or through physical extraction and unencrypted device backups, attackers can access plaintext sandbox files.

### 1.2 Platform Implementation Best Practices

#### iOS Implementation
- Do not store credentials or tokens in `UserDefaults`, standard SQLite databases, or `Documents`/`Library` directories without hardware-backed encryption.
- Use the **Keychain Services API** for small sensitive items such as session tokens and keys.
- For structured or relational databases, implement **SQLCipher** for SQLite or CoreData encryption.
- Apply iOS Data Protection flags (`Data.WritingOptions.completeFileProtection`) when storing sensitive application files directly to disk, ensuring content is encrypted on disk whenever the device is locked.

#### Android Implementation
- Replace standard `SharedPreferences` with **EncryptedSharedPreferences** from the Jetpack Security library.
- For file storage, use **EncryptedFile** using AES-256 GCM encryption.
- Encrypt SQLite or Room databases using **SQLCipher for Android**, referencing a master key managed inside the hardware-backed Android Keystore.

---

## 2. Keychain (iOS Specific)

### 2.1 Overview and Threat Analysis
The iOS Keychain provides a secure hardware-accelerated enclave managed by the OS to store small cryptographic items and credentials isolated from other applications. Improper accessibility attribute configuration can expose items across device restores or background sync.

### 2.2 Platform Implementation Best Practices
- Explicitly configure `kSecAttrAccessible` protection attributes when storing Keychain items:
  - `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`: Recommended for background synchronization tasks or push handlers. Data is accessible after first unlock and is never migrated to new devices via backups.
  - `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`: Recommended for foreground-only application credentials. Data is inaccessible when device is locked and excluded from backups.
- Never use deprecated attributes such as `kSecAttrAccessibleAlways`.
- Limit Keychain Sharing via `kSecAttrAccessGroup` to explicit, entitlement-verified app suites under the same developer team.
- Ensure `kSecAttrSynchronizable` is set to `false` unless explicit iCloud Keychain sync across user devices is intended.

---

## 3. Android Keystore (Android Specific)

### 3.1 Overview and Threat Analysis
The Android Keystore system lets applications generate and store cryptographic keys inside a hardware-backed container (Trusted Execution Environment or StrongBox HSM), preventing key extraction even if the application process or Android OS is compromised.

### 3.2 Platform Implementation Best Practices
- Enforce hardware protection during key generation via `KeyGenParameterSpec.Builder`.
- Check `KeyInfo.isInsideSecureHardware()` after generating keys to verify hardware backing.
- On Android 9 (API 28) and higher devices, enable `setIsStrongBoxBacked(true)` to enforce key isolation in a dedicated hardware security module chip.
- Implement **Key Attestation** for backend verification, validating the leaf certificate chain against Google's root certificate to mathematically confirm key creation inside secure hardware.

---

## 4. Biometric Authentication

### 4.1 Overview and Threat Analysis
Biometric authentication (Face ID, Touch ID, BiometricPrompt) replaces passcode entry for user convenience. However, local boolean checks (`evaluatedPolicy` success) can be bypassed via dynamic instrumentation tools like Frida. Biometrics must be backed by cryptographic proof.

### 4.2 Platform Implementation Best Practices

#### iOS Implementation
- Use `LAContext` for local authentication prompts, but do not rely solely on boolean returns for authorization.
- Protect Keychain items using `SecAccessControlCreateWithFlags` configured with `.biometryCurrentSet`. The Keychain item can only be decrypted when valid biometric authentication occurs.
- If biometrics are re-enrolled or changed, `.biometryCurrentSet` automatically invalidates the secret key, preventing unauthorized access from newly enrolled biometrics.

#### Android Implementation
- Use **BiometricPrompt** from the androidx.biometric library.
- Bind key usage to biometric authentication using `setInvalidatedByBiometricEnrollment(true)` and `setUserAuthenticationRequired(true)`.
- Pass a initialized `BiometricPrompt.CryptoObject` (wrapping a `Cipher` or `Signature`) to `BiometricPrompt.authenticate()`. Unlocking the key occurs only upon verified biometric authentication.

---

## 5. Certificate Pinning

### 5.1 Overview and Threat Analysis
Certificate pinning guards against Man-in-the-Middle (MitM) attacks caused by compromised Root Certificate Authorities (CAs) or malicious network proxies installed on the client device.

### 5.2 Platform Implementation Best Practices
- Pin to the **Subject Public Key Info (SPKI)** hash rather than the leaf X.509 certificate file. SPKI pinning survives standard certificate renewals while preserving security.
- Always include fallback backup pins (at least two distinct SPKI hashes) to prevent application outage when rotation occurs.

#### iOS Implementation
- Implement `URLSessionDelegate` using `urlSession(_:didReceive:completionHandler:)` to inspect server trust objects (`SecTrust`) and match public key SHA-256 hashes.

#### Android Implementation
- Configure pinning declaratively in `res/xml/network_security_config.xml`:
  ```xml
  <network-security-config>
      <domain-config cleartextTrafficPermitted="false">
          <domain includeSubdomains="true">api.yourdomain.com</domain>
          <pin-set expiration="2027-12-31">
              <pin digest="SHA-256">primary_spki_hash_base64</pin>
              <pin digest="SHA-256">backup_spki_hash_base64</pin>
          </pin-set>
      </domain-config>
  </network-security-config>
  ```

---

## 6. Jailbreak Detection (iOS)

### 6.1 Overview and Threat Analysis
Jailbroken iOS devices strip kernel protections, disable sandbox boundaries, and allow runtime hooking, memory inspection, and function interception.

### 6.2 Platform Implementation Best Practices
- Implement multi-layered defense-in-depth checks:
  - Check for existence of jailbreak files and package paths (`/Applications/Cydia.app`, `/Library/MobileSubstrate/MobileSubstrate.dylib`, `/usr/sbin/sshd`, `/etc/apt`).
  - Attempt sandbox write checks outside the app container (e.g., attempting to write to `/private/jailbreak.txt`).
  - Check for dynamic linker library injections by scanning loaded `dyld` images for known hooking frameworks (Frida, Cycript, Substrate).
- Execute checks at randomized intervals during execution rather than solely at startup.
- Send anti-tamper telemetry to server backends to terminate sensitive active sessions.

---

## 7. Root Detection (Android)

### 7.1 Overview and Threat Analysis
Rooted Android devices grant elevated privileges (su binary access), allowing memory dumping, hook injection via Xposed or Frida, and manipulation of application state.

### 7.2 Platform Implementation Best Practices
- Combine local heuristic checks with remote attestation:
  - Check for the existence of `su` binaries across common system paths (`/system/bin/su`, `/system/xbin/su`, `/sbin/su`, `/data/local/x/su`).
  - Check for root management packages (Magisk, SuperSU).
  - Inspect `Build.TAGS` for `test-keys` indicating custom or unofficial ROM builds.
- Mandate **Play Integrity API** attestation in production builds. Request an integrity token from the Play Integrity API and verify `appRecognitionVerdict`, `deviceRecognitionVerdict` (`MEETS_DEVICE_INTEGRITY`), and `environmentDetails` on your backend server.

---

## 8. SSL Configuration

### 8.1 Overview and Threat Analysis
Unencrypted HTTP cleartext traffic allows network eavesdropping, credential hijacking, and payload injection. Modern mobile platforms require explicit network transport security.

### 8.2 Platform Implementation Best Practices
- Enforce TLS 1.3 as the default network protocol, with TLS 1.2 as absolute minimum. Disable weak cipher suites and SSLv3/TLS 1.0/1.1.

#### iOS Implementation
- Retain strict **App Transport Security (ATS)** rules in `Info.plist`. Do not set `NSAllowsArbitraryLoads` to `true`.
- Specify explicit exception domains (`NSExceptionDomains`) with strict security keys if legacy subdomains require temporary exceptions.

#### Android Implementation
- Disable cleartext traffic globally in `AndroidManifest.xml` via `android:usesCleartextTraffic="false"`.
- Configure `res/xml/network_security_config.xml` with `<base-config cleartextTrafficPermitted="false">`.

---

## 9. Backup Rules

### 9.1 Overview and Threat Analysis
Default operating system backup settings may extract private application databases, shared preferences, and cached session tokens to unencrypted desktop backups or cloud storage.

### 9.2 Platform Implementation Best Practices

#### iOS Implementation
- Exclude sensitive databases or cached content files from iCloud and iTunes backups by setting the `.isExcludedFromBackup` URL resource flag:
  ```swift
  var url = URL(fileURLWithPath: filePath)
  var values = URLResourceValues()
  values.isExcludedFromBackup = true
  try url.setResourceValues(values)
  ```

#### Android Implementation
- For high-security applications, disable application backup completely in `AndroidManifest.xml`:
  ```xml
  <application android:allowBackup="false" ...>
  ```
- If backups are required, configure `android:dataExtractionRules` (Android 12+) and `android:fullBackupContent` (Android 11 and lower) to explicitly exclude database files, shared preferences containing tokens, and key files.

---

## 10. Exported Activities (Android Specific)

### 10.1 Overview and Threat Analysis
Activities declared in `AndroidManifest.xml` with `android:exported="true"` can be launched by any external app on the device, exposing internal workflows and bypassing authentication screens.

### 10.2 Platform Implementation Best Practices
- Set `android:exported="false"` by default for all internal activities, services, and broadcast receivers.
- Comply with Android 12+ requirements mandating explicit `android:exported` declaration for every component containing intent filters.
- If an activity must be exported, enforce custom permissions with `android:protectionLevel="signature"`, guaranteeing that only apps signed with your developer key can invoke the activity.

---

## 11. Intent Filters (Android Specific)

### 11.1 Overview and Threat Analysis
Intent filters expose application components to implicit intents. Attackers can craft malicious implicit intents to intercept data, trigger unauthorized actions, or hijack responses.

### 11.2 Platform Implementation Best Practices
- Validate incoming intent caller identity using `getCallingActivity()` or `getCallingPackage()` before processing intent extras.
- Use explicit intents (specifying exact class and package names) when launching internal application components.
- Avoid broadcasting sensitive data via implicit broadcast intents; use `LocalBroadcastManager` or explicit broadcast targets.

---

## 12. Deep Links

### 12.1 Overview and Threat Analysis
Custom URL schemes (e.g., `myapp://route`) do not provide domain ownership verification. Malicious applications installed on the same device can register identical schemes and hijack links, stealing payload data or spoofing screens.

### 12.2 Platform Implementation Best Practices
- Never transmit sensitive credentials, auth tokens, or personal identifiers inside deep link URLs.
- Treat all incoming deep link parameters as untrusted inputs; sanitize and validate parameters before parsing.
- For deep link authentication, send short-lived single-use verification tokens that are validated via encrypted HTTPS API requests.

---

## 13. Universal Links (iOS Specific)

### 13.1 Overview and Threat Analysis
Universal Links bind standard HTTPS domain URLs to iOS applications using domain association verification, preventing link hijacking by third-party apps.

### 13.2 Platform Implementation Best Practices
- Host a valid Apple App Site Association (AASA) file at `https://yourdomain.com/.well-known/apple-app-site-association`.
- Serve the AASA file with `Content-Type: application/json` over HTTPS without redirects.
- Configure Xcode Associated Domains capability with `applinks:yourdomain.com`.
- Handle incoming links safely inside `application(_:continue:restorationHandler:)` with thorough path validation.

---

## 14. App Links (Android Specific)

### 14.1 Overview and Threat Analysis
Android App Links use Digital Asset Links verification to verify domain ownership and route HTTPS URLs directly to your application without opening the system selection dialog.

### 14.2 Platform Implementation Best Practices
- Host the Digital Asset Links JSON file at `https://yourdomain.com/.well-known/assetlinks.json`.
- Include matching package name and official SHA-256 signing certificate fingerprints.
- Add `android:autoVerify="true"` to intent filters in `AndroidManifest.xml` so the Android system automatically validates domain association upon app installation.

---

## 15. Authentication Flows

### 15.1 Overview and Threat Analysis
Insecure mobile auth flows expose client secrets or enable authorization code interception attacks during OAuth handshakes.

### 15.2 Platform Implementation Best Practices
- Mandate **OAuth 2.1 / OIDC with PKCE (Proof Key for Code Exchange)** (RFC 7636). PKCE eliminates the need for embedded client secrets in mobile binaries and guards against code interception.
- Conduct authentication in system browsers using `ASWebAuthenticationSession` on iOS and **Custom Tabs** on Android.
- Never use embedded web views (`WKWebView` or Android `WebView`) for login screens, as they allow host apps to intercept entered credentials.

---

## 16. Session Handling

### 16.1 Overview and Threat Analysis
Improper session management leaves active sessions vulnerable to token replay, session fixed state exploitation, or privacy leaks when app snapshots are captured in task switchers.

### 16.2 Platform Implementation Best Practices
- Perform server-side validation on every sensitive API request; local client authorization checks are insufficient.
- Implement app background privacy protection: blur or cover application UI windows upon backgrounding to prevent sensitive user data from being recorded in OS task switcher snapshots.
- On user logout, invoke server-side token revocation and clear all locally cached tokens, database keys, and Keychain/SharedPreferences items simultaneously.

---

## 17. Token Storage

### 17.1 Overview and Threat Analysis
Access tokens and long-lived refresh tokens grant access to user accounts. Storing tokens in plaintext files or logs leads to immediate identity exposure.

### 17.2 Platform Implementation Best Practices
- Store short-lived Access Tokens and long-lived Refresh Tokens exclusively in secure storage (**iOS Keychain** or **Android EncryptedSharedPreferences** / Keystore).
- Never log tokens to console output or file loggers (`Log.d`, `NSLog`, `print`).
- Implement Refresh Token rotation: issue a new Refresh Token upon every token refresh call and invalidate the previous Refresh Token server-side.
