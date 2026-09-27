# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major global and regional regulations that bind mobile application developers and digital platforms shipping into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global markets. It checks honestly how far this repository already carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles: missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

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

Scope matters here. The withdrawal button obligation in this Directive attaches to distance financial services contracts, not to every consumer subscription. Treat it as binding today if your app sells insurance, credit, payment, investment, or another financial service into the EU, and as a strong design default otherwise, since Apple already requires an easy in-app cancellation path regardless.

The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating apps that genuinely fall in scope from those adopting it as a design default.
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
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination without requiring manual human approval.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

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
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
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
  Not applicable directly to runtime binary execution, but a missing CLI utility or linter in `scripts/` to check whether an `AI_LITERACY_LOG.md` exists and is current before releasing AI features.
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
1. Draft and publish an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review team literacy records on an annual basis.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been reviewed or updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026. This framework is a critical release blocker for any application incorporating artificial intelligence that reaches users in the European Union.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that those persons are informed that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems (text, audio, images, or video) must be marked in a machine-readable format and detectable as artificially generated or manipulated. Article 50(4) requires deployers of deepfakes to disclose that content has been artificially generated or manipulated.

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
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that machine-readable compliance headers are properly set and preserved.

---

## 7. Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates designated gatekeepers (such as Apple and Google) and grants third-party application developers enforceable rights regarding interoperability, side-loading, alternative app stores, alternative payment processors, and unbundled fee structures within the European Economic Area (EEA).

For mobile app developers shipping into the EU, compliance involves choosing between standard store models and alternative distribution frameworks (e.g., Apple's Alternative Terms Addendum for Apps in the EU, Core Technology Fee, alternative payment service providers, and web distribution). Developers must handle region-specific entitlements, web-to-app installation flows, and external payment disclosures correctly.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council on contestable and fair markets in the digital sector.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an enterprise EEA Distribution & Alternative Payments Policy to evaluate whether adopting DMA alternative terms or alternative billing is commercially and legally viable.
- **Missing Documentation:**
  The repository lacks developer runbooks explaining how to configure build targets for alternative store distribution, web distribution links, or non-StoreKit/non-Play payment gateways in EU builds.
- **Missing Code:**
  The sample codebases do not contain conditional compilation logic or regional runtime checks (e.g., checking if the user is located in the EEA) to toggle alternative billing sheets or web purchase links safely.
- **Missing Disclosure:**
  Template user interfaces do not include the mandatory DMA alternative payment modal disclosures informing EEA users that the transaction is processed outside the app store and that store purchase protections do not apply.
- **Missing Logging:**
  There are no backend schemas or event log specifications to track alternative billing transactions or export monthly sales reporting data mandated by gatekeeper developer agreements (e.g., Apple EU reporting).
- **Missing Testing:**
  No automated UI or integration tests exist to verify that alternative payment sheets trigger only for EEA IP addresses/accounts and fall back to native store billing outside the EU.
- **Missing Evidence:**
  The repository provides no template records of gatekeeper entitlement requests, Core Technology Fee (CTF) threshold calculation worksheets, or signed DMA addenda.
- **Missing Audit Trail:**
  An audit trail tracking changes to regional payment routing, fee structure calculations, and EEA distribution agreements is missing.

### 7.3 Remediation and Action Plan
1. Publish a DMA Compliance & Distribution Guide detailing regional entitlement configuration for alternative app marketplaces and web downloads.
2. Build sample cross-platform payment router code that checks user location and renders DMA-compliant modal disclosures for EEA transactions.
3. Implement backend transaction logging scripts for generating gatekeeper-mandated monthly reporting exports.
4. Add automated tests to verify regional fallback behavior between standard store billing and DMA alternative payment pathways.

---

## 8. Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The Digital Services Act (Regulation (EU) 2022/2065) establishes comprehensive obligations for online intermediary services, platforms, and marketplaces operating in the EU. Fully applicable since 17 February 2024, the DSA mandates trader identification (KYC), transparent recommendation algorithms, illegal content notice-and-action mechanisms, user complaint handling systems, and bans on dark patterns in online user interfaces.

Mobile apps that operate as marketplaces, facilitate user-to-user sales, or display user-generated content (UGC) must disclose trader credentials (name, address, email, phone number, trade register number) prior to contract conclusion and provide easily accessible reporting channels for illegal content.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council on a Single Market For Digital Services.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template DSA Trader Identification Policy and Notice-and-Action Policy for apps acting as online marketplaces or content hosts.
- **Missing Documentation:**
  No developer guidelines exist on how to design compliant DSA trader profile cards, illegal content report forms, or statement of reasons notifications.
- **Missing Code:**
  The codebase contains no re-usable UI components for DSA illegal content reporting, trader verification badges, or content moderation decision notices.
- **Missing Disclosure:**
  Marketplace and profile UI templates fail to display mandatory trader identity details (physical address, trade register number, self-certification status) before a transaction is initiated.
- **Missing Logging:**
  There are no database schemas or log formats designed to capture incoming illegal content notices, moderation decisions, or user appeals as required by Article 16 and Article 20 of the DSA.
- **Missing Testing:**
  No automated tests exist to verify that the notice-and-action flow correctly collects required reporting fields (reasons, location, submitter identity) or that dark pattern anti-patterns are absent from subscription/cancellation flows.
- **Missing Evidence:**
  The repository is missing template DSA transparency reports, annual content moderation summaries, or proof of trader KYC verification.
- **Missing Audit Trail:**
  An unalterable audit trail recording content moderation decisions, user appeal histories, and trader credential updates is absent.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Verification & Notice-and-Action Guide with accompanying UI wireframes for marketplace apps.
2. Develop standard React Native and Flutter UI components for illegal content reporting and DSA trader disclosure cards.
3. Design a database logging schema for content moderation notices, action logs, and transparency report generation.
4. Integrate automated UI tests verifying that trader information is rendered on product listings before checkout.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) sets mandatory accessibility requirements for key digital products and services placed on the EU market, including e-commerce apps, banking apps, e-books, transport services, and electronic communications services. Enforcement begins on 28 June 2025.

