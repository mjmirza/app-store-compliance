#!/usr/bin/env python3
"""Monitors technical standards updates across 10 core standards frameworks:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates."""

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

# Keywords used to classify incoming standards updates/announcements
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management system",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management system",
        "privacy controls",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai governance standard",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment framework",
        "enterprise risk management",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance standard",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "international electrotechnical commission",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "asvs",
        "open web application security project",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "govern identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "hardening benchmarks",
    ],
}

# Codebase signals (regex patterns) to find files affected by or referencing each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO/IEC 27001",
        r"ISO 27001",
        r"ISMS",
        r"information security management",
    ],
    "ISO 27701": [
        r"ISO/IEC 27701",
        r"ISO 27701",
        r"PIMS",
        r"privacy information management",
    ],
    "ISO 42001": [
        r"ISO/IEC 42001",
        r"ISO 42001",
        r"AIMS",
        r"artificial intelligence management",
    ],
    "ISO 31000": [
        r"ISO 31000",
        r"risk management framework",
        r"risk assessment",
    ],
    "ISO 9001": [
        r"ISO 9001",
        r"quality management system",
        r"QMS",
    ],
    "IEC standards": [
        r"IEC 62443",
        r"IEC 82304",
        r"IEC 62304",
        r"IEC standards",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"OWASP Top 10",
    ],
    "NIST AI RMF": [
        r"NIST AI RMF",
        r"AI Risk Management Framework",
        r"NIST AI",
    ],
    "NIST CSF": [
        r"NIST CSF",
        r"Cybersecurity Framework",
        r"NIST CSF 2.0",
    ],
    "CIS Benchmarks": [
        r"CIS Benchmarks",
        r"CIS Controls",
        r"Center for Internet Security",
    ],
}

# Strict Source Trust Hierarchy classification mapping
PRIORITY_SOURCES = {
    1: ["iso.org", "nist.gov", "cisecurity.org", "owasp.org", "iec.ch"],
    2: ["reuters.com", "apnews.com", "bloomberg.com"],
    3: ["ieee.org", "acm.org", "arxiv.org"],
    4: ["industryblog.com", "techblog.io"],
    5: ["linkedin.com", "reddit.com", "x.com", "twitter.com"],
}

# Mock announcements covering the 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 ISMS Update: Annex A Controls Revision for Cloud and Remote Working",
        "description": "ISO/IEC 27001 standard guidance updates Information Security Management System (ISMS) controls, mandating explicit policies for cloud service monitoring, threat intelligence integration, and secure remote working environments.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 10 Aug 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 PIMS Expansion: Standardized Privacy Impact Assessments and Data Mapping",
        "description": "ISO/IEC 27701 Privacy Information Management System guidelines specify mandatory Privacy Impact Assessment (PIA) documentation, explicit consent lifecycle logging, and data minimisation controls across all customer-facing applications.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 12 Aug 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AIMS Specification: Requirements for AI Governance and Model Traceability",
        "description": "The ISO/IEC 42001 Artificial Intelligence Management System (AIMS) mandates full model training lineage logging, continuous algorithmic impact assessments, and standardized human oversight mechanisms for production AI components.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 14 Aug 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines: Integrating Continuous Automated Risk Identification",
        "description": "ISO 31000 guidelines update risk assessment frameworks, recommending continuous automated risk monitoring in software delivery pipelines alongside structured risk register updates for operational hazards.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 17 Aug 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System: Code Quality Metrics and Deployment Gates",
        "description": "ISO 9001 QMS revisions emphasize software quality assurance controls, continuous integration testing coverage thresholds, and formal sign-off gates prior to release deployment.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 19 Aug 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Electrotechnical and Software Security Controls in Embedded Systems",
        "description": "International Electrotechnical Commission (IEC) guidelines update security lifecycle standards for connected software components, requiring secure boot configurations, firmware signing, and interface isolation.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 21 Aug 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & ASVS Update: Enhanced Mobile and Web Application Controls",
        "description": "OWASP releases revised Mobile Application Security Verification Standard (MASVS) and Application Security Verification Standard (ASVS) baselines, introducing strict token handling, anti-hooking, and secure API contract rules.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Mon, 24 Aug 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.1: Govern, Map, Measure, and Manage Core Controls",
        "description": "NIST releases updated AI RMF guidance detailing actionable measurement methodologies for AI system safety, bias mitigation, transparency disclosures, and adversarial robustness testing.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 26 Aug 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF) 2.0: Implementation Guidelines for Supply Chain Security",
        "description": "NIST CSF 2.0 guidance mandates explicit governance subcategories for supply chain risk management, continuous software bill of materials (SBOM) generation, and zero trust architecture alignment.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 28 Aug 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Revision: Hardening Recommendations for Containerized and Cloud Services",
        "description": "Center for Internet Security (CIS) releases updated benchmarks specifying non-root execution, read-only root filesystems, secure TLS configurations, and strict role-based access control (RBAC) policies.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 31 Aug 2026 11:00:00 GMT",
    },
]


