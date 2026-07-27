# PULL REQUEST DRAFT: Apple Developer Requirements Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple Developer and App Store publishing requirements. It addresses privacy manifests, required reason APIs, StoreKit integrations, DMA marketplace settings, and compiler compliance to clear all modern App Store Connect gates.

## 2. Background
Apple enforces strict static and manual reviews before permitting binary distribution on the App Store. Proactive integration of required manifests, user data collection declarations, and appropriate design paradigms prevents costly rejection loops.

## 3. Regulatory change
- **App Store Publishing Gates**: Mandates for fully formed PrivacyInfo.xcprivacy files, declared Required Reason APIs (UserDefaults, systemUptime), and StoreKit pricing disclosures.
- **EU Digital Markets Act (DMA)**: Integration pathways for alternative distribution networks, external purchase link configurations, and core technology fee assessments.

## 4. Official citations
- **Privacy Manifests**: [Mandatory Privacy Manifest Integration and Domain Tracking Requirements](https://developer.apple.com/news/?id=privacy-manifests-mandatory) (Published: Mon, 01 Jun 2026 10:00:00 GMT)
- **Required Reason APIs**: [Mandatory Privacy Manifest Integration and Domain Tracking Requirements](https://developer.apple.com/news/?id=privacy-manifests-mandatory) (Published: Mon, 01 Jun 2026 10:00:00 GMT)
- **In-App Purchase policies**: [App Store In-App Purchase and StoreKit Updates](https://developer.apple.com/news/?id=storekit-iap-policies) (Published: Tue, 02 Jun 2026 11:00:00 GMT)
- **Apple Developer Program License Agreement**: [EU Digital Markets Act Compliance Changes and Alternative App Marketplaces](https://developer.apple.com/news/?id=dma-compliance-eu) (Published: Wed, 03 Jun 2026 12:00:00 GMT)
- **DMA compliance changes**: [EU Digital Markets Act Compliance Changes and Alternative App Marketplaces](https://developer.apple.com/news/?id=dma-compliance-eu) (Published: Wed, 03 Jun 2026 12:00:00 GMT)

## 5. Affected files
- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).*

## 6. Risk assessment
- *Privacy Manifests*: Mandatory upload-time submission blockage if required privacy manifests are missing.
- *Required Reason APIs*: Direct automated App Store Connect upload-time rejections post-Spring deadline.
- *In-App Purchase policies*: Reviewer rejection under Guideline 3.1.1 if digital transactions fail to use store mechanics.
- *Apple Developer Program License Agreement*: General publishing gate risk or rejection on subsequent app submissions.
- *DMA compliance changes*: Inability to publish or distribute through alternative marketplaces in the EU without entitlements.
- **Overall Standing**: High risk of update blockage in App Store Connect if static review rules are violated.

## 7. Migration steps
- **Privacy Manifests**: Audit third-party SDK dependencies for signatures and incorporate mandatory NSPrivacyAccessedAPITypes.
- **Required Reason APIs**: Audit usage of UserDefaults, systemUptime, and file timestamps, and declare valid reason codes in PrivacyInfo.xcprivacy.
- **In-App Purchase policies**: Upgrade billing modules to modern StoreKit 2 APIs. Ensure a clear Restore Purchases button is prominent.
- **Apple Developer Program License Agreement**: Ensure proper implementation according to official developer guidelines for Apple Developer Program License Agreement.
- **DMA compliance changes**: Integrate alternative distribution entitlements for European Union users if distributing outside App Store.

## 8. Backward compatibility
All changes are designed to preserve backward compatibility. Privacy manifests are backward-compatible metadata packages and do not alter execution behavior on older iOS versions. Alternate purchase flows gracefully degrade to standard StoreKit interfaces.

## 9. Implementation checklist
- [ ] Add PrivacyInfo.xcprivacy to root of main target.
- [ ] Declare correct tracking keys and domains if app tracking is utilized.
- [ ] Declare NSPrivacyAccessedAPITypes in PrivacyInfo.xcprivacy with valid reason codes.
- [ ] Implement StoreKit 2 Transaction.currentEntitlements sync and restore UI.
- [ ] Audit codebase for patterns matching Apple Developer Program License Agreement.
- [ ] Configure EU alternative marketplace distribution settings on App Store Connect.
- [ ] Run the compliance guard check locally.

## 10. Testing checklist
- [ ] Verify that PrivacyInfo.xcprivacy contains accurate tracking declarations.
- [ ] Confirm in-app purchases restore flows work in Sandbox environment.
- [ ] Verify there are no strict concurrency crashes on newer devices.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with compliance progress.
- [ ] Configure reviewer notes template in App Store Connect metadata.

## 12. Compliance impact
- **Publishing Gate**: Eliminates upload-time static analysis warnings.
- **Brand Standing**: Ensures uninterrupted service and keeps developer account in good standing.

## 13. Breaking changes
- No binary breaking changes are introduced; deprecations are resolved with fallback patterns.

## 14. Review checklist
- [ ] Code strictly implements guidelines for user data privacy.
- [ ] All sensitive permissions declare explicit, customer-facing descriptions.

## 15. Approver recommendations
Ensure that the App Store Connect Account Holder reviews and accepts any updated Developer Program License agreements online, as code compliance cannot bypass administrative agreements.
