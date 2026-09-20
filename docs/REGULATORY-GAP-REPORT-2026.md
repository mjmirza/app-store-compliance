# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the App Store Compliance Playbook itself. It evaluates twenty major global and regional regulations that bind mobile and web application developers shipping into the EU, US, UK, Australia, Brazil, Canada, India, Singapore, South Korea, and China. It checks how far this repository carries each framework, what it covers only partially, and what gaps remain across the codebase, data, and documentation.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is systematically audited across eight compliance categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital systems and e-commerce applications, the GPSR mandates that online marketplaces clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template policy to classify whether an app listing falls inside Regulation (EU) 2023/988 or to define Responsible Person duties in the EU.
- **Missing Documentation:**
  The repository is missing developer checklists and step-by-step instructions on structuring online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements. UI templates lack code blocks for displaying manufacturer identity or safety warnings on EU storefronts.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, recalls, or corrective actions. The repository fails to supply templates for a centralized incident log.
- **Missing Testing:**
  No automated tests exist to verify that online interface elements dynamically display required product safety information, manufacturer details, or warning notices based on user geographic location.
- **Missing Evidence:**
  The repository lacks templates of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no audit trail system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented in response to safety alerts.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining designation of an EU-based Responsible Person and product classification criteria.
2. Incorporate GPSR-specific metadata requirements (manufacturer address, email, product identifier) into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory that demonstrate compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script that verifies the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives for gathering evidence. The mandatory compliance enforcement date is 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window to produce user data is 10 days, but in critical emergency cases, providers are legally required to produce requested data within a strict 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, so a development team receiving an EU judicial order has no guidance on who may act on it.
- **Missing Documentation:**
  While the repository mentions the e-Evidence Package, it lacks concrete operational runbooks for handling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:**
  There are no automated scripts or secure API endpoints in backend mock implementations to assist in securely exporting, filtering, and packaging user data in response to a valid legal order.
- **Missing Disclosure:**
  Public-facing documentation, including Privacy Policies, fails to explicitly disclose to EU users that their data may be preserved or disclosed to European law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository does not contain database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, data access activities, or data releases.
- **Missing Testing:**
  There are no integration tests or validation flows to simulate rapid 8-hour emergency retrieval and secure packaging of user data under simulated pressure.
- **Missing Evidence:**
  The repository is missing verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for compliance verification.
- **Missing Audit Trail:**
  A secure audit trail system to record every administrative interaction, data extraction, and transmission made by compliance officers during a legal request is absent.

### 2.3 Remediation and Action Plan
1. Draft and implement a comprehensive Law Enforcement Response Protocol establishing roles, responsibilities, and secure communication channels for executing EPOs.
2. Formally designate an EU establishment or legal representative and notify the designated central authority before the 18 August 2026 deadline.
3. Build secure backend scripts to automate extraction and encryption of requested user datasets, ensuring execution within the 8-hour emergency window.
4. Establish a tamper-proof audit trail to log incoming certificates, verification checks, data extractions, and secure transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts concluded by electronic means.

The statutory withdrawal period is 14 days from the conclusion of the contract. The cancellation path must be direct, clear, and at least as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating financial services apps from general distance contracts.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
- **Missing Code:**
  Front-end user interface templates and billing mock codes in this repository do not contain functional implementations of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining consequences and terms of contract revocation.
- **Missing Logging:**
  There are no logging mechanisms designed to capture and record when a user clicks the withdrawal button, the timestamp of the request, confirmation of contract termination, or initiation of refund flows.
- **Missing Testing:**
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance during consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent "Withdrawal Button" component within account settings of EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Verified age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although rejection patterns contain entries for state-level laws, mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  In-app onboarding flows do not display required state disclosures explaining that the user's age category is requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no backend system designed to log receipt of parental consent, consent revocations (such as `RESCIND_CONSENT` server notifications), or immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests to verify that minor accounts are blocked from accessing premium features or completing purchases without valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates or examples of parental consent agreements, identity verification logs, or data minimization records to prove compliance to state Attorneys General.
- **Missing Audit Trail:**
  An audit trail to record historical rollout of age-assurance features, changes in consent policies, and records of immediate verification data deletions is absent.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy specifying how state-level requirements are identified and how children's data is minimized.
2. Implement cross-platform native hooks in mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and procedures to purge raw age-verification data immediately after user age category confirmation.
4. Establish automated unit tests verifying that minor age categories disable in-app billing until verifiable parental consent flags are processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems must ensure a sufficient level of AI literacy among their staff and persons dealing with AI operations.

This requirement applies to all organizations with no headcount carve-out, meaning small development teams and solo creators are equally bound. Pragmatic compliance requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining team obligations under Article 4 or how to stay updated on AI safety and risk standards.
- **Missing Code:**
  The repository lacks a automated CLI helper tool or script to verify whether team literacy logs exist and remain up-to-date.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose commitment to or enforcement of AI literacy standards as mandated by Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no automated internal lints or pre-commit checks to verify that team members committing AI-related changes have valid, up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of acceptable evidence, such as a completed training log, a course record, or a written risk assessment.
