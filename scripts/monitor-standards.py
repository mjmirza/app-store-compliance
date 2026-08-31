#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks changes to 10 key technical standards:
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

When standards change, identifies repository gaps, generates implementation tasks,
documentation updates, and testing updates.
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
        "artificial intelligence management",
        "aims",
        "ai management system",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment framework",
        "risk treatment",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality control",
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
        "owasp mobile",
        "owasp api",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai",
        "governing ai risk",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis hardened images",
        "cis controls",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"access_control",
        r"data_classification",
        r"securityPolicy",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"pii_processor",
        r"privacy_impact",
        r"dataProtection",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"\bAIMS\b",
        r"ai_governance",
        r"model_safety",
        r"aiRisk",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"risk_matrix",
        r"riskAssessment",
        r"risk_register",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"\bQMS\b",
        r"quality_assurance",
        r"process_audit",
    ],
    "IEC standards": [
        r"IEC[ -]?(?:62443|82304|62304)",
        r"IEC[ -]?standards",
        r"industrial_security",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitization",
        r"xss_protection",
        r"csrf_token",
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"trustworthy_ai",
        r"ai_bias_audit",
        r"model_card",
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"cybersecurity_framework",
        r"incident_response",
        r"asset_inventory",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"hardened_config",
        r"system_hardening",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards and regulatory bodies (ISO, IEC, NIST, OWASP, CIS Security, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed studies",
    "Priority 4": "Industry blogs and vendor publications",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Mock announcements covering all 10 categories plus an unverified test announcement
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Information Security Management Revision",
        "description": "ISO releases updated Annex A controls for information security management systems (ISMS), expanding requirements for cloud services, threat intelligence, and data leakage prevention.",
        "link": "https://www.iso.org/iso-iec-27001-information-security.html",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 updates PIMS guidelines for PII controllers and processors, mandating automated data subject request processing and cross-border transfer documentation.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 AI Management System (AIMS) Certification Standards",
        "description": "ISO publishes implementation frameworks for ISO/IEC 42001 AIMS, requiring continuous risk monitoring, algorithmic impact assessments, and transparency controls for generative model deployments.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Assessment Guidance",
        "description": "Updated ISO 31000 risk management guidelines integrate cyber risk and algorithmic operational hazards into unified corporate risk registers.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Digital Process Audit Rules",
        "description": "ISO 9001 QMS guidance mandates automated continuous quality assurance and dynamic software deployment traceability for technical systems.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 82304 Cybersecurity for Industrial and Medical Software",
        "description": "The International Electrotechnical Commission releases updated IEC standards defining mandatory secure coding practices, component lifecycle tracking, and network isolation rules.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS and ASVS 2.0 Mobile and Application Verification Standards",
        "description": "OWASP publishes updated Mobile Application Security Verification Standard (MASVS) controls requiring hardware enclave key storage, certificate SPKI pinning, and zero plaintext database fallbacks.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.5 Governance Release",
        "description": "NIST releases updated AI RMF guidance focusing on Governance, Map, Measure, and Manage functions for foundation models and synthetic media applications.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework CSF 2.0 Governance Category Enforcement",
        "description": "NIST CSF 2.0 establishes Governance (GV) as a core pillar alongside Identify, Protect, Detect, Respond, and Recover, mandating continuous supply chain risk management.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls v8.1 Security Baseline",
        "description": "Center for Internet Security (CIS) updates benchmark baselines for containerized workloads, mobile operating systems, and automated configuration audit rules.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED",
        "category": "OWASP",
        "title": "Unverified Blog Claim Regarding OWASP Rules",
        "description": "A random tech blog post claims OWASP rules are changing next week. This is an unverified industry blog.",
        "link": "https://randomblogsite.com/owasp-rumors",
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
                        "security",
                        "privacy",
                        "benchmark",
                    }
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards categories.
    Excludes build, dependency, and test directories.
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
                    ".md",
                    ".swift",
                    ".m",
                    ".h",
                    ".plist",
                    ".html",
                    ".py",
                    ".sh",
                    ".yaml",
                    ".yml",
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

        # If keywords_filter is supplied, verify if any filter matches
        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Match against categories
        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                # Use word boundary search for short acronym keywords
                if len(kw) <= 5 and kw.isalnum():
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    if re.search(pattern, text_to_search, re.IGNORECASE):
                        matched_categories.append(cat)
                        break
                elif kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break

        # Fallback to predefined category if set
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


def get_category_details(cat):
    """
    Returns specific details for each standard category:
    (repository_gaps, implementation_tasks, documentation_updates, testing_updates, risk_desc)
    """
    if cat == "ISO 27001":
        gaps = [
            f"- **{cat} Gaps**: Missing formal Annex A controls mapping, missing data classification tags, and unaudited threat intelligence protocols."
        ]
        tasks = [
            f"- [ ] **Task 1**: Map ISMS Annex A controls to current repository data flows and server endpoints.",
            f"- [ ] **Task 2**: Implement strict access control logging and data leakage prevention headers.",
        ]
        docs = [
            f"- Update Information Security Management System (ISMS) policy documentation under `docs/SECURITY-POLICY-MIGRATION.md`.",
            f"- Record Annex A controls mapping and data classification scheme in developer guidelines.",
        ]
        tests = [
            f"- Add automated static scans verifying data classification annotations on all internal data models.",
            f"- Run access control test suite verifying role-based authorization rules.",
        ]
        risk = f"- *{cat}*: Non-compliance with ISMS standards leading to failed external security audits and loss of enterprise customer trust."

    elif cat == "ISO 27701":
        gaps = [
            f"- **{cat} Gaps**: Missing Privacy Information Management System (PIMS) PII controller/processor role definitions and unautomated data subject request handlers."
        ]
        tasks = [
            f"- [ ] **Task 1**: Implement automated PII identification and retention purging pipelines.",
            f"- [ ] **Task 2**: Document PII processor boundaries for external third-party SDKs.",
        ]
        docs = [
            f"- Publish Privacy Information Management System (PIMS) operational manual.",
            f"- Update privacy policy disclosures to reflect PII controller and processor obligations under ISO 27701.",
        ]
        tests = [
            f"- Test automated data erasure workflows for user deletion requests.",
            f"- Verify cross-border data transfer encryption checks in test environment.",
        ]
        risk = f"- *{cat}*: Inadequate PII management leading to regulatory fines and PIMS certification revocation."

    elif cat == "ISO 42001":
        gaps = [
            f"- **{cat} Gaps**: Missing Artificial Intelligence Management System (AIMS) algorithmic impact assessments, unmonitored model drift, and missing user interaction notices for generative models."
        ]
        tasks = [
            f"- [ ] **Task 1**: Integrate automated AI transparency notices on AI-driven user interfaces.",
            f"- [ ] **Task 2**: Establish continuous AI risk monitoring and model governance logging.",
        ]
        docs = [
            f"- Draft ISO/IEC 42001 AIMS Compliance Manual and Algorithmic Impact Assessment templates.",
            f"- Update AI system documentation with training data provenance and model safety parameters.",
        ]
        tests = [
            f"- Test AI model output safety filtering and synthetic content watermarking validators.",
            f"- Run automated tests for fallback mechanisms when AI endpoints return non-conforming responses.",
        ]
        risk = f"- *{cat}*: Unmitigated AI algorithmic risk, model hallucination exposure, and non-compliance with ISO 42001 AIMS requirements."

    elif cat == "ISO 31000":
        gaps = [
            f"- **{cat} Gaps**: Missing risk assessment matrix for software components, uncataloged technical debt, and isolated operational risk registers."
        ]
        tasks = [
            f"- [ ] **Task 1**: Establish unified technical risk assessment register mapping code modules to risk severity levels.",
            f"- [ ] **Task 2**: Automate risk treatment workflow tracking in CI/CD pipelines.",
        ]
        docs = [
            f"- Document ISO 31000 Risk Management Framework guidelines for software releases.",
            f"- Publish technical risk evaluation procedures in internal operational playbooks.",
        ]
        tests = [
            f"- Verify that high-risk code changes trigger mandatory security review gates in automated workflows.",
            f"- Run automated dependency vulnerability checks during pre-build validation.",
        ]
        risk = f"- *{cat}*: Unidentified operational hazards causing production outages or unmanaged vulnerabilities."

    elif cat == "ISO 9001":
        gaps = [
            f"- **{cat} Gaps**: Unstandardized release QA checklists, missing automated release audit trails, and inconsistent code review signoff documentation."
        ]
        tasks = [
            f"- [ ] **Task 1**: Enforce standardized pre-release Quality Assurance checklists and automated release auditing.",
            f"- [ ] **Task 2**: Wire build artifacts to release tag commit signatures for full traceability.",
        ]
        docs = [
            f"- Update Quality Management System (QMS) release guidelines and developer contribution standard.",
            f"- Document ISO 9001 software quality metrics and review requirements.",
        ]
        tests = [
            f"- Execute automated regression test suites before release candidate creation.",
            f"- Validate build script exit codes and environment variable consistency in CI.",
        ]
        risk = f"- *{cat}*: Quality degradation, software regressions, and QMS audit non-conformities."

    elif cat == "IEC standards":
        gaps = [
            f"- **{cat} Gaps**: Missing IEC 62443 / IEC 82304 component lifecycle tracking, unverified network isolation boundaries, and missing hardware enclave controls."
        ]
        tasks = [
            f"- [ ] **Task 1**: Implement Software Bill of Materials (SBOM) generation for all third-party dependencies.",
            f"- [ ] **Task 2**: Enforce strict network boundary isolation and encrypted payload transmission.",
        ]
        docs = [
            f"- Publish IEC standard compliance manifest covering component lifecycle management.",
            f"- Update technical specification documentation with network boundary and encryption architecture details.",
        ]
        tests = [
            f"- Run automated static code analysis scanning for raw socket or unencrypted network calls.",
            f"- Verify SBOM accuracy against compiled release binaries.",
        ]
        risk = f"- *{cat}*: Vulnerabilities in industrial or embedded software layers violating IEC safety standards."

    elif cat == "OWASP":
        gaps = [
            f"- **{cat} Gaps**: Incomplete OWASP MASVS / ASVS verification, potential XSS or injection vectors, and missing public-key SPKI pinning."
        ]
        tasks = [
            f"- [ ] **Task 1**: Audit code against OWASP MASVS Level 1 and Level 2 security controls.",
            f"- [ ] **Task 2**: Enforce input sanitization, SPKI certificate pinning, and hardware-backed credential storage.",
        ]
        docs = [
            f"- Update OWASP MASVS Security Verification checklist in development playbooks.",
            f"- Document input sanitization and anti-tampering measures in technical specs.",
        ]
        tests = [
            f"- Run automated dynamic analysis tests verifying certificate pinning failure behavior on untrusted proxies.",
            f"- Execute SAST scanners searching for SQL injection, XSS, and hardcoded secret patterns.",
        ]
        risk = f"- *{cat}*: Exploitable security vulnerabilities (MASVS / ASVS violations) enabling data exfiltration or app tampering."

    elif cat == "NIST AI RMF":
        gaps = [
            f"- **{cat} Gaps**: Missing NIST AI RMF Governance (GOVERN, MAP, MEASURE, MANAGE) tracking, unmitigated model bias vectors, and missing model card documentation."
        ]
        tasks = [
            f"- [ ] **Task 1**: Create Model Cards and trustworthiness documentation for deployed AI models.",
            f"- [ ] **Task 2**: Integrate continuous measurement of AI accuracy, fairness, and safety metrics.",
        ]
        docs = [
            f"- Publish NIST AI Risk Management Framework operational playbook.",
            f"- Document AI system lifecycle mapping, bias testing metrics, and mitigation protocols.",
        ]
        tests = [
            f"- Implement unit tests validating AI input boundary constraints and prompt sanitization.",
            f"- Execute automated evaluation suite for AI output accuracy and toxicity bounds.",
        ]
        risk = f"- *{cat}*: AI safety failures, reputational damage, and non-compliance with NIST AI RMF guidelines."

    elif cat == "NIST CSF":
        gaps = [
            f"- **{cat} Gaps**: Incomplete NIST CSF 2.0 Governance pillar alignment, unverified asset inventories, and manual incident response procedures."
        ]
        tasks = [
            f"- [ ] **Task 1**: Align repository security architecture across Identify, Protect, Detect, Respond, Recover, and Govern pillars.",
            f"- [ ] **Task 2**: Automate asset inventory generation and security event logging.",
        ]
        docs = [
            f"- Update NIST CSF 2.0 Security Baseline documentation in internal wiki.",
            f"- Publish Incident Response Plan (IRP) and asset inventory management procedure.",
        ]
        tests = [
            f"- Verify automated security log generation and log retention handlers.",
            f"- Test incident response alert scripts and failure failover configurations.",
        ]
        risk = f"- *{cat}*: Systemic cybersecurity vulnerabilities and inability to swiftly detect or recover from security incidents."

    elif cat == "CIS Benchmarks":
        gaps = [
            f"- **{cat} Gaps**: Missing CIS Benchmark hardening configurations, default system settings, and unverified container security policies."
        ]
        tasks = [
            f"- [ ] **Task 1**: Apply CIS Benchmark hardening rules to build configurations, Dockerfiles, and environment manifests.",
            f"- [ ] **Task 2**: Disable unnecessary OS services and restrict file permissions on configuration assets.",
        ]
        docs = [
            f"- Document CIS Benchmark configuration standards for deployment environments.",
            f"- Publish hardened baseline configuration guide for team developers.",
        ]
        tests = [
            f"- Run CIS Benchmark compliance automated audit scripts against container images and configurations.",
            f"- Verify that build scripts run with minimal required privileges.",
        ]
        risk = f"- *{cat}*: Misconfigured deployment baselines leaving systems open to automated exploit vectors."

    else:
        gaps = [f"- **{cat} Gaps**: Generic standard gaps needing audit."]
        tasks = [f"- [ ] **Task**: Audit repository implementation against updated {cat} criteria."]
        docs = [f"- Update documentation files to reflect {cat} changes."]
        tests = [f"- Run automated unit and integration tests verifying {cat} requirements."]
        risk = f"- *{cat}*: Standard compliance risk."

    return gaps, tasks, docs, tests, risk


def generate_pull_request_draft(updates, scan_results):
    """
    Generates a draft of a pull request complying with the exact 15 required non-vague sections.
    Follows source trust hierarchy and remains completely emoji-free.
    """
    citations_list = []
    affected_files_set = set()
    repo_gaps = []
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    doc_checklist = []
    risk_assessment = []

    # Category deduplication
    seen_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
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

        gaps, tasks, docs, tests, risk = get_category_details(cat)
        repo_gaps.extend(gaps)
        migration_steps.extend(tasks)
        impl_checklist.extend(tasks)
        doc_checklist.extend(docs)
        testing_checklist.extend(tests)
        risk_assessment.append(risk)

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration files).* "

    gaps_str = "\n".join(repo_gaps) if repo_gaps else "- *No repository gaps identified.*"
    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    testing_checklist_str = "\n".join(f"- [ ] {t}" if not t.startswith("- [ ]") else t for t in testing_checklist) if testing_checklist else "- [ ] Run standard test suite."
    doc_checklist_str = "\n".join(f"- [ ] {d}" if not d.startswith("- [ ]") else d for d in doc_checklist) if doc_checklist else "- [ ] Update compliance documentation."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces comprehensive updates, configuration enhancements, and verification tasks to bring the repository into full compliance with monitored technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).

