# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the repository itself. It takes twenty major global and regional regulations that bind app developers and digital product teams shipping into the European Union, United States, United Kingdom, Canada, Australia, Brazil, India, Singapore, South Korea, and China, and checks honestly how far this repository carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere to the strict source trust hierarchy.
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind. Assume the repository is incomplete unless proven otherwise.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges of online marketplaces, digital products, and complex supply chains. The GPSR applies to all non-food consumer products placed on the EU market. For digital platforms and software, the GPSR mandates displaying product safety warnings, instructions, manufacturer/importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook gives a developer no way to decide whether their listing falls inside Regulation (EU) 2023/988, and no template policy to define EU Responsible Person obligations or product safety governance.
- **Missing Documentation:** The repository lacks developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:** The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements. Additionally, mock user interfaces lack code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
- **Missing Disclosure:** Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address (email or website) as required under Article 19.
- **Missing Logging:** There are no architectural provisions or schemas for logging product safety incidents, user injury reports, safety recalls, or corrective action triggers.
- **Missing Testing:** No automated tests exist to verify that online interface elements dynamically display required product safety information, manufacturer details, or warning notices based on user geographic region.
- **Missing Evidence:** The repository lacks templates of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:** There is no audit trail or historical record system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented in response to a safety alert.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining the designation of an EU-based Responsible Person and product classification criteria.
2. Incorporate GPSR-specific metadata requirements (manufacturer address, email, product identifier) into rejection patterns and pre-submission checklists.
3. Add UI templates demonstrating compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script that verifies the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. Adopted in 2023, mandatory compliance enforcement begins on 18 August 2026. Judicial authorities of an EU Member State can issue orders directly to service providers offering services in the EU. Default compliance windows require producing data within 10 days, or within a strict 8-hour emergency window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no template Law Enforcement Request Policy or e-Evidence procedure defining who may validate and execute EU judicial production/preservation orders.
- **Missing Documentation:** Concrete operational runbooks or manuals for handling 10-day standard production orders and 8-hour emergency extraction orders are absent.
- **Missing Code:** There are no automated scripts, helper methods, or secure API endpoints in the backend mock implementations to filter, export, package, and encrypt user data in response to a valid legal order.
- **Missing Disclosure:** Public-facing privacy policies fail to explicitly disclose to EU users that data may be preserved or disclosed to European law enforcement pursuant to Regulation (EU) 2023/1543.
- **Missing Logging:** The repository lacks database schemas or logging modules designed to track incoming law enforcement requests, certificate verification statuses, data access activities, or data releases.
- **Missing Testing:** There are no integration tests or simulation routines to validate the rapid 8-hour emergency data retrieval and secure packaging pipeline.
- **Missing Evidence:** Verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) are not present for verification workflows.
- **Missing Audit Trail:** An unalterable, cryptographically signed audit trail recording every administrative interaction, data extraction, and transmission made during a legal request is completely absent.

### 2.3 Remediation and Action Plan
1. Draft and implement a comprehensive Law Enforcement Response Protocol defining roles and secure communication channels for executing EPOs.
2. Formally designate an EU legal representative and notify the designated central authority prior to the August 2026 deadline.
3. Build secure backend scripts to automate extraction and encryption of requested datasets within the 8-hour emergency window.
4. Establish a tamper-proof audit trail to log incoming certificates, verification steps, data extractions, and transmissions.

---

## 3. EU Contract Withdrawal Button Directive

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 on distance marketing of consumer financial services amends Directive 2011/83/EU. It mandates a prominent, easily accessible withdrawal button or cancellation function on online interfaces for distance contracts. Member States apply these rules starting 19 June 2026. The statutory withdrawal period is 14 days, and the cancellation path must be at least as simple as the subscription sign-up path.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no template policy for the 14-day statutory withdrawal right, and no clear guidance separating financial services scope from general subscription defaults.
- **Missing Documentation:** UI design guidelines and checklists specifying placement, prominence, contrast, and terminology required for a compliant withdrawal button are missing.
- **Missing Code:** Front-end components and billing mocks lack a functional implementation of an in-app withdrawal button, confirmation modal, or automated revocation handler.
- **Missing Disclosure:** Subscription registration screens do not prominently disclose the 14-day statutory right of withdrawal or provide direct links explaining contract revocation terms.
- **Missing Logging:** No logging mechanisms exist to capture timestamps, user identifiers, withdrawal button clicks, confirmation receipts, or refund initiation triggers.
- **Missing Testing:** Automated UI or end-to-end tests verifying frictionless contract termination without customer support intervention are missing.
- **Missing Evidence:** Templates for revocation confirmation receipts, standardized withdrawal forms, or refund proof artifacts are absent.
- **Missing Audit Trail:** Historical tracking of contract cancellations, refund processing logs, and UI change histories for the withdrawal path is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent "Withdrawal Button" UI component within account settings across mobile and web platforms.
3. Establish structured logging for cancellation requests, timestamps, and automated refund workflows.
4. Implement end-to-end automated UI tests verifying frictionless self-service contract withdrawal.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (such as Utah SB 142, Texas SB 2420, Louisiana HB 977/HB 570, Alabama HB 161) regulate minors' access to mobile applications, digital purchases, and content updates. Developers must obtain and verify age category signals (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and enforce verifiable parental consent for minor accounts while purging raw age verification data immediately after processing.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook has no template Minor Safety Policy specifying how state-level location checks, age category signals, and minor account restrictions are governed.
- **Missing Documentation:** Step-by-step developer guides for integrating Apple's Declared Age Range API and Google's Play Age Signals API in unified cross-platform codebases are absent.
- **Missing Code:** Code Mocks and platform handlers do not integrate native age signal APIs to restrict app access or digital purchases dynamically for minor users.
- **Missing Disclosure:** Onboarding interfaces do not inform users that age categories are processed to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:** Secure backend handlers for logging parental consent verification, consent revocation notifications, and immediate age document purging are missing.
- **Missing Testing:** Test suites lack integration tests verifying that minor accounts without parental consent are blocked from completing in-app purchases or accessing adult content.
- **Missing Evidence:** Example parental consent agreements, identity verification logs, and data minimization verification records are missing.
- **Missing Audit Trail:** An immutable audit trail recording age verification feature deployments, policy revisions, and data deletion receipts is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy detailing state signal handling and child data minimization.
2. Implement cross-platform native hooks querying Apple Declared Age Range and Google Play Age Signals APIs during onboarding.
3. Build backend automated cleanup scripts to purge raw age verification documents immediately upon category determination.
4. Establish automated unit and integration tests verifying minor purchase blocks in the absence of valid consent flags.

