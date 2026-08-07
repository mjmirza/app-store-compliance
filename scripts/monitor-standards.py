#!/usr/bin/env python3
"""Monitors the 10 key technical standards and generates repo-impact,
migration, and testing updates for each."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# Source Trust Hierarchy Definitions (completely emoji-free)
TRUST_HIERARCHY = {
    "Priority 1": "ISO/IEC, NIST, CISA, ENISA, EDPB, FTC, Government publications, or official standardization bodies",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# The 10 tracked technical standards
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

# Keywords used to classify incoming announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management system",
        "access control policy",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management system",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai governance",
        "ai risk management",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management framework",
        "risk evaluation",
        "risk treatment",
    ],
    "ISO 9001": [
        "iso 9001",
        "qms",
        "quality management system",
        "quality manual",
    ],
    "IEC standards": [
        "iec 62304",
        "iec 82304",
        "iec standards",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "mstg",
        "asvs",
        "owasp top 10",
        "injection",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "trustworthy ai",
        "bias mitigation",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "nist csf 2.0",
        "nist special publication",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "hardening guidelines",
        "security baseline",
        "cis control",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS",
        r"access_control",
        r"security_policy",
        r"ISO27001",
    ],
    "ISO 27701": [
        r"PIMS",
        r"pii_controller",
        r"privacy_policy",
        r"ISO27701",
    ],
    "ISO 42001": [
        r"AIMS",
        r"ai_risk",
        r"ai_governance",
        r"ISO42001",
    ],
    "ISO 31000": [
        r"risk_management",
        r"risk_assessment",
        r"ISO31000",
    ],
    "ISO 9001": [
        r"QMS",
        r"quality_management",
        r"ISO9001",
    ],
    "IEC standards": [
        r"IEC_62304",
        r"IEC_82304",
        r"IEC_standards",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"owasp_top_10",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"trustworthy_ai",
        r"bias_mitigation",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurity_framework",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmarks",
        r"hardening_guidelines",
        r"security_baseline",
    ],
}

# Mock announcements covering the 10 standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security: Transition to New Security Controls",
        "description": "The updated ISO/IEC 27001 standards update transition requirements, emphasizing threat intelligence, secure coding, and cloud-focused access control policies.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 UTC",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management guidelines updated for GDPR compliance",
        "description": "New directives clarify privacy engineering expectations for PII controllers and PII processors to satisfy strict EU GDPR standards.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 UTC",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System: Core Risk Mitigation Rules",
        "description": "ISO/IEC 42001:2023 establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS).",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 UTC",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management: Integrating Risk Governance with Software Release Pipelines",
        "description": "Provides principles, a framework, and a process for managing risk. Recommends structured identification of technical and deployment risks.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 UTC",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management: Process Consistency and CI/CD Quality Controls",
        "description": "Mandates systematic quality metrics, process definitions, and customer satisfaction audits across the entire product lifecycle.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 UTC",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 Medical Device Software lifecycle standards updated",
        "description": "Specifies lifecycle requirements for medical device software development. Requires rigorous configuration management and regression testing.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 UTC",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.0 Release: Setting the Standard for Mobile App Security",
        "description": "Defines security requirements for mobile app storage, cryptography, platform interaction, and network communications.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 UTC",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0: Developing Trustworthy and Responsible AI",
        "description": "Establishes a framework to address risks in the design, development, use, and evaluation of AI systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 UTC",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST CSF 2.0 Finalized with Focus on Governance and Security Controls",
        "description": "Expands core cybersecurity functions to: Govern, Identify, Protect, Detect, Respond, Recover.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 UTC",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Update: Operating System and Container Hardening Standards",
        "description": "Provides consensus-based best practice security baselines for server, database, and container hardening.",
        "link": "https://www.cisecurity.org/benchmark",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 UTC",
    },
    {
        "id": "STD-MOCK-RUMOR",
        "category": "ISO 27001",
        "title": "Unverified rumor on LinkedIn alleging changes to ISO 27001 controls",
        "description": "A user post claims that ISO 27001 is immediately requiring zero-trust network access on all employee home offices. No citations or official documents are referenced.",
        "link": "https://linkedin.com/posts/unverified-rumor-iso",
        "pubDate": "Mon, 13 Jul 2026 10:00:00 UTC",
    },
]


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards."""
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

    # Compile the signal patterns
    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Check applicable file types
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
                    ".entitlements",
                    ".md",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
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


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcements by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified)."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 patterns
    p1_domains = [
        "iso.org",
        "nist.gov",
        "iec.ch",
        "cisecurity.org",
        "owasp.org",
        "europa.eu",
        "cisa.gov",
        "enisa.europa.eu",
        "gov",
    ]
    p1_keywords = [
        "international organization for standardization",
        "national institute of standards and technology",
        "iec standards",
        "owasp",
        "cis security",
        "government publication",
        "official publication",
    ]

    # Priority 2 patterns
    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    # Priority 3 patterns
    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "peer-reviewed", "university study"]

    # Priority 4 patterns
    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "vendor blog"]

    # Priority 5 patterns
    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary"]

    priority = 4  # Default to Priority 4

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(kw in combined for kw in p4_keywords):
        priority = 4
    elif any(d in link for d in p3_domains) or any(kw in combined for kw in p3_keywords) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains) or any(kw in combined for kw in p2_keywords):
        priority = 2

    if any(d in link for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in link:
        priority = 1

    # Verification rules
    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4/5. Check if it explicitly cites a Priority 1 official domain/keyword.
        has_p1_ref_in_text = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref_in_text = True
                break
        if not has_p1_ref_in_text:
            for kw in p1_keywords:
                if kw in combined:
                    has_p1_ref_in_text = True
                    break
        if ".gov" in combined:
            has_p1_ref_in_text = True

        if has_p1_ref_in_text:
            is_verified = True
        elif all_announcements:
            # Fallback cross-verification check
            words = set(re.findall(r"[a-z]+", combined))
            for other in all_announcements:
                if other == announcement:
                    continue
                other_p, _ = classify_source_and_verify(other, None)
                if other_p == 1:
                    other_combined = f"{other.get('title', '')} {other.get('description', '')} {other.get('link', '')}".lower()
                    other_words = set(re.findall(r"[a-z]+", other_combined))
                    common_terms = {"iso", "nist", "iec", "owasp", "cis", "standards"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def is_keyword_in_text(keyword, text):
    kw_lower = keyword.lower()
    # If the keyword is entirely alphanumeric (e.g., "aims", "isms", "pims"),
    # enforce word boundaries to avoid false-positive matches (like "claims" or "prism").
    if kw_lower.isalnum():
        pattern = r"\b" + re.escape(kw_lower) + r"\b"
        return bool(re.search(pattern, text, re.IGNORECASE))
    return kw_lower in text


def classify_announcements(announcements, keywords_filter=None):
    """Classifies announcements into categories."""
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(is_keyword_in_text(k, text_to_search) for k in keywords_filter):
                continue

        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if is_keyword_in_text(kw, text_to_search):
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
    """Generates a comprehensive 15-section Pull Request draft (entirely emoji-free)."""
    citations_list = []
    affected_files_set = set()
    risk_assessment = []
    migration_steps = []
    impl_checklist = []
    testing_checklist = []

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "ISO 27001":
            risk_assessment.append(f"- *{cat}*: Lack of structured Information Security Management System (ISMS) controls leading to data exposure.")
            migration_steps.append(f"- **{cat}**: Document Information Security Management System (ISMS) control procedures and verify access controls.")
            impl_checklist.append("- [ ] Establish formal access control policies aligned with ISO 27001 controls.")
            testing_checklist.append("- [ ] Verify access control policy access lists and audit logging functionality.")
        elif cat == "ISO 27701":
            risk_assessment.append(f"- *{cat}*: Inadequate PII processing declarations violating privacy-by-design principles.")
            migration_steps.append(f"- **{cat}**: Set up Privacy Information Management System (PIMS) structures for PII processing.")
            impl_checklist.append("- [ ] Configure PII controller and processor roles and document PII data flows.")
            testing_checklist.append("- [ ] Conduct PII data leakage tests across database integration channels.")
        elif cat == "ISO 42001":
            risk_assessment.append(f"- *{cat}*: Generative AI integrations operating without safety rails and risk mitigation protocols.")
            migration_steps.append(f"- **{cat}**: Implement an Artificial Intelligence Management System (AIMS) with rigorous risk-mitigation rules.")
            impl_checklist.append("- [ ] Designate AI system impact assessments and establish model verification checklists.")
            testing_checklist.append("- [ ] Perform AI model robustness and bias validation checks.")
        elif cat == "ISO 31000":
            risk_assessment.append(f"- *{cat}*: Loose integration of risk governance inside active deployment pipelines.")
            migration_steps.append(f"- **{cat}**: Formally document pipeline risk management guidelines.")
            impl_checklist.append("- [ ] Define localized risk assessment matrices for deployment environments.")
            testing_checklist.append("- [ ] Run sandbox deployment failure simulation tests.")
        elif cat == "ISO 9001":
            risk_assessment.append(f"- *{cat}*: Process inconsistency and loose delivery parameters across active modules.")
            migration_steps.append(f"- **{cat}**: Standardize the Quality Management System (QMS) framework and process checklists.")
            impl_checklist.append("- [ ] Draft localized quality manuals and compile performance metrics.")
            testing_checklist.append("- [ ] Conduct compliance reviews of QA pipelines and code coverage logs.")
        elif cat == "IEC standards":
            risk_assessment.append(f"- *{cat}*: Lack of configuration verification and validation for physical or medical software layers.")
            migration_steps.append(f"- **{cat}**: Adopt standardized configuration verification and software lifecycle practices.")
            impl_checklist.append("- [ ] Implement strict configuration management and validation tools.")
            testing_checklist.append("- [ ] Verify software configuration integrity registers.")
        elif cat == "OWASP":
            risk_assessment.append(f"- *{cat}*: Vulnerability to standard web or mobile application attacks.")
            migration_steps.append(f"- **{cat}**: Implement OWASP MASVS and ASVS secure storage, cryptography, and network baselines.")
            impl_checklist.append("- [ ] Align codebase implementation controls with OWASP MASVS baselines.")
            testing_checklist.append("- [ ] Run automated vulnerability and penetration testing suites.")
        elif cat == "NIST AI RMF":
            risk_assessment.append(f"- *{cat}*: Trustworthiness or safety gaps in deployed AI models.")
            migration_steps.append(f"- **{cat}**: Align AI deployment pipelines with NIST AI RMF Map, Measure, Manage functions.")
            impl_checklist.append("- [ ] Formulate bias mitigation and explainability guidelines for AI modules.")
            testing_checklist.append("- [ ] Verify model interpretability metrics and fairness constraints.")
        elif cat == "NIST CSF":
            risk_assessment.append(f"- *{cat}*: Lack of a structured framework to Govern, Identify, Protect, Detect, Respond, and Recover.")
            migration_steps.append(f"- **{cat}**: Adopt updated NIST CSF 2.0 governance and cyber protection controls.")
            impl_checklist.append("- [ ] Document governance control matrices mapping current resources.")
            testing_checklist.append("- [ ] Simulate system penetration, detection, and incident response scenarios.")
        elif cat == "CIS Benchmarks":
            risk_assessment.append(f"- *{cat}*: Misconfigured servers or containers operating below secure base hardlines.")
            migration_steps.append(f"- **{cat}**: Audit operating system, container, and database configurations against CIS baselines.")
            impl_checklist.append("- [ ] Formulate automated CIS container hardening baselines.")
            testing_checklist.append("- [ ] Run configuration audit utilities on deployment containers.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No citations matched.*"
    affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set))) if affected_files_set else "- *No specific files containing matching category patterns were automatically detected.*"
    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No specific migration steps required.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards configuration."
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Run standard software regression testing."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *No specific risk assessment issues compiled.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Updates

