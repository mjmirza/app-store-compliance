# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It evaluates twenty major modern global and regional regulations that bind app developers shipping across the EU, US, UK, Australia, Brazil, India, Singapore, South Korea, China, and global storefronts. It checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight specific compliance categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address online marketplaces, digital products, and complex supply chains.

For digital systems and e-commerce applications, the GPSR mandates displaying product safety warnings, instructions, manufacturer/importer identity, and electronic contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository lacks a written General Product Safety Policy defining EU Responsible Person designation criteria and product safety risk classification rules.
- **Missing Documentation:** No developer checklists or user interface manuals exist for displaying manufacturer identity, postal/electronic contact details, and product safety warnings on EU storefronts.
- **Missing Code:** Mock UI templates and client code omit product safety warning components and manufacturer contact blocks required under Article 19.
- **Missing Disclosure:** Online checkout and product detail templates fail to display mandatory manufacturer details, registered trade names, and electronic contact information.
- **Missing Logging:** No logging schemas exist to capture product safety incidents, safety complaints, or recall notifications.
- **Missing Testing:** Automated tests to verify that product safety disclosures render dynamically for EU end-users are missing.
- **Missing Evidence:** Physical compliance evidence templates, such as EU Responsible Person designation agreements or Safety Technical Documentation sheets, are absent.
- **Missing Audit Trail:** No historical record system tracks updates to product safety disclosures or safety incident resolutions.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 (European Production and Preservation Orders) and Directive (EU) 2023/1544 (legal representatives). Mandatory enforcement begins on 18 August 2026.

Authorities can issue Production Orders directly to service providers in the EU. Standard response time is 10 days, while critical emergency requests require production within a strict 8-hour window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template Law Enforcement Request Policy exists to define internal roles, authorization levels, and execution guidelines for EU judicial orders.
- **Missing Documentation:** Runbooks for executing standard 10-day orders and emergency 8-hour data extractions are missing.
- **Missing Code:** Backend mock scripts lack secure CLI tools or API endpoints to filter, encrypt, and export requested user data within 8 hours.
- **Missing Disclosure:** Privacy policy templates do not disclose to EU users that user data may be produced under Regulation (EU) 2023/1543.
- **Missing Logging:** Database schemas to log incoming production/preservation certificates and verification statuses are missing.
- **Missing Testing:** Integration tests simulating 8-hour emergency data extraction under load do not exist.
- **Missing Evidence:** Sample European Production Order Certificates (EPOC) and EPOC-PR forms are absent.
- **Missing Audit Trail:** Cryptographically verified audit trails recording law enforcement data extractions and transmissions are not implemented.

---

## 3. EU Contract Withdrawal Button Directive

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU, requiring a prominent "withdrawal button" or "withdrawal function" on online interfaces for distance financial services contracts. Member States apply these rules from 19 June 2026. The statutory withdrawal period is 14 days.

Official Citation: Directive (EU) 2023/2673.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no template Consumer Contract Revocation Policy for the 14-day statutory right.
- **Missing Documentation:** UI/UX specification guides for withdrawal button placement, wording, and contrast are absent.
- **Missing Code:** In-app account settings templates lack functional withdrawal button or modal components.
- **Missing Disclosure:** Pre-contract subscription screens omit statutory 14-day withdrawal disclosures.
- **Missing Logging:** Event schemas to log withdrawal clicks, timestamps, and refund triggers are missing.
- **Missing Testing:** Automated end-to-end UI tests for self-service contract revocation without manual intervention are absent.
- **Missing Evidence:** Templates for automated withdrawal confirmation receipts and cancellation notices are missing.
- **Missing Audit Trail:** Immutable records tracking subscription revocation rates and UI revisions are not present.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
State laws including Utah SB 142, Texas SB 2420, Louisiana HB 977, and Alabama HB 161 regulate minors' app downloads, purchases, and updates, requiring verifiable parental consent and immediate deletion of raw verification data.

