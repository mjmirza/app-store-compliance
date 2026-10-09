# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind mobile and web app developers shipping into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global storefronts, checking honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking the historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

Developers must request and process the user's age category (via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Act No. 185, Alabama HB 161 (2026).

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
  There is no secure backend system designed to log the receipt of parental consent, consent revocations, or the immediate deletion of raw age-verification documents.
- **Missing Testing:**
  The test suites do not include automated integration tests to verify that the application blocks minor accounts from accessing premium features or completing in-app purchases in the absence of valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to prove compliance to state Attorneys General.
- **Missing Audit Trail:**
  An immutable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is entirely absent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable to application runtime, but a CLI tool or validator verifying whether a literacy log exists is missing.
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

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed so that persons are informed they are interacting with AI. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format. Article 50(4) requires deployers of deepfakes to disclose synthetic generation or manipulation.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  The codebase templates do not include helper classes or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the required immediate disclosure ("You are interacting with an AI system") at the time of the first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  The existing test runner scripts do not check for the presence of synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 (Digital Markets Act) regulates core platform services designated as gatekeepers (such as Apple's App Store and Google Play). It guarantees app developers the legal right to promote alternative payment methods, direct consumers to external web storefronts, utilize alternative app marketplaces, and access platform APIs without gatekeeper self-referencing or anti-steering restrictions.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal EU External Purchase and Alternative Distribution Policy to guide developers through entitlement declarations, StoreKit External Purchase Link entitlements, or Core Technology Commission fee reporting.
- **Missing Documentation:**
  Documentation contains overview mentions but lacks step-by-step technical guides for registering and configuring alternative app store submission pipelines or managing external link sheets.
- **Missing Code:**
  Code templates lack sample implementations for handling external purchase links, opening external link sheets safely, or validating store tokens for alternative distribution channels.
- **Missing Disclosure:**
  UI templates do not include standard required DMA external purchase disclosures informing users that they are exiting the gatekeeper payment ecosystem.
- **Missing Logging:**
  No backend logging schema is provided to track external transaction link clicks, user conversion events, or monthly CTC reporting metrics required by gatekeeper agreements.
- **Missing Testing:**
  The test suite does not include UI or unit tests verifying that external link sheets open correctly without triggering unexpected in-app purchase modals on EU storefronts.
- **Missing Evidence:**
  The repository lacks sample compliance declarations or documentation templates required when requesting Apple's `com.apple.developer.storekit.external-purchase-link` entitlement.
- **Missing Audit Trail:**
  No audit log structure exists to track entitlement request approvals, gatekeeper contract amendments, or external revenue reporting submissions.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (Digital Services Act) establishes strict obligations for online intermediary services, platforms, and marketplaces. For mobile app developers, it enforces trader status declarations (D-U-N-S verification, phone, email, bank details), notice-and-action mechanisms for illegal content, user moderation reporting, and advertising transparency.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template DSA Compliance Policy exists to assist developers in establishing notice-and-action handling, user content moderation, or trader status declarations.
- **Missing Documentation:**
  The repository lacks detailed instructions for setting up in-app content reporting mechanisms, user redress paths, or transparency disclosures for user-generated content (UGC).
- **Missing Code:**
  Frontend templates do not include functional notice-and-action report buttons, content reporting forms, or moderation queue hooks.
- **Missing Disclosure:**
  In-app UI templates lack required trader status disclosures (publishing legal entity name, address, email, phone) for apps distributing commercial goods or paid services in the EU.
- **Missing Logging:**
  No database schemas or logging modules exist to record incoming illegal content notices, moderation decisions, response timelines, or user appeals.
- **Missing Testing:**
  There are no automated tests verifying that content flagging features properly validate input, dispatch notices, or generate moderation ticket IDs.
- **Missing Evidence:**
  The playbook provides no sample DSA Annual Transparency Report templates or evidence sheets documenting moderation staffing and algorithmic parameters.
- **Missing Audit Trail:**
  An unalterable audit log for moderation actions, user suspensions, and appeal decisions is entirely absent from the codebase.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) mandates accessibility requirements for e-commerce, banking, e-books, and mobile applications across the EU. Compliant applications must meet harmonised standard EN 301 549 Chapter 11 / WCAG 2.1 Level AA accessibility standards and publish an accessible Accessibility Statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive Corporate Accessibility Policy defining organizational commitments to EN 301 549 / WCAG 2.1 AA standards and regular accessibility auditing.
