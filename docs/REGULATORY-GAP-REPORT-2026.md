# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind application developers shipping mobile and web applications worldwide, and systematically checks how far this repository carries each framework, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight mandatory gap categories:
1. Missing Policy
2. Missing Documentation
3. Missing Code
4. Missing Disclosure
5. Missing Logging
6. Missing Testing
7. Missing Evidence
8. Missing Audit Trail

Assume the repository is incomplete unless proven otherwise, and search until no additional gaps remain.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the old General Product Safety Directive (2001/95/EC) to address the safety challenges of online marketplaces, digital products, and complex supply chains. The GPSR mandates that online marketplaces and e-commerce applications clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook gives developers no template policy or operational framework to determine if their app or listing falls within Regulation (EU) 2023/988.
- **Missing Documentation:** Missing developer guides, integration manuals, or step-by-step instructions on structuring UI components to display GPSR safety warnings and manufacturer information.
- **Missing Code:** The pre-submission guard (`agent-os/hooks/app-store-compliance-guard.sh`) and rejection patterns (`data/rejection-patterns.json`) lack scanning rules or code blocks for GPSR product safety labels and Responsible Person details.
- **Missing Disclosure:** Interface templates lack mandatory UI placeholder components for Article 19 disclosures (manufacturer name, trade name/trademark, postal address, electronic address).
- **Missing Logging:** No database schemas, data structures, or logging specifications exist for capturing product safety incidents, safety complaints, or product recalls.
- **Missing Testing:** No automated UI or unit test suites exist to verify dynamic display of product safety information or geo-targeted safety disclosures.
- **Missing Evidence:** Lacks sample technical documentation files, safety risk assessment templates, or designated EU Responsible Person appointment proof.
- **Missing Audit Trail:** Lacks audit trail models to record safety warning reviews, policy updates, or corrective measures executed in response to safety alerts.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 (European Production and Preservation Orders) and Directive (EU) 2023/1544 (appointment of legal representatives). Enforcement is mandatory starting 18 August 2026. Judicial authorities can issue binding orders directly to service providers in the EU, requiring standard data production within 10 days and emergency data production within a strict 8-hour window.

