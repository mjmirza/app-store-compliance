# Mobile Security Compliance Audit and Best Practices Review (2026)

This comprehensive audit and best practices review details the 17 core mobile security domains for iOS and Android platforms. Prepared by the Senior Compliance Officer, this document addresses secure implementation patterns, potential rejection triggers, mitigation strategies, and platform-specific native mechanics.

Strictly aligned with industry standards (such as OWASP MASVS and OWASP MSTG), this reference guarantees compliance and integrity across all mobile development operations.

---

## 1. Secure Storage

### 1.1 Overview
Applications regularly handle highly sensitive localized assets including user credentials, OAuth access and refresh tokens, and encrypted database keys. By default, standard key-value containers (such as iOS `UserDefaults` and Android `SharedPreferences`) write directly to XML or plist configuration files in cleartext format. This allows trivial extraction on rooted/jailbroken devices or through standard file system backups.

### 1.2 Platform-Specific Mechanics
- **iOS Mechanics**: `UserDefaults` offers zero built-in cryptographic security. Similarly, databases constructed with CoreData or standard SQLite do not encrypt their tables on-disk unless specifically configured with an encryption adapter like SQLCipher or when using iOS Data Protection classes.
- **Android Mechanics**: Standard `SharedPreferences` writes data in plain XML formats to the application's private storage path (`/data/data/your.package/shared_prefs/`).

### 1.3 Best Practice Recommendations
1. **Never Store Secrets in Cleartext**: Migrate all sensitive key-value pairs out of default storage containers.
2. **Implement Jetpack Security**: On Android, replace plain `SharedPreferences` with `EncryptedSharedPreferences`. This API automatically encrypts both keys and values using AES-256-SIV (for keys) and AES-256-GCM (for values), storing its master cryptographic keys in the hardware-backed Android Keystore.
3. **Utilize iOS Keychain Services**: On iOS, leverage the iOS Keychain for critical session credentials and secrets.
4. **Implement SQLite/Room Encryption**: For larger datasets or SQLite/Room relational databases, enforce local on-disk encryption using SQLCipher, deriving the decryption key dynamically from a hardware-backed enclave.
5. **Apply Data Protection Classes**: Specify write options such as `Data.WritingOptions.completeFileProtection` when persisting files to the iOS file system, ensuring files are automatically encrypted and unreadable when the device is locked.

---

## 2. Keychain (iOS Specific)

### 2.1 Overview
The iOS Keychain Services API provides a hardware-accelerated, highly secure sandbox managed directly by the operating system. It isolates sensitive keys and passwords, shielding them from other sandbox applications.

### 2.2 Platform-Specific Mechanics
The behavior of items in the Keychain is determined by accessibility attributes (`kSecAttrAccessible`). These attributes define when the item can be read by the application and whether it can migrate to other physical devices during backups.

### 2.3 Best Practice Recommendations
1. **Enforce Strict Accessibility Attributes**: Always declare the most restrictive accessibility class when executing `SecItemAdd` or `SecItemUpdate` operations:
   - `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`: Highly recommended for applications utilizing background services or push notifications. Data is available after the first device unlock and cannot be transferred to other devices via backups.
   - `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`: Best for foreground-only applications. Data is only readable when the screen is active and unlocked, and is never backed up.
2. **Avoid Deprecated Classes**: Avoid deprecated attributes such as `kSecAttrAccessibleAlways` or classes that permit credential cloning across hardware environments unless explicitly designed for cross-device migration.
3. **Restrict Access Groups**: Narrowly limit any `kSecAttrAccessGroup` declarations. Restrict keychain sharing strictly to trusted applications belonging to the same Developer Team ID.
4. **Disable iCloud Synchronization**: Ensure that `kSecAttrSynchronizable` is explicitly set to `false` unless iCloud Keychain synchronization is a declared product requirement.

---

## 3. Android Keystore (Android Specific)

### 3.1 Overview
The Android Keystore system is a system-level cryptographic provider that lets developers generate and store private keys within a hardware-backed environment. This container makes keys extremely difficult to extract even if the device's main operating system is fully compromised.

### 3.2 Platform-Specific Mechanics
Android isolates keys using the Trusted Execution Environment (TEE) or dedicated physical hardware modules known as StrongBox Security Chips (introduced in Android 9, API 28).

