# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind app developers shipping into various global markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The Digital Markets Act (DMA), Regulation (EU) 2022/1925, applies to systemic gatekeepers and seeks to ensure contestable and fair markets in the digital sector. For mobile developers, it forces platforms like Apple and Google to permit alternative application stores, direct web distribution, and alternative payment solutions outside of traditional in-app purchases.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy templates are provided to help developers analyze whether their applications are eligible for alternative EU distribution channels, or how to handle direct-to-consumer payments.
- **Missing Documentation:**
  The repository is missing step-by-step documentation detailing the technical steps required to configure alternate web distribution domains, alternative browser engines, or alternate payment entitlements under DMA.
- **Missing Code:**
  The pre-submission checks do not dynamically verify that code blocks targeting alternate payment systems correctly interface with Apple's `ExternalPurchaseCustomLink` APIs or respect alternative payment restrictions.
- **Missing Disclosure:**
  There are no template user interfaces displaying standard disclosures when navigating users away from platform billing to external websites for billing.
- **Missing Logging:**
  No schemas or database scripts are provided to compile alternate transaction logs in the specific format required for Apple's mandatory monthly reporting cycles.
- **Missing Testing:**
  The test suites lack simulations for testing out-of-app payment redirects or capturing external checkout data under custom routing configurations.
- **Missing Evidence:**
  The repository has no templates for DMA transaction audit receipts or CSV schemas prepared for gatekeeper financial audits.
- **Missing Audit Trail:**
  No audit log tracks changes to payment configurations, alternative payment gateways, or reporting history.

### 7.3 Remediation and Action Plan
1. Draft an Alternate Payment and Steerage Policy mapping out compliance with gatekeeper requirements.
2. Build standardized frontend modules that trigger the required system-level disclosure sheets before initiating external payment routing.
3. Design database tables and scheduled scripts to aggregate transaction data into compliant monthly reports.
4. Incorporate automated integration tests checking for illegal mixing of IAP and external payments on the same EU storefront.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes a comprehensive framework for online platforms to combat illegal content, protect user rights, and enforce seller transparency. A critical operational rule is the verification and public display of "trader status" for merchants selling to EU users.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate policy templates or classification flows exist to help small teams define if they legally constitute a "trader" under Article 30.
- **Missing Documentation:**
  The repository lacks guides explaining how to configure corporate registry documentation, verified contact phone numbers, and payment details in store developer accounts.
- **Missing Code:**
  The pre-submission static analysis does not scan project configuration files or fastlane files for the presence of mandatory trader-related metadata.
- **Missing Disclosure:**
  Public-facing settings screens and "About" screens lack template placeholders for displaying verified trader contact information, registry indices, and compliance certifications.
- **Missing Logging:**
  The repository is missing database models or schemas for tracking user content reports, content moderation notices, or takedown actions.
- **Missing Testing:**
  No integration tests exist to verify that required trader details are dynamically visible to users based on geographic IP filters.
- **Missing Evidence:**
  No templates are provided to demonstrate successful identity verification (e.g., D-U-N-S receipts, corporate identity uploads).
- **Missing Audit Trail:**
  The repository lacks a content moderation audit trail tracking illegal content notices, internal appeals, and takedown justifications.

### 8.3 Remediation and Action Plan
1. Formulate an internal Trader Classification Guide and content notice/takedown policy.
2. Add placeholder layout sections in Settings UI references to display verified corporate address, registration number, phone, and email.
3. Build a standardized content notice-and-action logging table to document illegal content submissions.
4. Establish automated tests verifying that store-facing metadata matches corporate registries.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable on 28 June 2025. It mandates accessibility for key digital products and services, including e-commerce, banking, transport booking, and electronic communications software distributed to EU consumers.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository has no written accessibility policy template or structured development policy referencing harmonised standard EN 301 549.
- **Missing Documentation:**
  The playbook lists accessibility rules, but lacks a detailed technical manual describing the 64 requirements of EN 301 549 Chapter 11 and how they go beyond basic WCAG 2.1 AA.
