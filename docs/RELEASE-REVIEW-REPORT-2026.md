# App Store and Google Play Pre-Release Review Report (2026)

Target Repository: /app
Overall Release Authorization Status: BLOCKED

## Executive Summary
This report evaluates the repository against all fifteen required App Store and Google Play review domains prior to release authorization. Every issue identified across active scripts, static rejection pattern definitions, and metadata audits is documented below.

## 15-Domain Compliance Summary

| Domain | Status | Total Findings | Critical / High / Medium / Low | Mapped Audit Script |
| --- | --- | --- | --- | --- |
| Permissions | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Privacy Disclosures | ADVISORY (HIGH) | 1 | 0 / 1 / 0 / 0 | scripts/metadata-audit.py |
| Screenshots | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Metadata | ADVISORY (HIGH) | 4 | 0 / 2 / 2 / 0 | agent-os/hooks/app-store-compliance-guard.sh |
| Age Rating | BLOCKED | 1 | 1 / 0 / 0 / 0 | agent-os/hooks/app-store-compliance-guard.sh |
| AI Disclosures | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Subscription Disclosures | ADVISORY (HIGH) | 1 | 0 / 1 / 0 / 0 | agent-os/hooks/app-store-compliance-guard.sh |
| Payment Compliance | ADVISORY (HIGH) | 2 | 0 / 2 / 0 / 0 | agent-os/hooks/app-store-compliance-guard.sh |
| Accessibility | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Legal Documents | ADVISORY (HIGH) | 1 | 0 / 1 / 0 / 0 | agent-os/hooks/app-store-compliance-guard.sh |
| Support URL | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Privacy Policy | ADVISORY (HIGH) | 1 | 0 / 1 / 0 / 0 | scripts/metadata-audit.py |
| Terms of Service | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Export Compliance | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |
| Encryption Declarations | PASSED | 0 | 0 / 0 / 0 / 0 | scripts/release-audit.py |

## Severity-Ranked Findings Table

| Finding ID | Severity | Domain(s) | Description | Required Action | Mapped Script / Verification Source |
| --- | --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Age Rating | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | agent-os/hooks/app-store-compliance-guard.sh |
| BOTH-PLACEHOLDER | HIGH | Metadata | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | agent-os/hooks/app-store-compliance-guard.sh |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription Disclosures, Payment Compliance | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | agent-os/hooks/app-store-compliance-guard.sh |
| BOTH-LOOTBOX-ODDS | HIGH | Payment Compliance, Legal Documents | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | agent-os/hooks/app-store-compliance-guard.sh |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH | Metadata |  | Refer to platform guidelines for remediation. | scripts/metadata-audit.py |
| BOTH-MISSING-PRIVACY-POLICY | HIGH | Privacy Policy, Privacy Disclosures |  | Refer to platform guidelines for remediation. | scripts/metadata-audit.py |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Metadata | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | agent-os/hooks/app-store-compliance-guard.sh |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Metadata | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | agent-os/hooks/app-store-compliance-guard.sh |

## Domain-by-Domain Pre-Release Evaluation

### 1. Permissions
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Permissions.

### 2. Privacy Disclosures
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-MISSING-PRIVACY-POLICY:
  Action required: Refer to platform guidelines for remediation.
  Audit script: scripts/metadata-audit.py

### 3. Screenshots
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Screenshots.

### 4. Metadata
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-PLACEHOLDER: Placeholder content (lorem ipsum, example.com, dummy text) found in sources
  Action required: Replace placeholder text and assets with real content.
  Audit script: agent-os/hooks/app-store-compliance-guard.sh
- [MEDIUM] APPLE-2.3-FUTURE-FUNCTIONALITY: Future functionality language found
  Action required: Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh
- [MEDIUM] APPLE-2.3-NEGATIVE-APPLE-SENTIMENT: Negative Apple or iOS bug reference in copy
  Action required: Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh
- [HIGH] APPLE-2.3-CROSS-PLATFORM-REFERENCE:
  Action required: Refer to platform guidelines for remediation.
  Audit script: scripts/metadata-audit.py

### 5. Age Rating
- Domain Status: BLOCKED
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [CRITICAL] APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED: Pipeline calls a removed App Store Connect API age-rating endpoint
  Action required: Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh

### 6. AI Disclosures
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for AI Disclosures.

### 7. Subscription Disclosures
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-SUBSCRIPTION-HARD-CANCEL: Subscription cancellation appears to require a phone call, mail, or an in-person visit
  Action required: Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh

### 8. Payment Compliance
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-SUBSCRIPTION-HARD-CANCEL: Subscription cancellation appears to require a phone call, mail, or an in-person visit
  Action required: Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh
- [HIGH] BOTH-LOOTBOX-ODDS: Random reward mechanic present
  Action required: Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh

### 9. Accessibility
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Accessibility.

### 10. Legal Documents
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-LOOTBOX-ODDS: Random reward mechanic present
  Action required: Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling).
  Audit script: agent-os/hooks/app-store-compliance-guard.sh

### 11. Support URL
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Support URL.

### 12. Privacy Policy
- Domain Status: ADVISORY
- Verification Method: Automated static scanner and rule validation

Specific findings for this domain:
- [HIGH] BOTH-MISSING-PRIVACY-POLICY:
  Action required: Refer to platform guidelines for remediation.
  Audit script: scripts/metadata-audit.py

### 13. Terms of Service
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Terms of Service.

### 14. Export Compliance
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Export Compliance.

### 15. Encryption Declarations
- Domain Status: PASSED
- Verification Method: Automated static scanner and rule validation

Verification completed. Zero blocking or advisory findings identified for Encryption Declarations.

## Pre-Release Decision & Next Steps

RELEASE STATUS: BLOCKED.
Critical compliance findings exist. The release build cannot be authorized for App Store or Google Play submission until all critical findings are remediated.
