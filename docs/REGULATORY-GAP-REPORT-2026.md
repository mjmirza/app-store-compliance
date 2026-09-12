# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates repository requirements against twenty major global and regional regulatory frameworks binding mobile and web applications shipping into the EU, US, UK, APAC, and LATAM markets. It checks honestly how far this repository already carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight distinct gap categories:
1. missing policy
2. missing documentation
3. missing code
4. missing disclosure
5. missing logging
6. missing testing
7. missing evidence
8. missing audit trail

Assume the repository is incomplete unless proven otherwise. Continue searching until no additional gaps remain.

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

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or withdrawal function on the online interface for distance contracts for financial services concluded by electronic means.

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

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (ASAA) represent a growing wave of state-level legislation (Utah SB 142 as amended by HB 498, Texas SB 2420, Louisiana HB 977, Alabama HB 161) aimed at regulating minors' access to mobile applications, in-app purchases, and content updates.

Developers must request and process the user's age category (e.g., via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Furthermore, verified age verification data must be deleted immediately after verification to protect children's privacy.

Official Citations: Utah SB 142 / HB 498 (2026), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

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
  No helper script exists in the repository to automatically check whether an AI literacy training log exists and is current.
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

---

## 7. European Accessibility Act (EAA) & US ADA Title II

### 7.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act, EAA) became enforced on 28 June 2025 across EU member states, mandating strict accessibility compliance for e-commerce, banking, electronic communication, and mobile applications. In parallel, the US Department of Justice finalized ADA Title II web and mobile app accessibility rules (28 CFR Part 35 Subpart H, 2026) requiring WCAG 2.1 Level AA conformance by April 2027 (large entities) and April 2028 (small entities).

Official Citations: Directive (EU) 2019/882; US 28 CFR Part 35 Subpart H; US 45 CFR 84.84(b) (HHS Section 504).

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks an explicit, adoptable Accessibility Policy statement defining WCAG 2.1 AA conformance targets and grievance procedures.
- **Missing Documentation:**
  `docs/ACCESSIBILITY-COMPLIANCE-REPORT.md` details testing tools but lacks step-by-step developer remediation guides for complex UI components (e.g., custom web view wrappers or dynamic charts).
- **Missing Code:**
  Static analysis script `scripts/accessibility-audit.py` checks basic contrast and labels, but frontend UI templates lack native accessibility helpers for focus management and screen reader live region announcements.
- **Missing Disclosure:**
  Public-facing app templates do not include mandatory Accessibility Statements detailing conformance status, supported assistive technologies, and feedback contact channels.
- **Missing Logging:**
  No backend or client logging structure exists to record user-reported accessibility bugs, barrier feedback, or assist device capability flags.
- **Missing Testing:**
  While static checks exist, there are no automated end-to-end screen reader interaction tests (e.g. Playwright or XCTest with VoiceOver simulation) integrated into CI workflows.
- **Missing Evidence:**
  The playbook provides no templates for Voluntary Product Accessibility Templates (VPAT 2.4/2.5) or formal EU EAA Conformity Declarations.
- **Missing Audit Trail:**
  No versioned audit trail tracks accessibility remediation cycles, third-party audit reports, or historical VPAT revisions.

---

## 8. Amended US COPPA Rule (16 CFR Part 312)

### 8.1 Regulatory Overview and Background
The Federal Trade Commission (FTC) published finalized amendments to the Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312) alongside the FTC Enforcement Policy Statement Promoting Age-Verification Technology (February 2026). The rule imposes strict restrictions on targeted advertising, separate opt-in consent for third-party disclosures, enhanced security requirements, and strict data retention limits for child data.

Official Citation: FTC 16 CFR Part 312; FTC Enforcement Policy Statement (25 February 2026).

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No standalone Child Privacy Policy template exists in the repository meeting the updated 2026 FTC disclosure requirements.
- **Missing Documentation:**
  `docs/MOBILE-PRIVACY-MONITOR-2026.md` covers COPPA generally but lacks developer operational guides for handling separate parental consent for third-party disclosures versus core app features.
