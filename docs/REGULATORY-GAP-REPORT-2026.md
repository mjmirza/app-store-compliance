# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping across the European Union, United States, United Kingdom, Australia, Brazil, India, Singapore, South Korea, and China. It checks honestly how far this repository carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight core compliance gap categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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

## 7. US Children's Online Privacy Protection Act (Amended COPPA Rule)

### 7.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) published the Final Rule amending the Children's Online Privacy Protection Rule (16 CFR Part 312). The amended rule imposes heightened parental consent requirements, explicit opt-in mandates for targeted advertising and push notifications, strict data retention limits, and mandatory written information security programs for apps directed to children under 13 or actual knowledge child users.

Official Citation: FTC Final Rule, 16 CFR Part 312 (2025/2026).

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive COPPA Compliance Policy template covering third-party SDK consent, push notification gating, and data retention schedules.
- **Missing Documentation:**
  Developer guides do not detail how to configure SDK initialization flags (e.g., Google Mobile Ads `tagForChildDirectedTreatment`) across React Native and Flutter.
- **Missing Code:**
  Codebase templates do not contain age-gating screens or automated SDK disabling wrappers when a user is determined to be under 13.
- **Missing Disclosure:**
  Privacy notice templates omit mandatory FTC COPPA disclosures regarding operator details, data collection categories, and non-conditioning statements.
- **Missing Logging:**
  No database schemas exist for logging verifiable parental consent (VPC) methods, timestamps, or consent withdrawal events.
- **Missing Testing:**
  Test suites lack automated assertion scripts to verify that advertising IDs or geolocation permissions are suppressed for child accounts.
- **Missing Evidence:**
  The repository lacks templates for COPPA Safe Harbor self-assessments or annual third-party audit reports.
- **Missing Audit Trail:**
  There is no cryptographic audit trail to log parental consent approvals and data deletion requests for child user records.

### 7.3 Remediation and Action Plan
1. Add COPPA 2026 compliance checklists and SDK initialization code snippets.
2. Build mock age-gate and VPC verification handlers in sample codebases.
3. Implement automated test scripts to audit IDFA/GAID collection on child profiles.

---

## 8. California Consumer Privacy Act & CPPA Regulations (CPRA / ADMT)

### 8.1 Regulatory Overview and Background
The California Privacy Protection Agency (CPPA) finalized regulations under 11 CCR section 7200 regarding Automated Decision-Making Technology (ADMT), risk assessments, cybersecurity audits, and opt-out mechanisms for profiling in consumer-facing mobile applications.

Official Citation: California Code of Regulations, Title 11, Division 6, Chapter 1.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written ADMT Policy or California Privacy Policy template is provided in the playbook.
- **Missing Documentation:**
  Missing developer documentation detailing how to expose "Limit the Use of My Sensitive Personal Information" and ADMT opt-out toggles in app settings.
- **Missing Code:**
  No native or cross-platform code samples exist to parse and respect Opt-Out Preference Signals (such as Global Privacy Control / GPC).
- **Missing Disclosure:**
  In-app onboarding templates fail to disclose the logic, significance, and consequences of automated decision-making or profiling features.
- **Missing Logging:**
  No logging endpoints are provided to record consumer opt-out preferences or GPC signal processing events.
- **Missing Testing:**
  Test runners do not verify that ADMT features or targeted analytics are disabled when a consumer exercises their opt-out right.
- **Missing Evidence:**
  The repository lacks templates for CPPA Risk Assessments or Cybersecurity Audit filings.
- **Missing Audit Trail:**
  No audit trail system exists to maintain historical records of California consumer rights requests (DSARs) and fulfillment timestamps.

### 8.3 Remediation and Action Plan
1. Develop GPC signal listener middleware for mobile app templates.
2. Publish California ADMT disclosure guidelines and risk assessment templates.

---

## 9. Illinois Biometric Information Privacy Act (BIPA)

### 9.1 Regulatory Overview and Background
Illinois Biometric Information Privacy Act (740 ILCS 14), as amended, requires private entities collecting biometric identifiers (facial geometry, fingerprints, voiceprints) to obtain written release and publish retention schedules prior to collection.

Official Citation: Illinois General Assembly, 740 ILCS 14.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Biometric Data Retention and Destruction Policy template.
- **Missing Documentation:**
  No developer guide explains the distinction between device-local biometric auth (e.g., LocalAuthentication / BiometricPrompt) and remote biometric data collection.
- **Missing Code:**
  Codebases do not include BIPA-compliant written consent modal components or automatic deletion triggers upon user account termination.
