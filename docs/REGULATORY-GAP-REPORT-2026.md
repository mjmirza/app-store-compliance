# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, US, UK, Canada, Australia, Brazil, India, Singapore, South Korea, China, and worldwide markets. It checks honestly how far this repository carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is audited across eight distinct compliance dimensions: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere strictly to the source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless traceably corroborated by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains. The GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template General Product Safety Policy to determine whether their listing falls inside Regulation (EU) 2023/988 or to establish Responsible Person designation.
- **Missing Documentation:**
  The repository is missing specific developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements or Responsible Person declarations.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name or trademark, postal address, and electronic address under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, recalls, or corrective actions.
- **Missing Testing:**
  No automated tests exist to verify that online interface elements dynamically display required product safety information, manufacturer details, or warning notices based on the user's geographic location.
- **Missing Evidence:**
  The repository lacks physical templates or examples of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no audit trail or historical record system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented in response to a safety alert.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining the designation of an EU-based Responsible Person and product classification criteria.
2. Incorporate GPSR-specific metadata requirements into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory that demonstrate compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script that verifies the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. Mandatory enforcement applies from 18 August 2026. This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU, with a standard 10-day production window and an 8-hour emergency response deadline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, leaving development teams without established procedures for executing judicial orders.
- **Missing Documentation:**
  Lacks concrete operational runbooks for handling 10-day standard production orders and 8-hour emergency order procedures.
- **Missing Code:**
  No automated scripts or secure API endpoints exist in backend mock implementations to assist in securely exporting, filtering, and packaging user data in response to a valid legal order.
- **Missing Disclosure:**
  Public-facing documentation, including Privacy Policies, fails to explicitly disclose to EU users that their data may be preserved or disclosed to European law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository lacks database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, data access activities, or data releases.
- **Missing Testing:**
  No integration tests or validation flows simulate the rapid 8-hour emergency retrieval and secure packaging of user data under simulated pressure.
- **Missing Evidence:**
  The repository is missing verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR).
- **Missing Audit Trail:**
  A tamper-proof cryptographic audit trail system to record every administrative interaction, data extraction, and transmission made during a legal request is completely absent.

### 2.3 Remediation and Action Plan
1. Draft and implement a comprehensive Law Enforcement Response Protocol establishing roles and communication channels for EPOs.
2. Formally designate an EU legal representative and notify designated central authorities before 18 August 2026.
3. Build secure backend scripts to automate extraction and encryption of requested datasets for execution within the 8-hour emergency window.
4. Establish a tamper-proof cryptographic audit trail to log all incoming certificates, verification checks, and transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU) to mandate a prominent, easily accessible withdrawal function on the online interface for distance contracts for financial services. Member States apply these rules starting 19 June 2026. The statutory withdrawal period is 14 days from contract conclusion, requiring a cancellation path that is as simple and direct as the sign-up path.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Carries no template policy for the 14-day statutory withdrawal right or guidance separating distance financial services in scope from general subscription design defaults.
- **Missing Documentation:**
  Does not provide UI design guidelines or checklists specifying placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
- **Missing Code:**
  Front-end user interface templates and billing mock implementations contain no functional code for a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining revocation terms.
- **Missing Logging:**
  Lacks logging mechanisms designed to capture when a user clicks the withdrawal button, the timestamp, contract termination confirmation, or refund initiation.
- **Missing Testing:**
  No automated UI or unit tests exist to verify that the withdrawal flow can be completed without administrative friction or manual support tickets.
- **Missing Evidence:**
  Lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance during consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and interface updates is absent.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent, easily accessible withdrawal button component within account settings of EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions.
4. Implement automated end-to-end UI tests to verify frictionless contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minors' access to mobile applications, digital purchases, and features. Developers must process user age categories via Apple's Declared Age Range API or Google's Play Age Signals API and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access mature functionality, while deleting raw age-verification data immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Has no template minors policy specifying state-level age detection rules or minor account management workflows.
- **Missing Documentation:**
  Checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise step-by-step developer guidelines for integrating Declared Age Range API and Play Age Signals API.
- **Missing Code:**
  Mock client implementations do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app features dynamically.
- **Missing Disclosure:**
  Onboarding flows do not display required state disclosures explaining that user age categories are requested to comply with state accountability laws and that parental consent is required.
- **Missing Logging:**
  No backend system exists to log parental consent receipt, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw verification documents.
- **Missing Testing:**
  Test suites lack automated integration tests verifying that minor accounts are blocked from premium features or purchases without valid consent signals.
- **Missing Evidence:**
  Lacks templates of parental consent agreements, identity verification logs, or data minimization records to present to state Attorneys General.
- **Missing Audit Trail:**
  An immutable audit trail recording the historical rollout of age-assurance features, consent policy changes, and verification data deletions is absent.