- **Missing Documentation:**
  While accessibility rules are summarized, step-by-step developer implementation guidelines for screen reader support (VoiceOver / TalkBack), Dynamic Type scaling, and contrast ratios are incomplete.
- **Missing Code:**
  Codebase templates lack reusable accessible components (e.g., accessible modal dialogs, accessible touch targets, dynamic font scaling helpers, or high-contrast themes).
- **Missing Disclosure:**
  No template Accessibility Statement (conforming to EN 301 549 Annex B) is provided for inclusion in the app or store listing.
- **Missing Logging:**
  No logging mechanism exists to capture user accessibility feedback, barrier reports, or screen-reader error events.
- **Missing Testing:**
  The repository's static accessibility audit script lacks automated UI tree inspections for accessibility identifiers, color contrast ratios, or tap target size limits.
- **Missing Evidence:**
  The repository lacks physical evidence templates such as VPAT / WCAG 2.1 AA Conformance Reports or accessibility evaluation testing records.
- **Missing Audit Trail:**
  No audit trail exists to record historical accessibility audits, remediated design defects, or release-by-release accessibility regression checks.

---

## 10. US Amended COPPA Rule (16 CFR Part 312)

### 10.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) amended Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312) imposes enhanced obligations on child-directed apps and services with actual knowledge of under-13 users. Requirements include separate verifiable parental consent for third-party disclosures, strict data retention policies, mandatory written information security programs, and prohibitions on targeted advertising and nudge techniques.

Official Citation: FTC COPPA Rule, 16 CFR Part 312.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Child Data Retention & Security Policy is provided to meet the FTC's requirement for written data retention limits and security programs.
- **Missing Documentation:**
  Checklists mention COPPA generally but lack operational runbooks for integrating FTC-approved Verifiable Parental Consent (VPC) mechanisms (e.g., facial scan, credit card verification, or government ID).
- **Missing Code:**
  Mock client implementations lack VPC flows, separate opt-in logic for third-party SDK data sharing, or automatic SDK initialization blocks for under-13 users.
- **Missing Disclosure:**
  Direct Notice to Parents UI templates and child-directed Privacy Policy overlays are not included in the repository templates.
- **Missing Logging:**
  No database logging schema exists to record parent consent timestamps, method of verification, or parental consent revocation events.
- **Missing Testing:**
  Automated tests do not verify that analytics or ad SDKs are completely suppressed when a user is identified as under 13.
- **Missing Evidence:**
  The playbook lacks sample VPC verification audit records, SDK compliance assessments, or FTC safe harbor certification evidence.
- **Missing Audit Trail:**
  An immutable audit trail to document child data deletion requests, parent consent updates, and annual security reviews is absent.

---

## 11. California Privacy Rights Act (CPRA) & CPPA Regulations

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA) and implemented by the California Privacy Protection Agency (CPPA) regulations (11 CCR Title 4) governs personal data collection, processing, sale, sharing, automated decision-making (ADMT), and opt-out preferences (Global Privacy Control - GPC).

Official Citation: California Civil Code Sec. 1798.100 et seq.; 11 CCR section 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template CPRA / California Consumer Privacy Policy is provided covering sensitive personal information (SPI) limits, ADMT opt-out rules, or risk assessment protocols.
- **Missing Documentation:**
  Missing technical implementation guides for parsing `Sec-GPC` headers or mobile OS opt-out signals across native iOS and Android layers.
- **Missing Code:**
  Codebase templates lack automated handlers for Global Privacy Control (GPC) signals, "Do Not Sell or Share My Personal Information" links, or ADMT opt-out handlers.
- **Missing Disclosure:**
  In-app UI templates do not provide prominent "Do Not Sell/Share My Personal Info" or "Limit the Use of My Sensitive Personal Information" modal sheets.
