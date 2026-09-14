# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major global and regional regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, Canada, South Korea, India, Singapore, and China, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight distinct gap categories:
1. Missing policy
2. Missing documentation
3. Missing code
4. Missing disclosure
5. Missing logging
6. Missing testing
7. Missing evidence
8. Missing audit trail

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere to the strict source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces Directive 2001/95/EC to address safety challenges in online marketplaces, digital products, and complex supply chains.

The GPSR applies to non-food consumer products placed on the EU market. For digital systems and e-commerce software, the GPSR mandates displaying product safety warnings, technical instructions, manufacturer and importer identity, and postal/electronic contact details on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The repository lacks a template General Product Safety Policy establishing EU Responsible Person designation and product safety classification rules.
- **Missing Documentation:** No developer guidance or checklists explain how to structure product detail pages to display manufacturer details and safety warnings under GPSR.
- **Missing Code:** Automated guard scripts and recipes lack patterns to detect missing GPSR safety metadata (`manufacturerInfo`, `safetyWarning`) in product models or UI components.
- **Missing Disclosure:** Interface templates omit required UI slots for displaying the manufacturer name, registered trademark, postal address, and electronic contact details under Article 19.
- **Missing Logging:** No database schemas or event definitions exist to log safety incidents, consumer complaints, or product recall notifications.
- **Missing Testing:** No automated UI unit or integration tests verify the dynamic display of manufacturer info and safety notices based on user geo-location.
- **Missing Evidence:** Lacks sample technical documentation files, risk assessment templates, or EU Responsible Person verification certificates.
- **Missing Audit Trail:** Lacks audit logging to track safety policy revisions, safety warning reviews, or corrective action executions.

### 1.3 Remediation and Action Plan
1. Add a written General Product Safety Policy template to `templates/`.
2. Update `data/rejection-patterns.json` with pattern `BOTH-GPSR-COMPLIANCE-MISSING`.
3. Provide UI code samples in `references/` demonstrating compliant product detail layouts.
4. Add automated checks verifying GPSR disclosure components prior to submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 (European Production and Preservation Orders) and Directive (EU) 2023/1544 (Legal Representatives). Enforcement begins on 18 August 2026.

Authorities can issue European Production Orders (EPOs) directly to service providers in the EU. Standard compliance requires data production within 10 days; emergency orders mandate production within a strict 8-hour window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Law Enforcement Response Policy establishing emergency escalation paths and legal validation protocols.
- **Missing Documentation:** Lacks operational runbooks detailing technical workflows for executing 10-day standard and 8-hour emergency production orders.
- **Missing Code:** Missing backend helper scripts and API handlers to extract, filter, format, and encrypt requested user datasets securely.
- **Missing Disclosure:** Public privacy policy templates do not explicitly inform EU users that data may be produced under Regulation (EU) 2023/1543.
- **Missing Logging:** Lacks dedicated schema definitions to log law enforcement request IDs, verification status, access timestamps, and data extraction scopes.
- **Missing Testing:** Lacks integration tests simulating rapid data extraction and packaging within the 8-hour emergency limit.
- **Missing Evidence:** Lacks verified mock templates of European Production Order Certificates (EPOC) and Preservation Order Certificates (EPOC-PR).
- **Missing Audit Trail:** Lacks an immutable, append-only audit trail capturing compliance officer actions during legal request processing.

### 2.3 Remediation and Action Plan
1. Publish a Law Enforcement Response Protocol template for EU service providers.
2. Build backend data export utilities supporting encrypted emergency payloads.
3. Integrate e-Evidence request logging schemas into sample server configurations.
4. Establish cryptographic audit trails for legal request fulfillment.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU, requiring a prominent "withdrawal button" or "withdrawal function" on online interfaces for distance consumer contracts (such as financial services and digital subscriptions).