- **Missing Code:**
  Codebase templates lack automated retention purgers designed to hard-delete child personal information after the specific fulfillment purpose expires.
- **Missing Disclosure:**
  Direct parental notice templates in the repository do not reflect the amended requirement to itemize third-party data recipients and specific SDK tracking purposes.
- **Missing Logging:**
  No database schemas exist for logging verifiable parental consent (VPC) methods, consent scopes, or parental revocation requests.
- **Missing Testing:**
  Automated tests do not verify that child account creation flows disable secondary analytics SDKs before verifiable parental consent is registered.
- **Missing Evidence:**
  The repository lacks templates for COPPA Safe Harbor self-assessments or annual parental notification receipts.
- **Missing Audit Trail:**
  No immutable log records parental consent modifications, data deletion requests, or SDK permission grants for child accounts.

---

## 9. UK Online Safety Act (OSA 2023)

### 9.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced progressively through 2025-2027) imposes strict duties of care on user-to-user services and search services to protect users, particularly children, from illegal content, harm, and age-inappropriate material. Secondary legislation under the Children's Wellbeing and Schools Act (announced June 2026) further mandates under-16 functionality restrictions and AI companion age gates (18+ floor).

Official Citation: UK Online Safety Act 2023 (c. 50); Ofcom Codes of Practice (2025/2026).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a template Safety Policy for user-generated content (UGC) and interactive communications aligned with Ofcom safety duties.
- **Missing Documentation:**
  The playbook lacks developer guidance on completing mandatory Ofcom Children's Risk Assessments or illegal content risk assessments.
- **Missing Code:**
  No backend code components exist for automated illegal content filtering, priority content flagging, or enforcing the 18+ age gate on AI romantic companions.
- **Missing Disclosure:**
  Public terms lack required UK OSA disclosures detailing content moderation policies, report-and-remove procedures, and child safety safeguards.
- **Missing Logging:**
  No logging mechanisms exist to capture content reporting events, moderation actions, or Ofcom statutory compliance metrics.
- **Missing Testing:**
  No automated test suites test content reporting endpoints, appeal flows, or age assurance gating for UK IP ranges.
- **Missing Evidence:**
  The repository provides no completed examples or templates of Ofcom Risk Assessment documentation.
- **Missing Audit Trail:**
  No historical audit log tracks content moderation decisions, takedown response times, or annual safety review updates.

---

## 10. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880/2026)

### 10.1 Regulatory Overview and Background
Brazil's Law 15,211/2025 (Digital ECA) regulated by Decreto n. 12.880 (18 March 2026) establishes strict child safety, age assurance, and algorithmic protection rules for internet applications accessed by children and adolescents in Brazil, with ANPD enforcement commencing in 2027.

Official Citation: Law 15,211/2025; Decreto n. 12.880 of 18 March 2026; ANPD Resolution 2026.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Digital ECA Protection Policy template exists for developers targeting the Brazilian market.
- **Missing Documentation:**
  Documentation lacks step-by-step instructions on implementing Brazilian age signals and ANPD-compliant default privacy settings for minors.
- **Missing Code:**
  No native hooks exist for parsing Decreto 12.880 OS-level age signals or disabling recommended content algorithms for accounts identified as minors in Brazil.
- **Missing Disclosure:**
  App onboarding UI templates do not include mandatory Portuguese-language child safety disclosures or explanations of age verification procedures.
- **Missing Logging:**
  No logging schemas exist to capture parental authorization signals or age assurance verification results under ANPD guidelines.
- **Missing Testing:**
  CI pipelines lack tests verifying that accounts under 18 in Brazil have profiling and targeted advertising disabled by default.
- **Missing Evidence:**
  The repository lacks templates for ANPD Algorithmic Impact Assessments (RIPA) or child protection compliance reports.
- **Missing Audit Trail:**
  No audit trail tracks changes to minor account default privacy states or algorithmic recommendation settings.

---

## 11. India Digital Personal Data Protection Act (DPDPA 2023 & DPDP Rules 2025)

