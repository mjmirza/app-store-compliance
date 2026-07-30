<!-- PRIVACY_POLICY_MONITOR_START -->
# Mobile and Web Privacy Compliance Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-privacy.py` to track compliance areas.

## Monitored Privacy Requirements Update Log

### 1. [Privacy Manifest] Apple Mandatory Privacy Manifest Framework Implementation Deadline
- **Published Date**: Wed, 10 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-manifest-mandate](https://developer.apple.com/news/?id=privacy-manifest-mandate)
- **Description**: Apple announces strict validation rules for third-party SDK bundles. All binary uploads must contain a valid signed PrivacyInfo.xcprivacy detailing tracking domains and collected data types.

### 2. [Required Reason APIs] Strict Rejection Gate for Declared Reason API Violations
- **Published Date**: Thu, 11 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=required-reason-apis](https://developer.apple.com/news/?id=required-reason-apis)
- **Description**: Apple is initiating automated rejections for builds invoking system APIs like systemUptime, ProcessInfo, or UserDefaults without specific and valid reason codes mapped in the app bundle manifest.

### 3. [App Tracking Transparency] App Tracking Transparency Opt-In Enforcement Clarification
- **Published Date**: Fri, 12 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=att-enforcement](https://developer.apple.com/news/?id=att-enforcement)
- **Description**: App Review clarifies that accessing the Advertising Identifier (IDFA) or sharing device fingerprints requires prior user opt-in via the ATTrackingManager prompt. Failing to present the prompt leads to an automatic rejection.

### 4. [Advertising ID] App Tracking Transparency Opt-In Enforcement Clarification
- **Published Date**: Fri, 12 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=att-enforcement](https://developer.apple.com/news/?id=att-enforcement)
- **Description**: App Review clarifies that accessing the Advertising Identifier (IDFA) or sharing device fingerprints requires prior user opt-in via the ATTrackingManager prompt. Failing to present the prompt leads to an automatic rejection.

### 5. [Privacy Nutrition Labels] Storefront Validation of Privacy Nutrition Labels Mismatch
- **Published Date**: Sat, 13 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-nutrition-labels](https://developer.apple.com/news/?id=privacy-nutrition-labels)
- **Description**: Apple requires all self-reported privacy labels in App Store Connect to be kept accurate. Discrepancies between compiled code transmission behavior and declared data safety labels will trigger review delays.

### 6. [Data Safety] Storefront Validation of Privacy Nutrition Labels Mismatch
- **Published Date**: Sat, 13 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-nutrition-labels](https://developer.apple.com/news/?id=privacy-nutrition-labels)
- **Description**: Apple requires all self-reported privacy labels in App Store Connect to be kept accurate. Discrepancies between compiled code transmission behavior and declared data safety labels will trigger review delays.

### 7. [Data Safety] Google Play Store Data Safety Form Compliance Verification
- **Published Date**: Sun, 14 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469)
- **Description**: Google Play increases automated static verification of app binaries to identify undeclared analytics and tracking SDK usage. Discrepancies in the Data Safety declaration will lead to update blockages.

