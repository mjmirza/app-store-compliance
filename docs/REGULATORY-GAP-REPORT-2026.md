# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, India, South Korea, Singapore, Canada, Japan, and China, checking honestly how far this repository carries each one, what it only mentions in passing, and what it does not cover at all.

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
  While rejection-patterns contains pattern BOTH-GPSR-COMPLIANCE-MISSING, mock user interfaces and templates in this repository do not contain code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
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
2. Incorporate GPSR-specific metadata requirements (manufacturer address, email, product identifier) into `docs/PRE-SUBMISSION-CHECKLIST.md`.
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
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors (under 18 or under 16, depending on the state) to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack precise, step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
- **Missing Code:**
  Although rejection patterns contain pattern BOTH-US-ASAA-COMPLIANCE-MISSING, mock client implementations in the codebase do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
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
  While pattern EU-AI-ACT-ART-4-LITERACY-MISSING exists in patterns, no code check exists to verify whether an AI literacy training record file exists during pipeline builds.
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

## 7. US Amended COPPA Rule (16 CFR Part 312)

### 7.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) finalized amendments to the Children's Online Privacy Protection Act (COPPA) Rule (90 FR 16918), taking effect 23 June 2025 with general compliance mandatory by 22 April 2026. The expanded rule expands the definition of personal information to include biometric identifiers and government identifiers, requires separate opt-in consent for third-party disclosures and targeted advertising, mandates written data retention policies, and requires a written information security program.

Official Citation: 16 CFR Part 312 (90 FR 16918).

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template COPPA Written Data Retention Policy (312.10) or a COPPA Information Security Program policy (312.8).
- **Missing Documentation:**
  No developer guide exists detailing how to implement separate opt-in consent flows for third-party data sharing versus core app operation.
- **Missing Code:**
  Codebase templates do not contain code for knowledge-based authentication or government ID facial matching consent handlers.
- **Missing Disclosure:**
  Child-directed app templates do not include separate, explicit opt-in disclosure UI components for targeted advertising or ad-vendor data transfers.
- **Missing Logging:**
  No backend logging schema exists to record separate consent states (core service consent vs. advertising disclosure consent) or data retention deletion logs.
- **Missing Testing:**
  No automated tests verify that access to core app features remains unblocked when a parent denies third-party advertising disclosure consent.
- **Missing Evidence:**
  The repository lacks sample annual risk assessments or written security program documentation required under 312.8.
- **Missing Audit Trail:**
  No audit trail exists to track data retention schedule enforcement or historical parent consent revocations.

---

## 8. European Accessibility Act (EAA) / EN 301 549

### 8.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) became applicable on 28 June 2025, mandating accessibility for consumer mobile applications and digital services across the EU, referencing harmonised standard EN 301 549 Chapter 11 (WCAG 2.1 AA).

Official Citation: Directive (EU) 2019/882.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Organizational Accessibility Policy template covering ongoing compliance governance under EN 301 549.
- **Missing Documentation:**
  Documentation lacks a step-by-step guide for generating and publishing the legally mandated EAA Accessibility Statement (EN 301 549 Annex B/C).
- **Missing Code:**
  While static accessibility scanners exist in `scripts/accessibility-audit.py`, code templates lack built-in accessible component primitives for non-standard UI widgets.
- **Missing Disclosure:**
  Mobile app UI templates lack in-app accessibility disclosure modals or links to published accessibility statements.
- **Missing Logging:**
  No logging mechanism exists to capture user accessibility settings or screen reader compatibility feedback.
- **Missing Testing:**
  Automated tests in `scripts/accessibility-audit-test.sh` cover standard rules but do not perform comprehensive automated screen reader navigation checks.
- **Missing Evidence:**
  The repository lacks sample Accessibility Conformance Reports (VPAT / EN 301 549 evaluation reports).
- **Missing Audit Trail:**
  No audit trail tracks historical accessibility regression remediation or annual statement updates.

---

## 9. UK Online Safety Act 2023 & ICO Children's Code

### 9.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom from 25 July 2025) and the ICO Age Appropriate Design Code mandate highly effective age assurance, high privacy by default, data minimization, and mandatory Data Protection Impact Assessments (DPIAs) for services likely to be accessed by children.

