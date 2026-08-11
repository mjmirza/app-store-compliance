# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major modern global and regional regulations that bind app developers shipping into the EU, the US, and globally, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
  An unalterable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is entirely absent.

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

## 7. Children's Online Privacy Protection Act (COPPA) & Amended COPPA Rule

### 7.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6506, and its implementing Rule, 16 CFR Part 312, govern the collection of personal information from children under 13. The FTC finalized significant amendments on 22 April 2025 (90 FR 16918), with a general compliance enforcement date of 22 April 2026. This amended rule expands the definition of personal information to explicitly include biometric identifiers, voiceprints, gait, and facial templates, mandates a separate opt-in consent for third-party disclosures/targeted ads, requires a written data retention policy, and enforces a written information security program.

Official Citation: 16 CFR Part 312 - Children's Online Privacy Protection Rule.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a customizable, BIPA-aligned or COPPA-specific children's data policy, and does not provide a standard template to guide developers.
- **Missing Documentation:**
  The checklists fail to provide explicit operational runbooks for performing the mandated annual risk assessments or drafting the required written data retention policy.
- **Missing Code:**
  There are no reusable native or web-based Parental Gate UI components, and no code blocks to obtain a parent's separate opt-in consent before executing third-party SDK calls.
- **Missing Disclosure:**
   Boilerplate copies for clear, parent-directed notices detailing collection, usage, and parental rights under the 2026 Amended Rule are absent.
- **Missing Logging:**
  Database mock configurations do not include schemas or tables designed to securely record verifiable parental consent or track the scheduled purge dates of minors' data.
- **Missing Testing:**
  No automated integration tests exist to confirm that child sessions block non-compliant tracking or ad SDKs from making external API network calls.
- **Missing Evidence:**
  The repository provides no templates for Safe Harbor documentation or written information security program (WISP) certificates.
- **Missing Audit Trail:**
  There is no secure audit trail logging children's data deletions or tracking parental consent revocations dynamically.

### 7.3 Remediation and Action Plan
1. Add a customizable model Children's Privacy Policy and Written Information Security Program (WISP) template.
2. Code a reusable native in-app COPPA Parental Gate component with separate opt-in controls for third-party SDK data sharing.
3. Establish automated test suites to mock minor age profiles and verify that ad trackers remain fully suppressed during runtime.

---

## 8. UK ICO Age Appropriate Design Code (Children's Code)

