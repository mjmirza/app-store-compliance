# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping software globally, checking honestly how far this repository carries each requirement, what it only mentions in passing, and what remains missing.

Read this as an actionable work list for the playbook, not as legal advice. Where an item is identified as missing, it indicates a gap in this repository's policies, documentation, code templates, disclosures, logging, testing, evidence, or audit trails. Each framework is systematically audited across all eight compliance categories.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere strictly to the repository source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no graphical emoticons or unicode symbols.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces Directive 2001/95/EC to address digital products, online marketplaces, and modern software supply chains. The GPSR mandates that online interfaces display product safety warnings, instructions, manufacturer identity, and EU responsible person contact details.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook provides no template General Product Safety Policy to determine whether a software offering falls under GPSR or how to assign responsible entities.
- **Missing Documentation:** Lacks developer guidebooks and UI placement checklists for displaying GPSR-mandated safety notices and manufacturer contact information on EU app listings.
- **Missing Code:** Detection recipes and compliance guard scripts lack rules to scan for GPSR parameters, and mock UIs contain no components for product safety metadata.
- **Missing Disclosure:** Interface templates lack placeholders for manufacturer name, registered trade name, postal address, and electronic contact details required under Article 19.
- **Missing Logging:** No schemas or provisions exist for logging product safety incidents, safety recalls, or consumer safety warnings.
- **Missing Testing:** No automated UI or integration tests verify that safety disclosures and contact information dynamically display for EU users.
- **Missing Evidence:** Missing sample Technical Documentation sheets, safety risk assessments, or proof of designated EU Responsible Person appointment.
- **Missing Audit Trail:** No historical tracking system records safety notice revisions, risk reviews, or corrective action history.

### 1.3 Remediation and Action Plan
1. Draft a General Product Safety Policy establishing EU Responsible Person criteria and product safety classification rules.
2. Incorporate GPSR metadata fields into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in `references/` demonstrating compliant product detail pages with safety warnings and contact details.
4. Implement automated CI scripts to verify safety disclosures on target EU product pages.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 (European Production and Preservation Orders) and Directive (EU) 2023/1544 (Legal Representatives). Mandatory enforcement begins on 18 August 2026. Judicial authorities in EU Member States can issue orders directly to service providers offering services in the EU, requiring user data production within 10 days for standard orders and 8 hours for critical emergency orders.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a written Law Enforcement Request Policy defining roles, verification protocols, and emergency escalation paths for EU judicial orders.
- **Missing Documentation:** Operational runbooks for executing 10-day standard orders and 8-hour emergency extraction requests are missing.
- **Missing Code:** Backend mock scripts lack secure API endpoints or utilities to filter, package, and encrypt target user data under legal orders.
- **Missing Disclosure:** Public privacy policy templates do not explicitly notify EU users that data may be produced to EU law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:** Missing database schemas for logging legal request metadata, officer credentials, production timelines, and output manifests.
- **Missing Testing:** No simulated integration tests exist to execute an emergency 8-hour data retrieval and packaging workflow under stress conditions.
- **Missing Evidence:** Lacks sample EPOC and EPOC-PR certificate verification artifacts and designated EU legal representative appointment records.
- **Missing Audit Trail:** Unalterable, cryptographically signed audit logs tracking legal request receipt, administrative access, and data transfers are absent.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol covering EPOC/EPOC-PR intake, authentication, and emergency escalation.
2. Formally document EU legal representative designation protocols.
3. Build backend data export scripts capable of executing encrypted extraction within 8 hours.
4. Create an immutable logging table for law enforcement order processing.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU regarding distance financial services contracts, mandating a prominent, easily accessible "withdrawal button" on online interfaces. Applies to distance financial services (insurance, credit, payment, investment) with Member States applying rules from 19 June 2026. Grants a 14-day statutory withdrawal period executed via a direct, frictionless path.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Missing a formal Consumer Contract Revocation Policy clarifying statutory 14-day withdrawal rights for distance contracts.
- **Missing Documentation:** Lacks UI design specifications defining button prominence, placement, font size, and workflow friction limits.
- **Missing Code:** Front-end templates and payment mock implementations contain no code for a functional withdrawal button or modal sheet.
- **Missing Disclosure:** Subscription and checkout interfaces fail to disclose the statutory 14-day right of withdrawal or revocation consequences.
- **Missing Logging:** No logging schemas capture withdrawal clicks, cancellation timestamps, confirmation transmissions, or refund triggers.
- **Missing Testing:** Lacks automated UI tests verifying that the withdrawal flow completes self-service without requiring manual customer support intervention.
- **Missing Evidence:** Missing standardized withdrawal notice templates, digital revocation receipts, and refund confirmation records.
- **Missing Audit Trail:** Lacks historical logging of interface changes, cancellation rate metrics, or revocation compliance audits.

