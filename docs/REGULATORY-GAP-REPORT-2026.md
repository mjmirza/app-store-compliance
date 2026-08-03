# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind app developers shipping into the EU, the US, and other worldwide markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts concluded by electronic means.

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
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking the historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

Developers must request and process the user's age category and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in the repository lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although the rejection patterns contain entries for state-level laws, the mock client implementations in the codebase do not integrate with DeclaredAgeRange or the Play Age Signals library to restrict app access dynamically.
- **Missing Disclosure:**
  The in-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log the receipt of parental consent, consent revocations, or the immediate deletion of raw age-verification documents.
- **Missing Testing:**
  The test suites do not include automated integration tests to verify that the application blocks minor accounts from accessing premium features or completing in-app purchases in the absence of valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to prove compliance.
- **Missing Audit Trail:**
  An immutable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is entirely absent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with the technical complexity and impact of the AI integration.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable, since Article 4 binds people rather than code. However, a small automated check to verify whether a valid training log exists and has been updated within the current calendar year is missing.
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

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026. This framework is a critical release blocker for any application incorporating artificial intelligence that reaches users in the European Union.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that those persons are informed that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  The checklists in the repository mention Article 50 but lack detailed, technical, developer-facing instructions on how to implement machine-readable watermarking or deepfake disclosures.
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

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The Digital Markets Act (DMA), Regulation (EU) 2022/1925, was adopted to ensure contestable and fair markets in the digital sector. It places obligations on gatekeepers, leading to Apple's restructurings in the EU including alternative app marketplaces, alternative browser engines, and external communication links.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no model policies or decision matrices to guide developers in assessing alternative distribution channels, alternative payment gateways, or evaluating Apple's alternative terms versus standard terms.
- **Missing Documentation:**
  The repository lacks step-by-step documentation on how to implement alternative browser engines or contactless payment (HCE) features, or how to handle monthly transaction reporting to Apple.
- **Missing Code:**
  There are no static checks in the automated compliance guard to flag co-mingling of alternative external purchase links and standard StoreKit IAP within the same storefront.
- **Missing Disclosure:**
  No client-side UI templates are provided for displaying system-provided external payment disclosures or warning sheets when launching alternative checkout options.
- **Missing Logging:**
  No backend database schemas or reporting mechanisms are provided to track alternative-payment transactions or automate monthly report compilation for the External Purchase Server API.
- **Missing Testing:**
  The automated testing scripts do not simulate alternative payment routes or verify correct entitlement gating on EU storefronts.
- **Missing Evidence:**
  No templates are supplied representing compliant monthly transaction summaries or proof of notarization files.
- **Missing Audit Trail:**
  An unalterable history recording alternative terms acceptance, monthly sales submissions, and entitlement status is absent.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes a modern legal framework for online intermediaries. This includes verifying and publishing trader contact information on digital marketplaces like the App Store and Google Play.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks written policies or guidelines to help developers determine whether they qualify as "traders" under the DSA, or how to verify organizational D-U-N-S details.
- **Missing Documentation:**
  No instructions are provided showing how to complete the mandatory App Store Connect or Google Play Console trader compliance forms.
- **Missing Code:**
  No automated lints or guard checks exist to flag a missing or uncompleted trader declaration as an immediate storefront removal risk.
- **Missing Disclosure:**
  Storefront and public-facing metadata templates do not include placeholder sections to display published address, phone, and verified email details.
- **Missing Logging:**
  No schemas exist to track 2FA verification codes, trader registration status, or documentation upload logs.
- **Missing Testing:**
  The test suites do not evaluate whether a "not a trader" declaration displays appropriate consumer warnings to EU users.
- **Missing Evidence:**
  The playbook fails to include templates representing verified registration documentation or certification of EU-law compliance.
- **Missing Audit Trail:**
  No unalterable record tracks historical changes to the trader status, 2FA credentials, or storefront listing metadata.

---

## 9. European Accessibility Act (EAA) / EN 301 549

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, became applicable on 28 June 2025. It mandates strict digital accessibility for mobile applications and websites offering retail, banking, and travel services. The standard is EN 301 549, which incorporates WCAG 2.1 Level AA.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an enterprise-level Accessibility Policy adopting EN 301 549 Chapter 11, including criteria for evaluating microenterprise exemptions.
- **Missing Documentation:**
  No detailed guides exist outlining how EN 301 549 Chapter 11 mobile software requirements differ from basic WCAG 2.1 AA web guidelines.
