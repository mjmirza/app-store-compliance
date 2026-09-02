# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping into the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and worldwide markets, checking honestly how far this repository carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight compliance dimensions: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in online marketplaces, digital products, and complex supply chains. The GPSR applies to non-food consumer products on the EU market, requiring online interfaces to clearly display manufacturer and importer identity, safety warnings, and instructions.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives developers no template policy to determine if their product listing falls under Regulation (EU) 2023/988 or how to assign an EU-based Responsible Person.
- **Missing Documentation:**
  The repository lacks developer guides and checklists for structuring online product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR-related elements or UI components displaying safety details.
- **Missing Disclosure:**
  UI templates provide no guidance or components for displaying manufacturer name, registered trade name, postal address, and electronic contact as required under Article 19.
- **Missing Logging:**
  No architectural schemas exist for logging product safety incidents, recalls, or corrective actions in a centralized log.
- **Missing Testing:**
  No automated tests exist to verify that online UI elements dynamically display required product safety information based on user location.
- **Missing Evidence:**
  The repository lacks templates for Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining EU Responsible Person designation.
2. Incorporate GPSR metadata requirements into rejection patterns and pre-submission checklists.
3. Add UI templates demonstrating compliant product detail pages with safety warning labels.
4. Integrate an automated test runner script verifying the presence of safety disclosures prior to release.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders and Directive (EU) 2023/1544 on legal representatives. Mandatory enforcement applies from 18 August 2026, allowing EU judicial authorities to issue orders directly to service providers in the EU regardless of headquarters location. Default data production time is 10 days, with a strict 8-hour emergency response window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy for handling European Production and Preservation Orders.
- **Missing Documentation:**
  The repository lacks concrete operational runbooks for executing 10-day standard orders and 8-hour emergency orders.
- **Missing Code:**
  No backend API endpoints or helper scripts exist to securely export, filter, and package user data in response to a valid judicial order.
- **Missing Disclosure:**
  Privacy policies fail to explicitly disclose to EU users that data may be produced to European law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:**
  No database schemas exist to log incoming law enforcement requests, verification statuses, access activities, or data releases.
- **Missing Testing:**
  There are no integration tests simulating rapid 8-hour emergency retrieval and secure packaging of user data.
- **Missing Evidence:**
  The repository lacks verified templates of European Production Order certificates (EPOC) or Preservation Order certificates (EPOC-PR).
- **Missing Audit Trail:**
  An unalterable audit trail system recording administrative interactions, data extractions, and transmissions is absent.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol establishing roles and channels for executing EPOs.
2. Formally designate an EU establishment or legal representative before 18 August 2026.
3. Build backend data-extraction scripts supporting 8-hour emergency execution.
4. Implement a tamper-proof cryptographic audit trail logging all certificate requests and data extractions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends Directive 2011/83/EU. It requires a prominent, easily accessible withdrawal button on online interfaces for distance financial services contracts concluded electronically, with a 14-day statutory withdrawal period. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Consumer Cancellation and Withdrawal Policy covering the 14-day statutory withdrawal right.
- **Missing Documentation:**
  The repository provides no UI design guidelines specifying placement, prominence, and terminology for the withdrawal button.
- **Missing Code:**
  Front-end templates and billing mocks do not contain a functional withdrawal button or modal sheet.
- **Missing Disclosure:**
  Subscription flows do not prominently disclose the 14-day statutory right of withdrawal or contract revocation consequences.
- **Missing Logging:**
  There are no logging mechanisms to record withdrawal button clicks, timestamps, contract termination confirmations, or refund flows.
- **Missing Testing:**
  No automated UI tests exist to verify that the withdrawal flow completes without manual friction.
- **Missing Evidence:**
  The repository lacks standardized withdrawal confirmation receipts or standardized forms to prove compliance during consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation rates, interface audits, and refund triggers is missing.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent "Withdrawal Button" component within account settings in subscription templates.
