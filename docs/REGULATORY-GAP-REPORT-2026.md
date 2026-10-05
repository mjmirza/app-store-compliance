# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the repository itself. It takes twenty major global and regional regulations that bind mobile and web application developers shipping into key jurisdictions (EU, US Federal and State, UK, Australia, Brazil, India, Singapore, South Korea, China, and Canada), and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight core categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail. Assume the repository is incomplete unless proven otherwise.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems and e-commerce applications, the GPSR mandates that online marketplaces and storefront interfaces clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template General Product Safety Policy to establish product classification criteria, responsible person designation, or recall management protocols.
- **Missing Documentation:**
  The repository is missing specific developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack UI component templates or helper functions for displaying manufacturer identity or product safety warnings on EU storefronts.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address (such as email or website) as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or database schemas for logging product safety incidents, user complaints, recalls, or corrective actions.
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

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU, regardless of where the provider is headquartered. The default compliance window to produce user data is 10 days, but in critical emergency cases, providers are legally required to produce requested data within a strict 8-hour timeline.

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
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating distance financial services contracts from general subscriptions.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
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
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977 / Act 185, Alabama HB 161) regulating minors' access to mobile applications, in-app purchases, and content updates.

Developers must request and process user age categories via Apple's Declared Age Range API or Google's Play Age Signals API and obtain verifiable parental consent before allowing minors to download apps, purchase digital goods, or access major updates. Raw age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025/2026), Texas SB 2420 (2025), Louisiana HB 977 / Act 185 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minor age assurance policy explaining how to process state-specific age bands or handle minor account restrictions.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise developer instructions for integrating Apple's Declared Age Range API and Google's Play Age Signals API within a single multi-platform project.
- **Missing Code:**
  Although rejection patterns contain entries for state laws, mock client implementations do not integrate `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  Onboarding flows do not display required state disclosures explaining that user age categories are requested to comply with state accountability laws and that parental consent is required for minors.
- **Missing Logging:**
  There is no secure backend system designed to log parental consent receipts, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests to verify that minor accounts are blocked from premium features or in-app purchases without valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to present to state authorities.
- **Missing Audit Trail:**
  An immutable audit trail to record historical rollouts of age-assurance features, changes in consent policies, and records of immediate verification data deletions is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy specifying state-level requirements and data minimization.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API.
3. Build database triggers and automated procedures to purge raw age-verification data immediately after confirming age category.
4. Establish automated unit tests to verify that minor age categories block in-app billing until a valid parental consent flag is processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must ensure a sufficient level of AI literacy among staff and persons dealing with the operation of AI systems.

This requirement applies to all organizations with no headcount carve-out, meaning small development teams and solo creators are equally bound. Effective compliance requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Literacy Policy defining competency expectations for engineering teams.
- **Missing Documentation:**
  The repository lacks developer-facing guidelines explaining obligations under Article 4 or how to maintain team competency in AI safety and risk evaluation.
- **Missing Code:**
  The repository contains no CLI scripts or automated checks to verify whether a team's AI literacy log exists and remains up to date.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or vendor agreements do not disclose organizational commitment to AI literacy standards under Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry (`AI_LITERACY_LOG.md`) to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no internal lints or pre-commit hooks to check that team members committing AI feature code possess valid literacy records.
- **Missing Evidence:**
  The playbook provides no example of acceptable evidence, such as a completed training log, course completion records, or a written competency assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting annual reviews of the AI literacy policy or updates to team training records over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review team literacy records annually.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for AI systems, taking full legal effect on 2 August 2026.

Under Article 50(1), providers must ensure that AI systems intended to interact directly with natural persons inform users that they are interacting with an AI system. Article 50(2) mandates that outputs of generative AI systems must be marked in a machine-readable format and detectable as artificially generated or manipulated. Article 50(4) requires deployers of deepfakes to disclose that content has been artificially generated or manipulated.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Transparency and Disclosure Policy outlining when user notices must appear and how generated media must be marked.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed developer instructions on implementing C2PA metadata or machine-readable watermarks.
- **Missing Code:**
  Codebase templates do not include helper classes or middleware layers to inject machine-readable watermarks or C2PA provenance metadata into generated text, audio, image, or video assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display required immediate disclosures ("You are interacting with an AI assistant") at the time of first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was displayed to a specific user session.
- **Missing Testing:**
  Existing test runner scripts do not check for synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository lacks evidence artifacts, such as independent verification reports of content moderation filters or proof of watermark retention across encoding pipelines.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, model updates, vendor audits, and modifications to transparency disclosures is absent.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency Policy mandating direct user disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that machine-readable compliance headers are properly set and preserved.

---

## 7. US Amended COPPA Rule (16 CFR Part 312)

### 7.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) amended the Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312) with a final rule effective 23 June 2025 and general compliance mandatory on 22 April 2026.

The updated Rule expands personal information to include biometric identifiers and government issued IDs, requires separate opt-in consent for third-party disclosures, mandates written data retention policies with prohibition on indefinite retention, and requires a written information security program with annual risk assessments.

Official Citation: 16 CFR Part 312; Federal Register 90 FR 16918 (22 April 2025).

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive Children's Privacy and Data Retention Policy conforming to the 2026 amended COPPA Rule.
- **Missing Documentation:**
  Checklists mention basic COPPA requirements but lack detailed guidance on separate opt-in consent for targeted ads, biometric data handling, and written security program requirements.
- **Missing Code:**
  Code templates do not include dual-consent modalities (separate consent for core functionality vs. third-party disclosures) or automated data retention/purging workers.
- **Missing Disclosure:**
  Direct notice and privacy policy templates do not clearly break out third-party disclosure opt-ins or explicitly declare biometric data practices.
- **Missing Logging:**
  Backend schemas do not log separate opt-in states for third-party ad sharing versus core service collection, nor do they log automated data retention purge events.
- **Missing Testing:**
  Test suites do not simulate under-13 user flows to verify that third-party tracking SDKs remain disabled unless separate parental opt-in is granted.
- **Missing Evidence:**
  The repository contains no template written information security program (WISP), annual risk assessment checklist, or data retention schedule.
- **Missing Audit Trail:**
  There is no immutable audit trail tracking parental consent receipts, consent revocations, or automated child data deletion logs.

### 7.3 Remediation and Action Plan
1. Draft a complete COPPA 2026 Compliance Policy including a written data retention policy and information security program template.
2. Implement dual-consent UI components that separate core operational consent from third-party advertising opt-ins.
3. Add automated database purge tasks to delete child personal data once the specified retention period expires.
4. Build integration tests verifying SDK initialization flags respect parental opt-in states.

---

## 8. EU Digital Markets Act (DMA)

### 8.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms (including Apple App Store and Google Play) and grants developers rights to distribute apps through alternative app marketplaces, web distribution, and utilize alternative payment systems or external purchase steering.

For developers utilizing DMA entitlements in the EU (such as `com.apple.developer.storekit.external-purchase-link`), strict reporting, disclosure sheet presentation, and compliance terms apply.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Alternative Distribution and External Offer Policy for developers choosing to ship outside standard store billing.
- **Missing Documentation:**
  The repository lacks step-by-step developer guides on wiring the External Purchase Server API or managing marketplace notarization workflows.
- **Missing Code:**
  Codebase templates do not include native implementation examples calling Apple's `ExternalPurchaseCustomLink` API or handling alternative marketplace entitlement checks.
- **Missing Disclosure:**
  In-app UI flows do not provide compliant modal sheets informing users that transactions occur outside the App Store or Google Play ecosystems.
- **Missing Logging:**
  There are no server-side logging schemas designed to track external purchase link taps, transaction tokens, or monthly reporting payloads required by Apple/Google.
- **Missing Testing:**
  No automated tests exist to verify that external purchase links properly invoke disclosure sheets or that IAP and external links are not co-mingled on the same storefront.
- **Missing Evidence:**
  The repository lacks templates for reporting external sales transactions to gatekeepers within the required 15-day monthly window.
- **Missing Audit Trail:**
  An audit trail tracking entitlement requests, gatekeeper agreement acceptances, and monthly transaction report filings is absent.

### 8.3 Remediation and Action Plan
1. Create a detailed DMA Developer Integration Guide covering entitlements, notarization, and alternative billing rules.
2. Implement code helpers for calling `ExternalPurchaseCustomLink` and handling gatekeeper disclosure sheets.
3. Establish automated server scripts to aggregate external sales and generate monthly transaction reports for gatekeeper compliance.
4. Add unit tests ensuring store billing and external offer links are mutually exclusive per storefront.

---

## 9. EU Digital Services Act (DSA - Trader Status)

### 9.1 Regulatory Overview and Background
Articles 30 and 31 of the EU Digital Services Act (Regulation (EU) 2022/2065) require online platforms (including app stores) to collect, verify, and display trader identity and contact information for all entities distributing apps to EU consumers.

Developers distributing apps in the EU must declare trader or non-trader status, provide verified business details (address, phone, email, payment account), and keep this information accurate to prevent app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no formal DSA Trader Status Determination Policy to help organizations evaluate whether their distribution meets trader criteria under EU law.
- **Missing Documentation:**
  Documentation mentions DSA trader deadlines but lacks a detailed walkthrough of the verification process in App Store Connect and Google Play Console.
- **Missing Code:**
  The guard script lacks automated checks against project metadata files to confirm that DSA trader declarations are complete prior to release.
- **Missing Disclosure:**
  Product page metadata templates do not include standardized fields for trader contact information, registration numbers, or consumer right disclosures.
- **Missing Logging:**
  There is no logging system to track when trader verification documents were submitted, approved, or due for annual re-verification.
- **Missing Testing:**
  Automated metadata audit scripts (`scripts/metadata-audit.py`) do not check for missing DSA trader status flags in App Store Connect exports.
- **Missing Evidence:**
  The repository provides no templates or examples of acceptable trader verification evidence (such as trade register extracts or D-U-N-S confirmation records).
- **Missing Audit Trail:**
  An audit trail documenting trader status declarations, verification submissions, and platform verification approvals is missing.

### 9.3 Remediation Plan
1. Add a DSA Trader Decision Matrix to `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Update `scripts/metadata-audit.py` to flag missing DSA trader declarations in store listing metadata.
3. Maintain documented copies of trader verification credentials in a secure repository compliance folder.