- **Missing Logging:**
  No database schema is provided to log consumer rights requests (DSARs), opt-out preferences, or automated decision-making opt-out registrations.
- **Missing Testing:**
  No unit tests exist to verify that setting the GPC signal or opt-out flag disables third-party tracking scripts or ad network initialization.
- **Missing Evidence:**
  The repository lacks templates for CPPA Risk Assessments, Cybersecurity Audits, or Third-Party Data Processing Agreements (DPAs).
- **Missing Audit Trail:**
  No audit trail exists to track DSAR fulfillment timelines (45-day window), verification checks, or annual CPPA policy revisions.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14) regulates the collection, capture, purchase, receipt, storage, and handling of biometric identifiers and information (such as face scans, voiceprints, fingerprints, or iris scans). BIPA mandates written informed consent prior to collection, published retention schedules, and strict destruction protocols.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Biometric Data Information Policy or publicly available written biometric retention and destruction schedule is included in the repository.
- **Missing Documentation:**
  Missing developer guidelines explaining when local device authentication (e.g., Apple FaceID / TouchID, Android BiometricPrompt) bypasses BIPA versus when server-side biometric processing triggers statutory liability.
- **Missing Code:**
  Mock implementations do not contain BIPA-compliant consent modal sheets or explicit opt-in confirmation components prior to initializing biometric capture routines.
- **Missing Disclosure:**
  UI templates do not display explicit BIPA disclosures detailing the specific biometric identifier collected, purpose of use, and length of term for storage.
- **Missing Logging:**
  No backend logging structure exists to record written biometric consent execution, consent withdrawal, or scheduled data destruction events.
- **Missing Testing:**
  No automated tests verify that biometric SDKs or native features remain disabled until written consent flags are set to true.
- **Missing Evidence:**
  The playbook carries no sample written consent release forms or proof of biometric data destruction certificates.
- **Missing Audit Trail:**
  An immutable audit log tracking biometric consent history, retention schedule adherence, and data purge execution is missing.

---

## 13. FTC Negative Option Rule & Subscription Cancellation

### 13.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) Rule on Use of Negative Option Plans (16 CFR Part 425) and state-level automatic renewal laws (e.g., California AB 2863) mandate "Click-to-Cancel" subscription management. Businesses must provide a simple, frictionless cancellation mechanism that is at least as easy to use as the mechanism used to initiate the subscription, along with clear disclosures of auto-renewal terms prior to billing.

Official Citation: FTC 16 CFR Part 425; California Business & Professions Code Sec. 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal Negative Option and Subscription Renewal Policy governing trial conversions, auto-renewal notices, and cancellation workflows.
- **Missing Documentation:**
  Checklists mention StoreKit / Play Billing cancellation links but lack detailed design specifications for "Click-to-Cancel" single-click or two-click cancellation flows.
- **Missing Code:**
  Frontend code templates do not include self-service in-app subscription cancellation buttons, trial conversion warnings, or direct manage-subscription deep link handlers.
- **Missing Disclosure:**
  Checkout UI templates fail to display required pre-consent negative option disclosures (full price, billing frequency, cancellation deadline, auto-renewal terms) immediately adjacent to the buy button.
- **Missing Logging:**
  No database schema is provided to log negative option disclosure acceptance, pre-renewal notification delivery, or cancellation attempt logs.
- **Missing Testing:**
  Automated tests do not verify that subscription cancellation requests execute without mandatory survey blocks or multi-step retention save flows.
- **Missing Evidence:**
  The repository lacks sample negative option consent receipts or pre-renewal reminder email/push notification templates.
- **Missing Audit Trail:**
  No audit trail exists to log pre-renewal notices sent, cancellation completion timestamps, or refund processing records.

---

## 14. UK Online Safety Act 2023

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) imposes statutory duties of care on user-to-user (U2U) services and search services to protect users (especially children) from illegal content, harm, and age-inappropriate material. Regulated by Ofcom, the Act requires age assurance, illegal content risk assessments, content moderation, and child safety features.

