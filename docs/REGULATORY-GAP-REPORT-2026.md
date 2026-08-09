# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major regulations that bind app developers shipping into the EU, the US, and other global markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight angles, which are policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems and software, the GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety. URL: https://eur-lex.europa.eu/eli/reg/2023/988/oj

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

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council. URL: https://eur-lex.europa.eu/eli/reg/2023/1543/oj

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

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023. URL: https://eur-lex.europa.eu/eli/dir/2023/2673/oj

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

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026). URL: https://developer.apple.com/documentation/declaredagerange/

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

Official Citation: Regulation (EU) 2024/1689, Article 4. URL: https://eur-lex.europa.eu/eli/reg/2024/1689/oj

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

Official Citation: Regulation (EU) 2024/1689, Article 50. URL: https://eur-lex.europa.eu/eli/reg/2024/1689/oj

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
The EU Digital Markets Act (DMA), Regulation (EU) 2022/1925, seeks to prevent gatekeepers from imposing unfair conditions on businesses and consumers. For mobile application environments, the DMA mandates support for alternative app stores, alternative payment gateways, direct links for promotions (anti-steering bans), and direct side-loading capabilities in the European Union.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council. URL: https://eur-lex.europa.eu/eli/reg/2022/1925/oj

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a structured corporate anti-steering and direct promotion strategy policy to guide developers in making commercial decisions.
- **Missing Documentation:**
  While general references exist, there is no detailed developer-facing document outlining the steps required to apply for Apple's European Alternative Billing Entitlement or Core Technology Fee (CTF) exemptions.
- **Missing Code:**
  No helper classes or configuration structures exist to interact with external link sheets, out-of-app payment redirects, or specific Apple DMA entitlements.
- **Missing Disclosure:**
  Templates fail to provide mandatory user-facing disclosure forms explaining that alternative billing options transfer payment dispute processing away from Apple or Google to third-party operators.
- **Missing Logging:**
  There is no transactional logger or data model designed to track transactions routed through alternative payment gateways for mandatory monthly storefront reporting.
- **Missing Testing:**
  The repository does not contain test suites to simulate external billing redirects, verify target links are secure, or test alternative app distribution frameworks.
- **Missing Evidence:**
  No physical templates of Core Technology Fee reports or proof of compliance submissions to Apple/Google are provided.
- **Missing Audit Trail:**
  The repository fails to track changes, updates, or audits performed on direct promotion sheets, alternative payment integrations, or reporting tools.

### 7.3 Remediation and Action Plan
1. Draft an Anti-Steering and External Billing Integration Policy for EU-distributed applications.
2. Implement cross-platform billing components that dynamically render warnings when users exit native purchase environments.
3. Add secure logging models to aggregate external transaction records for compliant monthly reporting.
4. Create automated end-to-end integration tests to verify the integrity and security of alternative web payment redirections.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The Digital Services Act (DSA), Regulation (EU) 2022/2065, targets illegal content, transparent advertising, and systemic disinformation online. For app stores, the DSA enforces strict "Trader Status" identification rules. All developers publishing commercial apps in the EU must undergo detailed validation (requiring a verified D-U-N-S, telephone number, and email address), and online interfaces must host illegal content flagging mechanisms.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council. URL: https://eur-lex.europa.eu/eli/reg/2022/2065/oj

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No internal Policy on Illegal Content and User Safety exists to define response windows and legal workflows for reported files or profiles.
- **Missing Documentation:**
  Checklists fail to outline detailed developer walkthroughs to verify and configure DSA Trader details in App Store Connect or Google Play Console.
- **Missing Code:**
  Code templates do not include robust User-Generated Content (UGC) notice-and-action mechanisms or direct flagging forms.
- **Missing Disclosure:**
  Storefront interfaces do not display the developer's registered trade address, email, or verification status in a clear, standardized format.
- **Missing Logging:**
  There are no logging schema definitions to index incoming content flags, category values, investigator actions, or response durations.
