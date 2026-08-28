#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
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

# Keywords used to classify incoming policy announcements/articles into the 10 standards
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
        "pii processor",
        "pii controller",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai risk assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk evaluation criteria",
        "risk treatment plan",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality control processes",
        "continuous improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "electrotechnical commission",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "asvs",
        "owasp mobile top 10",
        "owasp llm top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "trustworthy ai",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "identify protect detect respond recover",
        "sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "hardening benchmarks",
        "cis hardened images",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO_27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"asset_management",
    ],
    "ISO 27701": [
        r"ISO_27701",
        r"PIMS",
        r"pii_processing",
        r"privacy_impact_assessment",
        r"data_retention",
    ],
    "ISO 42001": [
        r"ISO_42001",
        r"AIMS",
        r"ai_governance",
        r"model_card",
        r"algorithmic_impact",
    ],
    "ISO 31000": [
        r"ISO_31000",
        r"risk_register",
        r"risk_assessment",
        r"risk_treatment",
    ],
    "ISO 9001": [
        r"ISO_9001",
        r"QMS",
        r"quality_audit",
        r"process_control",
    ],
    "IEC standards": [
        r"IEC_62304",
        r"IEC_82304",
        r"IEC_62443",
        r"software_lifecycle",
        r"safety_class",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"top_10",
        r"xss_protection",
        r"sqli_guard",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"ai_risk_management",
        r"model_transparency",
        r"bias_mitigation",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurity_framework",
        r"incident_response",
        r"threat_detection",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"hardening_guide",
        r"secure_baseline",
        r"cis_control",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and government sources (ISO, IEC, NIST, CIS, OWASP, EU Commission, CISA, ENISA, FTC, ICO)",
    "Priority 2": "Reputable news organizations (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed journals",
    "Priority 4": "Industry blogs and corporate tech posts",
    "Priority 5": "Social media, unverified forums, AI-generated summaries",
}

