# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the App Store Compliance Playbook repository itself. It evaluates twenty major global and regional regulations that bind mobile and web application developers, systematically assessing how far this repository carries each framework, what is only covered partially, and what gaps exist.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight compliance categories: missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

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

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

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
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, regulates core platform services operated by designated gatekeepers (such as Apple and Google). It gives app developers rights to distribute apps via alternative marketplaces or web distribution, use alternative in-app payment processors, and link out to external purchase options.

To exercise DMA rights cleanly without store rejection or regulatory non-compliance, developers must adhere to strict platform entitlement rules (e.g. `com.apple.developer.storekit.external-purchase-link`), display required modal sheets, track external transactions, and calculate relevant fees (such as Apple's Core Technology Commission).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template DMA Alternative Distribution and Payments Policy for developers navigating EU gatekeeper options.
- **Missing Documentation:**
  While DMA is referenced in docs, there is missing step-by-step developer documentation for setting up alternative payment reporting and managing dual-store binaries.
- **Missing Code:**
  The guard and codebase lacks sample code demonstrating storefront country-code checks (`Storefront.current?.countryCode == "DEU"`) before opening external purchase links.
- **Missing Disclosure:**
  In-app purchase templates do not include the mandatory platform disclosure modal required when directing EU users to an external billing webpage.
- **Missing Logging:**
  There are no backend database models or logging mechanisms to record alternative transaction IDs, gross sale values, and CTC reporting figures.
- **Missing Testing:**
  No automated unit or UI tests verify that external purchase sheets appear only for users residing in EU Member States.
- **Missing Evidence:**
  The repository lacks templates of monthly transaction reports or gatekeeper reporting reconciliation statements.
- **Missing Audit Trail:**
  An unalterable audit trail tracking entitlement requests, store agreement acceptances (e.g., ADPLA Attachment 14), and fee calculations is absent.

### 7.3 Remediation and Action Plan
1. Draft a comprehensive DMA Alternative Payment & Distribution Policy.
2. Provide code snippets for storefront-gated external link triggers and custom modal sheets.
3. Add automated guard rules to verify that external purchase links are restricted to EU storefronts.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, applies to online intermediaries and platforms, imposing trader traceability duties (Article 30), content moderation transparency, and illegal content notice-and-action mechanisms.

App developers publishing on app stores must complete Trader Status declarations (providing D-U-N-S, verified email, phone number, and financial account details). Failure to provide verified trader status results in app removal from EU storefronts. Apps with user-generated content (UGC) or hosting services must also provide notice-and-action mechanisms.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template DSA Trader Compliance & Notice-and-Action Policy exists in the repository.
- **Missing Documentation:**
  Missing detailed guidelines for completing DSA trader verification across App Store Connect and Google Play Console.
- **Missing Code:**
  Code templates lack an in-app illegal content reporting mechanism (Notice and Action form) required for hosting and UGC applications.
- **Missing Disclosure:**
  Metadata audit scripts do not verify that DSA-mandated trader details (address, email, phone) are published on storefront listings for commercial accounts.
- **Missing Logging:**
  No logging schemas exist for capturing incoming illegal content reports, reviewer action timestamps, or user appeal outcomes.
- **Missing Testing:**
  No automated tests exist to verify that content reporting endpoints return expected confirmation payloads within statutory limits.
- **Missing Evidence:**
  Templates for annual DSA transparency reports and trader verification documents are missing.
- **Missing Audit Trail:**
  An immutable audit trail recording content moderation decisions, user notifications, and counter-notices is completely absent.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader & Content Moderation Compliance Guide.
2. Build an in-app notice-and-action reporting component for UGC app templates.
3. Integrate DSA trader metadata checks into `scripts/metadata-audit.py`.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, mandates accessibility requirements for products and services, including e-commerce apps, banking services, and mobile applications, applying fully from 28 June 2025.

Under harmonised standard EN 301 549 (aligned with WCAG 2.1 Level AA), apps must support screen readers (VoiceOver/TalkBack), dynamic font scaling, sufficient color contrast, keyboard navigation, and provide an easily accessible Accessibility Statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Corporate Accessibility Policy covering EN 301 549 and WCAG 2.1 AA commitments exists.
- **Missing Documentation:**
  While `docs/ACCESSIBILITY-COMPLIANCE-REPORT.md` exists, step-by-step developer guidelines for published Accessibility Statements and exemption documentation are missing.
- **Missing Code:**
  Sample UI templates lack complete accessibility attributes (`accessibilityLabel`, `accessibilityHint`, dynamic type scale bounds).
- **Missing Disclosure:**
  Public-facing app templates do not include an in-app link to an Accessibility Statement detailing conformance levels and feedback mechanisms.
- **Missing Logging:**
  No logging mechanisms exist to capture accessibility feedback, reported barriers, or assistive technology compatibility errors.
- **Missing Testing:**
  `scripts/accessibility-audit.py` performs basic static checks but lacks automated UI screen-reader tree parsing or contrast ratio evaluation tests.
- **Missing Evidence:**
  Templates for Accessibility Conformance Reports (VPAT / EN 301 549 evaluation sheets) are absent.
- **Missing Audit Trail:**
  An audit trail tracking historical accessibility audits, regression fixes, and user feedback resolution is missing.

### 9.3 Remediation and Action Plan
1. Draft an EN 301 549 / WCAG 2.1 AA Mobile Accessibility Policy.
2. Enhance `scripts/accessibility-audit.py` to scan for missing dynamic type scaling and contrast declarations.
3. Include an Accessibility Statement template in `templates/`.

---

## 10. US Children's Online Privacy Protection Act (COPPA) Amended Rule

### 10.1 Regulatory Overview and Background
The FTC's Amended COPPA Rule (16 CFR Part 312) strengthens protections for children under 13, adding biometric identifiers to PII, requiring separate opt-in consent for third-party disclosures and targeted advertising, mandating a written data retention policy, and enforcing a formal written information security program.

Mandatory compliance enforcement for the amended rule begins on 22 April 2026.

Official Citation: FTC 16 CFR Part 312, Children's Online Privacy Protection Rule.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written COPPA Data Retention Policy or written Children's Information Security Program template exists in the repository.
- **Missing Documentation:**
  Missing technical guides on implementing separate double opt-in consent flows for third-party SDK analytics in child-directed apps.
- **Missing Code:**
  Codebase templates lack automated age-gating hooks that disable advertising IDs and third-party trackers when a user is flagged under 13.
- **Missing Disclosure:**
  Privacy policy templates do not incorporate specific disclosures regarding biometric data as PII or separate opt-in consent for third parties.
- **Missing Logging:**
  No backend logging schema exists to record verifiable parental consent (VPC) methods, timestamps, and parental consent revocations.
- **Missing Testing:**
  Test suites lack automated verification that third-party tracking SDKs are completely suppressed in child-directed build flavors.
- **Missing Evidence:**
  The repository lacks templates for COPPA Safe Harbor compliance certificates or independent data safety audit records.
- **Missing Audit Trail:**
  An unalterable audit trail recording data destruction schedules and parental consent events is completely missing.

### 10.3 Remediation and Action Plan
1. Publish a COPPA Written Retention & Security Policy template.
2. Add a code module for age-gated SDK suppression and Verifiable Parental Consent handling.
3. Create automated pre-submission tests verifying zero ad-tracking SDK initialization in Kids category builds.

---

## 11. California Privacy Rights Act (CPRA) & CPPA 2026 Regulations

### 11.1 Regulatory Overview and Background
The California Privacy Rights Act (CPRA) and California Privacy Protection Agency (CPPA) regulations impose strict requirements on businesses collecting California residents' personal data, including honoring Global Privacy Control (GPC) signals, providing opt-out of sale/sharing/profiling, and limiting sensitive personal information use.

Automated Decision-Making Technology (ADMT) regulations mandate opt-out and access rights starting 1 January 2027.

Official Citation: California Civil Code Section 1798.100 et seq.; 11 CCR Section 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template CPRA / CCPA Consumer Privacy Policy or ADMT Policy exists.
- **Missing Documentation:**
  Lacks developer guides on implementing "Do Not Sell or Share My Personal Information" and GPC signal handling in mobile web views and native apps.
- **Missing Code:**
  No native code triggers exist to listen for `Sec-GPC` HTTP headers or system-level opt-out flags.
- **Missing Disclosure:**
  In-app onboarding flows lack explicit Notice at Collection templates specifying sensitive personal information categories.
- **Missing Logging:**
  No logging mechanisms exist to capture consumer privacy requests (access, deletion, opt-out) or record 45-day response SLA compliance.
- **Missing Testing:**
  Test scripts do not verify that setting the GPC header automatically disables third-party tracking pixels and ad network initialization.
- **Missing Evidence:**
  Missing CPPA risk assessment report templates and cybersecurity audit certification templates.
- **Missing Audit Trail:**
  An immutable audit trail tracking opt-out preferences, deletion request fulfillments, and ADMT evaluation logs is absent.

### 11.3 Remediation and Action Plan
1. Create a CPRA Notice at Collection and GPC Compliance Guide.
2. Implement native and web GPC signal detection handlers in sample apps.
3. Add automated checks for "Do Not Sell/Share" links in metadata and in-app settings.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, capture, purchase, receipt, or storage of biometric identifiers (facial geometry, fingerprints, voiceprints, retina scans).

BIPA requires written notice, explicit written release prior to collection, a publicly available retention schedule and destruction guidelines, and strict prohibition on profiting from or selling biometric data.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Biometric Data Retention and Destruction Policy template is provided.
- **Missing Documentation:**
  Missing developer guidelines detailing BIPA consent requirements before invoking FaceID, TouchID, or custom facial recognition SDKs.
- **Missing Code:**
  Sample code invoking local authentication (e.g. `LAContext`) lacks pre-execution written consent modal prompts.
- **Missing Disclosure:**
  Public privacy disclosures do not explicitly inform users of biometric collection purpose, storage length, and destruction schedules.
- **Missing Logging:**
  No secure backend schema exists to record written consent agreements or automated 3-year data destruction events.
- **Missing Testing:**
  No unit tests verify that biometric authentication features abort immediately if the user declines written consent.
- **Missing Evidence:**
  The repository lacks physical consent form templates and biometric security audit logs.
- **Missing Audit Trail:**
  An unalterable audit trail recording consent timestamps, policy updates, and biometric template purges is missing.

### 12.3 Remediation and Action Plan
1. Draft a BIPA Written Notice & Consent Policy template.
2. Create a pre-biometric consent modal component in sample iOS and Android codebases.
3. Add guard rules flagging un-consented biometric API usage.

---

## 13. US FTC Subscription Cancellation / Click-to-Cancel Rule

### 13.1 Regulatory Overview and Background
The FTC's updated Negative Option Rule (Click-to-Cancel), 16 CFR Part 425, mandates that businesses selling auto-renewing subscriptions make the cancellation process as easy as the sign-up process. It prohibits forcing users to speak to customer service agents, complete multi-step retention save-surveys, or navigate complex phone menus if they signed up online or in-app.

Official Citation: FTC 16 CFR Part 425, Rule on Use of Subscriptions and Other Negative Option Plans.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No FTC-aligned Subscription Management and Cancellation Policy exists.
- **Missing Documentation:**
  Lacks developer guides detailing prohibited cancellation friction (dark patterns, compulsory phone calls, multi-page save flows).
- **Missing Code:**
  Subscription UI templates do not include a 1-click self-service cancellation button.
- **Missing Disclosure:**
  Paywall UI templates fail to display clear, conspicuous pre-consent disclosures of auto-renewal terms, billing frequency, and cancellation steps right next to the CTA button.
- **Missing Logging:**
  No logging provisions exist to capture subscription consent timestamps, renewal notice dispatches, and instant cancellation requests.
- **Missing Testing:**
  Guard script `BOTH-SUBSCRIPTION-HARD-CANCEL` checks for phone-only cancellation text but lacks UI flow tests for multi-step dark pattern detection.
- **Missing Evidence:**
  Missing copies of negative option disclosures, billing confirmation emails, and cancellation receipts.
- **Missing Audit Trail:**
  An immutable audit trail tracking subscription sign-ups, renewal notices, and cancellation executions is absent.

### 13.3 Remediation and Action Plan
1. Formulate a Click-to-Cancel Subscription Compliance Guide.
2. Provide paywall and account settings UI templates featuring compliant disclosures and 1-click cancellation paths.
3. Add automated guard rules scanning for multi-page retention surveys prior to cancellation.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and the ICO Age Appropriate Design Code (Children's Code) mandate that services likely to be accessed by children enforce high privacy by default, turn geolocation off, disable profiling, perform mandatory Data Protection Impact Assessments (DPIAs), and implement Highly Effective Age Assurance (HEAA).

Official Citation: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No UK Children's Code Privacy Policy or HEAA Implementation Policy exists.
- **Missing Documentation:**
  Missing step-by-step DPIA templates tailored for child-accessible mobile applications.
- **Missing Code:**
  Codebases lack logic to automatically set default high-privacy configurations (geolocation OFF, profiling OFF, push notifications OFF between midnight and 6am) for UK minor accounts.
- **Missing Disclosure:**
  In-app onboarding flows lack child-friendly privacy notices and age-appropriate explanatory copy.
- **Missing Logging:**
  No backend logging schema exists to record DPIA completion, age-assurance results, or parental consent state changes.
- **Missing Testing:**
  Test runners do not verify that profiling and location APIs are disabled by default on child user profiles.
- **Missing Evidence:**
  Missing completed DPIA document examples and HEAA provider evaluation certificates.
- **Missing Audit Trail:**
  An unalterable audit trail recording age-assurance decisions, DPIA updates, and safety risk mitigation reviews is missing.

### 14.3 Remediation and Action Plan
1. Publish a UK Children's Code & DPIA Compliance Template.
2. Build child-profile default privacy configurations into mobile app starter templates.
3. Integrate DPIA verification into release readiness audit scripts.

---

## 15. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 and the App Distribution Services Online Safety Code require social media platforms and app distribution services to enforce a strict minimum age of 16 for social media accounts, utilize robust age assurance, and destroy age-assurance data immediately after verification.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024; eSafety Commissioner Industry Codes.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Australian Social Media Age Assurance & Data Minimization Policy exists in the playbook.
- **Missing Documentation:**
  Lacks technical manuals explaining eSafety Commissioner compliance, age-assurance methods, and immediate data destruction duties.
- **Missing Code:**
  No code exists to restrict under-16 user account creation or execute immediate age-data purging after confirmation.
- **Missing Disclosure:**
  Onboarding templates do not display required Australian statutory notices regarding minimum age rules and age data privacy.
- **Missing Logging:**
  No secure backend schema exists to record age confirmation pass/fail flags without storing raw age verification documents.
- **Missing Testing:**
  Integration tests do not verify that under-16 users are blocked from completing account registration on social media app profiles.
- **Missing Evidence:**
  Missing proof of compliance templates for eSafety Commissioner audits and independent age-assurance accuracy reports.
- **Missing Audit Trail:**
  An immutable audit trail recording age verification attempts, immediate raw data deletion events, and policy reviews is missing.

### 15.3 Remediation and Action Plan
1. Create an Australian Online Safety & Minimum Age Compliance Guide.
2. Develop under-16 account blocking and immediate data destruction helper utilities.
3. Add automated checks for Australian age-gating compliance in social app templates.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12,880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto n. 12.880 regulate child and adolescent protection in digital environments. They mandate ANPD-approved age verification (document checks, facial age estimation, CPF validation), prohibit simple self-declaration check-boxes, require guardian authorization, and mandate age rating displays before download.

Official Citation: Lei n. 15.211/2025; Decreto n. 12.880 de 18 de marco de 2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Brazil Digital ECA Compliance & Guardian Authorization Policy exists.
- **Missing Documentation:**
  Lacks developer guides detailing ANPD age assurance guidelines and CPF/facial estimation integration patterns.
- **Missing Code:**
  Codebases do not include ANPD-compliant age verification API integration routines or guardian consent workflows.
- **Missing Disclosure:**
  In-app storefront templates lack prominent pre-download age rating displays and guardian information notices in Portuguese.
- **Missing Logging:**
  No backend schema exists to record guardian authorization grants, contestation requests, or raw verification data purges.
- **Missing Testing:**
  Test runners do not verify that self-declaration check-boxes are rejected for Brazilian user IP ranges.
- **Missing Evidence:**
  Missing ANPD compliance declaration forms and age assurance technical audit records.
- **Missing Audit Trail:**
  An unalterable audit trail recording age verification checks, contestation resolutions, and guardian consent grants is absent.

### 16.3 Remediation and Action Plan
1. Publish a Brazil Digital ECA Compliance Guide.
2. Provide code snippets for ANPD-compliant age verification and guardian consent modals.
3. Add guard rules detecting prohibited self-declaration check-boxes for Brazil-targeted apps.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 establish strict consent requirements, mandate verifiable parental consent through government-backed systems (e.g. DigiLocker) for under-18s, prohibit behavioral tracking/targeted ads for children, and require interoperability with registered Consent Managers.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No DPDPA Data Fiduciary Policy or Child Data Protection Policy exists in the repository.
- **Missing Documentation:**
  Lacks developer manuals on integrating with Indian Consent Managers and DigiLocker-based verifiable parental consent flows.
- **Missing Code:**
  Codebases lack API client integrations for Consent Manager interoperability and DigiLocker parent verification tokens.
- **Missing Disclosure:**
  Consent notice templates are not available in English and all 22 official scheduled Indian languages as required by Section 6(1).
- **Missing Logging:**
  No logging provisions exist for recording itemized consent grants, withdrawal requests, or Data Protection Officer (DPO) contact logs.
- **Missing Testing:**
  Test suites do not verify that behavioral tracking and targeted ad SDKs are disabled for under-18 Indian users.
- **Missing Evidence:**
  Missing templates for Data Protection Impact Assessments and Significant Data Fiduciary audit records.
- **Missing Audit Trail:**
  An immutable audit trail recording multilingual consent presentations, consent manager API calls, and data destruction is missing.

### 17.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance & Consent Manager Interoperability Guide.
2. Provide multilingual consent notice templates and DigiLocker verification code examples.
3. Integrate automated checks for child ad-tracking prohibitions into release audit scripts.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice for Online Safety

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and IMDA Code of Practice for Online Safety for App Distribution Services require app-store age assurance, screening users under 18 from downloading age-inappropriate apps, immediate age-assurance data destruction, and designated safety contact channels.

Official Citation: Personal Data Protection Act 2012 (Act 26 of 2012); IMDA Code of Practice for Online Safety.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore PDPA & IMDA Online Safety Policy template is provided.
- **Missing Documentation:**
  Missing technical documentation on IMDA Code of Practice age assurance expectations and data protection officer (DPO) registration.
- **Missing Code:**
  Sample apps lack age-gating checks aligned with Singapore age ratings and immediate age data deletion routines.
- **Missing Disclosure:**
  Public-facing app templates do not disclose DPO contact details and IMDA safety reporting mechanisms.
- **Missing Logging:**
  No logging schemas exist for recording user safety complaints, age verification results, or data disposal confirmation.
- **Missing Testing:**
  Test runners do not verify that age-assurance data is purged immediately following API verification responses.
- **Missing Evidence:**
  Missing PDPA compliance audit checklists and IMDA safety report submission templates.
- **Missing Audit Trail:**
  An unalterable audit trail recording safety complaint resolutions, DPO inquiries, and age data purges is missing.

### 18.3 Remediation and Action Plan
1. Publish a Singapore PDPA & IMDA Online Safety Guide.
2. Add DPO contact disclosure templates and age data minimization helpers.
3. Include IMDA safety reporting checks in pre-submission checklists.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app billing support (allowing third-party payment gateways with a maximum 26% commission), dedicated `com.apple.developer.storekit.external-purchase` entitlement, and South Korea-specific binaries/modal sheets. The amended Personal Information Protection Act (PIPA) mandates CEO/CPO accountability and stringent breach notification timelines.

Official Citation: Telecommunications Business Act Article 22-9; Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No South Korea Alternative Billing & PIPA Privacy Policy template exists.
- **Missing Documentation:**
  Lacks developer guides detailing South Korea-specific StoreKit/Play Billing alternative payment integration and monthly transaction reporting.
- **Missing Code:**
  Codebases lack South Korea-specific payment modal sheets and commission reporting calculation utilities.
- **Missing Disclosure:**
  In-app payment templates do not include South Korea statutory notices explaining third-party payment processing terms and refund differences.
- **Missing Logging:**
  No logging schema exists to record alternative payment transactions, Korea Communications Commission (KCC) report figures, or PIPA breach logs.
- **Missing Testing:**
  Test suites do not verify that external payment entitlements are activated exclusively for South Korea storefront sessions.
- **Missing Evidence:**
  Missing monthly transaction reporting templates required by Apple/Google for South Korea alternative billing.
- **Missing Audit Trail:**
  An unalterable audit trail tracking alternative payment transactions, KCC reporting submissions, and PIPA privacy policy changes is absent.

### 19.3 Remediation and Action Plan
1. Create a South Korea Alternative Billing & PIPA Compliance Guide.
2. Provide code templates for South Korea alternative billing modal sheets.
3. Integrate storefront-gating checks for South Korea payment entitlements into guard scripts.

---

## 20. China Mobile App Filing (MIIT ICP Extension) & PIPL

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP Extension) for all apps distributed in China, requiring a local Chinese partner/entity, real-name registration, Personal Information Protection Law (PIPL) compliance, data localization, and a Banhao license for games.

Official Citation: MIIT Notice on Mobile Application Filing (2023); Personal Information Protection Law (PIPL).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China MIIT App Filing & PIPL Data Localization Policy template exists in the playbook.
- **Missing Documentation:**
  Lacks developer guides detailing MIIT filing number application, local entity requirements, and PIPL cross-border data transfer assessments.
- **Missing Code:**
  Codebases lack MIIT app filing number display components (required in app settings/about screens) and local real-name authentication hooks.
- **Missing Disclosure:**
  App store listing templates and in-app settings lack space or automated validation for displaying the MIIT filing number (e.g. Jing ICP Bei XXXXXXXX Hao).
- **Missing Logging:**
  No logging schema exists to record real-name authentication passes, PIPL consent grants, or cross-border data transfer logs.
- **Missing Testing:**
  `scripts/metadata-audit.py` does not check for the presence of valid MIIT filing number format in Chinese storefront metadata.
- **Missing Evidence:**
  Missing templates for MIIT filing confirmation receipts, PIPL Personal Information Protection Impact Assessments (PIPIA), and Banhao licenses.
- **Missing Audit Trail:**
  An unalterable audit trail recording real-name verification logs, cross-border data transfer audits, and MIIT filing renewals is missing.

### 20.3 Remediation and Action Plan
1. Draft a China MIIT App Filing & PIPL Compliance Guide.
2. Add MIIT filing number verification to `scripts/metadata-audit.py`.
3. Provide UI components displaying the MIIT filing number on about screens for China build targets.

---

## 21. Consolidated Gap Classification Matrix

This matrix summarizes the compliance evaluation across all twenty major global and regional regulatory frameworks. Each category is classified as Covered (fully implemented), Partial (mentioned or partially addressed), or Missing (absent from codebase, guard scripts, and documentation).

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence Package** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU Digital Markets Act** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **8. EU Digital Services Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act**| Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA / CPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US FTC Subscription Cancel**| Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **14. UK Online Safety & ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **20. China App Filing & PIPL**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Strategic Implementation Roadmap

This exhaustive audit demonstrates that while the repository provides excellent coverage of app store rejection rules and high-level regulatory awareness across all twenty legal frameworks, significant gaps remain in the technical implementation layer.

Specifically, across the eight evaluated categories:
1. **Policy:** Most frameworks require formal written policy templates that developers can adopt.
2. **Documentation:** Guidelines exist for legal background, but step-by-step technical implementation runbooks are needed.
3. **Code:** Sample app codebases require reference implementations for age gating, withdrawal buttons, consent managers, and GPC signal handlers.
4. **Disclosure:** Onboarding and paywall templates must embed statutory disclosure strings.
5. **Logging:** Database schemas for logging consent, withdrawal, age-verification data purges, and law enforcement requests must be added.
6. **Testing:** Automated guard scripts and test runners must expand beyond store rejection patterns to validate live regulatory compliance rules.
7. **Evidence:** Physical compliance templates (VPATs, DPIA forms, EPOC forms, MIIT receipts) should be added to `templates/`.
8. **Audit Trail:** Standardized cryptographic audit logging specifications must be defined for high-risk regulatory interactions.

## 23. Official Primary Sources

- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US FTC COPPA Rule, 16 CFR Part 312
- California Privacy Rights Act (CPRA), California Civil Code 1798.100
- Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14
- US FTC Negative Option / Subscription Rule, 16 CFR Part 425
- UK Online Safety Act 2023, c. 50
- Australia Online Safety Amendment (Social Media Minimum Age) Act 2024
- Brazil Digital ECA, Lei n. 15.211/2025 and Decreto n. 12.880/2026
- India Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)
- Singapore Personal Data Protection Act 2012 (Act 26 of 2012)
- South Korea Telecommunications Business Act & PIPA Amendment (Act No. 21445)
- China MIIT Mobile Application Filing Notice (2023) and PIPL