### 11.1 Regulatory Overview and Background
India's DPDPA 2023 and the DPDP Rules 2025 (G.S.R. 846(E)) mandate explicit consent mechanisms, verifiable parental consent for children (under 18), rights of data principal, and integration with registered Consent Managers by November 2026.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository does not supply a DPDPA-aligned Data Principal Rights Policy or Consent Manager Integration Policy.
- **Missing Documentation:**
  Checklists lack operational steps for supporting all 22 scheduled Indian languages in consent notices as required by DPDPA Section 5(3).
- **Missing Code:**
  No API client code exists for communicating with Indian Consent Managers or processing verifiable parental consent for Indian users.
- **Missing Disclosure:**
  Privacy notice templates do not provide multilingual placeholders or explicit itemization of Data Fiduciary contact details and Data Protection Officer (DPO) identity.
- **Missing Logging:**
  No database schemas exist for recording consent artifacts, language selection, or consent withdrawal notifications received from Consent Managers.
- **Missing Testing:**
  Automated tests do not validate consent notice rendering in Indian scheduled languages or the revocation workflow via Consent Manager webhooks.
- **Missing Evidence:**
  The playbook lacks standard templates for Data Protection Impact Assessments (DPIA) required for Significant Data Fiduciaries under DPDPA.
- **Missing Audit Trail:**
  No immutable log records historical consent grants, DPO appointment records, or data principal grievance resolutions.

---

## 12. California CPRA & Automated Decision-Making Technology (ADMT)

### 12.1 Regulatory Overview and Background
The California Privacy Protection Agency (CPPA) 2026 regulations under 11 CCR section 7200 et seq. govern Automated Decision-Making Technology (ADMT), risk assessments, and annual cybersecurity audits, imposing opt-out rights for profiling and automated decisioning.

Official Citation: California Consumer Privacy Act (CCPA) as amended by CPRA; 11 CCR sections 7121, 7155, 7157, 7200.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No California ADMT Opt-Out Policy or Profiling Disclosure Policy template is provided in the repository.
- **Missing Documentation:**
  `docs/MOBILE-PRIVACY-MONITOR-2026.md` lacks implementation runbooks for pre-goods/services profiling opt-out notices under CPPA Section 7200(b).
- **Missing Code:**
  Code templates lack middleware or flag checks to bypass automated decisioning algorithms when a user exercises their CPRA ADMT opt-out right.
- **Missing Disclosure:**
  UI onboarding templates do not display required CPPA "Notice at Collection" or "Opt-Out of Automated Decision-Making" modal sheets.
- **Missing Logging:**
  No backend logging structure records user ADMT opt-out selections or Global Privacy Control (GPC) signal interpretations.
- **Missing Testing:**
  No integration tests simulate GPC headers or ADMT opt-out toggles to confirm feature execution without automated profiling.
- **Missing Evidence:**
  The repository lacks templates for CPPA Risk Assessments for high-risk processing or ADMT evaluation reports.
- **Missing Audit Trail:**
  No audit trail maintains records of annual cybersecurity audits or historical CPPA risk assessment submissions.

---

## 13. UK Digital Markets, Competition and Consumers Act (DMCCA 2024)

### 13.1 Regulatory Overview and Background
Part 4, Chapter 2 of the UK DMCCA 2024 establishes a new mandatory statutory regime for subscription contracts starting in 2027. It requires explicit pre-contract information, mandatory reminder notices, frictionless end-to-end online cancellation, and statutory cooling-off cancellation rights.

Official Citation: Digital Markets, Competition and Consumers Act 2024 (c. 13), Part 4 Chapter 2.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository lacks a UK Subscription Contracts Policy template covering statutory cancellation windows and reminder notice schedules.
- **Missing Documentation:**
  Checklists do not detail DMCCA-specific requirements for sending pre-cancellation summary screens and immediate written acknowledgments.
- **Missing Code:**
  No automated job schedules exist in billing sample code to trigger subscription reminder notifications (6-month and trial end reminders) required by DMCCA.