- **Missing Code:**
  The accessibility scanner checks general elements but lacks specific checks to verify advanced properties required by EN 301 549, such as screen-reader focus hierarchies, keyboard commands, or physical switch controls.
- **Missing Disclosure:**
  The repository does not supply a compliant, reachable Accessibility Statement template as required under EAA transposition laws.
- **Missing Logging:**
  No database schemas are provided to log accessibility audits, user contrast preferences, or accessibility-related consumer complaints.
- **Missing Testing:**
  The automated testing scripts do not execute dedicated compliance checks for EN 301 549 Chapter 11 parameters on mobile codebases.
- **Missing Evidence:**
  There are no templates for a Voluntary Product Accessibility Template (VPAT) or EAA conformance report.
- **Missing Audit Trail:**
  An immutable audit trail tracking the history of accessibility compliance reviews, statement updates, and regression tests is missing.

---

## 10. US COPPA and Amended COPPA Rule 2025/2026

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6508, protects children under 13. The FTC Amended COPPA Rule (90 FR 16918) expands personal information to cover biometric identifiers, restricts ad-targeting, and mandates written information security and retention programs.

Official Citation: 15 U.S.C. 6501-6508 & 16 CFR Part 312 (Amended 2025).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template COPPA-compliant privacy policies, written data retention policies, or a written information security program as required under Section 312.8.
- **Missing Documentation:**
  The repository lacks developer guidelines explaining the updated 2025/2026 verifiable parental consent (VPC) methods (e.g., face-match or knowledge-based checks).
- **Missing Code:**
  No code examples are provided for parental gates, biometric data filtering flags, or separate ad-tracking opt-in consent mechanisms.
- **Missing Disclosure:**
  UI onboarding flows do not display separate, independent disclosures for targeted advertising or third-party data collection.
- **Missing Logging:**
  No backend database schemas are provided to log verifiable parental consent, consent revocations, or data-purging events.
- **Missing Testing:**
  No automated unit or integration tests exist to confirm that child-directed sections completely block tracking or advertising SDKs.
- **Missing Evidence:**
  The repository contains no templates for annual Children's Privacy Risk Assessments or parent agreement forms.
- **Missing Audit Trail:**
  An unalterable audit trail recording privacy policy updates, security program reviews, and parental consent logs is absent.

---

## 11. California and US State Privacy Laws

### 11.1 Regulatory Overview and Background
US State Privacy Laws (such as California's CCPA/CPRA, Virginia's VCDPA, and Texas's TDPSA) require developers to respect consumer rights and honor Global Privacy Control (GPC) opt-out signals.

Official Citations: California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA); California AB 2273.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks CCPA/CPRA-compliant privacy policy templates, "notice at collection" templates, or specific state privacy policy addenda.
- **Missing Documentation:**
  No instructions are provided on how to integrate and process Global Privacy Control (GPC) signals inside embedded WebViews or native apps.
- **Missing Code:**
  The repository lacks helper code to capture `Sec-GPC` headers or conditionally suppress third-party analytic and tracking SDKs based on user opt-out signals.
- **Missing Disclosure:**
  UI templates are missing the mandatory "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:**
  No logging schemas exist to track consumer rights requests, verification results, or active opt-out states.
- **Missing Testing:**
  The test suites do not simulate GPC header injection to verify that ad-tracking is dynamically suppressed.
- **Missing Evidence:**
  No templates exist for Data Protection Impact Assessments (DPIAs) required for high-risk data processing.
- **Missing Audit Trail:**
  An immutable record system to log consumer request resolution histories, opt-out preferences, and policy changes is missing.

---

## 12. Illinois BIPA and Biometric Regulations

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA) and similar laws (Texas CUBI, Washington MHMDA) place strict rules on collecting and processing biometric identifiers.

Official Citations: 740 ILCS 14 (Illinois BIPA) & Texas Business & Commerce Code Section 503.001 (CUBI).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template biometric privacy policies, written consent release forms, or public retention and destruction schedules.
- **Missing Documentation:**
  No detailed developer guides explain how to isolate and manage biometric data templates or adhere to the strict statutory destruction timelines.
