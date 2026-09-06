# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile and web application developers shipping into the EU, US, UK, Australia, Brazil, Canada, India, Singapore, South Korea, China, and global storefronts, and checks honestly how far this repository carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere to the strict source trust hierarchy.
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address online marketplaces, digital products, and complex supply chains.

The GPSR applies to non-food consumer products placed on the EU market. For digital systems and e-commerce applications, the GPSR mandates that online interfaces display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no way to decide whether their listing falls inside Regulation (EU) 2023/988, and no template General Product Safety Policy to hand a client or auditor.
- **Missing Documentation:**
  The repository is missing developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements. Additionally, mock user interfaces and templates in this repository do not contain code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address (such as email or website) as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, recalls, or corrective actions. The repository fails to supply templates for a centralized incident log.
- **Missing Testing:**
  No automated tests exist to verify that online interface elements dynamically display required product safety information, manufacturer details, or warning notices based on the user's geographic location.
- **Missing Evidence:**
  The repository lacks physical templates or examples of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no audit trail or historical record system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented in response to a safety alert.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining the designation of an EU-based Responsible Person and product classification criteria.
2. Incorporate GPSR-specific metadata requirements (manufacturer address, email, product identifier) into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory that demonstrate compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script that verifies the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. The mandatory compliance enforcement date is 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window to produce user data is 10 days, but in critical emergency cases, providers are legally required to produce requested data within a strict 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, so a team receiving an EU judicial order has no written operational protocol or authority matrix.
- **Missing Documentation:**
  While the repository mentions the e-Evidence Package in general, it lacks concrete operational runbooks, instructions, or detailed manuals for handling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:**
  There are no automated scripts or secure API endpoints in the repository's backend mock implementations to assist in securely exporting, filtering, and packaging user data in response to a valid legal order.
- **Missing Disclosure:**
  Public-facing documentation, including Privacy Policies, fails to explicitly disclose to EU users that their data may be preserved or disclosed to European law enforcement in accordance with Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository does not contain database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, data access activities, or data releases.
- **Missing Testing:**
  There are no integration tests or validation flows to simulate the rapid 8-hour emergency retrieval and secure packaging of user data under simulated pressure.
- **Missing Evidence:**
  The repository is missing verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for compliance officers to study and verify.
- **Missing Audit Trail:**
  A secure, unalterable audit trail system to record every administrative interaction, data extraction, and transmission made by compliance officers during a legal request is absent.

### 2.3 Remediation and Action Plan
1. Draft and implement a comprehensive Law Enforcement Response Protocol that specifically establishes the roles, responsibilities, and secure communication channels for executing EPOs.
2. Formally designate an EU establishment or legal representative and notify the designated central authority before the 18 August 2026 deadline.
3. Build secure backend scripts to automate the extraction and encryption of requested user datasets within the 8-hour emergency window.
4. Establish a tamper-proof cryptographic audit trail to log all incoming certificates, verification checks, data extractions, and secure transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on online interfaces for distance contracts concluded by electronic means.

The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating apps that fall in scope from those adopting it as a design default.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying the placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
- **Missing Code:**
  Front-end user interface templates and billing mock code in this repository do not contain any functional implementation of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining the terms of contract revocation.
- **Missing Logging:**
  There are no logging mechanisms designed to capture and record when a user clicks the withdrawal button, the timestamp of the request, confirmation of contract termination, or initiation of the refund flow.
- **Missing Testing:**
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible withdrawal button component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a self-service contract termination without manual intervention.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Raw age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect users in Texas, Utah, Louisiana, or Alabama, and how to handle minor accounts.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same project.
- **Missing Code:**
  Although rejection patterns contain entries for state laws, mock client implementations do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  In-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no backend system designed to log parental consent receipt, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests verifying that minor accounts are blocked from gated features or in-app purchases without valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates of parental consent agreements, identity verification logs, or data minimization records to prove compliance to state Attorneys General.
- **Missing Audit Trail:**
  An immutable audit trail recording the rollout of age-assurance features, consent policy changes, and immediate verification data deletion records is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy that specifies how state-level requirements are identified and how children's data is minimized.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and procedures to purge raw age-verification data immediately after age category confirmation.
4. Establish automated unit tests verifying that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is processed.

---

## 5. EU AI Act (Article 4 AI Literacy and Article 50 Transparency)

### 5.1 Regulatory Overview and Background
Regulation (EU) 2024/1689 (EU AI Act) establishes mandatory requirements for AI literacy (Article 4) and transparency (Article 50). Article 4 took effect on 2 February 2025, while Article 50 takes effect on 2 August 2026.