- **Missing Code:**
  Automated checks are restricted to static lints; there are no platform-specific code wrappers to programmatically track isDarkerSystemColorsEnabled or scale Dynamic Type elements.
- **Missing Disclosure:**
  No UI template is provided for a published EAA-compliant Accessibility Statement or in-app feedback channel.
- **Missing Logging:**
  No database or file schemas exist to collect, classify, and track user accessibility complaints or feature requests.
- **Missing Testing:**
  Automated tests only check scanner functionality; there are no end-to-end user interface automation tests (e.g. running VoiceOver or TalkBack simulations) checking navigation focus orders.
- **Missing Evidence:**
  The repository lacks template Voluntary Product Accessibility Templates (VPAT) or accessibility compliance reports.
- **Missing Audit Trail:**
  No audit log tracks regression test history, accessibility audits, or manual testing runs.

### 9.3 Remediation and Action Plan
1. Publish an internal EAA compliance policy establishing EN 301 549 as the technical development bar.
2. Provide a standardized, reachable Accessibility Statement template to be published within all apps.
3. Build native UI wrappers demonstrating dynamic layout constraints adjusting to high-contrast and font-scaling settings.
4. Design automated screen reader navigation integration tests.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, enforces privacy protection for children under 13. The FTC's amended COPPA Rule (general compliance date 22 April 2026) expands personal information to include biometric, genetic, voice, and gait data, mandates separate opt-ins for targeted ads, and demands written retention policies and written information-security programs.

Official Citation: 16 CFR Part 312, Children's Online Privacy Protection Rule.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing a template COPPA data retention policy and lacks a written information-security program template.
- **Missing Documentation:**
  No technical integration manuals are provided detailing how to implement advanced consent methods (e.g. face matching) or how to restrict tracking SDKs when a child is detected.
- **Missing Code:**
  The codebase has no frontend templates showing age-verification gates or conditional SDK initialization wrappers.
- **Missing Disclosure:**
  Onboarding templates lack distinct, separate opt-in checkboxes for third-party disclosures and behavioral advertising.
- **Missing Logging:**
  No secure database schemas are supplied to log parental consent approvals, consent revocations, or the automated destruction of age data.
- **Missing Testing:**
  No unit or integration tests simulate child onboarding or verify that ad-trackers are completely deactivated upon age detection.
- **Missing Evidence:**
  The repository lacks templates for Child Privacy Impact Assessments (CPIAs).
- **Missing Audit Trail:**
  There is no secure logging system to track consent lifecycle history or data minimization executions.

### 10.3 Remediation and Action Plan
1. Create written COPPA Data Retention and Information Security Program templates.
2. Develop dynamic age-gate components that conditionalize SDK tracking (e.g. deactivating IDFA/AAID) based on age bands.
3. Build database triggers to automatically purge raw age verification inputs immediately post-validation.
4. Implement automated testing suites to verify child privacy compliance during deployment.

---

## 11. California Privacy (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), regulates the collection and processing of California residents' personal data. The CPPA's 2026 regulations enforce strict rules on collection notices, opt-outs of data sales/sharing, and the dynamic honoring of Global Privacy Control (GPC) browser signals.

Official Citation: California Civil Code Section 1798.100 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no CCPA-compliant privacy policy templates, notices at collection, or employee privacy policy structures.
- **Missing Documentation:**
  No technical guides explain how to configure dynamic "Do Not Sell or Share My Info" or "Limit Sensitive Personal Info" controls inside native applications.
- **Missing Code:**
  The repository lacks code to process Global Privacy Control (GPC) headers (`Sec-GPC`) in webviews or to propagate opt-out signals to tracking libraries.
- **Missing Disclosure:**
  No settings screens or footer templates are provided containing compliant "Do Not Sell" and "Limit Sensitive PI" links.
- **Missing Logging:**
  No logging modules exist to record opt-out requests, deletion requests, or consent statuses.
- **Missing Testing:**
  No automated integration tests check if tracking pixels are blocked when GPC signals are active.