---

## 10. European Accessibility Act (EAA)

### 10.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became enforceable on 28 June 2025. It mandates that mobile applications and digital services in scope (including e-commerce, banking, travel, and media) conform to accessibility requirements specified in harmonised standard EN 301 549 (built on WCAG 2.1 Level AA).

EN 301 549 Chapter 11 sets specific non-web software and mobile app rules, including screen reader support, scalable text without clipping, sufficient color contrast, and an accessible published accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an organizational Accessibility Compliance Policy committing to EN 301 549 and WCAG 2.1 Level AA standards.
- **Missing Documentation:**
  Checklists cover basic Apple/Android accessibility rules but do not provide explicit mappings to EN 301 549 Chapter 11 mobile software requirements.
- **Missing Code:**
  Repository UI components lack comprehensive accessibility labels, traits, dynamic type scaling support, or high-contrast theme overrides.
- **Missing Disclosure:**
  There is no template Accessibility Statement (conforming to EN 301 549 Annex B and C) to be published in-app and on product web pages.
- **Missing Logging:**
  No logging mechanisms exist to capture accessibility feedback, user bug reports, or assistive technology compatibility issues.
- **Missing Testing:**
  While `scripts/accessibility-audit.py` exists, it is not wired into the mandatory submission guard hook, allowing accessibility regressions to bypass automated blocks.
