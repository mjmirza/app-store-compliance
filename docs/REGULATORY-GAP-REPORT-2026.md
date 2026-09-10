# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind app developers shipping into key international jurisdictions (European Union, United States, United Kingdom, Australia, Brazil, Canada, India, Singapore, South Korea, and China) and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight specific compliance gap angles: missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address online marketplaces, digital products, and e-commerce applications. For digital interfaces and software, the GPSR mandates clear display of product safety warnings, instructions, manufacturer and importer identity, and electronic contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook provides no developer criteria or template policy to determine if an app listing or e-commerce catalog falls inside Regulation (EU) 2023/988, nor any template policy for EU Responsible Person designation.
- **Missing Documentation:** The repository lacks developer-facing guidelines or step-by-step instructions on structuring online storefront product listings to display mandatory GPSR safety warnings, manufacturer details, and technical instructions.
- **Missing Code:** The automated compliance guard and detection recipes historically lacked detection patterns for GPSR metadata elements. UI components in the references directory do not provide code for rendering EU manufacturer contact cards or safety warning modal sheets.
- **Missing Disclosure:** Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name/trademark, postal address, and electronic address (email/website) per Article 19 of the GPSR.
- **Missing Logging:** There are no architectural provisions or schemas for logging product safety incidents, safety alerts, customer warnings, or recall notices.
- **Missing Testing:** No automated UI or integration tests exist to verify that product listings dynamically render mandatory safety disclosures based on user location.
- **Missing Evidence:** The repository lacks physical templates of Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:** There is no audit trail or historical record system to track when product safety warnings were updated or when safety measures were executed in response to a recall.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on legal representatives. The mandatory compliance enforcement date is 18 August 2026. Judicial authorities of an EU Member State can issue Production Orders directly to service providers in the EU. Standard compliance window is 10 days; emergency orders require compliance within 8 hours.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template Law Enforcement Request Policy detailing roles and responsibilities for handling European Production Orders (EPO) or Preservation Orders (EPOC-PR).
- **Missing Documentation:** Concrete operational runbooks detailing step-by-step procedures for fulfilling 10-day standard and 8-hour emergency legal orders are absent.
- **Missing Code:** No backend helper scripts or API endpoints exist in repository mock implementations to automate secure user data extraction, filtering, and cryptographic packaging for legal orders.
- **Missing Disclosure:** Privacy policies and public documentation fail to explicitly disclose to EU users that their data may be preserved or disclosed under Regulation (EU) 2023/1543.
- **Missing Logging:** Database schemas or logging modules designed to record incoming judicial orders, verification checks, access events, or data releases are missing.
- **Missing Testing:** No integration tests exist to simulate rapid 8-hour emergency retrieval and secure packaging of user datasets under time constraints.
- **Missing Evidence:** Verified sample templates of European Production Order certificates (EPOC) or Preservation certificates are missing.
- **Missing Audit Trail:** An immutable audit trail recording administrative access, extraction parameters, and transmission timestamps during legal processing is absent.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU) for distance marketing of financial services, requiring a prominent, easily accessible withdrawal button or function on online interfaces. Statutory withdrawal period is 14 days from contract conclusion. Transposition deadline is 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template policy exists for the 14-day statutory withdrawal right or criteria distinguishing financial services from general subscriptions.
- **Missing Documentation:** Interface guidelines detailing button placement, visual prominence, required wording, and modal confirmation steps are missing.
- **Missing Code:** Front-end templates and billing mocks do not include functional code for a one-click contract withdrawal button or modal sheet.
- **Missing Disclosure:** Onboarding and paywall interfaces fail to display prominent notices explaining the 14-day right of withdrawal and its financial terms.
- **Missing Logging:** No event logging structures exist to capture user withdrawal clicks, request timestamps, contract cancellation confirmations, or refund triggers.
- **Missing Testing:** Automated end-to-end UI tests to verify that contract withdrawal executes without manual friction or mandatory support interaction are missing.
- **Missing Evidence:** No standardized cancellation confirmation receipts or customer withdrawal acknowledgement form templates are provided.
- **Missing Audit Trail:** Systematic records tracking historical contract withdrawal rates, UI audit histories, and cancellation flow revisions are not implemented.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977/HB 570, Alabama HB 161) regulate minor access to mobile applications, purchases, and updates. Developers must request and process user age categories via Apple Declared Age Range API or Google Play Age Signals API and obtain verifiable parental consent before minor access.

