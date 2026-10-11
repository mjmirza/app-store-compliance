# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile and web app developers shipping across the EU, US, UK, APAC, LatAm, and global storefronts, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight mandatory angles: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Act No. 185, which replaces HB 570 (2025), Alabama HB 161 (2026).

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

## 7. EU AI Act Article 5 (Prohibited AI Practices)

### 7.1 Regulatory Overview and Background
Article 5 of the EU AI Act (Regulation (EU) 2024/1689) prohibits AI practices that pose unacceptable risks to fundamental rights. Prohibited practices include subliminal techniques, manipulative or deceptive AI, exploitation of vulnerabilities (age, disability, socio-economic status), social scoring, untargeted scraping of facial images, emotion recognition in workplaces and education, and biometric categorization predicting sensitive attributes.

Enforcement of Article 5 began on 2 February 2025. Non-compliance results in maximum fines under Article 99 of up to 35,000,000 EUR or 7% of total worldwide annual turnover.

Official Citation: Regulation (EU) 2024/1689, Article 5 & Article 99.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no explicit Prohibited AI Practices Governance Policy to systematically screen AI features for prohibited elements before development.
- **Missing Documentation:**
  The repository lacks developer guidelines or risk evaluation forms to assess whether a planned AI feature (such as biometric classification or sentiment analysis) violates Article 5.
- **Missing Code:**
  Static analysis tools and guard scripts lack detection rules to flag code patterns involving facial image scraping, emotion detection APIs, or subliminal audio/visual cues.
- **Missing Disclosure:**
  No standard internal disclosures exist to certify to platform operators and regulators that an AI application contains no prohibited practices.
- **Missing Logging:**
  There are no logging mechanisms or safety filters designed to record automated blocking of prohibited input prompts or prohibited inference model queries.
- **Missing Testing:**
  No automated unit tests or adversarial prompt test suites exist to verify that AI models resist generating manipulative or vulnerability-exploiting outputs.
- **Missing Evidence:**
  The repository contains no template risk assessment sheets or certification forms demonstrating pre-launch Article 5 compliance reviews.
- **Missing Audit Trail:**
  An immutable audit trail documenting feature design reviews, safety evaluations, and AI model risk assessments is absent.

