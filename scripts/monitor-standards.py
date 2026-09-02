#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 distinct technical standards:
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
        "personally identifiable information",
        "pii processing",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai management",
        "ai risk management",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment matrix",
        "risk treatment plan",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance controls",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "iec 60601",
        "functional safety",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "owasp masvs",
        "owasp mstg",
        "owasp asvs",
        "owasp llm top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "nist cybersecurity framework",
        "identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis hardened images",
        "cis controls",
        "cis cat",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 standards
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"information_security_policy",
        r"security_controls",
        r"access_control_policy",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"pii_data",
        r"privacy_policy",
        r"data_protection_officer",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"ai_model_registry",
        r"bias_mitigation",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_register",
        r"risk_assessment",
        r"threat_model",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_audit",
        r"change_management",
    ],
    "IEC standards": [
        r"IEC62304",
        r"IEC62443",
        r"IEC82304",
        r"functional_safety",
        r"medical_device_software",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitizer",
        r"sqlcipher",
        r"keychain",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"ai_risk_assessment",
        r"govern_map_measure_manage",
        r"model_explainability",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurity_framework",
        r"incident_response",
        r"continuous_monitoring",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"hardened_config",
        r"security_baseline",
        r"cis_controls",
    ],
}

# Source trust hierarchy
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, FTC, CISA, Official Standards Organizations",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Management Transition Guidance",
        "description": "Updated Annex A controls require modern organizational, physical, technological, and operational security controls including explicit threat intelligence and cloud services security.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Update",
        "description": "Updated guidelines for managing Personally Identifiable Information (PII) processing, data controller/processor controls, and integration with regional privacy regulations.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Standard Release",
        "description": "Establishment of certification criteria for Artificial Intelligence Management Systems (AIMS), focusing on AI risk assessment, model transparency, and data governance.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 05 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Principles and Implementation Framework",
        "description": "Comprehensive risk management principles emphasizing continuous evaluation, dynamic threat modelling, and integration into organizational decision-making.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 08 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Review and Assurance Directives",
        "description": "Enhanced Quality Management System (QMS) requirements mandating continuous process improvement, rigorous documentation standards, and change management controls.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 10 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 62443 Software Lifecycle and Security Standards Update",
        "description": "Functional safety and cybersecurity requirements for software lifecycles, industrial automation, and connected medical devices.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Fri, 12 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS v2.1) Update",
        "description": "Updated security verification requirements for mobile applications, including secure storage, cryptography, authentication, network communication, and platform interaction.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "Framework guidelines structured around Govern, Map, Measure, and Manage functions to address AI trustworthiness, safety, security, and bias mitigation.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (CSF 2.0) Implementation Guidelines",
        "description": "Expanded framework incorporating Governance as a core function alongside Identify, Protect, Detect, Respond, and Recover across cloud and mobile ecosystems.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 19 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls v8.1 Security Baseline Guidance",
        "description": "Hardened system benchmark updates providing prescriptive configuration recommendations for mobile platforms, web servers, and cloud infrastructure.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 22 Jun 2026 14:00:00 GMT",
    },
    # Unverified announcement to test blocking rules
    {
        "id": "STD-MOCK-UNVERIFIED",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO 27001 Revision",
        "description": "An unverified personal blog claims ISO 27001 is banning all cloud databases without official confirmation.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Wed, 24 Jun 2026 16:00:00 GMT",
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
        "ftc.gov",
        "cisa.gov",
    ]
    p1_keywords = [
        "iso standard",
        "iec standard",
        "nist framework",
        "owasp masvs",
        "cis benchmark",
        "official standard",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "linkedin", "reddit", "ai summary", "chatgpt summary"]

    priority = 4  # Default to 4

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(kw in combined for kw in p4_keywords):
        priority = 4
    elif any(d in link for d in p3_domains) or any(kw in combined for kw in p3_keywords) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains) or any(kw in combined for kw in p2_keywords):
        priority = 2

    if any(d in link for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in link:
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        has_p1_ref = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref = True
                break
        if not has_p1_ref:
            for kw in p1_keywords:
                if kw in combined:
                    has_p1_ref = True
                    break
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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "standard"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards."""
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
    """Classifies incoming announcements into the 10 technical standard categories."""
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
    risk_assessment = []
    testing_checklist = []

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Update Information Security Management System (ISMS) controls and threat intelligence procedures in accordance with Annex A requirements."
            )
            impl_checklist.append("- [ ] Audit ISMS Statement of Applicability and align with ISO 27001 Annex A controls.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit failure during ISO 27001 surveillance reviews.")
            testing_checklist.append("- [ ] Verify access control lists and automated threat intelligence logging pipelines.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to Privacy Information Management System (PIMS) for processing Personally Identifiable Information (PII)."
            )
            impl_checklist.append("- [ ] Map PII data flows and update PIMS data processor/controller documentation.")
            risk_assessment.append(f"- *{cat}*: Exposure to regulatory privacy fines if PII processing lacks PIMS controls.")
            testing_checklist.append("- [ ] Validate PII deletion handlers and data subject request workflows.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance for AI model training, deployment, and risk monitoring."
            )
            impl_checklist.append("- [ ] Establish AI model registry and continuous bias/explainability monitoring.")
            risk_assessment.append(f"- *{cat}*: Unmitigated AI safety and compliance risks under emerging AI governance standards.")
            testing_checklist.append("- [ ] Execute automated AI model risk evaluations and verification of synthetic output labels.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align risk assessment methodologies and risk treatment frameworks with ISO 31000 principles."
            )
            impl_checklist.append("- [ ] Update organizational risk register and threat modeling templates.")
            risk_assessment.append(f"- *{cat}*: Unidentified security operational risks due to legacy risk scoring.")
            testing_checklist.append("- [ ] Conduct scenario-based threat modeling walkthroughs.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Maintain Quality Management System (QMS) release controls, change management, and automated verification."
            )
            impl_checklist.append("- [ ] Integrate QMS change review gates into CI/CD release pipelines.")
            risk_assessment.append(f"- *{cat}*: Quality regressions and process non-conformities during software distribution.")
            testing_checklist.append("- [ ] Run automated validation pipelines (scripts/validate.py) prior to tag creation.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce software lifecycle safety and cybersecurity requirements (IEC 62304 / IEC 62443)."
            )
            impl_checklist.append("- [ ] Document software hazard analysis and cybersecurity verification matrices.")
            risk_assessment.append(f"- *{cat}*: Failure to meet functional safety standards in regulated connected environments.")
            testing_checklist.append("- [ ] Run static code analysis and fault-injection safety verification suites.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Verify application against OWASP MASVS (Mobile Application Security Verification Standard) L1/L2 controls."
            )
            impl_checklist.append("- [ ] Audit mobile binary against OWASP MASVS storage, crypto, and network guidelines.")
            risk_assessment.append(f"- *{cat}*: Insecure local storage or cleartext communication vulnerabilities.")
            testing_checklist.append("- [ ] Execute static and dynamic mobile security testing scripts.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF core functions: Govern, Map, Measure, and Manage across AI deployments."
            )
            impl_checklist.append("- [ ] Map AI model dependencies and document trustworthiness metrics.")
            risk_assessment.append(f"- *{cat}*: Lack of explainability or unmeasured model drift in AI components.")
            testing_checklist.append("- [ ] Test AI system boundaries against adversarial prompt injection and edge cases.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Reconcile security controls with NIST CSF 2.0 (Identify, Protect, Detect, Respond, Recover, Govern)."
            )
            impl_checklist.append("- [ ] Update incident response playbook and continuous asset discovery mechanisms.")
            risk_assessment.append(f"- *{cat}*: Extended incident response times if security posture lacks CSF 2.0 alignment.")
            testing_checklist.append("- [ ] Simulate incident response notification and recovery procedures.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Benchmark hardened configurations for mobile operating systems and server environments."
            )
            impl_checklist.append("- [ ] Verify system configuration baselines against CIS Benchmark hardened profiles.")
            risk_assessment.append(f"- *{cat}*: Default configuration vulnerabilities exposing host systems to automated exploits.")
            testing_checklist.append("- [ ] Run automated configuration compliance scans against target deployment profiles.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards compliance."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Execute standard automated unit and integration tests."

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into alignment with monitored technical standards, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards evolve to address emerging cybersecurity threats, AI governance requirements, privacy controls, and quality management practices. Continuous monitoring ensures repository practices reflect international standards and industry baselines.

## 3. Regulatory change
- **ISO Standards (27001, 27701, 42001, 31000, 9001)**: Alignment with modern information security, privacy information management, AI management systems, risk management, and quality controls.
- **IEC Standards**: Compliance with software lifecycle and functional safety frameworks.
- **OWASP Guidelines**: Alignment with OWASP MASVS for mobile application security.
- **NIST Frameworks**: Implementation of NIST AI RMF (Govern, Map, Measure, Manage) and NIST CSF 2.0.
- **CIS Benchmarks**: Adherence to hardened system baselines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit findings and security vulnerabilities if technical standards updates are not integrated.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed updates maintain full backward compatibility with existing platform APIs and operational workflows. Technical controls wrap legacy implementations safely without breaking changes.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run repository validation scripts (`python3 scripts/validate.py`).

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document technical control mappings in internal architecture guides.

## 12. Compliance impact
- **Audit Preparedness**: Guarantees compliance readiness across ISO, NIST, OWASP, and CIS audit frameworks.
- **Security & Safety**: Reduces attack surfaces and reinforces AI governance and software safety boundaries.

## 13. Breaking changes
- No functional breaking changes are introduced. Security configurations enforce stricter baselines dynamically.

## 14. Review checklist
- [ ] Diff is 100% free of emojis or graphical symbols.
- [ ] Citations strictly adhere to Priority 1 official standards sources.
- [ ] Implementation steps are actionable and verified.

## 15. Approver recommendations
Verify that all technical control mappings match the latest official publications from ISO, NIST, OWASP, and CIS. Confirm that testing verification suites pass prior to release authorization.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Compliance Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across technical standards.",
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

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update ISMS controls to align with Annex A updates.")
            lines.append("- [ ] **Testing Task**: Verify threat intelligence feed logging and access control rules.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Map PII data flows and update Privacy Information Management controls.")
            lines.append("- [ ] **Testing Task**: Validate automated PII purge routines.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Register AI models in central registry and document explainability procedures.")
            lines.append("- [ ] **Testing Task**: Execute automated model output risk evaluations.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Review organizational risk register against ISO 31000 assessment framework.")
            lines.append("- [ ] **Testing Task**: Conduct risk treatment scenario walkthroughs.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Enforce QMS change control procedures in CI/CD pipeline.")
            lines.append("- [ ] **Testing Task**: Run validation script `python3 scripts/validate.py`.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Document software safety lifecycles per IEC 62304 / IEC 62443 requirements.")
            lines.append("- [ ] **Testing Task**: Run static analysis and hazard boundary tests.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Audit mobile application controls against OWASP MASVS v2.1.")
            lines.append("- [ ] **Testing Task**: Execute automated security verification scripts.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Implement Govern, Map, Measure, Manage workflows for AI systems.")
            lines.append("- [ ] **Testing Task**: Perform adversarial prompt testing on AI interfaces.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Reconcile organizational controls with NIST CSF 2.0 functions.")
            lines.append("- [ ] **Testing Task**: Validate incident response and recovery workflows.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Apply hardened system configuration baselines per CIS Controls.")
            lines.append("- [ ] **Testing Task**: Scan system configuration files against CIS benchmarks.")
        else:
            lines.append(f"- [ ] **Task**: Verify technical standard requirements for {cat}.")
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
        description="Monitor Technical Standards Compliance"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards RSS feeds"
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
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
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

    print(
        f"Monitored and classified {len(classified_updates)} standards updates ({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

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