### 3.3 Remediation and Action Plan
1. Create a Consumer Contract Revocation Policy aligned with Directive (EU) 2023/2673.
2. Develop a reusable "Withdrawal Button" UI component for account settings templates.
3. Add backend events and logs for tracking contract revocation requests.
4. Write Playwright/UI automated tests confirming frictionless contract withdrawal.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minor access to mobile applications, purchases, and updates. Developers must query age categories (via Apple Declared Age Range API or Google Play Age Signals API), process verifiable parental consent for minor accounts, re-request consent on major app updates, and immediately delete raw age-verification records.

Official Citations: Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161.

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a state-specific Minor Age Assurance Policy detailing state detection, age band mapping, and account restriction rules.
- **Missing Documentation:** Missing integration guides explaining how to query native age APIs (Apple `DeclaredAgeRange` / Google `age-signals`) in unified cross-platform codebases.
- **Missing Code:** Codebase mocks lack native hooks to query platform age APIs or restrict minor functionality dynamically based on state age signals.
- **Missing Disclosure:** Onboarding interfaces do not inform users that age categories are requested under state accountability laws or that parental consent is mandatory for minors.
- **Missing Logging:** Missing backend logs for recording parental consent grants, consent revocations (`RESCIND_CONSENT`), or automated raw data purging.
- **Missing Testing:** Integration tests do not verify that minor accounts without consent are restricted from downloads, purchases, or major updates.
- **Missing Evidence:** Missing sample parental consent forms, age verification vendor certificates, or data destruction logs.
- **Missing Audit Trail:** Immutable audit records tracking historical age-assurance rollouts, policy updates, and verification data deletions are absent.

### 4.3 Remediation and Action Plan
1. Formulate a Minor Age Assurance and Data Minimization Policy for ASAA state jurisdictions.
2. Implement cross-platform native wrappers for Apple Declared Age Range and Google Play Age Signals APIs.
3. Write database triggers for immediate deletion of raw age validation artifacts.
4. Add automated unit tests verifying minor purchase blocks in the absence of valid parental consent flags.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) became mandatory on 2 February 2025. It obligates AI providers and deployers to ensure a sufficient level of AI literacy among staff and operators dealing with AI systems, taking into account their technical knowledge, experience, education, and context.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no internal AI Literacy Policy defining training competencies, refresh schedules, or role-based requirements.
- **Missing Documentation:** Developer guidebooks lack instruction on Article 4 compliance expectations or AI safety curriculum standards.
- **Missing Code:** Not directly applicable to product binaries, but missing automated compliance checks or repository lints verifying active training log currency.
- **Missing Disclosure:** B2B contracts, public documentation, or recruitment notices do not disclose compliance with Article 4 AI literacy standards.
- **Missing Logging:** Lacks an active, centralized training log (`AI_LITERACY_LOG.md`) to record employee training dates, course modules, and verification statuses.
- **Missing Testing:** No CI lints or pre-commit checks verify that developers touching AI code paths hold active literacy certifications.
- **Missing Evidence:** Missing sample training materials, course completion certificates, or competency assessment records.
- **Missing Audit Trail:** Lacks historical logging of policy reviews, curriculum updates, or employee training progress over time.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy establishing mandatory training topics (safety, privacy, bias, risk mitigation).
2. Establish a maintained `AI_LITERACY_LOG.md` file tracking team training completions.
3. Implement a CI script warning when training logs have not been reviewed within 12 months.
4. Document sample training curricula in `references/guidelines/by-app-type/ai-and-generative-apps.md`.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act mandates transparency obligations for AI systems, taking effect on 2 August 2026. Requires informing natural persons when interacting with AI systems (Art. 50(1)), marking generative AI outputs in machine-readable formats (Art. 50(2)), and disclosing deepfakes or synthetic media (Art. 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an AI Transparency and Output Watermarking Policy governing disclosure triggers and machine-readable output marking.
- **Missing Documentation:** Developer guidebooks lack detailed technical instructions on implementing C2PA metadata, cryptographic watermarking, or deepfake disclosures.
- **Missing Code:** Codebase templates lack watermarking helper classes, metadata injectors, or C2PA header utilities for generated text, image, or audio assets.
- **Missing Disclosure:** Conversational UI templates do not display required disclosures ("You are interacting with an AI assistant") at initial user exposure.
- **Missing Logging:** Lacks logging schemas to record that transparency notices were rendered during a user session.
- **Missing Testing:** Automated tests do not scan generated media outputs to confirm the presence of machine-readable synthetic watermarks or C2PA headers.
- **Missing Evidence:** Lacks independent validation reports for watermark durability or content moderation filter efficacy.
- **Missing Audit Trail:** Historical audit records tracking changes to AI disclosure text, model updates, or watermarking specs are missing.

### 6.3 Remediation and Action Plan
1. Create an AI Transparency and Output Marking Policy aligned with Article 50.
2. Inject immediate disclosure notices into conversational and generative UI templates.
3. Build C2PA metadata injection utilities into media generation pipelines.
4. Add automated test runners that inspect generated file headers for machine-readable watermarks.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms and enforces interoperability, anti-steering prohibition removal, alternative payment processing, and out-of-app purchasing links. Applies in full from 7 March 2024.

Official Citation: Regulation (EU) 2022/1925.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an EU Alternative Distribution and Anti-Steering Policy outlining entitlement requirements and reporting duties.
- **Missing Documentation:** Integration documentation lacks step-by-step guidance for configuring `com.apple.developer.storekit.external-purchase-link` or alternative payment flows.
- **Missing Code:** Mock billing services lack code implementations for handling external purchase web handoffs or calculating 5% Core Technology Commission reporting.
- **Missing Disclosure:** Interface templates fail to provide compliant external purchase modal sheets or fee transparency disclosures.
- **Missing Logging:** Missing database schemas for capturing external link clicks, transaction completions, and monthly reporting metrics.
- **Missing Testing:** Automated UI tests do not verify that external purchase links open compliant web views without embedded store interference.
- **Missing Evidence:** Lacks sample StoreKit entitlement approval records or monthly EU transaction reporting manifests.
- **Missing Audit Trail:** Unalterable audit logs capturing entitlement configuration changes, link URL modifications, and reporting submissions are absent.

### 7.3 Remediation and Action Plan
1. Publish an EU Alternative Payment and Out-of-App Purchase Guide.
2. Build sample StoreKit external purchase link integration components.
3. Add backend logging schemas for tracking monthly out-of-app transaction metrics.
4. Implement automated link navigation tests for EU alternative payment flows.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) applies fully from 17 February 2025. Requires trader status declarations, illegal content notice-and-action mechanisms, dark pattern prohibitions, recommender system transparency, and minor protection measures for online platforms.

