<!-- ANDROID_POLICY_MONITOR_START -->
# Android and Google Play Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-android.py` to track compliance areas.

## Monitored Requirements Update Log

### 1. [Google Play Developer Policies] Google Play Enforcement Process
- **Published Date**: Wed, 10 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9899234](https://support.google.com/googleplay/android-developer/answer/9899234)
- **Description**: Google Play's enforcement process for policy violations covers rejection, removal, suspension, limited visibility, and account termination, based on app metadata, in-app experience, and account information.

### 2. [Play Console announcements] New Play Console Mandatory Identity Verification for Personal Accounts
- **Published Date**: Mon, 15 Jun 2026 09:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10788890](https://support.google.com/googleplay/android-developer/answer/10788890)
- **Description**: To foster user trust, Google Play requires all personal developer accounts created before recent policy updates to complete mandatory identity verification by September 30, 2026. Failure to verify will result in update blockages and eventual listing removals.

### 3. [Target SDK requirements] Google Play Target SDK Policy: Support Android 16 (API 36) by August 31, 2026
- **Published Date**: Sun, 01 Mar 2026 08:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/requirements/target-sdk](https://developer.android.com/google/play/requirements/target-sdk)
- **Description**: Google Play is updating its Target SDK requirements. Starting August 31, 2026, all new apps and updates to existing apps must target Android 16 (API 36) or higher. Submissions failing to meet this threshold will be blocked by the publishing gate.

### 4. [Minimum SDK requirements] Minimum SDK Requirement Policy Change for Android 5.0 Deprecation
- **Published Date**: Thu, 12 Mar 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/about/versions](https://developer.android.com/about/versions)
- **Description**: To maintain high security and performance across the Google Play ecosystem, apps must set a minSdkVersion of 23 (Android 6.0) or higher to receive updates, formally deprecating support for legacy Android 5.0 and 5.1 (API 21/22).

### 5. [Android API deprecations] Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule
- **Published Date**: Fri, 20 Mar 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity/overview](https://developer.android.com/google/play/integrity/overview)
- **Description**: As announced previously, the Legacy SafetyNet Attestation APIs are fully deprecated and shut down. All anti-abuse, security check, and integrity verification flows must migrate to the modern Play Integrity API.

### 6. [Android permission model] Android Permission Model Update: Scoped Media and Storage Consent
- **Published Date**: Mon, 23 Mar 2026 14:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Description**: Under the updated User Data and Android Permission Model, apps requesting READ_MEDIA_IMAGES and READ_MEDIA_VIDEO face stricter verification. Broad photo access is restricted, and developers are urged to migrate to the native Android Photo Picker.

### 7. [Background execution restrictions] Strict Restrictions on Android Background execution and Exact Alarms
- **Published Date**: Fri, 27 Mar 2026 15:00:00 PDT
- **Official Resource**: [https://developer.android.com/about/versions/14/changes/schedule-exact-alarms](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms)
- **Description**: To conserve system battery life and improve device performance, Android is introducing tighter runtime checks. Tighter limitations on exact alarms (SCHEDULE_EXACT_ALARM) and background wake locks will trigger automatic job throttling.

### 8. [Foreground service policies] New Foreground Service Type Declaration Mandate on Play Console
- **Published Date**: Tue, 31 Mar 2026 16:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/components/foreground-services](https://developer.android.com/guide/components/foreground-services)
- **Description**: All applications targeting API 34+ that run foreground services must declare valid foregroundServiceType attributes in their manifest, hold matching FOREGROUND_SERVICE permissions, and submit a detailed Play Console foreground service declaration and video.

### 9. [Privacy Sandbox] Google Play Privacy Sandbox Beta Rollout and Advertising ID Phase-Out
- **Published Date**: Wed, 01 Apr 2026 10:00:00 PDT
- **Official Resource**: [https://developer.android.com/design-for-safety/privacy-sandbox](https://developer.android.com/design-for-safety/privacy-sandbox)
- **Description**: Google is expanding the Privacy Sandbox Beta on Android, initiating the gradual phase-out of the legacy persistent Advertising ID (GAID) in favor of the privacy-preserving Topics API, Attribution Reporting, and SDK Runtime environments.

### 10. [Play Integrity API] Play Integrity API Update: Nonce Verification and Integrity Token Enforcement
- **Published Date**: Mon, 06 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/integrity](https://developer.android.com/google/play/integrity)
- **Description**: To mitigate man-in-the-middle replay attacks, Google Play Integrity API now enforces server-side cryptographic nonce verification and strict integrity token checks before dispensing secure payloads.

### 11. [Play Billing] Play Billing Library v8.0 Mandatory Migration Deadline
- **Published Date**: Wed, 08 Apr 2026 12:00:00 PDT
- **Official Resource**: [https://developer.android.com/google/play/billing/deprecation-faq](https://developer.android.com/google/play/billing/deprecation-faq)
- **Description**: By August 31, 2026, all new apps and updates to existing apps must migrate to the Play Billing Library version 8.0 or higher. Apps attempting to publish using earlier Billing Library versions (including v7.x or below) will be automatically blocked.

### 12. [User Data policy] Google Play User Data Deletion and Web URL Mandate Update
- **Published Date**: Fri, 10 Apr 2026 13:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/13327111](https://support.google.com/googleplay/android-developer/answer/13327111)
- **Description**: All apps permitting in-app account creation must provide users with both an in-app account deletion flow and a public web-based data deletion URL. Unreachable or broken deletion URLs will trigger automated store rejections.

### 13. [Data Safety section] Data Safety Mismatch Enforcement: Automatic Static SDK Scanning
- **Published Date**: Mon, 13 Apr 2026 14:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Description**: Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.

### 14. [AI-generated content policies] Google Play Generative AI Safeguards and In-App Reporting Requirements
- **Published Date**: Thu, 16 Apr 2026 15:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/14747720](https://support.google.com/googleplay/android-developer/answer/14747720)
- **Description**: Applications integrating generative AI or conversational LLMs must provide robust user-safety controls, including prominent disclosures, an in-app content reporting/flagging mechanism, user blocking, and safeguards preventing deepfake/NSFW outputs.

### 15. [Accessibility requirements] Google Play Accessibility Service Misuse and Touch Target Audit
- **Published Date**: Tue, 21 Apr 2026 16:00:00 PDT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10964491](https://support.google.com/googleplay/android-developer/answer/10964491)
- **Description**: Google Play will flag and reject non-accessibility apps requesting the BIND_ACCESSIBILITY_SERVICE permission. Additionally, apps face strict audits ensuring a minimum 48dp touch target size and content descriptions for all interactive elements.

### 16. [Device compatibility requirements] Device Compatibility and Foldable Layout Guidelines Update
- **Published Date**: Fri, 24 Apr 2026 17:00:00 PDT
- **Official Resource**: [https://developer.android.com/guide/topics/large-screens/get-started-with-large-screens](https://developer.android.com/guide/topics/large-screens/get-started-with-large-screens)
- **Description**: Android releases update guidelines enforcing screen and aspect-ratio compatibility across multi-window systems, tablets, and foldable devices. Apps must support dynamic resizing and avoid fixed orientation limits where feasible.

### 17. [Security Bulletins] Android Security Bulletin: Cryptographic Keystore Isolation Mandate
- **Published Date**: Mon, 27 Apr 2026 10:00:00 PDT
- **Official Resource**: [https://source.android.com/docs/security/bulletin](https://source.android.com/docs/security/bulletin)
- **Description**: An Android Security Bulletin addresses high-severity vulnerabilities (CVE-2026-X). App developers are mandated to isolate sensitive user secrets and credentials inside the hardware-backed Android Keystore system and enforce biometrics.

### 18. [Android Enterprise requirements] Android Enterprise Work Profile Security Policy Enhancements
- **Published Date**: Thu, 30 Apr 2026 11:00:00 PDT
- **Official Resource**: [https://developer.android.com/work](https://developer.android.com/work)
- **Description**: Google announces new Android Enterprise standards for corporate and work profile apps. Enhanced controls under the DevicePolicyManager allow secure data boundaries, blocking side-loading and personal app data leakage.

### 19. [Firebase policy updates] Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules
- **Published Date**: Mon, 04 May 2026 09:00:00 PDT
- **Official Resource**: [https://firebase.google.com/support/privacy](https://firebase.google.com/support/privacy)
- **Description**: Firebase is sunsetting Dynamic Links, requiring developers to migrate to Firebase Hosting Deep Links, App Links, or universal links. Additionally, updated Realtime Database and Cloud Firestore rules enforce strict authorization boundaries.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Google Play Developer Policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Review Play Console Policy Center guidelines for newly revised developer policies.
- [ ] **Task 2**: Audit store listing metadata and in-app assets for program policy compliance.

### Tasks for Play Console announcements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Complete mandatory developer account identity verification on Play Console.
- [ ] **Task 2**: Check Play Console dashboard for pending account status warnings.

### Tasks for Target SDK requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Update `targetSdkVersion` in build.gradle files to 36.
- [ ] **Task 2**: Test target API level 36 behaviors on devices.

### Tasks for Minimum SDK requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Set `minSdkVersion` to 23 (Android 6.0) in Gradle configurations.
- [ ] **Task 2**: Clean up legacy compatibility code for API levels 21/22.

### Tasks for Android API deprecations
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Remove legacy SafetyNet Attestation code references from client and server.
- [ ] **Task 2**: Replace deprecated API references with current Android Jetpack libraries.

### Tasks for Android permission model
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Adopt native Android Photo Picker and scoped media access permissions.
- [ ] **Task 2**: Audit `AndroidManifest.xml` to remove unnecessary broad permission requests.

### Tasks for Background execution restrictions
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Audit background jobs and migrate to `WorkManager` and `JobScheduler`.
- [ ] **Task 2**: Review exact alarm usage (`SCHEDULE_EXACT_ALARM`) and request exemptions if required.

### Tasks for Foreground service policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Specify `foregroundServiceType` inside the manifest service tags.
- [ ] **Task 2**: Register foreground service type video verification demo on Play Console.

### Tasks for Privacy Sandbox
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Prepare analytics and attribution modules for Advertising ID (GAID) deprecation.
- [ ] **Task 2**: Integrate Privacy Sandbox Topics API and Attribution Reporting SDKs.

### Tasks for Play Integrity API
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Implement client-side Play Integrity API token requests.
- [ ] **Task 2**: Enforce server-side cryptographic nonce generation and token verification.

### Tasks for Play Billing
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Migrate project dependencies to Billing Library version 8.0.
- [ ] **Task 2**: Perform test transactions on Google Play console sandbox.

### Tasks for User Data policy
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Publish a public account and data deletion URL.
- [ ] **Task 2**: Connect the URL to the Play Console User Data safety form.

### Tasks for Data Safety section
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Conduct static/dynamic audit of third-party SDK network traffic.
- [ ] **Task 2**: Update Play Console Data Safety questionnaire declarations.

### Tasks for AI-generated content policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Integrate in-app reporting and content flagging mechanisms for AI outputs.
- [ ] **Task 2**: Add prominent AI safety disclosures prior to user interaction.

### Tasks for Accessibility requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Ensure interactive UI elements meet minimum 48dp touch target size.
- [ ] **Task 2**: Add `contentDescription` attributes to all ImageViews and ImageButtons.

### Tasks for Device compatibility requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Set `android:resizeableActivity=true` in manifest.
- [ ] **Task 2**: Test multi-window and foldable screen layout scaling.

### Tasks for Security Bulletins
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Isolate user credentials and cryptographic keys in hardware-backed Android Keystore.
- [ ] **Task 2**: Remediate security vulnerabilities published in Android Security Bulletins.

### Tasks for Android Enterprise requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Implement work profile boundaries and `DevicePolicyManager` compliance.
- [ ] **Task 2**: Verify corporate data separation and enterprise security profiles.

### Tasks for Firebase policy updates
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Migrate from Firebase Dynamic Links to Firebase Hosting deep links or App Links.
- [ ] **Task 2**: Update Realtime Database and Cloud Firestore security rules.

<!-- ANDROID_POLICY_MONITOR_END -->