Under the EAA and its harmonious standard EN 301 549 (referencing WCAG 2.1 Level AA), mobile applications must ensure full accessibility: screen reader support (VoiceOver/TalkBack), sufficient color contrast, text resizing without loss of content, scalable touch targets, non-reliance on sensory characteristics, and avoidance of visual flashing.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council on accessibility requirements for products and services.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no written Mobile Accessibility Policy defining institutional commitment to EN 301 549 / WCAG 2.1 AA standards or describing accessibility exception processes.
- **Missing Documentation:**
  While accessibility is mentioned in checklists, step-by-step developer implementation manuals for accessibility traits, dynamic type scaling limits, and custom screen reader rotors are absent.
- **Missing Code:**
  The sample app UI components lack explicit accessibility labels (`accessibilityLabel`, `accessible`, `contentDescription`), custom rotor implementations, or high-contrast theme overrides.
- **Missing Disclosure:**
  No template Accessibility Statement page or in-app accessibility help link is provided to inform users about accessible features and feedback mechanisms.
- **Missing Logging:**
  There are no logging mechanisms to record accessibility feedback, reported accessibility barriers, or assistive technology usage trends.
- **Missing Testing:**
  Although `scripts/accessibility-audit.py` exists, automated CI test suites do not execute static analysis for missing accessibility labels across all UI view hierarchies by default.
- **Missing Evidence:**
  The playbook lacks sample Voluntary Product Accessibility Templates (VPAT) or Accessibility Conformance Reports (ACR) proving WCAG 2.1 AA compliance.
- **Missing Audit Trail:**
  An immutable audit trail documenting periodic accessibility audits, remediation tracking, and expert accessibility review logs is missing.

### 9.3 Remediation and Action Plan
1. Draft an Accessibility Policy and public Accessibility Statement template aligned with Directive (EU) 2019/882 and EN 301 549.
2. Annotate all codebase UI templates with explicit VoiceOver/TalkBack accessibility properties and Dynamic Type support.
3. Wire `scripts/accessibility-audit.py` directly into pre-submission CI checks to block builds with missing accessibility identifiers or insufficient contrast.
4. Supply a filled VPAT/ACR template for mobile application releases.

---

## 10. US Children's Online Privacy Protection Act (COPPA & Amended COPPA Rule)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (16 CFR Part 312) regulates online services directed to children under 13 or general audience services with actual knowledge of collecting personal information from children under 13. The FTC's finalized COPPA Rule amendments (90 FR 16918, effective 23 June 2025, compliance mandatory 22 April 2026) expand personal information definitions to include biometric identifiers and government IDs, require separate opt-in consent for third-party disclosures and targeted ads, impose strict written retention schedules, and require formal written information security programs.

Official Citation: 16 CFR Part 312; FTC Final Rule 90 FR 16918 (22 April 2025).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template Children's Privacy Policy, a written COPPA Data Retention Policy (312.10), and a written Information Security Program document (312.8).
- **Missing Documentation:**
  Developer guides do not detail step-by-step procedures for implementing separate consent toggles for third-party disclosures versus core app features under the 2026 Amended Rule.