### 7.3 Remediation and Action Plan
1. Implement an Article 5 Prohibited AI Screening Checklist in `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Add static guard detection patterns to `data/rejection-patterns.json` for banned AI APIs (facial scraping, emotion recognition).
3. Require signed risk assessment evidence sheets prior to deploying new generative or biometric AI models.

---

## 8. EU Digital Markets Act (DMA)

### 8.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, regulates designated gatekeepers (such as Apple and Google) to ensure fair and open digital markets. For mobile developers, the DMA enables alternative app distribution (sideloading and third-party app marketplaces in the EU), alternative payment processing, and direct external purchase link steering without gatekeeper anti-steering restrictions.

Under updated Apple EU business terms (effective 1 October 2026), the Core Technology Fee (CTF) is replaced by the Core Technology Commission (CTC) under unified commercial terms.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal EU Alternative Distribution & External Fee Policy explaining how to evaluate gatekeeper entitlement agreements (ADPLA Attachment 14).
- **Missing Documentation:**
  Step-by-step developer documentation for setting up alternative marketplace entitlement certificates, alternative billing APIs, and external link handling under DMA is missing.
- **Missing Code:**
  Code templates do not include iOS/Android native implementations for DMA region-checking (`SKPaymentQueue` alternative distribution APIs, Google Play custom external billing flows).
- **Missing Disclosure:**
  Templates fail to provide user-facing disclosures notifying EU users when transactions occur outside gatekeeper payment systems.
- **Missing Logging:**
  Backend schemas do not provide transaction reporting logs required to fulfill gatekeeper monthly reporting obligations for alternative payments.
- **Missing Testing:**
  No automated integration tests verify storefront-gating logic that enables DMA entitlements strictly within the EU 27 Member States.
- **Missing Evidence:**
  The repository lacks templates of signed Gatekeeper Addendums (ADPLA Attachment 14) or alternative distribution security verification certificates.
- **Missing Audit Trail:**
  There is no audit trail system tracking monthly DMA sales reports, gatekeeper fee calculations, or entitlement activation dates.

### 8.3 Remediation and Action Plan
1. Update `docs/EU-REGULATORY-2026.md` with complete implementation code for EU region-gating of alternative payment links.
2. Build backend logging templates for external purchase transaction reporting.
3. Add automated test cases simulating EU vs. non-EU storefront responses for DMA entitlement checks.

---

## 9. EU Digital Services Act (DSA)

### 9.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes comprehensive rules for online intermediaries and platforms. For mobile developers, the DSA mandates Trader Status Declaration (declaring commercial entity name, address, email, phone number, and official registration details on storefronts), illegal content Notice and Action mechanisms, and recommender system transparency.

Compliance has been mandatory for all platforms and app developers since 17 February 2024.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Trader Status & Content Moderation Policy for apps operating on EU storefronts.
- **Missing Documentation:**
  Developer guides fail to detail exact App Store Connect and Google Play Console field requirements for DSA Trader Verification.
- **Missing Code:**
  UGC app templates lack code components for in-app Notice and Action reporting mechanisms to allow users to flag illegal content.
- **Missing Disclosure:**
  Templates do not include required in-app disclosures explaining the main parameters of recommendation algorithms used in the app.
- **Missing Logging:**
  No database schemas exist for logging incoming illegal content notices, moderation decisions, or user appeal outcomes.
- **Missing Testing:**
  Automated tests do not verify that content reporting endpoints process flags within required timeframes or generate ticket numbers.
- **Missing Evidence:**
  The repository contains no template files for DSA Transparency Reports or verification certificates of official registry details.
- **Missing Audit Trail:**
  An unalterable audit log of moderation actions, appeal decisions, and trader verification updates is missing.

### 9.3 Remediation and Action Plan
1. Add DSA Trader Verification items to `scripts/metadata-audit.py` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Provide in-app Notice & Action UI code snippets for user-generated content applications.
3. Create a standardized database logging format for content moderation requests and DSA compliance records.

---

## 10. European Accessibility Act (EAA)

### 10.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, mandates that products and services placed on the EU market (including mobile apps, e-commerce platforms, banking services, e-books, and audiovisual media) must meet strict accessibility requirements based on EN 301 549 and WCAG 2.1 AA standards.

Mandatory enforcement across all EU Member States began on 28 June 2025. Microenterprises (fewer than 10 employees and under 2,000,000 EUR annual turnover) providing services are exempt, but product requirements bind all entities regardless of size.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an explicit Digital Accessibility Policy defining organizational commitments to EN 301 549 and WCAG 2.1 AA standards.
- **Missing Documentation:**
  Checklists fail to provide comprehensive mapping between iOS VoiceOver / Android TalkBack attributes and statutory EAA requirements.
- **Missing Code:**
  UI templates lack accessibility labels, dynamic text scaling support (`DynamicType`, `FontScaling`), and required color contrast ratios in default stylesheets.
- **Missing Disclosure:**
  No template Accessibility Statement is provided for inclusion in apps or on websites detailing compliance status and feedback mechanisms.
- **Missing Logging:**
  There are no logging provisions for tracking accessibility feedback, barrier reports, or remediation tickets submitted by users.
- **Missing Testing:**
  While `scripts/accessibility-audit.py` exists, it lacks automated checks for screen-reader semantics, minimum touch target sizes (44x44 dp), and color contrast ratios.
- **Missing Evidence:**
  The repository lacks templates for Accessibility Conformance Reports (VPAT / EN 301 549 evaluation sheets) or expert accessibility audit evidence.
- **Missing Audit Trail:**
  An immutable history of accessibility audits, regression tests, and user bug resolutions is absent.

### 10.3 Remediation and Action Plan
1. Expand `scripts/accessibility-audit.py` to test contrast ratios, touch target sizes, and accessibility label presence.
2. Publish an Accessibility Statement template in `references/templates/`.
3. Integrate automated UI accessibility tests into CI workflows (`.github/workflows/ci.yml`).

---

## 11. Children's Online Privacy Protection Act (COPPA & Amended Rule)

### 11.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, enforced by the US Federal Trade Commission (FTC), regulates the online collection of personal information from children under 13. The FTC's Amended COPPA Rule (mandatory compliance 22 April 2026, supported by the FTC Age-Verification Policy Statement of 25 February 2026) imposes heightened restrictions on push notifications, targeted ads, biometric data, and third-party SDK data sharing in child-directed apps.

Official Citation: 16 CFR Part 312 (FTC) & FTC Enforcement Policy Statement (25 February 2026).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a COPPA Compliance Policy defining data minimization, neutral age gating, and verifiable parental consent (VPC) mechanisms.
- **Missing Documentation:**
  Documentation does not include detailed SDK vetting guides to identify and disable non-compliant tracking SDKs in child-directed apps.
- **Missing Code:**
  Native code templates do not implement neutral age gates or automatic disabling of advertising identifiers (`IDFA`, `GAID`) for minor users.
- **Missing Disclosure:**
  Direct Notice to Parents and Direct Parental Consent disclosure templates are absent from the repository.
- **Missing Logging:**
  No backend schema exists to record receipt of Verifiable Parental Consent, consent revocations, or automatic deletion of minor data upon age threshold expiry.
- **Missing Testing:**
  Automated tests do not verify that analytics and advertising SDKs are completely suppressed when an under-13 age signal is received.
- **Missing Evidence:**
  The repository contains no template records of FTC Safe Harbor certification or verified parental consent audit records.
- **Missing Audit Trail:**
  An unalterable audit log documenting child data deletions, SDK consent flags, and parental consent revocations is not implemented.

### 11.3 Remediation and Action Plan
1. Update `references/guidelines/by-app-type/kids-category-and-families.md` with neutral age gate code snippets.
2. Add automated guard checks to flag tracking SDKs (`AppsFlyer`, `Adjust`, `Facebook SDK`) in apps targeting children.
3. Draft Direct Notice to Parents disclosure templates in `references/templates/`.

---

## 12. FTC Health Breach Notification & Negative Option Rules

### 12.1 Regulatory Overview and Background
The FTC Health Breach Notification Rule (HBNR), 16 CFR Part 318 (effective 25 June 2024), requires non-HIPAA health apps and wellness trackers to notify users and the FTC in the event of unauthorized access or disclosure of personal health data. Concurrently, the FTC's Rule on Recurring Subscriptions and Other Negative Option Plans (16 CFR Part 425) requires "click-to-cancel" subscription flows that are as simple as enrollment.

Official Citations: 16 CFR Part 318 & 16 CFR Part 425 (FTC).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Health Data Security & Subscription Cancellation Policy.
- **Missing Documentation:**
  No operational runbooks exist for submitting 10-day FTC breach notifications or implementing 1-click subscription cancellation interfaces.
- **Missing Code:**
  Code templates do not include 1-click in-app cancellation components or encrypted health data export mechanisms.
- **Missing Disclosure:**
  Subscription paywall templates fail to include required FTC clear-and-conspicuous disclosures before billing consent is obtained.
- **Missing Logging:**
  Backend schemas lack security breach incident logs or timestamped consent logs for subscription renewals.
- **Missing Testing:**
  No automated integration tests verify that subscription cancellation executes without intermediate survey walls or retention friction.
- **Missing Evidence:**
  The repository lacks templates of FTC Breach Notification forms or pre-billing consent verification receipts.
- **Missing Audit Trail:**
  An unalterable record tracking subscription disclosures, consent timestamps, and breach incident evaluations is absent.

### 12.3 Remediation and Action Plan
1. Add FTC Negative Option Rule checklist items to `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Create 1-click subscription cancellation UI code samples in `references/rules/payments.md`.
3. Include an FTC Health Breach incident response runbook in `docs/MOBILE-SECURITY-2026.md`.

