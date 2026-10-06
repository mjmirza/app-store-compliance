# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the repository itself. It compares the repository's rules, detection patterns, checklists, scripts, and code templates against twenty major modern global and regional regulations that bind mobile application developers and digital service providers shipping across key international jurisdictions (European Union, United States, United Kingdom, Australia, Brazil, India, Singapore, South Korea, and China).

It evaluates repository completeness and identifies gaps across eight required compliance categories:
1. Missing policy
2. Missing documentation
3. Missing code
4. Missing disclosure
5. Missing logging
6. Missing testing
7. Missing evidence
8. Missing audit trail

Assumptions: The repository is incomplete unless proven otherwise. Search and analysis continue until no additional gaps remain.

## Source Trust Hierarchy and Methodology

All analysis and cited legal frameworks within this report adhere strictly to the repository source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI-generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. This document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
Regulation (EU) 2023/988 on general product safety entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the Directive 2001/95/EC to address safety in digital markets, software-driven consumer products, and e-commerce applications. Online interface templates must display manufacturer identity, electronic and postal contact details, EU Responsible Person details, and safety warning labels.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a General Product Safety Policy template detailing Responsible Person designation, recall escalation procedures, and product safety classification rules.
- **Missing Documentation:** The repository lacks step-by-step developer documentation on structuring product listings to display GPSR safety warnings, batch/type numbers, and manufacturer contacts.
- **Missing Code:** The automated compliance guard (`agent-os/hooks/app-store-compliance-guard.sh`) and detection recipes lack AST/regex patterns to detect missing GPSR UI declarations in app source code.
- **Missing Disclosure:** Front-end store UI templates do not provide placeholder components or guidance for displaying the manufacturer name, registered trade name, postal address, electronic address, and EU Responsible Person details required under Article 19.
- **Missing Logging:** No database schemas or log structures exist for tracking product safety incident reports, user safety notifications, or recall executions.
- **Missing Testing:** Automated test suites lack scripts to verify that product safety disclosures are dynamically rendered based on EU user geo-location.
- **Missing Evidence:** Missing downloadable templates for Technical Documentation sheets, safety risk assessments, and proof of EU Responsible Person registration.
- **Missing Audit Trail:** No tamper-evident mechanism exists to record historical reviews, safety warning updates, or incident remediation logs.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 establish European Production Orders (EPOs) and European Preservation Orders for electronic evidence in criminal matters. Compliance becomes strictly mandatory on 18 August 2026. Authorities can issue direct orders to service providers with a default 10-day production timeline and a strict 8-hour emergency timeline.

Official Citations: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The repository contains no Law Enforcement Request Policy defining authorization matrices, legal review steps, or emergency response escalation.
- **Missing Documentation:** Missing runbooks and operational guides for responding to EPOC and EPOC-PR requests within the mandatory 10-day standard or 8-hour emergency windows.
- **Missing Code:** Backend reference implementations lack automated data export scripts, encryption pipelines, or secure submission endpoints for legal data requests.
- **Missing Disclosure:** Public privacy policy templates do not disclose to EU users that user data may be preserved or produced under European Production and Preservation Orders.
- **Missing Logging:** No schema or mechanism is present to record incoming production/preservation orders, officer identity checks, scope validations, or data extraction activities.
- **Missing Testing:** Integration tests do not simulate rapid 8-hour emergency retrieval or secure package generation.
- **Missing Evidence:** Lacks verified sample templates of EPOC/EPOC-PR forms, legal representative designations, or central authority notifications.
- **Missing Audit Trail:** Unalterable cryptographic audit trails for tracking administrative access, data retrieval, and law enforcement transmissions are absent.

---

