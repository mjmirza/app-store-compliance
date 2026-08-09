# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty regulations that bind app developers shipping into global markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
  The playbook carries no template policy for the 14 day withdrawal right, and no guidance separating financial app scopes from general adoption defaults.
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
The US State App Store Accountability Acts (ASAA) represent a wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

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

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems (including mobile application developers utilizing third-party generative AI APIs) must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

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

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026. This framework is a critical release blocker for any application incorporating artificial intelligence that reaches users in the European Union.

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

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, targets large tech platforms designated as gatekeepers. For app developers, the DMA forces gatekeepers to allow third-party app stores, alternative payment systems, and external link steering within the EU.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no formal internal policy template for developers to outline their stance on deploying via third-party marketplaces or selecting alternative payment systems.
- **Missing Documentation:**
  While DMA entitlements are mentioned in `docs/EU-REGULATORY-2026.md`, the playbook does not offer step-by-step documentation on the operational overhead of monthly transaction reporting to Apple.
- **Missing Code:**
  The codebase does not contain templates for using alternative payment interfaces or implementing the `ExternalPurchaseCustomLink` system call.
- **Missing Disclosure:**
  There are no UI templates showing compliant disclosure designs when directing users outside the native App Store checkout flow.
- **Missing Logging:**
  No backend schema or code represents the secure storage of external payment tokens or transaction verification records required for revenue auditing.
- **Missing Testing:**
  No automated unit or integration tests are included to simulate external link flow transitions or the handling of checkout completion callbacks.
- **Missing Evidence:**
  The repository lacks templates of signed addendums (e.g., Alternative Terms Addendum) or completed monthly reports to show as evidence of compliant reporting.
- **Missing Audit Trail:**
  There is no audit trail schema to track external steering link changes, marketplace deployment histories, or billing reconciliation logs.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, establishes transparency and safety obligations for digital intermediaries. For mobile developers, this manifests as mandatory trader declarations on app stores to verify developer identity for EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not contain a policy framework or legal questionnaire to help developers determine whether their app counts as an intermediary, platform, or simply a trader under the DSA.
- **Missing Documentation:**
  The checklists fail to provide step-by-step operational checklists on setting up 2FA, obtaining D-U-N-S numbers, and responding to notice-and-action reports.
- **Missing Code:**
  There is no mock content-moderation reporting system or notice-and-action code block for user-generated content apps.
- **Missing Disclosure:**
  There are no mock UI interfaces showing the public display of trader registration info, verified telephone numbers, or email addresses as required for store listings.
- **Missing Logging:**
  There is no structural database logging format for user content reports, moderation actions, appeals, or administrative decisions.
- **Missing Testing:**
  The repository lacks automated validation scripts to check if mock Storefront listings have verified DSA contact URLs or visible trader metadata.
- **Missing Evidence:**
  No templates are provided to demonstrate verified trader credentials or mock compliance reports for systemic platform assessments.
- **Missing Audit Trail:**
  There is no audit trail system to log moderation activity, notices received, user bans, or when metadata listings were verified for EU users.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882, known as the European Accessibility Act (EAA), mandates that key products and services—including websites, mobile apps, and e-commerce—be fully accessible to persons with disabilities, aligning with the EN 301 549 technical standard.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no corporate accessibility policy template or framework outlining microenterprise exemption conditions or compliance roadmaps.
- **Missing Documentation:**
  The repository lacks detailed implementation manuals mapping WCAG 2.1 AA/WCAG 2.2 criteria to native Android XML/Compose or iOS UIKit/SwiftUI components.
- **Missing Code:**
  There are no fully implemented, compliant, accessible components (e.g., custom screen reader anchors or accessibility announcements) in the codebase.
- **Missing Disclosure:**
  Public-facing templates do not include standard Accessibility Statement documents or in-app paths disclosing the accessibility features of the service.
- **Missing Logging:**
  No architectural schemas or tracking systems exist to log user accessibility complaints, feedback, or dynamic font-scaling adjustments.
- **Missing Testing:**
  While static analysis is available via `scripts/accessibility-audit.py`, there are no end-to-end simulated screen reader unit tests or interactive contrast checks.
- **Missing Evidence:**
  The playbook does not hold templates for Accessibility Conformance Reports (ACRs) or Voluntary Product Accessibility Templates (VPATs).
- **Missing Audit Trail:**
  There is no formal tracking system or audit trail recording accessibility regressions, audit histories, or accessibility-related bug fixes.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, regulates the collection of personal information from children under 13 by online operators. An amended rule, taking full effect in 2026, places additional strict demands on biometrics, security, and third-party advertising.

