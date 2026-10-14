# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping across the European Union, the United States, the United Kingdom, Australia, Brazil, India, Singapore, South Korea, China, and global jurisdictions. It checks honestly how far this repository already carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your organization. Where it says something is missing, it means missing from this repository. Each framework is audited systematically across eight compliance gap categories:
1. Missing policy
2. Missing documentation
3. Missing code
4. Missing disclosure
5. Missing logging
6. Missing testing
7. Missing evidence
8. Missing audit trail

Assume the repository is incomplete unless proven otherwise, continuing the search until no unexamined regulatory gaps remain.

## Source Trust Hierarchy and Methodology

All analysis and cited legal frameworks within this report adhere strictly to the repository source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is strictly emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems and software, the GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template General Product Safety Policy to decide whether their listing falls inside Regulation (EU) 2023/988 or to hand to a client or team.
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

The withdrawal button obligation attaches to distance financial services contracts, and serves as an important design benchmark for consumer subscriptions. The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating apps that genuinely fall in scope from those adopting it as a design default.
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
  A systematic audit trail tracking historical cancellation rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination without requiring manual human approval.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Verified age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Act No. 185, replacing HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although rejection patterns contain entries for state-level laws, mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  In-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log the receipt of parental consent, consent revocations (such as the `RESCIND_CONSENT` server notification), or the immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests to verify that the application blocks minor accounts from accessing premium features or completing in-app purchases in the absence of valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to prove compliance to state Attorneys General.
- **Missing Audit Trail:**
  An immutable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy specifying how state-level requirements are identified and how children's data is strictly minimized.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and automated procedures to purge raw age-verification data immediately after the user's age category is confirmed.
4. Establish automated unit tests verifying that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems (including mobile application developers utilizing third-party generative AI APIs) must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations with no headcount carve-out. Pragmatic compliance for a software engineering team requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining team obligations under Article 4 or how to stay updated on emerging AI safety standards.
- **Missing Code:**
  No automated lint or script exists to verify whether an AI literacy record exists for team members committing AI feature code.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose commitment to or enforcement of AI literacy standards as mandated by Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no automated internal lints, pre-commit hooks, or CLI tools to verify that team members committing AI-related changes have valid, up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of what acceptable evidence looks like, such as a completed training log, a course record, or a written risk assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting when the AI literacy policy was reviewed, when training modules were updated, or how team training records evolved over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review the team's literacy records on an annual basis.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been reviewed or updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026. This framework is a critical release blocker for any application incorporating artificial intelligence that reaches users in the European Union.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that those persons are informed that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deployers of deepfakes to disclose that content has been artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed technical instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  The codebase templates do not include helper classes, middle-tier layers, or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the required immediate disclosure ("You are interacting with an AI system") at the time of first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  Existing test runner scripts do not check for the presence of synthetic media markers or verify that generated outputs are machine-detectable.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that machine-readable compliance headers are set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, imposes obligations on designated gatekeeper platforms (including Apple App Store and Google Play Store). It mandates alternative application distribution, alternative payment processors, external purchasing link entitlements, and prohibition of self-preferencing.

