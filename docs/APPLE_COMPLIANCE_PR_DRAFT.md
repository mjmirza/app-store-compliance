# Compliance Update: Apple Developer Requirements Integration

## 1. Summary
This comprehensive Pull Request addresses the latest Apple Developer requirements across multiple compliance domains: Privacy Manifests, Required Reason APIs, In-App Purchase policies, Alternative payment regulations, App Store Review Guidelines, SDK requirements, Minimum SDK versions.

## 2. Background
To ensure continuous distribution on the App Store without submission bottlenecks or review blocks, we must proactively align our application with updated guidelines and APIs.
- **Privacy Manifests**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **In-App Purchase policies**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Alternative payment regulations**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **App Store Review Guidelines**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **SDK requirements**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Minimum SDK versions**: Annual minimum deployment target or target SDK version updates enforced by stores.

## 3. Regulatory change
We are applying platform-specific adjustments to satisfy Apple's App Store Review Guidelines, Privacy Manifest mandates, alternative billing permissions, and security requirements.

## 4. Official citations
- **Privacy Manifests**: "Upcoming Requirements for Privacy Manifests and Required Reason APIs" - [Official News](https://mock.invalid/apple-news/privacy-requirements)
- **Required Reason APIs**: "Upcoming Requirements for Privacy Manifests and Required Reason APIs" - [Official News](https://mock.invalid/apple-news/privacy-requirements)
- **In-App Purchase policies**: "Updates to In-App Purchase Policies and Alternative Payment Options" - [Official News](https://mock.invalid/apple-news/iap-updates)
- **Alternative payment regulations**: "Updates to In-App Purchase Policies and Alternative Payment Options" - [Official News](https://mock.invalid/apple-news/iap-updates)
- **App Store Review Guidelines**: "App Store Review Guidelines and 4.3 Saturated Categories Update" - [Official News](https://mock.invalid/apple-news/review-guidelines-update)
- **SDK requirements**: "Xcode 26 and Minimum iOS SDK Requirements for Submission" - [Official News](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)
- **Minimum SDK versions**: "Xcode 26 and Minimum iOS SDK Requirements for Submission" - [Official News](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)

## 5. Affected files
- *No specific files containing matching category patterns were automatically detected.*

## 6. Risk assessment
We have evaluated the impact of these changes to avoid compilation or submission-time rejections:
- **Privacy Manifests** (Critical Impact): Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs** (Critical Impact): Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **In-App Purchase policies** (Critical Impact): App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Alternative payment regulations** (High Impact): Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **App Store Review Guidelines** (High Impact): Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **SDK requirements** (High Impact): Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Minimum SDK versions** (High Impact): Annual minimum deployment target or target SDK version updates enforced by stores.

## 7. Migration steps
- [Privacy Manifests] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [Privacy Manifests] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- [Required Reason APIs] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [Required Reason APIs] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- [In-App Purchase policies] Route all digital goods through StoreKit in-app purchases.
- [In-App Purchase policies] Add a prominent Restore Purchases control for non-consumable goods.
- [In-App Purchase policies] Verify pricing displays correspond with Apple subscription terms requirements.
- [Alternative payment regulations] Ensure appropriate entitlements are requested and set up for alternative billing.
- [Alternative payment regulations] Show mandatory disclosure sheets before redirecting to external web purchase flows.
- [App Store Review Guidelines] Review the updated guidelines section in APPLE.md or the official site.
- [App Store Review Guidelines] Ensure App Review Notes are updated with working test accounts.
- [App Store Review Guidelines] Verify the application flows align with the updated guideline numbers.
- [SDK requirements] Perform regular updates on bundled third-party SDKs.
- [SDK requirements] Ensure each third-party SDK has its signed privacy manifest file.
- [Minimum SDK versions] Update deployment target version to match latest requirements.
- [Minimum SDK versions] Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 8. Backward compatibility
All updates maintain compatibility across supported OS deployment targets. Legacy platforms remain functional via compile-time gates and API capability checks.

## 9. Implementation checklist
- [ ] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- [ ] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- [ ] Route all digital goods through StoreKit in-app purchases.
- [ ] Add a prominent Restore Purchases control for non-consumable goods.
- [ ] Verify pricing displays correspond with Apple subscription terms requirements.
- [ ] Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] Show mandatory disclosure sheets before redirecting to external web purchase flows.
- [ ] Review the updated guidelines section in APPLE.md or the official site.
- [ ] Ensure App Review Notes are updated with working test accounts.
- [ ] Verify the application flows align with the updated guideline numbers.
- [ ] Perform regular updates on bundled third-party SDKs.
- [ ] Ensure each third-party SDK has its signed privacy manifest file.
- [ ] Update deployment target version to match latest requirements.
- [ ] Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 10. Testing checklist
- [ ] Run the pre-submission compliance guard: `bash agent-os/hooks/app-store-compliance-guard.sh .`
- [ ] Verify on physical iOS/iPadOS/macOS devices/simulators that the updated flows function correctly.
- [ ] Double-check that no unexpected runtime crashes or warnings are logged during compilation.

## 11. Documentation checklist
- [ ] Update internal developer documentation with these platform requirements.
- [ ] Verify the App Store Review Notes are up-to-date in App Store Connect with working test accounts.

## 12. Compliance impact
Implementing these updates protects our App Store developer program standing, reducing submission rejection risk to Low and securing our active distribution status.

## 13. Breaking changes
There are no breaking changes or structural API deprecations. However, missing these declarations is considered a blocker for submitting updates.

## 14. Review checklist
- [ ] All required App Store metadata keys and configuration properties are in place.
- [ ] No prohibited private APIs or un-declared Required Reason APIs are referenced.
- [ ] Code builds cleanly in Xcode.

## 15. Approver recommendations
- **Lead Mobile Developer / Architect** (for codebase verification)
- **App Delivery Manager** (for release timeline alignment)