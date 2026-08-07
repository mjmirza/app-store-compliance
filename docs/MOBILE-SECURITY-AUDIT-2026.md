# Mobile Security Compliance Audit and Best Practices Review (2026)

This document provides a comprehensive mobile security compliance audit and best practices review covering all seventeen critical mobile security domains. It outlines the platform-specific mechanics for both iOS and Android, evaluates standard deployment risks, and provides concrete engineering recommendations aligned with industry standards (such as OWASP MASVS).

---

## 1. Secure Storage

### 1.1 Risk and Review
Storing sensitive data (such as access tokens, personally identifiable information, session keys, and database credentials) in plaintext allows unauthorized access. On rooted or jailbroken devices, attackers can extract files directly from the application sandbox. Additionally, unencrypted sandboxed directories are backed up to cloud services or physical machines in raw formats, exposing user data.

### 1.2 Platform Mechanics
- **iOS**: Standard storage files (such as UserDefaults or raw plist files) are stored in plaintext. While sandboxed, they are easily decrypted if the device is jailbroken or via physical backup extraction. iOS Data Protection provides file-level encryption, but it is bound to the device passcode and is decrypted once the device is unlocked.
- **Android**: Default Shared Preferences, raw internal files, and standard SQLite databases are written as plaintext XML/SQL files in `/data/data/<package_name>/`. On rooted devices or via standard debugging tools, this data is readily readable.

### 1.3 Recommended Improvements & Best Practices
- **iOS**: For key-value credentials or small strings, store them exclusively in the iOS Keychain Services API. For larger relational databases, integrate SQLCipher to encrypt the SQLite/CoreData instance. Apply `Data.WritingOptions.completeFileProtection` to force file encryption on disk when the device is locked.
- **Android**: Utilize the Jetpack Security library components `EncryptedSharedPreferences` and `EncryptedFile`. This library handles hardware-backed key generation and handles transparent AES-256-SIV encryption. For SQLite or Room databases, integrate SQLCipher for Android using a key generated and securely stored within the Android Keystore.

---

## 2. Keychain (iOS)

### 2.1 Risk and Review
The iOS Keychain provides secure storage for small secrets, but developers often select insecure accessibility classes or fail to protect items against physical device duplication. For example, synchronizing credentials to iCloud Keychain or allowing restoration on secondary physical hardware can violate data localization regulations.

### 2.2 Platform Mechanics
The Keychain is structured as a sqlite-backed secure database managed by the iOS security daemon (`securityd`). Access is controlled through entitlements and accessibility attributes (`kSecAttrAccessible`) which determine when a Keychain item can be read relative to the lock state of the device.

### 2.3 Recommended Improvements & Best Practices
- Enforce strict accessibility attributes during Keychain record creation:
  - Use `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` for background processes or notifications. The secret is accessible once the user unlocks the device after booting and is bound strictly to the current physical hardware (preventing backup restoration onto secondary devices).
  - Use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for foreground-exclusive secrets.
- Explicitly avoid `kSecAttrAccessibleAlways` (deprecated) and non-`ThisDeviceOnly` protection categories for high-risk assets.
- Bind Keychain keys to a specific access group (`kSecAttrAccessGroup`) to strictly limit cross-app data sharing.
- Disable `kSecAttrSynchronizable` unless cross-device synchronization via iCloud Keychain is a documented business requirement.

---

## 3. Android Keystore

### 3.1 Risk and Review
Cryptographic keys generated inside the Android Keystore can be compromised if they are implemented via software-backed emulation rather than hardware enclaves (TEE or StrongBox). Attackers utilizing system memory dumps or kernel-level exploits can extract keys from software emulation memory.

### 3.2 Platform Mechanics
The Android Keystore system delegates cryptographic key management to hardware-isolated modules:
- **Trusted Execution Environment (TEE)**: A secure area of the main processor.
- **StrongBox Keymaster**: A dedicated, tamper-resistant Hardware Security Module (HSM) chip available since Android 9 (API 28).