- **Missing Evidence:**
  The repository lacks formal Accessibility Conformance Reports (VPAT / EN 301 549 evaluation sheets) proving third-party audit verification.
- **Missing Audit Trail:**
  An audit trail tracking accessibility audit history, remediated contrast issues, and screen reader testing sessions is absent.

### 10.3 Remediation Plan
1. Formulate an EN 301 549 Mobile Accessibility Policy and template Accessibility Statement.
2. Wire `scripts/accessibility-audit.py` into automated CI workflows to block releases with critical accessibility failures.
3. Create template VPAT / EN 301 549 Conformance Evaluation sheets in the documentation directory.

---

## 11. California Privacy Rights Act (CPRA) & CPPA 2026 Regulations

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA) and enforced by the California Privacy Protection Agency (CPPA) establishes consumer privacy rights and strict business obligations.

The CPPA 2026 regulations enforce automated decision-making technology (ADMT) disclosures, opt-out mechanisms, cybersecurity audits, and mandatory honoring of Global Privacy Control (GPC) opt-out signals.

Official Citation: Cal. Civ. Code Section 1798.100 et seq.; CPPA Regulations (2026).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a California-specific Privacy Policy addendum covering ADMT opt-out rights and sensitive personal information controls.
- **Missing Documentation:**
  Developer guides do not detail how to parse and honor the `Sec-GPC` header in webviews or native app equivalents.
