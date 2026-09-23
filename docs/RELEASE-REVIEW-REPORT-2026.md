# Release Readiness Compliance Report

Target Directory: /app
Overall Compliance Status: BLOCKED

## Executive Summary
The release is currently BLOCKED due to one or more critical compliance issues that must be resolved before submitting to the platforms.

## Compliance Summary Table (13 Required Areas)

| Area | Status | Risks Found | Recommended Reviewers |
| --- | --- | --- | --- |
| Apple requirements | BLOCKED | 5 | Mobile Tech Lead, iOS Platform Architect |
| Google Play requirements | ADVISORY | 1 | Mobile Tech Lead, Android Platform Architect |
| Web requirements | PASSED | 0 | Frontend Technical Lead, Web Architect |
| Privacy | ADVISORY | 1 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| Security | PASSED | 0 | Product Security Engineering Team, DevSecOps Lead |
| Accessibility | PASSED | 0 | Frontend QA Team, Accessibility Specialist |
| AI regulations | ADVISORY | 1 | AI Ethics and Governance Committee, Lead AI Architect |
| Store metadata | ADVISORY | 4 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| Permissions | PASSED | 0 | Lead Developer, Mobile Platform Leads |
| Legal documentation | ADVISORY | 1 | Legal Counsel (Commercial/IP), Compliance Officer |
| SDK compatibility | PASSED | 0 | Lead Mobile Developer, Architecture Review Board |
| Deprecated APIs | PASSED | 0 | Lead Developer, Tech Debt/Platform Team |
| Platform announcements | PASSED | 0 | Lead Developer, Mobile Release Manager |

## App Store & Google Play Review Domains (15 Verification Areas)

| Domain | Status | Risks Found | Recommended Reviewers |
| --- | --- | --- | --- |
| permissions | PASSED | 0 | Lead Developer, Mobile Platform Leads |
| privacy disclosures | ADVISORY | 1 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| screenshots | ADVISORY | 1 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| metadata | ADVISORY | 4 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| age rating | BLOCKED | 1 | Compliance Officer, Product Safety Lead |
| AI disclosures | PASSED | 0 | AI Ethics and Governance Committee, Lead AI Architect |
| subscription disclosures | ADVISORY | 1 | Legal Counsel (Commercial/IP), Monetization Lead |
| payment compliance | ADVISORY | 2 | Payments Lead, Finance & Legal Counsel |
| accessibility | PASSED | 0 | Frontend QA Team, Accessibility Specialist |
| legal documents | ADVISORY | 1 | Legal Counsel (Commercial/IP), Compliance Officer |
| support URL | ADVISORY | 1 | Customer Support Lead, Product Marketing Manager |
| privacy policy | ADVISORY | 1 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| terms of service | ADVISORY | 1 | Legal Counsel (Commercial/IP), Compliance Officer |
| export compliance | PASSED | 0 | Trade Compliance Specialist, Legal Counsel |
| encryption declarations | PASSED | 0 | Product Security Engineering Team, Cryptography Specialist |

## Detailed Compliance Analysis (13 Required Areas)

### 1. Apple requirements
- Status: BLOCKED
- Recommended Reviewers: Mobile Tech Lead, iOS Platform Architect

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### 2. Google Play requirements
- Status: ADVISORY
- Recommended Reviewers: Mobile Tech Lead, Android Platform Architect

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### 3. Web requirements
- Status: PASSED
- Recommended Reviewers: Frontend Technical Lead, Web Architect

No outstanding risks found for this area.

### 4. Privacy
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### 5. Security
- Status: PASSED
- Recommended Reviewers: Product Security Engineering Team, DevSecOps Lead

No outstanding risks found for this area.

### 6. Accessibility
- Status: PASSED
- Recommended Reviewers: Frontend QA Team, Accessibility Specialist

No outstanding risks found for this area.

### 7. AI regulations
- Status: ADVISORY
- Recommended Reviewers: AI Ethics and Governance Committee, Lead AI Architect

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### 8. Store metadata
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### 9. Permissions
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Platform Leads

No outstanding risks found for this area.

### 10. Legal documentation
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### 11. SDK compatibility
- Status: PASSED
- Recommended Reviewers: Lead Mobile Developer, Architecture Review Board

No outstanding risks found for this area.

### 12. Deprecated APIs
- Status: PASSED
- Recommended Reviewers: Lead Developer, Tech Debt/Platform Team

No outstanding risks found for this area.

### 13. Platform announcements
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Release Manager

No outstanding risks found for this area.

## Detailed Analysis of 15 Verification Review Domains

### 1. permissions
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Platform Leads

No outstanding risks found for domain: permissions.

### 2. privacy disclosures
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### 3. screenshots
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |

### 4. metadata
- Status: ADVISORY
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/REGULATORY-TIMELINE.md<br>docs/PLATFORM-MECHANICS-2026.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>... and 2 more files |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### 5. age rating
- Status: BLOCKED
- Recommended Reviewers: Compliance Officer, Product Safety Lead

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |

### 6. AI disclosures
- Status: PASSED
- Recommended Reviewers: AI Ethics and Governance Committee, Lead AI Architect

No outstanding risks found for domain: AI disclosures.

### 7. subscription disclosures
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Monetization Lead

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### 8. payment compliance
- Status: ADVISORY
- Recommended Reviewers: Payments Lead, Finance & Legal Counsel

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### 9. accessibility
- Status: PASSED
- Recommended Reviewers: Frontend QA Team, Accessibility Specialist

No outstanding risks found for domain: accessibility.

### 10. legal documents
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 6 more files |

### 11. support URL
- Status: ADVISORY
- Recommended Reviewers: Customer Support Lead, Product Marketing Manager

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |

### 12. privacy policy
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### 13. terms of service
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### 14. export compliance
- Status: PASSED
- Recommended Reviewers: Trade Compliance Specialist, Legal Counsel

No outstanding risks found for domain: export compliance.

### 15. encryption declarations
- Status: PASSED
- Recommended Reviewers: Product Security Engineering Team, Cryptography Specialist

No outstanding risks found for domain: encryption declarations.
