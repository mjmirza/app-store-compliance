# Mobile Security Compliance Audit & Best Practices Report (2026)

## 1. Executive Summary
This document provides a highly technical, comprehensive compliance audit and security assessment of mobile applications (iOS and Android) across seventeen critical security domains. Grounded in the OWASP Mobile Application Security Verification Standard (MASVS) and platform-specific engineering guidelines from Apple and Google, this report outlines risks, system mechanics, secure implementation patterns, and actionable remediation tasks.

All recommendations are designed to prevent client-side credential harvesting, protect network communication integrity, secure platform boundaries, and ensure robust user account custody.

---

## 2. Comprehensive Security Review by Domain

### 2.1 Secure Storage
* **Assessment & Risks**:
  Storing sensitive data (such as session keys, personal identifier variables, access credentials, and database contents) in plaintext within standard sandbox files (e.g., standard `UserDefaults` or standard `SharedPreferences`) exposes data to local extraction. On rooted or jailbroken platforms, or through automated backup extraction mechanisms, these files can be easily retrieved and read.
* **Platform Mechanics**:
  - **iOS**: Apple's filesystem writes `UserDefaults` to standard XML plists inside the application container, which are unencrypted by default.
  - **Android**: Android stores standard `SharedPreferences` as XML files inside `/data/data/your.package/shared_prefs/`, accessible to any root user.
* **Remediation & Best Practices**:
  - **Key-Value Data**: Utilise the iOS Keychain Services API for small credentials and Google's Jetpack Security library `EncryptedSharedPreferences` on Android, which encrypts keys and values using AES-256-SIV.
  - **Database Encryption**: Enforce full database encryption using SQLCipher for Room, SQLite, or CoreData repositories.
  - **File Protection Class**: Use Apple's `.completeFileProtection` writing option when saving sensitive persistent documents directly to disk, ensuring they are encrypted when the device is locked.

### 2.2 Keychain (iOS)
* **Assessment & Risks**:
  The iOS Keychain is a secure hardware-accelerated repository. However, misconfiguring keychain accessibility options can lead to data exposure. For example, leaving credentials accessible when the device is locked, or allowing credential migration to other physical devices during automated iCloud/iTunes system backup restorations, presents major security risks.
* **Platform Mechanics**:
  Keychain Services utilize the Security framework to interact with the device's secure enclave and persistent keychains. Security flags govern keychain item visibility relative to device lock states.
