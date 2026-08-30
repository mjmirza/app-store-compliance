# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook repository itself. It evaluates twenty major modern global and regional regulations that bind mobile and web application developers, platform operators, and software providers shipping products into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global markets.

Read this document as an operational work list for the playbook repository, not as legal advice for your organization. Where this report identifies a gap or missing requirement, it signifies an omission within this repository's policies, documentation, code, disclosures, logging, testing, evidence, or audit trails. Each framework is systematically audited across these eight distinct compliance categories to identify missing elements and actionable remediation tasks.

## Source trust hierarchy and methodology

All analysis, statutory dates, and cited legal frameworks within this report adhere strictly to the repository's source trust hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are relied upon unless traceably corroborated by Priority 1 official publications. In accordance with strict repository guidelines, this document is 100% emoji-free and contains no emoticons, unicode symbols, or graphical decorations.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in online marketplaces, digital products, and complex e-commerce supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital products and e-commerce applications, the GPSR mandates that online interfaces clearly display product safety warnings, instructions, manufacturer identity, and electronic contact details directly on the user interface before purchase or download.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no standalone General Product Safety Policy template for developers or clients to define product safety governance, designated Responsible Persons in the EU, or safety recall procedures.
- **Missing Documentation:**
  The repository lacks developer manuals, integration guides, or listing checklists detailing how to structure app metadata and UI pages to display manufacturer details, electronic contact points, and GPSR-mandated safety warnings.
- **Missing Code:**
  Mock UI components, sample codebases, and frontend templates in the repository do not include code blocks or UI widgets for rendering manufacturer identity, Responsible Person data, or safety warning banners.
- **Missing Disclosure:**
  Storefront and in-app purchase interface templates do not incorporate placeholder fields or UI disclosures for the manufacturer's name, registered trade name, postal address, and electronic contact address as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no backend database schemas, logging interfaces, or event handlers designed to log safety incidents, consumer safety complaints, or product recall notifications.
- **Missing Testing:**
  No automated UI or integration tests exist to verify that mandatory GPSR safety disclosures and manufacturer contact details are displayed dynamically based on user geographic region.
- **Missing Evidence:**
  The repository contains no sample technical documentation files, safety risk assessment templates, or verified proofs of EU Responsible Person registration.
- **Missing Audit Trail:**
  An immutable audit trail system to log revisions to product safety notices, safety risk reviews, and incident handling histories is absent from the repository.

### 1.3 Remediation and Action Plan
1. Draft and publish a comprehensive General Product Safety Policy template aligned with Regulation (EU) 2023/988.
2. Incorporate GPSR metadata fields into `docs/PRE-SUBMISSION-CHECKLIST.md` and add rule definitions to `data/rejection-patterns.json`.
3. Provide compliant UI component templates displaying manufacturer contact details and safety warnings in the references directory.
4. Implement automated validation scripts to check for required GPSR disclosures prior to app release.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package comprises Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of designated establishments and legal representatives. Enacted in 2023, full enforcement applies from 18 August 2026.

This framework empowers judicial authorities in EU Member States to issue European Production Orders (EPOs) and European Preservation Orders (EPOC-PR) directly to service providers operating in the EU. Providers must produce requested data within 10 days for standard orders, or within a strict 8-hour window for emergency situations involving imminent threat to life or safety.

Official Citations: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook does not provide a Law Enforcement Request Protocol or e-Evidence Response Policy defining internal authorization chains, verification steps, and legal representative duties.
- **Missing Documentation:**
  While general references exist in regulatory overviews, the repository lacks operational runbooks detailing step-by-step procedures for handling 10-day standard orders and 8-hour emergency production orders.
- **Missing Code:**
  The repository contains no secure scripts, API handlers, or data-extraction automation tools to retrieve, filter, and cryptographically package user data for law enforcement compliance.
- **Missing Disclosure:**
  Public-facing documentation and privacy policy templates do not explicitly disclose to EU users that data may be subject to European Production and Preservation Orders under Regulation (EU) 2023/1543.
- **Missing Logging:**
  There are no logging schemas or secure database structures designed to capture incoming legal orders, verification timestamps, officer identities, and data release records.
- **Missing Testing:**
  No automated test suites or simulated response drills exist to validate that emergency data extractions can complete within the mandated 8-hour window.
- **Missing Evidence:**
  The repository lacks sample European Production Order Certificates (EPOC) or verification checklist templates for compliance teams.
- **Missing Audit Trail:**
  An unalterable, cryptographically signed audit log tracking legal requests, access authorizations, data extractions, and secure transmissions is not implemented in the repository.

### 2.3 Remediation and Action Plan
1. Create an e-Evidence Legal Response Protocol template detailing organizational roles, designated legal representatives, and emergency workflows.
2. Develop secure data extraction scripts capable of packaging encrypted user records within emergency response deadlines.
3. Add mandatory privacy disclosures explaining legal production obligations under EU law to privacy policy templates.
4. Establish a tamper-proof audit logging mechanism for tracking all law enforcement interactions and data releases.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 on distance marketing of consumer financial services amends Directive 2011/83/EU (Consumer Rights Directive). It mandates that consumers entering into distance contracts online must be provided with a prominent, easily accessible "withdrawal button" or "withdrawal function" directly on the digital interface.