- **Missing Disclosure:**
  Auth screens lack explicit BIPA disclosures detailing the specific biometric identifier collected and the retention duration.
- **Missing Logging:**
  No logging mechanism exists to store time-stamped written releases for biometric collection.
- **Missing Testing:**
  No unit or UI tests verify that biometric data capture is blocked prior to affirmative consent execution.
- **Missing Evidence:**
  The repository provides no example templates of valid BIPA written consent agreements.
- **Missing Audit Trail:**
  An immutable audit log for tracking biometric policy acceptance and destruction events is absent.

### 9.3 Remediation and Action Plan
1. Clarify local biometric SDK usage versus remote server storage in security docs.
2. Provide BIPA consent UI components and logging schemas.

---

## 10. US FTC Subscription Cancellation Rule ("Click-to-Cancel")

### 10.1 Regulatory Overview and Background
The Federal Trade Commission's Rule on Recurring Subscriptions and Negative Option Plans (16 CFR Part 425) mandates that negative option subscription cancellation mechanisms must be as easy to use as the enrollment mechanism ("Click-to-Cancel").

Official Citation: FTC Negative Option Rule, 16 CFR Part 425.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Subscription Renewal and Cancellation Policy is included.
- **Missing Documentation:**
  Documentation lacks concrete UI guidelines on avoiding dark patterns, save offers, or multi-step friction during cancellation.
- **Missing Code:**
  Sample app billing components do not provide a one-click self-service cancellation endpoint or UI route.
- **Missing Disclosure:**
  Paywall templates do not clearly disclose auto-renewal terms, billing amounts, and cancellation deadlines adjacent to the buy button.
- **Missing Logging:**
  No database log captures cancellation attempts, confirmations, or post-cancellation confirmation receipts.
- **Missing Testing:**
  Automated UI tests do not measure or verify the step count of the cancellation flow against the sign-up flow.
- **Missing Evidence:**
  The playbook lacks sample cancellation confirmation email templates and billing audit checklists.
- **Missing Audit Trail:**
  No audit trail records historical updates to paywall disclaimers or cancellation UI variations.

### 10.3 Remediation and Action Plan
1. Add FTC Click-to-Cancel UI patterns and automated step-count test validators.
2. Include clear paywall disclosure templates for iOS StoreKit and Google Play Billing.

---

## 11. UK Online Safety Act 2023 (UK OSA)

### 11.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (Ofcom regulations) imposes strict duties of care on user-to-user services and search services to prevent access by children to illegal or harmful content, mandating highly effective age assurance.

Official Citation: UK Online Safety Act 2023 (c. 50).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no UK Online Safety Act Compliance Policy or illegal content risk assessment template.
- **Missing Documentation:**
  No developer guide explains Ofcom's Age Assurance Principles or mandatory reporting procedures for illegal content.
- **Missing Code:**
  Codebases lack content moderation hooks or integration adapters for UK-approved age verification providers.
- **Missing Disclosure:**
  Terms of Service templates lack UK OSA risk warnings and age-restriction disclaimers.
- **Missing Logging:**
  No logging endpoints exist for user safety reports, illegal content takedowns, or age check verifications.
- **Missing Testing:**
  Test suites do not simulate age-gating enforcement or toxic content blocking for UK IP addresses.
- **Missing Evidence:**
  The repository provides no templates for Ofcom Risk Assessments or child safety compliance reports.
- **Missing Audit Trail:**
  There is no audit trail to track content moderation decisions or safety policy revisions.

### 11.3 Remediation and Action Plan
1. Add UK OSA risk assessment templates and Ofcom compliance guidelines.
2. Implement content report and moderation logging schemas in sample backends.

---

## 12. UK ICO Children's Code (Age Appropriate Design Code)

### 12.1 Regulatory Overview and Background
The UK Information Commissioner's Office (ICO) Age Appropriate Design Code establishes 15 standards of age-appropriate design for online services likely to be accessed by children under 18.

Official Citation: ICO Age Appropriate Design Code (Section 123 of the Data Protection Act 2018).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a written Children's Code Compliance Policy addressing high-privacy default settings.
- **Missing Documentation:**
  Developer docs do not explain how to configure default "off" settings for geolocation, profiling, and nudge techniques for UK minor users.
- **Missing Code:**
  Code templates do not automatically set maximum privacy defaults upon identifying a minor user.
- **Missing Disclosure:**
  Bite-sized privacy notices tailored to child comprehension levels are absent from app templates.
