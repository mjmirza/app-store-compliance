# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, the US, the UK, Australia, Brazil, Canada, India, Singapore, South Korea, China, and other international jurisdictions, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
  Not applicable directly to runtime binary execution, but missing internal automation scripts or pre-commit hooks to verify developer literacy compliance.
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
Regulation (EU) 2022/1925 (Digital Markets Act) governs designated gatekeepers (including Apple's iOS/App Store and Google Play) to ensure contestability and fairness in digital markets. For developers distributing in the EU, the DMA enables alternative app distribution channels (Web Distribution, Alternative App Marketplaces) and alternative payment processing systems.

To utilize DMA entitlements, developers must sign platform addenda (e.g. Apple's Attachment 14 to ADPLA / Core Technology Commission framework) and comply with technical reporting and security notarization rules.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal organizational policy on EU DMA entitlement management, alternative payment processing, or alternative distribution governance.
- **Missing Documentation:**
  While `docs/EU-REGULATORY-2026.md` describes DMA mechanics, there are no step-by-step developer implementation guides for configuring `com.apple.developer.storekit.external-purchase-link` or handling External Purchase Server API transaction reporting.
- **Missing Code:**
  No template code exists in the repository for invoking `ExternalPurchaseCustomLink` sheets or handling monthly server-to-server transaction reporting to Apple/Google.
- **Missing Disclosure:**
  Templates omit the required system-level disclosure wording and UI sheets informing users that alternative payments or external links bypass store purchase protections.
- **Missing Logging:**
  No database schemas or logging modules exist to record EU digital transactions for monthly CTC / fee reconciliation and audit purposes.
- **Missing Testing:**
  No test scripts verify that external link entitlements or alternative payment flows trigger mandatory disclosure sheets without co-mingling in-app purchase options.
- **Missing Evidence:**
  The repository provides no template or proof of developer eligibility documentation (e.g., 1M EUR letter of credit or install thresholds) required for operating alternative marketplaces.
- **Missing Audit Trail:**
  No audit trail system tracks the historical submission of monthly external purchase reports or modifications to alternative billing handlers.

### 7.3 Remediation and Action Plan
1. Draft an internal DMA Entitlement and Payment Compliance Policy.
2. Build code templates for `ExternalPurchaseCustomLink` invocation and External Purchase Server API monthly reporting.
3. Add automated guard checks to ensure StoreKit IAP and external offer links are never co-mingled on the same EU storefront.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (Digital Services Act) establishes strict transparency, illegal content handling, and trader verification rules across online platforms operating in the EU. Articles 30 and 31 mandate that app stores verify and display trader status and contact details for all developers selling to EU consumers.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy or guideline exists to help organizations determine whether their entity qualifies as a "trader" under EU consumer law.
- **Missing Documentation:**
  Developer runbooks for submitting D-U-N-S numbers, trader contact details, and handling notice-and-action mechanisms under DSA Article 16 are absent.
- **Missing Code:**
  The automated guard script does not check whether DSA trader status declarations in App Store Connect or Google Play Console metadata are completed.
- **Missing Disclosure:**
  UI templates do not provide standard DSA notice-and-action reporting forms or trader contact disclosures for in-app user-generated content or marketplace items.
- **Missing Logging:**
  There are no logging mechanisms to record incoming DSA content notices, trader status verifications, or moderation actions.
- **Missing Testing:**
  No automated tests exist to verify that non-trader vs. trader status disclosures are displayed accurately on EU app store listings.
- **Missing Evidence:**
  The playbook lacks verified template examples of completed DSA trader declarations or notice-and-action response records.
- **Missing Audit Trail:**
  An unalterable audit trail tracking DSA illegal content notices, counter-notifications, and resolution timelines is absent.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Verification Guide and Notice-and-Action Policy.
2. Add metadata audit checks in `scripts/metadata-audit.py` to confirm DSA trader fields are populated before EU release.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) makes accessibility mandatory across mobile apps and e-commerce services in the EU market as of 28 June 2025, governed by harmonized standard EN 301 549.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an enterprise Accessibility Policy outlining EN 301 549 Chapter 11 compliance duties.
- **Missing Documentation:**
  No technical mapping exists between EN 301 549 rules and mobile platform accessibility APIs (VoiceOver/TalkBack).
- **Missing Code:**
  Although `scripts/accessibility-audit.py` exists, mock app templates lack full accessible implementation patterns (e.g. Dynamic Type auto-scaling, switch control focus ordering).
- **Missing Disclosure:**
  Templates do not include standard EN 301 549 Annex B/C Accessibility Statements for publishing in-app or on web storefronts.
- **Missing Logging:**
  No logging framework exists to track accessibility feedback or user-reported barrier incidents.
- **Missing Testing:**
  Automated tests in `scripts/accessibility-audit-test.sh` cover basic static analysis, but lack end-to-end screen reader navigation testing scripts.
- **Missing Evidence:**
  The repository contains no template for an Accessibility Conformance Report (VPAT / EN 301 549 evaluation sheet).
- **Missing Audit Trail:**
  No audit trail tracks historical accessibility audits, remediation timelines, or VPAT version updates.

### 9.3 Remediation and Action Plan
1. Publish an EAA / EN 301 549 Accessibility Policy and template Accessibility Statement.
2. Expand `scripts/accessibility-audit.py` and provide an Accessibility Conformance Report (VPAT) template.

---

## 10. US Children's Online Privacy Protection Act (COPPA) & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) and the Amended COPPA Rule (effective June 2025, general compliance April 2026) regulate the collection of personal information from children under 13 by operators of child-directed or mixed-audience services.

Official Citation: 16 CFR Part 312 (FTC).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive COPPA Compliance Policy covering data retention limits (312.10) and written information security programs (312.8).
- **Missing Documentation:**
  Runbooks for integrating FTC-approved verifiable parental consent (VPC) mechanisms are missing.
- **Missing Code:**
  Code templates lack zero-data-collection modes, age-gating triggers, or biometric identifier exclusion logic for child users.
- **Missing Disclosure:**
  Direct-to-parent notice templates and separate opt-in consent disclosures for targeted advertising are absent.
- **Missing Logging:**
  No database schemas exist to log parent consent grants, consent revocations, or age-gate failures.
- **Missing Testing:**
  No unit/integration tests verify that child accounts are completely blocked from third-party analytics/ad SDK calls.
- **Missing Evidence:**
  No templates exist for written data retention schedules or annual information security risk assessments under Section 312.8.
- **Missing Audit Trail:**
  No immutable audit trail tracks parent consent lifecycle events or child data purge executions.

### 10.3 Remediation and Action Plan
1. Draft a COPPA & Child Data Protection Policy.
2. Create code templates for zero-tracker child modes and verifiable parental consent flows.

---

## 11. California Privacy Framework (CCPA / CPRA / CPPA / DROP / AADC)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA) and 2026 CPPA regulations sets strict data privacy, automated decision-making opt-out, Global Privacy Control (GPC), and Delete Act (DROP) requirements.

Official Citation: California Civil Code Title 1.81.5 and 11 CCR section 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template exists covering California consumer privacy rights, automated decision-making technology (ADMT), or risk assessments.
- **Missing Documentation:**
  Detailed guides on implementing Global Privacy Control (`Sec-GPC`) in webviews and native opt-outs are missing.
- **Missing Code:**
  No code exists to parse `Sec-GPC` headers or automatically disable data sale/sharing pipelines upon signal detection.
- **Missing Disclosure:**
  In-app templates lack "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links/modals.
- **Missing Logging:**
  No backend logging schema exists to record consumer opt-out requests, deletion requests, or GPC header detections.
- **Missing Testing:**
  No automated tests verify that receiving a GPC signal halts tracking and data broker payload transmissions.
- **Missing Evidence:**
  Templates for California privacy risk assessments and annual data request metrics reports are absent.
- **Missing Audit Trail:**
  No audit trail system records CCPA deletion request fulfillment timelines (45-day window) or GPC policy updates.

### 11.3 Remediation and Action Plan
1. Implement CCPA/CPRA Privacy Policy templates and GPC detection code snippets.
2. Add automated guard checks for "Do Not Sell or Share" link requirements in webviews and native apps.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14/) regulates the collection, capture, purchase, receipt, storage, and handling of biometric identifiers (fingerprints, face scans, voiceprints). SB 2979 (2024) clarifies violation liability per person.

