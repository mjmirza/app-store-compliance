# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the App Store Compliance Playbook itself. It evaluates twenty major global and regional regulations that bind mobile and web applications, checking honestly how far this repository carries each framework, what is documented or covered, and what remains to be implemented.

Read this document as an actionable compliance work list for the playbook and developers, not as formal legal advice. Where an item is marked as missing or partial, it indicates a gap in the repository's rules, detection recipes, code implementations, or automated guard hooks. Each framework is evaluated systematically across eight compliance gap domains: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

---

## Source Trust Hierarchy and Methodology

All analysis, citations, and regulatory evaluations in this report strictly adhere to the repository's Source Trust Hierarchy:
- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Reputable News Agencies): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic Publications): Academic papers and peer-reviewed journals.
- Priority 4 (Industry Publications): Industry blogs and vendor publications.
- Priority 5 (Social and Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

No Priority 4 or Priority 5 sources are trusted unless traceably corroborated by official Priority 1 publications. In strict adherence to repository standards, this document is 100% emoji-free and contains no emoticons or graphical symbols of any kind.

---

## 1. EU General Product Safety Regulation (GPSR)

### 1.1 Regulatory Overview and Background
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address safety challenges in e-commerce, digital marketplaces, and software-driven products.

The GPSR applies to non-food consumer products sold in the EU market. E-commerce applications and digital marketplaces must clearly display product safety warnings, instructions, manufacturer and importer identity, and contact details directly on the online user interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** The repository carries a baseline rejection pattern (`BOTH-GPSR-COMPLIANCE-MISSING`) but lacks a standalone, reusable General Product Safety Policy template for e-commerce developers.
- **Missing Documentation:** Lacks detailed step-by-step developer integration manuals showing how e-commerce product detail pages must structure manufacturer metadata and safety labels.
- **Missing Code:** Client UI templates do not include functional components or layout blocks for dynamically rendering EU Responsible Person details and safety disclosures on product screens.
- **Missing Disclosure:** Missing standard placeholder components to display manufacturer postal address, email, and localized product safety warnings on storefront UI templates.
- **Missing Logging:** Lacks database logging schemas or incident report structures for capturing product safety complaints or recall notifications.
- **Missing Testing:** Automated test suites do not check whether e-commerce product detail screens dynamically display required safety disclosures based on user geography.
- **Missing Evidence:** No example evidence packages demonstrating completed safety risk assessments or designated EU Responsible Person documentation.
- **Missing Audit Trail:** Lacks an immutable audit log schema to track safety warning updates, product recall actions, or corrective measure histories.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy template outlining EU Responsible Person designation and product safety classification rules.
2. Add UI templates in `references/` demonstrating compliant e-commerce product detail layouts with safety labels and manufacturer contact information.
3. Integrate automated static checks verifying safety label fields on e-commerce product detail views prior to store submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 on European Production and Preservation Orders for electronic evidence and Directive (EU) 2023/1544 on legal representatives. Mandatory enforcement applies starting 18 August 2026.

This framework allows EU Member State judicial authorities to issue production orders directly to service providers in the EU, regardless of headquarters location. Standard compliance requires data production within 10 days, while critical emergency requests demand execution within a strict 8-hour window.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544 of the European Parliament and of the Council.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a customizable Law Enforcement Request Policy template specifying roles, validation steps, and response procedures.
- **Missing Documentation:** Operational runbooks covering emergency 8-hour order processing are referenced in `docs/EU-REGULATORY-2026.md` but lack step-by-step internal handler guides.
- **Missing Code:** Missing automated backend data-extraction and encryption helper scripts to package user evidence under emergency conditions.
- **Missing Disclosure:** Privacy policy templates do not contain mandatory disclosures informing EU users that data may be produced under Regulation (EU) 2023/1543 orders.
- **Missing Logging:** Database schemas lack tables for logging incoming judicial orders, certificate validation statuses, or data extraction activities.
- **Missing Testing:** No automated integration test scripts to simulate rapid 8-hour user data extraction and secure archive generation.
- **Missing Evidence:** Lacks sample EPOC and EPOC-PR certificate templates for training compliance personnel on order validation.
- **Missing Audit Trail:** Lacks a cryptographic audit log mechanism to record officer interactions, certificate approvals, and data transmission timestamps.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol specifying roles, verification steps, and legal representative details ahead of August 2026.
2. Build backend helper scripts for automated user data extraction and encryption to satisfy the 8-hour emergency response window.
3. Implement a dedicated logging schema to maintain an audit trail of received orders, verification checks, and disclosures.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Consumer Rights Directive 2011/83/EU regarding distance financial services contracts, mandating a prominent, easily accessible withdrawal function on online interfaces. Member States apply these rules starting 19 June 2026.

Consumers exercising their statutory 14-day withdrawal right must be able to cancel the contract through a direct, frictionless path that is at least as simple as the initial sign-up flow.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council of 22 November 2023.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a dedicated Consumer Contract Withdrawal Policy template defining the 14-day statutory revocation window and refund flows.
- **Missing Documentation:** Does not provide explicit UI/UX layout checklists defining button prominence, positioning, or wording standards.
- **Missing Code:** Frontend app templates and billing mocks do not include a functional withdrawal button or modal sheet implementation.
- **Missing Disclosure:** Registration and checkout screens lack prominent disclosures notifying users of the 14-day statutory right of withdrawal.
- **Missing Logging:** Lacks logging schemas to record withdrawal button clicks, cancellation timestamps, and automatic refund initiation events.
- **Missing Testing:** Test suites lack automated UI flows confirming self-service contract withdrawal completes without human friction or customer support intervention.
- **Missing Evidence:** Missing standardized cancellation confirmation receipt templates for consumer dispute resolution.
- **Missing Audit Trail:** Lacks audit log structures tracking historic cancellation rates, interface modification histories, and refund settlement logs.

### 3.3 Remediation and Action Plan
1. Publish a Consumer Contract Withdrawal Policy template aligned with Directive (EU) 2023/2673.
2. Implement a reusable "Withdrawal Button" UI component and cancellation modal across account management templates.
3. Add automated end-to-end UI tests verifying frictionless self-service contract termination and refund trigger execution.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 977, Alabama HB 161) regulate minors' access to mobile applications, purchases, and updates.

