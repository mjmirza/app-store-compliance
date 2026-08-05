# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major modern regulations that bind app developers shipping globally, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, entered into force on 1 November 2022 and became fully applicable on 2 May 2023. It targets large online platform "gatekeepers" to ensure contestable and fair markets in the digital sector.

For application developers, the DMA establishes rights to distribute software through alternative app store marketplaces, distribute signed binaries directly from websites, utilize alternative in-app billing engines, and promote external purchases directly within applications.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides developers with no structured policy templates to assess whether utilizing alternative marketplaces or external billing entitlements aligns with their commercial or compliance risks.
- **Missing Documentation:**
  The repository lacks practical guidelines detailing the requirements for iOS direct web distribution, alternative marketplace configuration, or the commission stacking under the Alternative Terms Addendum.
- **Missing Code:**
  The repository's billing templates have no code blocks executing Apple's required `ExternalPurchaseCustomLink` system-provided disclosure sheet, nor do they support secure monthly sales reporting APIs.
- **Missing Disclosure:**
  Frontend checkout screens and metadata samples fail to display the required in-app consumer disclosures regarding the loss of App Store protections (e.g., Family Sharing, Ask-to-Buy) during alternative payment flows.
- **Missing Logging:**
  There are no logging provisions or database schemas in the repository designed to capture and log external-link redirections, alternative payment click-throughs, or monthly commission reports.
- **Missing Testing:**
  No automated integration or unit tests exist to verify that alternative billing components execute without functional breakage or that redirection links dynamically render based on region signals.
- **Missing Evidence:**
  The playbook does not supply templates for monthly sales reporting sheets, signed Alternative Terms agreements, or commission remittance logs.
- **Missing Audit Trail:**
  An unalterable audit trail tracking when specific external entitlements were implemented, when terms were signed, and how alternative payment options were deployed is not defined.

### 7.3 Remediation and Action Plan
1. Draft a comprehensive DMA Alternative Terms and Billing Policy to guide the deployment of external purchase links and non-WebKit browser engines.
2. Develop front-end code templates utilizing the `ExternalPurchaseCustomLink` API and displaying compliant alternative payment choice sheets.
3. Create database schemas to securely capture alternative billing activities and generate monthly sales summaries.
4. Integrate end-to-end UI tests simulating direct external checkout flows and verifying compliance metadata.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, entered into force on 16 November 2022 and became fully applicable on 17 February 2024. It establishes a modern harmonized framework on the liability and duties of intermediary services, including app distribution stores.

Under Articles 30 and 31 of the DSA, the App Store and Google Play are legally mandated to verify and publish "trader" contact and identity details (phone, email, postal address, and D-U-N-S verification) for all entities distributing apps to EU consumers. Non-compliance results in the immediate removal of applications from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook offers no template policy to help developers assess whether their organizational or individual status classifies them as a "trader" under EU consumer law, or how to declare "not a trader" safely.
- **Missing Documentation:**
  The repository lacks developer-facing runbooks illustrating the step-by-step 2FA identity, payment, and document verification processes required on App Store Connect and Google Play Console.
- **Missing Code:**
  No static validation checks exist in the automated compliance guard to verify that public contact metadata is present and aligned with declared trader information when EU distribution is enabled.
- **Missing Disclosure:**
  The repository lacks onboarding or metadata templates that disclose to the user that consumer-protection rights do not apply if the developer is legally registered as "not a trader".
- **Missing Logging:**
  There are no backend schemas or tracking structures to log consumer-protection inquiries, EU-specific compliance complaints, or verified trader detail updates.
- **Missing Testing:**
  No automated metadata linter checks exist to verify that required trader credentials (D-U-N-S address, email, phone) are correctly displayed in regional store listings.
- **Missing Evidence:**
  The playbook does not carry verified examples of successfully submitted EU trader documents, business registrations, or dual-factor contact confirmations.
- **Missing Audit Trail:**
  A secure audit trail tracking updates to corporate address records, phone verifications, and regional storefront exclusions is completely absent.

