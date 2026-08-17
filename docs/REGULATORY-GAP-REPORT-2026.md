# Global and Regional Regulatory Compliance Gap Report (2026)

This report audits the playbook itself. It takes twenty major global and regional regulations that bind mobile and web application developers, and evaluates how far this repository carries each one, what it mentions in passing, and what remains missing.

Read it as an operational work list for the playbook, not as legal advice for your company. Where it says something is missing, it means missing from this repository. Each framework is systematically audited across eight distinct compliance categories: policy, documentation, code, disclosure, logging, testing, evidence, and audit trail.

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
The EU General Product Safety Regulation (GPSR), Regulation (EU) 2023/988, entered into force on 12 June 2023 and became fully applicable on 13 December 2024. It replaces the General Product Safety Directive (2001/95/EC) to address online marketplaces, digital products, and complex e-commerce supply chains.

The GPSR applies to all non-food consumer products placed on the EU market. For digital software and e-commerce apps, the GPSR mandates displaying product safety warnings, instructions, manufacturer/importer identity, and electronic contact details directly on the online interface.

Official Citation: Regulation (EU) 2023/988 of the European Parliament and of the Council.

### 1.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  The playbook provides no policy template for developers to evaluate GPSR applicability or designate an EU Responsible Person.
- **Missing Documentation:**
  Lacks developer guides on structuring mobile and web product detail pages to display manufacturer identity and safety instructions.
- **Missing Code:**
  No UI mock components, detection scripts, or guard rules exist to scan for missing manufacturer contact info or safety labels on EU storefronts.
- **Missing Disclosure:**
  Online interface templates lack placeholder components for manufacturer address, email, or product safety warnings under Article 19.
- **Missing Logging:**
  No schemas or log specifications exist for capturing product safety incidents, safety complaints, or recall events.
- **Missing Testing:**
  No automated UI or unit tests verify that safety disclosures dynamically render based on user geolocation.
- **Missing Evidence:**
  Lacks physical compliance evidence templates, such as Technical Documentation sheets or EU Responsible Person designation contracts.
- **Missing Audit Trail:**
  No historical tracking system exists to record updates to product safety notices or corrective action implementations.

### 1.3 Remediation and Action Plan
1. Establish a written General Product Safety Policy outlining Responsible Person designation and product scope.
2. Incorporate GPSR metadata requirements into `docs/PRE-SUBMISSION-CHECKLIST.md` and `data/rejection-patterns.json`.
3. Provide UI templates showing compliant product detail pages with embedded contact details and safety labels.
4. Build automated test runners to verify GPSR disclosure presence prior to app submission.

---

## 2. EU e-Evidence Package

### 2.1 Regulatory Overview and Background
The EU e-Evidence Package consists of Regulation (EU) 2023/1543 (European Production and Preservation Orders) and Directive (EU) 2023/1544 (Legal Representatives). Mandatory enforcement begins on 18 August 2026.

This framework empowers EU judicial authorities to issue orders directly to service providers in the EU, regardless of headquarters location. Standard production orders require response within 10 days, while emergency orders mandate data production within 8 hours.

Official Citation: Regulation (EU) 2023/1543 and Directive (EU) 2023/1544.

### 2.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Law Enforcement Request Policy exists to guide handling of incoming European Production and Preservation Orders.
- **Missing Documentation:**
  Lacks operational runbooks detailing protocols for handling 10-day standard and 8-hour emergency order workflows.
- **Missing Code:**
  No backend utilities or endpoints exist to extract, filter, or package user data in response to legal orders within 8 hours.
- **Missing Disclosure:**
  Privacy Policy templates do not explicitly notify users that data may be preserved or produced under Regulation (EU) 2023/1543.
- **Missing Logging:**
  No logging mechanisms capture incoming judicial orders, certificate validation statuses, or data extraction events.
- **Missing Testing:**
  No simulation tests exist to validate rapid 8-hour data extraction and encryption workflows under load.
- **Missing Evidence:**
  Lacks mock samples of European Production Order Certificates (EPOC) or Preservation Order Certificates (EPOC-PR) for verification testing.
- **Missing Audit Trail:**
  No tamper-proof, cryptographic audit log records administrative actions, data extractions, or legal transmissions.

### 2.3 Remediation and Action Plan
1. Draft a Law Enforcement Response Protocol detailing emergency roles and communication channels.
2. Formally designate an EU establishment or legal representative prior to 18 August 2026.
3. Develop secure backend extraction scripts to meet 8-hour emergency response SLAs.
4. Implement a cryptographic audit trail logging all incoming orders and outgoing transmissions.

---

## 3. EU Contract Withdrawal Button

### 3.1 Regulatory Overview and Background
Directive (EU) 2023/2673 amends Directive 2011/83/EU regarding distance financial services contracts, mandating a prominent, easily accessible withdrawal button on online interfaces. Member States apply these rules from 19 June 2026.

The withdrawal right spans 14 days from contract conclusion. The cancellation path must be as direct and frictionless as the signup process.

Official Citation: Directive (EU) 2023/2673 of the European Parliament and of the Council.

### 3.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Consumer Contract Withdrawal Policy template exists for managing statutory 14-day cancellation rights.
- **Missing Documentation:**
  Lacks UI/UX design guidelines outlining withdrawal button positioning, prominence, and wording expectations.
