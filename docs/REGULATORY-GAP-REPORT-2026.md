# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major modern regulations that bind app and platform developers shipping globally, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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

The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating financial app subscriptions from those adopting it as a design default.
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
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Verified age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  The mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
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
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. Pragmatic compliance requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable, since Article 4 binds people rather than code. However, a small automated helper check is missing to flag whether the literacy registry file exists and is populated.
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
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that the machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, targets large online platforms designated as "gatekeepers" (such as Apple and Google) to ensure fair and open digital markets. Under the DMA, gatekeepers must allow alternative app marketplaces, web distribution of apps, non-IAP payment processing, and interoperability of basic services.

For mobile developers, this allows distributing iOS apps through alternative storefronts or directly from their websites in the EU, and using external purchase links or alternative payment services, subject to Apple's notarization checks and Core Technology Fee (CTF) rules.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template policy for evaluating whether to adopt Apple's Alternative Terms Addendum or remain on the standard App Store distribution model.
- **Missing Documentation:**
  There is no developer guide on configuring, deploying, and maintaining alternative distribution channels, nor detailed walk-throughs for the Core Technology Fee exemptions.
- **Missing Code:**
  The automated guard does not contain patterns or regex checks to verify that external purchase links correctly call the `ExternalPurchaseCustomLink` system-provided disclosure sheet.
- **Missing Disclosure:**
  We do not provide standard disclosure modals or template text that apps must display when transitioning EU users from native in-app purchases to external web checkouts.
- **Missing Logging:**
  There are no schemas or logging structures provided for recording out-of-app transactions to comply with Apple's mandatory monthly reporting requirements under the external purchase link entitlement.
- **Missing Testing:**
  The repository lacks automated unit or integration tests to verify the region-gating logic that restricts DMA-specific entitlements to EU/EEA storefronts only.
- **Missing Evidence:**
  No templates are included for submitting notarization compliance packages, proving security standards to Apple during alternative marketplace registration, or reporting monthly sales.
- **Missing Audit Trail:**
  We have no historical tracking system or template to log DMA entitlement agreements, marketplace registrations, or updates to external link targets.

### 7.3 Remediation and Action Plan
1. Draft a comprehensive DMA Strategy Policy outlining the trade-offs of alternative terms and the Core Technology Fee.
2. Develop code snippets demonstrating correct integration of the `ExternalPurchaseCustomLink` API.
3. Build a helper utility to format external transaction logs into the exact monthly format required by Apple.
4. Add automated region-gating verification checks inside the pre-submission guard.

---

## 8. EU Digital Services Act (DSA) - Trader Status

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, mandates that online marketplaces (including the Apple App Store and Google Play Store) obtain and verify the trace of all traders offering goods or services to EU consumers.

Under Articles 30 and 31 of the DSA, developers distributing apps in the EU must declare and verify their "Trader Status" (submitting name, address, phone number, email, and payment account details). For verified traders, this contact information is published directly on the public App Store product listing in the EU. Non-compliance results in the immediate removal of apps from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a clear decision tree or organizational policy to determine whether the app developer qualifies as a "trader" under EU consumer protection law.
- **Missing Documentation:**
  There are no checklists or step-by-step guides explaining the 2-factor verification process for trader status in App Store Connect or Google Play Console.
- **Missing Code:**
  The metadata auditing scripts (`scripts/metadata-audit.py`) do not check for the presence of the DSA trader declaration in the fetched store listing configuration.
- **Missing Disclosure:**
  No templates or copy guidelines are provided for the public trader disclosure fields, which must be accurate, verified, and kept up to date.
- **Missing Logging:**
  The repository lacks internal mechanisms to log and trace when trader status was declared, when it was verified, or when contact information was updated.
- **Missing Testing:**
  There are no automated checks to verify that when "non-trader" is selected, the required in-app consumer notification (that EU consumer-protection rules do not apply) is present and visible.
- **Missing Evidence:**
  The repository fails to supply templates of required documents for verification, such as D-U-N-S registry entries, utility bills, or proof of trade registries.
- **Missing Audit Trail:**
  An administrative audit trail to log changes to the developer's verified contact information or trace store enforcement actions under the DSA is completely absent.