### 8.1 Regulatory Overview and Background
The Age Appropriate Design Code (the Children's Code) is a statutory code of practice prepared by the UK Information Commissioner's Office (ICO) under Section 123 of the Data Protection Act 2018. It took full effect on 2 September 2021. It applies to "information society services likely to be accessed by children" in the UK under 18. It enforces 15 standards, including high-privacy by default, data minimization, turning off geolocation and profiling by default, and a mandatory Data Protection Impact Assessment (DPIA).

Official Citation: Data Protection Act 2018, Section 123.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not contain a model corporate policy or DPIA template specifically addressing the ICO's 15 standards.
- **Missing Documentation:**
  There are no guidelines or check-sheets to assist developers in evaluating whether their general-audience application is "likely to be accessed by children."
- **Missing Code:**
  Code templates lack middleware configuration logic to dynamically disable geolocation, background profiling, and tracking services when a UK minor user is detected.
- **Missing Disclosure:**
  UI templates do not offer age-appropriate explanations or "just-in-time" simplified disclosures tailored to children of varying developmental stages.
- **Missing Logging:**
  There are no provisions or database structures to log age-verification decisions and retain proof of high-privacy-by-default status.
- **Missing Testing:**
  No test cases are implemented to mock a UK minor session and assert that geolocation and behavioral profiling are off by default.
- **Missing Evidence:**
  The repository lacks physical compliance evidence, such as a completed standard-aligned DPIA report or an ICO self-assessment checklist.
- **Missing Audit Trail:**
  An unalterable history tracking modifications to default in-app privacy settings or reviews of children's protection features is missing.

### 8.3 Remediation and Action Plan
1. Draft and publish a ready-to-use template for a UK Children's Code Data Protection Impact Assessment (DPIA).
2. Build code helpers that automatically toggle off profiling and geolocation when the user's country is "GB" and age is determined to be under 18.
3. Design interactive consent layouts tailored to different age bands (under 13, 13-15, and 16-17).

---

## 9. UK Online Safety Act 2023

### 9.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enacted on 26 October 2023 with major children's protection duties coming into force on 25 July 2025, regulates user-to-user and search services. It mandates that platform operators take reasonable, proactive steps to shield children from illegal or harmful material. The Act enforces the use of Highly Effective Age Assurance (HEAA) methods (such as facial age estimation, credit card checks, or open banking) and explicitly outlaws simple self-declaration checkboxes.

Official Citation: Online Safety Act 2023 (c. 30).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain an internal content moderation or online safety policy aligning with UK statutory "harmful to children" definitions.
- **Missing Documentation:**
  The repository lacks documentation or check-sheets explaining how to integrate with Ofcom-approved age-assurance vendors.
- **Missing Code:**
  Front-end mocks fail to provide integrations with external facial-estimation or document-verification APIs to gate age-sensitive features.
- **Missing Disclosure:**
  No onboarding templates exist to explain the necessity of highly effective age checks or detail user data-handling rights during verification.
- **Missing Logging:**
  There are no backend mechanisms or schemas to log user content reports, illegal content takedowns, or age-assurance pass/fail verdicts.
- **Missing Testing:**
  The automated test suites do not check if access to restricted features is successfully blocked for unverified accounts.
- **Missing Evidence:**
  No template exists for Ofcom safety risk assessments or completed content moderation audits.
- **Missing Audit Trail:**
  There is no unalterable history log tracking incoming user content flag reports, review times, and eventual moderation actions.

### 9.3 Remediation and Action Plan
1. Establish a written Online Safety and Content Moderation Policy template.
2. Code UI wireframes and backend integration handlers for Ofcom-compliant facial estimation and credit card verification.
3. Build database models and API mocks to track illegal content reports and log rapid takedown actions.

---

## 10. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 10.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024, passing into law in late 2024 and fully applicable on 10 December 2025, bans minors under 16 from holding accounts on social media platforms in Australia. It places a statutory duty on platform operators to take reasonable steps to prevent under-16s from accessing their services, utilizing robust age-assurance methods. Crucially, the Act mandates that age-assurance data must be strictly ringfenced and destroyed immediately after use to protect user privacy.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not provide a template for a minor-exclusion or age-gate policy that aligns with the Australian statutory minimum age.
- **Missing Documentation:**
  There is no documentation regarding the eSafety Commissioner's guidelines, approved verification mechanisms, or data minimization standards.
- **Missing Code:**
  Code mocks fail to implement a strict under-16 block or include secure, immediate data-purge methods to erase identity scan buffers.
- **Missing Disclosure:**
  No templates exist to disclose the mandatory age gate or inform Australian users that identity records are completely deleted after verification.
- **Missing Logging:**
  Database models are missing, meaning developers cannot log the transactional success of age gates without retaining prohibited personal data.
- **Missing Testing:**
  No test cases are written to verify that Australian-based signup requests block under-16s and immediately trigger memory overwrites.
- **Missing Evidence:**
  The repository lacks templates for age-verification compliance certificates or formal records of data destruction runs.
- **Missing Audit Trail:**
  There is no historical record tracking age-assurance service uptime, changes to gating algorithms, or verified records of automatic purges.

### 10.3 Remediation and Action Plan
1. Publish an Australian Minor Exclusion Policy template with strict data minimization and deletion rules.
2. Write secure, memory-safe data processing routines to prevent age-verification documents from persisting in temporary storage.
3. Construct integration tests to mock Australian IP addresses and verify that users under 16 are blocked with instant document cleanup.

---

## 11. Brazil Digital ECA (Law 15,211/2025)

### 11.1 Regulatory Overview and Background
The Digital Statute of the Child and Adolescent (Estatuto da Criança e do Adolescente - Digital ECA), Law 15,211/2025, became fully enforceable on 17 March 2026. It mandates that any application or digital service offering products, subscriptions, or interactive content (such as loot boxes or chats) in Brazil must implement secure, non-circumventable age verification. It outlaws self-declaration checkboxes, requiring instead document verification, facial age estimation, or CPF database queries.

Official Citation: Lei nº 15.211/2025 - Estatuto da Criança e do Adolescente Digital.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing an LGPD-aligned child safety and Digital ECA compliance policy.
- **Missing Documentation:**
  Checklists lack Brazilian Indicative Rating (ClassInd) guidelines or CPF database query configuration checklists.
- **Missing Code:**
  The automated compliance guard has no rules to check for Portuguese indicative ratings, and codebase folders do not implement CPF query integrations.
- **Missing Disclosure:**
  Portuguese-localized UI strings and disclosure prompts explaining mandatory age checks are not provided.
- **Missing Logging:**
  Database mocks lack schemas to log Brazilian parent-guardian authorizations or document deletion verification stamps.
- **Missing Testing:**
  No automated tests are available to verify that Brazilian user sessions are redirected to CPF validation or document uploads.
- **Missing Evidence:**
  No template exists for the mandatory Data Protection Impact Report (Relatório de Impacto à Proteção de Dados - RIPD).
- **Missing Audit Trail:**
  An immutable log to record Brazilian compliance audits, rating updates, or database purge intervals is missing.

### 11.3 Remediation and Action Plan
1. Add a Digital ECA Policy and bilingual Portuguese age-assurance UI copy templates.
2. Implement code utilities for simulating CPF checks and Brazil document scanning in the onboarding mockups.
3. Build automated tests verifying that Brazil-based IP sessions are barred from 18-plus downloads without a verified age token.

---

## 12. India Digital Personal Data Protection Act (DPDPA) 2023 / DPDP Rules 2025

### 12.1 Regulatory Overview and Background
The Digital Personal Data Protection Act (DPDPA), 2023, along with the DPDP Rules 2025 notified on 13 November 2025, mandates strict requirements for processing personal data in India. Crucially, the child-safety provisions become enforceable on 13 May 2027. Under Section 9, everyone under 18 is classified as a child, requiring verifiable parental consent before processing child data. It prohibits any tracking, behavioral monitoring, or targeted advertising directed at children, and requires verifiable parental consent via government-backed platforms (such as DigiLocker).

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 26 of 2023).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template policy for Indian DPDPA compliance, minor data tracking bans, or parent-child mapping verification.
- **Missing Documentation:**
  The repository provides no documentation explaining how developers must integrate with India's government-backed identity services like DigiLocker.