- **Missing Disclosure:**
  Paywall and purchase screen templates fail to display the mandatory DMCCA Key Terms summary box before contract binding.
- **Missing Logging:**
  No database tables exist to log receipt and dispatch of mandatory subscription reminder notices or cancellation receipts.
- **Missing Testing:**
  Automated tests do not verify that subscription cancellation flows can be executed via a single online step without forced phone calls or chat prompts.
- **Missing Evidence:**
  The playbook provides no templates for DMCCA compliance verification audits or subscription disclosure records.
- **Missing Audit Trail:**
  No historical log tracks changes to subscription price terms, trial periods, or user cancellation journey steps.

---

## 14. EU Cyber Resilience Act (CRA)

### 14.1 Regulatory Overview and Background
Regulation (EU) 2024/2847 (Cyber Resilience Act) applies cybersecurity requirements to all digital products with digital elements placed on the EU market, mandating vulnerability reporting (24-hour initial notification to ENISA/CSIRTs) from 2026 and software bill of materials (SBOM) obligations from 2027.

Official Citation: Regulation (EU) 2024/2847 of the European Parliament and of the Council.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Cyber Resilience Compliance Policy or Vulnerability Disclosure Policy template is provided in the repository.
- **Missing Documentation:**
  Developers have no guides explaining how to maintain software security updates throughout the expected product support period under CRA Article 10.
- **Missing Code:**
  The repository lacks automated CI tools to generate standardized Software Bill of Materials (SBOM in CycloneDX or SPDX format) during build pipelines.
- **Missing Disclosure:**
  Public documentation templates do not include mandatory security contact endpoints (such as `security.txt` per RFC 9116) or defined support period declarations.
- **Missing Logging:**
  No architectural provision or logging schema exists for recording actively exploited vulnerabilities or security patch release metrics.
- **Missing Testing:**
  CI pipelines lack mandatory automated vulnerability scanning (SAST/DAST) gates blocking release on unpatched Critical/High CVEs.
- **Missing Evidence:**
  The playbook lacks templates for CRA EU Declarations of Conformity or Technical Documentation files required under Annex V.
- **Missing Audit Trail:**
  No tamper-proof log tracks vulnerability remediation timelines, ENISA notification submissions, or firmware/binary security releases.

---

## 15. EU Data Act (Regulation (EU) 2023/2854)

### 15.1 Regulatory Overview and Background
The EU Data Act (Regulation (EU) 2023/2854) entered into force in September 2025, mandating data access by design, interoperability, and data switching rights for connected products and related services. Switching charges must hit zero by January 2027.

Official Citation: Regulation (EU) 2023/2854 of the European Parliament and of the Council.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The repository provides no Data Sharing Policy or Data Portability and Switching Policy template.
- **Missing Documentation:**
  No developer guidelines detail how to structure backend APIs to provide real-time, direct data access to users or third parties designated by users under Article 4.
- **Missing Code:**
  Backend sample code lacks user-facing export endpoints capable of streaming raw generated telemetry data in standard machine-readable formats.
- **Missing Disclosure:**
  Pre-contract disclosures do not inform users of the nature, volume, and collection frequency of data generated by their use of the application.
- **Missing Logging:**
  No logging tables exist to track user data access requests, third-party data transmission authorizations, or cloud switching requests.
- **Missing Testing:**
  No integration tests verify that data export APIs function without error under high volume or multi-tenant user requests.
- **Missing Evidence:**
  The playbook provides no templates for Data Act Smart Contract Interoperability Declarations or FRAND licensing agreements.
- **Missing Audit Trail:**
  No immutable log records third-party data sharing consents, data transfer timestamps, or switching request completions.

---

## 16. Australia Social Media Minimum Age Act 2024

### 16.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 sets a mandatory 16-year minimum age for restricted social media platforms in Australia, requiring reasonable steps to prevent system access by age-restricted users.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024; eSafety Commissioner Rules.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Australian Minimum Age Compliance Policy template exists in the repository.
- **Missing Documentation:**
  Checklists lack developer instructions on determining whether an app meets the statutory definition of a "restricted social media platform" under Australian law.