Official Citations: Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161.

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No written Minor Account Governance Policy exists for handling state-level minor restrictions and age signals.
- **Missing Documentation:** Integration guides for Apple's Declared Age Range API and Google's Play Age Signals API are missing step-by-step native code examples.
- **Missing Code:** Mock mobile apps lack runtime code calling `DeclaredAgeRange` or `com.google.android.play:age-signals` to block minor purchases.
- **Missing Disclosure:** In-app onboarding screens omit state-mandated disclosures regarding age collection and parental consent requirements.
- **Missing Logging:** Backend systems lack logging for parental consent receipts, consent revocations (`RESCIND_CONSENT`), and immediate raw age data deletion triggers.
- **Missing Testing:** Test suites lack automated unit and integration tests asserting minor account restrictions upon receiving minor age signals.
- **Missing Evidence:** Standardized parental consent agreements and data minimization verification logs are missing.
- **Missing Audit Trail:** Audit trail records capturing age signal processing and raw data deletion events are absent.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 requires providers and deployers of AI systems to ensure staff AI literacy, in force since 2 February 2025.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template internal AI Literacy Policy defining competency standards.
- **Missing Documentation:** Developer guides explaining team obligations under Article 4 are missing.
- **Missing Code:** CI helper scripts verifying the presence of an active, up-to-date literacy log are absent.
- **Missing Disclosure:** Public or partner documentation does not disclose corporate adherence to AI literacy standards.
- **Missing Logging:** A centralized training registry (`AI_LITERACY_LOG.md`) tracking staff completions and annual refreshers is missing.
- **Missing Testing:** Pre-commit hooks checking developer training currency before committing AI code changes are missing.
- **Missing Evidence:** Completed sample training logs, course completion certificates, and competency evaluations are absent.
- **Missing Audit Trail:** Version-controlled logs documenting policy reviews and training curriculum updates are missing.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 imposes AI interaction disclosures, synthetic content watermarking, and deepfake disclosures from 2 August 2026.

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** No template AI Transparency and Output Marking Policy exists.
- **Missing Documentation:** Technical implementation guides for machine-readable watermarking (e.g., C2PA) and synthetic text marking are missing.
- **Missing Code:** Backend generation pipelines lack C2PA metadata injection utilities or watermarking helper libraries.
- **Missing Disclosure:** UI chat templates lack immediate notice ("You are chatting with an AI assistant") prior to first user interaction.
- **Missing Logging:** Database schemas to record user exposure to AI transparency notices are absent.
- **Missing Testing:** Test scripts verifying that generated images or text contain machine-readable AI markers are missing.
- **Missing Evidence:** Independent verification reports or algorithmic transparency audit results are absent.
- **Missing Audit Trail:** Records of model changes, prompt disclosures, and watermarking software versions are missing.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 governs gatekeeper mobile platforms in the EU, enabling alternative marketplaces, web distribution, and external payment links (`com.apple.developer.storekit.external-purchase-link`).

Official Citation: Regulation (EU) 2022/1925.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook lacks an EU External Distribution & Alternative Payments Policy.
- **Missing Documentation:** Step-by-step developer manuals for wiring `ExternalPurchaseCustomLink` and reporting monthly sales via External Purchase Server APIs are missing.
- **Missing Code:** Codebase templates omit native wrappers for `ExternalPurchaseCustomLink` and monthly sales reporting API handlers.
- **Missing Disclosure:** System disclosure sheet triggers prior to external offer redirection are missing in mock implementations.
- **Missing Logging:** Transaction logging schemas for tracking non-IAP sales subject to Core Technology Commission reporting are missing.
- **Missing Testing:** Automated tests verifying that StoreKit IAP and external offer links are never co-mingled on the same EU storefront are missing.
- **Missing Evidence:** Proof of notarization files, ADPLA Attachment 14 acceptance records, and monthly reporting receipts are absent.
- **Missing Audit Trail:** Historical logs of external link updates and reporting submission timestamps are missing.

---

## 8. EU Digital Services Act (DSA - Trader Status)