- **Missing Code:**
  There are no code routines or middleware components to dynamically suppress tracking cookies and behavioral ad SDKs when an Indian minor signs in.
- **Missing Disclosure:**
  The onboarding templates do not provide bilingual (English/Hindi) consent prompts for requesting parental authorization.
- **Missing Logging:**
  No logging setups exist to record consent verifications obtained through Indian governmental API channels or to track consent withdrawal triggers.
- **Missing Testing:**
  The automated testing scripts do not contain checks to verify that minor sessions launched in India are completely isolated from targeted advertising.
- **Missing Evidence:**
  No evidence templates exist for Indian personal data inventory mapping or child-data processing audits.
- **Missing Audit Trail:**
  The repository lacks a secure, verifiable history of Indian minor consent logs or parental relationship audits.

### 12.3 Remediation and Action Plan
1. Draft a comprehensive DPDPA Child-Data Consent and Tracking Prevention Policy template.
2. Code a middle-tier utility that disables advertising identifiers and personalized tracking when India-based minor accounts are identified.
3. Integrate mock API routes simulating DigiLocker-based identity verification.

---

## 13. California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA)

### 13.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), California Civil Code Section 1798.100 et seq., regulates the collection and processing of personal information of California residents. The CPPA finalized updated 2026 regulations (effective 1 January 2026), which mandate honoring the Global Privacy Control (GPC) opt-out signal, displaying clear notices at collection, and providing frictionless links for "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information."