### 8.3 Remediation and Action Plan
1. Establish a written DSA Trader Status Compliance Guideline outlining registration, verification, and storefront exposure obligations.
2. Implement automated script checks in the metadata audit tools to warn of missing or incomplete organization contact details for EU listings.
3. Provide interface mockups displaying public-facing trader contact cards for the app "About" menu.
4. Document the precise 2FA verification steps for App Store Connect to prevent silent app removals from EU storefronts.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable on 28 June 2025 across all EU Member States. It mandates strict accessibility requirements for a broad range of digital consumer products and services, including e-commerce apps, transport services, banking apps, and e-books.

Extending far beyond basic WCAG standards, the EAA is legally enforced through the EN 301 549 harmonized standard (specifically Chapter 11 for mobile apps). Failure to comply can lead to severe administrative penalties, market recall, and court-ordered product bans.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not provide a template Accessibility Policy or compliance strategy statement mapping out EAA microenterprise exemptions and technical milestones.
- **Missing Documentation:**
  The repository lacks technical guidelines illustrating the distinct mobile app requirements under EN 301 549 Chapter 11 (such as switch control, AssistiveTouch integration, and dynamic layout scaling boundaries).
- **Missing Code:**
  Although the playbook mentions accessibility conceptually, the frontend mock implementations do not include fluidly scaling layout containers or custom accessibility element matrices.
- **Missing Disclosure:**
  There are no templates or placeholders for the legally mandated, public-facing Accessibility Statement that must be published and linked within the app interface.
- **Missing Logging:**
  No logging architectures or schemas are provided to log accessibility-related feedback, user complaints, or system font-scaling settings.
- **Missing Testing:**
  The automated compliance guard does not check custom UI code for missing screen-reader labels (`accessibilityLabel`), contrast ratio failures, or fixed-layout containers that clip large text.
- **Missing Evidence:**
  The repository lacks templates of Voluntary Product Accessibility Templates (VPATs), EN 301 549 conformance checklists, or accessibility audit reports.
- **Missing Audit Trail:**
  A systematic log tracking historical accessibility evaluations, design reviews, and accessibility-issue resolutions is completely missing.

### 9.3 Remediation and Action Plan
1. Formulate a corporate Accessibility Compliance Policy mapped to EN 301 549 Chapter 11 and WCAG 2.1 Level AA.
2. Develop and commit fully fluid UI code patterns demonstrating text scaling, screen-reader compatibility, and logical focus order.
3. Incorporate a standard in-app template for a legally compliant Accessibility Statement.
4. Integrate static analysis rules into the pre-submission guard to flag missing accessibility identifiers and non-conforming color contrast.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6508, is enforced by the Federal Trade Commission (FTC). The highly demanding amended COPPA Rule (effective 23 June 2025, with full compliance by 22 April 2026) fundamentally expands children's data privacy obligations.

The 2026 updates expand personal information to include biometric templates, genetic identifiers, and government IDs, require separate opt-in consent for third-party disclosure/targeted ads, mandate written data retention policies, and enforce formal written information security programs.

Official Citation: 16 CFR Part 312, Federal Trade Commission.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not contain a template children's data minimization and retention policy, nor does it provide a model written information security program as required by 16 CFR Section 312.8.
- **Missing Documentation:**
  The playbook lacks operational runbooks explaining how to manage separate opt-in consent paths for third-party ad sharing and general app usage under the 2026 Rule.
- **Missing Code:**
  The codebase has no secure, child-directed age-gate widgets, verifiable parental consent (VPC) modal prompts, or automated third-party tracker exclusion logic.
- **Missing Disclosure:**
  There are no standardized model privacy disclosure notices compliant with the detailed, age-appropriate children's notice specifications of 16 CFR Section 312.4.
- **Missing Logging:**
  No database schemas or secure storage provisions are supplied to log parental consent approvals, consent revocations, or biometric data exclusion indicators.
