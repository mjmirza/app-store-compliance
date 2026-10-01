# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile and web application developers shipping into the EU, US, UK, Australia, Brazil, Canada, India, Singapore, South Korea, China, and global storefronts, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

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
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification.

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
  An immutable audit trail to record the historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is entirely absent.

### 4.3 Remediation and Action Plan
1. Create a detailed written Minor Age Assurance Policy that specifies how state-level requirements are identified and how children's data is strictly minimized.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and automated procedures to purge raw age-verification data immediately after the user's age category is confirmed.
4. Establish automated unit tests that verify that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is successfully processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with technical complexity and impact.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining team obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable to direct product code, but helper scripts to validate literacy log currency in CI pipelines are absent.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose commitment to or enforcement of AI literacy standards as mandated by Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no automated internal lints, pre-commit hooks, or CLI tools to verify that team members committing AI-related changes have valid, up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of acceptable evidence, such as a completed training log, a course record, or a written risk assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting when the AI literacy policy was reviewed, when training modules were updated, or how team training records evolved over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review team literacy records on an annual basis.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been reviewed or updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for certain AI systems, taking full legal effect on 2 August 2026.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons inform users that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems (text, audio, images, or video) must be marked in a machine-readable format and detectable as artificially generated or manipulated. Article 50(4) requires deployers of deepfakes to disclose that content has been artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosure must appear and how generated media should be marked.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed technical developer instructions on how to implement machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes, middle-tier layers, or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display required immediate disclosures ("You are interacting with an AI system") at the time of first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  Existing test runner scripts do not check for the presence of synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA) & Alternative Distribution

### 7.1 Regulatory Overview and Background
The Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeepers (such as Apple and Alphabet/Google) to ensure fair and contestable markets in the digital sector. For mobile developers distributing in the EU, the DMA mandates alternative app distribution (Web Distribution and Alternative App Marketplaces), alternative payment processing, and non-discriminatory access to hardware and platform features.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No written policy template guides developers on evaluating business models for alternative distribution versus App Store distribution under EU business terms (including Attachment 14 and Core Technology Commission rules).
- **Missing Documentation:**
  Documentation lacks comprehensive step-by-step developer guides on building, signing, and hosting notarized iOS web distribution packages or managing Alternative App Marketplace entitlements.
- **Missing Code:**
  The repository lacks boilerplate integration code for StoreKit External Purchase custom link sheets (`ExternalPurchaseCustomLink`) and automated reporting scripts for the External Purchase Server API.
- **Missing Disclosure:**
  UI templates do not include system-level or custom disclosure sheets informing EU users about external transaction terms and lack of Apple purchase protection when using alternative payment options.
- **Missing Logging:**
  Backend templates lack schemas to log external purchase transaction IDs, timestamps, and reporting confirmation tokens required for monthly reporting to platform gatekeepers.
- **Missing Testing:**
  No unit or end-to-end tests exist to verify that alternative payment links dynamically open system disclosure sheets or that IAP and external links are strictly segregated per EU storefront rules.
- **Missing Evidence:**
  The repository provides no example templates for notarization tickets, Stand-By Letters of Credit, or proof of meeting alternative marketplace eligibility thresholds.
- **Missing Audit Trail:**
  An immutable audit trail system to log ADPLA Attachment 14 acceptance, monthly transaction reports sent to Apple/Google, and notarization history is missing.

### 7.3 Remediation and Action Plan
1. Develop an EU Alternative Distribution Policy and Decision Framework.
2. Build code templates for `ExternalPurchaseCustomLink` modal triggers and External Purchase Server API monthly reporting.
3. Implement automated test suites to verify EU storefront entitlement declarations and link segregation rules.

---

## 8. EU Digital Services Act (DSA) Trader & Risk Requirements

### 8.1 Regulatory Overview and Background
The Digital Services Act (Regulation (EU) 2022/2065) establishes horizontal rules for online intermediaries. Articles 30 and 31 require app stores to collect, verify, and publicly display trader contact and identity information before developers can distribute apps to EU consumers.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal Trader Status Determination Policy helping developers evaluate whether their app distribution constitutes commercial trader activity under EU consumer law.
- **Missing Documentation:**
  Checklists lack detailed operational runbooks on submitting, verifying, and maintaining D-U-N-S numbers, 2FA trader contact info, and payment account details in App Store Connect and Google Play Console.