### 3.3 Best Practice Recommendations
1. **Enforce StrongBox Hardware Backing**: Always request dedicated hardware-backed key storage by invoking `setIsStrongBoxBacked(true)` during `KeyGenParameterSpec` creation on compatible hardware.
2. **Validate Hardware Containment**: Programmatically verify that the generated keys reside inside secure hardware by calling `KeyInfo.isInsideSecureHardware()` after key instantiation.
3. **Enforce Key Attestation**: For highly sensitive applications (e.g., financial and banking apps), implement cryptographic Key Attestation. This mathematically proves to a remote backend server that the key pair was created inside secure hardware and has not been tampered with.
4. **Restrict Cryptographic Scope**: Explicitly constrain key purposes upon initialization:
   - Restrict capabilities specifically (e.g., allow ONLY decryption and encryption with `KeyProperties.PURPOSE_ENCRYPT` and `KeyProperties.PURPOSE_DECRYPT`).
   - Use secure block modes like `KeyProperties.BLOCK_MODE_GCM` and block unpadded configurations by specifying `KeyProperties.ENCRYPTION_PADDING_NONE`.
5. **Configure Auth-Gated Keys**: Associate key usage with user presence by configuring `.setUserAuthenticationRequired(true)` combined with `.setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)`.

---

## 4. Biometric Authentication

### 4.1 Overview
Biometric authentication mechanisms (iOS FaceID/TouchID, Android BiometricPrompt) verify a user's physical presence. A common vulnerability is treating biometric authentication as a simple client-side UI gate that resolves to a boolean return (e.g., `isSuccess == true`). Attackers can easily bypass these checks at runtime using dynamic instrumentation engines like Frida to hook and spoof the boolean return values.

### 4.2 Platform-Specific Mechanics
- **iOS Mechanics**: Standard LocalAuthentication (`LAContext.evaluatePolicy`) is vulnerable to hooking if used standalone to authorize access without an underlying cryptographic secret.
- **Android Mechanics**: `BiometricPrompt` can be initiated with a `BiometricPrompt.CryptoObject` parameter, binding the authentication action directly to a hardware-backed cipher.

### 4.3 Best Practice Recommendations
1. **Implement Crypto-Backed Biometrics**: Always bind the biometric challenge to a cryptographic operation. Instead of merely checking a boolean, require the biometric prompt to unlock a key in the secure hardware vault.
2. **iOS SecAccessControl Binding**: Create Keychain credentials utilizing `SecAccessControlCreateWithFlags` with constraints such as `.biometryAny` or `.biometryCurrentSet`. The operating system will automatically prompt the user for biometrics and will release the decrypted token only upon successful authentication.
3. **Android CryptoObject Passing**: Initialize a `Cipher`, `Signature`, or `Mac` instance tied to a user-authentication-required Keystore key. Pass this instance wrapped in a `BiometricPrompt.CryptoObject` to `biometricPrompt.authenticate()`. This ensures that the cryptographic key is only authorized to sign or decrypt when the user successfully passes biometric verification.
4. **Detect Biometric State Changes**: Track changes in the biometric enrollment template database (e.g., on iOS, check the evaluation of `evaluatedPolicyDomainState`). Invalidate or force a re-login if new faces or fingerprints are added to the device.

---

## 5. Certificate Pinning

### 5.1 Overview
Certificate pinning (or public-key pinning) hardcodes the expected server certificate or public key hash directly within the client application. This mitigates Man-in-the-Middle (MITM) attacks by ensuring that the client rejects any connection to a spoofed server, even if the device has a user-approved malicious root certificate installed (e.g., corporate proxies, decryption firewalls, or malware).

### 5.2 Platform-Specific Mechanics
- **iOS Mechanics**: Pinning can be configured declaratively within the `Info.plist` using native Network Session Pinning (`NSPinnedDomains`).
- **Android Mechanics**: Enforced natively via the Network Security Configuration file (`res/xml/network_security_config.xml`).

