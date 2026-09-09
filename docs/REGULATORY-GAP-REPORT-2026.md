# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, Canada, India, Singapore, South Korea, China, and other global jurisdictions, and checks honestly how far this repository carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight core compliance gap categories, which are policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no way to decide whether their listing falls inside Regulation (EU) 2023/988, and no template policy to hand a client or stakeholder regarding designated EU Responsible Persons.
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
  The playbook carries no template Law Enforcement Request Policy or formal EU Legal Representative appointment protocol.
- **Missing Documentation:**
  While the repository mentions the e-Evidence Package in general, it lacks concrete operational runbooks or manuals for handling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:**
  There are no backend scripts, automated tools, or secure endpoints in the repository to assist in securely exporting, filtering, and packaging user data in response to a valid legal order within 8 hours.
- **Missing Disclosure:**
  Public-facing privacy documentation fails to explicitly disclose to EU users that their data may be preserved or disclosed to European law enforcement in accordance with Regulation (EU) 2023/1543.
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
  The playbook carries no template policy for the 14-day distance contract withdrawal right.
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
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent, easily accessible "Withdrawal Button" component within the account settings of EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify that the withdrawal button executes a frictionless, self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

These laws place strict operational obligations on both app stores and mobile application developers. Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025/2026), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy showing how to detect a user in Utah, Texas, Louisiana, or Alabama, and how to handle a minor account once detected.
- **Missing Documentation:**
  The checklists in `docs/PRE-SUBMISSION-CHECKLIST.md` lack step-by-step developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within the same multi-platform project.
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
4. Establish automated unit tests verifying that when the age category returns a minor band, in-app billing is disabled until a verifiable parental consent flag is successfully processed.

---

## 5. EU AI Act (Regulation (EU) 2024/1689)

### 5.1 Regulatory Overview and Background
The EU Artificial Intelligence Act (Regulation (EU) 2024/1689) is a comprehensive framework regulating AI development and deployment across the EU. Key provisions include Article 4 (AI Literacy, applicable 2 February 2025), Article 5 (Prohibited AI Practices, applicable 2 February 2025), and Article 50 (Transparency Obligations, applicable 2 August 2026, with Article 111(4) retrofit by 2 December 2026).

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template AI Literacy Policy (Art 4), AI Safety and Banned Practices Policy (Art 5), and AI Transparency and Content Marking Policy (Art 50).
- **Missing Documentation:**
  Checklists mention Article 50 but lack detailed developer-facing technical guides on C2PA metadata injection, machine-readable watermarking, or deepfake disclosure guidelines.
- **Missing Code:**
  Codebase templates do not contain helper classes or middle-tier utilities to inject machine-readable watermarks (such as C2PA) into generated audio, image, video, or text assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display immediate disclosures ("You are interacting with an AI system") at the first user interaction point.
- **Missing Logging:**
  There are no logging schemas to record that an AI transparency disclosure was displayed to a user or that user consent was captured for third-party AI data transfers (Apple Guideline 5.1.2(i)).
- **Missing Testing:**
  Existing test runner scripts do not verify the presence of synthetic media markers or check that generated outputs are machine-detectable as artificially created.
- **Missing Evidence:**
  The repository lacks an active `AI_LITERACY_LOG.md` training register, model documentation, or security risk assessment templates.
- **Missing Audit Trail:**
  An unalterable audit trail recording model version changes, prompt modifications, risk assessments, and literacy training updates is missing.

### 5.3 Remediation and Action Plan
1. Draft AI Literacy, Prohibited Practices, and Transparency Policies adhering to EU AI Act standards.
2. Implement C2PA watermarking utilities inside synthetic media generation codebases.
3. Add prominent AI interaction disclosures to all chat and generative interface templates.
4. Establish an automated CI lint that checks `AI_LITERACY_LOG.md` currency and verifies synthetic content marking.

---

## 6. EU Digital Markets Act (DMA - Regulation (EU) 2022/1925)