Official Citation: Online Safety Act 2023 (c. 50).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template UK Online Safety Policy or Illegal Content Risk Assessment framework is available in the repository.
- **Missing Documentation:**
  Checklists lack operational instructions for meeting Ofcom Codes of Practice regarding highly effective age assurance, content reporting, and harmful content filtering.
- **Missing Code:**
  Codebase templates lack age assurance gating modules, child-safety privacy mode defaults (disabling direct messages and location sharing by default for minors), or illegal content reporting queues.
- **Missing Disclosure:**
  UI templates do not include clear UK-specific safety guidance disclosures, terms of service child protection summaries, or reporting transparency notices.
- **Missing Logging:**
  No backend logging schema exists to record illegal content reports, Ofcom compliance alerts, age assurance verification results, or moderation turn-around times.
- **Missing Testing:**
  Test suites lack automated test cases verifying that minor accounts default to maximum privacy and restricted messaging configurations.
- **Missing Evidence:**
  The repository lacks physical templates for Ofcom Risk Assessment Reports, Age Assurance Accuracy Audit Results, or Senior Management Compliance Statements.
- **Missing Audit Trail:**
  An unalterable audit log tracking moderation actions, child safety complaints, and Ofcom inquiry responses is missing.

---

## 15. Australia Online Safety Framework

### 15.1 Regulatory Overview and Background
Australia's Online Safety Act 2021, the App Distribution Services Online Safety Code (registered September 2025), and the Online Safety Amendment (Social Media Minimum Age) Act 2024 enforce strict age verification (16+ minimum age for covered social media), Class 1C and Class 2 material filtering, and mandatory age assurance for age-restricted applications.

Official Citation: Online Safety Act 2021; App Distribution Services Code (2025); Social Media Minimum Age Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Australia Online Safety & Minimum Age Policy is provided to guide developers on complying with eSafety Commissioner codes and minimum age restrictions.
- **Missing Documentation:**
  Checklists lack technical instructions for integrating Australian-approved age assurance systems or handling eSafety removal notices within required timelines.
- **Missing Code:**
  Code templates lack dynamic age verification gates for Australian IP ranges or age-gated account registration flows for 16+ social features.
- **Missing Disclosure:**
  In-app UI templates lack eSafety-compliant reporting disclosures or mandatory warnings regarding age restrictions for covered services.
- **Missing Logging:**
  No backend logging mechanism exists to log age verification attempts, eSafety notice receipts, or content takedown timestamps.
- **Missing Testing:**
  Test suites do not verify that Australian accounts under 16 are blocked from registering or accessing covered social features.
- **Missing Evidence:**
  The repository lacks templates for eSafety Commissioner Compliance Declarations or Age Assurance Technology Audit Evidence.
- **Missing Audit Trail:**
  No audit trail exists to record eSafety takedown notice compliance, account termination records for underage users, or code review history.

---

## 16. Brazil Digital ECA & Child Safety Framework

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto n. 12.880 (18 March 2026) establish a national age verification and digital safety framework for children and adolescents. Mobile applications must enforce age assurance (leveraging Google Play Age Signals API or Apple age-rating blocks), provide parental consent tools, disable profiling and targeted ads for minors, and adhere to strict data minimization.

Official Citation: Law No. 15,211/2025; Decree No. 12,880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Brazil Child and Adolescent Digital Safety Policy (ECA Digital) exists in the repository.
- **Missing Documentation:**
  Missing developer runbooks for integrating Brazilian age-assurance signals and configuring parental controls in compliance with Decree 12.880.
- **Missing Code:**
  Code templates lack native hooks to process Brazilian age signal payloads or dynamically suppress profiling and push notifications for minor accounts.
- **Missing Disclosure:**
  UI templates do not provide Portuguese-language ECA disclosures or parental consent notification dialogs.
- **Missing Logging:**
  No backend logging schema is provided to capture parental consent verification, ANPD compliance logs, or raw verification data deletion receipts.
- **Missing Testing:**
  Automated tests do not verify that profiling and ad tracking are disabled for accounts identified as minors in Brazil.
- **Missing Evidence:**
  The repository lacks ANPD Compliance Certificates, Age Verification Audit Data, or Parental Consent Templates in Portuguese.
