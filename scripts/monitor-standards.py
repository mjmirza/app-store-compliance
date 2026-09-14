#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 distinct technical standards categories:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards categories
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

# Keywords used to classify incoming announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management system",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management",
        "privacy information management system",
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
        "qms",
        "quality management system",
        "quality control processes",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 81001",
        "iec 62443",
        "medical device software",
        "industrial automation security",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "owasp top 10",
        "open web application security project",
        "asvs",
        "mobile application security verification standard",
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
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "hardening guidelines",
        "cis benchmark",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"informationSecurityPolicy",
        r"accessControl",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacyImpactAssessment",
        r"dataProtectionOfficer",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"aiModelGovernance",
        r"algorithmicBias",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskRegister",
        r"riskAssessment",
        r"riskMatrix",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"qualityPolicy",
        r"processControl",
    ],
    "IEC standards": [
        r"IEC[ -]?62304",
        r"IEC[ -]?81001",
        r"IEC[ -]?62443",
        r"IECStandards",
        r"softwareLifecycleProcess",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"top10",
        r"sanitization",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"AIRiskManagement",
        r"aiTrustworthiness",
        r"modelAuditing",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"cybersecurityFramework",
        r"incidentResponse",
        r"assetManagement",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"systemHardening",
        r"secureConfiguration",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# 10 Comprehensive Mock Announcements for all 10 categories + 1 unverified fixture
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Revision",
        "description": "Updated Annex A controls mandate automated asset inventory tracking, threat intelligence integration, and secure coding practice enforcement across development pipelines.",
        "link": "https://www.iso.org/isoiec-27001-information-security.html",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "Provides guidelines for establishing, implementing, maintaining, and continually improving a Privacy Information Management System (PIMS) extending ISO 27001 for privacy management.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Guidance",
        "description": "Establishes structural standards for managing AI risk, traceability, model validation, continuous monitoring, and ethical evaluation of machine learning deployments.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Implementation Framework",
        "description": "Provides principles, framework, and process for managing risk systematically across technical operations, software releases, and infrastructure changes.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Software Development Standards",
        "description": "Mandates formalized process controls, continuous feedback loops, peer review records, and software release verification procedures to guarantee consistent delivery quality.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 81001 Health Software and Industrial System Safety Guidance",
        "description": "Defines life cycle requirements for medical device software and health IT infrastructure security, requiring documented risk management, configuration management, and verification.",
        "link": "https://www.iso.org/standard/38421.html",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) 2.0 Update",
        "description": "Updates security requirements across storage, authentication, cryptography, network communications, and platform interaction for mobile and web applications.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "Details core functions (Govern, Map, Measure, Manage) to cultivate trustworthy AI systems, address bias, ensure explainability, and maintain algorithmic safety.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Implementation Guide",
        "description": "Expands the CSF core to six functions: Govern, Identify, Protect, Detect, Respond, and Recover, providing actionable guidance for managing cybersecurity risks.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls Level 1 & Level 2 Hardening Guidelines",
        "description": "Provides consensus-developed security configuration recommendations for operating systems, cloud environments, container runtimes, and mobile platforms.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO Certification Rules",
        "description": "An unverified personal blog claims ISO certification will be immediately revoked for all repos without dark mode. This is an unverified blog post.",
        "link": "https://randomblogsite.com/iso-rumor",
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
        "gov.sg",
    ]
    p1_keywords = [
        "iso standard",
        "iec standard",
        "nist publication",
        "owasp Foundation",
        "center for internet security",
        "european commission",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
        "national institute of standards and technology",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "ieee.org"]
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
                        "security",
                        "risk",
                        "quality",
                    }
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans codebase to identify repository gaps matching the 10 technical standards categories.
    """
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


def clean_text(raw_html):
    """Strips HTML tags and collapses whitespace."""
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return " ".join(cleantext.split())


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
                            "description": clean_text(desc),
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
            migration_steps.append(
                f"- **{cat}**: Audit information security policies and update ISMS Annex A control alignment across development and operational workflows."
            )
            impl_checklist.append(
                "- [ ] Review ISMS Annex A controls for asset management and access control."
            )
            testing_checklist.append(
                "- [ ] Verify access control rule enforcement and log auditing."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-conformity risk in ISMS certification audits and potential information security control gaps."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to PIMS by implementing privacy risk assessment procedures and Data Protection Officer oversight."
            )
            impl_checklist.append(
                "- [ ] Document PIMS privacy controls and data subject rights procedures."
            )
            testing_checklist.append(
                "- [ ] Conduct automated privacy impact assessment test suite."
            )
            risk_assessment.append(
                f"- *{cat}*: Privacy management gaps leading to regulatory non-compliance under regional data protection laws."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance controls for AI models, datasets, and algorithmic transparency."
            )
            impl_checklist.append(
                "- [ ] Deploy AI model governance registry and risk assessment logs."
            )
            testing_checklist.append(
                "- [ ] Run algorithmic bias and model explainability test suites."
            )
            risk_assessment.append(
                f"- *{cat}*: Unregulated AI deployment risks including model drift, bias, and lack of traceability."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate ISO 31000 enterprise risk management principles into continuous integration and deployment reviews."
            )
            impl_checklist.append(
                "- [ ] Establish automated risk matrix evaluation in CI pipelines."
            )
            testing_checklist.append(
                "- [ ] Perform scenario testing for critical risk vectors."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational risks in software releases."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Align software development processes with QMS quality control requirements and peer review checklists."
            )
            impl_checklist.append(
                "- [ ] Mandate peer review records and QMS verification gates."
            )
            testing_checklist.append(
                "- [ ] Validate release candidate compliance against QMS quality benchmarks."
            )
            risk_assessment.append(
                f"- *{cat}*: Inconsistent delivery quality and missing audit records."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Apply IEC 62304 / IEC 81001 software life cycle processes and health IT cybersecurity requirements."
            )
            impl_checklist.append(
                "- [ ] Update software life cycle documentation per IEC 62304 standards."
            )
            testing_checklist.append(
                "- [ ] Execute IEC software verification and validation protocols."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to meet health and industrial safety software compliance gates."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement OWASP MASVS and ASVS security controls across storage, network, authentication, and input sanitization."
            )
            impl_checklist.append(
                "- [ ] Audit codebase against OWASP Top 10 and MASVS control checklists."
            )
            testing_checklist.append(
                "- [ ] Run static application security testing (SAST) and dynamic checks."
            )
            risk_assessment.append(
                f"- *{cat}*: Application vulnerability exposure to common exploit vectors."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Incorporate NIST AI RMF core functions (Govern, Map, Measure, Manage) for AI system trustworthiness."
            )
            impl_checklist.append(
                "- [ ] Document AI RMF Mapping and Measurement metrics."
            )
            testing_checklist.append(
                "- [ ] Test AI system robustness and bias mitigation controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI model behavior and ethical compliance failures."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Update cybersecurity controls to align with NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append(
                "- [ ] Map infrastructure controls to NIST CSF 2.0 subcategories."
            )
            testing_checklist.append(
                "- [ ] Conduct incident response simulation and recovery testing."
            )
            risk_assessment.append(
                f"- *{cat}*: Operational security vulnerabilities and delayed incident response."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce CIS Benchmarks Level 1 and Level 2 system hardening configurations and secure baseline rules."
            )
            impl_checklist.append(
                "- [ ] Apply CIS hardening templates to configuration files."
            )
            testing_checklist.append(
                "- [ ] Execute automated CIS compliance baseline scanner."
            )
            risk_assessment.append(
                f"- *{cat}*: System misconfigurations and unauthorized privilege escalation risks."
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
        else "- [ ] Perform generic verification of technical standards policies."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Perform generic test suite execution for technical standards."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces critical configuration, documentation, implementation, and testing updates to align the codebase with technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards govern operational security, software quality, risk management, privacy information handling, and artificial intelligence trustworthiness. Regular updates ensure our architecture remains resilient, secure, and fully compliant with international framework benchmarks.

## 3. Regulatory change
- **ISO Frameworks**: Enforcement of updated controls for ISO 27001 (ISMS), ISO 27701 (PIMS), ISO 42001 (AIMS), ISO 31000 (Risk Management), and ISO 9001 (QMS).
- **Technical & Industry Standards**: Adherence to IEC software life cycle safety (IEC 62304/81001), OWASP MASVS/ASVS controls, NIST AI RMF trustworthiness, NIST CSF 2.0 governance, and CIS Benchmarks hardening.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational risk if technical standards alignment is omitted during deployment.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards updates introduce modular configuration enforcement, documentation alignment, and testing verification without deprecating existing functional APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guards.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Execute full static analysis and unit test suites to confirm zero regressions.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Ensure architecture diagrams and risk registers reflect technical standards controls.

## 12. Compliance impact
- **Certification Readiness**: Preserves ISO certification audit readiness and NIST compliance standing.
- **Vulnerability Mitigation**: Ensures robust OWASP and CIS Benchmarks hardening against external threat vectors.
- **AI Governance**: Fulfills NIST AI RMF and ISO 42001 requirements for AI model safety.

## 13. Breaking changes
- No breaking software changes are introduced. Strict configuration rules apply to new builds.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official citations are verified Priority 1-3 sources.
- [ ] Verify that all 10 technical standards categories are evaluated.

## 15. Approver recommendations
Verify that the technical standards policy migration document in `docs/STANDARDS-POLICY-MIGRATION.md` is fully updated before merging this pull request.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """
    Writes or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md
    with repository gaps, implementation tasks, and testing updates.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Requirements Update Log",
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

    lines.append("## Identified Repository Gaps")
    lines.append("")
    for cat in CATEGORIES:
        matches = scan_results.get(cat, [])
        lines.append(f"### Repository Gaps for {cat}")
        if matches:
            for m in matches[:5]:
                lines.append(
                    f"- Line {m['line_num']} in `{m['file']}` matched signal pattern `{m['matched_pattern']}`"
                )
        else:
            lines.append(
                f"- No explicit matching signals found in repository files for {cat}. Codebase audit recommended."
            )
        lines.append("")

    lines.append(
        "## Automated Migration Recommendations, Implementation Tasks, and Testing Updates"
    )
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(
                f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source."
            )
            lines.append("")
            continue

        lines.append(f"### Implementation and Testing Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority technical standard area.")

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Implementation Task**: Update ISMS Annex A control alignment across development modules."
            )
            lines.append(
                "- [ ] **Testing Task**: Verify access control and security logging functionality."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Implementation Task**: Implement PIMS privacy risk procedures and data subject rights workflows."
            )
            lines.append(
                "- [ ] **Testing Task**: Run automated privacy impact assessment tests."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Implementation Task**: Deploy Artificial Intelligence Management System (AIMS) governance controls."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute algorithmic bias and model explainability tests."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Implementation Task**: Integrate risk register checks into CI deployment pipelines."
            )
            lines.append(
                "- [ ] **Testing Task**: Test operational risk mitigation scenarios."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Implementation Task**: Formalize software QMS peer review and release signoff checklists."
            )
            lines.append(
                "- [ ] **Testing Task**: Verify release candidate build compliance against QMS quality benchmarks."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Implementation Task**: Apply IEC 62304 / 81001 software life cycle security documentation."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute software verification and validation protocols."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Implementation Task**: Enforce OWASP MASVS/ASVS controls for storage, network, and inputs."
            )
            lines.append(
                "- [ ] **Testing Task**: Run static application security testing (SAST) suite."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Implementation Task**: Incorporate NIST AI RMF core functions (Govern, Map, Measure, Manage)."
            )
            lines.append(
                "- [ ] **Testing Task**: Test AI system robustness and bias controls."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Implementation Task**: Update cybersecurity controls to align with NIST CSF 2.0."
            )
            lines.append(
                "- [ ] **Testing Task**: Perform incident response simulation and recovery tests."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Implementation Task**: Enforce CIS Benchmarks Level 1 and Level 2 system hardening configurations."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute automated CIS hardening baseline scanner."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify technical criteria for {cat} are met."
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
        description="Monitor all Technical Standards Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards RSS feeds"
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
            parse_rss_feed("https://www.nist.gov/news-events/cybersecurity/rss.xml")
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

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, scan_results, args.output_docs)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
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
