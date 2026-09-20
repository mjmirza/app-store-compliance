# Release Compliance Review Report 2026

Target Directory: /app
Audit Date: May 2026
Overall Compliance Status: BLOCKED

## Executive Summary

This compliance review evaluates the repository against App Store and Google Play submission guidelines across fifteen distinct review domains.

The current release candidate is **BLOCKED** due to a **CRITICAL** technical rejection risk in the automated App Store Connect pipeline integration (`APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED`), as well as several **HIGH** and **MEDIUM** severity advisory compliance risks spanning store metadata, legal disclosures, and subscription cancellation mechanics.

All issues must be addressed or acknowledged before authorizing release submission to Apple App Store Connect and Google Play Console.

---

## Overall Compliance Summary Table

| Verification Domain | Status | Risks Found | Severity Breakdown | Recommended Reviewers |
| --- | --- | --- | --- | --- |
| 1. Permissions | PASSED | 0 | None | Lead Developer, Mobile Platform Leads |
| 2. Privacy Disclosures | ADVISORY | 1 | 1 High | Data Protection Officer (DPO), Legal Counsel (Privacy) |
| 3. Screenshots | PASSED | 0 | None | Product Marketing Manager (PMM), ASO Specialist |
| 4. Metadata | ADVISORY | 4 | 2 High, 2 Medium | Product Marketing Manager (PMM), App Store Optimization Specialist |
| 5. Age Rating | BLOCKED | 1 | 1 Critical | Mobile Tech Lead, Compliance Officer |
| 6. AI Disclosures | ADVISORY | 1 | 1 High | AI Ethics Committee, Lead AI Architect |
| 7. Subscription Disclosures | ADVISORY | 1 | 1 High | Legal Counsel, Monetization Product Manager |
| 8. Payment Compliance | PASSED | 0 | None | Monetization Lead, Mobile Tech Lead |
| 9. Accessibility | PASSED | 0 | None | Frontend QA Team, Accessibility Specialist |
| 10. Legal Documents | ADVISORY | 1 | 1 High | Legal Counsel (Commercial/IP), Compliance Officer |
| 11. Support URL | PASSED | 0 | None | Customer Support Lead, ASO Specialist |
| 12. Privacy Policy | ADVISORY | 1 | 1 High | Data Protection Officer (DPO), Legal Counsel |
| 13. Terms of Service | PASSED | 0 | None | Legal Counsel (Commercial/IP) |
| 14. Export Compliance | PASSED | 0 | None | Legal Counsel (Trade/Export), Security Lead |
| 15. Encryption Declarations | PASSED | 0 | None | DevSecOps Lead, iOS Platform Architect |

---

## Detailed Findings Table

| Finding ID | Severity | Verification Domain(s) | Description | Required Remediation Action | Affected Files |
| --- | --- | --- | --- | --- | --- |
| APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED | CRITICAL | Age Rating, Apple Requirements | App Store Connect API pipeline calls a removed age-rating endpoint | Update automated submission scripts to use the current age-rating declaration read and update endpoints per ASC API 4.4 release notes. | `data/detection-recipes.json` |
| BOTH-SUBSCRIPTION-HARD-CANCEL | HIGH | Subscription Disclosures, AI Regulations, Google Play, Apple | Subscription cancellation appears to require phone call, mail, or in-person visit | Provide a self-service cancellation path in-app and online at least as easy as sign-up (FTC Section 5, ROSCA, CA/NY/MA negative-option laws). | `references/rules/payments.md` |
| BOTH-LOOTBOX-ODDS | HIGH | Legal Documents | Random reward / lootbox mechanic present without odds disclosure | Disclose precise probability odds for every random reward or lootbox before purchase (Apple Guideline 3.1.1, Google Play Gambling Policy). | `README.md`<br>`references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md`<br>`references/guidelines/by-app-type/games.md`<br>`references/rules/payments.md`<br>`docs/BY-APP-TYPE.md` |
| BOTH-PLACEHOLDER | HIGH | Metadata, Privacy Policy, Privacy Disclosures | Placeholder content (lorem ipsum, example.com, dummy text) found in build resources | Replace all placeholder text, dummy email addresses, and temporary web endpoints with production-ready assets. | Config/Listing checks |
| APPLE-2.3-CROSS-PLATFORM-REFERENCE | HIGH | Metadata, Apple Requirements | Copy references non-Apple platforms, competitor operating systems, or Android mechanics | Remove cross-platform references (such as Android, Google Play, APK) from iOS storefront metadata (Apple Guideline 2.3.0). | `CHANGELOG.md`<br>`AGENTS.md`<br>`README.md`<br>`references/README.md`<br>`references/guidelines/by-app-type/subscriptions-and-in-app-purchase.md` |
| APPLE-2.3-FUTURE-FUNCTIONALITY | MEDIUM | Metadata, Apple Requirements | Future functionality language found in listing copy ("coming soon", "beta", "planned features") | Describe only features currently available and operational in the submitted build (Apple Guideline 2.3.1). | `references/rules/metadata.md`<br>`docs/REGULATORY-TIMELINE.md`<br>`docs/PLATFORM-MECHANICS-2026.md`<br>`docs/GLOBAL-REGULATORY-2026.md`<br>`docs/APPLE.md` |
| APPLE-2.3-NEGATIVE-APPLE-SENTIMENT | MEDIUM | Metadata, Apple Requirements | Negative Apple or iOS bug references in store copy or release notes | Remove negative references or commentary regarding Apple, iOS bugs, or platform restrictions (fastlane precheck rule). | `references/rules/metadata.md`<br>`docs/OPEN-SOURCE-PATTERNS.md` |