- **Missing Code:**
  No automated pre-submission guard checks scan app store metadata or configuration files to confirm that DSA trader verification flags are active before an EU release.
- **Missing Disclosure:**
  Templates fail to provide mandatory in-app disclosures informing EU consumers when an app is provided by a non-trader entity (where statutory consumer protection rights do not apply).
- **Missing Logging:**
  There are no logging mechanisms to record when trader declarations were submitted, updated, or re-verified across developer platform accounts.
- **Missing Testing:**
  No automated validation scripts exist to test whether app store metadata feeds contain verified trader address, phone, and email details for EU storefronts.
- **Missing Evidence:**
  The repository lacks sample documentation packages (such as government business registration certificates or utility bills) used to prove trader identity during platform audits.
- **Missing Audit Trail:**
  An unalterable record of all trader status changes, verification tickets, and communications with app store compliance teams is absent.

### 8.3 Remediation and Action Plan
1. Publish a Trader Status Classification Guide and Policy in the `docs/` folder.
2. Extend pre-submission scripts to check that DSA trader attributes are populated and verified in store metadata exports.
3. Maintain an internal compliance repository directory for verified trader identity evidence and verification receipts.

---

## 9. European Accessibility Act (EAA) / EN 301 549 Compliance

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) applies to consumer products and services, including mobile applications and e-commerce platforms. Technical compliance is defined by harmonised standard EN 301 549 (specifically Chapter 11 for non-web software and mobile apps), which builds upon WCAG 2.1 Level AA requirements.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no corporate Mobile and Web Accessibility Policy establishing mandatory adherence to EN 301 549 Chapter 11 standards for all EU-facing products.
- **Missing Documentation:**
  While general accessibility checklists exist, the repository lacks dedicated developer guides explaining the specific differences between WCAG 2.1 AA and EN 301 549 Chapter 11 mobile software requirements.
- **Missing Code:**
  Mock UI components lack complete implementations for Dynamic Type scaling, VoiceOver traits, accessible focus orders, custom rotor actions, and high-contrast color mode overrides.
- **Missing Disclosure:**
  Public-facing templates do not include a compliant Accessibility Statement (conforming to EN 301 549 Annex B/C) outlining conformance status, feedback mechanisms, and enforcement procedure links.
- **Missing Logging:**
  No logging frameworks exist to record accessibility feedback, user-reported accessibility barrier tickets, or remediation resolution timelines.
- **Missing Testing:**
  Static accessibility scripts (`scripts/accessibility-audit.py`) do not test for full EN 301 549 Chapter 11 rules (such as screen reader navigation flows, switch control support, or touch target sizes).
- **Missing Evidence:**
  The repository lacks sample Accessibility Conformance Reports (VPAT / EN 301 549 ACR) or expert audit reports required for regulatory defense.
- **Missing Audit Trail:**
  There is no historical record system tracking accessibility regression audits, remediation cycles, or updates to the published accessibility statement.

### 9.3 Remediation and Action Plan
1. Create an EN 301 549 Chapter 11 Mobile Accessibility Checklist and Policy.
2. Publish a standardized Accessibility Statement template under `templates/` for mobile and web listings.
3. Enhance `scripts/accessibility-audit.py` to validate Dynamic Type, touch target dimensions, and screen reader labels.

---

## 10. US Amended COPPA Rule (2025/2026 FTC Amendments)

### 10.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) Children's Online Privacy Protection Rule (16 CFR Part 312) was updated via amendments published at 90 FR 16918 (effective 23 June 2025, compliance enforced from April 2026). Key updates expand personal information to include biometric identifiers and government IDs, require separate opt-in consent for third-party disclosure and targeted advertising, mandate written data retention policies, and require a formal written information security program.

