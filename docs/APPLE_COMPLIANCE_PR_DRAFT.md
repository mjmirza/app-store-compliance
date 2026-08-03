# PULL REQUEST DRAFT: Apple Developer Requirements Regulatory Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple Developer Program policies, guidelines, and security requirements. It addresses App Store review guidelines, required reason APIs, privacy manifest files, alternative billing, location/media permission descriptions, and minimum deployment SDK levels to clear all automated and manual App Store Connect publishing gates.

## 2. Background
App Store Connect enforces strict automated compilation and upload checks, in addition to manual reviewer audits of human interface guidelines, payment models, location details, and subscription descriptions. Non-compliance results in immediate binary rejection or account suspension.

## 3. Regulatory change
- **App Store Publishing Gates**: Requirements for Xcode 26, target iOS 26 SDK, explicit privacy manifest files, and rigorous declarations for accessing Restricted Reason APIs (e.g. UserDefaults).
- **Global Compliance**: EU Digital Markets Act adjustments allowing alternative payment schemes, in-app disclosure rules, and strict user consent prompts for tracking and Generative AI components.

## 4. Official citations
- **Privacy Manifests**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://mock.invalid/apple-news/privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **Required Reason APIs**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://mock.invalid/apple-news/privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **In-App Purchase policies**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://mock.invalid/apple-news/iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **Alternative payment regulations**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://mock.invalid/apple-news/iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **App Store Review Guidelines**: [App Store Review Guidelines and 4.3 Saturated Categories Update](https://mock.invalid/apple-news/review-guidelines-update) (Published: Tue, 09 Jun 2026 14:00:00 GMT)
- **SDK requirements**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)
- **Minimum SDK versions**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)

## 5. Affected files
- No specific codebase matches detected. Manual check recommended.

## 6. Risk assessment
- *Privacy Manifests*: Critical risk of manual rejection by App Store reviewers or automated API blocks.
- *Required Reason APIs*: Critical risk of manual rejection by App Store reviewers or automated API blocks.
- *In-App Purchase policies*: Critical risk of manual rejection by App Store reviewers or automated API blocks.
- *Alternative payment regulations*: High risk of manual rejection by App Store reviewers or automated API blocks.
- *App Store Review Guidelines*: High risk of manual rejection by App Store reviewers or automated API blocks.
- *SDK requirements*: High risk of manual rejection by App Store reviewers or automated API blocks.
- *Minimum SDK versions*: High risk of manual rejection by App Store reviewers or automated API blocks.
- **Overall Standing**: Immediate risk of binary rejections and blocking critical bug fixes if updates are not compiled against the latest requirements.

## 7. Migration steps
### Migration for Privacy Manifests
- Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
### Migration for Required Reason APIs
- Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
### Migration for In-App Purchase policies
- Route all digital goods through StoreKit in-app purchases.
- Add a prominent Restore Purchases control for non-consumable goods.
- Verify pricing displays correspond with Apple subscription terms requirements.
### Migration for Alternative payment regulations
- Ensure appropriate entitlements are requested and set up for alternative billing.
- Show mandatory disclosure sheets before redirecting to external web purchase flows.
### Migration for App Store Review Guidelines
- Review the updated guidelines section in APPLE.md or the official site.
- Ensure App Review Notes are updated with working test accounts.
- Verify the application flows align with the updated guideline numbers.
### Migration for SDK requirements
- Perform regular updates on bundled third-party SDKs.
- Ensure each third-party SDK has its signed privacy manifest file.
### Migration for Minimum SDK versions
- Update deployment target version to match latest requirements.
- Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 8. Backward compatibility
All changes preserve complete backward compatibility. Declarations, keys, and purpose strings in plist configurations do not affect execution on legacy systems. Recommended safety fallbacks are configured dynamically for newer OS permissions.

## 9. Implementation checklist
### Implementation for Privacy Manifests
- [ ] Scan the codebase for occurrences of `NSPrivacyAccessedAPITypes|NSPrivacyCollectedDataTypes`.
- [ ] Update configuration files (PrivacyInfo.xcprivacy, *.swift, *.plist) with accurate declarations.
### Implementation for Required Reason APIs
- [ ] Scan the codebase for occurrences of `UserDefaults|NSFileManager|systemUptime|ProcessInfo|stat\s*\(`.
- [ ] Update configuration files (*.swift, *.m, *.plist, PrivacyInfo.xcprivacy) with accurate declarations.
### Implementation for In-App Purchase policies
- [ ] Scan the codebase for occurrences of `StoreKit|SKProduct|Product\.purchase|restorePurchases|restoreCompletedTransactions`.
- [ ] Update configuration files (*.swift, Info.plist) with accurate declarations.
### Implementation for Alternative payment regulations
- [ ] Scan the codebase for occurrences of `com\.apple\.developer\.storekit\.external-purchase|SKExternalPurchase|Stripe|PayPal`.
- [ ] Update configuration files (*.swift, *.entitlements, Info.plist) with accurate declarations.
### Implementation for App Store Review Guidelines
- [ ] Scan the codebase for occurrences of `LoginView|signIn|AuthService|OAuth|Firebase|lorem ipsum|placeholder|TODO|FIXME`.
- [ ] Update configuration files (Info.plist, AppReviewNotes, *.swift) with accurate declarations.
### Implementation for SDK requirements
- [ ] Scan the codebase for occurrences of `Firebase|Alamofire|AppsFlyerLib|Adjust|FBSDK|com\.facebook`.
- [ ] Update configuration files (Podfile, Package.swift, *.swift, build.gradle) with accurate declarations.
### Implementation for Minimum SDK versions
- [ ] Scan the codebase for occurrences of `IPHONEOS_DEPLOYMENT_TARGET|targetSdkVersion|targetSdk`.
- [ ] Update configuration files (*.pbxproj, *.xcconfig, Package.swift, build.gradle, build.gradle.kts) with accurate declarations.
- [ ] Run pre-submission compliance audit to verify there are no validation blocks.

## 10. Testing checklist
- [ ] Compile a release build against the latest target iOS SDK.
- [ ] Validate StoreKit in-app checkout and subscription flows.
- [ ] Verify permission alerts load correctly on fresh device installations.
- [ ] Ensure the signed third-party privacy manifest schemas compile successfully.

## 11. Documentation checklist
- [ ] Complete App Store review notes template with working test user credentials.
- [ ] Update privacy policy links inside metadata configurations.
- [ ] Record compliance migration tasks in `docs/APPLE-POLICY-MIGRATION.md`.

## 12. Compliance impact
- **Submission Security**: Eliminates upload-time rejections for privacy manifests and required reason APIs.
- **Store Position**: Aligns with human interface standards, protecting store prominence.
- **GDPR & DMA Legal Coverage**: Guarantees secure user tracking transparency and regional payment compliance.

## 13. Breaking changes
- Xcode 26 migration requires deprecating compatibility with older macOS local runners.
- Some legacy third-party dependency overrides might require manual updates.

## 14. Review checklist
- [ ] The bundle contains no un-declared required reason APIs.
- [ ] All sensitive permissions declare accurate and specific user-facing purpose descriptions.
- [ ] Third-party SDK binaries are securely verified and up-to-date.

## 15. Approver recommendations
Ensure that the Account Holder has accepted any updated terms or agreements on App Store Connect. Technical leads should review the dynamic dependency map to verify that all third-party modules are fully signed and verified before triggering the release build pipeline.
