# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulatory frameworks that bind mobile and web applications shipping across key international jurisdictions (EU, US, UK, Australia, Brazil, India, and other global markets). It checks honestly how far this repository already carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as an operational work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is audited across eight distinct compliance angles: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

## Source Trust Hierarchy and Methodology

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
  The automated compliance guard and detection recipes lack UI component implementations or helper functions to render GPSR elements dynamically.
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
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts concluded by electronic means.

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
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellations, refund rates, and subscription flow audits is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent, easily accessible "Withdrawal Button" component within account settings templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Raw age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within a multi-platform project.
- **Missing Code:**
  While rejection patterns reference state-level laws, the codebase lacks native code wrappers or helper utilities for `DeclaredAgeRange` or `com.google.android.play:age-signals`.
- **Missing Disclosure:**
  Onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log parental consent receipt, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests to verify that minor accounts are blocked from accessing premium features without valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:**
  An immutable audit trail to record age-assurance rollout, consent policy changes, and records of immediate verification data deletions is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy specifying state-level identification and data minimization rules.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers to purge raw age-verification data immediately after confirming the user's age category.
4. Establish automated unit tests verifying that minor account billing is disabled until a verifiable parental consent flag is processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among staff and persons dealing with AI operation.

This requirement applies to all organizations without headcount carve-outs. Small development teams must maintain a written policy, induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation explaining obligations under Article 4 or how to stay updated on emerging AI safety standards.
- **Missing Code:**
  No automated lint or script exists to check whether an internal AI literacy log is present and current in the repository.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose commitment to or enforcement of AI literacy standards.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no pre-commit hooks or automated checks to verify that team members committing AI-related changes have up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of acceptable evidence, such as a completed training log, course record, or written risk assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting policy reviews, training module updates, or team training record evolution over time.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Set up an automated check in the CI pipeline that warns if the literacy log has not been updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for AI systems, taking full legal effect on 2 August 2026.

Under Article 50(1), providers must ensure AI systems interacting directly with natural persons inform users they are interacting with AI. Article 50(2) mandates that outputs of generative AI systems (text, audio, images, video) must be marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deployers of deepfakes to disclose synthetic manipulation.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists mention Article 50 but lack detailed developer instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display immediate disclosure ("You are interacting with an AI system") at first user exposure.
- **Missing Logging:**
  There are no database logging schemas to record that an AI transparency warning was successfully displayed to a user session.
- **Missing Testing:**
  Existing test scripts do not check for synthetic media markers or verify that generated outputs are machine-detectable.
- **Missing Evidence:**
  The repository lacks independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and disclosure modifications is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy mandating direct disclosure and machine-readable output marking.
2. Incorporate explicit notices ("You are chatting with an AI assistant") inside conversational interface templates.
3. Implement metadata injection (C2PA specification or cryptographic watermarking) inside synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify machine-readable compliance headers.

---

## 7. EU AI Act Article 5 (Prohibited AI Practices)

### 7.1 Regulatory Overview and Background
Article 5 of the EU AI Act bans outright AI practices posing unacceptable risks to citizens' safety, livelihoods, and rights. This includes subliminal manipulation causing significant harm, exploitation of minor/vulnerability traits, social scoring, predictive policing based solely on profiling, untargeted facial scraping, workplace/educational emotion recognition (outside medical/safety), and biometric categorization inferring sensitive traits.

Official Citation: Regulation (EU) 2024/1689, Article 5.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an explicit Prohibited AI Practices Policy forbidding deployment or integration of banned AI algorithms.
- **Missing Documentation:**
  Developer guides do not detail how to audit third-party AI APIs (OpenAI, Anthropic, Google) against Article 5 prohibitions.
- **Missing Code:**
  No static analysis rules scan prompt templates or code pipelines for biometric emotion inference or subliminal manipulation patterns.
- **Missing Disclosure:**
  No template disclosures inform enterprise customers or end-users that deployed AI models strictly exclude prohibited practices.
- **Missing Logging:**
  There are no logging mechanisms to audit model inputs/outputs for potential prohibited practice signals.
- **Missing Testing:**
  No automated unit or integration tests evaluate AI model outputs against prohibited category classifiers.
- **Missing Evidence:**
  The repository lacks model vendor compliance certifications or prohibited practice risk screening forms.