### 8.1 Regulatory Overview and Background
Articles 30 and 31 of Regulation (EU) 2022/2065 require store providers to collect, verify, and publish trader identity and contact details for EU app distribution.

Official Citation: Regulation (EU) 2022/2065.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no corporate Trader Status Governance Policy.
- **Missing Documentation:** Verification guides explaining required DSA documentation (D-U-N-S, payment details, official ID) are absent.
- **Missing Code:** Metadata verification tools fail to check whether DSA trader declarations are complete prior to release.
- **Missing Disclosure:** Product page metadata templates do not include placeholder fields for trader address, email, and phone.
- **Missing Logging:** Systems to record DSA trader status verification timestamps and 2FA verification logs are missing.
- **Missing Testing:** Automated scripts verifying that trader status metadata fields are populated before EU deployment are missing.
- **Missing Evidence:** Official verification certificates, D-U-N-S extract files, and 2FA confirmation records are missing.
- **Missing Audit Trail:** Logs tracking changes to declared trader status or published business details are missing.

---

## 9. European Accessibility Act (EAA - Directive (EU) 2019/882)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 requires mobile applications and e-commerce services reaching EU users to comply with EN 301 549 Chapter 11 (WCAG 2.1 AA) and publish an accessibility statement, applicable from 28 June 2025.

Official Citation: Directive (EU) 2019/882.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository lacks an Accessibility Compliance Policy referencing EN 301 549.
- **Missing Documentation:** Developer manuals explaining EN 301 549 Chapter 11 rules beyond basic WCAG standards are missing.
- **Missing Code:** Dynamic Type, VoiceOver, and high-contrast UI component templates are incomplete across cross-platform samples.
- **Missing Disclosure:** Accessibility Statement templates (EN 301 549 Annex B/C) are missing.
- **Missing Logging:** Automated UI scanners fail to log non-compliant contrast or missing accessibility traits to central telemetry.
- **Missing Testing:** Automated CI pipeline integration for full EN 301 549 screen audits is missing.
- **Missing Evidence:** Formal accessibility audit reports, VPAT documents, and user testing proof are absent.
- **Missing Audit Trail:** Records of historical accessibility remediations and statement revisions are missing.

---

## 10. Amended US COPPA Rule (16 CFR Part 312)

### 10.1 Regulatory Overview and Background
The FTC's Amended COPPA Rule adds biometric identifiers, mandatory written data retention policies, separate third-party disclosure opt-ins, and written information security programs, effective 22 April 2026.

Official Citation: 16 CFR Part 312, 90 FR 16918.

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template Written Data Retention Policy or Information Security Program required under 312.10 and 312.8.
- **Missing Documentation:** Developer instructions on implementing separate opt-in consent for third-party ad sharing in kids' apps are missing.
- **Missing Code:** Age-gating libraries omit separate consent flow controllers for third-party disclosures.
- **Missing Disclosure:** Privacy policy templates lack mandatory disclosures identifying biometric data as PII.
- **Missing Logging:** Database schemas logging verifiable parental consent methods and data deletion timelines are missing.
- **Missing Testing:** Automated unit tests verifying that third-party ad SDKs are disabled prior to explicit consent are missing.
- **Missing Evidence:** Written InfoSec Risk Assessments and Safe Harbor certification evidence are absent.
- **Missing Audit Trail:** Logs capturing annual InfoSec reviews, retention policy updates, and parental consent revocations are missing.

---

## 11. California CCPA / CPRA & CPPA 2026 Regulations

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended requires Global Privacy Control (GPC) support, notice at collection, opt-out of sale/sharing/profiling, and sensitive personal information limits, with automated decision-making rules in 2027.