Official Citation: California Civil Code Section 1798.100 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a customizable, CPRA-compliant California Privacy Notice, Notice at Collection, or internal opt-out policy.
- **Missing Documentation:**
  Checklists fail to provide concrete developer guides explaining how to detect and process the GPC (`Sec-GPC`) header in native app contexts.
- **Missing Code:**
  Front-end templates do not feature the "Do Not Sell or Share" or "Limit Sensitive PI" buttons, and the backend lacks code to suppress sharing.
- **Missing Disclosure:**
  No boilerplate disclosures are provided for the California Notice at Collection.
- **Missing Logging:**
  The repository does not contain logging mechanisms or databases to record GPC signals or manual opt-out requests.
- **Missing Testing:**
  There are no automated integration tests to verify that GPC signals are parsed and honored by suppressing tracking.
- **Missing Evidence:**
  No evidence templates exist for California privacy audits or vendor service-provider agreements.
- **Missing Audit Trail:**
  There is no secure audit trail to record historical opt-out requests and verify that data sales/sharing ceased within statutory timelines.

### 13.3 Remediation and Action Plan
1. Publish a customizable model California Privacy Policy and a Notice at Collection.
2. Build UI layout blocks displaying prominent "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
3. Program a middleware script to check for the `Sec-GPC` header in webviews and automatically disable analytics SDKs.

---

## 14. Illinois Biometric Information Privacy Act (BIPA)

### 14.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, enacted in 2008, governs the collection, use, and storage of biometric identifiers and information (fingerprints, voiceprints, facial templates, retina scans). It imposes strict notice and consent requirements, mandates a publicly available retention and destruction schedule, prohibits the sale of biometric data, and establishes a private right of action. Amendment SB 2979 (effective 2 August 2024) limits multiple scans of the same biometric to a single violation.

Official Citation: 740 ILCS 14 - Biometric Information Privacy Act.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template Biometric Privacy Policy or biometric retention/destruction schedules.
- **Missing Documentation:**
  No developer manuals explain the secure handling of raw biometric metadata or discuss BIPA liability boundaries.
- **Missing Code:**
  Codebases do not provide distinct, explicit biometric notice screens, and mock backends do not implement BIPA's three-year automated deletion cycle.
- **Missing Disclosure:**
  The repository has no boilerplate text for written biometric disclosure statements detailing storage terms and collection purposes.
- **Missing Logging:**
  Database mockups lack structures to record written, affirmative user biometric consents or schedule automatic deletion dates.
- **Missing Testing:**
  No integration tests exist to verify that biometric scanning remains strictly locked until explicit consent is recorded.
- **Missing Evidence:**
  The playbook lacks templates for signed written biometric releases or records of secure biometric data purges.
- **Missing Audit Trail:**
  An immutable audit trail recording the capture of biometric consents and the execution of automated purges is completely absent.

### 14.3 Remediation and Action Plan
1. Add a comprehensive BIPA-compliant Biometric Information Privacy Policy and retention schedule template.
2. Code an explicit "Biometric Consent Screen" UI component requiring affirmative, opt-in consent before initiating FaceID or TouchID APIs.
3. Develop database purge scripts that trigger automated deletions of biometric templates three years after the last interaction or when the purpose is met.

---

## 15. EU Digital Markets Act (DMA)

### 15.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, regulates large online platforms designated as "gatekeepers" (such as Apple and Google) to ensure fair and open digital markets. It forces gatekeepers to allow alternative app stores, web-based app distribution, alternative payment processors, and custom out-of-app links without restrictive steering clauses. Developers utilizing DMA entitlements (e.g., `com.apple.developer.storekit.external-purchase-link` or alternative browser engines) must comply with strict reporting and gating rules.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template policy or checklist to help a developer navigate DMA entitlements.
- **Missing Documentation:**
  The repo lacks technical design guidelines explaining how to integrate Apple's `ExternalPurchaseCustomLink` or handle the Core Technology Fee (CTF) risk.
