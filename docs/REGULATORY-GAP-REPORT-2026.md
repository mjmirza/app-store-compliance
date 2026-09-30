# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind app developers shipping mobile and web applications worldwide, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

Assume the repository is incomplete unless proven otherwise.

## Source trust hierarchy and methodology

All analysis and cited legal frameworks within this report adhere to the strict source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, ANPD, CAC, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless corroborated traceably by Priority 1 publications. In line with repository guidelines, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital systems, online marketplaces, and e-commerce applications, the GPSR mandates that online interfaces clearly display product safety warnings, instructions, manufacturer and importer identity, and electronic contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template policy to establish an EU-based Responsible Person or to determine whether their listing falls inside Regulation (EU) 2023/988.
- **Missing Documentation:**
  The repository is missing specific developer checklists, guides, or instructional manuals on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack any rules or patterns to scan codebase files for GPSR-related elements. Additionally, mock user interfaces and templates in this repository do not contain code blocks for displaying manufacturer identity or product safety warnings.
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
2. Incorporate GPSR-specific metadata requirements into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory that demonstrate compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script that verifies the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. Adopted in 2023, the mandatory compliance enforcement date is 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window to produce user data is 10 days, but in critical emergency cases, providers are legally required to produce requested data within a strict 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy, so a team receiving an EU judicial order has no guidance on who may act on it or how to authenticate authority.
- **Missing Documentation:**
  While the repository mentions the e-Evidence Package, it lacks concrete operational runbooks or manuals for handling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:**
  There are no automated scripts or secure API endpoints in the repository's backend mock implementations to assist in securely exporting, filtering, and packaging user data in response to a valid legal order.
- **Missing Disclosure:**
  Public-facing documentation fails to explicitly disclose to EU users that their data may be preserved or disclosed to European law enforcement in accordance with Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository does not contain database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, data access activities, or data releases.
- **Missing Testing:**
  There are no integration tests or validation flows to simulate the rapid 8-hour emergency retrieval and secure packaging of user data under simulated pressure.
- **Missing Evidence:**
  The repository is missing verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for compliance officers to study and verify.
- **Missing Audit Trail:**
  A secure, unalterable audit trail system to record every administrative interaction, data extraction, and transmission made by compliance officers during a legal request is completely absent.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol establishing roles and secure channels for executing EPOs.
2. Formally designate an EU establishment or legal representative before the 18 August 2026 deadline.
3. Build secure backend scripts to automate extraction and encryption of requested datasets within the 8-hour emergency window.
4. Establish a tamper-proof audit trail to log all incoming certificates, verification checks, data extractions, and secure transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or function on the online interface for distance contracts for financial services concluded by electronic means.

The statutory withdrawal period is 14 days from contract conclusion. The cancellation path must be direct, clear, and as simple as the sign-up path. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day withdrawal right, and no guidance separating financial services apps in scope from general consumer subscriptions.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying placement, size, prominence, and terminology required to make the withdrawal button compliant with EU expectations.
- **Missing Code:**
  The front-end user interface templates and billing mock codes in this repository do not contain any functional implementation of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining terms of contract revocation.
- **Missing Logging:**
  There are no logging mechanisms designed to capture and record when a user clicks the withdrawal button, the timestamp of the request, confirmation of contract termination, or refund flow initiation.
- **Missing Testing:**
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow completes without administrative friction or manual customer service interaction.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent "Withdrawal Button" component inside account settings of subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions.
4. Implement automated end-to-end UI tests to verify frictionless contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minors' access to mobile applications, in-app purchases, and content updates.

Developers must request user age categories (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download apps, make purchases, or access major updates. Raw age verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minor age assurance policy explaining how to handle minor accounts across Utah, Texas, Louisiana, and Alabama.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API.
- **Missing Code:**
  The mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  In-app onboarding flows do not display required state disclosures explaining that user age categories are requested to comply with state laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no secure backend system designed to log parental consent receipt, consent revocations, or the immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests to verify that minor accounts are blocked from premium features or purchases without valid consent signals.
- **Missing Evidence:**
  The repository does not contain templates of parental consent agreements, identity verification logs, or data minimization records for state AG reviews.
- **Missing Audit Trail:**
  An immutable audit trail recording the rollout of age-assurance features, consent policy updates, and immediate verification data deletion is absent.

### 4.3 Remediation and Action Plan
1. Create a Minor Age Assurance Policy detailing state-level requirements and data minimization.
2. Implement cross-platform native hooks querying Apple Declared Age Range and Google Play Age Signals APIs during onboarding.
3. Build database triggers to purge raw age-verification data immediately after confirming user age categories.
4. Establish automated unit tests verifying that minor age bands disable in-app billing until consent flags pass.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) mandates AI literacy. Providers and deployers of AI systems must take measures to ensure a sufficient level of AI literacy among their staff and persons operating AI systems.