The statutory withdrawal period is 14 calendar days from contract conclusion. The cancellation workflow must be direct, frictionless, and at least as simple as the initial sign-up or subscription path. EU Member States must enforce these requirements by 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Contract Withdrawal Policy or statutory refund governance guidelines for 14-day distance contract cancellations.
- **Missing Documentation:**
  The repository lacks UI/UX design specifications, placement guidelines, and terminology requirements for building compliant withdrawal buttons in mobile and web applications.
- **Missing Code:**
  Frontend UI components and billing mock implementations in the repository omit functional implementations of a withdrawal button, confirmation modal, or automated refund trigger.
- **Missing Disclosure:**
  Subscription onboarding flows and checkout screens in the repository fail to present explicit disclosures regarding the statutory 14-day right of withdrawal and its operational terms.
- **Missing Logging:**
  There are no structured logging mechanisms to record withdrawal button clicks, withdrawal request timestamps, confirmation receipts, or refund execution states.
- **Missing Testing:**
  No automated UI or end-to-end integration tests exist to confirm that users can execute a contract withdrawal without administrative friction or customer support intervention.
- **Missing Evidence:**
  The repository lacks templates for automated withdrawal confirmation receipts, cancellation logs, or standardized refund evidence sheets.
- **Missing Audit Trail:**
  An immutable audit trail tracking historical cancellation volumes, refund processing times, and UI contract modifications is missing from the repository.

### 3.3 Remediation and Action Plan
1. Formulate a standardized 14-Day Contract Withdrawal Policy template for e-commerce and subscription applications.
2. Build reusable UI components for prominent withdrawal buttons and confirmation modals across mobile and web frameworks.
3. Integrate logging schemas to record withdrawal transactions and automated refund dispatch events.
4. Implement end-to-end UI automation tests verifying frictionless self-service cancellation paths.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minor accounts, age assurance, in-app purchases, and content updates.

These statutes mandate that mobile application developers query store-provided age signals (Apple Declared Age Range API, Google Play Age Signals API) and obtain verifiable parental consent before allowing minors to download apps, complete digital purchases, or access major updates. Raw age verification data must be purged immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a US State Minor Protection and Age Assurance Policy defining state-by-state compliance strategies and consent management.
- **Missing Documentation:**
  The repository provides no step-by-step developer documentation explaining how to integrate Apple Declared Age Range API and Google Play Age Signals API within a single multi-platform application.
- **Missing Code:**
  While rejection patterns reference state laws, sample client implementations omit native SDK bindings for querying store age signals, processing parental consent, or revoking access upon consent rescission.
- **Missing Disclosure:**
  Onboarding templates do not contain explicit state disclosures informing users why age categories are requested and explaining parental consent requirements.
- **Missing Logging:**
  There are no backend database structures to log verifiable parental consent grants, consent rescissions (`RESCIND_CONSENT`), or the immediate deletion of raw verification records.
- **Missing Testing:**
  The test suites omit automated integration tests validating that unverified minor accounts are blocked from gated updates or digital billing features.
- **Missing Evidence:**
  The repository contains no sample parental consent agreement forms, verification logs, or data minimization certification sheets.
- **Missing Audit Trail:**
  An immutable audit log tracking age-assurance feature deployments, consent policy changes, and data purge executions is not implemented in the repository.

### 4.3 Remediation and Action Plan
1. Publish a US State ASAA Compliance Policy and developer guide covering Apple and Google Play age-signal APIs.
2. Add cross-platform code snippets for querying `DeclaredAgeRange` and `com.google.android.play:age-signals`.
3. Create automated backend handlers to process consent rescission webhooks and immediately purge raw age data.
4. Add integration tests verifying feature gating when age signal returned corresponds to a minor category without consent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among their staff and operators dealing with AI operations.

This obligation became enforceable on 2 February 2025 and applies to all organizations regardless of headcount. Compliance requires maintaining an internal AI literacy policy, staff induction records, a refresh schedule, and an active training log.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no template AI Literacy Policy defining core competencies, risk evaluation skills, and training frequencies for development teams.
- **Missing Documentation:**
  The repository lacks operational guides explaining how engineering and compliance teams should document AI training and fulfill Article 4 duties.
- **Missing Code:**
  While code execution is not directly mandated by Article 4, the repository lacks automated repository lints or pre-commit checks to verify the currency of team training records.
- **Missing Disclosure:**
  Public documentation and partner disclosures in the repository fail to declare organizational adherence to EU AI literacy mandates.
- **Missing Logging:**
  The repository does not maintain an active, structured `AI_LITERACY_LOG.md` or training registry tracking employee names, training dates, and competency assessments.
- **Missing Testing:**
  No CI/CD pipeline checks exist to validate that commits modifying AI pipelines originate from personnel with verified, active AI literacy records.
- **Missing Evidence:**
  The repository contains no sample training completion certificates, course syllabus templates, or competency evaluation rubrics.
- **Missing Audit Trail:**
  An immutable audit trail documenting policy reviews, curriculum updates, and historical staff training logs is missing from the repository.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy template specifying competency benchmarks for AI system deployers.
2. Establish a centralized `docs/AI_LITERACY_LOG.md` file within the repository structure.
3. Configure an automated CI pipeline check that raises warnings when training logs go unupdated for over 12 months.
4. Provide sample competency rubrics and training verification evidence templates.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act establishes mandatory transparency rules for AI systems, taking effect on 2 August 2026.