Official Citation: California Civil Code Title 1.81.5.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no template CCPA/CPRA Privacy & Automated Decision-Making Policy.
- **Missing Documentation:** Implementation guides for handling Global Privacy Control headers (`Sec-GPC`) in webviews and native code are missing.
- **Missing Code:** Native code handlers to translate GPC signals into opt-out flags for ad SDKs are absent.
- **Missing Disclosure:** Notice at Collection and "Limit the Use of My Sensitive Personal Information" UI templates are missing.
- **Missing Logging:** Schemas logging opt-out requests, GPC signals, and consumer rights requests are missing.
- **Missing Testing:** End-to-end integration tests confirming that receiving `Sec-GPC` halts third-party data transmission are missing.
- **Missing Evidence:** Annual CPPA cybersecurity audit certificates and risk assessment filings are absent.
- **Missing Audit Trail:** Immutable records of consumer rights request fulfillments and GPC opt-out events are missing.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
BIPA (740 ILCS 14) mandates written notice, written release, a public retention schedule, and mandatory destruction of biometric identifiers within 3 years.

Official Citation: 740 ILCS 14.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template Biometric Privacy & Retention Policy.
- **Missing Documentation:** Developer guidelines for implementing written consent releases before biometric capture are missing.
- **Missing Code:** UI templates omit explicit biometric consent modal sheets prior to FaceID/TouchID or custom biometric initialization.
- **Missing Disclosure:** In-app screens lack public biometric retention and destruction schedule disclosures.
- **Missing Logging:** Database triggers logging biometric capture consent and automated 3-year destruction schedules are missing.
- **Missing Testing:** Unit tests verifying that biometric capture fails safely if written consent is unconfirmed are missing.
- **Missing Evidence:** Executed written consent records and destruction confirmation certificates are absent.
- **Missing Audit Trail:** Logs documenting biometric data purging events and policy publication history are missing.

---

## 13. US Subscription Cancellation (FTC Negative Option & State Laws)

### 13.1 Regulatory Overview and Background
ROSCA, Section 5 of the FTC Act, and state statutes (California, New York, Massachusetts) require that subscription cancellation be at least as easy as sign-up, prohibiting hard-cancellation mechanics (phone calls, letters).

Official Citations: 15 U.S.C. 8401 (ROSCA), Cal. Bus. & Prof. Code 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository lacks a Negative Option & Simple Subscription Cancellation Policy.
- **Missing Documentation:** Design guides specifying single-tap or simple online cancellation mechanics are missing.
- **Missing Code:** Web and in-app account management templates lack self-service subscription cancellation endpoints.
- **Missing Disclosure:** Pre-subscription disclosures detailing auto-renewal terms and cancellation methods are incomplete.
- **Missing Logging:** Event logging for pre-renewal reminders and cancellation request timestamps is missing.
- **Missing Testing:** Automated UI tests confirming that cancellation can be completed online without human intervention are missing.
- **Missing Evidence:** Records of pre-renewal notification delivery and subscription terms acceptance are absent.
- **Missing Audit Trail:** Logs tracking cancellation flow revisions and customer cancellation rates are missing.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Age Appropriate Design Code mandate Highly Effective Age Assurance, high privacy by default, profiling disabled by default, and mandatory Data Protection Impact Assessments (DPIAs).

Official Citations: UK Online Safety Act 2023, ICO Children's Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template UK Age-Appropriate Design Policy.
- **Missing Documentation:** Manuals detailing Ofcom-approved Highly Effective Age Assurance methods (facial estimation, open banking) are missing.
- **Missing Code:** Native code blocks setting geolocation and profiling off by default for UK minor profiles are missing.
- **Missing Disclosure:** Age-appropriate privacy notices tailored for under-18 comprehension are missing.
- **Missing Logging:** Schemas capturing age-assurance verification status without retaining raw verification identity assets are missing.
- **Missing Testing:** Automated tests verifying that profiling and tracking remain off by default for UK accounts are missing.
- **Missing Evidence:** Formally completed ICO Data Protection Impact Assessments (DPIAs) and Ofcom risk assessment records are missing.
- **Missing Audit Trail:** Version-controlled records of DPIA reviews and age-assurance method updates are missing.

---

## 15. Australia Online Safety Act & Digital ECA (Brazil)