## 3. EU Contract Withdrawal Button Directive

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU regarding distance marketing of financial services and online consumer contracts. It mandates a prominent, easily accessible "withdrawal button" or withdrawal function on digital user interfaces for contracts concluded online, allowing consumers to execute a 14-day statutory withdrawal with a single, frictionless flow. Mandatory Member State enforcement starts 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook provides no Consumer Contract Withdrawal and Refund Policy template for EU distance contracts.
- **Missing Documentation:** Missing design guidelines specifying UI placement, contrast, button label wording, and step minimization for withdrawal flows.
- **Missing Code:** Client and web templates do not include code components for an in-app withdrawal button or self-service contract revocation modal.
- **Missing Disclosure:** Purchase and subscription checkout screens lack clear pre-contract disclosures informing EU users of their 14-day statutory right of withdrawal.
- **Missing Logging:** Missing event-logging schemas to capture withdrawal request triggers, timestamping, contract termination confirmations, and refund triggers.
- **Missing Testing:** No automated UI or unit tests verify that the withdrawal path operates without friction, customer support intervention, or multi-step dark patterns.
- **Missing Evidence:** Lacks standardized electronic withdrawal confirmation receipts or standardized refund proof templates.
- **Missing Audit Trail:** Historical audit logging for tracking withdrawal rates, refund processing times, and cancellation interface version changes is not implemented.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State legislation (Utah SB 142 as amended by HB 498, Texas SB 2420, Louisiana HB 977, Alabama HB 161) mandates age assurance, age category retrieval, and verifiable parental consent before minors download apps, make purchases, or receive major updates. Raw age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142/HB 498, Texas SB 2420, Louisiana HB 977, Alabama HB 161.

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Minor Account Protection and Age Assurance Policy template governing state-level age category handling and parental consent verification.
- **Missing Documentation:** Lacks multi-platform integration guides for combining Apple Declared Age Range API and Google Play Age Signals API.
- **Missing Code:** Mobile client code templates lack native wrapper implementations querying `com.apple.developer.declared-age-range` or `com.google.android.play:age-signals`.
- **Missing Disclosure:** Onboarding UI templates omit disclosures explaining state-mandated age range collection and parental consent requirements.
- **Missing Logging:** Lacks backend logging schemas for capturing parental consent receipts, consent revocation signals (`RESCIND_CONSENT`), or immediate age-data deletion confirmations.
- **Missing Testing:** Test suites lack automated integration tests verifying feature gating and billing suppression for minor accounts missing parental consent.
- **Missing Evidence:** Lacks verified templates of parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:** Immutable audit logs to record age-assurance rollout history, policy updates, and data deletion events are absent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among staff and operators. In force since 2 February 2025 without headcount exemptions.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an internal AI Literacy Policy template specifying training curricula, role-based competency thresholds, and annual refresher schedules.
- **Missing Documentation:** Lacks developer guidelines explaining staff obligations regarding AI safety, risk assessment, bias prevention, and data privacy.
- **Missing Code:** CLI/lint tools do not check repository commits to verify that authors working on AI modules hold valid literacy certifications.
- **Missing Disclosure:** Public documentation and recruitment materials do not disclose organizational compliance with Article 4 literacy mandates.
- **Missing Logging:** Missing a centralized, versioned `AI_LITERACY_LOG.md` or database registry to record completed training, dates, and course materials.
- **Missing Testing:** Pre-commit hooks do not validate whether AI training records are up to date before permitting commits to AI components.
- **Missing Evidence:** Lacks sample training certificates, course completion records, or competence assessment rubrics.
- **Missing Audit Trail:** Historical audit records tracking annual policy reviews, curriculum updates, and staff qualification changes are absent.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 mandates AI interaction disclosures (Article 50(1)), machine-readable synthetic content marking (Article 50(2)), and deepfake disclosures (Article 50(4)). Mandatory enforcement takes effect on 2 August 2026, with Article 111(4) retrofitting requirements by 2 December 2026.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an AI Transparency and Content Marking Policy governing synthetic media marking and user disclosure.
- **Missing Documentation:** Lacks developer guides on embedding machine-readable metadata (e.g. C2PA specifications or cryptographic watermarking) in generated media.
- **Missing Code:** Code templates omit helper libraries or middleware for applying C2PA metadata headers or watermark payloads to generated assets.
- **Missing Disclosure:** Chat and generation UI templates do not include mandatory first-exposure notices ("You are interacting with an AI system").
- **Missing Logging:** Lacks event logging to capture user acknowledgment of AI interaction notices and metadata injection timestamps.
- **Missing Testing:** Automated test scripts do not inspect generated output files to verify machine-detectable watermarks or metadata headers.
- **Missing Evidence:** Lacks third-party filter evaluation reports or proof of metadata preservation across media conversion pipelines.
- **Missing Audit Trail:** Lacks immutable records documenting choices of watermarking technology, disclosure UI iterations, or vendor model audits.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 (DMA) regulates gatekeeper platforms. For mobile developers, it governs alternative app marketplaces, web distribution, external purchase links (`com.apple.developer.storekit.external-purchase-link`), and the Core Technology Commission (CTC) framework effective 1 October 2026.

