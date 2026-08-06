# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major modern regulations that bind app developers shipping into the EU, the US, and globally, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts concluded by electronic means.

The withdrawal button obligation in this Directive attaches to distance contracts concluded online, ensuring that consumers can exercise their 14-day statutory withdrawal rights frictionlessly. The cancellation path must be direct, clear, and at least as simple as the sign-up path, preventing merchants from using dark patterns to retain subscribers. Member States apply these rules from 19 June 2026.

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

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

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
  There is no secure backend system designed to log the receipt of parental consent, consent revocations, or the immediate deletion of raw age-verification documents.
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
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with the technical complexity and impact of the AI integration. Pragmatic compliance for a software engineering team requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable, since Article 4 binds people rather than code. A small helper script that checks whether a literacy log exists and is current would still be useful to prevent compliance lapses.
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

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that those persons are informed that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated or manipulated. Article 50(4) requires deployers of deepfakes to disclose that the content has been artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  The codebase templates do not include helper classes, middle-tier layers, or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
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
2. Incorporate explicit, prominent notices inside all conversational interface templates.
3. Implement standard metadata injection inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that the machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, seeks to ensure contestability and fairness in the digital sector. It defines large online platforms as gatekeepers. For app developers, the DMA forces gatekeepers (like Apple and Google) to allow alternative app stores, web-based app distribution, and alternative in-app payment mechanisms.

While the gatekeeper carries the primary burden, developers leveraging DMA freedoms (such as utilizing the `com.apple.developer.storekit.external-purchase-link` entitlement) must strictly adhere to specific reporting, disclosure, and transactional restrictions established by the gatekeeper to satisfy the gatekeeper's revised EU terms.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council on contestable and fair markets in the digital sector.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not carry an EU Alternative Distribution or Out-of-App Purchase policy template that developers can adapt to document their steering and out-of-app conversion strategy.
- **Missing Documentation:**
  The playbook lists the DMA in passing but lacks operational manuals outlining how to request, build, and configure the alternative payment or distribution entitlements in Xcode and Google Developer Play Console.
- **Missing Code:**
  The static audit scanner does not automatically verify the proper utilization of `ExternalPurchaseCustomLink` APIs or the presence of required entitlement configurations in the project's plist/manifest files.
- **Missing Disclosure:**
  The repository contains no UX wireframes or copy templates for the mandatory system-provided disclosure sheet shown to users before redirecting them to an external purchase flow.