### 3.3 Recommended Improvements & Best Practices
- Force hardware-backed key generation using `KeyGenParameterSpec` and programmatically verify hardware isolation after key creation by calling `KeyInfo.isInsideSecureHardware()`.
- Enforce dedicated StrongBox enclaves on supported devices (API 28+) via `setIsStrongBoxBacked(true)`.
- Configure strict cryptographic purpose constraints (e.g., limit key usage strictly to `PURPOSE_DECRYPT` or `PURPOSE_SIGN` and enforce padding modes like `AES/GCM/NoPadding`).
- Avoid insecure cipher configurations such as ECB mode (`AES/ECB/PKCS5Padding`).
- Enforce user authentication requirements (`setUserAuthenticationRequired(true)`) for high-security signing or decryption keys.

---

## 4. Biometric Authentication

### 4.1 Risk and Review
A critical security flaw is implementing biometric authentication as a pure UI-level gateway. If biometrics are checked using a simple boolean callback (e.g., checking if `LAContext.evaluatePolicy` returns true), attackers can use dynamic instrumentation frameworks like Frida to hook the class methods and force a successful return value, bypassing the lock entirely.

### 4.2 Platform Mechanics
- **iOS**: Uses LocalAuthentication (`LAContext`) or Keychain-integrated Access Control lists.
- **Android**: Uses the Jetpack Biometric library (`BiometricPrompt`) which coordinates with the system biometric service and Keystore enclaves.

### 4.3 Recommended Improvements & Best Practices
- **Implement Cryptographic Binding**: Never rely on a raw boolean return. Instead, generate a secret key inside the Keychain (iOS) or Keystore (Android) that is protected by biometric access control.
- **iOS Implementation**: Apply `SecAccessControl` to Keychain records during creation, using `.biometryAny` or `.biometryCurrentSet`. The OS will prompt for biometric verification and release the decrypted token only if the hardware verification succeeds.
- **Android Implementation**: Initialize a `BiometricPrompt.CryptoObject` wrapping a Keystore-backed cipher or signature. Configure the key with `setUserAuthenticationRequired(true)` and `setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)`. Pass this `CryptoObject` to the `authenticate()` method. The Keystore will only unlock the cryptographic key to perform operations if biometric verification succeeds.

---

## 5. Certificate Pinning

### 5.1 Risk and Review
Mobile devices are susceptible to Man-in-the-Middle (MITM) attacks if they rely on the operating system's default certificate authority (CA) store. Attackers can install custom root CA profiles on the device (e.g., via corporate proxy configurations, malware, or user-accepted profiles) to intercept, inspect, and modify encrypted network traffic.

### 5.2 Platform Mechanics
Certificate pinning limits trust to specified servers.
- **iOS**: Supports declarative network configuration in `Info.plist` using the `NSPinnedDomains` key (since iOS 14).
- **Android**: Supports declarative network configurations via `res/xml/network_security_config.xml` (since Android 7.0).

### 5.3 Recommended Improvements & Best Practices
- **Pin Subject Public Key Info (SPKI)**: Do not pin the leaf certificate itself because leaf certificates rotate frequently, which would cause application outages upon expiration. Instead, pin the SHA-256 hash of the Subject Public Key Info of the primary and backup intermediate certificate authorities.
- **Configure Redundant Backup Pins**: Always declare at least one backup pin from an alternative root CA or standby key to prevent bricking the application during emergency key rotations.
- **Declarative Configuration**: Avoid custom network delegate implementation code in OkHttp or URLSession, which is prone to manual implementation errors.
  - On Android, implement the Network Security Configuration file:
    ```xml
    <network-security-config>
        <domain-config>
            <domain includeSubdomains="true">api.production.com</domain>
            <pin-set expiration="2026-12-31">
                <pin digest="SHA-256">PrimarySPKIHashValue=</pin>
                <pin digest="SHA-256">BackupSPKIHashValue=</pin>
            </pin-set>
        </domain-config>
    </network-security-config>
    ```
  - On iOS, configure `NSPinnedDomains` inside the `Info.plist`.