Official Citation: Regulation (EU) 2022/1925.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Alternative Distribution and Anti-Steering Governance Policy for managing multi-channel releases and reporting.
- **Missing Documentation:** Lacks operational documentation on StoreKit External Purchase API integration, monthly CTC sales reporting, and ADPLA Attachment 14 compliance.
- **Missing Code:** Code templates lack implementation of `ExternalPurchaseCustomLink` system disclosure sheets and reporting payload generators.
- **Missing Disclosure:** Lacks in-app disclosures explaining transaction terms when users navigate to external payment surfaces.
- **Missing Logging:** Missing database schemas for logging monthly external purchase volumes, transaction IDs, and commission calculation inputs.
- **Missing Testing:** Test runners do not verify that external purchase links trigger system sheets or validate that StoreKit IAP and external links are not co-mingled on the same storefront.
- **Missing Evidence:** Lacks templates for CTC monthly reporting spreadsheets, stand-by letter of credit documentation, or notarization submission logs.
- **Missing Audit Trail:** Historical records of entitlement applications, sales reporting filings, and fee calculations are not maintained.

---

## 8. EU Digital Services Act (DSA) Trader Status

### 8.1 Regulatory Overview and Background
Articles 30 and 31 of Regulation (EU) 2022/2065 (DSA) mandate trader identity verification and public disclosure (D-U-N-S, address, phone, email, payment account) for developers distributing apps on EU storefronts. Non-trader declarations must be verified.

Official Citation: Regulation (EU) 2022/2065.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an EU Trader Identification and Compliance Policy defining criteria for classifying developer entities as traders or non-traders.
- **Missing Documentation:** Lacks step-by-step developer guides for completing DSA trader verification in App Store Connect and Google Play Console.
- **Missing Code:** Metadata audit scripts (`scripts/metadata-audit.py`) do not check store metadata configs for verified DSA trader fields or warning flags.
- **Missing Disclosure:** Product listing templates do not include standardized blocks for trader address, email, phone number, and commercial register numbers.
- **Missing Logging:** Lacks logging mechanisms to track 2FA verification steps, document upload dates, and store status confirmations.
- **Missing Testing:** Automated pre-submission scripts do not test whether an app targeting EU storefronts has completed DSA verification.
- **Missing Evidence:** Lacks repository examples of verified D-U-N-S profiles, commercial register extracts, or trader compliance certificates.
- **Missing Audit Trail:** Lacks historical logging of trader status changes, address updates, or store verification communications.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (EAA) became applicable on 28 June 2025. It mandates accessibility for consumer digital services and mobile apps under harmonised standard EN 301 549 (built on WCAG 2.1 Level AA, including Chapter 11 for mobile apps) and requires a published accessibility statement.

Official Citation: Directive (EU) 2019/882.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Organizational Accessibility Policy committed to EN 301 549 / WCAG 2.1 Level AA standards.
- **Missing Documentation:** Lacks developer documentation specifically addressing EN 301 549 Chapter 11 mobile software requirements (non-web software, assistive tech interoperability).
- **Missing Code:** Static accessibility scripts (`scripts/accessibility-audit.py`) do not fully check for screen reader focus trapping, custom gesture alternatives, or dynamic font scaling bounds.
- **Missing Disclosure:** Lacks template code or markdown layouts for an in-app and web-published Accessibility Statement conforming to EN 301 549 Annex B/C.
- **Missing Logging:** Lacks logging schemas for capturing user-reported accessibility defects, switch-control errors, or screen-reader crash events.
- **Missing Testing:** Test runners do not perform automated accessibility regression checks covering VoiceOver/TalkBack traversal, high-contrast themes, and 200% text scaling.
- **Missing Evidence:** Lacks sample VPAT (Voluntary Product Accessibility Template) or EN 301 549 Conformance Reports.
- **Missing Audit Trail:** Lacks historical records of accessibility audits, remediation tickets, and statement revisions.

