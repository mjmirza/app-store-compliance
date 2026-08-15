# Mobile Security Requirements and Best Practices (2026)

This playbook establishes a rigorous, comprehensive security reference for mobile application development. It addresses the 17 core mobile security domains required to protect user data, prevent unauthorized access, and ensure compliance with platform policies and industry standards (e.g., OWASP MASVS).

Each section provides a high-level review of the security domain, platform-specific mechanics (iOS and Android), concrete secure implementation recommendations, and rejection/compliance risks.

---

## 1. Secure Storage

### 1.1 Overview
Sensitive information (session tokens, passwords, personal data, API keys, private cryptographic keys) must never be stored in plaintext. Standard application sandbox structures - such as `UserDefaults` on iOS or standard `SharedPreferences` on Android - write content directly to XML or plist files in unencrypted formats, allowing easy retrieval on jailbroken/rooted devices, or via backup analysis.

### 1.2 Platform Implementation & Best Practices

#### iOS: Secure Storage
- **Unsecure Options:** `UserDefaults`, CoreData (without custom encryption), plain SQLite, or standard application documents/cache directories.
- **Secure Option:** Use the **Keychain Services API** for small pieces of data (tokens, credentials, keys). For larger databases, use SQLCipher to encrypt the local SQLite/CoreData database.
- **Data Protection Class:** When writing sensitive files directly to disk, use iOS Data Protection. Pass `Data.WritingOptions.completeFileProtection` to encrypt the file on disk, which remains encrypted when the device is locked.

#### Android: Secure Storage
- **Unsecure Options:** Plain `SharedPreferences`, standard internal/external storage files, or standard SQLite databases.
- **Secure Option:** Use **EncryptedSharedPreferences** and **EncryptedFile** (from the Jetpack Security library), which automatically handle key management and encryption of storage components using AES-256 (for files) and AES-256-SIV (for keys/values).
- **Database Encryption:** If using SQLite or Room, encrypt the database with **SQLCipher for Android**, using a hardware-backed master key generated in the Android Keystore.

---

## 2. Keychain (iOS Specific)

### 2.1 Overview
The iOS Keychain provides a secure, hardware-accelerated enclave to store small, highly sensitive configuration and credential items. The items are encrypted and managed directly by the operating system, isolated from other applications.

### 2.2 Secure Implementation Recommendations
- **Accessibility Attributes:** Always specify the strict accessibility attribute (`kSecAttrAccessible`) when creating or updating Keychain items:
  - `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`: **Highly Recommended** for background tasks or push notification handlers. The data is available after the user unlocks the device once, and is not restored to another physical device via backups.
  - `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`: Use for foreground-only apps. The data is accessible only when the device is unlocked and is not backed up.
  - **Avoid:** `kSecAttrAccessibleAlways` (deprecated) and non-`ThisDeviceOnly` classes if you want to prevent migration of the credentials to other physical devices during backups.
- **Access Group Sharing:** Limit Keychain sharing (`kSecAttrAccessGroup`) strictly to verified app suites from the same team using Keychain Sharing entitlements.
- **Keychain Backups:** Ensure the `kSecAttrSynchronizable` attribute is set to `false` (default) unless explicit iCloud Keychain synchronization is required.

---

## 3. Android Keystore (Android Specific)

### 3.1 Overview
The Android Keystore system lets developers store cryptographic keys in a hardware-backed container (such as the Trusted Execution Environment (TEE) or StrongBox Security Chip), making them extremely difficult to extract from the device even if the operating system is compromised or rooted.

### 3.2 Secure Implementation Recommendations
- **Hardware Backing:** Force the use of hardware-backed keys by checking `KeyInfo.isInsideSecureHardware()` after key generation. On devices supporting Android 9 (API 28) or higher, use `setIsStrongBoxBacked(true)` to enforce hardware protection using a dedicated HSM chip.
- **Key Attestation:** For high-security environments, use Key Attestation to mathematically prove to a backend server that the cryptographic key was created in hardware and has not been tampered with.
- **Purpose and Encryption Modes:** Strictly limit key capabilities during creation (e.g., allow ONLY decryption/encryption with specific padding schemes):
  ```kotlin
  val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
  keyGenerator.init(
      KeyGenParameterSpec.Builder("MySecureKeyAlias", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
          .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
          .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
          .setUserAuthenticationRequired(true) // require passcode/biometrics to use the key
          .build()
  )
  ```

