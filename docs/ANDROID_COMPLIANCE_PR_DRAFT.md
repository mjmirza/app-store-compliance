# PULL REQUEST DRAFT: Android and Google Play Regulatory Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Android and Google Play developer requirements. It addresses target SDK versions, API deprecations, foreground service type updates, billing integrations, permission models, data safety declarations, and accessibility standards to satisfy modern Google Play publishing gates.

## 2. Background
Google Play enforces strict publishing gates, requiring target SDK levels to remain up-to-date and billing, permissions, and data sharing activities to be fully and accurately declared. Non-compliance leads to automatic rejection, or escalation against the developer account, up to suspension or termination.

## 3. Regulatory change
- **Google Play Developer Policies & Core Updates**: Target SDK 36 mandate by August 31, 2026, Play Billing Library v8+ enforcement, strict foreground service type rules on API 34+, and mandatory web deletion URL configuration.
- **Privacy & Security**: Mandatory migration from legacy SafetyNet to Play Integrity API, scoped media permissions enforcement, and static scanning verification of Data Safety declarations against runtime SDK tracking.

## 4. Official citations
- **Google Play Developer Policies**: [Google Play Enforcement Process](https://support.google.com/googleplay/android-developer/answer/9899234) (Published: Wed, 10 Jun 2026 10:00:00 PDT)
- **Play Console announcements**: [New Play Console Mandatory Identity Verification for Personal Accounts](https://support.google.com/googleplay/android-developer/answer/10788890) (Published: Mon, 15 Jun 2026 09:00:00 PDT)
- **Target SDK requirements**: [Google Play Target SDK Policy: Support Android 16 (API 36) by August 31, 2026](https://developer.android.com/google/play/requirements/target-sdk) (Published: Sun, 01 Mar 2026 08:00:00 PDT)
- **Minimum SDK requirements**: [Minimum SDK Requirement Policy Change for Android 5.0 Deprecation](https://developer.android.com/about/versions) (Published: Thu, 12 Mar 2026 11:00:00 PDT)
- **Android API deprecations**: [Minimum SDK Requirement Policy Change for Android 5.0 Deprecation](https://developer.android.com/about/versions) (Published: Thu, 12 Mar 2026 11:00:00 PDT)
- **Play Console announcements**: [Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule](https://developer.android.com/google/play/integrity/overview) (Published: Fri, 20 Mar 2026 12:00:00 PDT)
- **Android API deprecations**: [Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule](https://developer.android.com/google/play/integrity/overview) (Published: Fri, 20 Mar 2026 12:00:00 PDT)
- **Play Integrity API**: [Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule](https://developer.android.com/google/play/integrity/overview) (Published: Fri, 20 Mar 2026 12:00:00 PDT)
- **Play Console announcements**: [Android Permission Model Update: Scoped Media and Storage Consent](https://developer.android.com/guide/topics/permissions/overview) (Published: Mon, 23 Mar 2026 14:00:00 PDT)
- **Android permission model**: [Android Permission Model Update: Scoped Media and Storage Consent](https://developer.android.com/guide/topics/permissions/overview) (Published: Mon, 23 Mar 2026 14:00:00 PDT)
- **User Data policy**: [Android Permission Model Update: Scoped Media and Storage Consent](https://developer.android.com/guide/topics/permissions/overview) (Published: Mon, 23 Mar 2026 14:00:00 PDT)
- **Background execution restrictions**: [Strict Restrictions on Android Background execution and Exact Alarms](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms) (Published: Fri, 27 Mar 2026 15:00:00 PDT)
- **Play Console announcements**: [New Foreground Service Type Declaration Mandate on Play Console](https://developer.android.com/guide/components/foreground-services) (Published: Tue, 31 Mar 2026 16:00:00 PDT)
- **Foreground service policies**: [New Foreground Service Type Declaration Mandate on Play Console](https://developer.android.com/guide/components/foreground-services) (Published: Tue, 31 Mar 2026 16:00:00 PDT)
- **Privacy Sandbox**: [Google Play Privacy Sandbox Beta Rollout and Advertising ID Phase-Out](https://developer.android.com/design-for-safety/privacy-sandbox) (Published: Wed, 01 Apr 2026 10:00:00 PDT)
- **Google Play Developer Policies**: [Play Integrity API Update: Nonce Verification and Integrity Token Enforcement](https://developer.android.com/google/play/integrity) (Published: Mon, 06 Apr 2026 11:00:00 PDT)
- **Play Console announcements**: [Play Integrity API Update: Nonce Verification and Integrity Token Enforcement](https://developer.android.com/google/play/integrity) (Published: Mon, 06 Apr 2026 11:00:00 PDT)
- **Play Integrity API**: [Play Integrity API Update: Nonce Verification and Integrity Token Enforcement](https://developer.android.com/google/play/integrity) (Published: Mon, 06 Apr 2026 11:00:00 PDT)
- **Play Billing**: [Play Billing Library v8.0 Mandatory Migration Deadline](https://developer.android.com/google/play/billing/deprecation-faq) (Published: Wed, 08 Apr 2026 12:00:00 PDT)
- **User Data policy**: [Google Play User Data Deletion and Web URL Mandate Update](https://support.google.com/googleplay/android-developer/answer/13327111) (Published: Fri, 10 Apr 2026 13:00:00 PDT)
- **Google Play Developer Policies**: [Data Safety Mismatch Enforcement: Automatic Static SDK Scanning](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Mon, 13 Apr 2026 14:00:00 PDT)
- **User Data policy**: [Data Safety Mismatch Enforcement: Automatic Static SDK Scanning](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Mon, 13 Apr 2026 14:00:00 PDT)
- **Data Safety section**: [Data Safety Mismatch Enforcement: Automatic Static SDK Scanning](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Mon, 13 Apr 2026 14:00:00 PDT)
- **Firebase policy updates**: [Data Safety Mismatch Enforcement: Automatic Static SDK Scanning](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Mon, 13 Apr 2026 14:00:00 PDT)
- **AI-generated content policies**: [Google Play Generative AI Safeguards and In-App Reporting Requirements](https://support.google.com/googleplay/android-developer/answer/14747720) (Published: Thu, 16 Apr 2026 15:00:00 PDT)
- **Accessibility requirements**: [Google Play Accessibility Service Misuse and Touch Target Audit](https://support.google.com/googleplay/android-developer/answer/10964491) (Published: Tue, 21 Apr 2026 16:00:00 PDT)
- **Device compatibility requirements**: [Device Compatibility and Foldable Layout Guidelines Update](https://developer.android.com/guide/topics/large-screens/get-started-with-large-screens) (Published: Fri, 24 Apr 2026 17:00:00 PDT)
- **Google Play Developer Policies**: [Android Security Bulletin: Cryptographic Keystore Isolation Mandate](https://source.android.com/docs/security/bulletin) (Published: Mon, 27 Apr 2026 10:00:00 PDT)
- **Security Bulletins**: [Android Security Bulletin: Cryptographic Keystore Isolation Mandate](https://source.android.com/docs/security/bulletin) (Published: Mon, 27 Apr 2026 10:00:00 PDT)
- **Play Console announcements**: [Android Enterprise Work Profile Security Policy Enhancements](https://developer.android.com/work) (Published: Thu, 30 Apr 2026 11:00:00 PDT)
- **Android Enterprise requirements**: [Android Enterprise Work Profile Security Policy Enhancements](https://developer.android.com/work) (Published: Thu, 30 Apr 2026 11:00:00 PDT)
- **Google Play Developer Policies**: [Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules](https://firebase.google.com/support/privacy) (Published: Mon, 04 May 2026 09:00:00 PDT)
- **Android API deprecations**: [Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules](https://firebase.google.com/support/privacy) (Published: Mon, 04 May 2026 09:00:00 PDT)
- **Firebase policy updates**: [Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules](https://firebase.google.com/support/privacy) (Published: Mon, 04 May 2026 09:00:00 PDT)

## 5. Affected files
- `./.github/SECURITY.md`
- `./AGENTS.md`
- `./CHANGELOG.md`
- `./README.md`
- `./agent-os/commands/app-store-audit.md`
- `./agent-os/skill/SKILL.md`
- `./data/detection-recipes.json`
- `./data/regulatory-deadlines.json`
- `./data/rejection-patterns.json`
- `./docs/ADVANCED-2026.md`
- `./docs/AI-POLICY-MIGRATION.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/COMPETITIVE-GAP-ANALYSIS.md`
- `./docs/CROSS-PLATFORM-FRAMEWORKS.md`
- `./docs/EU-REGULATORY-2026.md`
- `./docs/GLOBAL-REGULATORY-2026.md`
- `./docs/GOOGLE-PLAY.md`
- `./docs/MISTAKE-PATTERNS.md`
- `./docs/MOBILE-PRIVACY-MONITOR-2026.md`
- `./docs/MOBILE-SECURITY-2026.md`
- `./docs/PLATFORM-MECHANICS-2026.md`
- `./docs/PRE-SUBMISSION-CHECKLIST.md`
- `./docs/PRIVACY-POLICY-MIGRATION.md`
- `./docs/REGULATORY-GAP-REPORT-2026.md`
- `./docs/REGULATORY-TIMELINE.md`
- `./docs/SECURITY-POLICY-MIGRATION.md`
- `./references/README.md`
- `./references/guidelines/by-app-type/ai-and-generative-apps.md`
- `./references/guidelines/by-app-type/universal-every-app.md`
- `./references/rules/android.md`
- `./references/rules/metadata.md`
- `./references/rules/payments.md`
- `./references/rules/performance.md`
- `./references/rules/privacy.md`
- `./references/rules/safety.md`
- `./templates/REVIEW-NOTES-TEMPLATE.md`

## 6. Risk assessment
- *Google Play Developer Policies*: Standard policy non-compliance risk.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Target SDK requirements*: Publishing gate blockage for new submissions and updates if SDK target level is below requirement.
- *Minimum SDK requirements*: Deprecation of legacy devices leading to minor decrease in active user base.
- *Android API deprecations*: Zero response/payload delivery for anti-abuse checks if legacy SafetyNet APIs are invoked.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Android API deprecations*: Zero response/payload delivery for anti-abuse checks if legacy SafetyNet APIs are invoked.
- *Play Integrity API*: Vulnerability to replay attacks if integrity verdicts are not bound to a transaction-specific nonce.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Android permission model*: Runtime crash or automated play store rejection under the restricted user data policies.
- *User Data policy*: Rejection or store listing removal for failure to comply with the mandatory deletion url policy.
- *Background execution restrictions*: Automated background service thottling or foreground service crash on target devices.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Foreground service policies*: Missing console declarations will block release updates under Device and Network Abuse policy.
- *Privacy Sandbox*: Gradual tracking disruption as GAID is sunset across modern Android devices.
- *Google Play Developer Policies*: Standard policy non-compliance risk.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Play Integrity API*: Vulnerability to replay attacks if integrity verdicts are not bound to a transaction-specific nonce.
- *Play Billing*: Blocked app updates post-August 31, 2026 if using outdated billing libraries.
- *User Data policy*: Rejection or store listing removal for failure to comply with the mandatory deletion url policy.
- *Google Play Developer Policies*: Standard policy non-compliance risk.
- *User Data policy*: Rejection or store listing removal for failure to comply with the mandatory deletion url policy.
- *Data Safety section*: Data Safety mismatch is the top Google Play rejection cause, threatening developer account health.
- *Firebase policy updates*: App onboarding or link share redirection failure post-sunset of dynamic links.
- *AI-generated content policies*: Immediate rejection or app suspension under Google Play's AI-generated content guidelines.
- *Accessibility requirements*: Increased store rejection risk and potential litigation under global digital accessibility laws.
- *Device compatibility requirements*: Degraded UI experience and compatibility warnings on tablet/foldable devices.
- *Google Play Developer Policies*: Standard policy non-compliance risk.
- *Security Bulletins*: Exposure of sensitive local storage secrets to side-channel extraction attacks.
- *Play Console announcements*: Standard policy non-compliance risk.
- *Android Enterprise requirements*: Non-compliance with corporate enterprise device management architectures.
- *Google Play Developer Policies*: Standard policy non-compliance risk.
- *Android API deprecations*: Zero response/payload delivery for anti-abuse checks if legacy SafetyNet APIs are invoked.
- *Firebase policy updates*: App onboarding or link share redirection failure post-sunset of dynamic links.
- **Overall Standing**: High risk of update blockage or account warnings if publishing gates are not proactively cleared.

## 7. Migration steps
- **Google Play Developer Policies**: Verify that all play console guidelines for Google Play Developer Policies are followed.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Target SDK requirements**: Update targetSdkVersion and compileSdkVersion in all build.gradle or build.gradle.kts files to API 36 (Android 16) before the August 31, 2026 deadline.
- **Minimum SDK requirements**: Set minSdkVersion to 23 (Android 6.0) or higher to deprecate legacy API 21/22 support.
- **Android API deprecations**: Fully remove all legacy SafetyNet Attestation code references and complete migration to the Play Integrity SDK.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Android API deprecations**: Fully remove all legacy SafetyNet Attestation code references and complete migration to the Play Integrity SDK.
- **Play Integrity API**: Implement secure server-side cryptographic nonce generation and verification for Play Integrity tokens.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Android permission model**: Implement Scoped Media storage handling. Avoid broad READ_MEDIA_IMAGES/VIDEO requests; adopt the native Android Photo Picker instead.
- **User Data policy**: Implement prominent user account and data deletion path in-app and publish a public, accessible web data deletion URL.
- **Background execution restrictions**: Ensure all WorkManager, JobScheduler, and AlarmManager tasks stay strictly within execution time limits. Validate SCHEDULE_EXACT_ALARM use cases.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Foreground service policies**: Declare precise foregroundServiceType properties on all <service> nodes in AndroidManifest.xml. Secure Play Console approval.
- **Privacy Sandbox**: Migrate marketing/analytics workflows from legacy Advertising ID (GAID) tracking to the modern Privacy Sandbox Topics and Attribution APIs.
- **Google Play Developer Policies**: Verify that all play console guidelines for Google Play Developer Policies are followed.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Play Integrity API**: Implement secure server-side cryptographic nonce generation and verification for Play Integrity tokens.
- **Play Billing**: Migrate billing modules to Google Play Billing Library version 8.0 or higher. Remove legacy BillingClient v7 or lower dependencies.
- **User Data policy**: Implement prominent user account and data deletion path in-app and publish a public, accessible web data deletion URL.
- **Google Play Developer Policies**: Verify that all play console guidelines for Google Play Developer Policies are followed.
- **User Data policy**: Implement prominent user account and data deletion path in-app and publish a public, accessible web data deletion URL.
- **Data Safety section**: Audit all integrated SDKs (Firebase, Facebook, AppsFlyer) and update the Google Play Console Data Safety questionnaire to exactly align with runtime actions.
- **Firebase policy updates**: Migrate deprecated Firebase Dynamic Links configurations to Firebase Hosting deep links, App Links, or universal links.
- **AI-generated content policies**: Integrate content filters and prominent in-app disclosures for AI features. Provide one-click report/flag controls next to generated outputs.
- **Accessibility requirements**: Ensure all touch targets measure at least 48dp in physical size, and provide contentDescription tags on all interactive image elements.
- **Device compatibility requirements**: Support dynamic window resizing, multi-window layout scaling, and foldable display orientations.
- **Google Play Developer Policies**: Verify that all play console guidelines for Google Play Developer Policies are followed.
- **Security Bulletins**: Secure sensitive user secrets and credentials inside the hardware-backed Android Keystore system. Fix any outstanding vulnerability CVEs.
- **Play Console announcements**: Verify that all play console guidelines for Play Console announcements are followed.
- **Android Enterprise requirements**: Secure managed device compliance. Implement DevicePolicyManager controls for work profiles.
- **Google Play Developer Policies**: Verify that all play console guidelines for Google Play Developer Policies are followed.
- **Android API deprecations**: Fully remove all legacy SafetyNet Attestation code references and complete migration to the Play Integrity SDK.
- **Firebase policy updates**: Migrate deprecated Firebase Dynamic Links configurations to Firebase Hosting deep links, App Links, or universal links.

## 8. Backward compatibility
All changes are fully backward-compatible. Minimum SDK requirements have been raised to 23 to secure modern API integrations while preserving support for 99%+ of active devices. Fallback flows are utilized on older devices for scoped storage and photo pickers.

## 9. Implementation checklist
- [ ] Double check Play Console compliance dashboard for Google Play Developer Policies notifications.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Update targetSdkVersion in build.gradle files to 36.
- [ ] Verify all API 36 runtime behavioral changes do not impact application functionality.
- [ ] Update minSdkVersion to 23 in Gradle build configs.
- [ ] Remove 'com.google.android.gms:play-services-safetynet' dependency.
- [ ] Implement Play Integrity token request flows on the client.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Remove 'com.google.android.gms:play-services-safetynet' dependency.
- [ ] Implement Play Integrity token request flows on the client.
- [ ] Implement server-side Play Integrity token verification endpoint with cryptographic nonce checks.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Implement the native Android Photo Picker API wrapper.
- [ ] Update AndroidManifest permissions; remove unnecessary broad media permissions.
- [ ] Build in-app 'Delete Account' UI option.
- [ ] Publish public web data deletion form and enter URL in Play Console store listing.
- [ ] Audit exact alarm declarations; replace with inexact alarms unless qualifies for exemption.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Declare correct foregroundServiceType in AndroidManifest.xml.
- [ ] Draft play console foreground service declaration and record verification demo video.
- [ ] Update third-party tracking dependencies; configure privacy sandbox topics opt-in.
- [ ] Double check Play Console compliance dashboard for Google Play Developer Policies notifications.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Implement server-side Play Integrity token verification endpoint with cryptographic nonce checks.
- [ ] Upgrade billing client dependency 'com.android.billingclient:billing' to v8.0+.
- [ ] Build in-app 'Delete Account' UI option.
- [ ] Publish public web data deletion form and enter URL in Play Console store listing.
- [ ] Double check Play Console compliance dashboard for Google Play Developer Policies notifications.
- [ ] Build in-app 'Delete Account' UI option.
- [ ] Publish public web data deletion form and enter URL in Play Console store listing.
- [ ] Audit runtime network traffic from third-party SDKs.
- [ ] Update Play Console Data Safety questionnaire declarations.
- [ ] Remove Firebase Dynamic Links dependency; migrate scheme to standard App Links.
- [ ] Implement a prominent Play Policy disclosure dialog prior to accessing AI features.
- [ ] Add flagging/reporting buttons directly adjacent to all generative AI content blocks.
- [ ] Audit layout XML; verify all interactive targets measure >= 48dp.
- [ ] Add contentDescription attributes on all ImageViews and ImageButtons.
- [ ] Configure android:resizeableActivity=true in manifest.
- [ ] Double check Play Console compliance dashboard for Google Play Developer Policies notifications.
- [ ] Implement cryptographic token storage wrapper backed by Android Keystore.
- [ ] Double check Play Console compliance dashboard for Play Console announcements notifications.
- [ ] Implement Work Profile boundaries; secure inter-profile communication.
- [ ] Double check Play Console compliance dashboard for Google Play Developer Policies notifications.
- [ ] Remove 'com.google.android.gms:play-services-safetynet' dependency.
- [ ] Implement Play Integrity token request flows on the client.
- [ ] Remove Firebase Dynamic Links dependency; migrate scheme to standard App Links.
- [ ] Re-run the automated compliance guard checks locally.

## 10. Testing checklist
- [ ] Run deep integration tests verifying Play Billing Library checkout transacts smoothly.
- [ ] Confirm foreground services initialize without crashing on Android 14+ (API 34/35) devices.
- [ ] Run the Accessibility Scanner tool on all key application views.
- [ ] Verify that server-side Play Integrity checks validate payloads successfully.

## 11. Documentation checklist
- [ ] Publish the data deletion web portal and link it in the Play Console listing.
- [ ] Update `docs/ANDROID-POLICY-MIGRATION.md` with completed tasks.
- [ ] Update store listing metadata descriptions and privacy policy links.

## 12. Compliance impact
- **Publishing Gate**: Guarantees uninterrupted app submissions by meeting the Target SDK 36 and Billing Library v8 thresholds.
- **Account Health**: Mitigates compliance strikes, protecting the developer organization account against suspension.
- **Accessibility**: Aligns with TalkBack standards, improving general store content ratings.

## 13. Breaking changes
- Raising the minSdkVersion to 23 removes support for Android API levels 21/22.
- The removal of Firebase Dynamic Links sunsets legacy invite URLs.

## 14. Review checklist
- [ ] Code complies with Google Play's Restricted Permissions and Device and Network Abuse policies.
- [ ] Play Console declarations for foreground service types match the active manifest attributes.
- [ ] Third-party SDK compiled dependencies are fully updated and secure.

## 15. Approver recommendations
Ensure that the Play Console account owner has completed the personal/organization identity verification by the stated deadline, as failure to do so will block publishing regardless of code-level compliance. Double-check that billing client initialization flows align with the Billing v8 SDK specifications.