- **Missing Code:**
  No code modules implement age assurance gates or geo-fenced account blocks for Australian IP addresses for users under 16.
- **Missing Disclosure:**
  Onboarding UI templates lack mandatory Australian disclosures regarding age restrictions and verification procedures.
- **Missing Logging:**
  No logging mechanisms record age verification attempts, pass/fail status, or age signal verification tokens for Australian users.
- **Missing Testing:**
  CI test suites do not include geo-location mock tests verifying that Australian users under 16 are blocked from account creation.
- **Missing Evidence:**
  The playbook provides no templates for eSafety Commissioner compliance demonstration filings or age-assurance audit reports.
- **Missing Audit Trail:**
  No audit trail logs historical changes to age gating rules or system access rejections for minor accounts.

---

## 17. South Korea Telecommunications Business Act & PIPA

### 17.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (Article 22-9) and PIPA Amendment (Act No. 21445) enforce strict in-app payment alternative mandates, location data consent, minor protection, and mandatory data breach notifications within 24 hours.

Official Citation: Telecommunications Business Act; Personal Information Protection Act (Act No. 21445).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No South Korea Compliance Policy template covering alternative billing and PIPA data protection requirements exists.
- **Missing Documentation:**
  Developers lack documentation detailing KCC (Korea Communications Commission) submission requirements for third-party payment gateways in Korea.
- **Missing Code:**
  Sample code lacks Korean alternative payment SDK integrations and separate location data consent modal dialogs required by Korean law.
- **Missing Disclosure:**
  Paywall and privacy templates do not include mandated Korean disclosures regarding third-party payment fee structures or location data usage.
- **Missing Logging:**
  No backend logging schema captures location data access logs (mandatory 6-month retention under Korean Location Data Act) or alternative payment audit records.
- **Missing Testing:**
  No unit tests verify that Korean billing routes successfully trigger alternative payment providers when requested in KR locale.
- **Missing Evidence:**
  The repository lacks templates for PIPC (Personal Information Protection Commission) compliance reports or KCC payment registration documentation.
- **Missing Audit Trail:**
  No immutable log records 24-hour breach notification triggers, location consent grants, or payment gateway routing changes.

---

## 18. Singapore IMDA Code of Practice & OSRAA 2025

### 18.1 Regulatory Overview and Background
Singapore's IMDA Code of Practice for Online Safety for App Distribution Services and the Online Safety (Relief and Accountability) Act 2025 (OSRAA) mandate child safety measures, content moderation, and rapid compliance with IMDA blocking orders.

Official Citation: IMDA Code of Practice for App Distribution Services; OSRAA 2025.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore App Safety & Content Moderation Policy template exists in the playbook.
- **Missing Documentation:**
  Checklists lack operational runbooks for complying with IMDA Content Direction orders within statutory deadlines.
- **Missing Code:**
  Code templates lack administrative controls or feature flags allowing rapid region-specific disabling of flagged app features or accounts in Singapore.
- **Missing Disclosure:**
  App store listing and privacy templates lack required Singapore online safety disclosures and reporting contact links.
- **Missing Logging:**
  No database schemas record IMDA regulatory notifications, content moderation interventions, or user appeal outcomes.
- **Missing Testing:**
  No automated tests verify that content blocking toggles correctly restrict content availability in SG storefront configurations.
- **Missing Evidence:**
  The repository lacks standard templates for IMDA Annual Safety Compliance Reports.
- **Missing Audit Trail:**
  No audit log maintains historical records of regulatory directions received from IMDA or executive actions taken in response.

---

## 19. China Mobile App Filing & AI Companion Measures

### 19.1 Regulatory Overview and Background
China's MIIT Mobile App Filing requirement (ICP Extension) and CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, July 2026) mandate formal app registration with MIIT and prohibit AI companion/anthropomorphic services from interacting with minors.

Official Citation: MIIT Notice on Mobile Application ICP Filing (2023/2024); CAC Order No. 21 (2026).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China Filing & AI Safety Policy template is provided in the repository.
- **Missing Documentation:**
  Developers have no documentation explaining how to complete MIIT ICP filing or implement CAC real-name identity verification for Chinese releases.