- **Missing Code:**
  No client-side or backend code templates implement a functional withdrawal button or modal sheet.
- **Missing Disclosure:**
  Subscription checkout screens do not prominently display statutory 14-day withdrawal rights or consequences.
- **Missing Logging:**
  No log schemas track withdrawal requests, timestamps, confirmation receipts, or refund initiations.
- **Missing Testing:**
  No end-to-end automated UI tests verify frictionless, self-service withdrawal execution.
- **Missing Evidence:**
  Lacks standardized templates for withdrawal acknowledgement notices or cancellation receipts.
- **Missing Audit Trail:**
  No audit trail tracks historical cancellation rates, interface modifications, or refund reconciliation logs.

### 3.3 Remediation and Action Plan
1. Create a Consumer Contract Withdrawal Policy aligned with Directive (EU) 2023/2673.
2. Add a prominent withdrawal button component to account settings in UI reference templates.
3. Build logging triggers capturing cancellation timestamps and refund events.
4. Implement automated UI tests confirming frictionless contract termination without human intervention.

---

## 4. US State App Store Accountability Acts (ASAA)

### 4.1 Regulatory Overview and Background
US State App Store Accountability Acts (Utah SB 142, Texas SB 2420, Louisiana HB 570, Alabama HB 161) regulate minors' access to apps, in-app purchases, and major updates.