- **Missing Logging:**
  No database schemas or logging specifications are provided to assist developers in tracking external transactions for mandatory monthly reporting (within 15 calendar days of Apple's fiscal month end).
- **Missing Testing:**
  There are no unit or UI integration tests to verify that an external payment redirect does not occur without displaying the required disclosure sheet or that it is gated to the proper geographic region (EU/EEA storefronts).
- **Missing Evidence:**
  No template forms exist for generating monthly external purchase logs, Core Technology Fee (CTF) calculations, or annual developer self-certification documents for the European Commission.
- **Missing Audit Trail:**
  The playbook fails to specify an immutable audit trail system to log monthly transaction reporting, Commission payment confirmations, and entitlement modification logs.

### 7.3 Remediation and Action Plan
1. Draft a comprehensive DMA Alternative Distribution and Payment Strategy Policy.
2. Create developer guidelines for configuring EU external-link entitlements and programmatically showing the custom link disclosure sheet.
3. Add automated checks in the compliance guard to inspect plist and AndroidManifest files for DMA-related entitlements and geographic region-gating checks.
4. Provide template SQLite schemas and reporting script skeletons to capture and export external transaction data in Apple-compliant formats.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes a unified framework for a safe, predictable, and trusted online environment. Under Articles 30 and 31, online app stores must collect, verify, and publish contact and identity information for all "traders" distributing applications to EU consumers.

Developers must declare their trader status. If they are a trader, their full verified physical address, telephone number, and email address are displayed publicly on the App Store and Google Play storefronts, exposing them to direct consumer and regulatory scrutiny.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council on a Single Market For Digital Services.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no Trader Status Determination Policy to help developers legally evaluate whether their app's commercialization model classifies them as a "trader" under EU consumer law.
- **Missing Documentation:**
  The checklists lack detailed instructions on how to set up, verify, and maintain Digital Services Act trader compliance inside App Store Connect and Google Play Console.
- **Missing Code:**
  The metadata-audit script does not dynamically check if the app listing's contact information matches the verified trader status or contains a warning for apps distributing in the EU without verified trader metadata.
- **Missing Disclosure:**
  There are no templates for displaying the required public-facing contact disclosures directly inside the app's settings or "About" screens to match the public store metadata.
- **Missing Logging:**
  The repository does not contain architectural guidelines on how to log user-generated content (UGC) flag notifications and takedown requests as required for interactive platforms under the DSA.
- **Missing Testing:**
  No automated tests are present to verify that an EU storefront build enforces region-specific trader contact disclosures or contains appropriate content moderation flagging pathways.
- **Missing Evidence:**
  No template exists to document the verification artifacts required by the stores (such as D-U-N-S registrations, government ID matches, and SMS/voice 2FA verifications).
- **Missing Audit Trail:**
  There is no unalterable record system to track historical changes to trader status, updated contact details, or compliance certifications submitted to the platform operator.

### 8.3 Remediation and Action Plan
1. Write a formal DSA Trader Status Evaluation Policy and integrate it into the playbook's legal guides.
2. Expand the `scripts/metadata-audit.py` utility to verify that EU listings include a valid physical address, email, and phone number when trader status is enabled.
3. Design in-app "About" screen templates that dynamically pull and display the store-verified trader details.
4. Implement content moderation and report-abuse UI templates showing how traders must handle DSA-mandated content flagging.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable on 28 June 2025. It mandates that a broad range of digital products and services, including mobile applications and e-commerce websites, sold into the EU market must be accessible to persons with disabilities.

EAA compliance is technically defined by the European harmonised standard EN 301 549 Chapter 11, which incorporates Web Content Accessibility Guidelines (WCAG) 2.1 Level AA and adds specific mobile and non-web software requirements.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council on the accessibility requirements for products and services.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Accessibility Policy template outlining the developer's organizational commitment to maintaining compliance with the EAA and EN 301 549 standards.
- **Missing Documentation:**
  The documentation lacks specific guidelines explaining the additional 64 non-web requirements in EN 301 549 Chapter 11 that go beyond standard WCAG 2.1 AA web rules.
- **Missing Code:**
  Although `scripts/accessibility-audit.py` checks basic iOS and Android visual elements, it lacks the specific checks needed for complex EN 301 549 requirements such as keyboard navigation without an on-screen keyboard, or alternative sensory feedback.
- **Missing Disclosure:**
  The repository lacks templates for the mandatory published Accessibility Statement (EN 301 549 Annex B and C) that apps must link in the store listing and in-app menus.
- **Missing Logging:**
  There are no defined formats or logging requirements for tracking user accessibility feedback, issues, or remediation progress as mandated for large service providers.
- **Missing Testing:**
  The testing scripts do not simulate physical accessibility devices (like switch controls or braille displays) or test for multi-sensory failure modes.
- **Missing Evidence:**
  No templates are provided for generating a formal Accessibility Conformance Report (ACR) using the Voluntary Product Accessibility Template (VPAT) tailored for EN 301 549.
- **Missing Audit Trail:**
  An immutable audit log to track accessibility regression audits, compliance certifications, and updates to the accessibility statement is not present.

### 9.3 Remediation and Action Plan
1. Draft an EAA Accessibility Policy template and a standard Accessibility Statement format.
2. Upgrade `scripts/accessibility-audit.py` to cover the exact rules outlined in EN 301 549 Chapter 11.
3. Integrate WCAG 2.1 AA/2.2 contrast ratio checkers and screen reader tag validators directly into the static analysis guard.
4. Provide a sample VPAT template mapping app components to EN 301 549 requirements to serve as compliance evidence.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, restricts the collection of personal information from children under 13 by operators of child-directed websites or online services. The FTC's amended COPPA Rule (effective June 2025, with full compliance by 22 April 2026) expands the definition of personal information, restricts third-party disclosures, and mandates written retention and security policies.

Official Citation: Children's Online Privacy Protection Rule, 16 CFR Part 312 (FTC).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no written Child Data Retention Policy or Information Security Program templates as explicitly required under the amended COPPA Rule (312.10 and 312.8).
- **Missing Documentation:**
  Checks for children's apps in the playbook lack step-by-step guidelines on setting up COPPA-compliant verifiable parental consent (VPC) methods (such as database matching or face-to-photo-ID).
- **Missing Code:**
  The pre-submission compliance guard does not automatically scan for third-party SDK integrations that are known to collect identifiers within files flagged as "child-directed".
- **Missing Disclosure:**
  There are no mobile UI templates or copy patterns for the mandatory COPPA Direct Notice to Parents or COPPA-compliant privacy policy disclosures.
- **Missing Logging:**
  The repository lacks a database design or logging spec to record parental consents, consent revocations, and data deletion events securely without preserving raw children's data.
- **Missing Testing:**
  There are no automated unit tests to verify that if the user's declared age is under 13, all ad-network and analytics tracking SDKs are programmatically initialized in "restricted" or "disabled" modes.
- **Missing Evidence:**
  No template forms are provided for documenting annual Child Privacy Risk Assessments or compliance audits of third-party data-sharing partners.
- **Missing Audit Trail:**
  An immutable audit trail to record the historical versioning of parent notices, consent verification method changes, and children's data deletion logs is missing.

### 10.3 Remediation and Action Plan
1. Write COPPA-compliant Children's Privacy Policy and Written Information Security Program (WISP) templates.
2. Build native code templates for both iOS and Android demonstrating how to dynamically disable ad tracking and analytics SDKs when a user is flagged as under 13.
3. Add static analysis rules to the guard to flag unapproved SDKs (such as standard Facebook or Google Ad SDKs) in child-directed apps.
4. Implement secure logging interfaces to track consent metadata without storing sensitive PII.

---

## 11. California Consumer Privacy Act / California Privacy Rights Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), Cal. Civ. Code § 1798.100 et seq., establishes comprehensive data privacy rights for California residents. Effective 1 January 2026, the CPPA's latest regulations mandate honoring the Global Privacy Control (GPC) opt-out signal, displaying clear notices at collection, and restricting the sale, sharing, and profiling of sensitive personal information.

Official Citation: California Civil Code § 1798.100 et seq. (California Privacy Protection Agency).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a standard California Privacy Policy addendum or a Data Minimization Policy conforming to the latest CPRA requirements.
- **Missing Documentation:**
  The checklists fail to provide clear, multi-platform developer guidelines on how to programmatically detect and honor the Global Privacy Control (`Sec-GPC`) header in webviews and native settings.
- **Missing Code:**
  The codebase contains no implementation examples of CPRA-compliant "Do Not Sell or Share My Personal Info" and "Limit the Use of My Sensitive Personal Info" controls.
- **Missing Disclosure:**
  There are no UI onboarding mockups or copy examples for the mandatory California Notice at Collection displayed before data ingestion.
- **Missing Logging:**
  The repository is missing database logging schemas to track consumer rights requests (access, deletion, correction, opt-out) and document their resolution within statutory timelines (45 days).
- **Missing Testing:**
  No integration tests exist to verify that when a GPC opt-out signal is received, data sharing and targeted advertising network packets are immediately stopped.
- **Missing Evidence:**
  The playbook lacks templates for CPRA compliance evidence, such as annual Consumer Rights Request Metrics disclosures (required for businesses over threshold) or Data Protection Impact Assessments (DPIA) for high-risk processing.
- **Missing Audit Trail:**
  An unalterable audit log to track the history of consumer opt-out signals, privacy notice updates, and data deletion requests is completely absent.

### 11.3 Remediation and Action Plan
1. Create a California Privacy Policy and CPRA-compliant Notice at Collection template.
2. Provide native code blocks in Swift, Kotlin, and React Native to check for and honor the Global Privacy Control (GPC) opt-out signal.
3. Build a standardized SQLite database schema for logging, tracking, and auditing California consumer rights requests.
4. Establish automated tests that verify network tracking packets are silenced when a mock CPRA opt-out state is triggered.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, storage, and use of biometric identifiers (fingerprints, voiceprints, retina scans, facial templates) by private entities. Under BIPA, developers must obtain a written, signed release before capturing biometric data and publish a publicly accessible retention and destruction schedule.

Official Citation: Illinois Compiled Statutes, 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Biometric Data Retention and Destruction Policy template to satisfy the mandatory public schedule requirement.
- **Missing Documentation:**
  The checklists do not provide developer instructions on how to structure a BIPA-compliant written release form or how to distinguish native biometric authentication (like FaceID/TouchID, which do not expose raw templates) from server-side biometric capture.
- **Missing Code:**
  No code examples are provided to demonstrate compliant user interface prompts for capturing biometric consent prior to system enrollment.
- **Missing Disclosure:**
  The onboarding templates do not provide placeholder disclosures explaining the specific purpose and length of term for which biometric identifiers are collected.
- **Missing Logging:**
  There are no defined specifications or secure database models to log biometric consent events without storing sensitive biometric data itself.
- **Missing Testing:**
  There are no automated unit tests to verify that a biometric enrollment API call is blocked unless the consent flag is successfully written to the user's profile database.
- **Missing Evidence:**
  The repository lacks templates of signed Biometric Written Releases, consent verification documents, or certificates of physical destruction of biometric templates.
- **Missing Audit Trail:**
  An unalterable, cryptographically signed audit trail to record the historical activation of biometric features, consent logging, and scheduled data purging is completely missing.

### 12.3 Remediation and Action Plan
1. Formulate a compliant Biometric Information Privacy Policy and Written Consent Release template.
2. Develop UI wireframes and copy templates demonstrating the mandatory consent flow before enrolling users in biometric verification.
3. Integrate automated static code checks in the guard to scan codebase files for camera, face, or fingerprint APIs and warn if a corresponding biometric policy is missing.
4. Define a secure biometric consent metadata schema and automated data-purge triggers for the backend databases.

---

## 13. US Subscription Cancellation (FTC Negative Option Rule & State Laws)

### 13.1 Regulatory Overview and Background
While the FTC's federal "click to cancel" rule was vacated by the Eighth Circuit in July 2025, robust subscription cancellation requirements remain in force under Section 5 of the FTC Act, ROSCA, and major state negative-option laws (California, New York, Massachusetts). These statutes mandate that cancellation must be direct, frictionless, and at least as easy to complete as the subscription sign-up process.

Official Citations: Section 5 of the FTC Act (15 U.S.C. § 45), Restore Online Shoppers' Confidence Act (ROSCA) (15 U.S.C. § 8401), California Business and Professions Code § 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no Negative Option Subscription Billing and Cancellation Policy template to govern web-billed or cross-platform subscriptions.
- **Missing Documentation:**
  While the playbook warns against "hard cancel" loops, it lacks step-by-step developer guidelines on structuring a compliant self-service in-app cancellation interface.
- **Missing Code:**
  There are no mock user interface components or client-side code segments demonstrating a direct, frictionless, self-service cancellation flow.
- **Missing Disclosure:**
  Onboarding and checkout templates do not contain clear, conspicuous, pre-transaction disclosures of subscription terms, billing intervals, auto-renewal policies, and direct cancellation steps.
- **Missing Logging:**
  No database schemas or logging specifications are provided to capture subscription start events, consent confirmations, cancellation clicks, and refund execution timestamps.
- **Missing Testing:**
  The automated UI tests do not verify that a user can complete a subscription cancellation in the same number of steps (or fewer) as signing up, or check for the presence of deceptive cancel-prevention prompts.
- **Missing Evidence:**
  The repository lacks template cancellation confirmation receipts, customer dispute resolution records, or compliance certificates showing the cancellation path was reviewed.
- **Missing Audit Trail:**
  An immutable audit trail to record changes to subscription billing terms, pricing hierarchies, and modifications to the cancellation UI is not present.

### 13.3 Remediation and Action Plan
1. Draft a Negative Option Subscription Policy conforming to FTC ROSCA guidance and state laws.
2. Build interactive Swift and Kotlin UI templates for a frictionless, single-page "Cancel Subscription" button.
3. Establish robust database logging requirements to capture subscription lifecycles, cancellations, and associated customer communications.
4. Implement automated UI journey tests to count the clicks required to subscribe versus unsubscribe, flagging a compliance risk if the cancellation path contains more steps.

---

## 14. UK Online Safety Act (OSA) 2023

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enforced by Ofcom, places strict duties on providers of internet services (including mobile apps) that allow users to encounter user-generated content (UGC) or search the web. From 25 July 2025, services likely to be accessed by children must employ Highly Effective Age Assurance (HEAA) methods (such as facial age estimation, credit card checks, or open banking) to prevent minors from encountering harmful content.

Official Citation: Online Safety Act 2023 (c. 30), United Kingdom Parliament.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a UK Online Safety Policy or a dedicated Child Harm Prevention Policy template.
- **Missing Documentation:**
  The checklists lack technical guidelines explaining Ofcom's accepted Highly Effective Age Assurance standards or the 15 design standards under the ICO's Children's Code.
- **Missing Code:**
  The repository's interactive mock-ups do not integrate third-party age verification APIs or include content filtering modules to block restricted content for unverified accounts.
- **Missing Disclosure:**
  There are no template public disclosures or parental advice guidelines explaining what age assurance methods are used and what content moderation standards apply.
- **Missing Logging:**
  There are no backend schemas or tracking specifications for logging child-safety incident reports, content take-downs, or Ofcom reporting requirements.
- **Missing Testing:**
  The repository lacks test suites to simulate and verify that accounts marked as children are restricted from accessing search, messaging, or high-risk content.
- **Missing Evidence:**
  No template exists for documenting a Child Online Safety Risk Assessment or an ICO-compliant Data Protection Impact Assessment (DPIA).
- **Missing Audit Trail:**
  An unalterable audit trail recording content moderation actions, age-assurance tool modifications, and annual security audits is missing.

### 14.3 Remediation and Action Plan
1. Create a UK Online Safety Policy and Child Safety DPIA template.
2. Add developer guides and code snippets showing how to wire up facial age-estimation APIs or secure digital identity checks.
3. Implement SQLite schemas to log, moderate, and track UGC reports and administrative actions.
4. Establish integration tests that verify unverified minor accounts are prevented from accessing mature content.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024, effective 10 December 2025, mandates that designated social media platforms must take reasonable steps to prevent children under 16 from holding accounts. The law requires robust age-assurance waterfalls and dictates that any collected age-assurance data must be strictly ringfenced and destroyed immediately after use.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024, Commonwealth of Australia.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no Australian Minor Age Gating Policy or Age-Data Purging Policy templates conforming to eSafety Commissioner guidelines.
- **Missing Documentation:**
  Checklists fail to outline the eSafety Commissioner's approved age-assurance methods, or explain how to implement local Australian region-gating.
- **Missing Code:**
  The client-side mobile templates do not include age assurance check interfaces or automated scripts to trigger the immediate deletion of identity documents.
- **Missing Disclosure:**
  Onboarding UI screens do not display the required Australian disclosures stating that age data is collected purely for legally mandated verification and will be destroyed instantly.
- **Missing Logging:**
  No database schemas or transaction specs are provided to record the *fact* of age verification and parental approval without storing any identifying raw data.
- **Missing Testing:**
  There are no automated test cases to verify that when a user accesses the app from an Australian IP address, the age-gating screen is triggered and successfully blocks under-16s.
- **Missing Evidence:**
  The playbook lacks templates for documenting Australia eSafety compliance reports, age-assurance vendor audits, and data purging certifications.
- **Missing Audit Trail:**
  An unalterable audit trail system to log monthly automated data-deletion sweeps and age-gating algorithm updates is completely absent.

### 15.3 Remediation and Action Plan
1. Write an Australian Age-Gating and Data Minimization Policy.
2. Design onboarding flow templates including Australia-specific age disclosures and instant-purge mechanisms.
3. Build database cleanup scripts and scheduled triggers to completely erase raw identity documents from storage backends.
4. Add network-location simulation tests to verify that Australian IPs are directed to the mandatory age assurance waterfall.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Amendments to Brazil's Child and Adolescent Statute (ECA), codified as Law 15,211/2025, become enforceable on 17 March 2026. The law bans self-declaration checkboxes for age verification on mobile apps, websites, and social networks, requiring verifiable age assurance (facial estimation, CPF database check, or document matching) and restricting child data processing.

Official Citation: Lei Nº 15.211/2025, Child and Adolescent Statute (ECA), Federative Republic of Brazil.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazilian LGPD-compliant Minor Privacy and Verification Policy template.
- **Missing Documentation:**
  Checklists are missing detailed developer instructions on how to interface with Brazil's CPF (Cadastro de Pessoas Físicas) verification APIs or local facial analysis vendors.
- **Missing Code:**
  No native Swift or Kotlin code blocks exist to query the store's declared age bands or trigger alternative CPF validation sheets when distributing in Brazil.
- **Missing Disclosure:**
  The onboarding templates do not provide disclosure text in Portuguese explaining how Brazil's ECA mandates verifiable age check and how the user's data is processed.
- **Missing Logging:**
  The playbook fails to specify secure, LGPD-compliant logging systems to capture the verification success status and parent consent tokens.
- **Missing Testing:**
  No unit or integration tests exist to check that Brazilian storefront builds completely disable the fallback "I am over 18" self-declaration checkbox.
- **Missing Evidence:**
  The playbook is missing templates of LGPD Child Data Protection Impact Assessments (DPIA) or evidence sheets of local database validation.
- **Missing Audit Trail:**
  An unalterable log to record changes to Brazilian age-assurance systems, vendor contracts, and database deletion executions is absent.

### 16.3 Remediation and Action Plan
1. Draft a Brazilian ECA-compliant Age Assurance and Consent Policy.
2. Develop Swift and Kotlin code snippets showing how to execute a CPF validation request and parse Brazil-specific store age signals.
3. Write localized Portuguese UI templates for Brazilian ECA disclosures and verification screens.
4. Create automated test cases to ensure that self-declaration checkboxes are programmatically hidden on Brazilian storefronts.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 / DPDP Rules 2025

### 17.1 Regulatory Overview and Background
The India Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025 (notified on 13 November 2025), is enforceable starting 13 May 2027. The framework treats anyone under 18 as a child, requiring verifiable parental consent (VPC) through government-backed mechanisms (such as DigiLocker) and strictly prohibiting targeted advertising or behavioral tracking directed at children.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 40 of 2023), Parliament of India.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no Indian DPDPA-compliant Consent Policy or Minor Data Protection Policy templates.
- **Missing Documentation:**
  The repository lacks developer manuals on integrating India-specific consent managers or accessing government-backed DigiLocker systems.
