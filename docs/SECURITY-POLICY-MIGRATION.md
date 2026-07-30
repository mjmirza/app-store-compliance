<!-- SECURITY_POLICY_MONITOR_START -->
# Mobile Security Requirements Policy Migration & Compliance Report

This report is continuously generated and updated by `scripts/monitor-security.py` to track security compliance.

## Monitored Security Guidelines Update Log

### 1. [secure storage] NIST Guidelines on Mobile Data Protection
- **Published Date**: Fri, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://pages.nist.gov/Mobile-Threat-Catalogue/](https://pages.nist.gov/Mobile-Threat-Catalogue/)
- **Description**: NIST publishes updated recommendations on secure storage, mandating that all sensitive data must be encrypted using strong cryptographic systems such as AES-256 and SQLCipher, rather than unencrypted standard options like UserDefaults or plain SharedPreferences.

### 2. [Keychain] Apple Security Update: iOS Keychain Protection Class Enforcement
- **Published Date**: Sat, 16 May 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/security/](https://developer.apple.com/security/)
- **Description**: Apple security teams release advisory enforcing the use of strict Keychain accessibility attributes. Developers are instructed to use kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly to prevent unauthorized backup extraction and access group leaks.

### 3. [Android Keystore] Android Keystore Security Advisory on StrongBox Hardware Backing
- **Published Date**: Sun, 17 May 2026 12:00:00 GMT
- **Official Resource**: [https://source.android.com/docs/security/](https://source.android.com/docs/security/)
- **Description**: Google publishes Android Keystore guidelines requiring StrongBox hardware protection on devices that support it. Developers must use KeyGenParameterSpec to generate keys inside secure hardware and check isInsideSecureHardware at runtime.

### 4. [Keychain] OWASP MASVS Biometric Bypass Protection and Cryptographic Binding
- **Published Date**: Mon, 18 May 2026 13:00:00 GMT
- **Official Resource**: [https://mas.owasp.org/MASVS/](https://mas.owasp.org/MASVS/)
- **Description**: OWASP updates MASVS biometric authentication requirements, specifying that biometric prompts must be backed by cryptographic keys in Keychain or Keystore via CryptoObject and SecAccessControl, and simple boolean success callbacks are fully deprecated to prevent runtime instrument hooks.

### 5. [biometric authentication] OWASP MASVS Biometric Bypass Protection and Cryptographic Binding
- **Published Date**: Mon, 18 May 2026 13:00:00 GMT
- **Official Resource**: [https://mas.owasp.org/MASVS/](https://mas.owasp.org/MASVS/)
- **Description**: OWASP updates MASVS biometric authentication requirements, specifying that biometric prompts must be backed by cryptographic keys in Keychain or Keystore via CryptoObject and SecAccessControl, and simple boolean success callbacks are fully deprecated to prevent runtime instrument hooks.

### 6. [certificate pinning] ENISA Advisory on Certificate Pinning and Subject Public Key Info Hashes
- **Published Date**: Tue, 19 May 2026 14:00:00 GMT
- **Official Resource**: [https://www.enisa.europa.eu/publications](https://www.enisa.europa.eu/publications)
- **Description**: ENISA recommends certificate pinning using Subject Public Key Info SPKI hashes rather than full certificates. The advisory stresses utilizing NSPinnedDomains natively on iOS and network_security_config on Android with robust backup pin definitions.

### 7. [jailbreak detection] Apple Security Brief on Multi-layered Jailbreak Detection
- **Published Date**: Wed, 20 May 2026 15:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/downloads/](https://developer.apple.com/support/downloads/)
- **Description**: An official iOS security brief details the evasion tactics of jailbreak tools. App developers are advised to employ multi-layered detection heuristics, checking for Cydia, MobileSubstrate, and verifying dyld dynamic linkers rather than single boolean checks.

### 8. [root detection] Google Play Integrity API Integration for Robust Root Detection
- **Published Date**: Thu, 21 May 2026 16:00:00 GMT
- **Official Resource**: [https://developer.android.com/google/play/integrity](https://developer.android.com/google/play/integrity)
- **Description**: Google Play updates security rules, mandating hardware-backed Play Integrity API tokens for sensitive operations. Traditional local root detection (Magisk, su checks) must be paired with server-side signature verification of Integrity tokens.

### 9. [SSL configuration] CISA Bulletin on Disabling Cleartext HTTP Traffic in Production
- **Published Date**: Fri, 22 May 2026 17:00:00 GMT
- **Official Resource**: [https://www.cisa.gov/news-events/directives](https://www.cisa.gov/news-events/directives)
- **Description**: CISA issues a directive requiring mobile apps to completely disable cleartext HTTP traffic. App Transport Security ATS NSAllowsArbitraryLoads must be false on iOS, and usesCleartextTraffic must be false in Android manifests to mitigate active MITM interception.

### 10. [backup rules] Federal Trade Commission Advice on Mobile App Backup Rules
- **Published Date**: Sat, 23 May 2026 18:00:00 GMT
- **Official Resource**: [https://www.ftc.gov/business-guidance/](https://www.ftc.gov/business-guidance/)
- **Description**: The FTC alerts developers to secure mobile app backups. On Android, allowBackup must be false or dataExtractionRules configured to exclude local authentication tokens, databases, and preferences from cloud or adb backups to prevent credential leakage.

### 11. [exported activities] Android Vulnerability Report on Exported Activities and Intent Redirection
- **Published Date**: Sun, 24 May 2026 19:00:00 GMT
- **Official Resource**: [https://source.android.com/docs/security/bulletin](https://source.android.com/docs/security/bulletin)
- **Description**: A high-severity vulnerability report warns against setting android:exported to true without signature-level permission restrictions. Unprotected exported components expose internal business logic and can bypass authentication.

### 12. [intent filters] NIST Mobile Security on Intent Spoofing and Intent Filters Protection
- **Published Date**: Mon, 25 May 2026 20:00:00 GMT
- **Official Resource**: [https://pages.nist.gov/Mobile-Threat-Catalogue/](https://pages.nist.gov/Mobile-Threat-Catalogue/)
- **Description**: NIST releases guidelines on inter-process communication safety, requiring validation of implicit intents with getCallingPackage and getCallingActivity to block intent spoofing, and recommending explicit intents for internal app components.

### 13. [deep links] CISA Advisory on Custom URL Scheme Deep Link Hijacking Vulnerabilities
- **Published Date**: Tue, 26 May 2026 21:00:00 GMT
- **Official Resource**: [https://www.cisa.gov/news-events/alerts](https://www.cisa.gov/news-events/alerts)
- **Description**: CISA highlights deep link hijacking risks where multiple apps register identical custom URL schemes. Apps are advised to never transmit session tokens or credentials in deep links, and sanitize all parsed incoming parameters.

### 14. [session handling] CISA Advisory on Custom URL Scheme Deep Link Hijacking Vulnerabilities
- **Published Date**: Tue, 26 May 2026 21:00:00 GMT
- **Official Resource**: [https://www.cisa.gov/news-events/alerts](https://www.cisa.gov/news-events/alerts)
- **Description**: CISA highlights deep link hijacking risks where multiple apps register identical custom URL schemes. Apps are advised to never transmit session tokens or credentials in deep links, and sanitize all parsed incoming parameters.

### 15. [deep links] Apple Security Update: Universal Links Domain Verification Guidelines
- **Published Date**: Wed, 27 May 2026 22:00:00 GMT
- **Official Resource**: [https://developer.apple.com/security/](https://developer.apple.com/security/)
- **Description**: Apple security highlights guidelines on secure domain verification. Developers must host valid apple-app-site-association AASA files on HTTPS domains and declare matching Associated Domains in entitlements to prevent deep link spoofing.

### 16. [universal links] Apple Security Update: Universal Links Domain Verification Guidelines
- **Published Date**: Wed, 27 May 2026 22:00:00 GMT
- **Official Resource**: [https://developer.apple.com/security/](https://developer.apple.com/security/)
- **Description**: Apple security highlights guidelines on secure domain verification. Developers must host valid apple-app-site-association AASA files on HTTPS domains and declare matching Associated Domains in entitlements to prevent deep link spoofing.

### 17. [app links] Android App Links Auto-Verification and AssetLinks Configuration Mandate
- **Published Date**: Thu, 28 May 2026 23:00:00 GMT
- **Official Resource**: [https://developer.android.com/training/app-links](https://developer.android.com/training/app-links)
- **Description**: Google publishes Android App Links verification requirements, emphasizing assetlinks.json configuration and autoVerify true in AndroidManifest.xml, guaranteeing secure and direct domain-app association.

### 18. [authentication flows] OAuth 2.1 and PKCE Requirement Mandate for Mobile Apps
- **Published Date**: Fri, 29 May 2026 09:00:00 GMT
- **Official Resource**: [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- **Description**: The IETF OAuth Working Group advances OAuth 2.1, making Proof Key for Code Exchange PKCE mandatory for mobile applications. Mobile authentication must rely on ASWebAuthenticationSession or Custom Tabs instead of embedded webviews to protect secrets.

### 19. [session handling] OAuth 2.1 and PKCE Requirement Mandate for Mobile Apps
- **Published Date**: Fri, 29 May 2026 09:00:00 GMT
- **Official Resource**: [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- **Description**: The IETF OAuth Working Group advances OAuth 2.1, making Proof Key for Code Exchange PKCE mandatory for mobile applications. Mobile authentication must rely on ASWebAuthenticationSession or Custom Tabs instead of embedded webviews to protect secrets.

### 20. [session handling] NIST Guidance on Mobile Session Invalidation and Background Blurring
- **Published Date**: Sat, 30 May 2026 10:00:00 GMT
- **Official Resource**: [https://pages.nist.gov/Mobile-Threat-Catalogue/](https://pages.nist.gov/Mobile-Threat-Catalogue/)
- **Description**: NIST recommendations for high-assurance session handling include immediate server-side validation, short-lived tokens, complete local cache purge upon logout, and background blurring of multitasking window views to protect sensitive data screens.

### 21. [biometric authentication] OWASP MASVS Token Storage and Access Isolation Advisory
- **Published Date**: Sun, 31 May 2026 11:00:00 GMT
- **Official Resource**: [https://mas.owasp.org/MASVS/](https://mas.owasp.org/MASVS/)
- **Description**: OWASP MASVS updates token protection guidance, requiring short-lived access tokens and isolating long-lived refresh tokens using biometrics or hardware backing. Tokens must never be printed to logs or stored in plain local databases.

### 22. [token storage] OWASP MASVS Token Storage and Access Isolation Advisory
- **Published Date**: Sun, 31 May 2026 11:00:00 GMT
- **Official Resource**: [https://mas.owasp.org/MASVS/](https://mas.owasp.org/MASVS/)
- **Description**: OWASP MASVS updates token protection guidance, requiring short-lived access tokens and isolating long-lived refresh tokens using biometrics or hardware backing. Tokens must never be printed to logs or stored in plain local databases.

## Automated Security Migration Recommendations & Tasks

### Security tasks for secure storage
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task 1**: Replace plain SharedPreferences and UserDefaults with EncryptedSharedPreferences or Keychain wrappers.
- [ ] **Task 2**: Encrypt local database assets using SQLCipher or system-level Data Protection files.

### Security tasks for Keychain
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for Keychain.

### Security tasks for Android Keystore
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for Android Keystore.

### Security tasks for Keychain
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for Keychain.

### Security tasks for biometric authentication
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task 1**: Refactor local FaceID/TouchID prompts to release hardware-backed Keystore/Keychain keys.
- [ ] **Task 2**: Eliminate local boolean check dependencies from authentication controllers.

### Security tasks for certificate pinning
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task 1**: Configure native NSPinnedDomains or network_security_config SPKI base64 hashes.
- [ ] **Task 2**: Declare secondary standby backup public key pins.

### Security tasks for jailbreak detection
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for jailbreak detection.

### Security tasks for root detection
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for root detection.

### Security tasks for SSL configuration
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for SSL configuration.

### Security tasks for backup rules
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task 1**: Set allowBackup to false in manifest, or define robust dataExtractionRules files.
- [ ] **Task 2**: Set the isExcludedFromBackup flag on all local storage URL folders.

### Security tasks for exported activities
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for exported activities.

### Security tasks for intent filters
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for intent filters.

### Security tasks for deep links
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for deep links.

### Security tasks for session handling
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for session handling.

### Security tasks for deep links
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for deep links.

### Security tasks for universal links
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for universal links.

### Security tasks for app links
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for app links.

### Security tasks for authentication flows
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for authentication flows.

### Security tasks for session handling
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for session handling.

### Security tasks for session handling
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for session handling.

### Security tasks for biometric authentication
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task 1**: Refactor local FaceID/TouchID prompts to release hardware-backed Keystore/Keychain keys.
- [ ] **Task 2**: Eliminate local boolean check dependencies from authentication controllers.

### Security tasks for token storage
- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution.
- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for token storage.

<!-- SECURITY_POLICY_MONITOR_END -->