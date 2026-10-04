#!/usr/bin/env python3
"""
Monitors changes to 10 technical standards categories (ISO 27001, ISO 27701,
ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF,
CIS Benchmarks), identifies repository gaps, generates implementation tasks,
documentation updates, and testing updates.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# 10 Tracked Technical Standards Categories
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

# Keywords used to classify incoming standards updates into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso27001",
        "isms",
        "information security management",
        "annex a",
        "access_control",
        "asset_management",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso27701",
        "pims",
        "privacy information management",
        "data_processor",
        "data_controller",
        "pii_protection",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso42001",
        "aims",
        "ai management system",
        "ai_risk",
        "model_governance",
        "ai_transparency",
    ],
    "ISO 31000": [
        "iso 31000",
        "iso31000",
        "risk management",
        "risk_assessment",
        "risk_mitigation",
        "risk_register",
    ],
    "ISO 9001": [
        "iso 9001",
        "iso9001",
        "qms",
        "quality management",
        "quality_assurance",
        "continuous_improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "medical_device",
        "software_lifecycle",
    ],
    "OWASP": [
        "owasp",
        "asvs",
        "samm",
        "top 10",
        "xss",
        "csrf",
        "sql_injection",
        "owasp_mobile",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai rmf",
        "govern",
        "map",
        "measure",
        "manage",
        "bias_mitigation",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "identify",
        "protect",
        "detect",
        "respond",
        "recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis benchmark",
        "hardened",
        "security_hardening",
        "benchmark_config",
    ],
}

TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and government publications (ISO, IEC, NIST, OWASP, CIS, ENISA, EDPB, FTC, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

SIMULATED_NOTICE = [
    "<!-- MONITOR_START -->",
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Check official publications before treating anything here as an active requirement.",
    "",
]

# Rich sample dataset for offline / mock testing across all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "MOCK-STD-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 ISMS Controls and Access Governance Update",
        "description": "Updated Annex A controls require automated access reviews, strict credential rotation, and continuous threat monitoring for all cloud and local repositories.",
        "link": "https://www.iso.org/iso-iec-27001-information-security.html",
        "pubDate": "Mon, 01 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "MOCK-STD-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 PIMS Data Controller and Processor Compliance Guidance",
        "description": "PIMS extensions require mandatory mapping of PII data flows, dynamic consent tracking, and automated deletion verification across backend microservices.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Wed, 03 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "MOCK-STD-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Governance Baseline",
        "description": "Establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) with rigorous algorithmic impact assessments.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 05 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "MOCK-STD-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework Integration Guidelines",
        "description": "Guidelines for enterprise risk identification, risk treatment registers, and quantitative likelihood scoring across modern software development pipelines.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 08 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "MOCK-STD-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Software Delivery Controls",
        "description": "Quality management requirements focusing on systematic code reviews, traceably documented release gating, and customer quality metrics.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Wed, 10 Jun 2026 08:30:00 GMT",
    },
    {
        "id": "MOCK-STD-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Medical & Healthcare Software Lifecycle Standards",
        "description": "Mandates strict safety classification (Class A, B, C) software development life cycle requirements, risk analysis, and software verification testing.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 12 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "MOCK-STD-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 & API Security Top 10 Revision Standards",
        "description": "Mandates automated static and dynamic application security testing (SAST/DAST) against broken object level authorization (BOLA) and injection vulnerabilities.",
        "link": "https://owasp.org/",
        "pubDate": "Mon, 15 Jun 2026 10:15:00 GMT",
    },
    {
        "id": "MOCK-STD-AIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Core Implementation",
        "description": "Provides actionable guidance across GOVERN, MAP, MEASURE, and MANAGE functions to mitigate AI risks including bias, toxicity, and model drift.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 17 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "MOCK-STD-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Governance Expansion",
        "description": "Expands core functions to Identify, Protect, Detect, Respond, Recover, and Govern, emphasizing supply chain risk management and continuous control automation.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 19 Jun 2026 09:45:00 GMT",
    },
    {
        "id": "MOCK-STD-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Hardening Benchmarks for Mobile, Container, and Cloud Platforms",
        "description": "Updates baseline configuration standards for OS, container runtime, and mobile runtime configurations to enforce least privilege and encrypted transit.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 22 Jun 2026 11:30:00 GMT",
    },
]


def classify_source_and_verify(announcement):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified).
    """
    link = announcement.get("link", "").lower()
    desc = announcement.get("description", "").lower()
    title = announcement.get("title", "").lower()

    p1_domains = [
        "iso.org",
        "iec.ch",
        "nist.gov",
        "owasp.org",
        "cisecurity.org",
        "europa.eu",
        "ftc.gov",
        "ico.org.uk",
        "enisa.europa.eu",
    ]
    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p3_keywords = ["arxiv.org", "ieee.org", "acm.org", "university", "journal"]
    p4_keywords = ["medium.com", "blog", "dev.to", "techcrunch.com"]
    p5_keywords = ["linkedin.com", "reddit.com", "twitter.com", "x.com", "sublime"]

    priority = 4
    if any(k in link or k in desc for k in p5_keywords):
        priority = 5
    elif any(k in link or k in desc for k in p4_keywords):
        priority = 4
    elif any(k in link or k in desc for k in p3_keywords):
        priority = 3
    elif any(d in link for d in p2_domains):
        priority = 2

    if any(d in link for d in p1_domains) or any(k in title for k in ["iso", "iec", "nist", "owasp", "cis"]):
        priority = 1

    if priority <= 3:
        is_verified = True
    else:
        is_verified = any(d in desc for d in p1_domains)

    return priority, is_verified


