# Release Readiness Compliance Report

Target Directory: /app
Overall Compliance Status: BLOCKED

## Executive Summary
The release is currently BLOCKED due to one or more critical compliance issues that must be resolved before submitting to the platforms.

## 15 App Store and Google Play Review Domains

| Review Domain | Status | Risks Found | Mapped Scripts | Recommended Reviewers |
| --- | --- | --- | --- | --- |
| permissions | PASSED | 0 | agent-os/hooks/app-store-compliance-guard.sh, scripts/monitor-android.py | Lead Developer, Mobile Platform Leads |
| privacy disclosures | PASSED | 0 | scripts/monitor-privacy.py, scripts/validate-privacy-manifest.py | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| screenshots | ADVISORY | 1 | scripts/metadata-audit.py | Product Marketing Manager (PMM), Design Lead |
| metadata | ADVISORY | 4 | scripts/metadata-audit.py, scripts/monitor.py | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| age rating | BLOCKED | 1 | scripts/deadline-checker.py, agent-os/hooks/app-store-compliance-guard.sh | Trust & Safety Lead, Legal Counsel |
| AI disclosures | PASSED | 0 | scripts/monitor-ai-policy.py, scripts/monitor-regulatory.py | AI Ethics and Governance Committee, Lead AI Architect |
| subscription disclosures | ADVISORY | 1 | agent-os/hooks/app-store-compliance-guard.sh | Growth Product Manager, Legal Counsel (Commercial) |
| payment compliance | ADVISORY | 1 | agent-os/hooks/app-store-compliance-guard.sh | Payments & Billing Engineering Lead, Finance Lead |
| accessibility | PASSED | 0 | scripts/accessibility-audit.py | Frontend QA Team, Accessibility Specialist |
| legal documents | ADVISORY | 2 | scripts/monitor-regulatory.py, scripts/validate.py | Legal Counsel (Commercial/IP), Compliance Officer |
| support URL | ADVISORY | 1 | scripts/metadata-audit.py, scripts/verify-citations.py | Customer Support Operations Lead, Technical Writer |
| privacy policy | ADVISORY | 1 | scripts/monitor-privacy.py, scripts/metadata-audit.py | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| terms of service | ADVISORY | 1 | scripts/monitor-regulatory.py, agent-os/hooks/app-store-compliance-guard.sh | Legal Counsel (Commercial/IP), Compliance Officer |
| export compliance | PASSED | 0 | agent-os/hooks/app-store-compliance-guard.sh | Trade Compliance Officer, Product Security Lead |
| encryption declarations | PASSED | 0 | scripts/monitor-security.py, agent-os/hooks/app-store-compliance-guard.sh | Product Security Engineering Team, DevSecOps Lead |

## 13 Required Compliance Areas Summary

| Compliance Area | Status | Risks Found | Recommended Reviewers |
| --- | --- | --- | --- |
| Apple requirements | BLOCKED | 5 | Mobile Tech Lead, iOS Platform Architect |
| Google Play requirements | ADVISORY | 1 | Mobile Tech Lead, Android Platform Architect |
| Web requirements | PASSED | 0 | Frontend Technical Lead, Web Architect |
| Privacy | ADVISORY | 1 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| Security | PASSED | 0 | Product Security Engineering Team, DevSecOps Lead |
| Accessibility | PASSED | 0 | Frontend QA Team, Accessibility Specialist |
| AI regulations | PASSED | 0 | AI Ethics and Governance Committee, Lead AI Architect |
| Store metadata | ADVISORY | 4 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| Permissions | PASSED | 0 | Lead Developer, Mobile Platform Leads |
| Legal documentation | ADVISORY | 2 | Legal Counsel (Commercial/IP), Compliance Officer |
| SDK compatibility | PASSED | 0 | Lead Mobile Developer, Architecture Review Board |
| Deprecated APIs | PASSED | 0 | Lead Developer, Tech Debt/Platform Team |
| Platform announcements | BLOCKED | 1 | Lead Developer, Mobile Release Manager |

## Detailed Compliance Analysis: 15 Review Domains

### Domain 1: Permissions
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Platform Leads
- Mapped Scripts: agent-os/hooks/app-store-compliance-guard.sh, scripts/monitor-android.py

No outstanding risks found for this domain.

### Domain 2: Privacy Disclosures
- Status: PASSED
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)
- Mapped Scripts: scripts/monitor-privacy.py, scripts/validate-privacy-manifest.py