Official Citations: Utah SB 142 (2025/2026), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no minor age-assurance policy detailing state-level detection, parental consent workflows, or minor account restriction rules.
- **Missing Documentation:** Developer checklists lack step-by-step instructions for integrating native Declared Age Range and Play Age Signals APIs within unified codebases.
- **Missing Code:** Codebase templates do not contain active native integrations for `com.apple.developer.declared-age-range` or `com.google.android.play:age-signals` to restrict feature access dynamically.
- **Missing Disclosure:** Onboarding flows omit mandatory state disclosures informing users that age categories are retrieved to satisfy state accountability laws.
- **Missing Logging:** Backend logging for parental consent receipts, consent revocations (`RESCIND_CONSENT`), and immediate verification data deletion is missing.
- **Missing Testing:** Unit and UI test suites do not test feature gating, update blocking, or payment restriction when minor age signals are returned without consent flags.
- **Missing Evidence:** Physical templates for parental consent agreements, identity verification receipts, or data minimization records are missing.
- **Missing Audit Trail:** Immutable audit trails recording age assurance feature rollouts, API configuration changes, and verification data purging events are absent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 mandates that providers and deployers of AI systems ensure staff and operators possess a sufficient level of AI literacy. Mandatory since 2 Feb 2025 with no headcount exemption.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no template AI Literacy Policy defining core competencies (AI safety, risk assessment, bias, privacy).
- **Missing Documentation:** Developer manuals lack documentation explaining Article 4 obligations or staff training refresh schedules.
- **Missing Code:** No static checks or CLI tools exist to verify that developer environment configurations require active literacy training records.
- **Missing Disclosure:** Public documentation and partner agreements omit explicit commitments to enforcing team AI literacy standards.
- **Missing Logging:** Centralized training logs tracking employee inductions, module completions, and annual refresher dates are missing.
- **Missing Testing:** No automated CI lints verify whether team members committing AI feature code possess valid, current training records.
- **Missing Evidence:** No physical evidence templates (completed course logs, certificates, internal assessment results) are supplied.
- **Missing Audit Trail:** Historical audit records tracking policy reviews, training curriculum updates, and staff qualification changes are absent.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 mandates direct transparency for AI systems, taking effect 2 August 2026. Requires clear interaction notices ("You are chatting with an AI"), machine-readable marking of synthetic content, and deepfake disclosures.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook lacks a formal AI Transparency and Synthetic Media Disclosure Policy.
- **Missing Documentation:** Technical guidelines detailing C2PA metadata injection, invisible watermarking, and visible synthetic label formatting are incomplete.
- **Missing Code:** Middleware and helper classes for embedding machine-readable watermarks into generated text, audio, images, or video are missing from code templates.
- **Missing Disclosure:** Conversational UI templates do not embed mandatory initial disclosures ("You are interacting with an AI system").
- **Missing Logging:** Event schemas for logging user presentation of AI transparency notices prior to interaction are not implemented.
- **Missing Testing:** Test runners do not inspect synthetic media outputs to verify that machine-readable markers (C2PA headers) are correctly embedded.
- **Missing Evidence:** No documented proof of content moderation filter audits or metadata retention checks is provided.
- **Missing Audit Trail:** Cryptographic audit trails recording model deployment changes, prompt updates, and transparency disclosure revisions are missing.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 (DMA) regulates gatekeeper platforms and enforces non-discriminatory access, alternative app distribution, non-WebKit browser engines, NFC access, and out-of-app promotion link entitlements (`com.apple.developer.storekit.external-purchase-link`).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook lacks a written policy defining alternative payment and web distribution strategy for EU app versions.
- **Missing Documentation:** Developer guides lack step-by-step documentation for integrating `ExternalPurchaseCustomLink` APIs and executing monthly reporting.
- **Missing Code:** Base code templates do not include system disclosure sheet invocations or automated CTC reporting handlers.
- **Missing Disclosure:** Storefront templates omit mandatory system disclosure sheets informing users that transactions occur outside platform protection.
- **Missing Logging:** Logging mechanisms for capturing external link clicks, transaction referrals, and monthly volume reporting are absent.
- **Missing Testing:** Automated tests to ensure StoreKit IAP and external purchase links are never co-mingled on the same EU storefront are missing.
- **Missing Evidence:** Templates for monthly External Purchase Server API reports or stand-by letter of credit documentation are missing.
- **Missing Audit Trail:** Historical logs tracking entitlement activations, StoreKit addendum acceptances, and external link modifications are absent.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (DSA) regulates online intermediaries. Articles 30 and 31 mandate verified Trader Status declarations (D-U-N-S, phone, email publishing) and mandatory notice-and-action content moderation mechanisms for UGC apps.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No written policy exists guiding developers on DSA Trader classification or UGC illegal content removal protocols.
- **Missing Documentation:** Checklists omit step-by-step procedures for completing App Store Connect / Play Console DSA trader verification.
- **Missing Code:** Sample UGC code templates lack integrated 24-hour content reporting, user blocking, and notice-and-action moderation APIs.
- **Missing Disclosure:** App store metadata and in-app listings lack mandatory trader identity cards or non-trader consumer warnings.
- **Missing Logging:** Database logging structures for capturing content flagging events, moderator review decisions, and takedown notices are missing.
- **Missing Testing:** Automated integration tests verifying 24-hour moderation response flows and reporting button triggers are missing.
- **Missing Evidence:** Sample compliance documentation (verified trader registration receipts, annual DSA transparency reports) is missing.
- **Missing Audit Trail:** An unalterable audit log of moderation actions, account suspensions, and content reinstatement appeals is absent.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (EAA) applies to consumer products and digital services (banking, e-commerce, transport, e-books). Enforceable since 28 June 2025, it mandates compliance with harmonised standard EN 301 549 (WCAG 2.1 AA) and publication of an accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no formal Accessibility Policy defining EN 301 549 Chapter 11 compliance criteria.
- **Missing Documentation:** While basic accessibility is mentioned, detailed technical guides mapping EN 301 549 requirements to native iOS/Android views are missing.
- **Missing Code:** Interface templates lack complete accessibility attributes (`accessibilityLabel`, `accessibilityTraits`, `DynamicType` scaling, 4.5:1 contrast code).
- **Missing Disclosure:** Templates do not contain an in-app reachable Accessibility Statement conforming to EN 301 549 Annex B/C.
- **Missing Logging:** No event logging exists to record accessibility setting changes, screen reader activations, or user feedback on access barriers.
- **Missing Testing:** Automated accessibility regression test suites verifying Dynamic Type scaling and screen reader focus order across all screens are absent.
- **Missing Evidence:** No formal Accessibility Conformance Report (VPAT / EN 301 549 test evaluation) templates are provided.
- **Missing Audit Trail:** Immutable records tracking accessibility audits, third-party evaluation reports, and code remediation histories are absent.