This applies to all organizations regardless of size. Pragmatic compliance requires maintaining a written policy, induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining team obligations under Article 4 or how to stay updated on AI safety standards.
- **Missing Code:**
  The repository lacks automated helper scripts or static lints to verify if an active AI literacy log exists prior to committing AI-related code changes.
- **Missing Disclosure:**
  Public-facing documentation, recruitment materials, or partner contracts do not disclose the organization's commitment to AI literacy standards mandated by Article 4.
- **Missing Logging:**
  The repository is missing an active, centralized training log or registry to track employee inductions, course completions, and regular literacy refreshers.
- **Missing Testing:**
  There are no automated internal lints or CLI tools to verify that team members committing AI changes have valid, up-to-date literacy records.
- **Missing Evidence:**
  The playbook has no example of what acceptable evidence looks like, such as a completed training log, course completion certificates, or written risk assessments.
- **Missing Audit Trail:**
  There is no historical audit trail documenting when the AI literacy policy was reviewed, when training modules were updated, or how team training records evolved.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy defining required competency areas (AI safety, risk assessment, data privacy, bias identification).
2. Create `AI_LITERACY_LOG.md` within the repository to track training dates, modules, team member names, and verification methods.
3. Set up an automated check in the CI pipeline warning if the literacy log has not been reviewed within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act dictates transparency obligations for AI systems, taking effect on 2 August 2026.

Article 50(1) requires informing users when interacting with AI systems. Article 50(2) requires marking generative AI outputs (text, audio, image, video) in a machine-readable format detectable as artificially generated. Article 50(4) requires deepfake deployers to disclose artificial generation.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI transparency policy covering disclosure timing and generated media marking requirements.
- **Missing Documentation:**
  Checklists mention Article 50 but lack technical developer instructions for implementing machine-readable watermarking (e.g., C2PA) or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes, middle-tier layers, or utilities to inject machine-readable watermarks into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display the immediate disclosure ("You are interacting with an AI system") at the time of first exposure.
- **Missing Logging:**
  There are no database logging schemas or tracking mechanisms to record that an AI transparency warning was successfully displayed to a specific user session.
- **Missing Testing:**
  Existing test scripts do not check for synthetic media markers or verify that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository is missing factual evidence of compliance, such as independent security assessments of content moderation filters or proof of metadata retention.
- **Missing Audit Trail:**
  An unalterable audit trail recording technical choices, vendor audits, model changes, and disclosure modifications is not maintained.

### 6.3 Remediation and Action Plan
1. Formulate an AI Transparency Policy mandating direct disclosure and machine-readable output marking.
2. Incorporate explicit notices ("You are chatting with an AI assistant") inside conversational UI templates.
3. Implement standard metadata injection (C2PA specification) inside synthetic media pipelines.
4. Establish automated integration tests scanning media outputs for machine-readable compliance headers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates designated gatekeepers (such as Apple and Google) and grants rights to business users (developers).

Developers distributing apps in the EU can utilize alternative app marketplaces, web distribution, and alternative payment processors, but must comply with gatekeeper platform policies, reporting obligations, and security checks.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template DMA Compliance and Alternative Distribution Policy outlining rights and obligations when using alternative app stores or web distribution.
- **Missing Documentation:**
  Documentation does not detail technical setup requirements for alternative distribution frameworks (e.g., Apple Marketplace Kit, Web Distribution entitlement) or Core Technology Fee (CTF) / Core Technology Commission (CTC) accounting rules.
- **Missing Code:**
  The codebase contains no code or helper scripts for handling alternative payment processing links or DMA-compliant external link out-flow modals.