- **Missing Testing:**
  No automated UI tests simulate a citizen submitting an illegal content report or confirm the action triggers correct server notifications.
- **Missing Evidence:**
  The playbook contains no examples of completed DSA compliance reports, verification receipts, or D-U-N-S profile audits.
- **Missing Audit Trail:**
  There is no unalterable record system tracking the history of content moderation actions, notice resolutions, or policy alterations.

### 8.3 Remediation and Action Plan
1. Create a written UGC notice-and-action framework aligning with Article 16 of the Digital Services Act.
2. Develop standard, reusable notice-and-action UI blocks (Report Content modals) with category tagging.
3. Establish structured database schemas to securely log, investigate, and resolve user-generated abuse reports.
4. Integrate end-to-end testing flows to verify that submitted reports immediately alert moderation systems and update status records.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (EAA), Directive (EU) 2019/882, establishes harmonized accessibility requirements for digital products and services across EU Member States. Applicable starting June 2025, mobile applications and e-commerce websites must satisfy harmonized technical accessibility standard EN 301 549 (specifically Chapter 11) to ensure equal access for users with sensory, cognitive, or physical impairments.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council. URL: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  There is no Corporate Accessibility Policy setting target accessibility tiers (e.g., WCAG 2.1 AA / EN 301 549) or designating accessibility leads.
- **Missing Documentation:**
  Guides omit specific instructions on semantic structures, proper contrast ratios, and layout adaptions required for severe visual impairments under EN 301 549.
- **Missing Code:**
  Existing UI code templates lack proper accessibility tags, semantic descriptions (such as descriptive accessibility labels), or focus order definitions.
- **Missing Disclosure:**
  The repository is missing an accessible, public-facing Accessibility Statement template detailing compliance levels and contact routes.
- **Missing Logging:**
  No mechanism records accessibility feedback, screen-reader crashes, or contrast issues reported by active end-users.
- **Missing Testing:**
  Although basic linting checks may run, there are no end-to-end integration tests to verify dynamic voice feedback, dynamic type adjustments, or focus paths.
- **Missing Evidence:**
  The repository does not contain standardized compliance verification reports, screen-reader walkthrough videos, or accessibility audits.
- **Missing Audit Trail:**
  An audit trail to log accessibility reviews, visual regression tests, and iterative design alterations is absent.

### 9.3 Remediation and Action Plan
1. Draft a comprehensive Accessibility Policy committing the organization to complete EN 301 549 Chapter 11 compliance.
2. Revise existing code blocks to incorporate accessibility labels, accessibility traits, and logical focus orders.
3. Design and include an in-app "Accessibility Statement" template accessible to assistive devices by default.
4. Run automated accessibility scans using specialized tools (such as VoiceOver/TalkBack simulations) and document outcomes in a verification registry.

---

## 10. US Children's Online Privacy Protection Act (COPPA)

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (COPPA) protects children under the age of 13 by requiring verified parental consent prior to collecting personal information. The 2025/2026 Amended COPPA Rule updates extend personal information definitions to explicitly cover biometric identifiers (such as voiceprints, gait patterns, and facial templates) and enforce stricter data minimization, distinct opt-in consent for ad tracking, and written security protocols.

Official Citation: Children's Online Privacy Protection Rule, 16 CFR Part 312 (Amended 2025/2026). URL: https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not contain a template COPPA-compliant Written Information Security Program (WISP) or minor-focused data minimization rules.
- **Missing Documentation:**
  The repository is missing guidelines on how to conduct and document a COPPA-compliant minor privacy review, or how to isolate third-party SDKs in kid-centric app categories.
- **Missing Code:**
  Code snippets do not implement parental gates, age-gated onboarding, or programmatic switches to disable data collection SDKs dynamically.
- **Missing Disclosure:**
  Onboarding forms omit prominent COPPA disclosures explaining what information is collected, how it is used, and who can access it.
- **Missing Logging:**
  There is no database logging layout to track the execution, modification, or revocation of verifiable parental consent.