- **Missing Audit Trail:**
  There is no audit trail recording model safety evaluations or pre-deployment checks verifying absence of prohibited practices.

### 7.3 Remediation and Action Plan
1. Publish an internal Prohibited AI Practices Governance Policy mapping model feature sets against Article 5 prohibitions.
2. Build static analysis rules in `scripts/release-audit.py` to flag prompt engineering files containing emotion detection or behavioral manipulation keywords.
3. Require vendor compliance attestations for all integrated third-party GPAI API endpoints.

---

## 8. EU AI Act High-Risk AI Systems (Annex III & Annex I)

### 8.1 Regulatory Overview and Background
Annex III and Annex I of the EU AI Act define high-risk AI systems (such as biometric identification, critical infrastructure, education, employment, access to essential services, law enforcement, and physical product safety components). While the EU AI Omnibus package deferred compliance deadlines (Annex III to 2 December 2027, Annex I to 2 August 2028), high-risk systems require risk management, data governance, technical documentation, record-keeping, logging, transparency, human oversight, and cyber resilience.

Official Citation: Regulation (EU) 2024/1689, Annex I & Annex III.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no High-Risk AI System Policy defining fundamental rights impact assessment (FRIA) procedures or quality management systems (QMS).
- **Missing Documentation:**
  Technical documentation templates satisfying Annex IV specifications for high-risk system architectures are completely missing.
- **Missing Code:**
  No code modules implement automated human-in-the-loop oversight mechanisms or emergency kill-switch interfaces.
- **Missing Disclosure:**
  No template notices inform users that an automated decision is produced by a high-risk AI system or explain the logical reasoning.
- **Missing Logging:**
  Backend logging components do not capture high-risk AI system execution logs (model version, prompt parameters, execution context, confidence scores) as required by Article 12.
- **Missing Testing:**
  No test harnesses evaluate bias, fairness, robustness, or adversarial vulnerability in high-risk dataset inputs and model inferences.
- **Missing Evidence:**
  The playbook carries no templates for Conformity Assessment Certificates, CE marking technical files, or FRIA completion reports.
- **Missing Audit Trail:**
  An immutable audit trail documenting model training data lineage, hyperparameter tuning, and post-market monitoring logs is missing.

### 8.3 Remediation and Action Plan
1. Develop a High-Risk AI Quality Management System (QMS) framework and Fundamental Rights Impact Assessment (FRIA) template.
2. Build standardized high-risk execution logging libraries capturing input/output pairs and model confidence scores.
3. Integrate automated dataset bias and model robustness testing suites into CI/CD pipelines.

---

## 9. European Accessibility Act (EAA - Directive (EU) 2019/882)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became applicable on 28 June 2025. It mandates accessibility for products and services delivered via web and mobile applications (including e-commerce, banking, e-books, transport, and media services). Technical compliance is established through harmonised standard EN 301 549 (WCAG 2.1 Level AA plus Chapter 11 for mobile software).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an organizational Accessibility Policy committing to EN 301 549 Chapter 11 and WCAG 2.1 AA standards.
- **Missing Documentation:**
  Developer guides do not explain EN 301 549 Chapter 11 mobile specifics (such as non-web software requirements) beyond basic WCAG guidelines.
- **Missing Code:**
  Mobile code templates lack complete accessibility trait bindings, custom action handlers, and dynamic scaling layouts.
- **Missing Disclosure:**
  Template accessibility statements meeting EN 301 549 Annex B/C specifications are missing from repository templates.
- **Missing Logging:**
  No logging mechanisms record user accessibility settings or screen reader compatibility fallback activations.
- **Missing Testing:**
  While static scripts exist (`scripts/accessibility-audit.py`), automated UI screen-reader navigation tests and color contrast verification are incomplete.
- **Missing Evidence:**
  The repository lacks Third-Party Accessibility Audit Reports or Voluntary Product Accessibility Templates (VPAT / EN 301 549 report).
- **Missing Audit Trail:**
  An audit trail documenting accessibility regression reviews, remediation milestones, and user feedback responses is absent.

### 9.3 Remediation and Action Plan
1. Formulate a corporate Accessibility Policy and publish an EN 301 549 compliant Accessibility Statement template.
2. Expand `scripts/accessibility-audit.py` to cover all EN 301 549 Chapter 11 rules.
3. Require VPAT / EN 301 549 evidence documentation prior to application submission.

