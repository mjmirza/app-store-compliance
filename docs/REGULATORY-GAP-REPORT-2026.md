# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global app store markets, checking honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is systematically audited across eight distinct gap categories:
1. Missing Policy
2. Missing Documentation
3. Missing Code
4. Missing Disclosure
5. Missing Logging
6. Missing Testing
7. Missing Evidence
8. Missing Audit Trail

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

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

The withdrawal button obligation in this Directive attaches to distance financial services contracts, and serves as a strong design default across all consumer subscription models. The statutory withdrawal period is 14 days from contract conclusion. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

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
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

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
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems (including mobile application developers utilizing third-party generative AI APIs) must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with the technical complexity and impact of the AI integration.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable directly to runtime binary code, but helper scripts to check whether an AI literacy training log exists and is current are absent.
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
  An unalterable audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, regulates designated gatekeepers (Apple, Alphabet) and establishes rights for business users. In response, Apple and Google have introduced alternative store distribution, external purchase link entitlements, custom link sheets, and updated fee structures in the EU.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council of 14 September 2022 on contestable and fair markets in the digital sector.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive DMA EU Alternative Distribution Policy guiding developers on when to adopt alternative payment link sheets versus standard store billing.
- **Missing Documentation:**
  Checklists mention DMA entitlements but lack step-by-step developer guides for implementing the `com.apple.developer.storekit.external-purchase-link` entitlement or handling the CTC 5 percent reporting requirements.
- **Missing Code:**
  The repository lacks native code modules for handling the EU external purchase link sheet modal, parameter pass-through, or commission reporting telemetry.
- **Missing Disclosure:**
  In-app paywall UI templates do not include required EU DMA modal disclosures informing users when they are leaving the native app store payment environment.
- **Missing Logging:**
  No database schema or backend logging handler exists to record external purchase link clicks, transaction tokens, or fee reporting calculations.
- **Missing Testing:**
  The test suite contains no automated UI tests to verify that the external payment link sheet opens correctly and passes required legal attribution parameters.
- **Missing Evidence:**
  The repository lacks sample fee reporting spreadsheets, entitlement grant confirmations, or proof of gatekeeper compliance filings.
- **Missing Audit Trail:**
  There is no version-controlled audit trail tracking changes to DMA link sheets, fee structure acceptances, or reporting submissions.

### 7.3 Remediation and Action Plan
1. Draft an EU Digital Markets Act compliance guide covering alternative distribution and payment link obligations.
2. Provide reusable UI components for external purchase link sheets and modal notices.
3. Implement backend transaction logging for external commission calculations.
4. Add automated test scripts verifying external link sheet trigger logic and parameter integrity.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (DSA), Regulation (EU) 2022/2065, mandates trader status verification (D-U-N-S, phone, email publishing) for developers selling digital goods/services in the EU, alongside notice-and-action mechanisms for user-generated content (UGC) platforms.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council of 19 October 2022 on a Single Market For Digital Services.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal DSA Compliance Policy defining trader status criteria and notice-and-action handling procedures for illegal content.
- **Missing Documentation:**
  Documentation mentions trader status but does not provide complete developer guidelines for setting up public trader disclosures or handling DSA complaint mechanisms.
- **Missing Code:**
  No backend code or API endpoints exist in the repository to power a DSA-compliant notice-and-action mechanism or illegal content reporting interface.
- **Missing Disclosure:**
  Storefront and in-app metadata templates do not include standard trader disclosure layout fields (address, phone, verified email, registration details).
- **Missing Logging:**
  There are no logging schemas or incident management workflows to record incoming DSA notices, counter-notices, content removals, or user suspensions.
- **Missing Testing:**
  No automated tests verify that trader disclosures are present on product detail pages or that UGC reporting flows function without error.
- **Missing Evidence:**
  The playbook provides no templates for annual DSA transparency reports, trader verification proofs, or content moderation decision records.
- **Missing Audit Trail:**
  An unalterable audit log for tracking content moderation decisions, appeal outcomes, and trader status updates is absent.