### 15.1 Regulatory Overview and Background
Australia's Social Media Minimum Age Act 2024 and Brazil's Digital ECA (Law 15,211/2025) prohibit self-declaration checkboxes, requiring verified age assurance and immediate destruction of verification data.

Official Citations: Australia Online Safety Amendment Act 2024, Brazil Law 15,211/2025.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository carries no Age Assurance & Verification Data Destruction Policy for Australia and Brazil.
- **Missing Documentation:** Guides outlining accepted verification methods (CPF checks, facial estimation, document checks) are missing.
- **Missing Code:** Mobile client code fails to ringfence age verification data or invoke automated deletion endpoints post-verification.
- **Missing Disclosure:** In-app notices explaining mandatory age verification and immediate data destruction are missing.
- **Missing Logging:** Telemetry logging post-verification data purging events without storing personal identity details is missing.
- **Missing Testing:** Integration tests verifying that unverified accounts are blocked from adult content in Brazil and Australia are missing.
- **Missing Evidence:** ANPD/eSafety compliance risk assessments and third-party age assurance audit reports are missing.
- **Missing Audit Trail:** Audit logs recording verification attempts and post-verification data destruction timestamps are missing.

---

## 16. India Digital Personal Data Protection Act (DPDPA 2023)

### 16.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 require verifiable parental consent via government-backed systems (DigiLocker) for under-18s, prohibiting behavioral tracking and targeted ads.

Official Citation: India DPDPA 2023, G.S.R. 846(E).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no template DPDPA Compliance & Minor Data Protection Policy.
- **Missing Documentation:** Guides on integrating with registered Consent Managers and DigiLocker parental verification are missing.
- **Missing Code:** Native wrappers for Indian Consent Manager APIs and targeted ad suppression for under-18s are missing.
- **Missing Disclosure:** Multilingual consent notices in all 22 Eighth Schedule Indian languages are missing.
- **Missing Logging:** Database logging schemas for tracking parental consent tokens and Consent Manager interaction IDs are missing.
- **Missing Testing:** Automated tests verifying that behavioral ad tracking is disabled for Indian minor profiles are missing.
- **Missing Evidence:** Data Protection Board registration evidence and Consent Manager integration certifications are missing.
- **Missing Audit Trail:** Logs documenting consent withdrawals and Data Principal grievance redressal responses are missing.

---

## 17. Singapore IMDA Code of Practice for Online Safety

### 17.1 Regulatory Overview and Background
The IMDA Code of Practice for Online Safety requires app distribution services and platforms to enforce age assurance screening users under 18 from downloading age-inappropriate apps.

Official Citation: IMDA Code of Practice for Online Safety.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no Singapore Online Safety & Age Assurance Policy.
- **Missing Documentation:** Developer guides explaining IMDA age-rating alignment and store age signals are missing.
- **Missing Code:** Mobile app templates lack logic to handle Singapore storefront age restriction signals.
- **Missing Disclosure:** In-app content warning disclosures for Singapore users are missing.
- **Missing Logging:** Logging schemas capturing age verification results while ensuring immediate deletion of verification data are missing.
- **Missing Testing:** Unit tests verifying that 18-plus rated content is blocked on Singapore storefronts without valid age signals are missing.
- **Missing Evidence:** IMDA safety compliance declarations and safety contact appointment records are missing.
- **Missing Audit Trail:** Logs tracking age-assurance policy updates and harm reporting resolutions are missing.

---

## 18. South Korea Telecommunications Business Act & PIPA

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app billing support (`com.apple.developer.storekit.external-purchase` for KR), while PIPA amendments establish CEO accountability and chief privacy officer requirements.