- **Missing Code:**
  The repository contains no code examples or helper classes showing how to encrypt, handle, or purge raw biometric data distinct from standard device-level FaceID.
- **Missing Disclosure:**
  UI templates lack compliant onboarding warning panels and written consent/release checkboxes for biometric collection.
- **Missing Logging:**
  No backend database schemas exist to record the receipt of written biometric releases or the execution of data destruction events.
- **Missing Testing:**
  The test suites do not programmatically check that biometric features remain disabled until a valid consent-release state is logged.
- **Missing Evidence:**
  The playbook fails to supply templates for independent security assessments of biometric storage or biometric destruction certificates.
- **Missing Audit Trail:**
  An unalterable history tracking biometric consent receipts, policy changes, and destruction actions is absent.

---

## 13. US Subscription Cancellation

### 13.1 Regulatory Overview and Background
Despite the federal Negative Option Rule amendment being vacated in 2025, the FTC continues to enforce easy subscription cancellation under Section 5 and ROSCA. Major states (California, New York, Massachusetts) maintain strict negative-option statutes requiring cancellation to be as easy as sign-up.

Official Citations: FTC Act Section 5, Restore Online Shoppers' Confidence Act (ROSCA), California Business and Professions Code Section 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template negative-option subscription policies or cancellation guidelines.
- **Missing Documentation:**
  The repository lacks design checklists for self-service in-app cancellation (such as matching step-count and prominence to the signup flow).
- **Missing Code:**
  No mock codes or templates demonstrate an in-app "Click to Cancel" button or a self-service cancellation path for alternative-billed subscriptions.
- **Missing Disclosure:**
  Pre-purchase subscription interfaces do not prominently disclose billing periods, auto-renewal terms, or cancellation instructions.
- **Missing Logging:**
  No logging schemas exist to capture cancellation events, reasons, timestamps, or confirmation triggers.
- **Missing Testing:**
  The test suites do not verify that subscription cancellation can be completed in a self-service manner without administrative blocks.
- **Missing Evidence:**
  The repository is missing templates representing cancellation confirmation receipts, customer service scripts, or compliance audits.
- **Missing Audit Trail:**
  An immutable history tracking cancellation interface modifications, paywall updates, and compliance audits is absent.

---

## 14. UK Online Safety Act & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 requires platforms to use highly effective age assurance to protect children. The ICO Children's Code sets 15 standards for services likely to be accessed by under-18s, requiring high privacy, disabled geolocation, and disabled profiling by default.

Official Citations: UK Online Safety Act 2023 & ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template UK child safety policies, online safety compliance program frameworks, or age-assurance guides.
- **Missing Documentation:**
  No documentation exists explaining how to complete an ICO Children's Code Data Protection Impact Assessment (DPIA).
- **Missing Code:**
  The codebase templates fail to show how to integrate highly effective age-assurance methods or dynamically enforce "high privacy by default" settings (e.g. disabling precise location and profiling in code).
- **Missing Disclosure:**
  UI designs lack child-friendly privacy notices or simplified explanations of data collection.
- **Missing Logging:**
  No database schemas are provided to record age-assurance verification status, DPIA reviews, or the purging of verification data.
- **Missing Testing:**
  The test suites do not check that child accounts have location and profiling disabled by default.
- **Missing Evidence:**
  No templates are supplied for completed UK DPIAs, Ofcom compliance audits, or age-assurance certificates.
- **Missing Audit Trail:**
  An immutable log tracking age-assurance rule updates, safety audits, and DPIA history is missing.

---

## 15. Australia Online Safety Act

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment Act 2024 restricts under-16 access to designated social media platforms, requiring robust age assurance and the immediate destruction of verification data.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks written policy templates or guidelines for under-16 age restriction compliance.
- **Missing Documentation:**
  No guidelines exist detailing how to configure age-assurance waterfalls in accordance with eSafety Commissioner expectations.
- **Missing Code:**
  Code templates fail to demonstrate integration with eSafety-approved age estimation/verification engines or the secure destruction of verification data.
