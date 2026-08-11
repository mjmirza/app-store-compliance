# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind app developers shipping into the EU, US, and worldwide, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, seeks to ensure contestable and fair markets in the digital sector. It places strict obligations on designated "gatekeepers" (such as Apple and Google) but also directly shapes how third-party developers deploy applications, alternative store options, alternative billing channels, and custom web links within the EU storefront.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no formal decision policy or guide helping developers choose whether to opt into Apple's alternative terms (e.g., Core Technology Fee vs standard App Store terms).
- **Missing Documentation:**
  The guides omit specific walk-throughs for configuring alternate web distribution channels or custom browser engine entitlements under the DMA rules.
- **Missing Code:**
  Code recipes in this repository do not include functional implementations of the `ExternalPurchaseCustomLink` system-provided disclosure sheet interface.
- **Missing Disclosure:**
  Interface templates do not provide disclosure designs notifying the user that they are transacting outside the App Store or Google Play and that certain platform protections do not apply.
- **Missing Logging:**
  Schema blueprints do not support logging external-purchase transaction metrics required for monthly reporting under the External Purchase Server API.
- **Missing Testing:**
  The automated test suite lacks integration flows to verify that alternative browser engine or HCE payment capabilities are correctly region-gated to the EU/EEA.
- **Missing Evidence:**
  No templates exist for compiling or submitting monthly transaction files to Apple or Google to prove compliance with external-link royalty rules.
- **Missing Audit Trail:**
  An unalterable audit trail recording the developer's choice of fee models, terms addenda, and transition dates is not maintained.

### 7.3 Remediation and Action Plan
1. Formulate a developer-facing DMA Business Terms Decision Matrix to determine the economic feasibility of adopting alternative store terms.
2. Create Swift/Kotlin code templates wrapper classes that execute the `ExternalPurchaseCustomLink` api correctly.
3. Establish robust mock integration testing to verify that region gating dynamically suppresses DMA-specific entitlements outside the EU/EEA.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes a comprehensive framework for online intermediaries, hosting services, and online platforms. It places significant obligations on app stores to verify and publish the identity and contact details of "traders" selling apps to EU consumers.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository has no corporate policy template for managing "trader" versus "non-trader" designations or assessing user generated content hosting obligations.
- **Missing Documentation:**
  Playbook checklists lack step-by-step guidance on completing the two-factor authentication verification process for organization listings in App Store Connect.
- **Missing Code:**
  The repository has no static analysis tools or code rules to check if the trader status declaration matches actual monetization indicators (e.g., in-app purchases).
- **Missing Disclosure:**
  Trader contact details (address, phone, email) are not systematically disclosed in-app or linked in metadata descriptions to match public store listings.
- **Missing Logging:**
  Blueprints do not support logging illegal or harmful content reports from EU users or tracking the resolution times required under Article 16.
- **Missing Testing:**
  No automated tests exist to verify that the app flags or blocks EU storefront access if a trader status declaration is pending or incomplete.
- **Missing Evidence:**
  The repository lacks physical templates of verified trader upload documents, D-U-N-S registrations, or certification records.
- **Missing Audit Trail:**
  There is no historical system to record changes to trader contact data, store compliance declarations, or notices of content removals from national regulators.

### 8.3 Remediation and Action Plan
1. Add a trader-status qualification flow to the pre-submission guidelines to prevent unexpected metadata rejections.
2. Standardize notice-and-take-down UI components for consumer-facing apps to ensure Article 16 reporting compliance.
3. Design and distribute database schema templates specifically structured to log user safety reports with immutable timestamps.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable on 28 June 2025. It mandates accessibility for key digital products and services, including e-commerce, banking, e-books, and mobile apps distributed in the EU, aligned with the EN 301 549 Chapter 11 technical standard.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no corporate accessibility policy or microenterprise exemption decision matrix.
- **Missing Documentation:**
  The checklists do not provide an exhaustive mapping of EN 301 549 Chapter 11 mobile software requirements versus standard WCAG 2.1 Level AA web requirements.
- **Missing Code:**
  Although accessibility patterns are checked by static scripts, there are no live UI component examples of dynamic type support or voiceover announcement handlers.