---

## 5. EU AI Act (Regulation (EU) 2024/1689)

### 5.1 Regulatory Overview and Background
Regulation (EU) 2024/1689 (EU AI Act) establishes a comprehensive harmonized legal framework for artificial intelligence. Article 4 mandates AI literacy across organizations deploying AI systems. Article 50 enforces strict transparency obligations, requiring direct user disclosures when interacting with AI and machine-readable output watermarking (e.g., C2PA) for AI-generated content. Annexes define high-risk classification criteria and compliance requirements.

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no template AI Governance Policy, AI Literacy Policy under Article 4, or Synthetic Media Disclosure Policy under Article 50.
- **Missing Documentation:** Detailed technical developer instructions on implementing C2PA metadata watermarking, deepfake disclosures, and high-risk AI risk assessments are missing.
- **Missing Code:** Codebases lack helper classes or middleware for injecting machine-readable watermarks into generated text, audio, image, or video assets, and lack dynamic in-app AI interaction banners.
- **Missing Disclosure:** Chat and generation UI templates fail to display mandatory immediate disclosures ("You are interacting with an AI system") prior to initial user engagement.
- **Missing Logging:** Logging schemas to capture user exposure to AI transparency notices, model version disclosures, and moderation flags are absent.
- **Missing Testing:** Automated tests scanning generated media outputs for machine-readable watermarking headers or validating disclosure notice renders are missing.
- **Missing Evidence:** Factual evidence templates such as Fundamental Rights Impact Assessments (FRIA), technical documentation files under Article 11, and model safety evaluation records are missing.
- **Missing Audit Trail:** Unalterable audit trails tracking model updates, training data lineage, transparency disclosure revisions, and human oversight interventions are absent.

### 5.3 Remediation and Action Plan
1. Publish an internal AI Governance and Literacy Policy outlining competency frameworks and transparency standards.
2. Embed C2PA watermarking utilities into synthetic media pipelines.
3. Implement mandatory in-app AI interaction disclosures on all AI-driven UI screens.
4. Establish automated tests verifying watermark preservation and disclosure rendering.

---

## 6. EU Digital Markets Act (DMA)

### 6.1 Regulatory Overview and Background
The EU Digital Markets Act, Regulation (EU) 2022/1925, regulates gatekeeper platforms to ensure fair and contestable digital markets. For mobile developers, the DMA enables alternative app marketplaces, web distribution, third-party payment integration, and cross-service interoperability without discriminatory platform penalties.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no operational policy for distributing apps via alternative market channels or managing side-loaded/alternative store builds.
- **Missing Documentation:** Guides detailing how to configure build targets for EU alternative distribution (e.g., Apple EU ADPLA Attachment 14, CTFee/CTC compliance) are missing.
- **Missing Code:** Build scripts and environment configs do not contain conditional build targets or feature flags for alternative payment flows or external link entitlements.
- **Missing Disclosure:** In-app payment screens lack explicit user notices when diverting from default app store billing to external payment gateways.
- **Missing Logging:** Payment tracking modules lack schemas to log external purchase transaction IDs and fee calculation metrics required for gatekeeper reporting.
- **Missing Testing:** Automated test suites do not validate alternative entitlement links or side-loaded application update checks.
- **Missing Evidence:** Standardized template records documenting gatekeeper interoperability requests or CTFee/CTC calculation spreadsheets are absent.
- **Missing Audit Trail:** An audit log tracking distribution channel switching, fee reporting submissions, and external payment entitlement grants is missing.

