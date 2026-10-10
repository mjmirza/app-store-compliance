# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself against modern global regulatory frameworks. It takes twenty key regulations that bind app developers shipping into the EU, US, UK, APAC, LatAm, and other major global jurisdictions, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere to the strict source trust hierarchy:
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
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements. Additionally, mock user interfaces and templates in this repository do not contain code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
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

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977 / Act 185, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates, while deleting age verification data immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

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

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations with no headcount carve-out, taking effect on 2 February 2025.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  While Article 4 binds people rather than code, a validation helper or script that checks whether an AI literacy log exists and is current is missing.
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

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons inform users that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deployers of deepfakes to disclose synthetic creation.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes, middle-tier layers, or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the required immediate disclosure ("You are interacting with an AI system") at the time of the first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  Existing test runner scripts do not check for the presence of synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms and establishes new rights for developers distributing apps in the European Union, including alternative app marketplaces, web distribution, and external payment links.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template guides developers on choosing between App Store distribution, Web Distribution, or Alternative App Marketplaces under the EU unified terms (Attachment 14).
- **Missing Documentation:**
  Lacks step-by-step documentation detailing how to configure alternative payment entitlement addendums and calculate Core Technology Commission (CTC) reporting obligations.
- **Missing Code:**
  Missing client-side helper implementations for triggering `ExternalPurchaseCustomLink` system disclosure sheets or handling alternative payment gateways on iOS.
- **Missing Disclosure:**
  UI templates do not include mandatory customer disclosures informing users when transactions occur outside Apple's In-App Purchase ecosystem.
- **Missing Logging:**
  No database schema or reporting script is provided to automate monthly transaction reporting via Apple's External Purchase Server API.
- **Missing Testing:**
  No automated unit or UI tests verify that StoreKit IAP and external offer links are never co-mingled on the same EU storefront instance.
- **Missing Evidence:**
  Missing template proof of acceptance for Attachment 14 of the ADPLA or documentation of standby letters of credit for alternative marketplace operators.
- **Missing Audit Trail:**
  No audit trail system tracks monthly transaction submissions, reporting adjustments, or entitlement status updates for EU storefronts.

---

## 8. EU Digital Services Act (DSA) Trader Status

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065), Articles 30 and 31, requires online marketplaces (including the App Store and Google Play) to verify and display trader status and contact details for all commercial developers distributing apps in the EU.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No organizational policy or decision tree exists to help developers accurately classify whether they operate as a "Trader" or "Non-Trader" under EU law.
- **Missing Documentation:**
  Documentation lacks detailed guides on App Store Connect and Google Play Console DSA submission workflows and verification steps.
- **Missing Code:**
  No automated static check exists in the guard script to verify that DSA trader verification fields (D-U-N-S, phone, email) are declared prior to submission.
- **Missing Disclosure:**
  Public documentation fails to detail required product page disclosures (trader address, phone number, email) displayed to EU consumers.
- **Missing Logging:**
  No logging mechanism records annual reviews of published trader information or changes to registered corporate addresses and contacts.
- **Missing Testing:**
  No test runner verifies that app metadata files contain valid DSA trader contact strings before triggering release builds.
- **Missing Evidence:**
  Missing templates for storing official proof of trader verification, such as D-U-N-S registration certificates and government ID uploads.
- **Missing Audit Trail:**
  Lacks an immutable audit log recording when DSA declarations were submitted, verified, or updated across store developer accounts.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) entered into force with full applicability starting 28 June 2025. It mandates accessibility for e-commerce, banking, transport, and digital services reaching EU consumers, enforcing harmonised standard EN 301 549 (WCAG 2.1 Level AA).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate Accessibility Policy template exists to govern EN 301 549 Chapter 11 mobile software compliance.
- **Missing Documentation:**
  While accessibility is mentioned, guidelines do not explicitly address EN 301 549 Annex B/C Accessibility Statement requirements.
- **Missing Code:**
  Static analysis tools in `scripts/accessibility-audit.py` cover basic WCAG checks but lack automated checks for non-web mobile software requirements under EN 301 549 Chapter 11.
- **Missing Disclosure:**
  Repository UI templates do not include an in-app, accessible Accessibility Statement or feedback mechanism.
- **Missing Logging:**
  No logging system captures user accessibility feedback, barrier reports, or remediation timelines.
- **Missing Testing:**
  Automated test scripts do not evaluate screen reader traits, Dynamic Type reflow, or high contrast mode across both iOS and Android simultaneously.