- **Missing Audit Trail:**
  There is no historical audit trail documenting when AI literacy policies were reviewed, when training modules were updated, or how team training records evolved over time.

### 5.3 Remediation and Action Plan
1. Draft and publish an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create a centralized `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Designate a compliance coordinator to review team literacy records on an annual basis.
4. Set up an automated check in the CI pipeline that warns if the literacy log has not been reviewed or updated within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates strict transparency obligations for AI systems, taking full legal effect on 2 August 2026.

Under Article 50(1), providers must ensure AI systems interacting directly with natural persons inform users that they are interacting with AI. Article 50(2) mandates that outputs of generative AI systems (text, audio, images, or video) must be marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deployers of deepfakes to disclose artificial generation or manipulation.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering when disclosures must appear and how generated media should be marked.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` mention Article 50 but lack detailed developer-facing instructions on implementing machine-readable watermarking or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes or utilities to inject machine-readable watermarks (such as C2PA metadata) into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display required immediate disclosures ("You are interacting with an AI system") at first user exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  Existing test runner scripts do not check for synthetic media markers or verify that generated outputs are machine-detectable.
- **Missing Evidence:**
  The repository is missing evidence templates, such as independent assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An audit trail recording technical choices, vendor audits, model changes, and modifications to transparency disclosures is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency Policy mandating direct disclosure and machine-readable output marking.
2. Incorporate explicit notices ("You are chatting with an AI assistant") inside conversational interface templates.
3. Implement standard metadata injection (using C2PA or cryptographic watermarking) inside synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify machine-readable compliance headers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) establishes rules for gatekeeper platforms to ensure contestability and fairness in digital markets. For iOS and Android developers distributing in the EU, the DMA enables alternative app distribution (web distribution and third-party marketplaces) and alternative payment processing.

On 18 August 2026, Apple updated business terms for EU apps via Attachment 14 to the Apple Developer Program License Agreement, replacing the original Core Technology Fee with a Core Technology Commission (5% on digital transactions outside the App Store) effective 1 October 2026.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive DMA Entitlement and Distribution Policy guiding teams on choosing between standard App Store terms and Attachment 14 terms.
- **Missing Documentation:**
  Documentation lacks detailed operational step-by-step guides for setting up monthly reporting via the External Purchase Server API.
- **Missing Code:**
  Codebase samples lack functional implementations calling the `ExternalPurchaseCustomLink` API or handling modal sheets required before directing EU users to external web flows.
- **Missing Disclosure:**
  UI templates do not include system-level disclosure sheets or in-app notices informing users that external transactions bypass Apple or Google consumer protection mechanisms.
- **Missing Logging:**
  There are no backend database models or event logging structures to track external transaction IDs, amounts, currencies, and timestamps for monthly reporting.
- **Missing Testing:**
  The repository lacks automated unit tests to verify that external purchase links are conditionally restricted to EU storefronts and hidden for non-EU users.
- **Missing Evidence:**
  Templates for monthly External Purchase Server API execution reports and Attachment 14 acceptance confirmations are missing.
- **Missing Audit Trail:**
  An audit trail tracking historical entitlement declarations, fee calculations, and reporting submissions to platform gatekeepers is not maintained.

### 7.3 Remediation and Action Plan
1. Create a DMA Entitlement Strategy Guide explaining Attachment 14 terms, CTC calculations, and alternative payment requirements.
2. Implement wrapper classes for `ExternalPurchaseCustomLink` on iOS and equivalent web views on Android with regional storefront checks.
3. Build automated reporting pipelines to compile monthly external transaction logs into required API payloads.
4. Add automated test cases ensuring external offer links do not execute on non-EU storefronts.

---

## 8. EU Digital Services Act (DSA Articles 30 & 31)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) creates a unified framework for online intermediaries. Articles 30 and 31 require app stores to collect, verify, and display trader contact and identity information for all developers distributing apps in the EU.

Developers must declare trader or non-trader status in App Store Connect and Google Play Console. Verified trader information (business address, phone number, email) is displayed publicly on EU app store product pages.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Trader Compliance Policy providing legal criteria to determine whether an app developer qualifies as a trader under EU law.
- **Missing Documentation:**
  Checklists mention DSA trader status but lack detailed instructions on 2FA phone/email verification and document upload procedures in App Store Connect.
- **Missing Code:**
  `scripts/metadata-audit.py` does not programmatically check whether trader contact details or DSA compliance status fields are declared in pulled store metadata.
- **Missing Disclosure:**
  Templates for in-app "About" pages or web landing pages do not provide required trader contact information disclosures for non-trader declarations.
- **Missing Logging:**
  There are no logging mechanisms to record when trader declarations were submitted, modified, or re-verified in developer consoles.