- **Missing Disclosure:**
  Templates do not provide in-app disclosures informing users when transactions are processed via alternative payment processors outside app store billing.
- **Missing Logging:**
  No logging mechanisms exist to capture transaction records, installation metrics, or reporting logs required for DMA fee calculations.
- **Missing Testing:**
  Automated tests do not verify that alternative payment links function correctly or that external link out-flow modals comply with gatekeeper UI guidelines.
- **Missing Evidence:**
  The repository lacks templates for DMA entitlement applications, gatekeeper security attestations, or alternative store registration filings.
- **Missing Audit Trail:**
  An audit trail tracking changes in distribution channels, payment processor integrations, and CTF/CTC accounting declarations is missing.

### 7.3 Remediation and Action Plan
1. Publish a DMA Alternative Distribution Guide detailing entitlement requirements and fee structures.
2. Build UI code templates for DMA-compliant external payment link outs and modal notices.
3. Add automated test suites verifying alternative payment link flows and required modal displays.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) imposes obligations on online intermediary services, platforms, and marketplaces operating in the EU.

App developers acting as "traders" selling goods, services, or digital content to EU consumers must publish verified trader information (name, address, telephone, email, trade register number) on app store listings. Platforms hosting user-generated content (UGC) must implement Notice and Action mechanisms and illegal content reporting paths.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template DSA Trader Compliance Policy and UGC Moderation Protocol.
- **Missing Documentation:**
  Documentation does not provide developer guidance on collecting and maintaining verified trader credentials for store listings under Article 30 DSA.
- **Missing Code:**
  Codebases lack UI components and backend handlers for Notice and Action mechanisms allowing users to report illegal content under Article 16 DSA.
- **Missing Disclosure:**
  Mock store listings and in-app templates do not include designated DSA trader contact information or mandatory UGC content reporting disclosures.
- **Missing Logging:**
  No database schemas exist to log incoming illegal content reports, moderation actions, user appeals, or response timestamps.
- **Missing Testing:**
  Test suites fail to validate that Notice and Action flows submit reports successfully and generate confirmation receipts to reporters.
- **Missing Evidence:**
  The repository lacks sample DSA Transparency Reports, moderation logs, or trader verification records.
- **Missing Audit Trail:**
  An audit trail recording content moderation decisions, appeal outcomes, and annual DSA transparency reporting data is completely missing.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Information and UGC Notice & Action Policy template.
2. Develop front-end Notice & Action UI modals and backend report-processing scripts.
3. Integrate unit tests validating user reporting flows and automated confirmation receipts.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) requires products and services (including mobile applications, e-commerce, banking, e-books, and ticketing apps) placed on the EU market to be accessible to persons with disabilities. Compliance became mandatory on 28 June 2025.

Apps must align with EN 301 549 standards (harmonized with WCAG 2.1 AA), covering screen readers, dynamic text scaling, color contrast, keyboard navigation, and alternative input methods.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a written Mobile Accessibility Policy defining WCAG 2.1 AA / EN 301 549 standards and accessibility maintenance protocols.
- **Missing Documentation:**
  While accessibility is mentioned, developer guidelines lack detailed technical specifications for VoiceOver/TalkBack labels, touch target sizes, and contrast ratios.
- **Missing Code:**
  Code templates lack accessibility traits, semantic headings, `accessibilityLabel` attributes, and dynamic type scaling adjustments across iOS and Android views.
- **Missing Disclosure:**
  App metadata and in-app settings do not contain an Accessibility Statement detailing compliance status, supported assistive technologies, and feedback contact details.
- **Missing Logging:**
  No logging mechanisms exist to capture accessibility feedback, complaints, or assistive technology compatibility errors reported by users.
- **Missing Testing:**
  Automated accessibility scanning tools (such as axe-core or Accessibility Scanner) are not integrated into CI workflows to catch visual or structural accessibility regressions.
- **Missing Evidence:**
  The repository contains no sample Accessibility Conformance Reports (VPAT / EN 301 549 evaluation results) or third-party audit reports.
- **Missing Audit Trail:**
  An audit trail tracking historical accessibility code reviews, accessibility bug remediations, and statement updates is absent.