### 6.3 Remediation and Action Plan
1. Draft an Alternative Distribution and Interoperability Strategy guide.
2. Configure conditional build targets supporting external billing and alternative marketplace distributions.
3. Build transaction reporting logging modules for external link purchases.
4. Create automated verification scripts for gatekeeper entitlement configurations.

---

## 7. EU Digital Services Act (DSA)

### 7.1 Regulatory Overview and Background
The EU Digital Services Act, Regulation (EU) 2022/2065, sets rules for online intermediary services, platforms, and marketplaces. Requirements include Trader Status declarations under Article 30 (KYCT), Notice and Action mechanisms under Article 16, illegal content moderation transparency, dark pattern prohibitions under Article 25, and recommender system transparency under Article 27.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a formal DSA Content Moderation Policy, Notice and Action Protocol, and Trader Verification Policy.
- **Missing Documentation:** Step-by-step documentation explaining how developers must publish Trader declarations, manage user reporting channels, and handle appeal mechanisms is missing.
- **Missing Code:** User-generated content (UGC) UI templates lack functional "Flag Content / Notice and Action" components, illegal content intake modals, or dark-pattern-free cancellation flows.
- **Missing Disclosure:** Store listings and in-app profiles lack prominent displays of Trader identity (address, phone, email, register) and recommender system main parameters.
- **Missing Logging:** Database schemas for logging notice receipts, moderation decisions, appeal outcomes, and redressing timelines are missing.
- **Missing Testing:** Automated tests verifying that content flagging endpoints accept reports and generate ticket IDs are absent.
- **Missing Evidence:** Templates for DSA Transparency Reports (Article 15/24) and Trader verification certificate repositories are missing.
- **Missing Audit Trail:** An immutable audit log capturing moderator actions, automated moderation algorithm decisions, and appeal workflows is absent.

### 7.3 Remediation and Action Plan
1. Create a DSA Compliance Framework covering Trader declarations and Notice and Action workflows.
2. Implement in-app content reporting modal components for UGC apps.
3. Build logging modules to record notice timestamps, moderator decisions, and appeal statuses.
4. Generate automated DSA Transparency Report templates.

---

## 8. European Accessibility Act (EAA)

### 8.1 Regulatory Overview and Background
The European Accessibility Act, Directive (EU) 2019/882, mandates accessibility requirements for products and services placed on the EU market, becoming enforced on 28 June 2025. Mobile applications, e-commerce, banking, e-books, and digital services must meet technical harmonized standards (EN 301 549 aligned with WCAG 2.1 AA).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks an organizational Accessibility Policy defining WCAG 2.1 AA / EN 301 549 compliance standards and remediation timelines.
- **Missing Documentation:** Technical developer manuals detailing screen reader support (VoiceOver/TalkBack), dynamic type scaling, focus order, color contrast ratios, and touch target sizing guidelines are missing.
- **Missing Code:** Mock UI components lack explicit accessibility labels, semantic traits, contrast compliance variables, or Reduce Motion animation hooks.
- **Missing Disclosure:** Public Accessibility Statements (disclosing compliance status, non-accessible content, and feedback mechanisms) are absent from app templates and store listings.
- **Missing Logging:** Systems for logging accessibility barrier user feedback, support requests, and accessibility audit defect tickets are missing.
- **Missing Testing:** Automated accessibility regression suites (e.g., automated contrast, screen reader label, and scaling checks) are not fully integrated into standard build guards.
- **Missing Evidence:** Templates for EU Declarations of Conformity under EAA Article 15 and third-party accessibility audit certificates are missing.
- **Missing Audit Trail:** An audit log tracking accessibility defect discovery, remediation commits, and periodic expert accessibility evaluations is absent.

### 8.3 Remediation and Action Plan
1. Draft an Accessibility Policy mandating WCAG 2.1 AA and EN 301 549 standards.
2. Integrate accessibility UI components with explicit labels, dynamic type, and touch target checks.
3. Publish in-app Accessibility Statement templates with user feedback channels.
4. Configure automated accessibility scanning scripts within CI pipeline runs.

---

## 9. Children's Online Privacy Protection Act (COPPA) & Amended FTC Rule

### 9.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (16 CFR Part 312) and the FTC's Amended COPPA Rule regulate collection of personal data from children under 13. Requirements mandate Verifiable Parental Consent (VPC), strict data minimization, prohibitions on targeted advertising, separate opt-in consent for third-party disclosures, and immediate deletion of children's personal records upon request.

Official Citation: 16 CFR Part 312 (FTC COPPA Rule and 2026 Modernized Enforcement Statements).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a dedicated COPPA Compliance Policy defining child-directed app criteria, age-gating procedures, and third-party SDK exclusion protocols.
- **Missing Documentation:** Implementation guides for Verifiable Parental Consent mechanisms (e.g., credit card micro-charge, knowledge-based verification, facial age estimation) are missing.
- **Missing Code:** App templates lack native age-gating screens, neutral age screen components, or conditional SDK initialization wrappers disabling tracking for child users.
- **Missing Disclosure:** Specific Direct Notice to Parents templates and separate COPPA-compliant privacy policy disclosures are missing.
- **Missing Logging:** Database structures logging parent consent events, consent scope, verification method used, and deletion requests are absent.
- **Missing Testing:** Automated test routines verifying that ad networks and analytics SDKs are suppressed when an under-13 age is entered are missing.
- **Missing Evidence:** Sample Safe Harbor certification documentation and parental consent verification records are missing.
- **Missing Audit Trail:** An unalterable log tracking child data retention schedules, automated deletion execution, and annual COPPA policy reviews is absent.

