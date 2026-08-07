# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major regulations that bind app developers shipping into global markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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

Scope matters here, and it is easy to overstate. The withdrawal button obligation in this Directive attaches to distance financial services contracts, not to every consumer subscription. A general withdrawal button across all distance contracts has been proposed at EU level but is not yet law. Treat it as binding today if your app sells insurance, credit, payment, investment, or another financial service into the EU, and as a strong design default otherwise, since Apple already requires an easy in-app cancellation path regardless.

The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

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
  Not applicable, since Article 4 binds people rather than code. A small helper that checks whether a literacy log exists and is current would still be useful.
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
The Digital Markets Act (DMA), Regulation (EU) 2022/1925, applies strictly to designated gatekeepers and regulates the core distribution of applications within the EU. It enforces anti-steering prohibitions, alternative distribution channels, and external purchase structures. Under the DMA, developers can utilize external links, browser engines, alternative marketplaces, and contactless NFC implementations in the EEA.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template policy outlining the circumstances under which a developer should opt-in to Apple's Alternative Terms Addendum or alternative marketplaces.
- **Missing Documentation:**
  There is no step-by-step documentation detailing the financial trade-offs of the Core Technology Fee (CTF) or Core Technology Commission (CTC) for high-volume apps.
- **Missing Code:**
  The guard rules do not programmatically search the codebase for missing or incorrect StoreKit external purchase entitlements (`com.apple.developer.storekit.external-purchase-link`).
- **Missing Disclosure:**
  Billing and payment mockups do not provide the UI components or logic to display system-required external purchase warning modals before routing a user outside the app ecosystem.
- **Missing Logging:**
  No database schemas, server scripts, or mock schedulers are available to handle the collection, format verification, and monthly transmission of external purchase reports.
- **Missing Testing:**
  The repository has no automated tests verifying that the external billing links are correctly region-gated or that billing flows do not co-mingle Apple's IAP and external billing options.
- **Missing Evidence:**
  The playbook is missing template copies of the signed StoreKit External Purchase Link Entitlement Addendum.
- **Missing Audit Trail:**
  No immutable logs are defined to record historical alternative distribution configurations, notarization records, or DMA monthly compliance reports.

### 7.3 Remediation and Action Plan
1. Create a detailed DMA Integration Guide detailing fee thresholds and reporting requirements.
2. Implement automated checks within the compliance guard to identify missing region gates for external billing features.
3. Provide code templates that properly interface with the `ExternalPurchaseCustomLink` system API.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes comprehensive obligations for online platforms and intermediaries, specifically targeting transparency, consumer protection, and minor safety. Articles 30 and 31 mandate that marketplaces verify and display trader contact details (including address, phone number, and email) on app store listings.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate template is provided to guide developers in declaring themselves "traders" versus "non-traders" based on their commercial operations.
- **Missing Documentation:**
  Lacks operational guidelines on how to navigate the App Store Connect and Google Play Console DSA trader verification processes.
- **Missing Code:**
  No scripts or detection rules exist in the repository to warn developers when their release package is at risk of immediate EU store removal due to missing DSA status.
- **Missing Disclosure:**
  The repository metadata files do not provide structural layouts showing verified developer address, phone, and email information.
- **Missing Logging:**
  No backend databases or logs are defined to track corporate verification records, D-U-N-S registration matching, or 2FA verification steps.
- **Missing Testing:**
  There are no pre-submit validation scripts to test the availability and correctness of the published trader details prior to a release.
- **Missing Evidence:**
  Lacks verified templates of DSA-compliant corporate documentation, self-certification forms, or D-U-N-S verification receipts.
- **Missing Audit Trail:**
  There is no logging system tracking historical changes in trader declarations, verified addresses, or store verification events.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Declaration checklist in the pre-submission guide.
2. Build static analyzer checks to flag missing contact URLs or missing company verification details.
3. Develop templates for digital trader self-certifications.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, mandates that essential digital products and services, including mobile applications and websites, satisfy strict accessibility standards (EN 301 549 / WCAG 2.1 AA) beginning 28 June 2025. It targets e-commerce, banking, media, and transport apps.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy is provided to help organizations structure accessibility goals, evaluate microenterprise exemptions, or establish WCAG compliance.
- **Missing Documentation:**
  While general checklist items exist, the repository lacks detailed documentation on the specific EN 301 549 Chapter 11 rules that apply to non-web software.