Article 4 requires deployers and providers of AI systems to ensure a sufficient level of AI literacy among personnel. Article 50(1) mandates informing natural persons when interacting with AI systems. Article 50(2) requires synthetic content (text, audio, image, video) to be marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deepfake disclosures.

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Literacy Policy (Art. 4) and no template AI Transparency & Disclosure Policy (Art. 50).
- **Missing Documentation:**
  Documentation lacks developer instructions on machine-readable watermarking (C2PA specification), deepfake disclosure UI guidelines, and staff competency frameworks.
- **Missing Code:**
  Codebase templates lack middle-tier helper utilities to inject machine-readable provenance metadata into generated assets or detect synthetic outputs.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the mandatory in-app notice ("You are interacting with an AI system") prior to or at first interaction.
- **Missing Logging:**
  There are no logging mechanisms to record that an AI transparency disclosure was successfully presented to a user session.
- **Missing Testing:**
  Test suites do not include automated checks to scan generated media outputs for machine-readable watermarking headers or C2PA metadata.
- **Missing Evidence:**
  The repository lacks physical evidence templates, such as an active `AI_LITERACY_LOG.md` tracking staff training, course completion records, or model transparency sheets.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, model updates, literacy training revisions, and disclosure modifications is missing.

### 5.3 Remediation and Action Plan
1. Publish internal AI Literacy and AI Transparency policies defining competency requirements and disclosure guidelines.
2. Maintain an active `AI_LITERACY_LOG.md` within the repository to record team induction and annual refresher dates.
3. Implement C2PA metadata injection inside synthetic media pipelines and prominent AI interaction notices in UI templates.
4. Build automated CI integration tests to verify the presence of synthetic content markers in AI generation outputs.

---

## 6. EU Digital Markets Act (DMA)

### 6.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms (Apple and Google) and provides alternative distribution channels and payment choices for EU users.

Developers distributing apps in the EU can utilize Web Distribution, Alternative App Marketplaces, and alternative payment links. Under Apple's unified terms (effective 1 October 2026), Attachment 14 governs the Core Technology Commission (5%), while external link usage requires calling the `ExternalPurchaseCustomLink` disclosure API.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template EU Distribution and Alternative Payment Policy addressing DMA entitlement options, fee models, and Web Distribution rules.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides for requesting DMA entitlements, configuring External Purchase Server APIs, and accepting Attachment 14 in App Store Connect.
- **Missing Code:**
  Mock clients lack code integration for `ExternalPurchaseCustomLink` system sheets and automated monthly external purchase reporting routines.
- **Missing Disclosure:**
  UI templates omit required system-provided disclosure sheets warning users that transactions outside Apple/Google lack platform purchase protections.
- **Missing Logging:**
  Missing local and server logging schemas for external purchase link taps, entitlement status checks, and monthly sales report generation.
- **Missing Testing:**
  No automated unit tests exist to verify that StoreKit IAP and external offer links are not co-mingled within the same EU storefront build.
- **Missing Evidence:**
  Lacks templates for monthly external purchase reporting files, notarization submission receipts, or stand-by letter of credit documentation for alternative marketplaces.
- **Missing Audit Trail:**
  An immutable audit log recording DMA entitlement declarations, license agreement acceptances, and monthly reporting submissions is absent.

### 6.3 Remediation and Action Plan
1. Formulate an EU DMA Compliance Protocol outlining entitlement selection and monthly reporting workflows.
2. Integrate `ExternalPurchaseCustomLink` API calls and storefront region-gating checks across all external offer code paths.
3. Build automated reporting client scripts to format and submit monthly external purchase transactions.
4. Establish CI checks verifying that StoreKit IAP and external link promotion are strictly segregated per storefront.

---

## 7. EU Digital Services Act (DSA)

### 7.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065), specifically Articles 30 and 31, mandates that app stores verify and display trader identity details for developers distributing apps to EU consumers.

Every developer distributing in the EU must register and verify their DSA trader status (DUNS address, phone number, email, payment account details) or declare non-trader status. Non-compliance results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template DSA Compliance and Content Moderation Policy governing trader registration and illegal content notice-and-action handling.
- **Missing Documentation:**
  Developer checklists lack detailed runbooks for completing DSA trader verification in App Store Connect and Google Play Console.
- **Missing Code:**
  Codebase templates lack UI components for user-facing illegal content reporting or trader identification displays within app account settings.
- **Missing Disclosure:**
  App metadata and in-app account screens omit published DSA trader contact details (verified postal address, phone, email).
- **Missing Logging:**
  Missing logging schemas to capture user content flags, notice-and-action submissions, and DSA verification status updates.
- **Missing Testing:**
  No automated tests exist to check for missing trader declarations or broken illegal content reporting paths.
- **Missing Evidence:**
  Lacks verified copies of DSA trader verification receipts, 2FA validation records, or annual transparency reports.
- **Missing Audit Trail:**
  An unalterable audit log recording trader profile modifications, content moderation decisions, and user appeals is absent.