### 8.3 Remediation and Action Plan
1. Add a DSA Trader Verification & Notice-and-Action Policy template.
2. Include UI and metadata templates containing mandatory trader address, contact, and registration disclosures.
3. Build mock backend endpoints for logging and handling content notices and user appeals.
4. Create test cases to validate UGC reporting and trader disclosure rendering.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, entered into force on 28 June 2025. It mandates accessibility compliance across mobile apps, e-commerce, banking, and digital services reaching EU consumers, referencing harmonised standard EN 301 549 and WCAG 2.1 Level AA.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council of 17 April 2019 on the accessibility requirements for products and services.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an explicit Corporate Accessibility Policy establishing organization-wide commitment to WCAG 2.1 AA and EN 301 549 standards.
- **Missing Documentation:**
  While accessibility guidelines exist, developer documentation lacks complete mapping tables linking mobile UI components to specific EN 301 549 clauses.
- **Missing Code:**
  Static accessibility scripts check basic labels, but sample UI templates in the repo do not consistently include Dynamic Type scaling, semantic grouping, or high-contrast overrides.
- **Missing Disclosure:**
  Templates do not include a published, legally compliant Accessibility Statement template disclosing conformance status, known limitations, and contact feedback paths.
- **Missing Logging:**
  No schema exists to capture, categorize, and log user accessibility feedback, barrier reports, or remediation requests.
- **Missing Testing:**
  Automated accessibility tests coverage is limited to basic rules and lacks automated screen-reader navigation or color-contrast test harnesses.
- **Missing Evidence:**
  The repository contains no sample Accessibility Conformance Reports (VPAT / EN 301 549 ACR) or third-party accessibility audit certificates.
- **Missing Audit Trail:**
  There is no historical log recording accessibility audit results, detected regressions, or component-level accessibility fixes across release cycles.

### 9.3 Remediation and Action Plan
1. Formulate a comprehensive Accessibility Policy and published Accessibility Statement template.
2. Enhance `scripts/accessibility-audit.py` to cover Dynamic Type, touch target minimums, and screen-reader semantics.
3. Supply completed VPAT / EN 301 549 Accessibility Conformance Report templates.
4. Integrate automated accessibility regression testing into the CI/CD pipeline.

---

## 10. US Children's Online Privacy Protection Act (Amended COPPA Rule)

### 10.1 Regulatory Overview and Background
The FTC's Amended COPPA Rule (16 CFR Part 312) expands child privacy protections by explicitly adding biometric identifiers to personal information, requiring separate opt-in consent for third-party disclosures and targeted advertising, and mandating written data retention policies and information security programs.

Official Citation: FTC 16 CFR Part 312, Children's Online Privacy Protection Rule.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a dedicated Written Children's Data Retention and Information Security Policy compliant with the Amended COPPA Rule.
- **Missing Documentation:**
  Checklists mention COPPA but lack detailed developer guides on implementing separate opt-in consent for third-party disclosures versus core app functionality.
- **Missing Code:**
  Mock onboarding code does not include split consent UI flags separating core functionality consent from third-party advertising or analytics consent.
- **Missing Disclosure:**
  Privacy notice templates do not explicitly disclose biometric data collection or separate third-party data sharing practices for child-directed apps.
- **Missing Logging:**
  There are no backend schemas to record verifiable parental consent (VPC) methods, separate opt-in selections, or automated data deletion schedules.
- **Missing Testing:**
  No automated unit tests exist to confirm that third-party SDKs are disabled for minor accounts prior to obtaining verifiable parental consent.
- **Missing Evidence:**
  The repository lacks sample Verifiable Parental Consent (VPC) records, FTC Safe Harbor audit reports, or written retention schedules.
- **Missing Audit Trail:**
  An immutable audit trail recording consent grants, consent revocations, and data retention deletion executions is missing.

### 10.3 Remediation and Action Plan
1. Draft an Amended COPPA Compliance Policy including written retention schedules.
2. Implement split-consent UI logic for child-directed apps in mobile code templates.
3. Establish database schemas for tracking verifiable parental consent and SDK initialization gates.
4. Create unit tests verifying SDK suppression in child profiles.

---

## 11. US California Privacy Rights Act (CPRA) & CPPA Regulations

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended by the CPRA (Cal. Civ. Code section 1798.100 et seq.) and the 2026 CPPA Regulations enforce strict rules around Global Privacy Control (GPC) signals, Automated Decision-Making Technology (ADMT) opt-outs, Notice at Collection, and sensitive personal information limits.

Official Citation: California Consumer Privacy Act (CCPA/CPRA), Cal. Civ. Code section 1798.100 et seq.; 11 CCR section 7000 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive California Privacy Rights Policy detailing consumer request handling protocols (access, deletion, correction, opt-out).
- **Missing Documentation:**
  Developer guides do not detail technical steps for parsing `Sec-GPC` headers or exposing ADMT opt-out toggles inside mobile app settings.