- **Missing Testing:**
  Automated tests do not verify that personal data (such as identifiers) is completely stripped or that tracking requests are blocked for users under 13.
- **Missing Evidence:**
  No physical templates for verifiable parental consent agreements or written COPPA compliance reviews are provided.
- **Missing Audit Trail:**
  An unalterable audit trail recording our technical choices, third-party audits, and data purging activities is not maintained.

### 10.3 Remediation and Action Plan
1. Establish a clear Written Information Security Program focused on COPPA and state-level child safety.
2. Develop standard "Parental Gate" code components to block access to minor settings.
3. Build programmatic controls to block or strip telemetry, analytics, and advertising SDKs when a user is flagged as under-13.
4. Establish automated integration tests to verify zero tracking identifiers are compiled or transmitted from minor sessions.

---

## 11. California Consumer Privacy Act (CCPA/CPRA)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), establishes robust privacy rights for residents of California. Key requirements include the "Notice at Collection", the right to opt-out of the sale or sharing of personal data, sensitive personal information limits, and mandatory support for Global Privacy Control (GPC) opt-out signals.

Official Citation: California Consumer Privacy Act of 2018 (CCPA) / CPRA. URL: https://oag.ca.gov/privacy/ccpa

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template CPRA-compliant privacy notice, "Notice at Collection", or sensitive personal info policies are provided in the playbook.
- **Missing Documentation:**
  The repository lacks developer instructions on how to parse, detect, and programmatically honor Global Privacy Control (GPC) signals in user requests.
- **Missing Code:**
  The client and server templates in this repository fail to incorporate GPC detection middleware, and there is no mock implementation of a "Do Not Sell or Share My Personal Information" link.
- **Missing Disclosure:**
  Onboarding templates lack appropriate California "Notice at Collection" and explicit explanations regarding data sharing and sale.
- **Missing Logging:**
  There is no logging format to track user opt-out choices, GPC signal detections, or consumer rights verification logs.
- **Missing Testing:**
  No automated scripts test whether detecting a GPC header successfully stops tracking scripts and sets proper cookie states.
- **Missing Evidence:**
  The repository contains no template evidence packages or records of annual CPRA compliance audits.
- **Missing Audit Trail:**
  An audit trail documenting the history of California consumer request volumes, fulfillment timelines, and privacy notice updates is absent.

### 11.3 Remediation and Action Plan
1. Draft a CPRA-compliant privacy notice template including a structured "Notice at Collection".
2. Add server-side and client-side code components to automatically scan for and honor `Sec-GPC` request headers.
3. Implement a functional "Do Not Sell or Share My Personal Information" UI module.
4. Write integration tests to confirm that GPC detection halts personal data transmission and prevents third-party SDK initialization.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14, imposes strict requirements on organizations collecting, storing, or using biometric identifiers (such as fingerprints, facial geometry, retina scans, or voiceprints) from Illinois residents. BIPA mandates written notice, written consent releases, public retention schedules, and absolute bans on selling, leasing, or trading biometric data, backed by severe statutory damages.

Official Citation: Biometric Information Privacy Act, 740 ILCS 14. URL: https://www.recordinglaw.com/us-laws/data-privacy-laws/bipa/

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template Biometric Data Management Policy and public-facing Biometric Retention Schedule.
- **Missing Documentation:**
  Guides omit instructions on how to isolate native device biometric authentication (which is typically exempt) from direct biometric capture (which triggers BIPA).
- **Missing Code:**
  No consent modals, consent-release text forms, or biometric collection code blocks exist in the repository's templates.
- **Missing Disclosure:**
  In-app templates do not display explicit notices explaining the purpose of biometric capture, the retention period, or the destruction timelines.
- **Missing Logging:**
  There are no logging mechanisms designed to record the execution and verification of written biometric releases.
- **Missing Testing:**
  No tests verify that biometric capture functions are completely blocked or deactivated if a user declines consent or is located in Illinois without a valid release.
- **Missing Evidence:**
  The playbook provides no templates of written biometric consent agreements or destruction records.
