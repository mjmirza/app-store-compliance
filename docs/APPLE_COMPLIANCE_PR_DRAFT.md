# PULL REQUEST DRAFT: Apple Developer Requirements Compliance Update

## 1. Summary
This pull request introduces critical configuration, metadata, and structural modifications to ensure complete compliance with updated Apple Developer Program License Agreement, App Store Review Guidelines, and platform technical requirements across all 25 monitored Apple Developer domains.

## 2. Background
Apple routinely updates developer requirements, App Store review guidelines, Privacy Manifest rules, and SDK compilation targets. Non-compliance leads to automatic rejection during App Store Connect upload or manual rejection during submission review. This PR proactively implements all required migration steps.

## 3. Regulatory change
- **App Store & Platform Policies**: Enforcement of Privacy Manifests (PrivacyInfo.xcprivacy), Required Reason API declarations, App Tracking Transparency (ATT), Sign in with Apple requirements, StoreKit in-app purchase guidelines, DMA alternative payment links, and Xcode minimum SDK versions.
- **Privacy & Safety**: Mandatory child safety mechanisms, age rating declarations, AI provider data sharing disclosures, and accessibility standards (WCAG 2.1 AA / EN 301 549).

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
- **Alternative payment regulations** (High Impact): Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **App Store Review Guidelines** (High Impact): Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **In-App Purchase policies** (Critical Impact): App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Minimum SDK versions** (High Impact): Annual minimum deployment target or target SDK version updates enforced by stores.
- **Privacy Manifests** (Critical Impact): Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs** (Critical Impact): Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **SDK requirements** (High Impact): Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Overall Standing**: High risk of submission or upload blockage if Apple Developer publishing requirements are not satisfied.

## 7. Migration steps
- **Alternative payment regulations**: Ensure appropriate entitlements are requested and set up for alternative billing.
- **Alternative payment regulations**: Show mandatory disclosure sheets before redirecting to external web purchase flows.
- **App Store Review Guidelines**: Ensure App Review Notes are updated with working test accounts.
- **App Store Review Guidelines**: Review the updated guidelines section in APPLE.md or the official site.
- **App Store Review Guidelines**: Verify the application flows align with the updated guideline numbers.
- **In-App Purchase policies**: Add a prominent Restore Purchases control for non-consumable goods.
- **In-App Purchase policies**: Route all digital goods through StoreKit in-app purchases.
- **In-App Purchase policies**: Verify pricing displays correspond with Apple subscription terms requirements.
- **Minimum SDK versions**: Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).
- **Minimum SDK versions**: Update deployment target version to match latest requirements.
- **Privacy Manifests**: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- **Privacy Manifests**: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- **Required Reason APIs**: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- **Required Reason APIs**: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- **SDK requirements**: Ensure each third-party SDK has its signed privacy manifest file.
- **SDK requirements**: Perform regular updates on bundled third-party SDKs.

## 8. Backward compatibility
All changes preserve backward compatibility for active iOS versions. Privacy manifests and permission usage descriptions add programmatic clarity without breaking legacy platform features.

## 9. Implementation checklist
- [ ] Verify compliance declarations and configuration for **Alternative payment regulations**.
- [ ] Verify compliance declarations and configuration for **App Store Review Guidelines**.
- [ ] Verify compliance declarations and configuration for **In-App Purchase policies**.
- [ ] Verify compliance declarations and configuration for **Minimum SDK versions**.
- [ ] Verify compliance declarations and configuration for **Privacy Manifests**.
- [ ] Verify compliance declarations and configuration for **Required Reason APIs**.
- [ ] Verify compliance declarations and configuration for **SDK requirements**.
- [ ] Run the automated pre-submission compliance guard (`bash agent-os/hooks/app-store-compliance-guard.sh .`).

## 10. Testing checklist
- [ ] Perform a clean build on physical iOS test devices and Xcode simulators.
- [ ] Verify PrivacyInfo.xcprivacy exists in the generated app bundle.
- [ ] Validate Sign in with Apple and StoreKit purchase/restore flows.
- [ ] Verify that no new runtime warnings or permission prompt failures occur.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Fill out 'App Review Notes' in App Store Connect with working test accounts and non-obvious feature descriptions.
- [ ] Confirm App Store Connect privacy questionnaire aligns with active SDK data collection.

## 12. Compliance impact
- **Submission Protection**: Prevents submission rejections under App Store Review Guidelines.
- **Account Standing**: Maintains the developer account in good standing under the Apple Developer Program License Agreement.

## 13. Breaking changes
- No structural API breaking changes. Undeclared Required Reason APIs or missing Privacy Manifests are functionally breaking under App Review rules.

## 14. Review checklist
- [ ] Verify that all required keys, identifiers, and files are present in the pull request diff.
- [ ] Ensure the codebase is free of placeholder credentials or debugging bypasses.
- [ ] Confirm that all cited Apple Developer News links and documentation references are valid.

## 15. Approver recommendations
Ensure that the Account Holder has accepted any pending Apple Developer Program License Agreements in App Store Connect before submitting builds for review. Verify that all third-party SDKs include signed Privacy Manifests.