Developers must query age categories (via Apple's Declared Age Range API or Google's Play Age Signals API) and obtain verifiable parental consent before allowing minors to download, purchase digital goods, or apply major updates. Verification data must be deleted immediately after verification.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 977 (2026), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a reusable Minor Age Assurance Policy template outlining state-specific age detection and minor account restrictions.
- **Missing Documentation:** Pre-submission checklists lack detailed multi-platform code guides for simultaneously handling iOS Declared Age Range and Android Age Signals APIs.
- **Missing Code:** Mobile client templates do not implement native hooks for `DeclaredAgeRange` or `com.google.android.play:age-signals` to restrict features dynamically.
- **Missing Disclosure:** Onboarding UI screens do not display state disclosures explaining that age categories are queried to comply with state law and that parental consent is required.
- **Missing Logging:** Backend schemas do not capture parental consent receipt, `RESCIND_CONSENT` server notifications, or confirmation of raw verification data deletion.
- **Missing Testing:** Test suites lack automated integration tests verifying that minor account signals block in-app purchases when consent is missing.
- **Missing Evidence:** Missing sample parental consent forms, verification logs, and data deletion confirmation records.
- **Missing Audit Trail:** Lacks immutable audit logs tracking age assurance feature rollouts, policy updates, and immediate data purging records.

### 4.3 Remediation and Action Plan
1. Draft a Minor Age Assurance Policy defining state-level compliance requirements and data minimization rules.
2. Implement native cross-platform hooks for Apple Declared Age Range API and Google Play Age Signals API in client templates.
3. Build database cleanup routines to purge raw age verification data immediately after age category confirmation.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of the EU AI Act (Regulation (EU) 2024/1689) establishes a mandatory AI literacy duty effective since 2 February 2025. Providers and deployers of AI systems must ensure staff and operators possess a sufficient level of AI literacy, proportionate to context and risk.

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a customizable AI Literacy Policy template specifying required competency areas (AI safety, risk assessment, bias detection).
- **Missing Documentation:** Developer guidelines do not detail operational workflows for fulfilling Article 4 literacy obligations across engineering teams.
- **Missing Code:** Not directly applicable to product runtime code, but missing a repository linter to verify the existence of an updated AI literacy log.
- **Missing Disclosure:** External recruitment materials, partner agreements, and vendor contracts lack explicit AI literacy compliance declarations.
- **Missing Logging:** The repository lacks a centralized training log or registry (`docs/AI_LITERACY_LOG.md`) tracking induction and refresher dates.
- **Missing Testing:** No automated CI scripts exist to verify that team members committing AI feature code have recorded active literacy training.
- **Missing Evidence:** Lacks sample training record templates or completed competency assessment logs for regulatory inspection.
- **Missing Audit Trail:** Lacks historical audit records showing annual literacy policy reviews and curriculum updates.

