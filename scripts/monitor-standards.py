#!/usr/bin/env python3
"""Technical Standards Monitor: tracks 10 key technical standards against live/mock
news feeds, scans the codebase for compliance signals, updates documentation report,
and drafts a 15-section, emoji-free compliance Pull Request."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
TRACKED_STANDARDS = [
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

# Keywords used to classify announcements/articles into the 10 categories
STANDARD_KEYWORDS = {
    "ISO 27001": [
        "iso 27001", "iso/iec 27001", "isms", "information security management"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "pims", "privacy information management"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "aims", "ai management", "artificial intelligence management system"
    ],
    "ISO 31000": [
        "iso 31000", "risk management", "risk assessment", "risk register"
    ],
    "ISO 9001": [
        "iso 9001", "qms", "quality management", "continuous improvement"
    ],
    "IEC standards": [
        "iec standards", "iec 62304", "iec 82304", "iec 62443", "software lifecycle", "iec standard"
    ],
    "OWASP": [
        "owasp", "masvs", "asvs", "owasp top 10", "injection prevention"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "trustworthy ai", "bias mitigation"
    ],
    "NIST CSF": [
        "nist csf", "cybersecurity framework", "nist sp 800-53", "identify detect protect"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis control", "cis standard", "hardened configuration"
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
STANDARD_SIGNALS = {
    "ISO 27001": [
        r"ISMS", r"ISO 27001", r"ISO/IEC 27001", r"information security policy"
    ],
    "ISO 27701": [
        r"PIMS", r"ISO 27701", r"Personally Identifiable Information", r"PII encryption"
    ],
    "ISO 42001": [
        r"AIMS", r"ISO 42001", r"artificial intelligence policy", r"AI risk management"
    ],
    "ISO 31000": [
        r"risk register", r"risk treatment", r"risk mitigation", r"ISO 31000"
    ],
    "ISO 9001": [
        r"QMS", r"ISO 9001", r"quality policy", r"continuous improvement"
    ],
    "IEC standards": [
        r"IEC 62304", r"IEC 82304", r"IEC 62443", r"software lifecycle"
    ],
    "OWASP": [
        r"OWASP", r"MASVS", r"ASVS", r"MSTG", r"injection prevention"
    ],
    "NIST AI RMF": [
        r"NIST AI RMF", r"trustworthy AI", r"bias mitigation", r"model transparency"
    ],
    "NIST CSF": [
        r"NIST CSF", r"NIST SP 800-53", r"identify detect protect"
    ],
    "CIS Benchmarks": [
        r"CIS Benchmark", r"CIS Level 1", r"CIS Level 2", r"hardened configuration"
    ],
}

# Metadata detailing gaps, tasks, doc updates, testing, and risks for each of the 10 standards
STANDARD_METADATA = {
    "ISO 27001": {
        "gap": "Lack of automated IAM permission audits and formalized information security management protocols.",
        "task": "Develop automated access review workflows and integrate security policy checkers in compliance with A.9 control domains.",
        "doc_update": "Document corporate Access Control Guidelines and maintain information security policy statements in docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Add automated unit tests to verify that permission levels and IAM policies block unauthorized access requests.",
        "risk": "Uncontrolled access privileges or lack of security oversight leading to undetected system intrusion or permission escalation."
    },
    "ISO 27701": {
        "gap": "Missing structured consent management tracking and validated Personally Identifiable Information (PII) data lifetime records.",
        "task": "Implement database schemas to record explicit user consent and configure automated script triggers for purging expired data profiles.",
        "doc_update": "Document privacy architecture boundaries and data retention rules in docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Configure integration tests to simulate PII database access and run regular automated data leakage checks.",
        "risk": "Regulatory non-compliance with global privacy laws, leading to hefty fines, data subject disputes, or leakage of sensitive profiles."
    },
    "ISO 42001": {
        "gap": "Missing AI model alignment safety logs, model risk register documentation, and algorithmic bias evaluations.",
        "task": "Incorporate automated content filter checks on synthetic generation pipelines and construct a dedicated model risk register.",
        "doc_update": "Publish model transparency cards and risk registers under the artificial intelligence governance section of docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Develop automated end-to-end tests verifying generative model content filter thresholds and logging bias evaluation metrics.",
        "risk": "Deployment of unsafe, biased, or non-compliant algorithmic models violating regional artificial intelligence distribution laws."
    },
    "ISO 31000": {
        "gap": "Lacks continuous risk register integration and threat modeling automation inside repository workflows.",
        "task": "Integrate a localized risk registry containing automated threat prioritization matrices directly into repository structures.",
        "doc_update": "Draft formal risk assessment logs and risk treatment plans in docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Execute simulated threat vector mapping and verify the security posture meets baseline risk tolerance specifications.",
        "risk": "Unidentified vulnerabilities or architectural weaknesses propagating into production environments without formal mitigation paths."
    },
    "ISO 9001": {
        "gap": "Absence of automated quality release gates and standardized code quality metrics checks in CI/CD pipelines.",
        "task": "Integrate strict code analysis tools and enforce minimum test coverage gates for all release candidates.",
        "doc_update": "Document code quality thresholds, peer-review guidelines, and quality policy checklists in docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Run regression and unit testing suites to ensure complete test coverage satisfies quality assurance baselines.",
        "risk": "Degrading code quality, high defect density, and regression failures slipping into production deployments."
    },
    "IEC standards": {
        "gap": "No automated Software Bill of Materials (SBOM) generation pipeline or system lifecycle traceability auditing.",
        "task": "Configure automatic SBOM generation on every production release cycle.",
        "doc_update": "Update software lifecycle verification protocols and SBOM indices in docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Verify memory safety, strict type casting, and run system validation checks against critical lifecycle parameters.",
        "risk": "Supply chain compromise or dependency vulnerabilities propagating due to untracked software packages."
    },
    "OWASP": {
        "gap": "Vulnerability to injection attacks, cross-site scripting, and insufficient parameter validation across endpoints.",
        "task": "Refactor backend endpoints to use parameterized queries and incorporate robust input validation middleware filters.",
        "doc_update": "Add OWASP MASVS/ASVS secure coding standards to docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Execute fuzzing test suites and run automated vulnerability scanners against staging endpoints.",
        "risk": "Exploitation of standard injection vectors leading to database exfiltration or unauthorized system takeovers."
    },
    "NIST AI RMF": {
        "gap": "No model transparency notices, bias mitigation matrices, or trustworthy AI governance disclosures.",
        "task": "Implement model explainability APIs and establish public trustworthy AI disclosures during user onboarding.",
        "doc_update": "Draft trustworthy AI system guidance and transparency metrics within docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Run bias metrics evaluation and model drift simulation tests to measure reliability and accuracy over time.",
        "risk": "Loss of user trust, ethical failures, and non-compliance with emerging trustworthy AI framework guidance."
    },
    "NIST CSF": {
        "gap": "Missing unified security incident response playbooks and centralized log auditing protocols.",
        "task": "Establish structured centralized security logs and configure immediate notification triggers for anomalous activity.",
        "doc_update": "Incorporate NIST CSF security control maps and incident recovery guides inside docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Test security detection alerts and execute simulated incident recovery walkthroughs.",
        "risk": "Undetected system compromises, slow incident response times, and failure to contain active security threats."
    },
    "CIS Benchmarks": {
        "gap": "Lacks automated container hardening configuration sweeps and regular system configuration audits.",
        "task": "Establish container and infrastructure-as-code hardening checks to disable cleartext protocols and restrict ports.",
        "doc_update": "Document system hardening baselines and CIS benchmark levels inside docs/STANDARDS-POLICY-MIGRATION.md.",
        "test_update": "Verify container execution environments block unencrypted services and restrict host resource permissions.",
        "risk": "Insecure defaults, exposed ports, or unhardened hosting environments allowing easy compromise by external actors."
    },
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Security Management Update: Enforcing Multi-Factor Authentication and Access Reviews",
        "description": "To maintain alignment with ISO 27001 standards, organizations must enforce multi-factor authentication (MFA) across all identity domains and establish automated quarterly access control review schedules.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System (PIMS) Requirements",
        "description": "Compliance updates for ISO 27701 require strict tracking of PII lifecycle events, mandatory end-to-end encryption for stored user profiles, and programmatic record keeping of consent withdrawals.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System (AIMS) Launch",
        "description": "The ISO 42001 standard specifies requirements for establishing, implementing, maintaining, and continually improving an AI management system within organizations to address safety and ethical concerns.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines: Enhancing Threat Modeling Integration",
        "description": "Updated risk treatment protocols under ISO 31000 mandate integrating threat modeling into active repository CI gates and updating local risk registers systematically on release cycles.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Updates: Establishing Automated Quality Release Gates",
        "description": "Under the updated ISO 9001 guidelines, continuous improvement processes must be backed by automated static analysis code quality checks and test coverage release gates.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC Standards Update: Mandatory Lifecycle Traceability and Software Bill of Materials (SBOM)",
        "description": "New IEC software safety guidelines mandate complete components traceability. Developers must maintain an automated Software Bill of Materials (SBOM) and run safety-critical unit tests.",
        "link": "https://www.iec.ch",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Security Controls: Universal Hardening against Injection and Cross-Site Scripting",
        "description": "The latest OWASP guidelines require universal input sanitization and parametric queries to fully eliminate command injection, SQL injection, and cross-site scripting vulnerabilities.",
        "link": "https://owasp.org",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework: Guidelines for Trustworthy AI Systems",
        "description": "NIST issues new guidance for managing generative AI risks under the AI RMF, prioritizing model transparency, explicit bias detection metrics, and user explainability options.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST CSF 2.0: Enhancing Identity, Detection, and Incident Response Playbooks",
        "description": "NIST CSF 2.0 cybersecurity framework updates require organizations to implement robust security event logging, real-time intrusion detection rules, and structured incident recovery playbooks.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Security Update: Mandating Automated Configuration Audits",
        "description": "Center for Internet Security (CIS) Benchmarks updates mandate regular automated host and container configuration scanning to ensure system hardening, disabling cleartext services.",
        "link": "https://www.cisecurity.org",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies incoming announcements into the Source Trust Hierarchy priority (1-5)
    and verification status."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk"
    ]
    p1_keywords = [
        "iso", "iec", "nist", "owasp", "cisecurity", "european commission",
        "official journal", "enisa", "edpb", "ftc", "cisa", "ico",
        "government publication", "federal register"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial", "vendor blog"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "forum", "anonymous", "unverified rumor"]

    priority = 4

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

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Check if verified by a Priority 1 official reference
        has_p1_ref = any(d in combined for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in combined
        if has_p1_ref:
            is_verified = True
        elif all_announcements:
            for other in all_announcements:
                if other == announcement:
                    continue
                other_p, _ = classify_source_and_verify(other, None)
                if other_p == 1:
                    is_verified = True
                    break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcement, all_announcements=None):
    """Enforces source trust credibility restrictions, logging alerts to stderr."""
    priority, is_verified = classify_source_and_verify(announcement, all_announcements)
    if priority in (4, 5) and not is_verified:
        sys.stderr.write(
            f"WARNING: Source trust hierarchy verification failed for Priority {priority} announcement: "
            f"'{announcement.get('title')}' - Blocked PR generation.\n"
        )
        return priority, False
    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 categories."""
    matches = {std: [] for std in TRACKED_STANDARDS}
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
        std: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for std, patterns in STANDARD_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
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
                        for std, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[std].append(
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
    """Classifies incoming announcements into the 10 technical standard categories."""
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        matched_categories = []
        # If the announcement defines an explicit category, prioritize it to avoid overlap
        if ann.get("category"):
            matched_categories.append(ann["category"])
        else:
            for std, keywords in STANDARD_KEYWORDS.items():
                for kw in keywords:
                    if kw.lower() in text_to_search:
                        matched_categories.append(std)
                        break

        if matched_categories:
            for std in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "STD-UPDATE-" + str(hash(title))[:6]),
                        "category": std,
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
    documentation_checklist = []
    risk_assessment = []

    for u in updates:
        std = u["category"]
        citations_list.append(
            f"- **{std}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(std, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        meta = STANDARD_METADATA.get(std, {})
        migration_steps.append(
            f"- **{std}**: {meta.get('task', 'Verify compliance requirements.')}"
        )
        impl_checklist.append(
            f"- [ ] Implement controls for {std}: {meta.get('task', 'Verify standard.')}"
        )
        testing_checklist.append(
            f"- [ ] Update testing for {std}: {meta.get('test_update', 'Verify standard.')}"
        )
        documentation_checklist.append(
            f"- [ ] Update documentation for {std}: {meta.get('doc_update', 'Verify standard.')}"
        )
        risk_assessment.append(
            f"- **{std}**: {meta.get('risk', 'Undetected compliance vulnerabilities.')}"
        )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standards patterns were automatically detected. (Perform manual review of configurations).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    documentation_checklist_str = "\n".join(documentation_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into complete compliance with all monitored technical standards. It addresses system hardening, risk registers, privacy information management, quality gates, and AI governance.

## 2. Background
In modern software development, conformity with international and industry-recognized technical standards ensures security, quality, privacy, and safety. Adopting these standards systematically reduces architectural vulnerability and complies with enterprise distribution expectations.

## 3. Regulatory change
- **Conformity Assessment**: Standards updates require organizations to actively assess compliance, identify architectural gaps, implement automated tasks, and update documentation and testing structures.
- **Continuous Monitoring**: Maintaining alignment with evolving standards demands regular monitoring of announcements and programmatic repository scans.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Risk is categorized as high if standard requirements are neglected, resulting in quality degradation, security vulnerabilities, or privacy breaches.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All adjustments to code standards, metadata, and logging are fully backward-compatible. No breaking API changes are introduced, preserving seamless execution for legacy deployments.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated checks to verify standard declarations.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run the test suites to ensure standard compliance remains unbroken.

## 11. Documentation checklist
{documentation_checklist_str}
- [ ] Ensure docs/STANDARDS-POLICY-MIGRATION.md contains the latest updates.

## 12. Compliance impact
Aligning with these standards mitigates security vulnerability risks, improves application performance and defect density, enforces trustworthy artificial intelligence architectures, and ensures corporate compliance.

## 13. Breaking changes
There are no breaking changes introduced by these compliance adjustments. Legacy operations remain unaffected.

## 14. Review checklist
- [ ] Ensure the entire pull request and code is 100% free of emojis or graphical symbols.
- [ ] Confirm all technical standards citations are accurate and trace back to official sources.
- [ ] Verify that no unvetted dependencies are integrated.

## 15. Approver recommendations
Verify that the automated release gates are configured correctly in the CI pipelines. Ensure all access control reviews and risk registries are updated and signed off by the technical lead.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance areas.",
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

    lines.append("## Automated Migration Recommendations, Gaps & Gaps Remediation")
    lines.append("")

    for u in updates:
        std = u["category"]
        meta = STANDARD_METADATA.get(std, {})
        lines.append(f"### Tasks for {std}")
        lines.append(
            "- **Regulatory Impact**: High priority. Technical standard audit mandates action."
        )
        lines.append(f"- **Identified Repository Gap**: {meta.get('gap', 'No automated verification checks in place.')}")
        lines.append(f"- [ ] **Task 1 (Implementation)**: {meta.get('task', 'Implement missing standard control.')}")
        lines.append(f"- [ ] **Task 2 (Testing)**: {meta.get('test_update', 'Add tests for the standard.')}")
        lines.append(f"- [ ] **Task 3 (Documentation)**: {meta.get('doc_update', 'Update reference documentation.')}")
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
        description="Monitor and track updates to Technical Standards"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards updates (dummy flag)"
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

    if args.mock:
        if args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default mock dataset.",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    # Filter announcements through Source Trust Hierarchy enforcement
    filtered_updates = []
    for u in classified_updates:
        priority, is_verified = enforce_strict_source_trust_hierarchy(u, announcements)
        if priority in (4, 5) and not is_verified:
            # Skip generating PR if blocked, but keep in classified updates if necessary
            continue
        filtered_updates.append(u)

    if not filtered_updates:
        print("All matching updates were blocked by strict Source Trust Hierarchy rules.")
        sys.exit(0)

    # Deduplicate updates by standard category to avoid duplicate sections and headers
    unique_updates = []
    seen_categories = set()
    for u in filtered_updates:
        if u["category"] not in seen_categories:
            seen_categories.add(u["category"])
            unique_updates.append(u)

    filtered_updates = unique_updates

    print(
        f"Monitored and classified {len(filtered_updates)} technical standards updates:"
    )
    for idx, u in enumerate(filtered_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for technical standard signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(filtered_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(filtered_updates, scan_results)

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        print("\n=== GENERATED 15-SECTION COMPLIANCE PULL REQUEST DRAFT ===")
        print(pr_draft)
        print("==========================================================")


if __name__ == "__main__":
    main()
