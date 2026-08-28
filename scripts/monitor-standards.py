#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000,
ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).
Monitors changes to technical standards, identifies repository gaps, and
generates implementation tasks, documentation updates, and testing updates.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
CATEGORIES = [
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

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management system",
        "iso27001",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management system",
        "iso27701",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "ai management system",
        "artificial intelligence management system",
        "iso42001",
    ],
    "ISO 31000": [
        "iso 31000",
        "iso 31000:2018",
        "risk management guidelines",
        "iso31000",
    ],
    "ISO 9001": [
        "iso 9001",
        "iso 9001:2015",
        "quality management system",
        "qms",
        "iso9001",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 62304",
        "iec 82304",
        "iec standard",
        "electrotechnical",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "owasp masvs",
        "owasp asvs",
        "owasp samm",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai rmf",
        "nist ai risk management framework",
        "governing ai",
        "map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "nist sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis benchmark",
        "cis controls",
        "center for internet security",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"information_security",
        r"iso-27001",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"pii_processing",
        r"data_processor",
        r"data_controller",
        r"iso-27701",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"llm_safety",
        r"ai_impact_assessment",
        r"iso-42001",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_management",
        r"risk_assessment",
        r"risk_treatment",
        r"iso-31000",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_assurance",
        r"process_audit",
        r"quality_policy",
        r"iso-9001",
    ],
    "IEC standards": [
        r"IEC",
        r"IEC62443",
        r"IEC62304",
        r"IEC82304",
        r"electrotechnical_standard",
        r"iec-standards",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"injection",
        r"xss",
        r"csrf",
        r"owasp_top_10",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"AI_RMF",
        r"map_measure_manage",
        r"ai_risk_framework",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"CSF_2_0",
        r"cybersecurity_framework",
        r"sp800-53",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Control",
        r"cis_benchmarks",
        r"hardening_guide",
        r"cis-controls",
    ],
}