### 9.3 Remediation and Action Plan
1. Publish an Accessibility Policy and EN 301 549 compliance guide.
2. Add accessibility attributes and dynamic type scaling to all code UI components.
3. Integrate `scripts/accessibility-audit.py` into CI workflows and enforce zero-regression gates.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The FTC Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312 (including amended rules taking effect in 2026), regulates apps directed to children under 13 or general-audience apps with actual knowledge of child users.

COPPA requires verifiable parental consent (VPC) before collecting personal information, strict data minimization, clear privacy notices, zero targeted advertising / behavioral profiling of children, and immediate data deletion upon parental request.

Official Citation: 16 CFR Part 312 (FTC COPPA Rule).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a dedicated COPPA Compliance Policy outlining VPC mechanisms, neutral age gates, and ad-network restriction rules.
- **Missing Documentation:**
  Documentation does not provide step-by-step developer instructions for implementing neutral age gates, disabling tracking SDKs for child users, or handling FTC age-verification methods.
- **Missing Code:**
  Mock codebases do not contain neutral age gate components or logic to strip advertising IDs (IDFA/GAID) and analytics SDKs for child profiles.
- **Missing Disclosure:**
  In-app disclosures do not include direct parental notices detailing specific data points collected, VPC requirements, and parental rights to review/delete child data.
- **Missing Logging:**
  No database logging exists to record parental consent approvals, verification method types, or parental deletion requests.
- **Missing Testing:**
  Automated tests do not verify that neutral age gates block child users from entering personal info or that ad SDKs remain uninitialized for under-13 users.
- **Missing Evidence:**
  The repository lacks templates for FTC Safe Harbor certifications, parental consent logs, or ad-network compliance attestations.
- **Missing Audit Trail:**
  An immutable audit trail recording child data deletion operations, SDK initialization flags, and annual COPPA policy audits is missing.

### 10.3 Remediation and Action Plan
1. Formulate a COPPA Compliance Policy and neutral age gate implementation guide.
2. Build UI code templates for neutral age gates and dynamic SDK initialization control.
3. Create unit tests ensuring ad SDKs and personal data collection are disabled for minor user states.

---

## 11. California Privacy Rights Act & CCPA (CPRA/CCPA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA), 11 CCR section 7000 et seq., regulates the collection and processing of California residents' personal information.

Requirements include explicit privacy disclosures, opt-out rights for the sale or sharing of personal data ("Do Not Sell or Share My Personal Information"), global privacy control (GPC) signal processing, data minimization, risk assessments, and dedicated mechanisms for consumer rights requests (access, deletion, correction).

Official Citation: California Civil Code section 1798.100 et seq., 11 CCR Division 6.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a California Privacy Policy template addressing CPRA consumer rights, sensitive personal information handling, and retention schedules.
- **Missing Documentation:**
  Documentation does not detail how developers must implement Global Privacy Control (GPC) signal detection or CPRA risk assessment workflows.
- **Missing Code:**
  Codebases lack automated GPC header/signal detection logic (`Sec-GPC`), opt-out toggle components, or backend handler APIs for deletion and access requests.
- **Missing Disclosure:**
  Interface templates do not include "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information" links and notices.
- **Missing Logging:**
  No backend logging exists to capture consumer rights request submissions, verification steps, fulfillment timestamps, or opt-out preference updates.
- **Missing Testing:**
  Test suites fail to verify that GPC signals automatically set opt-out flags or that deletion APIs correctly cascade deletion to third-party sub-processors.
- **Missing Evidence:**
  The playbook contains no sample CPRA Cybersecurity Audits, Privacy Impact Assessments (PIAs), or annual consumer request metrics reports.
- **Missing Audit Trail:**
  An unalterable audit trail recording consumer rights request fulfillments, GPC signal processing history, and vendor data agreement updates is missing.

### 11.3 Remediation and Action Plan
1. Create a California Privacy Rights Policy and GPC integration specification.
2. Build code components for GPC header detection and "Do Not Sell/Share" UI toggles.
3. Establish automated unit tests validating GPC signal handling and consumer deletion request handlers.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, capture, purchase, receipt, storage, and handling of biometric identifiers and information (face scans, fingerprints, voiceprints, iris scans).

BIPA requires written policy disclosure, explicit written consent prior to biometric collection, strict prohibition of profiting from biometric data, mandated retention schedules, and destruction guidelines.