### 5.3 Best Practice Recommendations
1. **Pin Subject Public Key Info (SPKI)**: Never pin the raw leaf certificate itself, as standard certificate rotations or emergency renewals will brick the client application. Pin the SHA-256 hash of the Subject Public Key Info (SPKI).
2. **Provide Backup Pins**: Always declare at least one backup pin pointing to a separate Certificate Authority (CA) or standby intermediate certificate to ensure continuity during an emergency server certificate rotation.
3. **Use Declarative Network Configurations**:
   - On iOS, define domain configurations within the `Info.plist` under the `NSPinnedDomains` key. This minimizes custom delegation code which is prone to implementation errors.
   - On Android, define pins in `network_security_config.xml` under a `<pin-set>` block:
     ```xml
     <network-security-config>
         <domain-config>
             <domain includeSubdomains="true">api.mycompany.com</domain>
             <pin-set expiration="2026-12-31">
                 <pin digest="SHA-256">PrimarySPKIHashValue=</pin>
                 <pin digest="SHA-256">BackupSPKIHashValue=</pin>
             </pin-set>
         </domain-config>
     </network-security-config>
     ```
4. **Enforce Certificate Expiration Bounds**: Set realistic expiration dates on pin sets, ensuring that app updates can gracefully roll over pins prior to certificate expiration.

---

## 6. Jailbreak Detection (iOS)

### 6.1 Overview
A jailbroken iOS device circumvents crucial operating system kernel protections, rendering the client-side sandbox and storage completely accessible to attackers. Jailbreak detection must detect these compromised states and gracefully terminate or isolate sensitive functions.

### 6.2 Platform-Specific Mechanics
Jailbreaks rely on modifying file system permissions, mounting dynamic linking hooks (e.g., Cydia Substrate, Frida), and writing out administrative binaries.

### 6.3 Best Practice Recommendations
1. **Implement Multi-Layered Heuristic Audits**: Never rely on a single file check. Combine multiple independent indicators:
   - **File System Indicators**: Inspect standard directories for jailbreak binaries, package managers, and dynamic libraries (e.g., `/Applications/Cydia.app`, `/Applications/Sileo.app`, `/usr/sbin/sshd`, `/Library/MobileSubstrate/MobileSubstrate.dylib`, `/bin/bash`).
   - **Sandbox Writing Attempt**: Attempt to write a temporary text file outside the application sandbox (e.g., to `/private/jailbreak.txt`). Standard apps will fail with a write error, while a jailbroken app with elevated root permissions may succeed.
   - **Symlink Integrity Check**: Verify if common system folders (such as `/Applications` or `/Library/Ringtones`) have been replaced with symbolic links, a common storage-saving technique utilized by jailbreak wrappers.
   - **Dynamic Linker (dyld) Inspection**: Iterate over loaded dynamic libraries to detect active dynamic analysis engines or runtime injection tools (such as `Frida`, `CydiaSubstrate`, `Substitute`).
2. **Enforce Graceful Degradation or Termination**: If a compromised state is detected, securely wipe all cached session keys and localized databases, alert the user, and terminate the session.

---

## 7. Root Detection (Android)

### 7.1 Overview
Root access on Android compromises the security architecture of the Linux kernel, allowing rogue applications to inspect other apps' private memory, steal database assets, and spoof runtime outcomes.

### 7.2 Platform-Specific Mechanics
Local root detection heuristics check for custom ROM configurations or binary indicators on the system partition. However, modern rooting utilities (e.g., Magisk Hide, Zygisk) hide these indicators from local apps.

### 7.3 Best Practice Recommendations
1. **Perform Local Heuristic Checks**:
   - **SU Binary Search**: Scan standard environment paths for the presence of superuser binaries (e.g., `/system/bin/su`, `/system/xbin/su`, `/sbin/su`, `/system/sd/xbin/su`).
   - **Build Tag Auditing**: Read `android.os.Build.TAGS` and verify that they do not contain `"test-keys"`, which indicates a custom or developer ROM image.
   - **Package Indexing**: Search for root management package signatures in the package list (e.g., `com.topjohnwu.magisk`, `eu.chainfire.supersu`, `com.noshufou.android.su`).
2. **Mandate Hardware-Backed Attestation (Google Play Integrity API)**:
   - Local heuristic root checks are easily bypassed. Therefore, high-security applications must implement the **Google Play Integrity API**.
   - Call the Play Integrity API from the client application, retrieve the signed token, and forward it directly to your remote backend server.
   - Decrypt, parse, and verify the integrity verdict token on your backend. Ensure the device meets the `MEETS_DEVICE_INTEGRITY` or `MEETS_STRONG_INTEGRITY` assertions before granting session tokens or processing transactions.