# Source trust hierarchy classification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS Security, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications, Apple Developer, Android Developer)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Mock Announcements covering all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Annex A Security Controls Revision",
        "description": "Updated Annex A controls require cloud security management, threat intelligence integration, physical security monitoring, and secure coding practices for all application codebases.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System (PIMS) Requirement Update",
        "description": "Mandates specific PII controller and processor requirements, data subject rights workflow validation, and automated privacy impact mapping across cloud infrastructure.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Management System Guidance",
        "description": "Establishes requirements for establishing, implementing, maintaining and continually improving an AI Management System (AIMS), focusing on risk management, transparency, and model traceability.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Update",
        "description": "Provides guidelines on managing risk faced by organizations. Emphasizes integration of risk assessment frameworks into software release lifecycles.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Standard Refinement",
        "description": "Updates continuous quality verification, process audit tracking, software development lifecycle quality metrics, and customer satisfaction assurance loops.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 Industrial Cybersecurity and System Security Specifications",
        "description": "Requires defense-in-depth network segregation, cryptographic integrity checks for embedded devices, and strict component vulnerability management.",
        "link": "https://www.iec.ch/cybersecurity",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 Mobile Application Security Verification Standard",
        "description": "Defines updated security requirements for storage, cryptography, authentication, network communication, platform interaction, and code protection in mobile apps.",
        "link": "https://mas.owasp.org/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Companion Guidance",
        "description": "Outlines actionable steps across Govern, Map, Measure, and Manage functions to address risks associated with generative AI and LLM implementations.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework CSF 2.0 Governance Implementation Update",
        "description": "Expands the CSF scope with the new Govern function, mandating continuous supply chain risk monitoring, incident response drills, and asset baseline inventories.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Critical Security Controls v8.1 Hardening Guidelines",
        "description": "Provides updated hardening benchmarks for mobile operating systems, cloud environments, and containerized deployment infrastructure.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    # Unverified announcement example
    {
        "id": "STD-MOCK-UNVERIFIED",
        "category": "OWASP",
        "title": "Unverified Blog Claim Regarding OWASP Top 10 Changes",
        "description": "An unofficial blog post speculating on unannounced changes to OWASP standards without official citations.",
        "link": "https://randomblogsite.com/owasp-speculation",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified).
    """
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org",
        "iec.ch",
        "nist.gov",
        "owasp.org",
        "cisecurity.org",
        "europa.eu",
        "eur-lex.europa.eu",
        "enisa.europa.eu",
        "edpb.europa.eu",
        "ftc.gov",
        "cisa.gov",
        "ico.org.uk",
        "gov.uk",
        "apple.com",
        "developer.apple.com",
        "android.com",
        "developer.android.com",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open web application security project",
        "center for internet security",
        "european commission",
        "eur-lex",
        "official journal",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
        "ico",
        "government publication",
        "apple developer",
        "android developer",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = [
        "academic paper",
        "academic study",
        "university research",
        "peer-reviewed",
    ]

    p4_domains = [
        "techcrunch.com",
        "wired.com",
        "medium.com",
        "blog",
        "randomblogsite.com",
    ]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = [
        "tweet",
        "twitter",
        "linkedin",
        "reddit",
        "ai summary",
        "ai-generated summary",
        "ai generated summaries",
        "chatgpt summary",
    ]

    priority = 4

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(
        kw in combined for kw in p4_keywords
    ):
        priority = 4
    elif (
        any(d in link for d in p3_domains)
        or any(kw in combined for kw in p3_keywords)
        or ".edu" in link
    ):
        priority = 3
    elif any(d in link for d in p2_domains) or any(
        kw in combined for kw in p2_keywords
    ):
        priority = 2

    if (
        any(d in link for d in p1_domains)
        or any(kw in combined for kw in p1_keywords)
        or ".gov" in link
        or ".iso.org" in link
    ):
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        has_p1_ref = (
            any(d in combined for d in p1_domains)
            or any(kw in combined for kw in p1_keywords)
            or ".gov" in combined
        )
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
                    common_terms = {
                        "iso",
                        "nist",
                        "owasp",
                        "cis",
                        "iec",
                        "security",
                        "standard",
                    }
                    overlap = words.intersection(other_words).intersection(
                        common_terms
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards."""
    matches = {cat: [] for cat in CATEGORIES}
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
            url,
            headers={"User-Agent": "Mozilla/5.0 (StandardsComplianceMonitor/1.0)"},
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
                classified_updates.append(
                    {
                        "id": ann.get(
                            "id", "STD-UPDATE-" + str(hash(title))[:6]
                        ),
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
    doc_checklist = []
    risk_assessment = []

    seen_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u, updates)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in seen_categories:
            continue
        seen_categories.add(cat)

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Audit Information Security Management System (ISMS) controls, access policies, and asset management procedures."
            )
            impl_checklist.append(
                "- [ ] Review ISMS policy documentation and access control configurations."
            )
            testing_checklist.append(
                "- [ ] Execute access control and credential exposure automated security test suites."
            )
            doc_checklist.append(
                "- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with ISO 27001 ISMS compliance verification evidence."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance may lead to ISMS certification audit failures and security posture vulnerabilities."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Align Privacy Information Management System (PIMS) with PII controller/processor roles and consent tracking."
            )
            impl_checklist.append(
                "- [ ] Map PII data flows and update Privacy Impact Assessment (PIA) records."
            )
            testing_checklist.append(
                "- [ ] Verify data erasure (right to be forgotten) and PII export integration tests."
            )
            doc_checklist.append(
                "- [ ] Document PII processing registers in accordance with ISO 27701 guidance."
            )
            risk_assessment.append(
                f"- *{cat}*: Risk of privacy regulatory penalties and failure to meet PIMS audit requirements."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement AI Management System (AIMS) governance controls for LLM inputs, outputs, and model risk management."
            )
            impl_checklist.append(
                "- [ ] Implement AI safety guardrails, prompt/output logging, and human oversight controls."
            )
            testing_checklist.append(
                "- [ ] Run automated AI safety regression tests, toxicity filters, and model output validation."
            )
            doc_checklist.append(
                "- [ ] Maintain AI model cards and ISO 42001 risk assessment documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored generative AI features risking hallucination, bias, and algorithmic accountability failures."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate structured enterprise risk assessment frameworks into release and engineering decisions."
            )
            impl_checklist.append(
                "- [ ] Update risk treatment plans and matrix definitions in compliance tools."
            )
            testing_checklist.append(
                "- [ ] Perform continuous risk scoring verification on deployment pipeline checks."
            )
            doc_checklist.append(
                "- [ ] Publish updated risk matrix guidelines in `docs/`."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate risk assessment coverage leading to unmitigated operational or compliance vulnerabilities."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Strengthen Quality Management System (QMS) process audits, automated testing gates, and release metrics."
            )
            impl_checklist.append(
                "- [ ] Enforce mandatory code review, static analysis, and testing coverage gates."
            )
            testing_checklist.append(
                "- [ ] Validate CI/CD pipeline test coverage and quality gate enforcement."
            )
            doc_checklist.append(
                "- [ ] Document quality management procedures and release readiness checklists."
            )
            risk_assessment.append(
                f"- *{cat}*: Quality regressions causing customer dissatisfaction and QMS audit findings."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Apply IEC 62443 / IEC 62304 electrotechnical and software lifecycle security controls."
            )
            impl_checklist.append(
                "- [ ] Audit component dependency trees and apply cryptographic integrity verification."
            )
            testing_checklist.append(
                "- [ ] Execute static application security testing (SAST) and component vulnerability scans."
            )
            doc_checklist.append(
                "- [ ] Update system architecture security documentation per IEC guidelines."
            )
            risk_assessment.append(
                f"- *{cat}*: Embedded or infrastructure vulnerability exposure under electrotechnical security benchmarks."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Remediate OWASP Top 10 and MASVS mobile/web security risks across storage, transport, and authentication."
            )
            impl_checklist.append(
                "- [ ] Implement parameterized queries, input sanitization, and secure token storage."
            )
            testing_checklist.append(
                "- [ ] Run dynamic application security testing (DAST) and OWASP ZAP / penetration test suites."
            )
            doc_checklist.append(
                "- [ ] Maintain OWASP MASVS compliance verification checklists."
            )
            risk_assessment.append(
                f"- *{cat}*: High risk of exploitability (SQLi, XSS, CSRF, insecure storage) leading to security breaches."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI Risk Management Framework functions (Govern, Map, Measure, Manage)."
            )
            impl_checklist.append(
                "- [ ] Map AI system impacts, measure risk metrics, and implement manage controls."
            )
            testing_checklist.append(
                "- [ ] Test AI system robustness, red-teaming prompts, and adversarial input resilience."
            )
            doc_checklist.append(
                "- [ ] Document NIST AI RMF profile alignment in `docs/`."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to manage AI risks leading to reputational damage, bias, or safety hazards."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST Cybersecurity Framework (CSF 2.0) functions."
            )
            impl_checklist.append(
                "- [ ] Review Identify, Protect, Detect, Respond, Recover, and Govern controls."
            )
            testing_checklist.append(
                "- [ ] Validate incident response alerting, logging completeness, and recovery procedures."
            )
            doc_checklist.append(
                "- [ ] Update security architecture documentation with NIST CSF mapping."
            )
            risk_assessment.append(
                f"- *{cat}*: Gaps in cybersecurity posture increasing likelihood of unmitigated security incidents."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Critical Security Controls hardening guidelines across mobile, container, and cloud environments."
            )
            impl_checklist.append(
                "- [ ] Harden OS configurations, container images, and deployment manifests according to CIS benchmarks."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance scanner scripts against system configurations."
            )
            doc_checklist.append(
                "- [ ] Document CIS benchmark hardening configurations and audit trail procedures."
            )
            risk_assessment.append(
                f"- *{cat}*: Misconfigured system baselines exposing endpoints to known attack vectors."
            )

    citations_str = (
        "\n".join(citations_list) if citations_list else "- *No updates cited.*"
    )

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = (
        "\n".join(migration_steps)
        if migration_steps
        else "- *No migration steps identified.*"
    )
    impl_checklist_str = (
        "\n".join(impl_checklist)
        if impl_checklist
        else "- [ ] Perform generic verification of standards compliance."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Perform security and standards regression test suites."
    )
    doc_checklist_str = (
        "\n".join(doc_checklist)
        if doc_checklist
        else "- [ ] Update technical standards documentation."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the application and infrastructure into complete alignment with the latest revisions of monitored technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).