- **Missing Code:**
  Codebase templates do not contain Global Privacy Control signal handlers or native opt-out state managers.
- **Missing Disclosure:**
  In-app privacy notices lack explicit "Do Not Sell or Share My Personal Information" links and "Limit the Use of My Sensitive Personal Information" controls.
- **Missing Logging:**
  Backend systems lack logging schemas for recording GPC opt-out signals, consumer rights requests (know, delete, correct), and opt-out fulfillments.
- **Missing Testing:**
  No automated integration tests exist to confirm that when a GPC signal is received, tracking pixels and ad network SDKs are immediately disabled.
- **Missing Evidence:**
  The repository lacks template Risk Assessment sheets for ADMT and processing of high-risk personal information.
- **Missing Audit Trail:**
  An audit trail tracking consumer privacy request fulfillment within statutory timelines (45 days) is missing.

### 11.3 Remediation Plan
1. Implement a GPC signal listener component for webviews and native network stacks.
2. Add "Do Not Sell/Share" and "Limit Sensitive PI" UI components to mobile settings templates.
3. Build backend logging for GPC signals and consumer rights request workflows.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) regulates the collection, use, safeguarding, handling, and destruction of biometric identifiers and information (such as facial geometry, fingerprints, iris scans, or voiceprints).

BIPA requires written notice, written release prior to collection, a publicly available retention schedule, destruction within 3 years, and prohibits profiting from biometric data. Amending law SB 2979 (effective August 2024) clarifies that multiple collections of the same identifier constitute a single violation.

Official Citation: 740 ILCS 14/ (Biometric Information Privacy Act); SB 2979 (2024).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Biometric Privacy Policy or retention and destruction schedule conforming to BIPA standards.
- **Missing Documentation:**
  Checklists do not provide step-by-step developer guidelines for implementing written consent modals prior to initializing native biometric APIs (LocalAuthentication or BiometricPrompt).
- **Missing Code:**
  Mobile code templates call native biometric authentication without enforcing prior written consent modal sheets or consent state checks.
- **Missing Disclosure:**
  In-app onboarding flows lack explicit biometric notices detailing the specific purpose and duration for which biometric data is captured or processed.
- **Missing Logging:**
  Backend schemas do not log biometric consent receipts, written release confirmations, or automated destruction timestamps.
- **Missing Testing:**
  Test suites do not check whether biometric SDK calls are gated by confirmed consent flags in local storage or backend user profiles.
- **Missing Evidence:**
  The repository contains no template Biometric Written Release agreements or publicly accessible retention schedule documents.
- **Missing Audit Trail:**
  An immutable audit trail documenting biometric policy updates, user consent receipts, and biometric template deletion events is absent.

### 12.3 Remediation Plan
1. Draft a BIPA-compliant Biometric Privacy Policy and public retention schedule template.
2. Build UI consent modals that must be executed and logged prior to invoking native iOS/Android biometric authentication APIs.
3. Establish automated unit tests ensuring biometric authentication hooks verify valid consent state.

---