### 4.3 Remediation and Action Plan
1. Create a Minor Age Assurance Policy detailing state-level requirement detection and children's data minimization.
2. Implement cross-platform native hooks in mobile codebases to query Apple Declared Age Range and Google Play Age Signals APIs.
3. Build automated database triggers to purge raw age-verification data immediately following age category confirmation.
4. Establish automated unit tests verifying that minor account status disables billing until parental consent is verified.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. Providers and deployers of AI systems must ensure a sufficient level of AI literacy among their staff and persons dealing with AI operations. The requirement applies to all organizations with no headcount carve-out, taking effect on 2 February 2025.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Carries no template AI literacy policy defining competency levels, training scope, or compliance review schedules under Article 4.
- **Missing Documentation:**
  Lacks developer-facing documentation or checklists detailing team obligations under Article 4 or continuous safety training expectations.
- **Missing Code:**
  Not directly applicable to runtime application code, but lacks developer CLI tools or automated repository checks to confirm literacy log maintenance.
- **Missing Disclosure:**
  Public-facing documentation, contracts, or vendor agreements do not disclose organizational commitment to AI literacy standards.
- **Missing Logging:**
  Missing a centralized training log or registry (`AI_LITERACY_LOG.md`) to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  No automated pre-commit hooks or CI checks verify that team members committing AI features possess active literacy records.
- **Missing Evidence:**
  Lacks physical evidence templates, such as completed team training logs, course certificates, or internal risk assessments.
- **Missing Audit Trail:**
  There is no historical audit trail documenting policy reviews, module updates, or employee training progress over time.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy defining competency areas (AI safety, data privacy, risk assessment, bias detection).