## 2. Background
Technical standards are continuously updated to reflect evolving cybersecurity threats, privacy regulations, AI governance expectations, and quality management principles. Proactively addressing repository gaps ensures continuous compliance and passes rigorous third-party audits.

## 3. Regulatory change
- **Information Security & Privacy (ISO 27001, ISO 27701, ISO 31000, ISO 9001)**: Mandates robust ISMS/PIMS governance, risk treatment procedures, quality assurance loops, and continuous monitoring.
- **AI Governance & Risk (ISO 42001, NIST AI RMF)**: Requires formal AI Management Systems (AIMS), risk mapping (Govern, Map, Measure, Manage), prompt/response moderation, and traceability.
- **Cybersecurity & Application Security (OWASP, NIST CSF, CIS Benchmarks, IEC standards)**: Enforces OWASP MASVS/Top 10 controls, NIST CSF 2.0 Govern functions, CIS system hardening, and IEC electrotechnical safety baselines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit failure, security vulnerability exposure, or regulatory non-compliance if technical standards gaps remain unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed standard compliance modifications are fully backward-compatible. API signatures, core business logic, and user data models remain intact while operational security and governance controls are strengthened.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated static compliance checkers locally.

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with verified compliance evidence.

## 12. Compliance impact
- **Audit Readiness**: Ensures readiness for ISO 27001/27701/42001/9001 certification audits.
- **Security Posture**: Strengthens resistance against OWASP Top 10 vulnerabilities and aligns with CIS Benchmarks.
- **AI Safety & Governance**: Satisfies NIST AI RMF and ISO 42001 requirements for trustworthy AI systems.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced security filters and validation checks may reject malformed or unauthorized requests.

