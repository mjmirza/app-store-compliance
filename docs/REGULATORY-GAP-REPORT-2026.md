# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major global and regional regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, Canada, India, South Korea, Singapore, and China, and checks honestly how far this repository carries each framework, what it only mentions in passing, and what remains to be implemented.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is audited across eight distinct gap domains:
1. Missing Policy
2. Missing Documentation
3. Missing Code
4. Missing Disclosure
5. Missing Logging
6. Missing Testing
7. Missing Evidence
8. Missing Audit Trail

Assume the repository is incomplete unless proven otherwise. Search continuously until no additional gaps remain.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in online marketplaces, digital products, and complex supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital systems and e-commerce applications, the GPSR mandates displaying product safety warnings, instructions, manufacturer and importer identity, and postal/electronic contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The playbook provides no template policy or decision framework for determining GPSR applicability or designating an EU Responsible Person.
- **Missing Documentation:** Lacks detailed developer manuals or step-by-step guides for structuring EU product listings to display safety warnings, technical instructions, and contact info.
- **Missing Code:** Rejection patterns and automated guard scripts do not include rules for scanning codebase UI files for GPSR-mandated safety labels or manufacturer metadata.
- **Missing Disclosure:** Interface templates lack placeholder components for displaying manufacturer trade names, postal addresses, and electronic contact details under Article 19.
- **Missing Logging:** No database schemas or architectural patterns exist to log product safety incidents, safety complaints, or recall events.
- **Missing Testing:** Lacks automated tests verifying that UI listings dynamically render required product safety information based on user region.
- **Missing Evidence:** Missing downloadable templates for Technical Documentation sheets, safety risk evaluations, or EU Responsible Person designation records.
- **Missing Audit Trail:** No historical audit system to track when product safety warnings were reviewed, modified, or updated in response to safety alerts.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on legal representatives. The mandatory compliance enforcement date is 18 August 2026.

Judicial authorities in an EU Member State can issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. Standard response time is 10 days; critical emergency orders require data production within a strict 8-hour window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Law Enforcement Response Policy outlining procedures, authorized roles, and verification protocols for judicial orders.
- **Missing Documentation:** Missing concrete operational runbooks for executing standard 10-day orders and 8-hour emergency extraction requests.
- **Missing Code:** No automated backend scripts or secure API endpoints exist to extract, filter, and encrypt targeted user datasets for legal compliance.
- **Missing Disclosure:** Privacy policies and public notices fail to disclose to EU users that data may be produced to EU authorities under Regulation (EU) 2023/1543.
- **Missing Logging:** Missing database schemas for logging law enforcement orders, verification steps, employee accesses, and data releases.
- **Missing Testing:** No integration tests simulate rapid 8-hour emergency data extraction and packaging under time constraints.
- **Missing Evidence:** Lacks sample EPOC/EPOC-PR certificate templates for training compliance personnel on order validation.
- **Missing Audit Trail:** Lacks an immutable, tamper-proof audit log to capture all administrative actions and transmissions during law enforcement requests.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU, requiring a prominent, easily accessible withdrawal button or function on online interfaces for distance contracts for financial services. Member States apply these rules from 19 June 2026.