---

## 10. US COPPA and Amended COPPA Rule

### 10.1 Regulatory Overview and Background
16 CFR Part 312 (COPPA) covers child-directed services and actual knowledge collection from under-13s. The Amended Rule (90 FR 16918, effective 23 June 2025, compliance 22 April 2026) adds biometric identifiers to PII, mandates separate opt-in for ad-sharing, requires a written security program, and limits data retention.

Official Citation: 16 CFR Part 312 and FTC Final Rule 90 FR 16918.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository lacks a written Information Security Program and data retention policy conforming to COPPA section 312.8 and 312.10.
- **Missing Documentation:** Checklists omit detailed guidelines for implementing separate ad-sharing opt-in modals and biometric data minimization.
- **Missing Code:** Onboarding templates lack separate consent flags for third-party disclosure and automated biometric data purging functions.
- **Missing Disclosure:** Privacy policies fail to explicitly list biometric identifiers (voiceprint, facial template) as protected minor PII.
- **Missing Logging:** Logging schemas for tracking parental consent verifications, consent revocations, and automated record purges are missing.
- **Missing Testing:** Automated tests to ensure ad-tracking SDKs remain completely deactivated when minor flags are present are missing.
- **Missing Evidence:** Templates for FTC Safe Harbor submission packages, written security program annual reviews, and risk assessments are missing.
- **Missing Audit Trail:** An unalterable audit log tracking parental consent events, consent scope modifications, and data deletion cycles is absent.