def enforce_strict_source_trust_hierarchy(link):
    """Enforces source trust hierarchy, returning the priority tier (1-5)."""
    if not link:
        return 5
    link_lower = link.lower()
    for priority, domains in PRIORITY_SOURCES.items():
        for domain in domains:
            if domain in link_lower:
                return priority
    return 4


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals or references to the 10 technical standards."""
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
                    ".md",
                    ".py",
                    ".sh",
                    ".yml",
                    ".yaml",
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


def parse_rss_feed(url):
    """Fetches and parses live RSS or Atom XML feeds."""
    items = []
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (StandardsComplianceMonitor/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            def clean_tag(tag):
                return tag.split("}", 1)[1] if "}" in tag else tag

            for elem in root.iter():
                tag = clean_tag(elem.tag)
                if tag in ("item", "entry"):
                    title = ""
                    desc = ""
                    link = ""
                    pub_date = ""

                    for child in elem:
                        ctag = clean_tag(child.tag)
                        if ctag == "title":
                            title = child.text or ""
                        elif ctag in ("description", "summary", "content"):
                            desc = child.text or ""
                        elif ctag == "link":
                            link_val = child.get("href")
                            link = link_val if link_val else (child.text or "")
                        elif ctag in ("pubDate", "published", "updated"):
                            pub_date = child.text or ""

                    items.append(
                        {
                            "title": title.strip(),
                            "description": desc.strip() if desc else "",
                            "link": link.strip(),
                            "pubDate": pub_date.strip(),
                        }
                    )
    except Exception as e:
        print(f"Warning: Failed to fetch live feed {url}: {e}", file=sys.stderr)
    return items


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
                priority = enforce_strict_source_trust_hierarchy(ann.get("link", ""))
                classified_updates.append(
                    {
                        "id": ann.get("id", "STD-UPDATE-" + str(hash(title))[:6]),
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": ann.get("link", ""),
                        "pubDate": ann.get("pubDate", ""),
                        "priority_tier": priority,
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a draft of a pull request complying with exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    doc_checklist = []
    risk_assessment = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source Priority: Tier {u.get('priority_tier', 1)})"
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
                f"- **{cat}**: Audit ISMS controls against updated Annex A guidance, ensuring continuous monitoring for cloud infrastructure and remote access endpoints."
            )
            impl_checklist.append(
                "- [ ] Update Information Security Management System (ISMS) policy documentation and control maps."
            )
            testing_checklist.append(
                "- [ ] Verify cloud infrastructure configuration monitoring scripts pass ISMS compliance audits."
            )
            doc_checklist.append(
                "- [ ] Update ISMS policy documentation in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with enterprise ISMS mandates, leading to certification audit findings and unmitigated cloud risk."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) controls, integrating automated data lifecycle logging and privacy impact assessments."
            )
            impl_checklist.append(
                "- [ ] Update PIMS data mapping documentation and privacy impact assessment templates."
            )
            testing_checklist.append(
                "- [ ] Execute automated privacy consent lifecycle tests to confirm data minimization rules."
            )
            doc_checklist.append(
                "- [ ] Record PIMS control updates in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate privacy governance documentation risking regulatory non-compliance during privacy audits."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance for AI/ML pipelines, ensuring model traceability and risk logging."
            )
            impl_checklist.append(
                "- [ ] Configure AI model training lineage logging and continuous algorithmic impact assessment procedures."
            )
            testing_checklist.append(
                "- [ ] Perform automated verification of AI model lineage logs and fallback mechanisms."
            )
            doc_checklist.append(
                "- [ ] Document AIMS governance workflows in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored production AI models risking algorithmic bias, safety failures, and EU AI Act / ISO 42001 violations."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align enterprise risk assessment workflows with ISO 31000 guidelines, embedding risk evaluation into release pipelines."
            )
            impl_checklist.append(
                "- [ ] Update the repository risk assessment matrix and automated risk checker rules."
            )
            testing_checklist.append(
                "- [ ] Run pipeline risk evaluation scripts to verify zero high-risk unmitigated findings."
            )
            doc_checklist.append(
                "- [ ] Document updated risk evaluation thresholds in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Unidentified operational or technical risks escalating to production incidents."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enhance QMS code quality controls, enforcing automated test coverage gates and formal release review sign-offs."
            )
            impl_checklist.append(
                "- [ ] Configure CI quality gate checks for unit test coverage and code linting."
            )
            testing_checklist.append(
                "- [ ] Verify that CI/CD pipelines enforce automated quality test coverage thresholds prior to build output."
            )
            doc_checklist.append(
                "- [ ] Update QMS software quality procedures in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation and lack of release traceability in production systems."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce International Electrotechnical Commission software lifecycle and secure boot standards for connected components."
            )
            impl_checklist.append(
                "- [ ] Validate firmware signing configurations and interface isolation protocols."
            )
            testing_checklist.append(
                "- [ ] Run automated interface boundary tests for electrotechnical and embedded components."
            )
            doc_checklist.append(
                "- [ ] Update IEC software security standards references in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Software boundary vulnerabilities in connected device interfaces."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align application controls with updated OWASP MASVS and ASVS benchmarks, securing token storage and API contracts."
            )
            impl_checklist.append(
                "- [ ] Implement OWASP MASVS/ASVS recommendations for session token isolation and input validation."
            )
            testing_checklist.append(
                "- [ ] Run dynamic vulnerability and security regression test suites against OWASP Top 10 patterns."
            )
            doc_checklist.append(
                "- [ ] Update OWASP security verification checklists in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to OWASP Top 10 vulnerabilities including credential leakage and injection flaws."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Incorporate NIST AI Risk Management Framework 1.1 controls across Govern, Map, Measure, and Manage functions."
            )
            impl_checklist.append(
                "- [ ] Embed NIST AI RMF measurement frameworks for AI safety, bias mitigation, and transparency disclosures."
            )
            testing_checklist.append(
                "- [ ] Execute adversarial AI robustness and bias evaluation test suites."
            )
            doc_checklist.append(
                "- [ ] Record NIST AI RMF mapping in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-alignment with US federal AI governance baselines leading to compliance and safety gaps."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Adopt NIST Cybersecurity Framework 2.0 subcategories, focusing on continuous SBOM generation and zero trust architecture."
            )
            impl_checklist.append(
                "- [ ] Integrate automated Software Bill of Materials (SBOM) generation into deployment pipelines."
            )
            testing_checklist.append(
                "- [ ] Test automated dependency vulnerability scanners against the generated SBOM."
            )
            doc_checklist.append(
                "- [ ] Update NIST CSF 2.0 mapping documentation in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Supply chain vulnerabilities due to untracked dependencies or unverified third-party code."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply updated CIS Benchmarks hardening guidelines, ensuring non-root container execution and secure environment parameters."
            )
            impl_checklist.append(
                "- [ ] Update deployment configurations to enforce non-root execution and read-only root filesystems."
            )
            testing_checklist.append(
                "- [ ] Run static environment configuration security audits to verify CIS Benchmark compliance."
            )
            doc_checklist.append(
                "- [ ] Document CIS Benchmarks hardening rules in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Container escape or environment compromise due to misconfigured permissions."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standards signals were automatically detected. (Perform manual review of repository governance files).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Run automated standards verification test suite."
    doc_checklist_str = "\n".join(doc_checklist) if doc_checklist else "- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md`."
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the repository with updated technical standards across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It identifies repository gaps, generates implementation tasks, updates governance documentation, and adds automated standards verification tests.

## 2. Background
Maintaining alignment with international technical standards and cybersecurity frameworks is essential for organizational security, software quality, and regulatory compliance. Regular monitoring ensures that technical controls, risk assessments, and software practices reflect current revisions.

## 3. Regulatory change
- **Technical Standards Frameworks**: Updates across ISO/IEC standards (27001, 27701, 42001, 31000, 9001, IEC), OWASP verification standards, NIST AI RMF, NIST CSF 2.0, and CIS Benchmarks.
- **Source Trust Hierarchy**: Official standards organizations (ISO, NIST, CIS, OWASP, IEC) serve as Priority Tier 1 primary sources.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to high compliance and security risk if standards baselines diverge from official specifications.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards governance updates are backward-compatible. Technical control enhancements and documentation updates reinforce system security without breaking existing external API contracts.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Verify that all standards gaps identified during scanning have associated implementation tasks.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Execute `bash scripts/monitor-standards-test.sh` to confirm standards monitor operation.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Confirm all standards citations match official primary sources.

## 12. Compliance impact
- **Audit Preparedness**: Maintains full traceability for ISO 27001, ISO 27701, ISO 42001, and NIST CSF audits.
- **Risk Mitigation**: Ensures application controls align with OWASP MASVS and CIS Benchmarks.
- **Governance Integrity**: Establishes continuous standards monitoring across all 10 tracked frameworks.

## 13. Breaking changes
- No breaking software changes introduced. Hardened configuration requirements must be validated prior to deployment.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] Primary source citations are verified against Tier 1 official publications.
- [ ] Implementation and testing tasks are non-vague and actionable.

## 15. Approver recommendations
Verify that all governance policy documents in `docs/` reflect the latest standard control definitions. Confirm that CI automated test coverage gates validate SBOM generation and CIS container hardening rules before merging.
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


def update_documentation_report(updates, scan_results, output_filepath, is_simulated=False):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance across 10 core frameworks.",
        "",
        "## Monitored Standards Requirements Update Log",
        "",
    ])

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Source Priority**: Tier {u.get('priority_tier', 1)}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Repository Gaps, Implementation Tasks, and Testing Updates")
    lines.append("")

    processed_doc_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_doc_cats:
            continue
        processed_doc_cats.add(cat)
        lines.append(f"### Tasks for {cat}")

        # Repository gaps
        files = scan_results.get(cat, [])
        if files:
            lines.append(f"- **Repository Gaps Identified**: Found {len(files)} signal references in existing code requiring verification.")
            for f in files[:3]:
                lines.append(f"  - `{f['file']}:{f['line_num']}`: `{f['content']}`")
        else:
            lines.append(f"- **Repository Gaps Identified**: No explicit `{cat}` policy markers found in codebase. Policy documentation or code implementation required.")

        # Implementation tasks
        lines.append("- **Implementation Tasks**:")
        lines.append(f"  - [ ] **Task 1**: Audit repository controls against updated {cat} guidance.")
        lines.append(f"  - [ ] **Task 2**: Update configuration variables and governance matrices for {cat}.")

        # Documentation updates
        lines.append("- **Documentation Updates**:")
        lines.append(f"  - [ ] **Doc Task 1**: Record updated {cat} control mappings in `docs/STANDARDS-POLICY-MIGRATION.md`.")

        # Testing updates
        lines.append("- **Testing Updates**:")
        lines.append(f"  - [ ] **Test Task 1**: Add automated verification test cases validating {cat} requirements.")
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
        description="Monitor Technical Standards Updates (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live feed if available, or fall back to sample dataset with notice"
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

    if args.mock or (not args.live and not args.mock):
        used_mock = True
        if not args.json:
            print("Data. sample announcements built into this script, not live news.", file=sys.stderr if args.json else sys.stdout)
            print("Using comprehensive mock Technical Standards policy updates for compliance scanning...", file=sys.stderr if args.json else sys.stdout)

        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                if not args.json:
                    print(f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.", file=sys.stderr)
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        # Live mode attempt
        if not args.json:
            print("Data. sample announcements built into this script, not live news.")
        used_mock = True
        announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        if args.json:
            print(json.dumps({"status": "no_matches", "updates": []}))
        else:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} technical standards updates:")
        for idx, u in enumerate(classified_updates, 1):
            print(f" {idx}. [{u['category']}] {u['title']}")

    scan_results = scan_codebase_for_standards_signals(args.dir)

    if not args.json:
        total_matches = sum(len(matches) for matches in scan_results.values())
        print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
        print(f"Found {total_matches} signal matches in code.")

    if args.json:
        output_data = {
            "status": "success",
            "is_simulated": used_mock,
            "updates": classified_updates,
            "scan_results": {cat: len(matches) for cat, matches in scan_results.items()},
        }
        print(json.dumps(output_data, indent=2))
        sys.exit(0)

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, scan_results, args.output_docs, is_simulated=used_mock)
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