- **Missing Code:**
  Code templates lack age-gating mechanisms, parental gate modals, separate opt-in consent switches for targeted advertising, or secure deletion triggers for under-13 personal data.
- **Missing Disclosure:**
  In-app consent forms do not include mandatory 2026 COPPA disclosures regarding biometric data collection, third-party data sharing, or parental rights to review/delete data.
- **Missing Logging:**
  No backend logging schema exists to record verifiable parental consent (VPC) methods used, consent timestamps, separate ad opt-in flags, or automated data deletion events.
- **Missing Testing:**
  Test suites lack automated unit tests verifying that third-party tracking SDKs remain uninitialized when a user is identified as under 13 or prior to receiving verifiable parental consent.
- **Missing Evidence:**
  The repository lacks sample FTC Safe Harbor compliance certificates, written risk assessment templates, or verifiable parental consent record sheets.
- **Missing Audit Trail:**
  An unalterable audit trail recording changes to parental consent status, consent revocations, and data deletion logs for child accounts is absent.

### 10.3 Remediation and Action Plan
1. Create a written COPPA 2026 Compliance Package including Children's Privacy Policy, Data Retention Policy, and Information Security Program template.
2. Implement code patterns for robust age-gating, parental consent verification, and conditional SDK initialization.
3. Add automated integration tests verifying that ad network SDKs and telemetry are disabled for under-13 users.
4. Establish an audit logging mechanism to maintain tamper-proof records of VPC completions and data purges.

---

## 11. California Consumer Privacy Act (CCPA / CPRA / CPPA 2026 Regs) & AADC

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), and the CPPA 2026 Regulations mandate comprehensive privacy controls for California residents. Required mechanisms include "Do Not Sell or Share My Personal Information" links, Global Privacy Control (GPC) signal detection, "Limit the Use of My Sensitive Personal Information" toggles, and risk assessments. Furthermore, the California Age-Appropriate Design Code Act (AB 2273) and Digital Age Assurance Act (AB 1043, operative 1 January 2027) establish strict age-assurance and data protection duties for youth users.

Official Citations: Cal. Civ. Code Section 1798.100 et seq.; California CPPA Regulations (2026); California AB 2273 / AB 1043.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a California Specific Privacy Rights Notice template covering CCPA/CPRA rights, sensitive personal info usage policies, and GPC compliance procedures.
- **Missing Documentation:**
  Developer documentation fails to specify how mobile apps must handle GPC signals transmitted via embedded webviews or honor opt-out preferences across native app boundaries.
- **Missing Code:**
  Codebase templates do not contain code for detecting the `Sec-GPC` HTTP header, rendering a native "Do Not Sell or Share" toggle, or invoking native sensitive data limitation APIs.
- **Missing Disclosure:**
  In-app onboarding and setting screens lack required California Notice at Collection disclosures detailing categorized data collection, commercial purposes, and retention periods.
- **Missing Logging:**
  There are no logging mechanisms or database schemas to log consumer rights requests (access, delete, correct, opt-out), verification steps, or fulfillment timestamps within statutory deadlines.
- **Missing Testing:**
  No automated UI or integration tests exist to confirm that enabling "Do Not Sell or Share" or receiving a GPC signal halts third-party data transmission in real time.
- **Missing Evidence:**
  The playbook is missing template Cybersecurity Audit reports, CPPA Risk Assessment filings, or annual consumer request metrics summaries required by Cal. Civ. Code Section 1798.99.28.
- **Missing Audit Trail:**
  An immutable audit trail documenting consumer privacy request receipts, identity verification steps, opt-out propagation, and data deletion receipts is absent.

### 11.3 Remediation and Action Plan
1. Publish a CCPA/CPRA/CPPA Compliance Module with California Notice at Collection and Privacy Policy templates.
2. Build native React Native/Flutter modules for GPC header detection, native "Do Not Sell/Share" state management, and sensitive info limiting.
3. Implement a backend schema and workflow for logging and managing California consumer privacy requests within 45 days.
4. Create automated CI test suites to verify that opt-out toggles immediately cease ad-tracking SDK data transmissions.

---

## 12. Illinois Biometric Information Privacy Act (BIPA) & Texas CUBI

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) and Texas Capture or Use of Biometric Identifier Act (CUBI) strictly regulate the collection, capture, purchase, storage, and use of biometric identifiers (fingerprints, voiceprints, retina/iris scans, facial geometry scans). BIPA mandates prior written consent, a publicly available retention and destruction schedule, a complete prohibition on profiting from biometric data, and strict statutory damages ($1,000 per negligent violation, $5,000 per intentional violation under amended 740 ILCS 14/20).

