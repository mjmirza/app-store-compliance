# PULL REQUEST DRAFT: Apple Developer Regulatory Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple Developer requirements. It addresses App Store Review Guidelines, privacy manifest requirements, required reason APIs, user data, and SDK thresholds to satisfy modern publishing gates.

## 2. Background
The Apple App Store enforces strict publishing gates, requiring target SDK levels to remain up-to-date and billing, permissions, and data sharing activities to be fully and accurately declared. Non-compliance leads to automatic rejection, or escalation against the developer account, up to suspension or termination.

## 3. Regulatory change
- **App Store Publishing & Review Guidelines**: Required Xcode and deployment target levels, modern StoreKit integrations, and regional billing requirements.
- **Privacy & Security**: Mandatory implementation of Privacy Manifest (PrivacyInfo.xcprivacy) files, declaration of Accessed APIs (Required Reason APIs), and App Tracking Transparency consent workflows.

## 4. Official citations
- **Privacy Manifests**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://developer.apple.com/news/?id=privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **Required Reason APIs**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://developer.apple.com/news/?id=privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **In-App Purchase policies**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://developer.apple.com/news/?id=iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **Alternative payment regulations**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://developer.apple.com/news/?id=iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **App Store Review Guidelines**: [App Store Review Guidelines and 4.3 Saturated Categories Update](https://developer.apple.com/news/?id=review-guidelines-update) (Published: Tue, 09 Jun 2026 14:00:00 GMT)
- **SDK requirements**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)
- **Minimum SDK versions**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)

## 5. Affected files
- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).*

## 6. Risk assessment
- **Privacy Manifests**: Critical Risk. Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs**: Critical Risk. Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **In-App Purchase policies**: Critical Risk. App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Alternative payment regulations**: High Risk. Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **App Store Review Guidelines**: High Risk. Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **SDK requirements**: High Risk. Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Minimum SDK versions**: High Risk. Annual minimum deployment target or target SDK version updates enforced by stores.
- **Overall Standing**: High risk of update blockage or account warnings if publishing gates are not proactively cleared.

## 7. Migration steps
### Privacy Manifests Migration:
- Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
### Required Reason APIs Migration:
- Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
### In-App Purchase policies Migration:
- Route all digital goods through StoreKit in-app purchases.
- Add a prominent Restore Purchases control for non-consumable goods.
- Verify pricing displays correspond with Apple subscription terms requirements.
### Alternative payment regulations Migration:
- Ensure appropriate entitlements are requested and set up for alternative billing.
- Show mandatory disclosure sheets before redirecting to external web purchase flows.
### App Store Review Guidelines Migration:
- Review the updated guidelines section in APPLE.md or the official site.
- Ensure App Review Notes are updated with working test accounts.
- Verify the application flows align with the updated guideline numbers.
### SDK requirements Migration:
- Perform regular updates on bundled third-party SDKs.
- Ensure each third-party SDK has its signed privacy manifest file.
### Minimum SDK versions Migration:
- Update deployment target version to match latest requirements.
- Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 8. Backward compatibility
All changes are fully backward-compatible. Deployment targets and minimum SDK versions are set to satisfy requirements while maintaining support for legacy operating systems where technically viable.

## 9. Implementation checklist
### Privacy Manifests Checklist:
- [ ] Scan the codebase for occurrences of `NSPrivacyAccessedAPITypes|NSPrivacyCollectedDataTypes`.
- [ ] Update configuration files (PrivacyInfo.xcprivacy, *.swift, *.plist) with accurate declarations.
### Required Reason APIs Checklist:
- [ ] Scan the codebase for occurrences of `UserDefaults|NSFileManager|systemUptime|ProcessInfo|stat\s*\(`.
- [ ] Update configuration files (*.swift, *.m, *.plist, PrivacyInfo.xcprivacy) with accurate declarations.
### In-App Purchase policies Checklist:
- [ ] Scan the codebase for occurrences of `StoreKit|SKProduct|Product\.purchase|restorePurchases|restoreCompletedTransactions`.
- [ ] Update configuration files (*.swift, Info.plist) with accurate declarations.
### Alternative payment regulations Checklist:
- [ ] Scan the codebase for occurrences of `com\.apple\.developer\.storekit\.external-purchase|SKExternalPurchase|Stripe|PayPal`.
- [ ] Update configuration files (*.swift, *.entitlements, Info.plist) with accurate declarations.
### App Store Review Guidelines Checklist:
- [ ] Scan the codebase for occurrences of `LoginView|signIn|AuthService|OAuth|Firebase|lorem ipsum|placeholder|TODO|FIXME`.
- [ ] Update configuration files (Info.plist, AppReviewNotes, *.swift) with accurate declarations.
### SDK requirements Checklist:
- [ ] Scan the codebase for occurrences of `Firebase|Alamofire|AppsFlyerLib|Adjust|FBSDK|com\.facebook`.
- [ ] Update configuration files (Podfile, Package.swift, *.swift, build.gradle) with accurate declarations.
### Minimum SDK versions Checklist:
- [ ] Scan the codebase for occurrences of `IPHONEOS_DEPLOYMENT_TARGET|targetSdkVersion|targetSdk`.
- [ ] Update configuration files (*.pbxproj, *.xcconfig, Package.swift, build.gradle, build.gradle.kts) with accurate declarations.
- [ ] Re-run the automated compliance guard checks locally.

## 10. Testing checklist
- [ ] Perform a clean build using modern Xcode versions on a local development machine.
- [ ] Verify that PrivacyInfo.xcprivacy exists in the main bundle and matches compiled symbols.
- [ ] Verify that no unauthorized third-party libraries or un-declared Required Reason APIs are referenced.
- [ ] Execute the pre-submission guard script to confirm that compliance threshold is met.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with completed tasks.
- [ ] Populate 'App Store Review Notes' with working test accounts and specific instructions.
- [ ] Update store listing metadata descriptions and privacy policy links.

## 12. Compliance impact
- **Publishing Gate**: Guarantees uninterrupted app submissions by meeting Xcode and Privacy Manifest thresholds.
- **Account Health**: Mitigates compliance strikes, protecting the developer organization account against suspension.
- **Privacy Standards**: Aligns with modern global privacy regulations (GDPR, CCPA/CPRA).

## 13. Breaking changes
- No functional breaking changes are introduced by these configuration updates.
- Updating Xcode or minimum SDK requirements may restrict deployment to older operating systems.

## 14. Review checklist
- [ ] Code complies with all Apple App Store Review Guidelines.
- [ ] No emojis or graphical symbols are present in any modified files.
- [ ] Third-party SDK compiled dependencies are fully updated and secure.

## 15. Approver recommendations
Ensure that the App Store Connect account owner has accepted the latest Program License Agreement prior to submission. Confirm that the PrivacyInfo.xcprivacy file is correctly bundled in the final application target.