## 13. US Subscription Cancellation (Negative Option / ROSCA / State Laws)

### 13.1 Regulatory Overview and Background
While the FTC's federal "click-to-cancel" negative option rule amendment was vacated on procedural grounds in July 2025, online subscription cancellation remains heavily enforced under ROSCA (Restore Online Shoppers' Confidence Act), FTC Act Section 5, and state laws (California, New York, Massachusetts).

These laws mandate that canceling a subscription must be at least as easy as signing up ("click to cancel"), requiring a simple, frictionless, online self-service cancellation mechanism without requiring phone calls, physical mail, or deceptive dark patterns.

Official Citations: 15 U.S.C. Section 8401 et seq. (ROSCA); Cal. Bus. & Prof. Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Online Subscription Cancellation Policy establishing frictionless self-service termination standards for web-billed and companion subscriptions.
- **Missing Documentation:**
  Developer guides do not detail rules against dark patterns (e.g., forced retention surveys, multi-step confirm dialogs) in subscription cancellation flows.
- **Missing Code:**
  Billing code templates do not provide a 1-click or frictionless self-service cancellation endpoint or account UI panel.
- **Missing Disclosure:**
  Subscription paywalls fail to clearly disclose auto-renewal terms, cancellation mechanisms, and recurring charge schedules in immediate proximity to the call-to-action button.
- **Missing Logging:**
  Server schemas lack audit logs capturing cancellation request timestamps, confirmation delivery, and immediate subscription state transitions.
- **Missing Testing:**
  No end-to-end automated UI tests exist to confirm that users can navigate from account settings to subscription termination in two clicks or fewer.
- **Missing Evidence:**
  The repository lacks templates for automated cancellation confirmation receipts and refund transaction logs.
- **Missing Audit Trail:**
  An audit trail tracking cancellation flow revisions, retention offer prompt changes, and user cancellation completion rates is absent.

### 13.3 Remediation Plan
1. Formulate a Subscription Transparency and Easy Cancellation Policy.
2. Implement frictionless 1-click self-service cancellation UI components for non-IAP subscription management pages.
3. Build automated UI test flows verifying that cancellation paths contain no administrative obstacles or dark patterns.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the ICO Age Appropriate Design Code (Children's Code) set strict child safety and privacy requirements for services likely to be accessed by children under 18 in the UK.

Key duties include enforcing highly effective age assurance for age-restricted content, establishing high privacy settings by default, disabling geolocation and profiling by default, conducting Data Protection Impact Assessments (DPIAs), and reporting CSEA content.

Official Citations: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no UK Children's Code Compliance Policy or Online Safety Risk Assessment framework.
- **Missing Documentation:**
  Checklists do not detail the 15 standards of the ICO Children's Code or Ofcom's highly effective age assurance specifications.
- **Missing Code:**
  Codebase templates do not automatically apply "high privacy by default" settings (geolocation off, profiling off, public profile hidden) when a UK child account is detected.
- **Missing Disclosure:**
  Child-facing UI templates do not provide age-appropriate explanations of privacy rights, data collection, or safety reporting tools.
- **Missing Logging:**
  There are no server schemas to log child safety reports, content moderation actions, or age assurance verification methods without retaining raw age documents.
- **Missing Testing:**
  Test suites do not verify that default user profile creation sets geolocation and profiling flags to disabled for accounts under 18 in the UK.
- **Missing Evidence:**
  The repository lacks template Data Protection Impact Assessments (DPIAs) tailored to the UK Children's Code.
- **Missing Audit Trail:**
  An audit trail documenting annual online safety risk assessments, moderation log reviews, and age assurance method evaluations is missing.

### 14.3 Remediation Plan
1. Create a UK Children's Code Developer Guide and template DPIA document.
2. Build default user profile configuration modules that enforce high-privacy defaults based on jurisdiction and age.
3. Add automated test cases ensuring geolocation and profiling features are disabled by default for UK child profiles.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 (enforceable from December 2025 / 2026) mandates that age-restricted social media platforms take reasonable steps to prevent under-16s from holding accounts.

The eSafety Commissioner requires waterfall age assurance methods, strict ringfencing and immediate destruction of age verification data, and compliance with registered App Distribution Services and Equipment Industry Codes.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024; eSafety Industry Codes.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Minimum Age Compliance Policy and Data Destruction Protocol for age verification data.
- **Missing Documentation:**
  Checklists do not detail eSafety Commissioner waterfall age assurance guidelines or store-level download blocking requirements.
- **Missing Code:**
  Code templates do not contain age-gating modules or API connectors for Australian age verification systems.
- **Missing Disclosure:**
  Onboarding flows do not disclose to Australian users why age verification is conducted or guarantee the immediate destruction of verification credentials.
- **Missing Logging:**
  Backend schemas lack logging mechanisms to record age verification completion status while strictly excluding stored identity credentials.
- **Missing Testing:**
  No automated tests exist to confirm that under-16 Australian user profiles are blocked from social feature access.
- **Missing Evidence:**
  The repository lacks templates for age verification data destruction logs or eSafety compliance reporting summaries.
- **Missing Audit Trail:**
  An audit trail recording age-assurance system updates, privacy impact reviews, and data destruction verification is absent.

### 15.3 Remediation Plan
1. Draft an Australian Age Assurance Policy and Data Ringfencing Protocol.
2. Build age-gating UI components that process age signals and immediately discard raw identity artifacts.
3. Implement unit tests confirming that social features remain disabled for Australian under-16 accounts.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025 and Decreto 12.880, enforceable from March 2026) regulates child and adolescent protection on digital platforms, enforced by the ANPD.

