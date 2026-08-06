<!-- APPLE_POLICY_MONITOR_START -->
# Apple Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor.py` to track compliance areas.

## Monitored Requirements Update Log

### 1. [Privacy Manifests] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Severity Impact**: Critical
- **Repository Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 2. [Required Reason APIs] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Severity Impact**: Critical
- **Repository Impact**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 3. [In-App Purchase policies] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Severity Impact**: Critical
- **Repository Impact**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 4. [Alternative payment regulations] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Severity Impact**: High
- **Repository Impact**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 5. [App Store Review Guidelines] App Store Review Guidelines and 4.3 Saturated Categories Update
- **Published Date**: Tue, 09 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/review-guidelines-update](https://mock.invalid/apple-news/review-guidelines-update)
- **Severity Impact**: High
- **Repository Impact**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 6. [SDK requirements] Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/upcoming-requirements/?id=xcode-26](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)
- **Severity Impact**: High
- **Repository Impact**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

### 7. [Minimum SDK versions] Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Resource**: [https://developer.apple.com/news/upcoming-requirements/?id=xcode-26](https://developer.apple.com/news/upcoming-requirements/?id=xcode-26)
- **Severity Impact**: High
- **Repository Impact**: Annual minimum deployment target or target SDK version updates enforced by stores.
- **Scan Verdict**: No relevant file types or signatures found in the repository.
- **Identified Affected Files**: None found.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifests
- **Severity Impact**: Critical
- [ ] **Task 1**: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### Tasks for Required Reason APIs
- **Severity Impact**: Critical
- [ ] **Task 1**: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] **Task 2**: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### Tasks for In-App Purchase policies
- **Severity Impact**: Critical
- [ ] **Task 1**: Route all digital goods through StoreKit in-app purchases.
- [ ] **Task 2**: Add a prominent Restore Purchases control for non-consumable goods.
- [ ] **Task 3**: Verify pricing displays correspond with Apple subscription terms requirements.

### Tasks for Alternative payment regulations
- **Severity Impact**: High
- [ ] **Task 1**: Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] **Task 2**: Show mandatory disclosure sheets before redirecting to external web purchase flows.

### Tasks for App Store Review Guidelines
- **Severity Impact**: High
- [ ] **Task 1**: Review the updated guidelines section in APPLE.md or the official site.
- [ ] **Task 2**: Ensure App Review Notes are updated with working test accounts.
- [ ] **Task 3**: Verify the application flows align with the updated guideline numbers.

### Tasks for SDK requirements
- **Severity Impact**: High
- [ ] **Task 1**: Perform regular updates on bundled third-party SDKs.
- [ ] **Task 2**: Ensure each third-party SDK has its signed privacy manifest file.

### Tasks for Minimum SDK versions
- **Severity Impact**: High
- [ ] **Task 1**: Update deployment target version to match latest requirements.
- [ ] **Task 2**: Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

<!-- APPLE_POLICY_MONITOR_END -->