<!-- APPLE_POLICY_MONITOR_START -->

> **Simulated output, not live announcements.** This file was generated from sample
> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,
> publish dates, and descriptions below are examples that show the shape of a migration
> report, not real publications. Only the linked official documentation URLs are real.
> Re-run the monitor with `--live` against the real feeds before treating anything here
> as an actual requirement.

# Apple Developer Requirements Migration & Policy Report

This report is continuously generated and updated by `scripts/monitor.py` to track compliance across all 25 Apple developer requirement tracks.

## Monitored Requirements Update Log

### 1. [Privacy Manifests] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Verification Status**: Priority 4 (Unverified)
- **Release Impact**: Critical
- **Repo Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 2. [Required Reason APIs] Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/privacy-requirements](https://mock.invalid/apple-news/privacy-requirements)
- **Verification Status**: Priority 4 (Unverified)
- **Release Impact**: Critical
- **Repo Impact**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 3. [In-App Purchase policies] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Verification Status**: Priority 4 (Unverified)
- **Release Impact**: Critical
- **Repo Impact**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 4. [Alternative payment regulations] Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/iap-updates](https://mock.invalid/apple-news/iap-updates)
- **Verification Status**: Priority 4 (Unverified)
- **Release Impact**: High
- **Repo Impact**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

### 5. [App Store Review Guidelines] App Store Review Guidelines and 4.3 Saturated Categories Update
- **Published Date**: Tue, 09 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://mock.invalid/apple-news/review-guidelines-update](https://mock.invalid/apple-news/review-guidelines-update)
- **Verification Status**: Priority 1 (Verified)
- **Release Impact**: High
- **Repo Impact**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for Privacy Manifests
- **Impact Level**: Critical
- [ ] **Task 1**: Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] **Task 2**: Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### Tasks for Required Reason APIs
- **Impact Level**: Critical
- [ ] **Task 1**: Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] **Task 2**: Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### Tasks for In-App Purchase policies
- **Impact Level**: Critical
- [ ] **Task 1**: Route all digital goods through StoreKit in-app purchases.
- [ ] **Task 2**: Add a prominent Restore Purchases control for non-consumable goods.
- [ ] **Task 3**: Verify pricing displays correspond with Apple subscription terms requirements.

### Tasks for Alternative payment regulations
- **Impact Level**: High
- [ ] **Task 1**: Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] **Task 2**: Show mandatory disclosure sheets before redirecting to external web purchase flows.

### Tasks for App Store Review Guidelines
- **Impact Level**: High
- [ ] **Task 1**: Review the updated guidelines section in APPLE.md or the official site.
- [ ] **Task 2**: Ensure App Review Notes are updated with working test accounts.
- [ ] **Task 3**: Verify the application flows align with the updated guideline numbers.

<!-- APPLE_POLICY_MONITOR_END -->