- **Missing Code:**
  Codebase templates lack real-name authentication hooks (CAC compliant) or minor blocking filters for AI conversational companion features.
- **Missing Disclosure:**
  UI templates do not include MIIT ICP filing number display components required in app footers or settings pages.
- **Missing Logging:**
  No logging structure exists for recording real-name verification tokens or CAC AI content moderation logs.
- **Missing Testing:**
  CI workflows do not include tests verifying that AI companion features are strictly disabled when minor status is flagged in CN region builds.
- **Missing Evidence:**
  The playbook provides no templates for MIIT Filing receipts, CAC AI Algorithm Filing registrations, or safety assessment filings.
- **Missing Audit Trail:**
  No audit log tracks real-name verification records, algorithm updates, or CAC regulatory inspection histories.

---

## 20. US Illinois Biometric Information Privacy Act (BIPA, 740 ILCS 14)

### 20.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) regulates the collection, use, and retention of biometric identifiers and information (such as facial geometry, voiceprints, or fingerprints). The 2024 legislative amendment clarified per-person recovery, but strict written consent and public retention schedules remain mandatory.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14/1 et seq.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No template Biometric Information Privacy Policy meeting BIPA Section 15(a) requirements exists in the repository.
- **Missing Documentation:**
  Checklists lack developer guidance on distinguishing device-local biometric auth (e.g. iOS LocalAuthentication / Android BiometricPrompt) from backend biometric data processing.
- **Missing Code:**
  Mock code templates lack explicit written consent modal flows prior to initializing biometric capture SDKs.
- **Missing Disclosure:**
  In-app UI templates do not include mandatory BIPA disclosures itemizing the specific biometric data collected, purpose, and storage length.
- **Missing Logging:**
  No database schema exists for recording written biometric consent signatures, consent timestamps, or destruction confirmations.
- **Missing Testing:**
  Automated test suites do not check whether biometric processing APIs execute prior to written consent flag verification.
- **Missing Evidence:**
  The repository provides no templates for BIPA Biometric Retention and Destruction Schedules or annual compliance certificates.
- **Missing Audit Trail:**
  No immutable log tracks biometric consent receipts, data deletion cycles, or biometric vendor agreement reviews.

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
| **EAA / US ADA Title II** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **Amended US COPPA Rule** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **California CPRA/ADMT** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **UK DMCCA Subscriptions** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU Cyber Resilience Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU Data Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Australia Social Media Min Age** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **KR Telecom / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **SG IMDA / OSRAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **China App Filing / AI Companion** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Roadmap

The playbook provides exceptional coverage of app store rejection guidelines and primary regulatory dates. However, across all 20 evaluated global frameworks, significant operational gaps remain across code implementations, backend logging schemas, automated test suites, compliance evidence artifacts, and immutable audit trails.

Priority Remediation Actions:
1. Implement detection rules in `data/rejection-patterns.json` and `data/detection-recipes.json` for all 20 audited regulations.
2. Develop frontend UI components and backend sample scripts for high-priority 2026 deadlines (EU Contract Withdrawal Button, EU e-Evidence response scripts, AI Act Art 50 watermarking).
3. Create standardized compliance evidence and policy templates in `references/` for BIPA, COPPA, DPDPA, and EAA VPAT declarations.
4. Integrate CI/CD automated test guards verifying logging, consent retention, and disclosure presentation prior to submission authorization.

## 23. Official Priority 1 Sources

- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- EU Cyber Resilience Act, [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- EU Data Act, [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)
- US FTC COPPA Rule, 16 CFR Part 312
- UK Online Safety Act 2023, [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- UK DMCCA 2024, [UK Public General Acts 2024 c. 13](https://www.legislation.gov.uk/ukpga/2024/13/contents)
- India DPDPA 2023, Gazette of India, Act No. 22 of 2023
- US Illinois BIPA, 740 ILCS 14
- California CPRA Regulations, 11 CCR section 7000 et seq.