Official Citations: 740 ILCS 14/ (BIPA as amended by SB 2979); Tex. Bus. & Com. Code Section 503.001 (CUBI).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template Biometric Data Information Policy and a publicly disclosable Biometric Retention and Destruction Schedule.
- **Missing Documentation:**
  Developer guides fail to detail BIPA/CUBI written release requirements prior to executing native biometric authentication (e.g., LocalAuthentication / BiometricPrompt) or facial recognition.
- **Missing Code:**
  Sample codebases do not include BIPA-compliant written release consent modal screens or automated retention timer scripts to destroy stored biometric hashes within 3 years of last interaction.
- **Missing Disclosure:**
  In-app biometric consent prompts do not display mandatory BIPA disclosures regarding the specific purpose and duration for which biometric identifiers are stored.
- **Missing Logging:**
  No database schema or logging utility exists to record written biometric release consents, consent timestamps, document versions, or scheduled biometric destruction events.
- **Missing Testing:**
  Automated tests do not verify that biometric data capture functions fail closed and remain inactive if the user has not explicitly signed/accepted the written BIPA release.
- **Missing Evidence:**
  The repository lacks example copies of signed biometric consent releases, cryptographic proof of biometric template destruction, or third-party vendor non-disclosure agreements.
- **Missing Audit Trail:**
  An unalterable audit trail recording biometric consent capture, retention period monitoring, and deletion verification logs is missing.

### 12.3 Remediation and Action Plan
1. Draft a comprehensive Biometric Privacy Policy and Public Retention Schedule template.
2. Build reusable UI modal components for capturing BIPA/CUBI-compliant written consent before invoking biometric APIs.
3. Design a secure backend log schema for recording e-signed biometric releases and automated 3-year data destruction jobs.
4. Add automated integration tests verifying that biometric scanning routines are inaccessible until written consent flags are set.

---

## 13. US Subscription Cancellation (FTC Negative Option / ROSCA / State Laws)

### 13.1 Regulatory Overview and Background
While the FTC's formal "Click-to-Cancel" rule was vacated on procedural grounds, federal enforcement under Section 5 of the FTC Act and the Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) remains active. Furthermore, state-level automatic renewal laws in California (AB 2863), New York (GBL 527-a), and Massachusetts mandate that online subscription cancellation must be at least as easy as sign-up, offering a simple, frictionless online cancellation mechanism without requiring phone calls or customer service hurdles.

Official Citations: ROSCA 15 U.S.C. 8401; California AB 2863; New York GBL 527-a; FTC Section 5 Guidance.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Subscription Management & Automatic Renewal Policy explaining legal cancellation path obligations for web-billed and non-StoreKit/non-Play subscriptions.
- **Missing Documentation:**
  Developer guides do not provide step-by-step instructions for implementing one-click or simple online cancellation flows for cross-platform subscriptions.
- **Missing Code:**
  Codebase templates lack self-service subscription cancellation components, cancellation confirm modals, or automated subscription renewal reminder email triggers.
- **Missing Disclosure:**
  Subscription paywalls and onboarding screens do not display mandatory ROSCA disclosures (recurring billing amount, frequency, cancellation mechanism, and renewal dates) immediately adjacent to the call to action.
- **Missing Logging:**
  There are no backend event schemas to log subscription signup disclosures presented, user consent timestamps, cancellation initiation, or cancellation confirmation delivery.
- **Missing Testing:**
  No automated UI tests exist to verify that the subscription cancellation path can be completed in the same number of steps as signup without intervening force-retention surveys.
- **Missing Evidence:**
  The playbook lacks sample subscription confirmation email receipts, pre-renewal notification logs, or cancellation verification receipts.
- **Missing Audit Trail:**
  An immutable audit trail recording subscription state changes, cancellation requests, fee modifications, and pre-renewal notice transmissions is absent.

### 13.3 Remediation and Action Plan
1. Create a Subscription & Auto-Renewal Compliance Guide covering ROSCA and state click-to-cancel mandates.
2. Implement front-end self-service cancellation components and adjacent paywall disclosure layouts for custom web-billing flows.
3. Establish backend event logging for subscription disclosures, renewal reminders, and cancellation receipts.
4. Add end-to-end automated UI tests ensuring friction-free self-service cancellation paths.

---

## 14. UK Online Safety Act 2023 (OSA) & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the ICO Age Appropriate Design Code (Children's Code) impose strict duties of care on user-to-user services and search services accessible by children in the UK. Requirements include robust age assurance (preventing under-18 access to harmful content using "Highly Effective Age Assurance" methods like facial estimation or open banking), illegal content prevention, risk assessments, high default privacy settings, geolocation off by default, and profiling off by default.