- **Missing Disclosure:**
  No public-facing accessibility statement template or compliance disclosure is provided for integration within the mobile app or website.
- **Missing Logging:**
  There are no schemas or logging frameworks to capture user accessibility complaints or record assistive technology configuration sessions.
- **Missing Testing:**
  The automated audit tools only check basic code markers but do not execute screen reader flow simulation tests or high contrast contrast-ratio validation.
- **Missing Evidence:**
  Factual evidence templates, such as an Accessibility Conformance Report (ACR) using the VPAT template for mobile apps, are absent.
- **Missing Audit Trail:**
  The repository lacks an unalterable history system tracking accessibility audit results, regression fixes, or compliance statement revisions.

### 9.3 Remediation and Action Plan
1. Publish a technical standard guide mapping EN 301 549 Chapter 11 requirements to mobile components.
2. Develop interactive UI code blocks that dynamically scale font styles and respect native isDarkerSystemColorsEnabled.
3. Implement a standard accessibility feedback intake form and automated validation tests in the CI build system.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6506, and the amended FTC COPPA Rule (effective June 2025, compliance April 2026) regulate the collection of personal information from children under 13.

Official Citation: 16 CFR Part 312.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no template children's data policy or written information-security program (WISP) required under 16 CFR 312.8.
- **Missing Documentation:**
  Checks in `docs/PRE-SUBMISSION-CHECKLIST.md` do not outline the precise verifiable parental consent (VPC) methods required under the new 2025 FTC rules.
- **Missing Code:**
  No mock implementations exist for child-directed age gating, separate opt-ins for third-party disclosures, or secure biometric-identifier isolation.
- **Missing Disclosure:**
  Interface templates are missing standardized parental consent notices or child-directed privacy policy disclosures.
- **Missing Logging:**
  Blueprint databases fail to include schemas for tracking the receipt, update, or revocation of verifiable parental consent (VPC).
- **Missing Testing:**
  No automated unit tests simulate DOB boundary checks to verify that child-category users are dynamically blocked from tracking pixels.
- **Missing Evidence:**
  The playbook lacks templates for kid-directed privacy impact assessments or COPPA safe harbor compliance certificates.
- **Missing Audit Trail:**
  An immutable audit trail system to record the deletion of raw age-verification records or parental data retention limits is completely absent.

### 10.3 Remediation and Action Plan
1. Create a written boilerplate WISP plan and Children's Privacy Policy tailored to mobile apps.
2. Develop backend logic templates to separate opt-in tracking options and provide verifiable parental consent APIs.
3. Integrate unit tests verifying age gating boundaries and automated data deletion routines.

---

## 11. California Consumer Privacy Act / California Privacy Rights Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) and the California Privacy Rights Act (CPRA) establish robust privacy protections for consumers in California, mandating strict controls on data sharing, automated decision-making, and sensitive personal information.

Official Citation: Cal. Civ. Code Section 1798.100 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no comprehensive California Privacy Notice or "Limit the Use of My Sensitive Personal Information" policy template.
- **Missing Documentation:**
  Guides omit detailed steps for supporting the Global Privacy Control (GPC) signal within embedded web views or native mobile networking layers.
- **Missing Code:**
  The repository lacks helper functions to detect or honor the `Sec-GPC` HTTP header or handle CPPA-compliant user data deletion/correction workflows.
- **Missing Disclosure:**
  No boilerplate templates exist for "Do Not Sell or Share My Personal Information" or "Notice at Collection" disclosures.
- **Missing Logging:**
  Schema blueprints do not log consumer rights requests (access, deletion, correction) or track statutory response times.
- **Missing Testing:**
  Test suites do not simulate CPRA request lifecycles or verify that GPC signals dynamically disable advertising SDK trackers.
- **Missing Evidence:**
  No templates exist for compiling California data inventory sheets or statutory compliance reporting metrics.
- **Missing Audit Trail:**
  There is no historical log to trace when privacy notices were updated or how consumer request fulfillment histories were handled.

