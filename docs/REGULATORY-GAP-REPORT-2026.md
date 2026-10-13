# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, the US, the UK, Australia, Brazil, Canada, India, Singapore, South Korea, China, and global storefronts, checking honestly how far this repository carries each one, what it only mentions in passing, and what it does not cover at all.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems and software, the GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no way to decide whether their listing falls inside Regulation (EU) 2023/988, and no template policy to hand a client who asks.
- **Missing Documentation:**
  The repository is missing specific developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack any rules or patterns to scan codebase files for GPSR-related elements. Additionally, mock user interfaces and templates in this repository do not contain code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address (such as email or website) as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, recalls, or corrective actions. The repository fails to supply templates for a centralized, secure incident log.
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
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives for the purpose of gathering evidence. Adopted in 2023, the mandatory compliance enforcement date is 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU, regardless of where the provider is headquartered. The default compliance window to produce user data is 10 days, but in critical emergency cases, providers are legally required to produce the requested data within a strict 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, so a small team receiving an EU judicial order has nothing to start from and no guidance on who may act on it.
- **Missing Documentation:**
  While the repository mentions the e-Evidence Package in general, it lacks concrete operational instructions, runbooks, or detailed manuals for handling 10-day standard orders and 8-hour emergency orders.
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
  A secure, unalterable audit trail system to record every administrative interaction, data extraction, and transmission made by compliance officers during a legal request is completely absent.

### 2.3 Remediation and Action Plan
1. Draft and implement a comprehensive Law Enforcement Response Protocol that specifically establishes the roles, responsibilities, and secure communication channels for executing EPOs.
2. Formally designate an EU establishment or legal representative and notify the designated central authority before the 18 August 2026 deadline.
3. Build secure backend scripts to automate the extraction and encryption of requested user datasets, ensuring execution can occur within the 8-hour emergency window.
4. Establish a tamper-proof cryptographic audit trail to log all incoming certificates, verification checks, data extractions, and secure transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts for financial services concluded by electronic means.

Scope matters here. The withdrawal button obligation in this Directive attaches to distance financial services contracts and consumer subscriptions. The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14 day withdrawal right, and no guidance separating apps that genuinely fall in scope from those adopting it as a design default.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying the placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
- **Missing Code:**
  The front-end user interface templates and billing mock codes in this repository do not contain any functional implementation of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining the consequences and terms of contract revocation.
- **Missing Logging:**
  There are no logging mechanisms designed to capture and record when a user clicks the withdrawal button, the timestamp of the request, the confirmation of contract termination, or the initiation of the refund flow.
- **Missing Testing:**
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction (such as requiring customer service interaction).
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking the historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination without requiring manual human approval.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977 / Act 185, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 / Act 185 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although the rejection patterns contain entries for state-level laws, the mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  The in-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log the receipt of parental consent, consent revocations (such as the `RESCIND_CONSENT` server notification), or the immediate deletion of raw age-verification documents.
- **Missing Testing:**
  The test suites do not include automated integration tests to verify that the application blocks minor accounts from accessing premium features or completing in-app purchases in the absence of valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to prove compliance to state Attorneys General.
- **Missing Audit Trail:**
  An immutable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is entirely absent.

