#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards categories:
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

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management system",
        "isms",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management system",
        "pims",
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
        "risk management principles",
        "risk assessment framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
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
        "masvs",
        "top 10",
        "top ten",
        "asvs",
        "samm",
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
        "nist cybersecurity framework",
        "csf 2.0",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "cis hardening",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO\s*27001",
        r"ISMS",
        r"information_security",
        r"access_control",
        r"security_policy",
    ],
    "ISO 27701": [
        r"ISO\s*27701",
        r"PIMS",
        r"privacy_information",
        r"data_protection_officer",
    ],
    "ISO 42001": [
        r"ISO\s*42001",
        r"AIMS",
        r"ai_governance",
        r"ai_risk",
        r"ai_management",
    ],
    "ISO 31000": [
        r"ISO\s*31000",
        r"risk_management",
        r"risk_register",
        r"risk_assessment",
    ],
    "ISO 9001": [
        r"ISO\s*9001",
        r"QMS",
        r"quality_management",
        r"quality_policy",
    ],
    "IEC standards": [
        r"IEC\s*\d+",
        r"IEC_62443",
        r"IEC_82304",
        r"IEC_62304",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"DependencyCheck",
        r"top_10",
    ],
    "NIST AI RMF": [
        r"NIST\s*AI\s*RMF",
        r"AI_RMF",
        r"NIST_AI_100",
    ],
    "NIST CSF": [
        r"NIST\s*CSF",
        r"CybersecurityFramework",
        r"CSF_2\.0",
    ],
    "CIS Benchmarks": [
        r"CIS\s*Benchmarks",
        r"CIS_Controls",
        r"cis_hardening",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and government sources (ISO, IEC, NIST, OWASP, CIS, European Commission, FTC, CISA, BSI)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Mock announcements covering all 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STANDARDS-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Alignment Guidelines",
        "description": "Updated ISO 27001 Annex A security controls mandate enhanced threat intelligence, cloud services security, and secure coding practices across all organizational systems.",
        "link": "https://www.iso.org/isoiec-27001-information-security.html",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Extension Standards",
        "description": "ISO 27701 guidelines require establishing clear PIMS controls to extend ISO 27001 ISMS for privacy management, handling PII processing roles, and ensuring data subject rights fulfillment.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Certification Framework",
        "description": "ISO 42001 specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organizations.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Principles and Implementation Framework",
        "description": "ISO 31000 provides guidelines on managing risk faced by organizations. Application requires integrating risk assessment into governance and operational workflows.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Standards Verification",
        "description": "ISO 9001 requirements outline structured quality management processes, continuous improvement mechanisms, customer satisfaction tracking, and process validation.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Industrial Cyber Security and Healthcare Software Life Cycle",
        "description": "IEC 62443 and IEC 82304 standards mandate secure-by-design lifecycle controls, patch management verification, and system software integrity testing.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS and Top 10 Security Verification Standard Release",
        "description": "OWASP releases updated MASVS and ASVS benchmarks for mobile and web software verification, mandating threat modeling, dynamic analysis, and supply-chain bill of materials verification.",
        "link": "https://owasp.org/www-project-mobile-application-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-NIST-AIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Implementation Directives",
        "description": "NIST AI RMF outlines functions to Govern, Map, Measure, and Manage AI risks, emphasizing trustworthiness, transparency, explainability, safety, and bias reduction.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Governance Expansion",
        "description": "NIST CSF 2.0 expands cybersecurity outcomes beyond critical infrastructure to all organizations, elevating Governance as a core sixth function alongside Identify, Protect, Detect, Respond, and Recover.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls v8.1 Infrastructure Hardening Guidelines",
        "description": "CIS Controls v8.1 specifies foundational cybersecurity safeguards for operating systems, mobile devices, containers, and cloud environments to prevent unauthorized intrusion.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT",
    },
    {
        "id": "STANDARDS-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Rumor on ISO Certification Deadlines",
        "description": "An unverified personal blog claims ISO 27001 certification requires immediate daily audits of developer desktops or instant revocation.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 PDT",
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
        "ftc.gov",
        "cisa.gov",
        "bsi.bund.de",
        "gov.uk",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open worldwide application security project",
        "center for internet security",
        "official standard",
        "nist",
        "owasp",
        "cis benchmarks",
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
    ]

    priority = 4

    if any(d in link for d in p5_domains) or any(
        kw in combined for kw in p5_keywords
    ):
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
                    other_combined = (
                        f"{other.get('title', '')} {other.get('description', '')} {other.get('link', '')}".lower()
                    )
                    other_words = set(re.findall(r"[a-z]+", other_combined))
                    common_terms = {
                        "iso",
                        "nist",
                        "owasp",
                        "security",
                        "standard",
                        "cis",
                    }
                    overlap = words.intersection(other_words).intersection(
                        common_terms
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 technical standards categories."""
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
        dirs[:] = [
            d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")
        ]

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
            if (
                "monitor-standards" in file
                or "monitor-standards-test" in file
            ):
                continue

            try:
                with open(
                    filepath, "r", encoding="utf-8", errors="ignore"
                ) as f:
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
            headers={
                "User-Agent": "Mozilla/5.0 (TechnicalStandardsMonitor/1.0)"
            },
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
                            "id", "STANDARDS-UPDATE-" + str(hash(title))[:6]
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
    """Generates a draft of a pull request complying with the exact 15 required sections without emojis."""
    citations_list = []
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    doc_checklist = []
    risk_assessment = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
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
                f"- **{cat}**: Align information security controls with Annex A rules, covering access control, threat intelligence, and secure coding."
            )
            impl_checklist.append(
                "- [ ] Update access control and cryptography policies to align with ISO 27001 Annex A."
            )
            testing_checklist.append(
                "- [ ] Execute automated static code analysis and dependency vulnerability scans for ISO 27001 compliance."
            )
            doc_checklist.append(
                "- [ ] Document ISMS policies and Annex A control mappings in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-alignment leads to audit findings and loss of ISMS certification."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS framework with Privacy Information Management System (PIMS) controls for PII processing."
            )
            impl_checklist.append(
                "- [ ] Map PII collection, storage, and erasure procedures under ISO 27701 controls."
            )
            testing_checklist.append(
                "- [ ] Test PII data flow isolation and automatic data retention purge scripts."
            )
            doc_checklist.append(
                "- [ ] Update PIMS documentation and data subject rights procedures."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate PII management leading to regulatory privacy enforcement and PIMS failure."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) controls covering AI risk, transparency, and data lineage."
            )
            impl_checklist.append(
                "- [ ] Integrate AI model cards, training data lineage checks, and algorithmic impact assessments."
            )
            testing_checklist.append(
                "- [ ] Execute AI model validation tests for bias, robustness, and output safety boundaries."
            )
            doc_checklist.append(
                "- [ ] Publish AI management system (AIMS) governance statement."
            )
            risk_assessment.append(
                f"- *{cat}*: Ungoverned AI deployment resulting in bias, safety breaches, and AI Act non-compliance."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate structured risk management framework into software development and release lifecycles."
            )
            impl_checklist.append(
                "- [ ] Establish risk register and automated risk scoring across repository components."
            )
            testing_checklist.append(
                "- [ ] Verify risk assessment coverage for all new architectural features."
            )
            doc_checklist.append(
                "- [ ] Maintain updated risk register in repository documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational and security risks entering production without review."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize software quality management processes, automated regression testing, and code review gates."
            )
            impl_checklist.append(
                "- [ ] Enforce automated CI/CD quality gates, code reviews, and test coverage thresholds."
            )
            testing_checklist.append(
                "- [ ] Run end-to-end regression test suites and track defect resolution rates."
            )
            doc_checklist.append(
                "- [ ] Document software quality management system (QMS) release standards."
            )
            risk_assessment.append(
                f"- *{cat}*: Inconsistent software quality leading to customer dissatisfaction and software defects."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Apply IEC secure-by-design lifecycle controls and software integrity verification."
            )
            impl_checklist.append(
                "- [ ] Integrate SBOM generation and binary integrity checks into build pipelines."
            )
            testing_checklist.append(
                "- [ ] Validate patch management routines and component integrity verification."
            )
            doc_checklist.append(
                "- [ ] Update software lifecycle documentation in accordance with IEC standards."
            )
            risk_assessment.append(
                f"- *{cat}*: Security vulnerabilities in critical software components violating IEC safety standards."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Address OWASP MASVS and ASVS security verification requirements across web and mobile targets."
            )
            impl_checklist.append(
                "- [ ] Verify OWASP MASVS secure storage, network communication, and key management controls."
            )
            testing_checklist.append(
                "- [ ] Perform automated OWASP Dependency-Check and dynamic security testing."
            )
            doc_checklist.append(
                "- [ ] Document OWASP MASVS/ASVS verification results and control coverage."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to OWASP Top 10 vulnerabilities (e.g. injection, broken auth, insecure storage)."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Execute NIST AI RMF core functions (Govern, Map, Measure, Manage) across AI/ML workflows."
            )
            impl_checklist.append(
                "- [ ] Implement AI model documentation, prompt sanitization, and output verification controls."
            )
            testing_checklist.append(
                "- [ ] Conduct red-teaming and adversarial robustness testing on AI components."
            )
            doc_checklist.append(
                "- [ ] Document NIST AI RMF map and measure metrics for deployed models."
            )
            risk_assessment.append(
                f"- *{cat}*: AI safety failures, prompt injection, or hallucination-driven compliance violations."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity outcomes with NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append(
                "- [ ] Map repository controls to NIST CSF 2.0 subcategories."
            )
            testing_checklist.append(
                "- [ ] Run continuous security auditing scripts and incident response simulations."
            )
            doc_checklist.append(
                "- [ ] Maintain NIST CSF 2.0 alignment matrix in repository documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Security posture gaps failing cybersecurity framework benchmarks."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce CIS Controls v8.1 and hardening guidelines for operating systems, containers, and application configurations."
            )
            impl_checklist.append(
                "- [ ] Harden container files, configuration parameters, and environment settings per CIS Benchmarks."
            )
            testing_checklist.append(
                "- [ ] Execute automated CIS Benchmark compliance scanning scripts."
            )
            doc_checklist.append(
                "- [ ] Document CIS hardening standards and exception log."
            )
            risk_assessment.append(
                f"- *{cat}*: Unhardened systems vulnerable to automated exploitation and intrusion."
            )

    citations_str = (
        "\n".join(citations_list)
        if citations_list
        else "- *No updates cited.*"
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
        else "- [ ] Perform generic verification of technical standards."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Run standard test suites."
    )
    doc_checklist_str = (
        "\n".join(doc_checklist)
        if doc_checklist
        else "- [ ] Update standards policy documentation."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces comprehensive updates across codebase configuration, security controls, and governance documentation to align with key technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards established by ISO, IEC, NIST, OWASP, and CIS serve as the global benchmark for information security, privacy, quality, risk management, AI governance, and system hardening. Maintaining compliance ensures system resilience, regulatory readiness, and auditor approval.

## 3. Regulatory change
- **ISO Standards**: Updated ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk Management (ISO 31000), and Quality Management (ISO 9001) controls.
- **IEC Standards**: Enhanced industrial and healthcare software life cycle security standards (IEC 62443 / IEC 82304).
- **OWASP**: Aligned mobile and web application security verification standards (MASVS / ASVS).
- **NIST Frameworks**: Implementation of NIST AI RMF 1.0 core functions and NIST CSF 2.0 Governance function.
- **CIS Benchmarks**: CIS Controls v8.1 hardening safeguards.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Moderate-to-high risk of security gaps and audit failure if standards are not continually monitored and verified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes preserve backward compatibility. System controls, configuration hardening, and governance workflows operate gracefully without breaking existing runtime APIs or user workflows.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated repository compliance guards locally.

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
{doc_checklist_str}

## 12. Compliance impact
- **Audit Preparedness**: Verifies repository compliance against international standards and frameworks.
- **Security Posture**: Strengthens system hardening, vulnerability management, and threat response.
- **AI Governance**: Ensures AI/ML features operate within ethical, transparent, and compliant boundaries.

## 13. Breaking changes
- No functional breaking changes are introduced; security hardening measures elevate baseline requirements.

## 14. Review checklist
- [ ] Code and documentation diffs are 100% emoji-free.
- [ ] All cited sources satisfy Priority 1-3 trust hierarchy rules.
- [ ] Implementation and testing checklists cover all affected technical standards.

## 15. Approver recommendations
Verify that automated security scanners pass without high-severity findings, confirm the risk register is updated, and ensure that AI governance controls are verified before merging.
"""
    return pr_template


SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Re-run the monitor with `--live` against the real feeds before treating anything here",
    "> as an actual requirement.",
    "",
]