Official Citation: 740 ILCS 14/.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no formal Biometric Data Privacy Policy template.
- **Missing Documentation:**
  Developer guidelines on BIPA-compliant written release forms and 3-year destruction schedules are absent.
- **Missing Code:**
  No code snippets exist for presenting pre-capture biometric written consent screens or managing key retention.
- **Missing Disclosure:**
  UI templates omit mandatory pre-capture disclosures specifying biometric purpose and storage length.
- **Missing Logging:**
  No database schemas record biometric consent timestamps, written release acceptances, or automated deletion events.
- **Missing Testing:**
  No automated tests check whether biometric capture APIs (e.g. LocalAuthentication / BiometricPrompt) execute without prior release consent.
- **Missing Evidence:**
  No public biometric retention and destruction schedule template is provided in the repository.
- **Missing Audit Trail:**
  No audit trail tracks biometric data destruction timelines or consent revocations.

### 12.3 Remediation and Action Plan
1. Add a BIPA Biometric Compliance Policy and template written release disclosure.
2. Build sample code for pre-capture consent verification.

---

## 13. Subscription Cancellation Rules (FTC Click-to-Cancel / US ROSCA / UK DMCC)

### 13.1 Regulatory Overview and Background
US ROSCA, state negative option laws (California, New York, Massachusetts), and the UK Digital Markets, Competition and Consumers Act 2024 (DMCC Part 4 Ch 2) mandate that canceling a subscription must be at least as easy as starting one.