It bans self-declaration checkboxes for age verification, requiring document verification, facial age estimation, or CPF database checks. Operating systems and app stores must expose free age signals, seek guardian authorization, and block gambling/18+ apps for minors.

Official Citation: Lei n. 15.211/2025; Decreto n. 12.880 (18 March 2026).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Brazil Digital ECA Compliance Policy or Guardian Consent Policy.
- **Missing Documentation:**
  Documentation lacks developer guides for handling Brazil-specific age signals returned by the Google Play Age Signals API or Apple Declared Age Range API.
- **Missing Code:**
  Codebase templates do not integrate CPF or facial age estimation API handlers, nor do they enforce 18+ app blocks on Brazilian storefronts.
- **Missing Disclosure:**
  UI templates lack Portuguese-language age verification notices and guardian consent requests required under Decreto 12.880.
- **Missing Logging:**
  Backend schemas do not log ANPD-compliant age verification method IDs or guardian authorization timestamps.
- **Missing Testing:**
  Automated tests do not verify that Brazilian accounts returning minor age bands are blocked from 18+ features or loot box mechanics.
- **Missing Evidence:**
  The repository lacks templates for ANPD age assurance compliance reports or guardian consent audit files.
- **Missing Audit Trail:**
  An audit trail tracking Brazilian age assurance implementations, policy updates, and ANPD inspection records is missing.

### 16.3 Remediation Plan
1. Formulate a Brazil Digital ECA Integration Guide and Portuguese UI consent templates.
2. Implement backend handlers to process Google Play Age Signals API signals for Brazilian user sessions.
3. Add automated test cases ensuring loot box and 18+ content remain locked for Brazilian minor profiles.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 & Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 establish a comprehensive data protection regime, with consent and children's data provisions taking effect progressively through May 2027.

Key mandates include mandatory verifiable parental consent (e.g., via DigiLocker) before processing data of anyone under 18, absolute prohibition on behavioral tracking and targeted advertising to children, and appointment of Data Protection Officers.

Official Citation: Act No. 22 of 2023; DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no India DPDPA Data Protection Policy or Children's Consent Framework.
- **Missing Documentation:**
  Checklists do not detail the 22 official languages consent notice requirement or DigiLocker integration steps for parental consent.
- **Missing Code:**
  Code templates do not include multi-language consent notice renderers or tracking disablement hooks for Indian minor accounts.
- **Missing Disclosure:**
  Paywall and signup UI templates lack explicit consent notices formatted in specified Indian languages detailing data processing items.