- **Missing Code:**
  No codebase helper functions exist to dynamically disable behavioral tracking and targeted advertising networks when an under-18 Indian account is identified.
- **Missing Disclosure:**
  Onboarding templates do not include Indian-standard bilingual Consent Notices explaining what personal data is collected and how to withdraw consent.
- **Missing Logging:**
  There are no backend schemas or API specifications for recording verifiable consent, consent revocations, or data fiduciary tracking logs as mandated.
- **Missing Testing:**
  No automated tests verify that targeted ad networks are programmatically shut down and tracker SDK initializations are prevented for under-18 Indian users.
- **Missing Evidence:**
  The repository is missing templates of Indian Consent Agreements, Data Protection Impact Assessments (DPIA) for high-risk processing, and independent audit templates.
- **Missing Audit Trail:**
  An unalterable audit log to track the history of consent notices, consent manager registrations, and user consent withdrawals is not implemented.

### 17.3 Remediation and Action Plan
1. Write an India DPDPA Data Consent and Protection Policy template.
2. Build native code examples demonstrating how to programmatically block tracking SDKs and targeted ad requests when India-specific child flags are true.
3. Create localized bilingual (English/Hindi) Consent Notice and Disclosure UI templates.
4. Outline a database model to track and audit user consent acquisitions, modifications, and withdrawals securely.