---

## 4. Biometric Authentication

### 4.1 Overview
Biometric authentication (FaceID, TouchID, Android BiometricPrompt) must verify user identity safely. A critical mistake is treating biometrics as an offline UI lock that merely flips a boolean flag (e.g., `isLoggedIn = true`) upon success. Attackers can bypass boolean returns using runtime instrumentation (e.g., Frida hooks on `LAContext` or `BiometricPrompt`).

### 4.2 Secure Implementation Recommendations
- **Crypto-Backed Biometrics:** Rather than relying on simple success callbacks, require biometric authentication to unlock or authorize a cryptographic key stored in the Keychain or Keystore.
- **iOS Implementation:**
  - Create Keychain item with `SecAccessControl` using `.biometryAny` or `.biometryCurrentSet`.
  - When accessing the item, the OS automatically prompts the user for FaceID/TouchID and releases the decrypted token ONLY if biometrics pass.
  - **Avoid** simple offline `LAContext.evaluatePolicy` checks for session authorization unless paired with severe security constraints.
- **Android Implementation:**
  - Pass an initialized `BiometricPrompt.CryptoObject` (wrapping a Cipher, Signature, or Mac associated with a Keystore key) to `biometricPrompt.authenticate()`.
  - The Keystore key must be configured with `.setUserAuthenticationRequired(true)` and `.setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)`.
  - The key can only decrypt/sign if the user successfully passes strong biometric authentication.

---

## 5. Certificate Pinning

### 5.1 Overview
Certificate Pinning (or public-key pinning) mitigates Man-in-the-Middle (MITM) attacks by ensuring the client connects strictly to a server presenting a pre-defined cryptographic public key. This prevents traffic interception even if an attacker installs a malicious root certificate on the user's device (e.g., via corporate proxies, malware, or user-approved configuration profiles).

### 5.2 Secure Implementation Recommendations
- **Pin SPKI Hashes:** Do not pin the leaf certificate itself (which changes frequently during standard certificate rotations, causing app outages). Instead, pin the **Subject Public Key Info (SPKI)** hash of the intermediate or leaf public key.
- **Backup Pins:** Always include at least one backup pin (representing a standby Certificate Authority or intermediate key) to prevent bricking the app if the primary certificate needs emergency replacement.
- **Native Implementation:**
  - **iOS:** Use declarative Network Session Pinning in `Info.plist` using the `NSPinnedDomains` key (supported natively since iOS 14). This operates safely inside the networking stack without manual delegation code.
  - **Android:** Declare a Network Security Configuration file (`res/xml/network_security_config.xml`) and specify the pins within `<pin-set>` elements. The system automatically enforces pinning for any `HttpURLConnection` or OkHttp client:
    ```xml
    <network-security-config>
        <domain-config>
            <domain includeSubdomains="true">api.myproduction.com</domain>
            <pin-set expiration="2026-12-31">
                <pin digest="SHA-256">Base64EncodedSPKIHashHere=</pin>
                <pin digest="SHA-256">Base64EncodedBackupSPKIHashHere=</pin>
            </pin-set>
        </domain-config>
    </network-security-config>
    ```

---

## 6. Jailbreak Detection (iOS)

### 6.1 Overview
A jailbroken iOS device bypasses critical platform sandboxing protections, allowing attackers to access private application data directories, hook runtime methods, and intercept secure communications.