---

## 10. US COPPA & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
16 CFR Part 312 (COPPA) as amended (effective 23 June 2025, compliance date 22 April 2026) expands PII to include biometric and government identifiers, requires separate opt-in consent for third-party disclosure/targeted ads, mandates written data retention policies, and requires a written information security program.

Official Citation: 16 CFR Part 312 (90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an updated COPPA Compliance Policy incorporating biometric data definitions, separate opt-in requirements, and written retention schedules.
- **Missing Documentation:** Lacks developer implementation guides for verifiable parental consent (VPC) methods (e.g. face-match to ID, knowledge-based auth).
- **Missing Code:** Code templates omit separate opt-in consent UI flows for targeted ads versus core service functionality for child users.
- **Missing Disclosure:** Privacy policy templates do not detail biometric identifier handling, third-party disclosure opt-ins, or specific retention periods for children's data.
- **Missing Logging:** Lacks secure backend logging for VPC confirmations, opt-in/opt-out states, and mandatory deletion timestamps under Section 312.10.
- **Missing Testing:** Integration tests do not verify that ad-tracking SDKs are neutralized when an under-13 age response is received.
- **Missing Evidence:** Lacks templates for Written Information Security Programs (WISP), annual COPPA risk assessments, or Safe Harbor certificates.
- **Missing Audit Trail:** Lacks tamper-proof audit trails logging parental consent grants, revocations, and scheduled data purging events.

---

## 11. California Privacy (CCPA / CPRA / CPPA 2026 / GPC)

### 11.1 Regulatory Overview and Background
California Consumer Privacy Act (CCPA) as amended by CPRA and CPPA 2026 regulations mandates opt-out of sale/sharing/profiling, "Do Not Sell or Share" links, honoring Global Privacy Control (GPC) signals (`Sec-GPC`), automated decision-making technology (ADMT) disclosures, and sensitive personal info limits.

Official Citations: California Civil Code Sec 1798.100 et seq., 11 CCR Sec 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a California Privacy Rights Policy template covering ADMT opt-outs, sensitive personal info rules, and GPC signal compliance.
- **Missing Documentation:** Lacks technical documentation on passing and honoring GPC headers in mobile webviews and native network stacks.
- **Missing Code:** Code templates lack automatic GPC header detection (`Sec-GPC`) and native event handlers to halt third-party data tracking.
- **Missing Disclosure:** Privacy notices lack mandatory ADMT disclosures, "Limit the Use of My Sensitive Personal Information" notices, and explicit opt-out links.
- **Missing Logging:** Lacks backend database schemas to log consumer rights requests (know, delete, correct, opt-out) and response fulfillment times.
- **Missing Testing:** Test suites do not simulate GPC signal headers or verify that data broker sharing ceases upon signal detection.
- **Missing Evidence:** Lacks sample Consumer Rights Request Logs or CPPA Cybersecurity Audit Certification reports.
- **Missing Audit Trail:** Lacks immutable records tracking privacy policy revisions, GPC opt-out processing, and ADMT risk assessments.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
740 ILCS 14 (BIPA) requires written notice and a written release before collecting biometric identifiers (fingerprints, voiceprints, retina/facial scans), a publicly available retention schedule and destruction guideline, and prohibits profiting from biometric data.

Official Citation: 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a dedicated Biometric Data Privacy Policy template specifying written consent procedures and destruction schedules.
- **Missing Documentation:** Lacks developer guidelines on distinguishing local device biometric auth (e.g. FaceID/TouchID handled by OS) from server-side biometric collection.
- **Missing Code:** Client templates lack consent UI modals for executing e-signed biometric release agreements.
- **Missing Disclosure:** In-app screens lack written disclosures detailing specific biometric identifiers collected, storage purpose, and length of term.
- **Missing Logging:** Lacks secure backend logging for capture of e-signatures, consent timestamps, and automated destruction schedule triggers.
- **Missing Testing:** Unit/integration tests do not verify that biometric data pipelines are blocked prior to valid written release receipt.
- **Missing Evidence:** Lacks public retention and destruction schedule templates or sample consent agreement forms.
- **Missing Audit Trail:** Lacks cryptographic audit logs documenting consent acquisition, biometric data deletion within 3 years, and policy updates.

---

## 13. US Subscription Cancellation (FTC Negative Option & State ROSCA)

### 13.1 Regulatory Overview and Background
FTC Act Section 5, ROSCA (15 U.S.C. 8401), and state laws (California, New York, Massachusetts negative-option statutes) require that cancellation paths for auto-renewing subscriptions must be at least as easy as sign-up (simple, self-service online/in-app cancellation without mandatory phone calls or mail).

Official Citations: 15 U.S.C. 8401, Cal. Bus. & Prof. Code Sec 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Negative Option and Auto-Renewal Subscription Policy template.
- **Missing Documentation:** Lacks developer guides on implementing self-service cancellation paths for web/app subscriptions billed outside platform IAP.
- **Missing Code:** Code templates omit self-service "Cancel Subscription" UI buttons or API cancellation handlers for web-billed subscriptions.
- **Missing Disclosure:** Subscription checkout screens lack clear pre-purchase disclosures regarding auto-renewal terms, recurring pricing, and cancellation methods.
- **Missing Logging:** Lacks logging schemas to record cancellation clicks, retention offer interactions, cancellation timestamps, and confirmation emails sent.
- **Missing Testing:** Automated UI tests do not check that subscription cancellation can be executed in equal or fewer steps than sign-up.
- **Missing Evidence:** Lacks sample cancellation confirmation email templates or ROSCA compliance audit sheets.
- **Missing Audit Trail:** Lacks immutable logging of cancellation flow UX changes, retention attempt rules, and refund request histories.

---

## 14. UK Online Safety Act & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code (Children's Code) require highly effective age assurance (facial age estimation, open banking, credit card checks), high privacy by default, geolocation off by default, profiling off by default, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023 c. 50, ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Children's Safety and High-Privacy Default Policy template.
- **Missing Documentation:** Lacks developer guidelines on setting default configurations (geolocation off, profiling off) for UK child users.
- **Missing Code:** Code templates omit logic for toggling high-privacy defaults based on UK user detection and age verification status.
- **Missing Disclosure:** In-app notices lack explicit disclosures regarding age-estimation methods used and child safety reporting mechanisms.
- **Missing Logging:** Lacks logging for age-assurance method selection, DPIA completion markers, and child safety incident reports.
- **Missing Testing:** Integration tests do not verify that location tracking and targeted profiling are disabled by default for UK users.
- **Missing Evidence:** Lacks completed DPIA (Data Protection Impact Assessment) templates for child-accessible services.
- **Missing Audit Trail:** Lacks historical audit trails for age-assurance system updates, Ofcom compliance filings, and safety risk assessment reviews.

---

## 15. Australia Online Safety & Privacy Act ADM

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 and Privacy Act 1988 amendments mandate age restrictions for social media (under 16), destruction of age-assurance data, and explicit privacy policy disclosures regarding Automated Decision-Making (ADM) significantly affecting rights (APP 1.7-1.9).

Official Citations: Online Safety Amendment Act 2024, Privacy Act 1988 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Privacy and Age-Restricted Platform Policy template.
- **Missing Documentation:** Lacks developer guides on disclosing ADM operations and age-data destruction workflows under Australian law.
- **Missing Code:** Code templates lack automated purging utilities to delete age-assurance verification artifacts immediately following verification.
- **Missing Disclosure:** Privacy policies lack required APP 1.7-1.9 disclosures regarding the types of personal info used in ADM and decision impacts.
- **Missing Logging:** Lacks database logging schemas for recording age verification completions and immediate age-data destruction triggers.
- **Missing Testing:** Test runners do not verify that age verification raw data files or database fields are deleted after verification.
- **Missing Evidence:** Lacks sample eSafety compliance reports or ADM impact assessment templates.
- **Missing Audit Trail:** Lacks immutable logs recording ADM algorithm disclosures, age-data deletion confirmations, and policy updates.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 16.1 Regulatory Overview and Background
Law 15,211/2025 (Digital ECA) and Decreto 12.880 mandate approved age verification (document check, facial estimation, CPF database check; self-declaration checkboxes are prohibited), guardian authorization, and showing age ratings before download. Enforceable starting 17 March 2026.

Official Citations: Lei n. 15.211/2025, Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazil Digital ECA Compliance Policy template.
- **Missing Documentation:** Lacks developer documentation on integrating ANPD-approved age-assurance mechanisms and CPF checks.
- **Missing Code:** Code templates lack client logic to block self-declaration checkboxes for Brazilian users and force ANPD-approved verification flows.
- **Missing Disclosure:** Onboarding interfaces lack disclosures regarding age rating declarations and guardian consent requirements under Decreto 12.880.
- **Missing Logging:** Lacks backend schemas for logging guardian consent requests, contestation submissions, and ANPD age signal receipts.
- **Missing Testing:** Test suites do not verify that self-declaration age flows are rejected for Brazilian IP/locale requests.
- **Missing Evidence:** Lacks sample ANPD compliance filings or guardian authorization record templates.
- **Missing Audit Trail:** Lacks audit trails recording age verification method updates, guardian approvals, and ANPD regulatory reporting.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / Rules 2025)

