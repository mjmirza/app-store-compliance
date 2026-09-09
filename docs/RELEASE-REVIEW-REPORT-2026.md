# Release Readiness Compliance Report

Target Directory: /app
Overall Compliance Status: BLOCKED

## Executive Summary
The release is currently BLOCKED due to one or more critical compliance issues that must be resolved before submitting to the platforms.

## Compliance Summary Table

| Area | Status | Risks Found | Recommended Reviewers |
| --- | --- | --- | --- |
| permissions | PASSED | 0 | Lead Developer, Mobile Platform Leads |
| privacy disclosures | PASSED | 0 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| screenshots | PASSED | 0 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| metadata | BLOCKED | 28 | Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist |
| age rating | BLOCKED | 2 | Compliance Officer, Product Manager |
| AI disclosures | PASSED | 0 | AI Ethics and Governance Committee, Lead AI Architect |
| subscription disclosures | ADVISORY | 1 | Growth Lead, Legal Counsel (Commercial) |
| payment compliance | PASSED | 0 | Mobile Tech Lead, Payment Integration Specialist |
| accessibility | PASSED | 0 | Frontend QA Team, Accessibility Specialist |
| legal documents | ADVISORY | 1 | Legal Counsel (Commercial/IP), Compliance Officer |
| support URL | PASSED | 0 | Customer Support Lead, Web Master |
| privacy policy | ADVISORY | 1 | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| terms of service | PASSED | 0 | Legal Counsel (Commercial/IP) |
| export compliance | PASSED | 0 | Trade Compliance Officer, Legal Counsel |
| encryption declarations | PASSED | 0 | Security Lead, iOS Platform Architect |

## Detailed Compliance Analysis

### 1. permissions
- Status: PASSED
- Recommended Reviewers: Lead Developer, Mobile Platform Leads

No outstanding risks found for this area.

### 2. privacy disclosures
- Status: PASSED
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

No outstanding risks found for this area.

### 3. screenshots
- Status: PASSED
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

No outstanding risks found for this area.

### 4. metadata
- Status: BLOCKED
- Recommended Reviewers: Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| EU | HIGH | AI Act, Regulation (EU) 2024/1689 (mandatory 2025-02-02) absorbed into docs/EU-REGULATORY-2026.md section 1.3, references/guidelines/by-app-type/ai-and-generative-apps.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| European | HIGH | Accessibility Act (EAA), Directive (EU) 2019/882 (mandatory 2025-06-28) absorbed into docs/EU-REGULATORY-2026.md section 4, references/rules/design.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| FTC | HIGH | Health Breach Notification Rule, 16 CFR Part 318 (mandatory 2024-06-25) absorbed into docs/GLOBAL-REGULATORY-2026.md section 2.6, references/guidelines/by-app-type/health-fitness-and-medical.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Texas | CRITICAL | SB 2420 (App Store Accountability Act) (mandatory 2026-01-01) absorbed into docs/GLOBAL-REGULATORY-2026.md section 1, section 2.2, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| California | HIGH | CPRA (CPPA 2026 Regulations) (mandatory 2026-01-01) absorbed into docs/GLOBAL-REGULATORY-2026.md section 2.4, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Biometric | CRITICAL | Information Privacy Act (BIPA), 740 ILCS 14 (mandatory 2008-06-01) absorbed into docs/GLOBAL-REGULATORY-2026.md section 2.6, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| UK | CRITICAL | Online Safety Act 2023 (mandatory 2025-07-25) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.1, references/rules/safety.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| ICO | HIGH | Age Appropriate Design Code (Children's Code) (mandatory 2021-09-02) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.1, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Online | CRITICAL | Safety Amendment (Social Media Minimum Age) Act 2024 (mandatory 2025-12-10) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.2, references/rules/safety.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Digital | CRITICAL | ECA (Law 15,211/2025) (mandatory 2026-03-17) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.3, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Telecommunications | HIGH | Business Act (mandatory 2022-03-15) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.5, references/rules/payments.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| IMDA | CRITICAL | Code of Practice for Online Safety for App Distribution Services (mandatory 2026-04-01) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.7, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Mobile | CRITICAL | App Filing with the MIIT (ICP Extension) (mandatory 2024-03-31) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.9, references/rules/metadata.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Apple | CRITICAL | App Store Review Guidelines (Guideline 2.3.6) (mandatory 2026-01-31) absorbed into docs/EU-REGULATORY-2026.md section 6, references/rules/metadata.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Google | CRITICAL | Play Target API Requirement (mandatory 2025-08-31) absorbed into docs/PLATFORM-MECHANICS-2026.md section 2.5, references/rules/android.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| e-Evidence | HIGH | Package, Regulation (EU) 2023/1543 (mandatory 2026-08-18) absorbed into docs/EU-REGULATORY-2026.md section 5, references/rules/privacy.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Distance | HIGH | Marketing of Financial Services, Directive (EU) 2023/2673 (mandatory 2026-06-19) absorbed into docs/EU-REGULATORY-2026.md section 5, references/rules/payments.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| General | HIGH | Product Safety Regulation (GPSR), Regulation (EU) 2023/988 (mandatory 2024-12-13) absorbed into docs/REGULATORY-GAP-REPORT-2026.md section 1, references/rules/safety.md | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Play | HIGH | Catalog Access Program (Play Console Help answers 17117200 and 15582165) (mandatory 2026-07-22) absorbed into GOOGLE-PLAY-APP-REGISTRATION-MISSING | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| App | CRITICAL | Store Connect social media capability declaration (Apple Developer news 0d2gpmml and tlur8uvi) (mandatory 2026-09-01) absorbed into APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Data | MEDIUM | (Use and Access) Act 2025 section 103 and Schedule 10, commenced by SI 2026/82 regulation 3 (mandatory 2026-06-19) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.1 | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Interim | CRITICAL | Measures for AI Anthropomorphic Interactive Services, CAC Order No. 21 (mandatory 2026-07-15) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.9 | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| Decreto | CRITICAL | n. 12.880 of 18 March 2026, Articles 21 and 25, regulating the Digital ECA (mandatory 2026-03-18) absorbed into docs/GLOBAL-REGULATORY-2026.md section 3.3 | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| TAKE | CRITICAL | IT DOWN Act, Pub. L. 119-12 (mandatory 2026-05-19) absorbed into docs/GLOBAL-REGULATORY-2026.md section 2.6 | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| BOTH-PLACEHOLDER | HIGH | Placeholder content (lorem ipsum, example.com, dummy text) found in sources | Replace placeholder text and assets with real content. | None detected (Config/Listing check) |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Future functionality language found | Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1). | references/rules/metadata.md<br>docs/GLOBAL-REGULATORY-2026.md<br>docs/APPLE.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Negative Apple or iOS bug reference in copy | Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment). | references/rules/metadata.md<br>docs/RELEASE-REVIEW-REPORT-2026.md<br>docs/OPEN-SOURCE-PATTERNS.md |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH |  | Refer to guidelines for remediation. | CHANGELOG.md<br>AGENTS.md<br>README.md<br>references/README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>... and 29 more files |

### 5. age rating
- Status: BLOCKED
- Recommended Reviewers: Compliance Officer, Product Manager

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| Age-Restricted | CRITICAL | Content, Families, and Child Safety Standards policy expansion to anonymous and random chat apps (Play Console Help answers 17036597, 17122218, 14747720) (mandatory 2026-08-26) absorbed into GOOGLE-ANON-CHAT-MINOR-BLOCK | Refer to guidelines for remediation. | None detected (Config/Listing check) |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Pipeline calls a removed App Store Connect API age-rating endpoint | Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes). | data/detection-recipes.json |