- **Missing Code:**
  No middle-tier code or client helper exists to detect Global Privacy Control (GPC) HTTP headers or system-level opt-out signals automatically.
- **Missing Disclosure:**
  UI templates lack explicit "Notice at Collection" components detailing categories of personal and sensitive information collected and retention periods.
- **Missing Logging:**
  No database logging schema exists to record consumer opt-out requests, GPC signal recognitions, or ADMT opt-out selections.
- **Missing Testing:**
  No automated integration tests verify that sending a GPC signal disables ad-tracking or analytics events.
- **Missing Evidence:**
  The repo provides no templates for annual CCPA consumer request metrics reports or ADMT risk assessment documentation.
- **Missing Audit Trail:**
  There is no unalterable log recording consumer privacy request receipts, verification steps, and fulfillment timestamps.

### 11.3 Remediation and Action Plan
1. Create a California Privacy Rights & ADMT Opt-Out Policy.
2. Build GPC header detection and setting toggle code modules.
3. Add Notice at Collection UI components and retention period disclosures.
4. Implement automated tests verifying GPC header handling and ad-tracker suppression.

---

## 12. US Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, use, safeguarding, handling, and destruction of biometric identifiers and information (facial geometry, fingerprints, voiceprints). It requires written notice, written release, a publicly available retention schedule, and immediate destruction.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no standalone Biometric Data Privacy Policy or written destruction schedule compliant with BIPA section 15(a).
- **Missing Documentation:**
  Developer guides lack detailed instructions on handling device-native biometric authentication (Face ID / Touch ID / BiometricPrompt) versus custom biometric data collection.
- **Missing Code:**
  Codebase templates do not include written consent modal sheets or biometric consent flag checks prior to invoking biometric SDKs.
- **Missing Disclosure:**
  UI templates do not display explicit BIPA disclosures detailing the specific biometric identifier collected, purpose, and retention term.
- **Missing Logging:**
  No backend logging schema exists to record written release grants, timestamped biometric consents, or scheduled deletion events.
- **Missing Testing:**
  Automated tests do not verify that biometric data capture functions fail or abort when consent flags are unset.
- **Missing Evidence:**
  The repo contains no sample written releases, biometric risk assessments, or proof of zero-storage native biometric pass-through.
- **Missing Audit Trail:**
  An immutable audit trail recording consent acquisitions and biometric data deletion events is absent.

### 12.3 Remediation and Action Plan
1. Draft a BIPA-compliant Biometric Data Policy and Public Retention Schedule template.
2. Create reusable Biometric Written Release modal UI components.
3. Add native code hooks distinguishing local device hardware authentication from server-side biometric processing.
4. Add unit tests ensuring biometric features remain locked until explicit consent is recorded.

---

## 13. US Subscription Cancellation Rules (FTC Click-to-Cancel / State Laws)

### 13.1 Regulatory Overview and Background
Federal Trade Commission (FTC) negative option rules and state subscription cancellation laws (California SB 313 / AB 2863) require recurring subscription sellers to provide a simple, mechanism to cancel that is at least as easy to use as the mechanism used to initiate the subscription ("click-to-cancel"), alongside annual reminders and explicit consent.

Official Citation: FTC Rule on Use of Negative Option Plans, 16 CFR Part 425; Cal. Bus. & Prof. Code section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a formal Subscription Management and Cancellation Policy outlining click-to-cancel compliance.
- **Missing Documentation:**
  Checklists mention subscription disclosures but lack developer guidance on friction-free, self-service cancellation paths.
- **Missing Code:**
  Billing code templates do not include a direct, self-service "Cancel Subscription" button or API handler within user account settings.
- **Missing Disclosure:**
  Paywall UI templates do not consistently display prominent pre-consent disclosures containing full price, renewal frequency, and cancellation instructions.
- **Missing Logging:**
  There is no schema to log subscription signup disclosures, consent checkmarks, cancellation button clicks, and confirmation notices.
- **Missing Testing:**
  No automated UI tests verify that the cancellation path requires no more steps than the signup path.
- **Missing Evidence:**
  The playbook provides no sample cancellation receipts, annual renewal reminder email templates, or pre-consent disclosure logs.
- **Missing Audit Trail:**
  An unalterable audit trail tracking subscription policy updates, paywall changes, and historical cancellation processing times is missing.