Official Citation: UK Online Safety Act 2023; ICO Age Appropriate Design Code.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No UK Child Safety and Age Assurance Policy template exists in the playbook.
- **Missing Documentation:**
  The repository lacks a step-by-step developer guide for conducting and documenting a Children's Code DPIA.
- **Missing Code:**
  No code templates exist for integrating UK-approved highly effective age assurance methods (e.g. open banking, facial age estimation SDKs).
- **Missing Disclosure:**
  In-app onboarding templates do not provide UK-specific child safety and age assurance privacy notices.
- **Missing Logging:**
  No logging schema exists to record DPIA completion or age verification signal verification without storing prohibited child PII.
- **Missing Testing:**
  No automated tests verify that geolocation and profiling defaults are strictly disabled when a UK child account is flagged.
- **Missing Evidence:**
  The repository lacks completed sample Children's Code DPIA templates.
- **Missing Audit Trail:**
  No audit trail tracks Ofcom compliance risk reviews or historical age assurance mechanism updates.

---

## 10. Australia Online Safety Amendment Act 2024

### 10.1 Regulatory Overview and Background
Enforceable from 10 December 2025, Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts, requiring ringfencing and immediate deletion of age assurance data.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Under-16 Account Prevention Policy.
- **Missing Documentation:**
  Documentation does not detail eSafety Commissioner guidance or the required waterfall age assurance evaluation.
- **Missing Code:**
  No code exists to enforce immediate purging of Australian age verification token data post-verification.
- **Missing Disclosure:**
  No in-app disclosure component informs Australian users of statutory age restrictions and data ringfencing.
- **Missing Logging:**
  No secure, privacy-preserving log tracks the destruction timestamp of age-assurance verification tokens.
- **Missing Testing:**
  No unit test validates that under-16 account creation attempts are blocked and reported correctly.
- **Missing Evidence:**
  Sample independent eSafety compliance audit report templates are missing.
- **Missing Audit Trail:**
  No audit trail records historical changes to Australian age-gating rules or data destruction procedures.

---

## 11. Brazil Digital ECA (Law 15,211/2025)

### 11.1 Regulatory Overview and Background
Enforceable from 17 March 2026, Brazil's Digital ECA sets strict age verification rules for apps accessible to minors, banning simple self-declaration checkboxes and requiring document verification, facial age estimation, or CPF database checks.

Official Citation: Law 15,211/2025 (Estatuto da Criança e do Adolescente Digital).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Brazilian Digital ECA Compliance Policy template is provided in the repository.
- **Missing Documentation:**
  No guide exists for integrating ANPD-approved age verification workflows (such as CPF validation).
- **Missing Code:**
  Code templates lack CPF database check integration helpers or facial estimation API wrappers.
- **Missing Disclosure:**
  UI templates lack explicit LGPD/Digital ECA age verification consent disclosures.
- **Missing Logging:**
  No backend schema logs ANPD compliance verification events.
- **Missing Testing:**
  No automated test verifies that a simple checkbox self-declaration fails compliance checks for Brazil storefront builds.
- **Missing Evidence:**
  The repository lacks sample ANPD age-assurance compliance filings.
- **Missing Audit Trail:**
  No audit trail tracks changes to Brazilian age verification mechanisms or parent consent logs.

---

## 12. India Digital Personal Data Protection Act (DPDPA) 2023 & DPDP Rules 2025

### 12.1 Regulatory Overview and Background
Notified on 13 November 2025 with enforcement from 13 May 2027, India's DPDPA requires verifiable parental consent via government-backed systems (e.g., DigiLocker) for users under 18, and bans behavioral tracking and targeted ads for children.

Official Citation: DPDPA 2023 / DPDP Rules 2025.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Indian Minor Data Protection Policy template exists in the playbook.
- **Missing Documentation:**
  Developer guides lack instructions for DigiLocker or virtual token verifiable parental consent integration.
- **Missing Code:**
  No backend code exists to parse Indian government-backed consent tokens or toggle off ad tracking for Indian minor accounts.
- **Missing Disclosure:**
  UI templates lack multilingual DPDPA-compliant notice and consent components (in 22 scheduled languages).
- **Missing Logging:**
  No logging schema records parent consent token verification from Indian identity platforms.
- **Missing Testing:**
  No test verifies that ad SDKs are completely initialized in zero-tracking mode for under-18 Indian users.
- **Missing Evidence:**
  Sample Data Protection Officer (DPO) registration and consent artifact templates are absent.