- **Missing Code:**
  Mocks lack code implementations showing how to call the system-provided external payment sheet or how to format monthly transactional reports for Apple.
- **Missing Disclosure:**
  There are no UI templates demonstrating the required EU external-steering payment disclosure sheet.
- **Missing Logging:**
  Database schemas do not support tracking out-of-app conversions, transactions, or reporting metrics for the Gatekeepers.
- **Missing Testing:**
  No automated tests exist to verify that out-of-app steering flows work seamlessly without blocking-errors.
- **Missing Evidence:**
  No templates are provided for gatekeeper reporting spreadsheets or monthly fee reconciliation audits.
- **Missing Audit Trail:**
  There is no audit trail tracking historical DMA transactions or submissions of reports to Apple/Google.

### 15.3 Remediation and Action Plan
1. Draft a comprehensive DMA Entitlement Implementation Guide and fee risk calculator.
2. Implement code templates for invoking `ExternalPurchaseCustomLink` on iOS.
3. Create automated scripts to generate the monthly transaction report CSV required by App Store Connect for external payments.

---

## 16. EU Digital Services Act (DSA)

### 16.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes a comprehensive regulatory framework for online intermediaries. To distribute applications on EU storefronts, developers must undergo mandatory verification as "traders" or explicitly declare "non-trader" status. App stores must display verified trader information (registered address, phone number, email, and D-U-N-S verification) directly on the product's storefront listing.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository provides no template policy or internal corporate guide to help organizations classify themselves as traders or non-traders under the DSA.
- **Missing Documentation:**
  No developer checklists detail the exact documentation required for verification or how to manage multi-region developer listings.
- **Missing Code:**
  The automated pre-submission guard lacks patterns to identify if verified trader details or DSA compliance declarations are missing from configuration metadata.
- **Missing Disclosure:**
  Public listings in mock folders do not show placeholder blocks for trader contact details.
- **Missing Logging:**
  No logging structure exists to track developer account verifications, 2FA setup, or DSA status reviews.
- **Missing Testing:**
  No test suites verify that non-trader listings show appropriate consumer-protection warning notices in EU countries.
- **Missing Evidence:**
  The playbook is missing templates for DSA transparency reports or verification file folders.
- **Missing Audit Trail:**
  An unalterable audit trail recording account status changes and verification history is absent.

### 16.3 Remediation and Action Plan
1. Publish a detailed DSA Trader Compliance Guide and decision-tree policy.
2. Incorporate automated check rules in the metadata auditor to flag missing support email, phone, or address listings for EU-bound releases.
3. Add compliance templates for the annual DSA Transparency Report required for larger service providers.

---

## 17. European Accessibility Act (EAA)

### 17.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became applicable on 28 June 2025. It mandates accessibility requirements for key consumer products and services, including mobile applications and e-commerce websites. Under harmonised standard EN 301 549 Chapter 11, mobile applications must support accessibility elements (VoiceOver, Dynamic Type, color contrast, and keyboard navigation). In addition, developers must publish an official Accessibility Statement outlining compliance levels.

Official Citation: Directive (EU) 2019/882 on the accessibility requirements for products and services.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing a written corporate Accessibility Policy or a compliant model Accessibility Statement.
- **Missing Documentation:**
  The checklists lack detailed guidance on standard EN 301 549 Chapter 11 requirements (which are broader than standard WCAG Level AA).
- **Missing Code:**
  Although accessibility patterns exist in `rejection-patterns.json`, codebase templates do not feature responsive layouts that scale gracefully with high dynamic-type settings or include toggleable accessibility shortcuts.
- **Missing Disclosure:**
  E-commerce templates do not provide accessible, screen-reader-conforming disclosures or modal accessibility overlays.
- **Missing Logging:**
  There are no logging mechanisms designed to capture and log accessibility issues reported by end-users.
- **Missing Testing:**
  The repository does not contain automated testing rules (such as mock screen-reader scripts) to verify structural layout contrast and focus-ordering dynamically.
- **Missing Evidence:**
  No evidence templates exist for completed EN 301 549 accessibility audits or conformity reports.