---

## 10. EU Digital Services Act (DSA - Trader Status & Minors Protection)

### 10.1 Regulatory Overview and Background
Articles 30 and 31 of the Digital Services Act (Regulation (EU) 2022/2065) mandate that online marketplaces and app distribution platforms verify and display trader contact and identity information for all commercial entities distributing to EU consumers. Furthermore, DSA Article 28 requires high levels of privacy, safety, and security for minors.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal Trader Classification and Verification Policy for developers distributing apps in the EU.
- **Missing Documentation:**
  Checklists mention DSA trader status but lack detailed instructions on managing D-U-N-S verification and 2FA contact validation in store portals.
- **Missing Code:**
  No helper scripts verify whether trader metadata fields are complete and synchronized prior to release.
- **Missing Disclosure:**
  In-app disclosures do not present trader contact details or inform users of consumer protection rights when transacting with traders versus non-traders.
- **Missing Logging:**
  No database schemas store trader verification logs or record annual self-certifications.
- **Missing Testing:**
  No automated tests verify that trader disclosures are properly displayed on EU storefront listings or in-app web views.
- **Missing Evidence:**
  The repository lacks example uploads of verified trade registry extracts or payment account verification receipts.
- **Missing Audit Trail:**
  An unalterable log tracking updates to trader status declarations and store portal compliance checks is missing.

### 10.3 Remediation and Action Plan
1. Create a DSA Trader Verification Guide and Checklist detailing App Store Connect and Google Play Console verification steps.
2. Add automated validation logic in `scripts/metadata-audit.py` to check trader metadata completeness.
3. Maintain an internal compliance log of trader declarations and verification renewal dates.

---

## 11. EU Digital Markets Act (DMA - External Purchase & Interoperability)

### 11.1 Regulatory Overview and Background
The Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms (Apple App Store, Google Play) to ensure contestability and fairness. For app developers, this includes entitlements for alternative app marketplaces, web distribution, external purchase links, custom link sheets, and hardware/software interoperability.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Alternative Distribution and External Payment Policy evaluating entitlement choices and fee structures (Core Technology Fee / CTC).
- **Missing Documentation:**
  Documentation mentions DMA entitlements but lacks step-by-step developer guides for implementing the External Purchase Server API or custom disclosure sheets.
- **Missing Code:**
  Codebase templates do not contain StoreKit `ExternalPurchaseCustomLink` API implementations or automated monthly sales reporting integrations.
- **Missing Disclosure:**
  In-app paywalls lack custom modal sheet templates warning users that external transactions are not processed by Apple or Google.
- **Missing Logging:**
  No backend transaction logging schema captures external purchase tokens and reporting timestamps required for monthly platform fee reconciliation.
- **Missing Testing:**
  No automated UI tests verify that external purchase link sheets trigger correctly or that IAP and external links are strictly segregated per EU storefront rules.
- **Missing Evidence:**
  The repository lacks examples of completed platform entitlement addendums, monthly fee reports, or notarization submission logs.
- **Missing Audit Trail:**
  An audit trail recording DMA entitlement requests, StoreKit addendum approvals, and monthly fee reconciliation reports is absent.

### 11.3 Remediation and Action Plan
1. Draft a comprehensive DMA External Distribution and Payment Runbook.
2. Build mock StoreKit `ExternalPurchaseCustomLink` implementations and backend reporting scripts.
3. Implement automated pre-submission checks ensuring IAP and external purchase links are not co-mingled on the same storefront.

---

## 12. US Amended COPPA Rule (16 CFR Part 312)

### 12.1 Regulatory Overview and Background
The FTC's amended Children's Online Privacy Protection Rule (16 CFR Part 312, effective June 2025, mandatory April 2026) expands protections for children under 13. Key updates add biometric and government identifiers to personal information, mandate separate opt-in consent for third-party ad disclosures, require written data retention policies, and mandate formal information security programs.

Official Citation: FTC 16 CFR Part 312, 90 FR 16918.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Children's Data Retention and Information Security Policy satisfying 16 CFR 312.8 and 312.10.
- **Missing Documentation:**
  Checklists mention COPPA but lack operational runbooks for verifiable parental consent (VPC) via knowledge-based auth or face-match ID verification.
