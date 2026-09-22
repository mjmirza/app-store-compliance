# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major regulations that bind app developers shipping into the European Union, the United States, the United Kingdom, Australia, Brazil, Canada, India, Singapore, South Korea, Japan, and China. It checks honestly how far this repository carries each regulation, what it mentions in passing, and what remains missing from the codebase, templates, and automated guards.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is evaluated across eight distinct operational compliance categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market, both offline and online. For digital systems and software, the GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook gives a developer no template policy to establish an EU-based Responsible Person or determine product classification criteria under GPSR.
- **Missing Documentation:** Missing developer checklists and instructional guides on how to structure online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:** Automated compliance guards and detection recipes lack rules or regex patterns to scan codebase files for GPSR elements or manufacturer identity blocks.
- **Missing Disclosure:** Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name/trademark, postal address, and electronic address under Article 19.
- **Missing Logging:** No architectural provisions or database schemas exist for logging product safety incidents, recalls, or corrective actions.
- **Missing Testing:** No automated tests exist to verify that online interface elements dynamically display required safety disclosures or manufacturer details based on user location.
- **Missing Evidence:** Lacks physical templates or examples of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:** Lacks an audit trail system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining designation of an EU Responsible Person.
2. Incorporate GPSR metadata requirements into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in references demonstrating compliant product detail pages with safety warnings and contact details.
4. Integrate automated test scripts to verify safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on legal representatives. Mandatory enforcement takes effect on 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window to produce user data is 10 days, with a strict 8-hour emergency timeline for critical cases.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Law Enforcement Request Policy template for handling EU judicial orders and emergency production orders.
- **Missing Documentation:** Lacks operational runbooks specifying step-by-step procedures for fulfilling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:** Backend mock implementations lack automated scripts or API endpoints to securely export, filter, and package user data under time constraints.
- **Missing Disclosure:** Public privacy policies fail to explicitly disclose to EU users that data may be preserved or disclosed to European law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:** Lacks database schemas or logging modules designed to log law enforcement requests, verification statuses, data access, and data releases.
- **Missing Testing:** No integration tests simulate rapid 8-hour emergency retrieval and secure packaging of user data.
- **Missing Evidence:** Lacks sample European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for team training and validation.
- **Missing Audit Trail:** Unalterable audit trail system to record administrative interactions, data extractions, and transmissions during legal requests is absent.

### 2.3 Remediation and Action Plan
1. Implement a Law Enforcement Response Protocol for executing EPOs.
2. Designate an EU establishment or legal representative before 18 August 2026.
3. Build secure backend export scripts for 8-hour emergency window compliance.
4. Establish cryptographic audit logging for incoming legal certificates and extractions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button or function on online interfaces for distance financial services contracts concluded by electronic means.

The statutory withdrawal period is 14 days from contract conclusion. The cancellation path must be direct, clear, and at least as simple as sign-up. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** No template policy covering the 14-day statutory withdrawal right or distinguishing in-scope financial services from general subscriptions.
- **Missing Documentation:** Lacks UI design guidelines specifying placement, size, prominence, and terminology for a compliant withdrawal button.
- **Missing Code:** Front-end user interface templates and billing mocks contain no functional implementation of a withdrawal button or modal sheet.
- **Missing Disclosure:** Subscription registration flows fail to prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining revocation terms.
- **Missing Logging:** Lacks logging mechanisms to capture when a user clicks the withdrawal button, timestamps, cancellation confirmations, and refund triggers.
- **Missing Testing:** Lacks automated UI tests verifying that the withdrawal flow completes self-service without requiring customer support intervention.
- **Missing Evidence:** Lacks templates of withdrawal forms, cancellation receipts, or standardized confirmation receipts for consumer dispute resolution.
- **Missing Audit Trail:** Systematic audit trail tracking historical cancellation/refund rates, interface reviews, and policy updates is absent.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation Policy aligned with Directive (EU) 2023/2673.
2. Build a prominent Withdrawal Button component in account settings templates.
3. Implement cancellation request and refund transaction logging schemas.
4. Add automated UI tests verifying frictionless self-service cancellation.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minors' access to mobile applications, purchases, and updates.