- **Missing Logging:**
  No logging framework exists to confirm that default privacy settings were applied upon account creation.
- **Missing Testing:**
  Automated tests do not verify that nudge features (e.g., streak rewards) are disabled for child accounts.
- **Missing Evidence:**
  The playbook lacks ICO Data Protection Impact Assessment (DPIA) templates for child data processing.
- **Missing Audit Trail:**
  No system tracks changes to default privacy configurations or child privacy impact assessments.

### 12.3 Remediation and Action Plan
1. Create DPIA templates specifically for child-directed features.
2. Publish UI components with high-privacy default configurations.

---

## 13. Australia Online Safety Amendment & Social Media Minimum Age

### 13.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 and associated eSafety Codes enforce a mandatory minimum age of 16 for specified social media platforms and app distribution services in Australia.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No policy template exists for Australian social media age restrictions or eSafety Code compliance.
- **Missing Documentation:**
  Missing documentation on integration with Australian age assurance frameworks.
- **Missing Code:**
  Sample apps lack age verification logic to restrict users under 16 in Australia.
- **Missing Disclosure:**
  No onboarding disclosure warns Australian users under 16 of access restrictions.
- **Missing Logging:**
  No secure system logs age attestation or exemption events for Australian accounts.
- **Missing Testing:**
  No integration tests simulate Australian IP routing and under-16 account blocking.
- **Missing Evidence:**
  The repository lacks evidence templates for eSafety Commissioner compliance reviews.
- **Missing Audit Trail:**
  No audit trail tracks social media age-gate deployment and exception handling.

### 13.3 Remediation and Action Plan
1. Add Australia eSafety Code rules to rejection patterns and pre-submission checklists.
2. Implement mock age attestation logic for Australian regional settings.

---

## 14. Australia Privacy Act ADM Disclosures & Children's Code

### 14.1 Regulatory Overview and Background
The Privacy and Other Legislation Amendment Act 2024 introduces Australian Privacy Principles (APP 1.7-1.9) requiring explicit disclosures on Automated Decision-Making (ADM) and the upcoming Children's Online Privacy Code.

Official Citation: Privacy Act 1988 (Cth), as amended in 2024.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template ADM Disclosure Policy for Australian operations is provided.
- **Missing Documentation:**
  Missing developer guidelines on identifying and documenting ADM algorithms affecting individuals.
- **Missing Code:**
  Codebases lack ADM disclosure banners or privacy setting controls for ADM profiling.
- **Missing Disclosure:**
  Privacy notice templates do not include mandatory APP 1.7 statements regarding automated decisions.
- **Missing Logging:**
  No logging endpoint records ADM execution or privacy preference updates for Australian users.
- **Missing Testing:**
  Test scripts do not verify that ADM disclosures appear on relevant decision-making flows.
- **Missing Evidence:**
  The playbook lacks Privacy Impact Assessment (PIA) templates for Australian ADM features.
- **Missing Audit Trail:**
  No audit log maintains versioned histories of ADM algorithmic logic and privacy disclosures.

### 14.3 Remediation and Action Plan
1. Incorporate APP 1.7 ADM disclosure templates in mobile privacy guides.
2. Add Australian PIA templates to the documentation tree.

---

## 15. Brazil Digital ECA & Decreto 12.880

### 15.1 Regulatory Overview and Background
Brazil's Law 15,211/2025 (Digital ECA) and Decreto 12.880 of 18 March 2026 mandate child safety measures, parental supervision tools, age verification signals, and ANPD enforcement roadmaps for digital products.

Official Citation: Federal Law No. 15,211/2025 and Decreto No. 12,880/2026.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template addresses Brazil Digital ECA or ANPD child safety guidelines.
- **Missing Documentation:**
  Developer docs lack instructions for integrating Brazilian age signal mechanisms.
- **Missing Code:**
  Sample apps do not contain parental control tools or age signal parsers for Brazilian users.
- **Missing Disclosure:**
  Onboarding templates omit Portuguese disclosures regarding minor data protection under Digital ECA.
- **Missing Logging:**
  No logging framework stores parental consent or supervisor authorization records in Brazil.
- **Missing Testing:**
  Test runners do not test Portuguese age-gating strings or minor account restriction flows.
- **Missing Evidence:**
  The playbook provides no templates for ANPD Compliance Reports.
- **Missing Audit Trail:**
  No audit trail records parental supervisor linkings or minor account status changes.

### 15.3 Remediation and Action Plan
1. Add Digital ECA rules to global regulatory documentation and rejection patterns.
2. Provide Portuguese language disclosure templates and age signal integration samples.