- **Missing Audit Trail:**
  No audit trail tracks parent consent verification or DPDPA data principal request handling.

---

## 13. South Korea Telecommunications Business Act & PIPA

### 13.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options (requiring 26% commission reporting, specific approved gateways, and modal sheets), while PIPA imposes strict data protection and CEO accountability rules.

Official Citation: Telecommunications Business Act; Personal Information Protection Act (PIPA).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a South Korea Alternative Payment & PIPA Compliance Policy template.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for South Korea-specific binary builds and StoreKit external purchase entitlements (`SKExternalPurchase = "KR"`).
- **Missing Code:**
  No client code templates exist for showing the mandatory Korean external payment modal sheet or integration with KCP/Inicis/Toss gateways.
- **Missing Disclosure:**
  UI templates lack the mandatory pre-transaction external payment disclosure text required by South Korean regulators.
- **Missing Logging:**
  No backend schema logs monthly 15-day external purchase sales reporting metrics for Apple/Google remittance in Korea.
- **Missing Testing:**
  No automated UI test verifies that Korean builds show the mandatory modal sheet before diverting to external web checkout.
- **Missing Evidence:**
  The repository lacks sample monthly sales reporting spreadsheets or remittance confirmation artifacts.
- **Missing Audit Trail:**
  No audit trail tracks Korea-specific entitlement modifications or external payment transaction logs.

---

## 14. Singapore IMDA Code of Practice for Online Safety

### 14.1 Regulatory Overview and Background
Effective 1 April 2026, Singapore's IMDA Code of Practice requires app distribution services and app developers to implement robust age assurance to prevent under-18s from downloading age-inappropriate content.

Official Citation: IMDA Code of Practice for Online Safety for App Distribution Services.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore Online Safety & Age Assurance Policy template exists.
- **Missing Documentation:**
  No guide details IMDA age rating classifications or platform age-gating requirements for Singapore storefronts.
- **Missing Code:**
  Codebase templates lack hooks to check Singapore age assurance status prior to allowing feature access.
- **Missing Disclosure:**
  UI templates lack Singapore-specific content rating disclosures.
- **Missing Logging:**
  No backend logging schema records age assurance verification tokens for Singapore users.
- **Missing Testing:**
  No automated test verifies that 18+ content is blocked for unverified Singapore accounts.
- **Missing Evidence:**
  Sample IMDA safety compliance declaration templates are missing.
- **Missing Audit Trail:**
  No audit trail records age assurance data deletion logs post-verification.

---

## 15. China Mobile App Filing (MIIT) & PIPL

### 15.1 Regulatory Overview and Background
Mandatory since 2024, China's MIIT Mobile App Filing requires local entity partnership, real-name registration, PIPL data localization, and Banhao licenses for games.

Official Citation: MIIT Mobile Application Filing Rules; Personal Information Protection Law (PIPL).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China App Distribution & PIPL Cross-Border Transfer Policy template is provided.
- **Missing Documentation:**
  Documentation lacks a detailed guide for MIIT ICP app filing, Banhao licensing, and real-name authentication.
- **Missing Code:**
  Codebase templates lack real-name identity verification (national ID) API wrappers or local server data routing toggles.
- **Missing Disclosure:**
  UI templates lack PIPL-compliant separate consent disclosures for personal data processing and cross-border transfers.
- **Missing Logging:**
  No backend logging schema logs real-name verification events or PIPL consent logs.
- **Missing Testing:**
  No automated test verifies that unverified China accounts are restricted from interactive or social features.
- **Missing Evidence:**
  The repository lacks sample MIIT filing proof documents or PIPL Security Assessment reports.
- **Missing Audit Trail:**
  No audit trail tracks real-name verification record changes or PIPL data export audits.

---

## 16. US Subscription Cancellation (ROSCA & State Laws)

### 16.1 Regulatory Overview and Background
Despite the Eighth Circuit vacatur of the FTC's federal Click-to-Cancel rule, ROSCA and state laws (California, New York, Massachusetts) strictly require subscription cancellation paths to be at least as easy as sign-up (e.g. frictionless online/in-app cancellation).

Official Citation: Restore Online Shoppers' Confidence Act (15 U.S.C. 8401); California Cal. Bus. & Prof. Code 17600.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a Online Subscription Cancellation & Negative Option Policy template.
- **Missing Documentation:**
  Documentation lacks guidelines for building 1-click or self-service online cancellation flows for web-billed subscriptions.