- **Missing Evidence:**
  No templates are supplied for data inventory sheets or metrics reporting.
- **Missing Audit Trail:**
  There is no secure system to trace California consumer rights request (DSAR) lifecycles.

### 11.3 Remediation and Action Plan
1. Create a written CCPA/CPRA Privacy Policy and Notice at Collection template.
2. Programmatically monitor GPC signals and disable tracking SDKs conditionally when GPC is detected.
3. Add a standardized "Privacy Center" UI component with clear opt-out and limitation buttons.
4. Set up an immutable request log to track DSAR compliance deadlines.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, imposes strict requirements on the collection, storage, and use of biometric identifiers (fingerprints, retina scans, facial geometry). It mandates written policies, public retention schedules, explicit written releases, and enforces severe statutory damages with a private right of action.

Official Citation: 740 ILCS 14, Biometric Information Privacy Act.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written BIPA policy, public retention schedule, or biometric destruction templates are present in the repository.
- **Missing Documentation:**
  The playbook lacks technical manuals explaining the process of obtaining written releases prior to biometric enrollment.
- **Missing Code:**
  There are no UI templates or backend hooks illustrating secure biometric enrollment or the local hashing of facial/fingerprint data.
- **Missing Disclosure:**
  No onboarding screens exist with explicit, signed-consent releases detailing the purpose, storage timeline, and destruction schedule of biometric details.
- **Missing Logging:**
  No schemas are provided to record the exact date of biometric enrollment and the tracking of the signed release version.
- **Missing Testing:**
  No automated tests exist to verify that biometric login flows are blocked if the biometric consent has not been actively signed.
- **Missing Evidence:**
  The repository is missing template biometric release forms and self-audit compliance checklists.
- **Missing Audit Trail:**
  No unalterable logs track biometric record lifecycles, deletion dates, or verification records.

### 12.3 Remediation and Action Plan
1. Write a BIPA Biometric Policy and Consent template.
2. Implement a pre-enrollment dialog component that forces the user to sign a biometric release.
3. Develop database tables to record the release signature dates and automate deletion tasks after three years.
4. Establish tests to block access to biometric APIs until a valid signed consent flag is verified.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA), along with state negative-option statutes (e.g. California, New York, Massachusetts), requires online merchants to provide extremely clear auto-renewal disclosures, obtain informed consent before charging, and offer a simple, self-service cancellation mechanism that is "at least as easy as signing up" (click-to-cancel).

Official Citation: 15 U.S.C. Section 8401 et seq., and California Business and Professions Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a negative-option billing compliance policy template.
- **Missing Documentation:**
  No guidelines are provided for designing frictionless subscription cancellation flows for custom-billed or web-billed accounts.
- **Missing Code:**
  The repository lacks frontend or backend code executing a self-service cancellation path for non-IAP payments.
- **Missing Disclosure:**
  No paywall templates exist that clearly display auto-renewal terms, recurring pricing, billing cycles, or cancellation links.
- **Missing Logging:**
  No logging structures are provided to capture cancellation interactions, refund events, or subscription status updates.
- **Missing Testing:**
  No tests simulate a user initiating a subscription and successfully executing a single-click cancellation.
- **Missing Evidence:**
  The repository contains no template cancellation receipt models or compliance self-evaluation logs.
- **Missing Audit Trail:**
  No audit trail tracks billing change histories or subscription terms updates.

### 13.3 Remediation and Action Plan
1. Draft a corporate Negative Option Billing Policy.
2. Design a frictionless "Manage Subscription" paywall settings UI featuring a single-click, self-service "Cancel Subscription" button.
3. Build transaction tracking tables to record cancellation requests, timestamps, and execution confirmations.
4. Integrate automated end-to-end UI tests verifying that subscriptions can be successfully cancelled without customer support intervention.

---

## 14. UK Online Safety Act (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 enforces duties on services likely to be accessed by children to prevent exposure to illegal and harmful content. Enforced by Ofcom, the law expects providers to implement "Highly Effective Age Assurance" (such as facial age estimation or bank checks) and destroy verification data post-verification.

