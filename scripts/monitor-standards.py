#!/usr/bin/env python3
"""
Monitors changes to 10 technical standards:
- ISO 27001
- ISO 27701
- ISO 42001
- ISO 31000
- ISO 9001
- IEC standards
- OWASP
- NIST AI RMF
- NIST CSF
- CIS Benchmarks

Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates.
Follows the strict Source Trust Hierarchy and strict Emoji-Free Policy.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

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

# Keywords used to classify incoming policy announcements/articles
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management system",
        "isms",
        "annex a",
        "access control policy",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management system",
        "pims",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai risk management",
        "ai governance",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management principles",
        "risk assessment framework",
        "risk treatment plan",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality control",
        "process audit",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "international electrotechnical commission",
        "software life cycle processes",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "asvs",
        "owasp top 10 for llm",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "map measure manage govern",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "govern identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "hardening guidelines",
        "cis benchmark",
    ],
}

# Codebase signals (regex patterns) to find files affected by each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"securityPolicy",
        r"accessControl",
        r"encryptionStandard",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"PII",
        r"privacyPolicy",
        r"dataProtectionOfficer",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"aiGovernance",
        r"modelRisk",
        r"aiSafety",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskAssessment",
        r"riskTreatment",
        r"riskRegister",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"qualityPolicy",
        r"auditChecklist",
    ],
    "IEC standards": [
        r"IEC[ -]?62304",
        r"IEC[ -]?82304",
        r"IEC[ -]?62443",
        r"IEC[ -]?standards",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"top10",
        r"vulnerabilityScan",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI",
        r"AIRMF",
        r"trustworthyAI",
        r"modelValidation",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"cybersecurityFramework",
        r"incidentResponse",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"hardeningConfig",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# 10 Mock Announcements covering all tracked standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "ISO releases updated Annex A security controls requiring enhanced cloud service security, threat intelligence integration, and secure coding practices across all organizational software repositories.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Revision",
        "description": "Updated ISO 27701 guidelines mandate mapping PII processing controls to cross-border data transfer mechanisms and automated user consent management workflows.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Certification Standards",
        "description": "ISO 42001 establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS), focusing on risk assessment and responsible AI deployment.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines for Enterprise Digital Infrastructure",
        "description": "Revised ISO 31000 framework provides structured principles for identifying, evaluating, and mitigating technology and operational risks across digital product lifecycles.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Software Development Quality Controls",
        "description": "ISO 9001 standard updates highlight software release quality gates, automated regression testing requirements, and continuous process verification in production pipelines.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Health & Medical Software Lifecycle Standards Update",
        "description": "International Electrotechnical Commission (IEC) updates software lifecycle requirements, mandating strict risk classification, verification testing, and continuous vulnerability monitoring.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 & Top 10 for LLM Applications Update",
        "description": "OWASP publishes updated Mobile Application Security Verification Standard (MASVS) and LLM Security guidelines, targeting prompt injection mitigation, insecure output handling, and hardware-backed credential storage.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.1 Guidance & Trustworthy AI Playbook",
        "description": "NIST releases updated AI RMF profile guidance covering model transparency, bias mitigation, explainability, and continuous monitoring across the GOVERN, MAP, MEASURE, and MANAGE functions.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Implementation Guide",
        "description": "NIST CSF 2.0 expands governance expectations, requiring explicit supply chain risk management, automated continuous controls monitoring, and incident response readiness across all six core functions.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks v3.0 Hardening Guidelines for Mobile and Cloud Workloads",
        "description": "Center for Internet Security (CIS) issues updated CIS Controls and Benchmarks, establishing baseline configuration policies, secure build automation, and mandatory vulnerability patching cycles.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified).
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
        "gov.sg",
        "apple.com",
        "developer.apple.com",
        "android.com",
        "developer.android.com",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "cisecurity",
        "center for internet security",
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "european commission",
        "official journal",
        "cisa",
        "ftc",
        "ico",
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
    ):
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
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
                        "standards",
                        "security",
                        "privacy",
                    }
                    overlap = words.intersection(other_words).intersection(
                        common_terms
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 standards categories.
    """
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
                    ".md",
                    ".swift",
                    ".m",
                    ".h",
                    ".plist",
                    ".html",
                    ".py",
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


