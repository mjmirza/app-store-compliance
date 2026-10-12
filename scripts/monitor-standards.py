#!/usr/bin/env python3
"""Monitors technical standards changes across ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

Identifies repository gaps, generates implementation tasks, documentation updates,
testing updates, and drafts a 15-section PR proposal with strict source trust hierarchy validation.
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications, ISO/IEC, OWASP, CIS",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

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

# Keywords used to classify incoming standards announcements/articles
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management",
        "isms",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management",
        "pims",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai management system",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "enterprise risk management",
        "risk assessment framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality control",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "iec 61508",
        "iec/iso",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "asvs",
        "owasp llm top 10",
        "dependency-check",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "nist csf 2.0",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis controls",
        "center for internet security",
        "cis hardeners",
        "cis benchmark",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"SecurityPolicy",
        r"access_control",
        r"encryption_at_rest",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"PII",
        r"data_retention",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"model_card",
        r"ai_risk",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_assessment",
        r"risk_register",
        r"risk_mitigation",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"quality_management",
        r"QMS",
        r"process_audit",
    ],
    "IEC standards": [
        r"IEC62304",
        r"IEC82304",
        r"IEC62443",
        r"medical_device_software",
        r"industrial_control",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitizer",
        r"input_validation",
        r"csrf_token",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"ai_risk_management",
        r"model_bias",
        r"explainability",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurity_framework",
        r"incident_response",
        r"threat_detection",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Controls",
        r"hardening",
        r"secure_baseline",
    ],
}

# Mock announcements covering the 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Mandate: Alignment with Annex A Information Security Controls",
        "description": "Organizations must transition ISMS controls to align with ISO/IEC 27001:2022, incorporating threat intelligence, web filtering, and secure coding practices.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 18 May 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Extension: Mandating PII Controller and Processor Mapping",
        "description": "Updates to ISO/IEC 27701 mandate strict mapping of Personally Identifiable Information (PII) life cycles, data transfer assessments, and privacy impact controls.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 20 May 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS): Mandatory AI System Lifecycle Controls",
        "description": "ISO/IEC 42001 certification standard requires formal AI governance, impact assessments, data quality verification, and continuous monitoring of AI models.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 22 May 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Guidelines: Technical Risk Integration",
        "description": "Updated ISO 31000 implementation guidelines require integrating software supply chain and cybersecurity risk vectors into the central risk register.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 25 May 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management: Process Traceability and Automated CI Audit Trail",
        "description": "ISO 9001 revisions emphasize automated quality assurance, CI/CD pipeline verification, and strict release documentation traceability.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Wed, 27 May 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Medical & Industrial Software Safety Frameworks (IEC 62304 / IEC 62443)",
        "description": "Joint IEC guidelines mandate strict software lifecycle hazard analysis, secure network component configurations, and risk management for embedded software.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 29 May 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & Top 10 Security Updates: Addressing Modern Mobile and LLM Vulnerabilities",
        "description": "OWASP updates Mobile Application Security Verification Standard (MASVS) and LLM Top 10 to address prompt injection, insecure storage, and dynamic API security.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0: Continuous GOVERN, MAP, MEASURE, MANAGE Auditing",
        "description": "NIST guidance enforces continuous auditing across the GOVERN, MAP, MEASURE, and MANAGE functions for deployed machine learning and generative AI components.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF) 2.0: Governance Core and Supply Chain Integration",
        "description": "NIST CSF 2.0 introduces the GOVERN function, emphasizing organizational context, cybersecurity supply chain risk management (C-SCRM), and continuous control monitoring.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 05 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks & Controls v8.1: Updated Secure OS and Container Configuration Baselines",
        "description": "Center for Internet Security (CIS) releases updated benchmarks for hardened mobile operating systems, server baselines, and cloud storage configurations.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 08 Jun 2026 14:00:00 GMT",
    },
]

SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Check the linked official pages before treating anything here as an actual requirement.",
    "",
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and verification status."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org",
        "iec.ch",
        "owasp.org",
        "nist.gov",
        "cisecurity.org",
        "europa.eu",
        "eur-lex.europa.eu",
        "ftc.gov",
        "cisa.gov",
        "ico.org.uk",
        "gov.uk",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "open web application security project",
        "national institute of standards and technology",
        "center for internet security",
        "official publication",
        "official standard",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "peer-reviewed", "university research"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "chatgpt"]

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
        has_p1_ref = any(d in combined for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in combined
        if has_p1_ref:
            is_verified = True
        elif all_announcements:
            words = set(re.findall(r"[a-z]+", combined))
            for other in all_announcements:
                if other == announcement:
                    continue
                other_p, _ = classify_source_and_verify(other, None)
                if other_p == 1:
                    other_combined = f"{other.get('title', '')} {other.get('description', '')} {other.get('link', '')}".lower()
                    other_words = set(re.findall(r"[a-z]+", other_combined))
                    if words.intersection(other_words).intersection({"iso", "nist", "owasp", "iec", "cis"}):
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans codebase for files containing signals related to each of the 10 standards."""
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
        "dist",
    }

    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

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
                    ".yml",
                    ".yaml",
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
    """Classifies incoming announcements into the 10 standards categories."""
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


