# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major regulations that bind app developers shipping into the EU, the US, and globally, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
2. Incorporate GPSR-specific metadata requirements (manufacturer address, email, product identifier) into data/rejection-patterns.json and docs/PRE-SUBMISSION-CHECKLIST.md.
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
  The checklists in docs/PRE-SUBMISSION-CHECKLIST.md lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although the rejection patterns contain entries for state-level laws, the mock client implementations in the codebase do not integrate with DeclaredAgeRange or com.google.android.play:age-signals to restrict app access dynamically.
- **Missing Disclosure:**
  The in-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log the receipt of parental consent, consent revocations (such as the RESCIND_CONSENT server notification), or the immediate deletion of raw age-verification documents.
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
2. Create a centralized AI_LITERACY_LOG.md within the repository to track training dates, modules, team member names, and verification methods.
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
  The checklists in docs/PRE-SUBMISSION-CHECKLIST.md mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
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
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, was adopted in 2022 and became fully applicable on 2 May 2023. It aims to ensure contestable and fair markets in the digital sector by regulating "gatekeepers"—large digital platforms that provide core platform services, including Apple's App Store and iOS.

For mobile app developers, the DMA unlocks alternative distribution channels (such as alternative app marketplaces and web distribution) and permits alternative billing systems or external promotional links. Developers using these entitlements (e.g., com.apple.developer.storekit.external-purchase-link) must navigate strict, platform-imposed compliance, including core technology fee reports and distinct disclosure sheets.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council of 14 September 2022 on contestable and fair markets in the digital sector.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template business policies or assessment matrices to help developers determine whether migrating to alternative distribution terms (like Apple's Alternative Terms Addendum) is financially or operationally viable.
- **Missing Documentation:**
  The repository is missing detailed, step-by-step documentation on how to set up external link billing flows, including custom sheet presentation rules and Apple's fiscal-month reporting windows.
- **Missing Code:**
  There is no mock implementation or boilerplate code demonstrating integration with StoreKit's external link disclosure API (ExternalPurchaseCustomLink) or how to region-gate DMA-related features to the EU/EEA.
- **Missing Disclosure:**
  The onboarding templates do not provide disclosure designs for alternative app store distributions or alternative payment options.
- **Missing Logging:**
  There are no schemas or logging frameworks for capturing external transactions to generate the monthly reports required under the External Purchase Server API.
- **Missing Testing:**
  No automated integration tests exist to verify that the app blocks external purchase links or alternative billing mechanisms for non-EU/EEA storefronts.
- **Missing Evidence:**
  The repository lacks templates or checklists for compiling alternative app storefront notarization checks or demonstrating CTC/CTF fee exemption eligibility.
- **Missing Audit Trail:**
  A secure tracking system to record the history of developer agreements (e.g., when the Alternative Terms Addendum was signed or modified) is completely absent.

### 7.3 Remediation and Action Plan
1. Develop strategic decision matrices comparing alternative EU storefront terms against standard Apple business terms.
2. Draft and implement source-code patterns demonstrating EU-region checks and StoreKit external link API interactions.
3. Formulate a standardized reporting workflow for logging and compiling monthly transaction files for Apple's reporting endpoints.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, entered into force on 16 November 2022 and became fully applicable to all covered entities on 17 February 2024. It creates a comprehensive regulatory framework for online intermediaries and platforms to protect users' fundamental rights online, combat illegal content, and ensure high transparency.

Under Articles 30 and 31 of the DSA, app distribution platforms must gather and verify identifying information for "traders" distributing products in the EU. This "trader status" is verified using D-U-N-S numbers, telephone, and email verification, and must be publicly displayed on the app store listings.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council of 19 October 2022 on a Single Market For Digital Services.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no policy template or decision tree to guide developers in correctly self-classifying as a "trader" versus a "non-trader" under EU consumer protection law.
- **Missing Documentation:**
  The repository lacks guides explaining the documentation requirements and two-factor verification workflows required by Apple and Google to secure verified trader status.
- **Missing Code:**
  No codebase scanners or linters exist in the repository to dynamically check whether the required contact information or trader declaration matches the published storefront metadata.
- **Missing Disclosure:**
  Public-facing metadata templates do not include designated sections or boilerplate disclosures to display the verified postal address, telephone, and email of the trader.
- **Missing Logging:**
  The playbook does not provide schemas for logging user-reported illegal content or notices of copyright infringement as required under the DSA's Notice and Action mechanisms.
- **Missing Testing:**
  No integration tests exist to verify that non-trader notification dialogs are dynamically displayed to EU consumers during the onboarding or purchasing flows.
- **Missing Evidence:**
  The repository is missing standardized templates for preparing the documentation needed to verify trader identity, such as company registrations or utility bills.
- **Missing Audit Trail:**
  There is no audit trail schema to track user flag reports, moderation reviews, or when trader registration details were last verified or updated.

### 8.3 Remediation and Action Plan
1. Create a clear "Trader vs Non-Trader" classification flowchart for product listings.
2. Incorporate static rules into metadata audit scripts to verify that trader email, phone, and address exist in EU-facing metadata drafts.
3. Formulate templates for Notice and Action portal pages that apps can utilize to facilitate user reporting of illegal or infringing UGC content.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became fully applicable across EU Member States on 28 June 2025. It aims to harmonize accessibility requirements for key products and services across the European single market, specifically extending accessibility standards to e-commerce, banking, transport booking, and e-books.

The EAA applies to mobile apps and websites distributing covered services to EU consumers. Apps must comply with harmonized standard EN 301 549, which is built on WCAG 2.1 Level AA, and must include a publicly accessible accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council of 17 April 2019 on the accessibility requirements for products and services.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing an enterprise Accessibility Policy template that outlines WCAG 2.1/2.2 AA target compliance, microenterprise exemption rules, or national penalty mapping.
- **Missing Documentation:**
  While the playbook outlines accessibility rules in general, it lacks detailed documentation of the EN 301 549 Chapter 11 mobile software clauses, which contain unique mobile accessibility requirements.
- **Missing Code:**
  The codebase lacks mock accessibility statement pages or user interface components configured to facilitate deep accessible navigation.
- **Missing Disclosure:**
  The repository does not contain templates for a compliant, published Accessibility Statement as required by Member State implementations.
- **Missing Logging:**
  There are no logging provisions or database schemas to record accessibility barriers reported by users or the progress of remediation tickets.
- **Missing Testing:**
  The existing static accessibility scanner in this repository checks simple code patterns but lacks automated tests to simulate screen readers, dynamic scaling, or keyboard navigation flows.
- **Missing Evidence:**
  The playbook contains no templates for Voluntary Product Accessibility Templates (VPAT) or accessibility audit reports to prove compliance to regulators.
- **Missing Audit Trail:**
  There is no unalterable audit trail system to log the results of regular accessibility audits, user reports, and verification histories.

### 9.3 Remediation and Action Plan
1. Write a complete Accessibility Statement template conforming to the requirements of EN 301 549 Annex B.
2. Integrate advanced checking algorithms into the accessibility audit scripts to verify structural hierarchies and contrast minimums on mock outputs.
3. Designate a remediation framework to track accessibility bug reports from initial filing to verification check.

---

## 10. EU Data Act

### 10.1 Regulatory Overview and Background
The EU Data Act, Regulation (EU) 2023/2854, entered into force on 11 January 2024, with its core obligations becoming applicable on 12 September 2025 and its "access-by-design" requirements applicable on 12 September 2026. It establishes a harmonized framework for sharing data generated by the use of connected products or related services (such as smart wearables, connected medical devices, and smart home appliances).

For app developers interacting with connected devices, the Data Act mandates that apps must be designed in a way that data generated by their use is, by default, easily, securely, and directly accessible to the user and designated third parties.

Official Citation: Regulation (EU) 2023/2854 of the European Parliament and of the Council of 13 December 2023 on harmonised rules on fair access to and use of data.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no written Data Sharing and Portability Policy showing how to handle direct user access requests or cross-border transfers under the Data Act.
- **Missing Documentation:**
  The repository lacks detailed technical manuals explaining the API specifications or encryption standards required to make device-generated datasets accessible.
- **Missing Code:**
  The backend mock implementations completely lack endpoints or data conversion scripts to export raw iot/wearable telemetry data in structured, machine-readable formats.
- **Missing Disclosure:**
  User interfaces do not prominently disclose what categories of data are generated by the connected device and how the user can exercise their right to share that data.
- **Missing Logging:**
  There is no system schema to log data sharing consent, data access transactions, or third-party data recipient authorizations.
- **Missing Testing:**
  No automated integration tests exist to simulate or verify that user data can be successfully packaged and exported to third parties without friction.
- **Missing Evidence:**
  The repository lacks standardized templates of technical documentation sheets proving that the connected app meets "access-by-design" engineering requirements.
- **Missing Audit Trail:**
  The repository lacks a cryptographic audit trail tracking who accessed what data, when consent was granted, or when data transmission agreements were updated.

### 10.3 Remediation and Action Plan
1. Formulate a technical design guide outlining safe "access-by-design" database models and data packaging procedures.
2. Implement sample endpoints showing how telemetry and wearable datasets are parsed and packaged for user export.
3. Create a template Data Portability Request Log to securely maintain a legal audit trail of sharing agreements.

---

## 11. EU Cyber Resilience Act (CRA)

### 11.1 Regulatory Overview and Background
The EU Cyber Resilience Act (CRA), Regulation (EU) 2024/2847, entered into force on 11 December 2024. Active vulnerability reporting and security incident notification obligations become applicable on 11 September 2026, and the main security-by-design and vulnerability handling requirements become applicable on 11 December 2027.

The CRA establishes EU-wide cybersecurity requirements for "products with digital elements" placed on the EU market, including mobile applications that connect to physical products or serve as standalone software. Developers must ensure security-by-design, perform risk assessments, handle vulnerabilities, and report active exploits to ENISA.

Official Citation: Regulation (EU) 2024/2847 of the European Parliament and of the Council on horizontal cybersecurity requirements for products with digital elements.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no corporate Security-by-Design or Vulnerability Disclosure Policy template to coordinate vulnerabilities and ENISA reporting timelines.
- **Missing Documentation:**
  The repository is missing detailed, developer-facing documentation on how to perform cybersecurity risk assessments or generate a Software Bill of Materials (SBOM) for mobile apps.
- **Missing Code:**
  The codebase lacks integrated scripts or continuous integration configurations to automate Software Bill of Materials (SBOM) generation (such as CycloneDX) or static analysis checks.
- **Missing Disclosure:**
  Onboarding or settings pages do not disclose security support windows or instructions on how security researchers can securely report vulnerabilities.
- **Missing Logging:**
  The repository lacks centralized database logging schemas or incident management tracking templates designed to securely log discovered vulnerabilities or active exploits.
- **Missing Testing:**
  No automated security tests or fuzzing test workflows exist to verify that mobile endpoints resist standard OWASP Mobile Top 10 vulnerabilities.
- **Missing Evidence:**
  The playbook has no template of a CRA Conformity Assessment or CE declaration of conformity to prove compliance to national market surveillance authorities.
- **Missing Audit Trail:**
  An immutable audit trail system to log code commits, patch deployments, security reviews, and vulnerability resolution timelines is entirely missing.

### 11.3 Remediation and Action Plan
1. Establish a Vulnerability Disclosure Policy (VDP) template that includes clear mechanisms for researcher communication and ENISA reporting.
2. Add build-time configurations to output dependency lists and verify mobile assets against known vulnerability indices automatically.
3. Implement a cryptographic signature script to verify the authenticity of OTA software updates.

---

## 12. US Children's Online Privacy Protection Act (COPPA) & Amended COPPA Rule

### 12.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6508, and its implementing Rule (16 CFR Part 312), regulate operators of websites or online services directed to children under 13, and general-audience services with actual knowledge of child data collection. The FTC finalized the Amended COPPA Rule on 22 April 2025, with compliance enforced on 22 April 2026.

The Amended Rule expands the definition of Personal Identifiable Information (PII) to include biometric identifiers and facial templates, requires separate opt-in consent for third-party disclosures, mandates a written data retention policy, and requires a written information-security program.

Official Citation: Children's Online Privacy Protection Rule, 16 CFR Part 312.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Children's Privacy and Data Retention Policy mapping the specific requirements of 16 CFR Part 312.
- **Missing Documentation:**
  Checklists in docs/PRE-SUBMISSION-CHECKLIST.md are missing guidelines for the newly expanded definitions of PII and biometric identifiers introduced in the 2025 Amended Rule.
- **Missing Code:**
  The codebase has no mock parental gate implementation or integration scripts demonstrating how to obtain verifiable parental consent via face-match or knowledge-based authentication.
- **Missing Disclosure:**
  Onboarding interfaces do not provide compliant, direct privacy disclosures to parents before collecting any child data or sharing with third parties.
- **Missing Logging:**
  There is no secure backend schema to log parental consent actions, parental revocations, or the automatic deletion of children's data after the retention period.
- **Missing Testing:**
  No unit or integration tests exist to verify that when a user's age is confirmed under 13, all analytics, advertising SDKs, and biometric captures are dynamically disabled.
- **Missing Evidence:**
  The repository lacks templates of written Information Security Programs (WISP) or Data Protection Impact Assessments (DPIA) directed at child privacy.
- **Missing Audit Trail:**
  An unalterable audit trail logging when consent requests were sent, when parental consent was verified, and when raw verification assets were destroyed is absent.

### 12.3 Remediation and Action Plan
1. Build a template parental verification gate that satisfies FTC guidelines (e.g. face matching to ID or knowledge-based questions).
2. Code a sample onboarding script that strictly suppresses third-party tracking APIs when the age entry returned indicates a minor.
3. Create a model Written Information Security Program (WISP) for small mobile teams to satisfy the Amended COPPA Rule requirement.

---

## 13. California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA)

### 13.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), represents the baseline consumer privacy standard in California. The California Privacy Protection Agency (CPPA) finalized updated regulations effective 1 January 2026, phasing in automated decision-making controls and cybersecurity audits.

Covered businesses must provide a privacy policy, a notice at collection, facilitate consumer rights (access, deletion, correction), and provide prominent links allowing consumers to opt out of the sale or sharing of their personal information and limit the use of sensitive personal info.

Official Citation: California Civil Code Section 1798.100 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no comprehensive California Privacy Policy or Notice at Collection template.
- **Missing Documentation:**
  The checklists lack detailed documentation explaining how to process and honor Global Privacy Control (GPC) signals in native mobile views.
- **Missing Code:**
  There is no frontend boilerplate code for displaying "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information" links.
- **Missing Disclosure:**
  Public-facing documentation fails to include required CCPA disclosures regarding the categories of personal info collected and the purpose of collection.
- **Missing Logging:**
  There are no logging schemas to record consumer rights requests, fulfillment statuses, or Global Privacy Control (GPC) opt-out signals.
- **Missing Testing:**
  No automated test suites exist to verify that GPC opt-out signals are respected and that tracking pixels are dynamically blocked when opt-out is activated.
- **Missing Evidence:**
  The repository is missing templates of regulatory disclosure tables outlining data collection, sale, or sharing stats over the preceding 12 months.
- **Missing Audit Trail:**
  A secure audit trail system to log the receipt, verification, and resolution timelines of consumer rights requests is not implemented.

### 13.3 Remediation and Action Plan
1. Create a template CPRA-compliant Notice at Collection.
2. Code an inline middleware pattern that checks for GPC opt-out headers and blocks third-party advertising SDK initialization dynamically.
3. Draft a secure request-fulfillment database schema to record consumers' data requests and verify timelines.

---

## 14. Illinois Biometric Information Privacy Act (BIPA)

### 14.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, enacted in 2008, governs the collection, storage, and use of biometric identifiers (such as fingerprints, iris scans, and facial geometry) in Illinois. Amendment SB 2979 (effective 2 August 2024) limits liability by clarifying that repeated collections of the same biometric constitute a single violation.

BIPA requires written notice, a written release (consent) before capture, a publicly available retention schedule, and a strict ban on the sale or profit of biometric data. It is heavily litigated due to its private right of action and statutory damages.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template Biometric Data Privacy and Retention Policy specifying retention schedules and destruction criteria.
- **Missing Documentation:**
  The checklists do not provide developer instructions on distinguishing on-device biometric auth (e.g. Face ID / Touch ID) from backend biometric data storage.
- **Missing Code:**
  The codebase contains no code templates or dialog components for presenting and collecting BIPA-compliant written releases before capturing biometric data.
- **Missing Disclosure:**
  The UI mocks fail to display required BIPA disclosures regarding why the biometric data is collected and how long it will be stored.
- **Missing Logging:**
  There is no backend logging schema designed to securely record the receipt of biometric releases and consent timestamps without storing the biometric data itself.
- **Missing Testing:**
  No automated integration tests exist to verify that the app blocks the biometric capture flow if a user declines or revokes the biometric consent.
- **Missing Evidence:**
  The playbook lacks verified templates of signed biometric consent release forms or proof-of-destruction certificates for compliance records.
- **Missing Audit Trail:**
  A secure, immutable audit trail system to track consent acquisitions, retention reviews, and biometric data deletion schedules is entirely missing.

### 14.3 Remediation and Action Plan
1. Draft a standard Biometric Information Disclosure and Written Consent Release form.
2. Develop a native UI modal specifically designed to retrieve user approval before executing biometric data capture SDKs.
3. Establish a standard database schema to log biometric data lifetimes and destruction executions.

---

## 15. UK Online Safety Act 2023

### 15.1 Regulatory Overview and Background
The UK Online Safety Act 2023, which received royal assent on 26 October 2023 with age-assurance provisions coming into force on 25 July 2025, places legal duties on providers of internet services that allow users to share user-generated content or interact online.

Enforced by Ofcom, the Act mandates that providers implement highly effective age-assurance methods (such as facial age estimation or credit card checks) to protect children from harmful or age-inappropriate content. It carries substantial penalties for non-compliance.

Official Citation: Online Safety Act 2023 (c. 30).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Child Safety or Age Assurance Policy demonstrating compliance with Ofcom's highly effective age-assurance requirements.
- **Missing Documentation:**
  The repository is missing specific developer checklists or technical documentation detailing how to integrate third-party age estimation APIs.
- **Missing Code:**
  The codebase lacks mock integrations or API hooks to initiate facial age estimation or handle child-access blocks dynamically.
- **Missing Disclosure:**
  Public-facing documents and UI templates do not provide prominent child safety disclosures or easily accessible reporting links for harmful content.
- **Missing Logging:**
  There are no schemas or logging frameworks to capture user reports of illegal or harmful content and Ofcom's mandatory compliance audits.
- **Missing Testing:**
  No automated tests exist to verify that the application blocks minor accounts from accessing harmful or restricted user-generated content sections.
- **Missing Evidence:**
  The playbook contains no templates of Child Safety Risk Assessments or Ofcom compliance declarations.
- **Missing Audit Trail:**
  An immutable audit trail system to track content moderation decisions, user suspensions, and the deletion of age-verification data is not implemented.

### 15.3 Remediation and Action Plan
1. Formulate a Child Safety Risk Assessment checklist aligned with Ofcom guidelines.
2. Add a front-end "Report Content" flow to UGC templates to allow rapid flagging and moderation.
3. Code an automated age-assurance verification hook that checks for verification confirmation status before loading premium UGC.

---

## 16. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 16.1 Regulatory Overview and Background
The Australian Online Safety Amendment (Social Media Minimum Age) Act 2024, which became applicable on 10 December 2025, bans minors under 16 from holding accounts on social media platforms.

The Act places strict obligations on social media service providers to implement robust, privacy-preserving age-assurance systems to screen and block under-16 users, and mandates that any age-assurance data must be immediately ringfenced and destroyed to protect privacy.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template Social Media Age-Gating Policy mapping the strict requirements of the Australian minimum age ban.
- **Missing Documentation:**
  The repository lacks developer-facing documentation on how to ringfence and purge Australian age-assurance data.
- **Missing Code:**
  There are no native code blocks or platform checks to query Australian region settings and block under-16 registration attempts.
- **Missing Disclosure:**
  Onboarding templates fail to explicitly disclose that users under 16 are legally prohibited from creating accounts and that verification data is immediately destroyed.
- **Missing Logging:**
  The database schemas do not include provisions for logging age verification outcomes while strictly ensuring no retention of identifying age-assurance records.
- **Missing Testing:**
  No automated test workflows exist to verify that an Australian IP or locale triggers the age-verification funnel and successfully blocks minor sign-ups.
- **Missing Evidence:**
  The playbook contains no compliance templates for submitting age-assurance effectiveness audits to the eSafety Commissioner.
- **Missing Audit Trail:**
  An unalterable audit trail system to record the historical rollout of age-gating mechanisms and the execution of age data deletion triggers is completely absent.

### 16.3 Remediation and Action Plan
1. Draft a comprehensive Social Media Age-Assurance and Data Protection Policy.
2. Implement backend hooks that capture age status, complete the validation, and execute immediate data purging of raw verification tokens.
3. Design dynamic unit tests to simulate Australian location signals and confirm minor registration attempts are rejected.

---

## 17. Brazil Digital ECA (Law 15,211/2025)

### 17.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025), which became enforceable on 17 March 2026, regulates minors' access to digital environments, prohibiting simple self-declaration checkboxes for age verification.

Developers must implement robust age-verification methods (such as document checks, CPF database verification, or facial age estimation) for apps containing mature or age-restricted content.

Official Citation: Lei nº 15.211/2025 (Estatuto da Criança e do Adolescente Digital).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Brazil-specific Digital ECA Minor Protection Policy template.
- **Missing Documentation:**
  The repository lacks technical guides explaining how to integrate with the CPF (Cadastro de Pessoas Físicas) verification APIs.
- **Missing Code:**
  The frontend templates lack Portuguese-language age-verification modals or interface configurations for submitting verification documents.
- **Missing Disclosure:**
  Public-facing metadata lacks Brazilian parental warning disclosures and appropriate age rating descriptions.
- **Missing Logging:**
  There are no logging provisions to record the completion of parental consent or CPF checks in compliance with LGPD (Lei Geral de Proteção de Dados).
- **Missing Testing:**
  No automated tests exist to verify that the app restricts 18-plus features or loot-box mechanics on Brazil-locale devices without completed verification.
- **Missing Evidence:**
  The repository is missing templates of compliance audits demonstrating that age-verification methods are accurate and secure.
- **Missing Audit Trail:**
  There is no secure audit trail to log changes to the age-verification workflows or the immediate destruction of uploaded identification documents.

### 17.3 Remediation and Action Plan
1. Create a Portuguese-translated Minor Protection Policy template.
2. Build mock CPF check scripts demonstrating secure database integration without local data storage.
3. Program a scheduled transaction that automatically deletes uploaded ID documents immediately after confirmation.

---

## 18. India Digital Personal Data Protection Act (DPDPA) 2023 / DPDP Rules 2025

### 18.1 Regulatory Overview and Background
The Digital Personal Data Protection Act (DPDPA), 2023, along with the DPDP Rules 2025 (notified on 13 November 2025), establishes India's comprehensive data protection framework. The consent and child privacy rules become fully enforceable on 13 May 2027.

The DPDPA classifies everyone under 18 as a child, requiring verifiable parental consent through government-backed systems (such as DigiLocker) before processing any child data. It strictly prohibits targeted advertising or behavioral tracking of children.

Official Citation: The Digital Personal Data Protection Act, 2023 (No. 22 of 2023).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Consent Manager Policy or Child Data Protection Policy aligned with the DPDPA and DPDP Rules 2025.
- **Missing Documentation:**
  The repository lacks developer documentation outlining the technical integration of DigiLocker or other India-approved verifiable parental consent platforms.
- **Missing Code:**
  No code templates exist to demonstrate how to implement DPDPA-compliant, bilingual (English and scheduled languages) consent notices.
- **Missing Disclosure:**
  The onboarding flows lack explicit notices explaining what categories of children's data are processed and why behavioral tracking is suppressed.
- **Missing Logging:**
  There are no database schemas to record DPDPA consent, parent-child relationships, or parent consent revocations.
- **Missing Testing:**
  No integration tests exist to verify that the app blocks all tracking SDKs and personalized advertising scripts for users under 18 in India.
- **Missing Evidence:**
  The repository lacks templates for Consent Manager certifications or Child Personal Data Impact Assessments.
- **Missing Audit Trail:**
  A secure, unalterable audit trail logging the receipt, modification, and withdrawal of consent by Indian data principals is completely absent.

### 18.3 Remediation and Action Plan
1. Formulate DPDPA-compliant Consent Forms.
2. Draft sample bilingual onboarding modals asking child confirmation and parental details.
3. Design a test case that verifies all analytical triggers and tracking tokens remain null when user's age is set as minor in India storefronts.

---

## 19. Singapore IMDA Code of Practice for Online Safety / PDPA

### 19.1 Regulatory Overview and Background
The Singapore Infocomm Media Development Authority (IMDA) Code of Practice for Online Safety for App Distribution Services became applicable on 1 April 2026. This Code requires app distribution services and developers to implement age-assurance measures to prevent users under 18 from downloading age-inappropriate apps.

Additionally, the Personal Data Protection Act (PDPA) governs general data privacy in Singapore, requiring organizations to designate a Data Protection Officer (DPO) and report data breaches within 3 days.

Official Citation: IMDA Code of Practice for Online Safety, 2026 / Personal Data Protection Act 2012.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template Singapore-compliant Data Privacy and App Store Safety Policy.
- **Missing Documentation:**
  The checklists do not provide developer instructions on meeting Singapore's 18-plus download block and PDPA's 3-day breach notification workflows.
- **Missing Code:**
  There are no backend hooks or mock implementations in this repository demonstrating real-time integration with Singapore age-assurance platforms.
- **Missing Disclosure:**
  UI templates fail to display required disclosures regarding the appointment and contact details of the Data Protection Officer (DPO).
- **Missing Logging:**
  There is no database logging schema designed to track and report data breaches within the mandatory 3-day PDPA timeline.
- **Missing Testing:**
  No automated tests exist to verify that Singaporean users under 18 are prevented from accessing age-restricted features or downloads.
- **Missing Evidence:**
  The playbook contains no templates for PDPA Data Protection Impact Assessments or IMDA safety reports.
- **Missing Audit Trail:**
  A secure audit trail to log the history of security incident alerts, breach assessments, and DPO decisions is entirely missing.

### 19.3 Remediation and Action Plan
1. Establish a standard Incident Management runbook detailing the PDPA 3-day reporting requirements.
2. Draft compliant DPO contact disclosure blocks inside the settings templates.
3. Create a verification integration test simulating 18-plus access blocks for Singapore-based mock devices.

---

## 20. US FTC Health Breach Notification Rule / Washington My Health My Data Act (MHMDA)

### 20.1 Regulatory Overview and Background
The US FTC Health Breach Notification Rule, 16 CFR Part 318, finalized its 2024 amendments on 25 June 2024, establishing that any unauthorized sharing of health or sensitive personal data with third-party advertisers is treated as a breach, requiring a mandatory 60-day notification.

Additionally, Washington's My Health My Data Act (MHMDA), effective 31 March 2024, places strict consent, disclosure, and deletion requirements on consumer health data collected from users in Washington, carrying a private right of action.

Official Citations: 16 CFR Part 318 (FTC) / Revised Code of Washington Chapter 19.373.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no written template Consumer Health Privacy Policy or Health Breach Response Policy.
- **Missing Documentation:**
  The checklists do not provide step-by-step developer guidelines for identifying what features or SDKs collect consumer health data.
- **Missing Code:**
  The codebase lacks mock consent dialogs specifically designed to collect MHMDA-compliant, separate, explicit consent before collecting consumer health data.
- **Missing Disclosure:**
  Public-facing documentation fails to include a prominent, distinct Consumer Health Privacy Link on the homepage of health-adjacent UI mocks.
- **Missing Logging:**
  There are no logging provisions or database schemas to record health data consent, consent revocations, or deletion requests.
- **Missing Testing:**
  The test suites do not include automated integration tests to verify that health data collection and sharing is blocked on failure to obtain explicit consent.
- **Missing Evidence:**
  The repository is missing templates of signed consumer health privacy releases or breach assessment logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking the deployment of health data privacy settings, consent updates, and health breach notifications is entirely absent.

### 20.3 Remediation and Action Plan
1. Build a template Consumer Health Privacy Policy satisfying MHMDA requirements.
2. Develop mock frontend layouts displaying the prominent MHMDA links.
3. Formulate breach evaluation logs to systematically evaluate unauthorized health data leaks.

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
| **European Accessibility Act (EAA)** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU Data Act** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU Cyber Resilience Act (CRA)** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA & Amended COPPA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **California CCPA / CPRA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety Act 2023** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Online Safety Act 2024** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA 2023 / DPDP Rules 2025** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore IMDA Code of Practice** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **US FTC Health Breach / Washington MHMDA** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Five of the original six frameworks here are already named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

With the addition of 14 new regulations to complete a thorough 20-regulation sweep, the roadmap for this playbook is clear: it must move from being a store-rejection reference to a comprehensive global regulatory compliance engine.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex, FTC, and the other primary sources rather than trusting the dates here on their own.

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- EU Data Act, [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)
- EU Cyber Resilience Act, [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023, [c. 30](https://www.legislation.gov.uk/ukpga/2023/30/contents)
- India DPDPA, [No. 22 of 2023](https://egazette.gov.in/WriteReadData/2023/248045.pdf)
- US Health Breach Notification Rule, [16 CFR Part 318](https://www.federalregister.gov/documents/2024/05/30/2024-11425/health-breach-notification-rule)