Official Citation: 740 ILCS 14 (Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template Biometric Data Privacy Policy detailing retention schedules and destruction guidelines mandated by 740 ILCS 14/15(a).
- **Missing Documentation:**
  Developer guides fail to detail BIPA compliance requirements for mobile features utilizing Face ID, Touch ID, or custom biometric authentication/analysis models.
- **Missing Code:**
  Mock codebases do not contain BIPA-compliant pre-collection written consent modal components or backend destruction triggers for stored biometric templates.
- **Missing Disclosure:**
  Onboarding UI templates do not display explicit BIPA written disclosures informing users of biometric data collection, purpose, and storage duration before capture.
- **Missing Logging:**
  No database schemas exist to log written biometric consent receipts, timestamped consent acceptances, or automated destruction executions.
- **Missing Testing:**
  Test suites do not verify that biometric capture features remain inaccessible until affirmative written consent is logged.
- **Missing Evidence:**
  The repository contains no sample BIPA consent forms, biometric data flow diagrams, or destruction certification records.
- **Missing Audit Trail:**
  An audit trail recording biometric consent capture, policy reviews, and template destruction timestamps is absent.

### 12.3 Remediation and Action Plan
1. Draft a Biometric Information Privacy Policy and consent template.
2. Build UI consent modal components required before invoking biometric APIs.
3. Implement automated test cases verifying biometric feature gating based on explicit consent logs.

---

## 13. US FTC Subscription Cancellation Rules (Click-to-Cancel)

### 13.1 Regulatory Overview and Background
The FTC Rule on Negative Option Plans (Click-to-Cancel Rule), 16 CFR Part 425, prohibits deceptive subscription practices and mandates that cancelling a subscription must be as easy as signing up.

Key requirements include clear pre-consent disclosures of subscription terms, explicit consent for negative option features, simple one-click or frictionless cancellation mechanisms on the same medium used to subscribe, and annual subscription reminders.

Official Citation: 16 CFR Part 425 (FTC Trade Regulation Rule on Negative Option Plans).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template Negative Option Subscription Policy aligned with FTC Click-to-Cancel requirements.
- **Missing Documentation:**
  Documentation does not provide developer guidelines on structuring subscription paywalls, placement of terms disclosures, or frictionless cancellation design rules.
- **Missing Code:**
  Code templates lack self-service one-click subscription cancellation UI buttons or backend billing cancellation integrations.
- **Missing Disclosure:**
  Paywall UI templates fail to display FTC-mandated disclosures (billing frequency, recurring charge amount, cancellation procedure) immediately adjacent to the call-to-action button.
- **Missing Logging:**
  No logging mechanisms exist to capture user consent for recurring billing, timestamped terms exposures, or self-service cancellation submissions.
- **Missing Testing:**
  Automated UI tests do not verify that subscription cancellation completes without forced user retention surveys or phone/chat redirections.
- **Missing Evidence:**
  The playbook contains no sample subscription paywall audit reports, pre-consent billing logs, or cancellation friction assessments.
- **Missing Audit Trail:**
  An audit trail tracking paywall UI modifications, cancellation flow changes, and consent log archives is missing.

### 13.3 Remediation and Action Plan
1. Formulate an FTC Click-to-Cancel Compliance Policy and paywall design checklist.
2. Build front-end self-service cancellation components and adjacent paywall disclosure layouts.
3. Integrate end-to-end tests validating frictionless self-service cancellation flows.

---

## 14. UK Online Safety Act 2023

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 imposes duties of care on user-to-user services and search services to protect users (especially children) from illegal content and content harmful to children.

Requirements include mandatory risk assessments, robust age assurance / verification mechanisms, illegal content takedown workflows, user reporting tools, and transparent terms of service disclosures.

Official Citation: Online Safety Act 2023 (c. 50).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a UK Online Safety Act Compliance Policy and Child Safety Duty of Care Protocol.
- **Missing Documentation:**
  Developer guidelines do not detail Ofcom statutory guidance, age assurance technical standards, or illegal content risk assessment steps.
- **Missing Code:**
  Codebases lack user-to-user reporting tools, automated content filtering hooks, or age verification integration modules for UK users.
- **Missing Disclosure:**
  App terms of service and onboarding screens do not contain mandatory disclosures regarding illegal content policies, child protection measures, or user reporting paths.
- **Missing Logging:**
  No database schemas exist to log reported content, moderation actions, age assurance verification results, or Ofcom compliance metrics.
- **Missing Testing:**
  Test suites fail to validate that user reporting UI components correctly submit illegal content flags to moderation backends.
- **Missing Evidence:**
  The playbook contains no sample Ofcom Illegal Content Risk Assessments, Protection of Children Risk Assessments, or moderation logs.
- **Missing Audit Trail:**
  An immutable audit trail recording content moderation decisions, age assurance policy changes, and safety audit reports is missing.

### 14.3 Remediation and Action Plan
1. Draft an Online Safety Policy aligned with Ofcom statutory codes of practice.
2. Build UI reporting components for user-generated content and age verification hooks.
3. Add automated unit tests verifying content flag submissions and moderation logging.

---

## 15. Australia Online Safety Act & Age Minimum Legislation

### 15.1 Regulatory Overview and Background
Australia's Online Safety Act 2021 and the Online Safety Amendment (Social Media Minimum Age) Act 2024 enforce strict online safety expectations, mandatory industry codes, and an under-16 age restriction for specified social media platforms.

Requirements include implementing age assurance to prevent under-16 access on restricted services, rapid removal of cyberbullying or non-consensual intimate imagery, and clear reporting channels.

Official Citations: Online Safety Act 2021, Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Online Safety & Minimum Age Policy template detailing age-gating and eSafety Commissioner reporting obligations.
- **Missing Documentation:**
  Documentation does not provide developer guidance on eSafety Commissioner Industry Codes (Class 1C/2 material) or approved age assurance techniques.
- **Missing Code:**
  Codebases lack age verification gating logic for under-16 Australian users or automated content removal request endpoints.
- **Missing Disclosure:**
  App onboarding UI templates fail to display required notices explaining Australian age restriction rules and eSafety complaint mechanisms.
- **Missing Logging:**
  No database schemas exist to log age assurance verification results, under-16 blocking events, or eSafety takedown notice executions.
- **Missing Testing:**
  Test suites do not verify that Australian IP/locale users under 16 are blocked from account creation on age-restricted services.
- **Missing Evidence:**
  The repository contains no sample eSafety Industry Code compliance attestations or age assurance trial evaluations.
- **Missing Audit Trail:**
  An audit trail recording age gate updates, under-16 access rejections, and regulatory notice fulfillments is missing.

### 15.3 Remediation and Action Plan
1. Create an Australian Online Safety Compliance Policy and age-gating protocol.
2. Build age verification gating logic and eSafety notice reporting components.
3. Integrate automated unit tests validating under-16 user blocking for Australian locales.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Law No. 15,211/2025 (Digital ECA) and regulating Decreto n. 12.880 of 18 March 2026 establish child and adolescent protection standards for digital products, operating systems, and app stores in Brazil.

Key obligations include mandatory age signals/assurance, highest-privacy default settings for minor users, prohibition of behavioral profiling/targeted ads for children, and accessible reporting channels for parents and minors.

Official Citations: Lei No. 15,211/2025, Decreto No. 12.880 de 18 de Marco de 2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy outlining minor data protection and default privacy settings.
- **Missing Documentation:**
  Developer guidelines do not detail Decreto 12.880 technical standards, ANPD guidance, or age signal processing rules for Brazilian users.
- **Missing Code:**
  Codebases lack logic to automatically apply highest-privacy defaults (disabled tracking, private profile) when a Brazilian age signal indicates a minor user.
- **Missing Disclosure:**
  In-app disclosures do not provide Brazilian Portuguese notices explaining child data protection rights, parental controls, and complaint channels.
- **Missing Logging:**
  No logging mechanisms exist to capture age signal receipt, minor privacy default enforcement, or parental consent approvals in Brazil.
- **Missing Testing:**
  Test suites fail to verify that Brazilian minor users automatically receive maximum privacy defaults and zero targeted advertising.
- **Missing Evidence:**
  The repository contains no sample ANPD child privacy impact assessments or Digital ECA compliance reports.
- **Missing Audit Trail:**
  An audit trail tracking Brazilian age signal integrations, minor account privacy setting changes, and ANPD notice responses is missing.

### 16.3 Remediation and Action Plan
1. Formulate a Digital ECA Compliance Policy in Brazilian Portuguese and English.
2. Implement code hooks enforcing highest-privacy settings upon receiving minor age signals.
3. Build unit tests validating minor privacy default application for Brazilian users.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA), 2023 (Act No. 22 of 2023) and Digital Personal Data Protection Rules 2025 regulate processing of digital personal data in India.

