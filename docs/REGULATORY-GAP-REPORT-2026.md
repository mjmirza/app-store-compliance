# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulatory frameworks that bind mobile app developers shipping into the EU, US, UK, Australia, Brazil, Canada, South Korea, India, Singapore, and China, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are missing policy, missing documentation, missing code, missing disclosure, missing logging, missing testing, missing evidence, and missing audit trail.

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

Scope matters here, and it is easy to overstate. The withdrawal button obligation in this Directive attaches to distance financial services contracts, not to every consumer subscription. A general withdrawal button across all distance contracts has been proposed at EU level but is not yet law. Treat it as binding today if your app sells insurance, credit, payment, investment, or another financial service into the EU, and as a strong design default otherwise, since Apple already requires an easy in-app cancellation path regardless.

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
  No automated UI or unit tests exist in the repository to verify that the withdrawal flow can be completed successfully without administrative friction (such as requiring customer service interaction).
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance in the event of consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking the historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with the Distance Marketing of Financial Services Directive.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of all EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination without requiring manual human approval.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977 / HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025/2026), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

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

### 4.3 Remediation and Action Plan
1. Create a detailed written Minor Age Assurance Policy that specifies how state-level requirements are identified and how children's data is strictly minimized.
2. Implement cross-platform native hooks in the mobile codebases to query Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database triggers and automated procedures to purge raw age-verification data immediately after the user's age category is confirmed.
4. Establish automated unit tests that verify that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is successfully processed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy. It mandates that any provider or deployer of AI systems (including mobile application developers utilizing third-party generative AI APIs) must take measures to ensure a sufficient level of AI literacy among their staff and other persons dealing with the operation of AI systems.

This requirement applies to all organizations, with no headcount carve-out, meaning small development teams and solo creators are equally bound. The level of literacy required scales with the technical complexity and impact of the AI integration. Pragmatic compliance for a software engineering team requires maintaining a written policy, team induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI literacy policy, and nothing that helps a small team judge what counts as a sufficient level under Article 4.
- **Missing Documentation:**
  The repository lacks developer-facing documentation or checklists explaining the team's obligations under Article 4 or how to stay updated on emerging AI safety and risk evaluation standards.
- **Missing Code:**
  Not applicable directly to runtime app binaries, but missing tooling to verify team training status during CI/CD builds or pre-commit checks.
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

### 6.3 Remediation and Action Plan
1. Formulate a corporate AI Transparency and Disclosure Policy that mandates direct disclosure and machine-readable output marking.
2. Incorporate explicit, prominent notices (such as "You are chatting with an AI assistant") inside all conversational interface templates.
3. Implement standard metadata injection (using the C2PA specification or cryptographic watermarking) inside all synthetic media generation pipelines.
4. Establish automated integration tests to scan generated media outputs and verify that the machine-readable compliance headers are properly set and preserved.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates designated "gatekeeper" platforms to ensure contestability and fairness in digital markets. For mobile app developers distributing in the EU, the DMA enables alternative app marketplaces, web distribution, third-party payment processing, and non-discriminatory access to hardware/software features (such as NFC for contactless payments and alternative browser engines).

Apple and Google are designated gatekeepers. Developers leveraging DMA entitlements must meet specific compliance, security, reporting, and licensing terms (such as Apple's Attachment 14 and Core Technology Commission framework).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive DMA Operations Policy governing alternative distribution, entitlement management, and transaction reporting.
- **Missing Documentation:**
  While `docs/EU-REGULATORY-2026.md` describes DMA rules, the repository lacks step-by-step developer integration guides for registering, requesting, and managing DMA entitlements in Xcode and Play Console.
- **Missing Code:**
  Code templates lack automated client-side triggers calling `ExternalPurchaseCustomLink` sheets or handling `MarketplaceKit` installation flows.
- **Missing Disclosure:**
  No standard UI components exist for displaying DMA disclosure sheets informing users when they leave the store environment or transact with an alternative payment processor.
- **Missing Logging:**
  There are no backend schemas or API integration models to capture and format monthly transaction reports for submission via Apple's External Purchase Server API.
- **Missing Testing:**
  No automated tests exist to verify that DMA entitlement code is strictly region-gated to EU/EEA storefronts and fails gracefully outside those regions.
- **Missing Evidence:**
  The repository lacks templates for proving acceptance of updated developer agreement attachments (e.g., ADPLA Attachment 14) or verifying alternative marketplace eligibility criteria.
- **Missing Audit Trail:**
  There is no logging system to maintain an immutable record of external purchase transaction disclosures, reporting submissions, and fee reconciliation.

### 7.3 Remediation and Action Plan
1. Draft an Alternative Distribution and Anti-Steering Operational Policy.
2. Build reusable code modules wrapping `ExternalPurchaseCustomLink` and region-gating checks for EU storefronts.
3. Implement automated test scripts to validate monthly reporting log payloads against Apple's External Purchase Server API spec.
4. Add verification routines in `agent-os/hooks/app-store-compliance-guard.sh` to check for DMA entitlement declarations.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) creates a unified framework for online intermediaries, platforms, and marketplaces. Under Articles 30 and 31, app stores are required to verify and display trader status information (address, phone number, email, and payment account details) for all developers distributing apps in the EU.