Official Citations: UK Online Safety Act 2023 c. 50; Ofcom OSA Codes of Practice; UK ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Online Safety & Child Protection Policy outlining compliance with Ofcom duties and ICO Age-Appropriate Design principles.
- **Missing Documentation:**
  No documentation exists detailing how to conduct a Data Protection Impact Assessment (DPIA) for child-accessible services or how to integrate Ofcom-approved age assurance vendors.
- **Missing Code:**
  The codebase templates lack default configuration scripts to turn off geolocation tracking, turn off profiling, and set maximum privacy settings for UK child users.
- **Missing Disclosure:**
  UI templates do not include UK-specific age verification notices, child safety warnings, or reporting mechanism disclosures for harmful content.
- **Missing Logging:**
  There are no backend logging schemas to capture age assurance verification outcomes, CSEA report filings to the NCA portal, or illegal content moderation actions under UK law.
- **Missing Testing:**
  Automated tests do not verify that geolocation, profiling, and push notifications are disabled by default for UK accounts identified as minors.
- **Missing Evidence:**
  The playbook lacks template Ofcom Children's Risk Assessments, ICO DPIA worksheets, or evidence of highly effective age assurance testing.
- **Missing Audit Trail:**
  An unalterable audit trail documenting illegal content reports, Ofcom compliance filings, and age assurance verification logs is absent.

### 14.3 Remediation and Action Plan
1. Publish a UK Online Safety Act & ICO Children's Code Guide with template DPIA and risk assessment documentation.
2. Develop code hooks for applying high-privacy default profiles (geolocation off, profiling off) for UK minor users.
3. Build backend logging utilities for tracking illegal content notices and NCA CSEA report filings.
4. Create CI test suites verifying that minor accounts enforce restricted data processing defaults.

---

## 15. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Act 2021 and the Online Safety Amendment (Social Media Minimum Age) Act 2024 mandate that age-restricted social media platforms take reasonable steps to prevent under-16s from holding accounts. Enforced by eSafety, platforms must deploy robust age-assurance methods (waterfall methodology), ringfence and immediately destroy age-assurance data after verification, comply with App Distribution Services Industry Codes (Schedule 7), and provide rapid takedown mechanisms for cyberbullying and non-consensual intimate images.

Official Citations: Australia Online Safety Act 2021; Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Age-Restricted Social Media & Online Safety Policy covering eSafety compliance and under-16 account restrictions.
- **Missing Documentation:**
  Developer guides fail to detail eSafety's waterfall age assurance expectations or Australia App Distribution Services Code requirements.
- **Missing Code:**
  Codebase templates do not contain logic for executing age assurance checks for Australian users or routines to automatically purge age-verification artifacts immediately post-verification.
- **Missing Disclosure:**
  In-app onboarding does not provide mandatory Australian age-gating disclosures or eSafety reporting channel notices.
- **Missing Logging:**
  There are no backend logging schemas to record age verification completion flags (without storing raw identity documents) or eSafety takedown notice executions.
- **Missing Testing:**
  Automated tests do not verify that Australian users under 16 are blocked from creating social media accounts or that raw age data is deleted post-check.
- **Missing Evidence:**
  The playbook lacks template eSafety Risk Assessments, age assurance verification audit certificates, or data destruction logs.
- **Missing Audit Trail:**
  An immutable audit trail documenting account restriction enforcement, eSafety takedown requests, and age-assurance data purge events is missing.

### 15.3 Remediation and Action Plan
1. Create an Australian Online Safety Compliance Guide and eSafety Risk Assessment template.
2. Build code modules for integrating age-assurance methods and enforcing immediate raw verification data deletion.
3. Design backend log schemas for tracking eSafety compliance events while respecting data ringfencing mandates.
4. Add automated integration tests verifying under-16 account blocks for Australian user registrations.

---

## 16. Brazil Digital ECA (Law 15,211/2025) & LGPD

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, regulated by Decreto 12,880/2026) and the Lei Geral de Proteção de Dados (LGPD) establish strict age verification and child protection rules. Self-declaration checkboxes are explicitly prohibited. Apps must utilize ANPD-approved age-verification methods (document verification, facial estimation, CPF database check), obtain parental/guardian authorization, display age ratings prior to download, and strictly ringfence child data against commercial monetization.

Official Citations: Law 15,211/2025 (Digital ECA); Decreto n. 12.880 (18 March 2026); Lei 13.709/2018 (LGPD).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Brazil Digital ECA & LGPD Child Privacy Policy detailing verified age assurance and guardian consent mechanisms.
- **Missing Documentation:**
  Developer documentation does not explain how to integrate Brazilian CPF validation or ANPD-compliant facial estimation APIs.