### 4.3 Remediation and Action Plan
1. Create a detailed written Minor Age Assurance Policy that specifies how state-level requirements are identified and how children's data is strictly minimized.
2. Implement cross-platform native hooks in the mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and automated procedures to purge raw age-verification data immediately after the user's age category is confirmed.
4. Establish automated unit tests that verify that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is successfully processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems (including mobile application developers utilizing third-party generative AI APIs) must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with the technical complexity and impact of the AI integration. Pragmatic compliance for a software engineering team requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable directly to runtime mobile code, but missing developer tool scripts or lints that verify whether a literacy record is present in the repository before building an AI feature.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose our commitment to or enforcement of AI literacy standards as mandated by Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no automated internal lints, pre-commit hooks, or CLI tools to verify that team members committing AI-related changes have valid, up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of what acceptable evidence looks like, such as a completed training log, a course record, or a written risk assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting when the AI literacy policy was reviewed, when training modules were updated, or how team training records evolved over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining the required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review the team's literacy records on an annual basis.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been reviewed or updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026. This framework is a critical release blocker for any application incorporating artificial intelligence that reaches users in the European Union.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that those persons are informed that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems (text, audio, images, or video) must be marked in a machine-readable format and detectable as artificially generated or manipulated. Article 50(4) requires deployers of deepfakes to disclose that the content has been artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  The codebase templates do not include helper classes, middle-tier layers, or utilities to inject in-audible or invisible machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the required immediate disclosure ("You are interacting with an AI system") at the time of the first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  The existing test runner scripts do not check for the presence of synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording our technical choices, vendor audits, model changes, and modifications to our transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that the machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, regulates gatekeeper core platform services. For app developers, DMA provisions under Article 5(4) and Article 6 prohibit gatekeepers (such as Apple and Google) from restricting external link promotions, alternative in-app payment processing, or alternative app distribution channels in the EU/EEA.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written operational policy guiding developers on when and how to adopt DMA entitlements (External Purchase Link, Alternative Marketplace, HCE, Browser Engine) without violating store rules outside the EU.
- **Missing Documentation:**
  Lacks developer guides detailing the exact technical setup for Apple's Attachment 14 business terms, Core Technology Commission (CTC) reporting, or Web Distribution notarization flows.
- **Missing Code:**
  Missing code implementations for handling the required `ExternalPurchaseCustomLink` system disclosure sheets or monthly External Purchase Server API payload generators.
- **Missing Disclosure:**
  In-app UI components lack standard user disclosures required when navigating away to external web payment funnels under DMA entitlement rules.
- **Missing Logging:**
  No backend logging schema to record monthly external purchase transactions, fee calculations, or API submission receipts required by platform gatekeepers.
- **Missing Testing:**
  No automated unit or integration tests to verify that DMA entitlement code paths are strictly region-gated to EU/EEA storefronts and disabled for non-EU users.
- **Missing Evidence:**
  Missing proof templates for Account Holder acceptance of ADPLA Attachment 14, alternative marketplace eligibility criteria, or bank stand-by letter of credit documentation.
- **Missing Audit Trail:**
  No audit trail tracking entitlement requests, monthly transaction reports sent to Apple/Google, or fee reconciliation records.

### 7.3 Remediation and Action Plan
1. Document DMA Entitlement Adoption Policy and EU Storefront Region-Gating Rules.
2. Add code helpers for `ExternalPurchaseCustomLink` and monthly external purchase reporting scripts.
3. Add automated checks verifying that DMA code paths are inactive on non-EU storefronts.

---

## 8. EU Digital Services Act (DSA) Trader Status

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, Articles 30 and 31 require app stores to verify and publish the trader status, phone number, physical address, and email of all entities offering apps to EU consumers.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No internal policy defining trader versus non-trader criteria under EU consumer protection law for distributed mobile applications.
- **Missing Documentation:**
  Lacks step-by-step documentation on completing App Store Connect and Google Play Console DSA trader verification forms and uploading 2FA documentation.
- **Missing Code:**
  No pre-submission guard script rules to verify whether DSA trader status metadata is set in store listing configs prior to EU build distribution.
- **Missing Disclosure:**
  No in-app developer disclosure templates or settings screens displaying verified trader information directly to end-users as an alternative contact path.
- **Missing Logging:**
  No system logs capturing when trader verification status was confirmed or updated in platform consoles.
- **Missing Testing:**
  No automated tests checking metadata configuration files for verified trader address, phone, and email fields.
- **Missing Evidence:**
  Missing repository storage templates for trader verification documents (business registration, government ID, D-U-N-S verification receipts).
- **Missing Audit Trail:**
  No audit trail recording annual trader status reviews or store removal notices related to DSA compliance.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Compliance Guide and pre-submission validation script in `scripts/metadata-audit.py`.
2. Add trader verification record templates in the compliance documentation folder.

---

