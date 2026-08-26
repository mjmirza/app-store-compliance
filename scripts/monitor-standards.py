#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 distinct technical standards:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks.
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
        "isms",
        "information security management system",
        "annex a",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management system",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
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
        "iec",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "top 10",
        "asvs",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "hardening guidelines",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"accessControl",
        r"access_control",
        r"securityPolicy",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacyImpact",
        r"privacyPolicy",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"aiGovernance",
        r"modelRisk",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskAssessment",
        r"riskRegister",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"qualityPolicy",
        r"auditLog",
    ],
    "IEC standards": [
        r"IEC[ -]?[0-9]+",
        r"medicalDevice",
        r"industrialControl",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitization",
        r"inputValidation",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI",
        r"trustworthyAI",
        r"biasMitigation",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"SP[ -]?800-53",
        r"incidentResponse",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"hardening",
        r"secureBaseline",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications, Apple Developer, Android Developer)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management Standard Revision",
        "description": "Updated ISO/IEC 27001 controls require enhanced threat intelligence integration, cloud security controls, and secure coding verification across software development lifecycles.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Update",
        "description": "ISO/IEC 27701 updates extend PIMS operational guidelines to require automated data subject access request (DSAR) pipelines and explicit PII processing logging.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Specification",
        "description": "ISO/IEC 42001 establishes requirements for establishing, implementing, and continually improving an Artificial Intelligence Management System (AIMS) in organizations developing or using AI systems.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Implementation Guidelines",
        "description": "ISO 31000 framework update mandates continuous algorithmic risk assessments and integrated supply chain risk monitoring for software applications.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Code Auditing Alignment",
        "description": "ISO 9001 quality guidelines mandate documented release verification, automated regression testing, and strict change approval traceability.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 62304 Software Lifecycle and Cybersecurity Mandate",
        "description": "International Electrotechnical Commission (IEC) standard updates enforce secure software lifecycle requirements, static analysis validation, and vulnerability disclosures.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) Update",
        "description": "OWASP releases updated MASVS criteria targeting secure storage (MASVS-STORAGE), network communication (MASVS-NETWORK), resilience (MASVS-RESILIENCE), and code quality.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "NIST issues actionable profiles for AI RMF core functions: Govern, Map, Measure, and Manage, focusing on mitigating bias, toxicity, and unauthorized data extraction in LLM applications.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF) 2.0 Operational Implementation",
        "description": "NIST CSF 2.0 expands coverage to all organizations with an added explicit 'Govern' function, emphasizing continuous cyber risk management and supply chain risk posture.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls for Secure Operating Environments",
        "description": "CIS publishes updated benchmarks for mobile OS hardening, container security baselines, and automated security configuration auditing.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT",
    },
    # Unverified announcement to test blocking logic
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO Certification Fines",
        "description": "An unverified tech blog speculates about ISO certification requirements changing overnight with automatic compliance penalties.",
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

    # Priority 1 official domains and keywords
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
        "support.google.com",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "cisecurity",
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
        "federal register",
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

    priority = 4  # Default to 4 if nothing matches

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
        or ".org" in link
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
                        "nist",
                        "owasp",
                        "cis",
                        "security",
                        "privacy",
                        "risk",
                    }
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 standards categories.
    Excludes typical build, dependency, and test directories.
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

    # Compile the signal patterns
    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
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
    """
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
                f"- **{cat}**: Audit information security management system (ISMS) controls, access control matrices, and threat intelligence integrations."
            )
            impl_checklist.append(
                "- [ ] Update access control policies and ISMS documentation."
            )
            testing_checklist.append(
                "- [ ] Conduct vulnerability scanning and access log verification per ISO 27001 Annex A controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with ISMS framework increases risk of unauthorized data access and audit findings."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) controls, automated DSAR pipelines, and PII consent logging."
            )
            impl_checklist.append(
                "- [ ] Configure PIMS data controller and processor roles."
            )
            testing_checklist.append(
                "- [ ] Test automated DSAR data export and deletion endpoints for ISO 27701 validation."
            )
            risk_assessment.append(
                f"- *{cat}*: Unregulated PII processing leads to PIMS compliance failure and regulatory fines."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance, model risk tracking, and bias mitigation protocols."
            )
            impl_checklist.append(
                "- [ ] Document AI model risk register and governance procedures."
            )
            testing_checklist.append(
                "- [ ] Execute AI model safety and output quality validation test suite."
            )
            risk_assessment.append(
                f"- *{cat}*: Unchecked generative AI components introduce safety, quality, and liability risks."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Re-align enterprise risk management guidelines and integrate supply chain vulnerability tracking."
            )
            impl_checklist.append(
                "- [ ] Perform comprehensive risk assessment and update risk registers."
            )
            testing_checklist.append(
                "- [ ] Validate fail-safe and fallback procedures under high-risk scenarios."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational risks lead to service disruptions and compliance gaps."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize Quality Management System (QMS) change controls, release auditing, and static verification pipelines."
            )
            impl_checklist.append(
                "- [ ] Enforce mandatory change approval logging for release artifacts."
            )
            testing_checklist.append(
                "- [ ] Verify 100% test coverage for critical QMS workflows."
            )
            risk_assessment.append(
                f"- *{cat}*: Quality control failures degrade application reliability and user experience."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align software lifecycle with IEC 62443 / IEC 62304 standards, establishing static analysis and dependency auditing."
            )
            impl_checklist.append(
                "- [ ] Integrate automated static application security testing (SAST) in CI."
            )
            testing_checklist.append(
                "- [ ] Run static security scans and verify SBOM dependency integrity."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with industrial and medical software lifecycle standards blocks certification."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement OWASP MASVS / ASVS security controls for storage, network communication, and input sanitization."
            )
            impl_checklist.append(
                "- [ ] Enforce input sanitization and secure network transport configurations."
            )
            testing_checklist.append(
                "- [ ] Execute dynamic security tests for injection and session manipulation vulnerabilities."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to OWASP Top 10 vulnerabilities creates severe exploitation vectors."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI RMF functions (Govern, Map, Measure, Manage) for trustworthy AI deployments."
            )
            impl_checklist.append(
                "- [ ] Implement AI model transparency disclosures and output monitoring."
            )
            testing_checklist.append(
                "- [ ] Benchmark LLM responses against toxicity, hallucination, and bias evaluation datasets."
            )
            risk_assessment.append(
                f"- *{cat}*: AI risk mis-management leads to untrustworthy outputs and brand damage."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Adopt NIST CSF 2.0 governance controls, continuous security monitoring, and incident response playbooks."
            )
            impl_checklist.append(
                "- [ ] Map cybersecurity controls to NIST CSF 2.0 core functions."
            )
            testing_checklist.append(
                "- [ ] Simulate incident response procedures and verify audit trail logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Incomplete cybersecurity framework leaves organization vulnerable to advanced threats."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS hardening guidelines and configuration controls across operating systems and container environments."
            )
            impl_checklist.append(
                "- [ ] Apply CIS baseline hardening to configuration and deployment manifests."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance scanner script on production configurations."
            )
            risk_assessment.append(
                f"- *{cat}*: Unhardened default settings increase exposure to automated exploit scripts."
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
        else "- [ ] Perform generic verification of technical standards."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Run automated unit and integration tests."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces configuration, documentation, and structural enhancements to ensure complete compliance with updated technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).

## 2. Background
Compliance with recognized international standards and security frameworks is essential for organizational integrity, security posture, and regulatory alignment. This PR addresses identified gaps between existing codebase configurations and newly published standards updates.

## 3. Regulatory change
- **ISO Frameworks**: Alignment with ISO/IEC 27001 ISMS, ISO/IEC 27701 PIMS, ISO/IEC 42001 AIMS, ISO 31000 Risk Management, and ISO 9001 QMS updates.
- **Security Standards**: Implementation of OWASP MASVS/ASVS controls, IEC 62443/62304 lifecycle rules, and CIS hardening benchmarks.
- **NIST Frameworks**: Operationalization of NIST AI RMF 1.0 (Govern, Map, Measure, Manage) and NIST CSF 2.0 cybersecurity controls.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium-to-High risk of security vulnerability exposure and compliance audit failure if these controls are omitted.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Architectural boundaries and existing API contracts are preserved while security and quality controls are strengthened.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run static security scanners and repository validation scripts.

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document security control mappings in internal architecture records.
- [ ] Verify that audit logs trace all compliance-relevant events.

## 12. Compliance impact
- **Audit Readiness**: Ensures repository satisfies ISO, NIST, OWASP, and CIS audit criteria.
- **Security Posture**: Strengthens system resilience against modern threat vectors.
- **AI Safety & Trust**: Establishes transparent AI governance under NIST AI RMF and ISO 42001.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced validation controls fail gracefully on un-sanitized inputs.

## 14. Review checklist
- [ ] Code and documentation are completely free of emojis or graphical symbols.
- [ ] All cited sources satisfy the strict Source Trust Hierarchy.
- [ ] Security configurations enforce strong defaults and encryption requirements.

## 15. Approver recommendations
Verify that all automated test suites pass cleanly and confirm that security configuration baselines comply with CIS Benchmarks and OWASP guidelines prior to merge.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across technical standards.",
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

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
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

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority compliance standard.")

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update ISMS access control policies and audit threat intelligence integrations."
            )
            lines.append(
                "- [ ] **Task 2**: Verify encryption and key management procedures."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Configure Privacy Information Management System (PIMS) operational rules."
            )
            lines.append(
                "- [ ] **Task 2**: Test automated DSAR data processing endpoints."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish AI Management System (AIMS) model risk register."
            )
            lines.append(
                "- [ ] **Task 2**: Implement AI bias and safety monitoring controls."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Perform enterprise risk assessment and update risk register."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Document QMS change approval procedures and release logging."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Integrate SAST scanning for IEC 62443 / IEC 62304 compliance."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Audit codebase against OWASP MASVS / ASVS verification criteria."
            )
            lines.append(
                "- [ ] **Task 2**: Validate input sanitization and secure transport layers."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Map AI features to NIST AI RMF core functions (Govern, Map, Measure, Manage)."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity controls with NIST CSF 2.0 functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Apply CIS hardening benchmarks to build and deployment manifests."
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
            f"Technical standards documentation report updated successfully at: {output_filepath}"
        )
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Compliance (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live technical standards RSS/Atom feeds",
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

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(
            parse_rss_feed("https://www.iso.org/contents/data/standard/rss.xml")
        )
        announcements.extend(
            parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml")
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

    # 2. Classify updates into the 10 categories
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

    # 3. Scan the codebase for signals related to these categories
    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    # 6. JSON output format verification if requested
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