Consumers have a statutory 14-day withdrawal right. The cancellation path must be direct, clear, and at least as simple as the signup process. Member States enforce these rules starting 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Contract Withdrawal & Revocation Policy defining statutory 14-day cancellation rules.
- **Missing Documentation:** Lacks UI/UX design specifications governing withdrawal button visibility, wording, and placement in account settings.
- **Missing Code:** App templates lack functional withdrawal button components, modal confirmation sheets, and instant cancellation handlers.
- **Missing Disclosure:** Onboarding checkout screens omit mandatory disclosures explaining the 14-day statutory right of withdrawal and revocation terms.
- **Missing Logging:** Lacks event logging mechanisms to capture withdrawal initiation timestamps, confirmation receipts, and refund requests.
- **Missing Testing:** Lacks UI automation tests confirming frictionless self-service cancellation without human intervention.
- **Missing Evidence:** Lacks standard confirmation receipt templates or proof-of-withdrawal records for consumer dispute defense.
- **Missing Audit Trail:** Lacks an immutable audit trail tracking subscription flow changes, cancellation interface updates, and refund rates.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Implement self-service withdrawal button components in account management UI views.
3. Include automated UI test scripts validating zero-friction cancellation flows.
4. Add backend database logging for contract revocation events.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977 / Act 185, Alabama HB 161) regulate minor access to mobile apps, digital purchases, and updates.

Developers must query declared age categories (Apple Declared Age Range API, Google Play Age Signals API) and obtain verifiable parental consent for minor accounts. Raw verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Minor Account & Parental Consent Policy detailing age-gating rules and data minimization rules.
- **Missing Documentation:** Lacks cross-platform integration guides for unifying Apple Declared Age Range API and Google Play Age Signals API.
- **Missing Code:** Missing detection recipe command for pattern `BOTH-US-ASAA-AGE-SIGNALS-MISSING` and missing code hooks for `RESCIND_CONSENT` handling.
- **Missing Disclosure:** Onboarding flows omit required state disclosures explaining age category queries and parental consent mandates.
- **Missing Logging:** Lacks backend logging schemas for consent receipts, update approvals, and age data deletion events.
- **Missing Testing:** Lacks unit and integration tests verifying feature locks when age signals indicate a minor without active consent.
- **Missing Evidence:** Lacks sample parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:** Lacks audit logs recording age-assurance feature deployments, policy updates, and data deletion cycles.

### 4.3 Remediation and Action Plan
1. Add the missing recipe command for `BOTH-US-ASAA-AGE-SIGNALS-MISSING` in `data/detection-recipes.json`.
2. Provide native code wrappers for Apple Declared Age Range and Google Play Age Signals APIs.
3. Build backend handlers for processing `RESCIND_CONSENT` notifications.
4. Add automated tests validating age-gating enforcement on minor accounts.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among their staff and personnel operating AI systems. Live since 2 February 2025.

Applicable to all development teams with no headcount carve-out. Pragmatic compliance requires a written policy, induction records, regular refreshers, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a written Organizational AI Literacy Policy defining training requirements and competency areas.
- **Missing Documentation:** Lacks developer training guides on AI safety, risk evaluation, data privacy, and bias mitigation.
- **Missing Code:** Lacks CLI linting scripts or commit guards to verify that contributors working on AI modules hold active literacy training records.
- **Missing Disclosure:** Lacks public or contractual statements disclosing organization-wide compliance with Article 4 literacy mandates.
- **Missing Logging:** Lacks a standardized training log schema or `AI_LITERACY_LOG.md` registry to track staff inductions and course completions.
- **Missing Testing:** Lacks automated checks in CI pipelines to flag missing or stale annual literacy logs.
- **Missing Evidence:** Lacks sample course completion certificates, training materials, or competency assessment records.
- **Missing Audit Trail:** Lacks historical audit trails documenting AI literacy policy reviews, curriculum updates, and staff completion histories.

### 5.3 Remediation and Action Plan
1. Create an internal AI Literacy Policy template.
2. Add `templates/AI_LITERACY_LOG.md` to track team training dates, topics, and refreshers.
3. Wire a CI lint check into `scripts/validate.py` or pipeline guards to warn when literacy logs require annual review.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 dictates mandatory transparency obligations for AI systems, taking effect on 2 August 2026.