Official Citations: KOR TBA Article 22-9, KOR PIPA Act No. 21445.

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The repository lacks a South Korea Alternative Billing & PIPA Governance Policy.
- **Missing Documentation:** Step-by-step technical guides for building Korea-only binaries, approved payment gateway integration (KCP, Toss, Inicis), and monthly 26% fee reporting are missing.
- **Missing Code:** Native code templates for the mandatory Korean alternative payment modal sheet and server-side reporting APIs are missing.
- **Missing Disclosure:** Pre-payment modal disclosures informing users that Apple/Google protection features do not apply are missing.
- **Missing Logging:** Database logging for alternative payment transaction amounts, VAT calculations, and monthly commission reports is missing.
- **Missing Testing:** Integration tests verifying that the Korea external payment entitlement does not leak into other storefront binaries are missing.
- **Missing Evidence:** KCC compliance filings, approved payment gateway contracts, and CEO accountability declarations are missing.
- **Missing Audit Trail:** Historical logs of monthly sales reporting submissions and remittance receipts are missing.

---

## 19. China Mobile App Filing (MIIT) & CAC Regulations

### 19.1 Regulatory Overview and Background
China's MIIT Mobile App Filing, PIPL, and CAC Interim Measures for AI Anthropomorphic Services require local entity filing, real-name verification, data localization, and banning virtual companion services for minors.

Official Citations: MIIT ICP App Filing Rules, CAC Order No. 21.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:** The playbook carries no China App Filing & CAC Minor Protection Policy.
- **Missing Documentation:** Technical manuals detailing MIIT ICP filing, local entity partnership setup, and CAC AI service filing steps are missing.
- **Missing Code:** Code templates for China real-name verification (ID/phone check) and automatic minors mode toggles are missing.
- **Missing Disclosure:** Mandatory MIIT filing number display on app splash screens and setting pages is missing in UI templates.
- **Missing Logging:** Localized logging schemas capturing real-name verification states without cross-border data transfer are missing.
- **Missing Testing:** Integration tests asserting that companion AI features are disabled when a minor profile in China is detected are missing.
- **Missing Evidence:** Official MIIT ICP filing certificates, Banhao game licenses, and CAC security assessment filings are missing.
- **Missing Audit Trail:** Logs capturing bi-annual PIPL personal information compliance audits and real-name system updates are missing.

---

## 20. Consolidated Gap Classification Matrix

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **US state ASAA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **EU DMA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **EU DSA Trader** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **European Accessibility Act** | Partial | Covered | Partial | Missing | Missing | Missing | Missing | Missing |
| **Amended US COPPA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **California CCPA/CPRA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **Illinois BIPA** | Partial | Covered | Missing | Missing | Missing | Missing | Missing | Missing |
| **US Negative Option** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **UK OSA & Children's Code**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **Australia & Brazil ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **India DPDPA 2023** | Partial | Covered | Missing | Missing | Missing | Missing | Missing | Missing |
| **Singapore IMDA Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **South Korea TBA / PIPA** | Partial | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **China MIIT & CAC AI** | Partial | Covered | Missing | Missing | Missing | Missing | Missing | Missing |

---

## 21. Conclusion and Remediation Priorities

This comprehensive audit reveals that while the repository provides excellent legal documentation and rejection pattern coverage, significant implementation gaps remain across the codebase layer.

In priority order:
1. **Logging & Audit Trail:** Build standardized logging schemas and audit trail utilities for legal requests, consent receipts, age signal processing, and data deletions.
2. **Code & UI Templates:** Implement production-grade UI components for the EU Withdrawal Button, GPSR product safety cards, C2PA watermarking helpers, and store age signal APIs (`DeclaredAgeRange` / Play Age Signals API).
3. **Automated Testing:** Develop automated integration tests verifying that location-based regulatory disclosures and minor access restrictions render correctly.
4. **Evidence Templates:** Supply formal compliance evidence templates (DPIAs, VPATs, InfoSec Risk Assessments, and EPOC forms) for developer customization.

## 22. Sources

Primary official regulatory sources cited:
- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Regulation, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj)
- EU e-Evidence Directive, [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US FTC Amended COPPA Rule, [16 CFR Part 312, 90 FR 16918](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- Illinois BIPA, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- India DPDPA, [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