Developers must request age categories (via Apple's Declared Age Range API or Google Play Age Signals API) and obtain verifiable parental consent before minor access, while deleting raw age verification data immediately after use.

Official Citations: Utah SB 142 (2025), Texas SB 2420 (2025), Louisiana HB 570 (2025), Alabama HB 161 (2026).

### 4.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Minor Age Assurance & Data Minimization Policy exists for state-level compliance.
- **Missing Documentation:**
  Checklists lack multi-platform integration guides for Declared Age Range API and Play Age Signals API.
- **Missing Code:**
  Mock mobile codebases lack native integrations querying age APIs or handling parental consent callbacks.
- **Missing Disclosure:**
  Onboarding screens do not inform users that age categories are requested to comply with state accountability laws.
- **Missing Logging:**
  No backend logs record parental consent receipt, consent revocation (`RESCIND_CONSENT`), or verification data deletion.
- **Missing Testing:**
  Test suites do not simulate age-band signals or verify that minor accounts are restricted pending consent.
- **Missing Evidence:**
  Lacks parental consent agreement templates or verification data minimization records.
- **Missing Audit Trail:**
  No audit log tracks age-gating rollout dates, consent policy updates, or raw data purging events.

### 4.3 Remediation and Action Plan
1. Draft a Minor Age Assurance Policy detailing state identification and data minimization rules.
2. Add cross-platform native hooks for Apple Declared Age Range and Google Play Age Signals APIs.
3. Implement automated purging routines to delete raw age verification data immediately after validation.
4. Write automated integration tests confirming minor purchase blocks in the absence of valid consent flags.

---

## 5. EU AI Act Article 4 (AI Literacy)

### 5.1 Regulatory Overview and Background
Article 4 of Regulation (EU) 2024/1689 mandates that providers and deployers of AI systems ensure a sufficient level of AI literacy among personnel operating AI features, live since 2 February 2025.

Applicable to all organizations regardless of size, compliance requires a written policy, training records, induction protocols, and regular refresh logs.

Official Citation: Regulation (EU) 2024/1689, Article 4.

### 5.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No corporate AI Literacy Policy template exists to establish required competency baselines.
- **Missing Documentation:**
  Lacks developer guides explaining Article 4 training duties, safety guidelines, and risk evaluation standards.
- **Missing Code:**
  No automated lint or script checks for the presence or freshness of internal AI literacy logs.
- **Missing Disclosure:**
  Public documentation and vendor contracts do not state organizational adherence to Article 4 literacy standards.
- **Missing Logging:**
  No centralized log template (`AI_LITERACY_LOG.md`) exists to record employee inductions and refreshers.
- **Missing Testing:**
  No CI checks verify that developers committing AI feature code possess up-to-date literacy records.
- **Missing Evidence:**
  Lacks sample evidence artifacts, such as completed literacy logs, course completions, or competency assessments.
- **Missing Audit Trail:**
  No historical audit trail tracks policy reviews, training curriculum updates, or personnel certification dates.

### 5.3 Remediation and Action Plan
1. Publish an internal AI Literacy Policy defining training topics (AI safety, risk, bias, privacy).
2. Maintain a centralized `AI_LITERACY_LOG.md` tracking staff completions and verification dates.
3. Designate a compliance coordinator for annual literacy reviews.
4. Add a CI workflow check warning if literacy logs are stale beyond 12 months.

---

## 6. EU AI Act Article 50 (Transparency Obligations)

### 6.1 Regulatory Overview and Background
Article 50 of Regulation (EU) 2024/1689 mandates transparency for AI systems, taking effect on 2 August 2026.

Requires disclosing direct AI interaction (Article 50(1)), marking synthetic outputs in machine-readable formats (Article 50(2)), and disclosing deepfakes (Article 50(4)).

Official Citation: Regulation (EU) 2024/1689, Article 50.

### 6.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No AI Transparency Policy template exists governing user disclosures and synthetic output marking.
- **Missing Documentation:**
  Lacks technical developer guides for implementing machine-readable watermarks (e.g. C2PA) and deepfake notices.
- **Missing Code:**
  Codebase templates lack helper utilities for injecting watermarks or metadata headers into generated media.
- **Missing Disclosure:**
  Conversational UI templates do not display initial disclosure prompts ("You are chatting with an AI assistant").
- **Missing Logging:**
  No logs record that transparency disclosures were successfully displayed during user sessions.
- **Missing Testing:**
  No tests verify that generated media contains required machine-readable markers or disclosures.
- **Missing Evidence:**
  Lacks sample compliance evidence, such as third-party moderation audits or metadata persistence proofs.
- **Missing Audit Trail:**
  No audit trail records modifications to transparency UI strings, model changes, or watermarking specs.

### 6.3 Remediation and Action Plan
1. Draft an AI Transparency and Disclosure Policy mandating user notices and output marking.
2. Embed prominent AI interaction notices across all conversational interface templates.
3. Integrate C2PA metadata injection inside synthetic asset generation pipelines.
4. Add automated tests verifying machine-readable compliance headers on generated media outputs.

---

## 7. EU Digital Markets Act (DMA)

### 7.1 Regulatory Overview and Background
The EU Digital Markets Act (Regulation (EU) 2022/1925) regulates gatekeeper platforms, enabling alternative app marketplaces, web distribution, and external purchase link promotion in the EU.

Developers utilizing DMA entitlements (`com.apple.developer.storekit.external-purchase-link`) must display mandatory disclosure sheets via `ExternalPurchaseCustomLink` and comply with monthly reporting.

Official Citation: Regulation (EU) 2022/1925 of the European Parliament and of the Council.

### 7.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No EU Alternative Distribution Policy exists to evaluate DMA entitlement trade-offs and fee structures.
- **Missing Documentation:**
  Lacks step-by-step developer guides for implementing DMA entitlements and external payment server APIs.
- **Missing Code:**
  Reference codebases lack implementations of `ExternalPurchaseCustomLink` or reporting server webhooks.
- **Missing Disclosure:**
  In-app checkout flows lack DMA disclosure sheet triggers explaining that transactions occur outside Apple/Google.
- **Missing Logging:**
  No backend logging schema captures external purchase click-throughs or transaction reporting payloads.
- **Missing Testing:**
  No unit or UI tests verify that StoreKit IAP and external links are strictly segregated per storefront.
- **Missing Evidence:**
  Lacks sample External Purchase Server API monthly reports or signed entitlement addenda.
- **Missing Audit Trail:**
  No audit trail records monthly sales reporting transmissions, entitlement declarations, or fee calculations.

### 7.3 Remediation and Action Plan
1. Draft an EU DMA Distribution Policy detailing fee models and entitlement requirements.
2. Provide code templates demonstrating `ExternalPurchaseCustomLink` triggers and Server API integrations.
3. Implement automated lints ensuring IAP and external links are never co-mingled on the same storefront.
4. Establish monthly automated reporting scripts for External Purchase Server API submissions.

---

## 8. EU Digital Services Act (DSA - Trader Status & Minor Protection)

### 8.1 Regulatory Overview and Background
The EU Digital Services Act (Regulation (EU) 2022/2065) mandates trader status verification (Articles 30-31) and minor protection measures for apps distributed in the EU.

Traders must publish verified address, phone, and email details on store listings. Non-traders must display notices that consumer protection laws do not apply.

Official Citation: Regulation (EU) 2022/2065 of the European Parliament and of the Council.

### 8.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No DSA Trader Assessment Policy exists to assist developers in determining legal trader status in the EU.
- **Missing Documentation:**
  Lacks developer guides detailing App Store Connect and Google Play Console DSA submission requirements.
- **Missing Code:**
  Scripts lack pre-submission checks verifying that DSA trader fields are completed prior to EU publishing.
- **Missing Disclosure:**
  Store listing templates do not include placeholders for published trader contact details or non-trader disclaimers.
- **Missing Logging:**
  No logs record trader verification submission dates, 2FA confirmations, or status updates.
- **Missing Testing:**
  No automated metadata audits flag missing DSA trader declarations as EU storefront removal risks.
- **Missing Evidence:**
  Lacks mock verification documents, such as official business registration proofs or D-U-N-S records.
- **Missing Audit Trail:**
  No audit log tracks changes to published trader addresses, contact emails, or legal entity names.

### 8.3 Remediation and Action Plan
1. Establish a DSA Compliance Protocol guiding trader classification and submission.
2. Integrate DSA trader field verification into `scripts/metadata-audit.py`.
3. Add automated pre-submission warnings for unverified DSA trader status when targeting EU storefronts.
4. Maintain historical logs of DSA submission receipts and verification documents.

---

## 9. European Accessibility Act (EAA - Directive (EU) 2019/882 & EN 301 549)

### 9.1 Regulatory Overview and Background
The European Accessibility Act (Directive (EU) 2019/882) became applicable on 28 June 2025, mandating digital accessibility across e-commerce, banking, e-books, and transport apps.

Compliance is measured against EN 301 549 (v3.2.1), which builds on WCAG 2.1 AA and includes Chapter 11 software requirements. Apps must also publish an accessibility statement.

Official Citation: Directive (EU) 2019/882 of the European Parliament and of the Council.

### 9.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Digital Accessibility Policy template exists establishing organizational EN 301 549 / WCAG 2.1 AA baselines.
- **Missing Documentation:**
  Lacks developer guides detailing EN 301 549 Chapter 11 mobile software requirements beyond standard WCAG.
- **Missing Code:**
  Static scanner scripts (`scripts/accessibility-audit.py`) cover basic rules but omit complete EN 301 549 checks.
- **Missing Disclosure:**
  Template web and mobile codebases lack published Accessibility Statement components or screen reader links.
- **Missing Logging:**
  No log schemas capture accessibility user feedback, reported barriers, or remediation tickets.
- **Missing Testing:**
  Automated tests do not cover screen reader focus order, Dynamic Type clipping, or switch control navigation.
- **Missing Evidence:**
  Lacks sample Accessibility Conformance Reports (VPAT / EN 301 549 audit statements).
- **Missing Audit Trail:**
  No audit trail records historical accessibility audits, barrier remediation timelines, or statement updates.

### 9.3 Remediation and Action Plan
1. Draft a comprehensive Accessibility Policy committing to EN 301 549 Chapter 11 standards.
2. Enhance `scripts/accessibility-audit.py` to test screen reader labels, contrast, and Dynamic Type scaling.
3. Add Accessibility Statement templates in `references/` and UI code bases.
4. Establish annual third-party accessibility audit workflows and record VPAT evidence.

---

## 10. US Children's Online Privacy Protection Act (Amended COPPA Rule - 16 CFR Part 312)

### 10.1 Regulatory Overview and Background
The FTC's Amended COPPA Rule (16 CFR Part 312, effective 23 June 2025, mandatory 22 April 2026) regulates data collection from children under 13.

Key changes include expanding PII to biometric and government IDs, requiring separate opt-in consent for third-party disclosures/ads, mandatory written retention policies, and written info-security programs.

Official Citation: 16 CFR Part 312 (FTC Amended COPPA Rule, 90 FR 16918).

### 10.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Children's Privacy Policy or Written Data Retention Policy template exists under Section 312.10.
- **Missing Documentation:**
  Lacks developer checklists for implementing separate third-party opt-in consent and biometric PII handling.
- **Missing Code:**
  Client templates lack dual-consent toggles separating core service consent from third-party ad sharing.
- **Missing Disclosure:**
  Onboarding flows lack clear disclaimers detailing biometric data collection and third-party disclosure opt-ins.
- **Missing Logging:**
  No logs capture parental consent timestamps, verification method details, or data retention expiration dates.
- **Missing Testing:**
  No automated tests verify that third-party SDKs are disabled prior to receiving verifiable parental consent.
- **Missing Evidence:**
  Lacks sample Information Security Program documentation or annual COPPA risk assessment records.
- **Missing Audit Trail:**
  No audit trail records parental consent revocations, child account deletions, or retention schedule purges.

### 10.3 Remediation and Action Plan
1. Create a COPPA Compliance Policy including data retention schedules and info-security program outlines.
2. Build UI onboarding templates with separate opt-in consent controls for third-party data sharing.
3. Add backend automated deletion scripts to purge child data upon retention expiration.
4. Implement automated tests verifying zero data transmission to ad networks for child profiles.

---

## 11. California Consumer Privacy Act / Privacy Rights Act (CCPA/CPRA & CPPA 2026 Regulations)

### 11.1 Regulatory Overview and Background
The California Consumer Privacy Act as amended by the CPRA (Cal. Civ. Code § 1798.100 et seq.) and CPPA 2026 Regulations grants California residents rights to know, delete, correct, and opt-out of data sale/sharing.

Apps must honor Global Privacy Control (GPC) signals, provide "Do Not Sell or Share My Personal Info" links, limit sensitive PI usage, and conduct cybersecurity audits.

Official Citation: California Civil Code § 1798.100 et seq.; CPPA Regulations (2026).

### 11.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No California Privacy Rights Policy template covers CPPA 2026 automated decision-making and sensitive PI limits.
- **Missing Documentation:**
  Lacks guides on processing Global Privacy Control (`Sec-GPC`) headers in webviews and native app equivalents.
- **Missing Code:**
  Codebases lack GPC signal detection listeners or native opt-out state propagation utilities.
- **Missing Disclosure:**
  UI templates lack explicit "Do Not Sell or Share My Personal Information" and "Limit Sensitive PI" links.
- **Missing Logging:**
  No logs record consumer DSAR requests (know, delete, correct, opt-out) or GPC signal receipts.
- **Missing Testing:**
  No unit tests verify that receiving a GPC signal or opt-out toggle immediately halts ad-tracking SDKs.
- **Missing Evidence:**
  Lacks sample Cybersecurity Audit reports or Automated Decision-Making Technology risk assessments.
- **Missing Audit Trail:**
  No audit trail records DSAR fulfillment timelines (45-day window) or consumer opt-out preferences.

### 11.3 Remediation and Action Plan
1. Draft a California Privacy Rights Policy incorporating CPPA 2026 rules and GPC mandates.
2. Add GPC header detection in webviews and native privacy preference centers.
3. Build automated DSAR tracking database schemas capturing request fulfillment dates.
4. Write integration tests confirming ad tracking suspension upon GPC signal activation.

---

## 12. Illinois Biometric Information Privacy Act (BIPA - 740 ILCS 14)

### 12.1 Regulatory Overview and Background
The Illinois Biometric Information Privacy Act (740 ILCS 14) regulates the collection, capture, purchase, and storage of biometric identifiers (fingerprints, voiceprints, retina/facial scans).

Requires written notice, e-signed release prior to collection, publicly available retention schedule, destruction within 3 years of last interaction, and prohibits sale.

Official Citation: 740 ILCS 14/1 et seq. (amended by SB 2979, 2024).

### 12.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Biometric Data Privacy Policy or Public Retention/Destruction Schedule template exists under Section 15(a).
- **Missing Documentation:**
  Lacks developer guides detailing BIPA consent workflows and biometric data isolation requirements.
- **Missing Code:**
  Codebases lack pre-capture consent modal components or automated 3-year destruction triggers.
- **Missing Disclosure:**
  UI flows lack explicit written disclaimers stating the specific purpose and length of biometric storage.
- **Missing Logging:**
  No logs record e-signed biometric releases, capture timestamps, or destruction verification hashes.
- **Missing Testing:**
  No tests verify that biometric capture SDKs fail closed if written consent is unverified.
- **Missing Evidence:**
  Lacks sample executed biometric consent agreements or destruction certificates.
- **Missing Audit Trail:**
  No tamper-proof audit trail tracks biometric data lifecycle, policy updates, or destruction events.

### 12.3 Remediation and Action Plan
1. Create a BIPA-compliant Biometric Information Policy and public retention schedule template.
2. Develop modal components requiring explicit e-signed consent before biometric SDK initialization.
3. Build database cleanup routines enforcing 3-year destruction schedules.
4. Implement automated integration tests ensuring biometric features block unconsented users.

---

## 13. US Federal & State Subscription Cancellation Requirements (ROSCA & State Negative Option Laws)

### 13.1 Regulatory Overview and Background
The Restore Online Shoppers' Confidence Act (ROSCA, 15 U.S.C. § 8401), FTC Act Section 5, and state negative option laws (California, New York, Massachusetts) regulate recurring subscriptions.

Developers billing subscriptions outside store IAPs (web signups, cross-platform billing) must provide clear disclosure, informed consent, and a cancellation mechanism as easy as signup (e.g. online click-to-cancel).

Official Citation: 15 U.S.C. § 8401; Cal. Bus. & Prof. Code § 17600 et seq.

### 13.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Subscription Cancellation Policy template exists governing non-IAP web and companion billing flows.
- **Missing Documentation:**
  Lacks developer guides detailing online click-to-cancel design requirements and anti-friction rules.
- **Missing Code:**
  Web and mobile account templates lack self-service cancellation buttons or automated refund routines.
- **Missing Disclosure:**
  Subscription checkout screens omit clear disclaimers regarding recurring billing amounts and cancellation paths.
- **Missing Logging:**
  No logs capture cancellation request timestamps, user feedback, or subscription termination confirmations.
- **Missing Testing:**
  No automated UI tests verify that online cancellation executes within 3 clicks without requiring calls/emails.
- **Missing Evidence:**
  Lacks sample cancellation confirmation emails or renewal reminder notice records.
- **Missing Audit Trail:**
  No audit trail tracks subscription modification dates, cancellation rates, or renewal notice dispatches.

### 13.3 Remediation and Action Plan
1. Draft a ROSCA-compliant Subscription Policy mandating simple online cancellation.
2. Build self-service cancellation components within web and account setting UI templates.
3. Implement automated pre-renewal notifications and cancellation confirmation emails.
4. Write UI tests confirming frictionless online cancellation flows.

---

## 14. UK Online Safety Act 2023 & ICO Children's Code

### 14.1 Regulatory Overview and Background
The UK Online Safety Act 2023 (enforced by Ofcom) and ICO Age Appropriate Design Code regulate online services accessible to UK children under 18.

Requires Highly Effective Age Assurance (facial estimation, credit card checks, open banking), default high privacy settings, geolocation/profiling off by default, and a mandatory DPIA.

Official Citation: UK Online Safety Act 2023 c. 50; ICO Age Appropriate Design Code.

### 14.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No UK Child Safety Policy or ICO Children's Code Compliance Policy template exists.
- **Missing Documentation:**
  Lacks developer guides detailing Ofcom-approved age assurance implementation and DPIA creation.
- **Missing Code:**
  Codebases lack default high-privacy settings, automatic geolocation disabling, or age verification hooks.
- **Missing Disclosure:**
  UGC and interaction flows lack age-assurance prompts and child safety warning disclaimers.
- **Missing Logging:**
  No logs record DPIA reviews, age assurance verification methods, or child safety report actions.
- **Missing Testing:**
  No automated tests verify that geolocation and profiling toggles default to OFF for UK child profiles.
- **Missing Evidence:**
  Lacks sample Data Protection Impact Assessments (DPIA) or Ofcom age-assurance audit reports.
- **Missing Audit Trail:**
  No audit trail tracks changes to child safety moderation rules, DPIA revisions, or age-gating parameters.

### 14.3 Remediation and Action Plan
1. Create a UK Online Safety and ICO Children's Code Policy template.
2. Implement code controls forcing high-privacy, zero-profiling defaults for UK child accounts.
3. Produce a standard DPIA template tailored for UK mobile and web deployments.
4. Write unit tests confirming geolocation features remain disabled for minor profiles.

---

## 15. Australia Online Safety Amendment (Social Media Minimum Age) Act 2024

### 15.1 Regulatory Overview and Background
Australia's Online Safety Amendment Act 2024 (enforceable 10 December 2025) requires age-restricted social media platforms to take reasonable steps to prevent under-16s from holding accounts.

Age assurance must follow eSafety waterfall guidelines (self-declaration prohibited as sole method), and age data must be ringfenced and destroyed immediately after verification.

Official Citation: Online Safety Amendment (Social Media Minimum Age) Act 2024.

### 15.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Australian Social Media Minimum Age Policy template exists for age-restricted services.
- **Missing Documentation:**
  Lacks developer guides detailing eSafety age assurance waterfall methods and data ringfencing rules.
- **Missing Code:**
  Codebases lack native age verification waterfall integrations or immediate age-data purging routines.
- **Missing Disclosure:**
  Account creation flows lack notices explaining age restrictions and mandatory data destruction policies.
- **Missing Logging:**
  No logs record age verification status, data destruction timestamps, or under-16 account blocks.
- **Missing Testing:**
  No automated tests verify that under-16 accounts are blocked from social media feature access.
- **Missing Evidence:**
  Lacks sample eSafety compliance audit reports or data destruction verification certificates.
- **Missing Audit Trail:**
  No audit log tracks age-gating enforcement changes, blocked account counts, or raw data purges.

### 15.3 Remediation and Action Plan
1. Draft an Australian Under-16 Age Restriction Policy aligning with eSafety standards.
2. Build age verification waterfall components with immediate backend data destruction.
3. Implement automated purging routines destroying raw age verification data post-validation.
4. Add integration tests verifying account blocking for under-16 profiles in Australia.

---

## 16. Brazil Digital ECA (Law 15,211/2025 & LGPD)

### 16.1 Regulatory Overview and Background
Brazil's Digital ECA (Law 15,211/2025, enforceable 17 March 2026) amends child protection rules on top of LGPD.

Mandates approved age verification (document check, facial estimation, CPF database check; checkboxes prohibited) and requires Google Play Age Signals / Apple age gating integration.

Official Citation: Law No. 15,211/2025; Lei Geral de Proteção de Dados (LGPD, Law No. 13,709/2018).

### 16.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Brazilian Digital ECA Compliance Policy template exists detailing child data protection rules.
- **Missing Documentation:**
  Lacks developer checklists for implementing CPF validation, facial age estimation, and LGPD child consent.
- **Missing Code:**
  Codebases lack native integrations for Play Age Signals API (Brazil rollout 17 March 2026) or CPF verification.
- **Missing Disclosure:**
  Onboarding flows lack disclaimers detailing age verification requirements under Law 15,211/2025.
- **Missing Logging:**
  No logs capture parental consent confirmations, CPF verification hashes, or age signal responses.
- **Missing Testing:**
  No automated tests verify that simple checkbox self-declarations fail validation for Brazilian users.
- **Missing Evidence:**
  Lacks sample LGPD Relatório de Impacto à Proteção de Dados Pessoais (RIPD) for child data.
- **Missing Audit Trail:**
  No audit trail tracks age verification method updates, parental consent logs, or RIPD revisions.

### 16.3 Remediation and Action Plan
1. Create a Digital ECA Policy and RIPD template for Brazilian deployments.
2. Integrate Google Play Age Signals API and Apple Declared Age Range hooks for Brazil.
3. Build backend validation routines rejecting self-declaration checkboxes for Brazilian accounts.
4. Write unit tests confirming minor feature restrictions pending verified consent.

---

## 17. India Digital Personal Data Protection Act (DPDPA 2023 & DPDP Rules 2025)

### 17.1 Regulatory Overview and Background
India's DPDPA 2023 and DPDP Rules 2025 (notified 13 November 2025, consent rules active 13 May 2027) regulate personal data processing.

Requires verifiable parental consent via government-backed systems (e.g. DigiLocker) for users under 18, and bans behavioral tracking or targeted ads directed at children.

Official Citation: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023); DPDP Rules 2025.

