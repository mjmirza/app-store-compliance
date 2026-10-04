# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global storefronts, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms (such as Apple App Store and Google Play Store) to ensure fair competition and openness in digital markets.

For app developers operating in the EU, the DMA establishes rights to utilize alternative app distribution channels, implement external purchase links, offer alternative in-app payment systems alongside platform IAP, and access hardware/software interoperability features (such as HCE NFC and alternative browser engines).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an internal DMA Operations Policy detailing how the organization evaluates and chooses between App Store, Web Distribution, and Alternative App Marketplace channels.
- **Missing Documentation:**
  Existing guides explain DMA rules conceptually but lack step-by-step developer guides for setting up StoreKit External Purchase Link entitlements (`com.apple.developer.storekit.external-purchase-link`) and implementing the required custom link sheet APIs.
- **Missing Code:**
  The repository contains no functional code samples or SDK wrappers for invoking `ExternalPurchaseCustomLink` or integrating with the External Purchase Server API for monthly transaction reporting.
- **Missing Disclosure:**
  User onboarding and checkout UI templates do not provide required DMA disclosure modal components informing users that they are transacting outside platform ecosystems without platform consumer guarantees.
- **Missing Logging:**
  There are no server-side database schemas or log collectors designed to log external purchase transactions for monthly report submission to platform operators within the mandatory 15-day window.
- **Missing Testing:**
  No automated unit or end-to-end integration tests exist to verify that external purchase links correctly present system disclosure sheets and prevent illegal co-mingling of platform IAP and external links on the same storefront.
- **Missing Evidence:**
  The repository lacks templates for reporting sheets, proof of Attachment 14 acceptance under Apple's unified business terms, or stand-by letter of credit documentation for operating alternative marketplaces.
- **Missing Audit Trail:**
  No immutable record exists to track monthly external transaction reporting submissions, fee reconciliations, or entitlement changes over time.

### 7.3 Remediation and Action Plan
1. Draft a comprehensive DMA Distribution & Steering Strategy document outlining entitlement management and fee structure choices.
2. Implement code helpers for `ExternalPurchaseCustomLink` and server-side automation for External Purchase Server API monthly reporting.
3. Add UI components for DMA transaction disclosures and region-gated alternative payment option sheets.
4. Establish automated tests verifying that external offer links trigger mandatory system modal sheets and respect EU storefront boundaries.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) imposes strict transparency and consumer protection duties on online platforms and digital services providers operating in the EU market.

Under Articles 30 and 31, app stores are required to collect, verify, and publish trader contact and identity information for all developers offering apps to EU consumers. Developers who are traders must maintain verified status (D-U-N-S, address, phone, email, 2FA) or face app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no formal Trader Status Evaluation Policy to help developers determine whether their app activities classify them as a trader or non-trader under EU law.
- **Missing Documentation:**
  Checklists mention DSA trader requirements but lack detailed instructions on managing App Store Connect and Google Play Console trader verification workflows, D-U-N-S profile alignment, and 2FA contact validation.
- **Missing Code:**
  The repository lacks automated pre-submission CLI checks or guard hooks to query store metadata APIs and flag missing or unverified DSA trader declarations prior to submission.
- **Missing Disclosure:**
  In-app about screens and legal settings pages lack standardized components for displaying verified trader identity, physical address, phone number, and electronic contact details.
- **Missing Logging:**
  There is no logging system to capture consumer contact inquiries submitted via published DSA contact channels or to log notice-and-action reports received regarding illegal content.
- **Missing Testing:**
  No automated CI checks verify that store metadata configurations contain complete, verified DSA trader information before initiating release builds targeting EU storefronts.
- **Missing Evidence:**
  The repository lacks document templates for proving trader registration, D-U-N-S verification records, or two-factor authentication logs required during platform audits.
- **Missing Audit Trail:**
  There is no historical audit log tracking changes to trader declarations, contact detail updates, or platform compliance notifications.

### 8.3 Remediation and Action Plan
1. Publish a Trader Status Guidelines document explaining EU trader criteria and step-by-step App Store Connect / Play Console setup.
2. Update `scripts/metadata-audit.py` to inspect trader declaration status and flag missing EU DSA fields.
3. Add a standardized "Trader Identity & Contact" UI component in the references directory for inclusion in app settings.
4. Build a pre-release validation step that blocks deployment if DSA trader verification is pending or incomplete.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) entered into full application on 28 June 2025. It establishes mandatory accessibility requirements for consumer products and services, including mobile applications for e-commerce, banking, travel, media, and e-books reaching EU users.