### 11.3 Remediation and Action Plan
1. Deliver standard California privacy notice templates including explicit data collection disclosures.
2. Build networking middleware to process `Sec-GPC` signals and automatically disable third-party analytics.
3. Establish robust database logging schemas to monitor statutory compliance windows for deletion and correction requests.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA) regulates the collection, storage, and handling of biometric identifiers (such as fingerprints, facial scans, or iris patterns) by private entities.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no template written policy for BIPA, including the mandatory public-facing retention schedule and destruction guidelines.
- **Missing Documentation:**
  Playbook guidelines lack technical instructions on how to secure biometric credentials or handle biometrics on client-side versus server-side architectures.
- **Missing Code:**
  Codebases do not include functional biometric enrollment flows that require explicit, e-signed consent before accessing Face ID or Android Biometrics.
- **Missing Disclosure:**
  Interface templates do not provide a boilerplate "Biometric Consent and Disclosure Notice" to display before user enrollment.
- **Missing Logging:**
  Blueprints do not contain secure, minimized database schemas to log consent timestamps without capturing biometric raw data.
- **Missing Testing:**
  No automated tests exist to verify that biometric features are completely disabled if the user declines or revokes the biometric consent flag.
- **Missing Evidence:**
  The playbook is missing templates of signed biometric release forms or biometric vendor security assessment certificates.
- **Missing Audit Trail:**
  An unalterable audit trail recording changes to biometric policies, vendor security reviews, and raw biometric data purge records is missing.

### 12.3 Remediation and Action Plan
1. Draft a public BIPA Biometric Retention Schedule and destruction statement.
2. Develop in-app modal sheets demonstrating explicit biometric release agreements.
3. Set up automated test sequences simulating consent denials and verify the complete bypass of biometric prompts.

---

## 13. US Subscription Cancellation / Negative Option Laws

### 13.1 Regulatory Overview and Background
Despite the vacatur of the FTC Negative Option Rule amendment in 2025, state-level statutes (such as California, New York, and Massachusetts) independently require online subscriptions to offer an easy, prominent cancellation path that is at least as simple as the sign-up process.

Official Citation: California Business and Professions Code Section 17600 et seq.; New York General Business Law Section 335-a.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository has no master Subscription Negative Option Compliance Policy or refund guidelines for non-store-billed web companion subscriptions.
- **Missing Documentation:**
  Checklists do not detail the placement or font-size requirements for cancellation disclosures in billing UI designs.
- **Missing Code:**
  The repository does not include a self-service "click to cancel" button component or direct link wrapper for account billing interfaces.
- **Missing Disclosure:**
  Registration templates lack clear, nearby disclosures of recurring billing frequencies, billing totals, or automatic renewal dates.
- **Missing Logging:**
  Blueprints do not log the specific cancel events, timestamps, and customer exit surveys in an immutable subscription database.
- **Missing Testing:**
  No end-to-end integration tests exist to verify that users can successfully cancel a subscription without customer agent intervention.
- **Missing Evidence:**
  The playbook lacks template confirmation receipts or compliance assessment logs to prove simple cancellation paths to state Attorneys General.
- **Missing Audit Trail:**
  There is no historical tracking system to document paywall updates, price changes, or modifications to cancellation scripts.

### 13.3 Remediation and Action Plan
1. Create a "Click-to-Cancel" subscription management policy aligned with California state regulations.
2. Add a clear, prominent, frictionless cancellation link in account settings templates.
3. Develop automated end-to-end UI testing files verifying that cancellation can be completed in an equal number of steps as registration.

---

## 14. UK Online Safety Act 2023 (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 requires providers of services likely to be accessed by children to take proactive measures to prevent child exposure to illegal or harmful content, enforced by the regulator Ofcom.

Official Citation: Online Safety Act 2023 (c. 30).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no Online Safety Policy template or child-protection escalation procedure for UK storefronts.
- **Missing Documentation:**
  Guides omit instructions on how to integrate Highly Effective Age Assurance (HEAA) methods such as facial age estimation or bank-card verification.
- **Missing Code:**
  Code templates contain no native UI elements for user-generated content blocking or automated safety alerts for under-18 users.
- **Missing Disclosure:**
  Public listings and onboarding screens do not disclose the age-verification mechanics or the presence of UK-specific moderation filters.
- **Missing Logging:**
  The repository does not provide schemas or logging systems designed to record user safety reports, moderation actions, or age checks.