### 9.3 Remediation and Action Plan
1. Establish a written COPPA and Child Data Protection Policy.
2. Implement neutral age-gating UI components and conditional SDK initializer modules.
3. Build backend data retention and deletion pipelines for child records.
4. Construct automated integration tests confirming ad network suppression for minor profiles.

---

## 10. California Privacy Framework (CCPA / CPRA / CPPA Regulations)

### 10.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) as amended by the CPRA and enforced by the California Privacy Protection Agency (CPPA) regulates personal information processing. Mandatory rules include "Do Not Sell or Share My Personal Information" links, Global Privacy Control (GPC) signal recognition, Opt-Out Preference Signal (OOPS) handling, risk assessments (11 CCR section 7155), cybersecurity audits, and sensitive personal information limits.

Official Citation: California Civil Code section 1798.100 et seq., 11 CCR section 7000 et seq.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a California Privacy Rights Policy covering consumer rights requests (DSAR), opt-out mechanisms, and sensitive data processing rules.
- **Missing Documentation:** Developer instructions detailing how web and mobile apps must catch and parse HTTP `Sec-GPC` headers or native GPC signals are missing.
- **Missing Code:** App templates lack GPC auto-sensing middleware, "Do Not Sell/Share" toggle components, or DSAR submission API endpoints.
- **Missing Disclosure:** Specific California Notice at Collection templates and Notice of Right to Opt-Out disclosures are absent.
- **Missing Logging:** Backend logging modules to record consumer opt-out preferences, DSAR request dates, fulfillment timestamps, and verification steps are missing.
- **Missing Testing:** Automated tests verifying that receiving a GPC signal automatically toggles user tracking status to opt-out are missing.
- **Missing Evidence:** Templates for annual CPPA Risk Assessments, Cybersecurity Audit certificates, and DSAR metrics reports are missing.
- **Missing Audit Trail:** An audit log documenting changes to data retention schedules, opt-out preference updates, and DSAR handling timelines is absent.

### 10.3 Remediation and Action Plan
1. Draft a California Privacy Rights Policy and DSAR standard operating procedure.
2. Build GPC header parsing middleware and native opt-out signal handlers.
3. Create Notice at Collection and Opt-Out UI components.
4. Implement automated integration tests validating GPC opt-out enforcement.

---

## 11. Illinois Biometric Information Privacy Act (BIPA)

### 11.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14) regulates collection, capture, storage, retention, and destruction of biometric identifiers or information (fingerprints, voiceprints, facial scans). Requirements mandate prior written consent, a publicly available retention schedule, strict destruction guidelines, and prohibitions on selling or profiting from biometric data.

Official Citation: 740 ILCS 14 (Biometric Information Privacy Act).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no Biometric Data Governance Policy or public retention/destruction policy required under 740 ILCS 14/15(a).
- **Missing Documentation:** Guidelines explaining how mobile apps utilizing facial recognition, voice authentication, or biometric SDKs must structure written releases are missing.
- **Missing Code:** Mobile UI templates lack explicit BIPA written release modals, biometric consent capture screens, or automated biometric template purge routines.
- **Missing Disclosure:** Standalone in-app disclosures informing users of the specific purpose and length of term for biometric data storage are missing.
- **Missing Logging:** Database structures logging written consent agreements, biometric sample creation timestamps, and deletion confirmation logs are missing.
- **Missing Testing:** Automated tests verifying that biometric capture APIs cannot execute prior to consent database flag confirmation are missing.
- **Missing Evidence:** Templates for executed biometric written releases and certificate of biometric destruction records are missing.
- **Missing Audit Trail:** An immutable audit log capturing biometric template lifecycles, destruction schedule execution, and annual policy reviews is absent.

### 11.3 Remediation and Action Plan
1. Create a written Biometric Information Privacy Policy and destruction schedule.
2. Build explicit BIPA written consent modal components for apps utilizing biometric features.
3. Implement automated cleanup jobs to destroy biometric templates upon purpose completion.
4. Set up integration tests verifying biometric SDK blocking prior to consent receipt.

---

## 12. US & UK Subscription Cancellation Regimes (FTC Click-to-Cancel / UK DMCC Act 2024)

### 12.1 Regulatory Overview and Background
The FTC's Rule on Recurring Subscriptions (Click-to-Cancel, 16 CFR Part 425) and the UK Digital Markets, Competition and Consumers Act 2024 (DMCC Act, Part 4 Chapter 2) strictly regulate subscription products. Marketers must provide a cancellation mechanism that is as easy to use as the enrollment process (click-to-cancel), deliver clear pre-sale disclosures, obtain explicit consent for recurring charges, send renewal notices, and avoid dark patterns.