---

## 11. California Privacy (CCPA/CPRA and CPPA 2026 Regulations)

### 11.1 Regulatory Overview and Background
Cal. Civ. Code section 1798.100 et seq. (CCPA/CPRA) grants rights to know, delete, correct, opt-out of sale/sharing, and limit sensitive PI use. CPPA 2026 regulations enforce automated decision-making controls and Global Privacy Control (GPC) support.

Official Citation: California Consumer Privacy Act of 2018 and CPPA Regulations (11 CCR section 7000 et seq.).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template California Privacy Policy or Sensitive Personal Information Use Policy is provided.
- **Missing Documentation:** Technical manuals lack guidance on implementing native in-app GPC opt-out equivalents and automated consumer request handling.
- **Missing Code:** Code templates do not evaluate `Sec-GPC` headers in webviews or provide native opt-out hooks for data sale/sharing.
- **Missing Disclosure:** UI templates omit "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:** Backend systems lack logging schemas for capturing opt-out signals, GPC headers, and privacy request completion timelines.
- **Missing Testing:** Integration tests verifying that data broker and analytics SDKs immediately cease transmission upon receiving an opt-out signal are missing.
- **Missing Evidence:** Templates for annual CPPA cybersecurity audit submissions and risk assessments are missing.
- **Missing Audit Trail:** Immutable records tracking consumer rights request fulfillment, opt-out propagation, and policy revision dates are absent.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
740 ILCS 14 (BIPA) requires written notice and written release prior to capturing biometric identifiers (fingerprint, voiceprint, retina/iris, scan of hand/face geometry), a publicly available retention schedule, destruction within 3 years, and prohibits sale.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template Biometric Data Privacy Policy or 3-year destruction schedule is provided in the repository.
- **Missing Documentation:** Developer guides lack technical instructions on separating local biometric authentication (LocalAuthentication/BiometricPrompt) from server-side biometric capture.
- **Missing Code:** Code templates lack explicit consent release modal components for biometric capture.
- **Missing Disclosure:** UI flows fail to present written notice detailing specific biometric capture purposes and storage duration prior to collection.
- **Missing Logging:** Backend systems lack logging schemas for tracking written consent releases and scheduled biometric destruction events.
- **Missing Testing:** Automated tests verifying that raw biometric data is never transmitted to cloud endpoints without signed releases are missing.
- **Missing Evidence:** Written consent release agreement templates and biometric data destruction verification certificates are missing.
- **Missing Audit Trail:** An immutable audit log tracking biometric consent signatures, data destruction dates, and annual retention policy reviews is absent.

---

## 13. US Subscription Cancellation (ROSCA and State Laws)

### 13.1 Regulatory Overview and Background
Restore Online Shoppers' Confidence Act (15 U.S.C. 8401) and state statutes (California Bus. & Prof. Code section 17600, NY, MA) mandate that subscription cancellation must be direct, frictionless, and at least as easy as sign-up (click-to-cancel).

Official Citations: 15 U.S.C. 8401 (ROSCA) and California Bus. & Prof. Code section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no Subscription Cancellation and Auto-Renewal Policy template.
- **Missing Documentation:** Guidelines detailing self-service web/in-app cancellation flow requirements for web-billed subscriptions are missing.
- **Missing Code:** Account setting templates lack functional code for a one-click online subscription cancellation sheet.
- **Missing Disclosure:** Subscription sign-up screens omit clear disclosures of recurring billing charges, renewal frequency, and simple cancellation steps.
- **Missing Logging:** Database logging for subscription cancellation clicks, confirmation receipts, and billing termination events is missing.
- **Missing Testing:** UI test suites do not verify that cancellation can be completed online without mandatory phone calls, emails, or agent intervention.
- **Missing Evidence:** Templates for cancellation confirmation receipts and pre-renewal notice email logs are missing.
- **Missing Audit Trail:** Immutable records tracking cancellation rates, UI modification histories, and subscription flow audit logs are absent.