### 13.3 Remediation and Action Plan
1. Draft a Subscription Cancellation Policy and Paywall Disclosure Guide.
2. Implement reusable paywall and account-settings cancellation components.
3. Create backend logging schemas for tracking subscription consent and cancellation events.
4. Add end-to-end UI tests validating one-click subscription cancellation flows.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and the ICO Age Appropriate Design Code (Children's Code) mandate highly effective age assurance, strict content moderation, high privacy settings by default, data minimization, turning off geolocation and profiling by default, and conducting mandatory Data Protection Impact Assessments (DPIAs) for services likely to be accessed by children in the UK.

Official Citation: UK Online Safety Act 2023 (c. 50); ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a dedicated UK Children's Privacy and Online Safety Policy.
- **Missing Documentation:**
  Developer guides do not provide step-by-step instructions for completing an ICO-compliant Data Protection Impact Assessment (DPIA).
- **Missing Code:**
  Mobile code templates do not include automatic profile default enforcers (turning off profiling, location, and targeted ads for UK minor accounts).
- **Missing Disclosure:**
  UI templates lack child-friendly privacy notices and clear safety warning indicators suitable for different age tiers.
- **Missing Logging:**
  No backend schema exists to record age assurance verification outcomes, child safety risk flags, or DPIA mitigation steps.
- **Missing Testing:**
  Test suites lack automated verification that default account settings for UK child profiles remain strictly restricted.
- **Missing Evidence:**
  The repository contains no sample DPIA documents, ICO compliance self-assessments, or age assurance accuracy evaluation records.
- **Missing Audit Trail:**
  An unalterable log tracking child safety updates, age assurance configuration changes, and DPIA revisions is missing.

### 14.3 Remediation and Action Plan
1. Draft a UK Online Safety & Children's Code Policy template and DPIA guide.
2. Implement code utilities enforcing high-privacy defaults for UK child profiles.
3. Include age-appropriate child privacy notice UI components.
4. Add automated test routines verifying privacy-by-default enforcement for UK users.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australian Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from having accounts, mandates robust age assurance, and strictly requires the ringfencing and immediate destruction of age assurance data.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Under-16 Minimum Age Policy outlining platform obligations and age assurance data destruction rules.
- **Missing Documentation:**
  Checklists do not provide developer instructions on identifying Australian social media accounts or configuring age assurance gateways.
- **Missing Code:**
  Codebase templates do not contain age gate logic blocking under-16 account creation for Australian IP addresses or store regions.
- **Missing Disclosure:**
  Onboarding templates lack Australian age restriction notices explaining the legal prohibition and age verification requirement.
- **Missing Logging:**
  No logging schema exists to record age verification attempts while ensuring immediate purge of underlying identity documents.
- **Missing Testing:**
  No automated tests verify that Australian accounts indicating age under 16 are blocked from account creation.
- **Missing Evidence:**
  The repo contains no sample age assurance audit records, data destruction certifications, or eSafety Commissioner compliance submissions.
- **Missing Audit Trail:**
  An immutable audit trail recording age gate enforcement events and data purge confirmation hashes is absent.

### 15.3 Remediation and Action Plan
1. Formulate an Australian Minimum Age Compliance Policy and Data Purge Protocol.
2. Implement under-16 age gate components in onboarding code templates.
3. Build database cleanup routines enforcing zero-retention for age verification identity data.
4. Add automated tests verifying Australian under-16 account blocking.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12,880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025 and Decreto 12,880) requires digital products to implement verified age assurance (document check, facial estimation, CPF check), prohibits self-declaration check-boxes, mandates age-range signals for app store downloads, and requires parental authorization for minor accounts.

Official Citation: Lei n. 15.211/2025; Decreto n. 12.880 de 18 de marco de 2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazilian Child and Adolescent Digital Protection Policy.
- **Missing Documentation:**
  Developer guides lack detailed instructions on replacing self-declaration checkboxes with approved age verification mechanisms in Brazil.
- **Missing Code:**
  Code templates do not integrate with Brazil's OS-level age signal APIs or provide CPF / facial estimation verification hooks.
- **Missing Disclosure:**
  UI templates lack required Portuguese-language disclosures explaining age verification duties and parental consent requirements.
- **Missing Logging:**
  No logging schema exists to record ANPD-compliant age verification outcomes and parental consent tokens.
- **Missing Testing:**
  Test scripts do not check for the presence of mandatory Brazilian age verification screens or check-box prohibitions.