### 17.1 Regulatory Overview and Background
DPDPA 2023 and DPDP Rules 2025 mandate verifiable parental consent through government-backed systems (e.g. DigiLocker) for users under 18, ban behavioral tracking/targeted ads for minors, and require interoperability with registered Consent Managers.

Official Citations: Act No. 22 of 2023, G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India DPDPA Data Fiduciary Policy template.
- **Missing Documentation:** Lacks developer guides on integrating with DigiLocker VPC mechanisms and registered Consent Manager APIs.
- **Missing Code:** Code templates omit API handlers for receiving consent state updates from Indian Consent Managers or disabling ad tracking for under-18s.
- **Missing Disclosure:** Consent notices lack multi-lingual disclosures (all 22 Eighth Schedule languages requirement) and Data Protection Officer details.
- **Missing Logging:** Lacks database logging schemas for capturing Consent Manager token exchanges and parental consent receipts.
- **Missing Testing:** Automated tests do not verify that targeted advertising components are disabled for Indian users under 18.
- **Missing Evidence:** Lacks sample Data Protection Impact Assessment (DPIA) templates for Significant Data Fiduciaries.
- **Missing Audit Trail:** Lacks immutable audit logs for tracking consent notices, Consent Manager interactions, and data breach notifications.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Online Safety