Official Citation: 16 CFR Part 312 (FTC Amended COPPA Rule).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive Children's Data Protection Policy incorporating the 2025/2026 amended COPPA rules (biometric data rules, separate consent, and data retention limits).
- **Missing Documentation:**
  Checklists do not provide step-by-step developer runbooks for implementing new verifiable parental consent methods (such as face-match to government photo ID) or written information security programs under 312.8.
- **Missing Code:**
  Codebases lack logic to separate parental consent for app functionality from third-party advertising disclosures, and lack automated data deletion routines enforcing strict retention schedules under 312.10.
- **Missing Disclosure:**
  Privacy notice templates do not explicitly disclose the collection of biometric or government identifiers, nor do they provide distinct, unbundled opt-in checkboxes for third-party disclosures.
- **Missing Logging:**
  Backend schemas do not support logging distinct parental consent types (functional vs. third-party sharing) or automated records of child data deletion upon contract expiration.
- **Missing Testing:**
  Test suites fail to verify that feature access remains available to a child when the parent consents to core functionality but declines third-party advertising disclosure.
- **Missing Evidence:**
  The repository is missing templates for written Information Security Plans (WISP), annual security risk assessments, and FTC Safe Harbor compliance certificates.
- **Missing Audit Trail:**
  An immutable audit trail documenting parental consent receipts, consent revocations, and data deletion job executions is not present.

### 10.3 Remediation and Action Plan
1. Draft an Amended COPPA Compliance Policy and unbundled parental consent UI flow.
2. Add backend scripts to execute automated retention-based deletion of child personal data.
3. Update guard scripts to flag bundled parental consent forms that condition app access on ad targeting.

---

## 11. California Privacy Rights Act (CPRA) & CPPA 2026 Regulations

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), and the CPPA 2026 regulations enforce strict consumer privacy rights, including opt-outs for sale/sharing/targeted advertising, Global Privacy Control (GPC) honoring, and automated decision-making technology (ADMT) disclosures.

Official Citation: California Civil Code Section 1798.100 et seq.; California Code of Regulations Title 11.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a dedicated CPRA/CPPA Compliance Policy defining data minimisation standards, sensitive personal information limits, and ADMT opt-out mechanisms.
- **Missing Documentation:**
  Checklists lack operational developer guides for implementing Global Privacy Control (GPC) signal detection across native webviews and mobile apps.
- **Missing Code:**
  Web and mobile app templates do not include code to inspect the `Sec-GPC` HTTP header or pass platform-level privacy signals down to ad networks and analytics SDKs.
- **Missing Disclosure:**
  Privacy notices lack specific disclosures regarding Automated Decision-Making Technology (ADMT) logic, profiling purposes, and explicit "Do Not Sell or Share My Personal Information" links.
- **Missing Logging:**
  No backend schema exists to record consumer opt-out requests, GPC header detections, or Limit the Use of Sensitive Personal Information choices.
- **Missing Testing:**
  Automated tests do not simulate incoming `Sec-GPC` headers or native opt-out flags to verify that third-party tracking scripts are suppressed instantly.
- **Missing Evidence:**
  The repository lacks templates for Cybersecurity Audit reports or Risk Assessment submissions required under CPPA regulations.
- **Missing Audit Trail:**
  An immutable audit log tracking consumer rights requests (know, delete, correct, opt-out) from submission through fulfillment is absent.

### 11.3 Remediation and Action Plan
1. Create a GPC Signal Handling Integration Guide and Policy.
2. Build code middleware to inspect `Sec-GPC` headers and disable tracking SDKs dynamically.
3. Add automated tests verifying data flow suppression when GPC signals are active.

---

## 12. Illinois Biometric Information Privacy Act (BIPA) & State Biometric Laws

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) imposes strict rules on collecting, capturing, purchasing, receiving, or storing biometric identifiers (fingerprints, voiceprints, retina/iris scans, hand/face geometry). Key duties include written notice, written release, a public retention and destruction schedule, and a absolute ban on profiting from biometric data.