---

## 6. Jailbreak Detection (iOS)

### 6.1 Risk and Review
Running an application on a jailbroken iOS device compromises its security model. The operating system's sandbox controls are disabled, allowing other processes to inspect application memory, intercept sensitive storage, inject dynamic libraries, and modify application behavior at runtime.

### 6.2 Platform Mechanics
Jailbreaks install files, binaries, and libraries outside the standard sandboxed hierarchy. They alter runtime execution behavior and dynamic linker (`dyld`) activity.

### 6.3 Recommended Improvements & Best Practices
- **Multi-Layered Detection Heuristics**: Do not rely on a single file existence check. Combine multiple detection methodologies:
  1. **File Path Verification**: Check for known jailbreak-related directories, applications, and binaries (e.g., `/Applications/Cydia.app`, `/Applications/Sileo.app`, `/usr/sbin/sshd`, `/bin/bash`, `/private/var/lib/apt`).
  2. **Sandbox Privilege Escalation Heuristics**: Attempt to write a temporary text file outside the sandboxed application directory (e.g., `/private/jailbreak_test.txt`). This write operation should fail; if it succeeds, the application is running with root permissions.
  3. **Symlink Integrity Inspections**: Verify if common system directories (e.g., `/Library/Ringtones`, `/Applications`) have been replaced with symlinks.
  4. **Dynamic Linker (dyld) Auditing**: Iterate through loaded dynamic libraries at runtime to detect injection patterns, such as `MobileSubstrate` or `frida-agent`.
- **Response Protocol**: If compromise is detected, clear all in-memory keys, purge cached session tokens, alert the backend, and terminate the application session safely.

---

## 7. Root Detection (Android)

### 7.1 Risk and Review
A rooted Android device grants administrative privilege, allowing user-space tools to manipulate memory registers, read sandboxed internal storage folders, bypass local security guards, and execute arbitrary code. Local heuristic root checks are easily bypassed using masking tools (such as Magisk Hide or zygisk-based modules).

### 7.2 Platform Mechanics
Rooted environments introduce local binaries (e.g., `su`), alter system properties, and modify system partition behaviors.

### 7.3 Recommended Improvements & Best Practices
- **Combine Local and Hardware-Backed Checks**:
  1. **Local Searches**: Audit system directories for administrative binaries (such as `su`, `busybox`, `magisk`) across standard execution paths (e.g., `/system/bin/su`, `/system/xbin/su`, `/sbin/su`).
  2. **Build-Tags Verification**: Inspect `android.os.Build.TAGS` for custom rom markings (`test-keys`).
  3. **Package Inspection**: Scan the package manager for known root-management applications.
- **Deploy the Google Play Integrity API**: High-risk operations (e.g., payment transactions or authentication exchanges) must rely on the Play Integrity API. Send the integrity token to your secure backend, decrypt/verify the payload server-side using Google's verification servers, and assess the hardware-backed system verdict. Do not evaluate the integrity token solely within the client application.

---

## 8. SSL Configuration

### 8.1 Risk and Review
Weak network configurations allow cleartext HTTP traffic or outdated TLS protocols (such as TLS 1.0 or 1.1), exposing network requests to traffic interception, credential harvesting, and session hijacking over public Wi-Fi networks.

### 8.2 Platform Mechanics
Network frameworks use configuration manifests to govern connection behaviors globally.
- **iOS**: App Transport Security (ATS) regulates network request security.
- **Android**: Uses the manifest-declared network configuration.