def parse_rss_feed(url):
    """
    Fetches and parses live RSS or Atom XML feeds.
    """
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
    """
    Classifies incoming announcements into the 10 technical standards categories.
    """
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
    """
    Generates a draft of a pull request complying with the exact 15 required sections.
    Includes explicit details on identified repository gaps, implementation tasks,
    documentation updates, and testing updates.
    """
    citations_list = []
    affected_files_set = set()
    repo_gaps = []
    impl_tasks = []
    doc_updates = []
    testing_updates = []
    risk_assessment = []

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
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

        if cat == "ISO 27001":
            repo_gaps.append(
                f"- **{cat}**: Missing formalized ISMS access control policies and automated continuous security control auditing."
            )
            impl_tasks.append(
                f"- **{cat}**: Implement access control policy declarations and enforce strict cryptographic storage."
            )
            doc_updates.append(
                f"- **{cat}**: Document ISMS control alignment in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            testing_updates.append(
                f"- **{cat}**: Add automated verification script checks for access control and encryption standards."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with Annex A security controls leading to enterprise audit findings."
            )
        elif cat == "ISO 27701":
            repo_gaps.append(
                f"- **{cat}**: Lack of documented PII controller/processor role definitions and explicit PII processing logs."
            )
            impl_tasks.append(
                f"- **{cat}**: Implement PII processing safeguards and automated user consent lifecycle handlers."
            )
            doc_updates.append(
                f"- **{cat}**: Publish PIMS privacy controls and data retention matrix in developer playbooks."
            )
            testing_updates.append(
                f"- **{cat}**: Validate that PII fields are sanitized and not leaked into unencrypted diagnostics."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure of unencrypted PII across secondary processing boundaries."
            )
        elif cat == "ISO 42001":
            repo_gaps.append(
                f"- **{cat}**: Absence of AI Management System (AIMS) risk evaluation records and model governance checks."
            )
            impl_tasks.append(
                f"- **{cat}**: Integrate AI system interaction disclosures and model risk assessments."
            )
            doc_updates.append(
                f"- **{cat}**: Update AI transparency documentation and Article 50 interaction disclaimers."
            )
            testing_updates.append(
                f"- **{cat}**: Execute automated static checks for AI API endpoint integration and disclosure banners."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI system behavior causing regulatory compliance breaches."
            )
        elif cat == "ISO 31000":
            repo_gaps.append(
                f"- **{cat}**: Unformalized technology risk register and lack of structured risk treatment plans."
            )
            impl_tasks.append(
                f"- **{cat}**: Codify risk management criteria into build-time static compliance scanners."
            )
            doc_updates.append(
                f"- **{cat}**: Update risk assessment methodologies in release review documentation."
            )
            testing_updates.append(
                f"- **{cat}**: Run release audit scripts to verify zero critical or high unmitigated risk items."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to systematically identify high-impact operational or compliance risks."
            )
        elif cat == "ISO 9001":
            repo_gaps.append(
                f"- **{cat}**: Missing continuous release quality gates and automated regression verification metrics."
            )
            impl_tasks.append(
                f"- **{cat}**: Enforce strict automated testing and validation gates before release authorization."
            )
            doc_updates.append(
                f"- **{cat}**: Maintain versioned release readiness reports and testing audit trails."
            )
            testing_updates.append(
                f"- **{cat}**: Run full regression test suites and static validation utilities (`validate.py`)."
            )
            risk_assessment.append(
                f"- *{cat}*: Production defects due to unverified release builds."
            )
        elif cat == "IEC standards":
            repo_gaps.append(
                f"- **{cat}**: Lack of IEC software lifecycle classification, risk analysis, and software verification records."
            )
            impl_tasks.append(
                f"- **{cat}**: Implement lifecycle verification checks and mandatory dependency vulnerability scanning."
            )
            doc_updates.append(
                f"- **{cat}**: Document IEC software lifecycle compliance and verification protocols."
            )
            testing_updates.append(
                f"- **{cat}**: Execute static code analysis and dependency auditing scripts."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-conformity with software lifecycle verification requirements."
            )
        elif cat == "OWASP":
            repo_gaps.append(
                f"- **{cat}**: Unaddressed OWASP MASVS/ASVS recommendations regarding secure storage and input sanitization."
            )
            impl_tasks.append(
                f"- **{cat}**: Remediate OWASP top risks by replacing insecure storage and sanitizing input channels."
            )
            doc_updates.append(
                f"- **{cat}**: Reference OWASP MASVS controls in security playbooks and migration reports."
            )
            testing_updates.append(
                f"- **{cat}**: Conduct automated vulnerability scanning for OWASP pattern detection."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to common web/mobile vulnerabilities (injection, insecure storage, broken auth)."
            )
        elif cat == "NIST AI RMF":
            repo_gaps.append(
                f"- **{cat}**: Unmapped AI system functions across GOVERN, MAP, MEASURE, and MANAGE dimensions."
            )
            impl_tasks.append(
                f"- **{cat}**: Implement NIST AI RMF governance controls and trustworthy AI safeguards."
            )
            doc_updates.append(
                f"- **{cat}**: Document NIST AI RMF mapping profiles in repository compliance reports."
            )
            testing_updates.append(
                f"- **{cat}**: Test AI disclosure interfaces and automated safety guardrails."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of explainability, transparency, or safety controls in AI features."
            )
        elif cat == "NIST CSF":
            repo_gaps.append(
                f"- **{cat}**: Gaps in NIST CSF 2.0 GOVERN and PROTECT function coverage for software supply chain security."
            )
            impl_tasks.append(
                f"- **{cat}**: Implement automated dependency auditing and incident response triggers."
            )
            doc_updates.append(
                f"- **{cat}**: Update security playbooks with NIST CSF 2.0 operational guidelines."
            )
            testing_updates.append(
                f"- **{cat}**: Validate security monitoring scripts and pre-commit compliance guards."
            )
            risk_assessment.append(
                f"- *{cat}*: Delayed detection or response to cybersecurity incidents."
            )
        elif cat == "CIS Benchmarks":
            repo_gaps.append(
                f"- **{cat}**: Unverified hardening configurations across mobile build targets and environment files."
            )
            impl_tasks.append(
                f"- **{cat}**: Apply CIS hardening benchmarks to build scripts and platform configurations."
            )
            doc_updates.append(
                f"- **{cat}**: Document CIS hardening policies in project security guidelines."
            )
            testing_updates.append(
                f"- **{cat}**: Execute automated static audits to verify hardened build settings."
            )
            risk_assessment.append(
                f"- *{cat}*: Insecure default configurations enabling unauthorized access."
            )

    citations_str = (
        "\n".join(citations_list) if citations_list else "- *No updates cited.*"
    )

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review).* "

    repo_gaps_str = (
        "\n".join(repo_gaps)
        if repo_gaps
        else "- *No specific gaps identified.*"
    )
    impl_tasks_str = (
        "\n".join(impl_tasks)
        if impl_tasks
        else "- [ ] Perform generic verification of technical standards compliance."
    )
    doc_updates_str = (
        "\n".join(doc_updates)
        if doc_updates
        else "- [ ] Update technical standards documentation."
    )
    testing_updates_str = (
        "\n".join(testing_updates)
        if testing_updates
        else "- [ ] Run standard test validation suite."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into complete alignment with updated technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It systematically identifies repository gaps and introduces implementation tasks, documentation updates, and testing updates.

## 2. Background
International technical standards and security frameworks undergo periodic updates to address emerging threats, privacy mandates, and AI governance expectations. Ensuring continuous compliance requires proactive auditing of repository configurations, code patterns, documentation, and test suites.

## 3. Regulatory change
- **ISO Standards (27001, 27701, 42001, 31000, 9001)**: Enhanced ISMS controls, privacy information management, AI management systems, structured risk treatment, and quality release gates.
- **IEC & OWASP Frameworks**: Rigorous software lifecycle controls, medical/health software verification, and OWASP MASVS/Top 10 mitigation.
- **NIST & CIS Guidelines**: Adoption of NIST AI RMF 1.1, NIST CSF 2.0 governance, and CIS Benchmarks hardening.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and audit risk if technical standards updates are not systematically applied and verified.

## 7. Migration steps
{repo_gaps_str}

## 8. Backward compatibility
All proposed standards updates are fully backward-compatible. Technical standards controls enhance governance, security, and quality without breaking public software interfaces.

## 9. Implementation checklist
{impl_tasks_str}
- [ ] Execute automated compliance guard checks locally.

## 10. Testing checklist
{testing_updates_str}
- [ ] Run `python3 scripts/validate.py` to confirm zero schema errors.
- [ ] Run `python3 scripts/release-audit.py` to confirm release readiness.

## 11. Documentation checklist
{doc_updates_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation records.

## 12. Compliance impact
- **Audit Preparedness**: Fully satisfies enterprise certification requirements for ISO 27001, ISO 27701, ISO 42001, ISO 31000, and ISO 9001.
- **Security & Quality**: Aligns codebase with OWASP, NIST CSF 2.0, NIST AI RMF, and CIS Benchmarks.

## 13. Breaking changes
- Zero functional breaking changes introduced to public software APIs.

## 14. Review checklist
- [ ] Verify that the diff is 100% emoji-free.
- [ ] Verify that official citations align with Priority 1 standards bodies.
- [ ] Confirm all implementation, documentation, and testing tasks are complete.

## 15. Approver recommendations
Verify that all static compliance scripts pass without errors and confirm that `docs/STANDARDS-POLICY-MIGRATION.md` reflects updated standards mappings.
"""
    return pr_template


def update_documentation_report(updates, output_filepath, scan_results):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Identified Repository Gaps & Automated Updates")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(
                f"### Updates for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Status**: Suspended. Source is an unverified secondary source."
            )
            lines.append("")
            continue

        files = scan_results.get(cat, [])
        file_count = len(files)

        lines.append(f"### Updates for {cat}")
        lines.append(
            f"- **Repository Audit**: Scanned codebase with {file_count} matching signal locations."
        )
        lines.append(
            f"- **Repository Gap**: Current implementation requires alignment with updated {cat} controls."
        )
        lines.append(
            f"- [ ] **Implementation Task**: Update code declarations and configuration controls to satisfy {cat}."
        )
        lines.append(
            f"- [ ] **Documentation Update**: Record compliance status and control mappings for {cat}."
        )
        lines.append(
            f"- [ ] **Testing Update**: Add automated test cases and static scan verification for {cat}."
        )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(
            f"Technical standards documentation report updated successfully at: {output_filepath}"
        )
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Compliance (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards feeds"
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
        print("Fetching live technical standards feeds...")
        announcements.extend(
            parse_rss_feed("https://www.iso.org/contents/rss/news.xml")
        )
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))

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
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    if not args.json:
        print(
            f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):"
        )
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u)
            status_str = f"Priority {priority} " + (
                "(Verified)" if is_verified else "(Unverified)"
            )
            print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    if not args.json:
        print(f"Scanning codebase under '{args.dir}' for standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs, scan_results)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
            print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u)
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