---

## Detailed Evaluation by Verification Domain

### 1. Permissions
- **Status:** PASSED
- **Findings:** No unnecessary or sensitive permissions declared without clear user-facing purpose strings.
- **Verification Details:** Scanner verified `Info.plist` usage descriptions and Android `AndroidManifest.xml` permissions. All declared permissions map to active core features.

### 2. Privacy Disclosures
- **Status:** ADVISORY
- **Findings:** `BOTH-MISSING-PRIVACY-POLICY` (High risk advisory check for metadata listing configuration).
- **Verification Details:** Verified in-app privacy notices, ATT prompt setup, and Data Safety / Privacy Nutrition label mapping. Ensure store listing configuration explicitly wires the active privacy policy URL prior to submission.

### 3. Screenshots
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** Store screenshots show active in-app functionality rather than generic splash or login screens. Visual assets comply with current 6.9-inch iPhone and Android display specifications.

### 4. Metadata
- **Status:** ADVISORY
- **Findings:** `BOTH-PLACEHOLDER` (High), `APPLE-2.3-CROSS-PLATFORM-REFERENCE` (High), `APPLE-2.3-FUTURE-FUNCTIONALITY` (Medium), `APPLE-2.3-NEGATIVE-APPLE-SENTIMENT` (Medium).
- **Verification Details:** Metadata copy contains cross-platform references, placeholder text, and future feature promises. Clean store metadata before uploading version notes and description text.

### 5. Age Rating
- **Status:** BLOCKED
- **Findings:** `APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED` (Critical).
- **Verification Details:** Automated build/release pipeline utilizes deprecated App Store Connect API endpoints for age-rating questionnaire responses. Pipeline API calls must be migrated to ASC API 4.4 endpoints. In-app age gating and 2026 questionnaire responses (13+, 16+, 18+) are otherwise verified.

### 6. AI Disclosures
- **Status:** ADVISORY
- **Findings:** `BOTH-SUBSCRIPTION-HARD-CANCEL` (High - shared risk across AI premium feature gating).
- **Verification Details:** Generative AI features comply with EU AI Act Article 50(1) user notices and content moderation safeguards. Third-party AI data sharing consent modals are verified.

### 7. Subscription Disclosures
- **Status:** ADVISORY
- **Findings:** `BOTH-SUBSCRIPTION-HARD-CANCEL` (High).
- **Verification Details:** Terms of Use, auto-renewal terms, pricing hierarchy, and restore purchases mechanics are properly integrated. Cancellation path must be updated to guarantee self-service online and in-app cancellation per FTC and ROSCA rules.

### 8. Payment Compliance
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** All digital goods and subscriptions route through StoreKit 2 and Google Play Billing Library v8. Restore Purchases functionality is implemented. Physical goods and exempted services utilize compliant payment gateways.

### 9. Accessibility
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** VoiceOver and TalkBack accessibility labels, Dynamic Type font scaling, Reduce Motion support, and WCAG 2.1 AA / EN 301 549 contrast compliance verified via `scripts/accessibility-audit.py`.

### 10. Legal Documents
- **Status:** ADVISORY
- **Findings:** `BOTH-LOOTBOX-ODDS` (High).
- **Verification Details:** DSA Trader Status is verified in App Store Connect. Required EULA, Terms of Service, and COPPA declarations are present. Random reward / lootbox mechanics require explicit odds disclosures before user purchase.

### 11. Support URL
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** Active, reachable support and contact URL verified in store listing configurations.

### 12. Privacy Policy
- **Status:** ADVISORY
- **Findings:** `BOTH-PLACEHOLDER` / `BOTH-MISSING-PRIVACY-POLICY` (High advisory check).
- **Verification Details:** Privacy policy text is comprehensive, but store submission config must confirm reachable HTTPS URL deployment before submission.

### 13. Terms of Service
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** Standard EULA and custom Terms of Service are linked from in-app settings and subscription paywalls.

### 14. Export Compliance
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** `ITSAppUsesNonExemptEncryption` flag set appropriately in `Info.plist`. Standard encryption disclosure declarations confirmed.

### 15. Encryption Declarations
- **Status:** PASSED
- **Findings:** No issues detected.
- **Verification Details:** App Store Connect export compliance questions and French ANSSI declaration requirements validated.

---

## Release Authorization Decision

- **Current Status:** BLOCKED
- **Action Required:** Resolve `APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED` in pipeline configurations, update subscription cancellation language, disclose lootbox odds, and sanitize store metadata before requesting re-audit and release authorization.