### 8.3 Recommended Improvements & Best Practices
- **Globally Disable Cleartext Traffic**:
  - On Android, declare `android:usesCleartextTraffic="false"` in `AndroidManifest.xml`, or enforce it globally inside the Network Security Configuration file:
    ```xml
    <network-security-config>
        <base-config cleartextTrafficPermitted="false">
            <trust-anchors>
                <certificates src="system" />
            </trust-anchors>
        </base-config>
    </network-security-config>
    ```
  - On iOS, ensure that `NSAllowsArbitraryLoads` is set to `false` (default) inside `Info.plist`. If specific external legacy domains require cleartext access, restrict them to explicit `NSExceptionDomains` with structural justifications.
- **Enforce TLS 1.2 or TLS 1.3 Minimums**: Configure the TLS configuration context to reject outdated SSLv3, TLS 1.0, and TLS 1.1 handshakes.

---

## 9. Backup Rules

### 9.1 Risk and Review
By default, mobile operating systems include application sandboxed data in standard backups (iCloud/iTunes backups on iOS, and ADB/Google Drive backups on Android). If local SQLite databases or SharedPreferences files contain sensitive tokens or keys, an attacker can extract these credentials via automated ADB backup commands or by compromising cloud backup targets.

### 9.2 Platform Mechanics
- **iOS**: Files inside standard directories are synchronized during backups unless explicitly marked for exclusion.
- **Android**: Automated backups can be extracted physically via Android Debug Bridge (ADB) unless backup functionality is modified.

### 9.3 Recommended Improvements & Best Practices
- **iOS Exclusions**: Apply the `.isExcludedFromBackup` resource attribute to any sandboxed file or directory URL holding transactional or cached information:
  ```swift
  var url = URL(fileURLWithPath: databasePath)
  var values = URLResourceValues()
  values.isExcludedFromBackup = true
  try url.setResourceValues(values)
  ```
- **Android Exclusions**:
  - For high-security applications, completely disable backup support inside the `AndroidManifest.xml`:
    ```xml
    <application android:allowBackup="false" ...>
    ```
  - If backup support is required, configure precise extraction rules using `android:dataExtractionRules` (Android 12+) and `android:fullBackupContent` (Android 11-). Explicitly declare exclusions for databases, credentials, and preference files:
    ```xml
    <!-- res/xml/data_extraction_rules.xml -->
    <data-extraction-rules>
        <cloud-backup>
            <exclude domain="sharedpref" path="user_session.xml"/>
            <exclude domain="database" path="app_database.db"/>
        </cloud-backup>
        <device-to-device-backup>
            <exclude domain="sharedpref" path="user_session.xml"/>
            <exclude domain="database" path="app_database.db"/>
        </device-to-device-backup>
    </data-extraction-rules>
    ```

---

## 10. Exported Activities (Android)

### 10.1 Risk and Review
Activities declared with `android:exported="true"` can be launched by any other application running on the same device. If internal application activities (such as checkout, profile editing, or administrative panels) are unintentionally exported, malicious applications can launch them directly, bypassing onboarding gates, authentication screens, and authorization logic.

### 10.2 Platform Mechanics
The `android:exported` attribute determines the accessibility of activities, services, and broadcast receivers to external components. Android 12 (API 31) mandates explicit declaration of this attribute for any component declaring intent filters.

### 10.3 Recommended Improvements & Best Practices
- **Apply the Principle of Least Privilege**: Set `android:exported="false"` for all internal activities and components. Only export components that must be accessible from other apps (e.g., launch activities or deep link handlers).
- **Protect Exported Components**: If a component must be exported, enforce signature-level custom permissions:
  ```xml
  <activity android:name=".SensitiveExportedActivity"
            android:exported="true"
            android:permission="com.company.app.PERMISSION_SENSITIVE_FLOW">
  ```
- Set `android:protectionLevel="signature"` on the custom permission definition to ensure only apps signed with your exact certificate can invoke the component.

---

## 11. Intent Filters (Android)