Official Citation: 16 CFR Part 312 (COPPA Rule).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Children's Privacy Policy or COPPA-compliant privacy policy addendum is provided for the playbook's users.
- **Missing Documentation:**
  Detailed guides on verifiable parental consent (VPC) methods (such as face-matching or knowledge-based authentication) are missing.
- **Missing Code:**
  The repository has no functional code implementing a secure parental gate, age-gated onboarding, or third-party SDK exclusion based on age signals.
- **Missing Disclosure:**
  There are no UI templates showing direct notices to parents or clear consent requests for third-party tracking.
- **Missing Logging:**
  There is no secure system designed to log the receipt of parental consent, consent revocations, or the automatic deletion of minor account data.
- **Missing Testing:**
  There are no automated tests to verify that targeted advertising SDKs are disabled or that tracking stops when an under-13 age signal is active.
- **Missing Evidence:**
  The playbook provides no templates of written information-security programs or annual COPPA risk assessment forms.
- **Missing Audit Trail:**
  An unalterable audit trail recording our technical choices, SDK reviews, data minimization logs, and parent consent records is completely absent.

---

## 11. California Privacy (CCPA/CPRA/AADC)

### 11.1 Regulatory Overview and Background
California's privacy regime (CCPA, as amended by the CPRA) establishes robust consumer rights (know, delete, correct, opt-out of sale/sharing). The California Age-Appropriate Design Code (AADC) introduces protective standards for children under 18.

Official Citation: California Civil Code Sections 1798.100 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a customizable California Privacy Policy template or standard CCPA Privacy Notice.
- **Missing Documentation:**
  There is a gap in step-by-step developer guidelines on integrating the Global Privacy Control (GPC) opt-out signal within mobile webviews or API calls.
- **Missing Code:**
  No functional code blocks exist for handling dynamic Opt-Out ("Do Not Sell or Share My Info") requests or "Limit the Use of My Sensitive Personal Info" toggles.
- **Missing Disclosure:**
  UI onboarding templates do not offer CCPA Collection Notices or clear opt-out disclosure overlays.
- **Missing Logging:**
  No backend database schemas are provided to log GPC signals, opt-out states, deletion requests, or consent statuses.
- **Missing Testing:**
  There are no automated unit tests to verify that GPC headers (such as `Sec-GPC`) are honored and that data flows to analytics packages are stopped.
- **Missing Evidence:**
  The repository does not supply template Data Protection Impact Assessments (DPIAs) required under the AADC or records of consumer requests fulfilled.
- **Missing Audit Trail:**
  A secure, centralized history of opt-out configurations, policy updates, and compliance revisions is missing.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, mandates strict consent and disclosure requirements before collecting, storing, or using biometric identifiers (fingerprints, voiceprints, facial geometry).

Official Citation: 740 ILCS 14 (Illinois BIPA).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no written Biometric Data Policy template or public retention and destruction schedule template for developers to customize.
- **Missing Documentation:**
  The playbook lacks detailed developer runbooks mapping BIPA compliance to native FaceID/TouchID or Android BiometricPrompt integrations.
- **Missing Code:**
  The codebase does not contain biometric pre-consent dialogs or verification wrappers that block access to biometric APIs until a release is e-signed.
- **Missing Disclosure:**
  UI templates do not display the BIPA-mandated explicit disclosure screens explaining the purpose and duration of biometric storage.
- **Missing Logging:**
  The repository is missing database logging systems to safely track biometric consent timestamps without logging the raw biometric data.
- **Missing Testing:**
  No automated integration tests exist to verify that biometric features remain inactive until a verified consent flag is toggled in local state.
- **Missing Evidence:**
  The playbook provides no templates of written releases or audit forms to prove BIPA consent collection during legal disputes.
- **Missing Audit Trail:**
  An immutable audit trail to record when biometric policies were shown, when consent was granted, or when biometric data was purged is completely absent.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA) and state laws (California, New York, Massachusetts) require that online subscription cancellation be frictionless and at least as easy as signing up ("click to cancel").

Official Citation: 15 U.S.C. Sections 8401 et seq. (ROSCA).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no customizable Subscription Terms and Negative Option Policy template detailing cancellation procedures.
- **Missing Documentation:**
  The checklists lack detailed technical specifications on building compliant cancellation funnels that avoid dark patterns.
- **Missing Code:**
  The front-end user interface templates and billing mock codes in this repository do not contain any functional implementation of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Onboarding and paywall designs do not prominently display renewal terms, price escalations, or billing intervals immediately adjacent to purchase triggers.
- **Missing Logging:**
  The codebase has no tracking schemas designed to log cancellation requests, reasons, timestamps, or refund statuses.
- **Missing Testing:**
  No automated UI or unit tests exist in the repository to verify that the cancellation flow can be completed successfully in a frictionless, self-service manner.