- **Missing Testing:**
  The automated test engines do not check whether third-party tracking networks, analytics SDKs, or ad-serving scripts are active when a minor profile is detected.
- **Missing Evidence:**
  The repository is missing templates of COPPA-compliant parental consent agreements, identity verification logs, or annual child privacy risk assessments.
- **Missing Audit Trail:**
  An immutable audit trail documenting the lifecycle of parental consent acquisition, consent renewals, and child profile data deletion events is completely absent.

### 10.3 Remediation and Action Plan
1. Establish a comprehensive Children's Privacy and Biometric Data Retention Policy in accordance with the 2026 COPPA Rule.
2. Create reusable, secure in-app age gating and parental verification components.
3. Add automated network-traffic linter checks to block advertising SDKs inside sections marked as child-directed.
4. Establish cryptographic database logs to track parental consent states and automated child data-purging schedules.

---

## 11. California Privacy (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), Cal. Civ. Code Section 1798.100 et seq., is enforced by the California Privacy Protection Agency (CPPA) and California Attorney General. Detailed updated regulations took full legal effect on 1 January 2026.

The California framework mandates extensive consumer privacy rights (know, delete, correct, opt-out of data sale/sharing/profiling), strict notice-at-collection rules, and the automated honoring of Global Privacy Control (GPC) opt-out signals.

Official Citation: Cal. Civ. Code Section 1798.100 et seq., and CPPA Regulations.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a model notice-at-collection policy, a CCPA-compliant privacy policy template, or written procedures for handling consumer rights requests.
- **Missing Documentation:**
  There are no developer-facing guidelines explaining how to detect, parse, and natively process the Global Privacy Control (`Sec-GPC`) header signal inside mobile app webviews or native networking stacks.
- **Missing Code:**
  The codebase is missing middleware or utility helper classes to capture GPC signals, stop third-party SDK transfers, or render "Do Not Sell or Share My Info" modal sheets.
- **Missing Disclosure:**
  Standard checkout screens and onboarding interfaces do not provide compliant, prominent links for "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information".
- **Missing Logging:**
  No database schemas or logging architectures exist to record consumer opt-out preferences, GPC signal receipts, or sensitive personal data limitation requests.
- **Missing Testing:**
  The test runner lacks integration scripts validating that tracking endpoints and telemetry transmission are completely suppressed when a CCPA opt-out flag is set.
- **Missing Evidence:**
  The repository does not contain templates for 45-day SLA response tracking logs, Privacy Impact Assessments (PIAs), or annual consumer request metrics summaries.
- **Missing Audit Trail:**
  An unalterable, secure audit log documenting when consumer opt-outs were registered, when backend deletions were completed, and how data-exclusion rules were executed is not implemented.

### 11.3 Remediation and Action Plan
1. Formulate a California Consumer Privacy Policy covering CPPA 2026 regulations and notice-at-collection mandates.
2. Develop native codebase utilities to detect Global Privacy Control (`Sec-GPC`) headers and automatically restrict analytics data transmission.
3. Embed prominent "Do Not Sell or Share" link templates inside in-app privacy menus.
4. Design secure database structures to record opt-out request lifecycles and backend execution signals.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, is one of the most stringent biometric privacy laws in the United States. It regulates the collection, use, safeguarding, and destruction of biometric identifiers (including facial templates, retina scans, fingerprints, and voiceprints).

BIPA requires written notice, an e-signed written release (consent) before capture, an active public retention and destruction schedule, and strictly prohibits the sale or transfer of biometric data. Severe statutory damages are enforced via a private right of action.

Official Citation: 740 ILCS 14, Illinois General Assembly.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook is missing a template biometric data privacy policy outlining retention periods, security controls, and destruction timelines.
- **Missing Documentation:**
  No instructions exist detailing how to design a legally compliant, two-step biometric registration flow that captures valid written releases.
- **Missing Code:**
  The codebase lacks biometric consent components, face-matching opt-in prompts, or backend triggers executing the 3-year maximum data destruction cycle.