- **Missing Code:**
  While rejection pattern BOTH-SUBSCRIPTION-HARD-CANCEL exists, web/backend templates lack complete self-service cancellation API endpoints.
- **Missing Disclosure:**
  UI templates lack pre-checkout negative option disclosures (renewal terms, cancellation instructions).
- **Missing Logging:**
  No logging schema records subscription cancellation request timestamps and confirmation delivery.
- **Missing Testing:**
  No automated test verifies that cancellation can be completed in the same number of steps as initial subscription signup.
- **Missing Evidence:**
  Sample cancellation confirmation receipt templates and state compliance review artifacts are missing.
- **Missing Audit Trail:**
  No audit trail tracks changes to cancellation flows or customer retention flow interventions.

---

## 17. FTC Health Breach Notification Rule (16 CFR Part 318)

### 17.1 Regulatory Overview and Background
The FTC's 2024 Final Rule applies to non-HIPAA covered health apps, treating unauthorized sharing of health or sensitive personal data with third-party advertisers as a breach requiring 60-day notification.

Official Citation: 16 CFR Part 318 (89 FR 47028).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Non-HIPAA Health App Data Breach Notification Policy template.
- **Missing Documentation:**
  No guide exists detailing health data sharing boundaries with analytics and ad SDKs.
- **Missing Code:**
  Code templates lack health data isolation wrappers to prevent accidental transmission to third-party ad networks.
- **Missing Disclosure:**
  Health app onboarding templates lack explicit disclosures regarding potential third-party SDK access.
- **Missing Logging:**
  No security logging schema tracks health data egress or unauthorized SDK transfers.
- **Missing Testing:**
  No automated test scans outgoing network traffic from health app builds for health data leaks to known ad domains.
- **Missing Evidence:**
  Sample FTC breach notification letter templates are missing.
- **Missing Audit Trail:**
  No audit trail records health data access audits or vendor data transfer reviews.

---

## 18. California CPRA & CPPA 2026 Regulations

### 18.1 Regulatory Overview and Background
The CPPA 2026 regulations mandate Global Privacy Control (GPC) signal honoring, strict opt-outs for sale/sharing/profiling, and limits on Sensitive Personal Information (SPI) processing.

Official Citation: Cal. Civ. Code 1798.100 et seq.; CPPA Regulations 2026.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No CPRA/CPPA Sensitive Personal Information & Automated Decision-Making Policy template is provided.
- **Missing Documentation:**
  Documentation lacks technical instructions for detecting and processing the `Sec-GPC` header in webviews and native apps.
- **Missing Code:**
  No native code helper exists to automatically map platform opt-out signals to internal GPC opt-out flags.
- **Missing Disclosure:**
  UI templates lack standard "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links/modals.
- **Missing Logging:**
  No backend schema logs GPC signal receipt or opt-out preference persistence.
- **Missing Testing:**
  No automated test verifies that enabling GPC header immediately halts ad tracking SDK initialization.
- **Missing Evidence:**
  Sample Risk Assessment and Cybersecurity Audit reports (CPPA 2026 standards) are missing.
- **Missing Audit Trail:**
  No audit trail tracks user opt-out/opt-in preference changes or GPC signal processing history.

---

## 19. Illinois Biometric Information Privacy Act (BIPA)

### 19.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) requires written notice and release prior to capturing biometrics, a publicly available retention schedule, destruction within 3 years, and prohibits sale of biometric data.

Official Citation: 740 ILCS 14 (as amended by SB 2979 in 2024).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No BIPA Biometric Data Management & Retention Policy template is available in the repository.
- **Missing Documentation:**
  Developer guides lack instructions on implementing BIPA-compliant written releases and public destruction schedules.
- **Missing Code:**
  Codebase templates lack biometrics capture wrapper components that block camera/sensor access until a written release is e-signed.
- **Missing Disclosure:**
  UI templates lack explicit BIPA pre-capture written notice and consent modal sheets.
- **Missing Logging:**
  No backend logging schema records written release consent timestamps or mandatory 3-year deletion triggers.
- **Missing Testing:**
  No test verifies that biometric hardware APIs (Face ID / BiometricPrompt) cannot be invoked before release confirmation.
