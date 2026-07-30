<!-- APPLE_POLICY_MONITOR_START -->
# Apple Developer and App Store Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-apple.py` to track compliance areas.

## Monitored Requirements Update Log

### 1. [App Store Review Guidelines] Guidelines Update: App Store Review Guidelines Clarification
- **Published Date**: Mon, 15 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/review/guidelines/](https://developer.apple.com/app-store/review/guidelines/)
- **Description**: Apple has updated the App Store Review Guidelines regarding Guideline 2.1 and 4.3 to ensure higher standards of design quality and metadata verification. Testing credentials must be valid.

### 2. [Human Interface Guidelines] Guidelines Update: App Store Review Guidelines Clarification
- **Published Date**: Mon, 15 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/review/guidelines/](https://developer.apple.com/app-store/review/guidelines/)
- **Description**: Apple has updated the App Store Review Guidelines regarding Guideline 2.1 and 4.3 to ensure higher standards of design quality and metadata verification. Testing credentials must be valid.

### 3. [Apple Developer Program License Agreement] Upcoming Apple Developer Program License Agreement Updates
- **Published Date**: Tue, 16 Jun 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/terms/](https://developer.apple.com/support/terms/)
- **Description**: Apple announces modifications to the Developer Program License Agreement terms. Account owners must sign into App Store Connect to accept updated terms.

### 4. [Human Interface Guidelines] Human Interface Guidelines: Layout and Dark Mode Sizing Updates
- **Published Date**: Wed, 17 Jun 2026 12:00:00 PDT
- **Official Resource**: [https://developer.apple.com/design/human-interface-guidelines/](https://developer.apple.com/design/human-interface-guidelines/)
- **Description**: Apple updates recommended spacing, design guidelines, and typography scales for SwiftUI and UIKit layouts under HIG guidelines.

### 5. [Apple Privacy requirements] Apple Privacy Policy and Privacy Nutrition Label Compliance
- **Published Date**: Thu, 18 Jun 2026 13:00:00 PDT
- **Official Resource**: [https://developer.apple.com/privacy/](https://developer.apple.com/privacy/)
- **Description**: Stricter auditing of user data collection declarations. App Store Connect privacy labels must align exactly with your privacy policy URL and runtime data collection.

### 6. [Privacy Manifests] Privacy Manifests Enforcement and SDK Integration Requirements
- **Published Date**: Fri, 19 Jun 2026 14:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/privacy-manifests/](https://developer.apple.com/support/privacy-manifests/)
- **Description**: Enforcing signed PrivacyInfo.xcprivacy files for all third-party SDK dependencies. Failing declarations will trigger rejection at compile validation gates.

### 7. [Privacy Manifests] Required Reason APIs Declaration Mandate for UserDefaults and systemUptime
- **Published Date**: Sat, 20 Jun 2026 15:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/required-reason-api/](https://developer.apple.com/support/required-reason-api/)
- **Description**: Apps accessing UserDefaults, systemUptime, or stat file APIs must declare valid NSPrivacyAccessedAPITypes within their PrivacyInfo.xcprivacy manifest.

### 8. [Required Reason APIs] Required Reason APIs Declaration Mandate for UserDefaults and systemUptime
- **Published Date**: Sat, 20 Jun 2026 15:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/required-reason-api/](https://developer.apple.com/support/required-reason-api/)
- **Description**: Apps accessing UserDefaults, systemUptime, or stat file APIs must declare valid NSPrivacyAccessedAPITypes within their PrivacyInfo.xcprivacy manifest.

### 9. [Apple Developer Program License Agreement] App Tracking Transparency and IDFA Tracking Permission Prompt Enforcement
- **Published Date**: Sun, 21 Jun 2026 16:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-tracking-transparency/](https://developer.apple.com/app-tracking-transparency/)
- **Description**: Under ATT guidelines, requesting ASIdentifierManager or IDFA tracking requires prompting via ATTrackingManager and explaining the tracking purpose string.

### 10. [App Tracking Transparency] App Tracking Transparency and IDFA Tracking Permission Prompt Enforcement
- **Published Date**: Sun, 21 Jun 2026 16:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-tracking-transparency/](https://developer.apple.com/app-tracking-transparency/)
- **Description**: Under ATT guidelines, requesting ASIdentifierManager or IDFA tracking requires prompting via ATTrackingManager and explaining the tracking purpose string.

### 11. [Sign in with Apple] Sign in with Apple Social Login Integration Guidelines
- **Published Date**: Mon, 22 Jun 2026 17:00:00 PDT
- **Official Resource**: [https://developer.apple.com/sign-in-with-apple/](https://developer.apple.com/sign-in-with-apple/)
- **Description**: To maintain compatibility, any app offering third-party social authentication must prominently present Sign in with Apple (SIWA) on the landing view.

### 12. [In-App Purchase policies] In-App Purchase Policies, Auto-Renewable Subscription Terms
- **Published Date**: Tue, 23 Jun 2026 18:00:00 PDT
- **Official Resource**: [https://developer.apple.com/in-app-purchase/](https://developer.apple.com/in-app-purchase/)
- **Description**: StoreKit in-app purchases and subscription flows must comply with auto-renewable pricing guidelines and include restorePurchases functionality clearly.

### 13. [In-App Purchase policies] Alternative Payment Methods and External Purchase Link Disclosures
- **Published Date**: Wed, 24 Jun 2026 19:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/storekit-external-purchase/](https://developer.apple.com/support/storekit-external-purchase/)
- **Description**: Allows eligible developers to direct users to external purchase options on their website. Stricter billing warning sheets apply for non-StoreKit routes.

### 14. [Alternative payment regulations] Alternative Payment Methods and External Purchase Link Disclosures
- **Published Date**: Wed, 24 Jun 2026 19:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/storekit-external-purchase/](https://developer.apple.com/support/storekit-external-purchase/)
- **Description**: Allows eligible developers to direct users to external purchase options on their website. Stricter billing warning sheets apply for non-StoreKit routes.

### 15. [Apple Developer Program License Agreement] Digital Markets Act: EU Alternative App Marketplace Entitlements
- **Published Date**: Thu, 25 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/alternative-app-distribution/](https://developer.apple.com/support/alternative-app-distribution/)
- **Description**: Alternative marketplace and distribution mechanisms in the European Union under DMA rules. Outlines core technology fee regulations.

### 16. [DMA compliance changes] Digital Markets Act: EU Alternative App Marketplace Entitlements
- **Published Date**: Thu, 25 Jun 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/alternative-app-distribution/](https://developer.apple.com/support/alternative-app-distribution/)
- **Description**: Alternative marketplace and distribution mechanisms in the European Union under DMA rules. Outlines core technology fee regulations.

### 17. [Accessibility requirements] Accessibility standard EN 301 549 and VoiceOver Updates
- **Published Date**: Fri, 26 Jun 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/accessibility/](https://developer.apple.com/accessibility/)
- **Description**: Enhancing assistive technology guidelines. Applications must provide clean accessibilityLabel identifiers and support Dynamic Type scaling.

### 18. [AI-related App Store policies] App Store AI-Generated Content Moderation and LLM Policies
- **Published Date**: Sat, 27 Jun 2026 12:00:00 PDT
- **Official Resource**: [https://developer.apple.com/news/ai-guideline/](https://developer.apple.com/news/ai-guideline/)
- **Description**: Apps incorporating generative AI or LLMs must implement safety moderation tools, user disclosures, and 24-hour reporting flows for offensive outputs.

### 19. [Child safety requirements] Child safety requirements: COPPA and Kids Category Standards
- **Published Date**: Sun, 28 Jun 2026 13:00:00 PDT
- **Official Resource**: [https://developer.apple.com/app-store/kids-category/](https://developer.apple.com/app-store/kids-category/)
- **Description**: Apps targeted at children under-13 must avoid analytics or tracking SDKs, require age verification parental gates, and comply with COPPA criteria.

### 20. [HealthKit policies] HealthKit Data Mining, HKHealthStore Authorization Restrictions
- **Published Date**: Mon, 29 Jun 2026 14:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/healthkit/](https://developer.apple.com/documentation/healthkit/)
- **Description**: Prohibits using HealthKit or HKHealthStore user data for marketing, profiling, or behavioral advertising. Stricter purpose string requirements apply.

### 21. [Apple Developer Program License Agreement] Location permissions: CLLocationManager Purpose String Constraints
- **Published Date**: Tue, 30 Jun 2026 15:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/corelocation/](https://developer.apple.com/documentation/corelocation/)
- **Description**: Stricter reviews for background location usage. Ensure NSLocationWhenInUseUsageDescription explicitly explains the exact feature needing location.

### 22. [Location permissions] Location permissions: CLLocationManager Purpose String Constraints
- **Published Date**: Tue, 30 Jun 2026 15:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/corelocation/](https://developer.apple.com/documentation/corelocation/)
- **Description**: Stricter reviews for background location usage. Ensure NSLocationWhenInUseUsageDescription explicitly explains the exact feature needing location.

### 23. [Apple Developer Program License Agreement] Camera and microphone permissions: AVCaptureDevice Purpose Disclosures
- **Published Date**: Wed, 01 Jul 2026 16:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/avfoundation/](https://developer.apple.com/documentation/avfoundation/)
- **Description**: Requiring highly specific NSCameraUsageDescription and NSMicrophoneUsageDescription entries explaining features prior to media capture.

### 24. [Human Interface Guidelines] Camera and microphone permissions: AVCaptureDevice Purpose Disclosures
- **Published Date**: Wed, 01 Jul 2026 16:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/avfoundation/](https://developer.apple.com/documentation/avfoundation/)
- **Description**: Requiring highly specific NSCameraUsageDescription and NSMicrophoneUsageDescription entries explaining features prior to media capture.

### 25. [Camera and microphone permissions] Camera and microphone permissions: AVCaptureDevice Purpose Disclosures
- **Published Date**: Wed, 01 Jul 2026 16:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/avfoundation/](https://developer.apple.com/documentation/avfoundation/)
- **Description**: Requiring highly specific NSCameraUsageDescription and NSMicrophoneUsageDescription entries explaining features prior to media capture.

### 26. [Push Notification requirements] Push Notification requirements: APNs Payload and Entitlements Updates
- **Published Date**: Thu, 02 Jul 2026 17:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/usernotifications/](https://developer.apple.com/documentation/usernotifications/)
- **Description**: Stricter registration boundaries for remote notifications and verification of valid aps-environment flags in app entitlement configurations.

### 27. [Background execution policies] Background execution policies: UIBackgroundModes Restriction updates
- **Published Date**: Fri, 03 Jul 2026 18:00:00 PDT
- **Official Resource**: [https://developer.apple.com/documentation/uikit/app_play/choosing_background_execution/](https://developer.apple.com/documentation/uikit/app_play/choosing_background_execution/)
- **Description**: App Review will reject apps declaring background execution mode tags in UIBackgroundModes without core, continuous background functionality.

### 28. [Security updates] Security updates: ITSAppUsesNonExemptEncryption Compliance Review
- **Published Date**: Sat, 04 Jul 2026 19:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/export-compliance/](https://developer.apple.com/support/export-compliance/)
- **Description**: Reiterates requirement to correctly declare non-exempt encryption usage via ITSAppUsesNonExemptEncryption in Info.plist before storefront packaging.

### 29. [SDK requirements] SDK requirements: Third-Party SDK Privacy Declarations
- **Published Date**: Sun, 05 Jul 2026 10:00:00 PDT
- **Official Resource**: [https://developer.apple.com/support/third-party-sdk/](https://developer.apple.com/support/third-party-sdk/)
- **Description**: commonly used SDK bundles (such as Firebase, AppsFlyer, Facebook) must include valid privacy files and size optimization adjustments.

### 30. [Apple Developer Program License Agreement] Minimum SDK Deployment Target Enforcements for Submission
- **Published Date**: Mon, 06 Jul 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/news/sdk-target-guidelines/](https://developer.apple.com/news/sdk-target-guidelines/)
- **Description**: All submissions to the App Store must set IPHONEOS_DEPLOYMENT_TARGET and target recent iOS SDK platforms prior to compiling packages.

### 31. [Minimum SDK versions] Minimum SDK Deployment Target Enforcements for Submission
- **Published Date**: Mon, 06 Jul 2026 11:00:00 PDT
- **Official Resource**: [https://developer.apple.com/news/sdk-target-guidelines/](https://developer.apple.com/news/sdk-target-guidelines/)
- **Description**: All submissions to the App Store must set IPHONEOS_DEPLOYMENT_TARGET and target recent iOS SDK platforms prior to compiling packages.

### 32. [Xcode requirements] Xcode requirements: Mandatory Xcode Submission Build Mandate
- **Published Date**: Tue, 07 Jul 2026 12:00:00 PDT
- **Official Resource**: [https://developer.apple.com/news/xcode-requirements-mandate/](https://developer.apple.com/news/xcode-requirements-mandate/)
- **Description**: Apps must be compiled with the latest stable releases of Xcode to fulfill submission validation checks in App Store Connect.

### 33. [Human Interface Guidelines] Swift requirements: SWIFT_VERSION 6 Concurrency Policies
- **Published Date**: Wed, 08 Jul 2026 13:00:00 PDT
- **Official Resource**: [https://developer.apple.com/swift/](https://developer.apple.com/swift/)
- **Description**: Updates regarding evolving Swift concurrency, task queues, and asynchronous APIs to ensure high performance and thread-safe execution.

### 34. [Swift requirements] Swift requirements: SWIFT_VERSION 6 Concurrency Policies
- **Published Date**: Wed, 08 Jul 2026 13:00:00 PDT
- **Official Resource**: [https://developer.apple.com/swift/](https://developer.apple.com/swift/)
- **Description**: Updates regarding evolving Swift concurrency, task queues, and asynchronous APIs to ensure high performance and thread-safe execution.

### 35. [App Store Connect announcements] App Store Connect announcements: Management and Metadata Changes
- **Published Date**: Thu, 09 Jul 2026 14:00:00 PDT
- **Official Resource**: [https://developer.apple.com/news/app-store-connect-updates/](https://developer.apple.com/news/app-store-connect-updates/)
- **Description**: Updates to the metadata-audit schema, App Review Notes structures, and support/privacy URLs configuration rules inside the publishing portal.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for App Store Review Guidelines
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for App Store Review Guidelines are checked and handled.

### Tasks for Human Interface Guidelines
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Human Interface Guidelines are checked and handled.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for Human Interface Guidelines
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Human Interface Guidelines are checked and handled.

### Tasks for Apple Privacy requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Privacy requirements are checked and handled.

### Tasks for Privacy Manifests
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task 1**: Declare NSPrivacyCollectedDataTypes in PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Audit third-party SDK dependencies for matching privacy manifest files.

### Tasks for Privacy Manifests
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task 1**: Declare NSPrivacyCollectedDataTypes in PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Audit third-party SDK dependencies for matching privacy manifest files.

### Tasks for Required Reason APIs
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task 1**: Add UserDefaults accessed reason codes to PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Declare systemUptime reasons if accessing system boot metrics.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for App Tracking Transparency
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for App Tracking Transparency are checked and handled.

### Tasks for Sign in with Apple
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Sign in with Apple are checked and handled.

### Tasks for In-App Purchase policies
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task 1**: Verify restorePurchases functionalities trigger in purchase layouts.
- [ ] **Task 2**: Ensure subscription disclosures correspond to StoreKit regulations.

### Tasks for In-App Purchase policies
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task 1**: Verify restorePurchases functionalities trigger in purchase layouts.
- [ ] **Task 2**: Ensure subscription disclosures correspond to StoreKit regulations.

### Tasks for Alternative payment regulations
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Alternative payment regulations are checked and handled.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for DMA compliance changes
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for DMA compliance changes are checked and handled.

### Tasks for Accessibility requirements
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Accessibility requirements are checked and handled.

### Tasks for AI-related App Store policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for AI-related App Store policies are checked and handled.

### Tasks for Child safety requirements
- **Regulatory Impact**: Critical priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Child safety requirements are checked and handled.

### Tasks for HealthKit policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for HealthKit policies are checked and handled.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for Location permissions
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Location permissions are checked and handled.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for Human Interface Guidelines
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Human Interface Guidelines are checked and handled.

### Tasks for Camera and microphone permissions
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Camera and microphone permissions are checked and handled.

### Tasks for Push Notification requirements
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Push Notification requirements are checked and handled.

### Tasks for Background execution policies
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Background execution policies are checked and handled.

### Tasks for Security updates
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Security updates are checked and handled.

### Tasks for SDK requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for SDK requirements are checked and handled.

### Tasks for Apple Developer Program License Agreement
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Apple Developer Program License Agreement are checked and handled.

### Tasks for Minimum SDK versions
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Minimum SDK versions are checked and handled.

### Tasks for Xcode requirements
- **Regulatory Impact**: High priority. Publishing gates require action.
- [ ] **Task 1**: Update build tools and update deployment targets to Xcode mandate.
- [ ] **Task 2**: Clean build targets and verify output on emulator devices.

### Tasks for Human Interface Guidelines
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Human Interface Guidelines are checked and handled.

### Tasks for Swift requirements
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for Swift requirements are checked and handled.

### Tasks for App Store Connect announcements
- **Regulatory Impact**: Medium priority. Publishing gates require action.
- [ ] **Task**: Verify that all platform criteria for App Store Connect announcements are checked and handled.

<!-- APPLE_POLICY_MONITOR_END -->