### 7.3 Remediation and Action Plan
1. Draft a DSA Trader & Moderation Policy establishing procedures for identity verification and illegal content handling.
2. Incorporate DSA trader verification gates into pre-submission checklists and automated guard scripts.
3. Provide UI components for in-app illegal content reporting and trader identity display.
4. Establish an audit log to record content moderation decisions and trader status verification records.

---

## 8. European Accessibility Act (EAA)

### 8.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025. It mandates accessibility for consumer products and services, including mobile applications and e-commerce websites reaching EU consumers.

Technical compliance is governed by harmonised standard EN 301 549 (version 3.2.1), built on WCAG 2.1 Level AA with specific mobile application requirements in Chapter 11.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Organizational Accessibility Policy committing app development to EN 301 549 Chapter 11 and WCAG 2.1 AA.
- **Missing Documentation:**
  Documentation lacks developer guides on implementing Dynamic Type font scaling, VoiceOver/TalkBack traits, and touch target constraints.
- **Missing Code:**
  Mock UI components lack accessible contrast ratios, semantic screen reader traits, and flexible layout constraints.
- **Missing Disclosure:**
  Lacks a published Accessibility Statement (EN 301 549 Annex B and C) embedded in-app and linked on store product pages.
- **Missing Logging:**
  Missing logging mechanisms to record accessibility preference changes (font size scaling, high contrast, reduce motion) for UX adaptation.
- **Missing Testing:**
  While `scripts/accessibility-audit.py` checks basic rules, it lacks complete EN 301 549 Chapter 11 mobile test gauntlets.
- **Missing Evidence:**
  Lacks formal Accessibility Conformance Reports (VPAT / EN 301 549 audit sheets) produced by qualified accessibility auditors.
- **Missing Audit Trail:**
  An unalterable audit log tracking accessibility defect remediations, user accessibility feedback, and periodic re-audits is missing.

### 8.3 Remediation and Action Plan
1. Adopt an Accessibility Compliance Policy referencing EN 301 549 Chapter 11 and WCAG 2.1 Level AA.
2. Expand `scripts/accessibility-audit.py` to cover full EN 301 549 Chapter 11 mobile software requirements.
3. Provide an in-app Accessibility Statement template conforming to EN 301 549 Annex B.
4. Maintain formal VPAT / Accessibility Conformance Reports in the repository's evidence records.

---

## 9. US Children's Online Privacy Protection Act (COPPA and Amended Rule)

### 9.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) applies to operators of commercial websites and online services directed to children under 13, or general audience services with actual knowledge of collecting personal information from children under 13.

The FTC's Amended COPPA Rule (90 FR 16918, general compliance date 22 April 2026) expands personal information to include biometric and government identifiers, requires separate opt-in consent for third-party disclosures, mandates written data retention policies, and requires a written information security program.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an updated COPPA Policy incorporating the 2025/2026 Amended Rule requirements (biometrics, retention limits, security program).
- **Missing Documentation:**
  Lacks developer guides for verifiable parental consent (VPC) methods, biometric data handling, and written retention schedules.
- **Missing Code:**
  Lacks code modules for face-match ID verification, knowledge-based authentication, or automatic child data deletion timers.
- **Missing Disclosure:**
  Privacy policy templates omit explicit disclosures regarding separate opt-in consent for third-party ad sharing and biometric collection.
- **Missing Logging:**
  Missing database logging schemas capturing VPC grant and revocation timestamps, child account creation, and automated data deletion execution.
- **Missing Testing:**
  Test suites lack automated integration tests verifying that child accounts without VPC cannot trigger third-party tracking or data sharing.
- **Missing Evidence:**
  Lacks written Information Security Program documentation, annual risk assessments, or written Data Retention Policies (312.10).
- **Missing Audit Trail:**
  An immutable audit log recording child data purges, VPC consent modifications, and annual security program reviews is missing.

### 9.3 Remediation and Action Plan
1. Update COPPA compliance documentation to include the 2026 Amended Rule requirements.
2. Draft a written Data Retention Policy (312.10) and Information Security Program outline.
3. Build backend scripts to enforce automatic deletion of children's data upon expiration of retention periods.
4. Implement automated tests verifying that third-party SDK initialization is suppressed for child users until VPC is logged.

---

## 10. California Privacy Framework (CCPA, CPRA, CPPA 2026, AB 1043, SB 976)

### 10.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and 2026 CPPA regulations, governs consumer data privacy rights in California. Companion laws include AB 1043 (Digital Age Assurance Act) and SB 976 (social media addiction).

Requirements include notices at collection, rights to know, delete, correct, "Do Not Sell or Share Personal Information" controls, Global Privacy Control (GPC) support, sensitive data limitations, and minor protections.