Developers must declare whether they act as a "trader" or "non-trader". Declaring non-trader status informs EU consumers that EU consumer protection rights do not apply to transactions with the developer.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not supply a formal Trader Status Governance Policy to help organizations classify their developer accounts under EU law.
- **Missing Documentation:**
  Checklists mention DSA trader status but lack detailed instructions on how to complete the 2FA verification and document upload process in App Store Connect and Google Play Console.
- **Missing Code:**
  No static analysis scripts exist in the repository to scan project configuration files or metadata directories for missing trader declarations prior to submission.
- **Missing Disclosure:**
  Templates for in-app "About" pages or web footers lack standardized components for displaying mandatory trader identity information required under national implementations.
- **Missing Logging:**
  There are no backend logging mechanisms to record the verification state, 2FA confirmations, and annual re-verification dates of DSA trader credentials.
- **Missing Testing:**
  No automated tests verify that metadata export packages contain completed DSA trader information before publishing builds to EU storefronts.
- **Missing Evidence:**
  The repository lacks sample documentation packages (e.g., verified utility bills, D-U-N-S registration proofs, official business registers) needed for DSA verification.
- **Missing Audit Trail:**
  An unalterable audit log tracking updates to trader declarations, contact detail modifications, and platform verification confirmations is missing.

### 8.3 Remediation and Action Plan
1. Establish a Trader Status Verification Checklist and Governance Policy.
2. Add automated metadata verification rules in `scripts/metadata-audit.py` to flag unverified or missing DSA trader status fields.
3. Include standard DSA trader disclosure UI blocks in app template libraries.
4. Implement automated CI alerts 30 days prior to mandatory annual DSA re-verification deadlines.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) entered into force in 2019 and became applicable across all EU Member States on 28 June 2025. It mandates accessibility standards for a wide array of digital products and services, including mobile applications, e-commerce, banking, e-books, and transportation services.

Compliance is measured against the harmonised standard EN 301 549 (v3.2.1), which builds on WCAG 2.1 Level AA and includes Chapter 11 specific to non-web software and mobile apps. Microenterprises (fewer than 10 employees and under 2,000,000 euro turnover) are exempt for services only.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an overarching Accessibility Policy detailing organizational commitment to EN 301 549 and WCAG 2.1 AA standards.
- **Missing Documentation:**
  While accessibility is referenced in `docs/PRE-SUBMISSION-CHECKLIST.md`, developer guides lack comprehensive mapping of EN 301 549 Chapter 11 requirements for native iOS and Android components.
- **Missing Code:**
  Although `scripts/accessibility-audit.py` scans basic UI patterns, the repository templates lack built-in accessible component primitives (e.g., custom views with explicit VoiceOver traits or high-contrast theme toggles).
- **Missing Disclosure:**
  Public-facing documentation and app settings lack templates for the legally required Accessibility Statement (EN 301 549 Annex B and C).
- **Missing Logging:**
  There are no logging mechanisms to capture user-reported accessibility bugs, screen-reader compatibility errors, or assistive tech feedback.
- **Missing Testing:**
  Automated testing is limited to static analysis; end-to-end accessibility test flows (e.g., automated VoiceOver/TalkBack navigation scripts) are missing from CI pipelines.
- **Missing Evidence:**
  The repository contains no formal Accessibility Conformance Reports (ACR) or Voluntary Product Accessibility Templates (VPAT) based on EN 301 549.