* **Remediation & Best Practices**:
  - **Access Class Security**: Always enforce the strict `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` class for background-capable or push-notified tasks. For foreground-only apps, use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`.
  - **Avoid Insecure Flags**: Never use `kSecAttrAccessibleAlways` or classes lacking `ThisDeviceOnly` prefixes unless explicit migration to secondary hardware is traceably required and approved.
  - **Sync Controls**: Explicitly define `kSecAttrSynchronizable` as `false` unless secure iCloud Keychain synchronization is required.

### 2.3 Android Keystore (Android)
* **Assessment & Risks**:
  Standard software-backed cryptographic keys can be extracted from device memory if the operating system is rooted or compromise occurs. Without hardware-enclave boundaries, cryptographic signatures and decrypt operations are vulnerable to manipulation.
* **Platform Mechanics**:
  The Android Keystore system isolates cryptographic key materials within the Trusted Execution Environment (TEE) or a dedicated StrongBox hardware security module (HSM), making them inaccessible to the operating system itself.
* **Remediation & Best Practices**:
  - **Enforce Hardware Isolation**: Verify that keys are hardware-bound by checking `KeyInfo.isInsideSecureHardware()` after initialization.
  - **StrongBox Support**: On devices running Android 9 (API level 28) or higher, call `setIsStrongBoxBacked(true)` during `KeyGenParameterSpec` creation.
  - **Capability Minimization**: Restrict key usage capabilities. For example, authorize the key strictly for GCM block mode encryption and decryption, with no padding, and configure `.setUserAuthenticationRequired(true)` to bind key usage to active user locks.

### 2.4 Biometric Authentication
* **Assessment & Risks**:
  Implementing biometric authentication (FaceID, TouchID, or Android BiometricPrompt) as a simple boolean callback (e.g., `if (biometricPassed) { userLoggedIn = true }`) is highly vulnerable. Attackers can easily bypass these checks using runtime hooking frameworks (such as Frida) to force return values to true.
* **Platform Mechanics**:
  Secure biometric integration must bind the authentication outcome to the cryptographic decryption of a secret. The secret remains locked in hardware until the biometric challenge is satisfied.
* **Remediation & Best Practices**:
  - **iOS (Keychain Binding)**: Access credentials stored in the Keychain using a `SecAccessControl` reference created with `.biometryAny` or `.biometryCurrentSet` flags. The OS releases the item only after successful biometric validation.
  - **Android (CryptoObject Binding)**: Bind the `BiometricPrompt` execution to an active cryptographic key inside the Keystore. Pass an initialized `BiometricPrompt.CryptoObject` containing a `Cipher` or `Signature` object to the `authenticate()` function. Ensure the key requires strong biometric authentication to sign or decrypt.

### 2.5 Certificate Pinning
* **Assessment & Risks**:
  Relying solely on system-level certificate authority (CA) trust stores exposes network communication to intercept attacks. If a malicious CA is installed on the user's device (e.g., via a corporate profile or MDM container), attackers can intercept, read, and manipulate TLS-encrypted API traffic.
* **Platform Mechanics**:
  Certificate pinning limits acceptable connection certs to specific predefined parameters. Pinning leaf certificates causes service outages when they expire; pinning public keys is the accepted standard.
* **Remediation & Best Practices**:
  - **Pin Subject Public Key Info (SPKI)**: Extract and pin the SHA-256 hash of the Subject Public Key Info (SPKI) from the target server's primary and backup intermediate certificate authorities.
  - **Native Configuration (Android)**: Define a Network Security Configuration file (`res/xml/network_security_config.xml`) specifying `<pin-set>` elements for the production domain.
  - **Native Configuration (iOS)**: Utilize declarative network pinning within the application's `Info.plist` using the native `NSPinnedDomains` dictionary (supported natively in iOS 14+), avoiding manual URLSession delegate logic.

### 2.6 Jailbreak Detection (iOS)
* **Assessment & Risks**:
  An iOS device that has been jailbroken bypasses critical OS-level memory isolation, sandbox controls, and security configurations. Applications executing in jailbroken environments are highly susceptible to memory inspection, runtime manipulation, and dynamic hooking.
* **Platform Mechanics**:
  Jailbreak indicators typically involve un-sandboxed directory modifications, binary pathways, symlinks, and dynamic libraries loaded into the app's address space.
* **Remediation & Best Practices**:
  - **Multi-Layered Checks**: Do not rely on a single file check. Combine:
    1. **File Path Existence**: Scan for common pathways like `/Applications/Cydia.app`, `/Applications/Sileo.app`, and `/bin/bash`.
    2. **Directory Write Checks**: Attempt to write a temporary text file outside of the application's sandboxed documents directory (e.g., inside `/private/`).
    3. **Symlink Analysis**: Inspect if system pathways like `/Applications` are symlinks.
    4. **Dynamic Linker (dyld) Auditing**: Enumerate loaded dynamic libraries to detect hooks such as `MobileSubstrate` or `Frida`.
  - **Graceful Failure**: If jailbreak signals are verified, execute localized memory-wiping routines, invalidate active session tokens, notify backend monitoring, and safely degrade or terminate application execution.

### 2.7 Root Detection (Android)
* **Assessment & Risks**:
  Root access on Android grants superuser administrative privileges, bypassing standard Linux user sandboxing. Rooted devices allow unauthorized database extractions, API sniffing, and live application hooking.
* **Platform Mechanics**:
  Root frameworks (such as Magisk) hide their activity using dynamic masking (zygisk). Local heuristic searches for directories are easily bypassed.
* **Remediation & Best Practices**:
  - **Local Heuristics**: Search for common binaries (`/system/bin/su`, `/system/xbin/su`) and inspect `Build.TAGS` for `"test-keys"`.
  - **Play Integrity API**: For high-security endpoints, integrate Google's Play Integrity API. Forward the signed integrity token from the device to your backend server, where it must be decrypted and verified using Google's API. This ensures the app is running on a genuine, CTS-certified Android device.

### 2.8 SSL Configuration
* **Assessment & Risks**:
  Weak SSL/TLS configurations, support for deprecated protocols, or permitting cleartext HTTP traffic exposes user data to sniffing and active traffic modification on local networks (such as public Wi-Fi).
* **Platform Mechanics**:
  Platform network stacks can enforce strict TLS requirements and cleartext bans globally via manifest configuration settings.
* **Remediation & Best Practices**:
  - **Ban Cleartext**: Disable cleartext HTTP traffic globally.
    - **Android**: Set `android:usesCleartextTraffic="false"` in the application manifest, or declare `<base-config cleartextTrafficPermitted="false">` in the Network Security Configuration file.
    - **iOS**: Ensure App Transport Security (ATS) is active, avoiding any wildcard exemptions (`NSAllowsArbitraryLoads`) in the production configuration.
  - **Enforce TLS 1.2+**: Restrict cipher support and enforce a minimum of TLS 1.2, prioritizing TLS 1.3.

### 2.9 Backup Rules
* **Assessment & Risks**:
  By default, both iOS and Android include application sandbox storage directories in automatic backup processes (such as iCloud, Google Drive, or physical ADB extraction). If databases, session files, or local keys are written to standard directories, they are backed up and can be extracted.
* **Platform Mechanics**:
  Automated device backup services copy database, cache, and preference files unless files are explicitly flagged or excluded via configuration files.
* **Remediation & Best Practices**:
  - **iOS Exclusion**: Apply the `.isExcludedFromBackup` attribute to the URL of any local database or file containing sensitive session logs.
  - **Android Exclusion**: Disable broad backups by setting `android:allowBackup="false"` in the manifest. If backup is required, configure strict `android:dataExtractionRules` (Android 12+) and `android:fullBackupContent` (Android 11-) XML maps to explicitly exclude databases, credentials, and XML preference files.

### 2.10 Exported Activities (Android)
* **Assessment & Risks**:
  Declaring activities with `android:exported="true"` in the `AndroidManifest.xml` allows any other application on the same device to launch that activity. Unprotected exported components can be used to bypass authentication flows, inject malicious parameters, or cause state manipulation.
* **Platform Mechanics**:
  The Android OS allows inter-process communication (IPC) via Intents. Components with active intent-filters are exported by default unless explicitly declared otherwise.
* **Remediation & Best Practices**:
  - **Strict Defaulting**: Explicitly declare `android:exported="false"` for all internal activities, services, and content providers.
  - **Signature Permissions**: If an activity must be exported to allow launch from specific companion apps, protect it with custom permissions configured with `android:protectionLevel="signature"`, ensuring only applications signed with the exact same certificate can launch it.

### 2.11 Intent Filters (Android)
* **Assessment & Risks**:
  Registering implicit intent filters can expose components to intent spoofing or interception. External applications can craft and transmit malicious intent vectors to manipulate app logic.
* **Platform Mechanics**:
  Intent filters match incoming implicit intents against defined actions, categories, and data schemes.
* **Remediation & Best Practices**:
  - **Caller Verification**: In the receiving activity, call `getCallingPackage()` or `getCallingActivity()` to verify that the initiating package's identity matches a trusted signer certificate.
  - **Explicit Intents**: Use explicit intents (specifying target class parameters) for all internal communication, guaranteeing that intents are routed only to the intended components.

### 2.12 Deep Links
* **Assessment & Risks**:
  Custom URL schemes (e.g., `myapp://path`) are inherently insecure. Because any third-party application can register the same custom scheme on the device, deep links can be hijacked to intercept parameters, access tokens, or sensitive user data.
