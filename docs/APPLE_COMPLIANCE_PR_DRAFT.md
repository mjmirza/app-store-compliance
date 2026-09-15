# PULL REQUEST DRAFT: Apple Developer Requirements Compliance Update

## 1. Summary
This pull request addresses the latest Apple Developer and App Store Review requirements across monitored policy tracks. It aligns configuration files, entitlement declarations, privacy manifests, and SDK deployment targets to clear App Store Connect submission gates.

## 2. Background
Apple continuously updates its App Store Review Guidelines, Developer Program License Agreement, Human Interface Guidelines, and technical requirements (Privacy Manifests, Required Reason APIs, StoreKit policies, and Xcode minimum SDK versions). Proactively migrating codebase assets prevents submission rejections and build upload blocks.

## 3. Regulatory change
- **App Store & Platform Mechanics**: Strict enforcement of Privacy Info manifests, Required Reason API declarations, App Tracking Transparency prompts, StoreKit restore controls, and regional DMA alternative payment / distribution options.
- **Safety & Quality Guidelines**: AI content moderation requirements, COPPA child safety rules, accessibility WCAG 2.1 AA standards, and Swift strict concurrency / Xcode deployment targets.

## 4. Official citations
- **App Store Review Guidelines**: [Important updates concerning App Store Review Guidelines](https://developer.apple.com/news/?id=simulated-app-store-review-guidelines) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Apple Developer Program License Agreement**: [Important updates concerning Apple Developer Program License Agreement](https://developer.apple.com/news/?id=simulated-apple-developer-program-license-agreement) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Human Interface Guidelines**: [Important updates concerning Human Interface Guidelines](https://developer.apple.com/news/?id=simulated-human-interface-guidelines) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Apple Privacy requirements**: [Important updates concerning Apple Privacy requirements](https://developer.apple.com/news/?id=simulated-apple-privacy-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Privacy Manifests**: [Important updates concerning Privacy Manifests](https://developer.apple.com/news/?id=simulated-privacy-manifests) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Required Reason APIs**: [Important updates concerning Required Reason APIs](https://developer.apple.com/news/?id=simulated-required-reason-apis) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **App Tracking Transparency**: [Important updates concerning App Tracking Transparency](https://developer.apple.com/news/?id=simulated-app-tracking-transparency) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Sign in with Apple**: [Important updates concerning Sign in with Apple](https://developer.apple.com/news/?id=simulated-sign-in-with-apple) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **In-App Purchase policies**: [Important updates concerning In-App Purchase policies](https://developer.apple.com/news/?id=simulated-in-app-purchase-policies) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Alternative payment regulations**: [Important updates concerning Alternative payment regulations](https://developer.apple.com/news/?id=simulated-alternative-payment-regulations) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **DMA compliance changes**: [Important updates concerning DMA compliance changes](https://developer.apple.com/news/?id=simulated-dma-compliance-changes) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Accessibility requirements**: [Important updates concerning Accessibility requirements](https://developer.apple.com/news/?id=simulated-accessibility-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Child safety requirements**: [Important updates concerning Child safety requirements](https://developer.apple.com/news/?id=simulated-child-safety-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **HealthKit policies**: [Important updates concerning HealthKit policies](https://developer.apple.com/news/?id=simulated-healthkit-policies) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Location permissions**: [Important updates concerning Location permissions](https://developer.apple.com/news/?id=simulated-location-permissions) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Camera and microphone permissions**: [Important updates concerning Camera and microphone permissions](https://developer.apple.com/news/?id=simulated-camera-and-microphone-permissions) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Push Notification requirements**: [Important updates concerning Push Notification requirements](https://developer.apple.com/news/?id=simulated-push-notification-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Background execution policies**: [Important updates concerning Background execution policies](https://developer.apple.com/news/?id=simulated-background-execution-policies) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Security updates**: [Important updates concerning Security updates](https://developer.apple.com/news/?id=simulated-security-updates) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **SDK requirements**: [Important updates concerning SDK requirements](https://developer.apple.com/news/?id=simulated-sdk-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Minimum SDK versions**: [Important updates concerning Minimum SDK versions](https://developer.apple.com/news/?id=simulated-minimum-sdk-versions) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Xcode requirements**: [Important updates concerning Xcode requirements](https://developer.apple.com/news/?id=simulated-xcode-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **Swift requirements**: [Important updates concerning Swift requirements](https://developer.apple.com/news/?id=simulated-swift-requirements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)
- **App Store Connect announcements**: [Important updates concerning App Store Connect announcements](https://developer.apple.com/news/?id=simulated-app-store-connect-announcements) (Published: Tue, 15 Sep 2026 06:07:04 GMT)

## 5. Affected files
- `LICENSE`
- `agent-os/hooks/app-store-compliance-guard-test.sh`
- `agent-os/hooks/app-store-compliance-guard.sh`
- `scripts/metadata-audit-test.sh`
- `scripts/metadata-audit.py`
- `scripts/monitor-regulatory-test.sh`
- `scripts/monitor.py`
- `scripts/pull-metadata.sh`
- `scripts/release-audit.py`

## 6. Risk assessment
- *App Store Review Guidelines*: High impact - Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- *Apple Developer Program License Agreement*: Medium impact - Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- *Human Interface Guidelines*: Medium impact - UI/UX layout changes recommended or mandated by Apple.
- *Apple Privacy requirements*: High impact - Global updates to Apple's privacy policy requirements and user consent flows.
- *Privacy Manifests*: Critical impact - Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- *Required Reason APIs*: Critical impact - Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- *App Tracking Transparency*: High impact - Tracking consent rules and IDFA access restrictions.
- *Sign in with Apple*: High impact - Requirement to offer Sign in with Apple alongside any other third-party social login.
- *In-App Purchase policies*: Critical impact - App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- *Alternative payment regulations*: High impact - Permitted exceptions and requirements for offering third-party payment links (region-gated).
- *DMA compliance changes*: High impact - EU Digital Markets Act requirements for alternative app marketplaces, browser engines, and external link rules.
- *Accessibility requirements*: Medium impact - Accessibility standards compliance (WCAG 2.1 AA / EN 301 549) and App Store Accessibility Nutrition Labels.
- *Child safety requirements*: Critical impact - Strict constraints on apps targeted at children, COPPA compliance, and CSAM reporting duties.
- *HealthKit policies*: High impact - Restrictions on HealthKit data mining, usage of health data for ads, and mandatory user permission descriptions.
- *Location permissions*: High impact - Stricter constraints, usage descriptions, and prominent disclosures for access to location.
- *Camera and microphone permissions*: High impact - Required Info.plist purpose strings and user-initiated triggers for media access.
- *Push Notification requirements*: Medium impact - Security, opt-in prompts, and payload specifications for Push Notifications.
- *Background execution policies*: High impact - Strict limitation of background execution categories to prevent resource/battery drain.
- *Security updates*: Medium impact - Security updates, encryption declarations, and external dependencies vulnerability checks.
- *SDK requirements*: High impact - Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- *Minimum SDK versions*: High impact - Annual minimum deployment target or target SDK version updates enforced by stores.
- *Xcode requirements*: High impact - Enforced Xcode versions for compiling App Store submissions.
- *Swift requirements*: Medium impact - Evolving Swift language standards, compiler features, and data-race safety requirements.
- *App Store Connect announcements*: Medium impact - Administrative and portal changes published in App Store Connect announcements.
- **Overall Standing**: High risk of submission rejection or upload-time blockage in App Store Connect if requirements are not met.

## 7. Migration steps
- **App Store Review Guidelines**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **Apple Developer Program License Agreement**: Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.
- **Human Interface Guidelines**: UI/UX layout changes recommended or mandated by Apple.
- **Apple Privacy requirements**: Global updates to Apple's privacy policy requirements and user consent flows.
- **Privacy Manifests**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Required Reason APIs**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **App Tracking Transparency**: Tracking consent rules and IDFA access restrictions.
- **Sign in with Apple**: Requirement to offer Sign in with Apple alongside any other third-party social login.
- **In-App Purchase policies**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Alternative payment regulations**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **DMA compliance changes**: EU Digital Markets Act requirements for alternative app marketplaces, browser engines, and external link rules.
- **Accessibility requirements**: Accessibility standards compliance (WCAG 2.1 AA / EN 301 549) and App Store Accessibility Nutrition Labels.
- **Child safety requirements**: Strict constraints on apps targeted at children, COPPA compliance, and CSAM reporting duties.
- **HealthKit policies**: Restrictions on HealthKit data mining, usage of health data for ads, and mandatory user permission descriptions.
- **Location permissions**: Stricter constraints, usage descriptions, and prominent disclosures for access to location.
- **Camera and microphone permissions**: Required Info.plist purpose strings and user-initiated triggers for media access.
- **Push Notification requirements**: Security, opt-in prompts, and payload specifications for Push Notifications.
- **Background execution policies**: Strict limitation of background execution categories to prevent resource/battery drain.
- **Security updates**: Security updates, encryption declarations, and external dependencies vulnerability checks.
- **SDK requirements**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Minimum SDK versions**: Annual minimum deployment target or target SDK version updates enforced by stores.
- **Xcode requirements**: Enforced Xcode versions for compiling App Store submissions.
- **Swift requirements**: Evolving Swift language standards, compiler features, and data-race safety requirements.
- **App Store Connect announcements**: Administrative and portal changes published in App Store Connect announcements.

## 8. Backward compatibility
All changes preserve backward compatibility. Declarations in Info.plist and PrivacyInfo.xcprivacy are non-breaking metadata updates that do not affect runtime behavior on older iOS versions.

## 9. Implementation checklist
- [ ] [App Store Review Guidelines] Review the updated guidelines section in APPLE.md or the official site.
- [ ] [App Store Review Guidelines] Ensure App Review Notes are updated with working test accounts.
- [ ] [App Store Review Guidelines] Verify the application flows align with the updated guideline numbers.
- [ ] [Apple Developer Program License Agreement] Log in to App Store Connect as the Account Holder.
- [ ] [Apple Developer Program License Agreement] Accept the latest Program License Agreement.
- [ ] [Apple Developer Program License Agreement] Review any changes regarding company distribution versus individual distribution rules.
- [ ] [Human Interface Guidelines] Check user interface elements against current design recommendations in HIG.
- [ ] [Human Interface Guidelines] Verify touch targets are at least 44x44pt on iOS.
- [ ] [Human Interface Guidelines] Test dark mode and dynamic type sizing rendering.
- [ ] [Apple Privacy requirements] Publish or update your privacy policy URL.
- [ ] [Apple Privacy requirements] Confirm in-app accessibility to the privacy policy link.
- [ ] [Apple Privacy requirements] Verify data declaration matches actual SDK data collection.
- [ ] [Privacy Manifests] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] [Privacy Manifests] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.
- [ ] [Required Reason APIs] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] [Required Reason APIs] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.
- [ ] [App Tracking Transparency] Verify ATTrackingManager.requestTrackingAuthorization is called before starting any tracking.
- [ ] [App Tracking Transparency] Add NSUserTrackingUsageDescription with a clear reason explaining why tracking is used.
- [ ] [Sign in with Apple] Verify that Sign in with Apple is offered at least as prominently as other social logins.
- [ ] [Sign in with Apple] Ensure email private relays are supported and profiles are handled gracefully on first login.
- [ ] [In-App Purchase policies] Route all digital goods through StoreKit in-app purchases.
- [ ] [In-App Purchase policies] Add a prominent Restore Purchases control for non-consumable goods.
- [ ] [In-App Purchase policies] Verify pricing displays correspond with Apple subscription terms requirements.
- [ ] [Alternative payment regulations] Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] [Alternative payment regulations] Show mandatory disclosure sheets before redirecting to external web purchase flows.
- [ ] [DMA compliance changes] Declare alternative distribution entitlements if publishing outside App Store in the EU.
- [ ] [DMA compliance changes] Implement EU-specific disclosure sheets and fee-math checks if using external link entitlements.
- [ ] [Accessibility requirements] Audit UI elements for accessibility labels and traits.
- [ ] [Accessibility requirements] Verify dynamic font resizing is supported.
- [ ] [Accessibility requirements] Populate Accessibility Nutrition Labels in App Store Connect.
- [ ] [Child safety requirements] Ensure no third-party ad or tracking SDKs are present in kids-targeted apps.
- [ ] [Child safety requirements] Place parental gates on any external links or in-app purchases.
- [ ] [Child safety requirements] Integrate NCMEC reporting flows on actual knowledge of CSAM (for US UGC apps).
- [ ] [HealthKit policies] Ensure HealthKit data is never used for advertising, marketing, or behavioral tracking.
- [ ] [HealthKit policies] Add detailed HealthKit share and update usage descriptions to Info.plist.
- [ ] [Location permissions] Check that location requests match real, visible user-facing features.
- [ ] [Location permissions] Include precise, specific usage descriptions in Info.plist explaining what features require location.
- [ ] [Camera and microphone permissions] Ensure NSCameraUsageDescription and NSMicrophoneUsageDescription are present and describe real features.
- [ ] [Camera and microphone permissions] Use modern system pickers (like PHPickerViewController) where full photo library access is not needed.
- [ ] [Push Notification requirements] Verify aps-environment is set to development/production in entitlements.
- [ ] [Push Notification requirements] Ensure user consent is requested and handled gracefully before registering for remote notifications.
- [ ] [Background execution policies] Verify UIBackgroundModes keys match the actual, documented core functionality (e.g. audio, VoIP).
- [ ] [Background execution policies] Remove unused background execution declarations to avoid automatic rejection.
- [ ] [Security updates] Review Info.plist for ITSAppUsesNonExemptEncryption.
- [ ] [Security updates] Upload ANSSI encryption declaration if distributing non-exempt encryption in France.
- [ ] [Security updates] Perform dependency audit for known CVEs.
- [ ] [SDK requirements] Perform regular updates on bundled third-party SDKs.
- [ ] [SDK requirements] Ensure each third-party SDK has its signed privacy manifest file.
- [ ] [Minimum SDK versions] Update deployment target version to match latest requirements.
- [ ] [Minimum SDK versions] Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).
- [ ] [Xcode requirements] Upgrade build machine/CI to Xcode 26 (or required version).
- [ ] [Xcode requirements] Resolve any newly introduced compiler deprecations/warnings.
- [ ] [Swift requirements] Verify SWIFT_VERSION is at least 5.x or 6.0.
- [ ] [Swift requirements] Resolve strict concurrency issues if migrating to Swift 6 compiler runtime.
- [ ] [App Store Connect announcements] Check the metadata and publishing workflows for impact.
- [ ] [App Store Connect announcements] Verify store listing parameters match the latest schema.

## 10. Testing checklist
- [ ] Perform a clean build in Xcode targeting the latest minimum required iOS SDK.
- [ ] Execute `bash agent-os/hooks/app-store-compliance-guard.sh .` to confirm local compliance guard checks pass.
- [ ] Validate privacy manifest syntax and entries in PrivacyInfo.xcprivacy.
- [ ] Verify that external payment disclosure sheets and consent modals display correctly.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with completed tasks.
- [ ] Populate App Review Notes with valid test credentials.
- [ ] Verify Privacy Policy URL and store metadata.

## 12. Compliance impact
- **Submission Readiness**: Guarantees clean App Store Connect build uploads and reduces review rejection risks.
- **Developer Standing**: Keeps the organization compliant with the Apple Developer Program License Agreement.

## 13. Breaking changes
- Xcode 26 build requirements drop support for legacy deployment targets below minimum specified iOS versions.

## 14. Review checklist
- [ ] PR contains no high-unicode emojis or unauthorized symbols.
- [ ] Privacy manifest entries match actual third-party SDK data access.
- [ ] Entitlements match current App Store Connect provisioning profiles.

## 15. Approver recommendations
Ensure that the Account Holder has accepted the latest Apple Developer Program License Agreement in App Store Connect prior to submitting the build for review.