Official Citation: Regulation (EU) 2022/2065.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Missing a formal DSA Content Moderation and Notice-and-Action Policy defining illegal content handling workflows.
- **Missing Documentation:** Lacks developer guidebooks for implementing in-app illegal content reporting buttons or trader verification workflows.
- **Missing Code:** UI templates contain no functional notice-and-action report forms, recommender system toggle switches, or trader identity displays.
- **Missing Disclosure:** App metadata and profile templates fail to display verified trader contact details (D-U-N-S, address, email, phone) or recommender parameter descriptions.
- **Missing Logging:** Missing database tables for logging illegal content reports, moderation decisions, statement of reasons, and user appeals.
- **Missing Testing:** No integration tests verify that illegal content reports properly route to moderation queues or issue automated receipts within statutory timelines.
- **Missing Evidence:** Lacks sample DSA transparency reports, moderation auditor certificates, or trader verification records.
- **Missing Audit Trail:** Immutable audit logs recording moderation decision histories, appeal outcomes, and algorithmic recommender changes are absent.

### 8.3 Remediation and Action Plan
1. Draft a DSA Notice-and-Action Moderation Protocol.
2. Implement in-app content reporting UI components and statement-of-reasons logging schemas.
3. Create metadata templates containing verified trader contact fields.
4. Build automated tests verifying report submission workflows and receipt generation.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) applies from 28 June 2025. Mandates accessibility for e-commerce, banking, e-books, and mobile services reaching EU consumers, harmonized via standard EN 301 549 (WCAG 2.1 Level AA conformance).