- **Missing Evidence:**
  The repo provides no sample ANPD compliance reports, age verification accuracy audits, or parental consent documentation.
- **Missing Audit Trail:**
  An immutable audit trail recording verification events and parental authorization grants is missing.

### 16.3 Remediation and Action Plan
1. Draft a Brazilian Digital ECA Compliance Policy.
2. Build UI components supporting ANPD-compliant age verification flows and OS age signal integration.
3. Implement backend consent logging and data destruction triggers.
4. Add automated unit tests verifying the prohibition of self-declaration checkboxes for Brazilian users.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and DPDP Rules 2025 mandate verifiable parental consent for processing data of individuals under 18 through government-backed mechanisms (e.g., DigiLocker), prohibit behavioral tracking and targeted ads directed at children, and require interoperability with registered Consent Managers.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Personal Data Processing and Minor Protection Policy.
- **Missing Documentation:**
  Developer guides do not detail technical requirements for integrating with India Consent Managers or DigiLocker parental verification.
- **Missing Code:**
  Codebase templates do not contain Consent Manager API interoperability layers or ad-tracking suppression for Indian minor profiles.
- **Missing Disclosure:**
  Onboarding templates lack itemized, multilingual notice disclosures required under DPDPA section 5 in English and 22 scheduled languages.
- **Missing Logging:**
  No schema exists to capture consent tokens, language selections, withdrawal notices, or Consent Manager API calls.
- **Missing Testing:**
  Test suites lack automated checks verifying that behavioral ad tracking is suppressed for Indian users under 18.
- **Missing Evidence:**
  The repository contains no sample Data Protection Impact Assessments, Consent Manager integration certificates, or Data Protection Officer (DPO) records.
- **Missing Audit Trail:**
  An unalterable audit log recording consent notices served, parental consent verified, and withdrawal requests executed is absent.

### 17.3 Remediation and Action Plan
1. Formulate an India DPDPA Compliance Policy and Consent Manager Integration Guide.
2. Implement multilingual consent notice components and ad-tracking suppression logic.
3. Build database schemas for tracking Consent Manager tokens and parental consent state.
4. Add automated test suites for verifying child ad-tracking bans in Indian region builds.

---

## 18. Singapore Code of Practice for Online Safety & OSRAA

### 18.1 Regulatory Overview and Background
Singapore's IMDA Code of Practice for Online Safety for App Distribution Services and the Online Safety (Relief and Accountability) Act 2025 (OSRAA) require app distribution platforms and developers to enforce age assurance to stop under-18s from downloading age-inappropriate apps, destroy age-assurance data immediately, and act rapidly on notices from the Online Safety Commission to remove online harms.

Official Citation: IMDA Code of Practice for Online Safety (2025); Online Safety (Relief and Accountability) Act 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore Online Safety and Harm Removal Policy.
- **Missing Documentation:**
  Developer guides do not detail response protocols for Online Safety Commission directions or age assurance data destruction rules.
- **Missing Code:**
  Codebase templates lack rapid content takedown handlers or age assurance gate integration for Singapore storefronts.
- **Missing Disclosure:**
  UI templates do not include age rating notices or safety reporting disclosures tailored to Singapore regulatory standards.
- **Missing Logging:**
  No backend schema exists to record safety reporting tickets, commission directions, or content removal timestamps.
- **Missing Testing:**
  Automated tests do not verify that age-gated apps block downloads or account access for Singapore minor profiles.
- **Missing Evidence:**
  The repository provides no sample safety compliance reports, age assurance audit proofs, or commission response records.
- **Missing Audit Trail:**
  An immutable audit trail logging content moderation actions, harm notice receipts, and data purges is missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore Online Safety Compliance Policy.
2. Build UI safety reporting and rapid content moderation code modules.
3. Establish logging handlers for tracking commission notices and takedown actions.
4. Add automated test cases for Singapore age assurance gates.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative payment system support (Korean alt-billing entitlement, 26 percent commission tier, custom modal sheet), while the amended Personal Information Protection Act (PIPA, Act No. 21445) enforces executive accountability (CEO/CPO designation), stringent data transfer rules, and expanded breach notification timelines.

Official Citation: Telecommunications Business Act Article 22-9; Personal Information Protection Act (PIPA) Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Korean Alternative Billing & Executive Privacy Accountability Policy.
- **Missing Documentation:**
  Developer guides lack detailed steps for implementing Apple's South Korea external purchase entitlement (`com.apple.developer.storekit.external-purchase`) or Korean PIPA CPO requirements.