---

## 18. Singapore Personal Data Protection Act (PDPA) / IMDA Code of Practice

### 18.1 Regulatory Overview and Background
The Singapore Personal Data Protection Act (PDPA) establishes the baseline for data protection. On top of this, the IMDA's Code of Practice for Online Safety for App Distribution Services (effective 1 April 2026) mandates that app stores and developers implement robust age-assurance measures to prevent children under 18 from downloading age-inappropriate apps and ensure any age-assurance data is instantly destroyed once verified.

Official Citation: Personal Data Protection Act 2012 (No. 26 of 2012) and IMDA Code of Practice, Singapore.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Singapore PDPA-compliant Data Protection Policy or IMDA-compliant Child Gating Policy templates.
- **Missing Documentation:**
  Checklists fail to explain the IMDA's 18-plus block requirements or how developers must interface with local Singapore-specific verification protocols.
- **Missing Code:**
  The client-side templates lack code patterns to read Singapore-specific store age signals or trigger immediate, automated age-data deletion scripts.
- **Missing Disclosure:**
  Onboarding screens do not display required Singapore disclosures stating that age data is processed purely for IMDA compliance and is completely deleted instantly.
- **Missing Logging:**
  No database schemas are provided to securely log verification success tokens and parental approvals without storing any raw identifying data.