- **Missing Code:**
  Codebase templates do not include logic to interface with Google Play Age Signals API or Apple's Declared Age Range API for Brazilian users.
- **Missing Disclosure:**
  Onboarding UI templates lack mandatory Brazilian disclosures regarding age verification requirements and guardian consent procedures.
- **Missing Logging:**
  No backend schema exists to log guardian consent receipts, CPF verification status, or ANPD compliance audit events.
- **Missing Testing:**
  Automated tests do not confirm that self-declaration alone fails age verification for Brazilian user sessions or that minor profiles block ad tracking.
- **Missing Evidence:**
  The playbook lacks template ANPD Compliance Reports, CPF validation audit logs, or guardian authorization record sheets.
- **Missing Audit Trail:**
  An unalterable audit trail recording Brazilian age verification attempts, guardian consents, and LGPD data subject requests is absent.

### 16.3 Remediation and Action Plan
1. Draft a Brazil Digital ECA Compliance Guide detailing LGPD child data rules and ANPD age-assurance methods.
2. Implement cross-platform native code wrappers for Google Play Age Signals API and Apple Declared Age Range API targeting Brazilian users.
3. Design backend logging structures for recording guardian consent flags without storing unauthorized minor personal data.
4. Add automated test suites verifying that age verification blocks under-18 access without valid guardian signals.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA 2023) and DPDP Rules 2025 (notified 13 November 2025) impose comprehensive data protection requirements. Everyone under 18 is classified as a child. Mandatory obligations include clear consent notices in 22 official Indian languages, verifiable parental consent through government-backed mechanisms (e.g., DigiLocker), a total ban on behavioral tracking and targeted advertising to children, and registration of Consent Managers.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template India DPDPA Data Protection Policy covering verifiable parental consent, multi-language consent notices, and child data restrictions.
- **Missing Documentation:**
  No documentation exists detailing integration with Indian Consent Managers or DigiLocker-based verifiable parental consent flows.
- **Missing Code:**
  Codebase templates lack multi-lingual consent notice renderers (supporting Eighth Schedule languages) or logic to disable tracking for under-18 Indian users.
- **Missing Disclosure:**
  Consent screens do not present itemized disclosures in specified languages detailing exact personal data items collected and specified processing purposes.
- **Missing Logging:**
  There are no backend database schemas to log DPDPA consent notices presented, consent withdrawal requests, or Data Principal grievance filings.
- **Missing Testing:**
  Automated tests do not verify that ad targeting and tracking SDKs are completely suppressed when the user location is India and age is under 18.
- **Missing Evidence:**
  The playbook lacks template DPDPA Data Protection Impact Assessments, Consent Manager integration certificates, or grievance officer appointment notices.
- **Missing Audit Trail:**
  An immutable audit trail documenting consent lifecycle events, parental consent verifications, and Data Principal rights fulfillment logs is missing.

### 17.3 Remediation Action Plan
1. Publish an India DPDPA Compliance Guide detailing multi-lingual consent notices and child data prohibitions.
2. Create reusable UI components for multi-language consent presentation and DigiLocker VPC verification.
3. Build backend event logging for DPDPA consent records, withdrawals, and grievance tracking.
4. Add automated CI tests verifying complete tracking suppression for under-18 accounts in India.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
The Singapore Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services require robust personal data protection, mandatory breach notification within 3 days for significant harm, appointment of a Data Protection Officer (DPO), and app store / platform age-assurance measures to prevent under-18s from accessing age-inappropriate content.