### 11.1 Risk and Review
Registering intent filters automatically exports the component, opening it to implicit intent spoofing, component hijacking, or eavesdropping on system-wide communications. If an application responds to implicit intents without verifying the origin, it may process malicious data.

### 11.2 Platform Mechanics
Intent filters declare the capabilities of activities, services, or broadcast receivers to handle specific implicit intents.

### 11.3 Recommended Improvements & Best Practices
- **Prefer Explicit Intents**: Use explicit class intents (naming the exact package and class target) when communicating internally within the application. This prevents external interceptors from capturing the intent.
- **Verify Calling Identity**: For components responding to intent filters, call `getCallingActivity()` or `getCallingPackage()` within the target component to audit the caller's package name and verify its signature against a trusted public key before processing input data.
- **Enforce Custom Permissions**: Restrict broadcast receivers using signature-level permissions to block third-party applications from broadcasting fake events to your app.

---

## 12. Deep Links

### 12.1 Risk and Review
Custom URL schemes (such as `myapp://route?param=val`) are insecure because different applications can register the exact same scheme. If multiple apps register the same scheme, the platform does not guarantee which app will handle the link. This can lead to link hijacking, parameter injection, and exposure of sensitive credentials.

### 12.2 Platform Mechanics
Custom schemes are registered in the application manifests (`CFBundleURLSchemes` on iOS, `<data android:scheme="...">` on Android). When a link with that scheme is requested, the system launches an app associated with it.

### 12.3 Recommended Improvements & Best Practices
- **Treat Inputs as Untrusted**: Treat deep links as untrusted external inputs. Implement strict validation, sanitization, and parsing of all parameters.
- **Never Transmit Secrets**: Do not include authentication tokens, passwords, or session IDs in deep link URLs.
- **Exchanges Challenge Tokens**: For authentication-based flows (such as password resets or passwordless login), send a short-lived, single-use, cryptographically secure challenge token. The application must exchange this token via a secure HTTPS POST request to your backend, rather than acting on an active session token passed directly in the URL query string.

---

## 13. Universal Links (iOS)

### 13.1 Risk and Review
While Universal Links are more secure than custom URL schemes, insecure implementations can occur if the web association is misconfigured or if the wildcard paths are overly permissive, allowing attackers to route administrative or debug endpoints into the mobile client.

### 13.2 Platform Mechanics
Universal Links use standard HTTPS URLs (e.g., `https://production.com/profile`) to link to specific content. iOS validates ownership by downloading an association configuration from the host domain.

### 13.3 Recommended Improvements & Best Practices
- **Host a Valid AASA File**: Publish a valid `apple-app-site-association` (AASA) JSON file at the root or within the `.well-known` directory of your HTTPS server:
  - Serve the file with the `Content-Type: application/json` header, without redirects, and over a TLS-protected connection.
- **Apply Precise Path Inclusions**: Avoid using broad wildcards (such as `*`) that match all paths on your domain. Explicitly define restricted path lists:
  ```json
  {
    "applinks": {
      "details": [
        {
          "appIDs": ["TEAMID12345.com.company.app"],
          "components": [
            { "/": "/shop/*" },
            { "/": "/verify/*" }
          ]
        }
      ]
    }
  }
  ```
- Enforce the "Associated Domains" capability in Xcode using the exact `applinks:yourdomain.com` syntax.

---

## 14. App Links (Android)

### 14.1 Risk and Review
If Android App Links are not configured with auto-verification, the operating system defaults to displaying a "disambiguation dialog" that prompts the user to select which application should handle the link. This allows custom scheme hijacker apps to masquerade as the target application.

### 14.2 Platform Mechanics
Android App Links use HTTPS URLs verified against a Digital Asset Links JSON file hosted on the target domain.