Official Citation: Directive (EU) 2019/882.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an organizational Digital Accessibility Policy establishing WCAG 2.1 AA and EN 301 549 compliance standards.
- **Missing Documentation:** Guidebooks lack explicit developer instructions for accessibility traits, screen reader support, Dynamic Type scaling, and minimum touch target sizes.
- **Missing Code:** Mobile UI templates lack accessible labels, semantic traits, contrast compliance, or Reduce Motion support in custom controls.
- **Missing Disclosure:** Lacks a published Accessibility Statement template disclosing conformance levels, accessible alternatives, and feedback mechanisms.
- **Missing Logging:** Missing logging mechanisms for user-submitted accessibility feedback, barrier reports, or remediation tracking.
- **Missing Testing:** Automated test suites lack static accessibility scanners (`accessibility-audit.py`) integrated into CI/CD pipelines.
- **Missing Evidence:** Missing formal accessibility audit reports, VPAT/WCAG evaluation sheets, or screen reader usability test records.
- **Missing Audit Trail:** Historical tracking of accessibility bug remediation, UI redesigns, and statement updates is completely absent.

### 9.3 Remediation and Action Plan
1. Formulate a Comprehensive Digital Accessibility Policy aligned with EN 301 549.
2. Enhance UI templates with screen reader traits, Dynamic Type, and high-contrast styling.
3. Publish a standardized Accessibility Statement template.
4. Integrate `scripts/accessibility-audit.py` into automated PR review checks.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) and the Amended COPPA Rule (enforceable 22 April 2026) regulate services directed to children under 13 or with actual knowledge of child users. Mandates verifiable parental consent, separate opt-ins for third-party disclosures, written retention policies, written information security programs, and biometric identifier protections.

Official Citation: 16 CFR Part 312.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a written Children's Privacy and Data Retention Policy complying with 312.10 and 312.8 security program duties.
- **Missing Documentation:** Developer checklists lack step-by-step instructions for implementing new verifiable parental consent methods (knowledge-based, facial match to ID).
- **Missing Code:** Mock codebases lack parental gates, separate opt-in consent flows for targeted advertising, or automated retention purge scripts.
- **Missing Disclosure:** Privacy notices fail to provide clear 312.4 direct notices to parents or explicit disclosures regarding biometric identifier collection.
- **Missing Logging:** Missing backend database schemas for recording verifiable parental consent grants, consent revocations, and data deletion events.
- **Missing Testing:** No automated tests verify that child-directed flows block third-party ad SDK initialization prior to consent verification.
- **Missing Evidence:** Missing FTC-approved Safe Harbor certificates, annual security risk assessments, or written retention schedules.
- **Missing Audit Trail:** Immutable logs capturing consent history, data purge executions, and annual COPPA policy reviews are absent.

### 10.3 Remediation and Action Plan
1. Create a COPPA 2026 Compliant Children's Data Policy and Retention Schedule.
2. Build UI components for dual parental consent and direct parent notification.
3. Write automated tests confirming SDK suppression in child-directed app modes.
4. Establish an immutable parental consent logging schema.

---

## 11. California Consumer Privacy Act / Privacy Rights Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
CCPA/CPRA (Cal. Civ. Code § 1798.100 et seq.) and CPPA 2026 Regulations enforce consumer privacy rights for California residents. Requires notices at collection, rights to know/delete/correct, opt-outs for sale/sharing/profiling, Global Privacy Control (GPC) support, and sensitive personal info limits. Automated decision-making technology (ADMT) rules take effect 1 January 2027.

Official Citation: Cal. Civ. Code § 1798.100 et seq.; 11 CCR § 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a written California Privacy Policy and Automated Decision-Making Policy covering CPRA 2026 regulatory updates.
- **Missing Documentation:** Guidebooks lack technical instructions on parsing the `Sec-GPC` header in webviews or mapping native opt-out signals.
- **Missing Code:** Codebase templates lack middleware to detect GPC headers, process "Do Not Sell/Share" requests, or enforce sensitive data processing limits.
- **Missing Disclosure:** Onboarding interfaces lack Notice at Collection templates, "Do Not Sell or Share My Personal Information" links, or ADMT notices.
- **Missing Logging:** Missing logging schemas to record consumer rights requests (know, delete, correct, opt-out), fulfillment statuses, and GPC signal receptions.
- **Missing Testing:** No automated integration tests verify that detecting a GPC header automatically suppresses third-party tracking scripts.
- **Missing Evidence:** Missing annual CPPA cybersecurity audit certifications, risk assessment reports, or consumer request metrics logs.
- **Missing Audit Trail:** Historical audit records tracking privacy policy revisions, GPC handling updates, and consumer request fulfillment timelines are absent.