def update_documentation_report(
    updates, output_filepath, is_simulated=False
):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Compliance Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across technical standards.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ])

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

    lines.append(
        "## Automated Migration Recommendations, Implementation Tasks & Testing Updates"
    )
    lines.append("")

    processed_task_categories = set()
    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        task_key = (cat, is_verified)
        if task_key in processed_task_categories:
            continue
        processed_task_categories.add(task_key)

        if priority in (4, 5) and not is_verified:
            lines.append(
                f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source."
            )
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority technical standard compliance area."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update Annex A information security control matrix."
            )
            lines.append(
                "- [ ] **Task 2**: Verify access control policies and secure coding guidelines."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute automated dependency vulnerability and static analysis scans."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Configure Privacy Information Management System (PIMS) controls."
            )
            lines.append(
                "- [ ] **Task 2**: Audit PII processing activities and data subject request workflows."
            )
            lines.append(
                "- [ ] **Testing Update**: Validate PII data isolation and automated deletion routines."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Implement Artificial Intelligence Management System (AIMS) governance."
            )
            lines.append(
                "- [ ] **Task 2**: Create AI risk assessment and algorithmic transparency cards."
            )
            lines.append(
                "- [ ] **Testing Update**: Perform model bias, robustness, and output safety tests."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Maintain updated repository risk register."
            )
            lines.append(
                "- [ ] **Task 2**: Conduct risk treatment evaluation for system components."
            )
            lines.append(
                "- [ ] **Testing Update**: Assess risk scoring coverage for all new feature additions."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Standardize software quality management system (QMS) workflows."
            )
            lines.append(
                "- [ ] **Task 2**: Ensure continuous improvement metrics and PR review quality gates."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute full automated regression test suite."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Apply IEC secure software lifecycle standards."
            )
            lines.append(
                "- [ ] **Task 2**: Generate Software Bill of Materials (SBOM) for builds."
            )
            lines.append(
                "- [ ] **Testing Update**: Test patch management and binary integrity verification."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Verify OWASP MASVS and ASVS control coverage."
            )
            lines.append(
                "- [ ] **Task 2**: Remediate identified web and mobile vulnerabilities."
            )
            lines.append(
                "- [ ] **Testing Update**: Run OWASP Dependency-Check and dynamic security scans."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Execute NIST AI RMF core functions (Govern, Map, Measure, Manage)."
            )
            lines.append(
                "- [ ] **Task 2**: Implement prompt safety and output sanitization filters."
            )
            lines.append(
                "- [ ] **Testing Update**: Perform adversarial red-teaming and prompt injection tests."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Map repository security controls to NIST CSF 2.0 subcategories."
            )
            lines.append(
                "- [ ] **Task 2**: Implement Governance function policies across security operations."
            )
            lines.append(
                "- [ ] **Testing Update**: Run continuous security auditing and incident response drills."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Apply CIS Controls v8.1 hardening configurations."
            )
            lines.append(
                "- [ ] **Task 2**: Review container, server, and application environment hardening."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute automated CIS Benchmark compliance checks."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify that all criteria for {cat} are checked and handled."
            )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(
            f"Standards documentation report updated successfully at: {output_filepath}"
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
        default=None,
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

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
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
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(
        f"Monitored and classified {len(classified_updates)} standards updates ({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(
        f"Scanning codebase under '{args.dir}' for standards integration signals..."
    )
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(
        classified_updates, args.output_docs, is_simulated=used_mock
    )

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

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
