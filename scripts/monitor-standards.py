#!/usr/bin/env python3
"""
Monitors changes to 10 key technical standards categories:
- ISO 27001 (Information Security Management System)
- ISO 27701 (Privacy Information Management System)
- ISO 42001 (Artificial Intelligence Management System)
- ISO 31000 (Risk Management Guidelines)
- ISO 9001 (Quality Management System)
- IEC standards (e.g., IEC 62443, IEC 82304, IEC 62304)
- OWASP (MASVS, ASVS, Top 10, LLM Top 10)
- NIST AI RMF (AI Risk Management Framework)
- NIST CSF (Cybersecurity Framework 2.0)
- CIS Benchmarks (Center for Internet Security Benchmarks)

When standards change, this script:
1. Identifies repository gaps (code, policy, and test coverage)
2. Generates implementation tasks
3. Generates documentation updates (written to docs/STANDARDS-POLICY-MIGRATION.md)
4. Generates testing updates
5. Drafts a 15-section compliance Pull Request proposal (written to docs/STANDARDS_COMPLIANCE_PR_DRAFT.md)
6. Enforces strict source trust hierarchy validation (Priority 1-5)
"""

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

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "Official SDOs / Authorities (ISO, IEC, NIST, OWASP, CIS, ENISA, EDPB, FTC, CISA, European Commission)",
    "Priority 2": "Reputable News / Publishers (Reuters, AP, Bloomberg, IEEE Spectrum)",
    "Priority 3": "Academic Papers & Peer-Reviewed Studies",
    "Priority 4": "Industry Blogs & Vendor Whitepapers",
    "Priority 5": "Social Media, Forums & AI-generated Summaries (LinkedIn, Reddit, Twitter, ChatGPT summaries)",
}

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management",
        "pim controller",
        "pim processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai management system",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment criteria",
        "risk treatment plan",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "continual improvement",
        "quality policy",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "iec/tr 60601",
        "industrial automation security",
        "health software lifecycle",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "asvs",
        "owasp top 10",
        "owasp llm",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "govern map measure manage",
        "nist ai 100-1",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "govern identify protect detect respond recover",
        "nist csf 2.0",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "cis hardeners",
        "cis level 1",
        "cis level 2",
    ],
}

# Codebase signals (regex patterns) to find files affected by each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"asset_management",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"data_protection_officer",
        r"pii",
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
        r"risk_matrix",
        r"risk_assessment",
        r"risk_register",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_policy",
        r"audit_log",
    ],
    "IEC standards": [
        r"IEC62443",
        r"IEC82304",
        r"IEC62304",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"MSTG",
        r"top_10",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"AI_RMF",
        r"GovernMapMeasureManage",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"IdentifyProtectDetectRespondRecover",
        r"CSF_2_0",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Controls",
        r"CIS_Level",
    ],
}