## 14. Review checklist
- [ ] Code and documentation diff is 100% free of emojis or graphical symbols.
- [ ] All cited sources satisfy the strict Source Trust Hierarchy.
- [ ] Security keys, credentials, and sensitive tokens are strictly protected.

## 15. Approver recommendations
Verify that all technical standard controls have been tested and verified against official documentation. Confirm that test suites for OWASP, NIST, and ISO controls execute cleanly in CI before merging.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across the 10 monitored technical standards.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        priority, is_verified = classify_source_and_verify(u, updates)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    seen_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u, updates)

        if priority in (4, 5) and not is_verified:
            lines.append(
                f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source."
            )
            lines.append("")
            continue

        if cat in seen_categories:
            continue
        seen_categories.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority technical standard compliance area."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update ISMS access policies and information security controls."
            )
            lines.append(
                "- [ ] **Task 2**: Perform threat intelligence integration audit."
            )
            lines.append(
                "- [ ] **Testing Update**: Run access control and credential exposure automated test suite."
            )
            lines.append(
                "- [ ] **Documentation Update**: Record ISMS audit evidence in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Map PII controller and processor roles."
            )
            lines.append(
                "- [ ] **Task 2**: Update Privacy Impact Assessment (PIA) records."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute data subject erasure and PII export integration tests."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document PIMS data handling policies."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish AI Management System (AIMS) governance controls."
            )
            lines.append(
                "- [ ] **Task 2**: Implement prompt and response safety filters."
            )
            lines.append(
                "- [ ] **Testing Update**: Run automated AI safety regression and toxicity tests."
            )
            lines.append(
                "- [ ] **Documentation Update**: Maintain AI model cards and ISO 42001 risk documentation."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Update enterprise risk assessment matrix definitions."
            )
            lines.append(
                "- [ ] **Task 2**: Integrate risk treatment plans into release pipelines."
            )
            lines.append(
                "- [ ] **Testing Update**: Verify continuous risk scoring during CI checks."
            )
            lines.append(
                "- [ ] **Documentation Update**: Publish updated risk management guidelines."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Enforce mandatory QMS code review and static analysis gates."
            )
            lines.append(
                "- [ ] **Task 2**: Establish continuous quality verification feedback loops."
            )
            lines.append(
                "- [ ] **Testing Update**: Validate CI test coverage metrics and release gates."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document quality assurance checklists."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Audit component dependency trees for electrotechnical safety."
            )
            lines.append(
                "- [ ] **Task 2**: Implement cryptographic software integrity verification."
            )
            lines.append(
                "- [ ] **Testing Update**: Run component vulnerability SAST scans."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update system security architecture docs per IEC."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Remediate OWASP MASVS and Top 10 vulnerabilities."
            )
            lines.append(
                "- [ ] **Task 2**: Enforce secure token storage and input sanitization."
            )
            lines.append(
                "- [ ] **Testing Update**: Run DAST and OWASP ZAP automated security scans."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update OWASP compliance verification records."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Implement NIST AI RMF Govern, Map, Measure, and Manage functions."
            )
            lines.append(
                "- [ ] **Task 2**: Establish AI risk metric measurement protocols."
            )
            lines.append(
                "- [ ] **Testing Update**: Test AI system robustness and prompt red-teaming resilience."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document NIST AI RMF profile alignment."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity controls with NIST CSF 2.0 functions."
            )
            lines.append(
                "- [ ] **Task 2**: Audit supply chain risk monitoring procedures."
            )
            lines.append(
                "- [ ] **Testing Update**: Validate incident response alerting and logging completeness."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update security architecture docs with CSF mapping."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Harden system, container, and mobile OS configurations."
            )
            lines.append(
                "- [ ] **Task 2**: Implement CIS Critical Security Controls v8.1."
            )
            lines.append(
                "- [ ] **Testing Update**: Run automated CIS hardening benchmark scripts."
            )
            lines.append(
                "- [ ] **Documentation Update**: Record CIS hardening configurations."
            )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(
            f"Technical standards documentation updated successfully at: {output_filepath}"
        )
    except Exception as e:
        print(
            f"Error writing documentation to {output_filepath}: {e}",
            file=sys.stderr,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards Requirements"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live technical standards RSS feeds",
    )
    parser.add_argument(
        "--mock",
        type=str,
        default="inline",
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
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(
            parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml")
        )
        announcements.extend(
            parse_rss_feed("https://owasp.org/feed.xml")
        )
        announcements.extend(
            parse_rss_feed("https://www.cisecurity.org/feed")
        )

    if args.mock or (not args.live and not args.mock) or not announcements:
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

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(
        announcements, keywords_filter
    )

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    classified_updates = sorted(
        classified_updates, key=lambda x: x["category"]
    )

    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(
            u, classified_updates
        )
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(
            u, classified_updates
        )
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    if not args.json:
        print(
            f"Scanning codebase under '{args.dir}' for technical standards signals..."
        )
    scan_results = scan_codebase_for_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
            print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(
            f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr
        )

    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(
                u, classified_updates
            )
            cat = u["category"]
            report_data.append(
                {
                    "track": cat,
                    "title": u["title"],
                    "pubDate": u["pubDate"],
                    "link": u["link"],
                    "priority": priority,
                    "verified": is_verified,
                    "matches": scan_results.get(cat, []),
                }
            )
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