- **Missing Code:**
  Codebase templates do not contain South Korea-specific payment modal sheets or Korean store binary target configurations.
- **Missing Disclosure:**
  In-app billing UI templates lack Korean statutory payment disclosures informing users of alternative payment provider options.
- **Missing Logging:**
  No backend schema exists to log Korean alternative payment transactions, commission reporting data, or PIPA privacy consent logs.
- **Missing Testing:**
  No automated tests verify that the Korean alternative payment modal renders correctly when running in Korean locale/region builds.
- **Missing Evidence:**
  The repository contains no sample KCC compliance reports, Korean alternative billing commission filings, or PIPA audit documentation.
- **Missing Audit Trail:**
  An unalterable audit log tracking payment modal disclosures, CPO approvals, and PIPA breach logs is missing.

### 19.3 Remediation and Action Plan
1. Create a South Korea Billing & PIPA Compliance Guide.
2. Implement Korean alternative payment modal sheet UI components.
3. Build transaction logging utilities for Korean commission calculations.
4. Add automated UI tests for verifying Korean payment flow disclosures.

---

## 20. China Mobile App Filing (MIIT ICP) & CAC AI Companion Rules

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates app filing (ICP extension) and local entity representation prior to distribution, while CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services) requires identifying minor users, automatically switching them to minors mode, obtaining guardian consent under 14, and prohibiting virtual companion services for minors.

Official Citation: MIIT Mobile App Filing Rules (2023); CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no China App Filing & AI Companion Safety Policy.
- **Missing Documentation:**
  Developer guides do not detail step-by-step procedures for acquiring MIIT app filing numbers or configuring AI companion minors mode.
- **Missing Code:**
  Codebase templates lack automated Minors Mode switchers, real-name authentication hooks, or AI companion age gating for Chinese builds.
- **Missing Disclosure:**
  Metadata and UI templates do not include MIIT ICP filing number display components or guardian consent notices.
- **Missing Logging:**
  No schema exists to capture real-name verification status, minor mode activation logs, or guardian consent tokens.
- **Missing Testing:**
  Test suites lack automated checks verifying that AI companion features are disabled when minor mode is active.
- **Missing Evidence:**
  The repository provides no sample MIIT app filing certificates, CAC AI safety assessment filings, or real-name system audit proofs.
- **Missing Audit Trail:**
  An immutable audit trail logging real-name verification checks, minor mode triggers, and ICP metadata updates is absent.

### 20.3 Remediation and Action Plan
1. Draft a China Regulatory Compliance Policy covering MIIT filing and CAC AI companion rules.
2. Build UI components for displaying MIIT ICP numbers and switching to Minors Mode.
3. Implement real-name verification and guardian consent backend handlers.
4. Add automated tests verifying AI companion feature suppression in Minors Mode.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says **Covered**. **Partial** means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. **Missing** means the playbook does not carry it at all.

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
| **9. EU EAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. US CPRA / CPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK OSA / Children's Code**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. AU Minimum Age** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore OSRAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China ICP / CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is strong on store review guidelines and platform policies, and thinner on the legal layers that bind an app once live in specific jurisdictions.

In priority order:
1. Complete implementation of GPSR metadata and disclosure patterns in `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Expand the detection rules and automated guards for all 19 Partial frameworks.
3. Build code templates, UI components, backend logging schemas, and test harnesses for high-impact 2026 deadlines (EU AI Act Article 50, EU Withdrawal Button, US ASAA, Brazil Digital ECA, UK Online Safety).

Re-run validation and audit scripts regularly against official primary sources (EUR-Lex, FTC, Federal Register, ICO, eSafety, ANPD) to maintain repository accuracy.

---

## 23. Sources

Every regulation named above, at its primary source:
- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- FTC COPPA Rule: [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California Privacy Rights Act: [Cal. Civ. Code section 1798.100](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Amendment Act 2024: [Parliament of Australia](https://www.aph.gov.au/)
- Brazil Digital ECA: [Lei n. 15.211/2025](https://www.planalto.gov.br/)
- India DPDPA 2023: [Gazette of India](https://egazette.gov.in)
- Singapore OSRAA 2025: [Singapore Statutes Online](https://sso.agc.gov.sg/)
- South Korea PIPA: [Personal Information Protection Commission](https://www.pipc.go.kr/)
- China MIIT App Filing & CAC Orders: [MIIT / CAC Official Publications](http://www.miit.gov.cn/)