### 17.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No India DPDPA Data Protection Policy or Child Data Processing Policy template exists.
- **Missing Documentation:**
  Lacks developer guides detailing DigiLocker integration and under-18 ad-tracking prohibitions.
- **Missing Code:**
  Codebases lack DigiLocker verifiable consent API hooks or under-18 ad-blocking logic.
- **Missing Disclosure:**
  Consent notices lack multilingual disclaimers (specified in 8th Schedule languages) required by DPDPA.
- **Missing Logging:**
  No logs capture parental consent tokens, DigiLocker verification receipts, or Consent Manager requests.
- **Missing Testing:**
  No automated tests verify that behavioral tracking SDKs are hard-disabled for under-18 Indian profiles.
- **Missing Evidence:**
  Lacks sample Data Protection Impact Assessments or Significant Data Fiduciary audit filings.
- **Missing Audit Trail:**
  No audit trail records consent withdrawals, Data Principal grievance logs, or DigiLocker token purges.

### 17.3 Remediation and Action Plan
1. Draft a DPDPA Compliance Policy including multilingual consent notice guidelines.
2. Build integration components for DigiLocker parental verification.
3. Implement automated tracking suppression for under-18 users in India.
4. Add unit tests confirming complete ad-SDK disabling for minor accounts.

---