## 9. European Accessibility Act (EAA) / EN 301 549

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) became enforceable on 28 June 2025. It mandates accessibility across consumer digital services and mobile apps, evaluated under standard EN 301 549 (WCAG 2.1 AA / WCAG 2.2).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate Accessibility Compliance Policy setting standards for mobile UI components, design systems, and third-party vendor libraries.
- **Missing Documentation:**
  Lacks developer guides detailing EN 301 549 Chapter 11 mobile-specific requirements (non-web software) beyond standard web WCAG.
- **Missing Code:**
  Missing default accessibility modifiers, VoiceOver traits, dynamic font scaling wrappers, or high-contrast UI component abstractions in app UI templates.
- **Missing Disclosure:**
  No template for an in-app or public Accessibility Statement mandated by EN 301 549 Annex B/C detailing accessibility conformity and feedback mechanisms.
- **Missing Logging:**
  No logging mechanism to collect user accessibility feedback, barrier reports, or screen-reader usability issues.
- **Missing Testing:**
  No automated UI accessibility tests running static analysis on layout files or dynamic VoiceOver / TalkBack navigation checks.
- **Missing Evidence:**
  Missing Accessibility Conformance Reports (VPAT / EN 301 549 Evaluation Statements) proving compliance.
- **Missing Audit Trail:**
  No audit trail tracking accessibility remediations, annual accessibility audits, or design system updates.

### 9.3 Remediation and Action Plan
1. Publish an Accessibility Policy and EN 301 549 Chapter 11 developer checklist.
2. Integrate `scripts/accessibility-audit.py` into CI pre-submission pipelines.
3. Provide an in-app Accessibility Statement template in `templates/`.

---

## 10. US Children's Online Privacy Protection Act (COPPA) & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
16 CFR Part 312 (COPPA) regulates the collection of personal information from children under 13. The FTC's final amended COPPA Rule (90 FR 16918) introduces expanded PII definitions (biometrics, government IDs), separate opt-in consent for targeted ads, written retention schedules, and mandatory information security programs.