- **Missing Audit Trail:**
  An immutable audit trail tracking Brazilian age signal processing and verification data purge routines is missing.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and the DPDP Rules 2025 establish a comprehensive framework for processing digital personal data. Requirements include verifiable parental consent before processing child data (under 18), mandatory appointment of a Data Protection Officer (DPO) and Consent Manager integration, multi-language notice delivery (22 scheduled languages), and strict data breach notification timelines.

Official Citation: DPDPA 2023 (Act No. 22 of 2023); DPDP Rules 2025, G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template DPDPA Compliance Policy or Verifiable Parental Consent Policy for India is provided.
- **Missing Documentation:**
  Checklists lack guidelines for integrating with MeitY-approved Consent Managers, multi-lingual notice requirements, or 72-hour Data Protection Board (DPBI) breach reporting protocols.
- **Missing Code:**
  Code templates lack multi-language notice renders (supporting Eighth Schedule languages), Consent Manager API wrappers, or child data tracking blocks.
- **Missing Disclosure:**
  UI templates do not display explicit itemized consent notices detailing data points collected, purpose, and DPO contact details in the user's preferred Indian language.
- **Missing Logging:**
  No backend schema is provided to log consent artifacts, consent withdrawal receipts, or Consent Manager API interactions.
- **Missing Testing:**
  Test suites lack automated test cases verifying that child accounts (under 18) are restricted from behavioral tracking or targeted ads.
- **Missing Evidence:**
  The repository lacks templates for DPBI Data Breach Reports, Consent Manager Integration Audits, or DPO Appointment Notices.
- **Missing Audit Trail:**
  No audit trail exists to track consent history, consent withdrawal execution, or DPBI regulatory inquiry records.

---

## 18. Singapore Personal Data Protection Act (PDPA) & Online Safety Code

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA 2012, amended 2020) and the IMDA Code of Practice for Online Safety for App Distribution Services enforce strict data protection rules, age assurance for high-risk apps, mandatory breach notification (within 3 calendar days to PDPC), and in-app safety controls for designated services.

Official Citation: PDPA 2012; IMDA Code of Practice for Online Safety (2023/2025).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Singapore PDPA & IMDA Online Safety Policy exists in the repository.
- **Missing Documentation:**
  Missing technical documentation for handling Singapore 18+ download gating, Singpass / Myinfo identity verification, or 3-day PDPC breach notification workflows.
- **Missing Code:**
  Code templates lack hooks for Singpass / Myinfo age verification, Singapore-specific content reporting buttons, or PDPC breach alert scripts.
- **Missing Disclosure:**
  In-app templates do not display PDPC-compliant Data Protection Officer (DPO) contact disclosures or explicit purpose notices prior to collection.
- **Missing Logging:**
  No logging schema exists to record Singpass verification tokens, PDPC breach alerts, or user consent logs.
- **Missing Testing:**
  No automated unit tests verify that Singapore accounts undergo required age assurance checks before downloading age-restricted content.
- **Missing Evidence:**
  The repository lacks physical templates for PDPC Data Breach Notification Forms or IMDA Online Safety Audit Declarations.
- **Missing Audit Trail:**
  An unalterable audit log tracking PDPC notification history, DPO inquiry logs, and consent registry updates is absent.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (Article 22-9, alternative in-app billing) and the Personal Information Protection Act (PIPA) amendment (Act No. 21445, 2026) enforce strict alternative in-app payment support, mandatory local agent appointment, 72-hour PIPC breach reporting, and stringent biometrics and child data protections.

Official Citation: Telecommunications Business Act Art. 22-9; PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template South Korea Compliance Policy (covering alternative billing, local agent appointment, and PIPA rules) is provided.
- **Missing Documentation:**
  Checklists lack operational steps for implementing Korea-specific alternative billing APIs, KCC fee reporting, or Korean local agent contact disclosures.
- **Missing Code:**
  Codebase templates lack South Korean alternative payment gateway handlers, local agent contact UI footers, or PIPA consent popups.
- **Missing Disclosure:**
  UI templates do not display Korean-language local agent contact details, PIPA data processing disclosures, or alternative payment service fee notices.