### 5.3 Remediation and Action Plan
1. Create an AI Literacy Policy template defining required training modules and annual refresher cadences.
2. Establish a template `docs/AI_LITERACY_LOG.md` file within the repository to track training completions.
3. Add a CI check that warns if the AI literacy log has not been reviewed within the preceding 12 months.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of the EU AI Act mandates strict transparency rules for AI systems, taking full effect on 2 August 2026. Providers must disclose direct human-AI interaction, mark generative AI outputs in machine-readable formats, and label deepfakes.

Official Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an AI Transparency Policy template specifying when in-app disclosures must appear and how media outputs must be watermarked.
- **Missing Documentation:** Checklists mention Article 50 but lack technical integration guides for C2PA content provenance metadata injection.
- **Missing Code:** Client UI templates lack built-in "You are interacting with an AI system" disclosure headers and C2PA metadata tagging utilities for generated assets.
- **Missing Disclosure:** Chat and content creation UI templates fail to show mandatory disclosures at the time of first user interaction.
- **Missing Logging:** Database schemas lack session logging structures to confirm transparency warnings were displayed to the user.
- **Missing Testing:** Test runners do not scan generated media assets to confirm machine-readable watermarking metadata is preserved.
- **Missing Evidence:** Lacks independent audit evidence demonstrating content moderation filter effectiveness and synthetic media marking compliance.
- **Missing Audit Trail:** Lacks an audit trail tracking model updates, disclosure text changes, and technical transparency choices.

### 6.3 Remediation and Action Plan
1. Draft an AI Transparency Policy template mandating direct user disclosure and output watermarking.
2. Add visible "AI Assistant" badges and C2PA metadata taggers to conversational and generative UI templates.
3. Build automated test scripts to verify generated outputs contain valid machine-readable synthetic content markers.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms to ensure contestable and fair markets. For mobile developers, the DMA enables alternative distribution channels, alternative browser engines, and external offer promotion.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a DMA Entitlement Policy guide helping developers evaluate whether to adopt alternative payments or web distribution.
- **Missing Documentation:** Lacks operational documentation detailing monthly Core Technology Commission (CTC) reporting protocols.
- **Missing Code:** Mobile client code templates lack default logic calling `ExternalPurchaseCustomLink` disclosure sheets before opening external purchase links.
- **Missing Disclosure:** External offer flows lack template modal sheets explaining that purchases occur outside Apple or Google protections.
- **Missing Logging:** Lacks backend reporting server templates to record and calculate monthly external sales for platform reporting APIs.
- **Missing Testing:** Automated tests do not confirm that StoreKit IAP and external purchase links are mutually exclusive on the same EU storefront view.
- **Missing Evidence:** Lacks sample documentation proving notarization compliance and alternative marketplace eligibility.
- **Missing Audit Trail:** Lacks audit trail logs tracking ADPLA Attachment 14 agreement acceptance and monthly sales submission histories.

### 7.3 Remediation and Action Plan
1. Create a DMA Implementation Guide covering external link entitlements, custom link disclosure sheets, and CTC reporting.
2. Integrate `ExternalPurchaseCustomLink` API calls and disclosure sheet triggers into payment UI templates.
3. Build automated lints confirming StoreKit IAP and external link entitlements are not improperly combined on EU storefronts.

---

## 8. EU Digital Services Act (DSA)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) imposes trader transparency duties (Articles 30 and 31) and content moderation requirements. App developers selling digital goods in the EU must verify trader status (D-U-N-S, phone, address) or face storefront removal.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a DSA Trader & Moderation Policy template guiding developers through trader verification and illegal content handling.
- **Missing Documentation:** Storefront metadata checklists lack step-by-step guides for verifying trader credentials in App Store Connect and Google Play Console.
- **Missing Code:** UGC app templates lack standardized notice-and-action UI components for user reporting and content moderation.
- **Missing Disclosure:** Storefront metadata description templates do not include mandatory trader contact detail blocks.
- **Missing Logging:** Lacks database tables for tracking user content reports, moderation decisions, and takedown notices.
- **Missing Testing:** Test runners do not verify that UGC reporting buttons and moderation triggers are functional.
- **Missing Evidence:** Lacks sample DSA trader verification confirmation records and annual moderation transparency report templates.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing user flags, moderator actions, and appeal handling outcomes.