- **Missing Code:**
  The pre-submission compliance guard does not incorporate the automated accessibility auditing scripts (`scripts/accessibility-audit.py`), allowing accessibility regressions to pass without blocking.
- **Missing Disclosure:**
  There are no mockups, metadata models, or document templates for an official, public-facing Accessibility Statement.
- **Missing Logging:**
  The codebase lacks schemas or data endpoints designed to log user-reported accessibility defects or feedback.
- **Missing Testing:**
  No automated integration tests are written to verify contrast ratios, element focus sequences, or Dynamic Type responsive behavior under runtime simulation.
- **Missing Evidence:**
  Lacks templates for Voluntary Product Accessibility Templates (VPAT) or EAA self-declaration conformity records.
- **Missing Audit Trail:**
  No unalterable logs exist to track historical accessibility audits, user-remediation timelines, or code modifications addressing accessibility feedback.

### 9.3 Remediation and Action Plan
1. Fully integrate `scripts/accessibility-audit.py` as a blocking gate within the main compliance guard.
2. Design and publish an EAA-compliant Accessibility Statement markdown template.
3. Add automated contrast-checking algorithms within the static asset verification flow.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) protects the privacy of children under 13 by restricting the collection of personal information by child-directed services. The 2025/2026 amended COPPA Rule expands personal information to include biometric identifiers, imposes strict data-retention schedules, and requires a written information security program.

Official Citation: 16 CFR Part 312 - Children's Online Privacy Protection Rule.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a comprehensive template policy for managing minor accounts under the 2025/2026 amended COPPA Rule, especially regarding biometric and government identifiers.
- **Missing Documentation:**
  The checklists do not specify developer runbooks for implementing new verifiable parental consent methods, such as knowledge-based authentication or facial matching to photo ID.
- **Missing Code:**
  The mock clients do not contain functional blocks for the separate opt-in flow for third-party disclosure/targeted ads, nor do they support dynamic age gating that blocks children under 13.
- **Missing Disclosure:**
  In-app onboarding mockups lack conspicuous disclosures outlining exactly what child PII is collected, how it is used, and the parent's right to review or delete it.
- **Missing Logging:**
  No backend schemas designed to handle the secure storage of parental consent flags, parent contact info, or the immediate purging of raw verification inputs.
- **Missing Testing:**
  Test suites do not include automated tests simulating COPPA-compliant age-gate blocks, consent revocations, or data-sharing opt-out verification.
- **Missing Evidence:**
  Lacks concrete templates for written information-security programs (312.8) or written data retention policies (312.10) for child-directed apps.
- **Missing Audit Trail:**
  No immutable administrative log to track parental consent events, consent revocations (such as the `RESCIND_CONSENT` server notification), or annual risk assessment completions.

### 10.3 Remediation and Action Plan
1. Formulate a comprehensive COPPA Compliance Guide detailing biometric tracking limits and data security programs.
2. Create reusable, secure age-gate components within the onboarding templates.
3. Build database utility functions to purge parental consent validation data immediately after verification.

---

## 11. California Privacy (CCPA/CPRA/CPPA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), regulates the collection and processing of California residents' personal data. The California Privacy Protection Agency (CPPA) 2026 regulations enforce compliance with Global Privacy Control (GPC), opt-out mechanisms, and cybersecurity audits.

Official Citation: California Civil Code Section 1798.100 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template exists for a comprehensive California privacy policy, and there are no guidelines for the 2026 CPPA automated-decision-making rules.
- **Missing Documentation:**
  The playbook lacks detailed developer documentation explaining how to process and handle Global Privacy Control (GPC) opt-out headers.
- **Missing Code:**
  No middleware or client-side code is provided to query, detect, and propagate GPC (`Sec-GPC`) signal status to tracking and advertising SDKs.
- **Missing Disclosure:**
  Onboarding templates and preference screens do not include required user controls like "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information".
- **Missing Logging:**
  There are no backend database models or logging modules to record the receipt, status, and completion of consumer privacy rights requests within 45 days.
- **Missing Testing:**
  No automated integration tests exist to verify that setting a GPC header dynamically suppresses tracking and analytic network requests.