Under Article 50(1), providers must ensure AI systems interacting directly with natural persons inform users of AI interaction. Article 50(2) mandates that outputs of generative AI systems (text, audio, image, video) are marked in a machine-readable format and detectable as artificially generated. Article 50(4) requires deployers of deepfakes to disclose synthetic manipulation clearly.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an AI Transparency Policy specifying disclosure timing, synthetic media marking choices, and deepfake handling rules.
- **Missing Documentation:**
  Checklists mention Article 50 but lack technical integration guides detailing machine-readable watermarking standards (such as C2PA) and metadata embedding protocols.
- **Missing Code:**
  Sample codebases lack middle-tier utilities or helper classes for injecting C2PA metadata, watermarking synthetic media, or rendering AI interaction notices.
- **Missing Disclosure:**
  Chat UI and media generation templates fail to present prominent, immediate disclosures ("You are interacting with an AI system") at initial user exposure.
- **Missing Logging:**
  There are no backend logging schemas to capture user exposure to AI transparency notices or record synthetic media generation events.
- **Missing Testing:**
  Test suites contain no automated assertions or static scanners to verify that generated media outputs contain required machine-readable markers or metadata headers.
- **Missing Evidence:**
  The repository lacks verified test reports, watermarking validation outputs, or vendor content moderation audit certificates.
- **Missing Audit Trail:**
  An unalterable audit log tracking model deployments, watermarking key rotations, and transparency notice changes is not present in the repository.

### 6.3 Remediation and Action Plan
1. Formulate a comprehensive AI Transparency Policy template covering direct interaction notices and output watermarking.
2. Develop reusable code modules for C2PA metadata injection and in-app AI interaction banners.
3. Build automated integration tests to inspect generated synthetic assets for valid compliance metadata.
4. Create an immutable logging format for tracking AI notice impressions and watermarking events.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 (Digital Markets Act) imposes strict obligations on gatekeeper core platform services. For iOS and Android applications in the EU, the DMA mandates alternative app distribution, alternative browser engines, contactless NFC access, and out-of-app promotion and purchase links.

Apple's implementation requires the `com.apple.developer.storekit.external-purchase-link` entitlement, execution of system disclosure sheets (`ExternalPurchaseCustomLink`), notarization for non-App Store builds, and monthly sales reporting via the External Purchase Server API.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Alternative Distribution and Anti-Steering Policy guiding developers on EU entitlement management and revenue reporting.
- **Missing Documentation:**
  Documentation mentions DMA rules but lacks technical step-by-step guides for integrating the External Purchase Server API or configuring Web Distribution hosts.
- **Missing Code:**
  Sample mobile applications omit entitlement declarations, system disclosure sheet triggers (`ExternalPurchaseCustomLink`), and server-to-server reporting integrations.
- **Missing Disclosure:**
  In-app checkout templates lack required disclosures informing EU users that external transactions are executed outside platform protection mechanisms.
- **Missing Logging:**
  There are no backend logging schemas or event queues to log external purchase link activations and compile monthly 15-day reporting payloads.
- **Missing Testing:**
  No automated unit or integration tests exist to verify that StoreKit IAP and external purchase links are mutually exclusive on EU storefronts.
- **Missing Evidence:**
  The repository lacks sample notarization certificates, Web Distribution domain registration proofs, or External Purchase Server API submission logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking external revenue reporting, entitlement addendum sign-offs, and CTF/CTC fee calculations is absent.

### 7.3 Remediation and Action Plan
1. Publish an EU DMA Implementation Guide and compliance policy covering alternative distribution and steering rules.
2. Add reference code for invoking `ExternalPurchaseCustomLink` and compiling External Purchase Server API reporting JSON.
3. Build static checks verifying that apps do not co-mingle StoreKit IAP and external purchase links on the same EU storefront.
4. Establish automated logging for external link taps and transaction dispatch reporting.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (Digital Services Act) regulates online intermediaries and platforms. Articles 30 and 31 require app stores to collect, verify, and publish trader contact identity details for all entities distributing apps to EU consumers.

Developers distributing apps in the EU must submit verified business registration details, addresses, phone numbers, and emails to App Store Connect and Google Play Console. Failure to verify trader status results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no Trader Status Identification Policy or guidance for developers determining trader versus non-trader status under EU consumer law.
- **Missing Documentation:**
  Checklists note DSA trader submission but lack step-by-step documentation on 2FA verification, document upload requirements, and address publication impacts.
- **Missing Code:**
  The compliance guard scripts lack automated metadata verification checks to alert developers when trader declarations are unverified prior to release.
- **Missing Disclosure:**
  Storefront description templates lack explicit trader information blocks and consumer protection right warnings for non-trader listings.
- **Missing Logging:**
  There are no internal administrative logs to track trader declaration submissions, verification status changes, or store compliance updates.
- **Missing Testing:**
  No automated scripts exist to inspect App Store Connect metadata payloads and flag missing DSA trader verification states before submission.
- **Missing Evidence:**
  The repository contains no sample D-U-N-S verification records, official business registration uploads, or two-factor verification logs.
- **Missing Audit Trail:**
  An unalterable audit log documenting trader status declarations, verification attempts, and annual address confirmations is missing from the repository.

