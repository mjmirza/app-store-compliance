# PULL REQUEST DRAFT: Apple Developer and App Store Policy Compliance Update

## 1. Summary
This pull request introduces critical configuration adjustments and codebase compliance pathways to conform with the latest Apple Developer Program and App Store requirement updates.

## 2. Background
Apple enforces strict storefront reviews and automated app submission gates. Maintaining conformity with the latest Developer Program License Agreements, App Store Review Guidelines, and specialized technical specifications is essential to avoid submission rejection or distribution blockages.

## 3. Regulatory change
The updates address core compliance requirements, including:
- Access control guidelines and Required Reason API declarations.
- App privacy requirements, third-party data-sharing transparency, and Privacy Manifest integration.
- Target SDK, minimum development targets, and Xcode compiling rules.

## 4. Official citations
- **Privacy Manifests**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://developer.apple.com/news/?id=privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **Required Reason APIs**: [Upcoming Requirements for Privacy Manifests and Required Reason APIs](https://developer.apple.com/news/?id=privacy-requirements) (Published: Wed, 15 May 2026 10:00:00 GMT)
- **In-App Purchase policies**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://developer.apple.com/news/?id=iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **Alternative payment regulations**: [Updates to In-App Purchase Policies and Alternative Payment Options](https://developer.apple.com/news/?id=iap-updates) (Published: Mon, 01 Jun 2026 09:00:00 GMT)
- **App Store Review Guidelines**: [App Store Review Guidelines and 4.3 Saturated Categories Update](https://developer.apple.com/news/?id=review-guidelines-update) (Published: Tue, 09 Jun 2026 14:00:00 GMT)
- **SDK requirements**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)
- **Minimum SDK versions**: [Xcode 26 and Minimum iOS SDK Requirements for Submission](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26) (Published: Mon, 03 Feb 2026 08:00:00 GMT)

## 5. Affected files
- *No specific files containing matching category patterns were automatically detected.*

## 6. Risk assessment
- *Privacy Manifests* (Critical Impact): Failure leads to storefront review rejection or upload blocks.
- *Required Reason APIs* (Critical Impact): Failure leads to storefront review rejection or upload blocks.
- *In-App Purchase policies* (Critical Impact): Failure leads to storefront review rejection or upload blocks.
- *Alternative payment regulations* (High Impact): Failure leads to storefront review rejection or upload blocks.
- *App Store Review Guidelines* (High Impact): Failure leads to storefront review rejection or upload blocks.
- *SDK requirements* (High Impact): Failure leads to storefront review rejection or upload blocks.
- *Minimum SDK versions* (High Impact): Failure leads to storefront review rejection or upload blocks.
- **Overall Submission Security**: Failure to address high or critical impact updates blocks App Store Connect upload processing.

## 7. Migration steps
- **Privacy Manifests**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
  * Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
  * Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- **Required Reason APIs**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
  * Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
  * Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- **In-App Purchase policies**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
  * Route all digital goods through StoreKit in-app purchases.
  * Add a prominent Restore Purchases control for non-consumable goods.
  * Verify pricing displays correspond with Apple subscription terms requirements.
- **Alternative payment regulations**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
  * Ensure appropriate entitlements are requested and set up for alternative billing.
  * Show mandatory disclosure sheets before redirecting to external web purchase flows.
- **App Store Review Guidelines**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
  * Review the updated guidelines section in APPLE.md or the official site.
  * Ensure App Review Notes are updated with working test accounts.
  * Verify the application flows align with the updated guideline numbers.
- **SDK requirements**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
  * Perform regular updates on bundled third-party SDKs.
  * Ensure each third-party SDK has its signed privacy manifest file.
- **Minimum SDK versions**: Annual minimum deployment target or target SDK version updates enforced by stores.
  * Update deployment target version to match latest requirements.
  * Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

## 8. Backward compatibility
All changes represent non-breaking declaration updates, Info.plist purpose strings, or Privacy Info manifest configurations. There is zero deprecation of core functional APIs, and compatibility with older deployed iOS versions is preserved.

## 9. Implementation checklist
- [ ] Audit project elements for Privacy Manifests
  * Scan for regex signature: `NSPrivacyAccessedAPITypes|NSPrivacyCollectedDataTypes`
- [ ] Audit project elements for Required Reason APIs
  * Scan for regex signature: `UserDefaults|NSFileManager|systemUptime|ProcessInfo|stat\s*\(`
- [ ] Audit project elements for In-App Purchase policies
  * Scan for regex signature: `StoreKit|SKProduct|Product\.purchase|restorePurchases|restoreCompletedTransactions`
- [ ] Audit project elements for Alternative payment regulations
  * Scan for regex signature: `com\.apple\.developer\.storekit\.external-purchase|SKExternalPurchase|Stripe|PayPal`
- [ ] Audit project elements for App Store Review Guidelines
  * Scan for regex signature: `LoginView|signIn|AuthService|OAuth|Firebase|lorem ipsum|placeholder|TODO|FIXME`
- [ ] Audit project elements for SDK requirements
  * Scan for regex signature: `Firebase|Alamofire|AppsFlyerLib|Adjust|FBSDK|com\.facebook`
- [ ] Audit project elements for Minimum SDK versions
  * Scan for regex signature: `IPHONEOS_DEPLOYMENT_TARGET|targetSdkVersion|targetSdk`
- [ ] Run the pre-submission compliance guard checks locally.

## 10. Testing checklist
- [ ] Perform a clean compile using Xcode on a development machine.
- [ ] Verify that privacy manifest files are properly linked inside the compiled bundle.
- [ ] Walk through affected user flows (such as permission dialogs or privacy disclosures) to ensure visual and operational compliance.

## 11. Documentation checklist
- [ ] Update APP-STORE-COMPLIANCE or APPLE-POLICY-MIGRATION reference docs.
- [ ] Update App Review Notes in App Store Connect with valid demo account credentials and layout descriptions.

## 12. Compliance impact
- **Submission Security**: Minimizes manual rejection risks and clears automated publishing gates.
- **Enterprise Standing**: Protects developer organization status under the latest License Agreements.

## 13. Breaking changes
No technical API breaking changes are introduced. However, failing to comply with platform requirements makes previous app builds effectively non-distributable.

## 14. Review checklist
- [ ] Ensure the pull request contains zero emojis or graphical symbols.
- [ ] Confirm that all added plist keys and purpose strings are non-empty and accurate.
- [ ] Verify that no private or undocumented APIs are referenced in the codebase.

## 15. Approver recommendations
Ensure that senior iOS engineers and compliance officers review the technical implementation of Privacy Manifests and Required Reason APIs, as missing declarations can block submissions post-deadline.