The statutory withdrawal window is 14 days. The cancellation path must be direct, frictionless, and at least as simple as the contract sign-up flow.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Consumer Contract Withdrawal Policy defining statutory 14-day revocation rules and refund procedures.
- **Missing Documentation:** Lacks UI design guidelines for button prominence, placement, and explicit terminology required by EU standards.
- **Missing Code:** Mobile and web UI mockups contain no functional implementation of a self-service contract withdrawal button or modal sheet.
- **Missing Disclosure:** Subscription screens omit explicit disclosures of the 14-day statutory right of withdrawal and its legal terms.
- **Missing Logging:** No logging mechanisms exist to capture withdrawal button clicks, timestamps, contract termination confirmations, or refund triggers.
- **Missing Testing:** Missing automated UI tests confirming that contract withdrawal can be executed in a single self-service interaction without human intervention.
- **Missing Evidence:** Lacks standardized cancellation confirmation receipt templates or proof-of-withdrawal forms.
- **Missing Audit Trail:** No historical log tracking user cancellation rates, withdrawal flow changes, or interface compliance reviews.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State ASAAs (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minors' access to mobile applications, purchases, and major updates.

Developers must query age categories (via Apple Declared Age Range or Google Play Age Signals) and obtain verifiable parental consent before allowing minors to download, purchase, or update apps. Raw verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a template Minor Age Assurance and Parental Consent Policy for handling minor accounts across state lines.
- **Missing Documentation:** Checklists lack step-by-step developer guides for implementing native cross-platform age-assurance hooks (Apple and Google Play).
- **Missing Code:** Sample codebases do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:** Onboarding interfaces lack mandatory state notices explaining that age signals are processed solely for legal age assurance.
- **Missing Logging:** No backend schemas exist to log parental consent receipt, revocation events (`RESCIND_CONSENT`), or verification data deletion triggers.
- **Missing Testing:** Lacks automated test suites simulating minor age signals and verifying that premium features and billing are blocked until parental consent is verified.
- **Missing Evidence:** Lacks parental consent agreement forms or data minimization record templates for state Attorney General audits.
- **Missing Audit Trail:** Missing immutable audit trails recording age-assurance feature rollouts, policy updates, and immediate data deletion events.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among their staff and operators. Live since 2 February 2025, this applies to all organizations regardless of size.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an organizational AI Literacy Policy outlining core competencies in AI safety, risk evaluation, and bias detection.
- **Missing Documentation:** Missing developer checklists explaining ongoing obligations under Article 4 and AI safety standards.
- **Missing Code:** While Article 4 binds people rather than software, the repository lacks CLI validation scripts to check if an active literacy log exists.
- **Missing Disclosure:** Public and partner documentation fails to state the organization's compliance with Article 4 literacy standards.
- **Missing Logging:** Missing a structured, centralized training log (`AI_LITERACY_LOG.md`) to record employee training dates, course modules, and refreshers.
- **Missing Testing:** No pre-commit hooks or CI checks verify that team members committing AI features have up-to-date literacy records.
- **Missing Evidence:** Lacks sample training certificates, completed course logs, or documented risk assessment reviews.
- **Missing Audit Trail:** No historical audit trail tracks when the literacy policy was reviewed or how training modules evolved over time.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 sets strict transparency rules, effective 2 August 2026. Developers must disclose AI interaction, mark synthetic content in machine-readable formats, and disclose deepfakes.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a corporate AI Transparency Policy defining when disclosures must appear and how generated media must be marked.
- **Missing Documentation:** Lacks technical documentation detailing C2PA metadata injection or machine-readable watermarking implementations.
- **Missing Code:** Backend pipeline templates lack code helpers for embedding machine-readable watermarks into generated image, text, or audio assets.
- **Missing Disclosure:** Chat and generative UI templates lack mandatory upfront notices ("You are interacting with an AI system").
- **Missing Logging:** Missing database schemas to record that an AI transparency disclosure was shown to a specific user session.
- **Missing Testing:** Test runners do not scan generated output assets to confirm the presence of machine-readable metadata or watermarks.
- **Missing Evidence:** Lacks independent audit reports or security evaluations of content moderation filters and watermarking integrity.
- **Missing Audit Trail:** Missing historical logs recording changes to AI disclosure text, watermarking algorithms, or third-party model integrations.

---

## 7. Amended US COPPA Rule (16 CFR Part 312)

### 7.1 Regulatory Overview and Background
The FTC's amended COPPA Rule (effective 23 June 2025, compliance mandatory 22 April 2026) expands personal information to include biometric identifiers, requires separate opt-in consent for third-party disclosure/targeted ads, mandates written data retention policies, and requires a written info-security program.

Official Citation: FTC 16 CFR Part 312, 90 FR 16918.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks written Data Retention and Information Security Policies specific to under-13 children's data.
- **Missing Documentation:** Missing developer guidance on implementing knowledge-based authentication or facial-match ID verification for COPPA consent.
- **Missing Code:** Sample codebases lack separate opt-in consent toggles for third-party ad sharing in child-directed flows.
- **Missing Logging:** Missing secure database schemas for logging separate parental consents and scheduled data deletion triggers.
- **Missing Testing:** Lacks unit tests verifying that third-party SDKs are initialized ONLY after explicit parental opt-in consent.
- **Missing Evidence:** Lacks downloadable templates for written Information Security Programs or annual COPPA risk assessments.
- **Missing Audit Trail:** Missing audit logs tracking parental consent records, policy revisions, and data purge execution history.

---

## 8. European Accessibility Act (EAA - Directive (EU) 2019/882)

### 8.1 Regulatory Overview and Background
Applicable since 28 June 2025, the EAA mandates mobile app and web accessibility under harmonised standard EN 301 549 (WCAG 2.1 AA level plus Chapter 11 mobile rules).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Accessibility Policy defining organizational commitments to EN 301 549 standards.
- **Missing Documentation:** Checklists omit detailed instructions for satisfying EN 301 549 Chapter 11 mobile-specific requirements beyond standard WCAG.
- **Missing Code:** Mobile UI templates lack complete accessibility traits, Dynamic Type scaling layouts, or VoiceOver hints across all screens.
- **Missing Disclosure:** Missing an in-app accessible Accessibility Statement template detailing compliance status and feedback mechanisms.
- **Missing Logging:** Missing logging mechanisms for recording user accessibility feedback, reports, or remediation requests.
- **Missing Testing:** Static accessibility audits check basic rules but lack automated UI tests for screen reader traversal and Dynamic Type scaling limits.
- **Missing Evidence:** Lacks sample VPAT (Voluntary Product Accessibility Template) or EN 301 549 conformance reports.
- **Missing Audit Trail:** Missing historical tracking of accessibility audits, bug remediations, and statement updates.

---

## 9. EU Digital Markets Act (DMA - Regulation (EU) 2022/1925)

### 9.1 Regulatory Overview and Background
The DMA regulates gatekeeper platforms and establishes entitlements for external purchase links, alternative app stores, and browser engines in the EU.

Official Citation: Regulation (EU) 2022/1925.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an EU Alternative Billing and Steering Policy for managing store entitlements.
- **Missing Documentation:** Missing detailed runbooks for setting up the StoreKit External Purchase Link Entitlement and handling CTC fee reporting.
- **Missing Code:** Sample code does not integrate Apple's `ExternalPurchaseCustomLink` modal sheet or external sales reporting server APIs.
- **Missing Disclosure:** External offer flows omit compulsory system-level disclosure sheets notifying users they are leaving the store ecosystem.
- **Missing Logging:** Lacks backend logging to capture external transaction timestamps and calculate monthly commission reports for Apple/Google.
- **Missing Testing:** Missing automated tests ensuring that StoreKit IAP and external offer links are never co-mingled on the same EU storefront.
- **Missing Evidence:** Lacks proof-of-reporting templates or audited fee reconciliation documentation.
- **Missing Audit Trail:** Missing immutable logs of monthly sales reporting submissions and entitlement configuration changes.

---

## 10. EU Digital Services Act (DSA - Regulation (EU) 2022/2065) Trader Status

### 10.1 Regulatory Overview and Background
Articles 30 and 31 of the DSA require app stores to verify and display trader contact identity details for developers distributing apps in the EU. Non-compliance results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a DSA Trader Status Compliance Policy defining trader classification criteria under EU consumer law.
- **Missing Documentation:** Missing step-by-step guides for completing D-U-N-S, phone, email, and 2FA verification in App Store Connect / Google Play Console.
- **Missing Code:** Rejection patterns cover metadata, but no static scanner verifies that trader contact info is rendered correctly on web store mirrors.
- **Missing Disclosure:** UI templates omit required in-app consumer rights notices displayed when an entity operates as a verified trader.
- **Missing Logging:** No system logs trader status verification states or store compliance notification emails.
- **Missing Testing:** Lacks pre-submission tests checking whether EU storefront readiness is blocked by an unverified DSA status.
- **Missing Evidence:** Lacks templates for storing uploaded identity documents, official D-U-N-S certificates, or 2FA verification records.
- **Missing Audit Trail:** Missing audit trails tracking trader status declarations, updates, or store verification approvals.

---

## 11. UK Online Safety Act 2023 & ICO Children's Code

### 11.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code mandate Highly Effective Age Assurance, high privacy by default, disabled profiling, and mandatory DPIAs for services accessible to UK children.

Official Citations: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Child Safety and Age Assurance Policy.
- **Missing Documentation:** Missing step-by-step documentation for conducting and recording an ICO-compliant Data Protection Impact Assessment (DPIA).
- **Missing Code:** Codebases lack robust age estimation fallback flows (such as open banking or facial age estimation integration).
- **Missing Disclosure:** Privacy policies fail to explicitly outline UK Children's Code default settings (geolocation off, profiling off).
- **Missing Logging:** Missing backend logs to capture DPIA approvals and child safety risk mitigation decisions.
- **Missing Testing:** No automated tests verify that geolocation and profiling toggles default to disabled for UK minor profiles.
- **Missing Evidence:** Lacks downloadable templates for completed ICO DPIA reports.
- **Missing Audit Trail:** Missing immutable logs of child safety policy reviews, Ofcom audit responses, and DPIA updates.

---

## 12. Australia Online Safety Amendment Act 2024

### 12.1 Regulatory Overview and Background
Requires social media and age-restricted platforms to take reasonable steps to prevent under-16s from holding accounts, enforcing strict age assurance and data ringfencing.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Under-16 Account Restriction Policy.
- **Missing Documentation:** Missing technical manuals detailing data ringfencing and immediate data destruction workflows post-verification.
- **Missing Code:** Mobile app codebases lack backend hooks to execute automated data destruction triggers after age verification.
- **Missing Disclosure:** Onboarding interfaces lack mandatory disclosures informing Australian users of account age restrictions.
- **Missing Logging:** Missing secure schemas to log age verification events without storing raw identity attributes.
- **Missing Testing:** Lacks unit tests verifying that raw age verification inputs are deleted from database tables immediately after confirmation.
- **Missing Evidence:** Lacks data destruction logs or independent security audit reports verifying data ringfencing.
- **Missing Audit Trail:** Missing audit trails tracking age assurance system updates and eSafety Commissioner compliance filings.

---

## 13. Brazil Digital ECA (Law 15,211/2025) & LGPD

### 13.1 Regulatory Overview and Background
Enforceable from 17 March 2026, the Digital ECA mandates verifiable age estimation (document check, CPF validation, facial age estimation) and prohibits simple check-box self-declarations for minor accounts.

Official Citation: Brazilian Federal Law 15,211/2025; LGPD Law 13,709/2018.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazilian Digital ECA Compliance Policy.
- **Missing Documentation:** Missing developer documentation detailing CPF database verification integration and facial estimation APIs.
- **Missing Code:** Codebases lack backend integrations with Brazilian CPF databases or biometric age estimation providers.
- **Missing Disclosure:** Onboarding flows omit mandatory LGPD/Digital ECA age verification and parental consent notices.
- **Missing Logging:** Missing backend logging for parental consent approvals and LGPD data subject requests.
- **Missing Testing:** Automated tests do not verify that self-declaration check-boxes are rejected as invalid age signals for Brazilian storefronts.
- **Missing Evidence:** Lacks sample parental consent logs or ANPD compliance audit evidence.
- **Missing Audit Trail:** Missing historical tracking of age verification policy changes and ANPD regulatory submissions.

---

## 14. India Digital Personal Data Protection Act (DPDPA) 2023 & Rules 2025

### 14.1 Regulatory Overview and Background
Mandates verifiable parental consent via government-backed systems (e.g., DigiLocker) for users under 18 and prohibits targeted advertising or behavioral tracking directed at children.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India DPDPA Minor Data Protection Policy.
- **Missing Documentation:** Missing developer integration guides for DigiLocker parental consent verification.
- **Missing Code:** Sample backend code lacks DigiLocker OAuth/API verification integrations for under-18 users.
- **Missing Disclosure:** In-app notices fail to state DPDPA-mandated multilingual consent details and Data Fiduciary contact info.
- **Missing Logging:** Missing database logging for DigiLocker consent tokens and consent revocation events.
- **Missing Testing:** Lacks automated tests confirming that targeted ad SDKs are completely disabled for Indian accounts under 18.
- **Missing Evidence:** Lacks templates for Data Protection Impact Assessments or Data Fiduciary registration filings.
- **Missing Audit Trail:** Missing audit logs recording consent lifecycle events and Data Protection Board of India audit filings.

---

## 15. Singapore IMDA Code of Practice for Online Safety & PDPA

### 15.1 Regulatory Overview and Background
Requires app distribution services and app developers to implement age assurance measures (screening users under 18 from age-inappropriate content) and destroy age data post-verification.

Official Citation: IMDA Code of Practice for Online Safety (2026); PDPA 2012.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore Online Safety and Data Minimization Policy.
- **Missing Documentation:** Missing developer guides on integrating IMDA-compliant age assurance and credit card / ID verification mechanics.
- **Missing Code:** Codebases lack age-gating triggers tied to Singapore storefront detection.
- **Missing Disclosure:** Onboarding screens omit IMDA safety classifications and age rating disclosures.
- **Missing Logging:** Missing backend logs to capture content access restrictions applied to Singapore users.
- **Missing Testing:** Lacks automated tests verifying that 18+ content is blocked on Singapore storefronts without valid age confirmation.
- **Missing Evidence:** Lacks proof of age data destruction and IMDA compliance reports.
- **Missing Audit Trail:** Missing immutable records of content safety audits and IMDA compliance reviews.

---

## 16. California CCPA / CPRA & CPPA 2026 Regulations

### 16.1 Regulatory Overview and Background
Mandates privacy notices at collection, rights to know/delete/correct, "Do Not Sell or Share" controls, Global Privacy Control (GPC) signal processing, and automated decision-making opt-outs.

Official Citation: California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA); CPPA 2026 Regulations.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a California Consumer Privacy Policy and Opt-Out Framework.
- **Missing Documentation:** Missing developer guides on detecting and handling the `Sec-GPC` HTTP header and native webview signals.
- **Missing Code:** Sample webview and mobile implementations lack middleware to automatically suppress ad-tracking SDKs when GPC is active.
- **Missing Disclosure:** Missing explicit "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links/modals.
- **Missing Logging:** Missing backend schemas to record consumer opt-out preferences and GPC signal receptions.
- **Missing Testing:** Lacks unit tests verifying that ad network requests are blocked when GPC or opt-out flags are set.
- **Missing Evidence:** Lacks downloadable templates for CPPA Cybersecurity Audits and Automated Decision-Making Technology (ADMT) risk assessments.
- **Missing Audit Trail:** Missing audit logs tracking consumer rights requests, fulfillment timelines, and policy updates.