- **Missing Code:**
  No code modules implement separate opt-in consent flows for third-party advertising versus core app access.
- **Missing Disclosure:**
  Privacy policies in templates do not explicitly separate core service data processing from third-party disclosure opt-ins for child users.
- **Missing Logging:**
  No secure backend logging schema captures parental consent grants, consent revocations, or automatic deletion of raw verification credentials.
- **Missing Testing:**
  Test suites do not verify that child accounts are completely blocked from third-party ad SDK initialization prior to consent receipt.
- **Missing Evidence:**
  The repository lacks completed COPPA Information Security Risk Assessments or VPC vendor compliance certifications.
- **Missing Audit Trail:**
  An immutable audit trail documenting parental consent transactions, annual security risk assessments, and data purging execution logs is missing.

### 12.3 Remediation and Action Plan
1. Draft a formal COPPA Written Information Security Program (WISP) and Data Retention Policy template.
2. Implement backend VPC consent integration flows and separate ad-disclosure consent toggles in client code.
3. Build automated unit tests ensuring third-party tracking SDKs remain disabled for child accounts.

---

## 13. US FTC Health Breach Notification Rule (16 CFR Part 318)

### 13.1 Regulatory Overview and Background
The FTC's 2024 final Health Breach Notification Rule (16 CFR Part 318) covers non-HIPAA health applications, fitness trackers, and wellness services. It defines any unauthorized acquisition or sharing of sensitive health data (e.g., sharing health details with ad networks without affirmative consent) as a security breach requiring FTC and user notification within 60 days.

Official Citation: FTC 16 CFR Part 318, 89 FR 47028.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Health Data Breach Response Policy specifically defining unauthorized ad-sharing as a trigger event.
- **Missing Documentation:**
  Developer guides do not outline required health-data data flow mapping procedures to prevent accidental tracking pixel leakage.
- **Missing Code:**
  No code helpers scrub health metrics (steps, heart rate, sleep, cycle tracking) from outgoing analytics or advertising payloads.
- **Missing Disclosure:**
  Template privacy notices do not explicitly list all third-party data recipients for non-HIPAA health apps.
- **Missing Logging:**
  No security logging mechanisms capture third-party API transmission payloads containing sensitive health attributes.
- **Missing Testing:**
  No automated tests scan outgoing network requests from health modules for leaked health parameters.
- **Missing Evidence:**
  The repository carries no example FTC Breach Notification forms or vendor data-sharing audit records.
- **Missing Audit Trail:**
  An audit trail documenting health data flow reviews, consent toggles, and breach assessment investigations is absent.

### 13.3 Remediation and Action Plan
1. Create a Non-HIPAA Health App Data Governance and Breach Protocol guide.
2. Build network payload sanitizer utilities to strip sensitive health parameters from analytics pipelines.
3. Add static analysis rules in `scripts/release-audit.py` to flag health data variable transmission to third-party domains.

---

## 14. US Comprehensive State Privacy Laws (California CCPA/CPRA, Virginia, Colorado, etc.)

### 14.1 Regulatory Overview and Background
Over a dozen US states (California CCPA/CPRA, Virginia VCDPA, Colorado CPA, Connecticut, Texas TDPSA, Oregon, Delaware, New Jersey, Maryland MODPA) enforce comprehensive privacy frameworks. Common mandates require privacy notices at collection, consumer rights (know, delete, correct, opt-out of sale/sharing/targeted advertising), honoring Global Privacy Control (GPC) signals, and sensitive personal information processing limits.

Official Citations: California Civil Code Sec. 1798.100 et seq., and matching state statutes.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a US State Multi-State Privacy Rights Policy template.
- **Missing Documentation:**
  Checklists do not provide technical guides on implementing Global Privacy Control (`Sec-GPC`) handling in hybrid native/webview mobile apps.
- **Missing Code:**
  Client code templates lack GPC signal detection and automated opt-out state propagation to ad networks.
- **Missing Disclosure:**
  Onboarding templates lack "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:**
  No backend logging schema records consumer privacy rights requests (DSARs), verification outcomes, and completion timestamps.
- **Missing Testing:**
  No automated UI/integration tests verify that GPC headers or in-app opt-out toggles immediately halt third-party data transmission.
- **Missing Evidence:**
  The playbook carries no templates for Data Protection Assessments (DPAs) required for high-risk processing under state laws.
- **Missing Audit Trail:**
  An unalterable audit trail recording consumer request fulfillment within statutory windows (45 days) is missing.

### 14.3 Remediation and Action Plan
1. Publish a US Multi-State Privacy Compliance Guide and DSAR Request Handler template.
2. Build GPC header parsing and native opt-out propagation code utilities.
3. Integrate CI tests verifying that opt-out flags disable ad tracking SDKs.

---

## 15. US Illinois Biometric Information Privacy Act (BIPA - 740 ILCS 14)

### 15.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14) regulates collection, capture, purchase, storage, and use of biometric identifiers (fingerprint, voiceprint, retina/iris, scan of hand/face geometry). It mandates prior written notice and written release, a publicly available retention schedule, destruction within 3 years, and prohibits sale or profiting from biometrics.

Official Citation: 740 ILCS 14/1 et seq.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Biometric Information Privacy Policy and Retention/Destruction Schedule.
- **Missing Documentation:**
  Developer guides do not detail BIPA-compliant written release acquisition flows for face recognition or biometric authentication features.
- **Missing Code:**
  Codebase templates do not contain BIPA consent modal sheets or automated database purging routines for biometric templates.
- **Missing Disclosure:**
  Onboarding UI templates do not display explicit BIPA disclosures detailing specific purpose and length of biometric storage.
- **Missing Logging:**
  No secure backend schema logs written release timestamps, consent versions, and automated destruction timestamps.
- **Missing Testing:**
  No automated tests verify that biometric capture interfaces block execution until written consent is e-signed.
- **Missing Evidence:**
  The repository lacks templates of written biometric releases or certified biometric deletion logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking biometric data collection, storage duration, and scheduled destruction is absent.

### 15.3 Remediation and Action Plan
1. Draft a BIPA-Compliant Written Notice, Consent Release, and Retention Policy template.
2. Implement explicit biometric consent UI modals and automated template purging routines.
3. Add unit tests ensuring biometric SDKs initialize only post consent verification.

---

## 16. US Subscription Cancellation Requirements (ROSCA & State Negative Option Laws)

### 16.1 Regulatory Overview and Background
Federal law (Restore Online Shoppers' Confidence Act - ROSCA) and state negative option statutes (California, New York, Massachusetts) require that online subscription cancellation be simple, direct, and at least as easy as sign-up. A subscription flow billed outside platform in-app purchase that requires a phone call, mail, or complex hurdles to cancel violates these statutes.

Official Citations: 15 U.S.C. Sec. 8401 et seq., Cal. Bus. & Prof. Code Sec. 17600 et seq.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Subscription Transparent Billing and Cancellation Policy for non-IAP subscription flows.
- **Missing Documentation:**
  Checklists mention easy cancellation but lack UI design rules prohibiting dark patterns in cancellation flows.
- **Missing Code:**
  Web and account-settings templates lack self-service one-click subscription cancellation button implementations.
- **Missing Disclosure:**
  Paywall templates do not prominently display recurring billing terms, cancellation steps, and charge dates immediately adjacent to purchase buttons.
- **Missing Logging:**
  No database schemas record cancellation request timestamps, immediate confirmation emails, and refund processing logs.
- **Missing Testing:**
  While rejection patterns detect phone-only cancellation (`BOTH-SUBSCRIPTION-HARD-CANCEL`), no automated UI tests verify one-click web cancellation execution.
- **Missing Evidence:**
  The repository carries no examples of cancellation confirmation receipts or paywall disclosure audit logs.
- **Missing Audit Trail:**
  An audit trail documenting cancellation path modifications, churn analytics, and billing complaints is missing.

### 16.3 Remediation and Action Plan
1. Create a Subscription Billing, Paywall Disclosure, and Frictionless Cancellation Guide.
2. Build self-service subscription cancellation components for account management interfaces.
3. Add automated UI tests verifying that paywalls display required pricing terms adjacent to purchase triggers.

---

## 17. UK Online Safety Act 2023 & ICO Children's Code

### 17.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the Information Commissioner's Office (ICO) Age Appropriate Design Code regulate online services accessible by UK children under 18. Mandates require Highly Effective Age Assurance (facial age estimation, open banking, digital ID), high privacy by default, profiling off by default, geolocation off by default, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Child Safety and Age Appropriate Design Policy template.
- **Missing Documentation:**
  Developer guides do not detail Ofcom-approved age assurance implementation steps or ICO DPIA completion runbooks.
- **Missing Code:**
  Codebase templates do not implement default high-privacy settings toggles (disabling geolocation and profiling for UK accounts).
- **Missing Disclosure:**
  In-app disclosures do not explain age assurance processing or child safety reporting features in age-appropriate language.
- **Missing Logging:**
  No backend schema logs age-assurance verification outcomes or immediate purging of verification credentials.
- **Missing Testing:**
  No automated integration tests verify that UK minor accounts default to geolocation-off and profiling-disabled states.
- **Missing Evidence:**
  The repository carries no templates for completed ICO Children's Code DPIA reports or Ofcom risk assessment documents.
- **Missing Audit Trail:**
  An audit trail tracking UK age-assurance rollout, DPIA updates, and child safety incident reports is absent.

### 17.3 Remediation and Action Plan
1. Draft a UK ICO Children's Code Compliance Guide and DPIA Template.
2. Implement code utilities to enforce default high-privacy settings based on UK user locale.
3. Build automated test suites verifying profiling/geolocation default flags for minor accounts.

---

## 18. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 18.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts. Enforced by eSafety, it mandates robust age assurance (excluding self-declaration alone), ringfencing of age data, and immediate destruction of verification records.

Official Citation: Australia Online Safety Amendment Act 2024.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Minor Social Media Access and Data Ringfencing Policy.
- **Missing Documentation:**
  Developer checklists do not outline eSafety waterfall age-assurance methods or data segregation rules.
- **Missing Code:**
  Client templates do not integrate Australian age verification APIs or automated record destruction functions.
- **Missing Disclosure:**
  Onboarding flows do not display Australian-specific age restriction disclosures explaining mandatory account gating.
- **Missing Logging:**
  No backend logging schema records age verification execution while enforcing strict isolation from ad/marketing databases.
- **Missing Testing:**
  No automated unit tests verify that under-16 Australian user accounts are denied social feature activation.
- **Missing Evidence:**
  The repository lacks templates of eSafety compliance audit reports or data destruction verification certificates.
- **Missing Audit Trail:**
  An immutable audit trail documenting age assurance method effectiveness and age data purging logs is missing.

### 18.3 Remediation and Action Plan
1. Publish an Australian Online Safety Act Compliance Guide detailing eSafety requirements.
2. Implement age-verification gating hooks for social features.
3. Build database triggers to isolate and purge verification data post confirmation.

---

## 19. Brazil Digital ECA (Law 15,211/2025)

### 19.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, enforced by ANPD) establishes child and adolescent protection rules for digital applications. It prohibits simple self-declaration checkboxes for age verification, requiring accepted methods such as document verification, facial age estimation, or CPF database checks, alongside strict data minimization.

Official Citation: Law No. 15,211/2025 (Lei Digital ECA - Brasil).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazilian Digital ECA Age Verification and Child Privacy Policy.
- **Missing Documentation:**
  Checklists mention Brazil age gating but lack technical runbooks for CPF database verification or facial estimation SDK integration.
- **Missing Code:**
  Codebase templates lack Brazilian CPF validation helpers or ANPD-compliant age assurance modal sheets.
- **Missing Disclosure:**
  In-app notices do not explain why age verification is legally required under Law 15,211/2025.
- **Missing Logging:**
  No database schema logs CPF verification status without retaining raw personal tax identifiers.
- **Missing Testing:**
  No automated tests verify that self-declaration alone is rejected for Brazilian user accounts.
- **Missing Evidence:**
  The repository carries no ANPD compliance self-assessment templates or CPF vendor data privacy agreements.
- **Missing Audit Trail:**
  An audit trail documenting Brazilian age-assurance feature deployment and ANPD audit readiness is missing.

### 19.3 Remediation and Action Plan
1. Create a Brazil Digital ECA Compliance Guide and CPF/Facial Verification integration guide.
2. Implement CPF validation and age-estimation helper classes in client templates.
3. Build automated tests verifying that Brazilian onboarding flows enforce multi-factor age assurance.

---

## 20. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 20.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 regulate processing of digital personal data. For children under 18, it mandates verifiable parental consent through government-backed mechanisms (e.g., DigiLocker) and strictly prohibits behavioral tracking, targeted advertising, or harmful content targeting children.

Official Citation: Act No. 22 of 2023 (DPDPA) & DPDP Rules 2025.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Data Fiduciary and Child Data Protection Policy template.
- **Missing Documentation:**
  Developer guides do not detail DigiLocker / Virtual ID integration steps for verifiable parental consent in India.
- **Missing Code:**
  Client code templates lack DPDPA multilingual consent notices or parental consent verification handlers.
- **Missing Disclosure:**
  Paywalls and onboarding screens do not present itemized, standalone consent notices in all 22 scheduled Indian languages.
- **Missing Logging:**
  No database schema captures granular consent items, withdrawal requests, and Data Protection Officer (DPO) logging.
- **Missing Testing:**
  No automated tests verify that behavioral ad tracking is completely disabled for accounts flagged as under 18 in India.
- **Missing Evidence:**
  The repository carries no example DPDPA Consent Impact Assessments or DPO appointment documentation.
- **Missing Audit Trail:**
  An unalterable audit trail tracking consent grants, withdrawals, and data fiduciary compliance reviews is missing.

### 20.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Runbook and Multilingual Consent Notice template.
2. Build code modules for granular consent management and DigiLocker VPC verification.
3. Create automated integration tests ensuring child accounts exclude behavioral advertising SDKs.

---

## 21. Consolidated Gap Classification Matrix

This matrix summarizes the compliance status of the repository across all twenty evaluated frameworks.
- Covered: Fully supported with policies, documentation, code, disclosures, logging, tests, evidence, and audit trails.
- Partial: Framework named with dated citations, but lacking complete code implementations, tests, or operational runbooks.
- Missing: Framework absent or lacking structural coverage across most compliance categories.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU AI Act Art 5** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU AI Act High-Risk** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. EU DSA Trader Status** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. EU DMA External Purchase** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US FTC Health Breach** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. US State Privacy Laws** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. US Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Actionable Implementation Roadmap

To transition the repository from partial coverage to complete, audit-ready compliance across all twenty regulatory domains, the playbook development must prioritize the following sequential milestones:

1. **Phase 1: Code and Guard Detection Layer (Immediate)**
   - Expand `data/rejection-patterns.json` and `data/detection-recipes.json` to add concrete detection logic for all missing code and disclosure patterns (GPSR metadata, e-Evidence emergency protocols, Withdrawal Button UI, and BIPA biometric consent).
   - Update `agent-os/hooks/app-store-compliance-guard.sh` and `scripts/release-audit.py` to run static checks for missing compliance headers and disclosures.

2. **Phase 2: Reference Templates and Policy Assets (Short Term)**
   - Add template policy files under `templates/` for Law Enforcement Requests (e-Evidence), Children's Data Retention (COPPA/DPDPA), Biometric Release (BIPA), AI Literacy (Article 4), and General Product Safety (GPSR).
   - Create UI component code snippets in `references/` for EU Contract Withdrawal buttons, AI interaction notices, and GPC opt-out toggles.

3. **Phase 3: Automated Test Verification and Evidence Generation (Medium Term)**
   - Develop integration test scripts in `scripts/` to validate synthetic media watermarking (C2PA), paywall cancellation button accessibility, and child-account ad-tracking suppression.
   - Build automated evidence generators that log compliance status, training logs, and audit trails to `docs/` during CI/CD releases.

---

## 23. Sources

Primary official citations backing every evaluated framework:

- EU General Product Safety Regulation: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services Directive: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- US FTC Amended COPPA Rule: [FTC 16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US FTC Health Breach Notification Rule: [FTC 16 CFR Part 318](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-finalizes-changes-health-breach-notification-rule)
- US State App Store Accountability Acts: Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161
- California Consumer Privacy Act / CPRA: [Cal. Civ. Code Sec. 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois Biometric Information Privacy Act: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- UK ICO Children's Code: [ICO Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- Australia Online Safety Amendment Act 2024: [ComLaw C2024A00124](https://www.legislation.gov.au/Details/C2024A00124)
- Brazil Digital ECA: [Law No. 15,211/2025](https://www.in.gov.br/)
- India Digital Personal Data Protection Act: [Gazette of India No. 22 of 2023](https://egazette.gov.in/)