### 18.1 Regulatory Overview and Background
Singapore PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require app-store and developer age assurance (screening under-18s from downloading age-inappropriate content), destruction of age-assurance data, and 3-day breach notifications.

Official Citations: PDPA 2012, IMDA Code of Practice 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore PDPA and Online Safety Policy template.
- **Missing Documentation:** Lacks developer documentation on IMDA age-assurance expectations and 3-day Personal Data Protection Commission (PDPC) breach reporting.
- **Missing Code:** Code templates lack automated workflows for purging age-assurance credentials following age band classification.
- **Missing Disclosure:** Privacy policies omit required disclosures regarding Data Protection Officer (DPO) contact details and IMDA safety content tiers.
- **Missing Logging:** Lacks logging schemas to record PDPC breach notification triggers, DPO contact logs, and age verification purges.
- **Missing Testing:** Integration tests do not verify that age verification records are deleted immediately post-verification.
- **Missing Evidence:** Lacks sample PDPC Breach Notification forms or IMDA Safety Compliance Checklists.
- **Missing Audit Trail:** Lacks historical audit trails logging DPO appointments, breach investigations, and IMDA compliance reviews.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
The Telecommunications Business Act mandates alternative in-app payments (26% commission, approved Korea payment gateways, StoreKit entitlement `com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`), and PIPA Act No. 21445 requires board-approved CPOs and CEO accountability.

Official Citations: Telecommunications Business Act Art. 22-9, PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea Payment and Data Privacy Governance Policy template.
- **Missing Documentation:** Lacks developer documentation on building Korea-specific binaries, integrating KCP/Inicis/Toss gateways, and filing monthly 15-day sales reports.
- **Missing Code:** Code templates lack native modal sheet implementations required prior to opening external Korean payment gateways.
- **Missing Disclosure:** In-app purchase screens lack mandatory statutory disclosures regarding alternative payment provider terms and loss of store protection features.
- **Missing Logging:** Lacks backend logging schemas for capturing monthly Korean transaction totals, commission calculations, and CPO approvals.
- **Missing Testing:** Test runners do not verify that South Korean builds display the required modal sheet before launching third-party payment flows.
- **Missing Evidence:** Lacks sample monthly sales reporting spreadsheets for App Store Connect / KCC submissions.
- **Missing Audit Trail:** Lacks immutable audit trails tracking CPO appointment records, board approvals, and monthly payment reporting logs.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Companion Rules