### 8.3 Remediation and Action Plan
1. Incorporate DSA trader status verification checks into store listing metadata audit scripts.
2. Add notice-and-action reporting UI components to user-generated content app templates.
3. Create database logging structures to track user reports, moderation actions, and appeal decisions.

---

## 9. European Accessibility Act (EAA)

### 9.1 Regulatory Overview and Background
Directive (EU) 2019/882 (European Accessibility Act) applies from 28 June 2025. Mobile applications and e-commerce services in the EU must comply with harmonised standard EN 301 549 (WCAG 2.1 Level AA) and publish an accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Organizational Accessibility Policy template establishing EN 301 549 Chapter 11 standards for mobile software.
- **Missing Documentation:** Pre-submission checklists lack detailed guides explaining how EN 301 549 Chapter 11 expands upon base WCAG 2.1 rules.
- **Missing Code:** UI templates contain missing VoiceOver/TalkBack labels on custom graphics and lack automated Dynamic Type scaling support.
- **Missing Disclosure:** Mobile app templates do not include a published Accessibility Statement screen or link.
- **Missing Logging:** Lacks logging schemas to capture accessibility barrier reports submitted by users.
- **Missing Testing:** Static accessibility audits check base contrast and labels but do not validate screen reader focus order or switch control navigation.
- **Missing Evidence:** Lacks third-party accessibility audit report templates or voluntary product accessibility templates (VPAT / EN 301 549 conformance).
- **Missing Audit Trail:** Lacks audit logs tracking accessibility regression testing results and remediation histories across app updates.

### 9.3 Remediation and Action Plan
1. Publish an Accessibility Policy template aligned with EN 301 549 and WCAG 2.1 Level AA.
2. Add an Accessibility Statement view template to client mobile project structures.
3. Enhance `scripts/accessibility-audit.py` to check for focus order, touch target sizes, and screen reader labels.

---

## 10. US Children's Online Privacy Protection Act (COPPA) & Amended Rule

### 10.1 Regulatory Overview and Background
COPPA (16 CFR Part 312) protects children under 13. The Amended COPPA Rule (effective April 2026) expands PII to include biometric identifiers, requires separate opt-in consent for targeted ads, and mandates written retention and security programs.