Article 50(1) requires informing users when interacting with AI systems. Article 50(2) mandates machine-readable, detectable marking of synthetic media (text, audio, image, video). Article 50(4) requires explicit deepfake disclosures.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an AI Transparency and Disclosure Policy governing user notices and output marking.
- **Missing Documentation:** Lacks developer guides on embedding C2PA provenance metadata or synthetic watermarking into generated assets.
- **Missing Code:** Missing code utilities to inject machine-readable provenance headers into generative AI API pipelines.
- **Missing Disclosure:** UI chat and media templates fail to render mandatory initial disclosures ("You are interacting with an AI system").
- **Missing Logging:** Lacks logging mechanisms capturing when transparency disclosures were displayed to natural persons.
- **Missing Testing:** Lacks test runners verifying that synthetic media outputs contain machine-detectable provenance markers.
- **Missing Evidence:** Lacks evidence of independent red-teaming audits or vendor provenance compliance certificates.
- **Missing Audit Trail:** Lacks an audit trail documenting technical choices, metadata specifications, and disclosure UI updates.

### 6.3 Remediation and Action Plan
1. Publish an AI Transparency & Disclosure Policy template.
2. Provide code samples for C2PA provenance metadata injection in media pipelines.
3. Update UI templates to display initial AI interaction notices.
4. Add synthetic content detection tests to continuous integration checks.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms (Apple App Store, Google Play) and grants rights to developers distributing in the EU, including web distribution, alternative app stores, alternative payment processing, and external offer promotion.

App developers in the EU must comply with platform entitlements (`com.apple.developer.storekit.external-purchase-link`), display disclosure sheets, and submit monthly transaction reporting.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an EU Alternative Distribution Policy governing external link choices and reporting rules.
- **Missing Documentation:** Lacks operational developer runbooks for integrating StoreKit External Purchase Link entitlements and reporting APIs.
- **Missing Code:** Lacks mock client code demonstrating `ExternalPurchaseCustomLink` display sheets or automated monthly transaction report generation.
- **Missing Disclosure:** UI templates omit mandatory external transaction disclosures required when users navigate outside App Store Connect.
- **Missing Logging:** Lacks logging schemas to record external offer clicks, user redirections, and completed out-of-app transactions.
- **Missing Testing:** Lacks unit tests verifying that StoreKit IAP and external purchase links are never co-mingled on the same EU storefront.
- **Missing Evidence:** Lacks template documentation of accepted ADPLA Attachment 14 agreements or CTC commission reporting files.
- **Missing Audit Trail:** Lacks an audit trail capturing entitlement changes, reporting submissions, and external payment integration updates.

### 7.3 Remediation and Action Plan
1. Add DMA integration guidance to `docs/EU-REGULATORY-2026.md`.
2. Provide Swift and Kotlin code samples for region-gated external link disclosures.
3. Build reporting schema templates for monthly external transaction disclosures.

---

## 8. EU Digital Services Act (DSA) Trader Status

### 8.1 Regulatory Overview and Background
Articles 30 and 31 of Regulation (EU) 2022/2065 (Digital Services Act) mandate that app stores verify and display trader contact details (name, address, telephone, email, DUNS) for developers distributing apps in the EU.

Non-trader status declares that EU consumer protection laws do not apply. Unverified trader accounts face storefront removal across all 27 EU Member States.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an EU Trader Verification Policy helping organizations evaluate trader versus non-trader status.
- **Missing Documentation:** Lacks developer step-by-step guides for completing 2FA phone/email verification and D-U-N-S uploads in App Store Connect.
- **Missing Code:** Pre-submission scripts lack checks verifying DSA trader status declaration prior to submission.
- **Missing Disclosure:** Listing templates omit public trader contact blocks (postal address, verified phone, official email).
- **Missing Logging:** Lacks internal logging tracking DSA compliance submission dates and verification confirmation tokens.
- **Missing Testing:** Lacks automated metadata audit checks verifying trader declaration fields during release audits.
- **Missing Evidence:** Lacks proof of verified trader documentation, DUNS profile records, or 2FA verification receipts.
- **Missing Audit Trail:** Lacks an audit trail logging changes to trader declarations, corporate contact details, or status updates.

### 8.3 Remediation and Action Plan
1. Add DSA trader compliance checks to `scripts/metadata-audit.py`.
2. Update `docs/PRE-SUBMISSION-CHECKLIST.md` with DSA verification verification steps.
3. Include DSA trader contact field verification in automated guards.

---

## 9. European Accessibility Act (EAA) & EN 301 549

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) became mandatory on 28 June 2025. It applies to mobile apps and digital services in e-commerce, banking, travel, media, and electronic communication.