For developers shipping in the EU, the DMA creates technical mechanisms (such as Apple's `com.apple.developer.storekit.external-purchase-link` entitlement and Core Technology Commission 5% fee reporting) and mandates strict user disclosure sheets before redirecting to external web flows.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides high-level narrative overviews of the DMA but lacks a standardized developer policy template for selecting and maintaining DMA business terms versus default platform terms.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for executing external link reporting, calculating alternative payment commission structures, and implementing mandatory link modal UI sheets.
- **Missing Code:**
  Code templates lack native implementation scripts for StoreKit External Purchase Link APIs or Google Play Alternative Billing APIs.
- **Missing Disclosure:**
  In-app UI components omit the mandatory platform interstitial disclosure warning users before opening external payment links.
- **Missing Logging:**
  No backend logging models exist to capture external transaction events, completion statuses, or monthly CTC commission reporting datasets.
- **Missing Testing:**
  Automated tests do not verify that the external purchase link entitlement behaves correctly under simulated EU store region configurations.
- **Missing Evidence:**
  The repository contains no sample proof of reporting submissions or records of monthly commission reconciliation sent to gatekeeper platforms.
- **Missing Audit Trail:**
  There is no audit log tracking developer account entitlement applications, key exchanges, or contract election changes under DMA terms.

### 7.3 Remediation and Action Plan
1. Publish an EU Alternative Distribution and External Link Policy guide.
2. Build native UI modal templates for external link disclosures matching gatekeeper guidelines.
3. Implement automated transaction logging scripts for external payment reporting.
4. Add automated CI checks for entitlement key declarations in iOS `Entitlements.plist` and Android `AndroidManifest.xml`.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes harmonized rules on the provision of intermediary services, online platforms, and marketplaces in the EU.

For mobile applications, the DSA enforces mandatory Trader Status declarations (requiring verified D-U-N-S numbers, addresses, emails, and phone numbers in app store listings), illegal content notification mechanisms, and user grievance redirection paths. Failure to comply leads to app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template DSA Compliance Policy covering Trader declaration, content moderation, and user grievance procedures.
- **Missing Documentation:**
  Checklists mention Trader status, but lack operational runbooks for submitting verified credentials or handling user content takedown notices.
- **Missing Code:**
  No in-app UGC reporting modal components or notice-and-action API code blocks are provided in codebase templates.
- **Missing Disclosure:**
  App listing metadata check scripts do not explicitly audit for compulsory Trader disclosure fields (address, phone, email, registration details).
- **Missing Logging:**
  There are no backend schemas for logging incoming user content complaints, resolution timestamps, or moderator actions.
- **Missing Testing:**
  Metadata audit tools do not enforce automated verification of Trader contact fields across app store metadata JSON exports.
- **Missing Evidence:**
  The repository lacks verified sample forms for Trader status verification or annual content moderation transparency reports.
- **Missing Audit Trail:**
  No audit trail exists to log content moderation decisions, appeal histories, or changes to store Trader listing details.

### 8.3 Remediation and Action Plan
1. Update `scripts/metadata-audit.py` to strictly validate DSA Trader disclosure fields in store metadata.
2. Provide in-app Notice-and-Action reporting modal components in the `references/` directory.
3. Draft a standardized DSA Trader & Content Moderation Policy template.
4. Implement a backend schema for content complaint logging and resolution tracking.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became legally binding across EU Member States on 28 June 2025. It mandates accessibility requirements for electronic products and services, including mobile applications and e-commerce platforms.

Under the EAA, mobile apps must comply with harmonized standard EN 301 549, which aligns with WCAG 2.1 Level AA requirements. Key elements include screen reader compatibility, font scaling (Dynamic Type / font size adjustment), minimum color contrast ratios (4.5:1), and a published accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries an accessibility report but lacks a standardized corporate Accessibility Policy template for development teams.
- **Missing Documentation:**
  Developer guides lack detailed checklists for Android TalkBack accessibility service bindings and custom view accessibility trait declarations.
- **Missing Code:**
  While `scripts/accessibility-audit.py` scans for basic traits, sample application templates lack fully annotated accessible UI components (e.g. accessible custom sliders or charts).
- **Missing Disclosure:**
  No in-app Accessibility Statement template or modal component exists in the repository.
- **Missing Logging:**
  There are no provisions for logging accessibility feedback, user bug reports, or accessibility setting override events.
- **Missing Testing:**
  The test suite does not execute automated UI tests under simulated screen-reader environments (e.g., automated VoiceOver or TalkBack traversal scripts).
- **Missing Evidence:**
  The repository contains no sample Voluntary Product Accessibility Template (VPAT) or Accessibility Conformance Report (ACR) based on EN 301 549.
- **Missing Audit Trail:**
  No audit log tracks historical accessibility remediation reviews, user feedback tickets, or version-over-version contrast audits.

### 9.3 Remediation and Action Plan
1. Publish an Accessibility Policy and in-app Accessibility Statement template.
2. Expand `scripts/accessibility-audit.py` to check for required accessible trait bindings on custom views.
3. Add a sample EN 301 549 / WCAG 2.1 AA Conformance Report template.
4. Integrate UI automated tests verifying component behavior under enlarged font settings.

---

## 10. US Children's Online Privacy Protection Act (COPPA & Amended Rule)

### 10.1 Regulatory Overview and Background
The US Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, enforced by the FTC, regulates the collection of personal information from children under 13. The FTC's Amended COPPA Rule introduces strict limits on targeted advertising, mandatory opt-in consent for data sharing with third parties, and requirements for verifiable parental consent (VPC).

Apps directed to children or with actual knowledge of child users must minimize data collection, disable ad tracking, and provide clear privacy notices.

Official Citation: 16 CFR Part 312; FTC Final Rule Updates (2025/2026).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no dedicated COPPA / Minor Data Protection Policy template for apps entering the Kids Category.
- **Missing Documentation:**
  Checklists lack operational steps for implementing FTC-approved Verifiable Parental Consent (VPC) mechanisms (e.g., credit card micro-charge, government ID, or signed consent form).
- **Missing Code:**
  Codebase templates lack native bridges for disabling advertising identifier collection (IDFA/GAID) dynamically for child profiles.
- **Missing Disclosure:**
  In-app onboarding flows lack dedicated Direct Notice to Parents modal views.
- **Missing Logging:**
  There is no backend logging schema for capturing parental consent timestamps, methods used, or consent revocation requests.
- **Missing Testing:**
  Test runners do not verify that third-party analytics SDKs are completely suppressed when a child profile is active.
- **Missing Evidence:**
  The repository lacks sample parental consent records or documentation verifying COPPA Safe Harbor program certification.
- **Missing Audit Trail:**
  No audit trail system exists to track parental deletion requests, data retention purges, or child data access logs.

### 10.3 Remediation and Action Plan
1. Create a Children's Data Protection Policy and Parent Disclosure Notice template.
2. Provide code templates for dynamic SDK suppression and child account flagging.
3. Establish a backend logging structure for VPC tracking and automated deletion triggers.
4. Add automated CI lints ensuring no tracking SDKs are imported into child-directed build targets.

---

## 11. California Privacy Framework (CCPA / CPRA / CPPA Regulations)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and regulated by the California Privacy Protection Agency (CPPA) (11 CCR section 7000 et seq.), establishes consumer privacy rights including Opt-Out of Sale/Sharing, Right to Limit Use of Sensitive Personal Information, and mandatory Global Privacy Control (GPC) signal recognition.

2026 CPPA regulations introduce strict requirements for Automated Decision-Making Technology (ADMT) risk assessments and mandatory opt-out rights.

Official Citation: Cal. Civ. Code section 1798.100 et seq.; 11 CCR section 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a California-specific Consumer Privacy Rights Policy template including ADMT opt-out procedures.
- **Missing Documentation:**
  Documentation lacks step-by-step developer implementation steps for parsing `Sec-GPC` HTTP request headers or mobile GPC signals.
- **Missing Code:**
  Code templates do not include automated GPC signal listeners or "Do Not Sell or Share My Personal Information" UI links.
- **Missing Disclosure:**
  Sample privacy notices omit required California "Notice at Collection" components and ADMT descriptions.
- **Missing Logging:**
  No logging mechanisms exist to capture consumer opt-out preferences, GPC signal recognitions, or CCPA request receipts.
- **Missing Testing:**
  Automated tests do not verify that web and mobile web views honor `Sec-GPC: 1` headers by disabling tracking pixels.
- **Missing Evidence:**
  The repository lacks sample ADMT risk assessment documents or CCPA annual request metric reports.
- **Missing Audit Trail:**
  No audit trail tracks CCPA request fulfillment dates, identity verification steps, or consumer dispute logs.

### 11.3 Remediation and Action Plan
1. Add a California Notice at Collection and ADMT Opt-Out Policy template.
2. Build GPC header parsing middleware and "Do Not Sell/Share" UI link components.
3. Implement backend consumer request and opt-out preference logging schemas.
4. Add unit tests verifying GPC header parsing and tracking suppression.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, capture, purchase, receipt, storage, and handling of biometric identifiers (fingerprints, voiceprints, retina/iris scans, facial geometry).

BIPA requires written informed consent prior to collection, strict retention schedules, public written policies, and prohibits profiting from biometric data. 2024 amendments clarify that per-scan liability applies on a per-person basis rather than per-scan instance.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template Biometric Information Privacy Policy or written destruction schedule compliant with 740 ILCS 14/15(a).
- **Missing Documentation:**
  Checklists lack operational guidance for distinguishing local on-device biometric auth (e.g. FaceID / LocalAuthentication) from server-side biometric collection.
- **Missing Code:**
  Code templates lack written biometric consent modal sheets and automated destruction lifecycle timers.
- **Missing Disclosure:**
  Onboarding templates lack BIPA-mandated written disclosures informing the subject that biometric data is being collected and stored, and stating the specific purpose and length of term.
- **Missing Logging:**
  No backend schema exists to record the execution of written consent forms or biometric deletion events.
- **Missing Testing:**
  Test suites do not verify that raw biometric template data is excluded from application cloud backups or remote telemetry.
- **Missing Evidence:**
  The repository lacks sample signed biometric consent forms or certified destruction logs.
- **Missing Audit Trail:**
  No immutable audit trail records biometric consent revocations, retention schedule enforcement, or third-party processor audits.

### 12.3 Remediation and Action Plan
1. Draft a BIPA-compliant Biometric Information Policy and Consent Notice template.
2. Build UI modal components for explicit written biometric consent prior to feature activation.
3. Establish automated checks ensuring local biometric SDK usage (`LocalAuthentication` / `BiometricPrompt`) never transmits raw biometric templates off-device.
4. Implement a logging structure for recording written consent receipts and deletion events.

---

## 13. US Automatic Renewal & Subscription Cancellation Rules (FTC Negative Option Rule & UK DMCC Act)

### 13.1 Regulatory Overview and Background
The FTC's updated Negative Option Rule (16 CFR Part 425) in the US, along with the UK Digital Markets, Competition and Consumers (DMCC) Act 2024, enforces strict "Click-to-Cancel" subscription rules.

Sellers must provide a cancellation mechanism that is as easy to use as the consent mechanism, clear pre-purchase disclosures, explicit consent before charging, and timely renewal notifications.

Official Citations: 16 CFR Part 425 (FTC Negative Option Rule); UK DMCC Act 2024, Part 4 Chapter 2.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a standardized Automatic Renewal Policy template covering FTC and UK DMCC rules.
- **Missing Documentation:**
  Documentation lacks explicit design guidelines for self-service in-app cancellation flows and pre-renewal notification timing.
- **Missing Code:**
  Code templates lack automated pre-renewal email/push notification triggers and single-click cancellation modal components.
- **Missing Disclosure:**
  Paywall UI templates fail to display compulsory pre-consent billing disclosures directly adjacent to the call-to-action button.
- **Missing Logging:**
  No backend schemas exist to log renewal notice dispatches, cancellation attempt timestamps, or user consent captures.
- **Missing Testing:**
  UI test scripts do not verify that cancellation can be completed in the same number of steps as initial subscription signup.
- **Missing Evidence:**
  The repository contains no sample cancellation verification receipts or pre-renewal notice templates.
- **Missing Audit Trail:**
  No audit trail tracks paywall disclosure changes, cancellation success rates, or subscription terms modifications.

### 13.3 Remediation and Action Plan
1. Publish a Click-to-Cancel Subscription Policy and paywall disclosure checklist.
2. Provide code templates for single-click in-app cancellation and automated pre-renewal notification dispatches.
3. Establish backend logging for subscription events, cancellation timestamps, and renewal notices.
4. Add automated UI tests enforcing equal step counts for signup and cancellation.

---

## 14. UK Online Safety Act 2023 (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) imposes statutory duties of care on user-to-user services and search services. Regulated by Ofcom, the OSA requires age assurance, illegal content risk assessments, protection of children from harmful content, and transparent reporting mechanisms.

App distribution services and mobile applications with UGC or social interactions shipping to UK users must complete risk assessments and enforce effective age gating.

Official Citation: Online Safety Act 2023 (c. 50); Ofcom Statutory Codes of Practice.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no UK Online Safety Act Compliance Policy or Children's Risk Assessment template.
- **Missing Documentation:**
  Checklists lack developer runbooks for completing Ofcom-aligned risk assessments for user-to-user features.
- **Missing Code:**
  Code templates lack integration scripts for UK-compliant age estimation / verification vendor APIs.
- **Missing Disclosure:**
  Terms of service templates omit required disclosures regarding UK child safety measures and harmful content policies.
- **Missing Logging:**
  No logging structure exists to record age verification outcomes, content moderation actions, or priority content reports.
- **Missing Testing:**
  Test suites do not verify that unverified minor accounts are restricted from accessing user-to-user chat or UGC feeds in the UK.
- **Missing Evidence:**
  The playbook contains no sample completed Ofcom Risk Assessment documentation or age assurance audit certificates.
- **Missing Audit Trail:**
  No audit trail records risk assessment updates, safety policy revisions, or Ofcom reporting histories.

### 14.3 Remediation and Action Plan
1. Create a UK OSA Compliance Policy and Children's Risk Assessment framework document.
2. Build native UI components for age assurance checks during UK user onboarding.
3. Establish backend logging for moderation events and age verification flags.
4. Add automated integration tests verifying UGC access restriction for under-18 profiles.

---

## 15. Australia Online Safety & Privacy Act Framework (18+ Social Media Ban & APP 1.7-1.9)

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 enforces a strict age threshold prohibiting children under 16 from accessing designated social media platforms. Additionally, the Privacy Act 1988 amendments (inserted by the Privacy and Other Legislation Amendment Act 2024, APP 1.7-1.9) establish statutory rights regarding automated decision-making transparency and child privacy codes.

Platforms must take reasonable steps to prevent age-restricted users from having accounts.

Official Citations: Online Safety Act 2021 as amended in 2024; Privacy Act 1988 (Cth) APPs 1.7-1.9.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Minimum Age Compliance Policy and APP 1.7-1.9 Automated Decision Transparency document.
- **Missing Documentation:**
  Documentation lacks developer guidelines for identifying whether an app qualifies as a "designated social media service" under Australian law.
- **Missing Code:**
  Code templates lack mandatory age restriction onboarding blocks for Australian IP addresses.
- **Missing Disclosure:**
  Privacy notice templates do not include Australian APP 1.7 disclosures regarding automated personal data processing.
- **Missing Logging:**
  No backend schema logs Australian age attestation results or account termination events for under-age profiles.
- **Missing Testing:**
  Test runners do not simulate Australian geo-IP onboarding to verify that age restriction flows trigger correctly.
- **Missing Evidence:**
  The repository lacks sample documentation proving "reasonable steps" taken to prevent under-16 account creation.
- **Missing Audit Trail:**
  No audit trail tracks age verification system updates, geo-blocking changes, or privacy policy revisions under Australian law.

### 15.3 Remediation and Action Plan
1. Draft an Australian Age Minimum Policy and APP 1.7 Privacy Notice template.
2. Provide code templates for geo-IP sensitive age verification onboarding flows.
3. Build backend logging schemas for age attestation records and account gating.
4. Add automated tests verifying Australian geo-IP age gate triggering.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, regulated by Decreto n. 12.880 of 18 March 2026) establishes the child and adolescent protection framework in digital environments.