Official Citation: 16 CFR Part 312 (FTC Children's Online Privacy Protection Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an updated COPPA Compliance Policy template incorporating biometric identifier rules and separate ad-consent requirements.
- **Missing Documentation:** Developer checklists lack detailed guides on configuring zero-tracking ad networks for child-directed apps.
- **Missing Code:** Onboarding flows lack separate opt-in consent toggles for third-party ad sharing and lack verifiable parental consent modals.
- **Missing Disclosure:** Privacy policies lack explicit disclosures itemizing biometric identifier collection and third-party data sharing.
- **Missing Logging:** Lacks backend log structures confirming verifiable parental consent receipt and scheduled data deletion dates.
- **Missing Testing:** Automated test suites do not check whether tracking SDKs are completely suppressed when a user enters an under-13 birthdate.
- **Missing Evidence:** Lacks sample Written Information Security Program (WISP) and Written Data Retention Policy templates required under Section 312.10.
- **Missing Audit Trail:** Lacks immutable audit logs tracking parental consent grants, consent revocations, and child data deletion executions.

### 10.3 Remediation and Action Plan
1. Draft a COPPA Compliance Policy template incorporating 2026 Amended Rule duties.
2. Build onboarding templates featuring parental consent gates and separate ad-sharing consent toggles.
3. Implement automated test scripts confirming tracking SDK suppression upon under-13 age selection.

---

## 11. California Privacy Rights Act (CPRA) & CPPA 2026 Regulations

### 11.1 Regulatory Overview and Background
The CCPA/CPRA (California Civil Code) and CPPA 2026 Regulations enforce consumer privacy rights, including opt-outs for sale/sharing, Global Privacy Control (GPC) recognition, and automated decision-making technology (ADMT) controls.

Official Citation: California Civil Code Section 1798.100 et seq. and 11 CCR Division 6.

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a CPRA Privacy Policy template covering ADMT opt-out rights and sensitive personal information limits.
- **Missing Documentation:** Lacks technical documentation explaining how native mobile apps must handle GPC signals or equivalent opt-out toggles.
- **Missing Code:** Embedded webview components do not automatically pass `Sec-GPC` opt-out headers, and client settings lack a "Do Not Sell/Share" toggle.
- **Missing Disclosure:** Onboarding flows lack mandatory Notice at Collection disclosures detailing data retention per category.
- **Missing Logging:** Lacks database tables capturing consumer privacy requests (know, delete, opt-out) and response fulfillment dates.
- **Missing Testing:** Test runners do not verify that enabling the GPC header or opt-out toggle immediately halts ad tracking SDK transmissions.
- **Missing Evidence:** Lacks sample CPPA Risk Assessment documents and annual consumer request fulfillment metric reports.
- **Missing Audit Trail:** Lacks an audit trail tracking GPC signal processing, opt-out preference updates, and deletion request fulfillments.

### 11.3 Remediation Action Plan
1. Publish a CPRA/CCPA Policy template featuring Notice at Collection and ADMT opt-out language.
2. Inject `Sec-GPC` header propagation logic into webview helpers and client settings toggles.
3. Add backend logging schemas to record and track California consumer rights requests.

---

## 12. Illinois Biometric Information Privacy Act (BIPA)

### 12.1 Regulatory Overview and Background
Illinois BIPA (740 ILCS 14) requires written notice and a signed release prior to capturing biometric identifiers (fingerprints, facial templates, voiceprints). It mandates public retention schedules and prohibits profiting from biometric data.

Official Citation: 740 ILCS 14 (Biometric Information Privacy Act).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a standalone Biometric Data Privacy Policy template detailing retention schedules and destruction guidelines.
- **Missing Documentation:** Checklists lack explicit guides on distinguishing native device authentication (Face ID/Touch ID) from server-side biometric capture.
- **Missing Code:** Mobile client code templates lack explicit BIPA written release modal sheets prior to initializing biometric capture SDKs.
- **Missing Disclosure:** In-app consent screens fail to disclose the specific purpose and duration of biometric identifier storage.
- **Missing Logging:** Backend schemas lack tables recording written consent timestamps and automated 3-year destruction triggers.
- **Missing Testing:** Test suites do not verify that biometric feature initialization is blocked if the user declines the BIPA consent release.
- **Missing Evidence:** Lacks sample executed BIPA consent agreement forms and biometric destruction certificate templates.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing consent grants, consent revocations, and biometric data purging events.

### 12.3 Remediation Action Plan
1. Draft a Biometric Privacy Policy template and a BIPA Written Release Modal component.
2. Implement code checks confirming native Face ID/Touch ID processing stays on-device and does not transmit raw biometric templates.
3. Add backend logging routines to enforce the 3-year maximum retention limit for biometric data.

---

## 13. US Subscription Cancellation (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. 8401) and state negative option statutes (California, New York) require online subscription cancellations to be direct, simple, and at least as easy as the sign-up process.

Official Citation: 15 U.S.C. 8401 (ROSCA) and California Business & Professions Code Section 17600.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Subscription Cancellation & Renewal Policy template for web-billed or cross-platform subscriptions.
- **Missing Documentation:** Checklists do not detail state-specific negative option requirements for web-billed companion app funnels.
- **Missing Code:** Web/app account management templates do not include a self-service, one-click subscription cancellation button.
- **Missing Disclosure:** Checkout screens lack prominent pre-consent disclosures detailing recurring billing amounts, billing frequency, and cancellation steps.
- **Missing Logging:** Lacks database logging structures capturing subscription cancellation requests, timestamps, and confirmation notices.
- **Missing Testing:** Test runners do not verify that clicking the cancellation button immediately updates subscription status without requiring manual support calls.
- **Missing Evidence:** Lacks sample post-purchase email confirmation templates containing explicit cancellation instructions.
- **Missing Audit Trail:** Lacks audit logs tracking subscription cancellation rates, refund requests, and checkout disclosure updates.

### 13.3 Remediation Action Plan
1. Create a Subscription Negative Option Policy template and pre-checkout disclosure checklist.
2. Add a reusable, self-service Subscription Cancellation component to account management UI templates.
3. Implement automated integration tests confirming self-service subscription cancellation executes cleanly in database mocks.

---

## 14. UK Online Safety Act (OSA 2023) & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 and ICO Children's Code establish mandatory duties to protect children from harmful content, mandating Highly Effective Age Assurance (facial estimation, open banking) and high privacy by default.

Official Citation: Online Safety Act 2023 (c. 50) and ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a UK Child Safety & Online Protection Policy template outlining age assurance methods and risk assessments.
- **Missing Documentation:** Guidelines lack step-by-step instructions for completing an ICO-compliant Data Protection Impact Assessment (DPIA).
- **Missing Code:** Social and UGC UI templates lack default settings turning off precise geolocation and profiling for UK minor accounts.
- **Missing Disclosure:** Privacy notices lack child-friendly summary views suitable for different age tiers (under 13, 13-15, 16-17).
- **Missing Logging:** Lacks database logging schemas for recording age assurance checks while ensuring immediate destruction of raw verification data.
- **Missing Testing:** Test suites do not verify that new UK accounts default to high-privacy settings with profiling disabled.
- **Missing Evidence:** Lacks sample completed DPIA templates and Ofcom illegal content risk assessment records.
- **Missing Audit Trail:** Lacks an audit trail capturing age assurance method updates, risk assessment reviews, and child safety feature changes.

### 14.3 Remediation Action Plan
1. Publish an ICO Children's Code Compliance Guide and DPIA Template.
2. Build UI onboarding templates defaulting to high privacy, geolocation-off, and profiling-off for UK users.
3. Add automated test routines verifying child account default settings under UK regional configurations.

---

## 15. Australia Online Safety Act & Social Media Minimum Age Act 2024

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment (Social Media Minimum Age) Act 2024 requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts, supported by the eSafety Commissioner's industry codes.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024 and eSafety Industry Codes.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an Australian Social Media Age Restriction Policy template defining age verification waterfall methods.
- **Missing Documentation:** Checklists do not detail the eSafety Commissioner's waterfall age-assurance requirements.
- **Missing Code:** Client templates lack native integration hooks to query age verification signals or restrict under-16 account registration.
- **Missing Disclosure:** Registration screens lack explicit Australian disclosures explaining under-16 social account restrictions.
- **Missing Logging:** Lacks secure, ringfenced logging schemas capturing age assurance completion while enforcing immediate verification data destruction.
- **Missing Testing:** Test runners do not verify that Australian under-16 account registration attempts are blocked on social platform templates.
- **Missing Evidence:** Lacks sample eSafety annual compliance report templates and age assurance audit records.
- **Missing Audit Trail:** Lacks an immutable audit log tracking age assurance system updates and verification data purging executions.

### 15.3 Remediation Action Plan
1. Draft an Australian Age Restriction Policy template and eSafety compliance checklist.
2. Implement onboarding logic blocking under-16 account creation on Australian social media UI templates.
3. Add backend cleanup scripts ensuring age verification data is ringfenced and destroyed immediately post-verification.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & Decreto 12,880/2026)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025) and Decreto 12,880/2026 mandate strict age assurance (facial estimation, document checking, CPF checks) and parental authorization for minor accounts, prohibiting simple self-declaration checkboxes.