Official Citations: 15 U.S.C. 8401 (ROSCA), UK DMCC Act 2024.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal Negative Option and Subscription Renewal Policy.
- **Missing Documentation:**
  Developer guides for building self-service, 1-click subscription cancellation flows are missing.
- **Missing Code:**
  Web and companion account subscription code templates do not include in-app cancellation API endpoints.
- **Missing Disclosure:**
  Pre-checkout templates lack mandatory pre-contract subscription terms, auto-renewal notices, and cancellation instructions.
- **Missing Logging:**
  No schemas log pre-renewal notifications, cancellation attempts, or confirmation receipts.
- **Missing Testing:**
  No automated UI tests verify that canceling a subscription requires no phone calls or customer support chats.
- **Missing Evidence:**
  No templates exist for post-cancellation email confirmations or renewal notice logs.
- **Missing Audit Trail:**
  No audit trail tracks historical subscription retention flows or cancellation barrier edits.

### 13.3 Remediation and Action Plan
1. Draft a Subscription Cancellation Policy and checkout notice guidelines.
2. Build self-service subscription cancellation code templates.

---

## 14. UK Online Safety Act 2023

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 requires user-to-user and search services to enforce Highly Effective Age Assurance, prevent child exposure to illegal content, and perform statutory risk assessments enforced by Ofcom.

Official Citation: Online Safety Act 2023 (c. 50).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No UK Online Safety Policy or child safety governance template exists.
- **Missing Documentation:**
  Operational guides for Ofcom-approved age assurance methods (facial age estimation, open banking) are missing.
- **Missing Code:**
  No backend code exists to ringfence and immediately destroy age verification artifacts.
- **Missing Disclosure:**
  Templates lack UK-specific safety disclosures, age check notices, or illegal content reporting mechanisms.
- **Missing Logging:**
  No secure database schemas record CSEA incident reports or NCA portal submissions.
- **Missing Testing:**
  No tests verify that unverified child accounts are blocked from adult or user-to-user chat features.
- **Missing Evidence:**
  No template exists for an Ofcom Children's Risk Assessment or Illegal Content Risk Assessment report.
- **Missing Audit Trail:**
  No audit trail tracks age assurance data deletion or safety moderation decisions.

### 14.3 Remediation and Action Plan
1. Create a UK Online Safety Act Compliance Guide and Risk Assessment template.
2. Add code routines for age verification data destruction.

---

## 15. Australia Online Safety Framework

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 and App Distribution Services Online Safety Code (Schedule 7) enforce an under-16 social media ban and adult app download age assurance enforced by eSafety.

Official Citation: Online Safety Act 2021 as amended 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Australian Online Safety & Minimum Age Policy exists in the repository.
- **Missing Documentation:**
  Guides for implementing eSafety age assurance waterfall rules are absent.
- **Missing Code:**
  Code templates lack native age gating for Australian storefront accounts.
- **Missing Disclosure:**
  UI templates omit mandatory Australian age check notices and eSafety complaint disclosures.