---

## 16. India Digital Personal Data Protection Act (DPDPA 2023 / Rules 2025)

### 16.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 mandate verifiable parental consent for processing children's data, registration of Consent Managers, multi-language consent notices, and strict breach reporting.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPDP Rules 2025.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an India DPDPA Data Fiduciary Policy template.
- **Missing Documentation:**
  Missing technical guides on integrating with registered Consent Managers under Rule 4.
- **Missing Code:**
  Codebases lack multi-lingual consent screen components (covering 22 scheduled languages) or Consent Manager API hooks.
- **Missing Disclosure:**
  Consent notice templates do not provide clear explanations in specified languages as required under DPDPA Section 5.
- **Missing Logging:**
  No logging mechanism records consent itemization or withdrawal requests processed via Consent Managers.
- **Missing Testing:**
  Test scripts do not verify multi-language rendering or Consent Manager callback handling.
- **Missing Evidence:**
  The playbook lacks Data Protection Impact Assessment templates for Significant Data Fiduciaries in India.
- **Missing Audit Trail:**
  No immutable audit trail logs consent histories, withdrawal events, and breach notifications.

### 16.3 Remediation and Action Plan
1. Add DPDPA Consent Manager integration guides and multi-lingual disclosure frameworks.
2. Build sample consent artifact logging endpoints.

---

## 17. Singapore IMDA Code of Practice for Online Safety & OSRAA

### 17.1 Regulatory Overview and Background
Singapore's IMDA Code of Practice for Online Safety for App Distribution Services and OSRAA 2025 enforce child safety standards, age-appropriate content ratings, and reporting protocols for harmful online content.

Official Citation: IMDA Code of Practice for Online Safety and OSRAA 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore IMDA Online Safety Policy template is provided.
- **Missing Documentation:**
  Developer guidelines lack detailed instructions on complying with IMDA app store age rating alignment.
- **Missing Code:**
  Codebases lack content reporting tools and age-gating filters configured for Singapore standards.
- **Missing Disclosure:**
  App templates lack required Singapore age rating disclaimers and safety guidelines.
- **Missing Logging:**
  No logging schema exists for user reports submitted under OSRAA safety provisions.
- **Missing Testing:**
  Test suites do not check content restriction triggers against Singapore rating guidelines.
- **Missing Evidence:**
  The repository lacks templates for IMDA Annual Online Safety Assessments.
- **Missing Audit Trail:**
  No audit trail records content moderation responses to IMDA notices.

### 17.3 Remediation and Action Plan
1. Document IMDA safety code requirements in app store compliance guides.
2. Provide content moderation logging schemas.

---

## 18. South Korea Telecommunications Business Act & Amended PIPA

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options, while the amended PIPA (Act No. 21445) strictly regulates automated decision-making and cross-border data transfers.

Official Citation: Telecommunications Business Act Article 22-9 and PIPA Act No. 21445.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No policy template addresses South Korean third-party payment options or PIPA cross-border transfers.
- **Missing Documentation:**
  Missing step-by-step developer guide for implementing One Store or third-party Korean payment gateways alongside Kakao/Naver login requirements.
- **Missing Code:**
  Sample codebases do not include South Korean alternative payment UI flows or PIPA consent popups.
- **Missing Disclosure:**
  Paywall templates omit mandatory Korean payment processing disclaimers and cross-border data transfer disclosures.
- **Missing Logging:**
  No logging endpoint captures Korean payment selection events or PIPA consent logs.
- **Missing Testing:**
  Test scripts do not verify Korean payment gateway initialization or consent modal rendering.
- **Missing Evidence:**
  The repository lacks PIPC (Personal Information Protection Commission) audit compliance templates.
- **Missing Audit Trail:**
  No audit log tracks third-party payment transaction reporting or cross-border consent revisions.

### 18.3 Remediation And Action Plan
1. Add Korean alternative payment gateway guidelines and PIPA compliance documentation.
2. Implement Korean language consent templates and payment selection UI logic.

---

## 19. China MIIT Mobile App Filing & CAC AI Interim Measures

### 19.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates ICP app filing for distribution, while CAC Order No. 21 establishes Interim Measures for AI Anthropomorphic Interactive Services for minors.

Official Citations: MIIT Circular on App ICP Filing (2023) and CAC Order No. 21 (2026).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template covers China ICP filing prerequisites or CAC AI companion regulations.
- **Missing Documentation:**
  Documentation lacks developer instructions on displaying ICP filing numbers in app store listings and metadata.