Key requirements include clear and itemized consent notices in English and 22 scheduled Indian languages, verifiable parental consent before processing children's data, zero tracking/behavioral monitoring of children, appointment of Data Protection Officers (DPO), and integration with registered Consent Managers.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), G.S.R. 846(E).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a DPDPA Data Protection Policy detailing Data Fiduciary obligations, Consent Manager frameworks, and child data rules.
- **Missing Documentation:**
  Developer guides do not provide technical instructions for supporting multi-language consent notices (22 languages) or Consent Manager API integrations.
- **Missing Code:**
  Codebases lack multi-lingual consent notice rendering components, verifiable parental consent hooks for under-18 users, or DPDPA deletion API handlers.
- **Missing Disclosure:**
  In-app consent screens fail to display itemized, stand-alone consent notices specifying exact personal data points and purposes in the chosen scheduled language.
- **Missing Logging:**
  No backend logging exists to record consent preferences, language choices, parental verification receipts, or withdrawal requests.
- **Missing Testing:**
  Test suites do not verify that consent withdrawal immediately stops personal data processing or that child accounts block ad tracking.
- **Missing Evidence:**
  The repository contains no sample DPDPA Data Protection Impact Assessments (DPIA), DPO appointment records, or Consent Manager integration certificates.
- **Missing Audit Trail:**
  An immutable audit trail recording consent logs, language selection history, and parental consent verifications is missing.