---

## 13. California Privacy Rights Act (CPRA / CCPA / AADC)

### 13.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and updated by CPPA 2026 Regulations, along with the California Age-Appropriate Design Code (AADC), regulates privacy, sensitive personal information, automated decision-making technology (ADMT), and children's privacy. Mandatory compliance enforcement for CPPA 2026 regulations began 1 January 2026.

Official Citations: Cal. Civ. Code Section 1798.100 et seq. & CPPA Regulations.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a CPRA/CCPA Rights Handling Policy covering "Do Not Sell or Share My Personal Info" and "Limit the Use of My Sensitive Personal Info".
- **Missing Documentation:**
  Developer guides fail to detail technical implementation steps for honoring Global Privacy Control (GPC) signal headers in mobile and web applications.
- **Missing Code:**
  Codebase templates lack auto-detection logic for `Sec-GPC` HTTP headers or native opt-out signaling APIs.
- **Missing Disclosure:**
  Templates do not include California-specific "Notice at Collection" or sensitive personal information processing opt-out links.
- **Missing Logging:**
  Backend schemas lack logs for tracking CCPA opt-out requests, data deletion requests, or GPC signal acknowledgments.
- **Missing Testing:**
  No automated unit tests verify that receiving a GPC signal automatically sets tracking flags to disabled across third-party SDKs.