- **Missing Evidence:**
  Missing standardized Accessibility Conformance Reports (VPAT / EN 301 549 ACR) to prove compliance during regulatory audits.
- **Missing Audit Trail:**
  No audit trail records historical accessibility audits, regression fixes, or annual accessibility statement updates.

---

## 10. US Amended COPPA Rule

### 10.1 Regulatory Overview and Background
The FTC Amended Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312) expands child privacy protections by adding biometric identifiers to PII, requiring separate opt-in consent for third-party disclosures/ads, and mandating written retention and security programs, with general compliance starting 22 April 2026.

Official Citation: 16 CFR Part 312, 90 FR 16918.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Child Data Retention Policy or Information Security Program template exists in accordance with 16 CFR 312.8 and 312.10.
- **Missing Documentation:**
  Checklists do not provide technical guides for implementing separate opt-in consent flows for third-party data disclosure versus core app functionality.
- **Missing Code:**
  Mock codebases do not include verifiable parental consent method implementations (such as knowledge-based authentication or ID match) or biometric data filtering.
- **Missing Disclosure:**
  Onboarding UI templates lack updated COPPA direct notices to parents specifying newly covered personal information categories (e.g. biometric data).
- **Missing Logging:**
  No secure backend schema exists to log verifiable parental consent grants, opt-in consent for third-party sharing, or automatic data deletion timestamps.
- **Missing Testing:**
  No automated integration tests verify that third-party ad SDKs remain completely uninitialized when parental consent for targeted advertising is withheld.
- **Missing Evidence:**
  Missing physical templates of written Information Security Programs (WISP), annual risk assessments, or COPPA Safe Harbor audit certificates.
- **Missing Audit Trail:**
  Lacks an immutable audit log recording parental consent requests, parental opt-out revocations, and data deletion events under 16 CFR Part 312.

---

## 11. California Privacy (CCPA / CPRA & ADMT)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended by the CPRA (11 CCR section 7000 et seq.) establishes privacy rights including opt-out of sale/sharing, sensitive personal information limits, Global Privacy Control (GPC) support, and Automated Decision-Making Technology (ADMT) notice and opt-out requirements starting 2027.

Official Citation: California Civil Code Title 1.81.5 and 11 CCR section 7200 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template covers California ADMT opt-out procedures or sensitive personal information processing limits.
- **Missing Documentation:**
  Checklists lack step-by-step developer instructions for detecting and honoring `Sec-GPC` signals within native webviews and mobile network layers.
- **Missing Code:**
  Codebase templates do not contain middleware to parse GPC headers or programmatically restrict data sharing upon detecting a GPC signal.
- **Missing Disclosure:**
  In-app privacy notices lack explicit disclosures regarding ADMT processing logic or "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:**
  No logging backend records consumer privacy requests (know, delete, correct, opt-out) or measures response fulfillment within statutory timelines.
- **Missing Testing:**
  No automated tests simulate GPC header injections to confirm that tracking SDKs automatically disable data collection upon signal detection.
- **Missing Evidence:**
  Missing templates for CPRA Risk Assessments or Cybersecurity Audit reports required for high-revenue or high-risk data processors.
- **Missing Audit Trail:**
  No tamper-proof audit trail tracks consumer opt-out history, GPC signal recognitions, or annual privacy policy revisions.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) regulates the collection, use, safeguarding, handling, and destruction of biometric identifiers and information, requiring written notice, opt-in release, and a public retention schedule.

Official Citation: 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a written Biometric Data Retention and Destruction Policy template satisfying 740 ILCS 14/15(a).
- **Missing Documentation:**
  No developer guide exists explaining how to handle native biometrics (Face ID, Touch ID, BiometricPrompt) without capturing raw biometric identifiers on servers.
- **Missing Code:**
  Mock code templates lack explicit written consent modal components or client-side biometric release flows required before biometric authentication setup.
- **Missing Disclosure:**
  UI templates do not display required BIPA notices detailing the specific purpose and length of term for which biometric data is stored.
- **Missing Logging:**
  No backend system logs the exact timestamp and version of the biometric consent agreement signed by the user prior to feature activation.
- **Missing Testing:**
  Test suites lack automated checks to verify that biometric features remain completely inaccessible until written release consent is granted.
- **Missing Evidence:**
  Missing sample copies of publicly accessible biometric retention schedules and destruction guidelines.