def generate_pull_request_draft(updates, scan_results, all_announcements=None):
    """Generates a draft PR complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    risk_assessment = []
    processed_categories = set()

    blocked_updates = False
    for u in updates:
        priority, is_verified = classify_source_and_verify(u, all_announcements)
        if priority in (4, 5) and not is_verified:
            blocked_updates = True

    if blocked_updates:
        return (
            "BLOCKED: Compliance Pull Request generation blocked. Announcement source is unverified secondary source."
        )

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
                f"- **{cat}**: Align access control, asset management, and cryptography policies with ISO/IEC 27001 Annex A controls."
            )
            impl_checklist.append(
                "- [ ] Update access control matrix and enforce encryption at rest for all localized data stores."
            )
            testing_checklist.append(
                "- [ ] Test access control policies and verify automated audit logging for sensitive endpoints."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance risks audit failure for ISMS certification and potential customer trust erosion."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Establish Privacy Information Management System (PIMS) workflows for PII life cycle controls and processing agreements."
            )
            impl_checklist.append(
                "- [ ] Implement PII inventory mapping and document third-party processor transfer agreements."
            )
            testing_checklist.append(
                "- [ ] Execute privacy data flow audits and verify automated data purging rules."
            )
            risk_assessment.append(
                f"- *{cat}*: Regulatory liability under global privacy frameworks due to unmapped PII processing."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) controls for model lineage, risk assessment, and oversight."
            )
            impl_checklist.append(
                "- [ ] Maintain model cards and document AI system risk assessments and training data provenance."
            )
            testing_checklist.append(
                "- [ ] Perform continuous model behavior testing and verify explainability logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to AI governance failures, unintended algorithmic bias, and compliance violations."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate software supply chain and cybersecurity risk vectors into the central enterprise risk register."
            )
            impl_checklist.append(
                "- [ ] Document technical risk criteria and establish automated risk register reporting."
            )
            testing_checklist.append(
                "- [ ] Run risk scenario simulations and verify technical risk threshold alerts."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational and security risks due to disconnected technical risk monitoring."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enforce automated build pipeline traceability and continuous software quality audit logs."
            )
            impl_checklist.append(
                "- [ ] Configure CI/CD automated test verification gates and release asset signing."
            )
            testing_checklist.append(
                "- [ ] Validate automated release packaging and build artifact checksum verification."
            )
            risk_assessment.append(
                f"- *{cat}*: Software release defects and non-repeatable deployment procedures violating QMS requirements."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Implement hazard analysis and software lifecycle safety controls matching IEC 62304 / IEC 62443 requirements."
            )
            impl_checklist.append(
                "- [ ] Perform software safety classification and document defensive coding boundaries."
            )
            testing_checklist.append(
                "- [ ] Conduct fault injection testing and safety-critical pathway validation."
            )
            risk_assessment.append(
                f"- *{cat}*: Safety hazards and industrial/medical software compliance failure."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Audit code against OWASP MASVS, ASVS, and Top 10 recommendations to harden input validation and authentication."
            )
            impl_checklist.append(
                "- [ ] Enforce strict parameter sanitization, CSRF tokens, and secure headers."
            )
            testing_checklist.append(
                "- [ ] Execute automated SAST/DAST security scans and static dependency analysis."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerability to injection attacks, broken access control, and credential theft."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Embed NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions into model development pipelines."
            )
            impl_checklist.append(
                "- [ ] Create AI impact assessments and establish human-in-the-loop review mechanisms."
            )
            testing_checklist.append(
                "- [ ] Test AI system output reliability, safety bounds, and adversarial robustness."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI outputs leading to safety breaches and compliance non-conformity."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align system monitoring, incident response, and supply chain security with NIST CSF 2.0 Core functions."
            )
            impl_checklist.append(
                "- [ ] Update incident response playbooks and maintain software bill of materials (SBOM)."
            )
            testing_checklist.append(
                "- [ ] Test incident response alerting and automated threat detection triggers."
            )
            risk_assessment.append(
                f"- *{cat}*: Delayed threat detection and extended recovery times during security incidents."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS hardeners and secure baseline configurations across mobile, host, and cloud environments."
            )
            impl_checklist.append(
                "- [ ] Hardening system configurations and disable legacy unsecure protocols."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance benchmark scanning scripts against target environments."
            )
            risk_assessment.append(
                f"- *{cat}*: System compromise due to default or insecure configuration settings."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standards patterns were automatically detected. (Perform manual review).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the application into complete alignment with international and technical security standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Adherence to published technical standards guarantees robust security, privacy, quality, risk management, and AI governance. Regular updates reconcile our codebase and infrastructure configuration with evolving standard benchmarks.

## 3. Regulatory change
- **Technical & Security Standards Alignment**: Adherence to updated ISO/IEC, NIST, OWASP, and CIS guidelines.
- **Continuous Quality & Risk Control**: Integration of automated testing, hazard analysis, and software bill of materials (SBOM) tracking.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium-to-High risk of compliance audit findings and system vulnerability if technical standards baselines are not maintained.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards updates are fully backward-compatible. Refactored security boundaries, logging mechanisms, and configuration baselines do not break public API contracts or user features.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run compliance validation scripts to confirm alignment across target files.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Execute localized automated test suites to ensure zero regressions.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed checklists.
- [ ] Document technical risk mitigation policies and architecture diagrams in technical references.

## 12. Compliance impact
- **Standards Aligned**: Satisfies ISO, NIST, OWASP, and CIS compliance auditing requirements.
- **Enhanced Security**: Hardens application boundaries against vulnerabilities and operational failures.

## 13. Breaking changes
- No functional breaking changes for end users. Legacy unencrypted storage or insecure protocol fallbacks are disabled.

## 14. Review checklist
- [ ] Diff is 100% free of emojis or graphical symbols.
- [ ] Citations are backed by Priority 1 or verified official standards sources.
- [ ] Security and quality baselines have been verified via automated tests.

## 15. Approver recommendations
Verify that technical standards control implementations align with organizational security policies. Confirm that automated testing and documentation updates pass continuous integration validation before merging.
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
        "# Technical Standards Compliance & Migration Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
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
            "- **Compliance Impact**: High priority. Standards audit mandates action."
        )

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update access control policies and enforce encryption at rest.")
            lines.append("- [ ] **Task 2**: Review Annex A information security control coverage.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Audit PII data flows and update processing agreements.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Implement AIMS AI system lifecycle controls and maintain model cards.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Integrate technical and supply chain risk vectors into risk register.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Configure automated CI/CD quality assurance gates.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Perform software safety classification and hazard analysis.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Harden input validation and execute SAST/DAST security scans.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Integrate GOVERN, MAP, MEASURE, and MANAGE functions into AI pipelines.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align incident response playbooks with NIST CSF 2.0 Core.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Apply CIS hardening baselines across target configurations.")
        else:
            lines.append(f"- [ ] **Task**: Verify that technical requirements for {cat} are met.")
        lines.append("")

    lines.append("## Automated Testing Recommendations & Verification Updates")
    lines.append("")

    processed_test_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_test_cats:
            continue
        processed_test_cats.add(cat)
        lines.append(f"### Testing Updates for {cat}")
        lines.append(f"- [ ] **Test Step 1**: Verify control enforcement for {cat} using automated test scripts.")
        lines.append(f"- [ ] **Test Step 2**: Ensure zero regression in functionality during {cat} audit checks.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def run_monitor(start_dir=".", announcements=None, keywords_filter=None):
    """Runs the monitor scan and returns classified updates and scan results."""
    classified_updates = classify_announcements(announcements, keywords_filter)
    scan_results = scan_codebase_for_standards_signals(start_dir)
    return classified_updates, scan_results


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Changes (ISO, OWASP, NIST, CIS, IEC)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live RSS feeds or fallback to sample data if empty",
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
        "--dir",
        "--project",
        dest="dir",
        type=str,
        default=".",
        help="Codebase directory to scan",
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
        "--json",
        action="store_true",
        help="Output report in JSON format",
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        # Example live feed check for NIST / OWASP feeds
        live_items = parse_rss_feed("https://csrc.nist.gov/CSRC/media/feeds/rss/news-and-updates.xml")
        if live_items:
            announcements.extend(live_items)

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print(
            "Data. sample announcements built into this script, not live news.",
            file=sys.stderr if args.json else sys.stdout,
        )
        if not args.json:
            print("Using comprehensive mock Technical Standards updates for compliance scanning...")
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
        print(
            "Data. live feeds, fetched just now.",
            file=sys.stderr if args.json else sys.stdout,
        )

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates, scan_results = run_monitor(args.dir, announcements, keywords_filter)

    if not classified_updates:
        if args.json:
            print(json.dumps([]))
        else:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    if args.json:
        json_output = []
        for u in classified_updates:
            cat = u["category"]
            p, is_v = classify_source_and_verify(u, announcements)
            json_output.append({
                "id": u["id"],
                "category": cat,
                "title": u["title"],
                "description": u["description"],
                "link": u["link"],
                "pubDate": u["pubDate"],
                "source_priority": p,
                "verified": is_v,
                "affected_files": [f["file"] for f in scan_results.get(cat, [])],
            })
        print(json.dumps(json_output, indent=2))
        return

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for standards integration signals...")
    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock)
    else:
        print("No file written. Pass --output-docs <path> to save this report.")

    pr_draft = generate_pull_request_draft(classified_updates, scan_results, announcements)
    if used_mock and not pr_draft.startswith("BLOCKED:"):
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