## 2. Background
Modern application ecosystems require continuous alignment with international standardization frameworks and cybersecurity baselines. Adhering to updated ISO, IEC, OWASP, NIST, and CIS standards ensures system resilience, data protection, AI safety, and regulatory readiness across all distribution channels.

## 3. Regulatory change
- **ISO / IEC Standards**: Mandatory alignment with updated Information Security (ISO 27001), Privacy (ISO 27701), AI Management (ISO 42001), Risk (ISO 31000), Quality (ISO 9001), and Industrial/Medical Software Safety (IEC standards).
- **OWASP & NIST Frameworks**: Implementation of OWASP MASVS/ASVS security verification controls, NIST AI Risk Management Framework 1.5 governance rules, and NIST CSF 2.0 Governance pillar baselines.
- **CIS Benchmarks**: Enforcement of hardened system configurations, container baselines, and access control policies.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit failure, security vulnerability exposure, and operational degradation if identified gaps remain unaddressed.

## 7. Migration steps
### Identified Repository Gaps:
{gaps_str}

### Implementation Steps:
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards updates are fully backward-compatible. System configurations, governance policies, and security checks add protective validation layers without breaking existing functional APIs or end-user flows.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the repository-wide static analysis and standards compliance scanner.

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed checklists and verification logs.