- **Missing Evidence:**
  Lacks templates for service provider agreements, CPPA cybersecurity audit self-evaluations, or data processing assessments.
- **Missing Audit Trail:**
  No immutable log tracks when privacy requests were received, how they were verified, and the exact date deletion or correction was executed.

### 11.3 Remediation and Action Plan
1. Provide a CCPA-compliant privacy policy markdown template.
2. Develop a GPC header middleware interceptor for web and API requests.
3. Draft a CPPA-aligned service provider agreement template in the assets folder.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA) mandates strict guidelines for companies collecting biometric identifiers (fingerprints, retina scans, facial templates) from Illinois residents. It requires explicit written consent, public retention schedules, and strictly prohibits the sale or monetization of biometric data.

Official Citation: 740 ILCS 14/1 - Biometric Information Privacy Act.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate biometric data policy template is provided to govern the collection, retention, and secure disposal of biometric templates.
- **Missing Documentation:**
  The repository lacks developer guidelines addressing the Illinois SB 2979 amendment (making repeated scans a single violation) or Texas CUBI requirements.
- **Missing Code:**
  No code blocks demonstrate BIPA-compliant pre-capture biometric consent gates or native face/fingerprint collection interception.
- **Missing Disclosure:**
  The mockup files contain no onboarding or settings screens featuring biometric privacy notices or disclosure sheets.
- **Missing Logging:**
  No database schemas are defined to log user-signed biometric releases or schedules to enforce maximum 3-year data destruction limits.
- **Missing Testing:**
  No integration tests ensure that biometric scanning SDKs are locked and cannot initialize until a verified consent flag is recorded.
- **Missing Evidence:**
  The repository lacks physical templates of biometric release agreements or public-facing biometric retention schedules.
- **Missing Audit Trail:**
  There is no unalterable administrative log tracking when biometric systems were updated, when user consent was given, or when biometric databases were purged.

### 12.3 Remediation and Action Plan
1. Publish a standard Biometric Information Consent and Release agreement template.
2. Develop a UI component template that gates biometric SDK initialization behind a required toggle.
3. Build automatic DB triggers to enforce the 3-year data retention and destruction rules.

---

## 13. US Subscription Cancellation (Negative Option / ROSCA)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA) and state-level negative-option statutes (California, New York, Massachusetts) regulate subscription billing, auto-renewals, and trials. They mandate that subscription cancellation must be direct, frictionless, and at least as simple as the sign-up process.

Official Citations: 15 U.S.C. Section 8401 et seq. (ROSCA), California Business and Professions Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template policy exists for managing customer-facing subscription cancellation flows billed outside of the platform's native billing system.
- **Missing Documentation:**
  The checklists fail to outline UX design rules for ensuring cancellation paths are as simple as signing up (preventing forced phone calls or letters).
- **Missing Code:**
  The monetization templates contain no self-service cancellation paths, in-app cancellation buttons, or web portal cancellation shortcuts.
- **Missing Disclosure:**
  Paywall templates do not provide prominent disclosures of negative option terms, auto-renewal schedules, and refund policies before purchase.
- **Missing Logging:**
  No database structures or logs exist to record cancellation requests, user-selected reasons, or cancellation processing times.
- **Missing Testing:**
  No automated UI or end-to-end tests exist to verify that a user can successfully cancellation without administrative interventions.
- **Missing Evidence:**
  The playbook lacks templates for post-purchase confirmation emails, cancellation receipts, or user billing records.
- **Missing Audit Trail:**
  No immutable log tracks changes to negative option pricing, promotional trials, or cancellation workflow edits.

### 13.3 Remediation and Action Plan
1. Draft a ROSCA-compliant subscription cancellation policy guide.
2. Incorporate a frictionless, self-service cancellation modal component within account settings mockups.
3. Build logging modules to record exact user cancellation actions and feedback.

---

## 14. UK Online Safety Act

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enforced by Ofcom, establishes strict obligations for services that allow user-generated content or search functionality. It requires robust age-assurance mechanisms, content moderation protocols, and minor protection systems to prevent exposure to illegal or harmful material.