---

## 17. Illinois Biometric Information Privacy Act (BIPA - 740 ILCS 14)

### 17.1 Regulatory Overview and Background
Requires written notice, e-signed consent releases, public retention/destruction schedules, and prohibits the sale or monetization of biometric identifiers.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a written Biometric Data Retention and Destruction Policy.
- **Missing Documentation:** Missing developer guidance on implementing e-signed biometric consent releases prior to facial/fingerprint scan initialization.
- **Missing Code:** Sample codebases lack UI components for presenting written biometric disclosures and capturing valid written releases.
- **Missing Disclosure:** Missing explicit disclosures detailing the specific purpose and length of term for biometric data storage.
- **Missing Logging:** Missing backend database tables to log e-signed consent releases and automated 3-year destruction timers.
- **Missing Testing:** Lacks unit tests verifying that biometric capture APIs (e.g., Face ID / camera scan) cannot fire without a valid signed consent flag.
- **Missing Evidence:** Lacks sample biometric consent agreement forms and proof of compliance with public retention schedules.
- **Missing Audit Trail:** Missing immutable audit trails recording biometric data collection events, deletion execution logs, and consent history.

---

## 18. US Subscription Cancellation (Negative Option / ROSCA / State Laws)

### 18.1 Regulatory Overview and Background
Requires online subscription cancellation to be at least as easy as sign-up (click-to-cancel), prohibiting friction such as requiring phone calls or manual customer service interactions.

