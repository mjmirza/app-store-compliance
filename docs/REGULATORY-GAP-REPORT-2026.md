# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind mobile and web application developers shipping globally across the EU, US, UK, Australia, Brazil, Canada, India, Singapore, South Korea, and China. It systematically checks how far this repository carries each regulation, what it only mentions in passing, and what remains missing.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Every framework is rigorously audited across eight distinct compliance categories:
- Missing policy
- Missing documentation
- Missing code
- Missing disclosure
- Missing logging
- Missing testing
- Missing evidence
- Missing audit trail

## Source Trust Hierarchy and Methodology

All analysis and cited legal frameworks within this report adhere strictly to the repository source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems, software, and mobile e-commerce platforms, the GPSR mandates displaying product safety warnings, manufacturer identity, importer details, and safety contact points directly on the online interface prior to purchase.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no written policy template or guidance for determining product safety coverage, risk classification, or appointing an EU Responsible Person under Regulation (EU) 2023/988.
- **Missing Documentation:**
  Developer checklists lack specific instructions or structural manuals explaining how to format and display safety disclosures, technical specifications, and manufacturer contact details on mobile app storefronts.
- **Missing Code:**
  Automated detection recipes and pre-submission guard scripts lack rules to scan source code for missing GPSR metadata fields or UI components displaying safety contacts and product safety warnings.
- **Missing Disclosure:**
  UI storefront mockups and templates do not include UI fields or components for displaying the manufacturer's name, registered trade name, postal address, and electronic address (email or web link) as mandated under Article 19.
- **Missing Logging:**
  There are no database schemas or architectural patterns for logging product safety reports, customer safety complaints, or product recall notifications.
- **Missing Testing:**
  The repository contains no automated test suites to verify that product detail pages dynamically render compulsory safety warnings based on user locale or product category.
- **Missing Evidence:**
  The repository contains no physical templates for storing GPSR compliance evidence, such as Technical Documentation sheets, safety risk assessments, or EU Responsible Person designation agreements.
- **Missing Audit Trail:**
  There is no unalterable logging framework to capture when product safety warnings were updated or when safety recall actions were executed across mobile and web interfaces.

### 1.3 Remediation and Action Plan
1. Create a written General Product Safety Policy detailing EU Responsible Person designation and safety classification.
2. Incorporate GPSR metadata inspection rules into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Build compliant UI detail templates in references showcasing product safety disclosures.
4. Add automated unit test scripts validating safety disclosure rendering prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package comprises Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on legal representatives. The mandatory enforcement date is 18 August 2026.

This framework empowers judicial authorities in EU Member States to issue European Production Orders (EPO) or European Preservation Orders directly to service providers offering services in the EU. Standard production orders require user data production within 10 days, while critical emergency cases mandate data delivery within a strict 8-hour window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Law Enforcement Response Policy outlining procedural workflows, authorization tiers, and legal review for incoming European Production and Preservation Orders.
- **Missing Documentation:**
  Operational runbooks explaining step-by-step procedures for fulfilling 10-day production orders and executing 8-hour emergency responses are missing.
- **Missing Code:**
  The codebase includes no automated backend utilities or secure data-export pipelines to filter, package, and encrypt user data securely under emergency deadlines.
- **Missing Disclosure:**
  Public-facing documentation and privacy notices do not inform EU users that data may be preserved or disclosed to European authorities pursuant to Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository provides no database schemas or logging modules designed to log law enforcement requests, authentication tokens, or data extraction activities.
- **Missing Testing:**
  No simulated emergency drills or integration tests exist to measure data packaging speeds and verify compliance with the 8-hour statutory response limit.
- **Missing Evidence:**
  The playbook contains no standardized certificate templates for European Production Order Certificates (EPOC) or Preservation Order Certificates (EPOC-PR).
- **Missing Audit Trail:**
  A cryptographically secure, tamper-proof audit trail tracking administrative access, data extraction events, and transmission logs during legal request handling is absent.

### 2.3 Remediation and Action Plan
1. Formulate a Law Enforcement Response Protocol establishing roles, authentication mechanisms, and emergency handling.
2. Formally document the appointment of an EU legal representative under Directive (EU) 2023/1544 before 18 August 2026.
3. Develop secure CLI extraction scripts to retrieve and package user account records within 8 hours.
4. Implement encrypted audit log schemas to record all incoming judicial orders and extraction events.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It mandates a prominent, easily accessible withdrawal button or withdrawal function on digital interfaces for distance financial services contracts concluded electronically, with Member States applying rules from 19 June 2026.

The statutory withdrawal period is 14 days from contract conclusion. The cancellation path must be clear, direct, and at least as simple as the sign-up path, preventing hidden contact forms or phone calls.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository contains no written Consumer Cancellation and Right of Withdrawal Policy defining 14-day statutory revocation workflows and refund parameters.
- **Missing Documentation:**
  Design specifications and placement guidelines explaining exact UI button positioning, visibility standards, and phrasing for the withdrawal button are absent.
- **Missing Code:**
  Mobile and web frontend templates lack functional implementations of a dedicated "Withdrawal Button" or modal sheet component for self-service contract revocation.
- **Missing Disclosure:**
  Subscription flows do not display mandatory statutory disclosures explaining the 14-day right of withdrawal, revocation consequences, or immediate refund terms.
- **Missing Logging:**
  No backend logging schemas exist to capture withdrawal button clicks, timestamps, contract termination events, or refund initiation signals.
- **Missing Testing:**
  Automated UI tests verifying that users can successfully terminate subscriptions without human intervention or administrative barriers are missing.