---

## 14. UK Online Safety Act and ICO Children's Code

### 14.1 Regulatory Overview and Background
UK Online Safety Act 2023 and ICO Age Appropriate Design Code mandate highly effective age assurance (digital ID, facial estimation), high privacy by default, geolocation off by default, profiling off by default, and a Data Protection Impact Assessment (DPIA).

Official Citations: Online Safety Act 2023 (c. 50) and ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template UK Child Safety & Privacy Policy or DPIA framework is provided in the playbook.
- **Missing Documentation:** Developer checklists lack guidance on implementing Ofcom-approved highly effective age assurance methods.
- **Missing Code:** Native code templates do not enforce default-off settings for geolocation and profiling when UK child signals are detected.
- **Missing Disclosure:** UI templates fail to display child-friendly privacy notices and risk disclosures.
- **Missing Logging:** Backend schemas for capturing age assurance verification results and DPIA approvals are missing.
- **Missing Testing:** Integration tests verifying that precise location and ad profiling are disabled by default for UK minor accounts are missing.
- **Missing Evidence:** Sample DPIA documentation templates and Ofcom compliance self-assessments are missing.
- **Missing Audit Trail:** Immutable logs recording age assurance verification execution, age data destruction, and DPIA updates are absent.

---

## 15. Australia Online Safety Act and Privacy Act Updates

### 15.1 Regulatory Overview and Background
Online Safety Amendment (Social Media Minimum Age) Act 2024 (in force 10 Dec 2025) restricts under-16s on age-restricted social media platforms. Privacy Act APP 1.7-1.9 requires automated decision-making disclosures.

Official Citations: Online Safety Amendment Act 2024 and Privacy Act 1988 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no Australian Age-Restricted Platform Policy or Automated Decision-Making Policy.
- **Missing Documentation:** Documentation lacks guidance on integrating Australian waterfall age assurance and APP 1.7-1.9 disclosures.
- **Missing Code:** Code templates do not contain age restriction gates or automated decision-making transparency notices for Australian users.
- **Missing Disclosure:** Onboarding screens omit mandatory disclosures regarding automated processing significantly affecting rights.
- **Missing Logging:** Logging schemas for tracking age assurance attempts, verification data destruction, and automated decision logs are missing.
- **Missing Testing:** Automated tests verifying that under-16 accounts are prevented from opening social feeds on Australian storefronts are missing.
- **Missing Evidence:** Compliance evidence templates (eSafety Commissioner risk assessment summaries, age data destruction logs) are missing.
- **Missing Audit Trail:** Unalterable audit records tracking social feature gating, age verification attempts, and Privacy Act policy reviews are absent.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Lei n. 15.211/2025 (Digital ECA) and Decreto n. 12.880/2026 mandate strict age verification (CPF database, facial matching, document verification), banning simple checkbox self-declaration. Enforceable from 17 March 2026.

Official Citations: Lei n. 15.211/2025 and Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no Brazil Minor Protection and Age Verification Policy template.
- **Missing Documentation:** Step-by-step developer guides for integrating ANPD-approved age verification APIs (CPF, facial estimation) are missing.
- **Missing Code:** Codebase templates lack native interfaces for CPF validation, facial matching integration, or automatic 18-plus loot-box gating.
- **Missing Disclosure:** Storefront and in-app flows fail to disclose that age data is collected exclusively to satisfy the Digital ECA.
- **Missing Logging:** Backend schemas for capturing guardian authorization, CPF verification status, and immediate document purging are missing.
- **Missing Testing:** Integration tests verifying that unverified Brazilian accounts are blocked from adult features or loot boxes are missing.
- **Missing Evidence:** Templates for ANPD compliance reports, age verification data destruction logs, and guardian consent forms are missing.
- **Missing Audit Trail:** Immutable logs recording verification requests, guardian authorizations, and age verification system audits are absent.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
DPDPA 2023 and DPDP Rules 2025 (G.S.R. 846(E)) mandate verifiable parental consent for users under 18 (via DigiLocker or registered Consent Managers), prohibit behavioral tracking/targeted ads to children, and require synthetic content labeling.