- **Missing Audit Trail:**
  An immutable audit trail system to log updates to biometric algorithms, consent forms, and verified biometric purging events is missing.

### 12.3 Remediation and Action Plan
1. Formulate a comprehensive Biometric Information Privacy Policy and Retention Schedule aligning with BIPA requirements.
2. Develop standard BIPA-compliant consent modals and written release forms for biometric onboarding.
3. Build secure backend architectures to automatically delete raw biometric templates and vectors within three years of capture or upon account termination.
4. Establish automated tests to confirm biometric initialization is blocked for users who decline consent.

---

## 13. US Subscription Cancellation (FTC Click-to-Cancel Rule)

### 13.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) "Click-to-Cancel" rule (extending the Negative Option Rule) mandates that the process to cancel a subscription, trial, or auto-renewing service must be at least as easy and frictionless as the process to enroll. It bans hidden fees, mandatory phone calls to cancel, and excessive retention "saves" designed to trap consumers.

Official Citation: FTC Negative Option Rule / Subscription Cancellation Requirements. URL: https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing a formal Negative Option and Auto-Renewal Policy template outlining compliant billing structures.
- **Missing Documentation:**
  Guides do not outline FTC cancellation guidelines, "save" offer limitations, or visual prominence requirements for cancellation buttons.
- **Missing Code:**
  Existing billing and account management UI code blocks lack functional, frictionless, self-service cancellation paths.
- **Missing Disclosure:**
  Registration templates do not display the full subscription terms, pricing hierarchies, and recurring billing frequencies in a prominent visual area.
- **Missing Logging:**
  There are no logs to track cancellation timestamps, refund transactions, or negative option confirmations.
- **Missing Testing:**
  No automated UI tests confirm that a user can complete a subscription cancellation with the same number of steps and clicks required to register.
- **Missing Evidence:**
  The playbook provides no templates of cancellation confirmation receipts or records of compliance with auto-renewal disclosure checklists.
- **Missing Audit Trail:**
  A secure audit trail tracking visual changes to the cancellation page, checkout flows, and compliance reviews is not implemented.

### 13.3 Remediation and Action Plan
1. Create a written Subscription and Auto-Renewal Policy ensuring full click-to-cancel compliance.
2. Build frictionless "Cancel Subscription" UI components directly inside account settings.
3. Wire automatic email and SMS cancellation receipts with clear timestamps.
4. Write end-to-end UI tests to prove that the cancellation path is Completed in equal or fewer steps than the sign-up path.

---

## 14. UK Online Safety Act (OSA)

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 requires digital platforms, content hosts, and online distribution channels to actively protect children from harmful or age-inappropriate material. For apps distributed in the UK, the Act enforces strict age-verification standards, requiring "highly effective" age assurance methods (such as facial age estimation or digital ID verification) rather than self-declaration checkboxes.

Official Citation: Online Safety Act 2023 (c. 50). URL: https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No internal UK Children's Safety and Content Moderation Policy exists within the playbook's template library.
- **Missing Documentation:**
  The repository lacks developer manuals on how to integrate third-party age estimation APIs (such as Yoti) to verify minor users in the UK.
- **Missing Code:**
  Mock client implementations do not include programmatic hooks to redirect UK-based minors to highly effective age verification flows.
- **Missing Disclosure:**
  Onboarding forms omit disclosures explaining that the user's age must be verified using government-backed or biometric estimation methods.
- **Missing Logging:**
  No secure database structures are defined to track successful age checks while ensuring the immediate destruction of sensitive verification vectors.
- **Missing Testing:**
  Automated tests do not verify that underage or unverified users are blocked from access to adult-oriented content or chat features.
- **Missing Evidence:**
  The repository lacks templates of Child Safety Risk Assessments or proof of age-assurance accuracy metrics.
- **Missing Audit Trail:**
  An audit trail logging age-verification provider reviews, integration updates, and content moderation performance metrics is absent.