### 8.3 Remediation and Action Plan
1. Create a written DSA Trader Assessment Policy with a clear questionnaire for legal teams to verify trader status.
2. Update the metadata-audit script to flag missing DSA declarations as critical release blockers.
3. Add template copy for compliant in-app notices displayed to users when the developer is a declared "non-trader".
4. Set up an internal registry template (`docs/DSA_TRADER_REGISTRY.md`) to log verified credentials and annual self-certifications.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable on 28 June 2025. It mandates that key digital products and services, including mobile applications and e-commerce websites, placed on the EU market must be fully accessible.

The technical standard used to demonstrate compliance with the EAA is EN 301 549, which incorporates WCAG 2.1 Level AA requirements but adds specific mobile software requirements (Chapter 11) such as screen-reader compatibility (VoiceOver/TalkBack), text scaling (Dynamic Type), color contrast, and keyboard navigation.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing an organizational Accessibility Policy that formally adopts EN 301 549 and WCAG 2.1 AA as binding development standards.
- **Missing Documentation:**
  No detailed guides are provided on how to fulfill the specific mobile software clauses of EN 301 549 Chapter 11, which go beyond standard WCAG web rules.
- **Missing Code:**
  While accessibility is checked in general, the static audit script (`scripts/accessibility-audit.py`) lacks rule-level reporting mapping directly to EN 301 549 clauses.
- **Missing Disclosure:**
  The repository does not contain templates for the mandatory, public-facing Accessibility Statement, which must details compliance status, contact channels, and feedback mechanisms.
- **Missing Logging:**
  There are no logging provisions or feedback registers designed to capture user accessibility complaints, technical errors, or screen-reader bugs.
- **Missing Testing:**
  No automated UI test scripts (using tools like Axe-core or native test runners) are provided to verify contrast ratios, target sizes, or text scaling dynamically.
- **Missing Evidence:**
  The playbook does not supply templates for compiling a formal Voluntary Product Accessibility Template (VPAT) or an Accessibility Conformance Report (ACR) to prove compliance.
- **Missing Audit Trail:**
  An audit trail to track accessibility reviews, automated scans, user feedback resolutions, and historical compliance statements is entirely absent.

### 9.3 Remediation and Action Plan
1. Draft a comprehensive Corporate Accessibility Policy aligned with EN 301 549.
2. Publish a compliant, customizable Accessibility Statement template inside the references directory.
3. Update the accessibility audit script to map static rules directly to EN 301 549 Chapter 11 requirements.
4. Provide a template feedback register to track, prioritize, and log accessibility requests and issues.

---

## 10. Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6506, and the FTC's implementing Children's Online Privacy Protection Rule (16 CFR Part 312) protect the privacy of children under the age of 13.

The amended COPPA Rule (applicable from April 22, 2026) expands the definition of "personal information" to include biometric identifiers, facial templates, and voiceprints. It mandates separate opt-in consent for third-party tracking, strict data minimization, a written information-security program, and formal data retention policies with mandatory purging schedules.

