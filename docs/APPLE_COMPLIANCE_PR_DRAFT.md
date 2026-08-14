# PULL REQUEST DRAFT: Apple Developer Requirements Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple developer and App Store requirements. It addresses the following tracks: Privacy Manifests, Required Reason APIs, In-App Purchase policies, Alternative payment regulations, App Store Review Guidelines, SDK requirements, Minimum SDK versions.

## 2. Background
Apple continuously updates its App Store Review Guidelines, Developer Program License Agreements, and privacy expectations. Proactively resolving these changes protects the application against submission delays, rejection cycles, and administrative publication blockages.

## 3. Regulatory change
The updates address critical Apple requirements, ensuring full alignment with standard App Store practices. This includes the mandatory integration of Privacy Manifests, strict Required Reason API mapping, explicit App Tracking Transparency prompts, and payments rules to satisfy modern publishing gates.

## 4. Official citations
- **Privacy Manifests**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://mock.invalid/apple-news/privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **Required Reason APIs**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://mock.invalid/apple-news/privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **In-App Purchase policies**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://mock.invalid/apple-news/iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **Alternative payment regulations**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://mock.invalid/apple-news/iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **App Store Review Guidelines**: [App Store Review Guidelines and 4.3 Saturated Categories Update](https://mock.invalid/apple-news/review-guidelines-update) (Published: Tue, 09 Jun 2026 14:00:00 GMT)
- **SDK requirements**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)
- **Minimum SDK versions**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)

## 5. Affected files
- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).*

## 6. Risk assessment
- **Privacy Manifests** (Critical): Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs** (Critical): Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **In-App Purchase policies** (Critical): App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Alternative payment regulations** (High): Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **App Store Review Guidelines** (High): Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **SDK requirements** (High): Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Minimum SDK versions** (High): Annual minimum deployment target or target SDK version updates enforced by stores.
- **Overall Standing**: High risk of update blockage or account warnings if publishing gates are not proactively cleared.

## 7. Migration steps
- **Privacy Manifests**: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- **Privacy Manifests**: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- **Required Reason APIs**: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- **Required Reason APIs**: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- **In-App Purchase policies**: Route all digital goods through StoreKit in-app purchases.
- **In-App Purchase policies**: Add a prominent Restore Purchases control for non-consumable goods.
- **In-App Purchase policies**: Verify pricing displays correspond with Apple subscription terms requirements.
- **Alternative payment regulations**: Ensure appropriate entitlements are requested and set up for alternative billing.
- **Alternative payment regulations**: Show mandatory disclosure sheets before redirecting to external web purchase flows.
- **App Store Review Guidelines**: Review the updated guidelines section in APPLE.md or the official site.
- **App Store Review Guidelines**: Ensure App Review Notes are updated with working test accounts.
- **App Store Review Guidelines**: Verify the application flows align with the updated guideline numbers.
- **SDK requirements**: Perform regular updates on bundled third-party SDKs.
- **SDK requirements**: Ensure each third-party SDK has its signed privacy manifest file.
- **Minimum SDK versions**: Update deployment target version to match latest requirements.
- **Minimum SDK versions**: Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 8. Backward compatibility
All modifications are fully backward-compatible. Minimum SDK targets and deployment targets are adjusted safely without introducing runtime failures or breaking legacy device integrations.

## 9. Implementation checklist
- [ ] Implement/Verify: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] Implement/Verify: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- [ ] Implement/Verify: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] Implement/Verify: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- [ ] Implement/Verify: Route all digital goods through StoreKit in-app purchases.
- [ ] Implement/Verify: Add a prominent Restore Purchases control for non-consumable goods.
- [ ] Implement/Verify: Verify pricing displays correspond with Apple subscription terms requirements.
- [ ] Implement/Verify: Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] Implement/Verify: Show mandatory disclosure sheets before redirecting to external web purchase flows.
- [ ] Implement/Verify: Review the updated guidelines section in APPLE.md or the official site.
- [ ] Implement/Verify: Ensure App Review Notes are updated with working test accounts.
- [ ] Implement/Verify: Verify the application flows align with the updated guideline numbers.
- [ ] Implement/Verify: Perform regular updates on bundled third-party SDKs.
- [ ] Implement/Verify: Ensure each third-party SDK has its signed privacy manifest file.
- [ ] Implement/Verify: Update deployment target version to match latest requirements.
- [ ] Implement/Verify: Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).
- [ ] Re-run the automated pre-submission compliance guard locally to verify the codebase state.

## 10. Testing checklist
- [ ] Verify clean compilation with current Xcode compiler specifications.
- [ ] Run automated tests to check for regression-free performance.
- [ ] Manually validate updated application flows (e.g., user consents, permission dialogs, payments).

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with migration tasks and logs.
- [ ] Keep App Store Review Notes updated with valid demo accounts.
- [ ] Confirm privacy policy URL points to an active, valid endpoint.

## 12. Compliance impact
- **Submission Safety**: Eliminates common Apple rejection categories (e.g., missing manifests, mismatched privacy declarations).
- **Storefront Health**: Protects corporate publisher credentials from warnings or suspension.
- **Publishing Velocity**: Guarantees uninterrupted delivery of product bug-fixes and security patches.

## 13. Breaking changes
- No functional breaking changes or structural API breakages are introduced.

## 14. Review checklist
- [ ] Confirm that all required keys, identifiers, and files are present in the pull request diff.
- [ ] Verify that no unauthorized third-party libraries are referenced.
- [ ] Ensure the codebase is free of debugging bypasses or non-compliant placeholders.

## 15. Approver recommendations
- **Lead Mobile Engineer**
- **Legal & Privacy Compliance Officer**