- **Missing Testing:**
  Automated metadata tests do not flag missing trader verification statuses or missing contact information for EU storefront releases.
- **Missing Evidence:**
  The repository lacks templates for storing verified D-U-N-S records, utility bills, or 2FA verification receipts required for DSA compliance audits.
- **Missing Audit Trail:**
  No audit trail exists to track annual reviews of trader status or historical updates made to published contact details.

### 8.3 Remediation and Action Plan
1. Publish a DSA Trader Determination Guide to assist developers in evaluating commercial activity status.
2. Extend `scripts/metadata-audit.py` to audit pulled App Store Connect and Play Console metadata for DSA trader compliance.
3. Include standardized contact disclosure blocks in app boilerplate templates.
4. Add automated pre-submission checklist assertions verifying DSA trader status before EU app deployment.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became enforceable on 28 June 2025. It applies to digital products and services, including mobile applications and e-commerce platforms, available to EU consumers.

The technical standard for EAA compliance is EN 301 549 (version 3.2.1), which builds on WCAG 2.1 Level AA and includes specific mobile software requirements in Chapter 11 (non-web software). An Accessibility Statement and functional accessibility support (screen readers, dynamic text scaling, contrast) are legally required.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an enterprise Accessibility Policy establishing WCAG 2.1 AA / EN 301 549 compliance standards across engineering teams.
- **Missing Documentation:**
  While `docs/PLATFORM-MECHANICS-2026.md` mentions EAA, the repository lacks a dedicated EN 301 549 Chapter 11 mobile implementation guide.
- **Missing Code:**
  Codebase templates contain unlabelled UI elements, missing VoiceOver accessibility labels, fixed layout dimensions breaking text scaling, and hardcoded colors violating contrast minimums.
- **Missing Disclosure:**
  App templates and web landing pages do not include an Accessibility Statement conforming to EN 301 549 Annex B and C.
- **Missing Logging:**
  No logging or telemetry mechanisms exist to capture user accessibility preferences (Reduce Motion, Dynamic Type size, high contrast) to optimize UI rendering without privacy intrusion.
- **Missing Testing:**
  While `scripts/accessibility-audit.py` performs static checks, there are no automated UI tests running VoiceOver / TalkBack tree traversals or contrast verification on rendered screens.
- **Missing Evidence:**
  The repository lacks templates for Accessibility Conformance Reports (VPAT / EN 301 549 ACR) required during procurement or regulatory audits.
- **Missing Audit Trail:**
  An audit trail tracking annual accessibility audits, remediation tickets, and user feedback logs is not maintained.