- **Missing Logging:**
  Backend schemas do not log parental consent verification IDs, consent manager tokens, or data principal rights fulfillment events.
- **Missing Testing:**
  No automated tests exist to confirm that when an Indian account is flagged under 18, all ad network SDKs and tracking pixels are completely disabled.
- **Missing Evidence:**
  The repository lacks template Data Protection Impact Assessment (DPIA) files and DPO appointment records for Indian entities.
- **Missing Audit Trail:**
  An audit trail recording consent manager registrations, parental consent verification logs, and data erasure requests is missing.

### 17.3 Remediation Plan
1. Draft a DPDPA Compliance Policy and multi-language consent notice template structure.
2. Build consent notice UI components supporting official Indian languages and tracking disablement hooks.
3. Establish automated unit tests verifying ad tracking is disabled for under-18 Indian user profiles.

---

## 18. Singapore Personal Data Protection Act (PDPA & IMDA Code)

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services regulate data protection and age assurance.

From 1 April 2026, app distribution services and platform operators must implement age assurance measures (e.g., credit card or bank verification) to screen and prevent users under 18 from downloading age-inappropriate apps, with age data ringfenced and destroyed immediately.

Official Citation: Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety (2025/2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA & IMDA Compliance Policy specifying age assurance and data protection rules.
- **Missing Documentation:**
  Checklists do not detail IMDA app distribution age screening rules or 3-day breach notification duties to the PDPC.
- **Missing Code:**
  Code templates do not include age screening logic or platform age signal listeners for Singapore storefront releases.
- **Missing Disclosure:**
  UI templates do not display required age screening disclosures explaining data minimization and immediate credential deletion.
- **Missing Logging:**
  Backend schemas lack logging mechanisms for recording PDPC breach notification workflows or age verification confirmation tokens.
- **Missing Testing:**
  No automated tests exist to verify that Singapore user sessions returning under-18 age signals are blocked from 18+ content downloads.
- **Missing Evidence:**
  The repository lacks template PDPC Personal Data Breach Notification forms and IMDA age assurance audit records.
- **Missing Audit Trail:**
  An audit trail tracking Data Protection Officer actions, breach notifications, and age assurance system audits is absent.

### 18.3 Remediation Plan
1. Create a Singapore PDPA Developer Guide and breach response checklist.
2. Implement native age signal handlers for Singapore App Store and Google Play releases.
3. Add automated test cases ensuring 18+ content access is restricted for Singapore minor user profiles.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendments

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options (allowing third-party payment gateways with reduced commission), while the Personal Information Protection Act (PIPA) amendments (enforceable September 2026) introduce strict CEO liability, board-approved CPOs, and heavy surcharges.

For alternative payments on the Korea storefront, Apple requires a Korea-specific binary, approved payment providers (KCP, Inicis, Toss, NICE), pre-transaction modal disclosures, and 15-day monthly sales reporting.

Official Citation: Telecommunications Business Act Article 22-9; PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Alternative Billing and PIPA Compliance Policy.
- **Missing Documentation:**
  Checklists do not detail the strict 1-binary Korea requirement (`SKExternalPurchase = "KR"`) or PIPA CPO board-approval mandates.
- **Missing Code:**
  Codebase templates do not contain Korea alternative payment modal implementations or monthly sales reporting aggregators.
- **Missing Disclosure:**
  In-app payment screens lack the required Korean language modal sheet informing users that Apple/Google purchase protections do not apply to third-party billing.
- **Missing Logging:**
  Backend systems lack database schemas to log Korea external purchase transactions, VAT breakdowns, and monthly reporting payloads.
- **Missing Testing:**
  No automated tests exist to confirm that Korea alternative payment binaries properly present the mandatory system modal sheet before launching third-party gateways.
- **Missing Evidence:**
  The repository lacks templates for monthly Korea external purchase sales reports and CPO board appointment resolutions.
- **Missing Audit Trail:**
  An audit trail tracking Korea billing entitlement approvals, monthly reporting submissions, and PIPA compliance audits is missing.

### 19.3 Remediation Plan
1. Draft a South Korea Alternative Payment & PIPA Developer Guide.
2. Build native UI modal sheets for Korea alternative payment flows calling `SKExternalPurchase`.
3. Add automated server scripts to compile monthly sales reports for submission to platform operators.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Measures

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) for all apps distributed in China, requiring a local Chinese business entity or partner.

