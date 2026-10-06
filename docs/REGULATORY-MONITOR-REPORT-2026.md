<!-- REGULATORY_MONITOR_START -->

> **Simulated output, not live announcements.** This file was generated from sample
> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,
> publish dates, and descriptions below are examples that show the shape of a migration
> report, not real publications. Only the linked official documentation URLs are real.
> Re-run the monitor with `--live` against the real feeds before treating anything here
> as an actual requirement.

# Global Regulatory Intelligence Monitoring Report (2026)

This comprehensive compliance report is continuously updated by `scripts/monitor-regulatory.py` to evaluate global regulatory developments across key jurisdictions.

## Jurisdictional Coverage Overview

- **European Union**: EU AI Act, GDPR, Data Act, Data Governance Act, Cyber Resilience Act, NIS2, Digital Services Act, Digital Markets Act, ePrivacy Directive, European Accessibility Act, Product Liability Directive, AI Liability Directive, EU GPSR
- **United Kingdom**: UK Online Safety Act, ICO Children's Code, UK AI Regulation (DSIT, FCA, CMA, ICO)
- **United States**: US COPPA (FTC), US NIST AI RMF & CISA, US State ASAA, US State AI Legislation (California, Utah, Colorado)
- **Canada**: Canada OPC & AIDA (Artificial Intelligence and Data Act)
- **Australia**: Australia Online Safety & eSafety, Australia OAIC & AI Governance
- **Singapore**: Singapore IMDA & Online Safety, Singapore PDPC & AI Verify Framework
- **International**: International Standards (ISO/IEC 42001, ISO/IEC 27001, OECD AI Principles, G7/G20)

## Monitored Developments Log & Evaluation