3. Establish database logging for cancellation requests, timestamps, and refund transactions.
4. Implement end-to-end UI tests verifying self-service contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State-level legislation (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulates minors' access to mobile applications, purchases, and updates. Developers must request age categories (via Apple Declared Age Range API or Google Play Age Signals API) and obtain verifiable parental consent before allowing minors to download or purchase digital goods. Verification data must be deleted immediately after verification.

Official Citations: Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161.

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template policy detailing minor account detection or state-specific age assurance protocols.
- **Missing Documentation:**
  Checklists lack step-by-step developer guides for integrating Apple Declared Age Range API and Google Play Age Signals API in multi-platform apps.
- **Missing Code:**
  Mock client code does not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app features dynamically.
- **Missing Disclosure:**
  In-app onboarding flows fail to state that age categories are processed to comply with state accountability laws and that parental consent is mandatory.
- **Missing Logging:**
  No backend system exists to log parental consent receipts, consent revocations (`RESCIND_CONSENT`), or immediate raw verification data deletions.
- **Missing Testing:**
  Test suites lack automated integration tests verifying that minor accounts are blocked from purchases without consent signals.
- **Missing Evidence:**
  The repository lacks examples of parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:**
  An immutable audit trail recording feature rollouts, policy updates, and raw data deletion events is missing.

### 4.3 Remediation and Action Plan
1. Create a Minor Age Assurance Policy detailing state detection and data minimization.
2. Implement cross-platform native hooks querying Apple Declared Age Range and Google Play Age Signals APIs.
3. Build backend triggers to purge raw verification data immediately after category confirmation.
4. Add integration tests confirming billing restrictions for minor accounts lacking consent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 requires providers and deployers of AI systems to ensure a sufficient level of AI literacy among staff operating AI features, live since 2 February 2025. Compliance requires maintaining a written policy, induction records, refresh schedules, and training logs.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Literacy Policy defining competency levels and team requirements.
- **Missing Documentation:**
  The repository lacks developer documentation explaining Article 4 obligations or AI safety evaluation standards.
- **Missing Code:**
  No CLI helper or build script exists to verify that an AI literacy training log is present and up to date before deployment.
- **Missing Disclosure:**
  Public documentation and partner contracts fail to disclose organizational adherence to AI literacy standards.
- **Missing Logging:**
  An active centralized training log (`AI_LITERACY_LOG.md`) to record staff inductions and refreshers is absent.
- **Missing Testing:**
  No automated CI checks exist to verify that team members committing AI feature code possess valid literacy records.
- **Missing Evidence:**
  The playbook provides no examples of compliant training records, course completions, or competency assessments.
- **Missing Audit Trail:**
  No historical record tracks when the literacy policy was reviewed or how staff competencies evolved.

### 5.3 Remediation and Action Plan
1. Publish an internal AI Literacy Policy defining competency domains (safety, risk, privacy, bias).
2. Create `AI_LITERACY_LOG.md` to track team member training dates and verification sources.
3. Implement a CI script warning if the literacy log has not been reviewed within the calendar year.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 mandates strict transparency for AI systems reaching EU users from 2 August 2026. Obligations include informing users during AI interaction (Article 50(1)), marking synthetic outputs in a machine-readable format (Article 50(2)), and disclosing deepfakes (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Transparency Policy outlining interaction notices and media marking standards.
- **Missing Documentation:**
  Checklists mention Article 50 but lack technical guides on implementing C2PA metadata watermarking or deepfake disclosures.
- **Missing Code:**
  Codebase templates lack classes or middleware to embed machine-readable watermarks into generated audio, image, video, or text assets.
- **Missing Disclosure:**
  Chat UI templates do not display immediate notices ("You are interacting with an AI system") at first user exposure.
- **Missing Logging:**
  No database schemas log whether transparency notices were displayed during a user session.
- **Missing Testing:**
  Test scripts do not verify synthetic media markers or machine-detectability of generated content.
- **Missing Evidence:**
  The repository lacks evidence templates such as independent watermarking validation reports or content moderation audits.
- **Missing Audit Trail:**
  No audit trail records model updates, transparency disclosure changes, or watermarking implementation decisions.

### 6.3 Remediation and Action Plan
1. Formulate an AI Transparency Policy enforcing direct disclosures and output watermarking.
2. Add prominent notices ("You are chatting with an AI assistant") to conversational UI templates.
3. Integrate C2PA metadata watermarking helpers into synthetic media generation pipelines.
4. Add automated integration tests verifying machine-readable compliance headers in generated media.

---

## 7. EU AI Act Article 5 (Prohibited AI Practices)

### 7.1 Regulatory Overview and Background
Article 5 of Regulation (EU) 2024/1689 bans specific AI practices deemed unacceptable risks, live since 2 February 2025. Prohibited practices include subliminal manipulation, exploitation of vulnerabilities, social scoring, crime profiling, untargeted facial scraping, workplace/educational emotion recognition, and sensitive biometric categorization.

Official Citation: Regulation (EU) 2024/1689, Article 5.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Prohibited AI Assessment Policy guiding developers on identifying and banning prohibited features.
- **Missing Documentation:**
  No developer guide exists explaining how to evaluate models for hidden emotion inference, manipulative loops, or biometric profiling.
- **Missing Code:**
  The static analysis guard lacks detection patterns for facial scraping, emotion analysis, or manipulative UI loops in AI models.
- **Missing Disclosure:**
  Public documentation lacks formal statements certifying that AI systems exclude prohibited practices under Article 5.
- **Missing Logging:**
  No logging mechanisms exist to capture and flag potential runtime violations, such as unauthorized emotion detection calls.
- **Missing Testing:**
  Test suites contain no red-teaming scripts or adversarial tests to verify that AI models refrain from manipulative or profiling outputs.
- **Missing Evidence:**
  The repository provides no template Conformity Assessment or Prohibited Practice Audit Report.
- **Missing Audit Trail:**
  An immutable audit trail logging AI model architectural reviews and risk evaluations is absent.

### 7.3 Remediation and Action Plan
1. Publish an AI Prohibited Practices Screening Policy and checklist.
2. Add static guard rules in `data/rejection-patterns.json` targeting emotion detection and biometric categorization APIs.
3. Create automated red-teaming test scripts to validate model safety boundaries.

---

## 8. EU Digital Markets Act (DMA)

### 8.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms. For mobile developers, DMA provisions cover alternative app stores, web distribution, external purchase links (`com.apple.developer.storekit.external-purchase-link`), custom link sheets (`ExternalPurchaseCustomLink`), and monthly reporting.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Alternative Storefront and External Billing Policy guiding entitlement acquisition and fee models.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for wiring the External Purchase Server API or implementing MarketplaceKit.
- **Missing Code:**
  Mocks lack native implementations of `ExternalPurchaseCustomLink` sheets or external transaction reporting APIs.
- **Missing Disclosure:**
  Templates fail to provide required system-level disclosure sheets informing users that transactions occur outside Apple/Google billing.
- **Missing Logging:**
  No backend logging schema exists to record external purchase transactions for monthly reporting within 15 calendar days.
- **Missing Testing:**
  Automated tests do not verify that StoreKit IAP and external purchase links are never co-mingled on the same EU storefront.
- **Missing Evidence:**
  The repository lacks templates for reporting receipts, notarization logs, or alternative marketplace entitlement approvals.
- **Missing Audit Trail:**
  An unalterable audit trail tracking monthly sales reporting submissions and entitlement configuration changes is absent.

### 8.3 Remediation and Action Plan
1. Draft an EU Storefront & Billing Entitlement Policy.
2. Implement code wrappers for `ExternalPurchaseCustomLink` and monthly reporting payloads.
3. Create CI checks verifying that StoreKit IAP and external offer links are never combined in the same EU build.

---

## 9. EU Digital Services Act (DSA Article 30/31 Trader Status)

### 9.1 Regulatory Overview and Background
Articles 30 and 31 of the Digital Services Act (Regulation (EU) 2022/2065) mandate that app stores verify and display trader contact and identity details for developers distributing apps in the EU, active since 17 February 2025. Failure to complete verification results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an EU Trader Declaration Policy explaining trader versus non-trader criteria.
- **Missing Documentation:**
  Checklists lack operational instructions for submitting D-U-N-S, address, phone, email, and 2FA verification to App Store Connect and Google Play Console.
- **Missing Code:**
  No script exists in `scripts/` to audit App Store Connect API or Google Play API responses for DSA trader compliance status.
- **Missing Disclosure:**
  Product page metadata templates do not include mandatory trader contact disclosures or consumer protection notices.
- **Missing Logging:**
  No logging mechanism tracks developer portal compliance status or verification renewal dates.
- **Missing Testing:**
  Validation scripts do not check whether trader details are present before approving EU distribution.
- **Missing Evidence:**
  The repository provides no templates for D-U-N-S verification certificates or official trader declaration records.
- **Missing Audit Trail:**
  An audit trail tracking historical trader status changes and identity document verification submissions is absent.

### 9.3 Remediation and Action Plan
1. Create a DSA Developer Compliance Protocol covering trader criteria and 2FA setup.
2. Expand metadata audit scripts to verify trader status declarations before release authorization.

---

## 10. European Accessibility Act (EAA)

### 10.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025. It mandates accessibility for mobile apps and e-commerce services reaching EU users under harmonised standard EN 301 549 (WCAG 2.1 Level AA / EN 301 549 Chapter 11).

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a formal European Accessibility Policy defining EN 301 549 compliance criteria.
- **Missing Documentation:**
  Checklists mention WCAG but lack mobile-specific guides for EN 301 549 Chapter 11 (non-web software and mobile apps).
- **Missing Code:**
  Codebase templates lack automated accessibility wrappers for Dynamic Type, VoiceOver traits, or contrast helpers.
- **Missing Disclosure:**
  The repository provides no published Accessibility Statement template as required under EN 301 549 Annex B/C.
- **Missing Logging:**
  No logging exists to track accessibility feedback submitted by users or assistive technology compatibility errors.
- **Missing Testing:**
  The static accessibility audit script (`scripts/accessibility-audit.py`) does not check for EN 301 549 Chapter 11 rules.
- **Missing Evidence:**
  The repository lacks templates for Voluntary Product Accessibility Templates (VPAT) or EN 301 549 audit reports.
- **Missing Audit Trail:**
  An immutable audit trail logging accessibility remediations, testing sessions, and statement updates is absent.

### 10.3 Remediation and Action Plan
1. Publish an EN 301 549 Accessibility Compliance Standard and Accessibility Statement template.
2. Upgrade `scripts/accessibility-audit.py` to audit Chapter 11 mobile accessibility rules.
3. Integrate automated UI tests verifying VoiceOver labels, contrast ratios, and font scaling.

---

## 11. US Amended COPPA Rule

### 11.1 Regulatory Overview and Background
The FTC's Amended Children's Online Privacy Protection Act Rule (16 CFR Part 312, Federal Register 22 April 2025) takes effect with a mandatory compliance date of 22 April 2026. Key updates include expanding personal information to cover biometric and government identifiers, separate opt-in consent for targeted advertising, written data retention policies, and written information security programs.

Official Citation: 16 CFR Part 312, FTC Final Rule (90 FR 16918).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Written COPPA Data Retention Policy (312.10) and Written Information Security Program (312.8).
- **Missing Documentation:**
  Documentation lacks developer guides on new verifiable parental consent methods (face-match, knowledge-based auth).
- **Missing Code:**
  Codebases lack logic to separate third-party disclosure consent from general app onboarding.
- **Missing Disclosure:**
  Onboarding templates lack separate, non-conditioned opt-in disclosures for targeted advertising and third-party data sharing.
- **Missing Logging:**
  No backend logging schema captures separate opt-in consent states or automated deletion triggers for child data.
- **Missing Testing:**
  Test suites lack automated checks confirming that child data collection is blocked when targeted-ad opt-in is declined.
- **Missing Evidence:**
  The repository provides no templates for annual information security risk assessments or safe harbor audit reports.
- **Missing Audit Trail:**
  An unalterable audit trail tracking parental consent receipts, consent revocations, and data retention purges is absent.

### 11.3 Remediation and Action Plan
1. Draft a Written COPPA Data Retention Policy and Written Information Security Program template.
2. Implement dual-consent onboarding flows separating operational consent from targeted advertising opt-ins.
3. Add automated unit tests verifying data retention schedule enforcement and child data purging.

---

## 12. US Federal and State Subscription Cancellation Rules

### 12.1 Regulatory Overview and Background
Although the FTC Negative Option Rule amendment was vacated on procedural grounds in July 2025, underlying enforcement continues under FTC Act Section 5, ROSCA, and state negative-option statutes (California, New York, Massachusetts). Subscriptions billed outside app store in-app purchase must provide a cancellation mechanism at least as simple as sign-up (click-to-cancel).

Official Citations: ROSCA (15 U.S.C. 8401), California Bus. & Prof. Code 17600, NY Gen. Bus. Law 527-A.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Direct Cancellation and Negative Option Policy for web and cross-platform subscriptions.
- **Missing Documentation:**
  Checklists lack operational instructions for implementing self-service cancellation paths on web and account portals.
- **Missing Code:**
  Web-billing code mocks do not include one-click cancellation API endpoints or self-service cancellation UI sheets.
- **Missing Disclosure:**
  Subscription paywalls lack clear disclosures detailing auto-renewal terms, cancellation methods, and timing requirements.
- **Missing Logging:**
  No backend logging schema records subscription cancellation requests, effective cancellation dates, or retention offer declines.
- **Missing Testing:**
  Automated tests do not verify that cancellation can be completed online without requiring phone or email contact.
- **Missing Evidence:**
  The repository provides no templates for post-cancellation confirmation emails or cancellation flow audit logs.
- **Missing Audit Trail:**
  An immutable audit trail logging changes to cancellation UI flows and subscription terms is missing.

### 12.3 Remediation and Action Plan
1. Establish a Subscription Disclosure and Cancellation Standard.
2. Implement self-service cancellation API endpoints and UI components in web/cross-platform billing mocks.
3. Add end-to-end UI tests confirming frictionless cancellation execution.

---

## 13. US California Consumer Privacy Act (CCPA/CPRA) and State Privacy Laws

### 13.1 Regulatory Overview and Background
The CCPA/CPRA and comprehensive state privacy laws (Virginia, Colorado, Connecticut, Texas, Oregon, Delaware, New Jersey, Minnesota, Maryland) require privacy notices, opt-outs for sale/sharing/targeted advertising, sensitive data limits, and automated recognition of Global Privacy Control (GPC) signals (`Sec-GPC`).

Official Citations: Cal. Civ. Code 1798.100 et seq., CPPA Regulations (2026).

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Multi-State Privacy Compliance Policy outlining state-specific opt-out and sensitive data rules.
- **Missing Documentation:**
  Documentation lacks technical guides for detecting `Sec-GPC` headers in webviews and mapping them to native opt-out flags.
- **Missing Code:**
  Codebases lack native helper modules to parse GPC signals or toggle ad-SDK tracking dynamically.
- **Missing Disclosure:**
  In-app settings lack "Do Not Sell or Share My Personal Information" and "Limit Sensitive Data Use" modals.
- **Missing Logging:**
  No backend logging schema records user opt-out preferences, GPC signal detections, or consumer rights requests.
- **Missing Testing:**
  Test suites lack automated scripts verifying that ad-tracking SDKs are disabled when GPC signals are detected.
- **Missing Evidence:**
  The repository provides no templates for Data Protection Impact Assessments (DPIA) or GPC handling verification logs.
- **Missing Audit Trail:**
  An unalterable audit trail tracking consumer rights request fulfillment (know, delete, opt-out) is absent.

### 13.3 Remediation and Action Plan
1. Publish a Multi-State U.S. Privacy Policy and GPC Implementation Guide.
2. Implement GPC header parsing in webview handlers and bind signals to ad-SDK suppression logic.
3. Add automated tests verifying ad-tracking suppression upon receiving GPC signals.

---

## 14. US Health Breach Notification Rule & Illinois BIPA

### 14.1 Regulatory Overview and Background
The FTC Health Breach Notification Rule (16 CFR Part 318, 2024 Final Rule) treats unauthorized sharing of personal health data with ad vendors as a breach requiring notice within 60 days. Illinois BIPA (740 ILCS 14) mandates written notice, written releases, and public retention schedules prior to biometric data capture.

Official Citations: 16 CFR Part 318, 740 ILCS 14 (Illinois BIPA).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Health Data Breach Response Policy and a Public Biometric Retention and Destruction Policy.
- **Missing Documentation:**
  Checklists lack operational steps for categorizing health data flows and obtaining written BIPA releases before biometric collection.
- **Missing Code:**
  Codebases lack biometric consent modal templates or automated data destruction triggers for stored facial/fingerprint data.
- **Missing Disclosure:**
  Health app onboarding flows fail to disclose third-party ad-vendor data sharing as a breach trigger.
- **Missing Logging:**
  No backend schema logs health data transmissions, breach discovery timestamps, or biometric destruction logs.
- **Missing Testing:**
  Test scripts do not check whether health data payloads are transmitted to unauthorized ad-vendor endpoints.
- **Missing Evidence:**
  The repository provides no templates for FTC breach notification letters or BIPA written release forms.
- **Missing Audit Trail:**
  An immutable audit trail logging biometric data deletion events and health data vendor disclosures is missing.

### 14.3 Remediation and Action Plan
1. Publish a Health Data & Biometric Compliance Standard including BIPA consent forms.
2. Build network payload inspection tests verifying zero health data transmission to ad endpoints.
3. Implement automated database triggers enforcing 3-year maximum biometric data retention under BIPA.

---

## 15. UK Online Safety Act 2023 & ICO Age Appropriate Design Code

### 15.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom from July 2025) requires Highly Effective Age Assurance (facial estimation, open banking, ID check) for age-restricted content. The ICO Age Appropriate Design Code (Children's Code) mandates high privacy by default, geolocation off, profiling off, and mandatory DPIAs for services accessed by under-18s.

Official Citations: UK Online Safety Act 2023 c. 50, ICO Children's Code.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a UK Children's Privacy & Age Assurance Policy.
- **Missing Documentation:**
  Documentation lacks developer guides for executing Ofcom-approved Highly Effective Age Assurance or ICO DPIAs.
- **Missing Code:**
  Codebases lack high-privacy default profiles (geolocation disabled, profiling disabled) for UK minor accounts.
- **Missing Disclosure:**
  Onboarding flows fail to disclose child safety measures, age estimation methods, and privacy default settings.
- **Missing Logging:**
  No backend schema logs age assurance execution results or immediate verification data purges.
- **Missing Testing:**
  Automated tests do not verify that geolocation and profiling features are disabled by default for UK minor profiles.
- **Missing Evidence:**
  The repository provides no completed UK Children's Code DPIA templates or Ofcom age verification audit logs.
- **Missing Audit Trail:**
  An unalterable audit trail tracking age-assurance configuration changes and DPIA annual reviews is missing.

### 15.3 Remediation and Action Plan
1. Draft a UK Age Appropriate Design Code Standard and DPIA template.
2. Implement runtime environment flags disabling geolocation and profiling when UK child profiles are detected.
3. Add automated integration tests validating Ofcom age assurance workflows.

---

## 16. Australia Online Safety Amendment Act 2024

### 16.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 enforces a minimum age of 16 for age-restricted social media platforms starting 10 December 2025. Platforms must take reasonable steps (using eSafety-approved age assurance, not self-declaration) to prevent under-16s from holding accounts, and must destroy verification data immediately after use.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an Australian Social Media Age Restriction Policy.
- **Missing Documentation:**
  Checklists lack guidelines for integrating eSafety-compliant age-assurance waterfalls in social media apps.
- **Missing Code:**
  Mock code does not include age-assurance integration or automated verification data destruction triggers.
- **Missing Disclosure:**
  Account creation flows fail to inform Australian users that account access requires age verification and that raw verification data is purged.
- **Missing Logging:**
  No logging schema exists to record successful age verification outcomes and immediate raw data destruction events.
- **Missing Testing:**
  Test suites contain no automated tests verifying that under-16 accounts are blocked from social feature access in Australia.
- **Missing Evidence:**
  The repository provides no templates for eSafety compliance audits or data destruction verification certificates.
- **Missing Audit Trail:**
  An immutable audit trail logging age restriction enforcement and verification data purges is absent.

### 16.3 Remediation and Action Plan
1. Formulate an Australian Minimum Age Compliance Standard.
2. Build native age-assurance waterfall hooks and immediate raw data deletion handlers.
3. Add automated tests verifying social account creation blocks for under-16 users in Australia.

---

## 17. Brazil Digital ECA & LGPD

### 17.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025), enforceable from 17 March 2026 alongside the LGPD, prohibits self-declaration age checkboxes for minor protection. Accepted age verification includes document check, facial age estimation, and CPF database lookup. Verification data must be strictly minimized and ringfenced.

Official Citations: Law 15,211/2025 (Digital ECA), Law 13,709/2018 (LGPD).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Brazil Digital ECA Compliance Policy.
- **Missing Documentation:**
  Documentation lacks technical guides for integrating CPF validation or facial age estimation services for Brazilian accounts.
- **Missing Code:**
  Codebases lack CPF lookup helpers or facial age estimation integration modules.
- **Missing Disclosure:**
  Onboarding UI templates fail to display LGPD child privacy notices or Digital ECA verification disclosures.
- **Missing Logging:**
  No backend schema logs CPF validation states or facial estimation outcomes while ensuring raw image deletion.
- **Missing Testing:**
  Automated tests do not verify that self-declaration checkboxes are rejected for Brazilian account registration.
- **Missing Evidence:**
  The repository provides no templates for ANPD data protection impact reports or CPF verification audit records.
- **Missing Audit Trail:**
  An unalterable audit trail recording age verification system updates and LGPD compliance checks is missing.

### 17.3 Remediation and Action Plan
1. Publish a Brazil ECA & LGPD Child Privacy Standard.
2. Implement CPF validation and facial age estimation code modules with immediate raw data deletion.
3. Add automated tests confirming rejection of self-declaration checkboxes in Brazilian onboarding flows.

---

## 18. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 18.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 (notified November 2025, enforcement May 2027) require verifiable parental consent through government-backed mechanisms (e.g., DigiLocker) before processing data of individuals under 18. Behavioral tracking and targeted advertising to children are strictly prohibited.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks an India DPDPA Child Data Processing Policy.
- **Missing Documentation:**
  Checklists lack operational steps for integrating DigiLocker or virtual token parental consent mechanisms.
- **Missing Code:**
  Codebases lack DigiLocker verification API wrappers or ad-tracking disabling switches for Indian minor accounts.
- **Missing Disclosure:**
  Onboarding flows fail to present multilingual consent notices or parental consent requirements under DPDPA.
- **Missing Logging:**
  No backend schema logs DigiLocker parental consent verification tokens or consent revocation events.
- **Missing Testing:**
  Test suites lack automated scripts confirming that behavioral tracking and targeted ads are disabled for Indian under-18 users.
- **Missing Evidence:**
  The repository provides no templates for Data Protection Board of India audit filings or DigiLocker integration logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking parental consent receipts and child data processing audits is absent.

### 18.3 Remediation and Action Plan
1. Establish an India DPDPA Compliance Framework including DigiLocker consent workflows.
2. Implement DigiLocker API wrappers and child account ad-tracking suppression switches.
3. Add automated integration tests validating parental consent processing for Indian accounts.

---

## 19. Singapore IMDA Code of Practice for Online Safety & PDPA

### 19.1 Regulatory Overview and Background
Singapore's IMDA Code of Practice for Online Safety for App Distribution Services (enforceable April 2026) requires app-store age assurance to prevent under-18s from downloading age-inappropriate apps. Age-assurance data must be destroyed immediately after verification under the PDPA.

Official Citations: IMDA Code of Practice for Online Safety, Personal Data Protection Act 2012.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a Singapore App Distribution & Age Assurance Policy.
- **Missing Documentation:**
  Documentation lacks developer guides on handling platform-level age signals in Singapore.
- **Missing Code:**
  Mock code does not include handlers for Singapore age gating or automated age-data purging mechanisms.
- **Missing Disclosure:**
  App Store listing templates lack Singapore IMDA content rating disclosures and age suitability notices.
- **Missing Logging:**
  No backend schema logs age verification signals or data destruction confirmation events.
- **Missing Testing:**
  Test scripts do not verify that age-inappropriate app downloads or access are restricted for Singapore minor accounts.
- **Missing Evidence:**
  The repository provides no templates for IMDA online safety compliance reports or PDPA data destruction logs.
- **Missing Audit Trail:**
  An unalterable audit trail recording age verification parameters and platform compliance checks is missing.

### 19.3 Remediation and Action Plan
1. Publish a Singapore IMDA & PDPA Compliance Guide.
2. Implement age-signal handlers and data destruction verification logic for Singapore users.
3. Add automated tests validating age-gating restrictions for age-inappropriate app content.

---

## 20. South Korea Telecommunications Business Act & China Mobile App Filing (MIIT)

### 20.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment support (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`), a 26% commission structure, and monthly reporting. China's MIIT Mobile App Filing (ICP extension) requires local Chinese entity registration, real-name verification, PIPL privacy compliance, and Banhao game licenses prior to app distribution.

Official Citations: South Korea Telecommunications Business Act Art. 22-9, China MIIT Notice on Mobile App Filing (2023).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a South Korea Alternative Billing Policy and a China App Filing & PIPL Policy.
- **Missing Documentation:**
  Documentation lacks step-by-step guides for MIIT ICP filing, local entity establishment in China, or South Korea StoreKit reporting.
- **Missing Code:**
  Codebases lack South Korea native payment modal sheets, gross sales reporting scripts, or China real-name verification APIs.
- **Missing Disclosure:**
  Payment UI templates lack mandatory South Korean alternative payment disclosures; Chinese listing templates lack MIIT filing number disclosures.
- **Missing Logging:**
  No backend schema logs South Korean monthly sales reporting data or Chinese real-name identity verification tokens.
- **Missing Testing:**
  Automated tests do not verify that South Korea alternative billing binaries exclude standard StoreKit IAP co-mingling, or that MIIT filing status is validated.
- **Missing Evidence:**
  The repository provides no templates for MIIT app filing certificates, Banhao license records, or South Korea remittance receipts.
- **Missing Audit Trail:**
  An immutable audit trail logging monthly South Korea billing reports and Chinese regulatory filings is absent.

### 20.3 Remediation and Action Plan
1. Publish a South Korea Billing & China MIIT Filing Compliance Guide.
2. Build South Korea StoreKit alternative billing wrappers and monthly reporting scripts.
3. Add automated CI checks verifying MIIT filing registration and South Korea billing configuration.

---

## 21. Consolidated Gap Classification Matrix

Where a framework is already addressed in code, documentation, or rules, the cell indicates Covered. Partial indicates the framework is referenced with dates/citations but lacks full operational assets. Missing indicates the playbook currently lacks coverage for that dimension.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU AI Act Art 5** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. EU DSA Trader** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. EU EAA (EN 301 549)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. US Amended COPPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US Sub Cancellation** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US CCPA/CPRA & GPC** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. US Health Breach / BIPA**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. UK OSA & ICO Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Australia OSA 2024** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. India DPDPA 2023** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. Singapore IMDA Code**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. SK TBA & China Filing**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

This comprehensive gap report audits the playbook against 20 major modern global and regional regulations. While the repository provides strong coverage of App Store and Google Play rejection rules and key regulatory effective dates, significant gaps remain in code implementations, database logging schemas, automated test coverage, compliance evidence templates, and immutable audit trails across all twenty frameworks.

Addressing these gaps requires prioritizing:
1. Complete implementation of GPSR assets (the only regulation missing across all eight dimensions).
2. Development of native code wrappers and UI components for EU Withdrawal Button, EU AI Act Article 50 watermarking, and US ASAA / GPC handlers.
3. Creation of automated testing scripts and database schemas for e-Evidence emergency requests, COPPA dual-consent, and subscription cancellations.

This report must be updated whenever primary regulatory dates or statutory requirements change.

---

## 23. Sources

Primary official sources cited across all twenty regulatory frameworks:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services Directive: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US Amended COPPA Rule: [16 CFR Part 312 (Federal Register 90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- US FTC Health Breach Notification Rule: [16 CFR Part 318](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-finalizes-changes-health-breach-notification-rule)
- US ROSCA: [15 U.S.C. 8401](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- California Privacy Rights Act (CPRA): [Cal. Civ. Code 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Amendment Act 2024: [Federal Register of Legislation](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- Brazil Digital ECA: [Law 15,211/2025](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/)
- India DPDPA 2023: [Gazette of India Act No. 22 of 2023](https://egazette.gov.in/)
- Singapore IMDA Code of Practice: [IMDA Online Safety Regulations](https://www.twobirds.com/en/insights/2026/singapore/app-stores-in-singapore-required-to-implement-age-assurance-measures)
- South Korea Telecommunications Business Act: [Korea Legislation Research Institute](https://developer.apple.com/support/storekit-external-entitlement-kr/)
- China MIIT Mobile App Filing: [MIIT Notice 2023](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/)
