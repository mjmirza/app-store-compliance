# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major regulatory frameworks that bind app developers shipping into the European Union, the United States, the United Kingdom, Australia, Brazil, Canada, India, Singapore, South Korea, China, and other global markets, and checks honestly how far this repository already carries each one, what it only mentions in passing, and what it does not cover at all.

Read it as a work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is checked across eight core compliance gap categories:
- Missing Policy
- Missing Documentation
- Missing Code
- Missing Disclosure
- Missing Logging
- Missing Testing
- Missing Evidence
- Missing Audit Trail

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges of online marketplaces, digital products, and complex supply chains.

The GPSR applies to non-food consumer products placed on the EU market. For digital systems and software, the GPSR mandates that online interfaces display product safety warnings, instructions, manufacturer and importer identity, and electronic contact details.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook gives a developer no template policy to evaluate whether their digital listing falls inside Regulation (EU) 2023/988 or to designate an EU Responsible Person.
- **Missing Documentation:**
  The repository lacks specific developer checklists or instructional manuals on structuring product listings to display GPSR-mandated safety warnings, manufacturer details, and technical instructions.
- **Missing Code:**
  The automated compliance guard and detection recipes lack rules or patterns to scan codebase files for GPSR elements. Mock user interfaces do not contain code blocks for displaying manufacturer identity or product safety warnings on EU storefronts.
- **Missing Disclosure:**
  Online interface templates do not provide placeholder components or guidance for displaying the manufacturer's name, registered trade name, postal address, and electronic address as required under Article 19 of the GPSR.
- **Missing Logging:**
  There are no architectural provisions or schemas for logging product safety incidents, recalls, or corrective actions.
- **Missing Testing:**
  No automated tests exist to verify that online interface elements dynamically display required product safety information or manufacturer details based on geographic location.
- **Missing Evidence:**
  The repository lacks physical templates of compliance evidence, such as Technical Documentation sheets, safety risk assessments, or proof of a designated Responsible Person in the EU.
- **Missing Audit Trail:**
  There is no audit trail or historical record system to track when product safety policies were updated, when safety warnings were reviewed, or when corrective measures were implemented.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining the designation of an EU-based Responsible Person.
2. Incorporate GPSR-specific metadata requirements into `data/rejection-patterns.json` and `docs/PRE-SUBMISSION-CHECKLIST.md`.
3. Add UI templates in the references directory demonstrating compliant product detail pages including safety warning labels and electronic contact details.
4. Integrate an automated test runner script verifying the presence of safety disclosures prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence in criminal matters and Directive (EU) 2023/1544 on the appointment of legal representatives. The mandatory compliance enforcement date is 18 August 2026.

This framework allows judicial authorities of an EU Member State to issue European Production Orders (EPOs) or European Preservation Orders directly to service providers offering services in the EU. The default compliance window is 10 days, but in emergency cases, data must be produced within an 8-hour timeline.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Law Enforcement Request Policy for handling European Production Orders or designated legal representatives.
- **Missing Documentation:**
  The repository lacks concrete operational runbooks for executing 10-day standard orders and 8-hour emergency response protocols.
- **Missing Code:**
  There are no automated scripts or secure API endpoints in mock backends to assist in securely exporting, filtering, and packaging user data in response to a valid legal order.
- **Missing Disclosure:**
  Privacy Policy templates fail to explicitly disclose to EU users that data may be preserved or disclosed to European law enforcement under Regulation (EU) 2023/1543.
- **Missing Logging:**
  The repository does not contain database schemas or logging systems designed to track incoming law enforcement requests, verification statuses, or data releases.
- **Missing Testing:**
  There are no integration tests or validation flows simulating the rapid 8-hour emergency retrieval and secure packaging of user data.
- **Missing Evidence:**
  The repository lacks verified templates of European Production Order certificates (EPOC) or European Preservation Order certificates (EPOC-PR) for compliance verification.
- **Missing Audit Trail:**
  A secure, unalterable audit trail system to record administrative interactions, data extractions, and transmissions made during a legal request is absent.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol establishing roles, responsibilities, and secure communication channels for executing EPOs.
2. Formally designate an EU establishment or legal representative before the 18 August 2026 deadline.
3. Build secure backend scripts to automate extraction and encryption of requested user datasets within the 8-hour emergency window.
4. Establish a tamper-proof audit trail logging incoming certificates, verification checks, extractions, and transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
The Distance Marketing of Financial Services Directive (EU) 2023/2673 amends the Consumer Rights Directive (Directive 2011/83/EU). It requires a prominent, easily accessible withdrawal button on the online interface for distance contracts concluded electronically. Member States apply these rules from 19 June 2026.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for the 14-day statutory withdrawal right or criteria separating mandatory financial services from optional consumer default implementations.
- **Missing Documentation:**
  The repository does not provide UI design guidelines or checklists specifying placement, size, prominence, and terminology for a compliant withdrawal button.
- **Missing Code:**
  Front-end user interface templates and billing mock codes do not contain a functional implementation of a withdrawal button or withdrawal modal sheet.