Compliance with the EAA requires satisfying the harmonised standard EN 301 549 (specifically Chapter 11 for mobile apps and non-web software), which builds on WCAG 2.1 Level AA and adds specific mobile accessibility criteria including VoiceOver/TalkBack support, Dynamic Type scaling, color contrast, and published accessibility statements.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an overarching Digital Accessibility Policy establishing organizational commitment to EN 301 549 and WCAG 2.1 AA standards.
- **Missing Documentation:**
  While accessibility is referenced generally, the repository lacks a comprehensive EN 301 549 Chapter 11 mobile audit guide detailing the 64 additional requirements beyond base WCAG rules.
- **Missing Code:**
  Existing UI templates lack full accessibility markup, missing accessibility labels (`accessibilityLabel`), traits (`accessibilityTraits`), hint strings, and dynamic font scale container rules.
- **Missing Disclosure:**
  The repository lacks templates for a compliant Accessibility Statement (as required by EN 301 549 Annex B/C) to be published in-app and on product web pages.
- **Missing Logging:**
  There are no logging mechanisms or feedback collection schemas designed to capture user-reported accessibility barrier reports or assistive technology compatibility issues.
- **Missing Testing:**
  Automated accessibility scanning scripts in the repository (`scripts/accessibility-audit.py`) cover basic rule checks but lack full EN 301 549 Chapter 11 test suites and screen-reader automated simulation flows.
- **Missing Evidence:**
  The repository lacks templates for formal Accessibility Conformance Reports (VPAT / EN 301 549 ACR) to present to regulators or enterprise clients.
- **Missing Audit Trail:**
  No historical log tracks accessibility audit results, remediation cycles, or user accessibility feedback resolution over time.

### 9.3 Remediation and Action Plan
1. Formulate and publish a formal Digital Accessibility Policy aligned with EN 301 549 Chapter 11.
2. Upgrade `scripts/accessibility-audit.py` to validate EN 301 549 Chapter 11 mobile-specific rules alongside standard WCAG 2.1 AA checks.
3. Add a compliant Accessibility Statement markdown template (`ACCESSIBILITY_STATEMENT.md`) and in-app display component.
4. Create a standardized Voluntary Product Accessibility Template (VPAT / EN 301 549 ACR) template in the references directory.

---

## 10. US Amended COPPA Rule

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, was significantly expanded by the FTC's 2025 Final Rule (90 FR 16918, effective 23 June 2025, with full general compliance enforced from 22 April 2026).

The amended rule expands personal information to include biometric identifiers and government IDs, mandates separate opt-in consent for third-party disclosures and targeted ads, requires written data retention policies with prohibited indefinite retention, and mandates a written information security program with annual risk assessments.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive Children's Privacy and Data Retention Policy incorporating the expanded 2025 COPPA Rule requirements.
- **Missing Documentation:**
  Checklists mention basic COPPA age gating but lack detailed developer guides for implementing separate third-party disclosure opt-ins, biometric data inventories, and written retention schedules.
- **Missing Code:**
  Code templates lack two-step parental consent flows, separate opt-in toggles for third-party data sharing, and automated data purging scripts to eliminate children's data upon retention expiry.
- **Missing Disclosure:**
  Privacy policy templates do not contain updated COPPA disclosures explicitly listing biometric identifiers as personal information or detailing separate consent mechanisms for advertising.
- **Missing Logging:**
  There are no secure logging schemas to record separate consent states (general app use vs. third-party disclosure) or to log automated data retention purge executions.
- **Missing Testing:**
  The repository lacks automated unit tests to verify that children's data collection is completely suppressed unless both base consent and separate third-party opt-in flags are active.
- **Missing Evidence:**
  The repository lacks templates for a Written Information Security Program (WISP) document, annual risk assessment reports, or third-party vendor COPPA assessment records.
- **Missing Audit Trail:**
  No tamper-evident audit trail exists to track parental consent grants, consent revocations, age-gate inputs, and automated data destruction logs.

### 10.3 Remediation and Action Plan
1. Draft an updated COPPA Compliance Protocol incorporating biometric identifier handling and explicit retention limits.
2. Implement modular UI consent components supporting separate toggles for base app processing versus third-party ad sharing.
3. Build database cleanup routines to automatically purge child personal data in accordance with written retention schedules.
4. Establish automated tests verifying that no tracking SDKs initialize when an under-13 age signal is detected without valid verifiable parental consent.

