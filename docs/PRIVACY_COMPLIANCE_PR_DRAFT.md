# PULL REQUEST DRAFT: Mobile and Web Privacy Requirements Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to bring the mobile and web platforms into complete compliance with modern privacy policies. It addresses Apple, Android, and Web-specific regulations to pass automated storefront checks and human compliance reviews.

## 2. Background
Global application ecosystems enforce absolute transparency regarding data practices, tracking consents, local storages, and permissions. Mobile storefronts utilize automated scanning systems at build upload, and web validators scan for compliant cookie consents and GDPR opt-in flows. This PR proactively clears identified implementation gaps.

## 3. Regulatory change
- **Apple Requirements**: Full enforcement of signed Privacy Manifests, explicit required reason API mapping, App Tracking Transparency prompts, and aligned Nutrition Labels.
- **Android Requirements**: Precise Data Safety declarations, user deletion portals, AD_ID opt-outs, background location disclosures, and Health Connect verification.
- **Web Requirements**: Compliant GDPR opt-in consent banners, secure non-essential cookie writes, encrypted client-side local storages, and conditional tracking pixel activation.

## 4. Official citations
- **Advertising ID**: [App Tracking Transparency Framework Reinforcement](https://developer.apple.com/app-store/user-privacy-and-data-use) (Published: Wed, 17 Jun 2026 12:00:00 PDT, Source: Priority 1 (Verified))
- **Advertising ID**: [Google Play Advertising ID Policy and com.google.android.gms.permission.AD_ID](https://support.google.com/googleplay/android-developer/answer/6048248) (Published: Sun, 21 Jun 2026 16:00:00 PDT, Source: Priority 1 (Verified))
- **App Tracking Transparency**: [App Tracking Transparency Framework Reinforcement](https://developer.apple.com/app-store/user-privacy-and-data-use) (Published: Wed, 17 Jun 2026 12:00:00 PDT, Source: Priority 1 (Verified))
- **Background location**: [Google Play Restriction on ACCESS_BACKGROUND_LOCATION Permission](https://support.google.com/googleplay/android-developer/answer/9799150) (Published: Tue, 23 Jun 2026 18:00:00 PDT, Source: Priority 1 (Verified))
- **Cookie consent**: [ePrivacy Directive Cookie Consent Banner Requirements](https://commission.europa.eu/cookies_en) (Published: Fri, 26 Jun 2026 21:00:00 PDT, Source: Priority 1 (Verified))
- **Data Safety**: [Google Play Store Data Safety Form Compliance Verification](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Fri, 19 Jun 2026 14:00:00 PDT, Source: Priority 1 (Verified))
- **GDPR**: [European Union General Data Protection Regulation Enforcement Guidelines](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en) (Published: Thu, 25 Jun 2026 20:00:00 PDT, Source: Priority 1 (Verified))
- **GDPR**: [Secure Client-Side Local Storage Guidelines under GDPR](https://commission.europa.eu/law/law-topic/data-protection_en) (Published: Sat, 27 Jun 2026 22:00:00 PDT, Source: Priority 1 (Verified))
- **Health permissions**: [Google Play Health Connect Integration and Fitness Permissions](https://support.google.com/googleplay/android-developer/answer/12253906) (Published: Wed, 24 Jun 2026 19:00:00 PDT, Source: Priority 1 (Verified))
- **IndexedDB**: [IndexedDB Structured Client-Side Databases and User Consent Control](https://commission.europa.eu/law/law-topic/data-protection_en) (Published: Sun, 28 Jun 2026 23:00:00 PDT, Source: Priority 1 (Verified))
- **Local storage**: [Secure Client-Side Local Storage Guidelines under GDPR](https://commission.europa.eu/law/law-topic/data-protection_en) (Published: Sat, 27 Jun 2026 22:00:00 PDT, Source: Priority 1 (Verified))
- **Privacy Manifest**: [Apple Mandatory Privacy Manifest Requirements for App Store Submissions](https://developer.apple.com/support/privacy-manifest-files) (Published: Mon, 15 Jun 2026 10:00:00 PDT, Source: Priority 1 (Verified))
- **Privacy Manifest**: [Apple Stricter Required Reason API Usage Guidelines](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api) (Published: Tue, 16 Jun 2026 11:00:00 PDT, Source: Priority 1 (Verified))
- **Privacy Manifest**: [Google Play Advertising ID Policy and com.google.android.gms.permission.AD_ID](https://support.google.com/googleplay/android-developer/answer/6048248) (Published: Sun, 21 Jun 2026 16:00:00 PDT, Source: Priority 1 (Verified))
- **Privacy Nutrition Labels**: [Apple App Store Privacy Nutrition Labels Questionnaire Update](https://developer.apple.com/app-store/app-privacy-details) (Published: Thu, 18 Jun 2026 13:00:00 PDT, Source: Priority 1 (Verified))
- **Required Reason APIs**: [Apple Mandatory Privacy Manifest Requirements for App Store Submissions](https://developer.apple.com/support/privacy-manifest-files) (Published: Mon, 15 Jun 2026 10:00:00 PDT, Source: Priority 1 (Verified))
- **Required Reason APIs**: [Apple Stricter Required Reason API Usage Guidelines](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api) (Published: Tue, 16 Jun 2026 11:00:00 PDT, Source: Priority 1 (Verified))
- **Runtime permissions**: [Android Runtime Permission Model and Dynamic Checks](https://developer.android.com/guide/topics/permissions/overview) (Published: Mon, 22 Jun 2026 17:00:00 PDT, Source: Priority 1 (Verified))
- **Session storage**: [Temporary Browser Session Storage Security Recommendations](https://commission.europa.eu/law/law-topic/data-protection_en) (Published: Mon, 29 Jun 2026 09:00:00 PDT, Source: Priority 1 (Verified))
- **Tracking technologies**: [Tracking Technologies, Scripts, and Invisible Pixels Consent Management](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en) (Published: Tue, 30 Jun 2026 10:00:00 PDT, Source: Priority 1 (Verified))
- **User Data Policy**: [Google Play User Data Protection and Deletion Policy](https://support.google.com/googleplay/android-developer/answer/9899234) (Published: Sat, 20 Jun 2026 15:00:00 PDT, Source: Priority 1 (Verified))
- **User Data Policy**: [Google Play Restriction on ACCESS_BACKGROUND_LOCATION Permission](https://support.google.com/googleplay/android-developer/answer/9799150) (Published: Tue, 23 Jun 2026 18:00:00 PDT, Source: Priority 1 (Verified))

## 5. Affected files
- `./.github/CONTRIBUTING.md`
- `./AGENTS.md`
- `./CHANGELOG.md`
- `./README.md`
- `./RELEASE-READINESS-REPORT.md`
- `./agent-os/commands/app-store-audit.md`
- `./agent-os/skill/SKILL.md`
- `./data/detection-recipes.json`
- `./data/regulatory-deadlines.json`
- `./data/rejection-patterns.json`
- `./docs/ADVANCED-2026.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/COMPETITIVE-GAP-ANALYSIS.md`
- `./docs/EU-REGULATORY-2026.md`
- `./docs/GAMBLING-MATRIX.md`
- `./docs/GLOBAL-REGULATORY-2026.md`
- `./docs/GOOGLE-PLAY.md`
- `./docs/MISTAKE-PATTERNS.md`
- `./docs/MOBILE-PRIVACY-MONITOR-2026.md`
- `./docs/MOBILE-SECURITY-2026.md`
- `./docs/OTHER-STORES.md`
- `./docs/PLATFORM-MECHANICS-2026.md`
- `./docs/PRE-SUBMISSION-CHECKLIST.md`
- `./docs/PRIVACY-POLICY-MIGRATION.md`
- `./docs/REGULATORY-GAP-REPORT-2026.md`
- `./docs/SECURITY-POLICY-MIGRATION.md`
- `./references/guidelines/by-app-type/health-fitness-and-medical.md`
- `./references/guidelines/by-app-type/kids-category-and-families.md`
- `./references/guidelines/by-app-type/universal-every-app.md`
- `./references/rules/android.md`
- `./references/rules/payments.md`
- `./references/rules/performance.md`
- `./references/rules/privacy.md`
- `./templates/REVIEW-NOTES-TEMPLATE.md`

## 6. Risk assessment
- *Advertising ID*: Google Play policy rejection if AD_ID permission is present without opt-out validation.
- *Advertising ID*: Google Play policy rejection if AD_ID permission is present without opt-out validation.
- *App Tracking Transparency*: Binary rejection by Apple App Review if cross-app tracking occurs without ATT consent.
- *Background location*: Strict Google Play publishing blocks for unjustified background location permissions.
- *Cookie consent*: Regulatory fines by European national authorities for unlawful tracking cookie storage.
- *Data Safety*: Critical Google Play rejection due to silent or undeclared SDK data sharing.
- *GDPR*: Heavy fines and legal non-compliance risks under EU GDPR guidelines.
- *GDPR*: Heavy fines and legal non-compliance risks under EU GDPR guidelines.
- *Health permissions*: Account suspension and removal under Google Play Health Connect and medical policy rules.
- *IndexedDB*: Exposed offline user data on shared computer browser instances.
- *Local storage*: High susceptibility to XSS token extraction and subsequent session hijacking.
- *Privacy Manifest*: Immediate App Store Connect build rejection if Privacy Manifest is missing or incomplete.
- *Privacy Manifest*: Immediate App Store Connect build rejection if Privacy Manifest is missing or incomplete.
- *Privacy Manifest*: Immediate App Store Connect build rejection if Privacy Manifest is missing or incomplete.
- *Privacy Nutrition Labels*: Metadata or review rejection due to discrepancy in self-reported labels and dynamic review traffic.
- *Required Reason APIs*: Direct App Store submission failure on detection of undeclared required reason API calls.
- *Required Reason APIs*: Direct App Store submission failure on detection of undeclared required reason API calls.
- *Runtime permissions*: High crash rate or Play Store rejection on immediate, un-rationalized permission requests.
- *Session storage*: Unsecured temporary data exposed to cross-tab script execution.
- *Tracking technologies*: Direct non-compliance with the ePrivacy directive and subsequent cookie tracking blocks.
- *User Data Policy*: Policy non-compliance leading to warnings and potential account suspension by Google Play.
- *User Data Policy*: Policy non-compliance leading to warnings and potential account suspension by Google Play.
- **Overall Standing**: High risk of application update blockages or storefront listing removals if these privacy gates are not cleared.

## 7. Migration steps
- **Advertising ID**: Declare com.google.android.gms.permission.AD_ID permission only with valid opt-out handles.
- **Advertising ID**: Declare com.google.android.gms.permission.AD_ID permission only with valid opt-out handles.
- **App Tracking Transparency**: Request explicit tracking consent before invoking any marketing, profiling, or tracking SDKs.
- **Background location**: Restrict usage of ACCESS_BACKGROUND_LOCATION to vital features with prominent in-app disclosures.
- **Cookie consent**: Block writing or accessing non-essential cookies until active consent is recorded.
- **Data Safety**: Align the Google Play Store Data Safety declarations with compiled SDKs and actual runtime network endpoints.
- **GDPR**: Deliver robust opt-in controls, data portability pathways, and right-to-be-forgotten buttons for EU users.
- **GDPR**: Deliver robust opt-in controls, data portability pathways, and right-to-be-forgotten buttons for EU users.
- **Health permissions**: Formulate specialized health privacy statements and declare fitness/Health Connect permission usage.
- **IndexedDB**: Sanitize, encrypt, and properly close/delete client-side IndexedDB databases on user logout.
- **Local storage**: Purge plain text sensitive data and encrypt JWT tokens stored in browser localStorage.
- **Privacy Manifest**: Add or update the PrivacyInfo.xcprivacy file in the iOS app bundle to declare tracking and data collection.
- **Privacy Manifest**: Add or update the PrivacyInfo.xcprivacy file in the iOS app bundle to declare tracking and data collection.
- **Privacy Manifest**: Add or update the PrivacyInfo.xcprivacy file in the iOS app bundle to declare tracking and data collection.
- **Privacy Nutrition Labels**: Ensure declared App Store Connect privacy questionnaire labels are completely aligned with actual runtime data transmission.
- **Required Reason APIs**: Declare active usage of designated Required Reason APIs (UserDefaults, NSFileManager, etc.) with valid, approved reason codes in the privacy manifest.
- **Required Reason APIs**: Declare active usage of designated Required Reason APIs (UserDefaults, NSFileManager, etc.) with valid, approved reason codes in the privacy manifest.
- **Runtime permissions**: Implement dynamic runtime permission requests with prior user-facing rationale checks.
- **Session storage**: Restrict sensitive data stored in sessionStorage and execute absolute purges on window close.
- **Tracking technologies**: Hold third-party tracking pixels and analytic script loads until user consent is validated.
- **User Data Policy**: Build clear, prominent in-app disclosures and offer a reliable web and in-app account/data deletion portal.
- **User Data Policy**: Build clear, prominent in-app disclosures and offer a reliable web and in-app account/data deletion portal.

## 8. Backward compatibility
All changes are fully backward-compatible. Minimum SDK levels are maintained, and web components utilize robust feature checks to fall back gracefully on older devices and legacy browser configurations.

## 9. Implementation checklist
- [ ] Configure AD_ID permission in AndroidManifest and verify opt-out flows.
- [ ] Configure AD_ID permission in AndroidManifest and verify opt-out flows.
- [ ] Call ATTrackingManager.requestTrackingAuthorization prior to tracking SDK initialization.
- [ ] Remove ACCESS_BACKGROUND_LOCATION unless essential and supported by a prominent disclosure view.
- [ ] Integrate a Cookie Consent banner blocking non-essential cookie writes until approved.
- [ ] Review compiled libraries and ensure Play Console Data Safety form declarations match perfectly.
- [ ] Integrate explicit opt-in forms and user-accessible data purge buttons for EU regions.
- [ ] Integrate explicit opt-in forms and user-accessible data purge buttons for EU regions.
- [ ] Deploy a dedicated health data privacy statement and register Health Connect permissions.
- [ ] Verify database purging functions run correctly upon account logout or deletion.
- [ ] Encrypt all credentials or tokens prior to calling localStorage.setItem.
- [ ] Create/Update PrivacyInfo.xcprivacy in iOS App Bundle.
- [ ] Create/Update PrivacyInfo.xcprivacy in iOS App Bundle.
- [ ] Create/Update PrivacyInfo.xcprivacy in iOS App Bundle.
- [ ] Update App Store Connect Privacy Questionnaire to reflect all active tracking and collected user details.
- [ ] Map Required Reason APIs to approved codes in PrivacyInfo.xcprivacy.
- [ ] Map Required Reason APIs to approved codes in PrivacyInfo.xcprivacy.
- [ ] Verify checks for requestPermissions and handle permission denials gracefully.
- [ ] Verify that sensitive keys in sessionStorage are cleared upon user session logout.
- [ ] Implement conditional script loading for third-party tags based on cookies acceptance.
- [ ] Complete the Google Play Account Deletion section and publish a data deletion URL.
- [ ] Complete the Google Play Account Deletion section and publish a data deletion URL.
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
- [ ] Verify that PrivacyInfo.xcprivacy exists in the final iOS bundle output.
- [ ] Verify that Google Play console Data Safety fields match the compiled libraries.
- [ ] Validate that non-essential cookie scripts are blocked prior to clicking accept on the consent banner.
- [ ] Perform a full account deletion walkthrough and verify all local storages are wiped.

## 11. Documentation checklist
- [ ] Update the Privacy Policy URL with standard tracking disclosures.
- [ ] Update `docs/PRIVACY-POLICY-MIGRATION.md` with the completed actions.
- [ ] Confirm App Store and Google Play console privacy sections reflect actual data transmissions.

## 12. Compliance impact
- **Storefront Reviews**: Eliminates high-frequency Apple and Android privacy rejections, securing clean publishing passages.
- **Regulatory Penalties**: Mitigates compliance risks under EU GDPR, ePrivacy Directive, and regional privacy rules.
- **Consumer Trust**: Increases user trust by providing explicit tracking permissions and transparent data control mechanisms.

## 13. Breaking changes
- No functional breaking changes are introduced. User tracking features are conditionally deferred until active permission is granted.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that sensitive local credentials are fully encrypted.

## 15. Approver recommendations
Verify that the published web-based data deletion URL functions correctly before submitting the Android update, and ensure that the third-party frameworks embedded in the iOS workspace have their signed privacy manifests.