It mandates default high-privacy settings for minor accounts, strict parental supervision controls, age-verification mechanisms, and prohibition of behavioral profiling or targeted advertising directed at children and adolescents across Brazil.

Official Citations: Lei n. 15.211/2025; Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy template covering minor protection requirements.
- **Missing Documentation:**
  Checklists lack operational instructions for applying default high-privacy configurations to accounts registered in Brazil.
- **Missing Code:**
  Code templates lack parental control linking components and automated profiling opt-out triggers for minor accounts.
- **Missing Disclosure:**
  Onboarding templates omit required Portuguese disclosures regarding child privacy protections and parental supervision options.
- **Missing Logging:**
  No backend schema logs parental account links, consent confirmations, or privacy default enforcement events.
- **Missing Testing:**
  Test suites do not check whether ad-targeting flags are forced off when account country is Brazil and age is under 18.
- **Missing Evidence:**
  The repository lacks sample child impact assessments or Brazilian age verification compliance reports.
- **Missing Audit Trail:**
  No audit trail records changes to parental control settings, age verification policy updates, or Brazilian regulatory notifications.

### 16.3 Remediation and Action Plan
1. Publish a Brazil Digital ECA Compliance Policy and Privacy Default template.
2. Build code templates enforcing dynamic ad-profiling block on minor accounts in Brazil.
3. Establish backend logging for parental consent and high-privacy default enforcement.
4. Add automated CI tests verifying ad-tracking suppression for minor account targets.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 & DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025 (G.S.R. 846(E)), establishes mandatory obligations for Data Fiduciaries.