---

## 11. California Privacy (CCPA / CPRA / CPPA 2026 Regulations)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and governed by the California Privacy Protection Agency (CPPA) 2026 Regulations, imposes strict privacy and consumer control obligations on businesses operating in California.

Key requirements include honoring Global Privacy Control (GPC) signals sent via browser/webview headers, providing explicit "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links, providing notices at collection, handling consumer rights requests (know, delete, correct, opt-out), and preparing for automated decision-making technology (ADMT) disclosures and cybersecurity audits.

Official Citations: California Civil Code Sec. 1798.100 et seq., 11 CCR Sec. 7000 et seq. (CPPA Regulations).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a dedicated California Privacy Rights Policy covering CCPA/CPRA consumer rights, sensitive personal information handling, and ADMT evaluation criteria.
- **Missing Documentation:**
  Developer guides lack detailed technical specifications on how to intercept and honor `Sec-GPC` headers in embedded webviews and map them to native privacy state flags.
- **Missing Code:**
  Client templates do not include native code logic to detect Global Privacy Control signals or helper classes to manage "Do Not Sell/Share" and "Limit Sensitive PI" toggle states.
- **Missing Disclosure:**
  Onboarding and settings UI templates lack required California Notice at Collection components and "Do Not Sell or Share My Personal Information" modal sheets.
- **Missing Logging:**
  There are no backend database schemas or API logging interfaces designed to record consumer rights requests (access, deletion, correction, opt-out) and track the statutory 45-day response window.
- **Missing Testing:**
  The test suites contain no automated unit tests to confirm that sending a `Sec-GPC: 1` header or toggling the opt-out switch immediately halts data transmission to third-party ad networks.
- **Missing Evidence:**
  The repository lacks document templates for California Consumer Rights Request Metrics reporting or ADMT Risk Assessment records.
- **Missing Audit Trail:**
  No immutable log exists to track consumer opt-out requests, GPC signal detection events, data deletion executions, or annual privacy policy update reviews.

### 11.3 Remediation and Action Plan
1. Publish a comprehensive California Privacy Rights Compliance Guide detailing GPC signal handling and CCPA request workflows.
2. Add native client code utilities to intercept `Sec-GPC` webview headers and synchronize opt-out state across all SDKs.
3. Build UI components for Notice at Collection, "Do Not Sell/Share", and "Limit Sensitive PI" settings.
4. Implement automated CI tests verifying that opt-out states disable analytics and advertising SDK data pipelines.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, use, safeguarding, handling, and destruction of biometric identifiers (fingerprints, voiceprints, retina/iris scans, facial geometry scans) by private entities.

BIPA requires written informed notice and an executed written release prior to capturing any biometric data, a publicly available written retention schedule and destruction policy (mandating destruction within 3 years of last interaction), a strict prohibition on selling or profiting from biometric data, and strict storage security standards matching or exceeding industry best practices.