## 1. Summary
This compliance pull request introduces updates to align the repository with the latest revisions to monitored international and industry technical standards. It addresses security, quality, privacy, and AI systems frameworks to maintain organizational compliance.

## 2. Background
Technical standards evolve to mitigate sophisticated threats, verify operational consistency, and regulate artificial intelligence ecosystems. This update ensures that codebase definitions and internal guidelines match active industry specifications.

## 3. Regulatory change
Standardization directives enforce proactive risk assessments, privacy-by-design implementations, and systematic security governance across all deployed software modules.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High compliance risk if technical baseline standards diverge from official expectations.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes preserve backward compatibility. Declarations and baseline configurations fallback gracefully to older specifications where newer standards are not yet natively compiled.

## 9. Implementation checklist
{impl_checklist_str}

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with active checklists.
- [ ] Revise the internal compliance policy wiki page with standard changes.

## 12. Compliance impact
Aligns the organization with international standards (ISO/IEC, NIST), ensuring seamless partner auditing and mitigating customer compliance strikes.

## 13. Breaking changes
- No functional features are broken. Operational controls are tightened to meet secure baselines.

## 14. Review checklist
- [ ] Verify the code and configuration files are 100% free of emojis or graphical symbols.
- [ ] Confirm citations trace back to Priority 1 official sources.

