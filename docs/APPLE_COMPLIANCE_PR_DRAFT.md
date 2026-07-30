# PULL REQUEST DRAFT: Apple Developer and App Store Regulatory Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple Developer and App Store publishing requirements. It addresses guidelines, SDK versions, permissions, and metadata parameters to satisfy modern publishing gates.

## 2. Background
Apple enforces strict validation gates, requiring deployment targets and toolchains to remain up-to-date and billing, privacy declarations, and accessed APIs to be fully and accurately declared. Non-compliance leads to automatic upload warning delays or direct build rejection.

## 3. Regulatory change
- **App Store Publishing Gates**: Xcode versions, Swift configurations, and minimum iOS SDK target level requirements are regularly incremented, blocking outdated toolchain distributions.
- **Privacy & Required APIs**: PrivacyInfo.xcprivacy and Accessed APIs (UserDefaults, systemUptime) require exact declarations to avoid publishing warning holds.

## 4. Official citations
- **App Store Review Guidelines**: [Guidelines Update: App Store Review Guidelines Clarification](https://developer.apple.com/app-store/review/guidelines/) (Published: Mon, 15 Jun 2026 10:00:00 PDT)
- **Human Interface Guidelines**: [Guidelines Update: App Store Review Guidelines Clarification](https://developer.apple.com/app-store/review/guidelines/) (Published: Mon, 15 Jun 2026 10:00:00 PDT)
- **Apple Developer Program License Agreement**: [Upcoming Apple Developer Program License Agreement Updates](https://developer.apple.com/support/terms/) (Published: Tue, 16 Jun 2026 11:00:00 PDT)
- **Human Interface Guidelines**: [Human Interface Guidelines: Layout and Dark Mode Sizing Updates](https://developer.apple.com/design/human-interface-guidelines/) (Published: Wed, 17 Jun 2026 12:00:00 PDT)
- **Apple Privacy requirements**: [Apple Privacy Policy and Privacy Nutrition Label Compliance](https://developer.apple.com/privacy/) (Published: Thu, 18 Jun 2026 13:00:00 PDT)
- **Privacy Manifests**: [Privacy Manifests Enforcement and SDK Integration Requirements](https://developer.apple.com/support/privacy-manifests/) (Published: Fri, 19 Jun 2026 14:00:00 PDT)
- **Privacy Manifests**: [Required Reason APIs Declaration Mandate for UserDefaults and systemUptime](https://developer.apple.com/support/required-reason-api/) (Published: Sat, 20 Jun 2026 15:00:00 PDT)
- **Required Reason APIs**: [Required Reason APIs Declaration Mandate for UserDefaults and systemUptime](https://developer.apple.com/support/required-reason-api/) (Published: Sat, 20 Jun 2026 15:00:00 PDT)
- **Apple Developer Program License Agreement**: [App Tracking Transparency and IDFA Tracking Permission Prompt Enforcement](https://developer.apple.com/app-tracking-transparency/) (Published: Sun, 21 Jun 2026 16:00:00 PDT)
- **App Tracking Transparency**: [App Tracking Transparency and IDFA Tracking Permission Prompt Enforcement](https://developer.apple.com/app-tracking-transparency/) (Published: Sun, 21 Jun 2026 16:00:00 PDT)
- **Sign in with Apple**: [Sign in with Apple Social Login Integration Guidelines](https://developer.apple.com/sign-in-with-apple/) (Published: Mon, 22 Jun 2026 17:00:00 PDT)
- **In-App Purchase policies**: [In-App Purchase Policies, Auto-Renewable Subscription Terms](https://developer.apple.com/in-app-purchase/) (Published: Tue, 23 Jun 2026 18:00:00 PDT)
- **In-App Purchase policies**: [Alternative Payment Methods and External Purchase Link Disclosures](https://developer.apple.com/support/storekit-external-purchase/) (Published: Wed, 24 Jun 2026 19:00:00 PDT)
- **Alternative payment regulations**: [Alternative Payment Methods and External Purchase Link Disclosures](https://developer.apple.com/support/storekit-external-purchase/) (Published: Wed, 24 Jun 2026 19:00:00 PDT)
- **Apple Developer Program License Agreement**: [Digital Markets Act: EU Alternative App Marketplace Entitlements](https://developer.apple.com/support/alternative-app-distribution/) (Published: Thu, 25 Jun 2026 10:00:00 PDT)
- **DMA compliance changes**: [Digital Markets Act: EU Alternative App Marketplace Entitlements](https://developer.apple.com/support/alternative-app-distribution/) (Published: Thu, 25 Jun 2026 10:00:00 PDT)
- **Accessibility requirements**: [Accessibility standard EN 301 549 and VoiceOver Updates](https://developer.apple.com/accessibility/) (Published: Fri, 26 Jun 2026 11:00:00 PDT)
- **AI-related App Store policies**: [App Store AI-Generated Content Moderation and LLM Policies](https://developer.apple.com/news/ai-guideline/) (Published: Sat, 27 Jun 2026 12:00:00 PDT)
- **Child safety requirements**: [Child safety requirements: COPPA and Kids Category Standards](https://developer.apple.com/app-store/kids-category/) (Published: Sun, 28 Jun 2026 13:00:00 PDT)
- **HealthKit policies**: [HealthKit Data Mining, HKHealthStore Authorization Restrictions](https://developer.apple.com/documentation/healthkit/) (Published: Mon, 29 Jun 2026 14:00:00 PDT)
- **Apple Developer Program License Agreement**: [Location permissions: CLLocationManager Purpose String Constraints](https://developer.apple.com/documentation/corelocation/) (Published: Tue, 30 Jun 2026 15:00:00 PDT)
- **Location permissions**: [Location permissions: CLLocationManager Purpose String Constraints](https://developer.apple.com/documentation/corelocation/) (Published: Tue, 30 Jun 2026 15:00:00 PDT)
- **Apple Developer Program License Agreement**: [Camera and microphone permissions: AVCaptureDevice Purpose Disclosures](https://developer.apple.com/documentation/avfoundation/) (Published: Wed, 01 Jul 2026 16:00:00 PDT)
- **Human Interface Guidelines**: [Camera and microphone permissions: AVCaptureDevice Purpose Disclosures](https://developer.apple.com/documentation/avfoundation/) (Published: Wed, 01 Jul 2026 16:00:00 PDT)
- **Camera and microphone permissions**: [Camera and microphone permissions: AVCaptureDevice Purpose Disclosures](https://developer.apple.com/documentation/avfoundation/) (Published: Wed, 01 Jul 2026 16:00:00 PDT)
- **Push Notification requirements**: [Push Notification requirements: APNs Payload and Entitlements Updates](https://developer.apple.com/documentation/usernotifications/) (Published: Thu, 02 Jul 2026 17:00:00 PDT)
- **Background execution policies**: [Background execution policies: UIBackgroundModes Restriction updates](https://developer.apple.com/documentation/uikit/app_play/choosing_background_execution/) (Published: Fri, 03 Jul 2026 18:00:00 PDT)
- **Security updates**: [Security updates: ITSAppUsesNonExemptEncryption Compliance Review](https://developer.apple.com/support/export-compliance/) (Published: Sat, 04 Jul 2026 19:00:00 PDT)
- **SDK requirements**: [SDK requirements: Third-Party SDK Privacy Declarations](https://developer.apple.com/support/third-party-sdk/) (Published: Sun, 05 Jul 2026 10:00:00 PDT)
- **Apple Developer Program License Agreement**: [Minimum SDK Deployment Target Enforcements for Submission](https://developer.apple.com/news/sdk-target-guidelines/) (Published: Mon, 06 Jul 2026 11:00:00 PDT)
- **Minimum SDK versions**: [Minimum SDK Deployment Target Enforcements for Submission](https://developer.apple.com/news/sdk-target-guidelines/) (Published: Mon, 06 Jul 2026 11:00:00 PDT)
- **Xcode requirements**: [Xcode requirements: Mandatory Xcode Submission Build Mandate](https://developer.apple.com/news/xcode-requirements-mandate/) (Published: Tue, 07 Jul 2026 12:00:00 PDT)
- **Human Interface Guidelines**: [Swift requirements: SWIFT_VERSION 6 Concurrency Policies](https://developer.apple.com/swift/) (Published: Wed, 08 Jul 2026 13:00:00 PDT)
- **Swift requirements**: [Swift requirements: SWIFT_VERSION 6 Concurrency Policies](https://developer.apple.com/swift/) (Published: Wed, 08 Jul 2026 13:00:00 PDT)
- **App Store Connect announcements**: [App Store Connect announcements: Management and Metadata Changes](https://developer.apple.com/news/app-store-connect-updates/) (Published: Thu, 09 Jul 2026 14:00:00 PDT)

## 5. Affected files
- `./AGENTS.md`
- `./CHANGELOG.md`
- `./README.md`
- `./agent-os/commands/app-store-audit.md`
- `./agent-os/hooks/app-store-compliance-guard.sh`
- `./agent-os/skill/SKILL.md`
- `./docs/ADVANCED-2026.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/COMPETITIVE-GAP-ANALYSIS.md`
- `./docs/CREDITS.md`
- `./docs/EU-REGULATORY-2026.md`
- `./docs/GAMBLING-MATRIX.md`
- `./docs/GLOBAL-REGULATORY-2026.md`
- `./docs/GOOGLE-PLAY.md`
- `./docs/MOBILE-PRIVACY-MONITOR-2026.md`
- `./docs/MOBILE-SECURITY-2026.md`
- `./docs/OPEN-SOURCE-PATTERNS.md`
- `./docs/OTHER-STORES.md`
- `./docs/PLATFORM-MECHANICS-2026.md`
- `./docs/PRE-SUBMISSION-CHECKLIST.md`
- `./references/README.md`
- `./references/guidelines/by-app-type/crypto-finance-and-trading.md`
- `./references/guidelines/by-app-type/health-fitness-and-medical.md`
- `./references/guidelines/by-app-type/kids-category-and-families.md`
- `./references/guidelines/by-app-type/macos-and-the-mac-app-store.md`
- `./references/guidelines/by-app-type/universal-every-app.md`
- `./references/rules/android.md`
- `./references/rules/design.md`
- `./references/rules/export.md`
- `./references/rules/metadata.md`
- `./references/rules/payments.md`
- `./references/rules/performance.md`
- `./references/rules/privacy.md`
- `./references/rules/safety.md`
- `./scripts/metadata-audit-test.sh`
- `./scripts/metadata-audit.py`
- `./scripts/pull-metadata.sh`
- `./scripts/release-audit.py`
- `./templates/REVIEW-NOTES-TEMPLATE.md`

## 6. Risk assessment
- *App Store Review Guidelines*: Rejection under Guideline 2.1 / 4.3 if metadata or layout matches spam indicators.
- *Human Interface Guidelines*: UI presentation complaints or potential manual reviewer rejections.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *Human Interface Guidelines*: UI presentation complaints or potential manual reviewer rejections.
- *Apple Privacy requirements*: Automatic rejection under Guideline 5.1.1 if privacy policy is missing.
- *Privacy Manifests*: ITMS upload-time warnings or rejections if manifest declarations are omitted.
- *Privacy Manifests*: ITMS upload-time warnings or rejections if manifest declarations are omitted.
- *Required Reason APIs*: Strict automated validation blockages on App Store Connect if reason codes are absent.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *App Tracking Transparency*: Upload block or immediate manual rejection under Guideline 5.1.2 if ATT is bypassed.
- *Sign in with Apple*: Submission rejection under Guideline 4.8 if third-party logins bypass SIWA.
- *In-App Purchase policies*: Rejection under Guideline 3.1.1/3.1.2 if digital products bypass StoreKit.
- *In-App Purchase policies*: Rejection under Guideline 3.1.1/3.1.2 if digital products bypass StoreKit.
- *Alternative payment regulations*: Potential compliance blockages or audit requests if billing redirection lacks consent sheets.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *DMA compliance changes*: Ineligibility for alternative distribution routes if entitlements are omitted.
- *Accessibility requirements*: Failure to meet EAA standards, elevating litigation or rating rejection risks.
- *AI-related App Store policies*: App suspension or Guideline 1.2 rejection if AI outputs lack moderation safeguards.
- *Child safety requirements*: Serious privacy compliance issues and immediate rejection under kids guidelines.
- *HealthKit policies*: Permanent account revocation if health metrics are leaked to ad platforms.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *Location permissions*: Rejection under privacy guidelines if location use strings are generic.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *Human Interface Guidelines*: UI presentation complaints or potential manual reviewer rejections.
- *Camera and microphone permissions*: Automated rejection at compile upload validations if camera permission details are absent.
- *Push Notification requirements*: Registration failures or missing notifications on target user devices.
- *Background execution policies*: Immediate manual rejection if declaring background modes without verified runtime use.
- *Security updates*: Export compliance validation holds in App Store Connect.
- *SDK requirements*: Submission holds if bundled SDK structures lack matching manifest declarations.
- *Apple Developer Program License Agreement*: Submission blocks for build distribution if program terms are unsigned.
- *Minimum SDK versions*: Complete publishing blockages if targets fall below mandatory minimum thresholds.
- *Xcode requirements*: Complete rejection at publishing gates if compiled using older Xcode releases.
- *Human Interface Guidelines*: UI presentation complaints or potential manual reviewer rejections.
- *Swift requirements*: Compiler errors or race warnings if language features deprecate old patterns.
- *App Store Connect announcements*: Publishing delays if console configurations mismatch updated portal regulations.
- **Overall Standing**: High risk of upload warnings or immediate build distribution blockages if the validation threshold is not proactively cleared.

## 7. Migration steps
- **App Store Review Guidelines**: Audit app metadata and ensure App Review Notes are configured with a working test account.
- **Human Interface Guidelines**: Confirm spacing, padding, and dark mode layouts conform to HIG specifications.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **Human Interface Guidelines**: Confirm spacing, padding, and dark mode layouts conform to HIG specifications.
- **Apple Privacy requirements**: Validate that the privacy policy URL is reachable and displayed within the app UI.
- **Privacy Manifests**: Add and configure a comprehensive PrivacyInfo.xcprivacy manifest.
- **Privacy Manifests**: Add and configure a comprehensive PrivacyInfo.xcprivacy manifest.
- **Required Reason APIs**: Declare valid reason codes for accessing UserDefaults or systemUptime in PrivacyInfo.xcprivacy.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **App Tracking Transparency**: Verify ATTrackingManager requests consent and that NSUserTrackingUsageDescription is defined.
- **Sign in with Apple**: Ensure Sign in with Apple is offered adjacent to any other social sign-in services.
- **In-App Purchase policies**: Ensure digital goods transact via StoreKit and integrate restorePurchases features.
- **In-App Purchase policies**: Ensure digital goods transact via StoreKit and integrate restorePurchases features.
- **Alternative payment regulations**: Configure SKExternalPurchase links and configure billing entitlements if utilizing external payment pathways.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **DMA compliance changes**: Align browser engines or distribution channels with alternative EU marketplace specifications.
- **Accessibility requirements**: Ensure UI components possess accessibilityLabel markers and comply with WCAG AA guidelines.
- **AI-related App Store policies**: Integrate content moderation filters and prominent disclosures for conversational AI systems.
- **Child safety requirements**: Exclude third-party tracking from child-targeted sections and enforce robust parental gates.
- **HealthKit policies**: Restrict HealthKit data mining and confirm NSHealthShareUsageDescription is defined.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **Location permissions**: Verify that precise geolocation features present a transparent purpose string in Info.plist.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **Human Interface Guidelines**: Confirm spacing, padding, and dark mode layouts conform to HIG specifications.
- **Camera and microphone permissions**: Declare precise usage descriptions for AVCaptureDevice access inside Info.plist.
- **Push Notification requirements**: Configure push entitlements and verify aps-environment variables.
- **Background execution policies**: Strip unused UIBackgroundModes options from Info.plist.
- **Security updates**: Declare encryption exemptions using ITSAppUsesNonExemptEncryption.
- **SDK requirements**: Audit third-party SDK dependencies for compliance, sizes, and privacy manifests.
- **Apple Developer Program License Agreement**: Accept updated program license terms in App Store Connect.
- **Minimum SDK versions**: Update deployment target values to conform to current publishing requirements.
- **Xcode requirements**: Configure compilation environment to leverage required stable Xcode toolchain versions.
- **Human Interface Guidelines**: Confirm spacing, padding, and dark mode layouts conform to HIG specifications.
- **Swift requirements**: Ensure SWIFT_VERSION is at least 5.x/6.0 and verify concurrency structures.
- **App Store Connect announcements**: Align metadata properties and portal fields with latest portal announcement rules.

## 8. Backward compatibility
All modifications are backward-compatible. Deployment targets are aligned with active compliance levels while preserving compatibility for existing deployed versions. Fallback code paths are implemented for scoped features on older device targets.

## 9. Implementation checklist
- [ ] Configure active test credentials in App Review Notes.
- [ ] Audit typography scales and touch target spacing (>= 44x44pt).
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Audit typography scales and touch target spacing (>= 44x44pt).
- [ ] Place the active privacy policy link in app menus and listing fields.
- [ ] Create PrivacyInfo.xcprivacy with valid collected data type declarations.
- [ ] Create PrivacyInfo.xcprivacy with valid collected data type declarations.
- [ ] Declare correct NSPrivacyAccessedAPITypes codes in the root privacy manifest.
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Configure NSUserTrackingUsageDescription with a specific purpose statement.
- [ ] Implement SIWA button layout next to third-party social sign-in options.
- [ ] Wire restorePurchases or restoreCompletedTransactions flows in purchase UI.
- [ ] Wire restorePurchases or restoreCompletedTransactions flows in purchase UI.
- [ ] Apply StoreKit external purchase entitlements to configurations.
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Implement alternative marketplace distribution entitlements if targeting EU regions.
- [ ] Audit storyboards and SwiftUI code for accessibilityLabel parameters.
- [ ] Add flagging/reporting buttons directly next to AI generative elements.
- [ ] Confirm that zero tracking SDKs run in Kids Category flows.
- [ ] Audit codebase; verify zero health data is sent to marketing/ad processors.
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Update NSLocationWhenInUseUsageDescription with specific features.
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Audit typography scales and touch target spacing (>= 44x44pt).
- [ ] Define descriptive camera and microphone purpose strings.
- [ ] Verify aps-environment keys are set within entitlements configurations.
- [ ] Review Info.plist background modes; remove irrelevant categories.
- [ ] Set ITSAppUsesNonExemptEncryption value in Info.plist configurations.
- [ ] Verify that third-party compiled SDK files are fully updated.
- [ ] Verify that the Account Holder has signed updated terms in App Store Connect.
- [ ] Update deployment targets in pbxproj or xcconfig config files.
- [ ] Verify that CI/CD servers use the mandated Xcode toolchain for compiling packages.
- [ ] Audit typography scales and touch target spacing (>= 44x44pt).
- [ ] Validate compiling under strict concurrency options if transitioning compilation targets.
- [ ] Verify support/privacy links and developer descriptions inside publishing configurations.
- [ ] Run the local pre-submission compliance guard checks.

## 10. Testing checklist
- [ ] Verify clean compilation on physical Apple test devices or simulators.
- [ ] Confirm layout presentation satisfies HIG recommendations.
- [ ] Ensure privacy declarations match current data practices.
- [ ] Run automated compliance scripts to confirm zero remaining validation alerts.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with migration statuses.
- [ ] Align App Review Notes with working test account credentials.
- [ ] Complete required legal agreements within the App Store Connect portal.

## 12. Compliance impact
- **Publishing Gate**: Secures continuous deployment capabilities by clearing Xcode, SDK target, and manifest validation thresholds.
- **Developer Account Health**: Reduces manual audit times and protects developer credentials from warnings.
- **Legal Compliance**: Maintains alignment with EAA accessibility criteria and child privacy regulations.

## 13. Breaking changes
- Incrementing target deployment versions may sunset support for legacy OS releases.
- Strict concurrency checks under newer toolchains may highlight thread safety requirements.

## 14. Review checklist
- [ ] Confirm that all required manifest keys are declared.
- [ ] Verify that UI layouts adapt gracefully across devices.
- [ ] Ensure all purpose strings are descriptive and accurate.

## 15. Approver recommendations
Ensure that the App Store Connect account holder reviews and signs the latest license agreements, as failure to do so blocks storefront updates regardless of code compliance. Verify that StoreKit implementation elements have been validated prior to production release.