## 18. Singapore Personal Data Protection Act (PDPA) & IMDA App Store Age Assurance Code

### 18.1 Regulatory Overview and Background
Singapore's PDPA and IMDA Code of Practice for Online Safety (effective 1 April 2026) mandate data protection and app store age assurance.

Requires screening and stopping under-18 users from downloading age-inappropriate apps, appointing a DPO, reporting breaches within 3 days, and destroying age data after use.

Official Citation: Personal Data Protection Act 2012; IMDA Code of Practice for Online Safety (2026).

### 18.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No Singapore PDPA & IMDA Online Safety Policy template exists.
- **Missing Documentation:**
  Lacks developer guides detailing 3-day breach notification rules and IMDA age assurance checks.
- **Missing Code:**
  Codebases lack age assurance screening hooks or automated 3-day breach notification dispatch routines.
- **Missing Disclosure:**
  UI flows lack disclaimers identifying the appointed Data Protection Officer (DPO) and age assurance purpose.
- **Missing Logging:**
  No logs capture age assurance verification outcomes, age data destruction timestamps, or DPO contacts.
- **Missing Testing:**
  No automated tests verify that 18-plus rated app binaries block unverified Singapore downloads.
- **Missing Evidence:**
  Lacks sample Data Protection Impact Assessments or PDPC breach notification templates.