---

## 8. SSL Configuration

### 8.1 Overview
Weak Transport Layer Security (TLS) implementations leave mobile applications vulnerable to credential harvesting and traffic injection. Cleartext HTTP communication must be entirely disabled in production configurations.

### 8.2 Platform-Specific Mechanics
- **iOS Mechanics**: Controlled by App Transport Security (ATS) parameters in the `Info.plist`.
- **Android Mechanics**: Managed via `android:usesCleartextTraffic` in the manifest or globally configured through the Network Security Configuration file.

### 8.3 Best Practice Recommendations
1. **Enforce TLS 1.3 or TLS 1.2 Minimum**: Explicitly reject outdated protocols including SSL v3, TLS 1.0, and TLS 1.1.
2. **Disable Cleartext Traffic**:
   - On iOS, ensure `NSAllowsArbitraryLoads` is set to `false`. If specific legacy API endpoints require exceptions, declare them explicitly under `NSExceptionDomains` with strict, review-ready justifications.
   - On Android, configure `android:usesCleartextTraffic="false"` inside the `<application>` tag of `AndroidManifest.xml`.
3. **Configure System-Trust Base Anchors**: Establish a strict base networking trust model globally in your `network_security_config.xml`:
   ```xml
   <network-security-config>
       <base-config cleartextTrafficPermitted="false">
           <trust-anchors>
               <certificates src="system" />
           </trust-anchors>
       </base-config>
   </network-security-config>
   ```
4. **Reject User-Added Certificates in Production**: Do not permit user-installed certificates (e.g., `<certificates src="user" />`) in production build profiles to prevent end-user proxy interception.

---

## 9. Backup Rules

### 9.1 Overview
By default, mobile operating systems include application sandboxed data in automated, user-accessible backups (such as iCloud backups on iOS and ADB / Google Drive backups on Android). This means private files, logs, and databases are automatically extracted and stored on remote cloud platforms or local desktop machines.

### 9.2 Platform-Specific Mechanics
- **iOS Mechanics**: Files written to the local documents or cache folders are automatically included in system backups unless marked with explicit exclusion resources.
- **Android Mechanics**: Automated backup is active by default on any application declaring `android:allowBackup="true"`. This allows local file systems to be extracted using basic ADB desktop tools.

### 9.3 Best Practice Recommendations
1. **Enforce iOS Backup Exclusions**: Explicitly configure the `.isExcludedFromBackup` metadata attribute on any sensitive localized database, config file, or token storage path:
   ```swift
   var targetURL = URL(fileURLWithPath: localPath)
   var resourceValues = URLResourceValues()
   resourceValues.isExcludedFromBackup = true
   try targetURL.setResourceValues(resourceValues)
   ```
2. **Secure Android Backup Directives**:
   - For high-security applications, completely disable backup mechanisms inside `AndroidManifest.xml`:
     ```xml
     <application android:allowBackup="false" ...>
     ```
   - If backups are required, strictly configure `android:dataExtractionRules` (for Android 12+) and `android:fullBackupContent` (for Android 11-) to filter and target only safe directory nodes.
3. **Explicitly Exclude Secrets**: Exclude databases and SharedPreferences that hold session credentials:
   ```xml
   <!-- res/xml/data_extraction_rules.xml -->
   <data-extraction-rules>
       <cloud-backup>
           <exclude domain="sharedpref" path="auth_tokens.xml" />
           <exclude domain="database" path="user_session.db" />
       </cloud-backup>
       <device-to-device-backup>
           <exclude domain="sharedpref" path="auth_tokens.xml" />
           <exclude domain="database" path="user_session.db" />
       </device-to-device-backup>
   </data-extraction-rules>
   ```

---

## 10. Exported Activities (Android Specific)

### 10.1 Overview
Android components (Activities, Services, Broadcast Receivers) declared in `AndroidManifest.xml` can be launched by any other application running on the same device if they are marked as "exported". Unintentionally exporting components allows attackers to bypass authentication gates, inject malicious payloads, or manipulate application state.

### 10.2 Platform-Specific Mechanics
In Android 12 (API 31) and higher, the operating system strictly requires all components declaring intent filters to explicitly define `android:exported`. If a component contains an intent filter but lacks the tag, the application will fail compilation or installation.