Official Citations: California Civil Code Sec. 1798.100 et seq.; California AB 1043; California SB 976.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive California Privacy Policy covering CCPA/CPRA rights, GPC signals, automated decision-making, and minor feed restrictions.
- **Missing Documentation:**
  Missing developer implementation guides for parsing Global Privacy Control (GPC) headers, handling "Do Not Sell/Share" requests, and age signals under AB 1043.
- **Missing Code:**
  Lacks code hooks to parse `Sec-GPC` headers in webviews, propagate opt-out signals to ad SDKs, or restrict addictive feeds under SB 976.
- **Missing Disclosure:**
  Onboarding and account settings screens lack "Do Not Sell or Share My Personal Info" and "Limit Use of Sensitive PI" links and notices.
- **Missing Logging:**
  Missing logging schemas capturing consumer rights requests (know, delete, opt-out), GPC signal detections, and opt-out preference updates.
- **Missing Testing:**
  Lacks automated tests verifying that GPC header detection immediately halts third-party data sales and targeted ad tracking.
- **Missing Evidence:**
  Lacks data broker DROP registration records, automated decision-making risk assessments, or cybersecurity audit certifications.
- **Missing Audit Trail:**
  An unalterable audit log recording consumer rights fulfillment history, GPC opt-out processing, and privacy notice updates is absent.

### 10.3 Remediation and Action Plan
1. Formulate a California Privacy Policy incorporating GPC signal enforcement and minor protection controls.
2. Build code handlers to detect `Sec-GPC` headers and automatically disable targeted ad tracking across native and web interfaces.
3. Establish database schemas to log consumer rights requests and track fulfillment deadlines (45 days).
4. Implement automated CI tests validating that GPC signals suppress data collection endpoints.

---

## 11. Illinois Biometric Information Privacy Act (BIPA)

### 11.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14/) regulates the collection, use, safeguarding, and handling of biometric identifiers and information (retina/iris scans, fingerprints, voiceprints, scan of hand or face geometry).

BIPA requires written notice, written consent prior to collection, a publicly available retention schedule, destruction within 3 years of last interaction (or when purpose is satisfied), and prohibits sale or profit from biometric data. SB 2979 (effective August 2024) clarifies violation liability per individual.

Official Citation: 740 ILCS 14/ (Illinois Biometric Information Privacy Act).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Biometric Information Privacy Policy establishing notice, consent, retention schedules, and destruction guidelines.
- **Missing Documentation:**
  Missing developer guides for obtaining written or electronic biometric releases before capturing voice, face, or fingerprint data.
- **Missing Code:**
  Lacks UI release modal sheets for BIPA consent and backend scripts for automated biometric data destruction within statutory windows.
- **Missing Disclosure:**
  In-app screens capturing biometric data omit written notices stating the specific purpose and duration of biometric storage.
- **Missing Logging:**
  Missing database logging schemas capturing e-signed biometric consents, retention timers, and destruction execution timestamps.
- **Missing Testing:**
  Lacks automated unit tests verifying that biometric feature entry points are blocked until an e-signed BIPA release is logged.
- **Missing Evidence:**
  Lacks publicly available written biometric retention and destruction schedules, consent release templates, or destruction certificates.
- **Missing Audit Trail:**
  An unalterable audit log recording biometric consent receipts, data purges, and annual biometric compliance reviews is missing.

### 11.3 Remediation and Action Plan
1. Draft a BIPA-compliant Biometric Information Privacy Policy and public retention schedule template.
2. Create reusable UI consent modal components that capture e-signed releases prior to biometric collection.
3. Build automated data purge routines to destroy biometric identifiers within 3 years of user inactivity.
4. Add unit tests ensuring biometric SDKs cannot initialize without active consent logs.

---

## 12. US Subscription Cancellation Rules (ROSCA and State Negative Option Laws)

### 12.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative option statutes (California, New York, Massachusetts) regulate online subscription billing and automatic renewals.

These laws mandate clear disclosure of terms, informed consent prior to charging, and a simple, mechanism-equivalent cancellation path (cancellation must be as easy as sign-up, with no requirement to call, mail, or chat with support if sign-up occurred online).

Official Citation: 15 U.S.C. 8401 et seq. (ROSCA); California Business and Professions Code Sec. 17600.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Subscription Cancellation & Negative Option Policy enforcing simple, frictionless cancellation paths.
- **Missing Documentation:**
  Missing design guidelines specifying that web and companion account cancellation paths must be as easy as sign-up.
- **Missing Code:**
  Lacks self-service subscription cancellation UI components and backend cancellation webhooks for non-storefront billing funnels.
- **Missing Disclosure:**
  Subscription sign-up screens omit clear disclosures of recurring billing terms, cancellation steps, and billing schedules.
