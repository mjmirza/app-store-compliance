<!-- APPLE_POLICY_MONITOR_START -->
# Apple App Store Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor.py` to track compliance areas.

## Monitored Requirements Update Log

### 1. [Privacy Manifests] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Description**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.

### 2. [Required Reason APIs] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Description**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).

### 3. [In-App Purchase policies] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Description**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.

### 4. [Alternative payment regulations] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Description**: Permitted exceptions and requirements for offering third-party payment links (region-gated).

### 5. [App Store Review Guidelines] App Store Review Guidelines and 4.3 Saturated Categories Update
- **Published Date**: Tue, 09 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/review-guidelines-update](https://mock.invalid/apple-news/review-guidelines-update)
- **Description**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.

### 6. [SDK requirements] Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/upcoming-requirements/?id=xcode-26](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)
- **Description**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.

### 7. [Minimum SDK versions] Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/upcoming-requirements/?id=xcode-26](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)
- **Description**: Annual minimum deployment target or target SDK version updates enforced by stores.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifests
- **Regulatory Impact**: Critical priority. App Store submission expectations require action.
- [ ] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### Tasks for Required Reason APIs
- **Regulatory Impact**: Critical priority. App Store submission expectations require action.
- [ ] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### Tasks for In-App Purchase policies
- **Regulatory Impact**: Critical priority. App Store submission expectations require action.
- [ ] Route all digital goods through StoreKit in-app purchases.
- [ ] Add a prominent Restore Purchases control for non-consumable goods.
- [ ] Verify pricing displays correspond with Apple subscription terms requirements.

### Tasks for Alternative payment regulations
- **Regulatory Impact**: High priority. App Store submission expectations require action.
- [ ] Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] Show mandatory disclosure sheets before redirecting to external web purchase flows.

### Tasks for App Store Review Guidelines
- **Regulatory Impact**: High priority. App Store submission expectations require action.
- [ ] Review the updated guidelines section in APPLE.md or the official site.
- [ ] Ensure App Review Notes are updated with working test accounts.
- [ ] Verify the application flows align with the updated guideline numbers.

### Tasks for SDK requirements
- **Regulatory Impact**: High priority. App Store submission expectations require action.
- [ ] Perform regular updates on bundled third-party SDKs.
- [ ] Ensure each third-party SDK has its signed privacy manifest file.

### Tasks for Minimum SDK versions
- **Regulatory Impact**: High priority. App Store submission expectations require action.
- [ ] Update deployment target version to match latest requirements.
- [ ] Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

<!-- APPLE_POLICY_MONITOR_END -->