2. Establish a centralized `AI_LITERACY_LOG.md` within the repository tracking dates, modules, team member names, and verification methods.
3. Set up an automated CI workflow step that validates annual review of team AI literacy records.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act mandates strict transparency requirements for AI systems interacting with natural persons and synthetic media generation, taking effect on 2 August 2026. Providers must ensure users are informed of AI interactions (Article 50(1)), generated outputs are marked in a machine-readable format (Article 50(2)), and deepfakes/manipulated content are explicitly disclosed (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a corporate AI Transparency Policy specifying required user notice timing and synthetic media marking standards.
- **Missing Documentation:**
  Checklists mention Article 50 but lack technical step-by-step guides for implementing machine-readable watermarking (such as C2PA) or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include middle-tier utilities or helper classes to inject invisible/in-audible machine-readable metadata into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display immediate notices ("You are interacting with an AI system") at initial user interaction.
- **Missing Logging:**
  Lacks database logging schemas to record that AI transparency notices were successfully displayed during user sessions.
- **Missing Testing:**
  Test runners do not verify synthetic media watermarks or validate that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  Lacks factual evidence documentation, such as third-party security audits of content moderation filters or metadata retention proofs.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical architecture choices, vendor audits, model versions, and disclosure updates is absent.

### 6.3 Remediation and Action Plan
1. Formulate an AI Transparency and Disclosure Policy mandating user notices and output marking.
2. Implement immediate disclosure notices inside all conversational and generative UI templates.
3. Integrate standard metadata injection (C2PA specification) into synthetic media generation pipelines.
4. Add automated integration tests to scan generated media outputs and verify machine-readable compliance headers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act, Regulation (EU) 2022/1925, regulates core platform services and gatekeepers. For app developers operating in the EU, the DMA enables alternative app distribution, alternative payment processing, anti-steering entitlement links, and direct interoperability. Under Apple's Alternative Terms Addendum and Google's EU alternative billing programs, developers must comply with strict reporting, security, and unified fee entitlement rules.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks an Alternative Distribution and Payment Entitlement Policy guiding developers on DMA entitlement selection, CTF/CTC fee calculations, and gatekeeper terms.
- **Missing Documentation:**
  Lacks step-by-step technical documentation for configuring alternative payment link sheets, web distribution notarization packages, or external link disclosures.
- **Missing Code:**
  Codebase templates lack modular handlers for switching dynamically between StoreKit/Play Billing and external DMA payment links based on geographic region.
- **Missing Disclosure:**
  In-app purchase interfaces lack mandatory DMA disclosure modals informing EU users when they leave the app store billing system for external payment processors.
- **Missing Logging:**
  No database logging schemas exist to capture alternative transaction IDs, external payment timestamps, or monthly gatekeeper reporting payloads.
- **Missing Testing:**
  Test suites lack automated test flows to verify that alternative payment links correctly pass required tracking parameters while blocking non-EU users.
- **Missing Evidence:**
  Lacks templates for external transaction reporting logs, proof of security compliance for alternative payment gateways, or CTF fee reconciliation statements.
- **Missing Audit Trail:**
  An audit trail system recording historical fee model selections (e.g., legacy vs. unified ADPLA terms), gatekeeper reporting submissions, and link modifications is absent.

### 7.3 Remediation and Action Plan
1. Publish a DMA Entitlement and Alternative Distribution Operational Policy.
2. Build UI components for compliant external payment disclosures and anti-steering link banners.
3. Implement secure logging and monthly transaction reporting utilities for alternative billing transactions.
4. Establish automated geography-gating unit tests to restrict DMA entitlement features strictly to EU user sessions.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act, Regulation (EU) 2022/2065, entered into full force on 17 February 2024. It imposes obligations on online platforms, marketplaces, and app developers acting as traders on EU storefronts. App developers selling digital products or subscriptions must declare their Trader Status (including verified business address, phone number, and bank account details) on app store listings, maintain illegal content notice-and-action mechanisms, and ensure transparent recommendation systems.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks an organizational DSA Compliance Policy covering trader verification disclosures, illegal content intake, and user content moderation standards.
- **Missing Documentation:**
  Documentation lacks developer runbooks for submitting verified DSA trader credentials to Apple App Store Connect and Google Play Console.
- **Missing Code:**
  Lacks user-facing notice-and-action UI components for reporting illegal content or appealing moderation decisions in user-generated content (UGC) apps.
- **Missing Disclosure:**
  UGC and marketplace app templates fail to display mandatory DSA disclosures regarding content moderation policies, automated decision-making, or trader identity details.
- **Missing Logging:**
  No logging schemas exist to track incoming illegal content notices, administrative review outcomes, counter-notices, or moderation turn-around times.
- **Missing Testing:**
  Automated tests do not verify notice-and-action submission flows or check that trader verification metadata is correctly published on storefront listings.
- **Missing Evidence:**
  Lacks templates for annual transparency reports, illegal content handling statistics, or formal trader identity verification documents.
- **Missing Audit Trail:**
  An immutable audit trail recording content moderation decisions, appeal logs, notice handling timestamps, and trader profile updates is absent.

### 8.3 Remediation and Action Plan
1. Establish a DSA Trader and Content Moderation Policy.
2. Integrate in-app notice-and-action reporting buttons and appeal flows inside UGC application templates.
3. Build a database schema to log content notices, moderation decisions, and user notification timestamps.
4. Implement automated CI checks to verify that DSA trader disclosure URLs and metadata are present prior to store submission.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, becomes legally binding across Member States on 28 June 2025. It mandates accessibility standards (EN 301 549 / WCAG 2.1 AA) for e-commerce, banking, e-books, and digital services offered to EU consumers. Mobile apps must support screen readers, text scaling, contrast ratios, keyboard navigation, and alternative media formats, with microenterprises exempt only if offering services rather than physical products.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks an Accessibility Governance Policy defining accessibility standards (WCAG 2.1 AA / EN 301 549), testing cadence, and microenterprise exemption criteria.
- **Missing Documentation:**
  Developer guides lack detailed platform-specific implementation patterns for VoiceOver/TalkBack semantics, Dynamic Type scaling, and Reduce Motion support.
- **Missing Code:**
  Existing UI templates lack explicit accessibility labels, semantic traits, minimum touch target sizes (44x44 pt / 48x48 dp), and high-contrast theme overrides.
- **Missing Disclosure:**
  App documentation and website landing pages lack an Accessibility Statement detailing compliance levels, known limitations, and accessibility contact channels.
- **Missing Logging:**
  No logging or telemetry exists to record user accessibility preferences (e.g., screen reader active, bold text enabled) to evaluate accessibility utilization without compromising privacy.
- **Missing Testing:**
  Automated test scripts in `scripts/accessibility-audit.py` cover static pattern checks but lack screen reader UI tests, dynamic font scaling checks, or automated contrast ratio analysis.
- **Missing Evidence:**
  Lacks formal Accessibility Conformance Reports (VPAT / EN 301 549 evaluation sheets) or third-party accessibility audit certificates.
- **Missing Audit Trail:**
  An audit trail tracking historical accessibility remediation, user accessibility feedback, and periodic WCAG compliance evaluations is absent.

### 9.3 Remediation and Action Plan
1. Formulate a corporate Accessibility Policy adhering to Directive (EU) 2019/882 and EN 301 549 standards.
2. Publish an in-app Accessibility Statement and dedicated accessibility support feedback route.
3. Enhance `scripts/accessibility-audit.py` to enforce minimum touch targets, text contrast, and semantic labels during build pipeline checks.
4. Compile a standardized VPAT / EN 301 549 Accessibility Conformance Report template.

---

## 10. US Children's Online Privacy Protection Act (COPPA & Amended COPPA Rule)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 15 U.S.C. 6501-6508, and the FTC Amended COPPA Rule regulate the collection of personal information from children under 13. The updated FTC rules impose strict restrictions on targeted advertising, mandatory separate parental consent for third-party disclosure, strict data retention limits, and enhanced age-verification safeguards.

Official Citation: 16 CFR Part 312 (FTC COPPA Rule) and FTC Enforcement Policy Statement on Age-Verification (2026).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a specialized Child Privacy and COPPA Compliance Policy covering verifiable parental consent (VPC), separate ad-tracking consent, and strict data retention schedules.
- **Missing Documentation:**
  Checklists lack precise implementation steps for setting COPPA flags across third-party analytics SDKs, ad networks, and crash reporting tools.
- **Missing Code:**
  Code templates lack native age-gating screens, verifiable parental consent mechanisms (e.g., credit card micro-charge, signed consent form), or automatic SDK initialization block logic for child accounts.
- **Missing Disclosure:**
  Privacy policies fail to provide clear, prominent notices specifically detailing child data collection practices, operator contact details, and parental deletion rights.
- **Missing Logging:**
  Lacks backend logging schemas to document parental consent grants, consent revocations, and scheduled data deletion jobs for child accounts.
- **Missing Testing:**
  Test suites lack integration tests verifying that analytics and ad SDKs remain strictly disabled when an age gate identifies a user under 13.
- **Missing Evidence:**
  Lacks verified COPPA Safe Harbor certification documentation, parental consent verification records, or data retention audit receipts.
- **Missing Audit Trail:**
  An immutable audit trail recording child account status changes, parental consent interactions, and automatic data deletion executions is absent.

### 10.3 Remediation and Action Plan
1. Draft a COPPA and Child Data Protection Policy aligned with the FTC Amended Rule.
2. Implement strict age-gating UI components that disable non-essential SDKs immediately upon identifying a minor under 13.
3. Establish a backend service to handle verifiable parental consent workflows and automated account data deletion.
4. Add CI test routines to verify that child sessions generate zero third-party ad network network requests.

---

## 11. California Privacy Framework (CCPA / CPRA / CPPA ADMT / AADC / AB 1043)

### 11.1 Regulatory Overview and Background
The California Privacy Rights Act (CPRA), amending the California Consumer Privacy Act (CCPA), Cal. Civ. Code 1798.100 et seq., together with the California Privacy Protection Agency (CPPA) regulations on Automated Decision-Making Technology (ADMT), the Age-Appropriate Design Code (AADC), and AB 1043 (Digital Age Assurance Act), establishes comprehensive privacy standards. Developers must support opt-out preferences (Global Privacy Control - GPC), opt-out of automated profiling/ADMT, deliver age assurance signals, and provide frictionless "Do Not Sell/Share My Personal Information" mechanisms.

Official Citation: Cal. Civ. Code 1798.100 et seq., 11 CCR section 7000 et seq., and Cal. Civ. Code Title 1.81.9 (AB 1043).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a California Privacy Rights Policy covering CCPA/CPRA consumer rights, ADMT opt-out mechanisms, and AB 1043 age assurance obligations.
- **Missing Documentation:**
  Documentation lacks developer instructions for parsing Global Privacy Control (Sec-GPC) HTTP headers or handling native GPC signals in mobile WebViews.
- **Missing Code:**
  Code templates lack functional implementations of "Do Not Sell or Share My Personal Information" links, Limit Use of Sensitive Personal Information toggles, or GPC header parsers.
- **Missing Disclosure:**
  In-app notices and web footers fail to display California-specific privacy disclosures, Notice at Collection, or explicit ADMT processing explanations.
- **Missing Logging:**
  No backend logging schemas exist to capture CCPA opt-out requests, GPC signal receipts, ADMT opt-out choices, or consumer data rights fulfillment timestamps.
- **Missing Testing:**
  Test scripts do not verify that a received GPC header automatically sets internal tracking flags to opt-out across all integrated analytics modules.
- **Missing Evidence:**
  Lacks templates for consumer privacy request metrics reports, risk assessments for automated decision-making technology, or CCPA compliance audit proofs.
- **Missing Audit Trail:**
  An audit trail tracking historical CCPA request fulfillment times, GPC signal handling, and CPPA policy update history is missing.

### 11.3 Remediation and Action Plan
1. Formulate a California Consumer Privacy Policy covering CCPA, CPRA, ADMT regulations, and AB 1043 requirements.
2. Add "Do Not Sell/Share My Personal Information" and "Limit Sensitive Data Use" UI controls to settings screens.
3. Implement automated handling of Global Privacy Control (GPC) signals in backend and mobile network client layers.
4. Build automated unit tests to verify that GPC signal detection suppresses all commercial data sharing endpoints.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14/, regulates the collection, capture, purchase, receipt, storage, and use of biometric identifiers (facial geometry, fingerprints, voiceprints, retina/iris scans). BIPA mandates written informed consent prior to collection, strict retention schedules, mandatory destruction upon satisfaction of purpose or within 3 years, and prohibits profiting from biometric data.

Official Citation: 740 ILCS 14/ (Illinois Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a Biometric Data Privacy Policy establishing written retention schedules, destruction guidelines, and consent collection protocols under 740 ILCS 14/15.
- **Missing Documentation:**
  Lacks technical documentation clarifying the boundary between on-device local biometric authentication (e.g., Apple Face ID / Android BiometricPrompt where raw data stays in Secure Enclave) and backend biometric processing.
- **Missing Code:**
  Codebase templates lack explicit written consent modal screens, biometric data capture authorization sheets, or automated deletion routines for biometric templates.
- **Missing Disclosure:**
  In-app onboarding interfaces fail to display mandatory pre-collection BIPA disclosures specifying the exact purpose and duration for which biometric data is collected.
- **Missing Logging:**
  No database logging schemas exist to capture written consent timestamps, specific consent scope, or biometric data destruction events.
- **Missing Testing:**
  Test suites lack unit tests verifying that biometric feature flows block initialization if the user has not explicitly accepted the written BIPA release.
- **Missing Evidence:**
  Lacks physical evidence templates, such as signed biometric consent forms, Secure Enclave isolation verification receipts, or data destruction logs.
- **Missing Audit Trail:**
  An immutable audit trail recording biometric policy publication dates, consent receipts, and destruction timestamps is absent.

### 12.3 Remediation and Action Plan
1. Publish a standalone Biometric Information Privacy Policy with explicit retention and destruction timelines.
2. Create reusable BIPA consent modal components for applications utilizing biometric authentication or processing.
3. Implement backend data purge routines ensuring biometric data destruction within statutory time limits.
4. Establish automated CI checks verifying that biometric framework imports trigger BIPA consent checks.

---

## 13. US Federal Subscription Cancellation Rules (FTC Click-to-Cancel / Negative Option Rule)

### 13.1 Regulatory Overview and Background
The FTC Negative Option Rule (16 CFR Part 425), commonly known as the "Click-to-Cancel" rule, requires sellers of recurring subscription plans to provide a cancellation mechanism that is as easy to use as the mechanism used to initiate the subscription. For online/in-app subscriptions, cancellation must be available in the same medium and completed with no more steps than sign-up, requiring prominent disclosure of all material terms prior to billing consent.

Official Citation: 16 CFR Part 425 (FTC Trade Regulation Rule on Recurring Subscriptions and Other Negative Option Plans).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a Subscription Terms and Cancellation Policy enforcing Click-to-Cancel principles, billing disclosures, and pre-renewal notification schedules.
- **Missing Documentation:**
  Documentation lacks developer guidelines for designing frictionless in-app cancellation paths that avoid dark patterns (such as required phone calls or multi-step retention surveys).
- **Missing Code:**
  Codebase templates lack self-service one-click cancellation buttons or direct subscription management navigation hooks within account settings.
- **Missing Disclosure:**
  Paywall UI templates fail to display immediate pre-consent disclosures of subscription price, billing frequency, automatic renewal terms, and exact cancellation steps.
- **Missing Logging:**
  No backend logging schemas exist to capture cancellation initiation timestamps, cancellation completion receipts, or pre-renewal notice delivery logs.
- **Missing Testing:**
  Test runner scripts do not verify that the number of interaction steps required to cancel a subscription is equal to or fewer than the steps required to subscribe.
- **Missing Evidence:**
  Lacks templates for cancellation confirmation receipts, pre-billing reminder email logs, or paywall consent verification records.
- **Missing Audit Trail:**
  An audit trail tracking paywall design changes, cancellation flow modifications, and user subscription lifecycle events is absent.

### 13.3 Remediation and Action Plan
1. Draft a Subscription and Click-to-Cancel Policy compliant with 16 CFR Part 425.
2. Add direct, frictionless self-service cancellation paths inside user settings across all subscription UI templates.
3. Update paywall components to display prominent, unambiguous billing terms immediately adjacent to purchase buttons.
4. Implement automated UI tests measuring and comparing sign-up click counts against cancellation click counts.

---

## 14. UK Online Safety Act (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) imposes statutory duties of care on user-to-user services, search services, and app distribution platforms. Developers offering services accessible by children in the UK must perform Children's Access Assessments, conduct risk evaluations, implement robust age assurance or age verification, enforce content moderation for illegal content, and prevent children from encountering harmful content.

Official Citation: Online Safety Act 2023 (c. 50) and Ofcom Statutory Codes of Practice.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a UK Online Safety Policy covering duty of care compliance, Children's Access Assessments, and harmful content prevention protocols.
- **Missing Documentation:**
  Documentation lacks step-by-step guidelines for completing Ofcom-mandated risk assessments or integrating UK-compliant highly effective age assurance.
- **Missing Code:**
  Code templates lack automated risk-based content filtering, age verification gate integrations, or priority illegal content reporting mechanisms.
- **Missing Disclosure:**
  Public documentation and app terms fail to display clear UK-specific safety disclosures, reporting expectations, or child protection measures.
- **Missing Logging:**
  No database logging schemas exist to capture user content reports, age assurance verification results, or illegal content moderation actions.
- **Missing Testing:**
  Test suites lack automated verification of age-gating rules for UK user sessions or safety filter enforcement on user-generated content.
- **Missing Evidence:**
  Lacks completed Children's Access Assessment forms, Ofcom Risk Assessment documentation, or age assurance accuracy verification proofs.
- **Missing Audit Trail:**
  An immutable audit trail recording safety policy revisions, moderation interventions, and risk assessment updates is missing.

### 14.3 Remediation and Action Plan
1. Publish an Online Safety Act Compliance Policy and complete a formal Children's Access Assessment.
2. Build UK-specific age assurance integration layers into mobile onboarding flows.
3. Implement illegal content moderation logging and escalation pipelines in backend services.
4. Establish automated CI checks verifying that UK user flows pass mandatory safety and age-gating checks.

---

## 15. Australia Online Safety Code & Age Assurance Framework

### 15.1 Regulatory Overview and Background
The Australian eSafety Commissioner enforces mandatory industry codes under the Online Safety Act 2021, including the App Distribution Services Code and Class 1C/2 Material regulations. App developers must prevent child exposure to pornography, extreme violence, and severe cyber-abuse, utilizing effective age assurance, default restrictive privacy settings for minors, and accessible reporting channels.

Official Citation: Online Safety Act 2021 (Cth) and Consolidated Industry Codes (App Distribution Services Code).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks an Australian Online Safety and Age Assurance Policy defining content classification, minor protection standards, and eSafety reporting routes.
- **Missing Documentation:**
  Lacks developer guides for implementing default maximum privacy settings for Australian minor accounts or integrating eSafety-compliant reporting buttons.
- **Missing Code:**
  Code templates do not include automatic account restriction logic for minor profiles in Australia or integration with eSafety reporting APIs.
- **Missing Disclosure:**
  In-app terms fail to inform Australian users of safety standards, age restrictions, or direct eSafety Commissioner complaint paths.
- **Missing Logging:**
  No logging schemas exist to record safety complaint filings, moderation resolutions, or age verification audit events for Australian users.
- **Missing Testing:**
  Test routines do not verify that default privacy controls (e.g., hidden profiles, restricted direct messaging) activate automatically for Australian accounts.
- **Missing Evidence:**
  Lacks templates for eSafety compliance reports, age assurance system accuracy proofs, or content moderation audit documentation.
- **Missing Audit Trail:**
  An audit trail tracking safety code compliance reviews, moderation activity logs, and system configuration updates is missing.

### 15.3 Remediation and Action Plan
1. Draft an Australian Online Safety Code Policy and safety classification guide.
2. Implement automated default maximum privacy settings (restricted messaging, hidden location) for minor accounts.
3. Build in-app reporting tools connected to content moderation and incident logging backends.
4. Integrate CI test assertions verifying privacy defaults for Australian geographic user IP ranges.

---

## 16. Brazil Digital ECA (Decreto 12.880 & ANPD Age Verification)

### 16.1 Regulatory Overview and Background
Brazil's Decreto n. 12.880 of 18 March 2026 regulates the Digital Estatuto da Criança e do Adolescente (ECA) alongside the National Data Protection Authority (ANPD) guidelines. Developers offering services to Brazilian users must implement robust age verification/assurance, restrict profiling of children, block addictive design elements, obtain verifiable consent from legal guardians, and minimize data collection.

Official Citation: Decreto n. 12.880 de 18 de Março de 2026 and Lei Geral de Proteção de Dados (LGPD) Lei n. 13.709/2018.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a Brazilian Child and Adolescent Protection Policy aligned with Decreto 12.880 and LGPD Article 14 child data rules.
- **Missing Documentation:**
  Documentation lacks developer runbooks for integrating Brazilian age verification mechanisms or legal guardian consent workflows.
- **Missing Code:**
  Code templates lack native components for capturing CPF/guardian verification signals or disabling profiling and push notification loops for minors.
- **Missing Disclosure:**
  In-app onboarding interfaces fail to display child-friendly privacy notices in Portuguese as required by LGPD Article 14(6).
- **Missing Logging:**
  No backend logging schemas exist to capture legal guardian consent approvals, age verification confirmations, or child profile data purges.
- **Missing Testing:**
  Test suites lack automated test flows verifying that Brazilian accounts marked as minors have profiling, personalized ads, and addictive mechanics disabled.
- **Missing Evidence:**
  Lacks templates for LGPD Relatório de Impacto à Proteção de Dados Pessoais (RIPD) focusing on children, or guardian consent records.
- **Missing Audit Trail:**
  An immutable audit trail recording guardian consent receipts, ECA policy modifications, and data deletion executions is missing.

### 16.3 Remediation and Action Plan
1. Publish a Brazilian Digital ECA and LGPD Child Privacy Policy in Portuguese and English.
2. Build child-friendly Portuguese disclosure screens and guardian consent capture components.
3. Implement backend routines to disable profiling and personalized recommendation features for Brazilian child accounts.
4. Establish automated CI checks verifying child privacy enforcement for Brazil geographic user flows.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act 2023 (DPDPA) and DPD Rules 2025 (G.S.R. 846(E)) regulate personal data processing. Key obligations include itemized multilingual consent notices, verifiable parental consent for children under 18, prohibition of tracking or targeted ads directed at children, integration with registered Consent Managers, and appointing a Data Protection Officer.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPD Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks an Indian Data Protection Policy covering DPDPA obligations, Consent Manager integration, and minor data processing restrictions.
- **Missing Documentation:**
  Documentation lacks guidelines for implementing itemized consent notices in English and scheduled Eighth Schedule Indian languages.
- **Missing Code:**
  Codebase templates lack handlers for interacting with registered Consent Manager APIs, itemized consent selection sheets, or age verification for under-18 accounts.
- **Missing Disclosure:**
  Consent screens fail to display clear, standalone notices outlining data items collected, processing purposes, and withdrawal rights in compliant formats.
- **Missing Logging:**
  No backend logging schemas exist to record itemized consent grants, withdrawal notices, or Consent Manager API transaction tokens.
- **Missing Testing:**
  Test runner scripts do not verify that data collection halts immediately when an Indian user revokes consent via a Consent Manager.
- **Missing Evidence:**
  Lacks templates for DPDPA Data Protection Impact Assessments (DPIA), DPO contact declarations, or Consent Manager audit records.
- **Missing Audit Trail:**
  An immutable audit trail recording historical consent preferences, consent withdrawal requests, and parental consent logs is absent.

### 17.3 Remediation and Action Plan
1. Formulate a DPDPA Compliance Policy and Consent Management Protocol.
2. Develop itemized, multilingual consent UI sheets supporting Eighth Schedule Indian languages.
3. Build backend integration layers for registered Indian Consent Manager API protocols.
4. Add automated CI unit tests verifying immediate API endpoint shutdown upon consent revocation.

---

## 18. Singapore Personal Data Protection Act (PDPA) & OSRAA

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the Online Safety (Relief and Accountability) Act 2025 (OSRAA) establish statutory rules for data protection, mandatory breach notifications within 3 calendar days, age-appropriate design, and content safety relief. Organizations must appoint a Data Protection Officer (DPO), provide explicit opt-in consent, and protect children from online harms.

Official Citation: Personal Data Protection Act 2012 (Act 26 of 2012) and Online Safety (Relief and Accountability) Act 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a Singapore Data Protection and Online Safety Policy establishing DPO oversight, 3-day breach response protocols, and OSRAA safety duties.
- **Missing Documentation:**
  Documentation lacks operational runbooks for executing 72-hour Personal Data Protection Commission (PDPC) data breach notifications.
- **Missing Code:**
  Code templates lack automated breach detection logging utilities, DPO contact access components, or in-app OSRAA safety complaint tools.
- **Missing Disclosure:**
  Privacy notices fail to clearly disclose DPO business contact information or provide mandatory Singapore PDPA consent purpose declarations.
- **Missing Logging:**
  No database schemas exist to log data breach incidents, PDPC notification timelines, or user consent modifications.
- **Missing Testing:**
  Test suites lack automated routines to simulate breach containment timelines and verify DPO contact detail availability.
- **Missing Evidence:**
  Lacks templates for PDPC Breach Notification Forms, Data Protection Impact Assessments (DPIA), or DPO appointment documentation.
- **Missing Audit Trail:**
  An audit trail recording data breach incidents, policy updates, and PDPC correspondence history is missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA and OSRAA Operational Compliance Policy.
2. Publish DPO business contact details prominently across privacy documentation and in-app settings.
3. Implement automated 72-hour data breach incident logging and escalation workflows.
4. Establish CI checks confirming the presence of DPO contact metadata before release.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (in-app payment regulations) and Personal Information Protection Act (PIPA Act No. 21445) mandate third-party in-app payment support, strict consent for personal/location data collection, 1-year data destruction rules for inactive accounts, and mandatory local representative appointment for foreign entities exceeding threshold limits.

Official Citation: Telecommunications Business Act Article 22-9 and Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a South Korea PIPA and In-App Payment Policy covering Korea-specific payment option rights, local representative duties, and inactive account destruction.
- **Missing Documentation:**
  Documentation lacks technical guides for configuring South Korea alternative in-app billing routes or managing Korean location data consent.
- **Missing Code:**
  Code templates lack Korea-specific payment choice modal sheets, local location data consent dialogs, or 1-year inactive account auto-deletion scripts.
- **Missing Disclosure:**
  Privacy policies fail to disclose South Korean local representative details, location data processing terms, or separate automated processing consent notices.
- **Missing Logging:**
  No database schemas exist to log alternative payment fee reporting, location consent grants, or inactive account warning notice dispatches.
- **Missing Testing:**
  Test runner scripts do not verify that 1-year inactive accounts are flagged for data segregation or destruction as required by PIPA Article 39-6.
- **Missing Evidence:**
  Lacks Korean Local Representative designation agreements, KISA compliance certificates, or location data processing registers.
- **Missing Audit Trail:**
  An immutable audit trail recording inactive account notifications, data deletions, and alternative payment transaction logs is missing.

### 19.3 Remediation and Action Plan
1. Formulate a South Korea PIPA and Telecommunications Business Act Compliance Policy.
2. Build South Korea alternative payment choice sheets and explicit location data consent dialogs.
3. Implement automated 1-year inactive account data segregation and destruction workflows.
4. Add automated CI checks verifying South Korea local representative declarations and payment selection availability.

---

## 20. China App Filing & CAC Regulations

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) App Filing rules and Cyberspace Administration of China (CAC) regulations (including Interim Measures for AI Anthropomorphic Interactive Services CAC Order No. 21 and Personal Information Protection Law - PIPL) require mandatory ICP filing for app distribution, strict real-name identity verification, algorithm filing for generative AI, and minor protection modes.

Official Citation: MIIT Notice on App Filing (2023) and CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a China Compliance and AI Security Policy covering MIIT App Filing, CAC algorithm registration, and PIPL cross-border data transfer rules.
- **Missing Documentation:**
  Documentation lacks developer instructions for obtaining ICP filing credentials, completing CAC algorithm security assessments, or implementing Youth Mode.
- **Missing Code:**
  Codebase templates lack real-name identity verification integration handlers, CAC-mandated Youth Mode time-limit controls, or algorithm disclaimer overlays.
- **Missing Disclosure:**
  In-app disclosures fail to display MIIT ICP filing numbers on splash screens or provide mandatory CAC AI anthropomorphic interaction warnings.
- **Missing Logging:**
  No database logging schemas exist to capture real-name authentication logs, Youth Mode usage limits, or CAC security reporting payloads.
- **Missing Testing:**
  Test runner scripts do not verify that Youth Mode automatically restricts usage time (e.g., 40 mins/day) and blocks in-app purchases for minor accounts in China.
- **Missing Evidence:**
  Lacks templates for MIIT ICP filing certificates, CAC Algorithm Security Assessment reports, or PIPL Personal Information Protection Impact Assessments.
- **Missing Audit Trail:**
  An immutable audit trail recording algorithm updates, security filing submissions, real-name verification logs, and Youth Mode enforcement is missing.

### 20.3 Remediation and Action Plan
1. Draft a China Regulatory and CAC AI Compliance Policy.
2. Implement MIIT ICP filing number display components on application startup/splash screens.
3. Build Youth Mode time-limiting and real-name verification UI modules for China-facing builds.
4. Establish automated CI validation verifying ICP number presence and Youth Mode feature toggles for China release targets.

---

## 21. Consolidated Gap Classification Matrix

The following matrix audits all twenty frameworks across the eight compliance dimensions.
- **Covered:** Complete policy, implementation guidance, code, and verification present in the repository.
- **Partial:** Framework named with dated citation in repository, but step-by-step developer implementation or automated guard coverage is incomplete.
- **Missing:** Framework or compliance dimension completely absent from the repository.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act (Art 4 / Gen)**| Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA & Amended Rule**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / OSRAA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea PIPA / TBA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

This comprehensive audit of twenty major global and regional regulations highlights that while the playbook provides strong store rejection coverage and primary legal citations, significant implementation gaps exist across code templates, logging schemas, automated test coverage, compliance evidence artifacts, and immutable audit trails.

Priority Remediation Order:
1. Implement detection rules and UI components for EU GPSR (completely missing end-to-end).
2. Develop code templates and UI handlers for high-impact 2025/2026 mandates: EU Contract Withdrawal Button, EU AI Act Article 50 watermarking, US Click-to-Cancel, and US State ASAA age signal APIs.
3. Build logging schemas and automated pre-commit test scripts across all twenty frameworks to transition "Partial" items to fully "Covered".

This gap report must be updated continuously as regulatory enforcement dates arrive and platform guidance evolves. Always verify primary legal texts on EUR-Lex, FTC, Federal Register, and official gazettes.

---

## 23. Sources

Every regulation named above, cited to its primary official source:

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule, [16 CFR Part 312](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California Privacy Rights Act (CPRA), [Cal. Civ. Code 1798.100](https://leginfo.legislature.ca.gov)
- Illinois BIPA, [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- FTC Negative Option Rule (Click-to-Cancel), [16 CFR Part 425](https://www.ftc.gov)
- UK Online Safety Act 2023, [c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Act 2021, [Act No. 76 of 2021](https://www.legislation.gov.au)
- Brazil Decreto 12.880 & LGPD, [Lei n. 13.709/2018](https://www.in.gov.br)
- India Digital Personal Data Protection Act 2023, [Act No. 22 of 2023](https://egazette.gov.in)
- Singapore PDPA & OSRAA, [Act 26 of 2012](https://sso.agc.gov.sg)
- South Korea PIPA & Telecommunications Business Act, [Act No. 21445](https://www.law.go.kr)
- China CAC Interim Measures for AI Anthropomorphic Services, [CAC Order No. 21](http://www.cac.gov.cn)
