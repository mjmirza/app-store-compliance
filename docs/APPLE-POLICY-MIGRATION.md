<!-- APPLE_POLICY_MONITOR_START -->
# Apple Developer Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-apple.py` to track compliance areas.

## Active Requirements Log

| ID | Category | Announcement / Update | Date Published | Action Required | Status |
|---|---|---|---|---|---|
| APP-REQ-001 | Privacy Manifests | [Mandatory Privacy Manifest Integration and Domain Tracking Requirements](https://developer.apple.com/news/?id=privacy-manifests-mandatory) | Mon, 01 Jun 2026 10:00:00 GMT | Audit codebase and configuration | Pending Review |
| APP-REQ-002 | Required Reason APIs | [Mandatory Privacy Manifest Integration and Domain Tracking Requirements](https://developer.apple.com/news/?id=privacy-manifests-mandatory) | Mon, 01 Jun 2026 10:00:00 GMT | Audit codebase and configuration | Pending Review |
| APP-REQ-003 | In-App Purchase policies | [App Store In-App Purchase and StoreKit Updates](https://developer.apple.com/news/?id=storekit-iap-policies) | Tue, 02 Jun 2026 11:00:00 GMT | Audit codebase and configuration | Pending Review |
| APP-REQ-004 | Apple Developer Program License Agreement | [EU Digital Markets Act Compliance Changes and Alternative App Marketplaces](https://developer.apple.com/news/?id=dma-compliance-eu) | Wed, 03 Jun 2026 12:00:00 GMT | Audit codebase and configuration | Pending Review |
| APP-REQ-005 | DMA compliance changes | [EU Digital Markets Act Compliance Changes and Alternative App Marketplaces](https://developer.apple.com/news/?id=dma-compliance-eu) | Wed, 03 Jun 2026 12:00:00 GMT | Audit codebase and configuration | Pending Review |

## Core Migration Action Items

### Category: Privacy Manifests
- **Impact**: Updates affecting the 'Privacy Manifests' guideline parameters.
  - **Migration Tasks**:
    - [ ] Create a root PrivacyInfo.xcprivacy and audit external dependencies.

### Category: Required Reason APIs
- **Impact**: Updates affecting the 'Required Reason APIs' guideline parameters.
  - **Migration Tasks**:
    - [ ] Add NSPrivacyAccessedAPITypes declarations and reason codes to PrivacyInfo.xcprivacy.

### Category: In-App Purchase policies
- **Impact**: Updates affecting the 'In-App Purchase policies' guideline parameters.
  - **Migration Tasks**:
    - [ ] Implement clear Restore Purchases and conform pricing displays with subscription guidelines.

### Category: Apple Developer Program License Agreement
- **Impact**: Updates affecting the 'Apple Developer Program License Agreement' guideline parameters.
  - **Migration Tasks**:
    - [ ] Review implementation details and metadata for Apple Developer Program License Agreement.

### Category: DMA compliance changes
- **Impact**: Updates affecting the 'DMA compliance changes' guideline parameters.
  - **Migration Tasks**:
    - [ ] Review implementation details and metadata for DMA compliance changes.

<!-- APPLE_POLICY_MONITOR_END -->