- **Missing Audit Trail:**
  An immutable record of accessibility evaluations, user testing sessions with disabled users, and remediation milestones is not maintained.

### 9.3 Remediation and Action Plan
1. Adopt an EN 301 549 compliant Accessibility Policy and publish standard Accessibility Statement templates.
2. Expand `scripts/accessibility-audit.py` to cover all 64 EN 301 549 Chapter 11 rules.
3. Integrate automated UI testing for accessibility traits, touch target sizes, and contrast ratios into the pre-submission guard.
4. Generate standard VPAT/ACR template files in the repository for developer compliance packaging.

---

## 10. US Children's Online Privacy Protection Act (COPPA) & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA), 16 CFR Part 312, regulates the online collection of personal information from children under 13 by operators of child-directed websites/apps or general-audience services with actual knowledge of child users.

The FTC finalized major amendments to the COPPA Rule (Federal Register 90 FR 16918), with full compliance mandatory by 22 April 2026. Key changes expand "personal information" to include biometric identifiers and government IDs, require separate opt-in consent for third-party disclosures/targeted ads, mandate written data retention policies, and require a formal written information security program with annual risk assessments.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not contain a compliant Children's Privacy Policy template or a written Data Retention Policy specifically limiting child data retention.
- **Missing Documentation:**
  Step-by-step technical guides for implementing Verifiable Parental Consent (VPC) methods (e.g., knowledge-based auth, face-match ID verification) are missing.
- **Missing Code:**
  Codebase templates lack pre-configured parental gates, age-gating modules, or conditional SDK initialization wrappers to suppress tracking for under-13 users.
- **Missing Disclosure:**
  In-app onboarding flows lack two-tier consent disclosures that separate basic app functionality consent from third-party ad/tracking consent for children.
- **Missing Logging:**
  There are no backend database schemas to log parental consent tokens, verification method types, or consent revocation requests without storing raw PI.
- **Missing Testing:**
  No automated unit or integration tests exist to verify that zero third-party tracking calls or ad SDKs initialize when a user is flagged as under 13.
- **Missing Evidence:**
  The playbook lacks templates for the mandated Written Information Security Program (WISP) and annual risk assessment documentation.
- **Missing Audit Trail:**
  An unalterable audit trail tracking parental consent lifecycle events, consent withdrawals, and automated child data deletion triggers is absent.

### 10.3 Remediation and Action Plan
1. Draft a complete COPPA-compliant Written Information Security Program (WISP) and Data Retention Policy template.
2. Develop modular native age-gating and parental gate code components for iOS and Android.
3. Implement strict automated CI tests verifying that ad SDKs and analytics endpoints are completely disabled under child user profiles.
4. Establish cryptographic logging for parental consent receipts and data purge executions.

---

## 11. California Privacy Rights Act (CPRA / CCPA 2026 Regulations)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA) and the CPPA 2026 Regulations (11 CCR section 7200 et seq.), establishes broad data privacy rights for California residents.

Key requirements include privacy policies, notices at collection, rights to know, delete, correct, and opt-out of sale/sharing (including honoring Global Privacy Control signals), limits on sensitive personal information, automated decision-making technology (ADMT) disclosures, and mandatory risk assessments and cybersecurity audits.

Official Citation: California Civil Code section 1798.100 et seq.; 11 CCR section 7200 et seq.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a comprehensive California Privacy Policy template and a formal Sensitive Personal Information (SPI) Governance Policy.
- **Missing Documentation:**
  Technical guides do not detail how native mobile apps must handle Global Privacy Control (GPC) signals in embedded webviews or native network layers.
- **Missing Code:**
  Code templates do not include "Do Not Sell or Share My Personal Information" or "Limit the Use of My Sensitive Personal Information" toggle components.
- **Missing Disclosure:**
  Onboarding UI flows lack standardized Notice at Collection banners specifying data categories, purposes, and retention periods.
- **Missing Logging:**
  No backend logging schema exists to record consumer rights requests (DSARs), verification outcomes, and 45-day response timeline tracking.
- **Missing Testing:**
  Automated tests do not verify that setting an opt-out preference signal halts data transmission to third-party ad networks.
- **Missing Evidence:**
  The repository lacks template files for CPPA-mandated Risk Assessments and Cybersecurity Audit certifications.
- **Missing Audit Trail:**
  An immutable audit trail documenting DSAR processing history, opt-out signal receptions, and annual policy updates is missing.