* **Platform Mechanics**:
  The mobile OS routes custom scheme URLs to whichever application registers that scheme, without validating domain ownership or registry authority.
* **Remediation & Best Practices**:
  - **No Sensitive Parameters**: Never transmit access tokens, session keys, or personal credentials inside deep link URLs.
  - **Input Sanitization**: Treat all incoming deep link parameters as completely untrusted external inputs. Validate and sanitize inputs before routing them to internal controllers or webviews.
  - **One-time Challenges**: If deep links are used for authentication (e.g., magic login links), utilize single-use, short-lived challenge tokens that must be verified and exchanged via a secure HTTPS API call.

### 2.13 Universal Links (iOS)
* **Assessment & Risks**:
  While Universal Links are inherently secure because they bind a web domain to an app bundle ID, configuration errors can lead to fallback vulnerabilities or routing failures.
* **Platform Mechanics**:
  Universal Links utilize secure HTTPS URLs (e.g., `https://yourdomain.com/route`). The operating system validates domain ownership by pulling a secure file from the domain during app installation.
* **Remediation & Best Practices**:
  - **AASA Configuration**: Host a valid, redirect-free, JSON-formatted `apple-app-site-association` (AASA) file at `https://yourdomain.com/.well-known/apple-app-site-association`.
  - **Strict Path Routing**: Explicitly define path patterns in the AASA file, limiting universal routing strictly to designated secure directories.
  - **Entitlement Mapping**: Configure the Associated Domains capability in Xcode using the explicit `applinks:yourdomain.com` prefix.