### 20.1 Regulatory Overview and Background
MIIT Mobile App Filing requires local entity partnership, ICP filing, real-name verification, and CAC Order No. 21 (AI Anthropomorphic Interactive Services) mandates minor protection, automatic minor mode switching, and prohibiting virtual companion services for minors.

Official Citations: MIIT App Filing Notice (2023), CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China Distribution, ICP Filing, and CAC AI Compliance Policy template.
- **Missing Documentation:** Lacks step-by-step developer documentation on completing MIIT app filing, Banhao gaming licenses, and CAC AI service filings.
- **Missing Code:** Client templates lack logic to automatically detect minor accounts in China and toggle non-companion, restricted minor mode.
- **Missing Disclosure:** App metadata and onboarding screens lack MIIT app filing number displays, real-name verification notices, and CAC AI disclosures.
- **Missing Logging:** Lacks backend database logging for real-name ID verification tokens, minor mode toggle events, and CAC content filter triggers.
- **Missing Testing:** Test suites do not verify that AI companion/roleplay features are strictly disabled when the user is flagged as a minor in China.
- **Missing Evidence:** Lacks sample MIIT App Filing registration certificates, Banhao approval documents, or CAC AI security assessment reports.
- **Missing Audit Trail:** Lacks immutable records documenting real-name verification logs, ICP filing updates, and CAC safety audit submissions.

---

## 21. Consolidated Gap Classification Matrix

The matrix below summarizes repository coverage across all twenty audited frameworks:
- **Covered:** Comprehensive detection, documentation, code templates, and tests exist in the repository.
- **Partial:** Framework is referenced or cited with dated deadlines, but step-by-step code templates, detection rules, or test suites are missing.
- **Missing:** Framework is completely absent from detection patterns, checklists, code templates, and test suites.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **8. EU DSA Trader** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **9. European Accessibility Act** | Covered | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA & Amended Rule**| Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **11. California CCPA/CPRA/GPC**| Covered | Covered | Partial | Covered | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel**| Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **14. UK Online Safety & ICO** | Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **17. India DPDPA / Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA**| Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **20. China App Filing & CAC**| Covered | Covered | Missing | Covered | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Prioritized Action Plan

The repository exhibits strong coverage of store rejection mechanics and regulatory citations, but possesses consistent architectural gaps in backend logging schemas, automated unit/integration test runners, compliance evidence templates, and immutable audit trails across almost all regulations.

To achieve complete compliance, remediation should proceed in the following prioritized order:

1. **Add GPSR Rules & Templates:** Fully incorporate EU General Product Safety Regulation patterns into `data/rejection-patterns.json`, `data/detection-recipes.json`, and `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. **Implement Missing Code Layers:** Create reusable UI/backend code components for the EU Withdrawal Button, AI Act Article 50 C2PA metadata injection, Apple Declared Age Range / Google Play Age Signals wrappers, and GPC header detection.
3. **Build Logging & Audit Trail Schemas:** Add database schemas (`data/schemas/`) for logging legal requests (e-Evidence), parental consent receipts (ASAA/COPPA), withdrawal triggers, and age-data deletion confirmations.
4. **Expand Automated Guard & Testing:** Enhance `agent-os/hooks/app-store-compliance-guard.sh` and test runners to validate codebases against all missing regulatory patterns prior to release authorization.

## 23. Sources

Primary official legal publications establishing the obligations in this report:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Withdrawal Button: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California CCPA/CPRA: [California Civil Code Sec 1798.100 et seq.](https://leginfo.legislature.ca.gov)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- Brazil Digital ECA: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA Rules: [G.S.R. 846(E)](https://egazette.gov.in)
- China CAC AI Rules: [CAC Order No. 21](https://www.cac.gov.cn)