# Mock announcements covering all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "ISO releases updated Annex A control guidance enforcing threat intelligence integration, secure coding practices, and continuous monitoring for cloud and mobile software architectures.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Extension Requirements",
        "description": "ISO/IEC 27701 specifies updated requirements for PII controllers and processors, mandating automated consent recording, privacy impact assessments, and PII data lifecycle logs.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Certification Standard",
        "description": "The ISO/IEC 42001 standard requires organizations deploying AI systems to document AI risk assessments, establish algorithmic transparency, and implement continuous AI model monitoring.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Assessment and Treatment Guidelines",
        "description": "ISO 31000 updates risk treatment framework guidelines, requiring structured risk identification, impact quantification, and documented mitigation strategies across product engineering teams.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Process Verification Guidelines",
        "description": "ISO 9001 QMS guidance mandates traceably documented software development processes, release verification workflows, and formal customer feedback remediation tracking.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 and IEC 82304 Software Lifecycle Process Requirements",
        "description": "The International Electrotechnical Commission updates health and safety software lifecycle standards (IEC 62304 / IEC 82304), mandating formal software safety classification and risk management file verification.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS and Top 10 Security Verification Framework Release",
        "description": "OWASP publishes updated Mobile Application Security Verification Standard (MASVS) and ASVS requirements, introducing strict controls for storage encryption, API authentication, and LLM prompt security.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Companion Guidelines",
        "description": "NIST releases operational guidance for AI RMF core functions (Govern, Map, Measure, Manage), requiring explicit documentation of training data provenance, bias evaluations, and AI safety testing.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework CSF 2.0 Implementation Guide",
        "description": "NIST CSF 2.0 introduces Governance as a central pillar alongside Identify, Protect, Detect, Respond, and Recover, mandating organizational supply chain risk management and continuous vulnerability remediation.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Security Benchmarks and Configuration Baseline Update",
        "description": "Center for Internet Security issues updated hardening benchmarks for mobile operating systems, cloud containers, and web servers, mandating automated baseline compliance checks in CI/CD pipelines.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
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
        "cisecurity.org",
        "owasp.org",
        "europa.eu",
        "cisa.gov",
        "enisa.europa.eu",
        "ftc.gov",
        "ico.org.uk",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "cis benchmark",
        "owasp",
        "international organization for standardization",
        "electrotechnical commission",
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
        has_p1_ref_in_text = any(d in combined for d in p1_domains) or any(
            kw in combined for kw in p1_keywords
        )
        if has_p1_ref_in_text:
            is_verified = True

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 technical standards."""
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
                    ".md",
                    ".sh",
                    ".py",
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
    doc_checklist = []
    risk_assessment = []

    seen_categories = set()

    for u in updates:
        cat = u["category"]
        if cat in seen_categories:
            continue
        seen_categories.add(cat)

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
                f"- **{cat}**: Audit information security management systems (ISMS) and map Annex A controls to access management and cryptographic storage implementations."
            )
            impl_checklist.append(
                "- [ ] ISO 27001: Implement Annex A control mappings for data protection and threat monitoring."
            )
            testing_checklist.append(
                "- [ ] ISO 27001: Execute automated vulnerability scans and access control test suites."
            )
            doc_checklist.append(
                "- [ ] ISO 27001: Update information security management system policy documentation in `docs/`."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with ISMS framework leading to audit failure and unmitigated security exposure."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to Privacy Information Management System (PIMS), ensuring explicit PII controller/processor log controls."
            )
            impl_checklist.append(
                "- [ ] ISO 27701: Configure automated PII processing logs and privacy impact assessment records."
            )
            testing_checklist.append(
                "- [ ] ISO 27701: Test user PII deletion and consent withdrawal workflows."
            )
            doc_checklist.append(
                "- [ ] ISO 27701: Document PII controller and processor privacy policies."
            )
            risk_assessment.append(
                f"- *{cat}*: Risk of privacy breaches and regulatory fines due to unmonitored PII processing."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) controls for model transparency, risk assessments, and logging."
            )
            impl_checklist.append(
                "- [ ] ISO 42001: Deploy AI risk assessment frameworks and model card transparency disclosures."
            )
            testing_checklist.append(
                "- [ ] ISO 42001: Validate AI input sanitization and output safety guardrails."
            )
            doc_checklist.append(
                "- [ ] ISO 42001: Document AI governance policies and model lineage in compliance records."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI model deployments causing algorithmic bias or unauthorized output generation."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align risk evaluation criteria with ISO 31000 guidelines, updating repository risk registers."
            )
            impl_checklist.append(
                "- [ ] ISO 31000: Update risk registers with quantified impact and treatment milestones."
            )
            testing_checklist.append(
                "- [ ] ISO 31000: Perform periodic risk scenario simulations and failover tests."
            )
            doc_checklist.append(
                "- [ ] ISO 31000: Publish revised enterprise risk management documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Operational failures stemming from incomplete risk identification and treatment plans."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enforce Quality Management System (QMS) process controls and automated verification in build release pipelines."
            )
            impl_checklist.append(
                "- [ ] ISO 9001: Integrate process control gates into CI/CD release workflows."
            )
            testing_checklist.append(
                "- [ ] ISO 9001: Run full regression testing suites prior to tagging release binaries."
            )
            doc_checklist.append(
                "- [ ] ISO 9001: Document quality assurance standards and audit traceability metrics."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation and lack of release traceability."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Update IEC 62304 / IEC 82304 software lifecycle safety classifications and hazard analysis files."
            )
            impl_checklist.append(
                "- [ ] IEC standards: Update software safety class definitions and traceability matrices."
            )
            testing_checklist.append(
                "- [ ] IEC standards: Execute unit, integration, and system safety verification tests."
            )
            doc_checklist.append(
                "- [ ] IEC standards: Update software lifecycle management records and hazard analysis files."
            )
            risk_assessment.append(
                f"- *{cat}*: Critical safety and compliance non-conformity in regulated software environments."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Enforce OWASP MASVS/ASVS controls across authentication, network communication, storage, and code integrity."
            )
            impl_checklist.append(
                "- [ ] OWASP: Verify implementation of OWASP MASVS L1/L2 security controls."
            )
            testing_checklist.append(
                "- [ ] OWASP: Execute automated static application security testing (SAST) and dynamic scans."
            )
            doc_checklist.append(
                "- [ ] OWASP: Document security control verification against OWASP ASVS/MASVS checklists."
            )
            risk_assessment.append(
                f"- *{cat}*: Application vulnerability exposure to common web and mobile attack vectors."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI RMF core functions (Govern, Map, Measure, Manage) across AI feature pipelines."
            )
            impl_checklist.append(
                "- [ ] NIST AI RMF: Implement governance policies and bias mitigation measurement metrics."
            )
            testing_checklist.append(
                "- [ ] NIST AI RMF: Execute adversarial prompt testing and accuracy evaluation suites."
            )
            doc_checklist.append(
                "- [ ] NIST AI RMF: Maintain AI RMF compliance profile and data provenance logs."
            )
            risk_assessment.append(
                f"- *{cat}*: Failure to manage AI risks leading to untrustworthy AI deployments and regulatory scrutiny."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Integrate NIST CSF 2.0 Governance and Protect functions across infrastructure and application code."
            )
            impl_checklist.append(
                "- [ ] NIST CSF: Configure continuous threat monitoring and incident response playbooks."
            )
            testing_checklist.append(
                "- [ ] NIST CSF: Verify incident detection alerts and disaster recovery procedures."
            )
            doc_checklist.append(
                "- [ ] NIST CSF: Update NIST CSF target profiles and supply chain risk documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate threat detection and delayed incident response capability."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Audit and enforce CIS hardened configuration baselines for operating systems, containers, and application environments."
            )
            impl_checklist.append(
                "- [ ] CIS Benchmarks: Apply CIS hardening scripts to container and host configurations."
            )
            testing_checklist.append(
                "- [ ] CIS Benchmarks: Run automated compliance scanners (e.g., CIS CAT or equivalent baseline scripts)."
            )
            doc_checklist.append(
                "- [ ] CIS Benchmarks: Document configuration benchmark exceptions and hardening policies."
            )
            risk_assessment.append(
                f"- *{cat}*: System misconfigurations leaving environment exposed to known exploitation techniques."
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
        else "- [ ] Perform generic compliance review against technical standards."
    )
    testing_checklist_str = (
        "\n".join(testing_checklist)
        if testing_checklist
        else "- [ ] Run standard unit and integration test suites."
    )
    doc_checklist_str = (
        "\n".join(doc_checklist)
        if doc_checklist
        else "- [ ] Update standards policy migration records."
    )
    risk_assessment_str = (
        "\n".join(risk_assessment)
        if risk_assessment
        else "- *Low identified risk.*"
    )

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces comprehensive updates to align the repository with monitored technical standards, covering ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards provide rigorous frameworks for security, privacy, quality, risk management, AI governance, and system hardening. Continuous alignment ensures organizational compliance, mitigates security vulnerabilities, and satisfies institutional review expectations.

## 3. Regulatory change
- **Information Security and Privacy Standards**: Updates to ISO 27001 (ISMS), ISO 27701 (PIMS), and OWASP security controls.
- **AI Governance and Risk Frameworks**: Adherence to ISO 42001, NIST AI RMF, and ISO 31000 risk treatment guidelines.
- **Quality, Health, and Hardening Standards**: Compliance with ISO 9001 QMS, IEC 62304/82304 lifecycle rules, NIST CSF 2.0, and CIS Benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of security audit failures and compliance rejection if technical standards baselines drift.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes preserve backward compatibility across supported runtime environments. Configuration hardening and security controls operate transparently without breaking existing functional APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run repository validation scripts to confirm zero syntax or structural errors.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Verify that all automated test scripts pass without regression.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with complete implementation logs.

## 12. Compliance impact
- **Audit Preparedness**: Validates technical controls against international standards (ISO/IEC, NIST, OWASP, CIS).
- **Risk Mitigation**: Reduces system exposure to vulnerabilities and operational security risks.
- **AI Governance**: Ensures transparent and trustworthy AI system operations.

## 13. Breaking changes
- No breaking API changes are introduced. Enhanced hardening configurations may restrict insecure legacy protocols.

## 14. Review checklist
- [ ] Code and documentation diffs are 100% free of emojis or graphical symbols.
- [ ] Official citations are verified against Priority 1 standards organization sources.
- [ ] Hardening parameters match published CIS and NIST benchmarks.

## 15. Approver recommendations
Verify that updated technical controls are validated in pre-production environments before deploying to production release channels.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across ISO, IEC, OWASP, NIST, and CIS standards.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    seen = set()
    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + (
            "(Verified)" if is_verified else "(Unverified)"
        )
        lines.append(f"### {idx}. [{cat}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        if cat in seen:
            continue
        seen.add(cat)

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
        lines.append(
            "- **Regulatory Impact**: High priority technical standard requirement."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Implementation Task**: Align access management and cryptographic storage with Annex A controls."
            )
            lines.append(
                "- [ ] **Documentation Task**: Update ISMS policy documentation in `docs/`."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute automated vulnerability scans and access control checks."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Implementation Task**: Implement PII processing controls and consent logging."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document PIMS PII controller and processor roles."
            )
            lines.append(
                "- [ ] **Testing Task**: Validate automated PII deletion and data export requests."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Implementation Task**: Deploy AI Risk Management System (AIMS) controls and model cards."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document AI system lineage, training inputs, and safety boundaries."
            )
            lines.append(
                "- [ ] **Testing Task**: Run AI input sanitization and hallucination guardrail test suites."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Implementation Task**: Update repository risk registers and treatment milestones."
            )
            lines.append(
                "- [ ] **Documentation Task**: Publish revised risk evaluation criteria and mitigation plans."
            )
            lines.append(
                "- [ ] **Testing Task**: Simulate disaster recovery and risk mitigation procedures."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Implementation Task**: Enforce QMS build verification gates in release workflows."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document quality assurance standards and audit records."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute complete regression suite before tagging release candidates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Implementation Task**: Maintain IEC 62304 / IEC 82304 software safety classifications."
            )
            lines.append(
                "- [ ] **Documentation Task**: Maintain hazard analysis files and software traceability matrices."
            )
            lines.append(
                "- [ ] **Testing Task**: Run unit and integration verification against safety class requirements."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Implementation Task**: Implement OWASP MASVS/ASVS controls for input and storage security."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document security verification mappings against OWASP checklists."
            )
            lines.append(
                "- [ ] **Testing Task**: Execute SAST and dynamic security test suites."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Implementation Task**: Operationalize NIST AI RMF core functions across AI components."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document AI risk profile and dataset provenance."
            )
            lines.append(
                "- [ ] **Testing Task**: Run adversarial prompt testing and bias evaluation suites."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Implementation Task**: Apply NIST CSF 2.0 Governance and Protect controls."
            )
            lines.append(
                "- [ ] **Documentation Task**: Update cybersecurity target profiles and incident response plans."
            )
            lines.append(
                "- [ ] **Testing Task**: Perform threat detection and incident response drills."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Implementation Task**: Apply CIS hardening configurations to environment assets."
            )
            lines.append(
                "- [ ] **Documentation Task**: Document CIS benchmark exceptions and hardening baselines."
            )
            lines.append(
                "- [ ] **Testing Task**: Run automated CIS baseline compliance scanners."
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
            f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr
        )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Compliance Requirements"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live technical standards policy feeds",
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
        print("Fetching live Technical Standards RSS feeds...")
        announcements.extend(
            parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml")
        )
        announcements.extend(
            parse_rss_feed("https://owasp.org/feed.xml")
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
        print(f"Scanning codebase under '{args.dir}' for standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

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