### 10.3 Best Practice Recommendations
1. **Apply a Closed-by-Default Policy**: Set `android:exported="false"` for all internal Activities, Services, and Broadcast Receivers.
2. **Protect Mandatory Exported Components**:
   - If an activity must be exported (e.g., launching from the home screen, handling custom intents, or receiving callbacks), protect access using custom permissions:
     ```xml
     <activity android:name=".InternalDashboardActivity"
               android:exported="true"
               android:permission="com.mycompany.myapp.PERMISSION_LAUNCH_DASHBOARD">
     ```
3. **Enforce Signature-Level Permissions**: Configure custom permissions using the `"signature"` protection level. This guarantees that only applications signed with the exact same developer certificate can launch the exported component:
   ```xml
   <permission android:name="com.mycompany.myapp.PERMISSION_LAUNCH_DASHBOARD"
               android:protectionLevel="signature" />
   ```

---

## 11. Intent Filters (Android Specific)

### 11.1 Overview
Intent filters define which implicit intents an application component can respond to. Registering an intent filter automatically marks the component as exported by default, exposing it to untrusted applications on the device.

### 11.2 Platform-Specific Mechanics
Untrusted applications can send crafted implicit intents to intercept broadcast parameters, spoof events, or hijack active flows.

### 11.3 Best Practice Recommendations
1. **Validate and Sanitize Caller Identity**: Before executing business logic inside an exported component, verify the calling application's identity using `getCallingPackage()` or `getCallingActivity()`. Compare the caller's package certificate fingerprint against a known trust store.
2. **Utilize Explicit Intents for Internal Actions**: When launching internal components, always use explicit intents (specifying the exact target class or package name) instead of implicit intent configurations. This prevents third-party applications from intercepting or hijacking the intent:
   ```kotlin
   val targetIntent = Intent(context, InternalTargetActivity::class.java).apply {
       putExtra("payload_key", payloadData)
   }
   context.startActivity(targetIntent)
   ```
3. **Restrict Broadcast Receiver Access**: When registering dynamic broadcast receivers at runtime, specify receiver permissions and register them with `Context.RECEIVER_NOT_EXPORTED` on Android 13+ to block external injection.

---

## 12. Deep Links

### 12.1 Overview
Deep links let external sources launch specific screens or actions within your app. Standard custom URL schemes (e.g., `myapp://profile`) are inherently insecure because any other application can register the same custom scheme. This can lead to deep link hijacking, allowing malicious apps to steal session codes, access tokens, or sensitive parameters.

### 12.2 Platform-Specific Mechanics
Deep links bypass standard web verification protocols. Standard scheme deep links rely solely on local operating system registration, making them susceptible to collision and interception.

### 12.3 Best Practice Recommendations
1. **Treat Inputs as Untrusted**: Never assume incoming deep link parameters are safe. Always sanitize, validate, and parse deep link parameters to prevent SQL injection, path traversal, or code execution.
2. **Never Transmit Secrets**: Never pass sensitive authorization assets, session keys, passwords, or transactional details in a deep link URL.
3. **Utilize Single-Use Authorization Challenges**: If utilizing deep links for user login (e.g., magic login links), do not transmit active session tokens. Instead, pass a short-lived, single-use, cryptographically strong challenge token.
4. **Exchange Tokens securely**: Exchanged the single-use token on your remote server via a secure, explicit HTTPS API call from the app, and issue the active session token over that secure channel.

---

## 13. Universal Links (iOS Specific)

### 13.1 Overview
Universal Links are iOS's secure deep-linking mechanism. Instead of relying on custom URL schemes, they use standard HTTPS links (e.g., `https://mycompany.com/profile`). Universal Links cannot be hijacked or duplicated because domain ownership is validated against the website's configuration.

### 13.2 Platform-Specific Mechanics
iOS verifies the relationship between the application and the domain during installation. This verification is performed by downloading an association configuration file directly from the domain.

### 13.3 Best Practice Recommendations
1. **Configure a Valid AASA File**: Publish a valid **Apple App Site Association (AASA)** file on your web server at `https://yourdomain.com/.well-known/apple-app-site-association`.
2. **Verify Server Content-Type**: Ensure the AASA file is served with a `Content-Type: application/json` header, directly without HTTP redirects, and over a secure HTTPS connection.
3. **Define explicit Application Routing Bounds**: Specify only the required routing patterns inside the AASA file:
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
4. **Declare Associated Domains**: Enable the "Associated Domains" capability in Xcode, declaring the domains in the format `applinks:yourdomain.com`.