### 6.2 Secure Implementation Recommendations
- **Multi-layered defense:** Use multiple independent indicators to assess device compromise. Avoid single simple functions.
- **Standard Checks:**
  1. **File Existence:** Check for known jailbreak-related directories and binaries (e.g., `/Applications/Cydia.app`, `/Applications/Sileo.app`, `/Library/MobileSubstrate/MobileSubstrate.dylib`, `/bin/bash`, `/usr/sbin/sshd`, `/private/var/lib/apt`).
  2. **Directory Permissions:** Attempt to write a dummy file outside the app sandbox (e.g., to `/private/jailbreak.txt`). Standard apps will fail; jailbroken apps with root access may succeed.
  3. **Symlink Analysis:** Check if common directories like `/Library/Ringtones` or `/Applications` are symlinks, which jailbreak tools create to preserve disk space.
  4. **Dynamic Linker (dyld) Inspection:** Iterate over loaded dynamic libraries to detect hooks or injection libraries (e.g., `MobileSubstrate`, `Frida`).
- **Response:** If jailbreaking is detected, wipe cached tokens and local databases, notify the backend, and safely terminate or gracefully degrade features.

---

## 7. Root Detection (Android)

### 7.1 Overview
An Android device with root access grants administrative control, which bypasses critical security policies, memory isolation, and filesystem sandbox controls.

### 7.2 Secure Implementation Recommendations
- **Local Heuristics:**
  1. **Binary Search:** Look for administrative binaries like `su`, `busybox`, or root-management tools across standard paths (`/system/bin/su`, `/system/xbin/su`, `/sbin/su`, `/system/sd/xbin/su`).
  2. **Build Tags:** Check `android.os.Build.TAGS` for `"test-keys"`, indicating a custom or rooted ROM build instead of a release-signed image.
  3. **Superuser Apps:** Inspect the package list for root management packages (e.g., `com.noshufou.android.su`, `eu.chainfire.supersu`, `com.topjohnwu.magisk`).
- **Hardware-Backed Attestation (Highly Recommended):**
  - Standard local heuristics are easily bypassed using Magisk Hide or zygisk modules.
  - Rely on the **Google Play Integrity API**. Call the API from the device, forward the cryptographically signed verdict token to your backend server, and decrypt/verify it on the backend. This provides a hardware-backed verdict of device integrity and whether it runs on a certified Android build.

---

## 8. SSL Configuration

### 8.1 Overview
Misconfigured Transport Layer Security (TLS) leaves mobile applications vulnerable to credential sniffing and traffic modification. Cleartext traffic (HTTP) must be completely disabled in production.

### 8.2 Secure Implementation Recommendations
- **Enforce TLS 1.3 or 1.2 minimum:** Disable backward compatibility with deprecated SSL v3, TLS 1.0, and TLS 1.1.
- **iOS Implementation:**
  - Keep App Transport Security (ATS) enabled.
  - **Avoid** setting `NSAllowsArbitraryLoads` to `true` in production `Info.plist`. If certain domains require HTTP exceptions, specify them explicitly under `NSExceptionDomains` with strict justifications.
- **Android Implementation:**
  - Define cleartext policies in `AndroidManifest.xml` via `android:usesCleartextTraffic="false"`.
  - Alternatively, enforce it globally in the Network Security Configuration:
    ```xml
    <network-security-config>
        <base-config cleartextTrafficPermitted="false">
            <trust-anchors>
                <certificates src="system" />
            </trust-anchors>
        </base-config>
    </network-security-config>
    ```

---

## 9. Backup Rules

### 9.1 Overview
By default, mobile operating systems include application sandboxed files in automated backups (iCloud backups on iOS, ADB / Google Drive backups on Android). This means sensitive data stored insecurely is automatically transferred to cloud drives or accessible via physical extraction.

### 9.2 Secure Implementation Recommendations
- **iOS Backup Exclusion:**
  - Exclude any sensitive database or local config file from automatic iCloud and iTunes backups by adding the `.isExcludedFromBackup` resource attribute to the file's URL:
    ```swift
    var url = URL(fileURLWithPath: path)
    var values = URLResourceValues()
    values.isExcludedFromBackup = true
    try url.setResourceValues(values)
    ```