Compliance requires meeting harmonised standard EN 301 549 (WCAG 2.1 Level AA plus Chapter 11 non-web software requirements) and publishing an Accessibility Statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Organizational Accessibility Policy committing to EN 301 549 Chapter 11 compliance.
- **Missing Documentation:** Lacks developer manuals detailing mobile accessibility standards beyond basic WCAG 2.1 AA web rules.
- **Missing Code:** Codebase examples lack VoiceOver traits, Dynamic Type scaling layouts, and high-contrast color themes.
- **Missing Disclosure:** Public templates lack mandatory published Accessibility Statements detailing EN 301 549 compliance status.
- **Missing Logging:** Lacks incident logging schemas to capture user-reported accessibility barriers and screen reader incompatibilities.
- **Missing Testing:** While `scripts/accessibility-audit.py` checks static signals, automated UI tests for focus order and screen reader flows are missing.
- **Missing Evidence:** Lacks EN 301 549 Chapter 11 evaluation reports, VPAT documents, or expert accessibility audit certificates.
- **Missing Audit Trail:** Lacks an audit log tracking accessibility defect remediations, UI component updates, and annual statement reviews.

### 9.3 Remediation and Action Plan
1. Expand `scripts/accessibility-audit.py` test suite for EN 301 549 Chapter 11.
2. Provide accessible UI code components (VoiceOver, Dynamic Type, Contrast) in `references/`.
3. Add a template Accessibility Statement document in `templates/`.

---

## 10. US COPPA & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (16 CFR Part 312) protects children under 13. The FTC's amended COPPA Rule (effective June 2025, mandatory April 2026) expands personal info to include biometric identifiers, requires separate opt-in for ad disclosure, and mandates written retention/security policies.

Official Citation: 16 CFR Part 312 (FTC).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks written Information Security Program and Data Retention Policy templates mandated under 312.8 and 312.10.
- **Missing Documentation:** Lacks operational developer guides detailing knowledge-based authentication and ID face-match consent methods.
- **Missing Code:** Lacks client-side code blocks isolating biometric collection from third-party advertising SDKs.
- **Missing Disclosure:** Onboarding templates lack separate opt-in consent modals for third-party data sharing and targeted ads.
- **Missing Logging:** Lacks database logging capturing verifiable parental consent receipts, consent methods, and opt-out triggers.
- **Missing Testing:** Lacks unit tests confirming that child-directed app builds block third-party analytics and ad trackers by default.
- **Missing Evidence:** Lacks sample parental consent logs, annual risk assessments, or third-party vendor COPPA agreements.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing retention policy updates, security reviews, and consent revocations.

### 10.3 Remediation and Action Plan
1. Add a written Information Security Program & Retention Policy template for COPPA compliance.
2. Build consent modal templates with separate opt-in toggles for third-party disclosures.
3. Provide automated unit tests verifying ad SDK suppression for under-13 users.

---

## 11. California Privacy (CCPA / CPRA / ADMT / DROP)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended by CPRA (11 CCR) grants rights to know, delete, correct, opt-out of sale/sharing, limit sensitive PI, and opt-out of Automated Decision-Making Technology (ADMT). Honoring Global Privacy Control (GPC) is mandatory.

Official Citation: California Civil Code Sec. 1798.100 et seq.; 11 CCR Sec. 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a CCPA/CPRA Privacy Policy template covering ADMT processing and sensitive PI limits.
- **Missing Documentation:** Lacks developer runbooks for handling GPC signals in native mobile apps and embedded webviews.
- **Missing Code:** Lacks native hooks to parse and honor `Sec-GPC` headers or pass opt-out flags to ad networks.
- **Missing Disclosure:** UI templates omit mandatory "Do Not Sell or Share My PI" and "Limit Use of Sensitive PI" links.
- **Missing Logging:** Lacks log schemas tracking consumer privacy request receipts (know, delete, opt-out) and fulfillment status within 45 days.
- **Missing Testing:** Lacks automated tests verifying that GPC header detection instantly disables third-party tracking pixels.
- **Missing Evidence:** Lacks annual privacy request metrics reports or risk assessment documents required for ADMT processing.
- **Missing Audit Trail:** Lacks an audit trail capturing privacy policy updates, GPC configuration changes, and request response logs.

