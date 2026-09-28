<!-- APPLE_POLICY_MONITOR_START -->

> **Simulated output, not live announcements.** This file was generated from sample
> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,
> publish dates, and descriptions below are examples that show the shape of a migration
> report, not real publications. Only the linked official documentation URLs are real.
> Re-run the monitor with `--live` against the real feeds before treating anything here
> as an actual requirement.

# Apple Developer Requirements Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor.py` to track Apple developer requirements.

## Monitored Requirements Update Log

### 1. [Privacy Manifests] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-requirements](https://developer.apple.com/news/?id=privacy-requirements)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Critical
- **Repository Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 2. [Required Reason APIs] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=privacy-requirements](https://developer.apple.com/news/?id=privacy-requirements)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Critical
- **Repository Impact**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 3. [In-App Purchase policies] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=iap-updates](https://developer.apple.com/news/?id=iap-updates)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Critical
- **Repository Impact**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 4. [Alternative payment regulations] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=iap-updates](https://developer.apple.com/news/?id=iap-updates)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 5. [App Store Review Guidelines] App Store Review Guidelines and 4.3 Saturated Categories Update
- **Published Date**: Tue, 09 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=review-guidelines-update](https://developer.apple.com/news/?id=review-guidelines-update)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 6. [Xcode requirements] Upcoming SDK minimum requirements and Xcode 26 Mandate
- **Published Date**: Tue, 03 Feb 2026 08:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/?id=ueeok6yw](https://developer.apple.com/news/?id=ueeok6yw)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Enforced Xcode versions for compiling App Store submissions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 7. [Apple Developer Program License Agreement] Apple Developer Program License Agreement Terms Update
- **Published Date**: Wed, 10 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/terms/](https://developer.apple.com/terms/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- **Scan Verdict**: Found 1 file(s) matching signature patterns and extensions.
- **Affected Files**:
  - `LICENSE`

### 8. [Human Interface Guidelines] Human Interface Guidelines: Spatial Computing and Layout Standards
- **Published Date**: Thu, 11 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://developer.apple.com/design/human-interface-guidelines/](https://developer.apple.com/design/human-interface-guidelines/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: UI/UX layout changes recommended or mandated by Apple.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 9. [App Tracking Transparency] App Tracking Transparency Policy Enforcement and IDFA Consent
- **Published Date**: Fri, 12 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://developer.apple.com/app-store/user-privacy-and-data-use/](https://developer.apple.com/app-store/user-privacy-and-data-use/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Tracking consent rules and IDFA access restrictions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 10. [Sign in with Apple] Sign in with Apple Requirement Enforcement
- **Published Date**: Sat, 13 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://developer.apple.com/sign-in-with-apple/](https://developer.apple.com/sign-in-with-apple/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Requirement to offer Sign in with Apple alongside any other third-party social login.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 11. [Apple Developer Program License Agreement] Digital Markets Act Compliance Options for EU App Distribution
- **Published Date**: Sun, 14 Jun 2026 15:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/dma-asia-eu/](https://developer.apple.com/support/dma-asia-eu/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- **Scan Verdict**: Found 1 file(s) matching signature patterns and extensions.
- **Affected Files**:
  - `LICENSE`

### 12. [DMA compliance changes] Digital Markets Act Compliance Options for EU App Distribution
- **Published Date**: Sun, 14 Jun 2026 15:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/dma-asia-eu/](https://developer.apple.com/support/dma-asia-eu/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: EU Digital Markets Act requirements for alternative app marketplaces, browser engines, and external link rules.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 13. [Apple Privacy requirements] App Store Accessibility Nutrition Labels and VoiceOver Standards
- **Published Date**: Mon, 15 Jun 2026 16:00:00 GMT
- **Official Resource**: [https://developer.apple.com/accessibility/](https://developer.apple.com/accessibility/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Global updates to Apple's privacy policy requirements and user consent flows.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 14. [Accessibility requirements] App Store Accessibility Nutrition Labels and VoiceOver Standards
- **Published Date**: Mon, 15 Jun 2026 16:00:00 GMT
- **Official Resource**: [https://developer.apple.com/accessibility/](https://developer.apple.com/accessibility/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Accessibility standards compliance (WCAG 2.1 AA / EN 301 549) and App Store Accessibility Nutrition Labels.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 15. [AI-related App Store policies] Generative AI Safety, Consent, and Moderation Requirements
- **Published Date**: Tue, 16 Jun 2026 17:00:00 GMT
- **Official Resource**: [https://developer.apple.com/app-store/review/guidelines/#generative-ai](https://developer.apple.com/app-store/review/guidelines/#generative-ai)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: User consent and content moderation rules for AI models and Generative AI chatbot outputs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 16. [Child safety requirements] Kids Category and Child Safety Protection Guidelines
- **Published Date**: Wed, 17 Jun 2026 18:00:00 GMT
- **Official Resource**: [https://developer.apple.com/app-store/kids-apps/](https://developer.apple.com/app-store/kids-apps/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Critical
- **Repository Impact**: Strict constraints on apps targeted at children, COPPA compliance, and CSAM reporting duties.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 17. [HealthKit policies] HealthKit Privacy Rules and Data Usage Limits
- **Published Date**: Thu, 18 Jun 2026 19:00:00 GMT
- **Official Resource**: [https://developer.apple.com/healthkit/](https://developer.apple.com/healthkit/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Restrictions on HealthKit data mining, usage of health data for ads, and mandatory user permission descriptions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 18. [Location permissions] Location Permission Justification and Background Usage Audit
- **Published Date**: Fri, 19 Jun 2026 20:00:00 GMT
- **Official Resource**: [https://developer.apple.com/documentation/corelocation](https://developer.apple.com/documentation/corelocation)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Stricter constraints, usage descriptions, and prominent disclosures for access to location.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 19. [Apple Developer Program License Agreement] Camera and Microphone Usage Description Guidelines
- **Published Date**: Sat, 20 Jun 2026 21:00:00 GMT
- **Official Resource**: [https://developer.apple.com/documentation/avfoundation](https://developer.apple.com/documentation/avfoundation)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- **Scan Verdict**: Found 1 file(s) matching signature patterns and extensions.
- **Affected Files**:
  - `LICENSE`

### 20. [Push Notification requirements] Push Notification Authorization and APNs Payload Security
- **Published Date**: Sun, 21 Jun 2026 22:00:00 GMT
- **Official Resource**: [https://developer.apple.com/notifications/](https://developer.apple.com/notifications/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Security, opt-in prompts, and payload specifications for Push Notifications.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 21. [Background execution policies] UIBackgroundModes Enforcement and Resource Usage Audits
- **Published Date**: Mon, 22 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://developer.apple.com/documentation/uikit/app_lifecycle](https://developer.apple.com/documentation/uikit/app_lifecycle)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Strict limitation of background execution categories to prevent resource/battery drain.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 22. [Security updates] Security Declarations and Non-Exempt Encryption Requirements
- **Published Date**: Tue, 23 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://developer.apple.com/security/](https://developer.apple.com/security/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Security updates, encryption declarations, and external dependencies vulnerability checks.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 23. [Privacy Manifests] Third-Party SDK Security Audits and Privacy Manifest Bundling
- **Published Date**: Wed, 24 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/third-party-SDK-requirements/](https://developer.apple.com/support/third-party-SDK-requirements/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Critical
- **Repository Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 24. [Security updates] Third-Party SDK Security Audits and Privacy Manifest Bundling
- **Published Date**: Wed, 24 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/third-party-SDK-requirements/](https://developer.apple.com/support/third-party-SDK-requirements/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Security updates, encryption declarations, and external dependencies vulnerability checks.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 25. [SDK requirements] Third-Party SDK Security Audits and Privacy Manifest Bundling
- **Published Date**: Wed, 24 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/third-party-SDK-requirements/](https://developer.apple.com/support/third-party-SDK-requirements/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: High
- **Repository Impact**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 26. [Apple Developer Program License Agreement] Minimum Deployment Target and Platform SDK Policy
- **Published Date**: Thu, 25 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://developer.apple.com/support/xcode/](https://developer.apple.com/support/xcode/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- **Scan Verdict**: Found 1 file(s) matching signature patterns and extensions.
- **Affected Files**:
  - `LICENSE`

### 27. [Swift requirements] Swift 6 Language Safety and Strict Concurrency Audits
- **Published Date**: Fri, 26 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://developer.apple.com/swift/](https://developer.apple.com/swift/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Evolving Swift language standards, compiler features, and data-race safety requirements.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 28. [App Store Connect announcements] App Store Connect Portal Updates and Store Listing Schema
- **Published Date**: Sat, 27 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://developer.apple.com/app-store-connect/](https://developer.apple.com/app-store-connect/)
- **Verification Status**: Priority 1 (Verified)
- **Severity / Release Impact**: Medium
- **Repository Impact**: Administrative and portal changes published in App Store Connect announcements.
- **Scan Verdict**: Found 8 file(s) matching signature patterns and extensions.
- **Affected Files**:
  - `agent-os/hooks/app-store-compliance-guard.sh`
  - `agent-os/hooks/app-store-compliance-guard-test.sh`
  - `scripts/metadata-audit-test.sh`
  - `scripts/metadata-audit.py`
  - `scripts/release-audit.py`
  - `scripts/monitor.py`
  - `scripts/pull-metadata.sh`
  - `scripts/monitor-regulatory-test.sh`

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifests
- **Release Impact**: Critical
- **Repository Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- [ ] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### Tasks for Required Reason APIs
- **Release Impact**: Critical
- **Repository Impact**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- [ ] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### Tasks for In-App Purchase policies
- **Release Impact**: Critical
- **Repository Impact**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- [ ] Route all digital goods through StoreKit in-app purchases.
- [ ] Add a prominent Restore Purchases control for non-consumable goods.
- [ ] Verify pricing displays correspond with Apple subscription terms requirements.

### Tasks for Alternative payment regulations
- **Release Impact**: High
- **Repository Impact**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- [ ] Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] Show mandatory disclosure sheets before redirecting to external web purchase flows.

### Tasks for App Store Review Guidelines
- **Release Impact**: High
- **Repository Impact**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- [ ] Review the updated guidelines section in APPLE.md or the official site.
- [ ] Ensure App Review Notes are updated with working test accounts.
- [ ] Verify the application flows align with the updated guideline numbers.

### Tasks for Xcode requirements
- **Release Impact**: High
- **Repository Impact**: Enforced Xcode versions for compiling App Store submissions.
- [ ] Upgrade build machine/CI to Xcode 26 (or required version).
- [ ] Resolve any newly introduced compiler deprecations/warnings.

### Tasks for Apple Developer Program License Agreement
- **Release Impact**: Medium
- **Repository Impact**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- [ ] Log in to App Store Connect as the Account Holder.
- [ ] Accept the latest Program License Agreement.
- [ ] Review any changes regarding company distribution versus individual distribution rules.

### Tasks for Human Interface Guidelines
- **Release Impact**: Medium
- **Repository Impact**: UI/UX layout changes recommended or mandated by Apple.
- [ ] Check user interface elements against current design recommendations in HIG.
- [ ] Verify touch targets are at least 44x44pt on iOS.
- [ ] Test dark mode and dynamic type sizing rendering.

### Tasks for App Tracking Transparency
- **Release Impact**: High
- **Repository Impact**: Tracking consent rules and IDFA access restrictions.
- [ ] Verify ATTrackingManager.requestTrackingAuthorization is called before starting any tracking.
- [ ] Add NSUserTrackingUsageDescription with a clear reason explaining why tracking is used.

### Tasks for Sign in with Apple
- **Release Impact**: High
- **Repository Impact**: Requirement to offer Sign in with Apple alongside any other third-party social login.
- [ ] Verify that Sign in with Apple is offered at least as prominently as other social logins.
- [ ] Ensure email private relays are supported and profiles are handled gracefully on first login.

### Tasks for DMA compliance changes
- **Release Impact**: High
- **Repository Impact**: EU Digital Markets Act requirements for alternative app marketplaces, browser engines, and external link rules.
- [ ] Declare alternative distribution entitlements if publishing outside App Store in the EU.
- [ ] Implement EU-specific disclosure sheets and fee-math checks if using external link entitlements.

### Tasks for Apple Privacy requirements
- **Release Impact**: High
- **Repository Impact**: Global updates to Apple's privacy policy requirements and user consent flows.
- [ ] Publish or update your privacy policy URL.
- [ ] Confirm in-app accessibility to the privacy policy link.
- [ ] Verify data declaration matches actual SDK data collection.

### Tasks for Accessibility requirements
- **Release Impact**: Medium
- **Repository Impact**: Accessibility standards compliance (WCAG 2.1 AA / EN 301 549) and App Store Accessibility Nutrition Labels.
- [ ] Audit UI elements for accessibility labels and traits.
- [ ] Verify dynamic font resizing is supported.
- [ ] Populate Accessibility Nutrition Labels in App Store Connect.

### Tasks for AI-related App Store policies
- **Release Impact**: High
- **Repository Impact**: User consent and content moderation rules for AI models and Generative AI chatbot outputs.
- [ ] Show a consent modal naming the AI provider before any personal data is sent.
- [ ] Provide robust content moderation, reporting, and blocking for any user-generated or AI-generated content.

### Tasks for Child safety requirements
- **Release Impact**: Critical
- **Repository Impact**: Strict constraints on apps targeted at children, COPPA compliance, and CSAM reporting duties.
- [ ] Ensure no third-party ad or tracking SDKs are present in kids-targeted apps.
- [ ] Place parental gates on any external links or in-app purchases.
- [ ] Integrate NCMEC reporting flows on actual knowledge of CSAM (for US UGC apps).

### Tasks for HealthKit policies
- **Release Impact**: High
- **Repository Impact**: Restrictions on HealthKit data mining, usage of health data for ads, and mandatory user permission descriptions.
- [ ] Ensure HealthKit data is never used for advertising, marketing, or behavioral tracking.
- [ ] Add detailed HealthKit share and update usage descriptions to Info.plist.

### Tasks for Location permissions
- **Release Impact**: High
- **Repository Impact**: Stricter constraints, usage descriptions, and prominent disclosures for access to location.
- [ ] Check that location requests match real, visible user-facing features.
- [ ] Include precise, specific usage descriptions in Info.plist explaining what features require location.

### Tasks for Push Notification requirements
- **Release Impact**: Medium
- **Repository Impact**: Security, opt-in prompts, and payload specifications for Push Notifications.
- [ ] Verify aps-environment is set to development/production in entitlements.
- [ ] Ensure user consent is requested and handled gracefully before registering for remote notifications.

### Tasks for Background execution policies
- **Release Impact**: High
- **Repository Impact**: Strict limitation of background execution categories to prevent resource/battery drain.
- [ ] Verify UIBackgroundModes keys match the actual, documented core functionality (e.g. audio, VoIP).
- [ ] Remove unused background execution declarations to avoid automatic rejection.

### Tasks for Security updates
- **Release Impact**: Medium
- **Repository Impact**: Security updates, encryption declarations, and external dependencies vulnerability checks.
- [ ] Review Info.plist for ITSAppUsesNonExemptEncryption.
- [ ] Upload ANSSI encryption declaration if distributing non-exempt encryption in France.
- [ ] Perform dependency audit for known CVEs.

### Tasks for SDK requirements
- **Release Impact**: High
- **Repository Impact**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- [ ] Perform regular updates on bundled third-party SDKs.
- [ ] Ensure each third-party SDK has its signed privacy manifest file.

### Tasks for Swift requirements
- **Release Impact**: Medium
- **Repository Impact**: Evolving Swift language standards, compiler features, and data-race safety requirements.
- [ ] Verify SWIFT_VERSION is at least 5.x or 6.0.
- [ ] Resolve strict concurrency issues if migrating to Swift 6 compiler runtime.

### Tasks for App Store Connect announcements
- **Release Impact**: Medium
- **Repository Impact**: Administrative and portal changes published in App Store Connect announcements.
- [ ] Check the metadata and publishing workflows for impact.
- [ ] Verify store listing parameters match the latest schema.

<!-- APPLE_POLICY_MONITOR_END -->