### 6.1 Regulatory Overview and Background
The EU Digital Markets Act regulates gatekeeper platforms (including Apple App Store and Google Play) to ensure contestability and fairness. Developers distributing in the EU can utilize alternative app marketplaces, web distribution, and alternative payment links under modified business terms (such as the 5% Core Technology Commission taking effect 1 October 2026).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council of 14 September 2022 on contestable and fair markets in the digital sector.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a clear EU Alternative Distribution & Payment Policy guiding developers on choosing between standard App Store terms and DMA unified terms (Attachment 14).
- **Missing Documentation:**
  Missing developer runbooks for configuring the `com.apple.developer.storekit.external-purchase-link` entitlement, executing `ExternalPurchaseCustomLink`, and submitting monthly reporting.
- **Missing Code:**
  Templates do not contain code for the `ExternalPurchaseCustomLink` system disclosure sheet or backend reporting API integration scripts.
- **Missing Disclosure:**
  UI templates do not display required disclosures informing users that alternative purchases lose platform features like Apple Report-a-Problem or Family Sharing.
- **Missing Logging:**
  Missing logging infrastructure to capture external offer clicks, transaction records, and monthly CTC commission calculation data.
- **Missing Testing:**
  No automated unit/UI tests exist to verify that IAP and external links are never co-mingled on the same EU storefront.
- **Missing Evidence:**
  The repository lacks templates for Attachment 14 acceptance tracking or monthly CTC reporting receipts.
- **Missing Audit Trail:**
  Missing historical audit logs tracking DMA entitlement declarations, reporting API transmissions, and fee calculation adjustments.

### 6.3 Remediation and Action Plan
1. Publish a DMA Integration Guide explaining entitlement setup, disclosure requirements, and CTC fee reporting.
2. Build sample code blocks implementing the StoreKit External Purchase Link entitlement and disclosure sheet.
3. Create automated pre-submission checks ensuring no co-mingling of IAP and external offer links on EU storefronts.

---

## 7. EU Digital Services Act (DSA - Regulation (EU) 2022/2065)

### 7.1 Regulatory Overview and Background
The Digital Services Act imposes transparency and accountability obligations on online intermediaries and platforms. Articles 30 and 31 require app stores to collect, verify, and publish trader contact details (D-U-N-S, phone, email, 2FA) on app product pages, while imposing illegal content notice-and-action rules.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council of 19 October 2022 on a Single Market For Digital Services.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing template DSA Trader Compliance Policy and Illegal Content Notice-and-Action Protocol.
- **Missing Documentation:**
  Missing developer instructions for submitting and 2FA-verifying trader identity in App Store Connect and Play Console.
- **Missing Code:**
  Codebases lack in-app mechanisms for users to flag illegal content or manage recommender system main parameters.
- **Missing Disclosure:**
  Missing public trader disclosure templates and recommender system parameter transparency notices.
- **Missing Logging:**
  No logging schemas exist for tracking incoming illegal content notices, moderator responses, or trader status verification states.
- **Missing Testing:**
  No automated checks verify that trader status declarations are completed prior to EU storefront distribution.
- **Missing Evidence:**
  Lacks examples of D-U-N-S verification documentation, 2FA confirmation records, or annual DSA transparency reports.
- **Missing Audit Trail:**
  Missing unalterable audit log tracking content moderation actions, notice handling timelines, and trader status updates.

### 7.3 Remediation and Action Plan
1. Add DSA trader status verification checks to `scripts/metadata-audit.py` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Provide UI templates for in-app illegal content reporting and recommender system transparency disclosures.

---

## 8. European Accessibility Act (EAA - Directive (EU) 2019/882)