### 11.3 Remediation and Action Plan
1. Add GPC detection and opt-out code patterns to `references/rules/privacy.md`.
2. Provide a CCPA/CPRA Privacy Policy template including ADMT disclosures.
3. Build logging schema samples for tracking 45-day privacy request fulfillment.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) requires written notice and written release before collecting biometric identifiers (fingerprint, voiceprint, facial template). It mandates a public retention schedule and destruction within 3 years.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Biometric Data Retention & Destruction Policy.
- **Missing Documentation:** Lacks developer guidance on obtaining legally binding written releases prior to biometric capture.
- **Missing Code:** Code examples lack written consent modal sheets for biometric authentication flows.
- **Missing Disclosure:** UI templates omit public disclosures detailing biometric data retention schedules and destruction guidelines.
- **Missing Logging:** Lacks secure logging schemas recording consent timestamps, biometric hash generation, and scheduled deletion dates.
- **Missing Testing:** Lacks unit tests verifying that biometric authentication APIs (LocalAuthentication, BiometricPrompt) cannot execute without affirmative consent flags.
- **Missing Evidence:** Lacks sample executed release agreements, destruction certificates, or vendor BIPA compliance declarations.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing biometric policy reviews, destruction log executions, and consent revocations.

### 12.3 Remediation and Action Plan
1. Draft a Biometric Retention & Destruction Policy template.
2. Provide Swift (LocalAuthentication) and Kotlin (BiometricPrompt) code samples wrapping authorization in affirmative consent UI sheets.
3. Add automated tests verifying biometric consent preconditions.

---

## 13. US Subscription Cancellation (ROSCA / FTC / State Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state statutes (California, New York, Massachusetts) mandate that online subscription cancellation must be at least as simple as enrollment.

Subscriptions billed outside App Store IAP or Google Play Billing cannot require phone calls, letters, or complex multi-step friction to cancel.

Official Citation: 15 U.S.C. 8401 et seq.; Cal. Bus. & Prof. Code Sec. 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Subscription Cancellation & Recurring Billing Policy template.
- **Missing Documentation:** Lacks UI/UX design specifications defining frictionless online cancellation paths.
- **Missing Code:** Lacks mock web or in-app self-service cancellation components for non-IAP subscriptions.
- **Missing Disclosure:** Subscription checkout screens omit mandatory auto-renewal disclosures, billing frequency, and clear cancellation instructions.
- **Missing Logging:** Lacks event logging schemas to capture cancellation requests, retention offer responses, and refund processing timestamps.
- **Missing Testing:** Existing pattern `BOTH-SUBSCRIPTION-HARD-CANCEL` detects hard-cancellation strings, but automated end-to-end cancellation path tests are missing.
- **Missing Evidence:** Lacks sample cancellation confirmation receipts or customer service escalation logs.
- **Missing Audit Trail:** Lacks audit logs recording changes to subscription terms, checkout screens, or cancellation flows.

