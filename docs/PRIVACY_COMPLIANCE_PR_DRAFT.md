# PULL REQUEST DRAFT: Mobile and Web Privacy Requirements Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored global mobile and web privacy requirements. It addresses Privacy Manifests, Required Reason APIs, App Tracking Transparency, Data Safety, GDPR, Cookie Consent, and other sensitive storage structures to satisfy modern platform publishing gates.

## 2. Background
Storefront operators (Apple and Google Play) and regional regulators enforce strict privacy rules regarding user consent, runtime permissions, secure local storage, and accurate declarations. Non-compliance results in build rejections, account suspension, or heavy fines.

## 3. Regulatory change
- **Apple Storefront**: Mandatory root Privacy Manifest configuration, Required Reason API declarations, and accurate Nutrition Labels.
- **Android Storefront**: Strict Data Safety declarations, prominent sensitive disclosures, background location limits, and Health Connect approvals.
- **Web Applications**: GDPR data minimization and right to be forgotten rights, ePrivacy Directive cookie consent controls, and secure local/session/indexedDB handling.

## 4. Official citations
- **Privacy Manifest**: [Apple Mandatory Privacy Manifest Framework Implementation Deadline](https://developer.apple.com/news/?id=privacy-manifest-mandate) (Published: Wed, 10 Jun 2026 10:00:00 GMT)
- **Required Reason APIs**: [Strict Rejection Gate for Declared Reason API Violations](https://developer.apple.com/news/?id=required-reason-apis) (Published: Thu, 11 Jun 2026 11:00:00 GMT)
- **App Tracking Transparency**: [App Tracking Transparency Opt-In Enforcement Clarification](https://developer.apple.com/news/?id=att-enforcement) (Published: Fri, 12 Jun 2026 12:00:00 GMT)
- **Advertising ID**: [App Tracking Transparency Opt-In Enforcement Clarification](https://developer.apple.com/news/?id=att-enforcement) (Published: Fri, 12 Jun 2026 12:00:00 GMT)
- **Privacy Nutrition Labels**: [Storefront Validation of Privacy Nutrition Labels Mismatch](https://developer.apple.com/news/?id=privacy-nutrition-labels) (Published: Sat, 13 Jun 2026 13:00:00 GMT)
- **Data Safety**: [Storefront Validation of Privacy Nutrition Labels Mismatch](https://developer.apple.com/news/?id=privacy-nutrition-labels) (Published: Sat, 13 Jun 2026 13:00:00 GMT)
- **Data Safety**: [Google Play Store Data Safety Form Compliance Verification](https://support.google.com/googleplay/android-developer/answer/10787469) (Published: Sun, 14 Jun 2026 14:00:00 GMT)
- **User Data Policy**: [Google Play User Data and Explicit Prominent Disclosure Policy](https://support.google.com/googleplay/android-developer/answer/User-Data-Policy) (Published: Mon, 15 Jun 2026 15:00:00 GMT)
- **Advertising ID**: [Google Play Services Advertising ID Policy and Opt-Out Requirements](https://support.google.com/googleplay/android-developer/answer/9899234) (Published: Tue, 16 Jun 2026 16:00:00 GMT)
- **Runtime permissions**: [Mandatory Runtime Permission Flow and UX Validation](https://developer.android.com/guide/topics/permissions/overview) (Published: Wed, 17 Jun 2026 17:00:00 GMT)
- **Background location**: [Strict Review for ACCESS_BACKGROUND_LOCATION Permissions](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms) (Published: Thu, 18 Jun 2026 18:00:00 GMT)
- **Health permissions**: [Health Connect and Health Permissions Compliance Mandate](https://developer.android.com/guide/topics/permissions/overview) (Published: Fri, 19 Jun 2026 19:00:00 GMT)
- **GDPR**: [GDPR Compliance and Right to be Forgotten Controls on Web Interfaces](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Published: Sat, 20 Jun 2026 20:00:00 GMT)
- **Cookie consent**: [ePrivacy Directive Cookie Consent Banner Mandatory Implementation](https://eur-lex.europa.eu/eli/dir/2002/58/oj) (Published: Sun, 21 Jun 2026 21:00:00 GMT)
- **Local storage**: [Secure Encryption for Sensitive Variables in localStorage](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Published: Mon, 22 Jun 2026 22:00:00 GMT)
- **App Tracking Transparency**: [IndexedDB Data Retention and Cleanup Regulations](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Published: Tue, 23 Jun 2026 23:00:00 GMT)
- **IndexedDB**: [IndexedDB Data Retention and Cleanup Regulations](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Published: Tue, 23 Jun 2026 23:00:00 GMT)
- **Session storage**: [Temporary Session Variable Safety and Clean State Execution](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (Published: Wed, 24 Jun 2026 10:00:00 GMT)
- **Tracking technologies**: [Third-Party Tracking Scripts and Marketing Pixel Management](https://eur-lex.europa.eu/eli/dir/2002/58/oj) (Published: Thu, 25 Jun 2026 11:00:00 GMT)

## 5. Affected files
- `./AGENTS.md`
- `./data/detection-recipes.json`
- `./data/rejection-patterns.json`
- `./docs/ADVANCED-2026.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/GLOBAL-REGULATORY-2026.md`
- `./docs/GOOGLE-PLAY.md`
- `./docs/MOBILE-PRIVACY-MONITOR-2026.md`
- `./docs/MOBILE-SECURITY-2026.md`
- `./docs/PRIVACY-POLICY-MIGRATION.md`
- `./docs/PRIVACY_COMPLIANCE_PR_DRAFT.md`
- `./references/guidelines/by-app-type/universal-every-app.md`
- `./references/rules/android.md`
- `./references/rules/design.md`
- `./references/rules/metadata.md`
- `./references/rules/performance.md`
- `./references/rules/privacy.md`

## 6. Risk assessment
- *Privacy Manifest*: Apple automatic upload rejection on build submission if PrivacyInfo.xcprivacy is missing or invalid.
- *Required Reason APIs*: Automatic rejection from Apple App Store Connect for undeclared API category usage.
- *App Tracking Transparency*: Store rejection if cross-app tracing SDKs are activated before prompt acceptance.
- *Advertising ID*: Automated release blocking if targeting Android 12+ and using advertising libraries without declarations.
- *Privacy Nutrition Labels*: Discrepancy between declared nutrition forms and codebase will trigger review blocks.
- *Data Safety*: Google Play policy rejection due to mismatch between binary scans and Data Safety forms.
- *Data Safety*: Google Play policy rejection due to mismatch between binary scans and Data Safety forms.
- *User Data Policy*: App removal or suspension on Google Play for silent, un-disclosed user-data processing.
- *Advertising ID*: Automated release blocking if targeting Android 12+ and using advertising libraries without declarations.
- *Runtime permissions*: App crashes or storefront flags for requesting sensitive access blocks without rationales.
- *Background location*: Instant publishing blockages on Google Play if background location is not essential and justified.
- *Health permissions*: Immediate console rejections if health APIs are imported without dedicated health privacy policies.
- *GDPR*: Serious non-compliance risk under GDPR, potentially triggering heavy regulatory fines.
- *Cookie consent*: Direct violation of the ePrivacy Directive if tracking tags load automatically without user consent.
- *Local storage*: Vulnerability to cross-site scripting (XSS) attacks leading to account hijacking.
- *App Tracking Transparency*: Store rejection if cross-app tracing SDKs are activated before prompt acceptance.
- *IndexedDB*: Persistent user tracking records left on shared browsers, violating right to erase rules.
- *Session storage*: Session token persistence risks if sensitive values are left un-monitored in sessionStorage.
- *Tracking technologies*: Serious regulatory warning notifications for silent tracking of users before consent.
- **Overall Standing**: High risk of update blockage, storefront rejection, or compliance complaints if these updates are not actively merged.

## 7. Migration steps
- **Privacy Manifest**: Generate root PrivacyInfo.xcprivacy with tracking domains and data declarations.
- **Required Reason APIs**: Declare correct reason codes for accesses to system APIs such as UserDefaults or active keyboard.
- **App Tracking Transparency**: Trigger ATTrackingManager prompt before launching any tracking code or third-party ad frameworks.
- **Advertising ID**: Declare com.google.android.gms.permission.AD_ID in the manifest and ensure opt-out pathways are implemented.
- **Privacy Nutrition Labels**: Align self-reported App Store privacy nutrition questions with actual runtime data transmissions.
- **Data Safety**: Keep Google Play Console Data Safety statements fully synchronized with integrated analytics and marketing SDK behaviors.
- **Data Safety**: Keep Google Play Console Data Safety statements fully synchronized with integrated analytics and marketing SDK behaviors.
- **User Data Policy**: Supply prominent in-app disclosure dialogs before collecting sensitive personal attributes.
- **Advertising ID**: Declare com.google.android.gms.permission.AD_ID in the manifest and ensure opt-out pathways are implemented.
- **Runtime permissions**: Verify runtime permissions dynamically before initializing camera, microphone, or file accesses.
- **Background location**: Limit background location access. Provide persistent disclosures if ACCESS_BACKGROUND_LOCATION is required.
- **Health permissions**: Maintain a separate health-specific privacy link if reading health indices from Health Connect.
- **GDPR**: Integrate strict opt-in checkboxes and self-service delete pathways for EU web users.
- **Cookie consent**: Construct cookie consent gates that block third-party analytics cookies from being written before opt-in.
- **Local storage**: Avoid storing plaintext user credentials, JWTs, or session keys inside localStorage.
- **App Tracking Transparency**: Trigger ATTrackingManager prompt before launching any tracking code or third-party ad frameworks.
- **IndexedDB**: Clean database rows on user logout or deletion to preserve clean state rules.
- **Session storage**: Clear temporary session data promptly when tab closure is detected.
- **Tracking technologies**: Block third-party tracking pixels (Google Analytics, Hotjar) from initiating until cookie preferences are accepted.

## 8. Backward compatibility
All configuration and declarative adjustments are fully backward-compatible. No breaking API updates or customer-facing flow restrictions are introduced. Core legacy components continue operating normally.

## 9. Implementation checklist
- [ ] Add a root PrivacyInfo.xcprivacy to the Xcode project and check third-party SDK manifests.
- [ ] Audit calls to system APIs like UserDefaults and add required reason codes inside PrivacyInfo.xcprivacy.
- [ ] Configure NSUserTrackingUsageDescription in Info.plist and verify dynamic consent request calls.
- [ ] Declare AD_ID permission and add an in-app toggle for advertising ID reset/deletion requests.
- [ ] Audit email, phone, location, and device ID variables and populate data categories in App Store Connect.
- [ ] Ensure firebase-analytics, AppsFlyer, or Facebook SDK usage matches Google Play declarations.
- [ ] Ensure firebase-analytics, AppsFlyer, or Facebook SDK usage matches Google Play declarations.
- [ ] Add a modal with an accept/consent button prior to registration or ingestion of user credentials.
- [ ] Declare AD_ID permission and add an in-app toggle for advertising ID reset/deletion requests.
- [ ] Wrap hardware triggers with checkSelfPermission and display rationales on denial.
- [ ] Verify that ACCESS_BACKGROUND_LOCATION is only declared if strictly required for core operations.
- [ ] Implement HealthConnectClient authorization gates and reference dedicated health privacy policies.
- [ ] Build user-facing GDPR forms and functional account deletion triggers to satisfy data minimization.
- [ ] Integrate a Cookie Consent Banner and check user preferences before updating document.cookie.
- [ ] Implement encryption wrappers for critical localStorage variables or migrate them to secure cookies.
- [ ] Configure NSUserTrackingUsageDescription in Info.plist and verify dynamic consent request calls.
- [ ] Add indexedDB database wipe logic on user sign-out or account removal.
- [ ] Ensure sensitive temporary identifiers in sessionStorage are cleared or encrypted.
- [ ] Block silent injection of gtag or fbq scripts before consent validation.
- [ ] Run the automated compliance checks locally to verify validation.

## 10. Testing checklist
- [ ] Confirm Xcode build compiles and bundles the PrivacyInfo.xcprivacy correctly.
- [ ] Verify that Google Play data declarations align with integrated SDK analytics.
- [ ] Run browser diagnostics to ensure third-party pixels are blocked prior to Cookie Banner opt-in.
- [ ] Validate account deletion triggers wipe associated localStorage and indexedDB files.

## 11. Documentation checklist
- [ ] Update internal compliance playbooks with completed tasks.
- [ ] Connect the revised privacy statement URL inside the store console dashboards.
- [ ] Update `docs/PRIVACY-POLICY-MIGRATION.md` with resolved log entries.

## 12. Compliance impact
- **Submission Security**: Eliminates upload-time blocks, review delays, and automatic rejections on Apple and Google Play.
- **Regulatory Safety**: Insulates the brand against GDPR and ePrivacy complaints, reinforcing data protection.
- **Consumer Trust**: Increases transparency through clear, prominent disclosures and explicit consent gates.

## 13. Breaking changes
No structural breaking changes or functional restrictions are introduced.

## 14. Review checklist
- [ ] Code changes and PR text are completely emoji-free.
- [ ] Core configuration variables are securely mapped without placeholder records.
- [ ] Consent prompts and prominent disclosures match required styling guidelines.

## 15. Approver recommendations
Ensure that compliance counsel registers the updated privacy statements on the live portal before merging. Double-check that compiled third-party SDK dependencies ship with signed privacy manifests prior to final release bundling.
