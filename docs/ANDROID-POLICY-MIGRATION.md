<!-- ANDROID_POLICY_MONITOR_START -->
# Android and Google Play Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-android.py` to track compliance areas.

## Monitored Requirements Update Log

### 1. [Google Play Developer Policies] Google Play Enforcement Process
- **Published Date**: Wed, 10 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9899234](https://support.google.com/googleplay/android-developer/answer/9899234)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play's enforcement process for policy violations covers rejection, removal, suspension, limited visibility, and account termination, based on app metadata, in-app experience, and account information.

### 2. [Play Console announcements] New Play Console Mandatory Identity Verification for Personal Accounts
- **Published Date**: Mon, 15 Jun 2026 09:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10788890](https://support.google.com/googleplay/android-developer/answer/10788890)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To foster user trust, Google Play requires all personal developer accounts created before recent policy updates to complete mandatory identity verification by September 30, 2026. Failure to verify will result in update blockages and eventual listing removals.

### 3. [Target SDK requirements] Google Play Target SDK Policy: Support Android 16 (API 36) by August 31, 2026
- **Published Date**: Sun, 01 Mar 2026 08:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/requirements/target-sdk](https://developer.android.com/google/play/requirements/target-sdk)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play is updating its Target SDK requirements. Starting August 31, 2026, all new apps and updates to existing apps must target Android 16 (API 36) or higher. Submissions failing to meet this threshold will be blocked by the publishing gate.

### 4. [Minimum SDK requirements] Minimum SDK Requirement Policy Change for Android 5.0 Deprecation
- **Published Date**: Thu, 12 Mar 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/about/versions](https://developer.android.com/about/versions)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To maintain high security and performance across the Google Play ecosystem, apps must set a minSdkVersion of 23 (Android 6.0) or higher to receive updates, formally deprecating support for legacy Android 5.0 and 5.1 (API 21/22).

### 5. [Android API deprecations] Minimum SDK Requirement Policy Change for Android 5.0 Deprecation
- **Published Date**: Thu, 12 Mar 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/about/versions](https://developer.android.com/about/versions)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To maintain high security and performance across the Google Play ecosystem, apps must set a minSdkVersion of 23 (Android 6.0) or higher to receive updates, formally deprecating support for legacy Android 5.0 and 5.1 (API 21/22).

### 6. [Play Console announcements] Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule
- **Published Date**: Fri, 20 Mar 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity/overview](https://developer.android.com/google/play/integrity/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: As announced previously, the Legacy SafetyNet Attestation APIs are fully deprecated and shut down. All anti-abuse, security check, and integrity verification flows must migrate to the modern Play Integrity API.

### 7. [Android API deprecations] Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule
- **Published Date**: Fri, 20 Mar 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity/overview](https://developer.android.com/google/play/integrity/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: As announced previously, the Legacy SafetyNet Attestation APIs are fully deprecated and shut down. All anti-abuse, security check, and integrity verification flows must migrate to the modern Play Integrity API.

### 8. [Play Integrity API] Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule
- **Published Date**: Fri, 20 Mar 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity/overview](https://developer.android.com/google/play/integrity/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: As announced previously, the Legacy SafetyNet Attestation APIs are fully deprecated and shut down. All anti-abuse, security check, and integrity verification flows must migrate to the modern Play Integrity API.

### 9. [Play Console announcements] Android Permission Model Update: Scoped Media and Storage Consent
- **Published Date**: Mon, 23 Mar 2026 14:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Under the updated User Data and Android Permission Model, apps requesting READ_MEDIA_IMAGES and READ_MEDIA_VIDEO face stricter verification. Broad photo access is restricted, and developers are urged to migrate to the native Android Photo Picker.

### 10. [Android permission model] Android Permission Model Update: Scoped Media and Storage Consent
- **Published Date**: Mon, 23 Mar 2026 14:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Under the updated User Data and Android Permission Model, apps requesting READ_MEDIA_IMAGES and READ_MEDIA_VIDEO face stricter verification. Broad photo access is restricted, and developers are urged to migrate to the native Android Photo Picker.

### 11. [User Data policy] Android Permission Model Update: Scoped Media and Storage Consent
- **Published Date**: Mon, 23 Mar 2026 14:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Under the updated User Data and Android Permission Model, apps requesting READ_MEDIA_IMAGES and READ_MEDIA_VIDEO face stricter verification. Broad photo access is restricted, and developers are urged to migrate to the native Android Photo Picker.

### 12. [Background execution restrictions] Strict Restrictions on Android Background execution and Exact Alarms
- **Published Date**: Fri, 27 Mar 2026 15:00:00 PDT
- **Official Resource**: [https://developer.android.com/about/versions/14/changes/schedule-exact-alarms](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To conserve system battery life and improve device performance, Android is introducing tighter runtime checks. Tighter limitations on exact alarms (SCHEDULE_EXACT_ALARM) and background wake locks will trigger automatic job throttling.

### 13. [Play Console announcements] New Foreground Service Type Declaration Mandate on Play Console
- **Published Date**: Tue, 31 Mar 2026 16:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/components/foreground-services](https://developer.android.com/guide/components/foreground-services)
- **Verification Status**: Priority 1 (Verified)
- **Description**: All applications targeting API 34+ that run foreground services must declare valid foregroundServiceType attributes in their manifest, hold matching FOREGROUND_SERVICE permissions, and submit a detailed Play Console foreground service declaration and video.

### 14. [Foreground service policies] New Foreground Service Type Declaration Mandate on Play Console
- **Published Date**: Tue, 31 Mar 2026 16:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/components/foreground-services](https://developer.android.com/guide/components/foreground-services)
- **Verification Status**: Priority 1 (Verified)
- **Description**: All applications targeting API 34+ that run foreground services must declare valid foregroundServiceType attributes in their manifest, hold matching FOREGROUND_SERVICE permissions, and submit a detailed Play Console foreground service declaration and video.

### 15. [Privacy Sandbox] Google Play Privacy Sandbox Beta Rollout and Advertising ID Phase-Out
- **Published Date**: Wed, 01 Apr 2026 10:00:00 PDT
- **Official Resource**: [https://developer.android.com/design-for-safety/privacy-sandbox](https://developer.android.com/design-for-safety/privacy-sandbox)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google is expanding the Privacy Sandbox Beta on Android, initiating the gradual phase-out of the legacy persistent Advertising ID (GAID) in favor of the privacy-preserving Topics API, Attribution Reporting, and SDK Runtime environments.

### 16. [Google Play Developer Policies] Play Integrity API Update: Nonce Verification and Integrity Token Enforcement
- **Published Date**: Mon, 06 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity](https://developer.android.com/google/play/integrity)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To mitigate man-in-the-middle replay attacks, Google Play Integrity API now enforces server-side cryptographic nonce verification and strict integrity token checks before dispensing secure payloads.

### 17. [Play Console announcements] Play Integrity API Update: Nonce Verification and Integrity Token Enforcement
- **Published Date**: Mon, 06 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity](https://developer.android.com/google/play/integrity)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To mitigate man-in-the-middle replay attacks, Google Play Integrity API now enforces server-side cryptographic nonce verification and strict integrity token checks before dispensing secure payloads.

### 18. [Play Integrity API] Play Integrity API Update: Nonce Verification and Integrity Token Enforcement
- **Published Date**: Mon, 06 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity](https://developer.android.com/google/play/integrity)
- **Verification Status**: Priority 1 (Verified)
- **Description**: To mitigate man-in-the-middle replay attacks, Google Play Integrity API now enforces server-side cryptographic nonce verification and strict integrity token checks before dispensing secure payloads.

### 19. [Play Billing] Play Billing Library v8.0 Mandatory Migration Deadline
- **Published Date**: Wed, 08 Apr 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/billing/deprecation-faq](https://developer.android.com/google/play/billing/deprecation-faq)
- **Verification Status**: Priority 1 (Verified)
- **Description**: By August 31, 2026, all new apps and updates to existing apps must migrate to the Play Billing Library version 8.0 or higher. Apps attempting to publish using earlier Billing Library versions (including v7.x or below) will be automatically blocked.

### 20. [User Data policy] Google Play User Data Deletion and Web URL Mandate Update
- **Published Date**: Fri, 10 Apr 2026 13:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/13327111](https://support.google.com/googleplay/android-developer/answer/13327111)
- **Verification Status**: Priority 1 (Verified)
- **Description**: All apps permitting in-app account creation must provide users with both an in-app account deletion flow and a public web-based data deletion URL. Unreachable or broken deletion URLs will trigger automated store rejections.

### 21. [Google Play Developer Policies] Data Safety Mismatch Enforcement: Automatic Static SDK Scanning
- **Published Date**: Mon, 13 Apr 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.

### 22. [User Data policy] Data Safety Mismatch Enforcement: Automatic Static SDK Scanning
- **Published Date**: Mon, 13 Apr 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.

### 23. [Data Safety section] Data Safety Mismatch Enforcement: Automatic Static SDK Scanning
- **Published Date**: Mon, 13 Apr 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.

### 24. [Firebase policy updates] Data Safety Mismatch Enforcement: Automatic Static SDK Scanning
- **Published Date**: Mon, 13 Apr 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.

### 25. [AI-generated content policies] Google Play Generative AI Safeguards and In-App Reporting Requirements
- **Published Date**: Thu, 16 Apr 2026 15:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/14747720](https://support.google.com/googleplay/android-developer/answer/14747720)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Applications integrating generative AI or conversational LLMs must provide robust user-safety controls, including prominent disclosures, an in-app content reporting/flagging mechanism, user blocking, and safeguards preventing deepfake/NSFW outputs.

### 26. [Accessibility requirements] Google Play Accessibility Service Misuse and Touch Target Audit
- **Published Date**: Tue, 21 Apr 2026 16:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10964491](https://support.google.com/googleplay/android-developer/answer/10964491)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google Play will flag and reject non-accessibility apps requesting the BIND_ACCESSIBILITY_SERVICE permission. Additionally, apps face strict audits ensuring a minimum 48dp touch target size and content descriptions for all interactive elements.

### 27. [Device compatibility requirements] Device Compatibility and Foldable Layout Guidelines Update
- **Published Date**: Fri, 24 Apr 2026 17:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/large-screens/get-started-with-large-screens](https://developer.android.com/guide/topics/large-screens/get-started-with-large-screens)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Android releases update guidelines enforcing screen and aspect-ratio compatibility across multi-window systems, tablets, and foldable devices. Apps must support dynamic resizing and avoid fixed orientation limits where feasible.

### 28. [Google Play Developer Policies] Android Security Bulletin: Cryptographic Keystore Isolation Mandate
- **Published Date**: Mon, 27 Apr 2026 10:00:00 PDT
- **Official Resource**: [https://source.android.com/docs/security/bulletin](https://source.android.com/docs/security/bulletin)
- **Verification Status**: Priority 1 (Verified)
- **Description**: An Android Security Bulletin addresses high-severity vulnerabilities (CVE-2026-X). App developers are mandated to isolate sensitive user secrets and credentials inside the hardware-backed Android Keystore system and enforce biometrics.

### 29. [Security Bulletins] Android Security Bulletin: Cryptographic Keystore Isolation Mandate
- **Published Date**: Mon, 27 Apr 2026 10:00:00 PDT
- **Official Resource**: [https://source.android.com/docs/security/bulletin](https://source.android.com/docs/security/bulletin)
- **Verification Status**: Priority 1 (Verified)
- **Description**: An Android Security Bulletin addresses high-severity vulnerabilities (CVE-2026-X). App developers are mandated to isolate sensitive user secrets and credentials inside the hardware-backed Android Keystore system and enforce biometrics.

### 30. [Play Console announcements] Android Enterprise Work Profile Security Policy Enhancements
- **Published Date**: Thu, 30 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/work](https://developer.android.com/work)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google announces new Android Enterprise standards for corporate and work profile apps. Enhanced controls under the DevicePolicyManager allow secure data boundaries, blocking side-loading and personal app data leakage.

### 31. [Android Enterprise requirements] Android Enterprise Work Profile Security Policy Enhancements
- **Published Date**: Thu, 30 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/work](https://developer.android.com/work)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Google announces new Android Enterprise standards for corporate and work profile apps. Enhanced controls under the DevicePolicyManager allow secure data boundaries, blocking side-loading and personal app data leakage.

### 32. [Google Play Developer Policies] Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules
- **Published Date**: Mon, 04 May 2026 09:00:00 PDT
- **Official Resource**: [https://firebase.google.com/support/privacy](https://firebase.google.com/support/privacy)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: Firebase is sunsetting Dynamic Links, requiring developers to migrate to Firebase Hosting Deep Links, App Links, or universal links. Additionally, updated Realtime Database and Cloud Firestore rules enforce strict authorization boundaries.

### 33. [Android API deprecations] Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules
- **Published Date**: Mon, 04 May 2026 09:00:00 PDT
- **Official Resource**: [https://firebase.google.com/support/privacy](https://firebase.google.com/support/privacy)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: Firebase is sunsetting Dynamic Links, requiring developers to migrate to Firebase Hosting Deep Links, App Links, or universal links. Additionally, updated Realtime Database and Cloud Firestore rules enforce strict authorization boundaries.

### 34. [Firebase policy updates] Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules
- **Published Date**: Mon, 04 May 2026 09:00:00 PDT
- **Official Resource**: [https://firebase.google.com/support/privacy](https://firebase.google.com/support/privacy)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: Firebase is sunsetting Dynamic Links, requiring developers to migrate to Firebase Hosting Deep Links, App Links, or universal links. Additionally, updated Realtime Database and Cloud Firestore rules enforce strict authorization boundaries.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Google Play Developer Policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Review store metadata and in-app content against Google Play policies.
- [ ] **Task 2**: Audit sensitive permissions and clear policy center violations.

### Tasks for Play Console announcements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Verify developer identity verification status in Play Console.
- [ ] **Task 2**: Complete organization/personal account verification steps.

### Tasks for Target SDK requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Update `targetSdkVersion` in build.gradle files to 36.
- [ ] **Task 2**: Test target API level 36 behaviors on devices.

### Tasks for Minimum SDK requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Update `minSdkVersion` in build.gradle files to 23 (Android 6.0).
- [ ] **Task 2**: Test compatibility on API level 23+ minimum supported devices.

### Tasks for Android API deprecations
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Remove legacy SafetyNet Attestation SDK dependencies.
- [ ] **Task 2**: Migrate anti-abuse checks to the modern Play Integrity SDK.

### Tasks for Play Integrity API
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Implement server-side Play Integrity token verification endpoint.
- [ ] **Task 2**: Enforce cryptographic nonce checks on integrity payloads.

### Tasks for Android permission model
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Replace broad READ_MEDIA_IMAGES/VIDEO requests with Photo Picker.
- [ ] **Task 2**: Verify runtime permission prompts display valid user rationale.

### Tasks for User Data policy
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Publish a public account and data deletion URL.
- [ ] **Task 2**: Connect the URL to the Play Console User Data safety form.

### Tasks for Background execution restrictions
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Audit exact alarm (SCHEDULE_EXACT_ALARM) declarations.
- [ ] **Task 2**: Migrate background tasks to WorkManager and inexact alarms.

### Tasks for Foreground service policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Specify foregroundServiceType inside manifest service tags.
- [ ] **Task 2**: Register foreground service type declaration and video demo on Play Console.

### Tasks for Privacy Sandbox
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Integrate Privacy Sandbox Topics API and Attribution Reporting.
- [ ] **Task 2**: Prepare for persistent Advertising ID (GAID) deprecation.

### Tasks for Play Billing
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Migrate project dependencies to Billing Library version 8.0+.
- [ ] **Task 2**: Perform test transactions on Google Play console sandbox.

### Tasks for Data Safety section
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Perform dynamic network traffic audit on compiled SDKs.
- [ ] **Task 2**: Update Play Console Data Safety questionnaire declarations.

### Tasks for Firebase policy updates
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Migrate deprecated Firebase Dynamic Links to standard App Links.
- [ ] **Task 2**: Update Cloud Firestore and Realtime Database security rules.

### Tasks for AI-generated content policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Add generative AI user disclosure dialogs prior to feature access.
- [ ] **Task 2**: Implement in-app reporting/flagging buttons next to AI outputs.

### Tasks for Accessibility requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Audit layout XML to ensure interactive targets measure >= 48dp.
- [ ] **Task 2**: Add contentDescription tags on all interactive image views.

### Tasks for Device compatibility requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Set android:resizeableActivity=true for multi-window support.
- [ ] **Task 2**: Test layout responsiveness on tablet and foldable devices.

### Tasks for Security Bulletins
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Isolate sensitive credentials inside hardware-backed Android Keystore.
- [ ] **Task 2**: Patch identified vulnerability CVEs in third-party dependencies.

### Tasks for Android Enterprise requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Configure Work Profile boundaries via DevicePolicyManager.
- [ ] **Task 2**: Verify secure enterprise data segregation on managed devices.

<!-- ANDROID_POLICY_MONITOR_END -->