- **Missing Logging:**
  Missing logging schemas capturing cancellation initiation timestamps, confirmation receipts, and post-cancellation status.
- **Missing Testing:**
  Lacks end-to-end automated UI tests verifying that web/account-settings subscription cancellation completes without human intervention.
- **Missing Evidence:**
  Lacks cancellation confirmation receipt templates, refund processing logs, or state negative-option compliance checklists.
- **Missing Audit Trail:**
  An unalterable audit log recording subscription signup-to-cancellation ratios, flow modifications, and customer complaints is missing.

### 12.3 Remediation and Action Plan
1. Adopt a Subscription Cancellation Policy requiring mechanism-equivalent, self-service cancellation.
2. Build account settings UI components providing one-click cancellation for web-billed subscriptions.
3. Establish backend logging to record cancellation timestamps and send instant email receipts.
4. Implement automated UI tests verifying frictionless cancellation flows.

---

## 13. UK Online Safety Act 2023 and ICO Children's Code

### 13.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the Information Commissioner's Office (ICO) Age Appropriate Design Code (Children's Code) establish strict safety and privacy rules for online services accessed by UK users under 18.

Requirements include Highly Effective Age Assurance (facial age estimation, open banking, digital ID), high privacy settings by default, geolocation OFF by default, profiling OFF by default, Data Protection Impact Assessments (DPIAs), and CSEA reporting to the NCA portal.

Official Citations: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Online Safety & Age-Appropriate Design Policy covering age assurance, high privacy defaults, and child safety.
- **Missing Documentation:**
  Missing operational guides for implementing facial age estimation, open banking checks, DPIAs, and CSEA reporting to the NCA portal.
- **Missing Code:**
  Lacks code modules for age assurance integration, default high-privacy settings (geo off, profiling off), and CSEA hash matching.
- **Missing Disclosure:**
  Onboarding flows omit UK Children's Code disclosures explaining data minimisation, profiling defaults, and safety measures.
- **Missing Logging:**
  Missing logging schemas for age assurance checks, CSEA incident detections, and user safety complaint handling.
- **Missing Testing:**
  Lacks automated tests verifying that UK child accounts default to geolocation OFF, profiling OFF, and strict privacy settings.
- **Missing Evidence:**
  Lacks written Data Protection Impact Assessments (DPIAs) for children, Ofcom risk assessment records, or CSEA reporting logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking age-assurance verification outcomes, safety risk assessment updates, and CSEA reports is missing.

### 13.3 Remediation and Action Plan
1. Publish a UK Online Safety Policy incorporating ICO Children's Code standards.
2. Draft a Children's DPIA template and Ofcom Risk Assessment guide.
3. Configure default user privacy settings to disable geolocation and profiling for accounts under 18.
4. Set up CSEA reporting procedures and logging mechanisms for safety events.

---

## 14. Australia Online Safety Framework and Social Media Minimum Age Act 2024

### 14.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 and eSafety Industry Codes restrict access to social media platforms for children under 16, and mandate age assurance and access controls across app distribution services.

Platforms must take reasonable steps (waterfall age assurance methods) to prevent under-16s from holding accounts, ringfence age verification data, and delete age data immediately after verification.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Online Safety Policy covering the under-16 social media ban, waterfall age assurance, and eSafety industry codes.
- **Missing Documentation:**
  Missing developer runbooks for App Distribution Services Code compliance, head terms risk assessments, and age rating adjustments.
- **Missing Code:**
  Lacks code logic enforcing waterfall age verification (facial estimation, digital ID) and automatic account blocking for under-16s.
- **Missing Disclosure:**
  Onboarding screens omit explicit disclosures regarding mandatory age assurance under the Social Media Minimum Age Act 2024.
- **Missing Logging:**
  Missing logging mechanisms for age verification requests, account restriction events, and immediate age data destruction logs.
- **Missing Testing:**
  Lacks automated integration tests verifying that under-16 users in Australia are blocked from creating social accounts.
- **Missing Evidence:**
  Lacks documented waterfall age-assurance test results, eSafety initial risk assessment records, or data ringfencing proofs.
- **Missing Audit Trail:**
  An unalterable audit log recording age verification data destruction, restriction enforcement, and policy reviews is missing.

### 14.3 Remediation and Action Plan
1. Formulate an Australian Online Safety Policy detailing waterfall age assurance and data destruction rules.
2. Build integration handlers for age assurance APIs and automatic account gating for under-16 users in Australia.
3. Implement database procedures to purge raw age verification data immediately after processing.
4. Establish CI tests validating age-gating triggers for Australian storefront builds.

---

## 15. Brazil Digital ECA (Law 15,211/2025 and Decreto 12,880) and LGPD

### 15.1 Regulatory Overview and Background
Brazil's Law 15,211/2025 (Digital ECA), regulated by Decreto 12,880 and enforced by the ANPD alongside the LGPD, establishes strict child protection and age verification requirements for digital applications.