- **Missing Testing:**
  Automated tests do not simulate underage accounts to verify that they are strictly prevented from seeing high-risk user-generated content.
- **Missing Evidence:**
  Factual evidence templates of Ofcom-compliant Child Safety Risk Assessments are absent from the playbook.
- **Missing Audit Trail:**
  There is no unalterable log to trace changes to UK-specific content filtering parameters, age-verification vendors, or safety enforcement actions.

### 14.3 Remediation and Action Plan
1. Establish a written Child Online Safety policy tailored to UK distribution requirements.
2. Develop modular API connectors to integrate third-party age verification and content moderation services.
3. Create automated safety tests to verify that content filtering works correctly for child profiles.

---

## 15. UK Children's Code / ICO Age Appropriate Design Code

### 15.1 Regulatory Overview and Background
The ICO Age Appropriate Design Code (Children's Code) applies to online services likely to be accessed by children under 18 in the United Kingdom, establishing fifteen core standards of age-appropriate design.

Official Citation: Age Appropriate Design Code (ICO, 2021).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template Age Appropriate Design policy or written Child Data Protection Impact Assessment (DPIA).
- **Missing Documentation:**
  Checklists do not define step-by-step developer guidelines for setting "high privacy by default" across all client-side and server-side configurations.
- **Missing Code:**
  The codebase lacks configurations to dynamically disable geolocation tracking, profiling, and push notifications for users under 18.
- **Missing Disclosure:**
  Interface templates omit clear, age-appropriate language explaining data practices directly to child users of various developmental age bands.
- **Missing Logging:**
  Blueprint databases do not support logging default privacy setting enforcement states or child-directed nudge telemetry.
- **Missing Testing:**
  No automated unit tests exist to verify that profiling, sharing, and tracking SDKs are completely blocked by default for under-18 users.
- **Missing Evidence:**
  Factual templates of completed Children's Code DPIAs or age-estimation verification metrics are not provided.
- **Missing Audit Trail:**
  An unalterable audit trail tracking the history of default setting configurations, age range estimations, and design changes is completely absent.

### 15.3 Remediation and Action Plan
1. Produce an ICO Children's Code compliance template packet including a baseline mobile-specific DPIA.
2. Build network routing templates to prevent analytical SDK initialization for identified minor accounts.
3. Configure static tests to ensure tracking and push configurations default to "off" unless parental consent is set.

---

## 16. Australia Online Safety (Social Media Minimum Age) Act 2024

### 16.1 Regulatory Overview and Background
Enacted in December 2024 with enforcement starting in late 2025/2026, this Australian law mandates that social media platforms take reasonable steps to prevent users under 16 from creating accounts.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no written Minor Account Exclusion Policy or Australia-specific social media compliance strategy.
- **Missing Documentation:**
  Guides do not detail the accepted "waterfall" of age-assurance methods or guidelines for ringfencing and destroying collected age data.
- **Missing Code:**
  The codebase does not include functional integration with Apple's or Google's age range APIs specifically configured to enforce a hard 16-year block.
- **Missing Disclosure:**
  The onboarding flows fail to show Australia-specific disclosures explaining that under-16 access is legally restricted and verified.
- **Missing Logging:**
  There are no secure backend schemas to log age verification status while ensuring the immediate destruction of raw identification documents.
- **Missing Testing:**
  Integration test suites do not check if Australian storefront users under 16 are successfully blocked from registration.
- **Missing Evidence:**
  The playbook lacks templates for proving age-assurance system audits or data destruction logs to the Australian eSafety Commissioner.
- **Missing Audit Trail:**
  A secure, immutable history tracking age assurance rollout, vendor configurations, and data deletion receipts is missing.

### 16.3 Remediation and Action Plan
1. Establish a corporate policy for Australia Online Safety compliance, outlining exact data protection and erasure cycles.
2. Update cross-platform native SDK hooks to check Apple/Google age APIs and dynamically apply registration blocks.
3. Formulate standard backend data purging routines that execute automatically upon verification of child status.

---

## 17. Brazil Digital ECA (Law 15,211/2025)

### 17.1 Regulatory Overview and Background
Brazil's Digital Child and Adolescent Statute (Law 15,211/2025), enforceable from March 2026, mandates robust age verification and child-safety protocols for online applications accessed by minors.

Official Citation: Law No. 15,211 of Brazil, supplementing the LGPD.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template policy for compliance with the Brazilian Digital ECA or LGPD children's privacy provisions.
- **Missing Documentation:**
  The checklists do not cover Brazilian-specific age-verification methods (such as CPF database queries) or age-gated gaming restrictions.
- **Missing Code:**
  No codebase templates demonstrate the integration of Google Play's Age Signals API or Apple's Declared Age Range API for Brazilian storefronts.
- **Missing Disclosure:**
  Onboarding interfaces do not prominently disclose age-verification requirements in Brazilian Portuguese or outline parental supervision tools.
- **Missing Logging:**
  Database blueprints do not support logging parental consent or Brazilian CPF confirmation tokens in a minimized format.
- **Missing Testing:**
  No unit tests simulate Brazilian locale settings to verify that age signals are queried and handled dynamically during app initialization.
- **Missing Evidence:**
  Factual templates of LGPD-compliant children's data impact assessments (DPIAs) are absent.
- **Missing Audit Trail:**
  There is no secure audit trail to record changes to Brazilian-specific age gates, consent records, or localized policy updates.

### 17.3 Remediation and Action Plan
1. Draft a comprehensive Brazil LGPD Children's Data Processing Guide.
2. Build UI onboarding templates localized in Brazilian Portuguese incorporating Declared Age Range APIs.
3. Configure unit and automated testing environments to validate dynamic age signals returned on Brazilian IP addresses.

---

## 18. India Digital Personal Data Protection Act 2023 (DPDPA)

### 18.1 Regulatory Overview and Background
The India DPDPA, enacted in 2023 and supplemented by the DPDP Rules 2025, mandates strict consent-driven data processing, special protections for children's data (under 18), and the designation of a Consent Manager.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 26 of 2023).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no corporate DPDPA compliance policy, Consent Manager integration plan, or under-18 processing prohibition guidelines.
- **Missing Documentation:**
  Checklists omit detailed explanations of the "unconditional, specific, informed, and unambiguous" consent requirements of Section 6.
- **Missing Code:**
  The codebase lacks Indian localized "Consent Manager" interface integration or DigiLocker-based verifiable parental consent adapters.
- **Missing Disclosure:**
  Interface templates are missing the mandatory multi-lingual consent notices and explicit disclosures of the purposes and data categories processed.
- **Missing Logging:**
  Blueprints do not contain schemas to log Indian user consent preferences, Consent Manager tokens, or parental confirmations.
- **Missing Testing:**
  No automated unit tests exist to check if behavioral tracking and targeted advertising are dynamically disabled for Indian users under 18.
- **Missing Evidence:**
  The repository lacks templates of DPDPA data inventory lists, Consent Manager contracts, or parental verification evidence sheets.
- **Missing Audit Trail:**
  An unalterable audit trail tracking consent history, consent withdrawals, and localized privacy policy revisions is completely absent.

### 18.3 Remediation and Action Plan
1. Author a corporate DPDPA Consent Policy template covering Consent Manager architectures.
2. Build UI consent widgets presenting explicit, multi-lingual notice dialogs.
3. Establish database tables tracking individual user consent revisions and statutory consent withdrawal workflows.

---

## 19. Singapore PDPA / IMDA Code of Practice for Online Safety

### 19.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety (effective April 2026) mandate strict data protection and age-assurance protocols to prevent child exposure to harmful online content.

Official Citation: Personal Data Protection Act 2012 (No. 26 of 2012); IMDA Code of Practice.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written policy template for the Singapore PDPA, the designation of a Data Protection Officer (DPO), or IMDA child-safety rules.
- **Missing Documentation:**
  Playbook guidelines do not cover Singapore-specific age-verification methods or the IMDA code's data retention limitation rules.
- **Missing Code:**
  Code resources do not show how to retrieve and respect Singapore-storefront age signals or handle explicit PDPA-compliant consent gates.
- **Missing Disclosure:**
  Interface templates fail to display Singapore-specific notices detailing DPO contact information or age-assurance policies.
- **Missing Logging:**
  Blueprints do not log Singapore user consent actions or record the immediate deletion of age-assurance validation tokens.
- **Missing Testing:**
  No integration tests exist to verify that the application blocks Singapore-storefront users under 18 from accessing adult content.
- **Missing Evidence:**
  Factual templates for Singapore PDPA compliance audits or DPO registration documents are missing.
- **Missing Audit Trail:**
  A systematic audit trail tracking PDPA-related consent changes, DPO appointments, and age gate modifications is not implemented.

### 19.3 Remediation and Action Plan
1. Formulate a technical checklist for Singapore PDPA and IMDA compliance auditing.
2. Build age gate UI code integrations customized for Singapore storefront rules.
3. Develop automated tests verifying that no tracking or PII storage occurs for Singapore minor accounts.

---

## 20. South Korea Telecommunications Business Act

### 20.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates that app stores allow alternative in-app payment systems, establishing a detailed framework for developers to offer alternative billing methods on South Korean storefronts.

Official Citation: Telecommunications Business Act (Act No. 18420).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no South Korea Alternative In-App Billing Policy or transactional reporting guidelines.
- **Missing Documentation:**
  Playbook checklists do not outline the developer's 15-day reporting cycle or 45-day remittance obligations under the alternative StoreKit rules.
- **Missing Code:**
  The code templates lack South Korean-specific dual-billing client components, approved payment gateway (KCP, Toss) integrations, or the mandatory system-provided disclosure sheet custom code.
- **Missing Disclosure:**
  Paywall interfaces do not display South Korean-specific disclosures stating that alternative billing lacks standard platform protections.
- **Missing Logging:**
  Blueprints fail to include database schemas for tracking alternative billing transaction metrics required for monthly reporting.
- **Missing Testing:**
  No automated tests verify that the Korean alternative payment flows are restricted to the South Korean storefront.
- **Missing Evidence:**
  The playbook lacks template transaction report formats or remittance confirmation sheets for South Korean tax and platform audits.
- **Missing Audit Trail:**
  There is no historical log to track alternative payment configuration changes, billing gateway audits, or monthly sales reports.

### 20.3 Remediation and Action Plan
1. Draft a South Korea Alternative Billing Integration Policy aligned with legislative guidelines.
2. Build custom payment gateway wrapper integrations and localized system disclosure pop-ups.
3. Establish automated build targets that separate South Korean binaries from standard global production packages.

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
| **EU EAA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US CCPA/CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US Negative Option** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK Children's Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Singapore PDPA/IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **South Korea TBA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Almost all modern regulations are named and contextualized with dated sources and deadlines in `docs/EU-REGULATORY-2026.md` or `docs/GLOBAL-REGULATORY-2026.md`. What they lack is the concrete implementation layer within this repository, meaning dedicated static detection rules, functional code blocks, and automated testing engines. EU GPSR and the EAA stand out as requiring the most fundamental core additions to achieve complete compliance maturity.

---

## 22. Conclusion and Future Monitoring

The playbook is extremely strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most of the regulations are named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order.

1. Add GPSR and EAA, the frameworks needing the most fundamental core content.
2. Give the Partial frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
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
- EU DMA, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act (EAA), [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California Consumer Privacy Act, [Cal. Civ. Code Section 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)
- Illinois BIPA, [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004&ChapterID=57)
- California Negative Option Law, [Cal. Bus. & Prof. Code Section 17600](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=7&title=&part=3&chapter=1&article=9.)
- UK Online Safety Act 2023, [Online Safety Act 2023 (c. 30)](https://www.legislation.gov.uk/ukpga/2023/30/contents)
- UK Children's Code, [Age Appropriate Design Code (ICO)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- Australia Online Safety Amendment, [Social Media Minimum Age Act 2024](https://www.legislation.gov.au/C2024A00115/latest/text)
- Brazil Digital ECA, [Law No. 15,211 of Brazil](https://www.in.gov.br/)
- India DPDPA, [Digital Personal Data Protection Act, 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act, [Act No. 18420](https://www.law.go.kr/)

The US state App Store Accountability Acts are cited to their bill texts in [docs/GLOBAL-REGULATORY-2026.md](GLOBAL-REGULATORY-2026.md), which is the source of record for that section rather than this report.