### 11.3 Remediation and Action Plan
1. Draft a CPRA 2026 Privacy Policy and ADMT Governance Document.
2. Implement GPC header detection middleware in webviews and API handlers.
3. Build UI templates with "Do Not Sell/Share" and "Limit Sensitive Data" toggles.
4. Add automated tests confirming GPC header signal enforcement.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) regulates the collection, capture, purchasing, receiving, storing, and use of biometric identifiers or information. Requires written notice, written release prior to collection, public retention/destruction schedules, strict prohibition on sale or profiting, and security controls. SB 2979 (August 2024) clarified per-person violation limits.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a BIPA Biometric Governance Policy establishing mandatory written releases, retention limits, and destruction protocols.
- **Missing Documentation:** Guidebooks lack developer instructions for implementing BIPA-compliant consent flows prior to initializing SDKs processing biometric data.
- **Missing Code:** Templates contain no code for rendering written biometric consent modals, capturing electronic signatures, or executing 3-year maximum storage purges.
- **Missing Disclosure:** Privacy notices fail to provide explicit disclosures detailing specific biometric identifiers collected, purpose, and storage duration.
- **Missing Logging:** Missing database schemas for capturing written release timestamps, e-signatures, consent versions, and destruction confirmation events.
- **Missing Testing:** Automated tests do not verify that biometric data capture (e.g., face match, voiceprint) is blocked until a valid signed release is recorded.
- **Missing Evidence:** Missing public retention and destruction schedule documents, security audit logs, or third-party vendor compliance agreements.
- **Missing Audit Trail:** Immutable audit records logging biometric data lifecycle events, consent grants, and scheduled deletions are absent.

### 12.3 Remediation and Action Plan
1. Draft a Biometric Governance Policy and Public Retention Schedule.
2. Create BIPA written release modal sheet components with e-signature capture.
3. Build database triggers executing automated biometric data destruction within 3 years or when purpose expires.
4. Implement automated integration tests validating consent-gated biometric SDK initialization.

---

## 13. US Subscription Cancellation (Negative Option / ROSCA)

### 13.1 Regulatory Overview and Background
Regulated under FTC Act Section 5, ROSCA (15 U.S.C. § 8401), and state negative option statutes (California Cal. Bus. & Prof. Code § 17600, New York, Massachusetts). Requires clear terms before billing, affirmative consent, and a simple, frictionless cancellation mechanism ("click-to-cancel") at least as easy as the enrollment path. Binds web/off-store subscription billing.

Official Citations: 15 U.S.C. § 8401; Cal. Bus. & Prof. Code § 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Subscription Management and Negative Option Policy governing web-billed and off-store subscription cancellation mechanics.
- **Missing Documentation:** Guidebooks lack UI design rules specifying that online cancellation paths must not require phone calls, letters, or multi-step retention dark patterns.
- **Missing Code:** Off-store subscription templates contain no self-service cancellation interface code, one-click cancellation endpoints, or automated refund handlers.
- **Missing Disclosure:** Checkout flows fail to display clear pre-transaction disclosures of recurring charges, billing frequency, and simple cancellation instructions.
- **Missing Logging:** Missing database schemas for capturing cancellation button clicks, request timestamps, confirmation email dispatches, and refund status updates.
- **Missing Testing:** No automated UI tests verify that a user can execute a full subscription cancellation online in the same number of steps as enrollment.
- **Missing Evidence:** Missing standardized cancellation confirmation receipt templates, refund transaction records, or negative option audit logs.
- **Missing Audit Trail:** Immutable audit logs recording subscription flow modifications, cancellation success rates, and customer dispute histories are absent.

### 13.3 Remediation and Action Plan
1. Create a Subscription Transparency and Click-to-Cancel Policy.
2. Build self-service online cancellation UI components for off-store billing.
3. Write automated end-to-end tests validating frictionless online subscription cancellation.
4. Add backend event logging for subscription status changes and cancellation receipts.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and ICO Age Appropriate Design Code establish strict child safety and age assurance standards for services accessible by UK children under 18. Requires Highly Effective Age Assurance (facial age estimation, open banking, ID check), high privacy by default, geolocation off, profiling off, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: Online Safety Act 2023 c. 50; Data Protection Act 2018 s. 123.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Child Safety and Age-Appropriate Design Policy defining age assurance waterfalls and high-privacy defaults.
- **Missing Documentation:** Guidebooks lack step-by-step instructions for completing a UK Children's Code DPIA or integrating Ofcom-approved age assurance APIs.
- **Missing Code:** Codebase templates lack default settings toggles (geolocation disabled, profiling off, search engine indexing off) for UK minor accounts.
- **Missing Disclosure:** Onboarding interfaces fail to inform UK users of age assurance methods, safety risk assessments, or child safety controls.
- **Missing Logging:** Missing database schemas for logging age assurance verification results, DPIA completion dates, and CSEA portal incident reports.
- **Missing Testing:** Automated tests do not verify that geolocation and profiling services are forcibly disabled by default for UK child accounts.
- **Missing Evidence:** Missing completed ICO Children's Code DPIA templates, Ofcom risk assessment summaries, or age verification vendor certifications.
- **Missing Audit Trail:** Immutable audit logs recording age verification execution, safety feature toggles, and risk assessment updates are absent.