Official Citations: FTC Rule 16 CFR Part 425 (2024/2025/2026), UK DMCC Act 2024 c. 13.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a Subscription Lifecycle Policy defining clear cancellation standards, auto-renewal notification intervals, and refund terms.
- **Missing Documentation:** Design guides detailing compliant paywall architecture, opt-in disclosures, renewal reminder timing, and frictionless cancellation flows are missing.
- **Missing Code:** Billing code templates lack self-service single-click cancellation endpoints, pre-renewal notification triggers, or dark-pattern-free cancellation UI screens.
- **Missing Disclosure:** Paywall templates fail to display unambiguous, prominent recurring charge terms immediately adjacent to the call-to-action button.
- **Missing Logging:** Backend systems lack logging schemas to record subscription enrollment consent, pre-sale disclosure displays, renewal notice delivery receipts, and cancellation requests.
- **Missing Testing:** Automated UI tests confirming that cancellation requires no more steps than sign-up and contains no forced retention surveys are missing.
- **Missing Evidence:** Sample renewal notice templates, consent confirmation emails, and paywall screenshot audit archives are missing.
- **Missing Audit Trail:** An audit log tracking paywall wording revisions, cancellation conversion metrics, and renewal notification delivery records is absent.

### 12.3 Remediation and Action Plan
1. Formulate a Subscription Transparency and Click-to-Cancel Policy.
2. Upgrade paywall and account settings templates to include prominent disclosures and frictionless cancellation buttons.
3. Implement automated pre-renewal notification triggers and cancellation logging endpoints.
4. Establish automated UI tests checking cancellation step counts against sign-up step counts.

---

## 13. UK Online Safety Act 2023 (OSA)

### 13.1 Regulatory Overview and Background
The UK Online Safety Act 2023 places illegal content risk assessment, child safety duties, age assurance obligations, and priority content duties on user-to-user and search services. Enforced by Ofcom, platforms must prevent children from accessing harmful content, perform statutory risk assessments, enforce robust age verification, and provide clear reporting mechanisms.

Official Citation: Online Safety Act 2023 (c. 50).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks an Online Safety Governance Policy covering Ofcom risk assessment duties, child protection measures, and illegal content removal protocols.
- **Missing Documentation:** Developer guides explaining how to complete an Ofcom-aligned Children's Access Assessment and Illegal Content Risk Assessment are missing.
- **Missing Code:** UI templates lack age assurance integration handlers, UK-specific content filtering toggles, or Ofcom-compliant reporting channels.
- **Missing Disclosure:** Terms of Service templates lack clear disclosures of age limits, content moderation standards, and user rights regarding online safety.
- **Missing Logging:** Systems logging illegal content reports, age assurance verification outcomes, take-down timelines, and Ofcom inquiry responses are absent.
- **Missing Testing:** Automated tests verifying that unverified minor accounts cannot access age-restricted chat or media features in the UK are missing.
- **Missing Evidence:** Templates for official Ofcom Risk Assessment documents, Age Assurance Effectiveness records, and moderation capacity reports are missing.
- **Missing Audit Trail:** An unalterable audit log tracking safety policy updates, content moderation actions, and safety incident escalations is missing.

### 13.3 Remediation and Action Plan
1. Draft an Online Safety Policy and Ofcom Risk Assessment guide.
2. Integrate robust age assurance and content reporting components for UK deployments.
3. Build database logging modules for safety reports and moderation decisions.
4. Create automated test suites verifying minor feature gating under UK rules.

---

## 14. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 14.1 Regulatory Overview and Background
Australia's Online Safety Act 2021 and the Online Safety Amendment (Social Media Minimum Age) Act 2024 enforce strict child protection standards, mandatory age verification, and an under-16 social media ban for age-restricted platforms. Regulated by the eSafety Commissioner, services must take reasonable steps to prevent under-16s from having accounts and comply with registered Industry Codes.

Official Citations: Online Safety Act 2021, Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks an Australian Minimum Age and Safety Policy defining age-gating procedures and eSafety Commissioner compliance protocols.
- **Missing Documentation:** Step-by-step documentation detailing compliant age assurance integration and eSafety Industry Code requirements is missing.
- **Missing Code:** Mobile app templates lack native age verification hooks, under-16 account blocking logic, or eSafety report submission modals.
- **Missing Disclosure:** Registration flows lack prominent disclosures stating that individuals under 16 are prohibited from creating accounts on regulated services in Australia.
- **Missing Logging:** Database structures logging age verification attempts, account suspension events for under-16 users, and eSafety complaint notices are missing.
- **Missing Testing:** Integration tests verifying that Australian IP ranges triggering under-16 age inputs block account registration are absent.
- **Missing Evidence:** Templates for eSafety Safety by Design evaluations and age verification effectiveness audit certificates are missing.
- **Missing Audit Trail:** An audit trail recording account termination actions for under-16 users, policy updates, and regulator correspondence is missing.