- **Missing Evidence:**
  The repository contains no template records of Data Protection Impact Assessments (DPIAs) required for ADMT or high-risk processing.
- **Missing Audit Trail:**
  An immutable log tracking CCPA request fulfillment dates, opt-out status changes, and DPIA annual reviews is missing.

### 13.3 Remediation and Action Plan
1. Implement GPC header parsing in web and mobile network handler templates.
2. Draft a California Notice at Collection template in `docs/PRIVACY-POLICY-MIGRATION.md`.
3. Add CPRA opt-out handling tests to `scripts/monitor-privacy-test.sh`.

---

## 14. Illinois Biometric Information Privacy Act (BIPA)

### 14.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, strictly regulates the collection, capture, purchase, receipt, storage, and handling of biometric identifiers (facial geometry, fingerprints, voiceprints, retina/iris scans). BIPA mandates written consent prior to collection, strict retention schedules, and immediate destruction upon goal fulfillment.

Official Citation: 740 ILCS 14 (Illinois General Assembly).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Biometric Data Retention & Destruction Policy complying with 740 ILCS 14/15.
- **Missing Documentation:**
  Documentation fails to distinguish between local on-device biometric auth (FaceID/BiometricPrompt, exempt from BIPA storage rules) and server-side biometric processing (subject to full BIPA liability).
- **Missing Code:**
  Code templates lack explicit BIPA written release modal dialogs and automated retention destruction triggers.
- **Missing Disclosure:**
  No template BIPA Biometric Information Notice is provided detailing exact storage purposes and retention timelines.
- **Missing Logging:**
  Backend schemas do not provide unalterable logs capturing written consent releases or automated biometric payload destruction events.
- **Missing Testing:**
  Automated tests do not verify that biometric data is deleted from temporary storage immediately after feature execution.
- **Missing Evidence:**
  The repository contains no template executed BIPA consent receipts or destruction certificate logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking biometric consent grants, policy revisions, and data purges is missing.

### 14.3 Remediation and Action Plan
1. Clarify on-device vs. server-side biometric rules in `docs/MOBILE-SECURITY-2026.md`.
2. Add BIPA written release modal UI code in `references/rules/privacy.md`.
3. Include automated BIPA deletion checks in guard verification scripts.

---

## 15. UK Online Safety Act & Age Appropriate Design Code

### 15.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enforced by Ofcom, along with the ICO Age Appropriate Design Code (Children's Code), imposes mandatory duties of care on user-to-user services and search services. Requirements include age assurance, child safety risk assessments, illegal content removal, and strict default privacy settings for under-18 users. Mandatory enforcement began 25 July 2025.

Official Citations: UK Online Safety Act 2023 & ICO Age Appropriate Design Code.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Children's Code & Online Safety Policy covering high-privacy defaults and risk evaluations.
- **Missing Documentation:**
  Developer guides do not detail Ofcom-aligned illegal content risk assessment methodologies or age-assurance implementation patterns.
- **Missing Code:**
  Code templates do not default geolocation tracking, profiling, and targeted advertising to OFF for minor users in the UK.
- **Missing Disclosure:**
  Templates lack child-friendly terms of service summaries and age-assurance privacy notices.
