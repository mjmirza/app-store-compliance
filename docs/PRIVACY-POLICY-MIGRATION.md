<!-- PRIVACY_POLICY_MONITOR_START -->
# Mobile and Web Privacy Compliance Migration & Requirements Report

This report is continuously generated and updated by scripts/monitor-privacy.py to track active privacy compliance gaps.

## Monitored Requirements Update Log

### 1. [Privacy Manifest] Apple App Store Upload Enforcement for Privacy Manifests
- **Published Date**: Mon, 18 May 2026 10:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-manifest-enforce](https://developer.apple.com/news/?id=privacy-manifest-enforce)
- **Description**: Apple announced final enforcement of Privacy Manifest files. Submissions containing unrecognized or missing PrivacyInfo.xcprivacy configurations will be immediately rejected at the App Store Connect upload-time gate.

### 2. [Required Reason APIs] Stricter Verification on Required Reason APIs
- **Published Date**: Tue, 19 May 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=required-reason-apis](https://developer.apple.com/news/?id=required-reason-apis)
- **Description**: Apple is initiating rigorous automated checking for system uptime, file timestamp, and user default API calls. Developers must match each call to an approved reason code in their bundled manifest.

### 3. [App Tracking Transparency] Enhanced ATT Enforcement in Saturated Markets
- **Published Date**: Wed, 20 May 2026 12:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=att-enforce](https://developer.apple.com/news/?id=att-enforce)
- **Description**: The App Store Review team will reject applications accessing third-party tracking, analytics, or attribution services without exhibiting the App Tracking Transparency consent dialogue first.

### 4. [Privacy Nutrition Labels] App Store Privacy Nutrition Label Discrepancy Audits
- **Published Date**: Thu, 21 May 2026 13:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=nutrition-label-audits](https://developer.apple.com/news/?id=nutrition-label-audits)
- **Description**: Apple is updating review systems to audit network traffic of submitted apps, cross-referencing findings against declared Nutrition Labels. Discrepancies lead to immediate rejection.

### 5. [App Tracking Transparency] Google Play Store Data Safety Questionnaire Compliance
- **Published Date**: Fri, 22 May 2026 14:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/datasafety](https://support.google.com/googleplay/android-developer/answer/datasafety)
- **Description**: Google Play is updating Data Safety expectations. Apps sharing user data with external attribution or push notification services must declare these actions granularly to avoid account suspensions.

### 6. [Data Safety] Google Play Store Data Safety Questionnaire Compliance
- **Published Date**: Fri, 22 May 2026 14:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/datasafety](https://support.google.com/googleplay/android-developer/answer/datasafety)
- **Description**: Google Play is updating Data Safety expectations. Apps sharing user data with external attribution or push notification services must declare these actions granularly to avoid account suspensions.

### 7. [User Data Policy] Google Play Store Data Safety Questionnaire Compliance
- **Published Date**: Fri, 22 May 2026 14:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/datasafety](https://support.google.com/googleplay/android-developer/answer/datasafety)
- **Description**: Google Play is updating Data Safety expectations. Apps sharing user data with external attribution or push notification services must declare these actions granularly to avoid account suspensions.

### 8. [User Data Policy] Stricter Account Deletion and Personal Data Policy Requirements
- **Published Date**: Sat, 23 May 2026 15:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/userdata](https://support.google.com/googleplay/android-developer/answer/userdata)
- **Description**: Google Play reminds developers that apps permitting account creation must support in-app account deletion and must supply a valid, responsive web-based data deletion URL in the listing details.

### 9. [Advertising ID] Google Play Advertising ID Permission and Deletion Policy
- **Published Date**: Sun, 24 May 2026 16:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/adid-perm](https://support.google.com/googleplay/android-developer/answer/adid-perm)
- **Description**: Under Android 12+, developers targeting higher API levels who access the Advertising ID must explicitly declare the AD_ID permission in their manifest and provide opt-out preferences.

### 10. [Runtime permissions] Sensitive Scope Audits of Android Runtime Permissions
- **Published Date**: Mon, 25 May 2026 10:00:00 GMT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions](https://developer.android.com/guide/topics/permissions)
- **Description**: Google Play static analysis scans will flag apps declaring sensitive permissions in their AndroidManifest.xml if they bypass dynamic verification prompts or logical explanations.

### 11. [Background location] Enforcement Actions on ACCESS_BACKGROUND_LOCATION Declarations
- **Published Date**: Tue, 26 May 2026 11:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/bg-location](https://support.google.com/googleplay/android-developer/answer/bg-location)
- **Description**: Google is executing a strict sweep of background location access. Only highly essential user-facing features will be granted permission; all others must restrict location to foreground actions.

### 12. [Health permissions] Google Play Health Connect Data Permission Declarations
- **Published Date**: Wed, 27 May 2026 12:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/health-connect](https://support.google.com/googleplay/android-developer/answer/health-connect)
- **Description**: Apps interacting with Health Connect APIs must complete the dedicated health declaration form and must show a specialized in-app privacy policy prior to querying permissions.

### 13. [GDPR] EDPB Updates Guidelines on Cookie Consent and GDPR Data Erasure
- **Published Date**: Thu, 28 May 2026 13:00:00 GMT
- **Official Resource**: [https://edpb.europa.eu/our-work-tools/general-guidance](https://edpb.europa.eu/our-work-tools/general-guidance)
- **Description**: The European Data Protection Board finalized consent rules. Web entities are required to support clear consent revoke paths and ensure absolute right-to-erase triggers purge all analytical copies.

### 14. [Cookie consent] EDPB Updates Guidelines on Cookie Consent and GDPR Data Erasure
- **Published Date**: Thu, 28 May 2026 13:00:00 GMT
- **Official Resource**: [https://edpb.europa.eu/our-work-tools/general-guidance](https://edpb.europa.eu/our-work-tools/general-guidance)
- **Description**: The European Data Protection Board finalized consent rules. Web entities are required to support clear consent revoke paths and ensure absolute right-to-erase triggers purge all analytical copies.

### 15. [Cookie consent] European Union ePrivacy Compliance Sweep for Tracker Placement
- **Published Date**: Fri, 29 May 2026 14:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058)
- **Description**: ePrivacy updates mandate strict opt-in cookie banners. Non-essential cookies, analytics tools, or marketing pixels placed prior to explicit opt-in are subjected to direct regulatory prosecution.

### 16. [Local storage] OWASP Guidance on Client-Side Local Storage Security
- **Published Date**: Sat, 30 May 2026 15:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-web-security-testing-guide](https://owasp.org/www-project-web-security-testing-guide)
- **Description**: New OWASP security releases highlight threats regarding unencrypted JWTs, access credentials, or PII cached in localStorage. Developers are urged to shift sensitive secrets to secure HTTP-only cookies.

### 17. [GDPR] Structured Storage Security and Deletion Best Practices
- **Published Date**: Sun, 31 May 2026 16:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-web-security-testing-guide](https://owasp.org/www-project-web-security-testing-guide)
- **Description**: GDPR requirements mandate complete structured database cleanup. Ensure all tables and client objects created via IndexedDB are securely wiped during deletion flows or user account logout.

### 18. [IndexedDB] Structured Storage Security and Deletion Best Practices
- **Published Date**: Sun, 31 May 2026 16:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-web-security-testing-guide](https://owasp.org/www-project-web-security-testing-guide)
- **Description**: GDPR requirements mandate complete structured database cleanup. Ensure all tables and client objects created via IndexedDB are securely wiped during deletion flows or user account logout.

### 19. [Session storage] Session Hijacking Mitigation and Storage Restrictions
- **Published Date**: Mon, 01 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-web-security-testing-guide](https://owasp.org/www-project-web-security-testing-guide)
- **Description**: Security advisories emphasize locking sessionStorage objects during active browser cycles. Temporary secrets must be mitigated and cleared immediately upon session window termination.

### 20. [Tracking technologies] Directive Requirements on Third-Party Tracking Pixels
- **Published Date**: Tue, 02 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058)
- **Description**: Under regional guidelines, tracking pixels (Facebook, Google Analytics, Hotjar) cannot load or fetch telemetry metadata dynamically on page loading before obtaining consent.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifest (Apple Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### Tasks for Required Reason APIs (Apple Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] **Task 2**: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### Tasks for App Tracking Transparency (Apple Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Verify ATTrackingManager.requestTrackingAuthorization is called before starting any tracking.
- [ ] **Task 2**: Add NSUserTrackingUsageDescription with a clear reason explaining why tracking is used.

### Tasks for Privacy Nutrition Labels (Apple Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Conduct a data inventory to locate all points of user PII collection.
- [ ] **Task 2**: Verify that NSPrivacyCollectedDataTypes maps correctly to App Store Connect labels.

### Tasks for Data Safety (Android Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Audit all network endpoints and third-party SDKs for data collection activities.
- [ ] **Task 2**: Update the Play Console Data Safety questionnaire declarations to match the current state.

### Tasks for User Data Policy (Android Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Build explicit prominent disclosure dialogues shown before permission prompts or data ingestion.
- [ ] **Task 2**: Verify that in-app and web account deletion links are correctly active.

### Tasks for Advertising ID (Android Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Declare com.google.android.gms.permission.AD_ID in the manifest if using tracking features.
- [ ] **Task 2**: Ensure opt-out capability is supported by gracefully handling zeroed out identifiers.

### Tasks for Runtime permissions (Android Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Verify dynamic checks are present before accessing system hardware or personal data.
- [ ] **Task 2**: Test fallback paths to ensure graceful degradation if permissions are rejected.

### Tasks for Background location (Android Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Verify ACCESS_BACKGROUND_LOCATION is necessary, otherwise restrict location to foreground.
- [ ] **Task 2**: Implement a highly visible prominent disclosure detailing location usage in the background.

### Tasks for Health permissions (Android Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Complete the Health Connect declaration form in the Google Play Console.
- [ ] **Task 2**: Provide an in-app link to a specialized privacy policy covering sensitive health data.

### Tasks for GDPR (Web Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Validate that no personal data or tracking is initiated before consent is granted.
- [ ] **Task 2**: Offer a straightforward way for web users to request deletion of all collected personal data.

### Tasks for Cookie consent (Web Platform)
- **Severity Level**: CRITICAL
- [ ] **Task 1**: Implement or integrate a compliant cookie preference manager banner.
- [ ] **Task 2**: Audit all active scripts and delay analytical or marketing cookies until user opts in.

### Tasks for Local storage (Web Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Audit localStorage for occurrences of JWTs, credentials, or personal profiles.
- [ ] **Task 2**: Migrate sensitive session tokens to secure, HttpOnly, SameSite cookies.

### Tasks for IndexedDB (Web Platform)
- **Severity Level**: MEDIUM
- [ ] **Task 1**: Implement complete IndexedDB instance purge flows upon user logout or deletion request.
- [ ] **Task 2**: Apply cryptographic shielding where sensitive files are cached locally.

### Tasks for Session storage (Web Platform)
- **Severity Level**: MEDIUM
- [ ] **Task 1**: Enforce strict clearing of sessionStorage details immediately when tabs are destroyed.
- [ ] **Task 2**: Verify that no highly sensitive access key is kept unmitigated in sessionStorage.

### Tasks for Tracking technologies (Web Platform)
- **Severity Level**: HIGH
- [ ] **Task 1**: Map all active pixel tags and script inclusions.
- [ ] **Task 2**: Enforce conditional loading based on the active state of the user's consent preferences.

<!-- PRIVACY_POLICY_MONITOR_END -->