- **Missing Disclosure:**
  Subscription registration interfaces do not prominently disclose the 14-day statutory right of withdrawal or provide an in-app link explaining contract revocation terms.
- **Missing Logging:**
  There are no logging mechanisms designed to capture when a user clicks the withdrawal button, the timestamp, confirmation of termination, or initiation of refund flows.
- **Missing Testing:**
  No automated UI or unit tests exist to verify that the withdrawal flow can be completed without administrative friction or customer service intervention.
- **Missing Evidence:**
  The repository lacks templates of withdrawal forms, cancellation confirmation receipts, or standardized documentation to prove compliance during consumer disputes.
- **Missing Audit Trail:**
  A systematic audit trail tracking historical cancellation and refund rates, compliance audits of subscription flows, and updates to the cancellation interface is not implemented.

### 3.3 Remediation and Action Plan
1. Formulate a Consumer Cancellation and Refund Policy aligned with Directive (EU) 2023/2673.
2. Develop a prominent "Withdrawal Button" component within account settings of EU-facing subscription templates.
3. Establish robust logging of cancellation requests, timestamps, and refund transactions in a dedicated database schema.
4. Implement automated end-to-end UI tests to verify frictionless contract termination.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
The US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minors' access to mobile applications, in-app purchases, and content updates. Developers must process age categories via Apple's Declared Age Range API or Google's Play Age Signals API, obtain verifiable parental consent, and delete raw age verification data immediately.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook has no template minors policy specifying how to detect users in Texas, Utah, Louisiana, or Alabama and handle minor accounts.
- **Missing Documentation:**
  Checklists lack precise developer guidelines for integrating Apple's Declared Age Range API and Google's Play Age Signals API within multi-platform projects.