### 8. [User Data Policy] Google Play User Data and Explicit Prominent Disclosure Policy
- **Published Date**: Mon, 15 Jun 2026 15:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/User-Data-Policy](https://support.google.com/googleplay/android-developer/answer/User-Data-Policy)
- **Description**: Apps collecting sensitive user credentials, contacts, or device files must display a prominent, clear modal explaining what data is collected, followed by explicit user consent before any ingestion occurs.

### 9. [Advertising ID] Google Play Services Advertising ID Policy and Opt-Out Requirements
- **Published Date**: Tue, 16 Jun 2026 16:00:00 GMT
- **Official Resource**: [https://support.google.com/googleplay/android-developer/answer/9899234](https://support.google.com/googleplay/android-developer/answer/9899234)
- **Description**: Apps declaring the AD_ID permission must support user opt-out and provide pathways to delete or reset the advertising identifier within the application interface or linked privacy statement.

### 10. [Runtime permissions] Mandatory Runtime Permission Flow and UX Validation
- **Published Date**: Wed, 17 Jun 2026 17:00:00 GMT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Description**: Google Play restricts broad access to system cameras, directories, and background resources. Apps must dynamically query permissions at runtime and supply clear rationales when users previously denied requests.

### 11. [Background location] Strict Review for ACCESS_BACKGROUND_LOCATION Permissions
- **Published Date**: Thu, 18 Jun 2026 18:00:00 GMT
- **Official Resource**: [https://developer.android.com/about/versions/14/changes/schedule-exact-alarms](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms)
- **Description**: Google Play strictly limits background location access. Developers must submit extensive core use-case justifications and prominently display persistent disclosures to clear the publishing gate.

### 12. [Health permissions] Health Connect and Health Permissions Compliance Mandate
- **Published Date**: Fri, 19 Jun 2026 19:00:00 GMT
- **Official Resource**: [https://developer.android.com/guide/topics/permissions/overview](https://developer.android.com/guide/topics/permissions/overview)
- **Description**: Accessing Health Connect APIs requires completed console questionnaires and a dedicated, in-app health privacy statement explaining step or heart-rate tracking purposes.

### 13. [GDPR] GDPR Compliance and Right to be Forgotten Controls on Web Interfaces
- **Published Date**: Sat, 20 Jun 2026 20:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Description**: Web interfaces processing data from EU residents must provide strict opt-in checkboxes and accessible self-service data deletion and extraction features in compliance with data minimization.

### 14. [Cookie consent] ePrivacy Directive Cookie Consent Banner Mandatory Implementation
- **Published Date**: Sun, 21 Jun 2026 21:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/dir/2002/58/oj](https://eur-lex.europa.eu/eli/dir/2002/58/oj)
- **Description**: Non-essential tracking cookies and local variables must not be saved on initial load before the user explicitly registers cookie acceptance on the consent banner.

### 15. [Local storage] Secure Encryption for Sensitive Variables in localStorage
- **Published Date**: Mon, 22 Jun 2026 22:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Description**: Storing plaintext authentication credentials or personal identifiers in localStorage is prohibited due to cross-site scripting risks. Store secrets securely and encrypt stored items.

### 16. [App Tracking Transparency] IndexedDB Data Retention and Cleanup Regulations
- **Published Date**: Tue, 23 Jun 2026 23:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Description**: Databases holding offline records must respect user tracking consent preferences and execute complete cleanup routines when users logout or invoke deletion rights.

### 17. [IndexedDB] IndexedDB Data Retention and Cleanup Regulations
- **Published Date**: Tue, 23 Jun 2026 23:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Description**: Databases holding offline records must respect user tracking consent preferences and execute complete cleanup routines when users logout or invoke deletion rights.

### 18. [Session storage] Temporary Session Variable Safety and Clean State Execution
- **Published Date**: Wed, 24 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Description**: Session identifiers and tokens must be limited, shielded from un-authorized scripts, and terminated immediately upon browser window or tab closure.

### 19. [Tracking technologies] Third-Party Tracking Scripts and Marketing Pixel Management
- **Published Date**: Thu, 25 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://eur-lex.europa.eu/eli/dir/2002/58/oj](https://eur-lex.europa.eu/eli/dir/2002/58/oj)
- **Description**: Third-party pixels and analytics tags must remain inactive until explicit cookie preferences are registered. Unmanaged, silent script injection violates web compliance laws.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifest
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Integrate `PrivacyInfo.xcprivacy` at Xcode project root.
- [ ] **Task 2**: Cross-reference third-party SDK dependencies for signed manifests.

### Tasks for Required Reason APIs
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Audit references to file timestamps, system boot time, or `UserDefaults`.
- [ ] **Task 2**: Supply valid reasons inside the `NSPrivacyAccessedAPITypes` manifest block.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Wire `ATTrackingManager.requestTrackingAuthorization` prior to tracker initialization.
- [ ] **Task 2**: Populate `NSUserTrackingUsageDescription` in Info.plist.

### Tasks for Advertising ID
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Advertising ID.

### Tasks for Privacy Nutrition Labels
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Privacy Nutrition Labels.

### Tasks for Data Safety
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Audit runtime tracking dependencies (Firebase, AppsFlyer) and update declarations.
- [ ] **Task 2**: Synchronize Google Play Console Data Safety form inputs.

### Tasks for Data Safety
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Audit runtime tracking dependencies (Firebase, AppsFlyer) and update declarations.
- [ ] **Task 2**: Synchronize Google Play Console Data Safety form inputs.

### Tasks for User Data Policy
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for User Data Policy.

### Tasks for Advertising ID
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Advertising ID.

### Tasks for Runtime permissions
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Runtime permissions.

### Tasks for Background location
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Background location.

### Tasks for Health permissions
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Health permissions.

### Tasks for GDPR
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Supply user-accessible account deletion button in-app/on-web.
- [ ] **Task 2**: Ensure user data purging covers linked third-party analytics storage.

### Tasks for Cookie consent
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Configure Cookie Consent Banner to block tracking scripts before opt-in.
- [ ] **Task 2**: Provide granular cookies preferences selectors.

### Tasks for Local storage
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Local storage.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task 1**: Wire `ATTrackingManager.requestTrackingAuthorization` prior to tracker initialization.
- [ ] **Task 2**: Populate `NSUserTrackingUsageDescription` in Info.plist.

### Tasks for IndexedDB
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for IndexedDB.

### Tasks for Session storage
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Session storage.

### Tasks for Tracking technologies
- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits.
- [ ] **Task**: Review, implement, and verify all compliance criteria for Tracking technologies.

<!-- PRIVACY_POLICY_MONITOR_END -->