### 17.3 Remediation and Action Plan
1. Draft a DPDPA Compliance Policy and multi-lingual consent specification.
2. Build UI components for itemized multi-language consent notices and parental consent logic.
3. Integrate test suites validating consent log creation and deletion API execution.

---

## 18. Singapore PDPA & IMDA App Distribution Online Safety Code

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA 2012) and the IMDA Code of Practice for Online Safety for App Distribution Services enforce data protection, mandatory breach notifications, and online safety standards for app developers distributing apps in Singapore.

Requirements include explicit consent, purpose limitation, age assurance for content tiers, child safety standards, and mandatory reporting of data breaches to the PDPC within 3 business days.

Official Citations: Personal Data Protection Act 2012, IMDA App Distribution Online Safety Code (2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore PDPA Policy and IMDA Online Safety Protocol covering 3-day breach reporting and age assurance rules.
- **Missing Documentation:**
  Developer guidelines do not detail PDPC breach notification criteria or IMDA rating classification and content moderation requirements.
- **Missing Code:**
  Codebases lack age assurance components for restricted content tiers or automated data breach payload generators.
- **Missing Disclosure:**
  App listing and in-app privacy policies do not disclose Singapore DPO contact info or IMDA-aligned age rating justifications.
- **Missing Logging:**
  No database schemas exist to log consent choices, data access requests, or internal breach detection alerts.
- **Missing Testing:**
  Test suites fail to verify that data breach detection routines trigger compliance notification workflows within required timeframes.
- **Missing Evidence:**
  The playbook contains no sample PDPC Breach Notification Reports, DPO appointment filings, or IMDA safety code self-assessments.
- **Missing Audit Trail:**
  An audit trail recording breach response activities, consent updates, and IMDA compliance reviews is missing.

### 18.3 Remediation and Action Plan
1. Create a Singapore PDPA Policy and breach response runbook.
2. Build UI age gate components for IMDA restricted content tiers.
3. Integrate automated tests verifying breach detection notification triggers.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendments

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (Article 22-9) and Personal Information Protection Act (PIPA, Act No. 21445 amendment) regulate app store payments, in-app billing alternatives, biometric data handling, and executive accountability.

Key requirements include supporting third-party in-app payment processors without unfair discrimination, explicit consent for personal/biometric data processing, local legal representation, and designating the CEO/executive as the accountable party.

Official Citations: Telecommunications Business Act Article 22-9, PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Regulatory Compliance Policy detailing alternative payment options and PIPA executive accountability rules.
- **Missing Documentation:**
  Developer guidelines do not detail technical steps for integrating KCC-approved alternative payment gateways or PIPA local representative requirements.
- **Missing Code:**
  Codebases lack alternative payment selection UI components for South Korean users or PIPA consent management handlers.
- **Missing Disclosure:**
  In-app checkout screens do not display Korea-specific alternative payment terms, service fee disclosures, or local legal agent contact details.
- **Missing Logging:**
  No logging mechanisms exist to capture alternative payment transaction records, service fee calculations, or PIPA consent withdrawals.
- **Missing Testing:**
  Test suites do not verify that South Korean users are presented with third-party payment options during checkout.
- **Missing Evidence:**
  The playbook contains no sample KCC compliance filings, local representative agreements, or PIPA audit certificates.
- **Missing Audit Trail:**
  An audit trail tracking alternative payment integration updates, fee reporting, and PIPA policy modifications is missing.

### 19.3 Remediation and Action Plan
1. Draft a South Korea Payment & PIPA Compliance Policy.
2. Build UI checkout components supporting Korean alternative payment gateways.
3. Integrate test suites validating alternative payment UI presentation for Korean locales.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Rules

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) Mobile App Filing requirement and Cyberspace Administration of China (CAC) Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services) regulate app distribution and AI services in China.