Official Citation: 740 ILCS 14/ (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template Biometric Data Privacy Policy or public biometric retention and destruction policy as mandated by BIPA Section 15(a).
- **Missing Documentation:**
  Checklists do not provide developer instructions on separating local device biometric authentication (e.g., Apple Face ID / Touch ID, Android BiometricPrompt) from backend biometric collection.
- **Missing Code:**
  Templates do not include compliant written consent forms or automated data destruction scripts enforcing the 3-year maximum retention limit under BIPA.
- **Missing Disclosure:**
  Onboarding UI templates lack explicit biometric disclosures detailing the specific biometric identifier collected, the specific purpose, and the exact length of storage.
- **Missing Logging:**
  There are no backend logging mechanisms to record written release executions, consent timestamps, or destruction records for biometric templates.
- **Missing Testing:**
  No integration tests exist to verify that biometric features remain completely locked until an explicit written release is recorded.
- **Missing Evidence:**
  The repository lacks sample written release agreements, biometric vendor compliance attestations, or proof of destruction certificates.
- **Missing Audit Trail:**
  An unalterable audit log tracking the entire lifecycle of biometric data from consent through destruction is missing.

### 12.3 Remediation and Action Plan
1. Publish a BIPA Biometric Compliance Policy and Public Retention Schedule template.
2. Build UI templates for standalone written biometric consent releases.
3. Implement automated guard rules checking that any custom biometric collection code triggers an explicit written consent workflow.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Rules)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative-option laws (California SB 313/AB 2863, New York, Massachusetts) require clear disclosures, explicit informed consent, and a simple, direct "click-to-cancel" mechanism for recurring subscriptions billed outside standard app store in-app purchase systems.

Official Citation: 15 U.S.C. 8401 et seq.; Cal. Bus. & Prof. Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no written Subscription and Negative Option Policy defining rules for cancellation simplicity, pre-renewal notices, and trial conversions.
- **Missing Documentation:**
  Checklists do not provide developers with explicit design guidelines for building one-click online cancellation flows for web-billed subscriptions.
- **Missing Code:**
  Web and account-settings UI templates lack self-service cancellation buttons, retention save-discount flows that maintain easy exit paths, or cancellation API endpoints.
- **Missing Disclosure:**
  Checkout UI templates fail to display prominent negative option disclosures (billing amount, recurring frequency, trial duration, and cancellation method) directly adjacent to the action button.
- **Missing Logging:**
  No backend logging schemas exist to capture cancellation request timestamps, immediate termination confirmations, or pre-renewal notice emails sent.
- **Missing Testing:**
  No automated UI tests exist to confirm that a user can complete subscription cancellation in the same number of steps required to sign up, without mandatory customer support calls.
- **Missing Evidence:**
  The repository lacks templates of post-cancellation email receipts, billing terms acknowledgement records, or trial conversion notices.
- **Missing Audit Trail:**
  An immutable audit log tracking subscription lifecycles, cancellation attempts, and cancellation flow UI changes is absent.