- **Missing Audit Trail:**
  No audit trail records DPO appointment logs, breach incident timelines, or age data deletion logs.

### 18.3 Remediation and Action Plan
1. Create a Singapore PDPA Policy including DPO contact templates and breach response protocols.
2. Implement age assurance screening hooks and backend age data deletion triggers.
3. Add 3-day breach notification workflows inside incident response runbooks.
4. Write integration tests validating age-gating enforcement for Singapore storefronts.

---

## 19. South Korea Telecommunications Business Act & Personal Information Protection Act (PIPA)

### 19.1 Regulatory Overview and Background
South Korea's Telecommunications Business Act mandates alternative in-app payments, while PIPA regulates data protection and cross-border transfers.

Alternative payment requires a Korea-only binary (`com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`), 26% commission reporting, modal disclaimers, and local payment gateways.

Official Citation: Telecommunications Business Act; Personal Information Protection Act (PIPA).

### 19.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No South Korea Alternative Payment & PIPA Data Transfer Policy template exists.
- **Missing Documentation:**
  Lacks developer guides detailing Korea-only binary creation, approved gateways (KCP, Toss), and PIPA transfers.
- **Missing Code:**
  Codebases lack native modal sheet disclaimers or monthly 15-day sales reporting scripts for Korea.
- **Missing Disclosure:**
  Checkout flows lack Korean modal disclaimers informing users that Apple/Google purchase protection does not apply.