### 14.3 Remediation and Action Plan
1. Formulate an Online Child Protection and Content Safety Policy.
2. Integrate secure client-side and server-side hooks to process third-party biometric and database age verification.
3. Implement absolute data sanitization processes to permanently destroy age-estimation vectors immediately after processing.
4. Set up integration tests to confirm age-inappropriate app sections are entirely restricted for users under 18.

---

## 15. Australia Online Safety Amendment Act

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 establishes a strict statutory minimum age of 16 for holding social media and designated messaging accounts. To comply, operators must implement robust, verified age-assurance techniques, ringfence and permanently destroy age-checking records, and prevent minors under 16 from creating or accessing social profiles.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024. URL: https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template policy establishes how to identify Australian users, enforce the under-16 account ban, or manage parent bypass requests.
- **Missing Documentation:**
  Checklists omit developer instructions on Australian age-assurance requirements, specific eSafety Commissioner expectations, and regional penalties.
- **Missing Code:**
  No age-assurance modules or location-gated social deactivation mechanisms exist in the repository's code layouts.
- **Missing Disclosure:**
  Social UI templates fail to display clear notices that users under 16 are strictly prohibited from creating accounts under Australian law.
- **Missing Logging:**
  There is no logging model to track age checks or the immediate deletion of raw identity verification data.
- **Missing Testing:**
  No integration tests simulate a 15-year-old Australian user attempting to register and confirm that registration is completely blocked.
- **Missing Evidence:**
  The repository contains no template safety case assessments or records of compliance audits for the Australian eSafety Commissioner.
- **Missing Audit Trail:**
  An audit trail tracking the history of age-verification parameters, vendor reviews, and geolocation check modifications is missing.

### 15.3 Remediation and Action Plan
1. Create a written Australia Social Media Compliance Policy detailing the under-16 restriction.
2. Develop location-aware onboarding modules that dynamically check user location and enforce age assurance for Australian accounts.
3. Build database functions to automatically destroy identity documents, CPF logs, or document scans immediately after verification.
4. Program automated tests to confirm that under-16 registration attempts are blocked.

---

## 16. Brazil Digital ECA (Law 15,211/2025)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) targets child online safety by banning simple age self-declaration checkboxes and requiring approved age-assurance methods such as document checking, facial age estimation, or CPF database verification. It also requires that loot-box games and mature-themed apps implement strict age gating and rate 18-plus in Brazil.

Official Citation: Brazil Digital ECA (Law 15,211/2025) / ANPD Rules. URL: https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template policy for Brazilian storefronts and LGPD-aligned minor consent requirements.
- **Missing Documentation:**
  Checklists fail to cover Brazilian age-assurance requirements, CPF database check APIs, or regional classification rules.
- **Missing Code:**
  The codebase has no templates for capturing CPF numbers, processing Brazilian document verifications, or enforcing strict age locks.
- **Missing Disclosure:**
  Onboarding templates omit disclosures explaining that the user's age category is requested to comply with Law 15,211/2025.
- **Missing Logging:**
  No secure database structures are defined to log the receipt of parental consent or CPF verification flags.
- **Missing Testing:**
  Automated tests do not verify that self-declaration checkbox deactivation occurs on Brazilian IP ranges.
- **Missing Evidence:**
  The playbook contains no examples of completed Brazil compliance audits, classification filings, or LGPD data maps.
- **Missing Audit Trail:**
  An immutable audit trail tracking Brazilian age-verification rollout dates and algorithm reviews is absent.

### 16.3 Remediation and Action Plan
1. Draft a Written LGPD and Brazil Digital ECA Compliance Policy.
2. Develop standard CPF validation and document submission onboarding interfaces.
3. Build database schemas to securely log, investigate, and resolve parental consent disputes.
4. Set up integration tests to confirm self-declaration options are entirely disabled for Brazilian storefronts.

---

## 17. India Digital Personal Data Protection Act (DPDPA)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023, along with the DPDP Rules, establishes strict data protection standards, especially for children under 18. The DPDPA mandates verifiable parental consent through government-backed or approved systems (such as DigiLocker integrations) and strictly prohibits behavioral tracking, targeted advertisements, or any profiling directed at minor users.