- **Missing Audit Trail:**
  Lacks an immutable audit trail recording user consent receipts, biometric data destruction confirmations, and annual policy reviews.

---

## 13. US Subscription Cancellation (ROSCA & State Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative-option laws (California, New York, Massachusetts) require that online subscription cancellation must be at least as simple as the sign-up mechanism.

Official Citation: 15 U.S.C. 8401 et seq. and state statutes.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Subscription Cancellation Policy exists to govern web-billed or non-IAP subscription cancellation flows.
- **Missing Documentation:**
  Checklists lack explicit design requirements specifying maximum step counts, prohibited friction patterns, and online cancellation path standards.
- **Missing Code:**
  Codebase templates do not provide a self-service, single-click subscription cancellation component for web or account management portals.
- **Missing Disclosure:**
  Subscription paywall templates do not clearly disclose auto-renewal terms, recurring billing frequencies, or direct cancellation steps adjacent to purchase buttons.
- **Missing Logging:**
  No logging schema records cancellation request initiation timestamps, completion confirmations, or post-cancellation refund processing.
- **Missing Testing:**
  No automated UI tests confirm that cancellation can be completed in an equal or fewer number of steps compared to onboarding.
- **Missing Evidence:**
  Missing template cancellation confirmation receipts and proof of pre-renewal notification delivery.
- **Missing Audit Trail:**
  Lacks an unalterable audit log tracking subscription lifecycles, cancellation requests, and user retention offer interactions.

---

## 14. UK Online Safety Act (OSA) & Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and the ICO Age Appropriate Design Code (Children's Code) mandate age assurance (facial age estimation, credit card, open banking), high privacy by default, profiling off by default, and child safety protection for UK users under 18.

Official Citations: Online Safety Act 2023 c. 50 and ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Online Safety Policy or Child Safety Risk Assessment policy exists for UK-facing applications.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for completing mandatory Data Protection Impact Assessments (DPIA) under the ICO Children's Code.
- **Missing Code:**
  Code templates do not include native integrations for Highly Effective Age Assurance (HEAA) mechanisms or automated high-privacy default toggles for minor accounts.
- **Missing Disclosure:**
  UI templates lack child-appropriate explanations regarding how personal data is processed, presented in clear, age-tailored language.
- **Missing Logging:**
  No logging infrastructure captures age assurance verification outcomes, child safety report intakes, or illegal content removal actions within statutory timelines.
- **Missing Testing:**
  No automated tests verify that geolocation, profiling, and targeted push notifications are disabled by default when a UK child account is detected.
- **Missing Evidence:**
  Missing completed templates of Ofcom Illegal Content Risk Assessments or ICO Children's Code DPIAs.
- **Missing Audit Trail:**
  No immutable audit trail records age assurance verification results, child safety moderation decisions, or CSEA report filings with the NCA.

---

## 15. Australia Online Safety & ADS Code

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 and the App Distribution Services (ADS) Online Safety Code require age assurance to prevent under-16 access to social media platforms and restrict under-18 access to adult apps.

Official Citations: Online Safety Amendment Act 2024 and ADS Code (Schedule 7).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Age-Restricted Access Policy exists to govern Australian social media and age-sensitive app distribution requirements.
- **Missing Documentation:**
  Checklists lack developer operational guides for implementing multi-method age assurance waterfalls accepted by eSafety.
- **Missing Code:**
  Mock codebases do not integrate client-side age verification workflows or auto-restrict under-16 account creation for social media applications.
- **Missing Disclosure:**
  UI onboarding templates lack mandatory Australian legal notices explaining why age assurance is performed and how age data is protected.
- **Missing Logging:**
  No logging system captures age verification completion without storing raw age verification documents, adhering to strict data destruction duties.
- **Missing Testing:**
  No automated tests verify that raw identity documents used during Australian age assurance are destroyed immediately following verification.
- **Missing Evidence:**
  Missing templates of mandatory eSafety Industry Code Risk Assessments or proof of age data destruction protocols.
- **Missing Audit Trail:**
  Lacks an immutable audit trail tracking age verification events, age data destruction confirmations, and annual compliance reviews submitted to eSafety.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto n. 12.880 mandate accepted age verification methods (document, facial age estimation, CPF check), prohibiting self-declaration checkboxes, while requiring OS/store age signals and guardian authorization starting 2026.