- **Missing Disclosure:**
  Onboarding templates do not display the required written biometric notice explaining the specific purpose, storage method, and deletion schedule of the biometric data.
- **Missing Logging:**
  No database logging schemas capture biometric capture timestamps, consent approvals, biometric template hashing, or deletion markers.
- **Missing Testing:**
  No unit or integration tests exist to verify that biometric scanning SDKs are blocked from initialization until a valid, signed release is recorded in the user profile.
- **Missing Evidence:**
  The playbook lacks templates for BIPA-compliant biometric deletion logs, independent verification audits, or third-party processor declarations.
- **Missing Audit Trail:**
  A secure, cryptographic audit trail documenting the lifecycle of biometric consent capture, database matching events, and ultimate deletion is entirely absent.

### 12.3 Remediation and Action Plan
1. Draft an Illinois BIPA Biometric Privacy Policy and public retention schedule template.
2. Build an in-app biometric authorization modal template with e-signature capture functionality.
3. Develop automated database purge procedures executing biometric data destruction.
4. Integrate unit tests verifying the strict gating of biometric SDKs prior to user consent.

---

## 13. US Subscription Cancellation (Negative Option Rule / ROSCA)

### 13.1 Regulatory Overview and Background
US subscription compliance is governed by the Restore Online Shoppers' Confidence Act (ROSCA), 15 U.S.C. Section 8401 et seq., Section 5 of the FTC Act (prohibiting unfair or deceptive acts), and strict state-level negative option statutes (California, New York, Massachusetts).

These frameworks collectively dictate that any negative-option billing or automatically renewing subscription offered online must provide a cancellation mechanism that is at least as simple, direct, and frictionless as the signup process (the classic "click to cancel" standard).

Official Citations: 15 U.S.C. Section 8401 (ROSCA); Cal. Bus. & Prof. Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template negative-option billing policy or compliance roadmap for web-billed or companion subscription flows.
- **Missing Documentation:**
  The repository is missing UI/UX design manuals outlining how to construct frictionless, self-service subscription cancellation paths that do not require phone calls, letters, or multi-step retention walls.
- **Missing Code:**
  No functional code blocks, account setting panels, or automated webview links implementing direct subscription cancellation or refund triggers are provided.
- **Missing Disclosure:**
  Onboarding subscription registration screens do not contain clear, conspicuous disclosure cards outlining recurring charges, billing frequencies, and cancellation instructions.
- **Missing Logging:**
  No backend database schemas are provided to log recurring billing consents, cancellation click events, or retention save-offer metrics.
- **Missing Testing:**
  The test suites do not include automated UI tests verifying that a user can complete subscription termination independently in a single, frictionless session.
- **Missing Evidence:**
  The repository is missing templates of automated cancellation receipts, contract revocation confirmation logs, or billing dispute records.
- **Missing Audit Trail:**
  There is no secure audit trail tracking historical changes to subscription pricing terms, cancellation flows, or terms of service updates.

### 13.3 Remediation and Action Plan
1. Establish a written US Subscription and Negative Option Compliance Policy matching ROSCA and California Cal-SHOPPA requirements.
2. Develop a clean in-app subscription cancellation panel template within account settings.
3. Program automated UI tests validating that cancellation is executed with zero administrative hurdles.
4. Incorporate clear, prominent billing disclosure components on subscription signup templates.

---

## 14. UK Online Safety Act

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enacted on 26 October 2023 with key age-assurance duties taking full legal effect on 25 July 2025, establishes Ofcom as the digital safety regulator. It places a statutory duty of care on online service providers to protect children from illegal and harmful content.

Under Ofcom's guidelines, services accessible to UK minors must implement "Highly Effective Age Assurance" methods (such as facial age estimation, open banking, or credit card verification) that go far beyond simple age self-declaration checkboxes.