Accepted age verification methods include document verification, facial age estimation, facial matching, and CPF database checks (self-declaration checkboxes are prohibited). App stores and developers must block gambling/loot-box access for minors and obtain verifiable guardian consent.

Official Citations: Law 15,211/2025; Decreto n. 12.880 of 18 March 2026; Law 13,709/2018 (LGPD).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA & Child Protection Policy mandating approved age verification methods and parental authorization.
- **Missing Documentation:**
  Missing developer guides for integrating ANPD-approved age assurance (CPF check, facial matching) and Play Age Signals API in Brazil.
- **Missing Code:**
  Lacks code hooks for CPF database verification, guardian consent sheets, and 18-plus download/gambling restrictions.
- **Missing Disclosure:**
  In-app onboarding displays omit mandatory notices regarding Digital ECA age verification, guardian rights, and LGPD processing.
- **Missing Logging:**
  Missing database logging for age signal queries, guardian consent grants, and contestation request logs.
- **Missing Testing:**
  Lacks automated unit tests verifying that unverified users in Brazil cannot access loot-box features or 18-plus app content.
- **Missing Evidence:**
  Lacks ANPD age-assurance parameter compliance reports, CADE alternative distribution agreements, or guardian consent proofs.
- **Missing Audit Trail:**
  An unalterable audit log recording age verification attempts, contestation resolutions, and LGPD compliance audits is missing.

### 15.3 Remediation and Action Plan
1. Draft a Brazil Digital ECA Policy outlining approved age verification channels and LGPD consent rules.
2. Integrate Play Age Signals API and CPF validation logic into Brazilian onboarding flows.
3. Build logging routines for guardian consent grants and age verification contestations.
4. Add automated integration tests verifying that unverified Brazilian users are gated from 18-plus content.

---

## 16. India Digital Personal Data Protection Act (DPDPA 2023 and DPDP Rules 2025)

### 16.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act 2023 (DPDPA) and DPDP Rules 2025 regulate the processing of digital personal data.

Rules 3, 5-16, 22, and 23 (effective 13 May 2027) mandate verifiable parental consent for processing data of individuals under 18, prohibit behavioral tracking and targeted advertising to children, and require integration with registered Consent Managers. Synthetic content labeling requires 2-hour/3-hour takedown windows under IT Rules.

Official Citations: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025 (G.S.R. 846(E)).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Compliance Policy covering verifiable parental consent, Consent Managers, and child data restrictions.
- **Missing Documentation:**
  Missing developer implementation guides for DigiLocker parental consent, Consent Manager APIs, and synthetic content labeling.
- **Missing Code:**
  Lacks integration code for DigiLocker parental verification, Consent Manager interaction, and 2-hour/3-hour synthetic content takedowns.
- **Missing Disclosure:**
  Onboarding and consent screens omit multilingual DPDPA notices detailing processing purposes, Consent Manager rights, and DPO details.
- **Missing Logging:**
  Missing database schemas for logging consent withdrawal events, Consent Manager tokens, and synthetic content takedown actions.
- **Missing Testing:**
  Lacks automated tests verifying that under-18 users in India are blocked from targeted ads and behavioral tracking.
- **Missing Evidence:**
  Lacks Data Protection Officer (DPO) appointment records, Consent Manager integration certificates, or verifiable parental consent logs.
- **Missing Audit Trail:**
  An unalterable audit log recording consent notices, parental verifications, and synthetic content takedown requests is missing.

### 16.3 Remediation and Action Plan
1. Establish an India DPDPA Policy detailing verifiable parental consent and Consent Manager requirements.
2. Build code modules for DigiLocker parental verification and Consent Manager API interaction.
3. Implement multilingual consent notice UI components conforming to DPDP Rule 3.
4. Set up logging schemas to record consent tokens and takedown executions.

---

## 17. Singapore Personal Data Protection Act (PDPA) and IMDA Code of Practice

### 17.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services require robust data protection and age assurance controls.

From 1 April 2026, app stores and developers must implement age assurance (credit card or digital ID verification) to screen and stop users under 18 from downloading age-inappropriate content. Data retention is strictly limited to the verification purpose.

Official Citations: Personal Data Protection Act 2012 (No. 26 of 2012); IMDA Code of Practice for Online Safety.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA & IMDA Online Safety Policy covering credit card / digital ID age assurance and DPO accountability.
- **Missing Documentation:**
  Missing developer guides for IMDA App Distribution Services Code compliance, age screening, and 3-day breach notification.
- **Missing Code:**
  Lacks code modules for credit card / digital ID age verification, under-18 download screening, and immediate age data purge logic.
- **Missing Disclosure:**
  App listings and onboarding screens omit PDPA consent disclosures, DPO contact info, and IMDA age restriction notices.