Official Citations: Law 15,211/2025 and Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Brazilian Minor Protection Policy template exists detailing ANPD-approved age verification and guardian consent procedures.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides for querying Google Play Age Signals API and Apple Declared Age Range API for Brazilian users.
- **Missing Code:**
  Codebase templates do not contain client-side handlers to parse Brazilian age signal payloads or disable self-declaration checkboxes dynamically.
- **Missing Disclosure:**
  UI templates do not display required Brazilian notices explaining age rating classifications, guardian authorization steps, or contestation paths.
- **Missing Logging:**
  No logging infrastructure captures guardian consent grants, age rating contestation requests, or immediate raw verification data deletions.
- **Missing Testing:**
  No automated integration tests verify that self-declaration age checkboxes are completely blocked and replaced by verified signals when the locale is set to Brazil.
- **Missing Evidence:**
  Missing templates for ANPD Age Assurance Compliance Reports or official proof of ANPD-approved verification method implementation.
- **Missing Audit Trail:**
  Lacks an unalterable audit log recording Brazilian age verification transactions, guardian approvals, and age signal API updates.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 mandate verifiable parental consent through government-backed systems (DigiLocker) for users under 18, prohibiting behavioral tracking and targeted advertising to children.

Official Citations: DPDPA 2023 and DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Child Data Processing Policy exists to govern under-18 data handling and Consent Manager interoperability in India.
- **Missing Documentation:**
  Checklists lack technical integration manuals for connecting with DigiLocker or registered Consent Managers under Rule 4.
- **Missing Code:**
  Mock codebases do not include API handlers or consent gateways to interface with Indian registered Consent Managers or verifiable parental consent APIs.
- **Missing Disclosure:**
  Onboarding UI templates lack multilingual consent notices (available in 22 scheduled languages) required under DPDPA Section 5.
- **Missing Logging:**
  No backend schema logs parental consent artifacts from DigiLocker or tracks data principal consent withdrawal notices.
- **Missing Testing:**
  No automated tests verify that tracking SDKs, ad networks, and behavioral profiling features are disabled for Indian accounts flagged under 18.
- **Missing Evidence:**
  Missing sample templates for Data Protection Impact Assessments (DPIA) required for Significant Data Fiduciaries under DPDPA.
- **Missing Audit Trail:**
  No tamper-proof audit log records consent manager interactions, parental consent receipts, or data erasure requests.

---

## 18. Singapore PDPA & IMDA Online Safety

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and IMDA Code of Practice for Online Safety require app-store age assurance (screening under-18s from downloading age-inappropriate apps) and strict data minimization, with age data destroyed after verification.

Official Citations: Personal Data Protection Act 2012 and IMDA Code of Practice.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written Singapore Age Assurance & Data Protection Policy template exists for mobile applications distributing in Singapore.
- **Missing Documentation:**
  Checklists do not provide detailed guidelines on handling Apple's 18-plus download block or IMDA age-screening compliance for Singapore users.
- **Missing Code:**
  Codebase templates lack runtime helpers to restrict app access or verify age status before rendering age-inappropriate content to Singapore users.
- **Missing Disclosure:**
  UI templates do not include Singapore-specific data protection notices explaining that age verification data is collected solely for screening and immediately deleted.
- **Missing Logging:**
  No secure backend schema logs age check status confirmations while verifying immediate destruction of underlying identity attributes.
- **Missing Testing:**
  No automated tests confirm that 18-plus gated features are blocked for Singapore accounts until age assurance signals are verified.
- **Missing Evidence:**
  Missing templates for Singapore PDPC Data Protection Impact Assessments or age data destruction logs.
- **Missing Audit Trail:**
  Lacks an immutable audit log recording age screening checks, Data Protection Officer (DPO) designations, and data breach notification events to PDPC.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options (26% commission cap, specific StoreKit entitlement, reporting), while amended PIPA enforces CEO accountability, board-approved CPO requirements, and strict consent rules.

Official Citations: Telecommunications Business Act Article 22-9 and PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written South Korea Payment & Privacy Compliance Policy template exists for developers utilizing alternative in-app billing or processing Korean personal data.
- **Missing Documentation:**
  Checklists lack step-by-step developer manuals for building Korea-specific app binaries using the `com.apple.developer.storekit.external-purchase` entitlement (`SKExternalPurchase = "KR"`).
- **Missing Code:**
  Mock codebases do not include the required native modal disclosure sheet or API integration for approved Korean payment gateways (KCP, Inicis, Toss, NICE).