Requirements include mandatory ICP app filing numbers displayed in store metadata and in-app, local Chinese legal entity partnership, mandatory identification of minor users with automatic switching to Minors Mode, and real-name identity verification.

Official Citations: MIIT App Filing Rules (2024), CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a China Market Compliance Policy covering MIIT ICP filing, real-name verification, and CAC AI Minors Mode requirements.
- **Missing Documentation:**
  Developer guidelines do not detail the step-by-step process for obtaining MIIT app filings or implementing CAC-compliant AI Minors Modes.
- **Missing Code:**
  Codebases lack components for displaying ICP filing numbers in app settings/about screens, real-name authentication modules, or AI Minors Mode toggles.
- **Missing Disclosure:**
  App store metadata and in-app screens fail to display valid MIIT ICP filing numbers or CAC-mandated AI interaction warnings.
- **Missing Logging:**
  No database schemas exist to log real-name verification statuses, Minors Mode session durations, or AI conversation moderation flags.
- **Missing Testing:**
  Test suites fail to verify that enabling Minors Mode restricts AI chat features and enforces time limits.
- **Missing Evidence:**
  The repository contains no sample MIIT ICP filing confirmation certificates, CAC AI security assessment filings, or real-name vendor contracts.
- **Missing Audit Trail:**
  An audit trail recording ICP filing updates, Minors Mode session logs, and CAC security audit submissions is missing.

### 20.3 Remediation and Action Plan
1. Formulate a China Compliance Policy detailing MIIT ICP filing and CAC AI rules.
2. Build UI components displaying ICP filing credentials and AI Minors Mode controls.
3. Add automated unit tests verifying Minors Mode feature restrictions.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act (EAA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CPRA/CCPA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US FTC Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

This comprehensive audit evaluates twenty major global and regional regulatory frameworks binding modern web and mobile applications. While the playbook effectively covers store rejection mechanics and legal reference documentation, significant gaps remain across actionable implementation layers: written policies, code UI components, database logging schemas, automated test suites, compliance evidence templates, and unalterable audit trails.

Addressing these missing requirements ensures full organizational integrity and regulatory readiness across all target jurisdictions.

---

## 23. Sources

Every regulation named above is cited to its official primary source:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Contract Withdrawal: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- US State ASAA: Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA: 16 CFR Part 312 (FTC)
- California Privacy: California Civil Code section 1798.100 et seq., 11 CCR Division 6
- Illinois BIPA: 740 ILCS 14
- US FTC Subscription Cancellation: 16 CFR Part 425
- UK Online Safety Act: Online Safety Act 2023 (c. 50)
- Australia Online Safety: Online Safety Act 2021 & Amendment 2024
- Brazil Digital ECA: Lei No. 15,211/2025 & Decreto No. 12.880/2026
- India DPDPA: Digital Personal Data Protection Act, 2023 (G.S.R. 846(E))
- Singapore PDPA & IMDA: Personal Data Protection Act 2012 & IMDA Online Safety Code
- South Korea TBA & PIPA: Telecommunications Business Act Art 22-9 & Act No. 21445
- China App Filing & CAC: MIIT App Filing Rules & CAC Order No. 21