Official Citation: India Digital Personal Data Protection Act (DPDPA) 2023. URL: https://www.bassberry.com/news/indias-data-privacy-rules-what-your-business-needs-to-know/

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository is missing a formal Indian DPDPA compliance policy, minor profiling bans, and consent standards.
- **Missing Documentation:**
  Guides do not outline Indian DPDPA guidelines, DigiLocker integration structures, or visual prominence requirements.
- **Missing Code:**
  Existing code templates lack programmatic switches to disable data collection SDKs, telemetry, or profiling for Indian minor accounts.
- **Missing Disclosure:**
  Onboarding forms omit prominent Indian DPDPA disclosures explaining what information is collected and how it is used.
- **Missing Logging:**
  There is no database logging layout to track the execution, modification, or revocation of parental consent.
- **Missing Testing:**
  No automated tests verify that personal data is completely stripped or that tracking requests are blocked for users under 18 in India.
- **Missing Evidence:**
  No physical templates for verifiable parental consent agreements or written DPDPA compliance reviews are provided.
- **Missing Audit Trail:**
  An immutable audit trail recording our technical choices, third-party audits, and data purging activities is not maintained.

### 17.3 Remediation and Action Plan
1. Create a written India DPDPA Privacy Compliance Policy ensuring under-18 profiling bans are enforced.
2. Develop location-aware onboarding modules that check user location and block behavioral tracking for Indian accounts.
3. Build programmatic controls to block or strip telemetry, analytics, and advertising SDKs when a user is flagged as under-18.
4. Set up integration tests to confirm age-inappropriate app sections are entirely restricted.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety require digital services and app stores to implement highly effective age-assurance methods to prevent minor exposure to age-inappropriate digital assets. Collected verification records, credit card hashes, and age estimation vectors must be completely destroyed immediately after validation.

Official Citation: IMDA Code of Practice for Online Safety / Singapore PDPA. URL: https://www.twobirds.com/en/insights/2026/singapore/app-stores-in-singapore-required-to-implement-age-assurance-measures

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No internal Singapore PDPA and IMDA Online Safety compliance policies exist within the playbook's templates.
- **Missing Documentation:**
  Checklists fail to cover Singapore-specific age-assurance requirements, credit card hashing checks, or regional guidelines.
- **Missing Code:**
  No age-assurance modules or location-gated deactivation mechanisms exist in the repository's code layouts.
- **Missing Disclosure:**
  Onboarding templates omit disclosures explaining that the user's age category is requested to comply with IMDA rules.
- **Missing Logging:**
  There is no logging model to track age checks or the immediate deletion of raw identity verification data.
- **Missing Testing:**
  No integration tests simulate a Singapore-based user attempting to register and confirm that registration is blocked.
- **Missing Evidence:**
  The repository contains no template safety case assessments or records of compliance audits for Singapore's IMDA.
- **Missing Audit Trail:**
  An audit trail tracking the history of age-verification parameters, vendor reviews, and geolocation check modifications is missing.

### 18.3 Remediation and Action Plan
1. Formulate a Singapore Online Safety Compliance Policy detailing the minor restrictions.
2. Develop standard credit card verification and age estimation onboarding interfaces.
3. Build database functions to automatically destroy identity documents or document scans immediately after verification.
4. Program automated tests to confirm that under-18 registration attempts are blocked.

---

## 19. South Korea Telecommunications Business Act

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative billing options for in-app purchases. Apple and Google must permit developers to integrate third-party payment systems. Developers utilizing this entitlement must deploy South Korea-only binaries, render mandatory warning modal sheets, configure transaction reports, and pay a reduced storefront commission.

Official Citation: Telecommunications Business Act / South Korea Alternative Billing Entitlements. URL: https://developer.apple.com/support/storekit-external-entitlement-kr/

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template policy for alternative billing in South Korea and regional commission reporting.
- **Missing Documentation:**
  Guides omit instructions on how to isolate native device payment options from direct South Korean alternative payment gateways.