### 14.3 Remediation and Action Plan
1. Draft a UK Children's Code Policy and DPIA Framework.
2. Implement code wrappers for high-privacy defaults (geolocation and profiling suppressed for minors).
3. Create an immutable log table for age assurance verification results.
4. Build automated tests verifying default privacy flag states for UK user profiles.

---

## 15. Australia Online Safety & Social Media Minimum Age Act

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 and Privacy Act APP 1.7-1.9 amendments require age-restricted platforms to take reasonable steps to prevent under-16s from holding accounts, ringfence/destroy age data, and disclose automated decision-making in privacy policies. App Distribution Services Code (Schedule 7) mandates app-store age controls from September 2026.

Official Citations: Online Safety Act 2021; Privacy Act 1988 (as amended 2024).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Minor Account Restriction and ADM Disclosure Policy establishing under-16 account blocking and Privacy Act compliance.
- **Missing Documentation:** Guidebooks lack instructions on integrating eSafety-approved age assurance methods and ringfencing verification data.
- **Missing Code:** Codebase mocks lack logic to block under-16 registrations in Australia or automatically purge age assurance data post-verification.
- **Missing Disclosure:** Privacy policies lack required disclosures explaining personal information types processed by automated decision-making (ADM) systems.
- **Missing Logging:** Missing database schemas for logging age verification attempts, under-16 rejection events, and immediate data destruction logs.
- **Missing Testing:** No automated tests verify that Australian IP/locale registrations for under-16 users are blocked and verification data deleted.
- **Missing Evidence:** Missing eSafety compliance self-assessment records, age data destruction receipts, or ADM privacy impact reports.
- **Missing Audit Trail:** Immutable logs recording age-assurance algorithm updates, ADM disclosure revisions, and regulatory reporting are absent.

### 15.3 Remediation and Action Plan
1. Formulate an Australian Age Assurance and ADM Disclosure Policy.
2. Build native age validation wrappers with immediate post-verification data purging.
3. Update privacy policy templates with APP 1.7-1.9 automated decision-making notices.
4. Add automated tests confirming under-16 registration blocks for Australian locales.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil Digital ECA (Law 15,211/2025 and Decreto n. 12.880/2026) mandates strict age verification for digital services accessed by children and adolescents in Brazil, enforced from 17 March 2026 by ANPD. Rejects simple self-declaration checkboxes; requires document checks, facial age estimation, or CPF database validation, with mandatory 18+ download blocks for gambling/adult content.

Official Citations: Lei n. 15.211/2025; Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazil Digital ECA Compliance Policy governing age assurance, parental authorization, and ANPD data protection rules.
- **Missing Documentation:** Guidebooks lack developer instructions for connecting to CPF validation endpoints or executing ANPD-approved facial age estimation.
- **Missing Code:** UI templates contain no ANPD-compliant age verification modal sheets, guardian authorization flows, or 18+ content gates.
- **Missing Disclosure:** Onboarding interfaces do not display required disclosures informing Brazilian parents/guardians of age verification and data rights.
- **Missing Logging:** Missing database schemas for logging CPF verification statuses, age signal receptions, guardian consents, and contestation requests.
- **Missing Testing:** Automated tests do not verify that Brazilian accounts without ANPD-approved age validation are blocked from restricted content.
- **Missing Evidence:** Missing ANPD age assurance audit reports, CPF API integration certifications, or guardian consent documentation.
- **Missing Audit Trail:** Immutable logs tracking age validation decisions, guardian authorizations, and ANPD regulatory audit reports are absent.

### 16.3 Remediation and Action Plan
1. Create a Brazil Digital ECA Compliance and Guardian Consent Policy.
2. Build UI components for CPF/facial age validation and guardian authorization.
3. Add backend schemas for logging age verification results and contestations.
4. Write automated integration tests enforcing 18+ gates for Brazilian user locales.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India DPDPA 2023 and DPDP Rules 2025 enforce strict data protection obligations. Rule 4 (Consent Managers) takes effect 13 November 2026; rules 3, 5-16, 22-23 (verifiable parental consent, notice, child tracking prohibition) apply from 13 May 2027. Children defined as under 18; requires verifiable parental consent (e.g., via DigiLocker) and prohibits behavioral tracking or targeted ads to minors.