Official Citation: 740 ILCS 14 (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Biometric Data Management Policy detailing notice, release, retention, and destruction rules for biometric features.
- **Missing Documentation:**
  Developer checklists lack specific step-by-step guidance on identifying features that capture biometric identifiers (such as facial recognition onboarding, voice authentication, or liveness checks) and structuring BIPA-compliant consent flows.
- **Missing Code:**
  Codebase templates do not contain BIPA consent screen components, electronic signature capture utilities, or automated database routines to enforce 3-year maximum retention limits on biometric templates.
- **Missing Disclosure:**
  In-app onboarding flows lack mandatory pre-collection written disclosures informing users of the specific biometric identifier collected, the precise purpose, and the exact storage period.
- **Missing Logging:**
  There are no logging mechanisms designed to record the exact timestamp, disclosure version, and user authorization state for biometric releases.
- **Missing Testing:**
  The repository contains no unit or integration tests verifying that biometric capture APIs (such as camera/facial scanning frames) are strictly blocked until a valid BIPA release is executed.
- **Missing Evidence:**
  The repository lacks templates for a publicly accessible Biometric Retention Schedule and Destruction Policy document (`BIOMETRIC_RETENTION_POLICY.md`).
- **Missing Audit Trail:**
  An unalterable audit trail recording biometric consent executions, template destruction events, and annual security reviews is completely missing.

### 12.3 Remediation Action Plan
1. Draft a standardized Biometric Retention Schedule and Destruction Policy template for inclusion in client applications.
2. Create reusable UI components for BIPA written notice and electronic release capture before initializing camera or biometric hardware.
3. Build automated database purging jobs to destroy biometric templates upon account closure or reaching the 3-year retention cap.
4. Establish automated tests ensuring biometric SDKs remain uninitialized in the absence of an active, logged user release.

---

## 13. US Subscription Cancellation (FTC / ROSCA / State Negative Option Laws)

### 13.1 Regulatory Overview and Background
Subscription cancellation transparency is governed federally by Section 5 of the FTC Act and the Restore Online Shoppers' Confidence Act (ROSCA, 12 U.S.C. 8401), alongside strict state negative-option statutes in California (AB 313/SB 478), New York, and Massachusetts.

These legal frameworks mandate that any subscription or recurring billing mechanism sold to consumers must provide a simple, self-service cancellation mechanism that is at least as easy to use as the mechanism used to initiate the subscription. Buried cancellation paths, mandatory customer service phone calls, retention loops, or mailed letters are illegal.

Official Citations: 15 U.S.C. 45 (FTC Act Sec. 5), 15 U.S.C. 8401 (ROSCA), Cal. Bus. & Prof. Code Sec. 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no formal Subscription Cancellation and Auto-Renewal Policy outlining simple-cancellation standards across web and native account channels.
- **Missing Documentation:**
  Checklists fail to provide explicit design rules for cancellation flows, allowing potential ambiguity regarding whether phone-call or contact-form cancellation steps are permissible.
- **Missing Code:**
  Web and backend subscription management code templates in the repository do not include a self-service, one-click or two-tap cancellation path or subscription management webhook handler.
- **Missing Disclosure:**
  Subscription paywall templates do not prominently display full recurring billing terms, cancellation terms, renewal dates, and direct links to self-service cancellation paths immediately adjacent to the call-to-action button.
- **Missing Logging:**
  There are no database logging schemas designed to record cancellation request button clicks, timestamp receipts, immediate termination confirmations, or cancellation survey completion events.
- **Missing Testing:**
  No automated UI test scripts exist to verify that a user can successfully cancel an active subscription in two or fewer interactions without encountering forced retention blocks.
- **Missing Evidence:**
  The repository lacks templates for cancellation confirmation receipts, refund confirmation records, or compliance self-audit documentation proving frictionless cancellation.
- **Missing Audit Trail:**
  An immutable audit trail tracking historical cancellation request success rates, user cancellation timestamps, and paywall copy revisions is not maintained.

### 13.3 Remediation and Action Plan
1. Publish a Subscription Transparency and Frictionless Cancellation Guide for web and cross-platform billing flows.
2. Add self-service subscription management and cancellation UI components to all billing templates.
3. Build database logging tables to capture cancellation timestamps, authorization tokens, and immediate confirmation events.
4. Create automated end-to-end UI tests to verify that subscription cancellation completes in a self-service manner without administrative blocks.

---

## 14. UK Online Safety Act (OSA 2023)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) imposes legal duties of care on providers of user-to-user services and search services to protect users, particularly children, from illegal content and content harmful to children.

Key requirements include conducting statutory risk assessments, implementing Highly Effective Age Assurance (HEAA) methods (such as facial age estimation, open banking, or credit card checks; self-declaration is prohibited), turning off profiling and geolocation for children by default, maintaining child safety reporting mechanisms, and taking down illegal content (including CSAM and CSEA material) rapidly.

Official Citation: Online Safety Act 2023 (c. 50).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Online Safety and Child Protection Policy compliant with Ofcom's statutory codes of practice.
- **Missing Documentation:**
  Checklists mention UK requirements generally but lack precise step-by-step developer guides for implementing Highly Effective Age Assurance (HEAA) integrations or conducting an Online Safety Risk Assessment.
- **Missing Code:**
  Code templates lack integration with certified HEAA providers (e.g., Yoti, Veriff) and do not contain logic to automatically disable profiling, personalized feeds, and geolocation for UK minor accounts.
- **Missing Disclosure:**
  User-to-user UI templates lack clear UK-specific safety disclosures, reporting links, and clear explanations of content filtering and age gating policies.
- **Missing Logging:**
  There are no backend logging schemas or incident management workflows designed to capture user safety reports, illegal content flags, or CSAM/CSEA escalation logs to the UK National Crime Agency (NCA) portal.
- **Missing Testing:**
  The test suites do not include automated tests verifying that when a UK user is identified as a minor, profiling, geolocation, and direct messaging with strangers are strictly disabled.
- **Missing Evidence:**
  The repository lacks templates for an Online Safety Risk Assessment record, illegal content risk assessment summaries, or age-assurance efficacy test results.
- **Missing Audit Trail:**
  An immutable audit trail tracking content moderation decisions, user safety report resolutions, and HEAA verification logs is absent.

### 14.3 Remediation and Action Plan
1. Formulate a statutory UK Online Safety Policy and Risk Assessment Protocol.
2. Implement client code modules for certified Highly Effective Age Assurance (HEAA) methods and minor default state enforcement (profiling off, geolocation off).
3. Build backend workflows for user safety reporting, content moderation logging, and rapid NCA portal escalation.
4. Establish automated tests confirming that UK child accounts receive maximum privacy and safety defaults upon age determination.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 (enforceable from 10 December 2025, with penalties up to 49.5 million AUD) requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts.

The eSafety Commissioner's guidance mandates a waterfall of robust age-assurance methods (facial estimation, government ID verification, banking checks) and explicitly prohibits self-declaration checkboxes as a standalone method. Furthermore, all age-assurance data must be strictly ringfenced and destroyed immediately after verification.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Australian Social Media Minimum Age Policy or Age Data Ringfencing Protocol.
- **Missing Documentation:**
  Developer guides lack explicit technical details on integrating eSafety-approved age-assurance waterfalls and executing immediate age data destruction.
- **Missing Code:**
  The repository lacks native client and backend templates to execute Australian age-assurance verification, restrict under-16 account creation, and ringfence verification payloads.
- **Missing Disclosure:**
  Onboarding UI templates do not display mandatory disclosures informing Australian users that age verification is required by law and that raw verification data will be deleted immediately.
- **Missing Logging:**
  There are no database schemas designed to record age verification completion status while strictly logging the immediate deletion of raw identification documents.
- **Missing Testing:**
  The test suite lacks integration tests to verify that an under-16 user signal prevents account registration and immediately purges all submitted verification artifacts.
- **Missing Evidence:**
  The repository lacks templates for eSafety Industry Code Risk Assessments or independent age-assurance accuracy audit reports.
- **Missing Audit Trail:**
  An unalterable audit trail logging age-verification attempts, verification outcomes, and automated data deletion execution receipts is missing.

### 15.3 Remediation and Action Plan
1. Publish an Australian Age Assurance and Data Destruction Protocol document.
2. Implement native client components for eSafety-compliant age assurance and backend automated purging scripts for raw verification data.
3. Build UI onboarding templates displaying mandatory Australian age-assurance and data-deletion disclosures.
4. Create automated CI tests to verify that under-16 Australian users cannot create accounts and that verification payloads leave no residual logs.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, regulated by Decreto n. 12.880 of 18 March 2026 and enforced by the ANPD) establishes comprehensive child and adolescent protection duties for digital platforms, operating systems, and app developers.