### 8.1 Regulatory Overview and Background
The European Accessibility Act requires key digital products and services (including e-commerce, banking, travel, and audiovisual media apps) distributed in the EU to be fully accessible. The technical benchmark is harmonised standard EN 301 549 (built on WCAG 2.1 Level AA, with Chapter 11 governing mobile non-web software).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council of 17 April 2019 on the accessibility requirements for products and services.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Corporate Mobile Accessibility Policy aligning with EN 301 549 Chapter 11 and WCAG 2.1 AA.
- **Missing Documentation:**
  Lacks mobile-specific accessibility developer guides covering VoiceOver/TalkBack traits, Dynamic Type scaling, and touch target sizing.
- **Missing Code:**
  Codebase templates lack complete accessibility labels, traits, hints, and dynamic scaling on custom UI components.
- **Missing Disclosure:**
  Missing template Accessibility Statement (EN 301 549 Annex B/C) explaining accessibility features and feedback channels.
- **Missing Logging:**
  No logging infrastructure exists to capture user accessibility feedback or issue reports.
- **Missing Testing:**
  The existing static accessibility scanner (`scripts/accessibility-audit.py`) is not wired as a mandatory release blocker in the pre-submission guard hook.
- **Missing Evidence:**
  Lacks templates for formal EN 301 549 Conformance Assessment Reports and Voluntary Product Accessibility Templates (VPAT).
- **Missing Audit Trail:**
  Missing historical audit log tracking accessibility testing results, audit findings, and remediation timelines.

### 8.3 Remediation Plan
1. Wire `scripts/accessibility-audit.py` into the pre-submission workflow for EU storefront builds.
2. Publish an EN 301 549 Chapter 11 developer guide and accessible component templates in `references/`.
3. Provide a standard Accessibility Statement template in `templates/`.

---

## 9. US Children's Online Privacy Protection Act (COPPA & Amended Rule)

### 9.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) regulates the collection of personal information from children under 13 by operators of child-directed or mixed-audience apps. The FTC's Amended COPPA Rule (effective 23 June 2025, compliance mandatory 22 April 2026) expands personal information to include biometric identifiers, requires separate opt-in consent for third-party disclosures, mandates a written retention policy, and requires a written information security program.

Official Citation: FTC Children's Online Privacy Protection Rule, 16 CFR Part 312 (90 FR 16918).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Lacks a Written Children's Privacy Data Retention Policy (312.10) and Written Information Security Program (312.8).
- **Missing Documentation:**
  Checklists lack step-by-step guides for biometric data handling and separate opt-in consent flows under the 2025/2026 Amended Rule.
- **Missing Code:**
  Code templates lack separate opt-in consent modals for third-party ad sharing and automated biometric PII deletion routines.
- **Missing Disclosure:**
  Direct parental notices do not clearly distinguish core service collection from optional third-party disclosure.
- **Missing Logging:**
  Lacks logging schemas for parental consent receipts, consent revocations, and scheduled data retention purges.
- **Missing Testing:**
  No automated integration tests verify that under-13 accounts are blocked from third-party ad SDK initialization.
- **Missing Evidence:**
  Lacks templates for annual Information Security Program risk assessments and FTC Safe Harbor compliance certificates.
- **Missing Audit Trail:**
  Missing unalterable audit log tracking data retention schedule enforcement, parental consent verifications, and data purges.

### 9.3 Remediation Plan
1. Add Written Data Retention and Information Security Program templates for COPPA in `templates/`.
2. Implement code modules for separate third-party consent and automated biometric data purging.

---

## 10. California Privacy Rights Act (CPRA / CCPA & CPPA Regulations)

### 10.1 Regulatory Overview and Background
The CPRA (amending CCPA) grants California consumers robust privacy rights (know, delete, correct, opt-out of sale/sharing, limit sensitive PI). CPPA 2026 Regulations mandate honoring Global Privacy Control (GPC) signals and establish Automated Decision-Making Technology (ADMT) notice, opt-out, and access requirements.

