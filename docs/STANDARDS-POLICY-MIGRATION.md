<!-- STANDARDS_POLICY_MONITOR_START -->
# Technical Standards Policy Migration & Requirements Report

This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across ISO, IEC, OWASP, NIST, and CIS standards.

## Monitored Technical Standards Update Log

### 1. [CIS Benchmarks] CIS Security Benchmarks and Configuration Baseline Update
- **Published Date**: Wed, 24 Jun 2026 19:00:00 GMT
- **Official Resource**: [https://www.cisecurity.org/cis-benchmarks/](https://www.cisecurity.org/cis-benchmarks/)
- **Verification Status**: Priority 1 (Verified)
- **Description**: Center for Internet Security issues updated hardening benchmarks for mobile operating systems, cloud containers, and web servers, mandating automated baseline compliance checks in CI/CD pipelines.

### 2. [IEC standards] IEC 62304 and IEC 82304 Software Lifecycle Process Requirements
- **Published Date**: Sat, 20 Jun 2026 15:00:00 GMT
- **Official Resource**: [https://www.iec.ch/standards](https://www.iec.ch/standards)
- **Verification Status**: Priority 1 (Verified)
- **Description**: The International Electrotechnical Commission updates health and safety software lifecycle standards (IEC 62304 / IEC 82304), mandating formal software safety classification and risk management file verification.

### 3. [ISO 27001] ISO/IEC 27001 Information Security Management System Controls Update
- **Published Date**: Mon, 15 Jun 2026 10:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO releases updated Annex A control guidance enforcing threat intelligence integration, secure coding practices, and continuous monitoring for cloud and mobile software architectures.

### 4. [ISO 27701] ISO/IEC 27701 Privacy Information Management System Extension Requirements
- **Published Date**: Tue, 16 Jun 2026 11:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/27701](https://www.iso.org/standard/27701)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO/IEC 27701 specifies updated requirements for PII controllers and processors, mandating automated consent recording, privacy impact assessments, and PII data lifecycle logs.

### 5. [ISO 31000] ISO 31000 Enterprise Risk Management Assessment and Treatment Guidelines
- **Published Date**: Thu, 18 Jun 2026 13:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/31000](https://www.iso.org/standard/31000)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO 31000 updates risk treatment framework guidelines, requiring structured risk identification, impact quantification, and documented mitigation strategies across product engineering teams.

### 6. [ISO 42001] ISO/IEC 42001 Artificial Intelligence Management System Certification Standard
- **Published Date**: Wed, 17 Jun 2026 12:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/42001](https://www.iso.org/standard/42001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: The ISO/IEC 42001 standard requires organizations deploying AI systems to document AI risk assessments, establish algorithmic transparency, and implement continuous AI model monitoring.

### 7. [ISO 9001] ISO 9001 Quality Management System Process Verification Guidelines
- **Published Date**: Fri, 19 Jun 2026 14:00:00 GMT
- **Official Resource**: [https://www.iso.org/standard/9001](https://www.iso.org/standard/9001)
- **Verification Status**: Priority 1 (Verified)
- **Description**: ISO 9001 QMS guidance mandates traceably documented software development processes, release verification workflows, and formal customer feedback remediation tracking.

### 8. [NIST AI RMF] NIST AI Risk Management Framework 1.0 Companion Guidelines
- **Published Date**: Mon, 22 Jun 2026 17:00:00 GMT
- **Official Resource**: [https://www.nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- **Verification Status**: Priority 1 (Verified)
- **Description**: NIST releases operational guidance for AI RMF core functions (Govern, Map, Measure, Manage), requiring explicit documentation of training data provenance, bias evaluations, and AI safety testing.

### 9. [NIST CSF] NIST Cybersecurity Framework CSF 2.0 Implementation Guide
- **Published Date**: Tue, 23 Jun 2026 18:00:00 GMT
- **Official Resource**: [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework)
- **Verification Status**: Priority 1 (Verified)
- **Description**: NIST CSF 2.0 introduces Governance as a central pillar alongside Identify, Protect, Detect, Respond, and Recover, mandating organizational supply chain risk management and continuous vulnerability remediation.

### 10. [OWASP] OWASP MASVS and Top 10 Security Verification Framework Release
- **Published Date**: Sun, 21 Jun 2026 16:00:00 GMT
- **Official Resource**: [https://owasp.org/www-project-mobile-app-security/](https://owasp.org/www-project-mobile-app-security/)
- **Verification Status**: Priority 1 (Verified)
- **Description**: OWASP publishes updated Mobile Application Security Verification Standard (MASVS) and ASVS requirements, introducing strict controls for storage encryption, API authentication, and LLM prompt security.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for CIS Benchmarks
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Apply CIS hardening configurations to environment assets.
- [ ] **Documentation Task**: Document CIS benchmark exceptions and hardening baselines.
- [ ] **Testing Task**: Run automated CIS baseline compliance scanners.

### Tasks for IEC standards
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Maintain IEC 62304 / IEC 82304 software safety classifications.
- [ ] **Documentation Task**: Maintain hazard analysis files and software traceability matrices.
- [ ] **Testing Task**: Run unit and integration verification against safety class requirements.

### Tasks for ISO 27001
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Align access management and cryptographic storage with Annex A controls.
- [ ] **Documentation Task**: Update ISMS policy documentation in `docs/`.
- [ ] **Testing Task**: Execute automated vulnerability scans and access control checks.

### Tasks for ISO 27701
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Implement PII processing controls and consent logging.
- [ ] **Documentation Task**: Document PIMS PII controller and processor roles.
- [ ] **Testing Task**: Validate automated PII deletion and data export requests.

### Tasks for ISO 31000
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Update repository risk registers and treatment milestones.
- [ ] **Documentation Task**: Publish revised risk evaluation criteria and mitigation plans.
- [ ] **Testing Task**: Simulate disaster recovery and risk mitigation procedures.

### Tasks for ISO 42001
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Deploy AI Risk Management System (AIMS) controls and model cards.
- [ ] **Documentation Task**: Document AI system lineage, training inputs, and safety boundaries.
- [ ] **Testing Task**: Run AI input sanitization and hallucination guardrail test suites.

### Tasks for ISO 9001
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Enforce QMS build verification gates in release workflows.
- [ ] **Documentation Task**: Document quality assurance standards and audit records.
- [ ] **Testing Task**: Execute complete regression suite before tagging release candidates.

### Tasks for NIST AI RMF
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Operationalize NIST AI RMF core functions across AI components.
- [ ] **Documentation Task**: Document AI risk profile and dataset provenance.
- [ ] **Testing Task**: Run adversarial prompt testing and bias evaluation suites.

### Tasks for NIST CSF
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Apply NIST CSF 2.0 Governance and Protect controls.
- [ ] **Documentation Task**: Update cybersecurity target profiles and incident response plans.
- [ ] **Testing Task**: Perform threat detection and incident response drills.

### Tasks for OWASP
- **Regulatory Impact**: High priority technical standard requirement.
- [ ] **Implementation Task**: Implement OWASP MASVS/ASVS controls for input and storage security.
- [ ] **Documentation Task**: Document security verification mappings against OWASP checklists.
- [ ] **Testing Task**: Execute SAST and dynamic security test suites.

<!-- STANDARDS_POLICY_MONITOR_END -->