### 13.3 Remediation Action Plan
1. Draft a ROSCA and State Negative Option Compliance Policy.
2. Develop a self-service cancellation component for web-billed account management portals.
3. Build automated integration tests verifying that cancellation requires no human intervention or phone calls.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and the ICO Age Appropriate Design Code (Children's Code) mandate age-assurance measures, illegal content removal, risk assessments, and high-privacy default settings for services likely to be accessed by UK children under 18.

Official Citation: Online Safety Act 2023 (c. 50); Data Protection Act 2018 Section 123.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template UK Online Safety and Children's Privacy Policy covering Ofcom risk assessment duties or ICO design standards.
- **Missing Documentation:**
  Checklists lack operational developer guides on conducting Data Protection Impact Assessments (DPIA) tailored to UK children or implementing Highly Effective Age Assurance.
- **Missing Code:**
  Mobile and web code templates do not default high-privacy settings (geolocation disabled, profiling disabled, search indexing disabled) when a UK user is detected as a minor.
- **Missing Disclosure:**
  Public-facing templates lack child-friendly terms of service or prominent disclosures explaining content moderation and age-assurance mechanisms.
- **Missing Logging:**
  Backend schemas lack mechanisms to log age-verification outcomes, CSEA report submissions to the NCA portal, or illegal content moderation actions.
- **Missing Testing:**
  Test suites fail to verify that default settings for minor accounts automatically suppress geolocation and profiling capabilities.
- **Missing Evidence:**
  The repository lacks sample Children's Code DPIAs, Ofcom risk assessment summaries, or age-assurance vendor verification certificates.
- **Missing Audit Trail:**
  An immutable audit trail documenting content moderation actions, age-assurance updates, and child safety reviews is missing.

### 14.3 Remediation and Action Plan
1. Create a UK Children's Code DPIA Template and Default Settings Guide.
2. Build configuration templates ensuring minor account defaults enforce privacy-by-default rules.
3. Add automated test cases verifying geolocation and profiling suppression for minor accounts.

---

## 15. Australia Online Safety (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts, enforcing strict age assurance and data destruction rules.

Official Citation: Online Safety Act 2021 (as amended 2024).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Age-Restricted Social Media Policy specifying compliant age-assurance waterfall methods and data ringfencing protocols.
- **Missing Documentation:**
  Checklists do not provide developer instructions for implementing age-assurance waterfalls or verifying eSafety Commissioner compliance codes.
- **Missing Code:**
  Codebases lack integration scripts for approved age-assurance providers or automated data destruction handlers for raw identity artifacts in Australian user flows.
- **Missing Disclosure:**
  Onboarding templates do not display required disclosures informing Australian users that account creation is restricted to age 16+ and that age data is destroyed immediately after verification.
- **Missing Logging:**
  No backend logging exists to record age verification attempts, pass/fail status, and immediate destruction tokens for raw identification documents.
- **Missing Testing:**
  Automated tests do not verify that under-16 Australian accounts are blocked from account creation or that raw identity documents are purged immediately.
- **Missing Evidence:**
  The repository lacks sample eSafety risk assessments, age-assurance audit reports, or proof of identity data destruction logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking age-assurance platform deployments and regulatory submission records is absent.

### 15.3 Remediation Action Plan
1. Draft an Australian Age-Restricted Platform Compliance Policy.
2. Implement backend handlers to enforce immediate destruction of age-verification artifacts.
3. Build automated tests verifying under-16 account creation blocks for Australian storefronts.

---

## 16. Brazil Digital ECA (Law 15,211/2025) & Decreto 12.880

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto 12.880 regulate child and adolescent protection online, requiring ANPD-approved age-verification methods (document verification, facial estimation, CPF checks), parental authorization, and mandatory 18+ download gating for gambling and adult content.

Official Citation: Lei No. 15.211/2025; Decreto No. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository contains no template Brazil Digital ECA Compliance Policy covering parental authorization, CPF age checks, or ANPD reporting rules.
- **Missing Documentation:**
  Checklists do not offer developer runbooks for querying Google Play's Age Signals API or Apple's Declared Age Range API specifically for Brazil Digital ECA compliance.
- **Missing Code:**
  Codebases lack backend integrations for CPF verification services, facial age estimation APIs, or automated 18+ content gating for Brazilian IP addresses.
- **Missing Disclosure:**
  UI templates lack Portuguese-language disclosures regarding minor protection, guardian authorization requirements, and age-rating notices.
- **Missing Logging:**
  No logging mechanisms exist to capture guardian authorization records, age contestation requests, or age-verification system logs.
- **Missing Testing:**
  Test suites fail to verify that self-declaration checkboxes are rejected for Brazilian user accounts in favor of active age assurance.
- **Missing Evidence:**
  The repository lacks sample ANPD compliance filings, age-assurance provider audit reports, or guardian consent records.
- **Missing Audit Trail:**
  An unalterable audit log tracking guardian consent events, age-rating adjustments, and ANPD inspection responses is missing.

### 16.3 Remediation and Action Plan
1. Formulate a Brazil Digital ECA Compliance Guide and Policy.
2. Build code templates integrating ANPD-compliant age verification API connectors.
3. Add automated guard checks rejecting simple checkbox self-declarations for Brazilian store listings.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 & Rules 2025

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and the DPDP Rules 2025 require verifiable parental consent for processing data of individuals under 18, prohibit behavioral tracking and targeted advertising aimed at children, and establish registered Consent Managers.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Compliance Policy detailing rules for under-18 consent, Consent Manager integration, and data principal rights.
- **Missing Documentation:**
  Checklists do not provide developer instructions for integrating with DigiLocker or registered Consent Managers for verifiable parental consent in India.
- **Missing Code:**
  Codebases lack logic to suppress behavioral tracking, personalized recommendations, and targeted ads for users under 18 in India.
- **Missing Disclosure:**
  Consent notice templates lack multi-language (22 scheduled languages) disclosures detailing data processing purposes and Consent Manager options.
- **Missing Logging:**
  No backend schema exists to record Consent Manager tokens, parental consent receipts, or data erasure requests under DPDPA.
- **Missing Testing:**
  Automated tests do not verify that ad-targeting SDKs are disabled for under-18 Indian accounts.
- **Missing Evidence:**
  The repository lacks sample DPDPA consent notices, Consent Manager integration certifications, or Data Protection Officer appointment records.
- **Missing Audit Trail:**
  An immutable audit log tracking consent withdrawals, data erasure requests, and Data Protection Board communications is missing.

### 17.3 Remediation Action Plan
1. Draft an India DPDPA Compliance and Consent Policy.
2. Implement backend handlers to interface with registered Consent Manager APIs.
3. Build automated test cases verifying tracking suppression for under-18 Indian user profiles.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA App Store Rules

### 18.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require age assurance, data protection officer designation, 3-day breach notifications, and 18+ download blocks on mobile app stores.

Official Citation: Personal Data Protection Act 2012 (No. 26 of 2012); IMDA Code of Practice 2025/2026.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Singapore PDPA and IMDA Compliance Policy covering age assurance, breach response timelines, and DPO requirements.
- **Missing Documentation:**
  Checklists lack developer runbooks for implementing 3-day PDPC breach notification protocols and app-store age-rating declarations.
- **Missing Code:**
  Codebases lack backend triggers to initiate rapid 3-day breach reporting workflows or age-gating checks for Singapore users.
- **Missing Disclosure:**
  Privacy notice templates lack specific disclosures naming the Data Protection Officer and detailing cross-border data transfer safeguards under PDPA.
- **Missing Logging:**
  No backend schema exists to log data breach discovery timestamps, severity evaluations, or PDPC notification records.
- **Missing Testing:**
  Test suites fail to verify that 18+ rated apps enforce appropriate age-assurance barriers on Singapore storefronts.
- **Missing Evidence:**
  The repository lacks sample PDPC breach notification forms, DPO designation records, or IMDA compliance filings.
- **Missing Audit Trail:**
  An unalterable audit log tracking privacy policy updates, DPO reviews, and breach incident management is absent.

### 18.3 Remediation and Action Plan
1. Publish a Singapore PDPA and IMDA Compliance Protocol.
2. Build automated incident response scripts for 3-day PDPC breach notifications.
3. Add automated tests verifying 18+ download gating for Singapore store configurations.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment methods, while the Personal Information Protection Act (PIPA) amendment imposes strict CEO privacy accountability, board-approved CPOs, and under-16 consent rules.

Official Citation: Telecommunications Business Act Article 22-9; Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Korea Compliance Policy covering alternative in-app payment entitlement rules (`com.apple.developer.storekit.external-purchase`) and CEO/CPO privacy duties.
- **Missing Documentation:**
  Checklists lack operational developer runbooks for submitting monthly alternative billing sales reports to Apple/Google Korea or configuring GRAC age ratings.
- **Missing Code:**
  Codebases lack implementation for Korea-specific alternative payment sheets, approved local payment gateway connectors (KCP, Inicis, Toss), or monthly revenue reporting tools.
- **Missing Disclosure:**
  UI templates lack mandatory Korean pre-payment modal sheets informing users about alternative payment provider terms and lack of store refund support.
- **Missing Logging:**
  Backend schemas do not capture alternative payment transaction records, 15-day monthly sales report exports, or under-16 legal representative consent records.
- **Missing Testing:**
  Test suites do not verify that alternative billing options are restricted exclusively to Korean storefront binaries.
- **Missing Evidence:**
  The repository lacks sample monthly sales reports submitted to KCC/Apple, CPO board appointment resolutions, or GRAC rating certificates.
- **Missing Audit Trail:**
  An immutable audit log tracking alternative billing transaction reporting, CPO oversight reviews, and Korean regulatory filings is missing.

### 19.3 Remediation Action Plan
1. Create a South Korea Alternative Billing and PIPA Compliance Policy.
2. Build code templates for Korea alternative purchase modal sheets and monthly sales report generation.
3. Add automated test cases enforcing Korea storefront geo-restriction for alternative billing entitlements.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Interactive Services Rules

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) for all apps operating in China. Additionally, CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services) bans virtual companion/kin services for minors, mandates automatic minor mode switching, and requires real-name verification.

