# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile and web application developers shipping globally (across the European Union, United States, United Kingdom, Australia, Brazil, Canada, South Korea, India, Singapore, Japan, and China) and evaluates how far this repository carries each framework, what it mentions in passing, and what it lacks entirely.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight distinct compliance categories: missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital platforms and software applications, the GPSR mandates that online interfaces clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no written policy template or decision framework to determine whether their listing falls inside Regulation (EU) 2023/988 or how to designate an EU-based Responsible Person.
- **Missing Documentation:**
  The repository lacks developer guides, manuals, and step-by-step checklists explaining how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR elements. Additionally, mock user interfaces and templates do not contain code blocks for displaying manufacturer identity or product safety warnings.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name, postal address, and electronic address (email or website) as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, user complaints, recalls, or corrective actions.
- **Missing Testing:**
  No automated unit or integration tests exist to verify that online interface elements dynamically display required product safety information, manufacturer details, or warning notices based on user locale.
- **Missing Evidence:**
  The repository lacks physical templates or examples of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no audit trail system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented in response to a safety alert.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining Responsible Person designation and product classification criteria.
2. Incorporate GPSR metadata requirements into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory demonstrating compliant product detail pages including safety warning labels and contact details.
4. Integrate an automated test script verifying safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. Mandatory enforcement begins on 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window to produce user data is 10 days, but in emergency cases, providers must produce data within a strict 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, leaving teams receiving an EU judicial order without operational protocols or legal representative appointment frameworks.
- **Missing Documentation:**
  The repository lacks operational runbooks, manuals, or detailed instructions for executing 10-day standard orders and 8-hour emergency production orders.
- **Missing Code:**
  There are no backend scripts or secure API endpoints in mock implementations to extract, package, filter, and encrypt user data in response to a legal order.
- **Missing Disclosure:**
  Public-facing Privacy Policies fail to explicitly disclose to EU users that user data may be preserved or produced to European law enforcement pursuant to Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository lacks database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, data access, or data releases.
- **Missing Testing:**
  There are no integration tests or simulation scripts to validate rapid 8-hour emergency data retrieval and secure packaging under simulated pressure.
- **Missing Evidence:**
  The repository lacks verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for compliance verification.
- **Missing Audit Trail:**
  A tamper-proof, cryptographic audit trail system recording administrative interactions, data extractions, and transmissions made during legal compliance is absent.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol establishing roles, responsibilities, and secure communication channels.
2. Formally designate an EU legal representative and notify the designated central authority before 18 August 2026.
3. Build backend scripts to automate extraction and encryption of requested datasets within the 8-hour emergency window.
4. Implement a tamper-proof cryptographic audit trail to log all incoming certificates, checks, and transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or function on the online interface for distance contracts concluded electronically. Member States apply these rules from 19 June 2026.

The withdrawal period is 14 days from contract conclusion. The cancellation path must be direct, clear, and at least as simple as the sign-up path.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day right of withdrawal or guidance separating mandatory financial services scope from design defaults.
- **Missing Documentation:**
  The repository lacks UI design guidelines and checklists specifying placement, prominence, and terminology required for a compliant withdrawal button.
- **Missing Code:**
  Front-end user interface templates and billing mocks do not contain functional implementations of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces fail to prominently disclose the 14-day statutory right of withdrawal or link to withdrawal terms.
- **Missing Logging:**
  There are no logging mechanisms capturing when a user triggers the withdrawal button, timestamps, contract termination confirmations, or refund flow initiations.
- **Missing Testing:**
  No automated UI or unit tests exist to verify that the withdrawal flow can be completed without administrative friction or mandatory customer support interaction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized records to defend consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, subscription flow audits, and withdrawal interface updates is missing.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent Withdrawal Button component within account settings in subscription templates.
3. Establish database schemas for logging cancellation requests, timestamps, and refund transactions.
4. Implement end-to-end UI tests ensuring frictionless self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minor access to mobile applications, purchases, and major updates.