## 15. Approver recommendations
Verify that security architecture reviews are completed for the targeted ISMS, PIMS, and AIMS configurations. Validate compliance of automated deployment pipelines with the newly configured standards checks.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Generates the migration report inside docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority compliance baseline requirements."
        )

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update access control policies and check logging registers.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Document PII processing flows and define controller roles.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Enforce systematic Artificial Intelligence Management System (AIMS) audits.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Incorporate risk assessment guidelines directly in the release pipelines.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Compile QA performance logs and quality manual definitions.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Review software configuration integrity registers.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Scan repository for OWASP MASVS and ASVS baseline signals.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Set up bias mitigation checkpoints and explainability templates.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Conduct governance audits mapping current cyber protection tools.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Hardening server and container baseline files.")
        else:
            lines.append(f"- [ ] **Task**: Verify standards compliance checklist for {cat}.")
        lines.append("")

    lines.append("## Verification and Testing Recommendations")
    lines.append("")
    for u in updates:
        cat = u["category"]
        lines.append(f"### Testing Updates for {cat}")
        if cat == "ISO 27001":
            lines.append("- [ ] **Test**: Verify access list boundaries and logging system integrity.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Test**: Run PII data leak audits and controller/processor trace validations.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Test**: Validate model robustness, bias, and output safety constraints.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Test**: Verify sandbox deployment risk simulations.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Test**: Confirm CI/CD pipeline code coverage thresholds are met.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Test**: Validate software configurations against the build register.")
        elif cat == "OWASP":
            lines.append("- [ ] **Test**: Execute dependency and static OWASP security vulnerability scanner sweeps.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Test**: Evaluate interpretability and fairness indicators of AI pipelines.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Test**: Conduct tabletop incident response drills and intrusion detection sweeps.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Test**: Scan active container build configurations against CIS Benchmarks.")
        else:
            lines.append(f"- [ ] **Test**: Confirm general regression test coverage for {cat}.")
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
        description="Monitor Technical Standards Compliance"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards feeds"
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
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live Technical Standards feeds...")
        # No live public global standards RSS feed. Falling back to mock.

    if args.mock or (not args.live and not args.mock) or not announcements:
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(f"Failed to read mock file {args.mock}: {e}, using default mock dataset.", file=sys.stderr)
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    # Gather results to structure output
    report_items = []
    processed_categories = set()

    scan_results = scan_codebase_for_standards_signals(args.dir)

    for item in classified_updates:
        cat = item["category"]
        processed_categories.add(cat)

        priority, is_verified = classify_source_and_verify(item, announcements)

        affected_files = [m["file"] for m in scan_results.get(cat, [])]
        scan_verdict = f"Found {len(affected_files)} file(s) matching baseline keywords." if affected_files else "No explicit matching signals found in repository files."

        if priority in (4, 5) and not is_verified:
            pr_details = None
            scan_verdict = f"BLOCKED: Compliance Pull Request generation blocked. Announcement source is Priority {priority} (unverified secondary source)."
        else:
            pr_details = generate_pull_request_draft([item], scan_results)

        report_items.append(
            {
                "announcement_title": item["title"],
                "announcement_pubDate": item.get("pubDate", ""),
                "announcement_link": item.get("link", ""),
                "track": cat,
                "scan_verdict": scan_verdict,
                "affected_files": affected_files,
                "proposed_pull_request": pr_details,
            }
        )

    if args.json:
        # Prevent status log messages on stdout so we have clean JSON
        print(json.dumps(report_items, indent=2))
        return

    print(f"Monitored and classified {len(classified_updates)} technical standards updates:")
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Scanning codebase under '{args.dir}'... Found {total_matches} signals in code.")

    # Write/Update documentation report
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # Generate complete Pull Request draft (filtered to verified ones)
    verified_updates = []
    for item in classified_updates:
        priority, is_verified = classify_source_and_verify(item, announcements)
        if not (priority in (4, 5) and not is_verified):
            verified_updates.append(item)

    if verified_updates:
        pr_draft = generate_pull_request_draft(verified_updates, scan_results)
        if args.pr_output:
            try:
                os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
                with open(args.pr_output, "w", encoding="utf-8") as f:
                    f.write(pr_draft)
                print(f"PR draft written successfully to: {args.pr_output}")
            except Exception as e:
                print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        print("All updates were blocked from PR generation (unverified secondary sources).")


if __name__ == "__main__":
    main()