### 6. AI disclosures
- Status: PASSED
- Recommended Reviewers: AI Ethics and Governance Committee, Lead AI Architect

No outstanding risks found for this area.

### 7. subscription disclosures
- Status: ADVISORY
- Recommended Reviewers: Growth Lead, Legal Counsel (Commercial)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription cancellation appears to require a phone call, mail, or an in-person visit | Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws). | references/rules/payments.md |

### 8. payment compliance
- Status: PASSED
- Recommended Reviewers: Mobile Tech Lead, Payment Integration Specialist

No outstanding risks found for this area.

### 9. accessibility
- Status: PASSED
- Recommended Reviewers: Frontend QA Team, Accessibility Specialist

No outstanding risks found for this area.

### 10. legal documents
- Status: ADVISORY
- Recommended Reviewers: Legal Counsel (Commercial/IP), Compliance Officer

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-LOOTBOX-ODDS | HIGH | Random reward mechanic present | Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling). | README.md<br>references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md<br>references/guidelines/by-app-type/games.md<br>references/rules/payments.md<br>docs/BY-APP-TYPE.md<br>... and 7 more files |

### 11. support URL
- Status: PASSED
- Recommended Reviewers: Customer Support Lead, Web Master

No outstanding risks found for this area.

### 12. privacy policy
- Status: ADVISORY
- Recommended Reviewers: Data Protection Officer (DPO), Legal Counsel (Privacy)

| Finding ID | Severity | Description | Required Action | Affected Files |
| --- | --- | --- | --- | --- |
| BOTH-MISSING-PRIVACY-POLICY | HIGH |  | Refer to guidelines for remediation. | None detected (Config/Listing check) |

### 13. terms of service
- Status: PASSED
- Recommended Reviewers: Legal Counsel (Commercial/IP)

No outstanding risks found for this area.

### 14. export compliance
- Status: PASSED
- Recommended Reviewers: Trade Compliance Officer, Legal Counsel

No outstanding risks found for this area.

### 15. encryption declarations
- Status: PASSED
- Recommended Reviewers: Security Lead, iOS Platform Architect

No outstanding risks found for this area.