### 11.3 Remediation and Action Plan
1. Create a California Notice at Collection and Privacy Policy template compliant with 2026 CPPA regulations.
2. Implement native GPC header detection and state privacy opt-out toggle components.
3. Build a DSAR tracking log schema with automated 45-day deadline alerts.
4. Provide template Risk Assessment and Cybersecurity Audit documentation files.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, regulates the collection, use, safeguarding, handling, and destruction of biometric identifiers and information (such as retina/iris scans, fingerprints, voiceprints, or scans of hand or facial geometry).

BIPA requires written notice, explicit written release prior to collection, a publicly available retention schedule and destruction guidelines, a complete prohibition on profiting from biometric data, and strict statutory damages with a private right of action. SB 2979 (effective August 2024) clarified that multiple collections of the same biometric identifier from an individual constitute a single violation.

Official Citation: 740 ILCS 14 (Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a standalone Biometric Data Policy defining retention schedules and destruction guidelines.
- **Missing Documentation:**
  Developer checklists do not specify BIPA notice and consent requirements when integrating native biometric APIs (Face ID, Touch ID, Android BiometricPrompt).
- **Missing Code:**
  Code templates do not include pre-built BIPA consent modal sheets or secure local-only biometric processing wrappers.
- **Missing Disclosure:**
  Sample app interfaces do not present explicit, written biometric disclosures detailing the specific purpose and length of term for biometric data storage prior to enrollment.
- **Missing Logging:**
  There are no secure logging mechanisms to record written consent capture timestamps and automated destruction events after 3 years or purpose completion.
- **Missing Testing:**
  No automated tests check whether biometric features can be bypassed or initialized without setting a verified consent flag.
- **Missing Evidence:**
  The playbook contains no templates for written biometric releases, vendor BIPA compliance agreements, or destruction certification logs.
- **Missing Audit Trail:**
  An unalterable audit trail recording consent grants, revocation events, and schedule-based biometric data purges is completely absent.

### 12.3 Remediation and Action Plan
1. Draft a comprehensive Biometric Information Privacy Policy and Public Retention Schedule template.
2. Develop native consent UI components for iOS (LocalAuthentication) and Android (BiometricPrompt).
3. Implement automated code checks in `agent-os/hooks/app-store-compliance-guard.sh` detecting raw biometric processing without consent handlers.
4. Establish an immutable audit logging system for biometric consent receipts and destruction logs.

---

## 13. US FTC Subscription Cancellation / Negative Option & ROSCA

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA), 15 U.S.C. 8401 et seq., Section 5 of the FTC Act, and state negative option statutes (e.g., California, New York, Massachusetts) require that auto-renewing subscriptions provide clear and conspicuous disclosures, explicit informed consent, and a simple, frictionless mechanism to cancel.

While the FTC's 2024 Rule amendments were vacated on procedural grounds in July 2025, active enforcement under ROSCA and state laws continues aggressively against "click-to-cancel" friction (e.g., requiring phone calls, mail, or complex chat funnels to cancel online sign-ups).

Official Citations: 15 U.S.C. 8401 (ROSCA); 15 U.S.C. 45 (FTC Act Section 5); 16 CFR Part 425.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a clear Subscription Cancellation Policy outlining frictionless cancellation standards for web and hybrid subscription funnels.
- **Missing Documentation:**
  Developer guidelines do not detail cancellation UI requirements for subscriptions billed outside Apple IAP and Google Play Billing.
- **Missing Code:**
  Codebase templates lack pre-built self-service cancellation components and direct cancellation account settings screens.
- **Missing Disclosure:**
  Subscription paywalls in templates omit required negative option disclosures (billing frequency, recurring cost, cancellation path) immediately adjacent to the call-to-action button.
- **Missing Logging:**
  No backend database schema exists to log cancellation requests, timestamps, confirmation receipts, and automated refund processing triggers.
- **Missing Testing:**
  Automated UI tests do not check that subscription cancellation can be executed in the same number of steps as initial sign-up.
- **Missing Evidence:**
  The repository lacks sample cancellation confirmation emails and audit documentation proving cancellation accessibility.
- **Missing Audit Trail:**
  An immutable audit trail tracking cancellation conversion rates, customer friction reports, and subscription terms update history is missing.