- **Missing Logging:**
  No database schemas exist for logging child safety incident reports, Ofcom compliance reviews, or moderation queues.
- **Missing Testing:**
  Automated tests do not check that UK minor accounts have high-privacy default configurations enforced on account creation.
- **Missing Evidence:**
  The repository contains no template Ofcom Safety Risk Assessment documents or ICO Children's Code audit forms.
- **Missing Audit Trail:**
  An immutable audit trail documenting safety risk reviews, algorithm changes, and child safety incident resolutions is absent.

### 15.3 Remediation and Action Plan
1. Add high-privacy default verification checks to `scripts/monitor-privacy.py`.
2. Draft an Ofcom Risk Assessment template in `docs/GLOBAL-REGULATORY-2026.md`.
3. Build automated test cases for UK storefront age-gating and privacy default enforcement.

---

## 16. Australia Online Safety Act & App Distribution Services Code

### 16.1 Regulatory Overview and Background
Australia's Online Safety Act 2021, enforced by the eSafety Commissioner, along with the Online Safety Amendment (Social Media Minimum Age) Act 2024 and the App Distribution Services Online Safety Code (registered 9 September 2025, mandatory 9 September 2026), requires app stores and developers to enforce age assurance, prevent minor access to Class 1C/2 restricted material, and implement age limits (e.g. 16+ for social media platforms).

Official Citations: Online Safety Act 2021 & App Distribution Services Code (eSafety Commissioner).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Online Safety Compliance Policy covering age verification and Class 1C/2 content filtering.
- **Missing Documentation:**
  Guides do not detail technical steps for handling eSafety Commissioner removal notices or Australian storefront age gating.
- **Missing Code:**
  Native app templates lack integration logic for Australian age-assurance signals or restricted content access controls.
- **Missing Disclosure:**
  Templates fail to display required eSafety reporting contact information or Australia-specific age warning notices.
- **Missing Logging:**
  Backend schemas lack logs for capturing eSafety removal notices, content blocking events, or age verification results.
- **Missing Testing:**
  No automated tests verify that Class 1C/2 restricted content is blocked for users identified as Australian minors.
- **Missing Evidence:**
  The repository lacks templates for eSafety compliance reports or verified age assurance audit records.
- **Missing Audit Trail:**
  An immutable log of content moderation actions, notice fulfillment timestamps, and age-assurance system updates is missing.

### 16.3 Remediation and Action Plan
1. Add Australian age-assurance requirement details to `docs/GLOBAL-REGULATORY-2026.md`.
2. Include eSafety notice response procedures in `references/rules/safety.md`.
3. Add automated checks for Australia-specific age rating metadata in `scripts/metadata-audit.py`.

---

## 17. Brazil Digital ECA

### 17.1 Regulatory Overview and Background
Brazil's Digital ECA (Estatuto da Criança e do Adolescente), Law 15,211/2025 as regulated by Decreto n. 12.880 of 18 March 2026, establishes mandatory age-assurance, default privacy, and parental consent requirements for digital services accessed by children and adolescents in Brazil. ANPD enforcement begins in early 2027, with mandatory store compliance live since March 2026.

Official Citations: Lei nº 15.211/2025 & Decreto nº 12.880/2026 (Presidência da República).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy covering minor protection and data minimization under LGPD/ECA.
- **Missing Documentation:**
  Documentation does not detail ANPD-compliant age verification methods or Portuguese-language minor privacy disclosure requirements.
- **Missing Code:**
  Codebase templates lack integration hooks for processing Brazilian storefront age signals or disabling profiling for local minor accounts.
- **Missing Disclosure:**
  In-app onboarding templates lack Portuguese-language child privacy notices and parental consent request dialogs.
- **Missing Logging:**
  Backend schemas do not provide logs for recording Brazilian parental consent releases or immediate deletion of verification data.
- **Missing Testing:**
  No automated unit tests verify that Brazilian storefront users under 18 have advertising identifiers and location tracking automatically disabled.
- **Missing Evidence:**
  The repository lacks templates for LGPD/ECA Minor Data Protection Impact Assessments (DPIA-Child).