- **Missing Evidence:**
  Sample BIPA consent release forms and retention schedule documents are missing.
- **Missing Audit Trail:**
  No audit trail tracks biometric data collection events, user deletion requests, or purge verification logs.

---

## 20. EU Data Act & Cyber Resilience Act (CRA)

### 20.1 Regulatory Overview and Background
The EU Data Act (Regulation (EU) 2023/2854) mandates access-by-design for connected product data, while the Cyber Resilience Act (Regulation (EU) 2024/2847) requires mandatory vulnerability reporting and security-by-design.

Official Citation: Regulation (EU) 2023/2854; Regulation (EU) 2024/2847.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Data Act & CRA Security-by-Design and Vulnerability Management Policy template.
- **Missing Documentation:**
  Documentation lacks developer runbooks for ENISA 24-hour vulnerability reporting and connected device data export.
- **Missing Code:**
  No code templates exist for user-facing connected device data download or automated vulnerability report generation.
- **Missing Disclosure:**
  UI templates lack CRA security update notices or Data Act data-sharing disclosures.
- **Missing Logging:**
  No logging schema records connected device telemetry export requests or active vulnerability remediation logs.
- **Missing Testing:**
  No automated test verifies that IoT/connected device companion app endpoints expose raw data export capabilities.
- **Missing Evidence:**
  Sample CRA Software Bill of Materials (SBOM) and vulnerability report artifacts are missing.
- **Missing Audit Trail:**
  No audit trail tracks security patch rollouts, vulnerability notifications, or data sharing request processing.

---

## 21. Consolidated Gap Classification Matrix Across Twenty Regulations

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Partial | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Missing | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Missing | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Missing | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Missing | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Missing | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **7. US Amended COPPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **8. EAA / EN 301 549** | Missing | Covered | Covered | Missing | Missing | Covered | Missing | Missing |
| **9. UK Online Safety Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **10. AU Online Safety Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **11. Brazil Digital ECA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **12. India DPDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **13. SK Telecom / PIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **14. SG IMDA Code** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **15. China MIIT / PIPL** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **16. US Subscription Cancel** | Missing | Partial | Partial | Missing | Missing | Missing | Missing | Missing |
| **17. FTC Health Breach** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **18. California CPRA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **19. Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **20. EU Data Act / CRA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Action Plan

This comprehensive gap analysis demonstrates that while the repository accurately tracks regulatory timelines, deadlines, and high-level descriptions across major global jurisdictions, it carries systematic gaps in the operational compliance layer (written policies, code primitives, logging schemas, automated tests, evidence artifacts, and unalterable audit trails).

In priority order:
1. **Policy & Evidence Layer:** Create standardized, customizable template policies and evidence forms for high-impact 2025/2026 regulations (GPSR, e-Evidence, ASAA, COPPA, BIPA, AI Act Article 4/50).
2. **Code Primitives & UI Components:** Implement ready-to-use UI components and backend helpers for age gating (Declared Age Range / Age Signals), withdrawal buttons, GPC headers, and C2PA synthetic media watermarking.
3. **Automated Testing & Audit Trails:** Expand test scripts to validate compliance disclosures, data minimization triggers, and audit logging schemas across all supported platforms.

## 23. Sources

Every regulation named above, at its primary source.

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- FTC Amended COPPA Rule, [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- UK Online Safety Act 2023, [UK Legislation](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Act, [Federal Register of Legislation](https://www.legislation.gov.au/C2024A00114/asmade/text)
- Brazil Digital ECA, [Law 15,211/2025](https://www.in.gov.br/)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://www.meity.gov.in/content/digital-personal-data-protection-act-2023)
- South Korea Telecommunications Business Act & PIPA, [Korea Legislation Research Institute](https://elaw.klri.re.kr/)
- Singapore IMDA Code, [IMDA Official Regulatory Framework](https://www.imda.gov.sg/)
- China MIIT Application Filing & PIPL, [MIIT Official Publication](https://www.miit.gov.cn/)
- ROSCA / FTC Negative Option Rule, [15 U.S.C. 8401](https://www.ftc.gov/)
- FTC Health Breach Notification Rule, [16 CFR Part 318](https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule)
- California CPRA / CPPA Regulations, [California Privacy Protection Agency](https://cppa.ca.gov/)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- EU Data Act & CRA, [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj) & [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