Official Citations: Digital Personal Data Protection Act 2023 and DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template India Minor Data Protection Policy or Registered Consent Manager Integration Policy is provided.
- **Missing Documentation:** Guidelines detailing DigiLocker parental consent integration and under-18 ad tracking prohibition are missing.
- **Missing Code:** Code templates do not include Consent Manager API wrappers, DigiLocker integration hooks, or synthetic content labels.
- **Missing Disclosure:** Privacy notices fail to present clear, multilingual consent notices in all 22 scheduled Indian languages per DPDPA rules.
- **Missing Logging:** Database logging schemas for capturing Consent Manager tokens, parental consent receipts, and synthetic content takedowns are missing.
- **Missing Testing:** Automated tests verifying that all ad tracking SDKs are hard-disabled for under-18 Indian accounts are missing.
- **Missing Evidence:** Verification evidence templates (DigiLocker consent transaction records, Data Protection Board registration) are missing.
- **Missing Audit Trail:** Immutable records tracking consent receipts, withdrawal requests, and multilingual notice updates are absent.

---

## 18. Singapore Personal Data Protection Act and IMDA Code

### 18.1 Regulatory Overview and Background
Personal Data Protection Act 2012 and IMDA Code of Practice for Online Safety (effective 1 April 2026) require app stores and developers to screen and prevent under-18s from downloading age-inappropriate apps using credit card or digital verification.

Official Citations: Personal Data Protection Act 2012 and IMDA Code of Practice for Online Safety.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no Singapore Online Safety and Minor Protection Policy template.
- **Missing Documentation:** Developer guides lack documentation on integrating IMDA age assurance signals and handling 3-day data breach notifications.
- **Missing Code:** Native code templates lack logic to handle Singapore storefront age signals or execute 3-day breach reporting routines.
- **Missing Disclosure:** In-app flows omit mandatory notices explaining that age signals are retrieved per IMDA safety codes.
- **Missing Logging:** Backend schemas for capturing age signal receipts, verification data purging, and breach notification logs are missing.
- **Missing Testing:** Integration tests verifying that minor accounts on the Singapore storefront cannot access 18-plus content are missing.
- **Missing Evidence:** Templates for IMDA compliance attestations and Data Protection Officer (DPO) registration records are missing.
- **Missing Audit Trail:** Immutable logs recording age assurance checks, DPO appointment records, and breach response histories are absent.

---

## 19. South Korea Telecommunications Business Act and PIPA

### 19.1 Regulatory Overview and Background
Telecommunications Business Act Article 22-9 mandates alternative in-app payment options (StoreKit External Purchase KR). PIPA Act No. 21445 (effective 11 Sept 2026) imposes CEO accountability, mandatory CPO appointment, and punitive fines.

Official Citations: Telecommunications Business Act Article 22-9 and PIPA Amendment Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no South Korea In-App Payment Policy or PIPA CPO Governance Policy.
- **Missing Documentation:** Developer manuals lack step-by-step instructions for `com.apple.developer.storekit.external-purchase` (KR) integration and monthly 15-day sales reporting.
- **Missing Code:** Mocks lack implementation code for displaying mandatory Korean pre-payment disclosure modals or handling KCP/Toss payment gateways.
- **Missing Disclosure:** Checkout flows fail to display the required native modal sheet informing Korean users of alternative billing terms and lost platform protections.
- **Missing Logging:** Logging schemas for tracking alternative billing sales volume, 15-day monthly remittance reports, and CPO approvals are missing.
- **Missing Testing:** Automated tests verifying that Korean alternative payment flows render the required modal sheet and execute reporting are missing.
- **Missing Evidence:** Templates for monthly sales reports submitted to Apple/Google and board-approved CPO designation records are missing.
- **Missing Audit Trail:** Immutable logs tracking alternative billing transaction records, CPO privacy reviews, and regulatory reporting filings are absent.