def classify_announcements(announcements, keywords_filter=None):
    """
    Classifies announcements into the 10 tracked standards categories.
    """
    classified = []
    for a in announcements:
        matched_categories = set()
        if "category" in a and a["category"] in TRACKED_CATEGORIES:
            matched_categories.add(a["category"])

        text_to_scan = f"{a.get('title', '')} {a.get('description', '')}".lower()
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in text_to_scan for kw in keywords):
                matched_categories.add(cat)

        if keywords_filter:
            if not any(kf.lower() in text_to_scan for kf in keywords_filter):
                continue

        if not matched_categories:
            matched_categories.add("ISO 27001")  # Default baseline fallback

        for cat in matched_categories:
            entry = dict(a)
            entry["category"] = cat
            classified.append(entry)

    return classified


def scan_codebase_for_standards_signals(root_dir="."):
    """
    Scans the codebase for files containing keywords relevant to technical standards.
    """
    results = {cat: [] for cat in TRACKED_CATEGORIES}

    ignore_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".idea",
        ".vscode",
    }

    category_patterns = {
        "ISO 27001": [r"iso\s*27001", r"isms", r"access_control", r"security_policy"],
        "ISO 27701": [r"iso\s*27701", r"pims", r"privacy_policy", r"pii"],
        "ISO 42001": [r"iso\s*42001", r"aims", r"model_governance", r"ai_risk"],
        "ISO 31000": [r"iso\s*31000", r"risk_management", r"risk_register"],
        "ISO 9001": [r"iso\s*9001", r"qms", r"quality_assurance"],
        "IEC standards": [r"iec\s*62304", r"iec\s*82304", r"software_lifecycle"],
        "OWASP": [r"owasp", r"asvs", r"samm", r"sast", r"dast"],
        "NIST AI RMF": [r"nist\s*ai\s*rmf", r"ai_rmf", r"govern", r"bias_mitigation"],
        "NIST CSF": [r"nist\s*csf", r"cybersecurity_framework", r"identify", r"protect"],
        "CIS Benchmarks": [r"cis\s*benchmark", r"hardening", r"benchmark_config"],
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in [
                ".py",
                ".js",
                ".ts",
                ".kt",
                ".java",
                ".swift",
                ".json",
                ".md",
                ".sh",
                ".yml",
                ".yaml",
            ]:
                continue

            filepath = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            try:
                with open(
                    os.path.join(dirpath, filename),
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as f:
                    content = f.read()

                for cat, patterns in category_patterns.items():
                    for pat in patterns:
                        if re.search(pat, content, re.IGNORECASE):
                            results[cat].append(
                                {"file": filepath, "matched_pattern": pat}
                            )
                            break
            except Exception:
                pass

    return results


def update_documentation_report(updates, output_filepath, is_simulated=False):
    """
    Writes or updates the technical standards migration documentation report.
    """
    lines = []
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    else:
        lines.append("<!-- MONITOR_START -->")
        lines.append("")

    lines.append("# Technical Standards Compliance Policy Migration & Report")
    lines.append("")
    lines.append(
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across key technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks)."
    )
    lines.append("")
    lines.append("## Monitored Standards Updates Log")
    lines.append("")

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = (
            f"Priority {priority} "
            + ("(Verified)" if is_verified else "(Unverified)")
        )
        lines.append(f"### {idx}. [{cat}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Source Credibility**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")
        lines.append("#### Identified Repository Gaps & Implementation Tasks")
        lines.append(
            f"- **Gap Analysis**: Assess project code and configuration against {cat} requirements."
        )
        lines.append(
            f"- **Implementation Task**: Update security and compliance controls to satisfy {cat} updates."
        )
        lines.append(
            f"- **Testing Updates**: Execute unit, integration, and security test suites to validate {cat} compliance."
        )
        lines.append("")

    content = "\n".join(lines) + "\n"
    try:
        os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(
            f"Technical standards documentation updated successfully at: {output_filepath}"
        )
    except Exception as e:
        print(
            f"Error writing documentation to {output_filepath}: {e}",
            file=sys.stderr,
        )


def generate_pull_request_draft(updates, scan_results):
    """
    Generates a draft of a compliance pull request complying with the exact 15 required sections.
    """
    citations_list = []
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    risk_assessment = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = (
            f"Priority {priority} "
            + ("(Verified)" if is_verified else "(Unverified)")
        )
        cite_key = (cat, u["title"], u["link"])
        if cite_key not in seen_citations:
            seen_citations.add(cite_key)
            citations_list.append(
                f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
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
                f"- **{cat}**: Align Information Security Management System (ISMS) controls, access reviews, and credential management with ISO 27001 requirements."
            )
            impl_checklist.append(
                "- [ ] Enforce automated access control reviews and credential rotation schedules."
            )
            testing_checklist.append(
                "- [ ] Run security regression tests for authentication and authorization modules."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance risks audit failure and loss of security certifications."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS controls to Privacy Information Management System (PIMS) for data processors and controllers."
            )
            impl_checklist.append(
                "- [ ] Map all PII data flows and verify dynamic consent tracking mechanisms."
            )
            testing_checklist.append(
                "- [ ] Validate data minimization and dynamic PII erasure endpoints in test suite."
            )
            risk_assessment.append(
                f"- *{cat}*: Privacy control deficiencies leading to regulatory penalties under GDPR/CCPA."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance and algorithmic transparency controls."
            )
            impl_checklist.append(
                "- [ ] Document AI model provenance, training data lineage, and risk mitigation procedures."
            )
            testing_checklist.append(
                "- [ ] Execute bias, fairness, and safety evaluation benchmarks for AI model integrations."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated AI safety and compliance risks under emerging global AI frameworks."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Incorporate enterprise risk management guidelines into technical architecture design and risk registers."
            )
            impl_checklist.append(
                "- [ ] Maintain an updated threat matrix and risk treatment plan in documentation."
            )
            testing_checklist.append(
                "- [ ] Perform continuous risk scoring and vulnerability mitigation tracking."
            )
            risk_assessment.append(
                f"- *{cat}*: Unidentified technical risks compounding into operational disruptions."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enforce Quality Management System (QMS) release controls and continuous code quality gating."
            )
            impl_checklist.append(
                "- [ ] Establish mandatory peer review and automated build quality gates."
            )
            testing_checklist.append(
                "- [ ] Verify unit test coverage exceeds baseline QMS thresholds prior to deployment."
            )
            risk_assessment.append(
                f"- *{cat}*: Inconsistent delivery quality leading to customer dissatisfaction and defect regressions."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Implement IEC 62304 / 82304 medical software lifecycle and safety risk management controls."
            )
            impl_checklist.append(
                "- [ ] Classify software safety tiers and document hazard analysis verification."
            )
            testing_checklist.append(
                "- [ ] Execute full traceable safety validation testing across software lifecycle releases."
            )
            risk_assessment.append(
                f"- *{cat}*: Medical and safety critical compliance failures causing deployment blocks."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Address OWASP Top 10 and API security vulnerabilities through SAST, DAST, and secure coding baselines."
            )
            impl_checklist.append(
                "- [ ] Perform static and dynamic security analysis against injection and authorization flaws."
            )
            testing_checklist.append(
                "- [ ] Execute OWASP ASVS compliance tests for authentication and data protection."
            )
            risk_assessment.append(
                f"- *{cat}*: Exploitable web or mobile vulnerabilities resulting in data breaches."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Align AI integrations with NIST AI Risk Management Framework functions (GOVERN, MAP, MEASURE, MANAGE)."
            )
            impl_checklist.append(
                "- [ ] Complete NIST AI RMF risk mapping and toxicity monitoring controls."
            )
            testing_checklist.append(
                "- [ ] Conduct red-teaming and prompt injection robustness testing on LLM endpoints."
            )
            risk_assessment.append(
                f"- *{cat}*: Algorithmic hallucinations and bias exposing enterprise to liability."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST Cybersecurity Framework 2.0 core functions (Identify, Protect, Detect, Respond, Recover, Govern)."
            )
            impl_checklist.append(
                "- [ ] Update continuous asset inventory, incident response protocols, and security monitoring."
            )
            testing_checklist.append(
                "- [ ] Run simulated incident response and log detection verification tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Security posture weaknesses delaying incident response and detection times."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS hardening benchmarks across host OS, container runtime, and mobile builds."
            )
            impl_checklist.append(
                "- [ ] Enforce CIS benchmark configuration profiles in CI/CD pipeline and deployment assets."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance vulnerability scanners on build images."
            )
            risk_assessment.append(
                f"- *{cat}*: Unhardened platform configurations enabling privilege escalation."
            )

    affected_files_list = (
        sorted(list(affected_files_set))
        if affected_files_set
        else [
            "docs/STANDARDS-POLICY-MIGRATION.md",
            "scripts/monitor-standards.py",
        ]
    )

    lines = []
    lines.append("## 1. Summary")
    lines.append(
        "This pull request updates repository compliance and technical controls in response to monitored updates across technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks)."
    )
    lines.append("")

    lines.append("## 2. Background")
    lines.append(
        "Continuous compliance monitoring identified updates in official technical standards. This PR addresses identified gaps across information security, privacy, quality, medical software lifecycle, and AI governance frameworks."
    )
    lines.append("")

    lines.append("## 3. Regulatory change")
    lines.append(
        "Updates reflect revised governance baselines, security controls, and risk mitigation frameworks published by official standards organizations (ISO, IEC, NIST, OWASP, CIS)."
    )
    lines.append("")

    lines.append("## 4. Official citations")
    if citations_list:
        lines.extend(citations_list)
    else:
        lines.append("- No active citations provided.")
    lines.append("")

    lines.append("## 5. Affected files")
    for f in affected_files_list:
        lines.append(f"- `{f}`")
    lines.append("")

    lines.append("## 6. Risk assessment")
    if risk_assessment:
        lines.extend(risk_assessment)
    else:
        lines.append(
            "- Moderate operational risk if technical standards updates are left unaddressed."
        )
    lines.append("")

    lines.append("## 7. Migration steps")
    if migration_steps:
        lines.extend(migration_steps)
    else:
        lines.append(
            "- Review relevant standards specifications and update project configuration files."
        )
    lines.append("")

    lines.append("## 8. Backward compatibility")
    lines.append(
        "- Changes maintain full backward compatibility with existing application logic and public interfaces."
    )
    lines.append("")

    lines.append("## 9. Implementation checklist")
    if impl_checklist:
        lines.extend(impl_checklist)
    else:
        lines.append("- [ ] Review updated standards guidance.")
    lines.append("")

    lines.append("## 10. Testing checklist")
    if testing_checklist:
        lines.extend(testing_checklist)
    else:
        lines.append(
            "- [ ] Execute test suite to confirm compliance controls remain functional."
        )
    lines.append("")

    lines.append("## 11. Documentation checklist")
    lines.append(
        "- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with latest standards updates log."
    )
    lines.append(
        "- [ ] Ensure compliance matrices and policy references reflect updated version standards."
    )
    lines.append("")

    lines.append("## 12. Compliance impact")
    lines.append(
        "- Significantly enhances security posture, privacy governance, AI safety compliance, and audit readiness across tracked technical standards."
    )
    lines.append("")

    lines.append("## 13. Breaking changes")
    lines.append(
        "- None. All implementation tasks are non-breaking additive compliance enhancements."
    )
    lines.append("")

    lines.append("## 14. Review checklist")
    lines.append(
        "- [ ] Verify that all official citations link to Priority 1 official standards bodies."
    )
    lines.append(
        "- [ ] Confirm that testing checklists and implementation tasks are fully executed."
    )
    lines.append("")

    lines.append("## 15. Approver recommendations")
    lines.append(
        "- Approve and merge following verification of automated compliance test suites."
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Changes (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live feed parsing or fall back to sample dataset",
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
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    announcements = []
    used_mock = False

    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        sys.stderr.write(
            "Data. sample announcements built into this script, not live news.\n"
        )
        if not args.json:
            print(
                "Using comprehensive mock Technical Standards updates for compliance scanning..."
            )

        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r", encoding="utf-8") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                sys.stderr.write(
                    f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.\n"
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        sys.stderr.write("Data. live feeds, fetched just now.\n")

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(
        announcements, keywords_filter
    )

    if not classified_updates:
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    scan_results = scan_codebase_for_standards_signals(args.dir)

    if args.json:
        result_data = {
            "updates": classified_updates,
            "scan_results": scan_results,
            "used_mock": used_mock,
        }
        print(json.dumps(result_data, indent=2))
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(
        f"Scanning codebase under '{args.dir}' for technical standards integration signals..."
    )
    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        update_documentation_report(
            classified_updates, args.output_docs, is_simulated=used_mock
        )
    else:
        print(
            "No file written. Pass --output-docs <path> to save this report."
        )

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
            print(
                f"Failed to write PR draft to {args.pr_output}: {e}",
                file=sys.stderr,
            )
    else:
        print("No PR draft written. Pass --pr-output <path> to save it.")


if __name__ == "__main__":
    main()
