<!-- REGULATORY_POLICY_MONITOR_START -->
# Regulatory Policy Monitoring & Compliance Report

This report is continuously generated and updated by `scripts/monitor-regulatory.py` to keep track of global regulatory changes.

## Latest Monitored Policy Changes

### EU AI Act Article 50 Transparency Obligations taking full effect in August 2026 (EU AI Act)
- **Published**: Fri, 08 May 2026 12:00:00 GMT
- **Official Link**: [https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act](https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act)
- **Jurisdiction**: European Union
- **Impact Level**: Critical
- **Scan Verdict**: Found 23 file(s) containing active compliance signals.
- **Suggested Migration Tasks**:
    - [ ] Add clear in-app disclosures: 'You are interacting with an AI system.'
    - [ ] Mark all synthetic text, audio, images, or video in a machine-readable format.
    - [ ] Verify that no prohibited practices (such as biometric classification of sensitive traits) are used.
    - [ ] Document a team AI literacy policy in compliance with Article 4.

### FTC issues final updates to the COPPA Children's Online Privacy Rule (US COPPA)
- **Published**: Tue, 22 Apr 2025 09:00:00 GMT
- **Official Link**: [https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- **Jurisdiction**: United States (Federal)
- **Impact Level**: Critical
- **Scan Verdict**: Found 20 file(s) containing active compliance signals.
- **Suggested Migration Tasks**:
    - [ ] Implement verifiable parental consent methods (such as government photo ID verification) before collecting minor PII.
    - [ ] Maintain a written data retention policy with an automated purging schedule for minor accounts.
    - [ ] Ensure zero ad-tracking SDKs are active inside child-targeted sections.

### European Accessibility Act enforcement begins across all EU Member States (European Accessibility Act)
- **Published**: Sat, 28 Jun 2025 08:00:00 GMT
- **Official Link**: [https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)
- **Jurisdiction**: European Union
- **Impact Level**: High
- **Scan Verdict**: Found 10 file(s) containing active compliance signals.
- **Suggested Migration Tasks**:
    - [ ] Audit all UI components to ensure screen-reader labels (accessibilityLabel) and traits are present.
    - [ ] Verify support for system-wide font scaling (Dynamic Type) without breaking the layout.
    - [ ] Maintain WCAG 2.1 AA color contrast compliance (at least 4.5:1 for normal text).
    - [ ] Draft and publish an official accessibility statement reachable from within the app.

### Unverified rumors of GDPR policy changes on Reddit forum (GDPR)
- **Published**: Sun, 26 Jul 2026 12:00:00 GMT
- **Official Link**: [https://reddit.com/r/privacy/comments/12345/GDPR_rumor](https://reddit.com/r/privacy/comments/12345/GDPR_rumor)
- **Jurisdiction**: European Union
- **Impact Level**: High
- **Scan Verdict**: BLOCKED: Compliance Pull Request generation blocked. Announcement source is Priority 5 (unverified secondary source).
- **Suggested Migration Tasks**:
    - [ ] Ensure the app implements a clear, prominent consent modal before collecting personal data.
    - [ ] Offer a genuine in-app account deletion mechanism that removes all associated personal data.
    - [ ] Audit all analytics and tracking SDKs to ensure data flows are disabled until opt-in consent is given.

<!-- REGULATORY_POLICY_MONITOR_END -->