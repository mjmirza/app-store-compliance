#!/usr/bin/env python3
"""Technical Standards Compliance Requirements Monitoring Utility.
Tracks changes across 10 key technical standards categories:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001,
IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

Identifies repository gaps, generates implementation tasks, documentation updates,
and testing updates following strict source trust hierarchy validation.
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

# Keywords used to classify incoming standards announcements into the 10 categories
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
        "enterprise risk management",
        "risk assessment framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "qms",
        "quality management system",
        "quality assurance standard",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "iec 27001",
        "international electrotechnical commission",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "owasp top 10",
        "owasp llm",
        "asvs",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis mobile app benchmark",
        "cis hardening",
        "cis controls",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"accessControl",
        r"dataClassification",
        r"incidentResponse",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacyImpactAssessment",
        r"dataSubjectRights",
        r"consentRecord",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"aiImpactAssessment",
        r"modelTransparency",
        r"modelBiasAudit",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskRegister",
        r"riskTreatment",
        r"riskEvaluation",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"qualityPolicy",
        r"auditLog",
        r"continuousImprovement",
    ],
    "IEC standards": [
        r"IEC[ -]?(?:62304|82304|62443|27001)",
        r"softwareLifecycle",
        r"medicalSoftware",
        r"industrialCybersecurity",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"MSTG",
        r"LLM0[1-9]",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"AIRMF",
        r"governMapMeasureManage",
        r"aiTrustworthiness",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"CSF2\.0",
        r"cybersecurityFramework",
        r"identifyProtectDetect",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"securityHardening",
        r"baselineConfiguration",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed standards journals",
    "Priority 4": "Industry blogs and vendor publications",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Mock Announcements for all 10 categories + 1 unverified
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Amendment 1: Climate Action & Information Security Governance Integration",
        "description": "ISO and IEC issued amendments mandating climate risk evaluation within the context of the organization's Information Security Management System (ISMS) under clause 4.1 and 4.2.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Revision: Privacy Information Management System Requirements for AI Data Pipelines",
        "description": "Updated PIMS standards require explicit data controller and processor mapping for artificial intelligence dataset ingestion, model training, and user personal data subject rights handling.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Management System (AIMS) Certification Guidance",
        "description": "The first international standard for AI management systems requires continuous monitoring of AI risks, bias auditing, model transparency disclosures, and lifecycle risk controls.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Update for Emerging Digital Technologies",
        "description": "ISO 31000 updated guidance emphasizes dynamic risk registers, automated risk quantification, and integration of cyber risk assessments with business continuity planning.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001:2026 Quality Management Systems Revision and Software Delivery Guidelines",
        "description": "The revised ISO 9001 QMS framework incorporates continuous integration and continuous deployment (CI/CD) traceability, automated release review audits, and documented quality gates.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Software Lifecycle Processes and IEC 62443 Industrial Cybersecurity Update",
        "description": "IEC releases updated guidance for software lifecycle validation, risk management, cybersecurity hardening, and health/industrial app software verification.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) v2.1 Release",
        "description": "OWASP MASVS v2.1 updates mobile application security verification requirements across storage, crypto, auth, network, platform interaction, resilience, and code quality controls.",
        "link": "https://mas.owasp.org/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Implementation Profile Update",
        "description": "NIST releases updated profiles for AI RMF core functions (Govern, Map, Measure, Manage) specifically tailored for generative AI, agentic systems, and mobile AI deployments.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (NIST CSF 2.0) Implementation Guidelines",
        "description": "NIST CSF 2.0 expands scope beyond critical infrastructure to all organizations, adding the 'Govern' function alongside Identify, Protect, Detect, Respond, and Recover.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Mobile Application & OS Security Benchmarks v3.0 Guidance",
        "description": "Center for Internet Security (CIS) releases updated benchmarks for hardening mobile application runtimes, secure build configurations, and containerized deployment baselines.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    # Unverified announcement to test source trust blocking
    {
        "id": "STD-MOCK-UNVERIFIED-RUMOR",
        "category": "ISO 27001",
        "title": "Unverified ISO 27001 Rumors on Random Blog Site",
        "description": "An unverified industry blog claims ISO 27001 certifications will automatically expire next month without official documentation. No official sources cited.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified)."""
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
        "android.com",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open web application security project",
        "center for internet security",
        "european commission",
        "official journal",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
        "ico",
        "government publication",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "IEEE.org", "acm.org"]
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

    priority = 4  # Default to 4

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
        # Priority 4 or 5: Must be verified by a Priority 1 official source
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
                        "iec",
                        "nist",
                        "owasp",
                        "cis",
                        "standard",
                        "benchmark",
                    }
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcements):
    """Logs verification status to stderr for all announcements."""
    verified_count = 0
    blocked_count = 0
    for a in announcements:
        priority, is_verified = classify_source_and_verify(a, announcements)
        if priority in (4, 5) and not is_verified:
            blocked_count += 1
            print(
                f"Source Trust Restriction: Announcement '{a.get('title')}' is Priority {priority} (unverified secondary source). Compliance PR generation restricted.",
                file=sys.stderr,
            )
        else:
            verified_count += 1
    return verified_count, blocked_count


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards categories."""
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


def identify_repository_gaps(scan_results):
    """Identifies repository gaps across code, documentation, and testing for each standard."""
    gaps = {}
    for cat in CATEGORIES:
        matches = scan_results.get(cat, [])
        cat_gaps = {
            "code_gaps": [],
            "doc_gaps": [],
            "testing_gaps": [],
        }

        # Evaluate matches
        if not matches:
            cat_gaps["code_gaps"].append(
                f"Missing explicit codebase references or implementation hooks for {cat} controls."
            )
            cat_gaps["doc_gaps"].append(
                f"Missing formal policy documentation and governance mapping for {cat}."
            )
            cat_gaps["testing_gaps"].append(
                f"Missing automated verification tests or audit suites validating {cat} compliance."
            )
        else:
            has_doc = any("docs/" in m["file"] or m["file"].endswith(".md") for m in matches)
            has_code = any(not m["file"].endswith(".md") for m in matches)

            if not has_doc:
                cat_gaps["doc_gaps"].append(
                    f"Codebase contains signals for {cat}, but lacks corresponding documentation in docs/."
                )
            if not has_code:
                cat_gaps["code_gaps"].append(
                    f"Documentation references {cat}, but no active codebase implementation signals were detected."
                )

            cat_gaps["testing_gaps"].append(
                f"Ensure continuous test coverage for {cat} controls in automated CI workflows."
            )

        gaps[cat] = cat_gaps
    return gaps


def generate_pull_request_draft(updates, scan_results, gaps):
    """Generates a draft of a pull request complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_checklist = []

    # Category deduplication
    processed_categories = set()

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

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        # Standard-specific migration, risk, and checklists
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Align Information Security Management System (ISMS) controls with ISO/IEC 27001:2022 amendments, updating access control policy and data classification declarations."
            )
            impl_checklist.append(
                "- [ ] Update access control and data classification policies in compliance with ISO 27001 ISMS Annex A."
            )
            testing_checklist.append(
                "- [ ] Run access control verification tests to ensure ISO 27001 ISMS compliance."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-conformance with enterprise information security governance and audit failure during ISO 27001 certification."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) controls, documenting data controller/processor roles and personal data processing activities."
            )
            impl_checklist.append(
                "- [ ] Establish PIMS data subject rights workflows and controller/processor documentation."
            )
            testing_checklist.append(
                "- [ ] Validate data subject erasure and export handlers for ISO 27701 PIMS compliance."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate privacy information governance exposing the organization to GDPR/PIMS regulatory penalties."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Deploy Artificial Intelligence Management System (AIMS) controls, integrating AI risk assessment, transparency notices, and bias auditing into AI pipelines."
            )
            impl_checklist.append(
                "- [ ] Implement AI risk management procedures and transparency logging under ISO 42001 AIMS."
            )
            testing_checklist.append(
                "- [ ] Execute automated AI model transparency and safety test suites."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated AI safety and bias risks leading to non-compliance under emerging AI governance standards."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Update enterprise risk management guidelines, embedding dynamic risk registers and automated risk evaluation metrics into technical workflows."
            )
            impl_checklist.append(
                "- [ ] Maintain an active risk register aligned with ISO 31000 risk management framework principles."
            )
            testing_checklist.append(
                "- [ ] Verify that risk assessment scripts and automated checks execute without errors."
            )
            risk_assessment.append(
                f"- *{cat}*: Ineffective technical risk evaluation leading to unflagged operational or security vulnerabilities."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enhance Quality Management System (QMS) integration by connecting software CI/CD delivery pipelines to documented release audit logs."
            )
            impl_checklist.append(
                "- [ ] Verify CI/CD quality gate enforcement and automated release audit logging."
            )
            testing_checklist.append(
                "- [ ] Execute release readiness audit scripts to confirm ISO 9001 quality gate compliance."
            )
            risk_assessment.append(
                f"- *{cat}*: Quality control degradation and untracked software delivery defects impacting distribution approval."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align software lifecycle processes with IEC 62304 / IEC 82304 guidelines and industrial cybersecurity controls under IEC 62443."
            )
            impl_checklist.append(
                "- [ ] Audit software lifecycle classification and cybersecurity controls against IEC standards."
            )
            testing_checklist.append(
                "- [ ] Conduct static analysis and vulnerability scans to satisfy IEC software safety requirements."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to meet international electrotechnical software safety and cybersecurity baseline standards."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Enforce OWASP Mobile Application Security Verification Standard (MASVS) controls across storage, crypto, auth, network, and resilience layers."
            )
            impl_checklist.append(
                "- [ ] Audit codebase against OWASP MASVS v2.1 verification requirements."
            )
            testing_checklist.append(
                "- [ ] Run static security analysis scanners and mobile security test suite."
            )
            risk_assessment.append(
                f"- *{cat}*: Exploitable mobile vulnerabilities resulting from deviation from OWASP MASVS baseline standards."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Integrate NIST AI Risk Management Framework core functions (Govern, Map, Measure, Manage) for AI integrations."
            )
            impl_checklist.append(
                "- [ ] Map AI features against NIST AI RMF trustworthiness criteria."
            )
            testing_checklist.append(
                "- [ ] Test AI interaction disclosure modals and synthetic output marking mechanisms."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-alignment with NIST AI RMF leading to unmanaged AI trustworthiness and safety risks."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST Cybersecurity Framework 2.0 (NIST CSF 2.0) guidelines across Govern, Identify, Protect, Detect, Respond, and Recover functions."
            )
            impl_checklist.append(
                "- [ ] Align security architecture and operational practices with NIST CSF 2.0 functions."
            )
            testing_checklist.append(
                "- [ ] Validate security controls and incident detection handlers against NIST CSF 2.0 baselines."
            )
            risk_assessment.append(
                f"- *{cat}*: Security posture gaps violating enterprise NIST CSF 2.0 cybersecurity requirements."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Harden mobile runtime configurations and application baselines in accordance with CIS Mobile Application Benchmarks."
            )
            impl_checklist.append(
                "- [ ] Apply CIS Benchmark hardening rules to build configurations and runtime manifests."
            )
            testing_checklist.append(
                "- [ ] Verify build environment and app binary hardening against CIS Benchmark criteria."
            )
            risk_assessment.append(
                f"- *{cat}*: Hardening defects exposing application runtimes to platform exploitation."
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
        else "- [ ] Perform generic technical standards compliance verification."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Run standard automated test suite."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the application and documentation into full alignment with updated technical standards, covering ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
International technical standards define the baseline for information security, privacy, quality, risk management, AI governance, and cybersecurity. Adhering to these standards ensures enterprise readiness, regulatory compliance, and robust technical controls across mobile and web platforms.

## 3. Regulatory change
- **ISO / IEC Frameworks**: Adoption of updated ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk Management (ISO 31000), QMS (ISO 9001), and IEC software lifecycle standards.
- **Security & AI Baselines**: Alignment with OWASP MASVS v2.1, NIST AI RMF 1.0, NIST CSF 2.0, and CIS Benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and enterprise compliance risk if technical standards baselines remain unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical controls and policy updates enhance runtime governance without breaking existing public interfaces or user workflows.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated standards validation checks locally.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Execute `python3 scripts/validate.py` to ensure schema integrity.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Verify internal security and governance playbooks reflect updated standards controls.

## 12. Compliance impact
- **Enterprise Standards Alignment**: Demonstrates compliance with international ISO, IEC, NIST, OWASP, and CIS standards.
- **Audit Readiness**: Prepares codebase and documentation for third-party compliance reviews and certifications.

## 13. Breaking changes
- No functional breaking changes are introduced.

## 14. Review checklist
- [ ] Verify that the PR diff is 100% emoji-free.
- [ ] Confirm official citations derive from Priority 1-3 trusted sources.
- [ ] Validate that all testing updates pass cleanly.

## 15. Approver recommendations
Verify that updated technical control declarations match enterprise governance requirements and confirm that automated security and standards validation scripts pass cleanly in CI workflows.
"""
    return pr_template


def update_documentation_report(updates, gaps, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
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

    lines.append("## Identified Repository Gaps & Task Recommendations")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(
                f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Status**: Suspended. Source is an unverified Priority 4/5 secondary source."
            )
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory/Standards Impact**: High priority compliance area.")

        cat_gaps = gaps.get(cat, {})
        if cat_gaps.get("code_gaps"):
            lines.append("#### Code Gaps")
            for gap in cat_gaps["code_gaps"]:
                lines.append(f"- **Gap**: {gap}")
        if cat_gaps.get("doc_gaps"):
            lines.append("#### Documentation Gaps")
            for gap in cat_gaps["doc_gaps"]:
                lines.append(f"- **Gap**: {gap}")
        if cat_gaps.get("testing_gaps"):
            lines.append("#### Testing Gaps")
            for gap in cat_gaps["testing_gaps"]:
                lines.append(f"- **Gap**: {gap}")

        lines.append("#### Action Items")
        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update ISMS access control and classification policies in codebase/docs."
            )
            lines.append(
                "- [ ] **Task 2**: Implement automated access logging verification tests."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Document PIMS controller/processor responsibilities and PII handling."
            )
            lines.append(
                "- [ ] **Task 2**: Add tests verifying data subject rights and privacy controls."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish AIMS risk management procedures and AI transparency disclosures."
            )
            lines.append(
                "- [ ] **Task 2**: Integrate AI bias and safety audit checks into test pipelines."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Maintain dynamic risk register and integrate risk evaluation criteria."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Enforce CI/CD quality gates and document QMS software delivery standards."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Validate software lifecycle and industrial cybersecurity controls against IEC standards."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Audit mobile application security controls against OWASP MASVS v2.1."
            )
            lines.append(
                "- [ ] **Task 2**: Run static security scans and unit tests for MASVS controls."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Map AI integration points against NIST AI RMF Govern, Map, Measure, Manage functions."
            )
            lines.append(
                "- [ ] **Task 2**: Implement automated tests for AI transparency notices."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity controls with NIST CSF 2.0 functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Harden mobile runtime configuration against CIS Benchmarks."
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
        print(f"Standards documentation report written to: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Changes (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards RSS/Atom feeds"
    )
    parser.add_argument(
        "--mock",
        type=str,
        default="inline",
        help="Path to custom mock announcements JSON file, or 'inline' to use default mock dataset",
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
        help="Filepath to write standards migration report",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/STANDARDS_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to write drafted PR proposal",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format to stdout"
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live technical standards feeds...")
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/news.xml"))
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

    # Enforce strict source trust hierarchy
    verified_count, blocked_count = enforce_strict_source_trust_hierarchy(announcements)

    # 2. Classify updates into 10 categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified technical standards updates matched the current filters.")
        sys.exit(0)

    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    verified_updates = []
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u, announcements)
        if priority in (4, 5) and not is_verified:
            pass
        else:
            verified_updates.append(u)

    print(
        f"Monitored and classified {len(classified_updates)} standards updates ({blocked_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u, announcements)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    # 3. Scan codebase for signals
    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(m) for m in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 4. Identify repository gaps
    gaps = identify_repository_gaps(scan_results)

    # 5. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, gaps, args.output_docs)

    # 6. Generate Pull Request draft
    pr_draft = generate_pull_request_draft(verified_updates, scan_results, gaps)

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

    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u, announcements)
            cat = u["category"]
            report_data.append(
                {
                    "category": cat,
                    "title": u["title"],
                    "pubDate": u["pubDate"],
                    "link": u["link"],
                    "priority": priority,
                    "verified": is_verified,
                    "matches": scan_results.get(cat, []),
                    "gaps": gaps.get(cat, {}),
                }
            )
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