Official Citation: Online Safety Act 2023 (c. 30).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no formal child safety or harmful content prevention policy aligned with Ofcom's Online Safety Act expectations.
- **Missing Documentation:**
  Lacks developer guides on implementing Highly Effective Age Assurance (e.g., facial age estimation, digital ID) as opposed to self-declaration.
- **Missing Code:**
  The codebase does not implement client-side integration hooks for biometric or government database checks, nor does it provide a way to verify age-assurance data destruction.
- **Missing Disclosure:**
  In-app screens do not disclose Ofcom-mandated safety practices, age-gating rules, or parent-facing controls.
- **Missing Logging:**
  There are no database structures or logs for recording content moderation actions, user-generated report volumes, or age estimation successes.
- **Missing Testing:**
  Lacks automated test suites to simulate a minor attempting to bypass age-estimation gates or accessing restricted areas.
- **Missing Evidence:**
  No templates for UK Children's Code or Online Safety Act Data Protection Impact Assessments (DPIA) are available.
- **Missing Audit Trail:**
  No unalterable log of content moderation decisions, age assurance policy updates, or compliance audits under Ofcom supervision.

### 14.3 Remediation and Action Plan
1. Create an Online Safety Act Compliance runbook in the references folder.
2. Build mock integration points for facial estimation API vendors.
3. Publish a sample DPIA markdown template.

---

## 15. Australia Online Safety (Minimum Age)

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 enforces an age limit of 16 for social media platform access in Australia. It requires age-assurance verification methods that go beyond self-declaration, and mandates that verification data be ringfenced and destroyed immediately after use.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate minor protection policy for Australian users, specifically covering the Online Safety Amendment (Social Media Minimum Age) Act 2024.
- **Missing Documentation:**
  Lacks step-by-step documentation on the expected waterfall of age-assurance methods or compliance with Australian eSafety guidelines.
- **Missing Code:**
  Code templates do not provide a mechanism to ringfence age-verification data or automatically delete it immediately after verification.
- **Missing Disclosure:**
  Onboarding and account creation mockups do not display disclosures regarding the under-16 social media ban or parental consent requirements in Australia.
- **Missing Logging:**
  No secure logging structures to capture age assurance events without persistently storing or leaking personal identification documents.
- **Missing Testing:**
  Lacks automated integration tests to verify that an under-16 account is blocked from signing up on Australian storefronts.
- **Missing Evidence:**
  No template documents for eSafety compliance reviews, age verification vendor contracts, or minor data deletion records.
- **Missing Audit Trail:**
  No administrative log of changes to Australian age-assurance systems, vendor integrations, or eSafety correspondence.

### 15.3 Remediation and Action Plan
1. Draft a comprehensive Social Media Minimum Age policy template.
2. Write backend code templates displaying how to instantly flush ID upload buffers post-verification.
3. Build tests that assert age verification gates are active for Australian locales.

---

## 16. Brazil Digital ECA

### 16.1 Regulatory Overview and Background
Brazil's Law 15,211/2025 (Digital ECA), enforceable from 17 March 2026, requires robust age-verification methods (including document check, facial age estimation, or CPF checks) for mobile apps and services. It prohibits simple self-declaration checkboxes for gating underage access.

Official Citation: Lei No 15.211/2025 (Estatuto da Crianca e do Adolescente Digital).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a dedicated policy template for Brazilian minor protection under Law 15,211/2025 (Digital ECA) and LGPD requirements.
- **Missing Documentation:**
  No developer-focused instructions on utilizing Google Play's Age Signals API or Apple's Declared Age Range API for Brazil-specific storefronts.
- **Missing Code:**
  Codebase does not feature runtime client-side code integration for CPF database checks, document verification, or facial age estimation in Brazil.
- **Missing Disclosure:**
  Onboarding flows lack Portuguese-language disclosures explaining that age-verification data is requested to comply with Brazil's Digital ECA.
- **Missing Logging:**
  No secure backend logging to record Portuguese consent agreements, consent revocations, or the instant purging of Brazilian ID data.
- **Missing Testing:**
  Lacks automated unit or UI tests validating that Brazilian accounts rate-locked (e.g. 18-plus or loot-box apps auto-rated 18-plus) are barred from download without verified age signals.
- **Missing Evidence:**
  No templates of compliance agreements with Brazilian verification providers, ANPD audit files, or Portuguese-language parental consent records.
