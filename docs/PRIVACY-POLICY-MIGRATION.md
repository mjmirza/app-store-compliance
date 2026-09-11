<!-- PRIVACY_POLICY_MONITOR_START -->
# Mobile and Web Privacy Requirements Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-privacy.py` to track privacy compliance areas.

## Monitored Requirements Update Log

### 1. [Advertising ID] App Tracking Transparency Framework Reinforcement
- **Published Date**: Wed, 17 Jun 2026 12:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/user-privacy-and-data-use](https://developer.apple.com/app-store/user-privacy-and-data-use)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Developers must display the App Tracking Transparency (ATT) prompt via ATTrackingManager and obtain user permission before collecting the advertising identifier (IDFA) or tracking users across other apps or websites.

### 2. [Advertising ID] Google Play Advertising ID Policy and com.google.android.gms.permission.AD_ID
- **Published Date**: Sun, 21 Jun 2026 16:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/6048248](https://support.google.com/googleplay/android-developer/answer/6048248)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Apps targeting Android 12 or higher that use the Google Play Services Advertising ID must declare the AD_ID permission in their manifest and provide user options to reset or delete the ID.

### 3. [App Tracking Transparency] Updated Apple Developer Program License Agreement now available
- **Published Date**: Tue, 18 Aug 2026 08:00:32 PDT
- **Official Resource**: [https://developer.apple.com/news/?id=0cgo95n6](https://developer.apple.com/news/?id=0cgo95n6)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Attachment 14 of the Apple Developer Program License Agreement has been added to specify updated terms for apps in the European Union, including alternative distribution, alternative payments, and business terms. These terms will go into effect on October 1, 2026. Please review the changes and sign in to your account to accept the updated terms. Translations of the updated agreement will be...

### 4. [App Tracking Transparency] Updated Apple Developer Program License Agreement now available
- **Published Date**: Thu, 18 Jun 2026 07:30:54 PDT
- **Official Resource**: [https://developer.apple.com/news/?id=umq9wxmm](https://developer.apple.com/news/?id=umq9wxmm)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Attachment 12 of the Apple Developer Program License Agreement has been revised to specify terms for iOS apps in Brazil, including alternative distribution, alternative payments and out-of-app offers, and the Core Technology Commission. Please review the changes and sign in to your account to accept the updated terms. Translations of the updated agreement will be available on the Apple Developer...

### 5. [App Tracking Transparency] How Infold Games fashioned an open world for Infinity Nikki
- **Published Date**: Fri, 03 Apr 2026 09:02:01 PDT
- **Official Resource**: [https://developer.apple.com/news/?id=9mgkwjnm](https://developer.apple.com/news/?id=9mgkwjnm)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Infinity Nikki is a literally glowing example of what video game graphics can be. The fifth in a series of dress-up titles from Infold Games, Infinity Nikki is also the first to embrace elements of RPG action-adventure. But instead of tracking down weapons and battling bad guys, this installment finds its wide-eyed heroine solving puzzles by collecting enchanted outfits found throughout a series...

### 6. [App Tracking Transparency] Updated Apple Developer Program License Agreement now available
- **Published Date**: Fri, 06 Dec 2024 07:00:11 PST
- **Official Resource**: [https://developer.apple.com/news/?id=edbw1dhq](https://developer.apple.com/news/?id=edbw1dhq)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Attachment 2 of the Apple Developer Program License Agreement has been amended to specify requirements for use of the In-App Purchase API. Please review the changes and accept the updated terms in your account. View the full terms and conditions Translations of the updated agreement will be available on the Apple Developer website within one month.

### 7. [App Tracking Transparency] App Tracking Transparency Framework Reinforcement
- **Published Date**: Wed, 17 Jun 2026 12:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/user-privacy-and-data-use](https://developer.apple.com/app-store/user-privacy-and-data-use)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Developers must display the App Tracking Transparency (ATT) prompt via ATTrackingManager and obtain user permission before collecting the advertising identifier (IDFA) or tracking users across other apps or websites.

### 8. [Background location] Google Play Restriction on ACCESS_BACKGROUND_LOCATION Permission
- **Published Date**: Tue, 23 Jun 2026 18:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9799150](https://support.google.com/googleplay/android-developer/answer/9799150)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play strictly limits background location access. Developers must justify that background location is crucial to the app's core feature, and provide a clear prominent disclosure to the user.

### 9. [Cookie consent] ePrivacy Directive Cookie Consent Banner Requirements
- **Published Date**: Fri, 26 Jun 2026 21:00:00 PDT
- **Official Resource**: [https://commission.europa.eu/cookies_en](https://commission.europa.eu/cookies_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Websites targeting EU users must present a compliant Cookie Consent banner that blocks non-essential cookies (such as marketing or analytics) until explicit, active consent is granted.

### 10. [Data Safety] Google Play Store Data Safety Form Compliance Verification
- **Published Date**: Fri, 19 Jun 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play enforces strict validation of the Data Safety section. Submissions are dynamically scanned for compiled libraries and network activities to verify they align with the declared Data Safety form.

### 11. [GDPR] European Union General Data Protection Regulation Enforcement Guidelines
- **Published Date**: Thu, 25 Jun 2026 20:00:00 PDT
- **Official Resource**: [https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: The EDPB issues guidance on valid GDPR consent. Processing EU residents' personal data requires explicit opt-in, clear information, data portability, and a functional right to be forgotten (data erasure).

### 12. [GDPR] Secure Client-Side Local Storage Guidelines under GDPR
- **Published Date**: Sat, 27 Jun 2026 22:00:00 PDT
- **Official Resource**: [https://commission.europa.eu/law/law-topic/data-protection_en](https://commission.europa.eu/law/law-topic/data-protection_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Stashing unencrypted sensitive information, JWT tokens, or credentials in local web storage (localStorage) is highly discouraged. Stored data must respect user consent and remain protected from cross-site scripting (XSS) extraction.

### 13. [GDPR] Unverified Industry Blog Rumors on GDPR Fines
- **Published Date**: Wed, 01 Jul 2026 11:00:00 PDT
- **Official Resource**: [https://randomblogsite.com/gdpr-rumor](https://randomblogsite.com/gdpr-rumor)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: A random industry blog claims GDPR rules are being changed next week to fine all websites without an immediate dark mode. This is an unverified blog post.

### 14. [Health permissions] Google Play Health Connect Integration and Fitness Permissions
- **Published Date**: Wed, 24 Jun 2026 19:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/12253906](https://support.google.com/googleplay/android-developer/answer/12253906)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Accessing health or fitness data via Health Connect requires specialized developer declarations in the Play Console, a detailed health privacy policy, and prominent in-app disclosures.

### 15. [IndexedDB] IndexedDB Structured Client-Side Databases and User Consent Control
- **Published Date**: Sun, 28 Jun 2026 23:00:00 PDT
- **Official Resource**: [https://commission.europa.eu/law/law-topic/data-protection_en](https://commission.europa.eu/law/law-topic/data-protection_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Large-scale offline or structured data stored locally in browser IndexedDB instances must follow user privacy preferences, use encryption where sensitive data is involved, and perform cleanups upon logout.

### 16. [Local storage] Secure Client-Side Local Storage Guidelines under GDPR
- **Published Date**: Sat, 27 Jun 2026 22:00:00 PDT
- **Official Resource**: [https://commission.europa.eu/law/law-topic/data-protection_en](https://commission.europa.eu/law/law-topic/data-protection_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Stashing unencrypted sensitive information, JWT tokens, or credentials in local web storage (localStorage) is highly discouraged. Stored data must respect user consent and remain protected from cross-site scripting (XSS) extraction.

### 17. [Privacy Manifest] Apple Mandatory Privacy Manifest Requirements for App Store Submissions
- **Published Date**: Mon, 15 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/privacy-manifest-files](https://developer.apple.com/support/privacy-manifest-files)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Apple enforces mandatory Privacy Manifests (PrivacyInfo.xcprivacy) for all newly submitted apps and third-party SDK updates. The manifest must accurately declare data collection, tracking domains, and required reason API usage.

### 18. [Privacy Manifest] Apple Stricter Required Reason API Usage Guidelines
- **Published Date**: Tue, 16 Jun 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To prevent fingerprinting, Apple requires developers to specify approved reason codes in their Privacy Manifest if they access designated Required Reason APIs, such as UserDefaults, file timestamps, system uptime, and disk space.

### 19. [Privacy Manifest] Google Play Advertising ID Policy and com.google.android.gms.permission.AD_ID
- **Published Date**: Sun, 21 Jun 2026 16:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/6048248](https://support.google.com/googleplay/android-developer/answer/6048248)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Apps targeting Android 12 or higher that use the Google Play Services Advertising ID must declare the AD_ID permission in their manifest and provide user options to reset or delete the ID.

### 20. [Privacy Nutrition Labels] Hello Developer: May 2026
- **Published Date**: Tue, 12 May 2026 09:00:16 PDT
- **Official Resource**: [https://developer.apple.com/news/?id=qtzr82f0](https://developer.apple.com/news/?id=qtzr82f0)
- **Verification Status**: Priority 1 (Verified)
- **Description**: In this edition: Meet inspiring developers, advocates, and educators. Prepare your app for Accessibility Nutrition Labels. Meet the team behind the stylish open-world adventure Infinity Nikki. Get the most out of your Apple Developer account. Update your Intel-based Mac apps to Apple silicon. Read now

### 21. [Privacy Nutrition Labels] Apple App Store Privacy Nutrition Labels Questionnaire Update
- **Published Date**: Thu, 18 Jun 2026 13:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/app-privacy-details](https://developer.apple.com/app-store/app-privacy-details)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Apple requires developers to complete the self-reported Privacy Nutrition Labels in App Store Connect. All declared data collection and usage practices must match actual in-app behaviors.

### 22. [Required Reason APIs] Apple Mandatory Privacy Manifest Requirements for App Store Submissions
- **Published Date**: Mon, 15 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/privacy-manifest-files](https://developer.apple.com/support/privacy-manifest-files)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Apple enforces mandatory Privacy Manifests (PrivacyInfo.xcprivacy) for all newly submitted apps and third-party SDK updates. The manifest must accurately declare data collection, tracking domains, and required reason API usage.

### 23. [Required Reason APIs] Apple Stricter Required Reason API Usage Guidelines
- **Published Date**: Tue, 16 Jun 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To prevent fingerprinting, Apple requires developers to specify approved reason codes in their Privacy Manifest if they access designated Required Reason APIs, such as UserDefaults, file timestamps, system uptime, and disk space.

### 24. [Runtime permissions] Android Runtime Permission Model and Dynamic Checks
- **Published Date**: Mon, 22 Jun 2026 17:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Android runtime permissions must be requested dynamically when the app accesses sensitive capabilities like camera, contacts, or storage. Rationale must be explained before requesting the permission.

### 25. [Session storage] Temporary Browser Session Storage Security Recommendations
- **Published Date**: Mon, 29 Jun 2026 09:00:00 PDT
- **Official Resource**: [https://commission.europa.eu/law/law-topic/data-protection_en](https://commission.europa.eu/law/law-topic/data-protection_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Data kept in sessionStorage must be handled securely, ensuring sensitive credentials are not exposed to untrusted scripts, and are thoroughly purged once the user closes the tab or logs out.

### 26. [Tracking technologies] Tracking Technologies, Scripts, and Invisible Pixels Consent Management
- **Published Date**: Tue, 30 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Third-party analytical scripts (Google Analytics, Facebook Pixel, Hotjar) must be explicitly controlled and completely disabled by default until the user accepts cookie or tracking preferences.

### 27. [User Data Policy] Google Play User Data Protection and Deletion Policy
- **Published Date**: Sat, 20 Jun 2026 15:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9899234](https://support.google.com/googleplay/android-developer/answer/9899234)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play User Data policy requires prominent disclosures and explicit user consent before collecting any personal or sensitive data. Apps with in-app account creation must offer an in-app and web account deletion option.

### 28. [User Data Policy] Google Play Restriction on ACCESS_BACKGROUND_LOCATION Permission
- **Published Date**: Tue, 23 Jun 2026 18:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9799150](https://support.google.com/googleplay/android-developer/answer/9799150)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play strictly limits background location access. Developers must justify that background location is crucial to the app's core feature, and provide a clear prominent disclosure to the user.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Advertising ID
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Configure the AD_ID permission in AndroidManifest and handle user opt-outs.

### Tasks for Advertising ID
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Configure the AD_ID permission in AndroidManifest and handle user opt-outs.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.
- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.
- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.
- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.
- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.
- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.

### Tasks for Background location
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Ensure background location is backed by a prominent in-app disclosure view.

### Tasks for Cookie consent
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Deploy a cookie banner that halts non-essential cookie writes by default.

### Tasks for Data Safety
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Conduct a dependency audit for Google Play Data Safety alignment.

### Tasks for GDPR
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Provide opt-in controls and account deletion pathways for EU users.

### Tasks for GDPR
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Provide opt-in controls and account deletion pathways for EU users.

### Tasks for GDPR (BLOCKED: Announcement source is unverified)
- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.

### Tasks for Health permissions
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Complete specialized fitness declarations and publish health statements.

### Tasks for IndexedDB
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Safely wipe local database object stores upon user logout.

### Tasks for Local storage
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Encrypt any JWT tokens or user details kept in localStorage.

### Tasks for Privacy Manifest
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Create a PrivacyInfo.xcprivacy manifest at the root of the iOS target.
- [ ] **Task 2**: List all collected data types and tracking practices in the manifest.

### Tasks for Privacy Manifest
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Create a PrivacyInfo.xcprivacy manifest at the root of the iOS target.
- [ ] **Task 2**: List all collected data types and tracking practices in the manifest.

### Tasks for Privacy Manifest
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Create a PrivacyInfo.xcprivacy manifest at the root of the iOS target.
- [ ] **Task 2**: List all collected data types and tracking practices in the manifest.

### Tasks for Privacy Nutrition Labels
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Verify App Store Connect nutrition disclosures against codebase PII transmission.

### Tasks for Privacy Nutrition Labels
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Verify App Store Connect nutrition disclosures against codebase PII transmission.

### Tasks for Required Reason APIs
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Identify all required reason API references (e.g. UserDefaults).
- [ ] **Task 2**: Map reason codes under NSPrivacyAccessedAPITypes.

### Tasks for Required Reason APIs
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Identify all required reason API references (e.g. UserDefaults).
- [ ] **Task 2**: Map reason codes under NSPrivacyAccessedAPITypes.

### Tasks for Runtime permissions
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Ensure permissions are dynamically verified with clear user explanations.

### Tasks for Session storage
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Secure temporary session tokens and clear session variables upon closing tabs.

### Tasks for Tracking technologies
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Defer Google Analytics or Facebook Pixel scripts until consent is given.

### Tasks for User Data Policy
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Build clear in-app data deletion controls and set a public web deletion URL.

### Tasks for User Data Policy
- **Regulatory Impact**: High priority compliance area.
- [ ] **Task 1**: Build clear in-app data deletion controls and set a public web deletion URL.

<!-- PRIVACY_POLICY_MONITOR_END -->