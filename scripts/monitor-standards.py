#!/usr/bin/env python3
"""
Monitors 10 key technical standards categories (ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).
Scans codebase for repository gaps, generates implementation tasks, documentation updates,
and testing updates, and drafts a 15-section Pull Request.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

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

CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "annex a",
        "information security management",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management",
        "pii controller",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "ai management system",
        "ai risk assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management framework",
        "risk identification",
        "risk treatment",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management",
        "qms",
        "quality assurance",
        "continual improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 62443",
        "iec 82304",
        "electrotechnical",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "owasp top 10",
        "asvs",
        "samm",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai rmf",
        "nist ai 100-1",
        "trustworthy ai",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "govern identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis benchmark",
        "cis controls",
        "hardening guidelines",
    ],
}

CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"Annex A",
        r"security_policy",
        r"access_control",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"pii_processing",
        r"data_processor",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_risk",
        r"ai_governance",
        r"algorithm_audit",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_assessment",
        r"risk_register",
        r"threat_model",
        r"risk_matrix",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_policy",
        r"audit_trail",
        r"process_control",
    ],
    "IEC standards": [
        r"IEC",
        r"IEC62304",
        r"IEC62443",
        r"functional_safety",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitization",
        r"xss_prevention",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"AIRMF",
        r"ai_bias",
        r"trustworthy_ai",
        r"model_eval",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"CSF",
        r"incident_response",
        r"asset_management",
        r"zero_trust",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Controls",
        r"system_hardening",
        r"security_baseline",
    ],
}

MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 ISMS Controls Verification and Technological Safeguards",
        "description": "Updated guidelines for ISO 27001 Annex A controls mandate automated access control auditing, threat intelligence integration, and continuous monitoring of cryptographic key lifecycles.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 10 Aug 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 PIMS Privacy Controls: Mandatory Data Subject Rights Auditing",
        "description": "ISO 27701 Privacy Information Management System updates mandate explicit consent tracking, automated PII minimization checks, and data retention audit logging.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 12 Aug 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Guidance",
        "description": "The ISO 42001 standard specifies governance frameworks for AI systems, requiring algorithmic impact assessments, dataset provenance logging, and bias monitoring.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 14 Aug 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework: Dynamic Risk Assessment Standards",
        "description": "ISO 31000 guidance updates require continuous risk identification, automated risk scoring matrix validation, and periodic threat model reviews across software engineering pipelines.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 17 Aug 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System: Automated Quality Assurance & Verification",
        "description": "ISO 9001 quality management updates mandate automated continuous integration test coverage verification, release audit checklists, and formal process controls.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 19 Aug 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Functional Safety and Lifecycle Standards (IEC 62304 / IEC 62443)",
        "description": "IEC electrotechnical standards require strict software lifecycle management, system vulnerability handling, and component risk analysis in connected environments.",
        "link": "https://www.iec.ch/",
        "pubDate": "Fri, 21 Aug 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) v2.2 Update",
        "description": "OWASP MASVS guidelines mandate secure storage, hardware keystore backing, network communication pinning, and resilience against reverse engineering.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 24 Aug 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 (NIST AI 100-1) Compliance Alignment",
        "description": "NIST AI RMF guidelines require organizations to Govern, Map, Measure, and Manage AI risks with transparent model evaluations and human oversight mechanisms.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 26 Aug 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (CSF 2.0): Enforcing the Govern Function",
        "description": "NIST CSF 2.0 introduces Governance as a core pillar alongside Identify, Protect, Detect, Respond, and Recover, requiring enterprise security baseline alignment.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 28 Aug 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks & Controls: Automated System Hardening & Baseline Verification",
        "description": "CIS Benchmarks mandate defensive system hardening, secure default configurations, access restrictions, and automated security baseline scanning.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 31 Aug 2026 18:00:00 GMT",
    },
]

SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> This monitor has no live feed (technical standards bodies publish no RSS), so check the",
    "> linked official pages before treating anything here as an actual requirement.",
    "",
]


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
            if "monitor-standards" in file or "monitor-standards-test" in file:
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
    risk_assessment = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
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
                f"- **{cat}**: Audit Information Security Management System (ISMS) controls and implement access control verification."
            )
            impl_checklist.append(
                "- [ ] Review ISO 27001 Annex A controls and update access control policies."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with enterprise ISMS mandates risks security certification failure during audits."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Align Privacy Information Management System (PIMS) controls with PII processing requirements."
            )
            impl_checklist.append(
                "- [ ] Implement PII minimization checks and audit logging for PIMS compliance."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate PII management controls risk privacy regulatory penalties."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance and algorithmic transparency controls."
            )
            impl_checklist.append(
                "- [ ] Conduct AI impact assessment and dataset provenance logging for ISO 42001."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI models risk algorithmic bias and regulatory non-compliance."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Update risk management matrix and conduct continuous threat modeling."
            )
            impl_checklist.append(
                "- [ ] Update risk register and automated risk scoring criteria per ISO 31000."
            )
            risk_assessment.append(
                f"- *{cat}*: Outdated risk assessments lead to unmitigated system vulnerabilities."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Verify continuous quality assurance testing and release auditing controls."
            )
            impl_checklist.append(
                "- [ ] Configure automated test coverage gates and release verification checklists for ISO 9001."
            )
            risk_assessment.append(
                f"- *{cat}*: Process inconsistencies cause software quality regressions in production."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Ensure software lifecycle and electrotechnical functional safety controls match IEC standards."
            )
            impl_checklist.append(
                "- [ ] Audit software lifecycle process control logs against IEC requirements."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to meet functional safety standards in connected software environments."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Verify OWASP MASVS/ASVS controls for secure storage, network transport, and input sanitization."
            )
            impl_checklist.append(
                "- [ ] Run static analysis security testing (SAST) for OWASP Top 10 vulnerabilities."
            )
            risk_assessment.append(
                f"- *{cat}*: Application vulnerabilities expose sensitive user session tokens and credentials."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Align AI implementations with NIST AI RMF core functions (Govern, Map, Measure, Manage)."
            )
            impl_checklist.append(
                "- [ ] Document model evaluation benchmarks and human oversight protocols for NIST AI RMF."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of NIST AI RMF alignment leads to trustworthy AI compliance failures."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Update enterprise cybersecurity controls to align with NIST CSF 2.0 Governance functions."
            )
            impl_checklist.append(
                "- [ ] Map security controls against NIST CSF 2.0 subcategories."
            )
            risk_assessment.append(
                f"- *{cat}*: Gaps in cybersecurity framework coverage increase enterprise incident exposure."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce system hardening rules and secure default configurations."
            )
            impl_checklist.append(
                "- [ ] Run CIS Benchmark compliance audit scripts against repository build settings."
            )
            risk_assessment.append(
                f"- *{cat}*: Unhardened system configurations leave default attack surfaces open."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into alignment with monitored technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards evolve to address emerging cybersecurity threats, privacy expectations, quality assurance, and AI governance requirements. Maintaining continuous compliance ensures technical excellence and mitigates organizational risk.

## 3. Regulatory change
- **Technical & Security Standards**: Formal alignment with ISO/IEC standards, OWASP MASVS, NIST frameworks, and CIS Benchmarks.
- **AI Governance & Quality**: Integration of ISO 42001 and NIST AI RMF risk management protocols into the repository lifecycle.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance gaps and security vulnerabilities if standards updates are not systematically integrated.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards updates are fully backward-compatible. System configuration adjustments and governance documentation updates do not break existing public API contracts.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the automated compliance guard checks locally.

## 10. Testing checklist
- [ ] Execute continuous integration test suites to verify system quality controls.
- [ ] Verify static security analysis scans produce zero high-severity findings.
- [ ] Confirm AI governance logging and audit trails function as expected.
- [ ] Validate CIS Benchmark system hardening parameters.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed checklists.
- [ ] Cross-reference technical standards rules with internal compliance playbooks.

## 12. Compliance impact
- **Standards Aligned**: Ensures the repository satisfies ISO, OWASP, NIST, and CIS benchmark criteria.
- **Enterprise Readiness**: Satisfies vendor risk assessment and third-party security audit requirements.
- **System Integrity**: Reduces software vulnerability surface area and ensures operational reliability.

## 13. Breaking changes
- No functional breaking changes. Configuration defaults are hardened in accordance with CIS and OWASP recommendations.

## 14. Review checklist
- [ ] Code is 100% free of emojis or graphical symbols in comments and files.
- [ ] Standards citations are verified against Priority 1 official sources.
- [ ] Security and governance controls are fully documented.

## 15. Approver recommendations
Verify that all technical control updates have been reviewed by Information Security and Quality Engineering leads. Confirm that automated verification tests pass before merging.
"""
    return pr_template


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
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
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
                "- [ ] **Task 1**: Update ISMS access control policies and audit trails."
            )
            lines.append(
                "- [ ] **Task 2**: Verify cryptographic key management controls."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Review PIMS PII minimization and consent mechanisms."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Implement AIMS AI risk assessment and dataset provenance logging."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Update risk register and continuous threat evaluation matrix."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Verify quality assurance process controls and automated CI gates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Audit software lifecycle safety controls against IEC standards."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Run OWASP MASVS static security analysis and remediate vulnerabilities."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Document NIST AI RMF Govern, Map, Measure, Manage controls."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align enterprise security baseline with NIST CSF 2.0 Governance pillars."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Execute CIS system hardening baseline verification."
            )
        lines.append("")

    lines.append("## Testing & Verification Updates")
    lines.append("")
    for cat in processed_doc_cats:
        lines.append(f"### Testing Updates for {cat}")
        lines.append(f"- [ ] **Test 1**: Verify automated test suite coverage for {cat} controls.")
        lines.append(f"- [ ] **Test 2**: Run compliance static analysis checks for {cat} signals.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="No live standards feed exists (standards bodies publish no RSS), so this uses sample announcements and labels the report as simulated",
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
        default=None,
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default=None,
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("No live standards feed exists (standards bodies publish no RSS); using sample announcements.")

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print("Data. sample announcements built into this script, not live news.")
        print(
            "Using comprehensive mock Technical Standards updates for compliance scanning..."
        )
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
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
        print("Data. live feeds, fetched just now.")

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates:"
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
    else:
        print("No file written. Pass --output-docs <path> to save this report.")

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
    else:
        print("No PR draft written. Pass --pr-output <path> to save it.")


if __name__ == "__main__":
    main()