In addition, CAC (Cyberspace Administration of China) regulations—including PIPL, real-name verification, game Banhao licensing, and the Interim Measures for AI Anthropomorphic Interactive Services (July 2026)—require strict minor mode switching, guardian consent under 14, and bans on virtual companion services for minors.

Official Citation: MIIT Mobile App Filing Notice (2023/2024); CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no China App Distribution Policy or CAC AI Safety & Minor Protection Framework.
- **Missing Documentation:**
  Checklists do not detail MIIT app filing submission steps, local entity requirements, or CAC AI companion bans for minors.
- **Missing Code:**
  Code templates do not include automated "Minors Mode" UI switches, real-name identity verification hooks, or anti-addiction time limit timers.
- **Missing Disclosure:**
  In-app UI templates lack MIIT app filing number displays on splash screens or CAC-mandated minor protection disclosures.
- **Missing Logging:**
  Backend schemas do not log real-name verification status tokens, minor session duration timers, or CAC AI interaction safety filters.
- **Missing Testing:**
  No automated tests exist to verify that switching to Minors Mode restricts chat features, blocks virtual companion APIs, and enforces curfew time locks.
- **Missing Evidence:**
  The repository lacks template MIIT App Filing confirmation records, Banhao game license documentation, or CAC AI security assessment filings.
- **Missing Audit Trail:**
  An audit trail documenting MIIT filing updates, real-name system audits, and CAC compliance reviews is missing.

### 20.3 Remediation Plan
1. Create a China App Distribution & CAC Compliance Guide covering MIIT filing and AI rules.
2. Implement a configurable "Minors Mode" UI module and real-name verification backend interface.
3. Add automated test cases ensuring virtual companion AI features are completely disabled in Minors Mode.

---

## 21. Consolidated Gap Classification Matrix across Twenty Regulatory Frameworks

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step implementation. Missing means the playbook does not carry it at all.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA / CPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety / ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

The honest read. The playbook provides strong documentation and awareness regarding store rejection rules and regulatory deadlines. However, across all twenty frameworks, significant gaps remain in code implementations, automated testing, logging schemas, compliance evidence templates, and immutable audit trails.

---

## 22. Conclusion and Systematic Action Roadmap

The playbook excels at identifying store reviewer rejection patterns. To achieve full enterprise compliance readiness, it must expand beyond store review into post-launch legal enforcement domains across global jurisdictions.

### Priority Action Items
1. **Code & Templates:** Develop native code helpers for DMA external links (`ExternalPurchaseCustomLink`), C2PA watermark injection for AI Act Art 50, and GPC signal listeners.
2. **Automated Testing:** Wire `scripts/accessibility-audit.py` into the main guard hook and build unit tests for age-gating and subscription cancellation flows.
3. **Evidence & Audit Trails:** Build standardized Markdown templates for DPIAs, WISPs, AI Literacy logs, and Law Enforcement response records in a new `templates/compliance/` directory.

---

## 23. Official Primary Sources

Every regulation named above is cited to its official primary source:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Withdrawal Button: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Amended COPPA Rule: [16 CFR Part 312 / 90 FR 16918](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US ROSCA: [15 U.S.C. Section 8401](https://www.govinfo.gov/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap110.htm)
- California Privacy: [CCPA / CPRA Text](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety: [Federal Register of Legislation](https://www.legislation.gov.au/)
- Brazil Digital ECA: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA: [eGazette India G.S.R. 846(E)](https://egazette.gov.in)
- Singapore PDPA: [PDPC Singapore](https://www.pdpc.gov.sg)
- South Korea PIPA: [Korean Law Information Center](https://law.go.kr)
- China CAC AI Measures: [Cyberspace Administration of China](https://www.cac.gov.cn)