Key provisions include verifiable parental consent before processing child data (under 18), prohibition of tracking or behavioral monitoring of children, multi-lingual consent notices (22 scheduled languages), and mandatory appointment of a Data Protection Officer (DPO) and Consent Manager integration.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template DPDPA Compliance Policy or Data Fiduciary operational manual.
- **Missing Documentation:**
  Documentation lacks developer guides for integrating with RBI/MeitY-approved Consent Managers or presenting multi-lingual consent interfaces.
- **Missing Code:**
  Code templates lack multi-lingual consent presentation modals and child data processing suppression switches.
- **Missing Disclosure:**
  Consent notice templates lack itemized, clear disclosures in English and Indian Scheduled Languages specifying data categories and purposes.
- **Missing Logging:**
  No backend schema exists to log consent artifact IDs, consent withdrawal requests, or Consent Manager API calls.
- **Missing Testing:**
  Automated tests do not verify that consent notices render correctly across required language locales.
- **Missing Evidence:**
  The repository contains no sample Data Protection Impact Assessment (DPIA) or DPO designation records for India.
- **Missing Audit Trail:**
  No audit trail tracks consent lifecycle events, Data Fiduciary policy audits, or parental consent verifications.

### 17.3 Remediation and Action Plan
1. Create an India DPDPA Data Fiduciary Policy and Multi-lingual Consent template.
2. Build UI modal code components supporting Consent Manager API hooks and language selection.
3. Establish backend logging schemas for consent artifacts and withdrawal events.
4. Add automated tests validating multi-lingual consent text rendering.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice for Online Safety

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) 2012 (amended 2020) and the IMDA Code of Practice for Online Safety for App Distribution Services require robust data protection, consent management, mandatory breach notification (within 3 calendar days to PDPC), and online safety measures for app distribution.