Developers must request age category data (via Apple's Declared Age Range API or Google Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or access major updates. Verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a minor age assurance policy specifying regional detection and minor account restrictions.
- **Missing Documentation:** Lacks developer guides for integrating Apple's Declared Age Range API and Google Play Age Signals API across cross-platform frameworks.
- **Missing Code:** Mock client implementations do not call `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict feature access dynamically.
- **Missing Disclosure:** Onboarding flows fail to display state disclosures explaining that age category is requested for statutory compliance and parental consent is required.
- **Missing Logging:** Lacks backend logging schemas to record parental consent receipt, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw verification documents.
- **Missing Testing:** Lacks automated integration tests verifying that minor accounts are blocked from purchases or major updates without valid consent signals.
- **Missing Evidence:** Lacks sample parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:** Immutable audit trail recording rollout of age-assurance features, consent policy revisions, and immediate data purge execution is missing.

### 4.3 Remediation and Action Plan
1. Create a written Minor Age Assurance Policy detailing state-level compliance and data minimization.
2. Implement cross-platform native hooks for Apple's Declared Age Range API and Google's Play Age Signals API.
3. Add automated database purges for raw age-verification inputs post-verification.
4. Write integration tests blocking minor purchases until parental consent signals are confirmed.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory requirement for AI literacy, taking effect on 2 February 2025. Providers and deployers of AI systems must ensure their staff dealing with AI operation possess a sufficient level of AI literacy.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an internal AI Literacy Policy defining competency thresholds and refresh cadences.
- **Missing Documentation:** Lacks developer documentation explaining organizational AI literacy duties and risk assessment protocols.
- **Missing Code:** N/A for runtime application code, but helper scripts checking literacy log validity in development environments are missing.
- **Missing Disclosure:** Contracts and public materials do not disclose commitment to AI literacy standards under Article 4.
- **Missing Logging:** Centralized training log tracking staff inductions, course completions, and annual refreshers is missing.
- **Missing Testing:** Pre-commit hooks or CI lints checking that contributors have valid literacy records are absent.
- **Missing Evidence:** Lacks sample completed literacy logs, training syllabus templates, or risk evaluation records.
- **Missing Audit Trail:** Lacks historical audit trails documenting annual policy reviews, training module updates, and staff completion histories.

### 5.3 Remediation and Action Plan
1. Draft an internal AI Literacy Policy covering safety, bias, privacy, and risk assessment.
2. Maintain `AI_LITERACY_LOG.md` in the repository to record team training dates.
3. Enforce annual compliance reviews for all contributors touching AI features.
4. Add CI checks verifying that literacy logs are updated annually.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act mandates transparency for AI systems, taking effect on 2 August 2026. Interacting AI systems must inform natural persons that they are interacting with AI, and generative AI outputs (text, audio, image, video) must be marked in a machine-readable, detectable format.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an AI Transparency Policy defining disclosure timing, deepfake notices, and marking standards.
- **Missing Documentation:** Pre-submission checklists lack detailed developer instructions on C2PA metadata injection or synthetic media marking.
- **Missing Code:** Lacks helper utilities or middle-tier classes to embed machine-readable watermarks or metadata into generated media outputs.
- **Missing Disclosure:** Conversational UI templates do not display required immediate disclosures ("You are chatting with an AI assistant") prior to initial interaction.
- **Missing Logging:** Lacks database logging schemas to record that transparency notices were displayed to user sessions.
- **Missing Testing:** Test runners do not scan generated outputs to verify machine-detectable watermarks or synthetic media headers.
- **Missing Evidence:** Lacks independent content moderation reports or proof of metadata preservation in media pipelines.
- **Missing Audit Trail:** Audit trail tracking model changes, vendor audits, and modifications to transparency notices is absent.

### 6.3 Remediation and Action Plan
1. Publish an AI Transparency Policy mandating immediate user disclosure and output marking.
2. Inject clear "interacting with AI" notices into all chat and generation UI templates.
3. Integrate C2PA or cryptographic watermarking utilities into synthetic asset pipelines.
4. Add automated integration tests verifying machine-readable headers on generated outputs.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates core platform services provided by designated gatekeepers (Apple, Google). Mobile application developers in the EU can utilize alternative app marketplaces, web distribution, external purchase links, and alternative payment processors.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a policy for EU distribution channel selection, alternative payment handling, and Core Technology Commission (CTC) fee compliance.
- **Missing Documentation:** Lacks developer runbooks detailing StoreKit External Purchase Link entitlement setup, system disclosure sheet rules, and monthly reporting workflows.
- **Missing Code:** Lacks sample code calling `ExternalPurchaseCustomLink` or handling StoreKit external purchase sheets on iOS.
- **Missing Disclosure:** Payment interfaces lack required system disclosures informing users when transacting with the developer rather than the platform operator.
- **Missing Logging:** Lacks transaction logging modules designed for External Purchase Server API monthly reporting.
- **Missing Testing:** Lacks unit tests verifying that StoreKit IAP and external offer links are not co-mingled on the same EU storefront binary.
- **Missing Evidence:** Lacks sample Attachment 14 ADPLA acceptance records, notarization logs, or alternative marketplace distribution agreements.
- **Missing Audit Trail:** Lacks audit trail tracking fee calculations, monthly transaction reporting history, and entitlement additions.

### 7.3 Remediation and Action Plan
1. Formulate an EU Distribution and DMA Payment Policy.
2. Implement `ExternalPurchaseCustomLink` code helpers in iOS paywall templates.
3. Build monthly transaction aggregation scripts for External Purchase Server API reporting.
4. Add automated CI lints ensuring no IAP and external payment co-mingling exists on EU builds.

---

## 8. EU Digital Services Act (DSA - Trader Status)

### 8.1 Regulatory Overview and Background
Articles 30 and 31 of the EU Digital Services Act (Regulation (EU) 2022/2065) mandate that online app stores verify and display trader contact and identity details for developers distributing apps in the EU. Non-compliance results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an organizational policy for declaring and maintaining DSA Trader status across store accounts.
- **Missing Documentation:** Lacks documentation explaining required trader metadata (address, D-U-N-S, phone, email, payment account) and 2FA verification steps.
- **Missing Code:** Store metadata scripts lack validation for DSA trader fields prior to submission.
- **Missing Disclosure:** In-app legal information fails to display trader contact details or consumer protection disclosures.
- **Missing Logging:** Lacks logs capturing annual verification renewals and store trader status changes.
- **Missing Testing:** Pre-submission scanners do not verify whether DSA trader status is active and verified in store metadata.
- **Missing Evidence:** Lacks sample document verification uploads, D-U-N-S certificates, or trader declaration receipts.
- **Missing Audit Trail:** Lacks historical audit trail tracking changes to declared organizational addresses, phone numbers, and trader status declarations.

### 8.3 Remediation and Action Plan
1. Establish a DSA Compliance Policy requiring verified trader profiles on all EU store accounts.
2. Update `scripts/metadata-audit.py` to flag missing DSA trader declarations.
3. Maintain verified trader contact information in app legal templates.
4. Schedule annual audits of store account trader verification statuses.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025. It mandates accessibility for consumer products and services including e-commerce, banking, e-books, and transport apps distributed in the EU, enforcing the EN 301 549 standard (WCAG 2.1 Level AA plus Chapter 11 for mobile apps).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Accessibility Policy committing to EN 301 549 Chapter 11 compliance for mobile applications.
- **Missing Documentation:** Lacks developer guides mapping EN 301 549 Chapter 11 requirements to native iOS VoiceOver and Android TalkBack APIs.
- **Missing Code:** UI templates lack complete accessibility attributes (`accessibilityLabel`, `accessibilityTraits`, Dynamic Type support, high contrast tokens).
- **Missing Disclosure:** Lacks a published Accessibility Statement template complying with EN 301 549 Annex B/C requirements.
- **Missing Logging:** Lacks accessibility feedback logging modules to capture user-reported accessibility barriers.
- **Missing Testing:** `scripts/accessibility-audit.py` covers basic rules but lacks full automated checks for touch-target dimensions, screen reader focus order, and reduced motion response.
- **Missing Evidence:** Lacks sample VPAT (Voluntary Product Accessibility Template) or EN 301 549 conformance reports.
- **Missing Audit Trail:** Lacks audit trail tracking accessibility remediations, user feedback resolutions, and annual conformance evaluations.

### 9.3 Remediation and Action Plan
1. Adopt an organizational Accessibility Policy referencing EN 301 549 Chapter 11.
2. Publish an in-app and web Accessibility Statement template.
3. Enhance `scripts/accessibility-audit.py` to test contrast, scaling, and VoiceOver/TalkBack attributes automatically.
4. Generate formal VPAT/EN 301 549 compliance evidence reports prior to major releases.

---

## 10. US COPPA & Amended COPPA Rule

### 10.1 Regulatory Overview and Background
The Children's Online Privacy Protection Act (16 CFR Part 312) regulates operators of commercial websites and online services directed to children under 13, or general audience apps with actual knowledge of collecting child data. The FTC Amended COPPA Rule (effective 23 June 2025, compliance mandatory 22 April 2026) expands PII to include biometric identifiers and mandates written retention policies and written information security programs.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a COPPA Compliance Policy covering biometric identifier rules, separate opt-in consent for third-party disclosures, and data retention schedules.
- **Missing Documentation:** Lacks operational manuals for implementing FTC-approved verifiable parental consent (VPC) methods.
- **Missing Code:** Onboarding UI code lacks age-gating logic and separate VPC opt-in modal implementations.
- **Missing Disclosure:** Privacy policies lack explicit COPPA disclosures detailing child data categories, parental rights, and third-party vendor lists.
- **Missing Logging:** Lacks secure logging schemas to record VPC grants, consent revocations, and data deletion requests.
- **Missing Testing:** Lacks unit and integration tests verifying that child user data transmission to third parties is blocked absent VPC.
- **Missing Evidence:** Lacks written Information Security Program documents, annual COPPA risk assessments, or Safe Harbor certificates.
- **Missing Audit Trail:** Immutable audit trail tracking child account data purges, consent revocations, and annual security reviews is missing.

### 10.3 Remediation and Action Plan
1. Formulate an updated COPPA Policy and written Information Security Program.
2. Implement age-gate and Verifiable Parental Consent components in app onboarding templates.
3. Build automated data deletion scripts enforcing COPPA retention limits.
4. Add integration tests verifying zero third-party ad SDK initialization for child accounts.

---

## 11. California Privacy (CCPA/CPRA, CPPA 2026 Regulations, AADC)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended by the CPRA (Cal. Civ. Code section 1798.100 et seq.) and CPPA 2026 Regulations grant rights to California residents, including opt-out of sale/sharing, sensitive data limits, and Global Privacy Control (GPC) signal honor.

Official Citation: California Consumer Privacy Act of 2018 / California Privacy Rights Act of 2020.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a California Consumer Privacy Policy addressing GPC signal processing, "Do Not Sell/Share", and sensitive personal info usage.
- **Missing Documentation:** Lacks developer documentation on handling `Sec-GPC` headers in webviews and native opt-out synchronization.
- **Missing Code:** Webview implementations and native SDK wrappers do not automatically inspect or pass the `Sec-GPC` signal to tag managers or analytics SDKs.
- **Missing Disclosure:** In-app notices at collection lack required California links ("Do Not Sell or Share My Personal Information", "Limit the Use of My Sensitive Personal Information").
- **Missing Logging:** Lacks logging schemas to capture CCPA consumer requests (know, delete, correct, opt-out) and fulfillment statuses.
- **Missing Testing:** Automated tests do not simulate GPC signal headers to verify that ad tracking SDKs are dynamically suppressed.
- **Missing Evidence:** Lacks sample Data Protection Impact Assessments (DPIA) or annual privacy risk assessment records.
- **Missing Audit Trail:** Lacks audit trail tracking consumer request fulfillment within the statutory 45-day window.

### 11.3 Remediation and Action Plan
1. Update Privacy Policy templates with CCPA/CPRA disclosures and GPC support.
2. Implement GPC header parsing and native signal propagation code in client templates.
3. Build consumer request logging and tracking backend schemas.
4. Add automated test cases asserting ad tracker suppression when GPC is active.

---

## 12. Illinois Biometric Information Privacy Act (BIPA) / US Biometric Laws

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14) regulates the collection, capture, purchase, receipt, or storage of biometric identifiers (retina/iris scan, fingerprint, voiceprint, hand/face geometry). It mandates written notice, written release, public retention schedules, and destruction within three years.

Official Citation: Illinois Compiled Statutes 740 ILCS 14/1 et seq.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Biometric Data Information Policy outlining written consent protocols, retention schedules, and permanent destruction rules.
- **Missing Documentation:** Lacks developer guidelines distinguishing on-device biometric auth (LocalAuthentication/BiometricPrompt) from central biometric data capture.
- **Missing Code:** Lacks UI components for displaying BIPA-compliant written notices and obtaining explicit e-signature releases prior to biometric capture.
- **Missing Disclosure:** Privacy disclosures fail to state specific biometric data retention periods and destruction guidelines.
- **Missing Logging:** Lacks secure logging schemas to record biometric release execution, consent timestamps, and scheduled destruction dates.
- **Missing Testing:** Automated tests do not verify that biometric capture functions fail gracefully when written release consent is withheld.
- **Missing Evidence:** Lacks sample written consent release forms or public retention and destruction schedule documents.
- **Missing Audit Trail:** Unalterable audit trail tracking biometric data deletion after three years or upon purpose fulfillment is absent.

### 12.3 Remediation and Action Plan
1. Draft a standalone Biometric Data Retention and Destruction Policy.
2. Build BIPA notice and consent release modal templates for app onboarding.
3. Implement automated cron jobs executing biometric data destruction within retention deadlines.
4. Add unit tests asserting biometric capture blocking prior to explicit consent release.

---

## 13. US Federal / State Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative-option statutes (California, New York, Massachusetts) require auto-renewing subscription services to provide clear disclosures, informed consent, and a simple, frictionless cancellation mechanism at least as easy as sign-up ("click to cancel").

Official Citations: 15 U.S.C. 8401 et seq.; Cal. Bus. & Prof. Code section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Subscription Cancellation Policy requiring online self-service cancellation paths equal in simplicity to onboarding.
- **Missing Documentation:** Lacks developer design guidelines prohibiting dark patterns, phone-call-only cancellation requirements, or multi-step retention traps.
- **Missing Code:** Subscription paywall and account settings templates lack functional self-service cancellation UI components or API hooks for non-IAP web subscriptions.
- **Missing Disclosure:** Checkout screens do not display clear recurring billing terms, charge amounts, renewal dates, and cancellation instructions immediately adjacent to the buy button.
- **Missing Logging:** Lacks database logging schemas capturing subscription cancellation initiation, confirmation timestamps, and effective termination dates.
- **Missing Testing:** End-to-end automated UI tests do not verify that cancellation can be completed in the same number of steps as subscription activation.
- **Missing Evidence:** Lacks sample post-cancellation email receipts, disclosure records, or refund dispute documentation.
- **Missing Audit Trail:** Audit trail tracking historical cancellation rates, interface changes, and subscription retention flow modifications is absent.

### 13.3 Remediation and Action Plan
1. Formulate a Subscription Transparency and Cancellation Policy.
2. Build direct "Cancel Subscription" button components into user account settings templates.
3. Implement cancellation request and receipt generation backend flows.
4. Write UI tests verifying one-click or direct cancellation execution without support agent contact.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code (Children's Code) mandate age assurance and high-privacy defaults (geolocation off, profiling off, data minimisation) for services likely to be accessed by children under 18 in the UK.

Official Citations: UK Online Safety Act 2023 (c. 50); ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Child Safety and Age-Appropriate Design Policy.
- **Missing Documentation:** Lacks operational guides for conducting mandatory Data Protection Impact Assessments (DPIA) under the Children's Code.
- **Missing Code:** App templates do not default geolocation and profiling toggles to "OFF" for UK child accounts.
- **Missing Disclosure:** Public disclosures do not provide child-friendly privacy notices tailored to different age tiers.
- **Missing Logging:** Lacks logs capturing age assurance verification outcomes and age-appropriate default settings initialization.
- **Missing Testing:** Integration tests do not verify that geolocation and profiling services remain inactive for under-18 UK users.
- **Missing Evidence:** Lacks completed DPIA documentation, Ofcom compliance filings, or age assurance method certifications.
- **Missing Audit Trail:** Audit trail recording risk assessment updates, feature safety reviews, and child safety policy changes is missing.

### 14.3 Remediation and Action Plan
1. Draft a UK Children's Code Policy and DPIA template.
2. Implement child-account defaults (geolocation off, profiling off) in app config modules.
3. Write automated tests validating privacy-by-default flags for UK child user profiles.
4. Establish an audit trail repository for annual DPIA reviews.

---

## 15. Australia Online Safety Act & Privacy Act

### 15.1 Regulatory Overview and Background
The Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 and Privacy Act 1988 require age restriction (under-16 account blocks) for social media platforms, automated decision-making privacy disclosures, and age-assurance data destruction.

Official Citations: Online Safety Amendment (Social Media Minimum Age) Act 2024; Privacy Act 1988 (Cth).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Age Restriction and Privacy Policy covering social media minimum age rules and automated decision-making disclosures.
- **Missing Documentation:** Lacks developer runbooks detailing age-assurance data ringfencing and immediate destruction protocols.
- **Missing Code:** Lacks age restriction enforcement modules blocking under-16 account creation on social networking app templates.
- **Missing Disclosure:** Privacy policies fail to disclose automated decision-making processing under APP 1.7-1.9.
- **Missing Logging:** Lacks logging schemas recording age-assurance execution and verified age-data destruction timestamps.
- **Missing Testing:** Automated tests do not verify that age-assurance raw inputs are completely deleted from memory and disk post-verification.
- **Missing Evidence:** Lacks sample eSafety compliance reports, risk assessments, or proof of age-data deletion.
- **Missing Audit Trail:** Immutable audit trail tracking age-verification data destruction and policy updates is absent.

### 15.3 Remediation and Action Plan
1. Develop an Australian Regulatory Compliance Policy covering social media age gates.
2. Implement automated age-assurance data purge routines in backend services.
3. Update privacy policy templates with automated decision-making disclosures.
4. Build automated test suites verifying under-16 account rejection on Australian storefronts.

---

## 16. Brazil Digital ECA (Law 15,211/2025) & LGPD

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025 and Decreto 12,880/2026) mandates age verification (document check, facial estimation, CPF check) and prohibits simple self-declaration checkboxes for minor access, overseen by ANPD under the LGPD.

Official Citations: Law 15,211/2025; Decreto n. 12.880 of 18 March 2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazil Digital ECA Minor Protection Policy outlining approved age-verification mechanisms and parental consent.
- **Missing Documentation:** Lacks guides for integrating Google Play Age Signals API and Apple Declared Age Range API for Brazilian storefronts.
- **Missing Code:** App onboarding templates lack document check or CPF verification interface components, relying on banned checkboxes.
- **Missing Disclosure:** Onboarding interfaces lack mandatory disclosures informing parents of age-verification processing under Law 15,211/2025.
- **Missing Logging:** Lacks secure logs capturing ANPD-approved age-verification signals and parental authorization receipts.
- **Missing Testing:** CI tests do not assert that simple self-declaration checkboxes are blocked for Brazilian user registration.
- **Missing Evidence:** Lacks sample ANPD compliance documentation, age-assurance method certifications, or guardian authorization logs.
- **Missing Audit Trail:** Audit trail tracking age-verification method updates and minor data handling is missing.

### 16.3 Remediation and Action Plan
1. Draft a Brazil Digital ECA Compliance Policy.
2. Replace self-declaration checkboxes with native age signal API integrations or ANPD-compliant verification.
3. Build logging schemas for parental consent receipts and verification signals.
4. Add automated test cases asserting rejection of unverified minor accounts in Brazil.

---

## 17. India Digital Personal Data Protection Act (DPDPA) & DPDP Rules 2025

### 17.1 Regulatory Overview and Background
India's Digital Personal Data Protection Act 2023 and DPDP Rules 2025 mandate verifiable parental consent through government-backed systems (such as DigiLocker) for users under 18, and ban behavioral tracking and targeted ads directed at children.

Official Citations: Digital Personal Data Protection Act 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India DPDPA Policy covering verifiable parental consent and child ad tracking prohibitions.
- **Missing Documentation:** Lacks developer documentation for integrating registered Consent Managers and DigiLocker VPC workflows.
- **Missing Code:** Client SDK wrappers do not disable behavioral tracking and targeted ad SDKs for Indian users under 18.
- **Missing Disclosure:** Itemized consent notices in English and scheduled Indian languages (22 languages) are missing from onboarding templates.
- **Missing Logging:** Lacks logging schemas to record Consent Manager receipts, consent withdrawals, and parental verification tokens.
- **Missing Testing:** Automated tests do not verify that ad tracking remains disabled for under-18 Indian profiles.
- **Missing Evidence:** Lacks sample Data Protection Officer (DPO) designation records, Consent Manager integration certificates, or security audit reports.
- **Missing Audit Trail:** Unalterable audit trail tracking consent grants, modifications, and withdrawals is absent.

### 17.3 Remediation and Action Plan
1. Establish an India DPDPA Compliance Policy and Consent Manager protocol.
2. Build itemized consent notice components in multi-language templates.
3. Implement ad-tracking suppression logic for under-18 Indian user profiles.
4. Write integration tests verifying DigiLocker VPC token validation before minor account activation.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA App Distribution Safety Code

### 18.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require age assurance to screen and stop users under 18 from downloading age-inappropriate apps, alongside immediate age-data destruction.

Official Citations: Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore PDPA and IMDA Online Safety Policy covering Data Protection Officer (DPO) contact publishing and age assurance.
- **Missing Documentation:** Lacks developer runbooks detailing 3-day breach notification workflows to PDPC and immediate age-data purge requirements.
- **Missing Code:** Lacks age-screening modules restricting access to 18-plus content on Singapore storefronts.
- **Missing Disclosure:** Privacy policies lack explicit DPO contact details and PDPC breach notification procedures.
- **Missing Logging:** Lacks logging schemas to record age-screening executions and mandatory age-data destruction logs.
- **Missing Testing:** Integration tests do not verify that age-assurance data is completely deleted post-screening in Singapore flows.
- **Missing Evidence:** Lacks sample DPO appointment documentation, PDPC breach report templates, or IMDA compliance filings.
- **Missing Audit Trail:** Audit trail tracking DPO reviews, breach response drills, and age-data purges is missing.

### 18.3 Remediation and Action Plan
1. Formulate a Singapore PDPA Compliance Policy and DPO declaration.
2. Implement 18-plus age gating for Singapore storefront builds.
3. Build 3-day breach notification workflow templates.
4. Add automated unit tests verifying zero age-data retention after verification.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendments

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment support (`com.apple.developer.storekit.external-purchase` for KR), and PIPA amendments impose CEO/board-level privacy accountability and CPO requirements.

Official Citations: Telecommunications Business Act Article 22-9; Personal Information Protection Act (Act No. 21445).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea Payment and Privacy Accountability Policy.
- **Missing Documentation:** Lacks developer manuals for configuring Korea-specific StoreKit external purchase entitlements, approved local gateways (KCP, Toss, Inicis, NICE), and monthly 26% fee reporting.
- **Missing Code:** App templates lack South Korea alternative payment modal sheet implementations and local payment gateway hooks.
- **Missing Disclosure:** Checkout screens lack mandatory Korean external payment notices informing users of platform protection waivers.
- **Missing Logging:** Lacks transaction logging modules designed for monthly South Korea alternative payment fee reporting within 15 days.
- **Missing Testing:** Automated tests do not verify that Korean alternative billing flows display required modal sheets without co-mingling standard IAP.
- **Missing Evidence:** Lacks sample CPO board approval records, KCC compliance filings, or payment gateway agreement copies.
- **Missing Audit Trail:** Audit trail tracking monthly fee reporting history, CPO designations, and PIPA compliance audits is missing.

### 19.3 Remediation Act Plan
1. Adopt a South Korea Payment and PIPA Compliance Policy.
2. Implement South Korea external payment modal sheet components (`SKExternalPurchase = "KR"`).
3. Build monthly transaction aggregation scripts for South Korea fee reporting.
4. Add CI checks asserting Korea-only binary isolation for alternative payment builds.

---

## 20. China Mobile App Filing (MIIT) & PIPL & CAC Minor Protection Measures

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension) through a local Chinese entity. CAC measures (including CAC Order No. 21 for AI anthropomorphic services) require automatic minors mode, real-name verification, and Banhao licensing for games.

Official Citations: MIIT Mobile App Filing Notice (2023); Personal Information Protection Law (PIPL); CAC Order No. 21.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China App Filing and PIPL Compliance Policy.
- **Missing Documentation:** Lacks operational guides for MIIT filing submission, local Chinese entity partnership, and CAC AI service registration.
- **Missing Code:** App templates lack real-name identity verification components, automatic "Minors Mode" triggers, and CAC-compliant AI companion restrictions.
- **Missing Disclosure:** In-app legal notices lack MIIT filing number displays in app settings/about pages and PIPL cross-border transfer disclosures.
- **Missing Logging:** Lacks secure logging schemas to capture real-name verification statuses and minor usage duration limits.
- **Missing Testing:** Integration tests do not verify that minor accounts in China are restricted from virtual companion AI features and late-night usage.
- **Missing Evidence:** Lacks sample MIIT App Filing certificates, Banhao game licenses, or CAC AI service security assessment filings.
- **Missing Audit Trail:** Unalterable audit trail tracking real-name verification audits, minor mode switching events, and PIPL compliance reviews is missing.

### 20.3 Remediation and Action Plan
1. Formulate a China Market Regulatory Compliance Policy.
2. Implement MIIT filing number display components in app settings UI templates.
3. Build real-name verification and Minors Mode toggles into client templates.
4. Add automated test cases verifying minor AI companion feature blocks on China storefronts.

---

## 21. Consolidated Gap Classification Matrix

This matrix summarizes the compliance status across all twenty audited global and regional regulatory frameworks. "Covered" indicates full policy, code, and test coverage; "Partial" indicates regulation is named with dated citations but lacks full implementation templates; "Missing" indicates complete absence from automated guards, codebase, or templates.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act**| Partial | Covered | Partial | Missing | Missing | Partial | Missing | Missing |
| **10. US COPPA / Amended Rule**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California Privacy (CCPA)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / CAC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

The playbook provides exceptional coverage of app store rejection rules and platform submission guidelines. However, for legal compliance post-release, significant gaps remain across code implementation, logging, automated testing, evidence collection, and audit trails.

### Operational Remediation Roadmap:
1. **Immediate (Phase 1):** Add EU GPSR detection rules to `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh`.
2. **Short-Term (Phase 2):** Develop code templates and UI components for EU Withdrawal Button, EU AI Act Article 50 disclosures, and California GPC header handling.
3. **Mid-Term (Phase 3):** Build logging schemas and automated export scripts for EU e-Evidence 8-hour emergency responses, COPPA parental consent, and South Korea/EU DMA monthly fee reporting.
4. **Long-Term (Phase 4):** Implement automated end-to-end integration tests verifying dynamic age gating, ad-tracking suppression, and self-service subscription cancellation across all supported jurisdictions.

Re-evaluate this report quarterly against EUR-Lex, Federal Register, and primary national legislative Gazettes.

---

## 23. Official Primary Sources

Every regulation cited in this report, anchored to its official Primary (Priority 1) source:

- **EU GPSR:** [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **EU e-Evidence Regulation:** [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- **EU e-Evidence Directive:** [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- **EU Distance Marketing of Financial Services:** [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- **EU AI Act:** [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **EU Digital Markets Act:** [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- **EU Digital Services Act:** [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- **European Accessibility Act:** [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- **US COPPA Rule:** [16 CFR Part 312 (Federal Register 90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **US Utah SB 142:** [Utah Legislature SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html)
- **US Texas SB 2420:** [Texas Legislature SB 2420](https://capitol.texas.gov/)
- **California Privacy (CCPA/CPRA):** [California AG Privacy](https://oag.ca.gov/privacy/ccpa)
- **Illinois BIPA:** [740 ILCS 14/](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- **UK Online Safety Act 2023:** [UK Legislation OSA 2023](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- **UK ICO Children's Code:** [ICO Children's Code Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- **Australia Social Media Minimum Age Act:** [Australia Federal Register of Legislation](https://www.legislation.gov.au/)
- **Brazil Digital ECA (Decreto 12,880):** [Planalto Decreto 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- **India DPDP Rules 2025:** [Ministry of Electronics and Information Technology](https://www.meity.gov.in/)
- **Singapore PDPA:** [Personal Data Protection Commission Singapore](https://www.pdpc.gov.sg/)
- **South Korea PIPA:** [Personal Information Protection Commission Korea](https://www.pipc.go.kr/)
- **China CAC Order No. 21:** [Cyberspace Administration of China](https://www.cac.gov.cn/)