### 8.3 Remediation and Action Plan
1. Create a DSA Trader Determination Policy and step-by-step verification guide.
2. Update `scripts/metadata-audit.py` to inspect metadata configs for verified trader declaration flags.
3. Add trader contact block templates to metadata listing templates.
4. Establish an administrative record format for storing trader verification evidence.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) became enforceable on 28 June 2025. It mandates accessibility for mobile applications, e-commerce, banking, e-books, and digital services reaching EU consumers.

Compliance is measured against harmonised standard EN 301 549 version 3.2.1, which incorporates WCAG 2.1 Level AA and adds Chapter 11 software requirements for mobile applications. Developers must also publish a formal, accessible Accessibility Statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no organizational Accessibility Policy template defining EN 301 549 Chapter 11 commitments and governance.
- **Missing Documentation:**
  Documentation covers general accessibility rules but lacks comprehensive EN 301 549 Chapter 11 mapping guides for iOS VoiceOver and Android TalkBack.
- **Missing Code:**
  While accessibility audit scripts exist, sample codebases omit custom accessible view components, dynamic type scaling handlers, and accessible contrast themes.
- **Missing Disclosure:**
  The repository lacks templates for public Accessibility Statements required under EN 301 549 Annex B/C and EAA national transposition laws.
- **Missing Logging:**
  There are no logging mechanisms to record accessibility feedback submissions, user contrast mode changes, or screen reader interactions.
- **Missing Testing:**
  Automated testing scripts evaluate basic attributes but do not perform complete EN 301 549 Chapter 11 compliance audits across all 64 mobile criteria.
- **Missing Evidence:**
  The repository contains no sample Voluntary Product Accessibility Templates (VPAT), EN 301 549 evaluation reports, or user testing attestations.
- **Missing Audit Trail:**
  An immutable audit trail tracking accessibility regressions, issue remediation histories, and annual statement reviews is missing.

### 9.3 Remediation and Action Plan
1. Draft an EAA Compliance Policy and EN 301 549 Chapter 11 technical implementation guide.
2. Create reusable, fully accessible UI component libraries for Flutter, React Native, iOS, and Android.
3. Publish standardized Accessibility Statement templates in `templates/legal/`.
4. Expand `scripts/accessibility-audit.py` to audit all EN 301 549 mobile software criteria.

---

## 10. US Children's Online Privacy Protection Act (COPPA Amended Rule)

### 10.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) regulates online services directed to children under 13. The FTC's Amended COPPA Rule (finalized April 2025, mandatory 22 April 2026) significantly expands obligations.

Key amendments include expanding personal information to cover biometric identifiers and government IDs, requiring separate opt-in consent for third-party disclosures and targeted ads, mandating written data retention policies, and requiring a written information security program with annual risk assessments.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an updated COPPA Compliance Policy incorporating 2026 amendments for biometric data and retention limits.
- **Missing Documentation:**
  Checklists mention basic COPPA gates but lack developer guides for implementing separate third-party opt-in consent and age-gated onboarding.
- **Missing Code:**
  Sample codebases omit separate consent modal flows for third-party ad tracking and lack automated data retention purging logic for child profiles.
- **Missing Disclosure:**
  Onboarding templates lack granular consent disclosures separating core app functionality from third-party advertising disclosures.
- **Missing Logging:**
  There are no backend logging schemas to capture verifiable parental consent mechanisms (KBA, government ID match) or store separate opt-in consent states.
- **Missing Testing:**
  Test suites lack automated unit tests verifying that third-party analytics and ad SDKs are completely suppressed until separate parental opt-in is confirmed.
- **Missing Evidence:**
  The repository lacks sample Written Information Security Programs (WISP), annual COPPA risk assessments, or safe harbor certification proofs.
- **Missing Audit Trail:**
  An unalterable audit log tracking parental consent grants, consent revocations, and child data purge executions is absent.

### 10.3 Remediation and Action Plan
1. Formulate a complete 2026 Amended COPPA Policy template and Written Information Security Program (WISP) framework.
2. Develop UI components for granular, multi-step parental consent and biometric data disclosures.
3. Build automated SDK suppression wrappers to block third-party data transmission prior to explicit consent.
4. Add backend data purge triggers to enforce written retention schedules for child data.

---

## 11. California Consumer Privacy Act / CPRA (CPPA 2026 Regulations)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), regulates consumer data privacy. Final CPPA regulations effective 1 January 2026 enforce strict requirements for Global Privacy Control (GPC), notice at collection, and opt-out mechanisms.

Businesses must honor GPC signals (`Sec-GPC`), provide explicit "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links, and conduct cybersecurity audits.

Official Citation: California Civil Code Section 1798.100 et seq. and CPPA Regulations (2026).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template California Privacy Rights Policy or formal GPC Governance Guidelines.
- **Missing Documentation:**
  Checklists mention CCPA but lack technical implementation guides detailing GPC header processing in WebViews and native opt-out signaling.
- **Missing Code:**
  Sample web and mobile apps omit automated GPC header detection (`Sec-GPC`) and lack native logic to suppress ad data pipelines upon receiving opt-out signals.
- **Missing Disclosure:**
  UI templates omit mandatory "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" footer links.
- **Missing Logging:**
  There are no structured database schemas to log GPC signal receipts, consumer opt-out submissions, or consumer rights request fulfillments.
- **Missing Testing:**
  No automated integration tests exist to verify that setting the `Sec-GPC` header or toggling the in-app opt-out immediately disables tracking scripts.