Official Citation: 16 CFR Part 312 (Federal Trade Commission Children's Online Privacy Protection Rule).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a customizable, COPPA-compliant Children's Privacy Policy template for child-directed or mixed-audience apps.
- **Missing Documentation:**
  There are no detailed instructions or developer guides for integrating verifiable parental consent (VPC) methods such as government ID matching or knowledge-based authentication.
- **Missing Code:**
  The codebase has no template code for implementing age-gates that prevent the collection of personal information from children under 13 without consent.
- **Missing Disclosure:**
  No onboarding disclosure templates or "Direct Notices to Parents" are provided to outline the exact data collection and sharing practices.
- **Missing Logging:**
  There is no backend data logging schema designed to track parental consent flags, revocations, or the automatic purging of child records after the retention limit.
- **Missing Testing:**
  The test suite does not include simulated test cases verifying that tracking SDKs (like analytics or ads) remain deactivated for users identified as under-13.
- **Missing Evidence:**
  The playbook does not provide templates for required COPPA evidence, such as the written Information Security Program document or annual risk assessments.
- **Missing Audit Trail:**
  There is no unalterable log template or system to record consent histories, deletion actions, or the version history of the children's privacy policy.

### 10.3 Remediation and Action Plan
1. Publish a standard Children's Privacy Policy template and a Parental Notice template.
2. Implement a compliant native Age Gate component inside the UI templates directory.
3. Build database schema templates showing how to enforce automated child data retention limits and deletion schedules.
4. Write integration tests to verify that third-party SDKs are blocked when the age-gate returns an under-13 flag.

---

## 11. California Consumer Privacy Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), California Civil Code Sections 1798.100 et seq., grants California residents comprehensive privacy rights, including the right to know, delete, correct, opt-out of the sale or sharing of personal information, and limit the use of sensitive personal information.

App developers must display clear notices at collection, provide in-app mechanisms to opt-out (including honoring the Global Privacy Control signal), and support user data access and deletion requests.

Official Citation: California Civil Code Section 1798.100 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template exists for a California Privacy Policy or a dedicated "California Notice at Collection."
- **Missing Documentation:**
  The repository is missing technical guides on how to detect and parse the Global Privacy Control (GPC) signal (`Sec-GPC` header) within embedded web views or native network requests.
- **Missing Code:**
  There is no functional implementation or codebase template demonstrating the "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information" links.
- **Missing Disclosure:**
  Public-facing templates do not display the mandatory notices at collection that list the categories of personal data collected, purposes, and retention periods.
- **Missing Logging:**
  There are no schemas or databases provided to log and track GPC opt-out preferences or sensitive data restriction selections.
- **Missing Testing:**
  No automated tests exist to verify that GPC signals are correctly processed and result in the suppression of tracking SDKs.
- **Missing Evidence:**
  The playbook does not contain templates for compiling the required annual consumer request metrics (number of access/delete requests received, fulfilled, and denied).
- **Missing Audit Trail:**
  An immutable audit trail template to record when a user submitted a deletion or opt-out request, and when the deletion was confirmed across downstream subprocessors, is absent.

### 11.3 Remediation and Action Plan
1. Add a comprehensive CCPA/CPRA Privacy Policy Addendum and Notice at Collection template.
2. Implement GPC signal parsing helpers in native and hybrid mobile formats.
3. Provide UI components for "Do Not Sell/Share" and "Limit Sensitive Data Use" overlays.
4. Establish an automated unit test verifying that downstream SDK data flows are disabled when the GPC opt-out flag is set to true.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14/, regulates the collection, use, safeguarding, handling, storage, retention, and destruction of biometric identifiers and information (including fingerprints, voiceprints, retina scans, facial templates, or hand scans).

BIPA requires written notice, written consent, a publicly available retention schedule, and secure destruction of biometric data within 3 years of the last user interaction. BIPA includes a private right of action with severe statutory liquidated damages.

Official Citation: 740 ILCS 14/ (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a customizable Biometric Information Privacy Policy outlining data retention and destruction schedules.
- **Missing Documentation:**
  There are no developer-facing guides on secure biometric storage architectures (such as keeping biometric templates strictly in the local Secure Enclave rather than transmitting to servers).
- **Missing Code:**
  No code templates are provided for displaying the mandatory BIPA consent modal or collecting a valid electronic signature/consent block before capturing biometric data.
- **Missing Disclosure:**
  Onboarding templates do not display BIPA-specific disclosures detailing that biometric identifiers are collected, the purpose, and the retention period.
- **Missing Logging:**
  There are no database schemas for logging biometric consent events, consent revocations, or the execution of automated deletion routines.
- **Missing Testing:**
  The test suite lacks test cases to verify that native face or fingerprint scanning APIs (like LocalAuthentication on iOS) are blocked until BIPA consent is successfully recorded.
- **Missing Evidence:**
  No templates are included for verifying that biometric templates are securely purged from servers or proof of local-only storage.
- **Missing Audit Trail:**
  An unalterable, cryptographically signed audit trail to record biometric consent acquisitions, policy updates, and data purges is missing.

### 12.3 Remediation and Action Plan
1. Draft a standard BIPA-compliant Biometric Information Privacy Policy.
2. Develop UI templates for the biometric notice and consent screens.
3. Implement strict local-only static analysis rules in `data/rejection-patterns.json` to flag any server-side transmission of biometric identifiers.
4. Provide database logging triggers to securely record consent metadata without storing any raw biometric data.

---

## 13. US Subscription Cancellation (ROSCA)

### 13.1 Regulatory Overview and Background
Under the Restore Online Shoppers' Confidence Act (ROSCA), 15 U.S.C. 8401 et seq., and state-level negative option laws (such as California, New York, and Massachusetts subscription laws), developers must provide a simple mechanism for consumers to stop recurring charges.

The cancellation path must be at least as easy as the enrollment path ("click-to-cancel"). It cannot require a phone call, email, or a mailed letter if sign-up was completed with a single tap in the app. This applies to all subscriptions billed outside of Apple's or Google's native billing frameworks (e.g., direct web billing, Stripe integrations).

Official Citation: 15 U.S.C. 8401 et seq. (Restore Online Shoppers' Confidence Act).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template Subscription terms and Cancellation Policy for direct-billed or cross-platform services.
- **Missing Documentation:**
  There are no guides detailing the UX design requirements of a "click-to-cancel" flow, including prominent disclosures of the cancellation button.
- **Missing Code:**
  No front-end components or API routing templates are provided for a self-service subscription cancellation button.
- **Missing Disclosure:**
  The paywall and checkout interface templates do not prominently disclose the billing frequency, pricing hierarchy, or the exact self-service cancellation steps.
- **Missing Logging:**
  There are no database logging templates for recording the exact timestamp of a subscription cancellation request, the confirmation email dispatch, or the termination signal.
- **Missing Testing:**
  No automated UI tests are provided to verify that the subscription cancellation path can be completed in the same number of steps as the subscription sign-up.
- **Missing Evidence:**
  The playbook does not contain templates for subscription summaries or confirmation of cancellation receipts to prove compliance during consumer disputes.
- **Missing Audit Trail:**
  A historical record of subscription policy changes, pricing modifications, and compliance audits of the checkout funnel is not maintained.

### 13.3 Remediation and Action Plan
1. Formulate a ROSCA-compliant Subscription Terms and Cancellation Policy template.
2. Add a prominent "Cancel Subscription" button component inside the user profile templates.
3. Designate a billing database schema to log cancellation timestamps, IP addresses, and transaction hashes.
4. Implement automated end-to-end testing scripts to verify frictionless subscription cancellation.

---

## 14. UK Online Safety Act (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023, enacted on 26 October 2023, imposes a duty of care on providers of internet services (especially social media, messaging, and search platforms) to protect children from harmful content and prevent illegal content.

Ofcom acts as the regulator and enforces duties such as using "Highly Effective Age Assurance" methods (like facial age estimation, credit card checks, or digital IDs) to prevent minors from accessing adult content, filtering harmful material, and conducting formal children's risk assessments.

Official Citation: Online Safety Act 2023 (c. 30).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing an Online Safety Policy template that outlines the company's duty of care, content moderation criteria, and age gating protocols.
- **Missing Documentation:**
  There is no technical guide for integrating UK-approved age assurance providers or implementing Ofcom-compliant content filters.
- **Missing Code:**
  The codebase lacks mock classes or native implementations of robust age assurance checks (such as integrating third-party facial age estimation APIs).
- **Missing Disclosure:**
  No public-facing disclosures are provided to inform UK users of content filtering policies, reporting mechanisms, or safety safeguards.
- **Missing Logging:**
  There are no schemas or database models provided for logging content reports, moderator actions, or age verification check results.
- **Missing Testing:**
  The test suites do not include simulated tests to verify that flagged adult content is successfully hidden from users whose age is not verified as 18-plus.
- **Missing Evidence:**
  The playbook lacks templates for the mandatory UK Children's Risk Assessment or the Illegal Content Risk Assessment.
- **Missing Audit Trail:**
  An immutable audit log to record moderating decisions, user bans, content takedowns, and age check histories is absent.

### 14.3 Remediation and Action Plan
1. Create a written UK Online Safety Policy and Content Moderation Guidelines template.
2. Provide integration mockups for Ofcom-compliant age assurance services.
3. Build database logging tables for recording user reports and subsequent moderator actions.
4. Add a standard UK Children's Risk Assessment template (`docs/UK_OSA_RISK_ASSESSMENT.md`).

---

## 15. Australia Online Safety Act

### 15.1 Regulatory Overview and Background
The Australia Online Safety Act 2021, and its 2024 Amendment (Social Media Minimum Age Act 2024), enforces a strict age-restricted regime (minimum age of 16) for designated social media services, messaging apps, and online forums, enforced by the eSafety Commissioner.

Platforms must take "reasonable steps" to prevent under-16 users from holding accounts. The eSafety Commissioner expects advanced age-assurance techniques, and age-assurance data must be strictly ringfenced and destroyed immediately after use to protect user privacy.

Official Citation: Online Safety Act 2021 (Commonwealth of Australia).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australia-specific Minors and Social Media Age Gate Policy.
- **Missing Documentation:**
  No guidelines are provided on how to configure and deploy a waterfall of age assurance methods that comply with the eSafety Commissioner's expectations.
- **Missing Code:**
  There is no code in the codebase that executes the immediate deletion of raw age-assurance documents (like passports or driver's licenses) post-verification.
- **Missing Disclosure:**
  The onboarding templates do not display the mandatory Australian disclosures explaining that age verification is required by law and that parental consent data is ringfenced.
- **Missing Logging:**
  No logging schemas exist to track age-verification outcomes while ensuring that no personally identifiable biometric or database records are stored.
- **Missing Testing:**
  The test suite does not verify that when an Australian user is detected (via geo-location or storefront), the strict under-16 block is triggered in the absence of valid age verification.
- **Missing Evidence:**
  The repository is missing templates of data minimization records and compliance proofs for the eSafety Commissioner.
- **Missing Audit Trail:**
  An audit trail template to record the technical choices made, vendor audits conducted, and age gating updates is not implemented.

### 15.3 Remediation and Action Plan
1. Draft a written Australian Age Assurance and Data Minimization Policy.
2. Develop code triggers to purge verification assets immediately after verification.
3. Implement geofenced onboarding views that display Australian regulatory disclosures.
4. Integrate unit tests to verify that age verification data is never cached or stored long-term in local or remote databases.

---

## 16. Brazil Digital ECA

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025), enforceable from 17 March 2026, amends the Child and Adolescent Statute to mandate that applications, online games, and marketplaces placed on the Brazilian market must verify user age to prevent minors from accessing age-inappropriate content.

The National Data Protection Authority (ANPD) enforces these rules. Accepted age verification methods include document verification, facial age estimation, facial matching, or a CPF (Cadastro de Pessoas Físicas) database check. A simple "I am over 18" checkbox is legally insufficient.

Official Citation: Law No. 15.211 of 2025 (Brazil Digital ECA).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a template Digital ECA Compliance Policy or LGPD children's privacy addendum.
- **Missing Documentation:**
  There are no developer-facing guides on how to integrate CPF database queries or LGPD-compliant facial matching services.
- **Missing Code:**
  The automated pre-submission guard lacks patterns to detect whether Brazil-facing apps rated 18-plus (including all games with loot boxes) implement a mandatory age-verification gate.
- **Missing Disclosure:**
  Onboarding templates do not display Brazilian Portuguese disclosures explaining how age data is processed in compliance with LGPD and the Digital ECA.
- **Missing Logging:**
  There are no schemas provided for logging age confirmation outcomes without retaining sensitive personal data or CPF numbers.
- **Missing Testing:**
  No integration tests are provided to verify that the age-gate blocks access to 18-plus sections for unverified Brazilian user accounts.
- **Missing Evidence:**
  The repository lacks templates for LGPD Privacy Impact Assessments (Relatório de Impacto à Proteção de Dados Pessoais - RIPD) for child data.
- **Missing Audit Trail:**
  An immutable audit trail template to record age-verification vendor selections, system updates, and ANPD compliance reviews is missing.

### 16.3 Remediation and Action Plan
1. Formulate a Digital ECA and LGPD Children's Privacy Policy template.
2. Implement static analysis rules to flag loot box games on the Brazil storefront that lack age-verification controls.
3. Write a template RIPD document for child-directed features (`docs/BRAZIL_LGPD_RIPD.md`).
4. Develop mock integrations for CPF verification services.

---

## 17. India DPDPA - Verifiable Parental Consent

### 17.1 Regulatory Overview and Background
The India Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules 2025, mandates that any processing of personal data of a child (defined as any individual under the age of 18) must only occur after obtaining "verifiable parental consent."

Furthermore, developers are strictly prohibited from processing children's personal data that is likely to cause an detrimental effect on the child, and are banned from tracking, behavioral monitoring, or serving targeted advertising to children.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 40 of 2023).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not carry a written India DPDP children's data policy template.
- **Missing Documentation:**
  No documentation exists describing how to integrate Indian government-backed consent validation platforms, such as DigiLocker or Aadhaar-based parental verification.
- **Missing Code:**
  The codebase has no template code for a hard-gate onboarding flow that disables tracking, analytics, and targeted ads when a user is flagged as under-18 in India.
- **Missing Disclosure:**
  No direct parental notices or consent disclosure forms in English or scheduled Indian languages are provided.
- **Missing Logging:**
  There is no database schema designed to record parental consent tokens, verification hashes, or the opt-out status for child tracking.
- **Missing Testing:**
  The test suite does not include automated checks to verify that targeted advertising modules and analytics trackers are disabled for under-18 Indian users.
- **Missing Evidence:**
  No templates are included for submitting Data Protection Impact Assessments (DPIA) to the Data Protection Board of India.
- **Missing Audit Trail:**
  An unalterable log template to record the acquisition of parental consent, consent revocations, and data deletion requests is absent.

### 17.3 Remediation and Action Plan
1. Create an India DPDPA Child Data and Consent Policy template.
2. Implement backend hooks to programmatically strip out advertising SDK identifiers for Indian minor accounts.
3. Publish a bilingual (English/Hindi) Parental Notice and Consent Form template.
4. Write automated integration tests to verify the complete suppression of tracking when under-18 flags are active.

---

## 18. Singapore PDPA - Age Assurance

### 18.1 Regulatory Overview and Background
The Singapore Personal Data Protection Act (PDPA) 2012, along with the IMDA Code of Practice for Online Safety for App Distribution Services, requires app stores and developers to implement robust age assurance measures to prevent minors (under 18) from downloading age-inappropriate apps.

Under the IMDA Code, 18-plus applications must use reliable age verification methods (such as credit card checks or Singpass database queries), and age verification data must be deleted immediately after the purpose is met.

Official Citation: Personal Data Protection Act 2012 (No. 26 of 2012).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing an IMDA-aligned Singapore Age Assurance Policy.
- **Missing Documentation:**
  There is no guide on integrating Singpass Myinfo API queries or credit-card check APIs for age verification.
- **Missing Code:**
  The mock codebase lacks routines to ensure that Singpass-retrieved personal details are purged from memory immediately post-verification.
- **Missing Disclosure:**
  Onboarding templates do not display Singpass-specific data disclosure forms detailing the age verification process.
- **Missing Logging:**
  No logging structures exist to record that an age-verification check occurred while ensuring no personal identifiers or transaction details are preserved.
- **Missing Testing:**
  The test suite does not verify that when a Singaporean user account is detected, the app blocks the download or activation of 18-plus features until age assurance is complete.
- **Missing Evidence:**
  The playbook lacks templates of privacy audits and data minimization logs designed for PDPC inspections.
- **Missing Audit Trail:**
  An administrative audit trail template to record Singpass API integrations, security reviews, and age gating updates is missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA and IMDA-compliant Age Assurance Policy.
2. Develop code templates demonstrating the Singpass Myinfo age verification flow and subsequent data purge.
3. Implement geofenced onboarding notices for Singapore storefront distributions.
4. Include PDPA-compliant privacy audit checklists in `docs/PRE-SUBMISSION-CHECKLIST.md`.

---

## 19. South Korea Telecommunications Business Act

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (amended in 2021) prohibits app store operators from forcing developers to use their proprietary in-app payment systems.

Under the KCC (Korea Communications Commission) regulations, developers are permitted to offer alternative in-app payment systems. However, developers must register approved local payment gateways (such as KCP, Inicis, Toss, NICE), display a specific modal sheet, compile monthly transaction reports, and pay a reduced commission (typically 26%) to Apple or Google.

Official Citation: Telecommunications Business Act (South Korea).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an organizational policy or decision matrix on South Korean alternative payment options and reporting requirements.
- **Missing Documentation:**
  No guides are provided for configuring the South Korea-specific App Store external purchase entitlement (`com.apple.developer.storekit.external-purchase`) or setting up the required dual-binary structure.
- **Missing Code:**
  There are no code blocks implementing the mandatory Korean payment warning modal sheet or integrating local payment gateways (KCP/Toss).
- **Missing Disclosure:**
  We do not provide standard disclosure modals in Korean warning users that alternative payments do not support Family Sharing or Apple subscription management.
- **Missing Logging:**
  No database schemas are provided for tracking South Korean out-of-app transactions to satisfy Apple's strict monthly reporting and remittance timelines (within 15 calendar days).
- **Missing Testing:**
  No automated unit tests exist to check that alternative payment flows are restricted to the South Korean storefront binary only.
- **Missing Evidence:**
  The playbook does not contain templates for compiling the monthly KCC transaction reports or Apple's StoreKit Korea Sales report.
- **Missing Audit Trail:**
  An immutable record template to track local payment gateway contracts, KCC filing records, and monthly remittance receipts is completely absent.

### 19.3 Remediation and Action Plan
1. Formulate a South Korean Alternative In-App Payment Policy.
2. Publish Korean-language payment warning modal templates.
3. Build a transaction logging schema specifically tailored for KCC monthly reporting requirements.
4. Implement static analysis rules to verify South Korean geofencing and binary isolation.

---

## 20. China App Filing (MIIT)

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) of China mandates that all mobile applications distributed on app stores within China must complete an ICP (Internet Content Provider) App Filing.

New apps must file before launch, and existing apps must have completed filing by March 31, 2024. Apps without a valid filing number are systematically removed from all Chinese app stores. Filing requires a domestic Chinese legal entity or a registered local partner.

Official Citation: Notice of the Ministry of Industry and Information Technology on Organizing and Carrying out the Filing of Mobile Internet Applications (MIIT [2023] No. 105).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an entry-level compliance strategy policy for entering the Chinese market (including partnerships and local hosting rules).
- **Missing Documentation:**
  There are no guides detailing the MIIT filing process, the required paperwork, or how to obtain the necessary Chinese business license (Zhi Zhao).
- **Missing Code:**
  The metadata-audit script does not check for the presence of the Chinese App Filing ID (ICP Filing number) in the fetched metadata or app settings.
- **Missing Disclosure:**
  No templates are provided for displaying the mandatory ICP Filing ID on the app's settings or "About" page, as required by the MIIT.
- **Missing Logging:**
  The repository lacks schemas or logging tables to track real-name verification checks, content moderation triggers, or government censorship logs.
- **Missing Testing:**
  The test suites do not check that when a China storefront binary is generated, external AI service references (such as ChatGPT or OpenAI API keys) are fully stripped.
- **Missing Evidence:**
  The playbook does not supply templates for the MIIT commitment letters, security self-assessment reports, or game Banhao license documentation.
- **Missing Audit Trail:**
  An administrative audit trail to log Chinese government regulatory communications, app filing approvals, and localized content updates is absent.

### 20.3 Remediation and Action Plan
1. Draft a China App Filing and Market Entry Policy.
2. Update the metadata-audit script to flag missing ICP Filing IDs on China storefront builds.
3. Build a static lint rule to detect external AI references (like ChatGPT) inside China-targeted resources.
4. Create a localized "About" page UI template that includes placeholder slots for the ICP Filing ID.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Cancel (ROSCA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK OSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia OSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. SK Telecom Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Almost all global regulations are named in this playbook with dated sources and deadline entries. What they lack is the implementation layer, meaning detection rules in the guard, code templates, and tests.

---

## 22. Conclusion and Future Monitoring

The playbook is exceptionally strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Almost all frameworks here are named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order:
1. Complete the implementation layer for EU GPSR and EAA.
2. Formulate explicit checkable criteria and code templates for the other 18 global regulations.
3. Integrate automated checks inside the CI pipeline to maintain compliance.

---

## 23. Sources

Every regulation named above, at its primary official source (Priority 1).

- **GPSR**: [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **e-Evidence Regulation**: [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- **e-Evidence Directive**: [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **Distance Marketing of Financial Services**: [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **EU AI Act**: [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **DMA**: [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **DSA**: [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **EAA**: [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **COPPA**: [16 CFR Part 312 (Federal Register)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **CCPA/CPRA**: [California Civil Code Sections 1798.100 et seq.](https://oag.ca.gov/privacy/ccpa)
- **Illinois BIPA**: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004)
- **ROSCA**: [15 U.S.C. 8401 et seq.](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- **UK OSA**: [Online Safety Act 2023 (c. 30)](https://www.legislation.gov.uk/ukpga/2023/30/contents/enacted)
- **Australia OSA**: [Online Safety Act 2021 (Federal Register of Legislation)](https://www.legislation.gov.au/Details/C2021A00076)
- **Brazil Digital ECA**: [Law No. 15.211 of 2025 (Planalto)](http://www.planalto.gov.br)
- **India DPDPA**: [Digital Personal Data Protection Act, 2023 (Gazette of India)](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- **Singapore PDPA**: [Personal Data Protection Act 2012 (Singapore Statutes Online)](https://sso.agc.gov.sg/Act/PDPA212)
- **SK Telecom Act**: [Telecommunications Business Act (South Korea)](https://law.go.kr)
- **China App Filing**: [MIIT organisational filing provisions](http://www.miit.gov.cn)