### 14.3 Remediation and Action Plan
1. Draft an Australian Online Safety and Under-16 Compliance Policy.
2. Build native age assurance components and under-16 account blocking logic.
3. Implement structured logging for age verification and account termination events.
4. Construct automated integration tests verifying Australian under-16 account registration blocks.

---

## 15. Brazil Digital ECA (Law 15,211/2025 & Decreto n. 12.880)

### 15.1 Regulatory Overview and Background
Brazil's Law 15,211/2025 (Digital ECA / Estatuto da Crianca e do Adolescente Digital) and Decreto n. 12.880 regulate child and adolescent protection in digital environments. Key mandates include age verification, default privacy and safety settings for minors, bans on profiling or targeted advertising directed at children, and clear reporting mechanisms for illegal content.

Official Citations: Law 15,211/2025, Decreto n. 12.880 of 18 March 2026 (Brazil).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no Digital ECA Governance Policy outlining child safety standards and Brazilian regulatory requirements.
- **Missing Documentation:** Developer instructions detailing age-appropriate design, default high-privacy settings for minor accounts in Brazil, and ANPD roadmap steps are missing.
- **Missing Code:** Mocks lack default high-privacy configuration routines for Brazilian minor accounts, age verification components, or child reporting tools.
- **Missing Disclosure:** Privacy policies and onboarding screens lack Portuguese-language disclosures explaining minor data processing limits under Law 15,211/2025.
- **Missing Logging:** Database schemas logging age verification tokens, minor account privacy flag activations, and content reporting events are missing.
- **Missing Testing:** Automated tests verifying that minor accounts in Brazil default to zero targeted advertising and high privacy settings are missing.
- **Missing Evidence:** Templates for Child Impact Assessments under Brazilian law and ANPD compliance declaration forms are missing.
- **Missing Audit Trail:** An immutable audit log tracking minor privacy configuration changes, content moderation actions, and policy revisions is missing.

### 15.3 Remediation and Action Plan
1. Create a written Brazil Digital ECA Compliance Policy.
2. Implement age verification and automated high-privacy defaults for Brazilian minor profiles.
3. Build backend logging for age signals and privacy flag settings.
4. Configure automated tests checking minor account privacy configurations in Brazil.

---

## 16. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 16.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 regulate digital personal data processing. Key obligations include itemized, multi-lingual consent notices, verifiable parental consent for processing data of children (under 18) or persons with disabilities, appointment of a Data Protection Officer (DPO), and data breach notifications to the Data Protection Board of India.

Official Citations: DPDPA 2023 (Act No. 22 of 2023), DPDP Rules 2025 (G.S.R. 846(E)).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no DPDPA Governance Policy defining Data Fiduciary obligations, Consent Manager integration, or child data restrictions in India.
- **Missing Documentation:** Developer guides explaining multi-lingual consent notice rendering (22 schedule languages), parental consent mechanisms, and DPO appointment requirements are missing.
- **Missing Code:** UI templates lack itemized, multi-lingual consent modals, Consent Manager API integration hooks, or verifiable parental consent handlers.
- **Missing Disclosure:** Registration flows lack clear, standalone consent notices detailing processed personal data categories, purpose, and rights to withdraw consent in English and Indian languages.
- **Missing Logging:** Database schemas logging consent timestamps, language presented, withdrawal requests, and breach notification triggers are missing.
- **Missing Testing:** Automated tests verifying that processing stops upon consent withdrawal or that minor profiles block tracking are absent.
- **Missing Evidence:** Templates for Data Protection Impact Assessments (DPIA), DPO appointment letters, and Data Protection Board breach report forms are missing.
- **Missing Audit Trail:** An unalterable audit log tracking consent lifecycle events, Data Fiduciary audit reviews, and parental consent verifications is absent.

### 16.3 Remediation and Action Plan
1. Draft a DPDPA Compliance Policy and Consent Governance guide.
2. Build itemized, multi-lingual consent UI components and Consent Manager API wrappers.
3. Establish structured database logging for consent capture and withdrawal events.
4. Implement automated integration tests verifying immediate processing cessation upon consent revocation.

---

## 17. Singapore Personal Data Protection Act (PDPA) & IMDA Online Safety Code

### 17.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act 2012 (amended 2020/2024) and the IMDA Code of Practice for Online Safety set strict data protection, consent, purpose limitation, breach notification, and child protection requirements. App distribution platforms and online services must implement user safety measures, content moderation, and age-appropriate safeguards.

Official Citations: Personal Data Protection Act 2012 (No. 26 of 2012), IMDA Code of Practice for Online Safety (2023).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a Singapore PDPA and IMDA Safety Policy detailing Data Protection Officer duties, consent frameworks, and safety guidelines.
- **Missing Documentation:** Developer guides explaining how to implement PDPA mandatory 3-day breach notification protocols and IMDA online safety controls are missing.
- **Missing Code:** App templates lack in-app DPO contact links, mandatory consent request dialogs, or IMDA safety report modal dialogs.
- **Missing Disclosure:** Privacy policies lack Singapore-specific disclosures detailing purpose limitation, access/correction rights, and DPO contact details.
- **Missing Logging:** Backend structures logging consent records, access/correction requests, data breach assessments, and safety complaint intake are missing.
- **Missing Testing:** Automated tests verifying that personal data field extraction requires active opt-in consent flags are missing.
- **Missing Evidence:** Templates for PDPC Data Protection Impact Assessments (DPIA) and IMDA Online Safety compliance reports are missing.
- **Missing Audit Trail:** An audit log documenting breach evaluation decisions, DPO reviews, and user access request fulfillments is missing.