### 13.3 Remediation and Action Plan
1. Formulate a Subscription Transparency and Click-to-Cancel Policy.
2. Create self-service cancellation UI components for cross-platform and web-billed subscriptions.
3. Add automated tests in `scripts/metadata-audit.py` to verify negative option disclosures on paywalls.
4. Build backend cancellation transaction logging and confirmation email generator modules.

---

## 14. UK Online Safety Act 2023 & Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (OSA) and the ICO Age Appropriate Design Code (Children's Code) set stringent child safety, illegal content prevention, and age assurance duties for user-to-user services and search services operating in the UK.

Enforced by Ofcom and the ICO, requirements include illegal content risk assessments, Highly Effective Age Assurance (e.g., facial age estimation, open banking, digital ID), high privacy by default, geolocation off by default, profiling off by default, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023 (c. 50); Data Protection Act 2018 / ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Online Safety Policy covering UK OSA duties, illegal content prevention, and child protection.
- **Missing Documentation:**
  Developer guides do not detail Ofcom-approved Highly Effective Age Assurance integration standards or Children's Code DPIA templates.
- **Missing Code:**
  Code templates do not include default "high privacy" configuration flags (disabling geolocation, profiling, and targeted ads) for UK users.
- **Missing Disclosure:**
  UI templates omit required age-gating notices and clear reporting mechanisms for illegal or harmful content.
- **Missing Logging:**
  No backend logging mechanism exists to record illegal content reports, CSEA hash detections, or Ofcom risk assessment reviews.
- **Missing Testing:**
  No automated tests verify that profiling and location services are disabled by default when a UK child profile is detected.
- **Missing Evidence:**
  The repository lacks templates for mandatory OSA Illegal Content Risk Assessments and Children's Code DPIAs.
- **Missing Audit Trail:**
  An unalterable audit trail recording content moderation actions, takedown timelines, and age assurance verifications is missing.

### 14.3 Remediation and Action Plan
1. Adopt a UK Online Safety Compliance Policy and Children's Code DPIA template.
2. Implement native "High Privacy Default" configuration toggles in mobile templates.
3. Build backend reporting log schemas for illegal content and age verification events.
4. Establish automated CI pipeline checks for default privacy flags on UK builds.

---

## 15. Australia Online Safety Act, App Distribution Services Code & Social Media Minimum Age Act 2024

### 15.1 Regulatory Overview and Background
Australia's regulatory framework includes the Online Safety Act 2021, the App Distribution Services Online Safety Code (registered September 2025), and the Online Safety Amendment (Social Media Minimum Age) Act 2024.

Key requirements enforce an under-16 social media ban for designated platforms, mandatory age assurance and access controls on app stores, strict data ringfencing (age assurance data must be destroyed immediately after use), and maximum penalties reaching 49.5 million Australian dollars.

Official Citations: Online Safety Act 2021; Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an Australian Age-Restricted Services Policy and Data Ringfencing Policy.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides for implementing waterfall age assurance and complying with eSafety codes.
- **Missing Code:**
  Code templates lack automated logic to purge age verification data immediately after confirming age status.
- **Missing Disclosure:**
  UI flows omit statutory Australian age restriction notices and consent disclosures.
- **Missing Logging:**
  There are no backend schemas to record age verification confirmations while ensuring raw identity attributes are not logged.
- **Missing Testing:**
  Automated tests do not verify that under-16 users are blocked from creating accounts on designated social media interfaces.
- **Missing Evidence:**
  The repository lacks template Safety Risk Assessment reports required under the App Distribution Services Code.
- **Missing Audit Trail:**
  An immutable audit log tracking age assurance methodology updates and data destruction executions is missing.

### 15.3 Remediation and Action Plan
1. Draft an Australian Social Media Minimum Age & Data Ringfencing Policy.
2. Implement automated data purging procedures for raw age verification artifacts.
3. Build integration tests verifying age-based account creation blocks for under-16 users in Australia.
4. Provide template eSafety risk assessment documentation files.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto n. 12.880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and regulating Decree n. 12.880 of March 2026, enforced by the ANPD, establish rigorous child and adolescent protection rules across digital platforms, mobile apps, and app stores.

Key mandates require robust age verification (self-declaration checkboxes are explicitly banned; document verification, facial age estimation, or CPF database checks are required), verifiable guardian consent, automatic age rating display before download, blocking gambling/lottery apps for minors, and strict penalties up to 50 million reais per violation.