Official Citation: UK Online Safety Act 2023.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template UK child-safety policies or Ofcom response frameworks are included.
- **Missing Documentation:**
  The repository lacks technical documentation on integrating UK-compliant age estimation APIs or handling data minimization.
- **Missing Code:**
  No codebase integrations or SDK adapters exist to interface with third-party age verification vendors.
- **Missing Disclosure:**
  Onboarding templates do not display UK-friendly age-verification privacy notices.
- **Missing Logging:**
  No database schemas are provided to log content moderation, harmful content reports, or age check events.
- **Missing Testing:**
  No tests verify that under-18 accounts are programmatically blocked from accessing restricted features.
- **Missing Evidence:**
  No templates are supplied for UK Online Safety Risk Assessments.
- **Missing Audit Trail:**
  No audit log tracks content moderation decisions or age assurance verification histories.

### 14.3 Remediation and Action Plan
1. Create a written UK Online Safety Policy and Ofcom compliance runbook.
2. Add API integration templates for third-party facial age estimation providers.
3. Implement database schemas to log user content reports and subsequent moderation outcomes.
4. Build automated checks ensuring UK users are routed to highly effective age-assurance gates.

---

## 15. Australia Online Safety (Social Media Minimum Age) Act

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 prohibits children under 16 from holding accounts on social media platforms. It requires providers to take "reasonable steps" using robust age-assurance methods to block access and immediately destroy age data post-verification.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template is provided for Australian minor restrictions or data destruction standards.
- **Missing Documentation:**
  No guidelines exist for integrating with Australian digital identity systems or managing age assurance waterfalls.
- **Missing Code:**
  The repository contains no code blocks interfacing with digital ID providers or executing instant data-purge commands.
- **Missing Disclosure:**
  Signup templates do not disclose to Australian users the age verification process or the immediate data destruction rule.
- **Missing Logging:**
  No database tables exist to log age check outcomes without retaining raw, personal verification details.
- **Missing Testing:**
  The test suites do not check if Australian IP-based signups block minor registration.
- **Missing Evidence:**
  No templates are provided for Australian age verification audits.
- **Missing Audit Trail:**
  The codebase lacks secure logs tracing verification outcomes and the execution of data destruction triggers.

### 15.3 Remediation and Action Plan
1. Write an Australian Minor Age Assurance Policy.
2. Build frontend onboarding screens that screen out users under 16 using Australia-specific gating disclosures.
3. Code automated transaction scripts to purge raw verification data immediately following verification.
4. Establish integration tests to simulate underage registration blocks.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) enforces strict age verification requirements for digital platforms to protect children. Under LGPD guidance, self-declaration checkboxes are prohibited; platforms must utilize robust methods like document matching, CPF checks, or facial estimation, and ensure age data is immediately deleted.

Official Citation: Law No. 15,211/2025 (Digital ECA).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written compliance templates are provided for Brazil's Digital ECA or LGPD minor protections.
- **Missing Documentation:**
  The repository has no guidelines on Brazilian age assurance mechanisms, such as CPF (Cadastro de Pessoas Físicas) database queries.
- **Missing Code:**
  No code examples exist to call CPF validation services or integrate Brazilian age estimation tools.
- **Missing Disclosure:**
  Onboarding templates lack Brazilian Portuguese age gating disclosures.
- **Missing Logging:**
  No schemas are provided to log verified age bands while ignoring raw CPF or document inputs.
- **Missing Testing:**
  No tests exist to ensure Brazilian accounts are restricted from mature content or loot-box mechanics.
- **Missing Evidence:**
  No templates are supplied for ANPD (Autoridade Nacional de Proteção de Dados) data protection impact reports.
- **Missing Audit Trail:**
  The repository has no audit trail tracing age verification attempts, results, or document purging.