Official Citation: Online Safety Act 2023, UK Public General Acts.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template policy guiding developers on how to classify harmful content or how to implement Ofcom-conforming child protection programs.
- **Missing Documentation:**
  No technical documentation exists detailing Ofcom-approved age assurance vendors, API parameters, or the mandatory Age Appropriate Design criteria.
- **Missing Code:**
  The codebase contains no integration scripts, API client classes, or frontend hooks to connect with certified UK age verification providers.
- **Missing Disclosure:**
  Onboarding screens lack templates explaining to UK users how their identity or biometric data is processed during age estimation, and how data privacy is preserved.
- **Missing Logging:**
  No database schemas exist to record successful age verification events in a secure, minimized format that avoids storing raw PII.
- **Missing Testing:**
  There are no automated test cases simulating underage accounts attempting to access restricted features or bypass age gating.
- **Missing Evidence:**
  The repository does not carry templates of UK Online Safety child-safety risk assessments or data protection impact assessments (DPIAs) for Ofcom.
- **Missing Audit Trail:**
  An unalterable log recording changes to age-assurance thresholds, content moderation algorithms, and Ofcom compliance audits is completely absent.

### 14.3 Remediation and Action Plan
1. Formulate a UK Online Safety Compliance Policy and content risk-mitigation strategy.
2. Develop third-party age-assurance API wrappers and credential verification code templates.
3. Establish privacy-centric database models to record age confirmation states without capturing user PII.
4. Embed automated end-to-end test sequences simulating underage user account restrictions.

---

## 15. Australia Online Safety (Social Media Minimum Age Act)

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 entered into force on 10 December 2025 in Australia. It bans minors under the age of 16 from holding accounts on designated social media platforms, placing heavy enforcement duties on operators.

The eSafety Commissioner mandates that platforms take reasonable, highly reliable steps to verify user age. Crucially, any age verification data captured for compliance must be strictly ringfenced and destroyed immediately after the verification is completed.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024, Commonwealth of Australia.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not carry minor-exclusion policy templates or children's data-destruction policies tailored to Australian eSafety mandates.
- **Missing Documentation:**
  The checklists lack technical guidelines explaining how to ringfence Australian user data or how to configure automatic database purging hooks.
- **Missing Code:**
  The codebase lacks database triggers, cron job scripts, or API endpoints designed to automatically purge raw age-verification documents immediately post-verification.
- **Missing Disclosure:**
  Onboarding screens do not display mandatory notices informing Australian users of the legal 16-plus age restriction and the immediate data-deletion policy.
- **Missing Logging:**
  There is no backend logging architecture capturing cryptographic proof of data purging events or age-check completion indicators.
- **Missing Testing:**
  No automated tests exist to scan database storage fields post-verification and verify that raw age data (such as government IDs) is completely expunged.
- **Missing Evidence:**
  The playbook lacks templates of Australian eSafety Commissioner compliance certificates, data minimization reports, or privacy impact assessments (PIAs).
- **Missing Audit Trail:**
  An immutable audit trail documenting the schedule and execution history of raw age-data purging scripts is completely missing.

### 15.3 Remediation and Action Plan
1. Draft an Australian Minor Exclusion and Data Minimization Policy outlining age verification and immediate purging rules.
2. Develop automated database purge triggers and background cron-job scripts in python or SQL.
3. Integrate automated post-verification storage scanning tests to confirm that raw ID documents are deleted.
4. Establish cryptographic logs proving compliance to the Australian eSafety Commissioner.

---

## 16. Brazil Digital ECA

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) is enforceable from 17 March 2026, on top of the General Data Protection Law (LGPD). It regulates child safety online and is heavily enforced by the National Data Protection Authority (ANPD) and the National Secretariat for Children and Adolescents.

The Digital ECA strictly prohibits simple age self-declaration checkboxes for apps with mature or commercial content. Developers must utilize robust verification methods such as document validation, facial matching, or CPF database checks.