Developers must request user age categories (via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a minor age assurance policy detailing how to identify users in regulated states and process minor accounts.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API in multi-platform codebases.
- **Missing Code:**
  Mock client implementations do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict feature access dynamically.
- **Missing Disclosure:**
  In-app onboarding flows fail to display state disclosures explaining that age categories are requested to comply with state accountability laws and that parental consent is mandatory.
- **Missing Logging:**
  There is no backend logging system designed to record parental consent receipt, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw verification documents.
- **Missing Testing:**
  Test suites lack automated integration tests verifying that minor accounts are blocked from premium features or purchases without valid consent signals.
- **Missing Evidence:**
  The repository lacks templates for parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:**
  An immutable audit trail recording historical rollout of age-assurance features, consent policy updates, and immediate data deletion records is absent.

### 4.3 Remediation and Action Plan
1. Create a Minor Age Assurance Policy specifying state-level identification and strict data minimization rules.
2. Implement native cross-platform hooks querying Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers to purge raw age-verification data immediately after age confirmation.
4. Establish automated tests verifying in-app billing is disabled for minor accounts until valid parental consent signals are processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among staff and personnel operating AI systems, applicable since 2 February 2025.

This obligation applies to all organizations regardless of headcount. Pragmatic compliance requires a written policy, team induction records, a refresh schedule, and a completion log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template AI Literacy Policy defining sufficient competency standards under Article 4.
- **Missing Documentation:**
  The repository lacks developer documentation explaining obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  The codebase lacks CLI helper scripts to check whether the team literacy log exists, contains required entries, and is up to date.
- **Missing Disclosure:**
  Public documentation and partner contracts fail to disclose organizational adherence to AI literacy standards under Article 4.
- **Missing Logging:**
  The repository lacks a centralized training log or registry tracking employee inductions, course completions, and literacy refreshers.
- **Missing Testing:**
  There are no automated pre-commit checks or CI pipeline tools verifying that team members committing AI code hold active literacy records.
- **Missing Evidence:**
  The playbook lacks examples of valid compliance evidence, such as completed training logs, course certificates, or written risk assessments.
- **Missing Audit Trail:**
  There is no historical audit trail documenting annual policy reviews, training module updates, or literacy log evolution over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining core competency areas (AI safety, risk assessment, data privacy, bias).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review literacy records annually.
4. Set up an automated CI check warning if the literacy log has not been updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act establishes strict transparency obligations taking effect on 2 August 2026.

Providers must ensure AI systems interacting directly with natural persons inform users they are interacting with AI (Article 50(1)). Outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated (Article 50(2)). Deployers of deepfakes must disclose artificial generation or manipulation (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an AI Transparency Policy defining when disclosures must appear and how generated media must be marked.
- **Missing Documentation:**
  Checklists mention Article 50 but lack detailed developer instructions on implementing machine-readable watermarking (such as C2PA) or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes or middleware to inject machine-readable watermarks into generated media assets.
- **Missing Disclosure:**
  Chat and media generation UI templates fail to display immediate disclosures ("You are interacting with an AI system") at first user exposure.
- **Missing Logging:**
  There are no database logging schemas tracking whether AI transparency warnings were displayed during user sessions.
- **Missing Testing:**
  Test runner scripts do not check for synthetic media markers or verify that outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository lacks compliance evidence such as independent safety assessment reports or metadata retention proofs.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and disclosure modifications is absent.

### 6.3 Remediation and Action Plan
1. Formulate an AI Transparency and Disclosure Policy mandating direct disclosure and output marking.
2. Incorporate explicit notices ("You are chatting with an AI assistant") in conversational interface templates.
3. Implement standard metadata injection (using C2PA specifications or cryptographic watermarks) in generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify machine-readable compliance headers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeepers to ensure contestable and fair markets. For mobile developers, Apple's EU compliance model enables alternative app marketplaces, web distribution, external purchase links (`com.apple.developer.storekit.external-purchase-link`), and custom fee structures.

Developers utilizing external purchase promotion must display system disclosure sheets (`ExternalPurchaseCustomLink`) and report monthly transactions via the External Purchase Server API within 15 days of fiscal month end.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Alternative Distribution and Payment Steering Policy guiding EU entitlement selection and fee compliance.
- **Missing Documentation:**
  Documentation lacks step-by-step technical guides for configuring `com.apple.developer.storekit.external-purchase-link` and setting up automated monthly sales reporting.
- **Missing Code:**
  Codebase samples lack integration with `ExternalPurchaseCustomLink` disclosure sheets or automated scripts for External Purchase Server API reporting.
- **Missing Disclosure:**
  In-app offer flows fail to present mandatory pre-redirect system disclosure sheets informing users that purchases occur outside Apple's ecosystem.
- **Missing Logging:**
  There are no backend logging mechanisms recording external offer click-throughs or generating monthly reporting payloads.
- **Missing Testing:**
  Test suites lack end-to-end tests validating storefront region-gating (EU vs. non-EU) and entitlement declarations.
- **Missing Evidence:**
  The repository lacks templates for Signed StoreKit External Purchase Link Entitlement Addendums or CTC fee calculation sheets.
- **Missing Audit Trail:**
  An audit trail system tracking monthly external sales reports submitted to Apple and corresponding fee calculations is absent.

### 7.3 Remediation and Action Plan
1. Draft an EU Alternative Distribution Policy outlining entitlement usage and reporting duties.
2. Build native hooks calling `ExternalPurchaseCustomLink` before executing external link navigation.
3. Implement automated backend scripts to aggregate external sales and generate monthly External Purchase Server API reports.
4. Add automated CI checks verifying entitlement declarations match targeting rules.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
Articles 30 and 31 of the EU Digital Services Act (Regulation (EU) 2022/2065) mandate that app stores verify and display trader contact and identity details for all entity and individual developers distributing apps in the EU.

Enforced strictly by Apple since 17 February 2025, non-compliant developers face app removal from EU storefronts. Traders must provide verified D-U-N-S numbers, addresses, phone numbers, and emails validated via 2FA. Non-trader declarations inform EU consumers that consumer protection rights do not apply.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Trader Status Compliance Policy guiding organizations on determining trader status under EU law.
- **Missing Documentation:**
  Checklists lack step-by-step instructions for completing App Store Connect DSA trader verification (D-U-N-S, phone, 2FA) and non-trader declarations.
- **Missing Code:**
  Release audit scripts (`scripts/release-audit.py`) do not statically verify whether DSA trader status metadata fields are configured.
- **Missing Disclosure:**
  Public-facing product metadata templates do not include structured fields for trader address, phone number, and email.
- **Missing Logging:**
  There are no internal logs recording DSA trader status submission dates, 2FA verification timestamps, or status changes.
- **Missing Testing:**
  No pre-submission test script checks whether the developer's DSA trader status is active and verified prior to EU app release.
- **Missing Evidence:**
  The repository lacks templates for organizing verified D-U-N-S certificates, 2FA receipts, or corporate registration proofs.
- **Missing Audit Trail:**
  An audit log capturing historical modifications to trader status declarations and App Store Connect compliance records is missing.

### 8.3 Remediation and Action Plan
1. Formulate a DSA Trader Compliance Policy providing clear criteria for trader vs. non-trader declarations.
2. Expand `scripts/metadata-audit.py` to check for required DSA trader disclosures in metadata files.
3. Incorporate DSA trader status verification checks into `scripts/release-audit.py`.
4. Maintain a secure repository folder for storing official DSA compliance verification evidence.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025. It mandates accessibility for consumer products and services, including e-commerce, banking, e-books, and mobile applications reaching EU users.

Technical compliance requires meeting harmonised standard EN 301 549 (version 3.2.1), built on WCAG 2.1 Level AA, with specific non-web software and mobile requirements detailed in Chapter 11. Apps must also publish a formal Accessibility Statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Organizational Accessibility Policy committing app development to EN 301 549 Chapter 11 standards.
- **Missing Documentation:**
  Documentation mentions WCAG 2.1 AA generally but lacks detailed developer guides explaining EN 301 549 Chapter 11 mobile rules (Dynamic Type, VoiceOver traits, contrast).
- **Missing Code:**
  Static scanners in `scripts/accessibility-audit.py` cover basic iOS/Android checks but lack rules validating EN 301 549 specific criteria.
- **Missing Disclosure:**
  Templates do not include an in-app or web Accessibility Statement conforming to EN 301 549 Annex B/C requirements.
- **Missing Logging:**
  There are no issue tracking schemas or logging workflows for recording user-reported accessibility barrier reports.
- **Missing Testing:**
  Test suites lack automated UI accessibility audits verifying Dynamic Type scaling without layout truncation, VoiceOver trait correctness, and 4.5:1 contrast ratios.
- **Missing Evidence:**
  The repository lacks formal EN 301 549 / WCAG 2.1 AA audit reports, expert evaluation results, or conformance declarations.
- **Missing Audit Trail:**
  An audit trail tracking historical accessibility audits, remediation tickets, and accessibility statement revisions is missing.

### 9.3 Remediation and Action Plan
1. Establish a written Accessibility Policy aligning development with EN 301 549 Chapter 11 and WCAG 2.1 AA.
2. Publish an Accessibility Statement template (`docs/ACCESSIBILITY-STATEMENT-TEMPLATE.md`) conforming to EAA requirements.
3. Enhance `scripts/accessibility-audit.py` to enforce EN 301 549 rules across mobile layout codebases.
4. Integrate automated UI accessibility tests into CI pipelines to prevent layout truncation and contrast regressions.

---

## 10. US Children's Online Privacy Protection Act (Amended COPPA Rule)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, governs services directed to children under 13 or general-audience services with actual knowledge of child users. The FTC's amended COPPA Rule (effective 23 June 2025, mandatory compliance 22 April 2026) expands personal information to include biometric identifiers and government IDs.

Key duties include separate opt-in consent for third-party disclosures, written data retention policies (312.10), written information security programs (312.8), and verifiable parental consent methods (face-match to ID, knowledge-based authentication).

Official Citation: 16 CFR Part 312 (FTC Amended COPPA Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written COPPA Children's Data Retention Policy and a formal Information Security Program.
- **Missing Documentation:**
  Checklists lack developer instructions for implementing separate opt-in parental consent for third-party ad networks and managing biometric PII.
- **Missing Code:**
  Mock implementations lack native age-gating, verifiable parental consent integrations (face-match/KBA), or biometric data filters.
- **Missing Disclosure:**
  In-app onboarding flows fail to display compliant direct parental notices and privacy policy notices at collection prior to child data capture.
- **Missing Logging:**
  Backend schemas do not support logging verifiable parental consent grants, consent revocations, or automated deletion triggers under Section 312.10.
- **Missing Testing:**
  Test suites lack automated tests verifying that third-party tracking SDKs are completely blocked for under-13 users until opt-in parental consent is confirmed.
- **Missing Evidence:**
  The repository lacks templates for annual Information Security risk assessments or verifiable parental consent logs.
- **Missing Audit Trail:**
  An immutable audit trail recording data retention schedule enforcement, consent revocations, and data deletion executions is missing.

### 10.3 Remediation and Action Plan
1. Draft a written Children's Data Retention Policy and Information Security Program conforming to 16 CFR 312.8 and 312.10.
2. Implement native age-gating and verifiable parental consent modal components.
3. Configure backend logic to disable third-party ad SDKs dynamically for child accounts.
4. Establish automated tests verifying zero third-party data transmission for under-13 users without explicit parental consent.

---

## 11. California Privacy Rights Act (CPRA / CCPA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), and the CPPA 2026 regulations (effective 1 January 2026) govern businesses processing California residents' personal data.

Duties include privacy notices at collection, rights to know, delete, correct, and opt-out of sale/sharing/profiling, honoring Global Privacy Control (GPC) signals (`Sec-GPC`), limiting sensitive personal information usage, and automated decision-making technology (ADMT) opt-outs (phasing in 2027).

Official Citation: California Civil Code Section 1798.100 et seq. and CPPA Regulations.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a California-specific Consumer Privacy Policy and Sensitive Personal Information Handling Policy.
- **Missing Documentation:**
  Documentation lacks developer guides on detecting and honoring Global Privacy Control (GPC) headers in webviews and implementing native opt-out equivalents.
- **Missing Code:**
  Embedded webviews and native network modules lack code logic to parse `Sec-GPC` headers or halt data sharing/analytics endpoints automatically.
- **Missing Disclosure:**
  UI templates lack explicit "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:**
  There are no database logging schemas tracking consumer opt-out requests, GPC signal detection events, or rights fulfillment timestamps.
- **Missing Testing:**
  Test suites lack automated integration tests verifying that analytics and targeted ad tracking halt when a GPC signal or opt-out request is detected.
- **Missing Evidence:**
  The repository lacks templates for annual cybersecurity audit reports or consumer rights request fulfillment logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking CPRA opt-out requests, data deletion executions, and policy updates is absent.

### 11.3 Remediation and Action Plan
1. Create a California Consumer Privacy Policy template and GPC implementation guide.
2. Implement `Sec-GPC` header parsing in webview controllers and native opt-out hooks in analytics handlers.
3. Add "Do Not Sell or Share My Personal Info" UI components to settings templates.
4. Build automated integration tests asserting that data transmission to third parties drops to zero upon receiving opt-out signals.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, capture, purchase, receive, through trade, or obtain of biometric identifiers (fingerprints, retina/iris scans, voiceprints, facial geometry).

BIPA requires written notice, written releases prior to collection, a publicly available retention schedule and destruction guideline, destruction within 3 years of last interaction, and a strict ban on selling biometric data.

Official Citation: 740 ILCS 14 (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Biometric Information Privacy Policy and public retention schedule template.
- **Missing Documentation:**
  Checklists lack developer instructions for obtaining e-signed written releases before invoking native biometric capture APIs (FaceID/TouchID/biometric SDKs).
- **Missing Code:**
  Client templates lack biometric consent modal sheets and automated backend scripts to destroy biometric data after 3 years.
- **Missing Disclosure:**
  UI flows fail to present clear written notices disclosing that biometric identifiers are collected, stored, and used, including the specific purpose and term.
- **Missing Logging:**
  There are no secure logging schemas capturing executed written releases, consent timestamps, or 3-year data destruction executions.
- **Missing Testing:**
  Test runner scripts do not check whether biometric capture endpoints are blocked unless a signed consent flag is present.
- **Missing Evidence:**
  The repository lacks sample written consent releases or verified proof of automated 3-year biometric data destruction.
- **Missing Audit Trail:**
  An unalterable audit trail recording biometric consent capture, storage duration, and automated deletion is missing.

### 12.3 Remediation and Action Plan
1. Publish a Biometric Data Retention and Destruction Policy template conforming to 740 ILCS 14/15.
2. Develop a native written consent modal component required prior to invoking biometric SDKs.
3. Build automated database purging jobs executing biometric data destruction at the 3-year mark.
4. Add automated tests asserting that biometric APIs cannot be invoked without a verified written consent record.

---

## 13. US Subscription Cancellation and Click-to-Cancel Rules

### 13.1 Regulatory Overview and Background
While the FTC's federal Negative Option Rule amendment was vacated by the Eighth Circuit on 8 July 2025, underlying statutory obligations remain enforced under FTC Act Section 5, ROSCA, and state negative option statutes (California, New York, Massachusetts).

Cancellation mechanisms for subscriptions billed outside app store in-app purchase systems (e.g., web signups or cross-platform accounts) must be at least as simple as sign-up, operating via a simple online cancellation path without requiring phone calls, letters, or mandatory retention friction.

Official Citations: 15 U.S.C. 8401 et seq. (ROSCA) and California Business and Professions Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Subscription Auto-Renewal and Cancellation Policy guiding web-billed subscription management.
- **Missing Documentation:**
  Documentation lacks developer guidelines ensuring account settings cancellation paths mirror sign-up simplicity.
- **Missing Code:**
  Web and account UI templates lack self-service 1-click cancellation paths or modal flows for out-of-app subscriptions.
- **Missing Disclosure:**
  Subscription flows fail to prominently disclose auto-renewal terms, recurring billing frequencies, minimum commitments, and cancellation paths prior to consent.
- **Missing Logging:**
  Database schemas lack tables for logging cancellation requests, timestamps, confirmation receipts, and refund triggers.
- **Missing Testing:**
  Test suites lack automated end-to-end tests verifying that online cancellation flows complete successfully without requiring phone calls or support tickets.
- **Missing Evidence:**
  The repository lacks templates for subscription confirmation emails or cancellation receipts.
- **Missing Audit Trail:**
  An audit trail tracking cancellation flow completion rates, user drop-offs, and cancellation interface modifications is missing.

### 13.3 Remediation and Action Plan
1. Draft a Subscription Cancellation Policy requiring online self-service cancellation paths for out-of-app subscriptions.
2. Implement self-service cancellation components in account settings templates.
3. Build database logging schemas tracking cancellation requests and automated confirmation generation.
4. Establish automated UI tests ensuring cancellation completes in no more steps than sign-up.

---

## 14. UK Online Safety Act 2023 and ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom, age assurance from 25 July 2025) and the ICO Age Appropriate Design Code (Children's Code) govern services accessible to UK children under 18.

Requirements include Highly Effective Age Assurance (facial age estimation, open banking, digital ID, credit card checks; self-declaration prohibited), high privacy by default, data minimisation, geolocation off by default, profiling off by default, and a mandatory Data Protection Impact Assessment (DPIA).

Official Citations: UK Online Safety Act 2023 c. 50 and ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Child Safety and Age-Appropriate Design Policy.
- **Missing Documentation:**
  Documentation lacks step-by-step developer guides for conducting ICO-compliant DPIAs and integrating approved UK age assurance mechanisms.
- **Missing Code:**
  Codebases lack integration with UK-approved age assurance providers and logic enforcing high-privacy default settings for UK child profiles.
- **Missing Disclosure:**
  UI templates fail to present child-friendly privacy notices explaining data processing and age assurance methods clearly.
- **Missing Logging:**
  There are no logging schemas capturing DPIA execution, age verification outcomes, or immediate raw verification data deletion events.
- **Missing Testing:**
  Test runner scripts do not check whether geolocation, profiling, and targeted ads are disabled by default for UK child accounts.
- **Missing Evidence:**
  The repository lacks completed ICO Children's Code DPIA report templates or Ofcom risk assessment documents.
- **Missing Audit Trail:**
  An immutable audit trail recording DPIA reviews, age assurance updates, and child safety interventions is absent.

### 14.3 Remediation and Action Plan
1. Draft a UK Age-Appropriate Design Policy and DPIA template (`docs/UK-ICO-DPIA-TEMPLATE.md`).
2. Implement high-privacy default configuration profiles (geolocation off, profiling off, analytics off) for UK minor users.
3. Add backend integration patterns for certified UK age assurance providers with immediate raw data destruction.
4. Establish automated tests verifying high-privacy defaults apply automatically upon detecting a UK minor account.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 (enforceable from 10 December 2025) requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts.

Self-declaration alone is prohibited. Platforms must implement waterfall age-assurance methods, ringfence age-verification data, and destroy verification data immediately after use. Non-compliance carries fines up to 49.5 million AUD.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Under-16 Account Restriction and Age Verification Policy for Australia.
- **Missing Documentation:**
  Documentation lacks developer runbooks for implementing waterfall age assurance and strict age-data ringfencing.
- **Missing Code:**
  Codebases lack native hooks blocking account creation for under-16 Australian users or automated scripts to destroy verification data post-check.
- **Missing Disclosure:**
  Onboarding flows fail to inform Australian users that age verification is mandatory by law and that verification data is destroyed immediately.
- **Missing Logging:**
  There are no secure logs capturing age confirmation decisions while maintaining zero retention of raw verification documents.
- **Missing Testing:**
  Test runner scripts do not verify that account creation is blocked for under-16 Australian accounts when using non-compliant self-declaration.
- **Missing Evidence:**
  The repository lacks eSafety Commissioner compliance filing templates or certified age assurance vendor agreements.
- **Missing Audit Trail:**
  An unalterable audit trail recording age verification execution counts and raw data purge receipts is missing.

### 15.3 Remediation and Action Plan
1. Formulate an Australian Under-16 Age Restriction Policy and data ringfencing protocol.
2. Implement backend integrations with accredited age assurance providers, bypassing self-declaration checkboxes.
3. Build automated database triggers deleting raw verification records immediately post-determination.
4. Establish CI tests verifying under-16 accounts cannot complete onboarding on Australian storefront builds.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, enforceable from 17 March 2026, overseen by ANPD) establishes child and adolescent protection rules on digital platforms.

Self-declaration checkboxes are explicitly prohibited. Platforms must implement accepted age verification methods (document checks, facial age estimation, CPF database validation), enforce strict privacy defaults, and ringfence youth data.

Official Citation: Lei No. 15.211/2025 (Estatuto da Criança e do Adolescente Digital).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Youth Protection and Age Assurance Policy.
- **Missing Documentation:**
  Documentation lacks developer guides for integrating ANPD-approved Brazilian age verification APIs (CPF validation, facial estimation).
- **Missing Code:**
  Client templates lack CPF verification hooks or facial estimation SDK integrations for Brazilian storefront builds.
- **Missing Disclosure:**
  Onboarding UI templates fail to display mandatory notices informing Brazilian users that self-declaration is invalid and age proof is required.
- **Missing Logging:**
  Backend schemas lack tables for logging age verification outcomes and automated raw document purge confirmations.
- **Missing Testing:**
  Test runner scripts do not check whether self-declaration inputs fail age verification on Brazilian storefront builds.
- **Missing Evidence:**
  The repository lacks ANPD compliance audit report templates or age verification provider certificates.
- **Missing Audit Trail:**
  An immutable audit trail tracking age verification events, outcomes, and immediate raw data purges is missing.

### 16.3 Remediation and Action Plan
1. Draft a Brazil Youth Protection Policy conforming to Law 15,211/2025 and ANPD guidance.
2. Implement CPF database check and facial age estimation integration modules in mobile onboarding flows.
3. Configure automated raw verification data purging post-check.
4. Build automated tests asserting self-declaration options are disabled for Brazil storefront builds.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA 2023) and DPDP Rules 2025 (notified 13 November 2025, children's consent rules enforceable from 13 May 2027) regulate personal data processing.

Processing data of individuals under 18 requires verifiable parental consent via government-backed systems (such as DigiLocker). Behavioral tracking and targeted advertising to children are strictly prohibited.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India Under-18 Data Protection and Parental Consent Policy.
- **Missing Documentation:**
  Documentation lacks developer instructions for integrating DigiLocker/government-backed verifiable parental consent systems.
- **Missing Code:**
  Codebases lack DigiLocker API integration modules or automated suppression logic for behavioral ad tracking for Indian minor accounts.
- **Missing Disclosure:**
  UI templates fail to present bilingual (English and scheduled Indian languages) privacy notices and parental consent disclosures.
- **Missing Logging:**
  Backend schemas lack Consent Manager tables tracking parental consent grants, scope, and revocations.
- **Missing Testing:**
  Test runner scripts do not check whether targeted ad SDKs and analytics tracking are disabled for under-18 Indian accounts.
- **Missing Evidence:**
  The repository lacks Consent Manager registration templates or DigiLocker integration certificates.
- **Missing Audit Trail:**
  An unalterable audit trail recording parental consent grants, data processing activities, and consent withdrawals is missing.

### 17.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Policy and Consent Manager integration guide.
2. Implement DigiLocker verifiable parental consent hooks in onboarding templates.
3. Configure backend filters disabling ad tracking and profiling for under-18 Indian accounts.
4. Establish automated tests verifying zero behavioral tracking for minor accounts under Indian jurisdiction.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice

### 18.1 Regulatory Overview and Background
Singapore's PDPA and the IMDA Code of Practice for Online Safety for App Distribution Services (effective 1 April 2026) mandate app-store age assurance and data protection.

App distribution platforms and developer services must screen and prevent users estimated under 18 from downloading age-inappropriate apps. Age assurance data must be purged immediately after verification, and data breaches must be notified to PDPC within 3 days.

Official Citations: Personal Data Protection Act 2012 (No. 26 of 2012) and IMDA Code of Practice for Online Safety.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore Age Assurance and Breach Notification Policy.
- **Missing Documentation:**
  Documentation lacks developer guides for IMDA age screening compliance and 72-hour PDPC breach notification procedures.
- **Missing Code:**
  Codebases lack integration with app store age assurance signals or automated age data purge scripts.
- **Missing Disclosure:**
  UI templates fail to display clear notices explaining age screening requirements and Data Protection Officer (DPO) contact details.
- **Missing Logging:**
  Backend schemas lack 72-hour breach notification incident logs or age verification purge execution logs.
- **Missing Testing:**
  Test runner scripts do not check whether raw age verification files are deleted immediately following age determination.
- **Missing Evidence:**
  The repository lacks IMDA compliance filings or formal DPO designation documentation.
- **Missing Audit Trail:**
  An audit trail recording DPO appointments, breach notification drills, and age data purge executions is missing.

### 18.3 Remediation and Action Plan
1. Formulate a Singapore Data Protection Policy including 72-hour breach notification runbooks.
2. Implement age signal processing modules integrating with platform age-assurance frameworks.
3. Configure automated raw data deletion scripts post-verification.
4. Add CI checks asserting age verification data is never persisted in permanent storage.

---

## 19. South Korea Telecommunications Business Act

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app billing options for mobile applications distributed in South Korea.

Apple's implementation requires a Korea-only binary (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`), a 26% commission gross of VAT, approved Korean payment gateways (KCP, Toss, Inicis, NICE), pre-payment disclosure modal sheets, monthly sales reporting within 15 days, and remittance within 45 days.

Official Citation: Telecommunications Business Act Article 22-9 (South Korea).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Alternative In-App Payment Compliance Policy.
- **Missing Documentation:**
  Documentation lacks step-by-step developer guides for configuring South Korea-specific entitlement binaries, local payment gateways, and reporting workflows.
- **Missing Code:**
  Codebases lack build target configurations for South Korea binaries, Korean payment gateway integrations, or mandatory pre-payment disclosure modal sheets.
- **Missing Disclosure:**
  UI payment flows fail to display required pre-payment modal sheets informing users that alternative billing lacks Apple/Google purchase protection.
- **Missing Logging:**
  Backend schemas lack tables recording alternative billing sales, VAT calculations, and monthly reporting payloads.
- **Missing Testing:**
  Test runner scripts do not verify that Korea-specific builds refrain from co-mingling standard IAP and alternative billing within the same checkout flow.
- **Missing Evidence:**
  The repository lacks sample Korean payment gateway contracts or monthly sales reporting receipts.
- **Missing Audit Trail:**
  An immutable audit trail recording Korean alternative payment transactions, commission calculations, and monthly remittances is missing.

### 19.3 Remediation and Action Plan
1. Formulate a South Korea Alternative Payment Policy and build setup guide.
2. Implement Korea-specific binary target configurations and approved payment gateway integration modules.
3. Add mandatory native pre-payment disclosure modal sheets to checkout flows.
4. Establish automated build verification scripts ensuring alternative billing entitlement rules are strictly met.

---

## 20. China Mobile App Filing (MIIT ICP Extension), PIPL, and Banhao Licensing

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (an extension of ICP filing) for all apps distributed in mainland China (mandatory enforcement since 31 March 2024).

Foreign developers must partner with a local Chinese entity. Requirements include local filing credentials, PIPL privacy compliance, data localization (storing mainland user data on domestic servers), real-name user identity verification, and Banhao game publication licenses.

Official Citations: MIIT Notice on Organizing and Carrying Out Mobile Internet Application Filing (2023) and Personal Information Protection Law (PIPL).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China Market Entry, Data Localization, and App Filing Policy.
- **Missing Documentation:**
  Documentation lacks step-by-step developer guides for MIIT ICP app filing, local partner entity hosting, and Banhao game licensing.
- **Missing Code:**
  Codebases lack real-name identity verification SDK integrations or network routing logic ensuring mainland China user data stays on domestic servers.
- **Missing Disclosure:**
  Storefront and in-app templates fail to display MIIT ICP filing numbers, local partner entity names, and PIPL privacy declarations.
- **Missing Logging:**
  Backend schemas lack real-name identity verification logs and data transfer logs restricted to mainland China infrastructure.
- **Missing Testing:**
  Test runner scripts do not check whether non-Chinese server endpoints are blocked for mainland China app builds.
- **Missing Evidence:**
  The repository lacks templates for MIIT App Filing certificates, Banhao game licenses, or local entity partnership agreements.
- **Missing Audit Trail:**
  An unalterable audit trail recording MIIT filing renewals, real-name verification checks, and local data residency audits is missing.

### 20.3 Remediation and Action Plan
1. Formulate a China Market Compliance Policy covering MIIT filing, PIPL, and data residency.
2. Implement real-name identity verification integration modules and mainland server endpoint routing logic.
3. Add MIIT filing number metadata fields to store listing configuration templates.
4. Build automated pre-submission checks verifying local entity filing credentials and server routing compliance.

---

## 21. Consolidated Gap Classification Matrix

The table below summarizes the compliance coverage status across all twenty audited regulatory frameworks across the eight gap domains.
- **Covered**: Fully addressed with policies, documentation, code, disclosures, logging, testing, evidence, and audit trails.
- **Partial**: Named in documentation with citations, but missing complete code implementation, automated testing, or operational artifacts.
- **Missing**: Not addressed in the repository.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU EAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China Mobile App Filing**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Strategic Implementation Roadmap

The honest evaluation across all twenty modern global and regional regulations reveals that while the repository provides strong conceptual and documentation-level references for eighteen frameworks, critical operational layers remain absent. Specifically:
1. **EU GPSR** is absent end-to-end, requiring immediate inclusion of policies, metadata schemas, UI components, and guard rules.
2. The remaining nineteen frameworks carry **Partial** status, meaning they are cited and documented, but lack executable code templates, automated tests, logging schemas, formal evidence templates, and immutable audit trails.

### Prioritized Remediation Roadmap
1. **Immediate (Phase 1):** Integrate EU GPSR detection rules into `data/rejection-patterns.json`, `scripts/metadata-audit.py`, and `scripts/release-audit.py`.
2. **Short-Term (Phase 2):** Implement front-end code templates for the EU Contract Withdrawal Button, EU AI Act Article 50 disclosures, and California GPC header parsing.
3. **Mid-Term (Phase 3):** Develop automated backend scripts for e-Evidence 8-hour emergency data extraction, BIPA 3-year data destruction, and ASAA age-verification data purging.
4. **Long-Term (Phase 4):** Establish immutable audit trail schemas and CI test suites across all twenty regulatory domains to ensure continuous compliance verification prior to release.

---

## 23. Official Primary Sources

Every regulation evaluated in this report is cited to its official primary source in accordance with the strict source trust hierarchy.

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Financial Services Distance Marketing Directive: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Amended COPPA Rule: [16 CFR Part 312 (Federal Register 90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Privacy Rights Act: [California Civil Code Section 1798.100 et seq.](https://oag.ca.gov/privacy/ccpa)
- Illinois Biometric Information Privacy Act: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US Restore Online Shoppers' Confidence Act (ROSCA): [15 U.S.C. 8401 et seq.](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- Utah App Store Accountability Act: [Utah SB 142 (2025)](https://le.utah.gov/~2025/bills/static/SB0142.html)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Amendment Act 2024: [Online Safety Amendment (Social Media Minimum Age) Act 2024](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA: [Lei No. 15.211/2025](https://www.in.gov.br/)
- India DPDPA: [The Digital Personal Data Protection Act, 2023](https://egazette.gov.in/)
- Singapore PDPA: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act: [Telecommunications Business Act Article 22-9](https://www.law.go.kr/)
- China MIIT App Filing: [MIIT Mobile Internet Application Filing Notice (2023)](https://www.miit.gov.cn/)