### 17.3 Remediation and Action Plan
1. Draft a Singapore PDPA and IMDA Compliance Policy.
2. Implement DPO contact elements and consent intake UI components.
3. Build logging modules for data breach evaluations and user access requests.
4. Construct automated test scripts verifying opt-in consent validation prior to data collection.

---

## 18. South Korea Telecommunications Business Act & PIPA Amendment

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (Article 22-9, alternative in-app billing) and Personal Information Protection Act (PIPA Amendment, Act No. 21445) mandate strict operational requirements. Key rules include allowing third-party in-app payment systems, mandatory local data protection agent appointment for foreign entities, strict privacy notices, and rapid data breach reporting within 24 hours.

Official Citations: Telecommunications Business Act Article 22-9, Personal Information Protection Act (PIPA) Amendment.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no South Korea Regulatory Policy covering alternative billing integration, local agent appointment, or PIPA compliance.
- **Missing Documentation:** Developer guides detailing Korea-specific third-party billing SDK implementation and local agent disclosure formatting are missing.
- **Missing Code:** App build configurations lack conditional hooks for Korean alternative in-app payment gateways or Korean Local Agent contact modals.
- **Missing Disclosure:** In-app screens lack required Korean PIPA privacy notices, including explicit disclosures of foreign data transfers and local agent details.
- **Missing Logging:** Database schemas logging alternative payment fee calculations, transaction IDs, and 24-hour breach assessment logs are missing.
- **Missing Testing:** Automated tests validating alternative billing checkout flows and PIPA consent confirmation flags are missing.
- **Missing Evidence:** Templates for Local Agent Designation contracts and PIPC 24-hour breach notification forms are missing.
- **Missing Audit Trail:** An unalterable audit log capturing alternative billing transaction reports, PIPA policy revisions, and breach assessment timelines is absent.

### 18.3 Remediation and Action Plan
1. Establish a South Korea Billing and PIPA Governance Policy.
2. Build UI components for local agent disclosures and Korean alternative billing integrations.
3. Construct backend transaction logging modules for alternative in-app payments.
4. Implement automated integration tests verifying alternative billing checkout and PIPA disclosures.

---

## 19. China Mobile App Filing (MIIT ICP Extension) & CAC Regulations

### 19.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) Mobile App Filing rules (ICP extension) and Cyberspace Administration of China (CAC) regulations (including Personal Information Protection Law - PIPL, and AI interactive service rules) require all apps distributed in China to complete formal filing, register server infrastructure locally, obtain explicit consent, and enforce real-name identity verification.

Official Citations: MIIT Circular on App Filing (2023), CAC Order No. 21 (AI Services), PIPL (2021).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook carries no China Market Filing and Compliance Policy covering MIIT filing, CAC registration, and PIPL requirements.
- **Missing Documentation:** Developer instructions detailing how to prepare MIIT app filing metadata, real-name authentication integrations, and CAC AI service approvals are missing.
- **Missing Code:** App templates lack real-name identity verification integration hooks, MIIT filing number display components, or PIPL consent screens.
- **Missing Disclosure:** App store metadata and in-app launch screens lack mandatory MIIT filing number displays and PIPL-compliant privacy notices.
- **Missing Logging:** Backend structures logging real-name verification statuses, PIPL data cross-border transfer assessments, and CAC algorithm filing records are missing.
- **Missing Testing:** Automated tests verifying that China distribution builds display the MIIT filing number and block unauthenticated accounts are missing.
- **Missing Evidence:** Templates for MIIT App Filing confirmation receipts, CAC Algorithm Filing records, and PIPL Security Assessment reports are missing.
- **Missing Audit Trail:** An audit log tracking filing updates, real-name verification system audits, and CAC compliance submission histories is absent.

### 19.3 Remediation and Action Plan
1. Formulate a China Distribution and MIIT Filing Policy.
2. Implement MIIT filing number UI components and real-name verification hooks.
3. Establish logging modules for real-name authentication and PIPL transfer records.
4. Build automated tests verifying MIIT filing display and account authentication gating.

---

## 20. EU Cyber Resilience Act (CRA) & Product Liability Directive (PLD)

### 20.1 Regulatory Overview and Background
The EU Cyber Resilience Act (Regulation (EU) 2024/2847) and revised Product Liability Directive (Directive (EU) 2024/2853) regulate digital products with digital elements and software liabilities. CRA mandates cybersecurity by design, mandatory vulnerability reporting within 24 hours, software bill of materials (SBOM), and CE marking. The PLD explicitly classifies software and AI as "products", imposing strict liability for defective software causing harm.