Official Citation: California Consumer Privacy Act of 2018 as amended by CPRA (Cal. Civ. Code section 1798.100 et seq.) and CPPA Regulations (11 CCR section 7000 et seq.).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing California Privacy & Automated Decision-Making Technology (ADMT) Policy.
- **Missing Documentation:**
  Lacks developer guides for honoring GPC signals in embedded webviews and implementing native opt-outs.
- **Missing Code:**
  Codebases lack automatic `Sec-GPC` header detection in webviews and native "Do Not Sell or Share My Personal Info" handlers.
- **Missing Disclosure:**
  Missing Notice at Collection, "Limit the Use of My Sensitive Personal Information", and ADMT transparency notices.
- **Missing Logging:**
  No logs capture opt-out requests, GPC signal detections, or consumer rights fulfillment states.
- **Missing Testing:**
  No automated unit tests verify that detecting a GPC signal immediately halts third-party tracking flows.
- **Missing Evidence:**
  Lacks templates for CPPA ADMT Risk Assessments and annual cybersecurity audit certifications.
- **Missing Audit Trail:**
  Missing audit trail tracking consumer rights request processing (45-day SLA), opt-out state changes, and ADMT evaluation updates.

### 10.3 Remediation Plan
1. Add GPC signal handling utilities and native opt-out code snippets.
2. Provide Notice at Collection and ADMT disclosure templates in `templates/`.

---

## 11. Illinois Biometric Information Privacy Act (BIPA)

### 11.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) regulates the collection, use, and retention of biometric identifiers (fingerprints, voiceprints, facial geometry scans). It mandates written notice, written release/consent prior to collection, a public retention schedule, and destruction within 3 years, backed by private right of action statutory damages.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Written Biometric Data Policy outlining collection scope, retention schedules, and destruction guidelines.
- **Missing Documentation:**
  Lacks developer guidelines for BIPA compliance in face-match, voiceprint, or Touch ID / Face ID custom flows.
- **Missing Code:**
  Lacks standalone written release/consent modal UI components specifically for biometric data capture.
- **Missing Disclosure:**
  Lacks explicit written disclosures detailing specific biometric identifiers collected, purpose, and storage duration.
- **Missing Logging:**
  No logging mechanisms exist for recording consent timestamps or automated 3-year data destruction triggers.
- **Missing Testing:**
  No integration tests exist to verify that biometric capture APIs cannot execute without an active, signed release flag.
- **Missing Evidence:**
  Lacks executed written release templates and certificates of biometric data destruction.
- **Missing Audit Trail:**
  Missing immutable audit trail recording biometric consent capture, retention monitoring, and data purge execution.

### 11.3 Remediation Plan
1. Add a BIPA Written Biometric Policy and Release Consent template.
2. Build code guards that block biometric API calls until a valid consent flag is set.

---

## 12. US FTC Subscription Cancellation Rules ("Click-to-Cancel" / ROSCA)

### 12.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA) and state negative-option laws (California, New York, Massachusetts) mandate that online subscription cancellation must be clear, simple, and at least as easy as sign-up (click-to-cancel), prohibiting phone-only or mail-only cancellation traps.

Official Citation: Restore Online Shoppers' Confidence Act, 15 U.S.C. 8401 et seq., and Cal. Bus. & Prof. Code section 17600 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Simple Subscription Cancellation Policy for cross-platform or web-billed subscriptions.
- **Missing Documentation:**
  Lacks UI design guidelines requiring cancellation paths to match sign-up simplicity.
- **Missing Code:**
  Lacks functional self-service 1-click in-app or web cancellation flow templates for non-IAP subscriptions.
- **Missing Disclosure:**
  Missing pre-consent disclosures detailing auto-renewal terms, recurring charges, and cancellation mechanics.
- **Missing Logging:**
  No logging exists to capture cancellation requests, timestamps, and renewal reminder dispatches.
- **Missing Testing:**
  No automated E2E tests verify that cancellation executes frictionlessly without manual human intervention.
- **Missing Evidence:**
  Lacks standardized cancellation confirmation receipts and explicit consent records for recurring billing.