- **Missing Code:**
  Codebases lack real-name verification (ID matching) modules and anti-addiction time limit locks required for minors in China.
- **Missing Disclosure:**
  In-app about screens omit required MIIT ICP license display numbers and CAC AI disclaimers.
- **Missing Logging:**
  No backend logging handles real-name verification status tokens or anti-addiction session tracking.
- **Missing Testing:**
  Test suites do not simulate anti-addiction curfew shutdowns or ICP number verification checks.
- **Missing Evidence:**
  The playbook lacks templates for MIIT App Filing submission forms or CAC Security Assessments.
- **Missing Audit Trail:**
  No audit trail records real-name authentication events or CAC algorithm filing updates.

### 19.3 Remediation and Action Plan
1. Include MIIT ICP filing checklists in regional store deployment docs.
2. Document CAC AI safety requirements for interactive AI applications.

---

## 20. EU Cyber Resilience Act & EU Data Act

### 20.1 Regulatory Overview and Background
The Cyber Resilience Act (Regulation (EU) 2024/2847) mandates security-by-design, vulnerability reporting within 24 hours to ENISA, and SBOM management. The Data Act (Regulation (EU) 2023/2854) mandates user data accessibility and interoperability.

Official Citations: Regulation (EU) 2024/2847 (CRA) and Regulation (EU) 2023/2854 (Data Act).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No CRA Vulnerability Management Policy or Data Act Sharing Policy template exists in the playbook.
- **Missing Documentation:**
  Missing developer guides on generating Software Bill of Materials (SBOM) or implementing Data Act user data export APIs.
- **Missing Code:**
  Sample backends lack automated SBOM generation scripts or user data porting endpoints.
- **Missing Disclosure:**
  Privacy policies fail to disclose Data Act rights regarding connected device data access.
- **Missing Logging:**
  No logging framework exists for recording security vulnerability reports or ENISA notifications.
- **Missing Testing:**
  Test suites do not validate automated vulnerability scanning or data export payload formats.
- **Missing Evidence:**
  The repository lacks templates for CRA Conformity Assessments or SBOM artifacts.
- **Missing Audit Trail:**
  No audit log tracks reported security vulnerabilities, patch deployments, and ENISA notifications.

### 20.3 Remediation and Action Plan
1. Add CRA security requirements and SBOM generation scripts to mobile security playbooks.
2. Provide Data Act export interface guidelines and compliance checklists.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. California CPRA / ADMT** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US FTC Subscription** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. UK ICO Children's Code**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. Australia Social Media Age**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Australia Privacy ADM** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. India DPDPA Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Singapore IMDA / OSRAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. S. Korea Telecom / PIPA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China MIIT / CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. EU CRA / Data Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Modern regional and global frameworks are documented in high-level policy guides and deadline files, but the repository still lacks complete code, logging, testing, evidence, and audit trail implementations for end-to-end enforcement across all twenty regulations.

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. All twenty frameworks here are named with dated sources across `data/regulatory-deadlines.json`, `docs/EU-REGULATORY-2026.md`, and `docs/GLOBAL-REGULATORY-2026.md`. What is missing across the board is the concrete technical layer a developer can act on: detection rules the guard can fire on, code templates they can paste, logging schemas, and tests that prove compliance.

In priority order.

1. Add GPSR, the only framework absent end to end.
2. Give all nineteen Partial frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates and logging schemas, starting with AI Act Article 50 disclosures, COPPA age gating, and FTC subscription cancellation paths.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex, FTC, Ofcom, ANPD, and other primary sources rather than trusting the dates here on their own.

---

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Amended COPPA Rule, [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California CPPA Regulations, [11 CCR section 7200](https://cppa.ca.gov/regulations/)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- FTC Negative Option Rule, [16 CFR Part 425](https://www.ftc.gov/news-events/news/press-releases/2024/10/federal-trade-commission-announces-final-click-cancel-rule)
- UK Online Safety Act 2023, [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- UK ICO Children's Code, [ICO Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- Australia Online Safety Act, [Federal Register of Legislation](https://www.legislation.gov.au/)
- Brazil Digital ECA, [Lei No. 15.211/2025 and Decreto No. 12.880/2026](https://www.planalto.gov.br/)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Cyber Resilience Act, [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- EU Data Act, [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)

The US state App Store Accountability Acts are cited to their bill texts in [docs/GLOBAL-REGULATORY-2026.md](GLOBAL-REGULATORY-2026.md), which is the source of record for that section rather than this report.