- **Missing Logging:**
  No logs record external payment transactions, monthly remittance calculations, or PIPA consent transfers.
- **Missing Testing:**
  No automated tests verify that Korean alternative billing links open approved native payment gateways.
- **Missing Evidence:**
  Lacks sample Korean monthly sales reporting sheets or PIPA cross-border transfer agreements.
- **Missing Audit Trail:**
  No audit trail tracks monthly remittance submissions, entitlement declarations, or payment gateway audits.

### 19.3 Remediation and Action Plan
1. Draft a South Korea In-App Billing Policy detailing entitlement and reporting rules.
2. Build UI modal sheet components and native gateway integration helpers for Korea.
3. Develop monthly sales reporting scripts for StoreKit External Purchase API (Korea).
4. Write UI tests confirming native payment gateway invocation for Korean binaries.

---

## 20. China Mobile App Filing (MIIT / ICP Extension) & PIPL

### 20.1 Regulatory Overview and Background
China's Ministry of Industry and Information Technology (MIIT) mandates Mobile App Filing (ICP extension), local partnership, PIPL data localization, real-name verification, and Banhao gaming licenses.

Foreign developers must partner with Chinese local entities to submit filing details, enforce real-name ID verification, and localize personal data within mainland China.

Official Citation: MIIT Notice on Mobile Application Filing (2023); Personal Information Protection Law (PIPL).

### 20.2 Comprehensive Gap Analysis Across the Eight Compliance Categories

- **Missing Policy:**
  No China App Filing & PIPL Data Localization Policy template exists.
- **Missing Documentation:**
  Lacks developer checklists detailing MIIT filing submissions, local entity requirements, and Banhao licensing.
- **Missing Code:**
  Codebases lack real-name ID verification integration components or data localization endpoint routers.