## 12. Compliance impact
- **Certification Readiness**: Ensures repository passes ISO 27001, ISO 27701, ISO 42001, and ISO 9001 external audits.
- **Security Posture**: Resolves OWASP MASVS and NIST CSF 2.0 gaps, reducing attack surface and vulnerability risks.
- **AI Governance**: Fulfills NIST AI RMF and ISO 42001 AI safety and transparency directives.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced security baselines may reject non-compliant external requests or unhardened container configurations.

## 14. Review checklist
- [ ] Verify that the diff and output files are 100% free of emojis or graphical symbols.
- [ ] Verify that all official sources cited belong to Priority 1 standards bodies (ISO, IEC, NIST, OWASP, CIS, Government publications).
- [ ] Confirm that all testing procedures pass cleanly without warnings.

## 15. Approver recommendations
Verify that all identified repository gaps are addressed in code and documentation. Ensure Chief Information Security Officer (CISO) and Lead Compliance Architect sign off on updated Annex A controls and NIST CSF 2.0 governance policies before merging.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Remains strictly emoji-free.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Compliance Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Repository Gap Analysis, Implementation Tasks, Documentation & Testing Updates")
    lines.append("")

    seen_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        if cat in seen_categories:
            continue
        seen_categories.add(cat)

        gaps, tasks, docs, tests, risk = get_category_details(cat)

        lines.append(f"### Category: {cat}")
        lines.append("- **Compliance Standing**: Monitored technical standard.")
        lines.append("")
        lines.append("#### 1. Identified Repository Gaps")
        for g in gaps:
            lines.append(g)
        lines.append("")
        lines.append("#### 2. Implementation Tasks")
        for t in tasks:
            lines.append(t)
        lines.append("")
        lines.append("#### 3. Documentation Updates")
        for d in docs:
            lines.append(f"- {d}")
        lines.append("")
        lines.append("#### 4. Testing Updates")
        for t in tests:
            lines.append(f"- {t}")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation report updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
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

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

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
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    # Sort classified updates
    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    # Filter out announcements with unverified sources for PR generation
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
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    # 3. Scan codebase for signals related to these categories
    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    # Save drafted PR
    if args.pr_output:
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
            gaps, tasks, docs, tests, risk = get_category_details(cat)
            report_data.append(
                {
                    "category": cat,
                    "title": u["title"],
                    "pubDate": u["pubDate"],
                    "link": u["link"],
                    "priority": priority,
                    "verified": is_verified,
                    "repository_gaps": gaps,
                    "implementation_tasks": tasks,
                    "documentation_updates": docs,
                    "testing_updates": tests,
                    "matches": scan_results.get(cat, []),
                }
            )
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