Official Citations: Regulation (EU) 2024/2847 (CRA), Directive (EU) 2024/2853 (PLD).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook lacks a Cybersecurity by Design Policy, Vulnerability Disclosure Policy, and Software Liability Risk Policy.
- **Missing Documentation:** Technical manuals explaining how to generate CycloneDX/SPDX SBOMs, conduct vulnerability handling, and meet CRA CE marking standards are missing.
- **Missing Code:** Build pipelines lack automated SBOM generation scripts, vulnerability scanning integration, or automated 24-hour ENISA breach notification triggers.
- **Missing Disclosure:** Public documentation and store listings lack CE marking declarations, vulnerability contact points (security.txt), and security update window guarantees.
- **Missing Logging:** Systems logging vulnerability reports, patching timelines, security incident evaluations, and SBOM component changes are missing.
- **Missing Testing:** Automated security regression testing, dependency vulnerability scanning, and static analysis guards are not fully integrated into standard release checks.
- **Missing Evidence:** Templates for CRA EU Declarations of Conformity, Technical Documentation files, and third-party security assessment certificates are missing.
- **Missing Audit Trail:** An unalterable audit log tracking vulnerability intake, patch deployment history, SBOM revisions, and security incident response timelines is missing.

### 20.3 Remediation and Action Plan
1. Draft a Cyber Resilience and Software Liability Governance Policy.
2. Integrate automated SBOM generation and dependency vulnerability scanning into build pipelines.
3. Publish `security.txt` and CE declaration templates across repository projects.
4. Establish automated security regression tests and incident logging endpoints.

---

## 21. Consolidated Gap Classification Matrix

This matrix summarizes the compliance evaluation across all twenty audited global and regional regulatory frameworks.
Legend:
- **Covered:** Complete policy, documentation, code, disclosure, logging, testing, evidence, and audit trail exist in the playbook.
- **Partial:** Framework is mentioned or cited in documentation, but lacks complete operational code, tests, or audit implementations.
- **Missing:** Framework or category is entirely absent from the playbook implementation layer.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act (Art 4 / 50 / High Risk)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU Digital Markets Act (DMA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU Digital Services Act (DSA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. European Accessibility Act (EAA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. US COPPA & Amended FTC Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. California Privacy (CCPA/CPRA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US/UK Click-to-Cancel Regimes** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. UK Online Safety Act (OSA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Australia Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. India DPDPA 2023 / Rules 2025** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Singapore PDPA & IMDA Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China Mobile App Filing & CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. EU CRA & Product Liability** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Strategy

The comprehensive gap analysis reveals that while the playbook excels at tracking App Store and Google Play review guidelines and high-level regulatory deadlines, significant implementation gaps exist across code, logging, automated testing, evidence management, and unalterable audit trails.

### Prioritized Remediation Roadmap
1. **Phase 1 - Immediate Code & Guard Rules:** Add detection recipes, patterns, and code UI components for EU GPSR, Contract Withdrawal Button, and AI Act Article 50 disclosures.
2. **Phase 2 - Logging & Audit Infrastructure:** Implement standardized database logging schemas for user consent, age verification purging, DSAR requests, and law enforcement order processing.
3. **Phase 3 - Automated Compliance Testing:** Expand automated test suites to validate accessibility, age-gating, click-to-cancel steps, and GPC signal handling across build targets.
4. **Phase 4 - Policy & Evidence Template Center:** Provide complete, downloadable compliance policy templates, risk assessment forms, and audit trail verification scripts.

---

## 23. Official Primary Sources (Priority 1)

Every regulatory framework cited within this report is traceably grounded in official Priority 1 publications:

- **EU GPSR:** [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **EU e-Evidence Package:** [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **EU Contract Withdrawal Button:** [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **US State ASAA:** Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026)
- **EU AI Act:** [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **EU DMA:** [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **EU DSA:** [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **European Accessibility Act:** [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **US COPPA:** [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- **California CCPA/CPRA:** [California Civil Code section 1798.100](https://cppa.ca.gov/regulations/)
- **Illinois BIPA:** [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- **FTC Click-to-Cancel & UK DMCC Act:** FTC 16 CFR Part 425 & UK DMCC Act 2024 c. 13
- **UK Online Safety Act:** [Online Safety Act 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents/enacted)
- **Australia Online Safety:** Online Safety Act 2021 & Social Media Minimum Age Act 2024
- **Brazil Digital ECA:** Law 15,211/2025 & Decreto n. 12.880
- **India DPDPA:** Digital Personal Data Protection Act 2023 (Act No. 22 of 2023) & DPDP Rules 2025
- **Singapore PDPA:** Personal Data Protection Act 2012 & IMDA Online Safety Code
- **South Korea TBA & PIPA:** Telecommunications Business Act Article 22-9 & PIPA Act No. 21445
- **China Mobile App Filing & CAC:** MIIT Circular on App Filing (2023) & CAC Order No. 21
- **EU CRA & Product Liability:** [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) & [Directive (EU) 2024/2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj)