Official Citation: 16 CFR Part 312 (FTC Final Rule 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No formal Children's Privacy Policy or written Data Retention and Security Policy compliant with 16 CFR Part 312.8 and 312.10.
- **Missing Documentation:**
  Lacks developer runbooks on implementing FTC-approved verifiable parental consent (VPC) mechanisms (face-match ID, knowledge-based auth) and zero-tracking SDK gating.
- **Missing Code:**
  Codebase templates lack native parental gate components, age-gating triggers, or automatic SDK initialization blocks for child users.
- **Missing Disclosure:**
  Direct parental notices and in-app privacy disclosures lack updated COPPA disclosures regarding biometric data and separate ad-tracking opt-ins.
- **Missing Logging:**
  No backend schema for logging parental consent receipts, consent revocations, or automated deletion timestamps for child PII.
- **Missing Testing:**
  No automated integration tests verifying that analytics, ad networks, and tracking SDKs remain disabled when a child DOB is entered.
- **Missing Evidence:**
  Lacks templates for Annual Information Security Assessments, Safe Harbor certification records, or parental consent audit logs.
- **Missing Audit Trail:**
  No immutable audit trail documenting child PII deletion, SDK audits, or annual COPPA compliance reviews.

### 10.3 Remediation Plan
1. Implement COPPA Written Security Program and Retention Policy templates.
2. Build code modules for native parental gates and child account SDK suppression.
3. Add CI tests verifying zero tracking SDK execution for minor profiles.

---

## 11. California Consumer Privacy Act / Privacy Rights Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The CCPA/CPRA and CPPA 2026 regulations enforce privacy rights for California residents, mandating "Do Not Sell or Share" controls, Global Privacy Control (GPC) support, sensitive personal information limits, and automated decision-making opt-outs.

Official Citation: Cal. Civ. Code § 1798.100 et seq. and CPPA Regulations.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a comprehensive California Privacy Policy template incorporating 2026 CPPA regulatory additions.
- **Missing Documentation:**
  No developer guide on handling embedded webview `Sec-GPC` headers or native app opt-out signals.
- **Missing Code:**
  Missing code handlers for parsing Global Privacy Control headers or exposing native "Do Not Sell or Share My Personal Information" UI toggles.
- **Missing Disclosure:**
  Notice at Collection templates lack required CPPA disclosures for automated decision-making and sensitive personal info processing.
- **Missing Logging:**
  No schema for logging consumer privacy requests (know, delete, correct, opt-out) or tracking 45-day response deadlines.
- **Missing Testing:**
  No automated tests checking whether enabling GPC suppresses third-party tracking payloads.
- **Missing Evidence:**
  Lacks risk assessment templates or cybersecurity audit certification records required under CPPA rules.
- **Missing Audit Trail:**
  No audit trail tracking consumer privacy request fulfillment rates or GPC signal processing logs.

### 11.3 Remediation Plan
1. Add GPC header parser and native privacy opt-out toggle code components.
2. Create CCPA/CPRA Consumer Request Handling Runbook and Privacy Notice templates.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
740 ILCS 14 (BIPA) requires explicit written consent prior to collecting biometric identifiers (fingerprints, face scans, voiceprints), public retention schedules, and immediate destruction upon goal fulfillment.

Official Citation: Illinois Compiled Statutes 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Biometric Information Privacy Policy establishing a public retention schedule and destruction guidelines.
- **Missing Documentation:**
  Lacks technical guides on differentiating raw biometric template collection from on-device local authentication (e.g. Face ID / Touch ID).
- **Missing Code:**
  Missing written biometric release/consent modal sheets in mobile app templates.
- **Missing Disclosure:**
  In-app disclosures do not state specific biometric storage terms or destruction criteria before camera/biometric access.
- **Missing Logging:**
  No backend logging schema capturing e-signatures or explicit consents for biometric data processing.
- **Missing Testing:**
  No tests verifying that raw biometric features are blocked until an affirmative written consent flag is recorded.
- **Missing Evidence:**
  Lacks standardized biometric consent forms or destruction certificate templates.
- **Missing Audit Trail:**
  No unalterable audit trail recording biometric consent timestamps or destruction schedules.

### 12.3 Remediation Plan
1. Draft a BIPA-compliant Biometric Policy and Consent Modal template.
2. Add automated guard rules blocking biometric SDK calls without consent flags.

---

## 13. US FTC Subscription Cancellation / Click-to-Cancel Rules

### 13.1 Regulatory Overview and Background
Enforced under ROSCA (15 U.S.C. § 8401), FTC Act Section 5, and state negative option laws (California, New York, Massachusetts), cancellation of recurring subscriptions must be as easy as sign-up, offering a simple, frictionless online cancellation path.

Official Citation: 15 U.S.C. § 8401 (ROSCA) and state negative option statutes.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate Subscription Cancellation Policy requiring equal friction for onboarding and cancellation.
- **Missing Documentation:**
  Lacks developer UI guidelines for building compliant, self-service cancellation paths without forced phone calls or save-discount hurdles.
- **Missing Code:**
  Mobile app templates lack a 1-tap or simple self-service subscription cancellation flow for web-billed accounts.
- **Missing Disclosure:**
  Subscription paywalls lack clear, upfront disclosure of renewal terms, cancellation mechanics, and billing dates.
- **Missing Logging:**
  No logging schema tracking cancellation flow interactions, user attempts, or immediate termination receipts.
- **Missing Testing:**
  No UI automation tests verifying that cancellation can be completed in the same number of steps as registration.
- **Missing Evidence:**
  Lacks templates for pre-cancellation disclosures, confirmation receipts, or billing logs.
- **Missing Audit Trail:**
  No audit trail recording subscription cancellation success rates or paywall copy modifications.

### 13.3 Remediation Plan
1. Build frictionless Subscription Cancellation UI components for web/external billing.
2. Add paywall disclosure checklists to `docs/PRE-SUBMISSION-CHECKLIST.md`.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code require highly effective age assurance, child safety risk assessments, and default high-privacy settings for UK users.

Official Citation: UK Online Safety Act 2023 c. 50 and ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No UK Online Safety & Children's Code Compliance Policy.
- **Missing Documentation:**
  Lacks technical runbooks on executing Ofcom-approved age assurance (facial age estimation, open banking) and CSEA reporting.
- **Missing Code:**
  Missing code logic for defaulting UK minor profiles to high privacy, geolocation OFF, and profiling OFF.
- **Missing Disclosure:**
  No child-friendly privacy notices or UK Online Safety warnings in app onboarding.
- **Missing Logging:**
  No backend schema for logging child safety risk assessments, Ofcom reporting events, or CSEA report receipts.
- **Missing Testing:**
  No automated tests verifying high-privacy defaults for UK child accounts.
- **Missing Evidence:**
  Lacks templates for Data Protection Impact Assessments (DPIAs) required under the ICO Children's Code.
- **Missing Audit Trail:**
  No audit trail tracking risk assessment updates or Ofcom safety compliance audits.

### 14.3 Remediation Plan
1. Add ICO Children's Code high-privacy default configuration templates.
2. Provide DPIA template tailored for mobile applications reaching UK children.

---

## 15. Australia Online Safety Act & App Distribution Industry Codes

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 and App Distribution Services Industry Code (Schedule 7) impose under-16 account restrictions, waterfall age assurance, and age-gating for adult apps.

Official Citation: Online Safety Amendment Act 2024 and eSafety Industry Codes.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Australia Online Safety Policy addressing age-restricted social media or adult app download controls.
- **Missing Documentation:**
  Lacks developer guides for integrating eSafety-compliant waterfall age assurance and immediate age-data destruction.
- **Missing Code:**
  Missing code logic to handle Apple's Australia 18+ download block or 15+ rating removal updates.
- **Missing Disclosure:**
  In-app disclosures do not inform Australian users of mandatory age verification or data ringfencing rules.
- **Missing Logging:**
  No schema for logging age verification execution without retaining raw identity tokens.
- **Missing Testing:**
  No tests verifying under-16 account blocking on social media feature modules.
- **Missing Evidence:**
  Lacks risk assessment documentation required under the App Distribution Services Code.
- **Missing Audit Trail:**
  No audit trail recording age-data purge confirmations or annual eSafety compliance filings.

### 15.3 Remediation Plan
1. Create Australia Online Safety integration guide and age-data destruction verification script.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decree 12,880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA and Decree 12,880/2026 enforce mandatory age verification (document check, facial estimation, CPF database check) and guardian authorization, prohibiting simple self-declaration checkboxes for minors.

Official Citation: Lei nº 15.211/2025 and Decreto nº 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Brazil Child Protection and Age Verification Policy.
- **Missing Documentation:**
  Lacks technical documentation on connecting to Brazil Play Age Signals API or ANPD-approved age verification channels.
- **Missing Code:**
  Missing code modules for handling Brazil loot-box 18+ auto-rating and guardian consent flows.
- **Missing Disclosure:**
  No Portuguese-language disclosures explaining age signal queries or guardian approval requirements.
- **Missing Logging:**
  No backend schema capturing guardian consent tokens or ANPD-compliant verification logs.
- **Missing Testing:**
  No automated tests verifying that loot-box or 18+ gated features block unverified minor sessions in Brazil.
- **Missing Evidence:**
  Lacks templates for ANPD age-assurance compliance proofs or ADPLA Attachment 12 acceptance records.
- **Missing Audit Trail:**
  No audit trail tracking guardian consent revocations or age signal verification histories.

### 16.3 Remediation Plan
1. Add Brazil Digital ECA compliance module and Portuguese disclosure templates.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 mandate verifiable parental consent for individuals under 18 (e.g. via DigiLocker), prohibit behavioral tracking/targeted ads for children, and require multi-lingual consent notices.

Official Citation: Act No. 22 of 2023 and G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No India Data Protection Policy covering DPDPA consent managers and under-18 restrictions.
- **Missing Documentation:**
  Lacks developer guides on integrating with registered Consent Managers or DigiLocker VPC flows.
- **Missing Code:**
  Missing multi-lingual consent notice UI components in 22 scheduled Indian languages.
- **Missing Disclosure:**
  Consent notices lack itemized processing disclosures in clear, accessible language required by Rule 3.
- **Missing Logging:**
  No logging schema capturing consent artifacts, consent withdrawals, or Consent Manager API calls.
- **Missing Testing:**
  No tests verifying that behavioral tracking SDKs are completely disabled for under-18 users in India.
- **Missing Evidence:**
  Lacks Data Protection Board (DPBI) compliance filings or VPC integration proofs.
- **Missing Audit Trail:**
  No audit trail recording consent updates, parent authorization logs, or data principal grievance resolutions.

### 17.3 Remediation Plan
1. Add DPDPA multi-lingual consent disclosure templates and minor ad-block test cases.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
Singapore PDPA and IMDA Code of Practice for Online Safety mandate 3-day breach notification, DPO designation, and app-store age assurance stopping under-18 downloads of inappropriate content.

Official Citation: Personal Data Protection Act 2012 and IMDA Code of Practice.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore PDPA Policy or Incident Management Policy covering 3-day PDPC breach notification.
- **Missing Documentation:**
  Lacks operational runbooks for DPO contact publication and IMDA age-assurance alignment.
- **Missing Code:**
  Missing code logic for handling Singapore 18+ download blocks and age signal checks.
- **Missing Disclosure:**
  No disclosure of Data Protection Officer (DPO) contact details in app privacy settings.
- **Missing Logging:**
  No schema for logging personal data access logs or PDPC incident notification timelines.
- **Missing Testing:**
  No automated tests checking that 18+ gated assets are restricted on Singapore storefronts.
- **Missing Evidence:**
  Lacks templates for PDPC Breach Notification forms or IMDA compliance self-assessments.
- **Missing Audit Trail:**
  No audit trail tracking DPO reviews, security incidents, or age data deletion events.

### 18.3 Remediation Plan
1. Draft Singapore PDPA Compliance Guide and DPO Contact Disclosure template.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options (26% fee model) and PIPA Amendment (Act No. 21445) enforces strict CEO privacy accountability and board-approved CPO requirements.

Official Citation: Telecommunications Business Act and PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Korea Privacy and Alternative Payment Policy.
- **Missing Documentation:**
  Lacks developer guides for building Korea-only binaries (`SKExternalPurchase = "KR"`), integrating approved local payment gateways (KCP, Toss, Inicis, NICE), and submitting 15-day monthly sales reports.
- **Missing Code:**
  Missing code logic for Korea native external purchase modal sheets and StoreKit Korea payment entitlement configurations.
- **Missing Disclosure:**
  Paywalls lack required Korean-language disclosures regarding alternative payment terms and loss of Apple/Google consumer protections.
- **Missing Logging:**
  No backend schema for tracking Korea alternative billing sales, VAT calculations, and monthly remittance records.
- **Missing Testing:**
  No tests verifying that alternative payment entitlement `com.apple.developer.storekit.external-purchase` is restricted to KR storefront binaries.
- **Missing Evidence:**
  Lacks GRAC rating certificate records or KCC compliance filings.
- **Missing Audit Trail:**
  No audit trail recording monthly sales reports submitted to Apple/Google or CPO board approval minutes.

### 19.3 Remediation Plan
1. Provide Korea Alternative Payment Entitlement guide and monthly sales reporting helper script.

---

## 20. China Mobile App Filing (MIIT ICP Extension) & CAC AI Measures

### 20.1 Regulatory Overview and Background
MIIT Mobile App Filing (ICP extension), PIPL, and CAC Interim Measures for AI Anthropomorphic Interactive Services (Order No. 21) require local Chinese entity filing, real-name verification, automated minor mode switching, and a total ban on AI virtual companions for minors.

Official Citation: MIIT Mobile App Filing Rules and CAC Order No. 21.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China Compliance Policy covering MIIT App Filing, PIPL data localization, and CAC AI Minor restrictions.
- **Missing Documentation:**
  Lacks technical runbooks for obtaining local Chinese partnership filings, ICP numbers, and Banhao game licenses.
- **Missing Code:**
  Missing code modules for automatic Minors Mode switching, real-name authentication integrations, and AI companion blocking for under-18s in China.
- **Missing Disclosure:**
  No in-app display of MIIT App Filing ICP numbers or CAC synthetic content warnings.
- **Missing Logging:**
  No schema for logging real-name verification status or CAC compliance audit logs.
- **Missing Testing:**
  No automated tests verifying that AI chatbot companion features are completely disabled for Chinese minor IP/storefront sessions.
- **Missing Evidence:**
  Lacks templates for MIIT ICP filing certificates, CAC security assessments, or PIPL cross-border transfer approvals.
- **Missing Audit Trail:**
  No audit trail tracking bi-annual PIPL personal information compliance audits or CAC algorithmic filings.

### 20.3 Remediation Plan
1. Draft China App Distribution Runbook covering MIIT filing, PIPL, and CAC Order No. 21 AI restrictions.

---

## 21. Consolidated Gap Classification Matrix

The gap matrix evaluates all twenty audited global and regional frameworks across the eight core compliance domains.
- **Covered**: Repository includes actionable developer rules, code/scripts, and checklists.
- **Partial**: Framework is cited or mentioned, but lacks complete code templates, test automation, or formal evidence artifacts.
- **Missing**: Framework is not represented in code, detection rules, or dedicated operational policies.
- **N/A**: Category is not applicable to the specific regulatory mandate (e.g. code for organizational AI literacy).

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA / Amended Rule** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA/CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Click-to-Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety / ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Strategic Remediation and Execution Plan

To systematically resolve the identified gaps across all twenty regulatory frameworks, the playbook implementation roadmap is prioritized into three key execution phases:

### Phase 1: High-Priority Legal & Regulatory Release Blockers (Immediate)
1. **EU GPSR Implementation**: Add detection rules in `data/rejection-patterns.json` and `data/detection-recipes.json`, and provide UI metadata templates for EU storefront listings displaying manufacturer address, trade name, and electronic contact details.
2. **EU AI Act Article 50 & 4**: Build UI notice components ("You are interacting with an AI system"), C2PA/watermarking helper code, and an internal AI literacy tracking log (`AI_LITERACY_LOG.md`).
3. **EU Contract Withdrawal Button**: Add a self-service cancellation component template for subscription interfaces meeting Directive (EU) 2023/2673.
4. **US State ASAA & Brazil Digital ECA**: Add native age signal integration modules (`DeclaredAgeRange` and `com.google.android.play:age-signals`) and age-data deletion scripts.

### Phase 2: Core Platform Mechanics & Accessibility (Near-Term)
1. **European Accessibility Act (EAA)**: Expand `scripts/accessibility-audit.py` to enforce EN 301 549 Chapter 11 rules, and provide an in-app accessibility statement template.
2. **COPPA Amended Rule & BIPA**: Add templates for written Information Security Programs, retention schedules, and biometric consent modals.
3. **EU DMA & DSA Trader Status**: Enhance `scripts/metadata-audit.py` to validate DSA trader metadata and DMA entitlement region-gating.

### Phase 3: Global Compliance & Enforcement Hardening (Ongoing)
1. **Global Privacy & Subscription Flows**: Implement GPC header parsing in webview templates and 1-tap cancellation flows under ROSCA/state laws.
2. **International Regional Modules**: Provide regional distribution guides and configuration templates for UK, Australia, India, Singapore, South Korea, and China app distribution.

---

## 23. Official Sources

All citations adhere strictly to Priority 1 official regulatory and standardization sources:

- EU General Product Safety Regulation: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Children's Online Privacy Protection Rule: [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Privacy Protection Agency: [CPPA Regulations](https://cppa.ca.gov/regulations/ccpa_updates.html)
- FTC Take It Down Act & Health Breach Rule: [FTC Business Guidance](https://www.ftc.gov/business-guidance)
- UK Information Commissioner's Office: [ICO Children's Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- Australia eSafety Commissioner: [eSafety Social Media Regulations](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil ANPD & Digital ECA: [Governo Federal do Brasil](https://www.gov.br/anpd/pt-br/assuntos/eca-digital)
- India Ministry of Electronics & IT: [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore IMDA & PDPC: [IMDA Online Safety](https://www.mddi.gov.sg)
- South Korea Personal Information Protection Commission: [PPC Korea](https://www.ppc.go.jp)
- China Cyberspace Administration of China: [CAC Regulations](https://www.cac.gov.cn)