- **Missing Testing:**
  The test suites do not include automated integration tests to check that Singapore storefront builds enforce 18-plus download block rules.
- **Missing Evidence:**
  The repository is missing templates of Singapore PDPA Data Protection Impact Assessments (DPIA) or certificates of immediate data destruction.
- **Missing Audit Trail:**
  An unalterable audit log to record scheduled age-data purge sweeps and updates to Singapore-specific gating algorithms is completely absent.

### 18.3 Remediation and Action Plan
1. Create a Singapore PDPA and IMDA Online Safety Policy template.
2. Formulate localized Singapore age disclosures and integrate them into onboarding UI screens.
3. Build automated database triggers to guarantee that raw age-verification records are deleted immediately following validation.
4. Establish automated test cases to ensure that Singapore storefront builds adhere to the 18-plus download block.

---

## 19. South Korea Telecommunications Business Act

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates that major app store operators must allow developers to utilize alternative in-app billing providers. To comply, Apple and Google enforce highly specific, restricted, and region-gated South Korea alternative payment entitlements, complete with mandated disclosure screens, custom binaries, and rigid monthly transaction reporting.

Official Citation: Telecommunications Business Act, National Assembly of South Korea.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no written South Korea Alternative Billing Policy template to guide developers in managing South Korea-specific payment networks.
- **Missing Documentation:**
  The checklists fail to provide detailed, step-by-step instructions on setting up South Korea-specific entitlements (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`) and configuring approved local billing gateways.
- **Missing Code:**
  The static audit scanner does not automatically verify the proper configuration of South Korea alternative payment entitlements or the deployment of a separate South Korea binary.
- **Missing Disclosure:**
  The repository contains no UI templates or localized Korean copy for the mandatory system-provided payment disclosure sheet shown before redirecting to local gateways.
- **Missing Logging:**
  No database schemas or logging specifications are provided to capture, track, and export local transactions for mandatory monthly reporting within 15 calendar days of Apple's fiscal month end.
- **Missing Testing:**
  There are no automated unit or integration tests to verify that the South Korea payment redirect only triggers on the South Korea storefront and displays the required disclosure sheet first.
- **Missing Evidence:**
  No templates exist for generating monthly external purchase logs, local payment provider contracts, or South Korea-specific compliance self-certifications.
- **Missing Audit Trail:**
  An unalterable audit log to record monthly transaction submissions, commission calculations (26 percent), and entitlement configuration histories is missing.

### 19.3 Remediation and Action Plan
1. Draft a South Korea Alternative Payment Compliance and Entitlement Policy.
2. Develop developer guidelines for configuring South Korea-specific payments, including local gate setups and separate binary deployment.
3. Add automated checks to the guard to scan manifest files for South Korea alternative billing entitlements.
4. Provide template SQL database structures to organize, validate, and export South Korea transaction records.

---

## 20. China Mobile App Filing (MIIT ICP Extension)

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) of China mandates that all mobile applications distributed on Chinese app stores must obtain an official Mobile App Filing (an extension of the internet ICP filing system). Apps distributed without a valid filing number face immediate block and removal from Chinese storefronts. Furthermore, games distributed in China must obtain a Banhao publishing license, and all apps must implement real-name verification.

Official Citation: Provisions on the Administration of Mobile Internet Application Information Services, MIIT, People's Republic of China.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China Mobile App Filing and Local Partner Operations Policy template to guide developers in establishing compliant mainland-China distribution agreements.
- **Missing Documentation:**
  Checklists fail to provide detailed, step-by-step instructions on obtaining an ICP filing through a local Chinese partner or submitting the filing number inside App Store Connect.
- **Missing Code:**
  The static scanner does not verify that Chinese storefront builds contain mandatory real-name verification hooks, Chinese content moderation APIs, or the display of the ICP filing number in the app's settings screen.
- **Missing Disclosure:**
  Onboarding templates do not include Chinese-localized PIPL-compliant privacy disclosures, cookie disclosures, or the mandatory display of the ICP filing number on the first screen.
- **Missing Logging:**
  No database schemas or logging specs are provided to record real-name verification logs, Chinese-mandated IP address logging, or user activity logs securely.
- **Missing Testing:**
  No automated tests exist to verify that when a Chinese IP address is simulated, the app enforces strict real-name verification, localized Chinese moderation, and hides unapproved external payment links.
- **Missing Evidence:**
  The repository is missing templates of Chinese partner agreements, ICP filing submissions, or Banhao game license records.
- **Missing Audit Trail:**
  An unalterable audit log to record changes to Chinese filing metadata, real-name database integrations, and content moderation activities is completely absent.

### 20.3 Remediation and Action Plan
1. Create a China Mobile App Filing and Local Partner Operations Policy template.
2. Build native code examples demonstrating how to integrate real-name verification and display the ICP filing number inside the app's main menus.
3. Design localized Chinese PIPL-compliant privacy and consent UI screens.
4. Add network-location simulation test cases to verify that Chinese storefront builds programmatically disable non-approved external payments and enable real-name gating.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DMA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU DSA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **European Accessibility Act**| Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **California CCPA/CPRA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Subscription Cancel** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore PDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **South Korea Telecom Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **China App Filing** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is extremely strong on what gets an app rejected by a store reviewer at submission time, but significantly thinner on the global and regional laws that bind the app once it is live in production.

Of the twenty major regulations examined in this expanded report, several are partially mentioned in legal files but lack a developer-facing implementation layer. What is missing across the board is a standardized implementation and verification layer, consisting of:
1. Written policy templates for all twenty frameworks.
2. Step-by-step native and cross-platform coding guides.
3. Interactive user interface disclosure assets and localized copy templates.
4. Database schemas, SQL triggers, and logging rules to record compliant data-processing.
5. Automated integration and UI tests to prove compliance on simulated platforms and locations.

As regulatory bodies in the EU, US, and globally transition from baseline drafting to aggressive enforcement (particularly surrounding artificial intelligence, children's safety, and automatic billing), updating this playbook with actionable developer frameworks remains the highest priority.

This report is a snapshot. It goes stale the moment a deadline or legal enforcement moves. Re-run audits against primary Priority 1 sources regularly to maintain alignment.

---

## 23. Sources

Every regulation named above, cited at its primary official source.

- EU GPSR, [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA, [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA, [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312 (FTC)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Civil Code § 1798.100 et seq., [CCPA/CPRA Regulations (California Privacy Protection Agency)](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA, [740 ILCS 14 (Illinois General Assembly)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2940)
- US FTC Negative Option Rule, [Restore Online Shoppers' Confidence Act (ROSCA) (15 U.S.C. § 8401)](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option)
- UK Online Safety Act 2023, [Online Safety Act 2023 (c. 30) (legislation.gov.uk)](https://www.legislation.gov.uk/ukpga/2023/30/contents/enacted)
- Australia Online Safety Amendment, [Online Safety Amendment (Social Media Minimum Age) Act 2024 (Federal Register of Legislation)](https://www.legislation.gov.au/C2024A00109/text)
- Brazil Digital ECA, [Lei Nº 15.211/2025 (Portal da Legislação)](http://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm)
- India DPDPA, [The Digital Personal Data Protection Act, 2023 (Gazette of India)](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA, [Personal Data Protection Act 2012 (Singapore Statutes Online)](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act, [Telecommunications Business Act (Korea Legislation Research Institute)](https://elaw.klri.re.kr/kor_service/lawView.do?hseq=60244&lang=ENG)
- China Mobile App Provisions, [Provisions on the Administration of Mobile Internet Application Information Services (MIIT)](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/)
- Utah SB 142, [Utah Senate Bill 142 (Utah State Legislature)](https://le.utah.gov/~2025/bills/static/SB0142.html)
- Texas SB 2420, [Texas Senate Bill 2420 (Texas Legislature Online)](https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=SB2420)
- Louisiana HB 570, [Louisiana House Bill 570 (Louisiana State Legislature)](https://www.legis.la.gov/legis/BillInfo.aspx?i=248039)
- Alabama HB 161, [Alabama House Bill 161 (Alabama Legislature)](https://alison.legislature.state.al.us/)