Official Citation: Lei n. 15.211/2025 and Decreto n. 12.880/2026.

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Brazil Digital ECA Compliance Policy template covering CPF checks, age assurance, and loot-box restrictions.
- **Missing Documentation:** Checklists do not detail ANPD age assurance parameters or loot-box 18-plus auto-rating rules for Brazil.
- **Missing Code:** Client templates lack UI components for capturing CPF or document verification and lack parental consent modal triggers.
- **Missing Disclosure:** Registration and storefront screens lack Brazilian disclosures detailing age verification methods and parental rights.
- **Missing Logging:** Lacks backend database tables logging parental authorization grants and ANPD compliance verification events.
- **Missing Testing:** Test suites do not check whether self-declaration checkboxes are rejected for Brazilian user registrations.
- **Missing Evidence:** Lacks sample ANPD compliance report templates and parental consent authorization logs.
- **Missing Audit Trail:** Lacks audit log structures recording age assurance verification updates, parental consent grants, and account contestations.

### 16.3 Remediation Action Plan
1. Create a Brazil Digital ECA Policy template and CPF/document age verification UI workflow.
2. Build client validation checks preventing self-declaration checkboxes from satisfying age gates on Brazilian storefronts.
3. Implement backend logging routines capturing parental consent grants and account contestation handling.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 / DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 mandate verifiable parental consent (via government systems such as DigiLocker) for under-18s and prohibit behavioral tracking or targeted advertising directed at children.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) and DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks an India DPDPA Policy template detailing verifiable parental consent and under-18 tracking prohibitions.
- **Missing Documentation:** Checklists lack integration guides for interfacing with registered Consent Managers and DigiLocker systems.
- **Missing Code:** Client UI templates lack Consent Manager integration hooks and verifiable parental consent onboarding flows.
- **Missing Disclosure:** Privacy notices lack multilingual consent notices specifying data processing purposes in languages listed in the Eighth Schedule.
- **Missing Logging:** Lacks backend logging schemas capturing Consent Manager tokens and parental consent verification events.
- **Missing Testing:** Test runners do not verify that targeted ad tracking SDKs are disabled for Indian under-18 accounts.
- **Missing Evidence:** Lacks sample Data Protection Officer (DPO) appointment records and Consent Manager interoperability certificates.
- **Missing Audit Trail:** Lacks an audit trail capturing consent grants, consent withdrawals, and DPO grievance resolution histories.