### 14.3 Recommended Improvements & Best Practices
- **Enforce Auto-Verification**: Always include `android:autoVerify="true"` on the deep-linking intent-filter inside `AndroidManifest.xml` to prompt the OS to verify domain ownership at install time:
  ```xml
  <intent-filter android:autoVerify="true">
      <action android:name="android.intent.action.VIEW" />
      <category android:name="android.intent.category.DEFAULT" />
      <category android:name="android.intent.category.BROWSABLE" />
      <data android:scheme="https" android:host="company.com" />
  </intent-filter>
  ```
- **Host the Digital Asset Links File**: Publish the signed `assetlinks.json` file at `https://company.com/.well-known/assetlinks.json`:
  ```json
  [
    {
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.company.app",
        "sha256_cert_fingerprints": ["AA:BB:CC:DD:EE:FF:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66"]
      }
    }
  ]
  ```
  Ensure the fingerprint array contains the exact SHA-256 certificate fingerprints of both your release and play-signing keys.

---

## 15. Authentication Flows

### 15.1 Risk and Review
Hardcoding client secrets inside mobile binaries is a severe risk; attackers can easily extract secrets using basic decompilation tools. Additionally, using standard in-app WebViews (such as `WKWebView` or `WebView`) for authentication screens can lead to credential harvesting, as the parent application can inject arbitrary JavaScript to intercept user input.

### 15.2 Platform Mechanics
Authentication components govern user session authorization.

### 15.3 Recommended Improvements & Best Practices
- **Implement OIDC/OAuth 2.1 with PKCE**: Always enforce Proof Key for Code Exchange (PKCE) (RFC 7636). This standard generates a dynamic challenge and verifier per authentication request, eliminating the need to store static client secrets in the mobile client.
- **Enforce Secure System Browsers**: Use `ASWebAuthenticationSession` (iOS) or Android **Custom Tabs** for all user login flows. These components isolate cookies and authentication states from the host application, preventing local credential sniffing or session manipulation.

---

## 16. Session Handling

### 16.1 Risk and Review
Mobile applications frequently store persistent session tokens on the device without verifying validation state with the server, leading to orphan sessions. Additionally, leaving active screens visible in the multitasking application switcher can leak sensitive data (such as bank balances or identity records) to physical onlookers.

### 16.2 Platform Mechanics
Session lifecycles govern user authorization persistence.

### 16.3 Recommended Improvements & Best Practices
- **Enforce Server-Side Invalidation**: Ensure that logouts trigger complete server-side session invalidation. Do not rely solely on client-side deletion of local tokens.
- **Snapshot Blurring (App Switcher Masking)**: Hide and blur the application interface when backgrounded.
  - On iOS, listen to `UIApplication.willResignActiveNotification` and cover the main window with a temporary view or visual blur effect.
  - On Android, apply `WindowManager.LayoutParams.FLAG_SECURE` inside the activity configuration to prevent the OS from capturing screenshots in the multitasking window or allowing manual user screenshots of sensitive screens.
- Enforce short-lived access tokens and rotate refresh tokens.

---

## 17. Token Storage

### 17.1 Risk and Review
Tokens (such as access tokens, refresh tokens, and JSON Web Tokens) are sensitive authorization credentials. Storing them in plaintext configuration files, local application cache folders, or printing them in diagnostic logs (`print`, `NSLog`, `Log.d`) exposes them to leakage.

### 17.2 Platform Mechanics
Tokens act as cryptographic identity assertions.

### 17.3 Recommended Improvements & Best Practices
- **Never Log Secrets**: Ensure that diagnostic logs do not print tokens or session payloads.
- **Store in Enclaves**: Store access and refresh tokens strictly inside the secure iOS Keychain or Android `EncryptedSharedPreferences`.
- **Implement Refresh Token Rotation**: Design the authentication backend to rotate the refresh token on every usage, invalidating the previous token instantly.
- **Enforce Short Lifetimes**: Configure access tokens with short lifetimes (e.g., 15 minutes), requiring refresh token exchange for continued access.