- **Missing Audit Trail:**
  No immutable, persistent log tracking changes to Brazilian age gates, verification API versions, or CPF checking mechanisms.

### 16.3 Remediation and Action Plan
1. Author a Brazil Digital ECA compliance implementation manual.
2. Add detection rules in the pre-submission guard for the Play Age Signals API.
3. Build and publish a Brazilian parental consent markdown agreement template.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
The India Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025, regulates personal data processing in India. It mandates verifiable parental consent through government-backed systems (such as DigiLocker) before processing data of minors under 18, and prohibits child-targeted behavioral tracking and ads.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Indian personal data protection policy template aligned with the DPDP Act 2023 and DPDP Rules 2025.
- **Missing Documentation:**
  Lacks guides on India-specific children rules (under 18 is a child) or using government-backed verification systems like DigiLocker.
- **Missing Code:**
  Mock interfaces lack programmatic gates to block behavioral tracking and targeted advertising for accounts detected as under 18 in India.
- **Missing Disclosure:**
  Onboarding screens do not display bilingual consent notices or summaries of rights (e.g., in English and Hindi) as expected under DPDP consent rules.
- **Missing Logging:**
  No database schemas to record DigiLocker verification tokens, bilingual consent logs, or data protection officer appointment records.
- **Missing Testing:**
  Lacks test suites to simulate Indian minor accounts and ensure targeted ad-tracking scripts are completely bypassed.
- **Missing Evidence:**
  The repository is missing templates of DPDPA-compliant Consent Notices, Data Principal rights request forms, or Data Protection Officer reports.
- **Missing Audit Trail:**
  No immutable administrative trail to track the appointment of Indian consent managers, consent revocations, or data breach notifications to the DPBI.

### 17.3 Remediation and Action Plan
1. Create a bilingual (English/Hindi) DPDPA Consent Notice template.
2. Develop code examples gating third-party ad script loading for users under 18 in India.
3. Publish draft formats for Data Principal rights request handling.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
The Singapore Personal Data Protection Act (PDPA) establishes the baseline data privacy requirements, and the IMDA Code of Practice for Online Safety requires app distribution platforms to deploy age assurance measures starting 1 April 2026. This restricts under-18s from downloading age-inappropriate apps.

Official Citations: Personal Data Protection Act 2012, IMDA Code of Practice for Online Safety (2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a formal Singapore PDPA compliance policy, including rules for appointing a Data Protection Officer (DPO) and reporting breaches within 3 days.
- **Missing Documentation:**
  No developer checklists on meeting the IMDA Code of Practice for Online Safety (effective 1 April 2026), including stopping under-18s from downloading age-inappropriate apps.
- **Missing Code:**
  Mocks do not integrate credit-card check methods or age estimation SDKs for Singapore App Store and Google Play storefronts.
- **Missing Disclosure:**
  Onboarding pages lack disclosures regarding DPO contact details or IMDA-mandated age screening.
- **Missing Logging:**
  No backend logging of Singapore data access requests, consent revocations, or 3-day breach notification trackers.
- **Missing Testing:**
  No automated tests verifying that Singaporean IP addresses or storefronts are dynamically served the required age-gated experience.
- **Missing Evidence:**
  Missing template DPO appointment documents, IMDA compliance self-assessments, or 3-day breach notification templates.
- **Missing Audit Trail:**
  No unalterable log to record historical PDPA policy updates, DPO training records, or internal data breach incident reviews.

### 18.3 Remediation and Action Plan
1. Author a Singapore PDPA compliant corporate privacy program template.
2. Integrate a mock DPO registration and notification log in the references tree.
3. Build automated scripts verifying Singapore storefront region gating.

---

## 19. South Korea Telecommunications Business Act (Alternative Billing)

### 19.1 Regulatory Overview and Background
The South Korea Telecommunications Business Act mandates that app store operators permit alternative in-app payment systems. Developers can distribute a Korea-specific binary utilizing approved payment providers (KCP, Inicis, Toss, NICE) with a reduced platform commission of 26 percent, subject to strict monthly reporting requirements.

Official Citation: Telecommunications Business Act, South Korea.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate compliance policy template for alternative in-app billing on South Korean storefronts.
- **Missing Documentation:**
  No developer runbooks for configuring Korea-specific StoreKit/Play Billing entitlements, approved payment gateway integrations, or monthly sales reports.
- **Missing Code:**
  Mock codebase lacks a separate South Korea binary implementation, approved gateway integration (KCP, Inicis, Toss, NICE), or the mandatory system-provided billing disclosure modal.
- **Missing Disclosure:**
  billing user interfaces do not display the South Korean disclosure notice stating that Family Sharing, Ask-to-Buy, and Apple billing support are unavailable.
- **Missing Logging:**
  No server-side schemas or schedulers to format, batch, and transmit monthly sales reports to Apple within 15 days of Apple's fiscal month end.
- **Missing Testing:**
  No automated UI or integration tests validating that South Korean accounts are shown the correct, approved payment selector and are blocked from co-mingling standard IAP.
- **Missing Evidence:**
  Lacks signed copies of South Korea Alternative Billing Addendums or proof of contractual relationships with approved Korean payment gateways.
- **Missing Audit Trail:**
  No unalterable audit log tracking monthly sales reports, K-IAP entitlement changes, or payment gateway settlement history.

### 19.3 Remediation and Action Plan
1. Create a step-by-step South Korea billing integration guide.
2. Implement static analyzer rules checking for South Korean alternative purchase entitlements (`com.apple.developer.storekit.external-purchase`).
3. Develop templates for the required system-level South Korean billing disclosure modals.

---

## 20. China App Filing (MIIT)

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) in China mandates that all mobile applications must complete a Mobile App Filing (ICP filing extension) before distribution on Chinese app stores. Foreign developers must partner with local Chinese entities to obtain filing credentials, content moderation approval, and game licenses (Banhao).