- **Missing Code:**
  Mock client implementations do not integrate with `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict app access dynamically.
- **Missing Disclosure:**
  Onboarding flows do not display required state disclosures explaining that user age categories are requested to comply with state accountability laws and that parental consent is mandatory for minors.
- **Missing Logging:**
  There is no backend system to log receipt of parental consent, consent revocations (`RESCIND_CONSENT`), or immediate deletion of raw age-verification documents.
- **Missing Testing:**
  Test suites do not include automated integration tests verifying that minor accounts are blocked from premium features or purchases without consent signals.
- **Missing Evidence:**
  The repository lacks templates of parental consent agreements, identity verification logs, or data minimization records.
- **Missing Audit Trail:**
  An immutable audit trail recording the rollout of age-assurance features, consent policy changes, and records of immediate verification data deletion is absent.

### 4.3 Remediation and Action Plan
1. Create a Minor Age Assurance Policy specifying state-level identification and child data minimization.
2. Implement cross-platform native hooks querying Apple's Declared Age Range API and Google's Play Age Signals API during onboarding.
3. Build database procedures to purge raw age-verification data immediately after age confirmation.
4. Establish unit tests verifying that minor age bands disable in-app billing until parental consent is verified.

---

## 5. EU AI Act (Article 4 AI Literacy & Article 50 Transparency)

### 5.1 Regulatory Overview and Background
Regulation (EU) 2024/1689 (EU AI Act) establishes mandatory obligations. Article 4 (live since 2 February 2025) requires AI literacy for staff operating AI systems. Article 50 (effective 2 August 2026) dictates transparency: informing users they interact with AI (Article 50(1)), marking synthetic outputs in machine-readable format (Article 50(2)), and disclosing deepfakes (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template AI Literacy Policy (Article 4) or AI Transparency Policy (Article 50).
- **Missing Documentation:**
  Documentation lacks technical developer instructions on machine-readable watermarking (C2PA), synthetic media labeling, or deepfake disclosures.
- **Missing Code:**
  Codebase templates do not include helper classes or utilities to inject machine-readable watermarks or C2PA metadata into generated assets.
- **Missing Disclosure:**
  Chat and generation UI templates do not display immediate notices ("You are interacting with an AI system") at first user exposure.
- **Missing Logging:**
  There are no database schemas to record that AI transparency warnings were displayed to specific user sessions.
- **Missing Testing:**
  Test scripts do not verify the presence of synthetic media markers or check that generated outputs are machine-detectable.
- **Missing Evidence:**
  The repository lacks templates for AI training logs (`AI_LITERACY_LOG.md`) or proof of content moderation evaluations.
- **Missing Audit Trail:**
  An unalterable audit trail recording model choices, vendor audits, and modifications to transparency disclosures is missing.

### 5.3 Remediation and Action Plan
1. Formulate corporate AI Literacy and AI Transparency Policies.
2. Add explicit notices ("You are chatting with an AI assistant") inside conversational interface templates.
3. Implement C2PA metadata injection inside synthetic media generation pipelines.
4. Establish `AI_LITERACY_LOG.md` and automated CI checks verifying annual training reviews.

---

## 6. EU Digital Markets Act (DMA)

### 6.1 Regulatory Overview and Background
Regulation (EU) 2022/1925 (DMA) regulates gatekeeper platforms. In the EU, Apple supports Web Distribution, alternative app marketplaces, alternative payments, non-WebKit browser engines, and NFC HCE. Effective 1 October 2026, Apple introduced Attachment 14 replacing CTF with the Core Technology Commission (CTC) of 5% for digital transactions outside the App Store.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template policy for evaluating DMA business models, alternative distribution risks, or Attachment 14 acceptance procedures.
- **Missing Documentation:**
  Documentation lacks step-by-step guidance on implementing `ExternalPurchaseCustomLink`, monthly reporting via External Purchase Server API, and alternative marketplace entitlement requirements.
- **Missing Code:**
  The repository contains no code modules integrating `ExternalPurchaseCustomLink` or handling monthly server API transaction reporting.
- **Missing Disclosure:**
  UI templates lack the required system-provided external purchase disclosure sheet explaining that transactions occur with the developer, not Apple.
- **Missing Logging:**
  There are no database schemas or server-side logging systems to track external purchase transactions for monthly Apple reporting.
- **Missing Testing:**
  No unit or UI tests exist to verify that StoreKit IAP and external offer links are never co-mingled on the same EU storefront.
- **Missing Evidence:**
  The repository lacks template records verifying Account Holder acceptance of Attachment 14 or proof of alternative marketplace eligibility.
- **Missing Audit Trail:**
  An audit trail system recording monthly external purchase reporting submissions and commission calculations is absent.

### 6.3 Remediation and Action Plan
1. Create a DMA Entitlements and External Payments Policy.
2. Implement native wrapper functions calling `ExternalPurchaseCustomLink` for all EU external offer URLs.
3. Build backend logging and automated reporting scripts for the External Purchase Server API.
4. Add automated CI checks verifying entitlement declarations and StoreKit/external link isolation.

---

## 7. EU Digital Services Act (DSA)

### 7.1 Regulatory Overview and Background
Regulation (EU) 2022/2065 (DSA) regulates intermediary services. Articles 30 and 31 require app stores to verify and display trader status, business address, phone, and email for developers distributing apps in the EU. Dark patterns and illegal content handling are also regulated.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template DSA Trader Status Policy to guide developers in declaring trader vs. non-trader status in App Store Connect and Google Play Console.
- **Missing Documentation:**
  Documentation lacks step-by-step instructions on completing DSA two-factor verification, uploading business registration documents, and maintaining public contact metadata.
- **Missing Code:**
  There are no automated metadata scripts checking whether trader declarations are complete prior to release.
- **Missing Disclosure:**
  Templates do not include standard trader disclosure blocks for in-app contact screens or web storefront listings.
- **Missing Logging:**
  There is no system for logging user reports of illegal content or tracking response timelines as required for hosting providers.
- **Missing Testing:**
  No automated lints check store metadata files to ensure trader contact details match App Store Connect declarations.
- **Missing Evidence:**
  The repository lacks templates for trader verification documentation or proof of business registration uploads.
- **Missing Audit Trail:**
  An audit trail system tracking updates to trader status and responses to notice-and-action mechanisms is absent.

### 7.3 Remediation and Action Plan
1. Draft a DSA Compliance Policy defining trader status criteria under EU consumer law.
2. Expand `scripts/metadata-audit.py` to audit DSA trader declarations and contact metadata.
3. Provide standard UI components for displaying trader verification details in app account settings.
4. Establish a notice-and-action logging system for user-generated content applications.

---

## 8. European Accessibility Act (EAA)

### 8.1 Regulatory Overview and Background
Directive (EU) 2019/882 (EAA) became applicable on 28 June 2025. It mandates accessibility for mobile applications and e-commerce services reaching EU consumers. Technical compliance requires meeting harmonized standard EN 301 549 (specifically Chapter 11 for mobile apps), built on WCAG 2.1 Level AA.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no corporate European Accessibility Policy establishing EN 301 549 Chapter 11 compliance standards.
- **Missing Documentation:**
  Documentation focuses on basic WCAG guidelines but lacks step-by-step developer manuals specifically addressing EN 301 549 Chapter 11 mobile requirements (e.g., non-web software, biometric accessibility, screen reader traits).
- **Missing Code:**
  Existing UI code samples lack complete VoiceOver/TalkBack traits, dynamic scaling containers, and high-contrast color variables.
- **Missing Disclosure:**
  The repository provides no template for a legally compliant Accessibility Statement (EN 301 549 Annex B/C) explaining app accessibility features and feedback mechanisms.
- **Missing Logging:**
  There is no mechanism or logging schema to capture user accessibility feedback, issues, or assist requests.
- **Missing Testing:**
  While `scripts/accessibility-audit.py` exists, it does not validate EN 301 549 Chapter 11 non-web software specific criteria.
- **Missing Evidence:**
  The repository lacks templates for formal Accessibility Conformance Reports (VPAT / EN 301 549 ACR) required during regulatory audits.
- **Missing Audit Trail:**
  An immutable audit trail documenting annual accessibility testing cycles, user feedback resolutions, and code accessibility remediation is missing.

### 8.3 Remediation and Action Plan
1. Adopt an EN 301 549 Accessibility Policy and publish an in-app Accessibility Statement template.
2. Enhance `scripts/accessibility-audit.py` to check EN 301 549 Chapter 11 mobile rules.
3. Add accessible UI components supporting VoiceOver, TalkBack, Dynamic Type, and Reduce Motion.
4. Create an Accessibility Conformance Report (ACR) template in `templates/`.

---

## 9. US Children's Online Privacy Protection Act (COPPA & Amended Rule)

### 9.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) regulates online collection of personal information from children under 13. The FTC's amended COPPA Rule (90 FR 16918, effective 23 June 2025, compliance mandatory by 22 April 2026) expands personal information to include biometrics and government IDs, requires separate opt-in consent for third-party disclosures, and mandates written retention policies (312.10) and written security programs (312.8).

Official Citation: 16 CFR Part 312 (Federal Trade Commission).

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template COPPA Written Data Retention Policy (312.10) and a Written Information Security Program (WISP, 312.8).
- **Missing Documentation:**
  Checklists do not cover the 2026 amended COPPA rules regarding biometric identifiers, separate third-party disclosure consent, and knowledge-based parental verification.
- **Missing Code:**
  Code templates do not support separate opt-in consent toggles for third-party ad sharing vs. core app functionality for child users.
- **Missing Disclosure:**
  Direct notice templates to parents fail to list biometric identifiers and government IDs as personal data categories under the amended rule.
- **Missing Logging:**
  There is no logging system to record parental consent methods, timestamps, scope of consent (internal vs. third-party), or consent revocations.
- **Missing Testing:**
  Test suites do not verify that child accounts are prevented from transmitting personal data to ad vendors when core consent is granted but third-party consent is withheld.
- **Missing Evidence:**
  The repository provides no template for annual COPPA risk assessments or parental identity verification logs.
- **Missing Audit Trail:**
  An audit trail tracking the complete lifecycle of child personal data from collection to mandatory deletion is absent.

### 9.3 Remediation and Action Plan
1. Draft a COPPA Written Data Retention Policy and WISP template.
2. Implement separate consent flag handling in user profile models (core vs. third-party disclosure).
3. Update onboarding UI templates with compliant parental notice modals listing biometrics.
4. Add automated tests verifying data transmission blockage when third-party consent is absent.

---

## 10. California Privacy Framework (CCPA / CPRA / CPPA / AADC / DROP)

### 10.1 Regulatory Overview and Background
The California Consumer Privacy Act (CCPA), as amended by CPRA, and CPPA regulations establish strict privacy rules. Key obligations include Notice at Collection, "Do Not Sell or Share My Personal Information", Global Privacy Control (GPC) signal honor, "Limit the Use of My Sensitive Personal Information", automated decision-making opt-outs (effective 1 January 2027), and data broker DROP registration.

Official Citations: Cal. Civ. Code § 1798.100 et seq.; CPPA Regulations (2026).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook lacks a template California Privacy Rights Policy covering CCPA/CPRA consumer request processing and automated decision-making opt-outs.
- **Missing Documentation:**
  Documentation lacks developer guidelines for detecting and processing Global Privacy Control (`Sec-GPC`) headers in webviews and native app equivalents.
- **Missing Code:**
  There are no code helpers or native modules to parse `Sec-GPC` or expose "Do Not Sell/Share" and "Limit Sensitive PI" toggles in app settings.
- **Missing Disclosure:**
  In-app Notice at Collection templates do not categorize sensitive personal information or specify retention periods per category as required by CPRA.
- **Missing Logging:**
  There is no system to log CCPA consumer requests (know, delete, correct, opt-out) and track the statutory 45-day response window.
- **Missing Testing:**
  No automated tests exist to verify that setting the GPC signal automatically disables third-party tracking SDKs.
- **Missing Evidence:**
  The repository lacks templates for Data Protection Impact Assessments (DPIA) required for high-risk processing under CPPA rules.
- **Missing Audit Trail:**
  An immutable log of opt-out requests, GPC signal receipts, and data deletion fulfillments is not present.

### 10.3 Remediation and Action Plan
1. Create a California Privacy Compliance Policy template.
2. Build native and webview wrapper utilities to parse GPC signals and dynamically disable tracking SDKs.
3. Update Notice at Collection UI templates with category-specific retention disclosures.
4. Establish a consumer privacy request logging schema with 45-day deadline tracking.

---

## 11. Illinois Biometric Information Privacy Act (BIPA)

### 11.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14/) imposes strict rules on capturing biometric identifiers (fingerprints, face geometry, voiceprints). Requirements include written notice, written release before capture, a publicly available retention schedule, destruction within 3 years, and prohibition on sale. SB 2979 (effective 2 August 2024) clarifies that repeated capture of the same biometric constitutes a single violation.

Official Citation: 740 ILCS 14/ (Illinois General Assembly).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Biometric Information Privacy Policy outlining notice, consent, and retention rules.
- **Missing Documentation:**
  Developer guidelines do not detail BIPA requirements for local device biometric authentication (Face ID/Touch ID) vs. raw biometric data capture.
- **Missing Code:**
  Codebase templates do not include written release modal sheets or consent capture flows prior to initializing biometric SDKs.
- **Missing Disclosure:**
  Onboarding flows lack BIPA-compliant written notices explaining the specific purpose and length of term for biometric data storage.
- **Missing Logging:**
  There is no database schema to log written consent releases, consent timestamps, or automated 3-year destruction triggers.
- **Missing Testing:**
  Test suites do not verify that biometric data capture is blocked until written consent is affirmatively logged.
- **Missing Evidence:**
  The repository lacks templates for publicly accessible biometric retention and destruction schedules.
- **Missing Audit Trail:**
  An immutable audit trail recording consent acquisition, data usage, and permanent deletion of biometric artifacts is absent.

### 11.3 Remediation and Action Plan
1. Draft a BIPA Policy and Public Retention Schedule template.
2. Create UI consent modal components requiring explicit opt-in prior to biometric capture.
3. Implement automated data destruction cron scripts executing the 3-year cleanup rule.
4. Add automated CI tests verifying biometric SDK initialization gates.

---

## 12. US Subscription Cancellation (Negative Option Rule / ROSCA)

### 12.1 Regulatory Overview and Background
While the FTC's 2024 Negative Option Rule amendment was vacated in July 2025 on procedural grounds, ROSCA (15 U.S.C. § 8401), FTC Act Section 5, and state laws (California, New York, Massachusetts) enforce strict subscription cancellation rules. Subscriptions billed outside App Store IAP or Play Billing must provide a simple, online cancellation mechanism at least as easy as sign-up, with clear pre-consent disclosures.

Official Citations: 15 U.S.C. § 8401 (ROSCA); Cal. Bus. & Prof. Code § 17600.

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Subscription Cancellation Policy for web-billed or multi-platform subscriptions.
- **Missing Documentation:**
  Checklists do not detail the legal requirement for frictionless self-service cancellation paths on web and companion account portals.
- **Missing Code:**
  Mock billing applications do not include self-service online cancellation flows or one-click subscription termination endpoints.
- **Missing Disclosure:**
  Subscription purchase UI templates fail to display full recurring billing terms, cancellation deadlines, and renewal amounts immediately adjacent to the call to action.
- **Missing Logging:**
  There are no backend logging schemas to record subscription cancellation requests, timestamps, confirmation receipts, or effective termination dates.
- **Missing Testing:**
  No automated end-to-end tests verify that web subscription cancellation can be completed without contacting customer support.
- **Missing Evidence:**
  The repository lacks templates of cancellation confirmation emails or dispute evidence documentation.
- **Missing Audit Trail:**
  An audit trail tracking changes to subscription billing terms, cancellation rates, and flow modifications is absent.

### 12.3 Remediation and Action Plan
1. Formulate a Subscription Transparency and Easy Cancellation Policy.
2. Build self-service cancellation components in web and account portal templates.
3. Update subscription checkout UI templates with adjacent recurring billing terms disclosures.
4. Implement automated UI tests proving one-click online cancellation.

---

## 13. UK Online Safety Act 2023 & ICO Children's Code

### 13.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and the ICO Age Appropriate Design Code (Children's Code) establish strict child safety obligations. Requirements include Highly Effective Age Assurance (facial age estimation, open banking, digital ID), CSEA reporting to the NCA portal, and 15 design standards (high privacy by default, profiling off, geolocation off, DPIA).

Official Citations: UK Online Safety Act 2023; ICO Age Appropriate Design Code.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template UK Online Safety Policy or Children's Code Compliance Framework.
- **Missing Documentation:**
  Documentation lacks developer guidelines on integrating UK-approved age assurance methods or completing a Children's Code Data Protection Impact Assessment (DPIA).
- **Missing Code:**
  Code templates do not include default configurations that turn off geolocation, profiling, and targeted recommendations for UK minor users.
- **Missing Disclosure:**
  UI templates do not display age-appropriate transparency notices explaining data usage in child-friendly language.
- **Missing Logging:**
  There is no logging system to record CSEA reports submitted to the NCA portal or age verification outcome logs.
- **Missing Testing:**
  No automated tests exist to verify that child accounts default to maximum privacy settings upon account creation.
- **Missing Evidence:**
  The repository lacks templates for an ICO Children's Code DPIA or Ofcom risk assessment documentation.
- **Missing Audit Trail:**
  An immutable audit trail recording child safety risk assessments, feature changes, and age verification data destruction is missing.

### 13.3 Remediation and Action Plan
1. Draft a UK Children's Code Policy and DPIA template.
2. Implement high-privacy default profiles for minor accounts (geolocation off, profiling off).
3. Create child-friendly privacy disclosure components.
4. Add automated CI checks verifying default privacy settings for child account profiles.

---

## 14. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 14.1 Regulatory Overview and Background
The Online Safety Amendment (Social Media Minimum Age) Act 2024 (effective 10 December 2025) requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts. Additionally, eSafety Industry Codes (Schedule 7) require app stores and developers to apply age assurance, ringfence age data, and block 18+ app downloads.

Official Citations: Online Safety Act 2021; Social Media Minimum Age Act 2024 (Cth).

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Social Media Minimum Age Policy or Australian Industry Code compliance framework.
- **Missing Documentation:**
  Documentation lacks developer instructions on implementing eSafety-compliant waterfall age assurance or ringfencing age verification data.
- **Missing Code:**
  Mock social media platforms do not contain code blocks restricting under-16 account registration or enforcing 18+ download blocks for Australia.
- **Missing Disclosure:**
  Onboarding flows lack required disclosures explaining that age verification data is collected solely for age restriction compliance and will be destroyed.
- **Missing Logging:**
  There are no logging mechanisms to record age verification attempts, pass/fail status, or immediate data destruction timestamps.
- **Missing Testing:**
  Test suites do not verify that under-16 users are blocked from account creation on age-restricted social platforms.
- **Missing Evidence:**
  The repository lacks templates for eSafety safety risk assessments or age data ringfencing proof.
- **Missing Audit Trail:**
  An audit trail documenting the lifecycle and deletion of age verification tokens is absent.

### 14.3 Remediation and Action Plan
1. Formulate an Australian Age Assurance and Data Ringfencing Policy.
2. Implement waterfall age verification logic in account creation flows.
3. Build database functions ensuring immediate destruction of raw age verification artifacts.
4. Add automated integration tests validating under-16 registration blocks.

---

## 15. Brazil Digital ECA (Law 15,211/2025 & Decreto 12.880)

### 15.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, regulated by Decreto n. 12.880 of 18 March 2026) mandates verified age assurance (document verification, facial estimation, CPF database check) for online applications, prohibiting self-declaration checkboxes. ANPD enforces rules starting 17 March 2026 / January 2027, including 18+ download blocks and parental authorization for minors.

Official Citations: Lei n. 15,211/2025; Decreto n. 12.880 (Presidência da República).

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Brazil Digital ECA Compliance Policy or Child Protection Framework.
- **Missing Documentation:**
  Documentation lacks technical instructions on integrating CPF database verification, facial estimation SDKs, or ANPD age assurance guidelines.
- **Missing Code:**
  Mock applications do not include integration code for Brazil age assurance or Play Age Signals API handling for Brazilian accounts.
- **Missing Disclosure:**
  In-app disclosures do not inform Brazilian users of mandatory age verification under Law 15,211/2025 or explain guardian consent procedures.
- **Missing Logging:**
  There is no logging system to capture guardian consent grants, consent contestations, or age signal updates from Play services.
- **Missing Testing:**
  No automated tests exist to verify that Brazilian accounts lacking verified age signals are restricted from 18+ content and loot-box mechanics.
- **Missing Evidence:**
  The repository lacks templates for ANPD age assurance compliance reports or guardian consent logs.
- **Missing Audit Trail:**
  An immutable audit trail tracking age verification requests, contestations, and guardian authorization grants is missing.

### 15.3 Remediation and Action Plan
1. Adopt a Brazil Digital ECA Compliance Policy.
2. Integrate Play Age Signals API and Declared Age Range API for Brazilian storefronts.
3. Implement guardian authorization flow templates for minor accounts.
4. Add unit tests verifying 18+ content blocking without valid age verification.

---

## 16. India Digital Personal Data Protection Act (DPDPA 2023 & Rules 2025)

### 16.1 Regulatory Overview and Background
The Digital Personal Data Protection Act 2023 (Act No. 22 of 2023) and DPDP Rules 2025 (G.S.R. 846(E), 13 November 2025) establish India's data privacy framework. Key rules include verifiable parental consent before processing data of minors under 18, prohibition of behavioral tracking or targeted ads to children, consent notices in 22 official languages, and integration with registered Consent Managers.

Official Citations: Act No. 22 of 2023; G.S.R. 846(E) (MeitY).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template India DPDPA Data Protection Policy or Children's Consent Framework.
- **Missing Documentation:**
  Documentation lacks developer guidelines on integrating DigiLocker for verifiable parental consent, handling Consent Manager tokens, or supporting multi-language consent notices.
- **Missing Code:**
  Code templates do not contain logic to disable behavioral tracking and targeted advertising for Indian users under 18.
- **Missing Disclosure:**
  Consent notice templates are not available in the 22 scheduled languages of India as required under Section 5 of the DPDPA.
- **Missing Logging:**
  There is no logging schema to track consent artifacts, DigiLocker verification tokens, or Consent Manager API interactions.
- **Missing Testing:**
  No automated tests verify that targeted ad SDKs are disabled when an Indian user profile is identified as under 18.
- **Missing Evidence:**
  The repository lacks templates for Significant Data Fiduciary risk assessments or Data Protection Officer appointment records.
- **Missing Audit Trail:**
  An immutable audit log tracking consent grants, withdrawals via Consent Managers, and data erasure requests is absent.

### 16.3 Remediation and Action Plan
1. Draft an India DPDPA Compliance Policy and Children's Data Protection Framework.
2. Build consent notice templates supporting multi-language localization.
3. Implement profile logic blocking ad tracking for under-18 Indian users.
4. Add automated CI checks validating Consent Manager integration APIs.

---

## 17. Singapore Personal Data Protection Act (PDPA) & App Store Age Assurance

### 17.1 Regulatory Overview and Background
Singapore's PDPA 2012, alongside IMDA's Code of Practice for Online Safety (effective 1 April 2026), mandates app distribution age assurance. App stores and developers must implement age assurance measures (credit card check, digital ID) to screen and prevent users under 18 from downloading age-inappropriate apps. Data breach notifications must occur within 3 calendar days.

Official Citations: Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety (2026).

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no template Singapore PDPA & IMDA Online Safety Policy.
- **Missing Documentation:**
  Documentation lacks guidelines on 3-day data breach reporting to the PDPC and IMDA age assurance compliance.
- **Missing Code:**
  Mock apps lack integration code for Singapore age assurance screening and 18+ download restrictions.
- **Missing Disclosure:**
  Privacy Policy templates do not include Singapore-specific Data Protection Officer (DPO) contact information or mandatory 3-day breach notice disclosures.
- **Missing Logging:**
  There is no logging system designed to record data breach incidents, breach severity assessments, or PDPC notification timestamps.
- **Missing Testing:**
  No automated tests exist to verify that age-inappropriate features are gated for Singapore users without verified age status.
- **Missing Evidence:**
  The repository lacks templates for PDPC data breach notification forms or IMDA safety audit evidence.
- **Missing Audit Trail:**
  An immutable audit log of DPO reviews, data breach evaluations, and age verification purging is missing.

### 17.3 Remediation and Action Plan
1. Create a Singapore PDPA Policy and 3-day Data Breach Procedure template.
2. Add DPO contact disclosure blocks in privacy policy templates.
3. Implement age assurance screening hooks for Singapore storefronts.
4. Establish automated incident logging schemas with 72-hour notification countdowns.

---

## 18. South Korea Telecommunications Business Act & PIPA

### 18.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act (Article 22-9) mandates alternative in-app payment support on mobile app stores. Apple supports this via `com.apple.developer.storekit.external-purchase` (KR) with a 26% commission, approved Korean payment gateways (KCP, Inicis, Toss, NICE), a Korea-only binary, and monthly reporting within 15 days. Additionally, PIPA (Act No. 21445, effective 11 September 2026) imposes CEO accountability and board-approved CPO requirements.

Official Citations: Telecommunications Business Act Article 22-9; PIPA Act No. 21445 (PIPC).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no South Korea Alternative Payment & PIPA Compliance Policy.
- **Missing Documentation:**
  Documentation lacks step-by-step instructions on configuring Korea-only binaries, integrating approved gateways, and submitting monthly 15-day sales reports to Apple.
- **Missing Code:**
  The codebase contains no implementation of the mandatory Korean pre-payment modal sheet or StoreKit Korea external purchase API wrappers.
- **Missing Disclosure:**
  In-app payment screens do not display the statutory Korean disclosure modal informing users that Apple purchase protections do not apply.
- **Missing Logging:**
  There is no backend logging system to capture alternative payment transactions for mandatory 15-day reporting.
- **Missing Testing:**
  No automated tests verify that StoreKit IAP and Korean external payment gateways are never co-mingled in the same binary.
- **Missing Evidence:**
  The repository lacks templates for monthly StoreKit Korea sales reporting spreadsheets or board-approved CPO designation documents.
- **Missing Audit Trail:**
  An immutable audit trail tracking Korean transaction volumes, commission calculations, and remittance history is absent.

### 18.3 Remediation and Action Plan
1. Formulate a South Korea Alternative Payment and PIPA Policy.
2. Implement native UI modal sheets calling Korea external purchase APIs.
3. Build backend logging and automated 15-day reporting tools for Korea transactions.
4. Add CI checks verifying separate binary creation for Korean storefront distribution.

---

## 19. China Mobile App Filing (MIIT) & AI Regulations

### 19.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (extension of ICP filing) via a local Chinese entity. Additionally, CAC Order No. 21 (Interim Measures for AI Anthropomorphic Interactive Services, effective 15 July 2026) requires identifying minor users, automatically switching them to Minors Mode, obtaining guardian consent under 14, and prohibiting virtual companion services for minors.

Official Citations: MIIT Mobile App Filing Rules; CAC Order No. 21 (Cyberspace Administration of China).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no China App Distribution & AI Governance Policy.
- **Missing Documentation:**
  Documentation lacks guidelines on completing MIIT app filing, securing local Chinese entity representation, or implementing CAC Minors Mode.
- **Missing Code:**
  Mock AI and chat applications do not contain code for switching into Minors Mode or restricting AI virtual companion features.
- **Missing Disclosure:**
  UI templates do not display MIIT filing numbers in app settings or show required real-name registration notices.
- **Missing Logging:**
  There is no logging system to record real-name identity verification checks or Minors Mode activation events.
- **Missing Testing:**
  No automated tests exist to verify that AI virtual companion features are disabled when Minors Mode is active.
- **Missing Evidence:**
  The repository lacks templates for MIIT ICP filing certificates, local partner agreements, or CAC AI security assessments.
- **Missing Audit Trail:**
  An audit trail recording real-name verification checks, Minors Mode toggles, and content moderation logs is missing.

### 19.3 Remediation and Action Plan
1. Draft a China Regulatory Compliance Policy covering MIIT filing and CAC AI rules.
2. Implement Minors Mode UI toggle components and feature gating in AI templates.
3. Add MIIT filing number metadata fields in store listing audit scripts.
4. Create automated integration tests validating AI companion restrictions in Minors Mode.

---

## 20. EU Product Liability Directive & Data Act

### 20.1 Regulatory Overview and Background
The updated EU Product Liability Directive (Directive (EU) 2024/2853, effective 9 December 2026) classifies standalone software, mobile applications, and AI systems as "products" subject to strict defect liability. Furthermore, the EU Data Act (Regulation (EU) 2023/2854, access-by-design effective 12 September 2026) mandates that connected devices and companion mobile apps allow users to access and export generated data easily.

Official Citations: Directive (EU) 2024/2853; Regulation (EU) 2023/2854 of the European Parliament and of the Council.

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook carries no Software Product Liability Policy or Data Act User Data Access Policy.
- **Missing Documentation:**
  Documentation lacks developer guidelines on software defect risk assessments, update safety disclosures, or Data Act compliant data export APIs.
- **Missing Code:**
  Companion app templates lack code modules enabling users to export connected device telemetry data in real-time.
- **Missing Disclosure:**
  Terms of Service and EULA templates do not incorporate updated Product Liability Directive defect disclosures or Data Act data sharing rights.
- **Missing Logging:**
  There are no logging mechanisms to capture software crash logs, telemetry export requests, or security update distribution history.
- **Missing Testing:**
  No automated tests exist to verify that data export endpoints function properly and return complete, machine-readable datasets.
- **Missing Evidence:**
  The repository lacks templates for software safety technical files or Data Act compatibility evaluations.
- **Missing Audit Trail:**
  An immutable audit trail documenting software release safety checks, bug fixes, and patch distribution records is missing.

### 20.3 Remediation and Action Plan
1. Formulate a Software Product Liability and Data Act Compliance Policy.
2. Build real-time user data export endpoints in backend templates.
3. Update EULA templates with software defect liability and patch availability disclosures.
4. Add automated API tests verifying data export functionality for connected app profiles.

---

## 21. Consolidated Gap Classification Matrix

The classification matrix below summarizes the coverage status across all twenty regulatory frameworks evaluated in this report.
- **Covered:** The repository provides dedicated policies, code, documentation, and tests.
- **Partial:** The framework is cited or mentioned, but concrete implementation templates, code, or tests are absent.
- **Missing:** The framework is completely unaddressed in the repository.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act (Art 4/50)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **6. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. European Accessibility Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. US COPPA (Amended Rule)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **10. California Privacy (CCPA)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. UK Online Safety Act** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. Australia Online Safety** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. Singapore PDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. South Korea TBA & PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. China App Filing & AI** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. EU Product Liability/Data Act**| Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Strategy

This comprehensive gap report reveals a consistent pattern across all twenty evaluated global regulatory frameworks. The repository excels at reference documentation and statutory citations, but currently exhibits systemic gaps in executable code templates, automated test runners, backend logging schemas, compliance evidence templates, and immutable audit trails.

To transition from passive reference documentation to active compliance enforcement, the repository must prioritize:
1. Adding executable detection recipes for GPSR, e-Evidence, Withdrawal Buttons, BIPA, and ASAA to `data/rejection-patterns.json`.
2. Developing UI code components and native wrappers for AI disclosures, GPC signals, withdrawal buttons, and age assurance.
3. Expanding automated audit scripts (`scripts/release-audit.py`, `scripts/accessibility-audit.py`, `scripts/metadata-audit.py`) to validate legal disclosures and technical requirements.
4. Providing standardized evidence templates (`AI_LITERACY_LOG.md`, ACR EN 301 549, WISP) in `templates/`.

---

## 23. Official Sources

Every regulatory framework cited in this report traces directly to Priority 1 official publications:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU DMA: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU DSA: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Privacy: [California Consumer Privacy Act (OAG)](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14/ (ILGA)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US ROSCA: [15 U.S.C. § 8401](https://www.govinfo.gov/content/pkg/USCODE-2011-title15/html/USCODE-2011-title15-chap110.htm)
- UK Online Safety Act: [UK Public General Acts 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety: [Social Media Minimum Age Act 2024](https://www.legislation.gov.au/)
- Brazil Digital ECA: [Decreto n. 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in)
- Singapore PDPA: [Personal Data Protection Act 2012](https://sso.agc.gov.sg/Act/PDPA2012)
- South Korea PIPA: [Act No. 21445](https://law.go.kr)
- China AI Regulations: [CAC Order No. 21](https://www.cac.gov.cn)
- EU Product Liability Directive: [Directive (EU) 2024/2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj)
- EU Data Act: [Regulation (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)