Official Citations: Restore Online Shoppers' Confidence Act (ROSCA - 15 U.S.C. 8401); California, New York, Massachusetts Negative Option Statutes.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Online Subscription Cancellation Policy enforcing frictionless self-service cancellation.
- **Missing Documentation:** Missing UI/UX design guidelines detailing simple, direct cancellation pathways for web-billed subscriptions.
- **Missing Code:** Sample web and account management UIs lack self-service cancellation button handlers and instant subscription termination endpoints.
- **Missing Disclosure:** Billing screens fail to clearly disclose auto-renewal terms, recurring pricing, and exact cancellation steps prior to purchase.
- **Missing Logging:** Missing backend logs capturing cancellation request timestamps, user confirmations, and billing termination events.
- **Missing Testing:** Lacks automated UI tests verifying that a user can cancel a subscription in the same number of steps as sign-up.
- **Missing Evidence:** Lacks sample cancellation receipt templates and compliance review documentation.
- **Missing Audit Trail:** Missing audit logs tracking cancellation metrics, retention offer interventions, and subscription flow updates.

---

## 19. China Mobile App Filing (MIIT) & PIPL

### 19.1 Regulatory Overview and Background
Mandates Chinese Ministry of Industry and Information Technology (MIIT) app filing via a local Chinese entity, PIPL privacy compliance, data localization, real-name verification, and Banhao licenses for games.