Official Citations: Provisions on the Administration of Mobile Internet Application Information Services (MIIT).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template policies for managing Chinese mobile app distribution, including local entity partnerships or MIIT App Filing registration.
- **Missing Documentation:**
  Lacks step-by-step instructions on obtaining an ICP filing, a Banhao license for games, or real-name verification compliance under the PIPL.
- **Missing Code:**
  Mock clients do not integrate local real-name verification APIs, and lack the MIIT App Filing number display in the app's "About" or settings page.
- **Missing Disclosure:**
  Mockups do not show mandatory Chinese-language disclosures explaining real-name verification, PIPL privacy rights, or content moderation rules.
- **Missing Logging:**
  No database schemas or logs designed to record real-name verification status, local Chinese hosting logs, or content moderation actions.
- **Missing Testing:**
  No automated test suites validating that the MIIT App Filing registration number is rendered dynamically in Chinese storefront builds.
- **Missing Evidence:**
  Lacks template agreements with Chinese publishing partners, copies of MIIT filings, or Banhao game license applications.
- **Missing Audit Trail:**
  No immutable audit trail tracking local Chinese data storage audits, MIIT registration updates, or compliance reviews with Chinese regulatory authorities.

### 20.3 Remediation and Action Plan
1. Draft a corporate China mobile app localization and filing manual.
2. Create reusable UI templates that dynamically render the MIIT App Filing registration number on Settings/About screens.
3. Publish Chinese PIPL compliance notice templates.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU EAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **California Privacy** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US Subs Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **SK Telecom Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **China App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Almost all of these global frameworks are already named in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`, with dated sources and a deadline entry. What they lack is the implementation layer, meaning detection rules in the guard, code templates, and tests. GPSR is the only one historically absent end to end, which remains the playbook's highest remediation priority.

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most global frameworks are named with dated, verified sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order.

1. Add GPSR, the only framework historically absent end to end.
2. Give the remaining frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates, starting with the AI Act Article 50 disclosure line and the withdrawal path, since both carry 2026 deadlines.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

---

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- Illinois BIPA, [740 ILCS 14/1](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004&ChapterID=57)
- California Privacy (CCPA/CPRA), [California Civil Code Section 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5)
- UK Online Safety Act, [Online Safety Act 2023](https://www.legislation.gov.uk/ukpga/2023/30/contents/enacted)
- Australia Online Safety, [Online Safety Act 2021](https://www.legislation.gov.uk/asap/2021/10/contents)
- India DPDP, [Digital Personal Data Protection Act 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
