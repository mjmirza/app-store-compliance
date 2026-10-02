<!-- STANDARDS_POLICY_MONITOR_START -->

> **Simulated output, not live announcements.** This file was generated from sample
> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,
> publish dates, and descriptions below are examples that show the shape of a migration
> report, not real publications. Only the linked official documentation URLs are real.
> Re-run the monitor with `--live` against the real feeds before treating anything here
> as an actual requirement.

# Technical Standards Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.

## Monitored Technical Standards Update Log

### 1. [CIS Benchmarks] CIS Benchmarks Center for Internet Security Configuration Rules
- **Published Date**: Wed, 10 Jun 2026 19:00:00 GMT
- **Official Resource**: [https://www.cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Center for Internet Security releases updated CIS Benchmarks and CIS Controls, mandating strict OS hardening baselines, automated configuration drift detection, secure container builds, and minimal permission profiles.

### 2. [IEC standards] IEC 62443 / IEC 62304 Cybersecurity and Software Lifecycle Standards
- **Published Date**: Sat, 06 Jun 2026 15:00:00 GMT
- **Official Resource**: [https://www.iec.ch/homepage](https://www.iec.ch/homepage)
- **Verification Status**: Priority 1 (Verified)
- **Description**: The International Electrotechnical Commission updates security and lifecycle standards for connected software systems, mandating secure boot verification, component inventory SBOMs, and safe fallback handling.

### 3. [ISO 27001] ISO/IEC 27001 Information Security Management System Controls Revision
- **Published Date**: Mon, 01 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: International Organization for Standardization updates ISO/IEC 27001 Annex A controls, requiring enhanced threat intelligence, cloud services security management, physical security monitoring, and secure coding practices.

### 4. [ISO 27001] Unverified Blog Speculation on ISO 27001 Changes
- **Published Date**: Thu, 11 Jun 2026 20:00:00 GMT
- **Official Resource**: [https://randomblogsite.com/iso-rumor](https://randomblogsite.com/iso-rumor)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: An unverified blog claims ISO 27001 is banning all cloud servers next month. This is an unverified blog post.

### 5. [ISO 27701] ISO/IEC 27701 Privacy Information Management System Requirements Update
- **Published Date**: Tue, 02 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/27701](https://www.iso.org/standard/27701)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Updates to ISO/IEC 27701 establish rigorous guidelines for PII controllers and processors, mandating explicit consent records, automated PII mapping, cross-border transfer documentation, and Privacy Impact Assessments (PIAs).

### 6. [ISO 31000] ISO 31000 Risk Management Guidelines for Technical Infrastructure
- **Published Date**: Thu, 04 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/31000](https://www.iso.org/standard/31000)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO 31000 updates enterprise risk management principles, mandating systematic risk identification, probability/impact evaluation matrices, automated mitigation workflows, and continuous risk register auditing.

### 7. [ISO 42001] ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Standard Guidance
- **Published Date**: Wed, 03 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/42001](https://www.iso.org/standard/42001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: The ISO/IEC 42001 standard specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS), including AI risk assessments and continuous impact monitoring.

### 8. [ISO 42001] Unverified Blog Speculation on ISO 27001 Changes
- **Published Date**: Thu, 11 Jun 2026 20:00:00 GMT
- **Official Resource**: [https://randomblogsite.com/iso-rumor](https://randomblogsite.com/iso-rumor)
- **Verification Status**: Priority 4 (Unverified)
- **Description**: An unverified blog claims ISO 27001 is banning all cloud servers next month. This is an unverified blog post.

### 9. [ISO 9001] ISO 9001 Quality Management System Development Controls Alignment
- **Published Date**: Fri, 05 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/9001](https://www.iso.org/standard/9001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO 9001 updates emphasize software quality control processes, rigorous release gating, traceability of requirements to code, automated continuous integration testing, and defect root-cause analysis.

### 10. [NIST AI RMF] NIST AI Risk Management Framework 1.0 Companion Guidelines
- **Published Date**: Mon, 08 Jun 2026 17:00:00 GMT
- **Official Resource**: [https://www.nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- **Verification Status**: Priority 1 (Verified)
- **Description**: NIST issues updated AI RMF guidelines across GOVERN, MAP, MEASURE, and MANAGE functions, establishing technical requirements for AI trustworthiness, bias detection, explainability, and post-deployment monitoring.

### 11. [NIST CSF] NIST Cybersecurity Framework 2.0 Implementation Core Directives
- **Published Date**: Tue, 09 Jun 2026 18:00:00 GMT
- **Official Resource**: [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework)
- **Verification Status**: Priority 1 (Verified)
- **Description**: NIST CSF 2.0 expands coverage to all organizational sectors, introducing the GOVERN function alongside Identify, Protect, Detect, Respond, and Recover, with explicit software supply chain risk management rules.

### 12. [OWASP] OWASP Top 10 and MASVS Security Controls Revision
- **Published Date**: Sun, 07 Jun 2026 16:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
- **Verification Status**: Priority 1 (Verified)
- **Description**: OWASP updates Top 10 vulnerability categories and Mobile Application Security Verification Standard (MASVS), emphasizing anti-tampering, secure data storage at rest, network transport security, and LLM prompt injection defenses.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for CIS Benchmarks
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Apply CIS Benchmarks OS and container hardening templates.
- [ ] **Task 2**: Run automated configuration drift detection tools.

### Tasks for IEC standards
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Verify IEC 62443 / IEC 62304 software lifecycle compliance.
- [ ] **Task 2**: Automate Software Bill of Materials (SBOM) generation.

### Tasks for ISO 27001
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Review Annex A information security control mappings.
- [ ] **Task 2**: Update threat intelligence and secure coding guidelines.

### Tasks for ISO 27001 (BLOCKED: Announcement source is unverified)
- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.

### Tasks for ISO 27701
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Update Privacy Information Management System (PIMS) documentation.
- [ ] **Task 2**: Verify automated PII mapping and data retention controls.

### Tasks for ISO 31000
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Refresh enterprise infrastructure risk register.
- [ ] **Task 2**: Establish automated risk score evaluation matrices.

### Tasks for ISO 42001
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Establish Artificial Intelligence Management System (AIMS) policies.
- [ ] **Task 2**: Conduct AI risk assessments and continuous impact monitoring.

### Tasks for ISO 42001 (BLOCKED: Announcement source is unverified)
- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.

### Tasks for ISO 9001
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Update software Quality Management System release gates.
- [ ] **Task 2**: Ensure requirements-to-code traceability across build pipelines.

### Tasks for NIST AI RMF
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Map AI features to NIST AI RMF GOVERN/MAP/MEASURE/MANAGE functions.
- [ ] **Task 2**: Implement model bias detection and explainability checks.

### Tasks for NIST CSF
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Align cybersecurity framework with NIST CSF 2.0 GOVERN function.
- [ ] **Task 2**: Update supply chain risk management directives.

### Tasks for OWASP
- **Standards Impact**: High priority technical governance area.
- [ ] **Task 1**: Conduct OWASP Top 10 / MASVS vulnerability audit.
- [ ] **Task 2**: Implement anti-tampering and secure storage controls.

<!-- STANDARDS_POLICY_MONITOR_END -->