- **Missing Logging:**
  No schemas log age verification execution or data destruction under Australian privacy principles.
- **Missing Testing:**
  No unit tests verify that Australian accounts under 16 are blocked from restricted social features.
- **Missing Evidence:**
  No template exists for an Australian Industry Code Risk Assessment or eSafety compliance record.
- **Missing Audit Trail:**
  No audit trail tracks age verification data destruction or profile restriction updates.

### 15.3 Remediation and Action Plan
1. Publish an Australian Online Safety Compliance Policy.
2. Build age-gating code snippets aligned with eSafety guidelines.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto n. 12.880 regulate child online safety, age verification (CPF check, facial estimation), loot box restrictions, and parental authorization, enforced by ANPD.

Official Citation: Lei n. 15.211/2025 and Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no Brazil Digital ECA & Child Protection Policy template.
- **Missing Documentation:**
  Runbooks for integrating ANPD-approved age verification and loot box 18+ auto-rating rules are missing.
- **Missing Code:**
  No code snippets integrate with Google Play Age Signals API or Apple Declared Age Range for Brazil accounts.
- **Missing Disclosure:**
  Onboarding templates omit mandatory age rating disclosures and parental consent notices in Portuguese.
- **Missing Logging:**
  No logging schemas record guardian authorization grants, CPF checks, or verification data purges.
- **Missing Testing:**
  No integration tests verify that loot box mechanics are disabled for minor Brazilian accounts.
- **Missing Evidence:**
  No template exists for an ANPD Child Impact Assessment or age verification audit report.
- **Missing Audit Trail:**
  No audit trail records raw verification document purges or guardian authorization updates.

### 16.3 Remediation and Action Plan
1. Formulate a Brazil Digital ECA Compliance Policy.
2. Code integrations for Google Play Age Signals API and Apple Declared Age Range API for Brazil.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 mandate explicit consent notices, Consent Managers, verifiable parental consent for under-18s, and prohibition of behavioral tracking on children.

Official Citation: Act No. 22 of 2023 & G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No India DPDPA Data Protection Policy template is present in the playbook.
- **Missing Documentation:**
  Guides for integrating with registered Consent Managers and DigiLocker parental consent are missing.
- **Missing Code:**
  Code templates lack multilingual consent notices (22 scheduled languages) and under-18 ad tracking blockers.
- **Missing Disclosure:**
  Pre-consent disclosures lack explicit itemized data purpose lists and Data Protection Officer contact details.
- **Missing Logging:**
  No database schemas record consent grants, Consent Manager tokens, or parent verifications.
- **Missing Testing:**
  No automated tests check whether tracking SDKs are suppressed for Indian child users.
- **Missing Evidence:**
  No template exists for a DPDPA Data Protection Impact Assessment (DPIA) or Significant Data Fiduciary audit.
- **Missing Audit Trail:**
  No audit trail records consent withdrawal requests or Data Principal grievance resolutions.

### 17.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Policy and Consent Manager integration guide.
2. Build code logic to disable behavioral tracking for accounts under 18 in India.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require app store age assurance (from 1 April 2026), 3-day breach notifications, and data protection officer designation.

Official Citation: Personal Data Protection Act 2012 and IMDA Code 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore PDPA & IMDA Online Safety Policy template exists.
- **Missing Documentation:**
  Developer guidelines on IMDA age assurance screening and 3-day breach reporting are absent.
- **Missing Code:**
  No code exists to verify age signals for Singapore storefront downloads.
- **Missing Disclosure:**
  In-app disclosures omit DPO contact information and PDPA purpose notifications.
- **Missing Logging:**
  No database schemas record PDPA consent withdrawals or IMDA age check signals.
- **Missing Testing:**
  No automated tests verify 18+ download gating on Singapore storefront builds.
- **Missing Evidence:**
  No template exists for a Singapore Data Protection Impact Assessment (DPIA).
- **Missing Audit Trail:**
  No audit trail tracks breach discovery-to-notification timelines or age data deletion.

### 18.3 Remediation and Action Plan
1. Publish a Singapore PDPA Policy template.
2. Create age assurance verification helper functions.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment support (26% commission model), while PIPA (Act No. 21445) enforces strict CEO accountability and consent rules.