Enforceable from 17 March 2026, it requires accepted age-verification methods (document check, facial age estimation, CPF database validation; self-declaration is prohibited), parental/guardian authorization for minor accounts, age rating display before download, blocking of gambling/loot-box apps for minors, and immediate ringfencing/deletion of age-verification artifacts.

Official Citations: Lei n. 15.211/2025, Decreto n. 12.880 de 18 de marco de 2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy covering age verification, guardian authorization, and content rating rules.
- **Missing Documentation:**
  Developer checklists lack detailed guidance on handling Google Play Age Signals API and Apple Declared Age Range API signals specific to Brazilian user accounts.
- **Missing Code:**
  Code templates lack native CPF validation integration, facial estimation API wrappers, and guardian consent confirmation workflows required for Brazilian minor accounts.
- **Missing Disclosure:**
  Onboarding UI templates do not display required Brazilian disclosures explaining age verification mandates under Law 15,211/2025 and guardian consent requirements.
- **Missing Logging:**
  There are no backend schemas designed to log guardian authorization grants, age contestation requests, or the immediate purging of raw identity documents.
- **Missing Testing:**
  The test runner contains no automated tests to verify that loot-box features or gambling mechanics are dynamically hidden for Brazilian accounts rated under 18.
- **Missing Evidence:**
  The repository lacks document templates for ANPD Compliance Self-Assessments or proof of age-verification solution deployment.