- **Missing Audit Trail:**
  Missing historical audit trail tracking cancellation flow revisions, churn rates, and refund processing logs.

### 12.3 Remediation Plan
1. Add self-service subscription cancellation UI components and backend handlers in `templates/`.
2. Integrate pre-submission checks flagging non-IAP subscriptions lacking direct cancellation paths.

---

## 13. UK Online Safety Act 2023 & ICO Children's Code

### 13.1 Regulatory Overview and Background
The UK Online Safety Act 2023 requires user-to-user and search services to implement Highly Effective Age Assurance (facial age estimation, open banking, digital ID) to protect children from harmful content, alongside mandatory CSEA reporting. The ICO Children's Code mandates high privacy by default, data minimisation, and disabled profiling/geolocation for under-18s.

Official Citation: UK Online Safety Act 2023 (c. 50) and ICO Age Appropriate Design Code.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing UK Online Safety & Children's Code Compliance Policy.
- **Missing Documentation:**
  Lacks guides for integrating Highly Effective Age Assurance and executing CSEA reporting to the NCA portal.
- **Missing Code:**
  Lacks automated age assurance gating and CSEA reporting mechanism code integrations.
- **Missing Disclosure:**
  Missing child-friendly privacy notices and risk disclosures for user-to-user interaction.
- **Missing Logging:**
  No logging exists for CSEA report submissions, age assurance outcomes, or 30-day complaints handling.
- **Missing Testing:**
  No integration tests verify that under-18 UK accounts have geolocation, profiling, and late-night push notifications disabled by default.
- **Missing Evidence:**
  Lacks templates for UK Data Protection Impact Assessments (DPIA) and Ofcom risk assessment filings.
- **Missing Audit Trail:**
  Missing audit trail tracking safety risk assessment updates, age assurance system audits, and CSEA report handling.

### 13.3 Remediation Plan
1. Publish UK Children's Code DPIA template in `templates/`.
2. Add code routines enforcing high-privacy defaults (geolocation and profiling off) for UK minor accounts.

---

## 14. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 14.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts, using waterfall age assurance and mandatory age-data ringfencing and destruction.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 and App Distribution Services Online Safety Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Australian Social Media Minimum Age & Industry Code Policy.
- **Missing Documentation:**
  Lacks developer runbooks for waterfall age assurance and age-data ringfencing/destruction.
- **Missing Code:**
  Lacks age assurance integration for under-16 account blocking and immediate age-data purge routines after verification.
- **Missing Disclosure:**
  Lacks user notices explaining under-16 access restrictions and age data handling.
- **Missing Logging:**
  No logging exists for age assurance attempts or automated age-data destruction confirmation.
- **Missing Testing:**
  No automated tests verify under-16 account creation blocking on social media features.
- **Missing Evidence:**
  Lacks eSafety Commissioner risk assessment filings and age data ringfencing audit evidence.
- **Missing Audit Trail:**
  Missing unalterable audit trail recording age verification execution, immediate data destruction, and policy updates.

### 14.3 Remediation Plan
1. Add Australia age assurance and immediate data destruction code templates.
2. Incorporate eSafety Industry Code checklist items into `docs/PRE-SUBMISSION-CHECKLIST.md`.

---

## 15. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 15.1 Regulatory Overview and Background
Brazil's Digital ECA prohibits simple self-declaration checkboxes for age verification, requiring approved methods (document check, CPF database check, facial estimation) and mandatory guardian authorization for minor accounts, enforced by the ANPD.

Official Citation: Law 15,211/2025 and Decreto n. 12.880 of 18 March 2026.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Brazil Digital ECA Minor Protection Policy.
- **Missing Documentation:**
  Lacks guides for integrating ANPD-approved age verification methods and Google Play Age Signals API for Brazil.
- **Missing Code:**
  Lacks client integration with Google Play Age Signals API and Apple 18-plus download block mechanics for Brazil storefronts.
