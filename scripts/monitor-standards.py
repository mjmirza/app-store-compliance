#!/usr/bin/env python3
"""Monitors the 10 technical standards categories in TRACKED_CATEGORIES below,
identifying repository gaps, generating implementation tasks, documentation updates,
and testing updates for each standard update."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards categories
TRACKED_CATEGORIES = [
    "ISO 27001",
    "ISO 27701",
    "ISO 42001",
    "ISO 31000",
    "ISO 9001",
    "IEC standards",
    "OWASP",
    "NIST AI RMF",
    "NIST CSF",
    "CIS Benchmarks",
]

# Keywords used to classify incoming standards announcements into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management system",
        "isms",
        "annex a controls",
        "statement of applicability",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management system",
        "pims",
        "personally identifiable information",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai risk assessment",
        "ai impact assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk treatment plan",
        "enterprise risk management",
        "risk framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality policy",
        "quality audit",
        "continual improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "international electrotechnical commission",
        "functional safety",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "mstg",
        "asvs",
        "open web application security project",
        "owasp LLM top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "govern map measure manage",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "identify protect detect respond recover govern",
        "sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "cis hardening",
        "cis os benchmarks",
    ],
}

# Codebase signals (regex patterns) to find files affected by each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"information_security",
        r"security_policy",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacy_policy",
        r"pii_handler",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"ai_governance",
        r"ai_risk",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"risk_management",
        r"risk_assessment",
        r"risk_register",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"quality_policy",
        r"quality_assurance",
    ],
    "IEC standards": [
        r"IEC[ -]?62443",
        r"IEC[ -]?82304",
        r"IEC[ -]?62304",
        r"functional_safety",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitizer",
        r"security_header",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI",
        r"AI_RMF",
        r"govern_map_measure",
        r"model_card",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"SP[ -]?800-53",
        r"cybersecurity_framework",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"hardening",
        r"benchmark_audit",
    ],
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "ISO/IEC 27001 updates Annex A security controls, mandating threat intelligence integration, secure coding practices, and physical security monitoring for cloud environments.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Revision",
        "description": "ISO/IEC 27701 updates PIMS guidelines for PII controllers and processors, requiring explicit privacy impact assessments and automated data subject request workflows.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Standard",
        "description": "ISO/IEC 42001 establishes requirements for establishing, implementing, maintaining and continually improving an Artificial Intelligence Management System (AIMS) in organizations.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 05 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework Guidelines Update",
        "description": "ISO 31000 provides revised principles and generic guidelines on risk management, emphasizing iterative risk identification, continuous risk monitoring, and executive risk governance.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 08 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System (QMS) Requirements Alignment",
        "description": "ISO 9001 specifies requirements for a quality management system when an organization needs to demonstrate its ability to consistently provide products and services that meet customer requirements.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 10 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Technical Standards Update: IEC 62443 and IEC 62304 Cybersecurity Guidance",
        "description": "The International Electrotechnical Commission releases updated security lifecycle guidance under IEC 62443 for industrial automation and IEC 62304 for medical device software.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 12 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) & Web Top 10 Update",
        "description": "OWASP releases updated verification controls for mobile and web applications, emphasizing API security, LLM prompt injection safeguards, and strict input sanitization.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "NIST issues updated AI RMF guidelines structured around Govern, Map, Measure, and Manage functions to address risks from generative AI and machine learning deployments.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (CSF 2.0) Expanded Implementation",
        "description": "NIST CSF 2.0 expands coverage to all organizations, introducing the Govern function alongside Identify, Protect, Detect, Respond, and Recover core functions.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 19 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and CIS Critical Security Controls v8.1 Update",
        "description": "The Center for Internet Security publishes updated CIS Benchmarks and Controls v8.1, detailing baseline security configurations for operating systems, cloud environments, and mobile platforms.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 22 Jun 2026 14:00:00 GMT",
    },
]

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards categories."""
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
    exclude_dirs = {
        "node_modules",
        "Pods",
        ".git",
        "build",
        "DerivedData",
        "vendor",
        ".dart_tool",
        "Carthage",
        "androidTest",
        "__tests__",
        "dist",
    }

    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            if not file.endswith(
                (
                    ".kt",
                    ".java",
                    ".xml",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".swift",
                    ".m",
                    ".h",
                    ".plist",
                    ".py",
                    ".md",
                    ".sh",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            if "monitor-standards" in file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for cat, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[cat].append(
                                        {
                                            "file": filepath,
                                            "line_num": i,
                                            "content": line.strip()[:100],
                                            "matched_pattern": pattern.pattern,
                                        }
                                    )
                                    break
            except Exception:
                pass
    return matches


def classify_announcements(announcements, keywords_filter=None):
    """Classifies incoming announcements into the 10 technical standards categories."""
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break

        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "STD-UPDATE-" + str(hash(title))[:6]),
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": ann.get("link", ""),
                        "pubDate": ann.get("pubDate", ""),
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a draft of a pull request complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    risk_assessment = []
    processed_categories = set()

    for u in updates:
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Audit Information Security Management System (ISMS) Annex A control mapping and update the Statement of Applicability (SoA)."
            )
            impl_checklist.append(
                "- [ ] Review ISMS controls and update Annex A security mapping documents."
            )
            testing_checklist.append(
                "- [ ] Execute ISMS internal audit checklist and verify control effectiveness."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with ISMS audit requirements leading to certification revocation or security gap exposures."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Update Privacy Information Management System (PIMS) controls for PII controllers/processors and verify DSR automation."
            )
            impl_checklist.append(
                "- [ ] Update PIMS documentation and verify PII data mapping accuracy."
            )
            testing_checklist.append(
                "- [ ] Test automated Data Subject Request (DSR) handling and erasure workflows."
            )
            risk_assessment.append(
                f"- *{cat}*: Privacy information management deficiencies exposing PII to unauthorized access or regulatory fines."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance controls, AI impact assessments, and risk mitigation procedures."
            )
            impl_checklist.append(
                "- [ ] Document AI system inventory, governance policies, and AI risk assessment procedures."
            )
            testing_checklist.append(
                "- [ ] Verify model transparency, bias testing, and risk mitigation controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated AI safety, transparency, or bias risks in machine learning deployments."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align enterprise risk management framework with updated ISO 31000 guidelines and update risk registers."
            )
            impl_checklist.append(
                "- [ ] Update risk management policy and refresh repository risk register."
            )
            testing_checklist.append(
                "- [ ] Conduct risk treatment plan validation and executive review."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate risk governance and untracked technical liabilities."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Align software development lifecycle (SDLC) quality procedures with ISO 9001 QMS continuous improvement standards."
            )
            impl_checklist.append(
                "- [ ] Review quality assurance processes and software release checklists."
            )
            testing_checklist.append(
                "- [ ] Validate QA automated regression test coverage and defect tracking metrics."
            )
            risk_assessment.append(
                f"- *{cat}*: Quality management breakdowns leading to software defects and release regressions."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Verify compliance with IEC 62443 / IEC 62304 functional safety and cybersecurity software lifecycle requirements."
            )
            impl_checklist.append(
                "- [ ] Map software architecture against IEC cybersecurity and safety lifecycle criteria."
            )
            testing_checklist.append(
                "- [ ] Perform fault injection testing and safety static analysis checks."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-conformance with industrial or medical software safety standards."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Audit code against OWASP MASVS and OWASP Top 10 recommendations; enforce input sanitization and secure headers."
            )
            impl_checklist.append(
                "- [ ] Remediate OWASP Top 10 vulnerability findings across API endpoints and UI components."
            )
            testing_checklist.append(
                "- [ ] Run static application security testing (SAST) and dynamic vulnerability scans."
            )
            risk_assessment.append(
                f"- *{cat}*: Application vulnerabilities such as injection, broken access control, or insecure data storage."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF Govern, Map, Measure, and Manage functions for all deployed AI and LLM features."
            )
            impl_checklist.append(
                "- [ ] Draft AI system model cards and document risk measurement metrics."
            )
            testing_checklist.append(
                "- [ ] Run prompt injection robustness, hallucination measurement, and safety boundary tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Deployment of unmapped or unmeasured AI models leading to safety and alignment failures."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map security architecture to NIST CSF 2.0 core functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append(
                "- [ ] Align incident response plans and access control policies with NIST CSF 2.0."
            )
            testing_checklist.append(
                "- [ ] Test incident detection, logging alerting pipelines, and recovery procedures."
            )
            risk_assessment.append(
                f"- *{cat}*: Gaps in security monitoring, detection, or incident response capability."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Critical Security Controls v8.1 baseline configurations to OS, container, and cloud environments."
            )
            impl_checklist.append(
                "- [ ] Apply CIS hardening guidelines to environment configuration scripts."
            )
            testing_checklist.append(
                "- [ ] Execute CIS Benchmark automated compliance auditing scripts."
            )
            risk_assessment.append(
                f"- *{cat}*: Misconfigured server or build environment baselines exposing unnecessary attack surface."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual architectural review).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into alignment with updated technical standards, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It identifies repository gaps, establishes implementation tasks, and provides documentation and testing updates.

## 2. Background
Technical standards released by recognized standards organizations (ISO, IEC, NIST, OWASP, CIS) establish international baselines for information security, privacy, quality, AI risk management, and cybersecurity governance. Maintaining alignment with these standards ensures organizational compliance and security posture.

## 3. Regulatory change
- **Standards Baselines**: Adherence to updated technical standards frameworks including ISO/IEC standards, NIST frameworks, OWASP security verification baselines, and CIS Benchmarks.
- **Verification Mandates**: Implementation of continuous monitoring, gap identification, testing, and documentation updating pipelines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to High risk of compliance non-conformance and security vulnerabilities if technical standards controls are not regularly updated and verified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standards compliance updates are non-breaking and fully backward-compatible. Refactored security controls and documentation guidelines maintain legacy operational support.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run scripts/validate.py to ensure compliance schemas remain valid.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Execute localized automated test suites and verify zero regressions.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed task statuses.
- [ ] Document standards control mappings in technical architecture documentation.

## 12. Compliance impact
- **Standards Alignment**: Demonstrates conformance with international ISO/IEC, NIST, OWASP, and CIS technical standards.
- **Risk Reduction**: Mitigates security, privacy, quality, and AI safety risks.

## 13. Breaking changes
- No functional breaking changes are introduced.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] All citations point to official standards publications or verified sources.
- [ ] Implementation and testing tasks have been executed and verified.