### 16.3 Remediation and Action Plan
1. Formulate a Brazilian Portuguese Digital ECA compliance policy.
2. Develop frontend modules showing mandatory age-verification screens for Brazil.
3. Implement CPF database check API connectors with strict data retention limits.
4. Add integration tests verifying mature content locking for underage Brazilian accounts.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
The Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025, requires verifiable parental consent before processing data of children (defined as under 18) and strictly prohibits behavioral tracking or targeted advertising to minors.

Official Citation: Digital Personal Data Protection Act 2023.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template is provided for India's DPDPA or children's behavioral tracking bans.
- **Missing Documentation:**
  The repository lacks developer manuals on Indian verifiable parental consent frameworks (e.g. DigiLocker integration).
- **Missing Code:**
  No code modules or API connectors are available to integrate Indian government-backed consent systems.
- **Missing Disclosure:**
  Consent screens do not display mandatory bilingual notices explaining data processing purposes.
- **Missing Logging:**
  No backend databases exist to log Indian consent manager authorizations or parental approvals.
- **Missing Testing:**
  No automated tests verify that tracking pixels (e.g. Meta, Google Analytics) are completely deactivated for Indian minors.
- **Missing Evidence:**
  No templates are provided for DPDPA data audits or consent management contracts.
- **Missing Audit Trail:**
  No unalterable logs track Indian consent acquisition, revocation, or parent-child validations.

### 17.3 Remediation and Action Plan
1. Create an India DPDPA Compliance Policy and child tracking ban roadmap.
2. Build consent UI screens displaying bilingual information (English and scheduled regional languages).
3. Implement backend switches that block behavioral tracking pixels when Indian minor status is flagged.
4. Establish logging tables to store parent consent records securely.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Online Safety

### 18.1 Regulatory Overview and Background
Singapore's PDPA, alongside the IMDA Code of Practice for Online Safety, mandates robust age-assurance measures for app distribution services. It requires platforms and apps to screen and block users under 18 from downloading age-inappropriate content, while ensuring verification data is destroyed immediately post-verification.

Official Citation: Personal Data Protection Act 2012, and IMDA Code of Practice.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate policy templates are included for Singapore's PDPA or IMDA Online Safety guidelines.
- **Missing Documentation:**
  No developer manuals explain the Singapore 18-plus download block or data destruction timelines.
- **Missing Code:**
  No code examples are provided to connect with Singapore's national digital identity system (Singpass) or local age-assurance systems.
- **Missing Disclosure:**
  Onboarding flows do not disclose Singapore age-gating mechanisms or data retention limits.
- **Missing Logging:**
  No database schemas log age verification events while guaranteeing immediate raw data destruction.
- **Missing Testing:**
  No tests check if Singapore storefront downloads remain locked until adult verification is confirmed.
- **Missing Evidence:**
  No templates are supplied for PDPC-compliant Data Protection Impact Assessments (DPIAs).
- **Missing Audit Trail:**
  No audit trail exists tracking PDPA consent history or automated age-verification log purges.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA and IMDA compliance handbook.
2. Design frontend onboarding workflows that trigger age assurance disclosures for Singapore users.
3. Build Singpass API integration templates for secure, official age verification.
4. Write cron scripts to automate the destruction of age-gating session data.

---

## 19. South Korea Telecommunications Business Act (Alternative Billing)

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (TBA) mandates that major app store operators allow developers to offer alternative in-app payment systems. Developers utilizing this must comply with specific guidelines, including a 26% commission, a Korea-only binary, strict co-mingling bans, and monthly transaction reporting.

Official Citation: South Korea Telecommunications Business Act.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate billing policy templates are provided for South Korean alternative billing.
- **Missing Documentation:**
  The playbook mentions alternative payments but lacks a technical guide on configuring South Korean binaries or payment providers (KCP, Toss, NICE, Inicis).
- **Missing Code:**
  No code blocks execute the mandatory 26% alternative billing commission calculations or render the required system payment modal sheets.
- **Missing Disclosure:**
  No UI templates include the South Korean alternative billing warning disclosures before redirecting to alternative payments.