- **Missing Audit Trail:**
  An unalterable audit log tracking consent approvals, data purge events, and ANPD compliance reviews is missing.

### 17.3 Remediation and Action Plan
1. Document Brazil Digital ECA rules in `docs/GLOBAL-REGULATORY-2026.md` Section 3.3.
2. Add Portuguese minor disclosure templates in `references/templates/`.
3. Implement automated test cases verifying ECA default privacy settings.

---

## 18. India Digital Personal Data Protection Act (DPDPA)

### 18.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA), 2023, enforced by the Data Protection Board of India, regulates the processing of digital personal data. Key provisions include mandatory verifiable parental consent for processing data of children (under 18), prohibition of tracking or targeted ads directed at children, mandatory appointment of a Data Protection Officer (DPO), and Consent Manager integration (effective 13 November 2026).

Official Citation: The Digital Personal Data Protection Act, 2023 (Gazette of India).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a DPDPA Consent & Children's Data Governance Policy.
- **Missing Documentation:**
  Developer documentation fails to specify integration standards for India Consent Managers or DPDPA Notice at Collection in 22 official languages.
- **Missing Code:**
  Native code templates lack Consent Manager API integration layers or automatic suppression of behavioral tracking for Indian minor accounts.
- **Missing Disclosure:**
  In-app notice templates fail to provide multi-lingual DPDPA consent notices with itemized processing purposes.
- **Missing Logging:**
  Backend schemas do not provide immutable consent logs capturing consent withdrawal, purpose limitation, or DPO audit records.
- **Missing Testing:**
  No automated integration tests verify that withdrawing consent via a Consent Manager automatically purges user data across backend tables.
- **Missing Evidence:**
  The repository contains no template records of DPDPA Significant Data Fiduciary audit certificates or Consent Manager registration proofs.
- **Missing Audit Trail:**
  An unalterable audit trail tracking consent grant/withdrawal timestamps, DPO reviews, and Data Protection Board notifications is missing.

### 18.3 Remediation and Action Plan
1. Document India DPDPA requirements in `docs/GLOBAL-REGULATORY-2026.md` Section 3.6.
2. Build consent withdrawal and data purge mock handlers in backend template utilities.
3. Include DPDPA compliance checks in `scripts/monitor-privacy.py`.

---

## 19. Singapore Personal Data Protection Act (PDPA) & Online Safety Code

### 19.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) 2012, enforced by the PDPC, alongside the IMDA Code of Practice for Online Safety for App Distribution Services (effective 1 April 2026), regulates personal data collection, consent, breach notification (within 3 calendar days), and online safety controls for app distribution.

Official Citations: Personal Data Protection Act 2012 & IMDA Code of Practice (PDPC / IMDA).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA & IMDA Online Safety Policy covering data breach notification timelines and app safety standards.
- **Missing Documentation:**
  Documentation does not detail technical procedures for meeting the 72-hour mandatory PDPC breach notification window.
- **Missing Code:**
  Code templates lack automated breach logging triggers or IMDA age-assurance metadata tags for Singapore storefront releases.
- **Missing Disclosure:**
  Templates fail to include Singapore DPO contact details or IMDA online safety disclosures in user onboarding.
- **Missing Logging:**
  Backend schemas lack 72-hour breach notification countdown logs or PDPC incident reporting records.
- **Missing Testing:**
  Automated tests do not verify that user data access requests (PDPA Access & Correction) execute within statutory timelines (30 days).
- **Missing Evidence:**
  The repository contains no template PDPC Data Protection Trustmark (DPTM) certification evidence or IMDA safety audit forms.
- **Missing Audit Trail:**
  An unalterable log documenting privacy policy updates, DPO appointments, and breach evaluation records is missing.

### 19.3 Remediation and Action Plan
1. Add Singapore PDPA & IMDA requirements to `docs/GLOBAL-REGULATORY-2026.md` Section 3.7.
2. Include a 72-hour breach notification runbook in `docs/MOBILE-SECURITY-2026.md`.
3. Add automated checks for IMDA compliance tags in `scripts/metadata-audit.py`.

---