### 13.3 Remediation and Action Plan
1. Provide self-service subscription cancellation UI code templates for web views.
2. Update subscription pre-submission checklist items in `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add automated test runners verifying zero-friction cancellation paths.

---

## 14. UK Online Safety Act & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code mandate age assurance (facial age estimation, credit card verification, open banking) and high privacy by default (geolocation off, profiling off, mandatory DPIA) for services likely accessed by children under 18.

Official Citations: Online Safety Act 2023 c. 50; Data Protection Act 2018 / ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Children's Privacy & Safety Policy template.
- **Missing Documentation:** Lacks developer manuals for conducting Data Protection Impact Assessments (DPIAs) under the ICO Code.
- **Missing Code:** Lacks code examples enforcing high-privacy defaults (disabling location, turning off profiling) when UK minor users are detected.
- **Missing Disclosure:** Public UI templates omit UK-specific child safety disclosures and reporting mechanism links.
- **Missing Logging:** Lacks logging schemas to record age estimation results, DPIA completion dates, and child safety incident reports.
- **Missing Testing:** Lacks integration tests verifying that geolocation and profiling flags default to OFF for UK minor user profiles.
- **Missing Evidence:** Lacks sample completed DPIA documents, eSafety risk assessments, or age assurance vendor verification reports.
- **Missing Audit Trail:** Lacks audit trails capturing safety feature updates, DPIA reviews, and child safety report handling histories.

### 14.3 Remediation and Action Plan
1. Provide a template Data Protection Impact Assessment (DPIA) for UK ICO Children's Code compliance.
2. Provide code samples setting high-privacy defaults for under-18 accounts.
3. Add automated test cases checking default privacy toggle configurations.

---

## 15. Australia Online Safety Framework & Privacy Act Amendments

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 (in force December 2025) requires social media platforms to block under-16s using robust age assurance. The Privacy Act requires disclosing Automated Decision-Making (ADM) in privacy policies by December 2026.

Official Citations: Online Safety Act 2021 as amended 2024; Privacy Act 1988 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Social Media Age Restriction & ADM Disclosure Policy.
- **Missing Documentation:** Lacks developer runbooks detailing age-assurance data destruction mandates under Australian law.
- **Missing Code:** Lacks code components ringfencing and destroying age-assurance verification tokens immediately post-verification.
- **Missing Disclosure:** Privacy policy templates omit mandatory disclosures detailing ADM usage and rights impacts.
- **Missing Logging:** Lacks backend logging schemas recording ADM logic execution and age data destruction confirmation events.
- **Missing Testing:** Lacks unit tests verifying that raw age verification inputs are purged from memory and database tables post-validation.
- **Missing Evidence:** Lacks sample eSafety risk assessment filings or ADM transparency evaluation reports.
- **Missing Audit Trail:** Lacks immutable audit trails tracking age data destruction triggers, ADM policy updates, and compliance audits.

### 15.3 Remediation and Action Plan
1. Add ADM disclosure templates to privacy policy documentation.
2. Provide backend code patterns demonstrating immediate purge of age verification payloads.
3. Add automated tests verifying zero retention of sensitive age verification tokens.

---

## 16. Brazil Digital ECA & Decreto 12.880

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto 12.880 (March 2026) mandate document verification, facial estimation, or CPF database checks for age assurance. Self-declaration checkboxes are prohibited. App stores must provide free age signals.

Official Citations: Lei n. 15.211/2025; Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazil Age Assurance & Guardian Consent Policy template.
- **Missing Documentation:** Lacks developer guidelines for integrating ANPD-approved age verification methods (CPF check, facial estimation).
- **Missing Code:** Lacks client-side code blocks handling Play Age Signals API and Apple Declared Age Range API specifically for Brazil storefronts.
- **Missing Disclosure:** UI onboarding templates omit required disclosures explaining age verification mandates and age ratings before download.
- **Missing Logging:** Lacks logging schemas to record CPF verification outcomes, guardian consent authorizations, and contestation requests.
- **Missing Testing:** Lacks automated test scripts validating that self-declaration checkboxes are rejected for Brazilian user IP addresses.
- **Missing Evidence:** Lacks ANPD compliance audit certificates, guardian consent receipts, or loot-box 18+ auto-rating documentation.
- **Missing Audit Trail:** Lacks audit logs capturing age assurance method updates, ANPD policy alignment checks, and guardian consent records.

### 16.3 Remediation and Action Plan
1. Add Brazil Digital ECA compliance guidelines to `docs/GLOBAL-REGULATORY-2026.md`.
2. Provide code samples wrapping Play Age Signals API for Brazilian storefront accounts.
3. Add automated tests verifying rejection of self-declaration checkboxes for Brazil.

---

## 17. India Digital Personal Data Protection Act (DPDPA / Rules 2025)

### 17.1 Regulatory Overview and Background
The DPDPA 2023 and DPDP Rules 2025 (notified November 2025, mandatory May 2027) require verifiable parental consent via government systems (DigiLocker) for under-18s and prohibit behavioral tracking/targeted ads for children. Registered Consent Managers commence November 2026.

Official Citation: Act No. 22 of 2023; Gazette Notification G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India Data Fiduciary & Children's Data Policy template.
- **Missing Documentation:** Lacks developer integration runbooks for interoperating with registered Consent Managers and DigiLocker APIs.
- **Missing Code:** Lacks code handlers suppressing behavioral tracking and targeted ad SDKs for under-18 Indian accounts.
- **Missing Disclosure:** Onboarding flows omit mandatory multilingual consent notices detailing data processing items and Data Fiduciary contact info.
- **Missing Logging:** Lacks database logging schemas capturing Consent Manager tokens, parental consent receipts, and withdrawal events.
- **Missing Testing:** Lacks unit tests verifying that ad network initialization is completely blocked when user age is under 18 in India.
- **Missing Evidence:** Lacks sample Data Protection Board audit filings, Consent Manager integration certificates, or DigiLocker verification logs.
- **Missing Audit Trail:** Lacks an immutable audit trail recording consent notice revisions, Consent Manager configuration changes, and child data processing audits.

### 17.3 Remediation and Action Plan
1. Provide DPDPA consent notice templates in `templates/`.
2. Add code examples suppressing tracking SDKs for under-18 users in India.
3. Include automated integration checks for Consent Manager protocol support.

---

## 18. Singapore PDPA & IMDA App Distribution Safety Code

### 18.1 Regulatory Overview and Background
The Singapore Personal Data Protection Act (PDPA) and IMDA Code of Practice for Online Safety require app-store age assurance (effective April 2026) to block under-18s from downloading age-inappropriate apps. Verification data must be destroyed immediately after use.

Official Citations: Personal Data Protection Act 2012; IMDA Code of Practice 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore Data Protection & Age Assurance Policy template.
- **Missing Documentation:** Lacks developer guides on appointing a Data Protection Officer (DPO) and fulfilling 3-day breach reporting duties.
- **Missing Code:** Lacks client-side logic to handle Singapore 18-plus download block responses from App Store Connect / Play Console.
- **Missing Disclosure:** Public privacy policy templates omit mandatory disclosures regarding DPO contact details and age assurance data handling.
- **Missing Logging:** Lacks logging schemas to capture 3-day breach notification timelines and age data purge verification receipts.
- **Missing Testing:** Lacks automated unit tests checking immediate memory wipe of age verification inputs post-validation.
- **Missing Evidence:** Lacks sample DPO appointment certificates, IMDA risk assessment filings, or age data destruction receipts.
- **Missing Audit Trail:** Lacks audit logs recording DPO policy updates, breach report submissions, and annual PDPA compliance audits.

### 18.3 Remediation and Action Plan
1. Include DPO contact templates in privacy documentation.
2. Provide code samples demonstrating prompt data purge of verification tokens.
3. Add pre-submission checklist steps verifying DPO declaration for Singapore.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
The Telecommunications Business Act mandates alternative in-app billing (26% commission, approved local payment gateways, StoreKit entitlement). The PIPA amendment (effective September 2026) establishes CEO/CPO accountability and strict breach notification.

Official Citations: Telecommunications Business Act Art. 22-9; Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea Payment Compliance & Chief Privacy Officer Accountability Policy.
- **Missing Documentation:** Lacks developer runbooks for setting up Korea-only binaries, modal sheets, and monthly sales reporting to Apple/Google.
- **Missing Code:** Lacks code handlers for displaying the mandatory StoreKit Korea alternative payment modal sheet.
- **Missing Disclosure:** In-app checkout screens omit required modal disclosures stating transactions use alternative payment gateways.
- **Missing Logging:** Lacks logging schemas tracking monthly Korea alternative payment sales, VAT calculations, and commission reporting files.
- **Missing Testing:** Lacks unit tests verifying that alternative billing modal sheets display prior to launching local payment gateways.
- **Missing Evidence:** Lacks sample Korea Communications Commission (KCC) compliance reports, approved gateway contracts, or CPO appointment records.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing alternative payment transaction logs, reporting submissions, and CPO policy reviews.

### 19.3 Remediation and Action Plan
1. Provide Swift/Kotlin code samples for Korea alternative payment modal sheets.
2. Add sales reporting schema templates to `templates/`.
3. Include PIPA CPO accountability checklists in `docs/GLOBAL-REGULATORY-2026.md`.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Measures

### 20.1 Regulatory Overview and Background
Mandatory MIIT App Filing (ICP extension) requires a local Chinese partner/entity. CAC Order No. 21 (July 2026) regulates AI anthropomorphic companion services, banning virtual companion apps for minors and requiring automatic minor mode switching.

Official Citations: MIIT App Filing Notice 2023; CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China App Filing & Minor Protection Policy template.
- **Missing Documentation:** Lacks developer guides on MIIT filing steps, local partner agreements, real-name authentication, and Banhao game licensing.
- **Missing Code:** Lacks code components for automatic "Minors Mode" switching and age verification for AI chat services in China.
- **Missing Disclosure:** Onboarding interfaces omit mandatory MIIT ICP filing numbers in app footers/settings and real-name registration notices.
- **Missing Logging:** Lacks database logging schemas capturing real-name verification tokens, minor mode active durations, and CAC content filtering flags.
- **Missing Testing:** Lacks automated tests confirming that virtual companion chat features are strictly blocked when minor mode is active.
- **Missing Evidence:** Lacks sample MIIT ICP filing certificates, Banhao license documents, or CAC AI security assessment filings.
- **Missing Audit Trail:** Lacks audit logs recording real-name system updates, minor mode feature changes, and CAC compliance audit submissions.

### 20.3 Remediation and Action Plan
1. Add China App Filing and CAC AI compliance guides to `docs/GLOBAL-REGULATORY-2026.md`.
2. Provide code samples for automatic Minors Mode gating in AI applications.
3. Include MIIT ICP filing number checks in metadata audit scripts.

---

## 21. Consolidated Gap Classification Matrix

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Missing | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA Trader Status** | Partial | Covered | Missing | Covered | Missing | Partial | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Partial | Missing | Missing | Partial | Missing | Missing |
| **10. US COPPA & Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA/CPRA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Missing | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Covered | Missing | Partial | Missing | Missing |
| **14. UK Online Safety & Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Strategy

The playbook provides exceptional coverage of app store rejection guidelines (Apple App Store Review Guidelines, Google Play Developer Policies) and high-level regulatory summaries. However, when evaluated against operational compliance requirements across all eight gap categories, systematic omissions exist:

1. **Policy Layer:** Most frameworks are mentioned in reference documents, but ready-to-use policy templates (such as e-Evidence Law Enforcement Policy, BIPA Retention Policy, or GPSR Safety Policy) are absent.
2. **Implementation Code Layer:** The repository lacks runnable frontend/backend code snippets wrapping platform APIs (such as StoreKit External Purchase, Play Age Signals, C2PA Provenance, and GPC Header Parsers).
3. **Logging & Audit Trail Layer:** Zero database schemas or log specifications exist across all 20 frameworks to capture legal request fulfillments, consent receipts, age data deletions, or compliance audits.
4. **Testing & Evidence Layer:** Test suites currently focus on store rejection patterns rather than verifying regulatory compliance mechanics (such as 8-hour e-Evidence extraction or zero-friction cancellation paths).

### Remediation Priorities
- **Priority 1 (Immediate Code Remediation):** Add missing recipe command for `BOTH-US-ASAA-AGE-SIGNALS-MISSING` to `data/detection-recipes.json` and sync `references/`.
- **Priority 2 (High-Risk 2026 Mandates):** Provide UI/UX code components for EU Contract Withdrawal Button, Article 50 AI Transparency disclosures, and e-Evidence emergency request handlers.
- **Priority 3 (Audit & Evidence Frameworks):** Build sample logging schemas and audit trail specifications in `templates/` for COPPA, BIPA, and State ASAA consent lifecycle tracking.

---

## 23. Official Primary Sources

Every regulation cited in this report is anchored to official primary sources:
- EU GPSR: [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Contract Withdrawal: [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Federal COPPA Rule: [16 CFR Part 312 (Federal Register / FTC)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US FTC Act & ROSCA: [15 U.S.C. 8401 et seq. (US Code)](https://www.govinfo.gov/)
- California Privacy (CCPA/CPRA/ADMT): [California Civil Code Sec. 1798.100 (CPPA)](https://cppa.ca.gov/regulations/)
- Illinois BIPA: [740 ILCS 14/ (Illinois General Assembly)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act: [Online Safety Act 2023 c. 50 (UK Legislation)](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Online Safety Act: [Online Safety Act 2021 / Amendment 2024 (Federal Register of Legislation)](https://www.legislation.gov.au/)
- Brazil Digital ECA & Decreto 12.880: [Decreto n. 12.880 (Planalto)](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA 2023 & Rules 2025: [Gazette Notification G.S.R. 846(E) (eGazette India)](https://egazette.gov.in)
- Singapore PDPA & IMDA Code: [IMDA Code of Practice for Online Safety (IMDA)](https://www.mddi.gov.sg/)
- South Korea TBA & PIPA: [Act No. 21445 (National Law Information Center)](https://law.go.kr)
- China MIIT Filing & CAC Order 21: [CAC Order No. 21 (Cyberspace Administration of China)](https://www.cac.gov.cn/)