### 9.3 Remediation and Action Plan
1. Develop a comprehensive EN 301 549 Chapter 11 Mobile Accessibility Checklist and incorporate it into `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Expand `scripts/accessibility-audit.py` to perform static AST analysis on Swift, Kotlin, and React Native source files for missing accessibility attributes.
3. Publish standardized Accessibility Statement templates in the templates directory.
4. Create an automated VPAT / Accessibility Conformance Report generator script.

---

## 10. US Amended COPPA Rule (FTC)

### 10.1 Regulatory Overview and Background
The FTC's amended Children's Online Privacy Protection Rule (16 CFR Part 312 / 90 FR 16918) takes full effect on 22 April 2026. It applies to operators of child-directed commercial websites and online services (including mobile apps), as well as general-audience services with actual knowledge of child users under 13.

Key amendments expand personal information to include biometric identifiers and government identifiers, mandate separate opt-in consent for targeted advertising and third-party disclosures, require written data retention policies with mandatory deletion, and require a written information security program.

Official Citation: FTC 16 CFR Part 312 (Federal Register 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a COPPA Data Retention and Destruction Policy (Section 312.10) and a written Information Security Program (Section 312.8).
- **Missing Documentation:**
  Checklists mention COPPA but lack developer-facing guides on implementing dual-consent flows (separate opt-in for core service vs third-party ad sharing).
- **Missing Code:**
  Codebase samples do not include verifiable parental consent (VPC) flows (knowledge-based authentication or ID verification integration) or automated data-purging triggers.
- **Missing Disclosure:**
  Privacy policy templates lack clear disclosures regarding expanded personal information definitions (biometric data) and separate parental consent options.
- **Missing Logging:**
  There are no backend database models or audit logging structures to record parental consent timestamps, methods, consent scope, or withdrawal events.
- **Missing Testing:**
  The test suite lacks automated integration tests verifying that third-party ad SDKs remain deactivated until explicit secondary parental consent is recorded.
- **Missing Evidence:**
  Templates for annual Information Security Risk Assessments and written data retention schedules required by the FTC are missing.
- **Missing Audit Trail:**
  An immutable audit trail tracking parental consent lifecycle events, data deletion executions, and third-party SDK disclosure reviews is absent.

### 10.3 Remediation and Action Plan
1. Draft template COPPA Information Security Program and Data Retention Policy documents.
2. Add backend VPC integration handlers and secondary opt-in consent flag logic in client SDK code samples.
3. Update `scripts/validate-privacy-manifest.py` to flag third-party ad tracking in child-directed apps without parental consent flags.
4. Implement automated unit tests validating complete purging of child personal information upon consent revocation.

---

## 11. US California Privacy Rights Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and 2026 CPPA regulations, governs the personal information processing of California residents.

It requires businesses to provide a Privacy Policy, Notice at Collection, opt-out mechanisms for selling/sharing personal information (including honoring Global Privacy Control signals), controls for limiting sensitive personal information use, and mechanisms for exercising rights to know, delete, and correct. Automated Decision-Making Technology (ADMT) regulations phase in from 2026.

Official Citation: California Civil Code Section 1798.100 et seq. and CPPA Regulations.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a CCPA/CPRA Compliance Policy detailing procedures for fulfilling consumer privacy rights requests within statutory 45-day windows.
- **Missing Documentation:**
  Documentation lacks implementation guides for parsing Global Privacy Control (`Sec-GPC`) headers in webviews or native app network requests.
- **Missing Code:**
  Codebase templates lack functional implementations of "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information" toggles.
- **Missing Disclosure:**
  In-app Privacy Policy templates do not include California-specific disclosures detailing categories of personal information collected, sold, or shared in the preceding 12 months.
- **Missing Logging:**
  No logging schemas exist to capture consumer rights request submissions (Know, Delete, Correct, Opt-Out), identity verification steps, or resolution timestamps.
- **Missing Testing:**
  The test suite does not include automated unit tests verifying that activating the GPC signal or opt-out toggle suppresses data collection endpoints.
- **Missing Evidence:**
  The repository lacks templates for Consumer Rights Request Log reports or CPPA annual metrics disclosures required for large entities.
- **Missing Audit Trail:**
  An unalterable audit trail tracking GPC signal processing, opt-out request propagations to third-party vendors, and data deletion receipts is missing.

### 11.3 Remediation and Action Plan
1. Publish a California Consumer Privacy Rights Implementation Guide with standardized Privacy Policy templates.
2. Build native iOS/Android helper modules to parse `Sec-GPC` headers and expose global opt-out state properties.
3. Implement backend consumer request routing endpoints supporting automated data deletion and export.
4. Add test suites asserting that network requests suppress analytics/advertising payloads when GPC or opt-out flags are active.

---

## 12. US Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) regulates the collection, use, safeguarding, handling, storage, retention, and destruction of biometric identifiers and information (fingerprints, voiceprints, retina scans, facial geometry).

BIPA requires written notice, explicit written release prior to collection, a publicly available retention schedule and destruction guideline, and strict prohibitions on selling or profiting from biometric data. Amending law SB 2979 (August 2024) clarifies that multiple collections of the same biometric identifier constitute a single violation.

Official Citation: 740 ILCS 14/ (Illinois Compiled Statutes).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Biometric Information Privacy Policy and Biometric Data Retention Schedule conforming to BIPA Section 15(a).
- **Missing Documentation:**
  Documentation lacks developer guidelines distinguishing local on-device biometric auth (LocalAuthentication / BiometricPrompt) from remote biometric data collection.
- **Missing Code:**
  Code templates lack written consent modals or electronic signature capture flows required prior to initializing biometric capture SDKs.
- **Missing Disclosure:**
  In-app disclosures fail to explicitly inform users in writing that biometric identifiers are being collected, the specific purpose, and the duration of storage.
- **Missing Logging:**
  No backend logging models exist to capture written consent receipts, timestamps, consent version numbers, or scheduled data destruction dates.
- **Missing Testing:**
  Automated tests do not scan codebases for third-party biometric SDK initialization prior to written consent verification flags.
- **Missing Evidence:**
  Templates for BIPA Written Release agreements and automated data destruction execution receipts are missing.
- **Missing Audit Trail:**
  An immutable audit trail logging biometric consent capture, retention period calculations, and certified biometric data destruction events is absent.

### 12.3 Remediation and Action Plan
1. Create a BIPA Compliance and Biometric Policy Guide with sample written consent release agreements.
2. Update static code scanners in `agent-os/hooks/app-store-compliance-guard.sh` to audit biometric API usage (FaceID, camera facial geometry) for consent gates.
3. Build backend data retention workflows that trigger automatic purging of stored biometric vectors upon policy expiration dates.
4. Add unit test suites verifying local authentication fallbacks when biometric consent is withheld.

---

## 13. US Federal Negative Option Rule & State Subscription Cancellation Laws

### 13.1 Regulatory Overview and Background
Federal and state laws govern subscription enrollment, automatic renewals, negative option features, and cancellation mechanisms. While the FTC's federal "click to cancel" rule amendment was vacated on procedural grounds in July 2025, Section 5 of the FTC Act, ROSCA (Restore Online Shoppers' Confidence Act), and state laws (California AB 2863, New York, Massachusetts) strictly mandate simple, frictionless cancellation paths.

Subscriptions billed outside platform in-app purchase systems (via web funnels or companion account settings) must provide an online cancellation mechanism that is at least as simple as the sign-up mechanism, prohibiting forced phone calls, letters, or complex administrative steps.

Official Citations: 15 U.S.C. 8401 (ROSCA), California Bus. & Prof. Code Sec 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Subscription and Automatic Renewal Policy guiding web-billed subscription flows.
- **Missing Documentation:**
  Checklists cover App Store / Play Billing rules but lack explicit guidelines for web-billed companion subscription cancellation UX flows.
- **Missing Code:**
  Repository samples lack functional self-service subscription cancellation UI components or API handlers for web-billed accounts.
- **Missing Disclosure:**
  Subscription sign-up screen templates fail to include clear disclosures regarding recurring billing terms, fee amounts, billing frequency, and cancellation instructions.
- **Missing Logging:**
  No database schemas exist to log pre-purchase consent acknowledgments, renewal notice dispatches, or cancellation request timestamps.
- **Missing Testing:**
  Automated UI tests do not check that web-billed subscription cancellation can be accomplished entirely online in equal or fewer steps than enrollment.
- **Missing Evidence:**
  Templates for email booking confirmations, pre-renewal reminder logs, and cancellation confirmation receipts are missing.
- **Missing Audit Trail:**
  An audit trail tracking cancellation flow modifications, user drop-off metrics during cancellation, and renewal notification logs is absent.

### 13.3 Remediation and Action Plan
1. Draft a Web-Billed Subscription Compliance Guide detailing ROSCA and California automatic renewal requirements.
2. Develop modular self-service cancellation UI components and backend account cancellation APIs in boilerplate code.
3. Incorporate metadata and link checks in `scripts/metadata-audit.py` to ensure external subscription links point directly to online cancellation paths.
4. Add automated UI tests verifying frictionless cancellation execution.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) and the Information Commissioner's Office (ICO) Age Appropriate Design Code (Children's Code) govern online services likely to be accessed by children under 18 in the UK.

The OSA imposes duties on user-to-user and search services to prevent access to illegal content and content harmful to children, mandating Highly Effective Age Assurance (facial age estimation, digital ID, open banking). The ICO Children's Code establishes 15 standards, including high privacy by default, data minimization, disabled geolocation and profiling by default, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023 (c. 50), ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Online Child Safety Policy and a template UK Children's Code Data Protection Impact Assessment (DPIA).
- **Missing Documentation:**
  Documentation lacks technical operational guides for integrating Ofcom-approved Highly Effective Age Assurance providers in UK app builds.
- **Missing Code:**
  Codebase templates do not implement high-privacy-by-default settings (disabled geolocation, disabled profiling, strict ad defaults) for UK child accounts.
- **Missing Disclosure:**
  Onboarding UI templates lack age-appropriate disclaimers and child-friendly privacy notices required under Standard 4 of the ICO Code.
- **Missing Logging:**
  No logging mechanisms exist to capture age assurance verification outcomes, age confidence scores, or DPIA review milestones.
- **Missing Testing:**
  The test suite lacks automated checks verifying that geolocation tracking and targeted advertising remain disabled by default for UK user profiles.
- **Missing Evidence:**
  Templates for completed ICO Children's Code DPIAs and Ofcom risk assessment submissions are missing.
- **Missing Audit Trail:**
  An audit trail tracking changes to age assurance thresholds, child safety moderation policies, and DPIA updates is absent.

### 14.3 Remediation and Action Plan
1. Publish a UK Online Safety Compliance Manual and Children's Code DPIA template.
2. Add client-side configuration toggles enforcing strict default privacy states when UK user region is detected.
3. Integrate static analysis rules in compliance scanners checking for geolocation SDK initialization without explicit age gates.
4. Build automated unit test suites validating default privacy setting assertions.

---

## 15. Australia Online Safety Act & Social Media Minimum Age Act

### 15.1 Regulatory Overview and Background
Australia's Online Safety Act 2021 and the Online Safety Amendment (Social Media Minimum Age) Act 2024 regulate online safety, age verification, and access to age-restricted services.

The Social Media Minimum Age Act restricts individuals under 16 from holding accounts on designated social media platforms, requiring platforms to take reasonable steps (waterfall age assurance methods) to prevent under-16 account creation. Apple and Google enforce 18-plus download restrictions on the Australian App Store and Play Store.

Official Citations: Online Safety Act 2021 (C2021A00076) and Amendment Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Age-Restricted Services Policy outlining age assurance implementation and data destruction rules.
- **Missing Documentation:**
  Documentation lacks guidelines on eSafety Industry Codes (Schedule 7 App Distribution Services) compliance for Australian releases.
- **Missing Code:**
  Codebase templates do not contain waterfall age verification logic or data-ringfencing modules to purge age proof data post-verification.
- **Missing Disclosure:**
  UI templates do not display required Australian statutory disclosures informing users that age data is collected solely for age assurance and destroyed immediately after.
- **Missing Logging:**
  No backend models exist to log age verification completion flags separate from personal identity data.
- **Missing Testing:**
  The test suite lacks automated integration tests verifying that raw identity documents used for Australian age checks are erased immediately following verification.
- **Missing Evidence:**
  Templates for eSafety Risk Assessment records and age assurance data destruction certificates are missing.
- **Missing Audit Trail:**
  An audit trail tracking annual eSafety Code compliance reviews and age verification system audits is absent.

### 15.3 Remediation and Action Plan
1. Draft an Australian Online Safety and Age Assurance Compliance Guide.
2. Implement backend data-ringfencing routines that isolate and destroy raw identity verification artifacts.
3. Add automated checks in `scripts/release-audit.py` asserting that age verification data retention triggers conform to Australian rules.
4. Create unit tests verifying account creation blocking for under-16 age signals on social platform builds.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025), regulated by Decreto 12.880 of March 2026 and enforced by ANPD, establishes a comprehensive child protection framework for digital environments.

It requires age verification (document verification, facial age estimation, CPF database checks) for age-restricted services, prohibiting self-declaration checkboxes. App stores and developers must block gambling and 18-plus content from minors, obtain guardian authorization, and show age ratings prior to download. Google Play supports this via the Play Age Signals API.

Official Citations: Law 15,211/2025 and Decreto n. 12.880 (18 March 2026).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy governing age verification, guardian consent, and content gating.
- **Missing Documentation:**
  Checklists lack technical integration steps for processing Google Play Age Signals API and Apple Declared Age Range API signals on Brazilian storefronts.
- **Missing Code:**
  Code samples do not contain client handlers for CPF validation APIs, facial age estimation SDK integrations, or guardian consent flows.
- **Missing Disclosure:**
  In-app onboarding flows lack Portuguese-language disclosures explaining age verification duties under Decreto 12.880.
- **Missing Logging:**
  No backend database schemas exist to log guardian authorization events, CPF verification tokens, or age category classifications.
- **Missing Testing:**
  The test suite lacks automated unit tests verifying that minor age signals returned by the Play Age Signals API in Brazil disable loot boxes and 18-plus features.
- **Missing Evidence:**
  Templates for ANPD compliance reports and guardian consent verification logs are missing.
- **Missing Audit Trail:**
  An audit trail recording age verification method selection, consent revocations, and system adaptations under ANPD parameters is absent.

### 16.3 Remediation and Action Plan
1. Create a Brazil Digital ECA Implementation Guide with Portuguese disclosure templates.
2. Build native module wrappers integrating Google Play Age Signals API (`com.google.android.play:age-signals`) for Brazil.
3. Update `data/rejection-patterns.json` to include rules flagging unverified age verification checkboxes on Brazilian builds.
4. Add automated test suites verifying content gating based on returned Brazilian age bands.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act 2023 (DPDPA) and DPDP Rules 2025 establish a legal framework for digital personal data processing.

The Act requires itemized consent notices in English and 22 scheduled languages, registered Consent Managers, and verifiable parental consent prior to processing data of children (under 18). Behavioral tracking and targeted advertising to children are strictly prohibited.

Official Citations: Act No. 22 of 2023 and DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an India DPDPA Personal Data Processing Policy and Child Data Governance Framework.
- **Missing Documentation:**
  Documentation lacks developer guidelines for integrating with India's registered Consent Managers and DigiLocker for verifiable parental consent.
- **Missing Code:**
  Code templates do not support multi-lingual consent notices in 22 scheduled Indian languages or DigiLocker VPC API handlers.
- **Missing Disclosure:**
  Consent UI components fail to display clear, itemized notices detailing data categories collected, processing purposes, and Data Fiduciary contact details.
- **Missing Logging:**
  No database schemas exist to capture consent tokens, language selections, or consent withdrawal events processed via Consent Managers.
- **Missing Testing:**
  The test suite lacks automated tests verifying that targeted advertising and user tracking SDKs are completely suppressed for under-18 Indian accounts.
- **Missing Evidence:**
  Templates for Data Protection Impact Assessments (DPIAs) and Data Auditor verification reports required for Significant Data Fiduciaries are missing.
- **Missing Audit Trail:**
  An unalterable audit trail tracking consent lifecycle events, Data Principal rights requests, and consent manager API calls is absent.

### 17.3 Remediation and Action Plan
1. Publish an India DPDPA Compliance Manual including multi-lingual consent notice templates.
2. Build client SDK handlers for managing itemized consent states and DigiLocker parental verification flows.
3. Expand static code auditing scripts to flag un-gated ad SDKs on Indian app builds.
4. Implement unit tests asserting ad suppression for minor user profiles.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act 2012 (PDPA) and IMDA Code of Practice for Online Safety for App Distribution Services govern data protection and online safety.

The IMDA Code mandates app store age assurance measures (effective 1 April 2026), requiring screening to prevent under-18 users from downloading age-inappropriate apps. Apple enforces an 18-plus download block on the Singapore App Store. Data Protection Officer (DPO) designation and 3-day breach notification are required under PDPA.

Official Citations: Singapore PDPA 2012 and IMDA Code of Practice for Online Safety.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA Compliance Policy and Personal Data Breach Notification Protocol.
- **Missing Documentation:**
  Documentation lacks developer guidelines on IMDA age rating alignment and DPO declaration requirements.
- **Missing Code:**
  Codebase templates do not include client-side handlers for processing Singapore age rating restrictions or DPO contact routing.
- **Missing Disclosure:**
  In-app Privacy Policies lack explicit disclosures regarding 3-day PDPC breach notification procedures and DPO contact details.
- **Missing Logging:**
  No backend logging models exist to capture data breach identification timestamps, risk assessments, or PDPC notification logs.
- **Missing Testing:**
  Automated tests do not verify that Singapore storefront releases enforce 18-plus download gating and age verification checks.
- **Missing Evidence:**
  Templates for PDPC Data Breach Notification Forms and DPO Appointment documentation are missing.
- **Missing Audit Trail:**
  An audit trail tracking annual data protection reviews, breach response drills, and IMDA age restriction updates is absent.

### 18.3 Remediation and Action Plan
1. Publish a Singapore Privacy and Online Safety Compliance Guide.
2. Add DPO contact disclosure blocks to app boilerplate templates.
3. Update `scripts/release-audit.py` to verify 3-day breach response workflows and DPO declarations.
4. Implement unit tests validating age rating enforcement on Singapore app builds.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendments

### 19.1 Regulatory Overview and Background
South Korea's Personal Information Protection Act (PIPA) amendments (Act No. 21445) and Telecommunications Business Act govern data protection and app store payments.

PIPA establishes severe CEO liability, board-approved Chief Privacy Officers (CPOs), and strict consent requirements. The Telecommunications Business Act mandates alternative in-app payment options (Apple StoreKit External Purchase entitlement `com.apple.developer.storekit.external` with `SKExternalPurchase = "KR"`), approved local payment gateways (KCP, Toss, Inicis, NICE), 26% commission reporting, and mandatory Korean storefront disclaimers.

Official Citations: PIPA Act No. 21445 and Telecommunications Business Act.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a South Korea PIPA & TBA Compliance Policy governing local payment gateway integrations and CPO responsibilities.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for setting up Apple Korea External Purchase entitlement, local payment SDKs, and 15-day monthly reporting.
- **Missing Code:**
  Codebase samples lack functional implementations of Korean native payment gateway integrations and mandatory StoreKit external purchase modal sheets.
- **Missing Disclosure:**
  UI templates do not include required Korean language disclosure sheets informing users that alternative payments bypass standard platform dispute resolution.
- **Missing Logging:**
  No backend database schemas exist to capture Korean external transaction details, gross VAT amounts, and monthly remittance calculations.
- **Missing Testing:**
  The test suite lacks automated unit tests verifying that Korean external purchase entitlements are strictly restricted to Korea-only binaries.
- **Missing Evidence:**
  Templates for 15-day monthly sales reports and Korean Game Rating and Administration Committee (GRAC) rating certificates are missing.
- **Missing Audit Trail:**
  An audit trail tracking monthly payment reporting submissions, CPO appointment records, and PIPA compliance reviews is absent.

### 19.3 Remediation and Action Plan
1. Create a South Korea Alternative Payment and Privacy Manual.
2. Develop boilerplate code modules for StoreKit External Purchase implementation in Korean app binaries.
3. Build automated monthly report generators for South Korean external billing transactions.
4. Add automated test cases asserting that `SKExternalPurchase = "KR"` is present only in South Korea builds.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Measures

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) Mobile App Filing requirement (ICP extension), Personal Information Protection Law (PIPL), and Cyberspace Administration of China (CAC) regulations govern mobile applications distributed in China.

Foreign developers must partner with local Chinese entities to complete App Filing. CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, July 2026) mandates automatic minor mode switching, guardian consent under 14, and bans virtual companion services for minors. CAC Minors Content Classification rules ban harmful algorithmic push.

Official Citations: MIIT Mobile App Filing Rules and CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a China MIIT App Filing and PIPL Compliance Policy governing local partnership models and AI minor protection.
- **Missing Documentation:**
  Documentation lacks developer guides on completing ICP/MIIT app filing, Banhao gaming license applications, and CAC AI service registrations.
- **Missing Code:**
  Codebase templates lack automated "Minors Mode" switching components, real-name identity verification SDK wrappers, or algorithmic recommendation toggles.
- **Missing Disclosure:**
  UI templates lack PIPL-compliant separate consent disclosures for cross-border data transfers and facial recognition processing.
- **Missing Logging:**
  No backend database schemas exist to log real-name verification status tokens, CAC compliance audit logs, or minor mode usage timestamps.
- **Missing Testing:**
  The test suite lacks automated unit tests verifying that China-facing builds automatically restrict AI companion features when minor mode is active.
- **Missing Evidence:**
  Templates for MIIT App Filing confirmation records, CAC AI security assessments, and local entity partnership agreements are missing.
- **Missing Audit Trail:**
  An audit trail tracking biennial PIPL compliance audits (required for large handlers) and CAC algorithmic filing updates is absent.

### 20.3 Remediation and Action Plan
1. Publish a China App Distribution, MIIT Filing, and CAC AI Compliance Manual.
2. Develop client-side "Minors Mode" UI components and real-name verification interface stubs.
3. Update `scripts/metadata-audit.py` to flag missing MIIT filing numbers on Chinese Android/iOS metadata listings.
4. Add automated unit test suites verifying restriction of AI roleplay features under minor mode flags.

---

## 21. Consolidated Gap Classification Matrix

The classification table below summarizes the repository's current coverage across all twenty global and regional regulations.
- **Covered:** The repository provides full policy, documentation, code, disclosure, logging, testing, evidence, and audit trail implementations.
- **Partial:** The regulation is named with official citations and dates, but actionable code, tests, or complete templates are missing.
- **Missing:** The framework was previously absent or lacks end-to-end support across all eight categories.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Covered | Covered | Partial | Covered | Partial | Partial | Partial | Partial |
| **8. EU DSA (Trader Status)** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **9. European Accessibility Act** | Covered | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US Amended COPPA** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **11. US CCPA/CPRA** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **12. US Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Negative Option / ROSCA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Covered | Covered | Partial | Covered | Partial | Partial | Partial | Partial |
| **20. China MIIT / CAC AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Roadmap

The playbook provides an industry-leading reference for app store reviewer rejections. To provide complete legal compliance for distributed mobile and web applications, the repository's implementation layer must be expanded across all twenty audited global frameworks.

### Implementation Priorities

1. **Phase 1 (Immediate - High Enforcement Risk):**
   - Add GPSR metadata checks and UI warning components to `scripts/metadata-audit.py` and references.
   - Implement EU AI Act Article 50 machine-readable watermarking and disclosure UI wrappers.
   - Implement EU Contract Withdrawal Button UI components and database logging schemas.
2. **Phase 2 (Mid-Term - 2026 Deadlines):**
   - Integrate EU e-Evidence Package 8-hour emergency data extraction scripts and legal rep notification templates.
   - Add native wrappers for Apple Declared Age Range API and Google Play Age Signals API across US State ASAA, Brazil Digital ECA, and Australian builds.
   - Expand `scripts/accessibility-audit.py` to cover full EN 301 549 Chapter 11 mobile software requirements.
3. **Phase 3 (Long-Term - Global Expansion):**
   - Build multi-lingual consent components for India DPDPA (22 scheduled languages).
   - Implement South Korea alternative payment modal sheets and 15-day monthly server reporting.
   - Add China MIIT App Filing validation to metadata audit scripts and minor mode UI components.

Re-audit this gap report against official primary sources (EUR-Lex, Federal Register, legislation.gov.uk, govinfo, etc.) on a quarterly basis.

---

## 23. Official Primary Citations

Primary official publications establishing the legal baseline for the twenty audited regulatory frameworks:

- **EU GPSR:** [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **EU e-Evidence Package:** [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **EU Contract Withdrawal Button:** [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **US State ASAA:** [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html)
- **EU AI Act:** [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **EU Digital Markets Act:** [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **EU Digital Services Act:** [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **European Accessibility Act:** [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **US Amended COPPA Rule:** [FTC 16 CFR Part 312 (Federal Register 90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **US California Privacy Rights Act:** [CPPA Regulations](https://cppa.ca.gov/regulations/ccpa_updates.html)
- **US Illinois BIPA:** [740 ILCS 14/ (Illinois General Assembly)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- **US ROSCA & Negative Option:** [15 U.S.C. 8401 (GovInfo)](https://www.govinfo.gov)
- **UK Online Safety Act:** [Online Safety Act 2023 (legislation.gov.uk)](https://www.legislation.gov.uk/ukpga/2023/50/contents/enacted) and [ICO Children's Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- **Australia Online Safety:** [Online Safety Act 2021 (legislation.gov.au)](https://www.legislation.gov.au/C2021A00076/asmade/text)
- **Brazil Digital ECA:** [Decreto n. 12.880 (Planalto)](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- **India DPDPA:** [Digital Personal Data Protection Act 2023 (eGazette)](https://egazette.gov.in)
- **Singapore PDPA:** [Personal Data Protection Act 2012 (SSO AGC)](https://sso.agc.gov.sg/Act/PDPA2012)
- **South Korea TBA & PIPA:** [Personal Information Protection Act (law.go.kr)](https://law.go.kr)
- **China Mobile App Filing & CAC AI:** [MIIT Official Portal](https://www.miit.gov.cn/) and [CAC Official Portal](https://www.cac.gov.cn)