- **Android Backup Rules:**
  - **Do not** leave `android:allowBackup="true"` without defining tight filters. Backups allow extraction of private `/data/data/your.package/` files using simple `adb backup` commands.
  - For high-security applications, completely disable backup:
    ```xml
    <application android:allowBackup="false" ...>
    ```
  - If backup is required, strictly configure `android:dataExtractionRules` (Android 12+) and `android:fullBackupContent` (Android 11-) in the manifest to target safe folders and explicitly exclude databases, shared preferences holding tokens, and credential files:
    ```xml
    <!-- res/xml/data_extraction_rules.xml -->
    <data-extraction-rules>
        <cloud-backup>
            <exclude domain="sharedpref" path="auth_tokens.xml"/>
            <exclude domain="database" path="secure_db.db"/>
        </cloud-backup>
        <device-to-device-backup>
            <exclude domain="sharedpref" path="auth_tokens.xml"/>
            <exclude domain="database" path="secure_db.db"/>
        </device-to-device-backup>
    </data-extraction-rules>
    ```

---

## 10. Exported Activities (Android Specific)

### 10.1 Overview
Any activity declared in `AndroidManifest.xml` with `android:exported="true"` can be launched by any other application running on the device. Unintentionally exported activities expose internal business logic, allow authorization bypass, and can cause tapjacking or state manipulation.

### 10.2 Secure Implementation Recommendations
- **Strict Default:** Set `android:exported="false"` for all internal activities.
- **Enforcement since Android 12:** Android 12 (API 31) requires every component (activity, service, receiver) that has intent filters to explicitly declare `android:exported`. If it lacks the tag, the app cannot be installed or submitted.
- **Exported Component Protection:**
  - If an activity must be exported (e.g., launching from the home screen or third-party launchers), protect it using custom permission limits:
    ```xml
    <activity android:name=".MyExportedActivity"
              android:exported="true"
              android:permission="com.mycompany.myapp.PERMISSION_LAUNCH_ACTIVITY">
    ```
  - Ensure the permission uses `android:protectionLevel="signature"`, guaranteeing that only apps signed with your exact developer key can launch the activity.

---

## 11. Intent Filters (Android Specific)

### 11.1 Overview
Intent filters define which implicit intents an application component can respond to. Registering intent filters automatically exports the component, potentially exposing it to untrusted third-party apps.

### 11.2 Secure Implementation Recommendations
- **Intent Spoofing & Hijacking Prevention:** Validate the sender and verify incoming data within the receiving component before acting on it.
  - Use `getCallingActivity()` or `getCallingPackage()` to check if the caller matches a trusted package name and certificate.
- **Secure Intent Dispatches:** When launching an internal component, use explicit intents (specifying the exact target class or package) instead of implicit intents. This prevents malicious third-party apps on the same device from intercepting or "hijacking" the intent.
  ```kotlin
  val explicitIntent = Intent(context, TargetActivity::class.java).apply {
      putExtra("param", value)
  }
  startActivity(explicitIntent)
  ```

---

## 12. Deep Links

### 12.1 Overview
Deep links let external sources invoke internal routes within the app. Standard deep links using custom URL schemes (e.g., `myapp://route`) are inherently insecure, as any other application on the device can register the exact same scheme and hijack the communication, potentially stealing auth tokens or parameters.

### 12.2 Secure Implementation Recommendations
- **Sanitize Input:** Treat deep links as untrusted external inputs. Always sanitize, validate, and parse deep link parameters to prevent SQL injection, path traversal, or remote code execution.
- **Do Not Transmit Secrets:** Never include authentication tokens, session IDs, passwords, or transactional data in deep link URLs.
- **Auth Token Exchange:** If deep links are used for authentication (e.g., magic login links), pass a short-lived, single-use, cryptographically strong challenge token that is exchanged on the server using an explicit HTTPS request, never an active session token itself.

---

## 13. Universal Links (iOS Specific)

### 13.1 Overview
Universal Links are iOS's secure deep-linking mechanism. Instead of custom URL schemes, they use standard HTTPS links (e.g., `https://mycompany.com/profile`). Because domain validation is performed against the website's configuration, Universal Links cannot be hijacked or duplicated by other applications.