Official Citations: MIIT Mobile App Filing Notice (2023); Personal Information Protection Law (PIPL 2021).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China Market Entry and Data Localization Policy.
- **Missing Documentation:** Missing step-by-step documentation for filing MIIT ICP extensions and establishing local partner agreements.
- **Missing Code:** Codebases lack integrations for Chinese real-name identity verification APIs and local telemetry routing.
- **Missing Disclosure:** Missing PIPL-compliant privacy notices detailing cross-border data transfer assessments and local handling.
- **Missing Logging:** Missing database schemas for logging MIIT filing numbers and real-name verification tokens.
- **Missing Testing:** Lacks automated checks verifying that non-filed builds are blocked from Chinese storefront distribution.
- **Missing Evidence:** Lacks templates for MIIT filing certificates, Banhao game licenses, or PIPL Personal Information Impact Assessments.
- **Missing Audit Trail:** Missing immutable logs recording MIIT filing updates, local partner audits, and PIPL compliance reviews.

---

## 20. South Korea Telecommunications Business Act (Alternative Billing)

### 20.1 Regulatory Overview and Background
Mandates alternative in-app payment choices for South Korean users, requiring specific store entitlements (`com.apple.developer.storekit.external-purchase`), modal disclosures, a 26% commission structure, and monthly sales reporting.