- **Missing Logging:**
  Missing logging schemas for age screening queries, data breach detection/notification events, and DPO contact logs.
- **Missing Testing:**
  Lacks automated tests verifying that under-18 users in Singapore are blocked from accessing 18-plus rated app features.
- **Missing Evidence:**
  Lacks Data Protection Officer (DPO) registration proof, IMDA age assurance compliance records, or age data deletion proofs.
- **Missing Audit Trail:**
  An unalterable audit log recording age screening events, data breach incident logs, and annual PDPA compliance audits is missing.

### 17.3 Remediation and Action Plan
1. Draft a Singapore PDPA Policy covering age assurance and 3-day breach notification timelines.
2. Integrate age screening logic and immediate data purge routines for Singapore user sessions.
3. Document DPO appointment details and IMDA compliance procedures.
4. Implement CI tests verifying age-gating for Singapore app builds.

---

## 18. South Korea Telecommunications Business Act and PIPA Amendment

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment choices for mobile applications, while the Personal Information Protection Act (PIPA Amendment, Act No. 21445, effective 11 September 2026) establishes strict CPO board accountability and penalties up to 10% of turnover.

External payments on iOS require entitlement `com.apple.developer.storekit.external-purchase` (`SKExternalPurchase = "KR"`), approved payment providers (KCP, Inicis, Toss, NICE), a 26% commission, a native disclosure modal sheet, and 15-day monthly sales reporting. GRAC rating certificates (RCN) govern age ratings.

Official Citations: Telecommunications Business Act Article 22-9; Personal Information Protection Act (Act No. 21445).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Compliance Policy covering alternative in-app billing, GRAC age ratings, and executive PIPA accountability.
- **Missing Documentation:**
  Missing developer runbooks for Korean external purchase entitlement (`SKExternalPurchase = "KR"`), 26% fee reporting, and GRAC certificates.
- **Missing Code:**
  Lacks native external payment modal sheets, approved Korean payment gateway wrappers (Toss, KCP), and 12+ descriptor overrides.
- **Missing Disclosure:**
  Payment selection UI lacks required Korean disclosure modals stating transaction terms, vendor identity, and Apple/Google non-involvement.
- **Missing Logging:**
  Missing logging mechanisms for Korean external payment transactions, monthly fee reporting calculations, and CPO oversight logs.
- **Missing Testing:**
  Lacks automated unit tests verifying that Korean binaries do not co-mingle StoreKit IAP and external billing on the same screen.
- **Missing Evidence:**
  Lacks GRAC rating certificate records, monthly external purchase sales reports, or Chief Privacy Officer (CPO) board approval proofs.
- **Missing Audit Trail:**
  An unalterable audit log recording external payment transactions, monthly fee submissions to Apple/Google, and CPO audits is missing.

### 18.3 Remediation and Action Plan
1. Formulate a South Korea Compliance Policy covering alternative payments, GRAC ratings, and CPO duties.
2. Build native Korean external purchase disclosure sheets and gateway integration wrappers.
3. Establish automated logging for monthly 26% commission calculation and reporting.
4. Implement CI checks verifying that Korean builds contain required GRAC certificates and non-commingled payment UI.

---

## 19. China Mobile App Filing (MIIT, CAC, and PIPL)

### 19.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) for all apps distributed in China. CAC Interim Measures for AI Anthropomorphic Interactive Services (effective 15 July 2026) regulate AI chat/companion apps, while the Personal Information Protection Law (PIPL) governs privacy.

Foreign developers must partner with a local Chinese entity to complete MIIT filing. AI apps must verify real-name identity, automatically switch minors into minors mode, obtain guardian consent for under-14s, and ban virtual companion services for minors. Games require a Banhao license.

Official Citations: MIIT Notice on Mobile Application Filing (2023); CAC Order No. 21 (2026); Personal Information Protection Law (PIPL 2021).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China Distribution & Data Compliance Policy covering MIIT App Filing, real-name verification, and minors mode.
- **Missing Documentation:**
  Missing developer guides for local entity partnership, MIIT ICP filing, CAC AI anthropomorphic service measures, and Banhao licensing.
- **Missing Code:**
  Lacks code modules for real-name ID verification, automatic minors mode switching, and algorithmic recommendation disabling.
- **Missing Disclosure:**
  App splash screens omit MIIT app filing numbers, PIPL privacy notices, and CAC minor mode activation prompts.
- **Missing Logging:**
  Missing logging schemas for real-name verification logs, minor mode transitions, and PIPL cross-border transfer logs.
- **Missing Testing:**
  Lacks automated tests verifying that minor users in China are automatically placed in minors mode without virtual companion access.
- **Missing Evidence:**
  Lacks MIIT App Filing certificates, Banhao game licenses, local entity partnership contracts, or PIPL personal info audit reports.