Official Citation: MIIT Mobile App Filing Rules (2023/2024); CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no China Compliance Policy covering MIIT App Filing, local entity requirements, Banhao licenses, or CAC AI minor restrictions.
- **Missing Documentation:**
  Checklists lack developer runbooks for completing MIIT app filing through local Chinese partners or implementing CAC-mandated Minors Mode UI flows.
- **Missing Code:**
  Codebases lack integrations for real-name identity verification APIs, automatic Minors Mode switching logic, or keyword content filtering required by CAC rules.
- **Missing Disclosure:**
  UI templates lack Chinese-language terms disclosing ICP filing numbers, real-name verification notices, and CAC AI interaction notices.
- **Missing Logging:**
  Backend schemas do not support logging real-name verification status tokens, Minors Mode activation events, or content filtering triggers.
- **Missing Testing:**
  Test suites fail to verify that AI companion features are blocked when a user account is identified as a minor in China.
- **Missing Evidence:**
  The repository lacks sample MIIT filing receipts, Banhao gaming license documentation, or local Chinese entity partnership agreements.
- **Missing Audit Trail:**
  An unalterable audit log tracking CAC algorithm filing submissions, real-name verification records, and MIIT app registration history is absent.

### 20.3 Remediation and Action Plan
1. Publish a China App Distribution and CAC AI Compliance Guide.
2. Build code components for Minors Mode activation and real-name verification API connectors.
3. Add automated guard rules verifying that AI companion features check minor status before rendering in Chinese app builds.

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
| **8. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. CPRA / CPPA 2026** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Minimum Age** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most frameworks audited above are named with dated sources in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, and `data/regulatory-deadlines.json`. What they lack is the implementation layer, meaning detection rules in the guard, code templates, and automated tests. GPSR remains the primary framework absent end-to-end, making it the highest priority for initial remediation.