---

## 20. China Mobile App Filing and CAC AI Measures

### 20.1 Regulatory Overview and Background
MIIT Mobile App Filing (ICP extension) is mandatory for app distribution in China. CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, effective 15 July 2026) mandates minor identification, automatic minors mode, and prohibition of virtual companion/kin services for minors.

Official Citations: MIIT Mobile App Filing Provisions and CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no China App Filing & Cross-Border Data Transfer Policy or CAC AI Anthropomorphic Services Policy.
- **Missing Documentation:** Guidelines detailing MIIT ICP filing procedures, local Chinese entity partnership requirements, and CAC AI filing steps are missing.
- **Missing Code:** Code templates lack automatic Minors Mode switching logic, real-name verification (ID/phone) hooks, or minor chatbot access blocks.
- **Missing Disclosure:** Onboarding screens omit mandatory real-name verification disclosures and MIIT ICP filing number displays.
- **Missing Logging:** Backend logging schemas for recording real-name verification checks, minors mode triggers, and CAC AI safety logs are missing.
- **Missing Testing:** Automated tests verifying that AI chatbot features automatically disable virtual companion modes when minor signals are present are missing.
- **Missing Evidence:** Templates for MIIT ICP filing certificates, CAC AI security assessment filings, and Banhao game licenses are missing.
- **Missing Audit Trail:** Immutable logs tracking real-name verification events, CAC security assessment updates, and minors mode activation logs are absent.

---

## 21. Consolidated Gap Classification Matrix

The table below provides a comprehensive evaluation across all twenty major global and regional regulations, evaluating each framework across the eight required gap categories.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA & Amended Rule** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA/CPRA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act & ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & DPDP Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Comprehensive Remediation and Action Plan

To systematically address the gaps identified across all twenty regulatory frameworks, the repository roadmap prioritizes remediation as follows:

1. **Immediate High-Priority Framework Additions (Q3 2026):**
   - Establish full end-to-end detection rules in `data/rejection-patterns.json` and `data/detection-recipes.json` for EU GPSR, EU e-Evidence, EU Withdrawal Button, US ASAA, and EU AI Act Articles 4 & 50.
   - Build UI components and mock implementations in `references/` demonstrating compliant GPSR manufacturer cards, 14-day withdrawal sheets, C2PA synthetic media marking, and GPC headers.

2. **Global & Regional Operational Compliance Layer (Q4 2026):**
   - Expand `agent-os/hooks/app-store-compliance-guard.sh` and `scripts/release-audit.py` to statically audit all twenty frameworks prior to release certification.
   - Integrate automated test runners verifying end-to-end user flows for parental consent, 24-hour UGC moderation, 8-hour e-Evidence extraction, and one-click subscription cancellation.

3. **Logging, Audit Trail, and Evidence Packaging (Q1 2027):**
   - Publish standardized compliance evidence templates (DPIA forms, written Information Security Programs, BIPA consent releases, VPAT EN 301 549 statements) in `templates/`.
   - Implement reference backend logging schemas for tamper-proof cryptographic audit trails capturing consent events, verification data purges, and automated decision-making disclosures.

---

## 23. Sources

Every regulation named above, at its primary source:

- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California Privacy (CCPA/CPRA), [Cal. Civ. Code section 1798.100](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act, [Online Safety Act 2023](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Online Safety Act, [Online Safety Amendment Act 2024](https://www.legislation.gov.au/)
- Brazil Digital ECA, [Lei n. 15.211/2025](https://www.planalto.gov.br/)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore PDPA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/)
- South Korea TBA & PIPA, [Telecommunications Business Act & PIPA](https://law.go.kr/)
- China CAC AI Measures, [CAC Order No. 21 (2026)](https://www.cac.gov.cn/)