- **Missing Disclosure:**
  Missing pre-download age rating displays and guardian authorization notices.
- **Missing Logging:**
  No logs capture guardian authorization receipts or temporary age verification result caching.
- **Missing Testing:**
  No automated tests verify that self-declaration checkboxes are disabled for Brazil storefront builds.
- **Missing Evidence:**
  Lacks ANPD compliance documentation and approved age verification partner agreements.
- **Missing Audit Trail:**
  Missing audit trail tracking age rating updates, guardian consent records, and ANPD inspection readiness.

### 15.3 Remediation Plan
1. Add Brazil Digital ECA compliance checklists and Play Age Signals integration guides.
2. Provide code blocks for guardian authorization workflows.

---

## 16. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 16.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 require verifiable parental consent through government-backed systems (such as DigiLocker) for users under 18, prohibit behavioral tracking and targeted ads to children, and establish registered Consent Managers.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPDP Rules 2025 (G.S.R. 846(E)).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing India DPDPA Data Protection & Child Data Policy (under-18 threshold).
- **Missing Documentation:**
  Lacks implementation guides for DigiLocker Verifiable Parental Consent (VPC) and Consent Manager interoperability.
- **Missing Code:**
  Lacks code modules for DigiLocker VPC integration and mechanisms blocking behavioral tracking for under-18s.
- **Missing Disclosure:**
  Missing multilingual consent notices in all 22 scheduled Indian languages detailing data processing purpose and DPO contact.
- **Missing Logging:**
  No logging exists for Consent Manager interactions, parental consent records, or data erasure executions.
- **Missing Testing:**
  No automated tests verify that under-18 accounts receive zero behavioral tracking or targeted advertising.
- **Missing Evidence:**
  Lacks Data Protection Board registration records and Consent Manager integration certificates.
- **Missing Audit Trail:**
  Missing immutable audit trail of consent receipts, consent withdrawals, and data principal rights fulfillment.

### 16.3 Remediation Plan
1. Add DPDPA 22-language consent notice templates and DigiLocker VPC integration guides.
2. Implement automated checks ensuring zero tracking for under-18 users in India.

---

## 17. Singapore Personal Data Protection Act (PDPA) & IMDA Online Safety Code

### 17.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require app-store age assurance to prevent under-18s from downloading age-inappropriate apps, ringfencing and destroying age data after verification, backed by 3-day breach notification duties.

Official Citation: Personal Data Protection Act 2012 and IMDA Code of Practice for Online Safety for App Distribution Services.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Singapore PDPA & IMDA App Distribution Online Safety Policy.
- **Missing Documentation:**
  Lacks developer runbooks for IMDA age assurance integration and 3-day breach notification protocols.
- **Missing Code:**
  Lacks runtime age screening blocking under-18s from downloading age-inappropriate apps and immediate age-data destruction routines.
- **Missing Disclosure:**
  Missing clear privacy notices identifying the appointed Data Protection Officer (DPO) and age assurance rules.
- **Missing Logging:**
  No logs capture DPO contact requests, 3-day breach notifications, or age-data purges.
- **Missing Testing:**
  No automated tests verify under-18 download restriction enforcement for Singapore storefronts.
- **Missing Evidence:**
  Lacks DPO appointment records, IMDA compliance filings, and age data destruction certificates.
- **Missing Audit Trail:**
  Missing audit trail tracking DPO reviews, data breach response logs, and age assurance system audits.

### 17.3 Remediation Plan
1. Publish Singapore DPO appointment notice template and age assurance guidelines.
2. Add automated checks for immediate age-data destruction.

---

## 18. South Korea Telecommunications Business Act & PIPA Amendment

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates allowing alternative in-app payment providers (26% commission model, approved Korean gateways KCP, Inicis, Toss, NICE, modal sheet display). The amended PIPA (Act No. 21445) makes CEOs personally accountable and mandates board-approved Chief Privacy Officers (CPOs).