### 13.2 Secure Implementation Recommendations
- **AASA Configuration:** Host a valid **Apple App Site Association (AASA)** file on your domain at `https://yourdomain.com/.well-known/apple-app-site-association`.
  - Serve the file with `Content-Type: application/json` and no redirects.
  - The file specifies which app bundle IDs are authorized to handle specific URL paths:
    ```json
    {
      "applinks": {
        "details": [
          {
            "appIDs": ["TEAMID12345.com.mycompany.myapp"],
            "components": [
              { "/": "/profile/*" }
            ]
          }
        ]
      }
    }
    ```
- **Associated Domains Entitlement:** Enable the "Associated Domains" capability in Xcode and add the domain in the format `applinks:yourdomain.com`.

---

## 14. App Links (Android Specific)

### 14.1 Overview
Android App Links are standard HTTPS links that are configured to automatically launch the matching app directly, bypassing the platform "disambiguation dialog" by verifying domain ownership.

### 14.2 Secure Implementation Recommendations
- **AssetLinks Verification:** Host the **Digital Asset Links** JSON file on your domain at `https://yourdomain.com/.well-known/assetlinks.json`:
  ```json
  [
    {
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.mycompany.myapp",
        "sha256_cert_fingerprints": ["AA:BB:CC:DD:EE:FF:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66"]
      }
    }
  ]
  ```
- **Manifest Verification Tag:** Add `android:autoVerify="true"` to the intent filter within `AndroidManifest.xml` to instruct the operating system to verify the domain ownership on app installation:
  ```xml
  <intent-filter android:autoVerify="true">
      <action android:name="android.intent.action.VIEW" />
      <category android:name="android.intent.category.DEFAULT" />
      <category android:name="android.intent.category.BROWSABLE" />
      <data android:scheme="https" android:host="yourdomain.com" />
  </intent-filter>
  ```

---

## 15. Authentication Flows

### 15.1 Overview
Mobile authentication flows must handle user credentials securely, prevent reverse engineering of backend secrets, and implement cryptographic challenges to prevent replay attacks.

### 15.2 Secure Implementation Recommendations
- **OAuth 2.1 / OIDC with PKCE:** Always use **Proof Key for Code Exchange (PKCE)** (RFC 7636) for mobile OAuth integration. PKCE eliminates the need to store client secrets inside the mobile app binary (where they can easily be extracted via reverse engineering) and protects the authorization code exchange against intercept attacks.
- **Embedded vs. System Browser:** Use secure system components (like `ASWebAuthenticationSession` on iOS and **Custom Tabs** on Android) for authentication screens. Avoid using embedded `WKWebView` or Android `WebView` components, which allow the hosting app to sniff or manipulate credentials and passwords entered by the user.

---

## 16. Session Handling

### 16.1 Overview
Session tokens must be securely generated, properly scoped, periodically rotated, and gracefully destroyed when no longer in use.

### 16.2 Secure Implementation Recommendations
- **Server-Side Session Validation:** The client must never make local assumptions about session validity. Every critical action must be authorized and validated on the server.
- **Session Timeout & Background Policy:**
  - Clear sensitive screen data and cached sessions when the app is backgrounded.
  - Blur the app's snapshot (multitasking view) to prevent sensitive user information from leaking to screenshots.
- **Logout Integrity:** When a user logs out, perform a complete session invalidation on the server-side, and simultaneously clear all local access/refresh tokens, cookies, and local database keys on the device.

---

## 17. Token Storage

### 17.1 Overview
Tokens (Access Tokens, Refresh Tokens, JWTs) are sensitive authorization credentials. If leaked, they allow full identity theft.

### 17.2 Secure Implementation Recommendations
- **No Disk Leakage:** Never write tokens to regular files, unencrypted SQLite databases, standard logs, or console output (`NSLog`, `print`, `Log.d`).
- **Secure Vaulting:** Store tokens strictly inside the **iOS Keychain** or **Android EncryptedSharedPreferences** / Keystore-encrypted database.
- **Refresh Token Isolation:** Refresh tokens have long lifetimes and must be protected with additional security constraints (e.g., biometrics required or scoped to `ThisDeviceOnly`). Access tokens should be short-lived (e.g., 15 minutes), with refresh tokens rotated on each use.