No outstanding risks found for this domain.

### Domain 3: Screenshots
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), Design Lead
- Mapped Scripts: scripts/metadata-audit.py

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |

### Domain 4: Metadata
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist
- Mapped Scripts: scripts/metadata-audit.py, scripts/monitor.py

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### Domain 5: Age Rating
- Status: BLOCKED
- Recommended Reviewers: Trust & Safety Lead, Legal Counsel
- Mapped Scripts: scripts/deadline-checker.py, agent-os/hooks/app-store-compliance-guard.sh

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |

### Domain 6: Ai Disclosures
- Status: PASSED
- Recommended Reviewers: AI Ethics and Governance Committee, Lead AI Architect
- Mapped Scripts: scripts/monitor-ai-policy.py, scripts/monitor-regulatory.py

No outstanding risks found for this domain.

### Domain 7: Subscription Disclosures
- Status: ADVISORY
- Recommended Reviewers: Growth Product Manager, Legal Counsel (Commercial)
- Mapped Scripts: agent-os/hooks/app-store-compliance-guard.sh

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### Domain 8: Payment Compliance
- Status: ADVISORY
- Recommended Reviewers: Payments & Billing Engineering Lead, Finance Lead
- Mapped Scripts: agent-os/hooks/app-store-compliance-guard.sh

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### Domain 9: Accessibility
- Status: PASSED
- Recommended Reviewers: Frontend QA Team, Accessibility Specialist
- Mapped Scripts: scripts/accessibility-audit.py

No outstanding risks found for this domain.

### Domain 10: Legal Documents
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer
- Mapped Scripts: scripts/monitor-regulatory.py, scripts/validate.py

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### Domain 11: Support Url
- Status: ADVISORY
- Recommended Reviewers: Customer Support Operations Lead, Technical Writer
- Mapped Scripts: scripts/metadata-audit.py, scripts/verify-citations.py

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |

### Domain 12: Privacy Policy
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)
- Mapped Scripts: scripts/monitor-privacy.py, scripts/metadata-audit.py

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### Domain 13: Terms Of Service
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer
- Mapped Scripts: scripts/monitor-regulatory.py, agent-os/hooks/app-store-compliance-guard.sh

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### Domain 14: Export Compliance
- Status: PASSED
- Recommended Reviewers: Trade Compliance Officer, Product Security Lead
- Mapped Scripts: agent-os/hooks/app-store-compliance-guard.sh

No outstanding risks found for this domain.

### Domain 15: Encryption Declarations
- Status: PASSED
- Recommended Reviewers: Product Security Engineering Team, DevSecOps Lead
- Mapped Scripts: scripts/monitor-security.py, agent-os/hooks/app-store-compliance-guard.sh

No outstanding risks found for this domain.

## Detailed Compliance Analysis: 13 Compliance Areas

### Area 1: Apple requirements
- Status: BLOCKED
- Recommended Reviewers: Mobile Tech Lead, iOS Platform Architect

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### Area 2: Google Play requirements
- Status: ADVISORY
- Recommended Reviewers: Mobile Tech Lead, Android Platform Architect

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### Area 3: Web requirements
- Status: PASSED
- Recommended Reviewers: Frontend Technical Lead, Web Architect

No outstanding risks found for this area.

### Area 4: Privacy
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### Area 5: Security
- Status: PASSED
- Recommended Reviewers: Product Security Engineering Team, DevSecOps Lead

No outstanding risks found for this area.

### Area 6: Accessibility
- Status: PASSED
- Recommended Reviewers: Frontend QA Team, Accessibility Specialist

No outstanding risks found for this area.

### Area 7: AI regulations
- Status: PASSED
- Recommended Reviewers: AI Ethics and Governance Committee, Lead AI Architect

No outstanding risks found for this area.

### Area 8: Store metadata
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### Area 9: Permissions
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Platform Leads

No outstanding risks found for this area.

### Area 10: Legal documentation
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### Area 11: SDK compatibility
- Status: PASSED
- Recommended Reviewers: Lead Mobile Developer, Architecture Review Board

No outstanding risks found for this area.

### Area 12: Deprecated APIs
- Status: PASSED
- Recommended Reviewers: Lead Developer, Tech Debt/Platform Team

No outstanding risks found for this area.

### Area 13: Platform announcements
- Status: BLOCKED
- Recommended Reviewers: Lead Developer, Mobile Release Manager

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |
