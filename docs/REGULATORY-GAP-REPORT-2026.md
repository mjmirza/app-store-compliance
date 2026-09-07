# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile application developers shipping into the EU, US, UK, APAC, and LATAM markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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

## 7. EU AI Act Prohibited AI Practices and High-Risk Systems

### 7.1 Regulatory Overview and Background
Article 5 of the EU AI Act (Regulation (EU) 2024/1689) prohibits unacceptable-risk AI practices, such as non-consensual intimate imagery (NCII) generation, biometric categorization systems, emotion recognition in workplace or education, and untargeted scraping for facial recognition. Furthermore, as amended by Regulation (EU) 2026/1744, Article 111(4) sets mandatory compliance dates for retrofitting synthetic media watermarks and halting prohibited systems.

Official Citation: Regulation (EU) 2024/1689, Article 5 and Article 111(4) as amended by Regulation (EU) 2026/1744.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Prohibited AI Use Policy defining prohibited use cases (e.g. social scoring, emotion recognition) and escalation paths for developers integrating third-party models.
- **Missing Documentation:**
  No step-by-step compliance guidance exists for verifying model safety filters or conducting fundamental rights impact assessments (FRIA) for high-risk AI deployments.
- **Missing Code:**
  The compliance guard scripts do not programmatically detect or flag prohibited AI API calls, untargeted biometric processing, or emotion recognition logic in project codebases.
- **Missing Disclosure:**
  In-app disclosures do not inform users about automated risk classifications, prohibited feature exclusions, or high-risk AI processing safeguards.
- **Missing Logging:**
  There are no audit-ready logging provisions to record model input/output safety checks, content suppression actions, or real-time guardrail triggers.
- **Missing Testing:**
  Automated red-teaming tests and adversarial input test suites for checking NCII, CSAM, and prohibited content filtering are absent from the test scripts.
- **Missing Evidence:**
  The repository lacks templates for Fundamental Rights Impact Assessments (FRIA), conformity assessments, or technical documentation required for high-risk AI systems.
- **Missing Audit Trail:**
  No immutable ledger or timestamped audit trail records model versioning history, safety filter updates, or incident resolution steps.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) became fully applicable on 17 February 2024. Articles 30, 31, and 32 mandate trader traceability (KYTC), online interface design standards (prohibiting dark patterns), notice-and-action mechanisms for illegal content, and transparent recommender systems.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a standardized Trader Traceability and Notice-and-Action Policy for apps acting as marketplaces or intermediary platforms.
- **Missing Documentation:**
  Developer documentation is missing clear implementation guidelines on how to structure DSA-compliant trader verification profiles and reporting mechanisms.
- **Missing Code:**
  Mock UI components do not contain functional notice-and-action reporting overlays, trader status verification forms, or recommender system parameters.
- **Missing Disclosure:**
  App templates do not include mandatory DSA disclosures regarding trader contact details, business registration numbers, or main parameters of recommender algorithms.
- **Missing Logging:**
  There are no database schemas for logging incoming illegal content notices, moderation decisions, or trader verification records.
- **Missing Testing:**
  No test scripts exist to validate the notice-and-action workflow, dark pattern avoidance in cancellation flows, or recommender disclosure displays.
- **Missing Evidence:**
  Templates for annual transparency reports or independent audit evidence required for intermediary services under Article 24 are not provided.
- **Missing Audit Trail:**
  A tamper-proof audit trail tracking moderation actions, appeal outcomes, and trader verification changes is missing.

---

## 9. EU Digital Markets Act (DMA)

### 9.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) applies to designated gatekeepers and third-party developers operating on core platform services. It governs alternative app distribution, alternative payment processing, fee structures (such as Core Technology Commission / CTF), and non-discrimination.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an EU Alternative Distribution and External Payment Policy explaining eligibility, fee calculations, and store agreement terms.
- **Missing Documentation:**
  Missing developer documentation detailing region-gating rules, StoreKit/Play Billing alternative payment links, and entitlement declarations.
- **Missing Code:**
  Codebases lack regional geo-fencing helpers to enforce DMA alternative payment links strictly within EU storefronts while excluding non-EU territories.
- **Missing Disclosure:**
  In-app subscription interfaces lack disclosures explaining to EU users that an external payment processor is used and outlining dispute resolution rights.
- **Missing Logging:**
  No logging infrastructure exists to capture external purchase link clicks, transaction tokens, or fee reporting payloads required by platform providers.
- **Missing Testing:**
  Automated tests do not verify storefront-gated payment UI toggles or external browser link redirection logic under EU vs. non-EU location conditions.
- **Missing Evidence:**
  The repository provides no templates for reporting external revenue, fee reconciliation sheets, or proof of alternative entitlement approvals.
- **Missing Audit Trail:**
  An unalterable audit log tracking changes to store fee options, regional entitlement choices, and payment route configurations is absent.

---

## 10. European Accessibility Act (EAA)

### 10.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) took effect on 28 June 2025. It mandates accessibility standards based on EN 301 549 and WCAG 2.1 AA across e-commerce, banking, e-books, and mobile services sold to EU consumers.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no formal Accessibility Policy defining WCAG 2.1 AA / EN 301 549 targets or exception handling procedures.
- **Missing Documentation:**
  While accessibility audit scripts exist, developer guidelines lack step-by-step instructions for dynamic type scaling, assistive touch targets, and screen reader flow mapping.
- **Missing Code:**
  Mobile UI component codebases lack built-in accessibility wrappers, semantic label props, or contrast auto-checkers in component libraries.
- **Missing Disclosure:**
  Templates do not include an in-app Accessibility Statement link or contact mechanism for accessibility feedback.
- **Missing Logging:**
  There are no logging mechanisms to record accessibility complaints, user display preference overrides, or screen reader compatibility logs.
- **Missing Testing:**
  Static accessibility audits cover text contrast and touch targets, but automated UI tests for screen reader traversal (VoiceOver / TalkBack) are not included.
- **Missing Evidence:**
  The repository lacks templates for Accessibility Conformance Reports (VPAT / EN 301 549 declaration sheets) to prove compliance during regulatory audits.
- **Missing Audit Trail:**
  No historical audit log tracks accessibility remediation cycles, design review sign-offs, or user issue resolution timelines.

---

## 11. US Children's Online Privacy Protection Act (Amended COPPA Rule)

### 11.1 Regulatory Overview and Background
The FTC's Amended COPPA Rule (16 CFR Part 312) imposes strict restrictions on the collection, use, and disclosure of personal information from children under 13. It requires verifiable parental consent (VPC), separate consent for third-party disclosures, strict data retention limits, and prohibition of targeted advertising.

Official Citation: FTC Amended COPPA Rule, 16 CFR Part 312.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a dedicated Children's Privacy Policy template that incorporates FTC 2026 age-verification safe harbor provisions.
- **Missing Documentation:**
  Checklists mention COPPA but lack developer runbooks for configuring neutral age gates, handling third-party SDK data stripping, and executing parent consent flows.
- **Missing Code:**
  Codebases do not include reusable neutral age gate UI components or native SDK blockers that disable ad trackers automatically for child users.
- **Missing Disclosure:**
  Onboarding templates lack explicit parental disclosures detailing specific data types collected, third-party sharing practices, and parental rights to inspect or delete data.
- **Missing Logging:**
  No backend logging schema exists to record VPC verification tokens, parental consent timestamps, or automated 30-day child data retention purges.
- **Missing Testing:**
  Unit and UI test suites do not test child account flow segregation or verify that analytics SDKs remain dormant when a user specifies an under-13 age.
- **Missing Evidence:**
  Templates for Safe Harbor membership certificates, COPPA risk audits, or third-party SDK compliance attestations are absent.
- **Missing Audit Trail:**
  An immutable audit trail recording parental consent requests, data deletion events, and SDK allowlist modifications is missing.

---

## 12. US State Comprehensive Privacy Regulations (California CPRA / CPPA)

### 12.1 Regulatory Overview and Background
California Privacy Rights Act (CPRA) and CPPA 2026 regulations enforce requirements regarding automated decision-making technology (ADMT), opt-out preference signals (Global Privacy Control / GPC), sensitive personal information (SPI) limits, and mandatory risk assessments.

Official Citations: California Consumer Privacy Act / CPRA, Cal. Civ. Code section 1798.100 et seq.; CPPA Regulations (2026).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive State Privacy Rights Policy covering opt-out rights, ADMT evaluation, and sensitive personal information handling.
- **Missing Documentation:**
  Missing developer documentation on integrating GPC header parsing in web and mobile app webviews or executing consumer rights request workflows (DSAR).
- **Missing Code:**
  Code templates do not contain automated GPC signal listeners or native "Do Not Sell/Share My Personal Information" modal components.
- **Missing Disclosure:**
  Templates omit required "Notice at Collection", "Notice of Right to Opt-Out of Sale/Sharing", and disclosures explaining automated decision-making logic.
- **Missing Logging:**
  There are no logging mechanisms to record consumer privacy requests (DSARs), opt-out timestamps, or GPC signal processing confirmations.
- **Missing Testing:**
  No test scripts simulate GPC signal detection or verify that data sharing endpoints are disabled when opt-out preference headers are set.
- **Missing Evidence:**
  The repository provides no templates for Cybersecurity Audits, ADMT Risk Assessments, or Annual DSAR Metrics reports required by the CPPA.
- **Missing Audit Trail:**
  An unalterable audit trail recording DSAR fulfillment timelines, opt-out status changes, and policy version updates is missing.

---

## 13. Illinois Biometric Information Privacy Act (BIPA)

### 13.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) regulates the collection, capture, purchase, storage, and handling of biometric identifiers and information (facial recognition, fingerprints, voiceprints). It requires written release prior to collection, published retention schedules, and permanent destruction protocols.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no BIPA Biometric Information Privacy Policy or written retention schedule template.
- **Missing Documentation:**
  Developer guides lack instructions on how to handle native biometrics (Face ID / Touch ID / BiometricPrompt) locally without transferring biometric data off-device.
- **Missing Code:**
  Codebases lack guard rails that verify whether biometric authentication APIs bypass local secure enclaves or transmit raw biometric templates to remote servers.
- **Missing Disclosure:**
  UI templates omit mandatory BIPA pre-collection written disclosures explaining specific biometric data usage, retention periods, and destruction guidelines.
- **Missing Logging:**
  No logging schemas exist to capture written user consent signatures, consent timestamps, or automated biometric data destruction logs.
- **Missing Testing:**
  Test suites do not check for accidental remote transmission of biometric payloads or verify that local enclave authentication flags are respected.
- **Missing Evidence:**
  Templates for Biometric Consent Agreements, Destruction Proof Certificates, or Security Audits of biometric processing logic are missing.
- **Missing Audit Trail:**
  An immutable audit trail tracking biometric consent capture, retention schedule adherence, and destruction verification records is absent.

---

## 14. US Subscription Cancellation Rules (FTC Click-to-Cancel)

### 14.1 Regulatory Overview and Background
The FTC's Negative Option Rule (Click-to-Cancel) and state subscription laws (California AB 2863) mandate that canceling a subscription must be as easy as signing up, requiring an immediate online cancellation mechanism, advance renewal notices, and clear disclosure of terms.

Official Citation: FTC Trade Regulation Rule on Recurring Subscriptions and Other Negative Option Plans, 16 CFR Part 425; Cal. Bus. & Prof. Code section 17600 et seq.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Recurring Subscription and Negative Option Cancellation Policy outlining cancellation mechanics and pre-renewal notice rules.
- **Missing Documentation:**
  Developer documentation lacks step-by-step UI guides for building 1-click self-service cancellation paths without coercive dark patterns or forced support calls.
- **Missing Code:**
  In-app subscription management UI templates do not include functional 1-click cancellation buttons or automated pre-renewal notice email dispatch triggers.
- **Missing Disclosure:**
  Subscription paywall screens lack clear, conspicuous disclosures of billing frequency, cancellation deadline, recurring charge amount, and direct cancellation link.
- **Missing Logging:**
  No database schemas exist to log pre-renewal notice dispatches, cancellation attempt timestamps, or retention offer interactions.
- **Missing Testing:**
  Test scripts do not verify that subscription cancellation completes in equal or fewer steps than initial enrollment.
- **Missing Evidence:**
  The repository provides no templates for Subscription Terms Disclosure Audits or proof of delivery logs for pre-renewal notices.
- **Missing Audit Trail:**
  An unalterable audit log tracking subscription term changes, cancellation flow modifications, and customer cancellation timestamps is missing.

---

## 15. UK Online Safety Act 2023 and ICO Children's Code

### 15.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) and ICO Age Appropriate Design Code (Children's Code) mandate illegal content risk assessments, age-assurance measures, default high-privacy settings for children, and restriction of harmful content for UK users.

Official Citation: UK Online Safety Act 2023, c. 50; ICO Age Appropriate Design Code.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Online Safety & Children's Code Policy detailing age-assurance approaches and duties of care for user-generated content.
- **Missing Documentation:**
  Developer guides lack step-by-step instructions on implementing high-privacy defaults (geolocation off, profiling off) for UK minor profiles.
- **Missing Code:**
  Codebases lack automated logic to enforce UK-specific default settings (disabling targeted recommendations and location tracking for underage users).
- **Missing Disclosure:**
  In-app terms lack UK-specific child safety disclosures, reporting mechanisms for illegal content, and explanation of age-assurance protocols.
- **Missing Logging:**
  No backend logging schema exists to record UK illegal content reports, age-assurance verification outcomes, or risk assessment sign-offs.
- **Missing Testing:**
  Test suites do not simulate UK user IP profiles to verify that geolocation and profiling toggles default to disabled for minor accounts.
- **Missing Evidence:**
  Templates for UK Illegal Content Risk Assessments, Children's Rights Impact Assessments (CRIA), or Ofcom compliance records are absent.
- **Missing Audit Trail:**
  An immutable audit trail recording risk assessment updates, safety filter modifications, and moderation escalation histories is missing.

---

## 16. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 16.1 Regulatory Overview and Background
The Australian Online Safety Amendment (Social Media Minimum Age) Act 2024 and the eSafety Commissioner's App Distribution Code establish a mandatory age floor (16+) for social media platforms and age-assurance duties for app distribution services.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024, No. 128; eSafety App Distribution Code.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Age-Restricted Social Media Policy specifying age floor enforcement and reasonable steps for age assurance.
- **Missing Documentation:**
  Developer guides omit instructions on how to integrate Australian age-assurance signals and handle age-restricted account suspensions.
- **Missing Code:**
  Codebases do not include geo-targeted age gating for Australian users or API hooks to prevent account creation for users under 16.
- **Missing Disclosure:**
  Onboarding flows for social media app templates lack prominent notices explaining the statutory 16+ age limit for Australian residents.
- **Missing Logging:**
  No backend schema logs Australian age verification checks, account restriction triggers, or age-override appeal requests.
- **Missing Testing:**
  Test scripts do not verify that Australian IP addresses block under-16 account registration while allowing standard flows in non-restricted regions.
- **Missing Evidence:**
  Templates for eSafety Reasonable Steps Risk Evaluations, Age Assurance Audit Certificates, or regulatory compliance filings are missing.
- **Missing Audit Trail:**
  An unalterable audit log tracking regional age-limit updates, account blocking events, and age verification vendor changes is absent.

---

## 17. Brazil Digital ECA (Law 15,211/2025 and Decreto 12.880)

### 17.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025 and Decreto 12.880/2026) establishes strict protection for children and adolescents on digital platforms, mandating age verification signals on app stores and operating systems, content moderation, and advertising prohibitions aimed at minors.

Official Citation: Lei No. 15.211/2025 e Decreto No. 12.880/2026 da República Federativa do Brasil.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Brazil Digital ECA Compliance Policy covering minor protection, ad restrictions, and parental control tools.
- **Missing Documentation:**
  Developer guides lack documentation on handling Brazilian store age signals, ANPD compliance guidelines, and parental supervision settings.
- **Missing Code:**
  Codebases lack components to process Brazilian age signal flags, disable behavioral advertising, or restrict minor interactions.
- **Missing Disclosure:**
  Templates do not include mandatory Portuguese-language child protection notices, reporting channels for child abuse material, or parental tool disclosures.
- **Missing Logging:**
  No logging infrastructure exists to capture age signal verification results, parental control configurations, or content flagging events in Brazil.
- **Missing Testing:**
  Test suites do not check that Brazilian user sessions disable targeted ad networks and enable strict content filtering when age signals indicate a minor.
- **Missing Evidence:**
  Templates for ANPD Minor Privacy Impact Assessments, Child Safety Compliance Declarations, or ad-network isolation proofs are missing.
- **Missing Audit Trail:**
  An immutable audit trail recording ad targeting policy changes, age signal integration checks, and child protection incident logs is missing.

---

## 18. India Digital Personal Data Protection Act (DPDPA 2023 and Rules 2025)

### 18.1 Regulatory Overview and Background
India's DPDPA 2023 and the 2025 DPDP Rules mandate explicit, verifiable consent prior to processing personal data, interoperability with registered Consent Managers, prohibition of tracking/behavioral monitoring of children, and duties of Significant Data Fiduciaries.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPDP Rules, 2025 (G.S.R. 846(E)).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Data Protection Policy covering Consent Manager interoperability and children's data tracking bans.
- **Missing Documentation:**
  Developer guides omit instructions on implementing bilingual consent notices (in English and 22 8th Schedule languages) and Consent Manager API interfaces.
- **Missing Code:**
  Codebases do not include Consent Manager API connectors, language-selector consent notices, or conditional tracking disablers for Indian accounts.
- **Missing Disclosure:**
  Onboarding templates lack itemized, clear consent notices detailing specific personal data points and processing purposes in required official languages.
- **Missing Logging:**
  No backend logging schema captures Consent Manager tokens, consent withdrawal timestamps, or data fiduciary audit logs.
- **Missing Testing:**
  Test scripts do not verify Consent Manager API request/response handling or multilingual consent rendering under Indian locale settings.
- **Missing Evidence:**
  Templates for Data Protection Impact Assessments (DPIA), Consent Architecture Diagrams, or Data Protection Officer (DPO) designation proofs are missing.
- **Missing Audit Trail:**
  An unalterable audit log tracking consent notice updates, Consent Manager integration changes, and data processing activity records is missing.

---

## 19. Singapore Personal Data Protection Act (PDPA) and IMDA Code of Practice

### 19.1 Regulatory Overview and Background
Singapore's PDPA and the IMDA Code of Practice for Online Safety for App Distribution Services impose obligations regarding data breach notifications (within 3 calendar days), consent management, age-appropriate design, and app safety standards.

Official Citation: Personal Data Protection Act 2012 (Act 26 of 2012); IMDA Code of Practice for Online Safety (2026).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA & IMDA Safety Policy covering 72-hour breach notification procedures and app safety guidelines.
- **Missing Documentation:**
  Developer guides omit step-by-step instructions for implementing rapid breach assessment protocols and IMDA online safety controls.
- **Missing Code:**
  Codebases lack automated breach detection alert hooks or IMDA safety content filtering configuration options.
- **Missing Disclosure:**
  App templates omit Singapore Data Protection Officer (DPO) contact disclosures and data transfer impact notices.
- **Missing Logging:**
  No database logging schema exists to record potential data incidents, breach evaluation metrics, or 72-hour notification triggers to PDPC.
- **Missing Testing:**
  Test scripts do not simulate rapid breach notification workflows or verify IMDA safety rating displays.
- **Missing Evidence:**
  Templates for PDPC Data Breach Assessment Checklists, IMDA Safety Code Declarations, or Cross-Border Data Transfer Assessments are missing.
- **Missing Audit Trail:**
  An immutable audit trail recording security incident investigations, PDPC notification logs, and DPO audit reviews is missing.

---

## 20. South Korea Telecommunications Business Act and China Mobile App Filing

### 20.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (mandating third-party in-app payment choices and age descriptor rules) and China's MIIT Mobile App Filing (ICP Extension) & CAC Rules require strict local compliance, filing numbers, and regional payment choices.

Official Citations: South Korea Telecommunications Business Act Article 22-9; China MIIT Notice on App Filing (2024/2026) & CAC Order No. 21.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Korea/China Market Specific Compliance Policy covering local filing, payment gateway choice, and content restrictions.
- **Missing Documentation:**
  Developer guides omit instructions on displaying ICP filing numbers in app metadata, integrating Korean alternative billing APIs, and handling CAC AI companion rules.
- **Missing Code:**
  Codebases lack UI components to display ICP numbers in app settings/footers, Korean third-party billing selector hooks, or China real-name verification UI.
- **Missing Disclosure:**
  App metadata and in-app screens lack required ICP filing number disclosures, CAC AI interactive notices, and Korean billing fee comparisons.
- **Missing Logging:**
  No backend schema exists to record Korean alternative billing transaction tokens, MIIT app filing status records, or real-name identity verification logs.
- **Missing Testing:**
  Test scripts do not verify that Korean locale sessions render alternative payment options or that China build targets validate ICP registration fields.
- **Missing Evidence:**
  Templates for MIIT ICP License Verification Sheets, KCC Billing Compliance Filings, or CAC AI Service Registrations are missing.
- **Missing Audit Trail:**
  An unalterable audit log tracking ICP filing renewals, alternative payment fee updates, and regional compliance submission records is missing.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step implementation, detection rule, or code template to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU AI Act Prohibited/High-Risk** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. European Accessibility Act (EAA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. US COPPA (Amended Rule)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US State Privacy (CPRA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. UK Online Safety Act / ICO Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Australia Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. Korea TBA / China App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Priorities

The playbook is strong on store rejection rules and dated regulatory references, but requires systematic expansion across the operational implementation layer (code, logging, automated testing, evidence templates, and immutable audit trails).

In priority order:

1. Add GPSR detection rules, metadata schemas, and UI safety warning templates (the single framework missing end-to-end).
2. Implement backend code templates and database logging schemas for high-urgency 2026 deadlines (EU Contract Withdrawal button, EU AI Act Article 50 synthetic media watermarking, e-Evidence emergency extraction, and US state age-assurance hooks).
3. Expand automated compliance guard checks (`agent-os/hooks/app-store-compliance-guard.sh`) and test runners to validate disclosure rendering, consent logging, and regional geo-fencing.
4. Supply standardized compliance evidence templates (VPAT / EN 301 549, Fundamental Rights Impact Assessments, DPIA, parental consent logs) in the references directory.

---

## 23. Sources

Every regulation named above, at its primary source:

- GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU AI Omnibus Amendment: [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- FTC COPPA Rule: [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California Privacy Rights Act: [Cal. Civ. Code section 1798.100](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- FTC Negative Option Rule: [16 CFR Part 425](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Amendment: [Act No. 128 of 2024](https://www.legislation.gov.au/Details/C2024A00128)
- Brazil Digital ECA: [Lei No. 15.211/2025](https://www.in.gov.br/) and [Decreto No. 12.880/2026](https://www.in.gov.br/)
- India DPDPA: [Act No. 22 of 2023](https://egazette.gov.in/) and [DPDP Rules 2025](https://egazette.gov.in/)
- Singapore PDPA: [Act 26 of 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act: [Act No. 18400](https://www.law.go.kr/)
- China Mobile App Filing: [MIIT Notice on App Filing](https://www.miit.gov.cn/)