### 1. [European Union] EU AI Act
- **Announcement Title**: EU AI Act Article 50 Transparency Obligations taking full effect in August 2026
- **Published Date**: Fri, 08 May 2026 12:00:00 GMT
- **Official Resource Link**: [https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act](https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Critical
- **Scan Verdict**: Found 31 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `README.md`
  - `templates/REVIEW-NOTES-TEMPLATE.md`
  - `references/guidelines/by-app-type/ai-and-generative-apps.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `references/rules/safety.md`
  - `references/rules/android.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/ADVANCED-2026.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/COMPETITIVE-GAP-ANALYSIS.md`
  - `docs/APPLE.md`
  - `docs/AI-POLICY-MIGRATION.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `scripts/metadata-audit.py`
  - `scripts/release-audit.py`
  - `scripts/monitor-android.py`
  - `scripts/monitor-regulatory.py`
  - `scripts/monitor.py`
  - `scripts/monitor-privacy.py`
  - `scripts/monitor-ai-policy.py`
  - `data/regulatory-deadlines.json`
  - `data/detection-recipes.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Add clear in-app disclosures: 'You are interacting with an AI system.'
  - [ ] Mark all synthetic text, audio, images, or video in a machine-readable format.
  - [ ] Verify that no prohibited practices (such as biometric classification of sensitive traits) are used.
  - [ ] Document a team AI literacy policy in compliance with Article 4.

### 2. [European Union] EU GPSR
- **Announcement Title**: EU General Product Safety Regulation (GPSR) enforcement fully applicable across EU Member States
- **Published Date**: Fri, 13 Dec 2024 09:00:00 GMT
- **Official Resource Link**: [https://eur-lex.europa.eu/eli/reg/2023/988/oj](https://eur-lex.europa.eu/eli/reg/2023/988/oj)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: High
- **Scan Verdict**: Found 10 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `references/rules/payments.md`
  - `references/rules/safety.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/MISTAKE-PATTERNS.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `scripts/monitor-android.py`
  - `scripts/monitor-regulatory.py`
  - `data/detection-recipes.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Ensure e-commerce product detail templates display manufacturer identity (name, registered trade name/trademark).
  - [ ] Provide manufacturer postal address and electronic address (email or website) directly on the interface.
  - [ ] Display relevant product safety warnings or instructions in languages accepted by the member states of distribution.
  - [ ] Formally verify that an EU-based Responsible Person is designated for any products sold to EU consumers.

### 3. [United States] US COPPA
- **Announcement Title**: FTC issues final updates to the COPPA Children's Online Privacy Rule
- **Published Date**: Tue, 22 Apr 2025 09:00:00 GMT
- **Official Resource Link**: [https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Critical
- **Scan Verdict**: Found 25 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `AGENTS.md`
  - `README.md`
  - `references/README.md`
  - `references/guidelines/by-app-type/kids-category-and-families.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `references/rules/android.md`
  - `agent-os/commands/app-store-audit.md`
  - `agent-os/skill/SKILL.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/SECURITY-POLICY-MIGRATION.md`
  - `docs/ADVANCED-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/COMPETITIVE-GAP-ANALYSIS.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/MOBILE-SECURITY-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`

  **Recommended Migration Tasks**:
  - [ ] Implement verifiable parental consent methods (such as government photo ID verification) before collecting minor PII.
  - [ ] Maintain a written data retention policy with an automated purging schedule for minor accounts.
  - [ ] Ensure zero ad-tracking SDKs are active inside child-targeted sections.

### 4. [European Union] European Accessibility Act
- **Announcement Title**: European Accessibility Act enforcement begins across all EU Member States
- **Published Date**: Sat, 28 Jun 2025 08:00:00 GMT
- **Official Resource Link**: [https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: High
- **Scan Verdict**: Found 9 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `AGENTS.md`
  - `README.md`
  - `references/rules/performance.md`
  - `references/rules/android.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/PLATFORM-MECHANICS-2026.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`

  **Recommended Migration Tasks**:
  - [ ] Audit all UI components to ensure screen-reader labels (accessibilityLabel) and traits are present.
  - [ ] Verify support for system-wide font scaling (Dynamic Type) without breaking the layout.
  - [ ] Maintain WCAG 2.1 AA color contrast compliance (at least 4.5:1 for normal text).
  - [ ] Draft and publish an official accessibility statement reachable from within the app.

### 5. [United Kingdom] UK Online Safety Act
- **Announcement Title**: UK Ofcom issues final guidance under UK Online Safety Act for App Stores and Platforms
- **Published Date**: Mon, 10 Nov 2025 10:00:00 GMT
- **Official Resource Link**: [https://www.ofcom.org.uk/online-safety/protecting-children](https://www.ofcom.org.uk/online-safety/protecting-children)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Critical
- **Scan Verdict**: Found 21 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `references/guidelines/by-app-type/kids-category-and-families.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/PLATFORM-MECHANICS-2026.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/ADVANCED-2026.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `data/regulatory-deadlines.json`
  - `data/detection-recipes.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Upgrade minor age assurance flows to leverage verified methods (such as document checking or facial age estimation).
  - [ ] Store and process verification data in a ringfenced environment and destroy it immediately after use.
  - [ ] Verify that default privacy settings for minor accounts are highly restrictive.

### 6. [European Union] Data Act
- **Announcement Title**: Canada AIDA and OPC issue joint principles for Generative AI deployment
- **Published Date**: Wed, 14 Jan 2026 11:00:00 GMT
- **Official Resource Link**: [https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/](https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Medium
- **Scan Verdict**: Found 8 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `references/guidelines/by-app-type/health-fitness-and-medical.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `scripts/monitor-regulatory.py`
  - `scripts/monitor-privacy.py`
  - `data/regulatory-deadlines.json`

  **Recommended Migration Tasks**:
  - [ ] Implement secure, user-accessible endpoints or download options for all user-generated device data.
  - [ ] Provide transparent disclosures about how and when device sensor data is processed.
  - [ ] Ensure data portability features are integrated into smart device companion apps.

### 7. [Canada] Canada OPC and AIDA
- **Announcement Title**: Canada AIDA and OPC issue joint principles for Generative AI deployment
- **Published Date**: Wed, 14 Jan 2026 11:00:00 GMT
- **Official Resource Link**: [https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/](https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: High
- **Scan Verdict**: Found 21 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `templates/REVIEW-NOTES-TEMPLATE.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `references/rules/safety.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/ADVANCED-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/APPLE.md`
  - `docs/AI-POLICY-MIGRATION.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `scripts/metadata-audit.py`
  - `scripts/release-audit.py`
  - `scripts/monitor-android.py`
  - `scripts/monitor-regulatory.py`
  - `scripts/monitor.py`
  - `scripts/monitor-ai-policy.py`

  **Recommended Migration Tasks**:
  - [ ] Formulate plain-language Canadian privacy disclosures for AI features.
  - [ ] Establish risk mitigation mechanisms for generative AI outputs.

### 8. [Australia] Australia Online Safety
- **Announcement Title**: Australia eSafety Commissioner enforces Social Media Minimum Age rules
- **Published Date**: Thu, 19 Feb 2026 09:00:00 GMT
- **Official Resource Link**: [https://www.esafety.gov.au/about-us/industry-regulation](https://www.esafety.gov.au/about-us/industry-regulation)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Critical
- **Scan Verdict**: Found 31 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `AGENTS.md`
  - `README.md`
  - `references/README.md`
  - `references/guidelines/by-app-type/games.md`
  - `references/guidelines/by-app-type/social-and-user-generated-content.md`
  - `references/rules/payments.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/design.md`
  - `references/rules/metadata.md`
  - `references/rules/android.md`
  - `agent-os/commands/app-store-audit.md`
  - `agent-os/skill/SKILL.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/PLATFORM-MECHANICS-2026.md`
  - `docs/GAMBLING-MATRIX.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/MISTAKE-PATTERNS.md`
  - `docs/ADVANCED-2026.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/CROSS-PLATFORM-FRAMEWORKS.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `docs/OPEN-SOURCE-PATTERNS.md`

  **Recommended Migration Tasks**:
  - [ ] Enforce robust age estimation or verification for social elements on Australian storefronts.
  - [ ] Ringfence and completely destroy age verification data to comply with eSafety rules.

### 9. [Singapore] Singapore Online Safety
- **Announcement Title**: Singapore IMDA and PDPC update Model AI Governance Framework for Generative AI
- **Published Date**: Tue, 10 Mar 2026 08:00:00 GMT
- **Official Resource Link**: [https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework](https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Critical
- **Scan Verdict**: Found 17 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `agent-os/commands/app-store-audit.md`
  - `agent-os/skill/SKILL.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/PLATFORM-MECHANICS-2026.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`

  **Recommended Migration Tasks**:
  - [ ] Adopt native platform age-assurance APIs for users on the Singapore storefront.
  - [ ] Verify that no age verification data is stored longer than legally necessary.

### 10. [Singapore] Singapore PDPC and AI Verify
- **Announcement Title**: Singapore IMDA and PDPC update Model AI Governance Framework for Generative AI
- **Published Date**: Tue, 10 Mar 2026 08:00:00 GMT
- **Official Resource Link**: [https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework](https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: Medium
- **Scan Verdict**: Found 23 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `templates/REVIEW-NOTES-TEMPLATE.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/metadata.md`
  - `references/rules/safety.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/GAP-ANALYSIS-2026-09.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/ADVANCED-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/APPLE.md`
  - `docs/AI-POLICY-MIGRATION.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `scripts/metadata-audit.py`
  - `scripts/release-audit.py`
  - `scripts/monitor-android.py`
  - `scripts/monitor-regulatory.py`
  - `scripts/monitor.py`
  - `scripts/monitor-ai-policy.py`
  - `data/regulatory-deadlines.json`
  - `data/detection-recipes.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Conduct safety testing using AI Verify framework evaluation parameters.
  - [ ] Document AI alignment and safety safeguards for regional distribution.

### 11. [International] International AI and Security Standards
- **Announcement Title**: ISO/IEC 42001 Artificial Intelligence Management System International Standard Guidance
- **Published Date**: Wed, 15 Apr 2026 14:00:00 GMT
- **Official Resource Link**: [https://www.iso.org/standard/81230.html](https://www.iso.org/standard/81230.html)
- **Verification Status**: Verified (Priority 1 Official Source)
- **Compliance Impact Level**: High
- **Scan Verdict**: Found 33 file(s) containing active compliance signals.

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `AGENTS.md`
  - `README.md`
  - `references/rules/performance.md`
  - `references/rules/entitlements.md`
  - `references/rules/android.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/OTHER-STORES.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/PLATFORM-MECHANICS-2026.md`
  - `docs/MOBILE-PRIVACY-MONITOR-2026.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/SECURITY-POLICY-MIGRATION.md`
  - `docs/ADVANCED-2026.md`
  - `docs/CREDITS.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/PRIVACY-POLICY-MIGRATION.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/MOBILE-SECURITY-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `docs/OPEN-SOURCE-PATTERNS.md`
  - `scripts/monitor-security.py`
  - `scripts/release-audit.py`
  - `scripts/monitor-android.py`
  - `scripts/monitor-regulatory.py`
  - `scripts/monitor.py`
  - `scripts/monitor-privacy.py`
  - `data/regulatory-deadlines.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Align AI governance procedures with ISO/IEC 42001 management system controls.
  - [ ] Maintain an ISO 27001 compliant information security risk management process.

### 12. [European Union] GDPR
- **Announcement Title**: Unverified rumors of GDPR policy changes on Reddit forum
- **Published Date**: Sun, 26 Jul 2026 12:00:00 GMT
- **Official Resource Link**: [https://reddit.com/r/privacy/comments/12345/GDPR_rumor](https://reddit.com/r/privacy/comments/12345/GDPR_rumor)
- **Verification Status**: BLOCKED (Unverified Priority 4/5 Source)
- **Compliance Impact Level**: High
- **Scan Verdict**: BLOCKED: Compliance Pull Request generation blocked. Announcement source is Priority 5 (unverified secondary source).

  **Identified Affected Files**:
  - `CHANGELOG.md`
  - `AGENTS.md`
  - `README.md`
  - `references/guidelines/by-app-type/vpn-and-networking.md`
  - `references/rules/privacy.md`
  - `references/rules/performance.md`
  - `references/rules/android.md`
  - `docs/EU-REGULATORY-2026.md`
  - `docs/REGULATORY-TIMELINE.md`
  - `docs/BY-APP-TYPE.md`
  - `docs/ANDROID-POLICY-MIGRATION.md`
  - `docs/MOBILE-PRIVACY-MONITOR-2026.md`
  - `docs/GOOGLE-PLAY.md`
  - `docs/ADVANCED-2026.md`
  - `docs/REGULATORY-GAP-REPORT-2026.md`
  - `docs/GLOBAL-REGULATORY-2026.md`
  - `docs/REGULATORY_COMPLIANCE_PR_DRAFT.md`
  - `docs/PRIVACY-POLICY-MIGRATION.md`
  - `docs/APPLE.md`
  - `docs/REGULATORY-MONITOR-REPORT-2026.md`
  - `docs/PRE-SUBMISSION-CHECKLIST.md`
  - `data/regulatory-deadlines.json`
  - `data/detection-recipes.json`
  - `data/rejection-patterns.json`

  **Recommended Migration Tasks**:
  - [ ] Ensure the app implements a clear, prominent consent modal before collecting personal data.
  - [ ] Offer a genuine in-app account deletion mechanism that removes all associated personal data.
  - [ ] Audit all analytics and tracking SDKs to ensure data flows are disabled until opt-in consent is given.

<!-- REGULATORY_MONITOR_END -->