- **Missing Audit Trail:**
  An unalterable audit log recording MIIT filing updates, minor mode usage records, and biannual PIPL compliance audits is missing.

### 19.3 Remediation and Action Plan
1. Draft a China Distribution Policy covering MIIT filing, PIPL compliance, and CAC AI rules.
2. Build code modules for real-name verification and automatic minors mode switching.
3. Display MIIT ICP filing numbers on app splash screens and settings UI.
4. Maintain local entity partnership records and PIPL compliance audit reports in evidence files.

---

## 20. EU Data Act, Cyber Resilience Act (CRA), and Product Liability Directive (PLD)

### 20.1 Regulatory Overview and Background
The EU Data Act (Regulation (EU) 2023/2854), Cyber Resilience Act (Regulation (EU) 2024/2847), and Product Liability Directive (Directive (EU) 2024/2853) reshape software product safety, cybersecurity, and data access.

The Data Act requires access-by-design for connected products (from 12 September 2026). The Cyber Resilience Act mandates vulnerability reporting and security-by-design (from September 2026 / December 2027). The Product Liability Directive treats standalone software and app updates as products under strict liability (from 9 December 2026).

Official Citations: Regulation (EU) 2023/2854; Regulation (EU) 2024/2847; Directive (EU) 2024/2853.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Data Act & Software Product Liability Policy covering access-by-design, vulnerability handling, and strict software liability.
- **Missing Documentation:**
  Missing developer guidelines for IoT data access interfaces, CRA vulnerability disclosure protocols, and software defect tracking.
- **Missing Code:**
  Lacks standardized API endpoints for user data porting under the Data Act and security patch auto-updater mechanisms under CRA.
- **Missing Disclosure:**
  Product listings omit disclosures regarding data generated by connected products, security update lifecycles, and defect reporting paths.
- **Missing Logging:**
  Missing system logging schemas for connected device data streams, software vulnerability reports, and security patch deployments.
- **Missing Testing:**
  Lacks automated integration tests verifying user data export capabilities and security patch integrity checks prior to release.
- **Missing Evidence:**
  Lacks Technical Documentation files under CRA, vulnerability handling procedures, or software product liability risk assessments.
- **Missing Audit Trail:**
  An unalterable audit log tracking software release versions, vulnerability disclosures, patch histories, and defect remediations is missing.

### 20.3 Remediation and Action Plan
1. Adopt an EU Data Act, CRA, and Software Product Liability Policy.
2. Establish vulnerability disclosure protocols and security patch lifecycle documentation.
3. Build API endpoints enabling user access and portability for connected device data.
4. Implement CI security patch verification tests and maintain unalterable vulnerability remediation audit logs.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4/50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. European Accessibility Act**| Partial | Covered | Missing | Partial | Missing | Partial | Missing | Missing |
| **9. US COPPA & Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. California Privacy** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. UK Online Safety & Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China Mobile App Filing**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. EU Data Act / CRA / PLD**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Nineteenth of the twenty frameworks are named across `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`, with dated sources and deadline entries. What they lack is the implementation layer, meaning detection rules in the guard, code templates, testing scripts, and evidence templates. GPSR is the only framework absent end to end, making it the first priority for addition.

---

## 22. Conclusion and Future Monitoring

The playbook provides exceptional coverage of app store rejection rules and high-level regulatory awareness across global jurisdictions. However, across all twenty major regulatory frameworks, the repository's primary gap resides in the operational implementation layer: code templates, automated test suites, backend logging schemas, evidence artifacts, and unalterable audit trails.

In priority order:

1. Add GPSR, the only framework absent end-to-end.
2. Expand detection rules in `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh` for all Partial frameworks.
3. Provide code templates for AI Act Article 50 disclosures, EU contract withdrawal, and state ASAA age signals.
4. Develop automated test runner scripts and evidence templates for BIPA, COPPA, EAA, and international age assurance frameworks.

This report is a snapshot. Re-run it against EUR-Lex, Federal Register, and official government publications to track regulatory developments.

---

## 23. Sources

Every regulation named above, at its primary official source.

- GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California CCPA/CPRA: [California Civil Code 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)
- Illinois BIPA: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US ROSCA: [15 U.S.C. 8401](https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap110.htm)
- UK Online Safety Act: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Social Media Minimum Age Act: [Act No. 131 of 2024](https://www.legislation.gov.au/C2024A00131/asmade/text)
- Brazil Digital ECA: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA: [Act No. 22 of 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA: [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea PIPA: [Act No. 21445](https://law.go.kr/LSW/lsRvsRsnListP.do?chrClsCd=010102&lsId=011357)
- China Mobile App Filing: [MIIT Notice 2023](https://www.miit.gov.cn/)
- EU Data Act: [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)