- **Missing Disclosure:**
  Onboarding templates do not display required disclosures explaining under-16 restrictions or the purpose of age collection.
- **Missing Logging:**
  No database schemas exist to log age-verification attempts or record the immediate deletion of raw verification documents.
- **Missing Testing:**
  The test suites do not programmatically verify that under-16 users are blocked from social features.
- **Missing Evidence:**
  The repository is missing templates for eSafety audits or verification-data destruction receipts.
- **Missing Audit Trail:**
  An unalterable audit trail tracking updates to the age-assurance waterfall and platform safety audits is completely absent.

---

## 16. Brazil Digital ECA

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) prohibits simple age self-declaration and mandates approved age-assurance methods (such as CPF database checks or facial matching), on top of LGPD minor consent requirements.

Official Citation: Law 15,211/2025 (Digital ECA).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template Brazil child safety policies, LGPD compliance policy templates, or Brazil storefront guidelines.
- **Missing Documentation:**
  No instructions are provided on how to implement Brazilian age-assurance methods (like CPF checks) on mobile platforms.
- **Missing Code:**
  The codebase lacks code structures to query Brazilian CPF databases, validate Brazilian minor accounts, or auto-rate loot-box games to 18-plus.
- **Missing Disclosure:**
  Onboarding screens do not display Brazilian CPF collection disclosures or LGPD parental consent statements.
- **Missing Logging:**
  No logging schemas exist to record Brazilian parental consent, CPF validation outcomes, or the immediate deletion of verification documents.
- **Missing Testing:**
  The test suites do not programmatically check that Brazilian users are presented with CPF/parental verification prior to in-app purchases.
- **Missing Evidence:**
  The repository is missing templates representing completed ANPD compliance audits or LGPD minor-data DPIAs.
- **Missing Audit Trail:**
  No immutable record logs age-assurance CPF checks, LGPD compliance updates, or consent records.

---

## 17. India Digital Personal Data Protection Act

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and the 2025 Rules enforce strict under-18 consent frameworks (such as DigiLocker-backed consent) and prohibit targeted advertising and behavioral tracking of minors.

Official Citation: Digital Personal Data Protection Act, 2023.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template Indian child privacy policies or DPDP compliance guidelines.
- **Missing Documentation:**
  No developer guides explain the under-18 consent frameworks or the absolute ban on minor behavioral tracking and targeted advertising.
- **Missing Code:**
  The repository contains no code templates showing how to integrate with DigiLocker or other government-approved parental consent systems.
- **Missing Disclosure:**
  UI templates are missing child-directed notices and DPDP-compliant parental consent prompts.
- **Missing Logging:**
  No database schemas are provided to record DigiLocker parental consent or track the suppression of behavioral analytics for Indian minors.
- **Missing Testing:**
  Test suites do not verify that Indian minor accounts have all tracking, analytics, and advertising SDKs programmatically disabled.
- **Missing Evidence:**
  No templates exist for DPDP compliance declarations or parental consent audit certificates.
- **Missing Audit Trail:**
  An immutable history logging DPDP consent records, parent verification attempts, and policy changes is missing.

---

## 18. Singapore Online Safety & PDPA

### 18.1 Regulatory Overview and Background
Singapore's IMDA Code of Practice requires app-store age assurance from 1 April 2026, screening and stopping minor access to age-inappropriate apps and ensuring data minimization.