- **Missing Audit Trail:**
  An unalterable audit trail recording age verification outcomes, guardian consent events, and raw document deletion timestamps is completely absent.

### 16.3 Remediation and Action Plan
1. Draft a comprehensive Brazil Digital ECA Operational Guidelines document.
2. Implement client code wrappers for Play Age Signals API (Brazil rollout) and native CPF/facial verification flows.
3. Build UI components for Brazilian age verification, guardian consent, and content gating for under-18 users.
4. Establish automated tests verifying that accounts under 18 are blocked from accessing loot boxes or gambling features in Brazil.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act 2023 (DPDPA), alongside the DPDP Rules 2025 (notified 13 November 2025, with phased enforcement through 13 May 2027), establishes a comprehensive data protection regime for processing digital personal data in India.

Key requirements include obtaining free, specific, informed, unconditional, and unambiguous consent with a clear consent notice in 22 official languages, verifiable parental consent for processing data of children (under 18) through government-backed mechanisms (such as DigiLocker), a complete ban on behavioral tracking and targeted advertising directed at children, and interoperability with registered Consent Managers.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an India DPDPA Data Protection Policy covering verifiable parental consent, multi-language notices, and Consent Manager integration.
- **Missing Documentation:**
  Checklists fail to provide technical guidelines for integrating with DigiLocker or registered Consent Managers under Rule 4 of the DPDP Rules 2025.
- **Missing Code:**
  Code templates lack DigiLocker verifiable parental consent API adapters, multi-language consent notice renderers, and automated flags to suppress targeted ads for under-18 users.
- **Missing Disclosure:**
  In-app consent screens do not provide standardized multi-language consent notices with itemized processing purposes and Data Protection Officer (DPO) contact details.
- **Missing Logging:**
  There are no backend database schemas designed to capture structured consent records, consent withdrawal requests, or Consent Manager API synchronization events.
- **Missing Testing:**
  The test suite contains no automated unit tests to verify that when an Indian user is flagged as under 18, all behavioral profiling and targeted ad SDKs are completely disabled.
- **Missing Evidence:**
  The repository lacks templates for a DPDPA Data Protection Impact Assessment (DPIA) or proof of Data Fiduciary registration.
- **Missing Audit Trail:**
  An immutable audit trail logging consent grants, consent withdrawals, parental consent verifications, and Data Protection Board inquiry records is absent.

### 17.3 Remediation and Action Plan
1. Publish an India DPDPA Developer Guide covering verifiable parental consent and multi-language disclosures.
2. Implement code modules for DigiLocker parental consent verification and multi-language consent UI sheets.
3. Build database logging schemas for Consent Manager interoperation and consent withdrawal execution.
4. Create automated CI tests to ensure that under-18 Indian user profiles receive complete immunity from behavioral tracking.

---

## 18. Singapore PDPA / IMDA Code of Practice for Online Safety

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA), enhanced by the IMDA Code of Practice for Online Safety for App Distribution Services (commenced March 2025, with age-assurance enforcement from 1 April 2026), regulates data protection and online safety.

The IMDA Code mandates that app distribution services and platforms implement age assurance to screen and prevent users under 18 from downloading age-inappropriate apps. Furthermore, age-assurance data must be strictly minimized and destroyed once the verification purpose is served, and data protection officers (DPO) must be designated with published contact details.

Official Citations: Personal Data Protection Act 2012 (No. 26 of 2012), IMDA Code of Practice for Online Safety (2025).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore Online Safety and Age Assurance Policy detailing IMDA Code compliance and DPO governance.
- **Missing Documentation:**
  Checklists lack developer guidance on handling Singapore 18-plus download blocks (enforced by Apple/Google from Feb/Apr 2026) and implementing credit-card/digital ID age assurance.
- **Missing Code:**
  Code templates lack wrappers for Singapore age-assurance methods and lack automated routines to delete verification data immediately following age classification.
- **Missing Disclosure:**
  In-app settings and store listing metadata lack published Data Protection Officer (DPO) contact details and clear age-rating disclosures required by IMDA.
- **Missing Logging:**
  There are no logging schemas designed to record age verification completion flags while logging the immediate purging of raw verification tokens.