- **Missing Evidence:**
  The playbook lacks templates of subscription agreements, email receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

---

## 14. UK Online Safety Act (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023, overseen by Ofcom, places significant duties of care on providers of online services to protect children from harmful content and to remove illegal content quickly.

Official Citation: UK Online Safety Act 2023.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No customizable Online Safety Policy or Child Safety Policy template is provided.
- **Missing Documentation:**
  The repository lacks developer checklists explaining how Ofcom's "Highly Effective Age Assurance" requirements apply to general applications.
- **Missing Code:**
  No codebase integrations demonstrate the use of facial age estimation or secure database age checks.
- **Missing Disclosure:**
  Public-facing materials do not detail child-safety measures, safety rating processes, or age limits.
- **Missing Logging:**
  No structured logging format is supplied to track reports of harmful content, automated flagging, or moderation outcomes.
- **Missing Testing:**
  The test suite does not include functional test cases simulating user content moderation reporting or rapid content takedown.
- **Missing Evidence:**
  The repository does not contain child-safety risk assessment templates or design review worksheets.
- **Missing Audit Trail:**
  An audit trail to record historical safety system updates, risk assessments, or moderator training records is missing.

---

## 15. Australia Online Safety Act (Social Media Minimum Age)

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 enforces age-restrictions (under 16) on social media platforms, requiring robust age assurance and the destruction of age-verification data.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template exists for Australia-specific age limits, social-media data ringfencing, or age-assurance policies.
- **Missing Documentation:**
  The playbook lacks operational instructions on how to set up child-access blocks specifically for Australian IP addresses.
- **Missing Code:**
  No codebase helper classes demonstrate blocking under-16 accounts based on storefront or IP routing.
- **Missing Disclosure:**
  In-app onboarding does not clearly state the 16+ age restriction or the data destruction policy for Australian users.
- **Missing Logging:**
  There is no specialized logging framework that tracks age checks while guaranteeing the immediate destruction of raw verification files.
- **Missing Testing:**
  No automated integration tests verify that an Australian storefront account rated under 16 is barred from account creation.
- **Missing Evidence:**
  No templates of age-data deletion certificates or regulatory compliance logs are provided.
- **Missing Audit Trail:**
  An immutable audit trail showing compliance assessments of age-gating accuracy or Ofcom/eSafety-directed reviews is absent.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) prohibits simple self-declaration checkboxes for age verification, requiring document checks, facial age estimation, or database matching to protect minors.

Official Citation: Law 15,211/2025 (Brazil Digital ECA).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template policy or LGPD children-privacy addendum exists to address Brazil's strict age-verification mandates.
- **Missing Documentation:**
  Detailed instructions on integrating Brazilian CPF database validation or local partner checks are missing.
- **Missing Code:**
  The repository lacks mock integrations with Brazilian age-verification engines or local validation tools.
- **Missing Disclosure:**
  No onboarding UI templates provide Brazilian Portuguese notices regarding mandatory age validation.
- **Missing Logging:**
  No backend database schemas exist to log Brazilian age-verification outcomes without retaining sensitive CPF or document data.
- **Missing Testing:**
  The test suite contains no automated unit or integration tests verifying the block of minor registration for Brazil storefronts.
- **Missing Evidence:**
  No sample LGPD impact reports or age-assurance audits are included.
- **Missing Audit Trail:**
  An audit trail recording age-validation methodology updates, third-party audits, or local compliance certifications is missing.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's DPDPA 2023, along with the DPDP Rules 2025, requires verifiable parental consent through government-backed platforms (such as DigiLocker) for users under 18, and bans children's behavioral tracking.

Official Citation: Digital Personal Data Protection Act, 2023.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no customizable DPDPA-compliant privacy policy or specific Consent Manager policy framework.
- **Missing Documentation:**
  Step-by-step documentation on DigiLocker integration or local Indian identity verification flows is missing.
- **Missing Code:**
  No code templates are available to disable ad tracking or behavioral analysis dynamically when the user is located in India and is under 18.
- **Missing Disclosure:**
  Onboarding designs do not feature multi-lingual Indian language disclosures regarding data use and parent consent.
- **Missing Logging:**
  No logging mechanisms exist to record parental consent via standard DigiLocker callbacks or local verification hashes.
- **Missing Testing:**
  No automated tests exist to verify that targeted advertising APIs are deactivated for Indian minor accounts.
- **Missing Evidence:**
  The repository contains no DPDPA-compliant Consent Forms or Data Protection Officer appointment letters.
- **Missing Audit Trail:**
  An unalterable audit trail recording consent updates, consent revocations, and data processing justifications is completely missing.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice

### 18.1 Regulatory Overview and Background
Singapore's PDPA governs data collection, requiring a designated DPO. The IMDA Code of Practice requires app storefronts to enforce age-assurance and immediately destroy verification data.