### 17.3 Remediation Action Plan
1. Draft an India DPDPA Compliance Guide covering under-18 parental consent and Consent Manager integration.
2. Add multilingual consent notice components to onboarding UI templates.
3. Build test automation confirming targeted ad SDK suppression for Indian minor accounts.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA Online Safety Code

### 18.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety for App Distribution Services require app store age assurance and strict protection of children's data, ensuring minor access to age-inappropriate content is restricted.

Official Citation: Personal Data Protection Act 2012 and IMDA Code of Practice for Online Safety (2025/2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a Singapore PDPA & IMDA Online Safety Policy template detailing DPO appointment and age assurance rules.
- **Missing Documentation:** Checklists do not detail IMDA app distribution age assurance requirements.
- **Missing Code:** Client templates lack integration hooks for platform age assurance APIs on Singapore storefront configurations.
- **Missing Disclosure:** App metadata and in-app notices lack clear disclosures detailing content ratings and age restrictions.
- **Missing Logging:** Lacks backend logging structures to record age assurance verification without retaining raw identity data.
- **Missing Testing:** Test suites do not check whether 18-plus rated app templates block unverified downloads on Singapore configurations.
- **Missing Evidence:** Lacks sample DPO registration records and IMDA compliance self-assessment documents.
- **Missing Audit Trail:** Lacks an audit log capturing age restriction updates, DPO contact publications, and data protection reviews.

### 18.3 Remediation Action Plan
1. Publish a Singapore Privacy & Online Safety Policy template including DPO declaration requirements.
2. Build client age gate components aligning with IMDA app store age assurance guidelines.
3. Add test routines verifying 18-plus content gating under Singapore storefront configurations.

---

## 19. South Korea Telecommunications Business Act & PIPA Amendment

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payment options, while the amended Personal Information Protection Act (PIPA, Act No. 21445) enforces CEO accountability and strict breach notifications.

Official Citation: Telecommunications Business Act Article 22-9 and PIPA Act No. 21445.

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a South Korea Alternative Payment & PIPA Compliance Policy template.
- **Missing Documentation:** Checklists do not detail the 26% commission reporting and approved Korean payment gateway integration rules.
- **Missing Code:** Mobile client templates lack `com.apple.developer.storekit.external-purchase` modal sheets tailored for Korea (`SKExternalPurchase = "KR"`).
- **Missing Disclosure:** Payment screens lack mandatory Korean modal sheets explaining that Apple/Google protections do not apply to external payments.
- **Missing Logging:** Lacks backend reporting tables to capture monthly sales for Korean telecommunication authority reporting.
- **Missing Testing:** Test runners do not verify that alternative billing options in Korea invoke approved native payment SDKs (KCP, Toss, Inicis).
- **Missing Evidence:** Lacks sample CPO appointment records and monthly sales reporting receipts.
- **Missing Audit Trail:** Lacks audit logs capturing alternative payment transaction submissions and PIPA breach notification logs.

### 19.3 Remediation Action Plan
1. Draft a South Korea In-App Payment & PIPA Policy template.
2. Implement Korean external payment modal sheet logic calling StoreKit external purchase APIs.
3. Add backend sales logging schemas to support monthly Korean transaction reporting.

---

## 20. China Mobile App Filing (MIIT) & CAC AI Companion Rules

### 20.1 Regulatory Overview and Background
China's MIIT Mobile App Filing (ICP extension) is mandatory for app distribution. Additionally, CAC Order No. 21 (2026) regulates AI companion apps, prohibiting virtual companion services for minors and mandating automatic minor mode switching.

Official Citations: MIIT Circular on Mobile App Filing (2023) and CAC Order No. 21 (2026).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories
- **Missing Policy:** Lacks a China App Distribution & CAC AI Compliance Policy template covering MIIT filing, real-name checks, and minor modes.
- **Missing Documentation:** Checklists do not detail MIIT app filing submission steps or CAC AI companion minor restrictions.
- **Missing Code:** AI chat templates lack automatic minor mode switching logic and real-name verification UI hooks for China builds.
- **Missing Disclosure:** Storefront descriptions and in-app screens lack mandatory ICP filing number displays and CAC AI disclosures.
- **Missing Logging:** Lacks backend logging schemas capturing real-name verification tokens and minor mode activation events.
- **Missing Testing:** Test suites do not check whether AI companion features are disabled when a minor profile is detected on China builds.
- **Missing Evidence:** Lacks sample MIIT app filing approval records and CAC AI algorithm filing confirmation documents.
- **Missing Audit Trail:** Lacks an immutable audit trail capturing MIIT filing updates, real-name verification logs, and minor mode activations.

### 20.3 Remediation Action Plan
1. Create a China Mobile App Compliance Guide detailing MIIT filing and CAC AI companion rules.
2. Build UI templates featuring ICP filing number badges, real-name verification modals, and automatic minor modes.
3. Implement automated test routines confirming AI companion features are suppressed under minor profiles in China builds.

---

## 21. Consolidated Gap Classification Matrix

This matrix classifies the compliance status of the playbook and repository across all twenty evaluated global and regional regulations across the eight compliance gap categories.
- **Covered:** Full policy, documentation, code, and test coverage exists in the repository.
- **Partial:** The framework is cited and documented, but lacks complete code templates, automated tests, or logging structures.
- **Missing:** The framework or specific category is entirely absent from the repository's automated guards, recipes, or documentation.

| Regulatory Framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit Trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Partial | Missing | Partial | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU Withdrawal Button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US State ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Covered | Covered | Partial | Covered | Partial | Partial | Missing | Missing |
| **8. EU DSA** | Covered | Covered | Partial | Covered | Missing | Partial | Missing | Missing |
| **9. European Accessibility Act** | Covered | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA & Amended Rule** | Covered | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **11. California CPRA / CPPA** | Covered | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **12. Illinois BIPA** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **14. UK OSA & Children's Code** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Online Safety** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA & IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA & PIPA** | Covered | Covered | Partial | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing & CAC** | Covered | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Remediation Roadmap

The App Store Compliance Playbook provides robust coverage for store-level rejection rules (Apple App Review Guidelines and Google Play Developer Policies) and core regulatory frameworks (DMA, DSA, COPPA, CPRA, EAA, AI Act).

However, expanding the playbook's reach to cover the full legal lifecycle of mobile and web applications reveals consistent operational gaps across backend logging, automated testing, evidence collection, and immutable audit trails.

To achieve complete end-to-end regulatory compliance, the repository work plan prioritizes:
1. **Short-Term (Q3 2026):** Add missing UI components and code templates for EU GPSR, EU Withdrawal Button, and AI Act Article 50 disclosures.
2. **Medium-Term (Q4 2026):** Develop reusable backend database logging schemas for BIPA consent, COPPA retention, e-Evidence requests, and GPC opt-outs.
3. **Long-Term (Q1 2027):** Expand automated static check scripts (`scripts/validate.py`, `scripts/release-audit.py`) to verify regulatory code patterns, evidence logs, and audit trails prior to submission.

---

## 23. Official Primary Sources (Priority 1)

All regulatory citations herein trace directly to official Priority 1 publications:
- EU GPSR, [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package, [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing of Financial Services, [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- EU AI Act, [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act, [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act, [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act, [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule Amendments, [16 CFR Part 312 (90 FR 16918)](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- California Privacy Rights Act (CPRA), [California Civil Code 1798.100](https://leginfo.legislature.ca.gov)
- Illinois Biometric Information Privacy Act, [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- UK Online Safety Act 2023, [c. 50](https://www.legislation.gov.uk/ukpga/2023/50/contents/enacted)
- Brazil Digital ECA, [Lei n. 15.211/2025](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/) and [Decreto n. 12.880/2026](https://www.planalto.gov.br)
- India Digital Personal Data Protection Act, [Act No. 22 of 2023](https://egazette.gov.in)
- Singapore IMDA Code of Practice for Online Safety, [IMDA Official Code](https://www.imda.gov.sg)
- South Korea Telecommunications Business Act & PIPA, [law.go.kr](https://law.go.kr)
- China CAC AI Companion Rules, [CAC Order No. 21](https://www.cac.gov.cn)