Organisations must designate a Data Protection Officer (DPO) and provide clear mechanisms for withdrawal of consent.

Official Citations: Personal Data Protection Act 2012 (Act 26 of 2012); IMDA Code of Practice for Online Safety (2023/2025).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository carries no Singapore PDPA Compliance Policy or Mandatory Data Breach Notification Policy template.
- **Missing Documentation:**
  Checklists lack operational runbooks for executing 3-day PDPC data breach notifications or IMDA online safety self-assessments.
- **Missing Code:**
  Code templates lack in-app consent withdrawal buttons specifically wired to Singapore user preference endpoints.
- **Missing Disclosure:**
  Privacy notice templates omit compulsory DPO contact details and PDPC breach notification rights disclosures.
- **Missing Logging:**
  No backend schema logs PDPA consent withdrawal events, breach detection timestamps, or DPO inquiry logs.
- **Missing Testing:**
  Test runners do not check for the presence of valid DPO contact fields within Singapore privacy declarations.
- **Missing Evidence:**
  The repository contains no sample IMDA Online Safety Code Self-Assessment or PDPC Breach Notification report forms.
- **Missing Audit Trail:**
  No audit trail records data protection policy revisions, DPO appointment records, or breach incident logs.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA Policy and 3-Day Breach Notification runbook.