In priority order:
1. Add GPSR detection rules, policy templates, and UI components.
2. Extend detection rules in `data/rejection-patterns.json` and `data/detection-recipes.json` for all partial frameworks.
3. Build code templates, starting with EU AI Act Article 50 disclosures, EU contract withdrawal buttons, GPC signal handlers, and ROSCA subscription cancellation flows.

This report is a snapshot. It goes stale as deadlines move, so re-run it against EUR-Lex, FTC, and official primary sources rather than relying solely on these dates.

---

## 23. Sources

Every regulation named above, cited to its primary source.

- GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions)
- California Privacy Rights Act: [Cal. Civ. Code Section 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- ROSCA: [15 U.S.C. 8401](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option)
- UK Online Safety Act: [Online Safety Act 2023](https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online)
- Australia Online Safety Act: [Online Safety Act 2021](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA: [Law 15,211/2025](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/)
- India DPDPA: [DPDP Act 2023](https://www.bassberry.com/news/indias-data-privacy-rules-what-your-business-needs-to-know/)
- Singapore PDPA: [PDPA 2012](https://www.twobirds.com/en/insights/2026/singapore/app-stores-in-singapore-required-to-implement-age-assurance-measures)
- South Korea TBA / PIPA: [Telecommunications Business Act Article 22-9](https://developer.apple.com/support/storekit-external-entitlement-kr/)
- China App Filing & CAC: [MIIT App Filing Rules](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/)