- **Missing Evidence:**
  The repository contains no sample Privacy Impact Assessments (PIA), cybersecurity audit reports, or GPC compliance proofs.
- **Missing Audit Trail:**
  An immutable audit log recording consumer rights requests, opt-out timestamp logs, and policy modification histories is missing.

### 11.3 Remediation and Action Plan
1. Draft a CPRA/CCPA Compliance Policy template incorporating 2026 GPC and sensitive data rules.
2. Build frontend scripts and native modules to inspect `Sec-GPC` headers and sync opt-out states.
3. Add "Do Not Sell/Share" UI components and notice at collection templates to `templates/privacy/`.
4. Implement automated CI tests validating ad tracking suppression upon GPC signal detection.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14) regulates the collection, use, and retention of biometric identifiers (fingerprints, retina scans, voiceprints, facial geometry).

BIPA requires prior written notice, explicit written release before collection, a publicly available retention and destruction schedule, strict prohibition of sale or profit, and destruction within 3 years of last interaction. SB 2979 (effective August 2024) clarified per-person statutory liability.

Official Citation: 740 ILCS 14 (Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no standalone Biometric Information Privacy Policy template meeting BIPA statutory criteria.
- **Missing Documentation:**
  The repository lacks technical integration guidelines detailing BIPA disclosure requirements for mobile face and fingerprint authentication.
- **Missing Code:**
  Sample codebases omit pre-capture consent modal sheets and lack automated backend data destruction scripts for biometric templates.
- **Missing Disclosure:**
  In-app biometric onboarding flows omit explicit written disclosures detailing the specific purpose and duration of biometric data collection.
- **Missing Logging:**
  There are no backend database structures to log written consent execution, timestamped releases, or automated schedule-based data purges.
- **Missing Testing:**
  Test suites lack automated unit tests verifying that biometric capture APIs (LocalAuthentication / BiometricPrompt) are blocked until written release consent is logged.
- **Missing Evidence:**
  The repository contains no sample written release forms, publicly accessible retention schedules, or data destruction logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking written consent receipts, biometric policy updates, and template destruction events is missing.

### 12.3 Remediation and Action Plan
1. Create a BIPA-compliant Biometric Information Policy and Public Retention Schedule template.
2. Develop pre-capture consent UI components for iOS LocalAuthentication and Android BiometricPrompt flows.
3. Build automated database triggers to purge biometric data within statutory destruction timelines.
4. Add integration tests ensuring biometric APIs cannot be initialized without prior consent logging.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative option laws (California AB 3129, New York GBL 527-a, Massachusetts) regulate recurring subscriptions.

While the FTC federal Click-to-Cancel rule was vacated on procedural grounds in July 2025, ROSCA and state statutes actively mandate that online subscription cancellation must be at least as simple as sign-up, provided through the same medium, and fully frictionless (never requiring a phone call or physical letter).

Official Citations: 15 U.S.C. 8401 (ROSCA) and California Business and Professions Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Subscription Management and Cancellation Policy template for web-billed or cross-platform services.
- **Missing Documentation:**
  Checklists cover App Store / Google Play subscription rules but lack guides for web-based subscription funnels and state negative option compliance.
- **Missing Code:**
  Sample web billing applications lack self-service one-click cancellation buttons, modal confirmation flows, and automated churn handling endpoints.
- **Missing Disclosure:**
  Subscription checkout templates omit clear disclosures of recurring billing terms, cancellation steps, and pre-renewal notification paths.
- **Missing Logging:**
  There are no backend logging schemas to record subscription cancellation button clicks, timestamped confirmation emails, or immediate access termination logs.
- **Missing Testing:**
  No automated UI tests exist to verify that a web subscriber can successfully cancel a subscription within 3 clicks without contacting customer support.
- **Missing Evidence:**
  The repository contains no sample cancellation confirmation email templates, renewal notice logs, or subscription flow audit reports.
- **Missing Audit Trail:**
  An immutable audit log tracking subscription flow UI changes, cancellation drop-off rates, and renewal notification dispatches is absent.

### 13.3 Remediation and Action Plan
1. Draft a ROSCA and State Negative Option Subscription Policy template for web and hybrid applications.
2. Create reusable frontend cancellation components providing frictionless one-click termination.
3. Add mandatory renewal notification and cancellation disclosure templates to `templates/monetization/`.
4. Implement automated UI tests verifying that cancellation paths match sign-up simplicity.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the ICO Age Appropriate Design Code (Children's Code) regulate services accessible to UK children under 18.

Key duties include enforcing Highly Effective Age Assurance (facial age estimation, credit card checks, open banking), maintaining high privacy settings by default, disabling geolocation and profiling by default, and completing mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023 c. 50 and ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Child Safety and Age Appropriate Design Policy template covering Ofcom and ICO mandates.
- **Missing Documentation:**
  Checklists mention UK rules but lack detailed integration manuals for Ofcom-approved Highly Effective Age Assurance vendors.
- **Missing Code:**
  Sample codebases omit logic to automatically set high privacy, disable geolocation, and suppress profiling for UK child accounts.
- **Missing Disclosure:**
  In-app onboarding flows lack child-friendly privacy notices and transparency disclosures required under the ICO Code.
- **Missing Logging:**
  There are no backend database structures to log age estimation results, default privacy enforcement, or DPIA mitigation steps.
- **Missing Testing:**
  Test suites contain no automated unit tests verifying that geolocation and profiling services are disabled by default for UK accounts.
- **Missing Evidence:**
  The repository contains no sample ICO Children's Code DPIA templates, Ofcom risk assessments, or age verification vendor audit certificates.
- **Missing Audit Trail:**
  An unalterable audit log tracking DPIA revisions, age assurance system updates, and child safety incident reports is missing.

### 14.3 Remediation and Action Plan
1. Formulate a UK Online Safety Act Compliance Policy and ICO Children's Code DPIA template.
2. Develop code wrappers to enforce high privacy defaults (geolocation OFF, profiling OFF) based on UK user signals.
3. Integrate third-party age estimation vendor interfaces in sample code.
4. Add automated integration tests verifying privacy-by-default configurations for UK users.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 mandates that age-restricted social media platforms take reasonable steps to prevent under-16s from holding accounts. Enforced from 10 December 2025 by eSafety.

Accepted age assurance methods require a waterfall approach (facial age estimation, digital ID, document verification). Self-declaration checkboxes are explicitly prohibited. Age verification data must be ringfenced and destroyed immediately after processing.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Australian Social Media Age Restriction Policy or eSafety compliance governance guide.
- **Missing Documentation:**
  The repository lacks developer integration manuals for Australian age assurance waterfalls and data destruction workflows.
- **Missing Code:**
  Sample social media applications omit native integration blocks for eSafety-approved age estimation APIs and age data ringfencing wrappers.
- **Missing Disclosure:**
  Onboarding templates lack disclosures informing Australian users of minimum age requirements and age data deletion protocols.
- **Missing Logging:**
  There are no secure logging schemas to record age verification completion without storing prohibited raw age attributes.
- **Missing Testing:**
  No automated integration tests exist to confirm that under-16 Australian user accounts are blocked from social feed creation.
- **Missing Evidence:**
  The repository contains no sample eSafety compliance audit certificates, age verification accuracy reports, or data destruction attestations.
- **Missing Audit Trail:**
  An immutable audit log tracking age restriction system deployments, eSafety notice responses, and data purge verifications is missing.

### 15.3 Remediation and Action Plan
1. Create an Australian Minimum Age Restriction Policy and developer implementation guide.
2. Add code modules for eSafety-compliant age assurance waterfalls and immediate data destruction.
3. Build backend handlers to ringfence age verification sessions from general user profiling databases.
4. Implement automated UI tests verifying under-16 account blocking for Australian IP ranges.

---

## 16. Brazil Digital ECA (Law 15,211/2025) & LGPD

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025), enforced by the ANPD from 17 March 2026 alongside the LGPD, establishes strict digital protection rules for children and adolescents.

The law mandates robust age verification (document check, facial estimation, CPF database validation), prohibits self-declaration checkboxes, restricts profiling and targeted advertising to minors, and requires verifiable parental consent. Apple and Google Play enforce 18-plus blocks and Play Age Signals API integration in Brazil.

Official Citation: Lei Nº 15.211/2025 (Estatuto da Criança e do Adolescente Digital) and Lei Nº 13.709/2018 (LGPD).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazilian Digital ECA Compliance Policy and LGPD Minor Data Protection Policy template.
- **Missing Documentation:**
  Checklists mention Brazil rules but lack detailed integration documentation for CPF verification APIs and Google Play Age Signals in Brazil.
- **Missing Code:**
  Sample mobile applications omit CPF validation logic, Play Age Signals API hooks for Brazil, and loot-box 18-plus gating modules.
- **Missing Disclosure:**
  UI templates omit Portuguese-language child privacy notices and parental consent request disclosures.
- **Missing Logging:**
  There are no backend database structures to log verifiable parental consent, CPF validation states, or parental consent revocations.
- **Missing Testing:**
  Test suites contain no automated unit tests verifying that loot-box or social features are gated behind 18-plus verification for Brazilian accounts.
- **Missing Evidence:**
  The repository contains no sample LGPD Data Protection Impact Assessments (DPIA), ANPD compliance reports, or CPF API verification logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking age verification system updates, parental consent logs, and ANPD inquiry responses is missing.

### 16.3 Remediation and Action Plan
1. Publish a Brazilian Digital ECA Policy and LGPD Minor Privacy template in `templates/legal/`.
2. Add reference code for CPF validation and Google Play Age Signals API integration for Brazilian users.
3. Build automated test cases verifying 18-plus gating on loot-box and age-restricted features.
4. Establish secure, privacy-compliant logging schemas for parental consent management.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act (DPDPA) 2023 and the DPDP Rules 2025 (notified November 2025, mandatory May 2027) establish a comprehensive data protection regime.

For children under 18, the DPDPA mandates verifiable parental consent obtained through government-backed identity systems (such as DigiLocker) before processing any personal data. Behavioral tracking, targeted advertising, and harmful content delivery to children are strictly prohibited.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Indian DPDPA Compliance Policy template or Governance Framework for Significant Data Fiduciaries.
- **Missing Documentation:**
  The repository lacks developer integration guides for DigiLocker parental consent workflows and multi-lingual notice requirements in 22 scheduled languages.
- **Missing Code:**
  Sample codebases omit DigiLocker OAuth/consent API bindings, parental consent verification handlers, and ad-tracking suppression for under-18s.
- **Missing Disclosure:**
  UI templates lack granular consent notices presented in English and scheduled Indian languages detailing specific data processing purposes.
- **Missing Logging:**
  There are no backend logging schemas to record DigiLocker consent receipts, consent withdrawal notifications, or Data Protection Officer (DPO) logs.
- **Missing Testing:**
  No automated unit tests exist to verify that targeted ad SDKs are disabled when the user signal corresponds to an Indian account under 18.
- **Missing Evidence:**
  The repository contains no sample DPDPA Data Protection Impact Assessments, Data Audit reports, or DigiLocker integration certificates.
- **Missing Audit Trail:**
  An unalterable audit log tracking consent withdrawal requests, DPO grievance resolutions, and annual data audits is missing.

### 17.3 Remediation and Action Plan
1. Draft an Indian DPDPA Policy template and multi-lingual consent notice guidelines.
2. Develop code wrappers for DigiLocker verifiable parental consent API integration.
3. Build static checks verifying complete ad tracking suppression for under-18 Indian users.
4. Establish structured audit logging formats for handling data principal rights and DPO records.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Code of Practice

### 18.1 Regulatory Overview and Background
Singapore's Personal Data Protection Act (PDPA) and the IMDA Code of Practice for Online Safety for App Distribution Services establish privacy and child safety standards.

Effective 1 April 2026, app stores and developers must implement age assurance measures to prevent under-18s from accessing age-inappropriate content. Age assurance data must be destroyed immediately after verification. Apple enforces 18-plus download blocks in Singapore from February 2026.

Official Citations: Personal Data Protection Act 2012 (No. 26 of 2012) and IMDA Code of Practice for Online Safety (2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no Singapore PDPA & IMDA Online Safety Policy template.
- **Missing Documentation:**
  Checklists lack developer instructions for integrating IMDA-compliant age assurance and executing mandatory data destruction protocols.
- **Missing Code:**
  Sample applications omit credit card / Singpass age verification integration hooks and lack immediate verification data purge routines.
- **Missing Disclosure:**
  UI templates omit mandatory Singapore privacy notices regarding age verification purpose and data retention limits.
- **Missing Logging:**
  There are no structured backend database schemas to record age verification completion status without retaining underlying identity documents.
- **Missing Testing:**
  Test suites contain no automated assertions verifying that raw age verification records are deleted within 60 seconds of transaction completion.
- **Missing Evidence:**
  The repository contains no sample Data Protection Officer (DPO) designation forms, IMDA compliance reports, or age verification audit logs.
- **Missing Audit Trail:**
  An immutable audit log tracking age verification system updates, DPO contact publications, and data destruction verifications is missing.

### 18.3 Remediation and Action Plan
1. Formulate a Singapore PDPA and IMDA Online Safety Compliance Policy template.
2. Build code modules for Singpass / credit card age verification and automated data purging.
3. Publish DPO contact disclosure templates and privacy policy addendums for Singapore users.
4. Create automated test cases verifying zero retention of raw age verification payloads.

---

## 19. South Korea Telecommunications Business Act & PIPA

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment methods, while the Personal Information Protection Act (PIPA) governs personal data protection.

Apple's Korea alternative payment implementation requires the `com.apple.developer.storekit.external-purchase` entitlement (value `SKExternalPurchase = "KR"`), a dedicated South Korea binary, approved Korean payment gateways (KCP, Inicis, Toss, NICE), a native system disclosure modal, 26% commission reporting within 15 days, and monthly remittance.

Official Citations: Telecommunications Business Act Article 22-9 and Personal Information Protection Act (Act No. 10465).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no South Korea Alternative Billing and PIPA Compliance Policy template.
- **Missing Documentation:**
  Documentation mentions Korean alternative payments but lacks technical guides for building Korea-only binaries and wiring approved Korean payment SDKs.
- **Missing Code:**
  Sample mobile applications omit `SKExternalPurchase = "KR"` entitlement declarations, system modal triggers, and reporting payload generators.
- **Missing Disclosure:**
  In-app checkout templates lack mandatory pre-transaction disclosures informing Korean users of alternative payment terms and non-platform protection.
- **Missing Logging:**
  There are no backend database structures to log Korean alternative payment transactions, calculate 26% commissions, and compile 15-day monthly reports.
- **Missing Testing:**
  No automated unit tests exist to verify that Korean alternative payment entitlements are strictly gated to South Korea storefront binaries.
- **Missing Evidence:**
  The repository contains no sample approved payment gateway contracts (KCP, Toss, Inicis), monthly sales report payloads, or PIPA privacy audit logs.
- **Missing Audit Trail:**
  An unalterable audit log tracking monthly sales reporting, fee remittance receipts, and PIPA compliance reviews is missing.

### 19.3 Remediation and Action Plan
1. Publish a South Korea Alternative Payment & PIPA Policy template.
2. Add reference code for `SKExternalPurchase = "KR"` entitlement configuration and approved Korean payment gateway SDK wrappers.
3. Build automated reporting scripts to compile 15-day monthly sales reporting JSON.
4. Implement static checks ensuring Korean alternative payment code is restricted to South Korea binaries.

---

## 20. China Mobile App Filing (MIIT / ICP) & PIPL

### 20.1 Regulatory Overview and Background
The Ministry of Industry and Information Technology (MIIT) of China mandates Mobile App Filing (an extension of the ICP filing regime). Unfiled apps are blocked from distribution on Chinese storefronts.

Foreign developers must partner with a local Chinese entity or establish a local subsidiary. Compliance also requires adherence to the Personal Information Protection Law (PIPL), real-name identity verification, local data hosting, content moderation pipelines, and a Banhao license for gaming applications.

Official Citations: MIIT Circular on Mobile Application Filing (2023) and Personal Information Protection Law (PIPL, 2021).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook contains no China MIIT Filing and PIPL Compliance Policy template.
- **Missing Documentation:**
  Checklists note MIIT filing requirements but lack detailed operational manuals covering ICP domain binding, local partner agreements, and Banhao licensing steps.
- **Missing Code:**
  Sample codebases omit real-name identity verification modules, local Chinese cloud storage adapter configurations, and content moderation API triggers.
- **Missing Disclosure:**
  Storefront description and in-app privacy templates omit PIPL-compliant disclosures, local entity contact details, and MIIT filing number displays.
- **Missing Logging:**
  There are no backend logging schemas to capture real-name verification logs, user content moderation flags, or cross-border data transfer assessments.
- **Missing Testing:**
  No automated integration tests exist to verify that Chinese app builds direct user data exclusively to local mainland Chinese server endpoints.
- **Missing Evidence:**
  The repository contains no sample MIIT app filing submission receipts, ICP license documentation, or PIPL Personal Information Protection Impact Assessments (PIPIA).
- **Missing Audit Trail:**
  An immutable audit log tracking real-name verification records, content moderation actions, and annual PIPL compliance audits is missing.

### 20.3 Remediation and Action Plan
1. Create a China MIIT App Filing and PIPL Compliance Policy template in `templates/legal/`.
2. Add code modules for real-name identity verification and local Chinese storage endpoint routing.
3. Publish metadata listing templates displaying MIIT filing numbers and local operator disclosures.
4. Establish structured audit logging formats for content moderation and real-name verification records.

---

## 21. Consolidated Gap Classification Matrix

The matrix below evaluates the repository's current coverage across all twenty audited regulations.
- **Covered:** The repository contains actionable guidelines, detection rules, code samples, disclosures, logging, testing, evidence, and audit trails.
- **Partial:** The regulation is cited or referenced in documentation, but lacks actionable code, tests, logging, or evidence.
- **Missing:** The regulation is entirely unaddressed in the repository.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. US COPPA (Amended)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA / GPC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety / ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea Telecom Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China Mobile App Filing** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Roadmap

The playbook repository provides comprehensive coverage of store rejection guidelines, platform policies, and regulatory deadline dates. However, across all twenty global regulations, significant operational gaps remain in the implementation layer: specifically automated code detectors, reusable UI components, logging schemas, integration test suites, evidence templates, and unalterable audit trails.

### Priority Remediation Order:
1. **Immediate (Phase 1):** Add missing detection rules to `data/rejection-patterns.json` and `data/detection-recipes.json` for EU GPSR, US ASAA, EU Withdrawal Button, EU e-Evidence, and CPRA GPC.
2. **Short-Term (Phase 2):** Create reusable legal policy templates in `templates/legal/` and UI component libraries for AI transparency (Art 50), contract withdrawal buttons, and parental consent modals.
3. **Mid-Term (Phase 3):** Build automated integration test scripts (`scripts/release-audit.py`, `scripts/accessibility-audit.py`) and backend logging schemas to verify compliance evidence and maintain audit trails prior to app release.

---

## 23. Sources

Every audited framework is cited below to its official primary source:

- **EU GPSR:** [Regulation (EU) 2023/988 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **EU e-Evidence Package:** [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **EU Contract Withdrawal:** [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **US State ASAAs:** [Utah SB 142 Text](https://le.utah.gov/~2025/bills/static/SB0142.html) & [Apple Texas SB 2420 Announcement](https://developer.apple.com/news/?id=btkirlj8)
- **EU AI Act:** [Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **EU DMA:** [Regulation (EU) 2022/1925 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **EU DSA:** [Regulation (EU) 2022/2065 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **European Accessibility Act:** [Directive (EU) 2019/882 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **US COPPA Amended Rule:** [FTC Final COPPA Rule (Federal Register)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **California CPRA / GPC:** [California AG CCPA](https://oag.ca.gov/privacy/ccpa) & [CPPA Regulations](https://cppa.ca.gov/regulations/ccpa_updates.html)
- **Illinois BIPA:** [Illinois General Assembly BIPA 740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- **US Subscription Cancellation / ROSCA:** [FTC ROSCA Guidance](https://www.ftc.gov/business-guidance/resources/complying-ftc-guidance-about-online-negative-option-plans)
- **UK Online Safety Act & ICO:** [UK Online Safety Act 2023](https://www.legislation.gov.uk/ukpga/2023/50/contents) & [ICO Children's Code Guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- **Australia Online Safety Amendment:** [eSafety Industry Regulation](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- **Brazil Digital ECA:** [ANPD Portal](https://www.gov.br/anpd/pt-br)
- **India DPDPA:** [India Gazette DPDPA 2023](https://egazette.gov.in/)
- **Singapore PDPA & IMDA:** [IMDA App Distribution Safety Code](https://www.imda.gov.sg/)
- **South Korea Telecom Act:** [Apple StoreKit External Purchase Korea](https://developer.apple.com/support/storekit-external-entitlement-kr/)
- **China Mobile App Filing:** [MIIT App Filing Portal](https://beian.miit.gov.cn/)