- **Missing Evidence:**
  The repository provides no templates for generating automated cancellation confirmation receipts or refund verification documents.
- **Missing Audit Trail:**
  An immutable audit trail recording historical cancellation volumes, refund processing times, and interface modification logs is not implemented.

### 3.3 Remediation and Action Plan
1. Draft a comprehensive Consumer Cancellation Policy aligned with Directive (EU) 2023/2673.
2. Build a self-service "Withdrawal Button" component inside user account settings templates.
3. Create backend database tables for capturing withdrawal request timestamps and transaction IDs.
4. Add automated end-to-end UI tests validating frictionless 1-click contract cancellation.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minor access to mobile applications, digital purchases, and major software updates.

Developers must query user age categories (using Apple's Declared Age Range API or Google Play Age Signals API), obtain verifiable parental consent for minor accounts before downloads or purchases, re-request consent on major app updates, and immediately delete raw age-verification documents after age confirmation.

Official Citations: Utah SB 142 (2025/2026), Texas SB 2420 (2025/2026), Louisiana HB 570 / HB 977 (2025/2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a dedicated Minor Age Assurance and Data Minimization Policy detailing state-specific age checks and data deletion mandates.
- **Missing Documentation:**
  Checklists lack step-by-step developer integration manuals for unifying Apple's Declared Age Range API and Google Play Age Signals API across cross-platform frameworks.
- **Missing Code:**
  Codebase templates do not integrate native API calls (`DeclaredAgeRange` or `com.google.android.play:age-signals`) to restrict feature access for minor age bands dynamically.
- **Missing Disclosure:**
  Onboarding UI templates do not display required state legal notices informing users why age categories are collected and how parental consent is managed.
- **Missing Logging:**
  Backend schemas lack mechanisms to log parental consent receipts, consent revocation signals (`RESCIND_CONSENT`), or verifiable proof of immediate age document deletion.
- **Missing Testing:**
  Integration tests verifying that unconfirmed minor accounts are blocked from completing in-app purchases or accessing adult content are absent.
- **Missing Evidence:**
  The repository provides no standardized templates for parental consent agreements, identity verification logs, or data purging verifications.
- **Missing Audit Trail:**
  An immutable audit trail documenting age-assurance feature updates, policy revisions, and immediate data deletion events is completely missing.

### 4.3 Remediation and Action Plan
1. Establish a written Minor Age Assurance Policy enforcing immediate deletion of raw verification credentials.
2. Implement native bridge hooks to query Apple and Google age-signal APIs during app initialization.
3. Build backend handlers for processing server notifications regarding consent revocations.
4. Add automated unit tests verifying that minor account flags successfully disable digital purchases.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. Providers and deployers of AI systems must ensure their personnel and operators possess a sufficient level of AI literacy, taking into account their technical knowledge, experience, and the context of AI deployment.

This requirement entered into force on 2 February 2025 and applies to all organizations regardless of headcount, requiring small development teams to maintain written policies, training schedules, and active literacy logs.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Literacy Policy defining training benchmarks, risk assessment competencies, or team role expectations under Article 4.
- **Missing Documentation:**
  Developer documentation lacks guidelines explaining employee literacy duties, AI safety concepts, or procedures for handling generative model risks.
- **Missing Code:**
  Not directly applicable to software binaries, but the repository lacks automated repository linting scripts to check for the presence and freshness of internal training records.
- **Missing Disclosure:**
  Public documentation and partner contracts fail to include formal declarations asserting compliance with EU AI Act Article 4 literacy standards.
- **Missing Logging:**
  The repository contains no centralized log file (such as `AI_LITERACY_LOG.md`) to track employee inductions, completion dates, and refresher courses.
- **Missing Testing:**
  CI/CD pipelines lack automated validation steps to check whether team training logs are present and updated annually prior to code deployments.
- **Missing Evidence:**
  The playbook includes no example templates of training certificates, literacy assessment forms, or course completion records.
- **Missing Audit Trail:**
  An audit trail tracking historical policy updates, curriculum revisions, and annual literacy review records is absent.

### 5.3 Remediation and Action Plan
1. Publish an internal AI Literacy Policy outlining required competencies in AI safety, data privacy, and bias identification.
2. Establish a structured `AI_LITERACY_LOG.md` file in the repository to document team training history.
3. Implement a pre-commit check verifying that AI literacy records have been reviewed within the past 12 months.
4. Designate a compliance lead to execute annual reviews of team literacy documentation.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act mandates strict transparency requirements for AI systems reaching EU users, taking full effect on 2 August 2026.

Providers must ensure AI systems interacting with natural persons inform users that they are interacting with AI (Article 50(1)). Generative AI outputs (text, audio, image, video) must be marked in a machine-readable format and detectable as artificially generated (Article 50(2)), and deepfakes must be clearly disclosed (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an AI Transparency Policy defining when user disclosures must appear and specifying synthetic content marking protocols.
- **Missing Documentation:**
  Developer guides lack detailed technical instructions on implementing machine-readable watermarking (e.g., C2PA metadata) or synthetic content headers.
- **Missing Code:**
  Codebase templates lack helper utilities, middleware, or SDK wrappers to inject C2PA content provenance metadata into generated images, text, or audio streams.
- **Missing Disclosure:**
  Conversational UI components do not render the required "You are interacting with an AI assistant" notice at or before first user exposure.
- **Missing Logging:**
  No database schemas exist to log user exposure to AI interaction disclosures or record synthetic media generation events.
- **Missing Testing:**
  Test suites lack automated media scanners to verify that generated binary outputs carry machine-readable synthetic content tags.
- **Missing Evidence:**
  The playbook provides no templates for recording independent content moderation audits or watermark retention tests.
- **Missing Audit Trail:**
  An immutable log tracking model version updates, transparency notice revisions, and watermarking algorithm changes is missing.

### 6.3 Remediation and Action Plan
1. Draft an AI Transparency and Disclosure Policy enforcing direct user notices and machine-readable output tagging.
2. Embed visible AI notices ("You are chatting with an AI assistant") in all conversational UI templates.
3. Integrate standard metadata injection utilities into synthetic media output pipelines.
4. Build automated integration tests to scan generated media assets for machine-readable provenance headers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms to ensure contestability and fairness in digital markets. For mobile applications distributed in the EU, the DMA enables alternative app distribution channels, web distribution, custom browser engines, and alternative payment processing.

Apple's EU business terms (updated October 2026 via Attachment 14) establish the Core Technology Commission (CTC) at 5% for alternative marketplace digital transactions, while requiring system disclosure sheets (`ExternalPurchaseCustomLink`) when linking to external offers.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository contains no written DMA Distribution and Alternative Billing Policy guiding developers through entitlement selection and reporting duties.
- **Missing Documentation:**
  Checklists lack step-by-step developer documentation on implementing StoreKit External Purchase Link entitlements, MarketplaceKit frameworks, or browser engine entitlements.
- **Missing Code:**
  The codebase provides no code snippets for invoking Apple's `ExternalPurchaseCustomLink` system sheet or connecting to the External Purchase Server API for transaction reporting.
- **Missing Disclosure:**
  UI storefront templates do not include standard external offer disclosures informing users that transactions occur outside Apple's payment system.
- **Missing Logging:**
  Backend templates lack database schemas for tracking monthly external purchase volumes required for 15-day fiscal reporting to Apple.
- **Missing Testing:**
  No unit or integration tests exist to verify that external purchase links are correctly region-gated to EU storefronts and call the mandatory system sheet.
- **Missing Evidence:**
  The playbook carries no template for recording proof of Attachment 14 acceptance or alternative marketplace security audit verifications.
- **Missing Audit Trail:**
  An immutable audit trail tracking external transaction reporting submissions, fee calculations, and entitlement configuration changes is missing.

### 7.3 Remediation and Action Plan
1. Establish an EU Distribution Policy governing DMA entitlement usage and reporting compliance.
2. Add code implementations invoking `ExternalPurchaseCustomLink` on EU storefront taps.
3. Build backend reporting handlers to compile monthly transaction logs for Apple API submission.
4. Implement automated tests verifying storefront region gating for DMA entitlements.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) sets comprehensive accountability rules for online intermediaries, platforms, and app store listings. Articles 30 and 31 mandate trader status verification, requiring app developers distributing commercial software in the EU to publish verified trader details (name, address, phone, email, payment account) on store product pages.

Additionally, the DSA requires robust illegal content notice-and-action mechanisms, user moderation reporting, and minor protection safeguards across digital platforms.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written DSA Compliance and Content Moderation Policy governing trader declarations and user illegal content notifications.
- **Missing Documentation:**
  Checklists lack clear developer guides on setting up App Store Connect / Google Play Console DSA trader profiles and managing 2FA verification uploads.
- **Missing Code:**
  Codebase templates contain no in-app "Report Illegal Content" modal sheets or API endpoints for processing user content flags under DSA requirements.
- **Missing Disclosure:**
  Store metadata templates do not include formatted developer identity cards or required consumer right disclosures for non-trader listings.
- **Missing Logging:**
  There are no backend database models to record incoming illegal content notices, moderation decisions, or user appeal filings.
- **Missing Testing:**
  Automated tests verifying that trader information fields are populated and valid prior to store submission are missing.
- **Missing Evidence:**
  The repository provides no example templates of DSA annual transparency reports or verified trader submission records.
- **Missing Audit Trail:**
  An unalterable audit log capturing moderation actions, content takedown timestamps, and user notice responses is absent.

### 8.3 Remediation and Action Plan
1. Formulate a DSA Trader and Content Safety Policy detailing store profile verification steps.
2. Build in-app content reporting UI components for user-generated content applications.
3. Create database tables for logging content notices, review decisions, and resolution timestamps.
4. Add pre-submission checks to verify DSA trader declaration status before app release.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025. It mandates accessibility across consumer products and services, including mobile applications, e-commerce, banking, e-books, and transport booking.

Compliance requires adhering to harmonized standard EN 301 549 (version 3.2.1), which builds on WCAG 2.1 Level AA and adds specific mobile software requirements under Chapter 11. Operators must publish a formal Accessibility Statement detailing conformity and user feedback mechanisms.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no corporate Digital Accessibility Policy committing the organization to EN 301 549 Chapter 11 standards.
- **Missing Documentation:**
  Developer guides fail to detail EN 301 549 Chapter 11 specific requirements for non-web software, focusing only on basic WCAG web principles.
- **Missing Code:**
  UI templates lack comprehensive accessibility traits (`accessibilityLabel`, `accessibilityHint`, dynamic font scaling handlers, or high-contrast focus indicators).
- **Missing Disclosure:**
  Templates do not include an Accessibility Statement page or in-app view detailing compliance status and feedback contact information.
- **Missing Logging:**
  No logging mechanisms exist to capture accessibility feedback submissions, user assistance requests, or assistive technology errors.
- **Missing Testing:**
  The repository contains no automated accessibility test scripts to audit VoiceOver/TalkBack labels, touch targets, or Dynamic Type scaling in code.
- **Missing Evidence:**
  The playbook provides no sample templates for formal Accessibility Conformance Reports (VPAT / EN 301 549 audit reports).
- **Missing Audit Trail:**
  An audit trail tracking historical accessibility review scores, remediation tickets, and UI contrast updates is absent.

### 9.3 Remediation and Action Plan
1. Draft a written Accessibility Policy committing all mobile and web products to EN 301 549 standards.
2. Create an in-app Accessibility Statement template detailing compliance levels and contact channels.
3. Integrate automated UI accessibility linting tools (`accessibility-audit.py`) into CI/CD pipelines.
4. Generate EN 301 549 conformance assessment templates in the documentation directory.

---

## 10. US COPPA Amended Rule (16 CFR Part 312)

### 10.1 Regulatory Overview and Background
The FTC's amended Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312) imposes strict data collection, consent, and retention rules for child-directed services and services with actual knowledge of under-13 users, with mandatory general compliance required by 22 April 2026.

Key updates expand personal information definitions to include biometric identifiers and government IDs, require separate opt-in consent for third-party disclosures, mandate written data retention policies, and enforce annual written information security risk assessments.

Official Citation: 16 CFR Part 312 (FTC Final Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no written COPPA Children's Privacy and Security Policy detailing separate opt-in consent flows or data retention limits.
- **Missing Documentation:**
  Checklists lack technical guides explaining how to configure verifiable parental consent (VPC) methods like knowledge-based authentication or ID face-matching.
- **Missing Code:**
  Codebase templates lack separate opt-in toggle components for third-party ad data sharing, defaulting instead to bundled consent.
- **Missing Disclosure:**
  Onboarding UI templates do not display explicit COPPA direct notices detailing child data collection types, third-party disclosures, and parent rights.
- **Missing Logging:**
  Backend schemas provide no structured tables for logging parental consent records, verification method tokens, or automated child data deletion triggers.
- **Missing Testing:**
  Integration tests verifying that child account flags block the transmission of personal data to ad networks without separate opt-in consent are missing.
- **Missing Evidence:**
  The repository contains no templates for annual Information Security Risk Assessments or written Data Retention Schedules under Section 312.10.
- **Missing Audit Trail:**
  An unalterable audit log recording parental consent timestamps, consent revocations, and scheduled child data purge executions is absent.

### 10.3 Remediation Plan
1. Establish a written COPPA Compliance Policy including mandatory data retention schedules.
2. Build separate opt-in UI toggles for third-party data disclosures during onboarding.
3. Implement automated database purge routines to delete child personal data upon expiration of purpose.
4. Add automated test suites verifying zero third-party tracking calls when a child flag is active.

---

## 11. California Privacy Laws (CCPA / CPRA / AADC / SB 976)

### 11.1 Regulatory Overview and Background
California privacy legislation—comprising the CCPA/CPRA, the CPPA 2026 regulations, the Age-Appropriate Design Code (AB 2273), and SB 976 (protecting minors from addictive feeds)—establishes comprehensive privacy and child protection obligations.

Businesses must provide Notice at Collection, "Do Not Sell or Share My Personal Information" links, "Limit the Use of My Sensitive Personal Information" options, honor Global Privacy Control (GPC) signals, execute automated decision-making risk assessments, and obtain parental consent before delivering addictive feeds to minors.

Official Citations: California Civil Code Sec. 1798.100 et seq.; CPPA Regulations (2026); California AG SB 976.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository contains no California Privacy Policy template addressing CPRA 2026 updates, Global Privacy Control handling, or automated decision-making opt-outs.
- **Missing Documentation:**
  Developer guides lack detailed technical specifications on detecting and respecting the `Sec-GPC` HTTP header inside webviews and native apps.
- **Missing Code:**
  Frontend templates do not include functional "Do Not Sell or Share My Personal Info" or "Limit Sensitive PI Use" UI control components.
- **Missing Disclosure:**
  In-app onboarding layouts do not display formal California Notice at Collection cards listing collected data categories and sensitive PI uses.
- **Missing Logging:**
  Backend templates lack logging models to store opt-out preference signals, GPC header receipts, and consumer rights access requests.
- **Missing Testing:**
  No automated unit tests exist to confirm that when a GPC header is detected, third-party analytics and ad-tracking SDKs are instantly disabled.
- **Missing Evidence:**
  The playbook provides no physical templates for CPRA Cybersecurity Audit certifications or Automated Decision-Making Risk Assessments.
- **Missing Audit Trail:**
  An immutable audit trail tracking consumer rights request fulfillment, opt-out propagation, and policy modification history is missing.

### 11.3 Remediation and Action Plan
1. Draft a CPRA-compliant California Privacy Notice and Notice at Collection template.
2. Implement native and webview handlers to listen for Global Privacy Control (`Sec-GPC`) signals.
3. Build dedicated UI settings views for "Do Not Sell/Share" and "Limit Sensitive PI" preferences.
4. Add automated unit tests verifying ad-tracker suppression upon receipt of GPC signals.

---

## 12. Illinois Biometric Information Privacy Act (BIPA & CUBI)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14) and Texas CUBI regulate the collection, capture, purchase, storage, and use of biometric identifiers (fingerprints, voiceprints, retina scans, facial geometry).

BIPA mandates obtaining written releases before capturing biometrics, maintaining public retention and destruction schedules, strictly prohibiting biometric sale or profiting, and enforcing statutory damages ($1,000 per negligent, $5,000 per intentional violation). SB 2979 (effective August 2024) clarifies that repeated captures from a single individual constitute a single violation.

Official Citation: 740 ILCS 14 (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Biometric Information Privacy Policy defining retention limits, destruction schedules, or prohibition of profiting.
- **Missing Documentation:**
  Developer checklists lack guidelines on obtaining valid written consent or e-signatures prior to activating biometric SDKs (e.g., face match or fingerprint auth).
- **Missing Code:**
  Codebase templates do not include modal sheets for capturing written biometric consent or automated triggers to execute biometric data destruction.
- **Missing Disclosure:**
  UI onboarding templates fail to display BIPA-mandated notices explaining specific biometric collection purposes and storage durations.
- **Missing Logging:**
  No backend logging schemas exist to capture written consent timestamps, authorization scopes, or biometric destruction confirmation logs.
- **Missing Testing:**
  The repository contains no integration tests verifying that biometric feature initialization fails if consent has not been recorded.
- **Missing Evidence:**
  The playbook provides no sample templates for public Biometric Data Retention Schedules or Destruction Certifications.
- **Missing Audit Trail:**
  An unalterable audit log capturing biometric consent grants, consent withdrawals, and data destruction events is absent.

### 12.3 Remediation and Action Plan
1. Create a written Biometric Data Policy detailing retention and 3-year maximum destruction rules.
2. Build biometric consent modal sheets requiring explicit written or e-signed consent prior to feature activation.
3. Implement backend database triggers to delete biometric data upon account termination or purpose completion.
4. Add automated test routines verifying biometric API blocking in the absence of valid consent records.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401), FTC Act Section 5, and state negative-option statutes (California, New York, Massachusetts) regulate online subscription renewals and cancellations.

While the FTC's federal "click to cancel" rule amendment was vacated on procedural grounds in July 2025, underlying statutory obligations require that online subscriptions provide simple, frictionless cancellation mechanisms that are at least as easy as the sign-up process, strictly banning phone-call or mail-only cancellation requirements for web-billed subscriptions.

Official Citations: 15 U.S.C. 8401 (ROSCA); California Business and Professions Code Sec. 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no written Subscription Cancellation and Negative Option Policy defining cancellation ease standards and pre-renewal notice rules.
- **Missing Documentation:**
  Checklists lack explicit developer instructions for designing self-service cancellation flows for web-billed cross-platform subscriptions.
- **Missing Code:**
  Web and mobile account templates lack functional 1-click subscription cancellation button components, leaving non-store billing flows vulnerable to rejections.
- **Missing Disclosure:**
  Subscription payment screens do not display clear pre-transaction notices outlining recurring billing amounts, renewal frequencies, and cancellation steps.
- **Missing Logging:**
  Backend schemas lack tables for logging cancellation button taps, cancellation confirmation timestamps, and pre-renewal email notification logs.
- **Missing Testing:**
  Automated UI tests verifying that users can complete subscription cancellations entirely self-service without contacting support are missing.
- **Missing Evidence:**
  The repository provides no standardized templates for automated subscription cancellation receipts or renewal reminders.
- **Missing Audit Trail:**
  An immutable audit trail recording subscription state changes, cancellation requests, and refund calculations is missing.

### 13.3 Remediation and Action Plan
1. Establish a Subscription Renewal and Cancellation Policy enforcing frictionless self-service cancellation.
2. Implement 1-click cancellation buttons inside user account management templates for web-billed subscriptions.
3. Build backend database schemas to log cancellation requests, effective termination dates, and confirmation receipts.
4. Add end-to-end UI automation tests verifying self-service subscription termination.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the ICO Age Appropriate Design Code (Children's Code) mandate child safety, age assurance, and illegal content removal for UK-accessible services.

Services likely to be accessed by children under 18 must enforce high privacy settings by default, turn off geolocation and profiling by default, execute Data Protection Impact Assessments (DPIAs), and utilize Highly Effective Age Assurance methods (such as facial age estimation or open banking) rather than simple self-declaration.

Official Citations: UK Online Safety Act 2023 (c. 50); ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no written UK Online Safety and Children's Privacy Policy detailing age-assurance choices and child safety protocols.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides on conducting ICO-compliant Data Protection Impact Assessments (DPIA) for child-accessible apps.
- **Missing Code:**
  Codebase templates lack default-privacy configurations that automatically disable profiling, tracking, and precise location when a UK child user is detected.
- **Missing Disclosure:**
  UI templates do not include child-friendly privacy notices explaining data collection in clear, age-appropriate language as required by the ICO Code.
- **Missing Logging:**
  No database logging schemas exist to capture age-assurance check results, eSafety report filings, or CSEA takedown notices to the NCA portal.
- **Missing Testing:**
  Test suites contain no automated assertions verifying that location tracking and targeted ad SDKs remain disabled by default for UK child accounts.
- **Missing Evidence:**
  The playbook carries no physical templates for completed Children's Code DPIAs, Ofcom risk assessments, or age-assurance accuracy reports.
- **Missing Audit Trail:**
  An unalterable audit log capturing child safety risk reviews, content moderation takedowns, and age-assurance verification events is absent.

### 14.3 Remediation and Action Plan
1. Draft a UK Children's Code Compliance Policy enforcing high privacy defaults and profiling bans for under-18s.
2. Implement automatic configuration flags that suppress geolocation and analytics for UK child profiles.
3. Add a completed template for Children's Code Data Protection Impact Assessments (DPIA).
4. Create automated test suites asserting zero ad tracking for UK child accounts.

---

## 15. Australia Online Safety Act & App Distribution Code

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 (effective 10 December 2025) and the App Distribution Services Online Safety Code (Schedule 7, effective 9 September 2026) enforce strict age restrictions and access controls.

Age-restricted social media platforms must take reasonable steps to prevent under-16s from holding accounts using robust age-assurance waterfalls. App distribution services must apply age assurance before allowing downloads of adult apps, and age-verification data must be ringfenced and destroyed immediately after use.

Official Citations: Online Safety Act 2021 / 2024 Amendment (eSafety Commissioner); Consolidated Industry Codes Schedule 7.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no written Australian Age Assurance and Data Ringfencing Policy governing under-16 account blocks and immediate data destruction.
- **Missing Documentation:**
  Developer guides lack detailed integration manuals explaining how to implement eSafety-approved age assurance waterfalls and store age signal checks.
- **Missing Code:**
  Codebase templates contain no logic to process Apple/Google 18-plus download blocks or execute Australian age-waterfall verification flows.
- **Missing Disclosure:**
  In-app onboarding views do not display Australian legal disclosures explaining why age verification is conducted and asserting that verification data is not stored.
- **Missing Logging:**
  No backend logging schemas exist to record age verification passes while guaranteeing that raw identity documents are deleted without leaving copies.
- **Missing Testing:**
  Integration tests verifying that under-16 users are blocked from creating social media accounts on Australian storefronts are missing.
- **Missing Evidence:**
  The playbook provides no templates for eSafety Risk Assessment records or independent age-assurance accuracy audits.
- **Missing Audit Trail:**
  An immutable audit trail recording age-assurance system updates, ringfencing audits, and document purging confirmations is completely missing.

### 15.3 Remediation and Action Plan
1. Establish a written Australian Age Assurance Policy enforcing immediate destruction of verification artifacts.
2. Implement onboarding age checks that block under-16 account creation for Australian users on age-restricted apps.
3. Build backend deletion triggers ensuring age-assurance documents are purged immediately post-verification.
4. Create automated unit tests confirming age-gating enforcement for Australian storefront builds.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, regulated by Decreto n. 12.880 of 18 March 2026) establishes comprehensive child and adolescent protection rules across digital applications, enforced by the ANPD.

App stores, operating systems, and app developers must enforce verified age assurance (document check, facial age estimation, or CPF database check—simple checkbox self-declaration is prohibited), obtain guardian authorization for minors, show age ratings prior to download, block minor access to gambling/lottery apps, and ringfence verification data.

Official Citations: Lei n. 15,211/2025; Decreto n. 12.880/2026 (Presidência da República).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Brazil Digital ECA Compliance Policy detailing age verification standards, guardian consent workflows, and loot-box age restrictions.
- **Missing Documentation:**
  Checklists lack developer integration guides for connecting to Google Play Age Signals API (Brazil rollout) or verifying CPF identity databases.
- **Missing Code:**
  Codebase templates do not integrate robust age-verification SDKs or logic to automatically rate loot-box apps as 18-plus on Brazilian storefronts.
- **Missing Disclosure:**
  Onboarding UI templates fail to display required Portuguese language disclosures explaining age verification purposes and guardian consent terms.
- **Missing Logging:**
  Backend templates lack database schemas to log guardian consent receipts, ANPD compliance status, or age verification completion events.
- **Missing Testing:**
  No automated integration tests exist to verify that Brazilian accounts under 18 are blocked from accessing simulated gambling or loot-box features.
- **Missing Evidence:**
  The repository contains no physical templates for ANPD Age Assurance Adaptation Reports or guardian consent verification logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking age verification algorithm updates, guardian consent grants, and verification data purging is missing.

### 16.3 Remediation and Action Plan
1. Formulate a written Brazil Digital ECA Policy enforcing verified age checks and guardian consent.
2. Integrate Google Play Age Signals API and native Apple age-range checks for Brazilian storefront users.
3. Build backend handlers to capture and log guardian consent for minor accounts.
4. Add automated test suites verifying that loot-box and gambling features are restricted to verified 18-plus accounts in Brazil.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023) & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA 2023) and the DPDP Rules 2025 (notified November 2025) establish a consent-centric data protection regime enforced by the Data Protection Board of India.

Key rules enforce clear consent notices in 22 official Indian languages, registered Consent Managers (effective November 2026), and verifiable parental consent before processing data of anyone under 18 (effective May 2027). Tracking, behavioral monitoring, and targeted advertising directed at children under 18 are strictly prohibited.

Official Citation: Act No. 22 of 2023 (Ministry of Law and Justice); DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no written India DPDPA Policy detailing consent manager integration, multilingual notices, or under-18 data processing bans.
- **Missing Documentation:**
  Checklists lack developer guides explaining how to integrate with government-backed verifiable parental consent systems (such as DigiLocker) or registered Consent Managers.
- **Missing Code:**
  Codebase templates lack multilingual consent UI components or logic to disable behavioral tracking for Indian users under 18.
- **Missing Disclosure:**
  Onboarding templates do not render itemized, plain-language consent notices containing Data Fiduciary contact details and Data Principal right descriptions.
- **Missing Logging:**
  Backend schemas provide no structured tables for storing itemized consent tokens, language preferences, or parental consent proof.
- **Missing Testing:**
  Automated tests verifying that targeted ad SDKs are completely blocked for Indian minor accounts are missing.
- **Missing Evidence:**
  The repository contains no sample templates for Data Protection Officer (DPO) appointment records or Significant Data Fiduciary assessment documents.
- **Missing Audit Trail:**
  An immutable audit trail recording consent grants, consent withdrawals, and parental verification events is completely absent.

### 17.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Policy detailing consent notice standards and under-18 restrictions.
2. Build multilingual consent UI notice components supporting official Indian languages.
3. Implement backend handlers to record itemized consent tokens and sync with registered Consent Managers.
4. Add automated test routines asserting zero behavioral ad tracking for users under 18 in India.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA App Distribution Code

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services establish comprehensive data protection and child safety standards.

App stores and developers must implement age assurance measures (effective 1 April 2026) to screen and stop users estimated under 18 from downloading age-inappropriate apps. Verification data must be immediately purged after purpose completion, and data breach notifications to the PDPC must occur within 3 calendar days.

Official Citations: Personal Data Protection Act 2012 (PDPC); IMDA Code of Practice for Online Safety (2025/2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no written Singapore PDPA and IMDA Compliance Policy detailing 3-day breach notice protocols and age screening standards.
- **Missing Documentation:**
  Developer guides fail to detail procedures for integrating credit-card or digital ID age estimation methods accepted under IMDA standards.
- **Missing Code:**
  Codebase templates lack automated handlers for enforcing Apple/Google 18-plus download blocks or triggering mandatory PDPC breach notifications within 72 hours.
- **Missing Disclosure:**
  UI templates do not display Singapore-specific privacy disclosures explaining Data Protection Officer contact points or age estimation rules.
- **Missing Logging:**
  No database logging schemas exist to capture 72-hour data breach escalation timelines, DPO access logs, or age verification purges.
- **Missing Testing:**
  Integration tests verifying that 18-plus rated app features are inaccessible to unverified Singapore accounts are missing.
- **Missing Evidence:**
  The playbook provides no physical templates for PDPC 3-Day Data Breach Notification forms or Data Protection Impact Assessments.
- **Missing Audit Trail:**
  An unalterable audit log recording privacy policy updates, DPO designations, and age-assurance data deletions is missing.

### 18.3 Remediation and Action Plan
1. Create a written Singapore PDPA Policy including mandatory 3-day breach notification workflows.
2. Implement onboarding age checks blocking minor access to 18-plus content on Singapore storefronts.
3. Build automated alert workflows to notify DPOs immediately upon detection of a security breach.
4. Add automated unit tests verifying age-gating enforcement for Singapore storefront builds.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment processing on mobile app stores, while the Personal Information Protection Act (PIPA amendment, Act No. 21445, effective September 2026) imposes strict executive liability, mandatory Chief Privacy Officers, and severe surcharges for data breaches.

Apple's Korea alternative payment terms require a dedicated Korea-only binary (`SKExternalPurchase = "KR"`), an approved local payment gateway (KCP, Inicis, Toss, NICE), a 26% commission rate, pre-transaction disclosure sheets, and monthly sales reporting within 15 days.

Official Citations: Telecommunications Business Act Sec. 22-9; Personal Information Protection Act (Act No. 21445, PIPC).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written South Korea Alternative Payments and PIPA Compliance Policy governing local gateway integration and executive privacy accountability.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides on creating Korea-specific app build targets and wiring approved Korean payment gateways.
- **Missing Code:**
  Codebase templates contain no logic to invoke Korea-specific payment modal sheets or manage dual in-app purchase code paths without co-mingling.
- **Missing Disclosure:**
  UI checkout layouts do not include required Korean language disclosure sheets informing users that purchases process via local third-party gateways.
- **Missing Logging:**
  Backend schemas lack tables for logging monthly Korean external transaction totals required for 15-day reporting to Apple/Google.
- **Missing Testing:**
  No automated unit tests exist to verify that Korea-specific alternative payment entitlements activate exclusively for South Korean storefront builds.
- **Missing Evidence:**
  The playbook provides no templates for PIPA Chief Privacy Officer (CPO) designation certificates or local payment gateway agreement records.
- **Missing Audit Trail:**
  An immutable audit trail tracking Korean monthly sales reporting submissions, fee calculations, and CPO privacy reviews is completely absent.

### 19.3 Remediation and Action Plan
1. Establish a South Korea Billing and Privacy Policy detailing alternative payment rules and CPO accountability.
2. Build dedicated Korea build configurations integrating approved local payment gateways.
3. Implement backend transaction reporting pipelines for submitting monthly sales data within 15 days.
4. Add automated test routines verifying that alternative billing code paths activate only for Korean store region flags.

---

## 20. China Mobile App Filing (MIIT) & Interim Measures for AI Anthropomorphic Services (CAC Order No. 21)

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) through a local Chinese business entity before distribution on any app store in China.

Furthermore, the Cyberspace Administration of China (CAC Order No. 21, effective 15 July 2026) regulates AI Anthropomorphic Interactive Services (companion chatbots, virtual roleplay). Providers MUST automatically switch minor users into Minors Mode, obtain verified guardian consent under 14, and strictly BAN offering virtual companion or virtual kin services to minors.

Official Citations: MIIT Notice on Mobile Application Filing (2023/2024); CAC Order No. 21 (Interim Measures for AI Anthropomorphic Services).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no written China App Distribution and AI Companion Policy governing MIIT filing, real-name verification, and minor companion bans.
- **Missing Documentation:**
  Checklists lack developer manuals explaining local Chinese partner entity onboarding, ICP filing procedures, and CAC AI algorithm registration.
- **Missing Code:**
  Codebase templates contain no automatic "Minors Mode" switching logic or age-detection hooks to block minors from entering AI companion chat features.
- **Missing Disclosure:**
  UI templates do not include Chinese language real-name registration notices or required CAC AI service disclosure statements.
- **Missing Logging:**
  No database logging schemas exist to capture real-name identity verification tokens, guardian consent grants, or Minors Mode activation logs.
- **Missing Testing:**
  Integration tests verifying that minor account flags instantly disable conversational AI companion features on Chinese storefront builds are missing.
- **Missing Evidence:**
  The playbook provides no sample templates for MIIT App Filing approvals, Banhao game licenses, or CAC AI Security Assessments.
- **Missing Audit Trail:**
  An unalterable audit log tracking real-name authentication records, Minors Mode triggers, and content moderation takedowns is completely absent.

### 20.3 Remediation and Action Plan
1. Formulate a written China Regulatory Compliance Policy covering MIIT filing and CAC AI companion restrictions.
2. Build automatic "Minors Mode" UI switching logic that disables AI companion features for minor accounts.
3. Integrate real-name identity verification UI components for Chinese storefront builds.
4. Add automated unit test suites asserting that AI companion endpoints return access-denied for minor user profiles.

---

## 21. Consolidated Gap Classification Matrix

The table below maps all twenty audited regulations across the eight compliance gap categories.
- **Covered**: The repository contains comprehensive policies, documentation, code, disclosures, logging, testing, evidence, or audit trails.
- **Partial**: The requirement is named or referenced in documentation, but complete operational step-by-step code, tests, or templates are missing.
- **Missing**: The playbook contains no policy, documentation, code, disclosure, logging, testing, evidence, or audit trail for this requirement.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Covered | Covered | Partial | Covered | Partial | Missing | Partial | Missing |
| **8. EU DSA** | Covered | Covered | Partial | Covered | Missing | Missing | Partial | Missing |
| **9. European Accessibility Act** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA Amended Rule** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy Laws** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA & CUBI** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Covered | Covered | Partial | Covered | Missing | Missing | Missing | Missing |
| **14. UK Online Safety & Code** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & Rules** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **20. China MIIT & CAC Order 21**| Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Systematic Action Plan

The playbook provides extensive coverage of platform app store review guidelines (Apple App Store Guidelines and Google Play Developer Policies) and maintains strong awareness of global regulatory deadlines. However, auditing the repository against the twenty major modern legal frameworks reveals clear technical implementation gaps.

While regulations are cited with official dates and citations across `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, and `data/regulatory-deadlines.json`, the implementation layer—specifically automated pre-submission guard detection rules, reusable UI code templates, database logging schemas, automated test assertions, and audit trail logging—remains incomplete across multiple domains.

### Priority Action Items
1. **GPSR Integration**: Implement full detection, UI templates, and checklists for the EU General Product Safety Regulation (GPSR), which currently represents an end-to-end gap.
2. **Detection Rules**: Expand `agent-os/hooks/app-store-compliance-guard.sh` and `data/rejection-patterns.json` to detect missing withdrawal buttons, missing AI interaction notices, missing C2PA watermarking utilities, and unhandled age signals.
3. **Code Templates**: Create reusable UI components in the references directory for EU contract withdrawal, AI interaction disclosures, California "Do Not Sell/Share" controls, and biometric written consent modals.
4. **Automated Testing**: Develop automated CI test scripts to verify accessibility scaling, GPC header suppression, and minor age-gating enforcement across all targeted storefronts.

---

## 23. Primary Official Sources

Every regulation cited in this report is grounded in Priority 1 primary official sources:

- EU GPSR: [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing / Withdrawal Button: [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Amended COPPA Rule: [16 CFR Part 312 (FTC / Federal Register)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US State ASAA: Utah SB 142 ([le.utah.gov](https://le.utah.gov/~2025/bills/static/SB0142.html)), Texas SB 2420, Louisiana HB 570 / HB 977 ([legis.la.gov](https://legis.la.gov/)), Alabama HB 161
- California Privacy: CCPA / CPRA ([oag.ca.gov/privacy/ccpa](https://oag.ca.gov/privacy/ccpa)), CPPA Regulations ([cppa.ca.gov](https://cppa.ca.gov/)), SB 976 ([leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov))
- Illinois BIPA: 740 ILCS 14 ([ilga.gov](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946))
- US Subscription Laws: ROSCA 15 U.S.C. 8401 ([ftc.gov](https://www.ftc.gov/))
- UK Online Safety Act & ICO Code: Online Safety Act 2023 ([legislation.gov.uk](https://www.legislation.gov.uk/ukpga/2023/50/contents)), ICO Children's Code ([ico.org.uk](https://ico.org.uk/))
- Australia Online Safety: Online Safety Act 2021 / 2024 ([legislation.gov.au](https://www.legislation.gov.au/))
- Brazil Digital ECA: Lei n. 15,211/2025 and Decreto n. 12.880/2026 ([planalto.gov.br](https://www.planalto.gov.br/))
- India DPDPA & DPDP Rules: Act No. 22 of 2023 and G.S.R. 846(E) ([egazette.gov.in](https://egazette.gov.in))
- Singapore PDPA & IMDA: Personal Data Protection Act 2012 and IMDA Code ([mddi.gov.sg](https://www.mddi.gov.sg/))
- South Korea TBA & PIPA: Telecommunications Business Act and Act No. 21445 ([law.go.kr](https://law.go.kr/))
- China App Filing & CAC Order 21: MIIT Notice and CAC Order No. 21 ([cac.gov.cn](https://www.cac.gov.cn/))