Official Citation: Telecommunications Business Act Article 22-9 & PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No South Korea In-App Payment & PIPA Compliance Policy exists.
- **Missing Documentation:**
  Step-by-step runbooks for obtaining Korea-specific entitlements (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`) and approved Korean payment gateways (KCP, Toss) are missing.
- **Missing Code:**
  No code templates exist for rendering mandatory Korean external payment modal sheets or handling monthly sales reporting.
- **Missing Disclosure:**
  UI templates omit required Korean modal disclosures informing users that Apple/Google purchase protections do not apply to external Korean payment gateways.
- **Missing Logging:**
  No database schemas record Korean external transactions for 15-day monthly reporting.
- **Missing Testing:**
  No unit/integration tests verify that Korea-specific binaries isolate external payment handlers without co-mingling standard IAP.
- **Missing Evidence:**
  No template exists for PIPA Chief Privacy Officer (CPO) board approval records or Korean transaction reports.
- **Missing Audit Trail:**
  No audit trail tracks monthly remittance reporting to Apple/Google or PIPA consent updates.

### 19.3 Remediation and Action Plan
1. Draft a South Korea Alternative Payment & PIPA Policy.
2. Build code templates for Korean external purchase modal sheets and monthly transaction reporting.

---

## 20. China Mobile App Filing (MIIT) & CAC AI/Minors Regulations

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) for all distributed apps. The Cyberspace Administration of China (CAC) Order No. 21 regulates AI anthropomorphic services (minors mode, guardian consent under 14, virtual companion bans for minors).

Official Citations: MIIT Notice on Mobile App Filing (2023) & CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China App Filing & CAC Compliance Policy template is provided in the repository.
- **Missing Documentation:**
  Developer runbooks for obtaining local Chinese partner licensing, Banhao game licenses, and MIIT app filing are missing.
- **Missing Code:**
  Code templates lack CAC-mandated automatic "Minors Mode" triggers, real-name authentication hooks, and anti-addiction timers.
- **Missing Disclosure:**
  UI templates omit mandatory MIIT filing number disclosures in app settings/footers and CAC AI companion warnings.
- **Missing Logging:**
  No database schemas record real-name authentication verification tokens or minor usage duration logs.
- **Missing Testing:**
  No automated tests check whether minor accounts are forcibly logged off during restricted evening hours under Chinese anti-addiction rules.
- **Missing Evidence:**
  No templates exist for CAC personal information compliance audit reports or MIIT filing proof documents.
- **Missing Audit Trail:**
  No audit trail records real-name data verification or CAC minor mode toggle events.

### 20.3 Remediation and Action Plan
1. Publish a China Regulatory Compliance Guide (MIIT filing, CAC AI rules).
2. Build code templates for CAC Minors Mode switching and real-name authentication integration.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU EAA** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is exceptionally strong on app store review rejection patterns and platform guidelines. However, across global and regional statutory laws, while nineteen of twenty frameworks are referenced with dated sources in `docs/EU-REGULATORY-2026.md` and `docs/GLOBAL-REGULATORY-2026.md`, the operational implementation layer—specifically runnable code templates, backend logging schemas, automated test assertions, compliance evidence templates, and unalterable audit trails—remains missing or incomplete.

Priority roadmap for the playbook:

1. **GPSR Integration:** Add full GPSR coverage across all 8 dimensions as it is currently absent end-to-end.
2. **Implementation Blueprints:** Provide copy-pasteable code templates for EU Article 50 AI disclosures, Contract Withdrawal buttons, Declared Age Range / Play Age Signals integrations, and GPC header parsers.
3. **Automated Testing & Audit Trail Utilities:** Develop automated CI test scripts and cryptographic audit logging helpers to enable developers to verify statutory compliance prior to release.

Re-run and re-verify this report regularly against official primary sources (EUR-Lex, FTC, legislation.gov.uk, eSafety, ANPD, etc.) to adapt to moving regulatory dates.

---

## 23. Sources

Every regulation named above, cited at its primary official source:

- GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Digital Markets Act (DMA): [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- Digital Services Act (DSA): [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act (EAA): [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California CCPA/CPRA: [California Civil Code Title 1.81.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)
- Illinois BIPA: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act: [Online Safety Act 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Brazil Digital ECA: [Lei n. 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore PDPA: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act: [Act No. 18200](https://law.go.kr)
- China CAC AI Measures: [CAC Order No. 21](https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm)