Official Citations: Singapore Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety (2025/2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Singapore PDPA Compliance Policy and a formal 3-Day Data Breach Notification Protocol.
- **Missing Documentation:**
  Developer guides do not detail IMDA age assurance expectations or PDPA business contact information disclosure rules.
- **Missing Code:**
  Codebase templates lack age-gating components for Singapore users or automated data breach notification dispatch helpers.
- **Missing Disclosure:**
  In-app disclosures do not specify DPO business contact details or clear descriptions of personal data processing purposes as required by PDPA.
- **Missing Logging:**
  No backend logging schema exists to record data subject access/correction requests or data breach assessment logs within the 3-day notification window.
- **Missing Testing:**
  Automated tests do not verify that 18-plus content downloads/access are blocked for unverified Singapore user sessions.
- **Missing Evidence:**
  The playbook lacks template PDPA Data Protection Impact Assessments, DPO appointment letters, or IMDA compliance audit records.
- **Missing Audit Trail:**
  An unalterable audit trail recording PDPA consent capture, data access logs, and breach investigation timelines is absent.

### 18.3 Remediation and Action Plan
1. Create a Singapore PDPA & IMDA Compliance Guide featuring a 3-Day Breach Notification Protocol.
2. Build code helpers for displaying DPO contact details and executing Singapore regional age assurance checks.
3. Design backend log schemas for data breach evaluation and PDPA consent management.
4. Integrate automated test suites verifying 18-plus access restrictions for Singapore accounts.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
The South Korea Telecommunications Business Act mandates alternative in-app payment processing for mobile applications, prohibiting app store operators from forcing proprietary billing systems. Additionally, the amended Personal Information Protection Act (PIPA Act No. 21445, effective September 2026) imposes strict CEO/CPO accountability, heavy punitive surcharges (up to 3% of total turnover), rigid cross-border transfer disclosures, and explicit consent rules for processing under-14 data.

Official Citations: South Korea Telecommunications Business Act Article 22-9; PIPA Amendment Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a South Korea Alternative In-App Payments & PIPA Compliance Policy detailing legal billing options and CEO/CPO privacy duties.
- **Missing Documentation:**
  Developer documentation fails to specify Apple's Korea-specific `SKExternalPurchase` entitlement requirements, approved Korean payment gateways (KCP, Toss, Inicis, NICE), or reporting workflows.
- **Missing Code:**
  Codebase templates do not contain Korea-specific StoreKit/Play billing logic, native pre-payment modal disclosure sheets, or monthly sales reporting exporters (26% commission handling).
- **Missing Disclosure:**
  In-app payment flows lack mandatory Korean disclosures informing users about alternative payment terms, refund policies, and store protection waivers.
- **Missing Logging:**
  No backend database schema exists to log alternative billing transactions, monthly sales summaries, or PIPA cross-border data transfer logs.
- **Missing Testing:**
  Automated tests do not verify that alternative billing sheets display exclusively for Korean binaries/sessions and properly log required transaction metadata.
- **Missing Evidence:**
  The playbook lacks template KCC alternative payment filings, Apple Korea entitlement approval letters, or PIPA CPO designation records.
- **Missing Audit Trail:**
  An immutable audit trail documenting alternative billing transactions, monthly commission reporting logs, and PIPA consent management is missing.

### 19.3 Remediation Action Plan
1. Draft a South Korea In-App Payment & PIPA Compliance Guide with step-by-step StoreKit external entitlement runbooks.
2. Build native code modules for displaying Korea alternative payment modal sheets and formatting approved gateway payloads.
3. Implement backend transaction logging and automated monthly sales export scripts for gatekeeper reporting.
4. Add automated integration tests verifying Korea payment flow logic and pre-checkout disclosures.

---

## 20. China Mobile App Filing (MIIT) & CAC AI/Minors Rules

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP filing extension) for all mobile applications operating in China. Foreign developers must partner with a local Chinese entity. Furthermore, CAC regulations (Interim Measures for AI Anthropomorphic Interactive Services CAC Order No. 21, Minors Online Content Rules) strictly regulate AI chat/companion services, require automatic "Minors Mode", mandate real-name identity verification, and require personal information compliance audits every two years.

Official Citations: MIIT Mobile App Filing Rules (2023/2024); CAC Order No. 21 (2026); PIPL (Personal Information Protection Law).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a China Mobile App Filing & CAC Compliance Policy covering local entity partnerships, PIPL data localization, and AI anthropomorphic service rules.
- **Missing Documentation:**
  Developer guides fail to detail MIIT app filing submission steps, Banhao game licensing rules, or CAC real-name identity verification integration.
- **Missing Code:**
  Codebase templates do not contain automated "Minors Mode" triggers, real-name authentication UI flows, or CAC synthetic content labeling markers.
- **Missing Disclosure:**
  UI templates lack mandatory MIIT filing number disclosures in app footers/settings or CAC AI interaction disclosures.
- **Missing Logging:**
  No backend schema exists to log real-name verification checks, Minors Mode session durations, or PIPL cross-border data transfer security assessments.
- **Missing Testing:**
  Automated tests do not confirm that Chinese accounts without real-name verification are blocked from AI chat features or forced into Minors Mode.
- **Missing Evidence:**
  The playbook lacks template MIIT Filing Certificates, CAC AI Security Assessments, or PIPL Compliance Audit reports.
- **Missing Audit Trail:**
  An unalterable audit trail documenting real-name verification logs, Minors Mode toggles, and PIPL biennial audit records is absent.