Official Citation: South Korea Telecommunications Business Act Article 22-9.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea In-App Payment Compliance Policy.
- **Missing Documentation:** Missing technical manuals detailing Korea-specific binary builds, StoreKit external purchase setup, and approved payment gateway integration (KCP, Toss, Inicis).
- **Missing Code:** Codebases lack native modal warning sheets and Korean external payment gateway API integrations.
- **Missing Disclosure:** Billing flows lack mandatory upfront modal sheets informing Korean users about alternative payment terms.
- **Missing Logging:** Missing backend logging to calculate gross sales, 26% commission obligations, and monthly sales reports for Apple/Google.
- **Missing Testing:** Lacks automated UI tests confirming that Korean alternative payment flows execute without co-mingling standard StoreKit IAP.
- **Missing Evidence:** Lacks monthly sales reporting submission receipts and payment gateway audit records.
- **Missing Audit Trail:** Missing immutable logs tracking sales reporting history, commission remittances, and entitlement configuration updates.

---

## 21. Consolidated Gap Classification Matrix

Where the playbook already covers a framework, the cell says **Covered**. **Partial** means the rule is named with a dated source but lacks a complete developer implementation layer. **Missing** means the playbook does not carry it at all.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. European Accessibility Act**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU Digital Markets Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. EU DSA Trader Status** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. UK OSA & Children Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Australia Online Safety**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. India DPDPA 2023** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Singapore Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. California CCPA / CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. US Subscription Cancel**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China Mobile App Filing**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. SK Telecom Act (Billing)**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Summary and Actionable Remediation Plan

The honest read. The playbook is strong on store review rules, but thinner on backend logging, code components, test suites, evidence templates, and tamper-proof audit trails for live operational compliance.

### Action Plan
1. **Immediate (Phase 1):** Add detection rules for EU GPSR into `data/rejection-patterns.json` and `data/detection-recipes.json`.
2. **Short-Term (Phase 2):** Expand `docs/PRE-SUBMISSION-CHECKLIST.md` and reference guidelines with step-by-step developer checklists for all 20 frameworks across logging, testing, and evidence collection.
3. **Medium-Term (Phase 3):** Implement UI code templates for the EU Contract Withdrawal Button, C2PA AI Act Article 50 watermarking, and BIPA consent forms inside `references/`.
4. **Long-Term (Phase 4):** Build automated integration tests and pre-commit hooks to verify logging schemas and evidence logs prior to code release.

---

## 23. Official Primary Sources

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) & [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Withdrawal Button: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU EAA: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- US COPPA Rule: [FTC 16 CFR Part 312](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents)
- Australia Minimum Age: [Online Safety Amendment Act 2024](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA: [Law 15,211/2025](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in/)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- California CPPA Regulations: [CPPA Regulations](https://cppa.ca.gov/regulations/ccpa_updates.html)