- **Missing Code:**
  No alternative billing modals, consent forms, or reporting API hooks exist in the repository's templates.
- **Missing Disclosure:**
  In-app templates do not display explicit notices explaining that alternative billing options transfer payment dispute processing away from Apple or Google.
- **Missing Logging:**
  There are no logging mechanisms designed to record South Korea alternative billing transactions.
- **Missing Testing:**
  No tests verify that South Korea alternative payment options display the mandatory modal sheet.
- **Missing Evidence:**
  The playbook provides no templates of South Korean transaction reports or commission filings.
- **Missing Audit Trail:**
  An audit trail tracking South Korea alternative billing updates and visual modifications is absent.

### 19.3 Remediation and Action Plan
1. Draft a Written South Korea Telecommunications Business Act alternative billing policy.
2. Develop standard South Korea-compliant warning modal components.
3. Build database schemas to securely log and report alternative billing transactions for storefront commission reviews.
4. Write integration tests to confirm the South Korean modal displays correct pricing and warnings.

---

## 20. China Mobile App Filing (MIIT)

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates that all mobile applications distributed on Chinese app stores must complete a formal App Filing (ICP extension). Non-filed apps are blocked from operating. Requirements include having a local Chinese entity or partner, real-name registration, local data hosting under the PIPL, and a Banhao license for games.

Official Citation: MIIT Mobile App Filing Requirements (ICP Extension) / PIPL. URL: https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No internal Chinese Mobile App Filing and PIPL Compliance Policy exists within the playbook's templates.
- **Missing Documentation:**
  The repository lacks developer manuals on how to complete the MIIT filing or host data locally under the PIPL.
- **Missing Code:**
  Mock client implementations do not include programmatic hooks to enforce real-name registration or verify MIIT filing status.
- **Missing Disclosure:**
  Onboarding forms omit disclosures explaining that Chinese user data is hosted locally under PIPL.
- **Missing Logging:**
  No secure database structures are defined to track real-name registration checks while ensuring data minimization.
- **Missing Testing:**
  Automated tests do not verify that Chinese users are restricted from registering without real-name validation.
- **Missing Evidence:**
  The repository lacks templates of Chinese MIIT filing submissions or PIPL compliance reviews.
- **Missing Audit Trail:**
  An audit trail tracking the history of real-name registration checks and Chinese data hosting audits is missing.

### 20.3 Remediation and Action Plan
1. Formulate a China MIIT App Filing and PIPL Compliance Policy.
2. Develop standard Chinese real-name registration and local PIPL data hosting interfaces.
3. Build database structures to securely log real-name registration checks while ensuring data privacy.
4. Program automated tests to confirm that Chinese users are restricted from registering without real-name validation.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step by step way to satisfy it. Missing means the playbook does not carry it at all.

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
| **EU EAA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US COPPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **California Privacy** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Click-to-Cancel** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **UK Online Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Australia Online Safety** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **India DPDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore PDPA** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **South Korea Telecom Act** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |
| **China App Filing** | Missing | Partial | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live. Most of the major regulatory frameworks here are named with dated sources. What is missing is the layer a developer can act on, meaning detection rules the guard can fire on, code templates they can paste, and tests that prove the obligation is met.

In priority order:

1. Add GPSR, the only framework absent end to end.
2. Give the remaining Partial frameworks detection rules in `data/rejection-patterns.json` and checklist items a developer can tick.
3. Add the code templates, starting with the AI Act Article 50 disclosure line and the withdrawal path, since both carry 2026 deadlines.

This report is a snapshot. It goes stale the moment a deadline moves, so re-run it against EUR-Lex and the other primary sources rather than trusting the dates here on their own.

## 23. Sources

Every regulation named above, at its primary source:

- GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EAA, [Directive (EU) 2019/882](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)
- COPPA, [Children's Online Privacy Protection Rule (16 CFR Part 312)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