### 2.14 App Links (Android)
* **Assessment & Risks**:
  Similar to Universal Links, misconfiguring Android App Links can cause the OS to fall back to the standard, insecure browser chooser or a custom scheme, exposing links to hijacking.
* **Platform Mechanics**:
  Android App Links verify web domain association via a digital asset file hosted on the target domain.
* **Remediation & Best Practices**:
  - **AssetLinks Configuration**: Host a valid `assetlinks.json` file on your domain at `https://yourdomain.com/.well-known/assetlinks.json`. Include the application's package name and its unique SHA-256 certificate signing fingerprint.
  - **Auto-Verification**: Declare `android:autoVerify="true"` within the intent filter in `AndroidManifest.xml` to instruct the OS to verify domain ownership at install time.

### 2.15 Authentication Flows
* **Assessment & Risks**:
  Hardcoding API client secrets inside mobile binaries is a critical vulnerability; binaries can be easily reverse engineered to extract these secrets. Additionally, using embedded webviews for login screens allows the hosting app to access keystrokes and credentials.
* **Platform Mechanics**:
  OAuth 2.1 and OpenID Connect (OIDC) protocols govern secure client authentication without exposing long-term backend credentials.
* **Remediation & Best Practices**:
  - **Proof Key for Code Exchange (PKCE)**: Enforce PKCE (RFC 7636) for all mobile authentication flows, removing the requirement for a client secret during authorization code exchange.
  - **Secure System Browsers**: Conduct authentication exclusively within secure system browser components, such as `ASWebAuthenticationSession` on iOS and Custom Tabs on Android, preventing the parent app from inspecting input fields.

### 2.16 Session Handling
* **Assessment & Risks**:
  Relying solely on client-side state validation, failing to invalidate active sessions on the server upon logout, or exposing sensitive application UI contents within system multitasking views (snapshots) leads to session hijacking and data leakage.
* **Platform Mechanics**:
  Mobile OS platforms capture system multitasking snapshots of the application's current screen state to display in the app switcher.
* **Remediation & Best Practices**:
  - **Server-Side Invalidation**: Ensure that logging out triggers complete server-side session revocation of both access and refresh tokens.
  - **UI Snapshot Masking**: Mask or blur the active user interface screen during application backgrounding transitions. On iOS, add a blurring view overlay in `applicationWillResignActive` or configure a custom window background. On Android, call `window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)` inside activities containing sensitive data.

### 2.17 Token Storage
* **Assessment & Risks**:
  Writing long-lived OAuth refresh tokens or access tokens to plaintext cache directories, log buffers, or insecure SQLite databases allows local attackers to hijack the user's active session.
* **Platform Mechanics**:
  Platform logs (such as Logcat on Android or unified logging on iOS) are readable by system debugging utilities or companion applications with specific permissions.
* **Remediation & Best Practices**:
  - **Enclave Isolate**: Access tokens and long-lived refresh tokens must be saved exclusively inside secure hardware-backed containers (the iOS Keychain or Android `EncryptedSharedPreferences`).
  - **Token Lifespans**: Enforce short access token lifespans (e.g., 15 minutes) and implement one-time-use, rotating refresh tokens.
  - **Log Sanitization**: Ensure that logging mechanisms strip all authorization header values, bear tokens, and credential strings before writing to output buffers.

---

## 3. Recommended Implementation Roadmap & Recommendations

To maintain a secure repository posture, follow this prioritization sequence:

1. **Phase 1: Secure Storage & Key Management** (High Priority)
   - Migrate key-value storage tasks to `EncryptedSharedPreferences` (Android) and strict Keychain access classes (iOS).
   - Configure hardware keystore protection with `setIsStrongBoxBacked(true)`.

2. **Phase 2: Authentication & Session Protection** (Medium Priority)
   - Transition OAuth flows to PKCE via native system browsers.
   - Enforce server-side session invalidation and multitasking snapshot masking.

3. **Phase 3: Network & Domain Association** (Medium Priority)
   - Enforce TLS 1.2+ minimums and configure SPKI certificate pinning.
   - Validate apple-app-site-association and assetlinks.json domain alignments.