- **Missing Disclosure:**
  UI onboarding flows lack PIPL-compliant privacy notices and real-name registration disclaimers.
- **Missing Logging:**
  No logs capture MIIT filing approval numbers, real-name verification tokens, or data localization transfers.
- **Missing Testing:**
  No automated tests verify that non-filed binaries fail pre-submission checks when targeting China.
- **Missing Evidence:**
  Lacks sample MIIT App Filing registration certificates or PIPL Personal Information Impact Assessments.
- **Missing Audit Trail:**
  No audit trail tracks MIIT filing updates, real-name verification system audits, or data localization logs.

### 20.3 Remediation and Action Plan
1. Establish a China Compliance Policy detailing MIIT filing and local partner requirements.
2. Integrate MIIT filing number verification into `scripts/metadata-audit.py`.
3. Build real-name ID verification modal components for mainland China deployments.
4. Add automated checks verifying Banhao license metadata for game apps targeting China.

---

## 21. Consolidated Gap Classification Matrix

The matrix below evaluates repository coverage across all twenty major regulatory frameworks and eight compliance gap categories.
- **Covered:** Comprehensive policy, documentation, code, or tests exist in the repository.
- **Partial:** Framework is cited with dated sources, but complete operational code, checklists, or automated tests are incomplete.
- **Missing:** Framework or category is absent from the repository.

| Regulatory framework | Policy | Documentation | Code | Disclosure | Logging | Testing | Evidence | Audit trail |
|---|---|---|---|---|---|---|---|---|
| **1. EU GPSR** | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| **2. EU e-Evidence** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **3. EU withdrawal button** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **4. US state ASAA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **5. EU AI Act Art 4** | Partial | Covered | N/A | Partial | Missing | Missing | Missing | Missing |
| **6. EU AI Act Art 50** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **7. EU DMA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **8. EU DSA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **9. European Accessibility Act** | Partial | Covered | Partial | Partial | Missing | Partial | Missing | Missing |
| **10. US COPPA (Amended)** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **11. California CCPA/CPRA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **12. Illinois BIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **13. US Subscription Cancel** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **14. UK Online Safety / ICO** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **15. Australia Min Age** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **16. Brazil Digital ECA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **17. India DPDPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **18. Singapore PDPA / IMDA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **19. South Korea TBA / PIPA** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |
| **20. China App Filing / PIPL** | Partial | Covered | Missing | Partial | Missing | Missing | Missing | Missing |

---

## 22. Conclusion and Future Monitoring

This comprehensive audit of twenty major global and regional regulations highlights a key pattern: while the repository excels at documenting store guidelines and regulatory deadlines (providing robust documentation and citations), operational implementation layers-specifically native code templates, automated guard rules, structured logging schemas, and integration test suites-remain missing across many frameworks.

In priority order:
1. Complete operational code components for high-risk imminent enforcement dates (EU AI Act Art 50 transparency, EU Contract Withdrawal button, US State ASAAs, and EU GPSR metadata).
2. Integrate static scanner rules into `agent-os/hooks/app-store-compliance-guard.sh` and `scripts/metadata-audit.py` to catch regulatory omissions pre-submission.
3. Build reusable UI components and backend database schemas for logging DSAR requests, parental consent, and biometric deletion records.

---

## 23. Sources

Every regulation cited above is mapped directly to its official primary source:

- EU GPSR: [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- EU e-Evidence Package: [Regulation (EU) 2023/1543](https://eur-lex.europa.eu/eli/reg/2023/1543/oj) and [Directive (EU) 2023/1544](https://eur-lex.europa.eu/eli/dir/2023/1544/oj)
- EU Distance Marketing / Withdrawal: [Directive (EU) 2023/2673](https://eur-lex.europa.eu/eli/dir/2023/2673/oj)
- US State ASAAs: [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html), [Texas SB 2420](https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=SB2420), [Louisiana HB 570](https://www.legis.la.gov/legis/BillInfo.aspx?i=246387)
- EU AI Act: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- EU Digital Markets Act: [Regulation (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)
- EU Digital Services Act: [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)
- European Accessibility Act: [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj)
- US COPPA Rule: [16 CFR Part 312 (FTC)](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- California CCPA/CPRA: [Cal. Civ. Code § 1798.100](https://oag.ca.gov/privacy/ccpa)
- Illinois BIPA: [740 ILCS 14](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2946)
- US ROSCA: [15 U.S.C. § 8401](https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act)
- UK Online Safety Act: [UK Online Safety Act 2023 c. 50](https://www.legislation.gov.uk/ukpga/2023/50/enacted)
- Australia Online Safety Act: [Online Safety Amendment Act 2024](https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId=r7279)
- Brazil Digital ECA: [Lei Nº 15.211/2025](https://www.in.gov.br/)
- India DPDPA: [Digital Personal Data Protection Act 2023](https://egazette.gov.in/)
- Singapore PDPA / IMDA Code: [IMDA Code of Practice for Online Safety](https://www.imda.gov.sg/)
- South Korea TBA & PIPA: [Telecommunications Business Act & PIPA](https://www.pipc.go.kr/)
- China MIIT App Filing & PIPL: [MIIT App Filing Notice](https://www.miit.gov.cn/)