Official Citation: Personal Data Protection Act 2012 (Singapore).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate PDPA Privacy Policy template or Singapore-specific DPO appointment guide is provided.
- **Missing Documentation:**
  Operational guidelines on handling Singapore IMDA child-safety reviews are absent.
- **Missing Code:**
  The codebase has no modules for automating the immediate deletion of user identity documents post-verification.
- **Missing Disclosure:**
  UI templates do not display required Singapore-specific notices concerning data processing or DPO contact details.
- **Missing Logging:**
  There are no logging provisions to record Singapore age verification states while maintaining strict data-minimization rules.
- **Missing Testing:**
  No automated tests are provided to confirm that Singapore storefront accounts under 18 are prevented from installing inappropriate content.
- **Missing Evidence:**
  No templates exist for Singapore PDPA-compliant Data Protection Impact Assessments (DPIAs).
- **Missing Audit Trail:**
  An immutable audit trail to track compliance checks, data transfer records, and DPO audit logs is missing.

---

## 19. South Korea Telecommunications Act (Alternative Billing)

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates that app stores allow alternative in-app payment systems. Developers using this must submit monthly reports and pay a 26% commission.

Official Citation: Telecommunications Business Act (South Korea).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no corporate policy template detailing the usage of Korean-approved billing providers or commission payments.
- **Missing Documentation:**
  The checklists lack detailed technical specifications on building South Korea-specific payment binaries.
- **Missing Code:**
  No mock client-side codes demonstrate displaying the mandatory South Korean external-purchase modal sheet before checkout.
- **Missing Disclosure:**
  UI templates do not show South Korea-compliant warning notices regarding alternate payment systems.
- **Missing Logging:**
  No backend schema represents the secure storage of external payment tokens or transaction verification records required for revenue auditing.
- **Missing Testing:**
  No integration tests simulate Korean alternative billing flows or payment completion events.
- **Missing Evidence:**
  No templates are provided to demonstrate completed monthly sales reports for South Korean tax and store authorities.
- **Missing Audit Trail:**
  There is no audit trail system to log South Korean transaction history, billing reconciliation, or commission fee payments.

---

## 20. China App Filing (MIIT ICP Extension)

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates that all mobile apps obtain an ICP filing/App filing before listing on app stores, requiring a local Chinese entity or partner.

Official Citation: MIIT Announcement on Mobile App Filing (2023).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template or legal checklist is available to guide developers on structuring partnerships with Chinese local entities.
- **Missing Documentation:**
  The repository is missing step-by-step developer guides on obtaining MIIT App Filings, real-name registration, and Banhao game licenses.
- **Missing Code:**
  The codebase contains no real-name verification blocks or Chinese SMS validation API mocks.
- **Missing Disclosure:**
  UI designs do not include compliant displays of China MIIT filing numbers in-app (e.g., in the Settings or About section).
- **Missing Logging:**
  No database schemas are provided to log real-name verification states, content moderation logs, or server-side firewall activities.
- **Missing Testing:**
  No automated validation scripts check if mock builds destined for China storefronts contain the mandatory filing numbers.
- **Missing Evidence:**
  No templates of MIIT filing applications, partner entity agreements, or local hosting contracts are provided.
- **Missing Audit Trail:**
  There is no audit trail schema to track MIIT updates, real-name validation changes, or content moderation histories.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK OSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. Most of these regulations are already named in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`, with dated sources and a deadline entry. What they lack is the implementation layer, meaning detection rules in the guard, code templates, and tests. GPSR is the only one absent end to end, so it is the first thing to add.

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most of the frameworks here are already named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order.

1. Add GPSR, the only framework absent end to end.
2. Give the Partial frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates, starting with the AI Act Article 50 disclosure line and the withdrawal path, since both carry 2026 deadlines.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- COPPA, [16 CFR Part 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)
- California CCPA, [California Civil Code 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004&ChapterID=57)
- ROSCA, [15 U.S.C. 8401](https://www.gpo.gov/fdsys/pkg/USCODE-2011-title15/pdf/USCODE-2011-title15-chap110.pdf)
- UK Online Safety Act, [UK OSA 2023](https://www.legislation.gov.uk/ukpga/2023/30/contents/enacted)
- Australia Online Safety Act, [Online Safety Act 2021](https://www.legislation.gov.au/Details/C2021A00076)
- Brazil Digital ECA, [Brazil Federal Legislation](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- Singapore PDPA, [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea TBA, [Telecommunications Business Act](https://law.go.kr/LSW/lsInfoP.do?lsiSeq=250000)
- China Mobile App Filing, [MIIT App Filing Regulations](https://www.miit.gov.cn/)