- **Missing Logging:**
  No logging schema exists to record alternative billing transactions, PIPC breach logs, or local agent inquiry records.
- **Missing Testing:**
  Test suites lack automated tests verifying that South Korean users can select and complete alternative payment methods without encountering store billing blocks.
- **Missing Evidence:**
  The repository lacks templates for PIPC Data Breach Notification Forms, KCC Alternative Billing Reports, or Local Agent Designation Agreements.
- **Missing Audit Trail:**
  No audit trail exists to track PIPC regulatory filings, alternative billing transaction records, or local agent communication logs.

---

## 20. China App Filing & Synthetic Automation Rules

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) App Filing Requirement (ICP extension), Cyberspace Administration of China (CAC) Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services), and Deep Synthesis Provisions mandate app filing registration, real-name identity verification, watermarking of AI-generated content, and human safety moderation.

Official Citation: MIIT Notice on App Filing (2023); CAC Order No. 21 (2025/2026); CAC Deep Synthesis Provisions.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template China App Filing & CAC AI Safety Compliance Policy is available in the repository.
- **Missing Documentation:**
  Checklists lack detailed instructions for completing MIIT app filing, integrating real-name verification, or embedding CAC-compliant invisible watermarks in AI output.
- **Missing Code:**
  Code templates lack real-name identity verification hooks, MIIT filing number footer displays, or CAC AI watermark injectors.
- **Missing Disclosure:**
  UI templates do not display the MIIT ICP filing number on splash screens or disclose anthropomorphic AI interaction in accordance with CAC Order No. 21.
- **Missing Logging:**
  No logging schema exists to record real-name verification tokens, CAC AI safety filtering logs, or MIIT regulatory compliance checks.
- **Missing Testing:**
  Test suites do not verify that China storefront builds fail if the MIIT filing display or real-name verification module is omitted.
- **Missing Evidence:**
  The repository lacks templates for MIIT App Filing Certificates, CAC Security Assessment Reports, or Real-Name Verification Audit Logs.
- **Missing Audit Trail:**
  An immutable audit log tracking real-name verification events, CAC content moderation blocks, and MIIT update filings is absent.

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
| **9. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA / CPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. FTC Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Most frameworks are named in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`, with dated sources and deadline entries. What they lack across the board is the implementation layer: automated detection rules in the guard, UI and backend code templates, testing scripts, physical evidence templates, and unalterable audit trail logging schemas. GPSR is the primary framework completely absent end to end.

---

## 22. Conclusion and Remediation Roadmap

The playbook is strong on store rejection rules and legal deadline tracking, but thinner on the operational code, logging, testing, evidence, and audit trail artifacts required for live app compliance.

Priority remediation sequence:

1. Add GPSR rules, detection patterns, and checklists to eliminate the complete end-to-end gap.
2. Expand `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh` to include automated detection rules for all 20 frameworks across code and metadata.
3. Add functional UI and backend code templates for key 2026 requirements, starting with the EU AI Act Article 50 watermarking/disclosure tools, the EU Contract Withdrawal Button, FTC Click-to-Cancel workflows, and age signal handlers.
4. Supply standardized schema templates for compliance logging, verifiable parental consent evidence, accessibilityVPAT reports, and audit trail generation.

This report is a living snapshot. It must be regularly validated against EUR-Lex, FTC, Ofcom, ANPD, and official government publications.

---

## 23. Official Primary Sources

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing / Contract Withdrawal: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act (DMA): [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act (DSA): [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act (EAA): [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US FTC COPPA Rule: [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- US FTC Negative Option Rule: [16 CFR Part 425](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)
- California CPRA / CPPA Regulations: [11 CCR Section 7000 et seq.](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023: [Legislation.gov.uk c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Online Safety Act: [Federal Register of Legislation](https://www.legislation.gov.au/Details/C2021A00076)
- Brazil Digital ECA (Law 15,211/2025): Official Gazette of Brazil
- India DPDPA 2023: [Gazette of India Egazette](https://egazette.gov.in)
- Singapore PDPA: [PDPC Singapore Guidance](https://www.pdpc.gov.sg)