Official Citation: Lei Numero 15.211 de 17 de Marco de 2025, Brazil.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks written policy templates to evaluate Brazilian age-assurance requirements or define LGPD child-consent compliance workflows.
- **Missing Documentation:**
  Missing developer runbooks detailing how to query Brazil's CPF (Cadastro de Pessoas Físicas) registration databases or utilize certified local age estimation APIs.
- **Missing Code:**
  No client-side or server-side code integrations with Brazilian CPF verification endpoints or biometric age-gating modules are provided.
- **Missing Disclosure:**
  Onboarding user interfaces do not display required Brazilian disclosures explaining that self-declaration is legally prohibited for mature or loot-box-enabled apps.
- **Missing Logging:**
  The repository is missing database logging schemas to securely log CPF verification outcomes or LGPD-compliant parental consent confirmations.
- **Missing Testing:**
  No automated localization tests exist to verify that users connecting from Brazilian IP addresses are routed through strict age verification pipelines rather than self-declaration.
- **Missing Evidence:**
  The playbook does not contain templates for LGPD child privacy risk assessments or ANPD-ready compliance proofs.
- **Missing Audit Trail:**
  An unalterable audit trail recording changes to Brazilian age-gating rules, database validations, and compliance audits is completely absent.

### 16.3 Remediation and Action Plan
1. Establish a written Brazil Digital ECA Compliance Policy mapping LGPD children's privacy rules.
2. Build code templates querying Brazilian CPF verification APIs and processing biometric age estimation.
3. Develop localization hooks forcing Brazilian users into strict age gating flows.
4. Create database logging schemas to track LGPD parental consent captures and ANPD-ready proof files.

---

## 17. India DPDPA

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025 (notified 13 November 2025), schedules children's consent and tracking regulations for full enforcement starting 13 May 2027.

The DPDPA classifies everyone under the age of 18 as a child. It strictly mandates verifiable parental consent through government-backed digital frameworks (such as DigiLocker) before processing any child data, and completely prohibits the behavioral tracking and targeted profiling of minors.

Official Citation: Digital Personal Data Protection Act, 2023, Parliament of India.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template policy for Indian DPDPA children's data protection, nor does it define rules to govern minor tracking restrictions.
- **Missing Documentation:**
  The repository lacks technical guidelines illustrating how to integrate Indian government-backed consent services (e.g., DigiLocker) or configure minor-restricted ad pipelines.
- **Missing Code:**
  No API clients, backend hooks, or webhook verification classes exist to integrate with Indian national e-consent frameworks or DigiLocker APIs.
- **Missing Disclosure:**
  The repository lacks standardized, bilingual privacy notices in English and scheduled Indian languages as required under the DPDP Rules.
- **Missing Logging:**
  There are no database logging schemas tracking the acquisition, verification, or revocation of Indian parental consent signals.
- **Missing Testing:**
  The test engines do not check whether tracking cookies and behavioral ad network SDKs are completely deactivated for users under 18 in India.
- **Missing Evidence:**
  The playbook does not provide templates for Indian DPDPA compliance self-assessments or Indian Data Processing Agreements (DPAs).
- **Missing Audit Trail:**
  An immutable audit trail documenting parental consent verifications, user profiling deactivations, and DPDP compliance reviews is completely absent.

### 17.3 Remediation and Action Plan
1. Formulate an Indian DPDPA Children's Privacy and Ad-Tracking Prohibition Policy.
2. Develop backend wrappers and webhook targets for Indian DigiLocker parental consent verification.
3. Integrate automated test checks to ensure that all profiling and telemetry SDKs are completely disabled for Indian minors.
4. Include multilingual DPDPA notice templates inside the repository's references folder.

---

## 18. Singapore PDPA/IMDA Code of Practice

### 18.1 Regulatory Overview and Background
The Personal Data Protection Act (PDPA) of Singapore and the Infocomm Media Development Authority (IMDA) Code of Practice for Online Safety for App Distribution Services require robust digital safety controls, with key app-store age assurance rules fully applicable from 1 April 2026.