Official Citations: Lei n. 15.211/2025; Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Brazil Digital ECA Compliance Policy governing adolescent protection and age verification.
- **Missing Documentation:**
  Developer guides do not detail integration with ANPD-approved age verification methods or Google Play Age Signals API for Brazil.
- **Missing Code:**
  Codebase templates do not contain logic to replace simple checkbox age gates with ANPD-compliant verification flows.
- **Missing Disclosure:**
  In-app onboarding flows omit required Portuguese-language age verification and parental authorization disclosures.
- **Missing Logging:**
  No backend logging schema exists to record guardian authorization grants, contestation logs, and age signal receptions.
- **Missing Testing:**
  Automated tests do not verify that gambling, loot box, or mature features are blocked when a Brazilian user profile is under 18.
- **Missing Evidence:**
  The playbook contains no templates for ANPD Age Assurance Impact Assessments or guardian consent records.
- **Missing Audit Trail:**
  An unalterable audit trail recording age signal evaluations, parental consent grants, and account restrictions is missing.

### 16.3 Remediation and Action Plan
1. Establish a Brazil Digital ECA Compliance Policy and Portuguese disclosure templates.
2. Integrate Google Play Age Signals API (`com.google.android.play:age-signals`) and iOS Declared Age Range API for Brazil storefronts.
3. Create automated tests blocking loot box and gambling features for under-18 Brazilian accounts.
4. Build secure logging schemas for guardian authorization receipts and ANPD audit records.

---

## 17. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and the DPDP Rules 2025 establish a comprehensive data protection regime.

Key provisions mandate explicit, itemized consent notices available in 22 official Indian languages, verifiable parental consent before processing data of minors (under 18) via government-backed platforms (e.g., DigiLocker), strict bans on tracking and targeted advertising directed at children, and integration with registered Consent Managers.

Official Citations: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025 (G.S.R. 846(E)).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Compliance Policy and Children's Data Processing Policy.
- **Missing Documentation:**
  Developer guides omit instructions for multi-language consent notice implementation and DigiLocker VPC integration.
- **Missing Code:**
  Code templates lack integration modules for Indian Consent Managers or automated suppressors for behavioral ads targeting under-18 users.
- **Missing Disclosure:**
  Sample UIs omit itemized, multi-lingual consent notices in Schedule 8 languages detailing data processing purposes.
- **Missing Logging:**
  No backend schema exists to record consent state changes, Consent Manager API tokens, or Data Principal erasure requests.
- **Missing Testing:**
  Automated tests do not verify that behavioral tracking SDKs are completely suppressed for Indian minor accounts.
- **Missing Evidence:**
  The repository contains no template Data Protection Impact Assessments (DPIAs) required for Significant Data Fiduciaries.
- **Missing Audit Trail:**
  An unalterable audit log tracking consent grants, withdrawals, and Consent Manager API synchronization is missing.