# Comprehensive mock announcements for all 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Controls Alignment Update",
        "description": "ISO/IEC 27001 Annex A controls mandate automated threat intelligence integration, secure coding controls, and cloud service data protection audits for all production systems.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 specifies controls for PIMS controllers and processors, requiring mandatory consent logging, PII inventory mapping, and automated data subject request (DSR) workflows.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Certification Standards",
        "description": "ISO/IEC 42001 sets requirements for AI governance, model lineage documentation, bias mitigation, and continuous algorithmic risk monitoring across AI lifecycle stages.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Update",
        "description": "ISO 31000 guidelines require formalized quantitative risk assessment criteria, clear risk appetite thresholds, and integrated risk registers across all technical operations.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Revisions",
        "description": "ISO 9001 QMS revisions emphasize process-driven software release quality, mandatory root-cause analysis for regression bugs, and formalized customer feedback integration.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 & IEC 82304 Cybersecurity for Connected Software and Devices",
        "description": "IEC standards mandate secure software lifecycle practices, secure boot verification, threat modeling for embedded software components, and vulnerability disclosure programs.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 and OWASP Top 10 for LLM Update",
        "description": "OWASP releases updated Mobile Application Security Verification Standard (MASVS v2.1) and Top 10 for LLMs, requiring strict input validation, prompt injection defense, and secure hardware key storage.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Profile Guidance",
        "description": "NIST AI RMF guidelines require implementation of the GOVERN, MAP, MEASURE, and MANAGE functions with documented AI model cards, red-teaming benchmarks, and safety guardrails.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) GOVERN Function Enforcement",
        "description": "NIST CSF 2.0 expands coverage to all organizational technology systems, adding GOVERN as a primary core function alongside Identify, Protect, Detect, Respond, and Recover.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks for Mobile OS and Server Hardening",
        "description": "CIS Benchmarks require Level 1 and Level 2 security profile hardening for operating systems, disabling legacy ciphers, enforcing secure permissions, and enabling automated configuration compliance checks.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 12:00:00 GMT",
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
        "iso",
        "iec",
        "nist",
        "owasp",
        "cis benchmark",
        "european commission",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
        "sdo",
        "official standard",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com", "ieee.org"]
    p2_keywords = ["reuters", "associated press", "bloomberg", "ieee spectrum"]

    p3_domains = ["arxiv.org", "ssrn.com", "acm.org", "ieee.org"]
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
                        "iec",
                        "standard",
                    }
                    overlap = words.intersection(other_words).intersection(
                        common_terms
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans codebase for files matching signals for each of the 10 technical standards categories."""
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
                    ".sh",
                    ".md",
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
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (TechnicalStandardsComplianceMonitor/1.0)"
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
    """Classifies announcements into the 10 categories, evaluating source trust."""
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

        priority, is_verified = classify_source_and_verify(ann, announcements)

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
                        "priority": priority,
                        "is_verified": is_verified,
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a 15-section Pull Request draft for technical standards updates."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_checklist = []

    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        p_str = f"Priority {u['priority']}" + (
            " (Verified)" if u["is_verified"] else " (Unverified)"
        )
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Source: {p_str}, Date: {u['pubDate']})"
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
                f"- **{cat}**: Align information security policies and Annex A controls with ISO/IEC 27001:2022 standards."
            )
            impl_checklist.append(
                "- [ ] Update information security management policy and access control registers."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance risks audit failure and potential data breaches due to outdated controls."
            )
            testing_checklist.append(
                "- [ ] Verify access control rule evaluation and log retention mechanisms."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to PIMS, implementing PII mapping and consent verification workflows."
            )
            impl_checklist.append(
                "- [ ] Integrate automated PII identification and consent audit trail logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate PII management leading to regulatory fines under global privacy laws."
            )
            testing_checklist.append(
                "- [ ] Test Data Subject Right (DSR) export and erasure integration handlers."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) controls for model lineage and continuous monitoring."
            )
            impl_checklist.append(
                "- [ ] Deploy model card tracking, bias auditing, and continuous AI monitoring."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI system drift, algorithmic bias, and non-compliance with AI regulations."
            )
            testing_checklist.append(
                "- [ ] Execute automated model evaluation benchmarks and adversarial safety testing."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Formulate quantitative risk assessment criteria and maintain an active risk register."
            )
            impl_checklist.append(
                "- [ ] Update organizational risk matrix and automated risk scoring criteria."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational risks and lack of documented risk treatment procedures."
            )
            testing_checklist.append(
                "- [ ] Validate risk scoring calculations against defined operational thresholds."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Implement QMS process quality controls, automated release validation, and defect root-cause tracking."
            )
            impl_checklist.append(
                "- [ ] Establish automated CI/CD quality gates and defect metrics reporting."
            )
            risk_assessment.append(
                f"- *{cat}*: Quality regressions in production systems impacting service availability."
            )
            testing_checklist.append(
                "- [ ] Run end-to-end regression test suites on release candidates."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62443 / IEC 82304 software lifecycle security requirements and secure component design."
            )
            impl_checklist.append(
                "- [ ] Update software bill of materials (SBOM) and component threat models."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerabilities in third-party software components exposing system boundaries."
            )
            testing_checklist.append(
                "- [ ] Perform automated dependency vulnerability scanning and secure boot checks."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Apply OWASP MASVS v2.1 and ASVS standards, enforcing secure storage, transport security, and LLM prompt defense."
            )
            impl_checklist.append(
                "- [ ] Implement OWASP MASVS storage and network controls across client builds."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerability to OWASP Top 10 exploits, prompt injection, and credential theft."
            )
            testing_checklist.append(
                "- [ ] Run static (SAST) and dynamic (DAST) security scans against OWASP MASVS rules."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Apply NIST AI RMF core functions (GOVERN, MAP, MEASURE, MANAGE) across AI components."
            )
            impl_checklist.append(
                "- [ ] Document AI system risk profiles and implement red-teaming safeguards."
            )
            risk_assessment.append(
                f"- *{cat}*: High risk of AI hallucination, safety failures, and ethical non-compliance."
            )
            testing_checklist.append(
                "- [ ] Execute red-teaming safety evaluations on LLM prompt interfaces."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Transition to NIST CSF 2.0 structure, incorporating explicit GOVERN controls alongside core functions."
            )
            impl_checklist.append(
                "- [ ] Map organizational security controls to NIST CSF 2.0 subcategories."
            )
            risk_assessment.append(
                f"- *{cat}*: Security gaps in incident response, continuous detection, or governance frameworks."
            )
            testing_checklist.append(
                "- [ ] Simulate incident response playbooks and verify detection alert triggers."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Harden system build configurations in accordance with CIS Level 1 and Level 2 profiles."
            )
            impl_checklist.append(
                "- [ ] Apply CIS Benchmark hardening parameters to application configurations."
            )
            risk_assessment.append(
                f"- *{cat}*: Insecure default configurations allowing privilege escalation or information leakage."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance audit scripts against build artifacts."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category signals were automatically detected. (Perform manual review of technical standards configurations).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)
    testing_checklist_str = "\n".join(testing_checklist)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into complete alignment with updated technical standards across 10 monitored frameworks: ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards are continuously revised by global standards development organizations (SDOs) like ISO, IEC, NIST, OWASP, and CIS. Maintaining active compliance ensures operational resilience, security posture, privacy governance, and regulatory audit readiness.

## 3. Regulatory change
- **Technical Standards Evolution**: Alignment with modern ISO/IEC frameworks, NIST CSF 2.0, NIST AI RMF 1.0, and OWASP MASVS v2.1 guidelines.
- **Source Trust Verification**: All updates are validated against Priority 1-3 trusted sources in accordance with organizational compliance requirements.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit failure, security vulnerabilities, or operational degradation if technical standards requirements are neglected.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards migrations are backward-compatible and do not disrupt existing application interfaces or runtime APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run technical standards verification scripts locally.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Confirm all CI/CD compliance validation pipelines pass cleanly.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed checklists and gap analysis.
- [ ] Update internal architecture diagrams and technical control documentation.

## 12. Compliance impact
- **Audit Readiness**: Ensures complete alignment with ISO, NIST, OWASP, and CIS audit frameworks.
- **Security & Resilience**: Strengthens application security posture against modern threat vectors.

## 13. Breaking changes
- No breaking API changes are introduced. Enhanced security controls may enforce stricter validation on incoming inputs.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] All technical controls are mapped to verified Priority 1-3 official sources.
- [ ] All implementation and testing tasks have been executed and verified.

## 15. Approver recommendations
Verify that all technical control mappings in `docs/STANDARDS-POLICY-MIGRATION.md` match the required SDO specification releases before merging.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Writes or updates the documentation report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Requirements Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across 10 technical standards categories.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        status_str = f"Priority {u['priority']} " + (
            "(Verified)" if u["is_verified"] else "(Unverified)"
        )
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Source Trust Status**: {status_str}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Repository Gap Analysis & Implementation Tasks")
    lines.append("")

    processed_categories = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority. Technical standards update mandates action."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Audit ISMS policies against ISO/IEC 27001:2022 Annex A controls."
            )
            lines.append(
                "- [ ] **Task 2**: Verify access control and threat intelligence integration."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Update PIMS controller/processor data flow maps."
            )
            lines.append(
                "- [ ] **Task 2**: Test automated consent logging and PII export/erasure workflows."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Document AI model cards and algorithmic risk governance."
            )
            lines.append(
                "- [ ] **Task 2**: Implement continuous bias and safety evaluation pipelines."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Re-evaluate risk appetite thresholds and update risk register."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Review software quality metrics and CI/CD quality gates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Perform threat modeling for connected software components (IEC 62443 / 82304)."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Perform static and dynamic security audits against OWASP MASVS v2.1."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Map AI components against GOVERN, MAP, MEASURE, and MANAGE functions."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity controls with NIST CSF 2.0 subcategories."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Execute CIS Benchmark automated compliance scans on build outputs."
            )
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
        description="Monitor Technical Standards Changes (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS)"
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
        help="Filepath to save drafted PR",
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live Technical Standards feeds...")
        feeds = [
            "https://www.iso.org/rss/xnews.xml",
            "https://www.nist.gov/news-events/news/rss.xml",
        ]
        for feed in feeds:
            announcements.extend(parse_rss_feed(feed))

    if args.mock or (not args.live and not args.mock) or not announcements:
        print("Using comprehensive mock Technical Standards updates...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default dataset.",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    valid_updates = [u for u in classified_updates if u["is_verified"]]
    blocked_count = len(classified_updates) - len(valid_updates)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        p_str = f"Priority {u['priority']}" + (
            " (Verified)" if u["is_verified"] else " (Unverified)"
        )
        print(f" {idx}. [{u['category']}] {u['title']} - {p_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    if not valid_updates:
        print(
            "All updates were unverified Priority 4/5 sources. PR generation blocked."
        )
        sys.exit(0)

    pr_draft = generate_pull_request_draft(valid_updates, scan_results)

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