Official Citations: Act No. 22 of 2023; DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India DPDPA Data Protection and Minor Protection Policy defining parental consent and consent manager interoperability.
- **Missing Documentation:** Guidebooks lack instructions for integrating with registered Consent Managers or DigiLocker-backed parental verification systems.
- **Missing Code:** Codebase mocks contain no code for multi-lingual consent notices (22 scheduled languages), DigiLocker consent flows, or minor ad-tracking suppression.
- **Missing Disclosure:** Privacy notices fail to present clear, itemized consent requests in English and scheduled Indian languages as required under Rule 3.
- **Missing Logging:** Missing database schemas for capturing Consent Manager tokens, DigiLocker verification IDs, parental consents, and withdrawal requests.
- **Missing Testing:** Automated tests do not verify that behavioral tracking scripts are suppressed for Indian users identified as under 18.
- **Missing Evidence:** Missing Data Protection Officer (DPO) appointment records, Consent Manager integration certificates, or parental consent audit sheets.
- **Missing Audit Trail:** Immutable logs capturing consent notices served, language selections, consent grants, and DPDPA compliance reviews are absent.

### 17.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Policy and Consent Manager Protocol.
2. Build multi-lingual consent notice UI components supporting scheduled Indian languages.
3. Implement automated tests verifying ad tracking suppression for under-18 Indian accounts.
4. Create database schemas for logging Consent Manager verification tokens.

---

## 18. Singapore PDPA & IMDA Code of Practice for Online Safety

### 18.1 Regulatory Overview and Background
Singapore Personal Data Protection Act (PDPA) and IMDA Code of Practice for Online Safety for App Distribution Services require robust data governance, 3-day breach notification, and mandatory age assurance from 1 April 2026. App stores and services must screen and stop users under 18 from downloading age-inappropriate content, with immediate destruction of age verification data post-use.

Official Citations: Personal Data Protection Act 2012; IMDA Code of Practice (2025).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore Data Protection and IMDA Online Safety Policy covering breach reporting and age-assurance data destruction.
- **Missing Documentation:** Guidebooks lack developer instructions on handling IMDA age assurance signals or reporting priority online harms to the Online Safety Commission.
- **Missing Code:** UI templates contain no code for parsing Singapore age signals, enforcing 18+ download blocks, or executing immediate verification data deletion.
- **Missing Disclosure:** Privacy notices fail to disclose 3-day breach notification protocols, DPO contact details, or age-assurance data minimization practices.
- **Missing Logging:** Missing database schemas for capturing age verification attempts, 3-day breach notification logs, and data destruction confirmations.
- **Missing Testing:** Automated tests do not verify that raw age verification credentials collected for Singapore accounts are immediately purged from memory and storage.
- **Missing Evidence:** Missing designated DPO registration records, IMDA compliance self-assessments, or breach notification runbooks.
- **Missing Audit Trail:** Immutable audit logs capturing breach reports, age verification data purges, and IMDA regulatory reviews are absent.

### 18.3 Remediation and Action Plan
1. Formulate a Singapore PDPA and IMDA Online Safety Compliance Policy.
2. Implement backend hooks for 3-day breach notification workflows and age data purging.
3. Add UI components for displaying DPO contact details and age safety warnings.
4. Build automated tests verifying zero retention of raw age verification data.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea Telecommunications Business Act mandates alternative in-app payment options (26% commission, StoreKit external entitlement `com.apple.developer.storekit.external-purchase` for KR, custom modal sheet, monthly reporting). Amended PIPA (Act No. 21445, effective 11 September 2026) imposes CEO/CPO accountability, board-approved CPO seats, and punitive surcharges up to 3% of total turnover.

Official Citations: Telecommunications Business Act Art. 22-9; PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea Payment & PIPA Compliance Policy defining alternative payment mechanics, CEO accountability, and CPO requirements.
- **Missing Documentation:** Guidebooks lack step-by-step instructions for building Korea-specific binaries, implementing the mandatory StoreKit KR modal sheet, or submitting monthly sales reports.
- **Missing Code:** Mock payment services lack code for the KR StoreKit modal sheet, 26% fee calculations, or KCP/Inicis/Toss payment gateway handoffs.
- **Missing Disclosure:** Checkout flows fail to display the required statutory modal notice informing Korean users of third-party payment processing consequences.
- **Missing Logging:** Missing database schemas for logging Korean alternative payment transactions, monthly sales aggregations, and CPO audit logs.
- **Missing Testing:** Automated UI tests do not verify that selecting alternative payments in Korea presents the un-modified statutory modal sheet before gateway handoff.
- **Missing Evidence:** Missing KCP/Toss payment gateway integration agreements, monthly KCC sales submission receipts, or CPO appointment board resolutions.
- **Missing Audit Trail:** Immutable audit logs tracking monthly revenue reporting to Apple/KCC, CPO oversight reviews, and payment policy updates are absent.