- **Missing Testing:**
  The test runner lacks automated checks to verify that 18-plus rated content or features are strictly inaccessible to unverified Singapore user accounts.
- **Missing Evidence:**
  The repository lacks document templates for an IMDA Online Safety Risk Assessment or PDPA Data Protection Audit report.
- **Missing Audit Trail:**
  An unalterable audit trail logging DPO inquiries, age verification success events, and data destruction execution receipts is missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA & IMDA Online Safety Compliance Guide.
2. Implement client code helpers for Singapore age assurance and immediate verification data deletion routines.
3. Add UI components displaying DPO contact details and IMDA-compliant age disclosures.
4. Establish automated tests verifying that 18-plus features are blocked for unverified Singapore accounts.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (amended to mandate alternative in-app payment systems) and Personal Information Protection Act (PIPA, Act No. 21445, effective September 2026) impose strict operational duties on mobile applications.

For alternative payments, Apple and Google mandate specific entitlement declarations (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`), a 26% platform commission, approved local payment gateways (KCP, Inicis, Toss, NICE), a Korea-only binary build, explicit native modal disclosures, and monthly sales reporting within 15 days. PIPA adds CEO/CPO accountability, board-approved privacy officers, and heavy surcharges for privacy violations.

Official Citations: Telecommunications Business Act Art. 22-9, Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no South Korea Alternative Billing Policy or PIPA Executive Privacy Governance Policy.
- **Missing Documentation:**
  Developer guides lack detailed technical instructions on building Korea-only binaries, configuring approved Korean payment gateways, and executing monthly StoreKit external purchase reporting.
- **Missing Code:**
  The codebase templates lack native modal sheets for Korean alternative billing disclosures (`SKExternalPurchase = "KR"`) and lack server-side API clients for monthly sales reporting.
- **Missing Disclosure:**
  Payment UI templates do not include the required native disclosure modal informing Korean users of alternative billing terms and differences in platform support services.
- **Missing Logging:**
  There are no server-side database schemas or log collectors designed to log Korean alternative payment transactions for monthly report submission within the 15-day window.
- **Missing Testing:**
  No automated unit tests verify that alternative billing options are restricted exclusively to South Korea storefront binaries and never co-mingle with standard platform IAP on other storefronts.
- **Missing Evidence:**
  The repository lacks templates for monthly StoreKit external purchase sales reports, payment gateway agreements, or PIPA Chief Privacy Officer designation records.
- **Missing Audit Trail:**
  An immutable audit trail tracking monthly transaction reports submitted to Apple/Google, fee remittances, and PIPA compliance reviews is absent.

### 19.3 Remediation and Action Plan
1. Formulate a South Korea Compliance Manual covering alternative billing entitlements and PIPA executive governance.
2. Create client code components for Korean alternative billing modal sheets and server-side monthly reporting automation scripts.
3. Build database schemas to record alternative payment transactions and generate monthly platform CSV reports.
4. Create automated CI tests verifying that Korea-specific payment entitlements are active only in South Korean app builds.

---

## 20. China Mobile App Filing (MIIT ICP Extension) & CAC Regulations

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (an extension of the Internet Content Provider ICP filing system) for all applications distributed on app stores in mainland China.

Enforced strictly since March 2024, foreign developers must partner with a local Chinese entity or establish a local subsidiary to obtain an ICP filing number. Furthermore, applications must comply with the Personal Information Protection Law (PIPL), real-name identity verification rules, CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, effective July 2026, banning virtual companion services for minors), and obtain a Banhao gaming license for paid or IAP games.

Official Citations: MIIT Circular on Mobile Application Filing (2023), CAC Order No. 21 (2026), Personal Information Protection Law (PIPL).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no China Market Entry Policy covering MIIT filing, local entity partnership, PIPL data localization, or AI minor restrictions.
- **Missing Documentation:**
  Checklists fail to provide detailed, step-by-step instructions on navigating MIIT app filing workflows, App Store Connect ICP entry fields, and CAC AI minor mode requirements.
- **Missing Code:**
  Code templates lack real-name identity verification API integrations, Chinese local cloud storage adapters (for PIPL data localization), and automatic "minors mode" switches for AI chat apps.
- **Missing Disclosure:**
  App settings and store listing metadata templates lack required MIIT ICP filing number display components and PIPL-compliant Chinese privacy notices.
- **Missing Logging:**
  There are no logging schemas designed to capture real-name verification logs, AI chat content filtering logs, or minor mode activation events required by Chinese cyber authorities.
- **Missing Testing:**
  The test runner contains no automated tests to verify that AI companion or virtual kin features are completely disabled when an account is flagged as a Chinese minor.
- **Missing Evidence:**
  The repository lacks document templates for MIIT App Filing Certificates, Banhao game licensing records, or PIPL Personal Information Protection Impact Assessments.
- **Missing Audit Trail:**
  An unalterable audit trail logging MIIT filing updates, real-name authentication records, content moderation actions, and CAC compliance filings is completely absent.

### 20.3 Remediation and Action Plan
1. Draft a China Market Compliance Guide detailing MIIT filing, local partnership structures, and CAC AI minor bans.
2. Implement UI components for displaying MIIT ICP filing numbers in app footers and settings.
3. Build native code utilities for real-name identity verification and automatic minor mode switching in AI applications.
4. Establish automated CI checks verifying that Chinese builds contain valid MIIT ICP numbers and restrict minor access to companion AI features.

---

## 21. Consolidated Gap Classification Matrix Across 20 Regulations

Where the playbook already covers a framework, the cell says **Covered**. **Partial** means the rule is named with a dated source but a developer still lacks step-by-step implementation, code, or testing tools. **Missing** means the playbook does not carry it at all.

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
| **9. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China Mobile App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Summary Roadmap and Strategic Priority Order

The gap analysis demonstrates that while the repository excels at identifying store rejection guidelines and mentioning core legal frameworks in high-level documentation, significant gaps exist in the executable layer (detection code, guard rules, UI components, logging schemas, automated test runners, evidence templates, and audit trail systems).

To systematically resolve these compliance gaps across all twenty regulations, the following priority roadmap is established:

1. **Phase 1: Critical Missing Baseline (GPSR Integration)**
   - Fully integrate the EU General Product Safety Regulation (GPSR) across all repository layers, including detection patterns in `data/rejection-patterns.json`, metadata checks in `scripts/metadata-audit.py`, and UI disclosure components.

2. **Phase 2: Executable Detection & Guard Rules**
   - Expand `agent-os/hooks/app-store-compliance-guard.sh` and `data/detection-recipes.json` to scan codebases for missing withdrawal buttons (EU Directive 2023/2673), missing AI disclosures (EU AI Act Art 50), missing age-assurance hooks (US ASAA, Brazil ECA, UK OSA), and missing GPC signal handlers (California CCPA).

3. **Phase 3: Code Templates & UI Component Libraries**
   - Add reference code implementations in `references/` for `ExternalPurchaseCustomLink` (EU/KR DMA), `DeclaredAgeRange` (Apple), `Play Age Signals` (Android), BIPA written releases, frictionless cancellation buttons, and C2PA synthetic content watermarking.

4. **Phase 4: Logging Schemas & Audit Trail System**
   - Design standardized database schemas and logging utilities for law enforcement request handling (EU e-Evidence 8-hour window), parental consent receipts, age data immediate purging logs, and monthly external purchase transaction reporting.

5. **Phase 5: Automated Compliance Testing Engines**
   - Enhance repository test runners (`scripts/release-audit.py`, `scripts/accessibility-audit.py`, `scripts/metadata-audit.py`) to run automated checks verifying EN 301 549 Chapter 11 accessibility compliance, AI watermarking presence, and multi-language consent notice completeness prior to release.

---

## 23. Sources

Every regulation cited above, anchored to its official Priority 1 source:

- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Amended COPPA Rule, [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Privacy Rights Act & CPPA Regulations, [Cal. Civ. Code Sec. 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois Biometric Information Privacy Act, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US ROSCA & FTC Act Sec. 5, [15 U.S.C. 8401](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- UK Online Safety Act 2023, [2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Amendment Act 2024, [Cth Legislation](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA, [Lei n. 15.211/2025 & Decreto 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India Digital Personal Data Protection Act 2023, [Act No. 22 of 2023 & DPDP Rules 2025](https://egazette.gov.in)
- Singapore PDPA & IMDA Code of Practice for Online Safety, [IMDA Code 2025](https://www.mddi.gov.sg)
- South Korea Telecommunications Business Act & PIPA, [Act No. 21445](https://law.go.kr)
- China Mobile App Filing & CAC Order No. 21, [MIIT App Filing & CAC 2026](https://www.cac.gov.cn)