- **Missing Disclosure:**
  UI templates do not display mandatory Korean pre-payment modal disclosures informing users that Apple/Google purchase protections do not apply.
- **Missing Logging:**
  No database schema or script automates monthly sales reporting to Apple within 15 calendar days or calculates 26% commission remittances.
- **Missing Testing:**
  No automated integration tests confirm that Korean alternative payment binaries do not co-mingle Apple IAP and alternative billing on the same Korean storefront.
- **Missing Evidence:**
  Missing templates for Board-Approved Chief Privacy Officer (CPO) designation documents or official payment gateway agreements.
- **Missing Audit Trail:**
  Lacks an unalterable audit log tracking monthly Korean transaction reports, commission payments, and PIPA personal information access logs.

---

## 20. China Mobile App Filing & CAC AI Rules

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) through a local Chinese entity/partner, alongside CAC Interim Measures for AI Anthropomorphic Interactive Services (banning minor companion chatbots) and PIPL privacy rules.

Official Citations: MIIT App Filing Notice 2023 and CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written China Regulatory & AI Safety Policy template exists to govern MIIT app filing, local partnership arrangements, and minor mode restrictions.
- **Missing Documentation:**
  Checklists lack detailed developer guides for completing MIIT ICP filing, real-name verification, and CAC AI service registration.
- **Missing Code:**
  Mock codebases lack automated handlers to detect Chinese minor users and force-switch them into "Minors Mode", blocking virtual companion features.
- **Missing Disclosure:**
  UI templates do not include MIIT ICP filing number displays in app settings or CAC-mandated minor mode disclosures.
- **Missing Logging:**
  No logging infrastructure captures real-name verification statuses, minor mode activations, or illegal content filtering logs under PIPL/CAC rules.
- **Missing Testing:**
  No automated tests verify that AI companion or chat features are completely disabled when the user is located in China or identified as a minor.
- **Missing Evidence:**
  Missing sample templates for Chinese MIIT App Filing approvals, Banhao game licenses, or PIPL Personal Information Protection Impact Assessments.
- **Missing Audit Trail:**
  Lacks an immutable audit trail recording real-name registration checks, CAC security assessment filings, and minor mode session logs.

---

## 21. Consolidated Gap Classification Matrix

The matrix below consolidates the audit status across all twenty audited global regulatory frameworks against the eight mandatory compliance gap categories.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act (EAA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA/CPRA/ADMT)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation (ROSCA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act (OSA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety & ADS Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China Mobile App Filing & CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Roadmap

This audit demonstrates that while the repository provides detailed analytical and deadline coverage for twenty major global regulatory frameworks, significant operational gaps remain across code, logging, testing, evidence, and audit trails.

### Recommended Implementation Roadmap:
1. **Core Code & Guard Integration:** Add static detection patterns in `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh` for all twenty frameworks.
2. **UI & Code Templates:** Provide reusable UI components for EU withdrawal buttons, AI Article 50 disclosures, BIPA consent modals, and South Korea alternative payment sheets.
3. **Automated Testing Suite:** Develop dedicated integration scripts to test GPC headers, age signal API parsers, synthetic media watermarks, and accessibility EN 301 549 rules.
4. **Audit Trail & Evidence Templates:** Create standardized markdown and JSON schemas for WISP documents, DPIA records, AI literacy logs, and law enforcement request audit trails.

---

## 23. Official Primary Citations

- **GPSR:** [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **e-Evidence:** [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **Withdrawal Button:** [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **EU AI Act:** [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **EU DMA:** [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **EU DSA:** [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **EAA:** [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **COPPA Rule:** [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **California CCPA/CPRA:** [California Civil Code Title 1.81.5](https://oag.ca.gov/privacy/ccpa)
- **Illinois BIPA:** [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- **ROSCA:** [15 U.S.C. 8401](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- **UK OSA:** [Online Safety Act 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- **Australia Social Media Age Act:** [Online Safety Amendment Act 2024](https://www.legislation.gov.au/Details/C2024A00115)
- **Brazil Digital ECA:** [Law 15,211/2025](https://www.planalto.gov.br/) and [Decreto 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- **India DPDPA:** [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- **Singapore PDPA:** [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- **South Korea TBA & PIPA:** [Telecommunications Business Act](https://law.go.kr) and [PIPA Act No. 21445](https://law.go.kr)
- **China App Filing:** [MIIT Mobile App Filing Notice 2023](https://www.miit.gov.cn/)