- **Missing Audit Trail:**
  A historical log tracking accessibility updates, audit records, and community feedback is absent.

### 17.3 Remediation and Action Plan
1. Add an EAA-conforming model Accessibility Statement and Accessibility Policy.
2. Implement sample screen-reader-friendly UI layouts that natively support the EN 301 549 Chapter 11 guidelines.
3. Introduce automated CI tests using visual regression checkers to verify layout integrity under 300% system font scaling.

---

## 18. South Korea Telecommunications Business Act

### 18.1 Regulatory Overview and Background
The Telecommunications Business Act in South Korea, amended in 2021/2022, prevents app store operators from forcing developers to use their proprietary in-app payment systems. To satisfy this law, developers can utilize South Korea-specific billing entitlements (such as Apple's `com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`). This requires distributing a South Korea-specific binary, integrating with approved local payment gateways (Toss, NICE, etc.), displaying a mandatory payment modal, and submitting monthly sales reports.

Official Citation: South Korea Telecommunications Business Act, Article 22-9.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no policy template for South Korean payment gate configuration or alternative checkout rules.
- **Missing Documentation:**
  No developer manuals explain how to build, sign, and distribute a region-restricted binary or configure Korean local payment gateways.
- **Missing Code:**
  The codebase lacks integrations with South Korean payment SDKs or the logic required to call Apple's Korean StoreKit external-purchase APIs.
- **Missing Disclosure:**
  There are no Korean-localized modal disclosure templates warning users that Apple/Google payment protections do not apply to external transactions.
- **Missing Logging:**
  Database structures do not track South Korean external billing metrics separately to generate mandatory monthly sales reports.
- **Missing Testing:**
  No unit or UI tests exist to verify that alternative billing is successfully loaded for South Korean App Store sessions.
- **Missing Evidence:**
  No evidence templates exist for monthly transaction sheets or payment settlement reconciliations.
- **Missing Audit Trail:**
  A cryptographic audit trail to track external billing modifications, payment reports, and submission stamps to Apple is missing.

### 18.3 Remediation and Action Plan
1. Draft a South Korean Payment Compliance Guide and billing integration manual.
2. Implement code templates for showing the South Korean StoreKit payment warning sheet.
3. Create backend database reporting templates that separate Korean payment data and automate the generation of monthly compliance reports.

---

## 19. China Mobile App Filing with the MIIT (ICP Extension)

### 19.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) of China requires all mobile applications distributed on Chinese app stores to complete a formal Mobile App Filing (an extension of the classic ICP filing system). This became mandatory on 31 March 2024. Apps without a valid filing number (registered through a licensed local partner or Chinese entity) are blocked and removed from all Chinese storefronts.

Official Citation: Notice of the Ministry of Industry and Information Technology on Carrying out Mobile Internet Application Filing (MIIT [2023] No. 105).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an internal policy guide explaining how to establish Chinese local distribution partnerships or how to classify apps under Chinese regulations.
- **Missing Documentation:**
  No checklists outline the step-by-step procedure for submitting App Filing documentation to the MIIT or obtaining a Banhao license for games.
- **Missing Code:**
  The metadata auditor has no patterns to verify that the app's MIIT filing number is properly declared in config files or displayed in the UI.
- **Missing Disclosure:**
  No localized UI wireframes show where to display the MIIT filing number on the app's "About" or "Settings" screen (a strict requirement in China).
- **Missing Logging:**
  No logging schemas track the verification of Chinese user real-name identification.
- **Missing Testing:**
  There are no automated test scripts to scan builds for unauthorized third-party Chinese SDKs or unfiled server endpoints.
- **Missing Evidence:**
  No template forms exist for MIIT application submissions, corporate license documentation, or local legal entity agreements.
- **Missing Audit Trail:**
  There is no audit trail tracking the history of MIIT filings, annual reviews, or license status updates.

### 19.3 Remediation and Action Plan
1. Publish a China App Store Distribution and MIIT Filing Guide.
2. Implement a UI component that automatically displays the MIIT filing number on the app's Settings screen when launched in China.
3. Write metadata check rules to flag any China-storefront app version lacking a declared filing number.

---

## 20. US Subscription Cancellation (ROSCA & State Negative-Option Laws)

### 20.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) enforces Section 5 of the FTC Act and the Restore Online Shoppers' Confidence Act (ROSCA) to police "negative option" billing practices (such as automatic renewals). While the FTC's consolidated "Click to Cancel" rule was vacated by the Eighth Circuit on 8 July 2025, robust state negative-option laws in California, New York, and Massachusetts remain in full force. These state statutes require that cancelling a subscription must be "at least as easy" as signing up, and prohibit requiring phone calls, mailed letters, or in-person visits to cancel if sign-up was completed online.

Official Citation: Restore Online Shoppers' Confidence Act (ROSCA), 15 U.S.C. 8401-8405.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no model policy or drafting checklist for negative-option subscriptions billed outside of platform IAP (such as web-billed subscriptions).
- **Missing Documentation:**
  No guidelines exist to specify the placement, wording, or accessibility of "Click to Cancel" options on mobile or web interfaces.
- **Missing Code:**
  Mocks lack code implementations for a self-service cancellation flow or a one-click cancel button.
- **Missing Disclosure:**
  No template copy is provided for clear subscription-billing disclosures, renewal notifications, or cancel confirmation modals.
- **Missing Logging:**
  Database schemas are missing tracking mechanisms to record the exact timestamp, user ID, and source of subscription cancellations.
- **Missing Testing:**
  There are no UI test cases to verify that subscription cancellation can be completed successfully without administrative obstacles.
- **Missing Evidence:**
  No templates exist for post-cancellation email receipts or subscription auditing sheets.
- **Missing Audit Trail:**
  A secure audit trail tracking the ratio of trial conversions, cancellation feedback, and subscription modifications is not implemented.

### 20.3 Remediation and Action Plan
1. Add a customizable model Negative-Option Subscription Agreement and Cancellation Policy.
2. Code a prominent, one-click "Cancel Subscription" button component within account settings templates.
3. Implement database logging to record cancellation events and immediately send automated cancel confirmations.
4. Write automated end-to-end tests to verify that the cancellation flow executes a frictionless, self-service cancellation without requiring manual human approval.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 4**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US COPPA & Amended Rule** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK ICO Children's Code** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety Act** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA & Rules** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **California CCPA/CPRA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU DMA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU DSA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **European Accessibility Act**| Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **South Korea Telecom Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **China Mobile App Filing** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Subscription Cancel** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. All twenty frameworks here are already named with dated sources across our database. What they lack is the implementation layer, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order.

1. Add GPSR, the only framework historically absent end to end.
2. Give the fifteen Partial/Missing frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates, starting with the AI Act Article 50 disclosure line and the withdrawal path, since both carry urgent deadlines.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

---

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- COPPA, [16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- UK ICO Children's Code, [Data Protection Act 2018 Section 123](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- UK Online Safety Act 2023, [Online Safety Act 2023 (c. 30)](https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online)
- Australia Online Safety, [Online Safety Amendment (Social Media Minimum Age) Act 2024](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA, [Lei nº 15.211/2025](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/)
- India DPDPA, [The Digital Personal Data Protection Act, 2023](https://www.bassberry.com/news/indias-data-privacy-rules-what-your-business-needs-to-know/)
- California CCPA/CPRA, [California Civil Code Section 1798.100 et seq.](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA, [740 ILCS 14](https://www.recordinglaw.com/us-laws/data-privacy-laws/bipa/)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)
- South Korea Telecommunications Business Act, [Article 22-9](https://developer.apple.com/support/storekit-external-entitlement-kr/)
- China Mobile App Filing, [MIIT [2023] No. 105 Notice](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/)
- US Subscription Cancellation, [Restore Online Shoppers' Confidence Act (ROSCA)](https://www.wilmerhale.com/en/insights/client-alerts/20250801-eighth-circuit-vacates-the-ftcs-click-to-cancel-rule-but-federal-and-state-regulators-likely-to-remain-active)