### 20.3 Remediation and Action Plan
1. Create a China App Filing & CAC Regulations Guide detailing MIIT filing requirements and PIPL data localization mandates.
2. Build UI code templates for rendering MIIT filing numbers, real-name authentication forms, and automatic Minors Mode switching.
3. Design backend log schemas for real-name verification status and CAC AI content moderation logs.
4. Integrate automated CI tests verifying that Chinese regional sessions enforce real-name gating and Minors Mode restrictions.

---

## 21. Consolidated Gap Classification Matrix

The classification matrix below provides an honest, comprehensive evaluation of the playbook across all twenty audited global and regional regulatory frameworks.
- **Covered:** The repository provides full policy, documentation, code, disclosure, logging, testing, evidence, or audit trail implementation.
- **Partial:** The framework is cited with dated sources and general guidance, but actionable developer implementation tools or code templates are incomplete.
- **Missing:** The playbook carries no coverage or implementation for this specific category.
- **N/A:** The category is not applicable to the specific regulatory mandate (e.g., code execution for human-facing training policies).

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. Digital Markets Act (DMA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. Digital Services Act (DSA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act (EAA)** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA & Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA/CPRA/CPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA & Texas CUBI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act & ICO Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA & LGPD** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & DPDP Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Implementation Roadmap

This comprehensive gap analysis demonstrates that while the playbook is exceptionally strong on platform-specific app store rejection rules (Apple App Store Guidelines and Google Play Content Policies), significant implementation gaps exist regarding live legal compliance frameworks across global jurisdictions.

To transform this repository into a complete, end-to-end regulatory compliance engine, implementation must proceed in four prioritized phases:

1. **Phase 1: Immediate Gap Elimination (GPSR & EAA)**
   - Add full GPSR detection rules, metadata schemas, and product detail page code templates.
   - Wire `scripts/accessibility-audit.py` into mandatory CI pre-submission checks to satisfy EAA / EN 301 549 mandates before June 2025.

2. **Phase 2: High-Priority 2026 Deadlines (EU AI Act, ASAA, e-Evidence)**
   - Implement machine-readable watermarking (C2PA) and in-app AI interaction disclosures for EU AI Act Article 50 (effective August 2026).
   - Add native Apple Declared Age Range and Google Play Age Signals code integrations for US state ASAAs and Brazil Digital ECA.
   - Develop secure 8-hour emergency user data extraction scripts for EU e-Evidence Package orders (effective August 2026).

3. **Phase 3: Multi-Jurisdictional Privacy & Age Assurance (COPPA, CCPA, DPDPA, UK OSA)**
   - Build reusable UI consent components for multi-lingual consent notices (India DPDPA), BIPA written releases, and ROSCA one-click cancellation.
   - Implement backend logging schemas for verifiable parental consent, consent withdrawals, and automated raw age-verification data deletion.

4. **Phase 4: Alternative Distribution & Marketplace Compliance (DMA, DSA, South Korea TBA, China Filing)**
   - Build conditional cross-platform payment routers for EEA (DMA) and South Korea alternative billing modalities.
   - Create DSA trader identity profile components and illegal content notice-and-action logging workflows.
   - Provide step-by-step runbooks for China MIIT app filing and local entity pairing.

---

## 23. Sources

Every regulatory framework cited within this report is anchored directly in official, Priority 1 primary legal publications:

- EU General Product Safety Regulation (GPSR): [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services Directive: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act (DMA): [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act (DSA): [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/dir/2022/2065/oj)
- European Accessibility Act (EAA): [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US FTC Children's Online Privacy Protection Rule (COPPA): [90 FR 16918](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US Utah App Store Accountability Act: [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html)
- California Privacy Protection Agency (CPPA): [CPPA Regulations](https://cppa.ca.gov/regulations/ccpa_updates.html)
- California Legislature: [California Legislative Information](https://leginfo.legislature.ca.gov)
- Illinois Biometric Information Privacy Act (BIPA): [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US FTC Negative Option Rule ANPRM: [FTC ANPRM Press Release](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option)
- UK Online Safety Act 2023: [UK Legislation c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents/enacted)
- Australia Social Media Minimum Age Act 2024: [Federal Register of Legislation C2024A00113](https://www.legislation.gov.au/C2024A00113/asmade/text)
- Brazil Digital ECA Regulation: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India Gazette (DPDP Rules 2025): [E-Gazette India](https://egazette.gov.in)
- Singapore Statutes Online (PDPA): [Singapore SSO PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea National Law Information Center: [Korea Law Information Center](https://law.go.kr)
- China Ministry of Industry and Information Technology: [MIIT China](https://www.miit.gov.cn/)