2. Build UI components for frictionless consent withdrawal and DPO contact.
3. Establish backend logging for consent status changes and incident detection.
4. Add automated checks verifying DPO contact disclosures in metadata exports.

---

## 19. South Korea Telecommunications Business Act & PIPA Framework

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act prohibits app store operators from forcing specific in-app payment systems and enforces alternative billing options.

Concurrently, the Personal Information Protection Act (PIPA, Act No. 21445) enforces strict rules regarding cross-border data transfers, mandatory consent separation, immediate data destruction, and local representative appointment for overseas entities.

Official Citations: Telecommunications Business Act (Act No. 18037); Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Alternative Billing & PIPA Data Protection Policy template.
- **Missing Documentation:**
  Documentation lacks developer runbooks for configuring Korean alternative payment gateways and registering a Korean Local Representative.
- **Missing Code:**
  Code templates lack native Korean alternative payment SDK bridges and explicit separated consent item UI checkmarks.
- **Missing Disclosure:**
  Privacy policy templates fail to present mandatory separated consent items (essential vs. optional collection) as required under PIPA.
- **Missing Logging:**
  No backend schema logs Korean alternative billing transaction records or PIPA cross-border transfer consents.
- **Missing Testing:**
  Automated tests do not check that optional data collection checkmarks are unselected by default during Korean onboarding.
- **Missing Evidence:**
  The repository lacks sample Korean Local Representative designation agreements or PIPA cross-border transfer impact assessments.
- **Missing Audit Trail:**
  No audit trail tracks changes to Korean payment gateway configurations, consent form revisions, or data destruction execution logs.

### 19.3 Remediation and Action Plan
1. Publish a South Korea PIPA Compliance Policy and Separated Consent template.
2. Build UI components for separated consent item selection during Korean onboarding.
3. Establish backend transaction and consent logging for Korean alternative billing.
4. Add automated UI tests verifying unchecked optional consent defaults.

---