Official Citations: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Law Enforcement Request Policy template for handling cross-border judicial orders under Regulation (EU) 2023/1543.
- **Missing Documentation:** Lacks operational runbooks or manuals detailing step-by-step procedures for fulfilling 10-day standard orders and 8-hour emergency orders.
- **Missing Code:** Backend mock implementations lack automated data export scripts or secure endpoints for packaging and encrypting requested user data.
- **Missing Disclosure:** Public privacy policy templates do not disclose to users that data may be produced or preserved under European Production Orders.
- **Missing Logging:** Lacks database schemas for logging law enforcement certificates, verification steps, or data extraction activities.
- **Missing Testing:** Lacks automated simulation tests to validate data extraction and packaging within the mandatory 8-hour emergency window.
- **Missing Evidence:** Lacks sample European Production Order Certificates (EPOC) or Preservation Order Certificates (EPOC-PR) for verification testing.
- **Missing Audit Trail:** Lacks an immutable cryptographic audit log recording administrative handling, verification checks, and data releases.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU) regarding distance financial services contracts, mandating a prominent, easily accessible withdrawal button/function on online interfaces. Member States apply these rules from 19 June 2026. The cancellation path must be as frictionless as sign-up.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a template Consumer Withdrawal Policy defining the 14-day statutory right of withdrawal and applicable exceptions.
- **Missing Documentation:** Lacks UI layout specs and design guidance detailing withdrawal button prominence, styling, and text hierarchy.
- **Missing Code:** Subscription and billing UI templates lack functional implementations of a withdrawal button or contract termination modal sheet.
- **Missing Disclosure:** Checkout flows fail to display mandatory pre-contractual disclosures regarding the 14-day withdrawal right and refund conditions.
- **Missing Logging:** Lacks event logging specs for capturing user clicks on the withdrawal button, confirmation timestamps, and refund triggers.
- **Missing Testing:** Lacks automated UI test scripts to verify self-service contract revocation without requiring manual customer support intervention.
- **Missing Evidence:** Lacks template cancellation receipts, standardized withdrawal forms, or refund confirmation records.
- **Missing Audit Trail:** Lacks audit trail mechanisms to track historical cancellation rates, UI flow updates, or contract termination logs.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State laws (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minors' access to mobile applications, purchases, and updates. Developers must process minor age categories (via Apple Declared Age Range API or Google Play Age Signals API), obtain verifiable parental consent, and immediately delete raw age verification data.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Minor Age Assurance Policy detailing state-specific age checks, parental consent flows, and data minimization.
- **Missing Documentation:** Lacks cross-platform developer integration guides for unifying Apple Declared Age Range API and Google Play Age Signals API.
- **Missing Code:** Codebase mock implementations do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict minor accounts dynamically.
- **Missing Disclosure:** Onboarding UI flows do not display required state disclosures explaining age category collection and parental consent requirements.
- **Missing Logging:** Lacks backend logging schemas for capturing parental consent receipts, `RESCIND_CONSENT` server notifications, and data purging triggers.
- **Missing Testing:** Test suites lack automated integration tests verifying that minor accounts without consent signals are blocked from gated features.
- **Missing Evidence:** Lacks sample parental consent forms, age verification receipts, or data deletion confirmation records.
- **Missing Audit Trail:** Lacks an unalterable audit trail recording policy changes, age assurance feature rollouts, and raw data purge logs.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 requires providers and deployers of AI systems to ensure a sufficient level of AI literacy among personnel operating AI systems. Effective since 2 February 2025 with no headcount carve-out.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a formal corporate AI Literacy Policy specifying required competency domains (safety, privacy, bias, risk evaluation).
- **Missing Documentation:** Lacks developer training manuals or operational guidelines explaining Article 4 obligations for development teams.
- **Missing Code:** Lacks CI/CD linting scripts or automated helper tools to check for the presence and validity of team AI literacy records.
- **Missing Disclosure:** Public documentation and contracts do not disclose the organization's adherence to AI literacy standards under Article 4.
- **Missing Logging:** Lacks an active, centralized training log (`AI_LITERACY_LOG.md`) tracking employee inductions, modules completed, and refresher dates.
- **Missing Testing:** Lacks pre-commit or CI test hooks that verify team members committing AI-related code have valid, up-to-date literacy records.
- **Missing Evidence:** Lacks sample training completion certificates, course materials, or formal literacy assessment records.
- **Missing Audit Trail:** Lacks an audit trail documenting annual literacy policy reviews, training module updates, and historical team records.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 mandates transparency for AI systems, taking effect 2 August 2026. Developers must inform users when interacting with AI (50(1)), mark synthetic outputs in machine-readable format (50(2)), and disclose deepfakes (50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a corporate AI Transparency Policy specifying disclosure rules and synthetic content marking requirements.
- **Missing Documentation:** Lacks technical integration guides for embedding machine-readable watermarks (e.g., C2PA metadata) into generated assets.
- **Missing Code:** Chatbot and generation UI templates lack helper classes or middleware for injecting machine-readable watermarks or deepfake headers.
- **Missing Disclosure:** Conversational and generation UI templates do not display the mandatory disclosure ("You are interacting with an AI system") at first exposure.
- **Missing Logging:** Lacks database logging specifications to record that transparency notices were successfully presented to specific user sessions.
- **Missing Testing:** Automated test suites do not check generated media for machine-readable synthetic content markers or C2PA headers.
- **Missing Evidence:** Lacks independent audit reports or security test records verifying content moderation and metadata retention.
- **Missing Audit Trail:** Lacks an immutable audit log capturing model changes, technical watermarking choices, and disclosure UI updates.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 regulates gatekeeper platforms (Apple App Store and Google Play). Third-party developers distributing in the EU can utilize alternative app marketplaces, web distribution, and external payment links via dedicated entitlements (`com.apple.developer.storekit.external-purchase-link`).

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a DMA Entitlement & External Distribution Policy guiding developers on choosing between App Store, Web Distribution, and Alternative Marketplaces.
- **Missing Documentation:** Lacks developer guides detailing monthly reporting procedures under the External Purchase Server API.
- **Missing Code:** Codebase templates lack native entitlement declarations, `ExternalPurchaseCustomLink` API call wrappers, or fallback handlers.
- **Missing Disclosure:** External payment flows lack system disclosure sheets informing users that transactions occur outside Apple/Google billing.
- **Missing Logging:** Lacks server-side database schemas for logging out-of-app transactions, customer purchase IDs, and reporting payloads.
- **Missing Testing:** Lacks unit and integration tests verifying that apps do not co-mingle StoreKit IAP and external purchase links on the same EU storefront.
- **Missing Evidence:** Lacks template reporting files, monthly sales summaries, or signed StoreKit Addendum records.
- **Missing Audit Trail:** Lacks an audit log tracking entitlement requests, monthly sales reporting submissions, and fee calculation audits.

---

## 8. EU Digital Services Act (DSA - Trader Status)

### 8.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (Articles 30 and 31) requires app stores to verify and display trader contact details for developers distributing in the EU. Non-compliance results in app removal from EU storefronts.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Trader Status Determination Policy helping organizations and individual developers correctly classify their status under EU law.
- **Missing Documentation:** Lacks step-by-step developer guides for verifying trader credentials in App Store Connect and Google Play Console.
- **Missing Code:** Pre-submission guard scripts do not scan store metadata configurations for missing or unverified DSA trader declarations.
- **Missing Disclosure:** In-app setting pages do not display published trader details (D-U-N-S, address, phone, email) or non-trader consumer warnings.
- **Missing Logging:** Lacks logging specifications to track trader credential updates or 2FA verification statuses in internal compliance databases.
- **Missing Testing:** Automated metadata audit scripts (`scripts/metadata-audit.py`) lack explicit flags to validate trader disclosure fields.
- **Missing Evidence:** Lacks copies of verified D-U-N-S records, phone/email 2FA completion receipts, or official trader verification certificates.
- **Missing Audit Trail:** Lacks an audit trail tracking historical trader status changes, document uploads, or store verification approvals.

---

## 9. European Accessibility Act (EAA / EN 301 549)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 requires digital products and services (including mobile apps) to comply with harmonised accessibility standards (EN 301 549 / WCAG 2.1 Level AA) starting 28 June 2025.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks an Organizational Digital Accessibility Policy establishing compliance thresholds under EN 301 549 Chapter 11.
- **Missing Documentation:** Lacks developer guidelines detailing mobile-specific accessibility implementations (VoiceOver, Dynamic Type, contrast ratios).
- **Missing Code:** Sample UI layouts lack comprehensive accessibility labels (`accessibilityLabel`), traits, or dynamic font scaling overrides.
- **Missing Disclosure:** Repository templates do not contain a standardized, published Accessibility Statement (EN 301 549 Annex B/C).
- **Missing Logging:** Lacks logging mechanisms to track accessibility feedback, user-reported barriers, or assistive technology compatibility issues.
- **Missing Testing:** While `scripts/accessibility-audit.py` exists, automated CI runners do not execute full EN 301 549 Chapter 11 mobile checks on every build.
- **Missing Evidence:** Lacks completed Accessibility Conformance Reports (VPAT / EN 301 549 ACR) or third-party accessibility audit certifications.
- **Missing Audit Trail:** Lacks an audit log tracking accessibility regression tests, remediation cycles, and annual accessibility statement reviews.

---

## 10. US COPPA Amended Rule (16 CFR Part 312)

### 10.1 Regulatory Overview and Background
The FTC amended the Children's Online Privacy Protection Act Rule (90 FR 16918), with mandatory compliance starting 22 April 2026. Key updates include adding biometric and government IDs to personal information, separate opt-in consent for targeted ads/third-party disclosure, written retention policies, and written information security programs.

Official Citation: FTC Children's Online Privacy Protection Rule, 16 CFR Part 312.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Written Children's Data Retention Policy and Written Information Security Program (WISP) required under 16 CFR 312.8 and 312.10.
- **Missing Documentation:** Lacks developer manuals for implementing new verifiable parental consent methods (knowledge-based auth, face-match ID).
- **Missing Code:** Mobile templates lack separate opt-in consent toggles for targeted advertising versus core app access in child-directed flows.
- **Missing Disclosure:** Privacy policy templates do not distinguish between core functional data collection and third-party ad disclosures for under-13 users.
- **Missing Logging:** Lacks database schemas for logging separate parental consents, age gate attempts, and mandatory data retention/deletion schedules.
- **Missing Testing:** Automated test suites do not verify that third-party tracking SDKs are hard-disabled when parental opt-in consent for ads is absent.
- **Missing Evidence:** Lacks formal risk assessment reports, annual security program reviews, or verifiable parental consent provider contracts.
- **Missing Audit Trail:** Lacks an immutable audit trail recording children's data deletion events, WISP annual reviews, and parental consent logs.

---

## 11. California Privacy Rights Act (CPRA / CCPA / CPPA 2026)

### 11.1 Regulatory Overview and Background
The CPRA amends the CCPA, with CPPA 2026 regulations effective 1 January 2026. Mandates explicit privacy notices, "Do Not Sell or Share" opt-outs, Global Privacy Control (GPC) support, and limits on sensitive personal information.

Official Citation: California Consumer Privacy Act of 2018, as amended by CPRA (Cal. Civ. Code Section 1798.100 et seq.).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a California Consumer Privacy Policy covering rights to know, delete, correct, opt-out, and limit sensitive personal data.
- **Missing Documentation:** Lacks developer instructions for handling embedded webview `Sec-GPC` headers and native platform privacy opt-outs.
- **Missing Code:** Webview and native code templates lack automated listeners for Global Privacy Control (`Sec-GPC`) signals to suppress ad tracking.
- **Missing Disclosure:** In-app settings lack "Do Not Sell or Share My Personal Information" and "Limit the Use of My Sensitive Personal Information" links.
- **Missing Logging:** Lacks backend database logging for consumer privacy requests (know, delete, opt-out) and response fulfillment timelines.
- **Missing Testing:** Lacks unit tests verifying that receiving a GPC signal automatically disables third-party analytics and ad network SDKs.
- **Missing Evidence:** Lacks sample Data Protection Impact Assessments (DPIA) or cybersecurity audit reports required under CPPA rules.
- **Missing Audit Trail:** Lacks an immutable log recording consumer request dates, verification steps, fulfillment responses, and GPC signal receptions.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
BIPA (740 ILCS 14) regulates biometric identifiers (facial templates, fingerprints, iris scans). Requires written notice, written release, public retention schedule, destruction within 3 years, and prohibits sale.

Official Citation: Illinois Biometric Information Privacy Act, 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Public Biometric Data Retention and Destruction Schedule policy template.
- **Missing Documentation:** Lacks integration guides for obtaining e-signed written releases before invoking device biometric APIs (FaceID/BiometricPrompt).
- **Missing Code:** Codebase templates lack written release modal components or e-signature consent capture logic prior to biometric registration.
- **Missing Disclosure:** Biometric authentication UI components do not display mandatory disclosures detailing specific purpose and length of term.
- **Missing Logging:** Lacks database logging specifications to capture timestamped written consents and automated 3-year data destruction triggers.
- **Missing Testing:** Automated tests do not check that biometric feature flows block API execution until a valid written release signal is logged.
- **Missing Evidence:** Lacks sample executed biometric release forms or formal proof of zero-sale agreements with third-party biometric vendors.
- **Missing Audit Trail:** Lacks an unalterable audit log tracking biometric consent receipts, retention schedule reviews, and biometric data deletions.

---

## 13. US Subscription Cancellation (ROSCA & Negative Option)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA) and state negative option laws (CA, NY, MA) mandate that online subscription cancellation must be simple, frictionless, and at least as easy as sign-up (e.g., click-to-cancel without requiring phone calls or letters).

Official Citations: 15 U.S.C. Section 8401 et seq. (ROSCA); Cal. Bus. & Prof. Code Section 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Subscription Negative Option & Cancellation Policy defining frictionless online cancellation standards.
- **Missing Documentation:** Lacks developer guidelines for building web and in-app self-service subscription cancellation flows.
- **Missing Code:** Account management UI templates lack self-service one-click cancellation button components for web/external billing flows.
- **Missing Disclosure:** Subscription checkout screens lack explicit negative option disclosures (recurring charge amount, frequency, simple cancellation method).
- **Missing Logging:** Lacks logging schemas to record subscription sign-up consent, recurring billing notices, and cancellation request timestamps.
- **Missing Testing:** Test suites do not verify that web and external billing subscription cancellation paths complete without human intervention.
- **Missing Evidence:** Lacks sample cancellation confirmation receipts, checkout disclosure screenshots, or recurring billing notification logs.
- **Missing Audit Trail:** Lacks an audit trail capturing historical subscription flow modifications, cancellation retention rates, and refund logs.

---

## 14. UK Online Safety Act 2023

### 14.1 Regulatory Overview and Background
Enforced by Ofcom, the UK Online Safety Act requires services accessible by children to implement Highly Effective Age Assurance (facial age estimation, open banking, digital ID, credit card check) to prevent access to harmful content.

Official Citation: UK Online Safety Act 2023 c. 50.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a UK Child Safety & Content Risk Assessment Policy complying with Ofcom statutory guidance.
- **Missing Documentation:** Lacks technical integration guides for connecting to Highly Effective Age Assurance providers in UK-facing apps.
- **Missing Code:** Codebase templates lack integration logic for third-party age estimation APIs or fallback restriction handlers.
- **Missing Disclosure:** UK onboarding flows do not display mandatory disclosures regarding age verification requirements and content filtering.
- **Missing Logging:** Lacks secure logging schemas to record age assurance verification outcomes while ensuring raw verification data deletion.
- **Missing Testing:** Test suites lack automated flows simulating UK user IP detection and enforcement of Highly Effective Age Assurance.
- **Missing Evidence:** Lacks completed Ofcom Illegal Content Risk Assessments or Children's Access Risk Assessment documentation.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing risk assessment reviews, safety feature updates, and age verification logs.

---

## 15. UK ICO Children's Code

### 15.1 Regulatory Overview and Background
The ICO Age Appropriate Design Code sets 15 standards for services likely to be accessed by children under 18 in the UK. Mandates high privacy by default, data minimization, profiling/geolocation off by default, and a Data Protection Impact Assessment (DPIA).

Official Citation: ICO Age Appropriate Design Code (Code of Practice under Section 123 of Data Protection Act 2018).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks an Age-Appropriate Design Policy incorporating the ICO's 15 standards for child-accessible services.
- **Missing Documentation:** Lacks developer checklists for implementing high privacy defaults (geolocation off, profiling off, nudge techniques banned).
- **Missing Code:** App configuration templates do not default geolocation, push notifications, and profiling toggles to OFF for minor accounts.
- **Missing Disclosure:** In-app privacy information is not presented in clear, age-appropriate language tailored to child age tiers.
- **Missing Logging:** Lacks database logging specifications to capture child privacy preference changes and DPIA mitigation tracking.
- **Missing Testing:** Automated tests do not verify that child accounts default to maximum privacy settings upon registration.
- **Missing Evidence:** Lacks formal ICO Children's Code DPIA documentation or child UX testing research reports.
- **Missing Audit Trail:** Lacks an audit trail recording annual DPIA reviews, child default configuration changes, and policy updates.

---

## 16. Australia Online Safety Act

### 16.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 enforces account restrictions for under-16s on social media, supervised by eSafety. Requires robust age assurance and mandatory destruction of age data.

Official Citation: Australia Online Safety Act 2021 as amended by Social Media Minimum Age Act 2024.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks an Australian Social Media Age Restriction Policy detailing account blocking and age data destruction protocols.
- **Missing Documentation:** Lacks developer integration guides for implementing eSafety-compliant age assurance waterfalls.
- **Missing Code:** Social feed codebase templates lack age-gating hooks that prevent under-16 registration on Australian storefronts.
- **Missing Disclosure:** Australian onboarding screens lack explicit disclosures informing users of statutory age restrictions and data destruction.
- **Missing Logging:** Lacks backend database triggers designed to purge raw age-assurance verification documents immediately after processing.
- **Missing Testing:** Automated tests do not verify that Australian IP user accounts under 16 are blocked from account creation.
- **Missing Evidence:** Lacks completed eSafety Industry Code compliance declarations or independent age assurance audit reports.
- **Missing Audit Trail:** Lacks an immutable log recording raw data deletion events, age-gating updates, and eSafety compliance reviews.

---

## 17. Brazil Digital ECA (Law 15,211/2025)

### 17.1 Regulatory Overview and Background
Law 15,211/2025 (Digital ECA) regulates child and adolescent protection online, enforced by ANPD starting 17 March 2026. Prohibits self-declaration checkboxes; requires document checks, facial estimation, or CPF checks, and integration with Google Play Age Signals / Apple Declared Age Range.

Official Citation: Brazil Federal Law No. 15,211/2025 (Estatuto da Criança e do Adolescente Digital).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Brazilian Child Protection & Age Assurance Policy complying with Law 15,211/2025.
- **Missing Documentation:** Lacks developer integration guides for combining CPF verification or facial estimation with mobile app onboarding.
- **Missing Code:** Codebase templates lack handlers for processing Brazilian CPF/facial age verification or Google Play Age Signals for Brazil.
- **Missing Disclosure:** Brazilian onboarding UI flows do not display mandatory disclosures explaining age verification methods and ANPD compliance.
- **Missing Logging:** Lacks database schemas for logging age verification outcomes while executing immediate raw identity data destruction.
- **Missing Testing:** Test runner scripts do not simulate Brazilian storefront account creation to verify self-declaration checkboxes are absent.
- **Missing Evidence:** Lacks ANPD compliance filings, formal age verification vendor assessments, or data minimization records.
- **Missing Audit Trail:** Lacks an unalterable audit log recording verification data purges, policy updates, and ANPD inspection records.

---

## 18. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 18.1 Regulatory Overview and Background
The DPDPA 2023 and DPDP Rules 2025 regulate personal data processing in India. Enforces verifiable parental consent via government-backed channels (e.g., DigiLocker) for under-18s and bans behavioral tracking/targeted ads for children.

Official Citation: The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks an India Child Data Processing & Verifiable Parental Consent Policy complying with DPDPA Section 9.
- **Missing Documentation:** Lacks technical manuals for integrating with DigiLocker or virtual tokenized parental consent gateways in India.
- **Missing Code:** Codebase templates lack handlers to disable ad tracking, profiling, and behavioral analytics for Indian minor accounts.
- **Missing Disclosure:** Indian onboarding screens lack multi-lingual consent notices in all 22 Eighth Schedule languages specified under DPDPA.
- **Missing Logging:** Lacks database logging schemas for capturing verifiable parental consent tokens, withdrawal notices, and DPO interactions.
- **Missing Testing:** Automated tests do not check that Indian user profiles marked under-18 completely block ad SDK network calls.
- **Missing Evidence:** Lacks Data Protection Board of India (DPBI) compliance audit filings or Consent Manager registration documentation.
- **Missing Audit Trail:** Lacks an immutable audit trail recording consent grants, consent withdrawals, and annual child data processing audits.

---

## 19. Singapore IMDA Code of Practice for Online Safety

### 19.1 Regulatory Overview and Background
Enforced from 1 April 2026 by IMDA, requires app stores and distribution services to implement age assurance measures, stopping under-18s from accessing age-inappropriate content and destroying age assurance data after use.

Official Citation: IMDA Code of Practice for Online Safety for App Distribution Services (2026).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a Singapore Online Safety & App Distribution Policy aligning with IMDA requirements.
- **Missing Documentation:** Lacks developer guidance for handling Apple and Google Play 18-plus download blocks on Singapore storefronts.
- **Missing Code:** Codebase templates lack age-gating hooks that check for Singapore storefront entitlement or adult verification status.
- **Missing Disclosure:** Singapore store listings and onboarding screens lack required content rating and age restriction disclosures.
- **Missing Logging:** Lacks server-side logging specifications to record age assurance confirmation tokens while enforcing zero raw data retention.
- **Missing Testing:** Test suites do not simulate Singapore region users attempting to access 18-plus content without verified age signals.
- **Missing Evidence:** Lacks completed IMDA Safety Compliance Certificates or annual safety audit report submissions.
- **Missing Audit Trail:** Lacks an unalterable audit trail logging age data destruction, safety policy revisions, and IMDA reporting history.

---

## 20. China Mobile App Filing (MIIT)

### 20.1 Regulatory Overview and Background
Mandated by MIIT (Ministry of Industry and Information Technology), all apps operating in China must complete an ICP/App Filing via a local Chinese partner or entity. Enforces real-name verification, PIPL privacy, data localization, and Banhao licensing for games.

Official Citation: MIIT Notice on the Administrative Filing of Mobile Internet Applications (2023).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** Lacks a China Market Compliance Policy covering MIIT App Filing, PIPL privacy, data localization, and local partner setup.
- **Missing Documentation:** Lacks step-by-step developer manuals for completing MIIT filing through local Chinese cloud and store portals.
- **Missing Code:** Codebase templates lack real-name authentication UI modal components or Chinese ID verification SDK wrappers.
- **Missing Disclosure:** China storefront builds lack required MIIT Filing Number displays in app settings and store metadata listings.
- **Missing Logging:** Lacks database logging specifications for real-name verification tokens and local data storage compliance logs.
- **Missing Testing:** Automated metadata audit scripts (`scripts/metadata-audit.py`) do not check for valid MIIT filing numbers on China builds.
- **Missing Evidence:** Lacks copies of official MIIT App Filing approvals, Chinese business licenses, or PIPL cross-border transfer security assessments.
- **Missing Audit Trail:** Lacks an audit trail recording filing submissions, annual MIIT renewals, and local data residency verification checks.

---

## 21. Consolidated 20-Framework Gap Classification Matrix

This matrix evaluates all 20 regulatory frameworks across all eight mandatory gap categories.
- **Covered:** Comprehensive policy, documentation, code, disclosure, logging, testing, evidence, or audit trail exists in the repository.
- **Partial:** Mentioned with citations and dates, but lacks operational implementation, code blocks, or automated checks.
- **Missing:** Absent from the repository or lacks structured artifacts in that specific category.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA (Trader)** | Covered | Covered | Missing | Partial | Missing | Partial | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA Amended** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CPRA/CCPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. UK ICO Children's Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. Singapore IMDA Code** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China MIIT App Filing** | Partial | Covered | Missing | Partial | Missing | Partial | Missing | Missing |

---

## 22. Actionable Remediation Roadmap

To eliminate all identified regulatory gaps across the playbook, execution must follow a structured 4-phase remediation roadmap:

1. **Phase 1: Complete Missing Framework Coverage (Immediate)**
   - Add EU GPSR detection patterns into `data/rejection-patterns.json` and `agent-os/hooks/app-store-compliance-guard.sh`.
   - Update `data/regulatory-deadlines.json` to verify all 20 deadlines are tracked with accurate jurisdictions and enforcement dates.

2. **Phase 2: Code & Integration Layer Expansion (Short-Term)**
   - Add UI code templates for EU AI Act Article 50 disclosures, EU withdrawal button, and BIPA written release modals.
   - Expand `agent-os/hooks/app-store-compliance-guard.sh` to scan for missing DSA trader metadata, missing GPC webview listeners, and unverified age assurance APIs.

3. **Phase 3: Logging, Evidence & Audit Trail Schemas (Medium-Term)**
   - Create template database schemas for logging law enforcement requests (e-Evidence), parental consent receipts (ASAA/COPPA), and raw identity data purges.
   - Add template compliance evidence files (VPAT/EN 301 549 ACR, DPIA templates, AI Literacy training logs).

4. **Phase 4: Automated Continuous Testing (Long-Term)**
   - Wire `scripts/accessibility-audit.py` and `scripts/metadata-audit.py` directly into CI workflow triggers (`.github/workflows/ci.yml`).
   - Implement mock test runners simulating geo-targeted compliance behavior for EU, US, UK, Brazil, India, Australia, Singapore, and China.

---

## 23. Official Citations & Sources

Every framework analyzed above is cited directly to its official primary source:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive: [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing / Withdrawal: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312 (Federal Register 90 FR 16918)](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions)
- Utah ASAA: [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html)
- California CPRA / CCPA: [Cal. Civ. Code Section 1798.100 et seq.](https://oag.ca.gov/privacy/ccpa)
- Global Privacy Control: [Global Privacy Control Specification](https://globalprivacycontrol.org/)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK ICO Children's Code: [ICO Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/)
- Australia Online Safety Act: [eSafety Industry Regulation](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in/)