Official Citation: Telecommunications Business Act Article 22-9 and Personal Information Protection Act (Act No. 21445).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing South Korea Alternative Payment Policy and CEO-Accountable Privacy Policy under amended PIPA.
- **Missing Documentation:**
  Lacks developer guide for Korea-only binary creation, approved payment gateway integration, and modal sheet display.
- **Missing Code:**
  Lacks `com.apple.developer.storekit.external-purchase` (`SKExternalPurchase = "KR"`) implementation and native alternative payment sheet.
- **Missing Disclosure:**
  Missing explicit in-app modal sheet informing users they are transacting via an alternative payment provider.
- **Missing Logging:**
  No transaction logs exist formatted for monthly South Korea alternative billing reporting (due within 15 days).
- **Missing Testing:**
  No automated tests ensure Korea-only binaries do not co-mingle StoreKit IAP with alternative billing.
- **Missing Evidence:**
  Lacks approved payment gateway contracts, board-approved CPO designation, and monthly reporting receipts.
- **Missing Audit Trail:**
  Missing audit trail tracking alternative billing sales, remittance records, CPO board reports, and PIPA compliance reviews.

### 18.3 Remediation Plan
1. Add Korea alternative payment entitlement code snippets and disclosure modal sheet templates.
2. Include South Korea CPO designation requirements in `docs/PRE-SUBMISSION-CHECKLIST.md`.

---

## 19. China Mobile App Filing (MIIT / ICP) & CAC AI Regulations

### 19.1 Regulatory Overview and Background
China mandates MIIT Mobile App Filing (ICP extension) through a local Chinese entity partner, real-name identity verification, PIPL privacy compliance, and Banhao game licensing. CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services) requires automatic Minors Mode switching and bans virtual companion services for minors.

Official Citation: MIIT Notice on Mobile Application Administrative Filing and CAC Order No. 21.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing China Compliance & Content Moderation Policy (MIIT Filing, PIPL, Real-Name Verification, Minors Mode).
- **Missing Documentation:**
  Lacks developer guide for local partner/entity filing, ICP extension, Banhao game licensing, and CAC AI registration.
- **Missing Code:**
  Lacks real-name identity verification SDK integration, Minors Mode automatic switch, and CAC-compliant content moderation filters.
- **Missing Disclosure:**
  Missing MIIT filing number display on splash/settings screen, PIPL privacy notice, and CAC AI companion disclosures.
- **Missing Logging:**
  No logs exist for real-name verification, real-time content moderation decisions, or minor usage duration limits.
- **Missing Testing:**
  No automated tests verify that Minors Mode blocks virtual companion features and algorithmic recommendations to minors.
- **Missing Evidence:**
  Lacks MIIT ICP App Filing certificates, local entity partnership contracts, Banhao licenses, and CAC AI algorithm registration proof.
- **Missing Audit Trail:**
  Missing immutable audit trail of real-name verifications, content moderation removals, and CAC compliance audit reports.