## 20. China App Filing & CAC AI Measures

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) Mobile App Filing requirement (mandatory since 31 March 2024), alongside CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, effective 15 July 2026), requires all apps distributed in China to complete ICP app filing and strictly forbids generative AI anthropomorphic interactive companion services from engaging with minors.

Official Citations: MIIT Notice on Mobile Application Filing & CAC Order No. 21 (MIIT / CAC).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China App Filing & Generative AI Compliance Policy detailing ICP registration and CAC minor companion bans.
- **Missing Documentation:**
  Developer guides fail to detail App Store Connect and Google Play submission fields for MIIT ICP app filing numbers.
- **Missing Code:**
  Codebase templates lack strict age-gate blocks preventing minors in China from accessing conversational AI or anthropomorphic chatbots.
- **Missing Disclosure:**
  Templates fail to display MIIT ICP filing numbers on app splash screens or settings pages as required by Chinese law.
- **Missing Logging:**
  Backend schemas lack real-name registration verification logs or CAC AI safety incident logs.
- **Missing Testing:**
  No automated integration tests verify that AI chatbot interfaces strictly block minor accounts on Chinese IP ranges or storefronts.
- **Missing Evidence:**
  The repository contains no template MIIT App Filing registration certificates or CAC AI Algorithm Filing proof sheets.
- **Missing Audit Trail:**
  An unalterable audit log tracking ICP filing renewals, CAC safety reviews, and real-name verification checks is missing.

### 20.3 Remediation and Action Plan
1. Update `docs/GLOBAL-REGULATORY-2026.md` Section 3.9 with MIIT filing and CAC AI rules.
2. Add MIIT ICP filing number checks to `scripts/metadata-audit.py`.
3. Create automated guard detection rules for CAC minor chatbot restrictions in `scripts/monitor-ai-policy.py`.

---

## 21. Consolidated Gap Classification Matrix Across All 20 Regulations

The table below provides a complete, honest audit matrix of the playbook across all 20 global regulations and all 8 compliance dimensions.
- **Covered**: Fully documented, with detection rules, code templates, and tests.
- **Partial**: Named and cited with dates, but missing full implementation tools, code blocks, or automated tests.
- **Missing**: Completely absent from the repository.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU AI Act Art 5** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. EU EAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. US COPPA & Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. FTC Health & Subscription** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. California CPRA / CCPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. UK OSA & Children's Code**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Strategic Remediation Roadmap

This comprehensive audit of twenty major global regulations reveals that while the playbook provides strong legal background and official primary citations for most regulatory frameworks, significant operational gaps exist in the implementation layer: specifically native code templates, automated guard detection rules, structured logging schemas, and comprehensive CI integration tests.

### Priority Action Items
1. **Immediate (Phase 1):** Complete EU GPSR implementation across all 8 dimensions as the sole framework previously absent end-to-end.
2. **Short-Term (Phase 2):** Expand `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh` to add automated detection logic for BIPA, DPDPA, Australia eSafety, and CAC AI companion restrictions.
3. **Medium-Term (Phase 3):** Implement reusable code components for EU withdrawal buttons, C2PA watermarking for AI Act Article 50, and Global Privacy Control (GPC) header processing in reference templates.
4. **Long-Term (Phase 4):** Develop standardized database logging schemas for legal evidence retention, consent revocation tracking, and automated 72-hour breach notification workflows.

## 23. Official Primary Sources

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing Directive: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- FTC Health Breach Notification: [16 CFR Part 318](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-318)
- FTC Negative Option Rule: [16 CFR Part 425](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)
- UK Online Safety Act 2023: [Legislation.gov.uk](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Online Safety Act 2021: [Federal Register of Legislation](https://www.legislation.gov.au/Details/C2021A00076)
- Brazil Lei nº 15.211/2025 & Decreto nº 12.880/2026: [Planalto Presidência da República](https://www.planalto.gov.br/)
- India DPDPA 2023: [Gazette of India](https://egazette.gov.in/)
- Singapore PDPA & IMDA Code: [PDPC Singapore](https://www.pdpc.gov.sg/)
- China MIIT & CAC Order No. 21: [CAC Government Portal](http://www.cac.gov.cn/)