Under these mandates, app distribution services and app developers must screen and prevent users estimated under 18 from downloading or accessing age-inappropriate content. Verification data must be minimized and destroyed once the verification purpose is completed.

Official Citation: Personal Data Protection Act 2012, and IMDA Code of Practice, Singapore.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template policy guiding developers on Singapore-specific age-appropriate filtering or PDPA-compliant children's data destruction.
- **Missing Documentation:**
  The repository lacks developer manuals on how to configure IMDA-compliant age filters or how to manage verification logs safely.
- **Missing Code:**
  No frontend or backend logic exists in the codebase to dynamically apply mature-content locks or automate age data-purging workflows for Singaporean users.
- **Missing Disclosure:**
  Onboarding templates do not provide placeholder disclosures notifying Singaporean consumers that age estimation is active to comply with IMDA online safety regulations.
- **Missing Logging:**
  No database logging structures or schemas capture Singapore compliance reviews, successful age screening events, or the destruction of verification artifacts.
- **Missing Testing:**
  No automated UI tests check whether mature content is successfully hidden from users who fail Singapore's age confirmation flow.
- **Missing Evidence:**
  The playbook lacks templates for IMDA-conforming self-assessments, child protection risk audits, or PDPA-compliant processing records.
- **Missing Audit Trail:**
  An unalterable log tracing age-assurance threshold modifications, IMDA compliance reviews, and data-purging executions is completely missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA and IMDA Online Safety Compliance Policy.
2. Develop mature-content filter wrappers and dynamic age-gating triggers inside the backend codebase.
3. Incorporate automated test scripts verifying content blockage for under-18 Singapore accounts.
4. Design secure, minimized database schemas to log verification events without storing raw identity attributes.

---

## 19. South Korea Telecommunications Act (Alternative Billing)

### 19.1 Regulatory Overview and Background
The South Korean Telecommunications Business Act, amended in 2021 with enforcement starting 15 March 2022, legally prohibits app store operators from forcing developers to use a single proprietary payment system. It establishes a statutory right to use alternative in-app payment systems.

Apple's approved implementation for the Korean storefront enforces strict technical rules: developers must use approved Korean billing SDKs (KCP, Inicis, Toss, NICE), display a system alternative-billing choice sheet, remit a 26 percent commission, report monthly sales within 15 days, and publish a Korea-only binary.

Official Citation: Telecommunications Business Act, South Korea.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no model policy or risk matrix guiding developers on the technical and financial overhead of South Korean alternative billing.
- **Missing Documentation:**
  The repository is missing granular developer guides illustrating how to navigate the South Korean payment provider approval process or complete monthly commission spreadsheets.
- **Missing Code:**
  The codebase lacks integration wrappers for Korean billing SDKs, alternative payment selection modals, or Apple's required native payment choice sheets.
- **Missing Disclosure:**
  There are no UI templates of the mandatory South Korean alternative-purchase modal disclosure screen that warning users of the loss of App Store protections.
- **Missing Logging:**
  No database logging schemas are provided to record South Korean alternative billing transactions or compile the mandatory monthly sales reporting spreadsheets.
- **Missing Testing:**
  The test suites do not include automated integration or unit tests verifying that the Korea-specific binary displays payment options correctly under localized system flags.
- **Missing Evidence:**
  The playbook does not carry templates for South Korean monthly sales reporting spreadsheets or commission remittance logs.
- **Missing Audit Trail:**
  A systematic log tracking alternative payment configurations, commission calculations, and updates to Korean payment gateways is completely missing.

### 19.3 Remediation and Action Plan
1. Formulate a South Korean Alternative In-App Billing Compliance Policy.
2. Develop front-end choice sheets and alternative billing modal screen templates.
3. Create database logging schemas to track Korean gateway transactions and generate monthly reporting sheets.
4. Program automated unit tests validating Korea-specific billing components under regional flags.

---

## 20. China App Filing (MIIT)