### 19.3 Remediation Plan
1. Add China MIIT filing checklist and real-name verification guidance to `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Provide Minors Mode UI switching and CAC AI disclosure code templates.

---

## 20. Cyber Resilience Act (CRA) & Product Liability Directive (PLD)

### 20.1 Regulatory Overview and Background
The EU Cyber Resilience Act (Regulation (EU) 2024/2847) mandates security-by-design, Software Bill of Materials (SBOM) management, and 24-hour actively exploited vulnerability reporting to ENISA/CSIRTs. The revised Product Liability Directive (EU) 2024/2853 applies strict liability to standalone software and app updates placed on the market from 9 December 2026.

Official Citation: Regulation (EU) 2024/2847 (Cyber Resilience Act) and Directive (EU) 2024/2853 (Product Liability Directive).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  Missing Security-by-Design & Software Vulnerability Handling Policy under CRA and PLD.
- **Missing Documentation:**
  Lacks developer runbooks for 24-hour actively exploited vulnerability reporting to ENISA/CSIRTs and SBOM management.
- **Missing Code:**
  Lacks automated SBOM generation tooling integration, secure auto-update delivery framework, and in-app vulnerability reporting endpoints.
- **Missing Disclosure:**
  Missing public security support period disclosures, known vulnerability notices, and End-of-Life (EOL) announcements.
- **Missing Logging:**
  No logging exists for security vulnerability disclosures, patch releases, or CSIRT/ENISA incident notifications.
- **Missing Testing:**
  Continuous automated security scanning (SAST/DAST/dependency vulnerability scanning) is not integrated as a mandatory release blocker.
- **Missing Evidence:**
  Lacks formal Security Risk Assessment documents, ENISA vulnerability notification records, and CE marking conformity declarations.
- **Missing Audit Trail:**
  Missing unalterable audit trail tracking security vulnerability reports, patch deployment histories, and SBOM updates.

### 20.3 Remediation Plan
1. Integrate automated SBOM generation (`cyclonedx` / `spdx`) and dependency vulnerability checks into CI pipelines.
2. Publish an ENISA/CSIRT 24-hour vulnerability incident notification runbook in `templates/`.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says Covered. Partial means the rule is named with a dated source but a developer still has no step-by-step way to satisfy it. Missing means the playbook does not carry it at all.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Partial | Missing | Missing |
| **9. US COPPA (Amended Rule)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. California Privacy (CPRA/GPC)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US FTC Click-to-Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China Mobile App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. EU CRA & PLD** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook is exceptionally strong on what gets an app rejected by a store reviewer, and thinner on the laws that bind the app once it is live across global jurisdictions. Nineteen of the twenty frameworks evaluated here are named with dated sources across `docs/EU-REGULATORY-2026.md`, `docs/GLOBAL-REGULATORY-2026.md`, `data/regulatory-deadlines.json`, and `data/rejection-patterns.json`.

What they lack is the operational execution layer that a software engineer or compliance team can act on immediately, specifically:
1. Automated guard detection rules (`data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh`) that trigger during pre-submission scans.
2. Native code templates and UI components (in `references/` and `templates/`) that can be integrated directly into applications.
3. Automated test suites and verification scripts that prove compliance prior to release.

In priority order:
1. Complete GPSR coverage, as it is the only framework absent end-to-end.
2. Add detection rules and pre-submission checklist items for the 19 Partial frameworks.
3. Supply runnable code templates and automated tests for high-priority 2026 deadlines (EU AI Act Article 50 transparency, EU Contract Withdrawal Button, US State ASAAs, and EU e-Evidence Package).

This report is a living snapshot. Re-evaluate quarterly against EUR-Lex, the Federal Register, and official primary regulatory portals to maintain complete accuracy.

---

## 23. Sources

Every regulation named above, cited to its primary official source:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- EU Cyber Resilience Act: [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- EU Product Liability Directive: [Directive (EU) 2024/2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj)
- US COPPA Rule: [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California CPRA / CCPA: [Cal. Civ. Code section 1798.100 et seq.](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US ROSCA: [15 U.S.C. 8401 et seq.](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- UK Online Safety Act: [UK Online Safety Act 2023 (c. 50)](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Act: [Online Safety Act 2021 / 2024 Amendments](https://www.legislation.gov.au/C2021A00076/latest/text)
- Brazil Digital ECA: [Law 15,211/2025 and Decreto 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA: [Digital Personal Data Protection Act, 2023](https://egazette.gov.in)
- Singapore PDPA: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea TBA & PIPA: [Telecommunications Business Act Article 22-9](https://law.go.kr) and [PIPA Act No. 21445](https://law.go.kr)
- China Mobile App Filing: [MIIT App Filing Notice](https://www.miit.gov.cn/) and [CAC Order No. 21](https://www.cac.gov.cn)