Official Citation: IMDA Code of Practice for Online Safety (2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template Singapore Online Safety policies or guidelines for PDPA-compliant child data handling.
- **Missing Documentation:**
  No developer instructions explain how to integrate with credit-card or digital-verification systems to satisfy the IMDA age-assurance code.
- **Missing Code:**
  No code templates demonstrate PDPA-compliant age gating or the automatic deletion of age-assurance data immediately after verification.
- **Missing Disclosure:**
  Interfaces do not display required Singapore storefront disclosures concerning age-appropriate content access.
- **Missing Logging:**
  No database schemas are provided to log Singapore storefront age verification events or record data deletion triggers.
- **Missing Testing:**
  Test suites do not check that Singapore storefront downloads/launches block users under 18 from age-inappropriate sections.
- **Missing Evidence:**
  No templates are supplied representing Singapore compliance audits or PDPA minor-data DPIAs.
- **Missing Audit Trail:**
  An immutable audit trail tracking Singapore age-gating rules and subsequent data destruction logs is absent.

---

## 19. South Korea Telecommunications Business Act

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payments, requiring specific entitlements, Korea-only binaries, and monthly transaction reporting.

Official Citation: South Korea Telecommunications Business Act.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template policies for South Korea alternative billing or commission reporting guidelines.
- **Missing Documentation:**
  No developer guides or checklists exist for managing the Korea-only binary or the approved payment gateways (KCP, Inicis, Toss, NICE).
- **Missing Code:**
  The repository lacks code templates for configuring `SKExternalPurchase = "KR"` or implementing Korea-specific payment modal screens.
- **Missing Disclosure:**
  UI templates do not include the South Korea system-mandated alternative billing warning modal.
- **Missing Logging:**
  No backend database schemas are provided to track alternative-payment transactions or compile monthly Korean alternative sales reports.
- **Missing Testing:**
  The test suites do not check that standard StoreKit IAP and Korean alternative billing do not co-mingle within the same South Korea binary storefront.
- **Missing Evidence:**
  The playbook fails to supply templates representing monthly transaction summaries or proof of notarization files for Korea.
- **Missing Audit Trail:**
  No record system tracks South Korean compliance filings, alternative payment integrations, or transaction report histories.

---

## 20. China Mobile App Filing

### 20.1 Regulatory Overview and Background
China's MIIT requires mandatory app filings (ICP filings) for all apps distributed on Chinese storefronts, alongside real-name verification, content moderation, and Banhao gaming licenses.

Official Citation: MIIT Mobile App Filing Directive (2023).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks template China app compliance policies or ICP/MIIT filing guidelines.
- **Missing Documentation:**
  No developer guides explain China mobile app filing requirements, Banhao gaming licenses, or real-name verification.
- **Missing Code:**
  The repository lacks code examples for Chinese real-name verification interfaces or PIPL-compliant local data storage routing.
- **Missing Disclosure:**
  UI templates do not provide PIPL-compliant disclosures or display ICP filing numbers on the launch or settings screens.
- **Missing Logging:**
  No backend database schemas exist to log real-name verification events, ICP submission results, or PIPL local storage encryption logs.
- **Missing Testing:**
  Test suites do not verify that China storefront builds disable unfiled external APIs or enforce real-name gating prior to gameplay.
- **Missing Evidence:**
  No templates are supplied representing MIIT filing proofs, PIPL privacy impact assessments, or Banhao license certificates.
- **Missing Audit Trail:**
  An immutable audit trail tracking Chinese app filings, real-name verification updates, or PIPL compliance audits is absent.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 4**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DMA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU DSA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU EAA / EN 301 549** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US State Privacy** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Cancellation** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **SK Telecom Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **China App Filing** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook remains a powerful reference for storefront-level guidelines, yet lacks the deep operational structures required to ensure compliance once an application is live. To fully bridge these gaps:

1. Prioritize adding GPSR and DMA/DSA-specific checklist gates.
2. Provide concrete client-side and backend mock implementations for contract withdrawal, Global Privacy Control detection, and verifiable parental consent.
3. Establish robust database logging and unalterable audit trail templates across all 20 global and regional frameworks.

This analysis is static. Regulations change frequently, and practitioners must continuously consult primary official sources to verify dates and enforcement requirements.

---

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California CCPA, [California Civil Code Section 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&division=3.&title=1.81.5.&part=4.&chapter=&article=)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004&ChapterID=57)
- UK Online Safety Act, [Online Safety Act 2023 (c. 50)](https://www.legislation.gov.uk/ukpga/2023/50/contents/enacted)
- Australia Online Safety Act, [Online Safety Amendment (Social Media Minimum Age) Act 2024](https://www.legislation.gov.au/Details/C2024A00125)
- Brazil Digital ECA, [Law 15,211/2025](http://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm)
- India DPDPA, [Digital Personal Data Protection Act, 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA & IMDA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea Telecommunications Business Act, [Telecommunications Business Act](https://law.go.kr)
- China MIIT Directive, [MIIT Mobile App Filing Directive 2023](http://www.miit.gov.cn)