## 20. China Mobile App Filing (MIIT ICP Extension) & CAC AI Measures

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP Extension) for all mobile applications distributed in mainland China. Apps distributed on domestic app stores or Apple's App Store China must display a valid ICP filing number in the app settings and store metadata.

Additionally, the Cyberspace Administration of China (CAC) enforces CAC Order No. 21 (Interim Measures for Generative AI Services), requiring safety assessments, real-name registration, and strict content moderation for AI services operating in China.

Official Citations: MIIT Circular on Launching Mobile Internet Application Filing (2023); CAC Order No. 21 (2023/2025).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China App Filing & CAC Generative AI Compliance Policy template.
- **Missing Documentation:**
  Checklists lack operational steps for securing an ICP filing through a local Chinese entity or hosting provider.
- **Missing Code:**
  Code templates do not include UI footer components for displaying MIIT ICP filing numbers or CAC real-name auth hooks.
- **Missing Disclosure:**
  In-app settings templates omit required display of MIIT ICP registration numbers on mainland China app builds.
- **Missing Logging:**
  No backend schema logs real-name identity verification checks or CAC safety filter moderation logs.
- **Missing Testing:**
  Automated metadata audit tools do not check for valid ICP filing strings when app distribution includes China storefronts.
- **Missing Evidence:**
  The repository contains no sample MIIT ICP filing receipts or CAC Generative AI Safety Assessment filings.
- **Missing Audit Trail:**
  No audit trail tracks ICP filing updates, real-name verification system logs, or CAC moderation policy audits.

### 20.3 Remediation and Action Plan
1. Create a China App Filing & CAC AI Safety Policy document.
2. Build UI code components displaying MIIT ICP registration strings in app settings.
3. Update `scripts/metadata-audit.py` to check for ICP filing strings when targeting mainland China.
4. Establish backend schemas for logging real-name verification statuses and safety filter events.

---

## 21. Consolidated Gap Classification Matrix

The classification matrix below maps the current compliance coverage across all twenty audited regulatory frameworks and all eight compliance gap categories within this repository.
- Covered: The repository carries complete, actionable code, documentation, or policies.
- Partial: The rule is referenced with a cited source, but developer implementation assets, code, or tests are missing.
- Missing: The obligation is entirely absent from repository policies, documentation, code, logging, testing, evidence, and audit trails.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act**| Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA / Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA/CPRA/CPPA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **13. US Cancel / UK DMCC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. SK Telecommunications/PIPA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is enterprise-grade on store rejection patterns enforced by Apple App Store and Google Play review teams, but requires systematic expansion into the post-release operational compliance layer binding live applications.

To eliminate remaining regulatory gaps, implementation must proceed in four prioritized phases:
1. **Phase 1 (Immediate - High Enforcement Risk):** Build detection rules, code templates, and tests for EU GPSR, EU AI Act Article 50, and US State ASAA.
2. **Phase 2 (2026 Deadlines):** Implement EU e-Evidence response runbooks, EU Contract Withdrawal Button UI sheets, and FTC / UK DMCC Click-to-Cancel cancellation flows.
3. **Phase 3 (Global Minor Protection & Privacy):** Implement verifiable parental consent logging, dynamic profiling suppression hooks for COPPA, Brazil ECA, India DPDPA, and Australia Online Safety.
4. **Phase 4 (Regional Storefront & Accessibility):** Add metadata validation for DSA Trader declarations and China MIIT ICP filing numbers in `scripts/metadata-audit.py`, and expand EAA / WCAG 2.1 AA automated UI test coverage.

This report is audited continuously against primary legal feeds via `scripts/monitor-regulatory.py`.

---

## 23. Sources

Primary official sources cited in this audit report:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312 / Federal Register Updates](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California CCPA/CPRA/CPPA: [Cal. Civ. Code section 1798.100 et seq.](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA: [740 ILCS 14/1 et seq.](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- FTC Negative Option Rule: [16 CFR Part 425](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)
- UK Online Safety Act: [Online Safety Act 2023 (c. 50)](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Privacy Act & Online Safety: [Privacy Act 1988](https://www.legislation.gov.au/C2004A03712/latest/text)
- Brazil Digital ECA: [Lei n. 15.211/2025](https://www.in.gov.br)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore PDPA: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea PIPA: [Personal Information Protection Act](https://www.law.go.kr)
- China App Filing & CAC AI: [MIIT Application Filing Circular](https://www.miit.gov.cn) and CAC Order No. 21