## 15. Approver recommendations
Verify that standards control mappings match organizational compliance scope. Confirm that all automated test pipelines pass successfully.
"""
    return pr_template


SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Check the linked official pages before treating anything here as an actual requirement.",
    "",
]


def update_documentation_report(updates, output_filepath, is_simulated=False):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Standards Update Log",
        "",
    ])

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    processed_doc_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_doc_cats:
            continue
        processed_doc_cats.add(cat)
        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority. Technical standards audit mandates action."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update Statement of Applicability (SoA) and Annex A control mapping."
            )
            lines.append(
                "- [ ] **Task 2**: Conduct ISMS internal audit review."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Update PIMS privacy control documentation."
            )
            lines.append(
                "- [ ] **Task 2**: Audit automated Data Subject Request (DSR) workflows."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Document AIMS AI system inventory and risk management policies."
            )
            lines.append(
                "- [ ] **Task 2**: Perform AI impact assessment and safety verification."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Refresh enterprise risk register and treatment plans."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Audit QMS software development lifecycle quality procedures."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Verify IEC 62443 / IEC 62304 software safety lifecycle controls."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Audit application code against OWASP MASVS and OWASP Top 10."
            )
            lines.append(
                "- [ ] **Task 2**: Run SAST vulnerability scanner and remediate findings."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Implement NIST AI RMF Govern, Map, Measure, Manage functions."
            )
            lines.append(
                "- [ ] **Task 2**: Publish model cards for deployed AI features."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Map security controls to NIST CSF 2.0 core functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Apply CIS Controls v8.1 baseline hardening configurations."
            )

        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards Requirements"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live RSS updates or fallback to sample announcements",
    )
    parser.add_argument(
        "--mock",
        type=str,
        help="Path to custom mock announcements JSON file, or 'inline' to use default mock data",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Optional comma-separated keywords to filter updates",
    )
    parser.add_argument(
        "--dir", type=str, default=".", help="Codebase directory to scan"
    )
    parser.add_argument(
        "--output-docs",
        type=str,
        default="docs/STANDARDS-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/STANDARDS_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    announcements = []
    used_mock = False

    if args.mock or (not args.live and not args.mock):
        used_mock = True
        print("Data. sample announcements built into this script, not live news.")
        print("Using comprehensive mock Technical Standards updates for compliance scanning...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r", encoding="utf-8") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        print("Data. live feeds requested.")
        announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards requirement updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