### 20.1 Regulatory Overview and Background
In accordance with the Ministry of Industry and Information Technology (MIIT) of China, Mobile App Filing (an extension of the established internet ICP filing system) is strictly mandatory under the Anti-Telecom and Online Fraud Law. New apps from 1 September 2023, and existing apps by 31 March 2024, must be fully filed or face immediate store takedown.

Filing requires a registered Chinese business entity or local partner, strict real-name verification, localized data processing in compliance with the Personal Information Protection Law (PIPL), and an official Banhao license for game distribution.

Official Citation: Circular of the Ministry of Industry and Information Technology on Launching Mobile Internet Application Filing Work, China.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no written policy templates or strategic plans for foreign developers looking to navigate China-specific app distribution rules.
- **Missing Documentation:**
  The checklists lack detailed instructions on finding a Chinese partner, submitting filing documents to the MIIT system, or complying with PIPL data localization rules.
- **Missing Code:**
  No frontend or backend codebase templates exist to handle Chinese real-name phone verification, MIIT-compliant SMS verification, or local server data-routing.
- **Missing Disclosure:**
  Onboarding templates do not showcase how to prominently display the MIIT filing number in the app's "About" screen or "Settings" page as legally required.
- **Missing Logging:**
  There are no database schemas or data-handling logs designed to track real-name verification statuses or localized PIPL data transfer consent.
- **Missing Testing:**
  The test suites do not include automated verification tests to confirm that sensitive user data generated by Chinese users remains strictly localized and does not egress.
- **Missing Evidence:**
  The repository lacks templates of Chinese MIIT filing receipts, local entity partnership agreements, or PIPL compliance audits.
- **Missing Audit Trail:**
  An immutable audit trail documenting the assignment of China filing credentials, local hosting configs, and real-name verification audits is completely absent.

### 20.3 Remediation and Action Plan
1. Establish a written China MIIT App Filing and PIPL Data Localization Compliance Policy.
2. Build frontend user interface templates for real-name SMS verification and MIIT filing number displays.
3. Integrate data localization checks in mock network pipelines to block international data egress for Chinese users.
4. Create database logging models for real-name credentials matching PIPL consent.

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
| **EU DMA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU DSA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU EAA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **California Privacy** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Subscription Cancellation** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore PDPA/IMDA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **South Korea Alternative Billing** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **China App Filing** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |

The honest read. Five of the six original regulations are named in existing playbook documentation with dated sources. What they lack is the implementation layer: detection rules in the guard, code templates, and tests. The fourteen additional frameworks are currently absent or only mentioned in passing, so this expanded report serves as the definitive compliance implementation backlog for the playbook.

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. All twenty frameworks listed here require direct, actionable remediation to bridge the gap between simple storefront review readiness and comprehensive global regulatory compliance.

In priority order:

1. Add GPSR, the only framework originally absent end to end.
2. Formulate explicit detection rules in `data/rejection-patterns.json` for all 20 global regulations.
3. Build the backend and front-end code templates, starting with the EU AI Act Article 50 disclosures and the EU Contract Withdrawal button, since both carry urgent active deadlines.
4. Establish cryptographic audit trails and database schemas to securely log user privacy choices, age verification completions, and data deletion records.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

---

## 23. Sources

Every regulation named above, at its primary official source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- CCPA / CPRA, [California Civil Code Section 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2940)
- US ROSCA, [15 U.S.C. Section 8401](https://www.govinfo.gov/app/details/USCODE-2011-title15/USCODE-2011-title15-chap110-sec8401)
- UK Online Safety Act, [Online Safety Act 2023](https://www.legislation.gov.uk/ukpga/2023/30/contents)
- Australia Online Safety Act, [Online Safety Amendment Act 2024](https://www.legislation.gov.au/Details/C2024A00123)
- Brazil Digital ECA, [Law 15,211/2025](https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2025/Lei/L15211.htm)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act, [Telecommunications Business Act Amendment](https://www.kcc.go.kr)
- China App Filing, [MIIT App Filing Circular](http://www.miit.gov.cn)