---

## 14. App Links (Android Specific)

### 14.1 Overview
Android App Links are secure deep links that use standard HTTPS. By verifying domain ownership, App Links route traffic directly to your application without showing a platform "disambiguation dialog".

### 14.2 Platform-Specific Mechanics
Android verifies the relationship between your application and your website domain during installation. This verification is performed by fetching a JSON file from the domain's well-known path.

### 14.3 Best Practice Recommendations
1. **Host a Digital Asset Links File**: Publish a valid **Digital Asset Links** JSON file on your web server at `https://yourdomain.com/.well-known/assetlinks.json`.
2. **Declare Domain Ownership**: Link the application package name directly to the SHA-256 fingerprint of your app's signing certificate:
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
3. **Enforce Manifest Verification**: Add `android:autoVerify="true"` to the intent filter in `AndroidManifest.xml` to instruct the OS to verify domain ownership on installation:
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
Mobile authentication processes must secure credentials, prevent the leakage of server-side secrets in app binaries, and implement cryptographic challenges to prevent replay attacks.

### 15.2 Platform-Specific Mechanics
Hardcoding client secrets inside mobile binaries is a critical security vulnerability. Attackers can easily extract these secrets using basic static reverse-engineering tools.

### 15.3 Best Practice Recommendations
1. **Enforce OAuth 2.1 with PKCE**: Always implement **Proof Key for Code Exchange (PKCE)** (RFC 7636) for mobile OAuth 2.0 integrations. PKCE eliminates the need to embed client secrets in your source code and protects the authorization code exchange from interception.
2. **Utilize Secure System Browsers**: Use secure, system-provided browser components for authentication flows:
   - On iOS, implement **ASWebAuthenticationSession**.
   - On Android, implement **Custom Tabs**.
3. **Avoid Embedded WebViews**: Do not use embedded `WKWebView` or Android `WebView` components for login screens. These components allow the hosting application to inspect, log, or manipulate user credentials and keystrokes.
4. **Implement Cryptographic State Verification**: Include a cryptographically strong, random `state` and `nonce` parameter in all authorization requests to prevent cross-site request forgery and replay attacks.

---

## 16. Session Handling

### 16.1 Overview
Mobile session tokens must be securely generated, properly scoped, periodically rotated, and gracefully invalidated both locally and on the server.

### 16.2 Platform-Specific Mechanics
Relying solely on local token deletion during logout leaves orphan sessions active on the server, exposing users to session hijacking.

### 16.3 Best Practice Recommendations
1. **Enforce Server-Side Validation**: Never rely on local client-side assumptions about session validity. Always validate session tokens on your remote backend for every critical request.
2. **Implement Complete Server-Side Logout**: When a user logs out, perform a complete session invalidation on the backend server. Concurrently, clear all local access and refresh tokens, cookies, and local database keys on the device.
3. **Secure Background Multitasking**:
   - Clear sensitive UI layouts, transaction details, and cached memory references when the application transitions to the background.
   - Implement **multitasking screen blurring** to prevent sensitive user information from leaking into system multitasking snapshots.
4. **Configure Session Timeouts**: Enforce strict session expiration policies on both short-lived access tokens and refresh tokens.

---

## 17. Token Storage

### 17.1 Overview
Tokens (Access Tokens, Refresh Tokens, JWTs) are highly sensitive credentials. If leaked, they allow full unauthorized access to the user's account and data.

### 17.2 Best Practice Recommendations
1. **Isolate Token Storage**: Store all access and refresh tokens strictly inside secure hardware-backed containers:
   - On iOS, store tokens in the **iOS Keychain**.
   - On Android, store tokens in **EncryptedSharedPreferences** or a hardware-encrypted SQLite database.
2. **Never Write Tokens to Storage Cleartext**: Do not write tokens to regular files, unencrypted SQLite databases, or local device caches.
3. **Enforce Logging Controls**: Never print sensitive session keys or refresh tokens to standard device logs (`NSLog`, `print`, `Log.d`).
4. **Isolate and Rotate Refresh Tokens**: Use short-lived access tokens (e.g., 15 minutes) and rotate the long-lived refresh token on every single invocation.