- **Missing Logging:**
  No database schemas are provided to log and format the monthly South Korean transaction records required within 15 days of fiscal month-end.
- **Missing Testing:**
  No tests simulate alternative payment flows or verify that Korea-specific builds restrict billing correctly.
- **Missing Evidence:**
  The repository lacks standard CSV logs or submission formats for KCC (Korea Communications Commission) compliance checks.
- **Missing Audit Trail:**
  No audit log tracks alternative payment enablement, configurations, or transaction reporting histories.

### 19.3 Remediation and Action Plan
1. Formulate a South Korean Alternative Payment and Reporting Policy.
2. Develop frontend modal warning dialogues before initializing South Korean billing gateways.
3. Code monthly sales aggregation scripts formatted to meet Apple/Google Korea specifications.
4. Establish test files to simulate payment routing through certified South Korean providers.

---

## 20. China Mobile App Filing (MIIT)

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) of China mandates that all mobile apps operating in China undergo official app filing (ICP extension). Non-filed apps are removed from Chinese storefronts. This requires local partner entities, Computer Software Copyright certificates, real-name registration, PIPL privacy compliance, and data localization.

Official Citation: MIIT Circular on Implementing Mobile Internet Application Filing (2023).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template policy exists for Chinese MIIT app filings or coordinating with Chinese local entities.
- **Missing Documentation:**
  The repository lacks guides detailing the paperwork needed for filings (such as copyright certificates or Banhao game license applications).
- **Missing Code:**
  No codebase helper functions display the mandatory MIIT filing number dynamically on app launch screens or settings.
- **Missing Disclosure:**
  Onboarding flows lack PIPL-compliant disclosures or real-name registration warning templates.
- **Missing Logging:**
  No backend database schemas are provided to store real-name verification statuses or log data localization paths.
- **Missing Testing:**
  No tests check if the Chinese build displays the mandatory filing number on the launch interface.
- **Missing Evidence:**
  The repository has no checklists to aggregate business certificates or domain ownership records for MIIT submissions.
- **Missing Audit Trail:**
  No secure audit log tracks MIIT filing approval statuses, filing numbers, or local data audit records.

### 20.3 Remediation and Action Plan
1. Write a corporate China Storefront and MIIT Filing Policy.
2. Build UI elements that dynamically display the registered MIIT filing number at the bottom of the startup screen on Chinese builds.
3. Design database systems to enforce local data storage (data localization) and verify real-name verification flags.
4. Setup automated pipeline lints to block China storefront releases lacking filing numbers.

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
| **EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **California Privacy** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **South Korea TBA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **China Mobile App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Most of these regulations are already named in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`, with dated sources and a deadline entry. What they lack is the implementation layer, meaning detection rules in the guard, code templates, and tests. GPSR is the only one absent end to end, so it is the first thing to add.

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most frameworks here are already named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order.

1. Add GPSR, the only framework absent end to end.
2. Give the remaining frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates, starting with the AI Act Article 50 disclosure line and the withdrawal path, since both carry 2026 deadlines.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

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
- Children's Online Privacy Protection Rule, [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California Consumer Privacy Act, [Cal. Civ. Code Section 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5)
- Biometric Information Privacy Act, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- Restore Online Shoppers' Confidence Act, [15 U.S.C. Section 8401](https://www.govinfo.gov/app/details/USCODE-2011-title15/USCODE-2011-title15-chap110)
- UK Online Safety Act 2023, [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Online Safety Amendment Act 2024, [Parliament of Australia Bill Page](https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId=r7245)
- Brazil Law No. 15,211/2025, [Official Gazette of Brazil](https://www.in.gov.br/)
- Digital Personal Data Protection Act 2023, [Gazette of India](https://egazette.gov.in/)
- Singapore Personal Data Protection Act 2012, [Singapore Statutes Online](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act, [Korea Legislation Research Institute](https://elaw.klri.re.kr/)
- China MIIT Mobile App Filing, [Ministry of Industry and Information Technology](https://www.miit.gov.cn/)