### 17.3 Remediation and Action Plan
1. Formulate an India DPDPA Data Protection Policy and multi-lingual consent notice templates.
2. Develop code interfaces for Indian Consent Manager APIs and DigiLocker verifiable parental consent workflows.
3. Build automated unit tests verifying the total suppression of ad targeting for under-18 Indian users.
4. Establish immutable logging schemas for consent lifecycle events and Data Principal rights executions.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice for Online Safety

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act 2012 (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services regulate data protection and child safety.

Key requirements include designating a Data Protection Officer (DPO), mandatory 3-day breach notification to the PDPC, and mandatory app-store age assurance (effective April 2026) to prevent users under 18 from downloading age-inappropriate applications, with strict data minimization barring post-verification retention.

Official Citations: Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety (2025/2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Singapore PDPA Policy and IMDA Online Safety Compliance Policy.
- **Missing Documentation:**
  Checklists omit developer runbooks for 3-day PDPC breach notification protocols and DPO designation procedures.
- **Missing Code:**
  Code templates lack native hooks to process age assurance signals and immediately destroy raw verification artifacts.
- **Missing Disclosure:**
  Sample app settings lack mandatory disclosures identifying the Data Protection Officer and detailing data transfer practices.
- **Missing Logging:**
  No backend logging schema exists to track breach detection timestamps and 72-hour regulatory notification lifecycles.
- **Missing Testing:**
  Automated tests do not check that raw age verification tokens are automatically deleted from local and server storage.
- **Missing Evidence:**
  The playbook lacks sample PDPC Breach Notification Reports and IMDA Compliance Self-Assessment forms.
- **Missing Audit Trail:**
  An unalterable audit trail recording DPO review decisions, breach assessments, and age data destruction events is missing.

### 18.3 Remediation and Action Plan
1. Draft a Singapore PDPA Policy and 72-Hour Breach Notification Protocol.
2. Implement native code modules to handle IMDA age signals and execute immediate data purges.
3. Add automated checks in `scripts/release-audit.py` verifying DPO contact disclosures in app metadata.
4. Build secure logging schemas for breach detection and notification audit trails.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment (Act No. 21445)

### 19.1 Regulatory Overview and Background
South Korea's legal framework includes the Telecommunications Business Act (mandating alternative in-app payment choices) and the Personal Information Protection Act (PIPA) Amendment (Act No. 21445, effective September 2026).

Key mandates require allowing alternative payment processors (with strict platform commission reporting, e.g., Apple's 26% Korea-specific entitlement), executive-level CPO accountability, strict cross-border data transfer disclosures, and stringent breach notification timelines.

Official Citations: Telecommunications Business Act; Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Alternative Payment & PIPA Compliance Policy.
- **Missing Documentation:**
  Developer guides omit detailed instructions for setting up Korea-specific iOS binaries (`SKExternalPurchase = "KR"`), modal disclosure sheets, and monthly sales reporting.
- **Missing Code:**
  Code templates lack native wrappers for Korea alternative billing SDKs (KCP, Toss, Inicis, NICE) and custom disclosure sheets.
- **Missing Disclosure:**
  App Store listings and in-app checkout flows lack mandatory statutory disclosures regarding alternative payment terms and cross-border data transfers.
- **Missing Logging:**
  No backend schema exists to aggregate monthly Korea alternative payment transaction totals for 15-day reporting cycles.
- **Missing Testing:**
  Automated tests do not verify that Korean alternative billing flows display required system disclosure sheets before processing.
- **Missing Evidence:**
  The repository lacks sample monthly transaction report files and CPO designation certification records.
- **Missing Audit Trail:**
  An immutable audit trail recording alternative payment transactions, platform fee calculations, and reporting submissions is missing.

### 19.3 Remediation and Action Plan
1. Establish a South Korea Alternative Payment & PIPA Compliance Policy.
2. Build native code modules for `SKExternalPurchase` ("KR") entitlement gating and approved Korean payment gateway integrations.
3. Implement backend transaction aggregation scripts matching Apple's 15-day monthly reporting spec for Korea.
4. Provide template cross-border data transfer notices and CPO governance documentation.

---

## 20. China App Filing (MIIT ICP Extension) & CAC Regulations (Order No. 21)

### 20.1 Regulatory Overview and Background
China's digital regulatory environment mandates Mobile App Filing with the Ministry of Industry and Information Technology (MIIT) as an extension of the ICP licensing system, alongside CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services) and PIPL privacy rules.

Key obligations require all apps distributed in China to be filed through a local Chinese entity, enforce real-name identity verification, automatically switch minors into "Minors Mode", ban AI companion/chat services for minors under 14, and maintain strict content moderation and data localization.

Official Citations: MIIT Mobile App Filing Notice (2023/2024); CAC Order No. 21 (2026); Personal Information Protection Law (PIPL).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a China Regulatory Compliance Policy covering MIIT filing, PIPL, and CAC AI rules.
- **Missing Documentation:**
  Developer guides lack step-by-step instructions for completing MIIT app filing through local Chinese entity partners.
- **Missing Code:**
  Codebase templates lack automated "Minors Mode" switching logic, real-name identity verification integration, and CAC-compliant content filters.
- **Missing Disclosure:**
  App interfaces omit required Chinese-language ICP/app filing numbers in app footers and settings screens, as well as CAC AI interaction notices.
- **Missing Logging:**
  No backend schema exists to record real-name verification statuses, Minors Mode activation events, and CAC content filter triggers.
- **Missing Testing:**
  Automated tests do not check that AI chat and companion features are completely disabled when a user is flagged as a minor under 14 in China.
- **Missing Evidence:**
  The repository contains no sample MIIT Filing Certificates, Banhao game licenses, or PIPL Personal Information Protection Impact Assessments (PIPIA).
- **Missing Audit Trail:**
  An unalterable audit log tracking MIIT filing status, real-name verification logs, and CAC compliance audit reports is missing.

### 20.3 Remediation and Action Plan
1. Adopt a China App Compliance & MIIT Filing Policy.
2. Develop native "Minors Mode" UI components and real-name verification API wrappers.
3. Build automated build-time checks verifying that China-targeted builds contain valid MIIT filing numbers in metadata.
4. Establish immutable logging schemas for CAC content moderation and real-name verification audit trails.

---

## 7. Consolidated Gap Classification Matrix

The table below summarizes the compliance coverage status across all twenty audited global and regional regulations across the eight core gap categories.
- **Covered**: Fully implemented with policy, documentation, code, disclosures, logging, testing, evidence, and audit trails.
- **Partial**: Named and referenced with dated sources and deadlines, but missing actionable code, testing, or evidence templates.
- **Missing**: Not currently addressed in repository codebase, documentation, or tooling.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence Package** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Contract Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4 (Literacy)** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50 (Transparency)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU Digital Markets Act (DMA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU Digital Services Act (DSA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act (EAA)**| Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA & Amended Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA / CCPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US FTC Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act & Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety Framework**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA & DPDP Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC Rules** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 8. Conclusion and Future Monitoring

The playbook demonstrates strong coverage of store-level submission rejection rules (Apple App Review Guidelines and Google Play Content Policies). However, when evaluated against broader statutory legal frameworks that bind mobile applications after release, significant actionable gaps remain.

While nineteen of the twenty audited regulations are documented with dated sources and deadlines in `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, and `data/regulatory-deadlines.json`, the implementation layer—specifically actionable code components, automated test suites, evidence templates, and immutable audit logging schemas—remains incomplete.

To close these gaps systematically, development priorities are structured as follows:

1. **Immediate (GPSR & High-Priority Enforcement)**: Integrate EU GPSR metadata validation and safety warning disclosures into `data/rejection-patterns.json` and `scripts/metadata-audit.py`.
2. **Code & UI Primitives**: Build reusable native code components for EU Article 50 AI disclosures, Contract Withdrawal buttons, Declared Age Range / Play Age Signals handlers, and Global Privacy Control header parsers.
3. **Automated Testing & Guard Enforcement**: Expand `agent-os/hooks/app-store-compliance-guard.sh` and script test runners to validate statutory disclosures, age gating, and privacy default configurations prior to app submission.
4. **Evidence & Audit Tooling**: Provide standardized written policy templates (WISP, DPIA, VPAT/ACR, AI Literacy Logs) and backend database schemas for audit trail logging.

This gap report is a living document and must be continuously re-evaluated against official primary publications (EUR-Lex, FTC, Federal Register, Ofcom, ANPD, OAIC, CAC) as regulatory deadlines mature.

---

## 9. Sources

Every regulation named in this report is cited directly to its primary official source under the strict Priority 1 source trust hierarchy:

- EU General Product Safety Regulation (GPSR): [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services Directive (Withdrawal Button): [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act (DMA): [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act (DSA): [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act (EAA): [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Children's Online Privacy Protection Act (COPPA) Rule: [16 CFR Part 312 (FTC)](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California Privacy Rights Act & Regulations: [CPPA Regulations (11 CCR section 7200 et seq.)](https://cppa.ca.gov/regulations/ccpa_updates.html)
- Illinois Biometric Information Privacy Act (BIPA): [740 ILCS 14 (ILGA)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US FTC Negative Option Rule & ROSCA: [FTC Rulemaking (16 CFR Part 425)](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option)
- UK Online Safety Act 2023 & Children's Code: [ICO Children's Code Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- Australia Online Safety Framework & Legislation: [Parliament of Australia Bills](https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId=r7268)
- Brazil Digital ECA: [Decreto n. 12.880/2026 (Planalto)](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India Digital Personal Data Protection Act & Rules: [Gazette of India (egazette.gov.in)](https://egazette.gov.in)
- Singapore Personal Data Protection Act & IMDA Code: [PDPC Singapore](https://www.pdpc.gov.sg/overview-of-pdpa/the-legislation/personal-data-protection-act)
- South Korea Personal Information Protection Act: [Ministry of Government Legislation (law.go.kr)](https://law.go.kr)
- China Mobile App Filing & CAC Regulations: [Cyberspace Administration of China (cac.gov.cn)](https://www.cac.gov.cn)