### 19.3 Remediation stain and Action Plan
1. Draft a South Korea Alternative Payment and PIPA Governance Policy.
2. Build native UI modal sheet components for Korean alternative billing flows.
3. Implement backend transaction logging and monthly KCC sales report generators.
4. Add automated UI tests validating the mandatory Korean payment modal sheet.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Companion Rules

### 20.1 Regulatory Overview and Background
China Mobile App Filing (MIIT ICP extension) is mandatory for all apps operating in China. Requires local partner entity, real-name verification, PIPL compliance, data localization, and Banhao license for games. CAC Interim Measures for AI Anthropomorphic Interactive Services (Order No. 21, effective 15 July 2026) mandates automatic minor mode, under-14 guardian consent, and a strict ban on virtual companion services for minors.

Official Citations: MIIT Notice on Mobile App ICP Filing (2023); CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China App Filing and CAC AI Companion Governance Policy covering MIIT filing, real-name verification, and AI minor mode rules.
- **Missing Documentation:** Guidebooks lack developer instructions for integrating Chinese real-name verification APIs, localizing data within mainland China, or configuring CAC minor modes.
- **Missing Code:** Codebase mocks contain no logic for automatic minor mode switching, real-name ID verification, or blocking AI companion features for minor accounts in China.
- **Missing Disclosure:** App metadata templates fail to display verified MIIT ICP filing numbers, CAC AI registration notices, or real-name data collection warnings.
- **Missing Logging:** Missing database schemas for logging MIIT filing numbers, real-name verification tokens, CAC AI safety assessments, and minor mode activations.
- **Missing Testing:** Automated tests do not verify that AI chatbot interfaces automatically block virtual companion features when minor mode is active for Chinese accounts.
- **Missing Evidence:** Missing MIIT ICP filing approval certificates, CAC AI safety assessment filings, or local Chinese partner agreement records.
- **Missing Audit Trail:** Immutable audit logs tracking real-name verification events, CAC safety filings, algorithm updates, and MIIT status changes are absent.

### 20.3 Remediation and Action Plan
1. Formulate a China Mobile App Filing and CAC AI Governance Policy.
2. Implement UI components for real-name verification and automatic minor mode switches.
3. Add metadata fields in `data/rejection-patterns.json` for MIIT ICP registration numbers.
4. Build automated tests verifying AI companion blocking in CAC minor mode.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell indicates Covered. Partial means the rule is named with dated sources but lacks step-by-step developer implementation assets. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act (EAA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA (Amended Rule)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA/CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea Telecom / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is robust on store reviewer rejection patterns, but requires expansion across the post-launch statutory enforcement layer. Nineteen of the twenty frameworks audited are identified in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json` with dated primary citations. What remains missing across almost all frameworks is the implementation layer: detection guard rules, code templates, UI components, logging schemas, automated test runners, and unalterable audit trails.

Priority Action Roadmap:
1. Complete EU GPSR implementation across all eight categories, as it was previously absent end-to-end.
2. Implement automated code detection rules in `data/rejection-patterns.json` and `data/detection-recipes.json` for all nineteen Partial frameworks.
3. Provide front-end and backend code templates for high-priority 2026 obligations (AI Act Article 50 disclosures, EU contract withdrawal button, state ASAA age signal hooks, and BIPA written releases).
4. Integrate automated CI/CD compliance scanners verifying disclosure presence, accessibility traits, and machine-readable synthetic watermarking headers.

---

## 23. Sources

Every regulation cited above is referenced to its primary official publication:
- GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services (Withdrawal Button): [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California CCPA/CPRA: [Cal. Civ. Code § 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100.)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- FTC ROSCA / Negative Option: [15 U.S.C. § 8401](https://www.law.cornell.edu/uscode/text/15/8401)
- UK Online Safety Act: [Online Safety Act 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Social Media Minimum Age Act: [Online Safety Act 2021](https://www.legislation.gov.au/C2021A00076/latest/text)
- Brazil Digital ECA: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore PDPA & IMDA Code: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act & PIPA: [PIPA Amendment Act No. 21445](https://law.go.kr)
- China CAC AI Anthropomorphic Measures: [CAC Order No. 21](https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm)
