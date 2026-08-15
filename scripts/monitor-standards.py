#!/usr/bin/env python3
"""Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 distinct technical standards: ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
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

# Keywords used to classify incoming announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management",
        "isms",
        "annex a controls",
        "statement of applicability",
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
        "artificial intelligence management",
        "aims",
        "ai management system",
        "responsible ai governance",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "enterprise risk management",
        "risk treatment plan",
        "risk assessment matrix",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance controls",
        "continual improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 81001",
        "iec 62443",
        "international electrotechnical commission",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "owasp masvs",
        "mastg",
        "owasp mobile top 10",
        "owasp api top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "govern map measure manage",
        "trustworthy ai",
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
        "cis controls",
        "hardening guidelines",
        "cis level 1",
        "cis level 2",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"InformationSecurityPolicy",
        r"SecurityAccessControl",
        r"AssetManagement",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"PIIProcessor",
        r"PIIController",
        r"PrivacyImpactAssessment",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"AIGovernance",
        r"AIBiasAudit",
        r"AIRiskAssessment",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"RiskAssessment",
        r"RiskRegister",
        r"RiskTreatment",
        r"RiskMatrix",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"QualityAssurance",
        r"DocumentControl",
        r"QualityPolicy",
    ],
    "IEC standards": [
        r"IEC[ -]?62304",
        r"IEC[ -]?81001",
        r"IEC[ -]?62443",
        r"MedicalSoftware",
        r"IECStandard",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MASTG",
        r"OWASPTop10",
        r"SQLInjection",
        r"XSSFilter",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"GovernMapMeasureManage",
        r"TrustworthyAI",
        r"AITransparency",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"CybersecurityFramework",
        r"IdentifyProtectDetect",
        r"CSFControls",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CISControls",
        r"HardeningGuide",
        r"CISLevel1",
        r"CISLevel2",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed journals",
    "Priority 4": "Industry blogs and vendor publications",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Mock announcements covering all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Security Annex A Control Verification Mandate",
        "description": "ISO/IEC 27001 mandates updated Annex A controls for information security management systems (ISMS), requiring explicit access control lists, threat intelligence integration, and secure coding practices across repositories.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System (PIMS) Data Processor Guidelines",
        "description": "Updates to ISO/IEC 27701 specify explicit PII controller and processor requirements, mandating documented PII lifecycle management, user consent mechanisms, and automated data subject request handlers.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Certification Rules",
        "description": "The ISO/IEC 42001 framework establishes global requirements for AI management systems, enforcing systemic AI risk management, bias evaluation, transparency disclosures, and model provenance logging.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Guidelines Update",
        "description": "ISO 31000 guidelines mandate structured risk assessment matrices and continuous risk treatment plans across software architecture, deployment infrastructure, and vendor integrations.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Software Lifecycle Controls",
        "description": "ISO 9001 standard updates require formalized software design reviews, traceable documentation controls, automated testing coverage requirements, and continual quality improvement metrics.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 81001 Health Software Lifecycle and Cybersecurity Standards",
        "description": "IEC standards for health and medical device software enforce strict lifecycle process validation, threat modeling, SBOM tracking, and secure patch management for digital applications.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 Mobile Application Security Verification Standard",
        "description": "OWASP releases updated MASVS Level 1 and Level 2 security controls, mandating strict anti-tampering, network pinning, cryptographic storage, and dynamic injection protections for mobile platforms.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 (NIST AI 100-1) Profile Implementation",
        "description": "NIST AI RMF guidelines detail operational controls across the Govern, Map, Measure, and Manage functions to ensure trustworthy, explainable, safe, and privacy-preserving AI integration.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Operational Governance Directives",
        "description": "NIST CSF 2.0 expands cybersecurity controls across six core functions: Govern, Identify, Protect, Detect, Respond, and Recover, mandating enterprise supply chain risk management.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls and Benchmark Hardening Standard Releases",
        "description": "Center for Internet Security publishes updated CIS Benchmarks for mobile OS and cloud build environments, detailing Level 1 and Level 2 security baseline hardening rules.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Industry Blog Rumors on ISO 27001 Revisions",
        "description": "A random tech blog claims ISO 27001 will require immediate daily external audits for all mobile apps. This is an unverified industry blog rumor.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies an announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified)."""
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
        "gov.sg",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "owasp",
        "center for internet security",
        "european commission",
        "eur-lex",
        "official journal",
        "enisa",
        "edpb",
        "ftc",
        "nist",
        "cisa",
        "ico",
        "government publication",
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
                        "iec",
                        "security",
                        "privacy",
                        "ai",
                    }
                    overlap = words.intersection(other_words).intersection(
                        common_terms
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards categories."""
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

    # Compile the signal patterns
    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Check applicable file types
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
                    ".html",
                    ".md",
                    ".py",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
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
                                    # Break to avoid duplicate entry for the same line and category
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
                "User-Agent": "Mozilla/5.0 (StandardsComplianceMonitor/1.0)"
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

        # If keywords_filter is supplied, verify if any filter matches
        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Match against categories
        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break  # Break keyword loop for this category

        # Fallback to predefined category if set
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
    risk_assessment = []
    seen_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
        )

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in seen_categories:
            continue
        seen_categories.add(cat)

        # Category-specific migration details
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Audit ISMS Annex A controls, enforcing threat intelligence integration, strict access controls, and secure development policies."
            )
            impl_checklist.append(
                "- [ ] Update Statement of Applicability and verify ISO 27001 Annex A security control mappings."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with enterprise ISMS mandates resulting in audit findings and security certification loss."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Establish PII controller and processor data governance workflows, user consent management, and automated subject request handling."
            )
            impl_checklist.append(
                "- [ ] Configure PIMS data mapping and record of processing activities for PII."
            )
            risk_assessment.append(
                f"- *{cat}*: Unregulated PII handling causing regulatory privacy violations and PIMS audit failures."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement AI management system (AIMS) controls including algorithmic impact assessment, bias tracking, and transparency disclosures."
            )
            impl_checklist.append(
                "- [ ] Implement AI system transparency logs and bias mitigation controls per ISO/IEC 42001."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI model deployment exposing the organization to algorithmic bias and regulatory penalties."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align enterprise risk assessment matrices and maintain systematic risk treatment plans for software assets."
            )
            impl_checklist.append(
                "- [ ] Conduct ISO 31000 risk assessment and update the enterprise risk register."
            )
            risk_assessment.append(
                f"- *{cat}*: Unidentified operational or technical risks escalating into critical enterprise security incidents."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Formalize quality management system (QMS) software lifecycle controls, document reviews, and automated verification."
            )
            impl_checklist.append(
                "- [ ] Enforce QMS document control policies and release verification gates."
            )
            risk_assessment.append(
                f"- *{cat}*: Product defect slippage and QA process degradation failing QMS audit standards."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Validate health and medical device software lifecycle processes under IEC 62304 / IEC 81001 including threat modeling."
            )
            impl_checklist.append(
                "- [ ] Complete IEC 62304 software safety classification and lifecycle documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Medical or health software regulatory rejection by health authorities."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement OWASP MASVS Level 1 and Level 2 controls covering anti-tampering, secure storage, network pinning, and input validation."
            )
            impl_checklist.append(
                "- [ ] Audit application code against OWASP MASVS v2.1 verification criteria."
            )
            risk_assessment.append(
                f"- *{cat}*: Critical application vulnerabilities exposing client sessions to interception or reverse-engineering."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI RMF Govern, Map, Measure, and Manage functions for trustworthy AI integration."
            )
            impl_checklist.append(
                "- [ ] Document NIST AI RMF profile alignment for all generative and predictive AI features."
            )
            risk_assessment.append(
                f"- *{cat}*: Deployment of non-explainable or untrusted AI components violating government AI guidelines."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map software infrastructure and CI/CD pipelines to NIST CSF 2.0 core functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append(
                "- [ ] Align enterprise cybersecurity posture with NIST CSF 2.0 governance requirements."
            )
            risk_assessment.append(
                f"- *{cat}*: Supply chain cybersecurity gaps and slow incident response readiness."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Level 1 and Level 2 benchmark hardening rules across build environments and mobile application settings."
            )
            impl_checklist.append(
                "- [ ] Verify environment configurations against CIS Benchmark hardening guidelines."
            )
            risk_assessment.append(
                f"- *{cat}*: Insecure OS configurations and build toolchain vulnerabilities leading to compromise."
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
        else "- [ ] Perform generic verification of technical standards compliance."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical updates to bring the repository into complete compliance with international technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP MASVS, NIST AI RMF, NIST CSF 2.0, and CIS Benchmarks.

## 2. Background
Modern enterprise software must satisfy rigorous international security, quality, risk, and privacy management frameworks. Storefront operators, enterprise auditors, and government regulatory bodies mandate verifiable adherence to published technical standards prior to release.

## 3. Regulatory change
- **ISO / IEC Standards**: Mandatory ISMS Annex A controls, PIMS privacy governance, AIMS AI management systems, and medical software lifecycle requirements.
- **Security & AI Frameworks**: OWASP MASVS mobile security controls, NIST AI RMF trustworthy AI guidelines, NIST CSF 2.0 governance, and CIS Benchmark environment hardening rules.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit failure, security vulnerability exposure, or enterprise distribution rejection if technical standard controls remain unverified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standard controls are non-breaking and fully backward-compatible. Technical standards compliance enhancements introduce configuration and process safeguards without modifying existing user-facing contract APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
- [ ] Verify that security and privacy control mappings are validated by automated static analysis.
- [ ] Conduct threat model validation against OWASP MASVS controls.
- [ ] Confirm AI model logging and transparency mechanisms conform to NIST AI RMF and ISO 42001.
- [ ] Validate CIS Benchmark build environment hardening settings.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document technical standard control mappings in repository architecture guides.
- [ ] Maintain an up-to-date risk register and statement of applicability.

## 12. Compliance impact
- **Audit Readiness**: Ensures total alignment with ISO/IEC certification audits and enterprise vendor risk evaluations.
- **Security Posture**: Strengthens mobile and cloud application defenses against OWASP Top 10 risks.
- **AI Governance**: Establishes transparent, trustworthy AI operations aligned with international standards.

## 13. Breaking changes
- No functional breaking changes are introduced. Controls reinforce security and governance posture.

## 14. Review checklist
- [ ] Verify that the diff is 100% free of emojis or graphical symbols in code and documentation.
- [ ] Confirm all official standards citations are verified against Priority 1 sources.
- [ ] Ensure security controls match OWASP and NIST framework requirements.

## 15. Approver recommendations
Verify that ISMS and PIMS control evidence is properly cataloged and confirm that AI component transparency disclosures satisfy ISO 42001 and NIST AI RMF requirements before authorizing release.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Requirements Policy Migration & Requirements Report",
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

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    seen_task_categories = set()
    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            if f"{cat}_blocked" in seen_task_categories:
                continue
            seen_task_categories.add(f"{cat}_blocked")
            lines.append(
                f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)"
            )
            lines.append(
                "- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source."
            )
            lines.append("")
            continue

        if cat in seen_task_categories:
            continue
        seen_task_categories.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Compliance Impact**: High priority technical standards area."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update Statement of Applicability for ISO 27001 Annex A controls."
            )
            lines.append(
                "- [ ] **Task 2**: Verify secure development policies and access controls across modules."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Configure PIMS PII controller and processor data governance workflows."
            )
            lines.append(
                "- [ ] **Task 2**: Implement automated data subject request handling functions."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish AI Management System (AIMS) transparency and bias logging."
            )
            lines.append(
                "- [ ] **Task 2**: Conduct algorithmic risk and impact assessments for AI modules."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Maintain ISO 31000 risk registers and treatment plans for software assets."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Formalize QMS document control policies and release verification gates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Complete IEC 62304 / IEC 81001 lifecycle process validation and threat modeling."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Audit application code against OWASP MASVS Level 1 and Level 2 security controls."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Operationalize NIST AI RMF Govern, Map, Measure, and Manage functions."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Map infrastructure and deployment pipelines to NIST CSF 2.0 core functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Apply CIS Level 1 and Level 2 benchmark hardening rules across build environments."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify that all technical criteria for {cat} are checked and handled."
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

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(
            parse_rss_feed("https://www.iso.org/contents/rss/news.xml")
        )
        announcements.extend(
            parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml")
        )

    # Fallback to mock data if live has no updates or mock is explicitly requested (default)
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

    # 2. Classify updates into the 10 required categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")]
        if args.keywords
        else None
    )
    classified_updates = classify_announcements(
        announcements, keywords_filter
    )

    if not classified_updates:
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    # Sort classified updates to keep them structured
    classified_updates = sorted(
        classified_updates, key=lambda x: x["category"]
    )

    # Filter out announcements with unverified sources for PR generation
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

    # 3. Scan the codebase for signals related to these categories
    if not args.json:
        print(
            f"Scanning codebase under '{args.dir}' for standards integration signals..."
        )
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    # Save drafted PR
    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
            print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(
            f"Failed to write PR draft to {args.pr_output}: {e}",
            file=sys.stderr,
        )

    # 6. JSON output format if requested
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
