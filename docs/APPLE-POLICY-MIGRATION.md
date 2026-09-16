# Apple Developer & App Store Policy Migration Report

This document details monitored Apple developer requirement updates, repository impact, affected codebase files, required migration steps, and estimated release impact across all 25 Apple compliance tracks.

**Last Monitored Date**: 2026-09-16 08:30:18

## Summary of Monitored Tracks

Total Track Updates Evaluated: 7

| # | Compliance Track | Release Impact | Announcement Title | Affected Files Count |
|---|---|---|---|---|
| 1 | Privacy Manifests | Critical | Upcoming Requirements for Privacy Manifests and Required Reason APIs | 0 |
| 2 | Required Reason APIs | Critical | Upcoming Requirements for Privacy Manifests and Required Reason APIs | 0 |
| 3 | In-App Purchase policies | Critical | Updates to In-App Purchase Policies and Alternative Payment Options | 0 |
| 4 | Alternative payment regulations | High | Updates to In-App Purchase Policies and Alternative Payment Options | 0 |
| 5 | App Store Review Guidelines | High | App Store Review Guidelines and 4.3 Saturated Categories Update | 0 |
| 6 | SDK requirements | High | Xcode 26 and Minimum iOS SDK Requirements for Submission | 0 |
| 7 | Minimum SDK versions | High | Xcode 26 and Minimum iOS SDK Requirements for Submission | 0 |

## Detailed Track Analysis & Migration Requirements

### 1. Track: Privacy Manifests
- **Announcement**: Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Link**: https://mock.invalid/apple-news/privacy-requirements
- **Release Impact**: Critical
- **Repository Impact**: Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.
- [ ] Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.

### 2. Track: Required Reason APIs
- **Announcement**: Upcoming Requirements for Privacy Manifests and Required Reason APIs
- **Published Date**: Wed, 15 May 2026 10:00:00 GMT
- **Official Link**: https://mock.invalid/apple-news/privacy-requirements
- **Release Impact**: Critical
- **Repository Impact**: Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.
- [ ] Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.

### 3. Track: In-App Purchase policies
- **Announcement**: Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Link**: https://mock.invalid/apple-news/iap-updates
- **Release Impact**: Critical
- **Repository Impact**: App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Route all digital goods through StoreKit in-app purchases.
- [ ] Add a prominent Restore Purchases control for non-consumable goods.
- [ ] Verify pricing displays correspond with Apple subscription terms requirements.

### 4. Track: Alternative payment regulations
- **Announcement**: Updates to In-App Purchase Policies and Alternative Payment Options
- **Published Date**: Mon, 01 Jun 2026 09:00:00 GMT
- **Official Link**: https://mock.invalid/apple-news/iap-updates
- **Release Impact**: High
- **Repository Impact**: Permitted exceptions and requirements for offering third-party payment links (region-gated).
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Ensure appropriate entitlements are requested and set up for alternative billing.
- [ ] Show mandatory disclosure sheets before redirecting to external web purchase flows.

### 5. Track: App Store Review Guidelines
- **Announcement**: App Store Review Guidelines and 4.3 Saturated Categories Update
- **Published Date**: Tue, 09 Jun 2026 14:00:00 GMT
- **Official Link**: https://mock.invalid/apple-news/review-guidelines-update
- **Release Impact**: High
- **Repository Impact**: Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Review the updated guidelines section in APPLE.md or the official site.
- [ ] Ensure App Review Notes are updated with working test accounts.
- [ ] Verify the application flows align with the updated guideline numbers.

### 6. Track: SDK requirements
- **Announcement**: Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Link**: https://developer.apple.com/news/upcoming-requirements/?id=xcode-26
- **Release Impact**: High
- **Repository Impact**: Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Perform regular updates on bundled third-party SDKs.
- [ ] Ensure each third-party SDK has its signed privacy manifest file.

### 7. Track: Minimum SDK versions
- **Announcement**: Xcode 26 and Minimum iOS SDK Requirements for Submission
- **Published Date**: Mon, 03 Feb 2026 08:00:00 GMT
- **Official Link**: https://developer.apple.com/news/upcoming-requirements/?id=xcode-26
- **Release Impact**: High
- **Repository Impact**: Annual minimum deployment target or target SDK version updates enforced by stores.
- **Scan Verdict**: No relevant file types or signatures found in the repository.

**Identified Affected Files**:
- None detected in static scanner.

**Generated Migration Tasks**:
- [ ] Update deployment target version to match latest requirements.
- [ ] Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).

---
*Report generated automatically by `scripts/monitor.py`.*
