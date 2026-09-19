#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards categories (ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks).
Identifies repository gaps, generates implementation tasks, documentation updates,
and testing updates, drafting a 15-section compliance Pull Request.
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
        "information security management",
        "isms",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management",
        "pims",
        "personally identifiable information",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai risk management standard",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment framework",
        "enterprise risk management",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance standard",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "international electrotechnical commission",
        "functional safety",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "asvs",
        "open web application security project",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "trustworthy ai",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "nist csf 2.0",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis hardening",
        "cis level 1",
        "cis level 2",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO 27001",
        r"ISMS",
        r"access_control_policy",
        r"information_security",
        r"security_incident",
    ],
    "ISO 27701": [
        r"ISO 27701",
        r"PIMS",
        r"PII",
        r"privacy_impact_assessment",
        r"data_controller",
    ],
    "ISO 42001": [
        r"ISO 42001",
        r"AIMS",
        r"ai_governance",
        r"llm_audit",
        r"model_card",
    ],
    "ISO 31000": [
        r"ISO 31000",
        r"risk_matrix",
        r"risk_register",
        r"risk_assessment",
    ],
    "ISO 9001": [
        r"ISO 9001",
        r"QMS",
        r"quality_audit",
        r"continuous_improvement",
    ],
    "IEC standards": [
        r"IEC 62443",
        r"IEC 82304",
        r"IEC 62304",
        r"IEC",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"top_10",
        r"sanitization",
    ],
    "NIST AI RMF": [
        r"NIST AI RMF",
        r"AI RMF",
        r"trustworthy_ai",
        r"ai_bias_check",
    ],
    "NIST CSF": [
        r"NIST CSF",
        r"CSF 2\.0",
        r"cybersecurity_framework",
        r"incident_response",
    ],
    "CIS Benchmarks": [
        r"CIS Benchmark",
        r"CIS_Hardening",
        r"hardened_config",
        r"cis_level",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CISecurity, European Commission, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# 10 Comprehensive Mock Announcements for all 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Management System Controls Update",
        "description": "ISO published updated guidance on mandatory Annex A security controls, emphasizing threat intelligence, cloud services security, and secure coding practices across digital assets.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management Extension Refinements",
        "description": "ISO releases refined PIMS guidance aligning data processor and controller responsibilities with international data protection frameworks, enforcing strict PII mapping and consent tracking.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Management System (AIMS) Requirements",
        "description": "ISO mandates continuous risk management, bias evaluation, transparency declarations, and model impact assessments for entities deploying artificial intelligence systems.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Implementation Framework",
        "description": "ISO updates the risk assessment framework to integrate cybersecurity and digital operational resilience into overall corporate risk treatment strategies.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Digital Software Guidance",
        "description": "ISO releases updated guidance on applying ISO 9001 quality assurance principles to modern agile software release cycles and automated integration pipelines.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 82304 Software Lifecycle and Functional Safety Guidelines",
        "description": "The International Electrotechnical Commission updates software lifecycle requirements for secure development and system integrity across interconnected digital products.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 Mobile and Web Verification Standards (MASVS / ASVS) Release",
        "description": "OWASP updates MASVS and ASVS specifications, adding strict requirements for client-side API security, token encryption in transit, and dynamic runtime protection.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT",
    },
    {
        "id": "STD-MOCK-NIST-AIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 (NIST AI 100-1) Compliance Standard",
        "description": "NIST publishes actionable metrics for the Govern, Map, Measure, and Manage functions of the AI RMF, focusing on trustworthy AI, hallucination mitigation, and model provenance.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT",
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (CSF 2.0) Govern Function Implementation",
        "description": "NIST CSF 2.0 expands coverage to all organizations, introducing the Govern function to ensure executive oversight, continuous supply chain risk management, and formal security policies.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Level 1 and Level 2 Hardening Guidelines Update",
        "description": "Center for Internet Security updates benchmark recommendations for containerized environments, cloud infrastructure, and mobile client operating systems.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "OWASP",
        "title": "Unverified Blog Claiming Imminent OWASP Policy Bans",
        "description": "An unverified industry blog speculates on upcoming OWASP changes without official citations. This is a secondary blog post.",
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
        "ico.org.uk",
        "gov.uk",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open web application security project",
        "center for internet security",
        "european commission",
        "cisa",
        "ftc",
        "nist ai rmf",
        "nist csf",
        "iso/iec",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "IEEE.org"]
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
        has_p1_ref = any(d in combined for d in p1_domains) or any(
            kw in combined for kw in p1_keywords
        )
        if has_p1_ref or ".gov" in combined:
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
                    overlap = words.intersection(other_words).intersection(
                        {"iso", "nist", "owasp", "cis", "iec", "security"}
                    )
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards categories.
    Returns matching files to identify repository gaps.
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
                    ".py",
                    ".sh",
                    ".yaml",
                    ".yml",
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
    risk_assessment = []

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
                f"- **{cat}**: Align information security policies and Annex A control mappings with ISO/IEC 27001:2022 standards."
            )
            impl_checklist.append("- [ ] Audit Annex A control mapping and update information security policies.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit findings during formal ISMS certification reviews.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS controls to PIMS by documenting PII controller and processor roles and data flow inventories."
            )
            impl_checklist.append("- [ ] Map PII data flows and update Privacy Information Management System documentation.")
            risk_assessment.append(f"- *{cat}*: Unmapped PII processing risks regulatory penalties under global privacy statutes.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish an Artificial Intelligence Management System (AIMS) framework covering model cards, bias audits, and risk tracking."
            )
            impl_checklist.append("- [ ] Publish AI model cards and integrate AIMS continuous risk tracking into AI features.")
            risk_assessment.append(f"- *{cat}*: AI safety and governance failures leading to algorithmic harm or regulatory sanctions.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Update enterprise risk assessment registers and risk matrices following ISO 31000 guidelines."
            )
            impl_checklist.append("- [ ] Update the risk register with current cybersecurity and digital operational risk vectors.")
            risk_assessment.append(f"- *{cat}*: Incomplete risk identification leaving key operational dependencies unmitigated.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Integrate ISO 9001 quality assurance controls into continuous integration pipelines and deployment testing."
            )
            impl_checklist.append("- [ ] Verify quality gates and automated testing coverage in CI workflows.")
            risk_assessment.append(f"- *{cat}*: Software quality degradation impacting release readiness and customer SLAs.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align software development lifecycle procedures with IEC 62443 / IEC 82304 functional safety guidelines."
            )
            impl_checklist.append("- [ ] Document software lifecycle safety verification steps for embedded and client components.")
            risk_assessment.append(f"- *{cat}*: Functional safety vulnerabilities in critical software operational environments.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Validate client and API endpoints against OWASP MASVS and ASVS security verification standards."
            )
            impl_checklist.append("- [ ] Verify OWASP MASVS controls for network security, authentication, and code resilience.")
            risk_assessment.append(f"- *{cat}*: Susceptibility to top web and mobile application security vulnerabilities.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF core functions (Govern, Map, Measure, Manage) across generative and predictive AI workflows."
            )
            impl_checklist.append("- [ ] Complete NIST AI RMF Govern and Measure checklists for all production AI integrations.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI model output leading to bias, hallucination, or untrusted decisions.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map technical security controls to NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append("- [ ] Update incident response protocols and security governance controls to match CSF 2.0.")
            risk_assessment.append(f"- *{cat}*: Gaps in security posture visibility during incident detection and response.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce CIS Level 1 and Level 2 hardening benchmarks across build targets, containers, and deployment setups."
            )
            impl_checklist.append("- [ ] Run automated CIS benchmark hardening scans on build environment configurations.")
            risk_assessment.append(f"- *{cat}*: Misconfigured system defaults exposing infrastructure to unauthorized access.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, documentation, and technical updates to bring the repository into complete alignment with monitored international technical standards. It addresses repository gaps across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Compliance with technical standards provides assurance of information security, privacy management, AI governance, software quality, and infrastructure hardening. Automated monitoring detects changes in international standards and verifies repository controls to prevent compliance gaps.

## 3. Regulatory change
- **ISO/IEC Standards**: Updates to ISO 27001 (ISMS), ISO 27701 (PIMS), ISO 42001 (AIMS), ISO 31000 (Risk Management), ISO 9001 (Quality Management), and IEC software lifecycle standards.
- **OWASP Frameworks**: Alignment with OWASP MASVS and ASVS client/server security requirements.
- **NIST Frameworks**: Alignment with NIST AI RMF (NIST AI 100-1) and NIST CSF 2.0 governance controls.
- **CIS Benchmarks**: Enforced OS, container, and configuration hardening benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and audit risk if technical standards controls are unmapped or unverified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standards updates maintain complete backward compatibility across supported platform targets and existing API interfaces.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Execute automated standards compliance verification scans.

## 10. Testing checklist
- [ ] Verify that information security control mappings match ISO 27001 Annex A guidelines.
- [ ] Perform static OWASP MASVS code analysis and verify zero high/critical findings.
- [ ] Validate NIST AI RMF model cards and bias check logs for production AI endpoints.
- [ ] Run automated build validation checks (`python3 scripts/validate.py`).

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with implementation status.
- [ ] Document AI governance practices in accordance with ISO 42001 and NIST AI RMF.
- [ ] Document incident response procedures mapped to NIST CSF 2.0.

## 12. Compliance impact
- **Audit Preparedness**: Prepares the organization for ISO/IEC certification audits and customer security questionnaires.
- **Security Posture**: Strengthens application resilience against OWASP Top 10 vulnerabilities.
- **AI Governance**: Ensures transparent and trustworthy AI deployments compliant with ISO 42001 and NIST AI RMF.

## 13. Breaking changes
- No breaking software changes introduced. Hardened configurations enforce strict defaults for unauthenticated endpoints.

## 14. Review checklist
- [ ] Verification that code and documentation diffs are 100% emoji-free.
- [ ] Verification that all citations point to Priority 1 official standards bodies.
- [ ] Verification that security controls match CIS Benchmarks.

## 15. Approver recommendations
Verify that the technical controls documented in `docs/STANDARDS-POLICY-MIGRATION.md` have been verified against active deployment configurations before release authorization.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md
    with implementation tasks, documentation updates, and testing updates.
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
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations, Implementation Tasks, and Testing Updates")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks and Testing Updates for {cat}")
        lines.append("- **Regulatory Impact**: High priority technical standard compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Implementation Task**: Audit Annex A controls and update information security policies.")
            lines.append("- [ ] **Documentation Update**: Update ISMS documentation and access control matrices.")
            lines.append("- [ ] **Testing Update**: Run security policy static compliance checks.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Implementation Task**: Document PII controller and processor data flows.")
            lines.append("- [ ] **Documentation Update**: Update Privacy Information Management System (PIMS) manual.")
            lines.append("- [ ] **Testing Update**: Verify user consent logs and PII access controls.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Implementation Task**: Establish AIMS framework for AI models and features.")
            lines.append("- [ ] **Documentation Update**: Publish AI model cards and impact assessment reports.")
            lines.append("- [ ] **Testing Update**: Execute automated AI bias and output safety tests.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Implementation Task**: Update enterprise risk register with digital operational risks.")
            lines.append("- [ ] **Documentation Update**: Update risk treatment plans and threat matrices.")
            lines.append("- [ ] **Testing Update**: Validate risk mitigation controls in CI workflow.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Implementation Task**: Integrate QMS continuous quality gates into release pipelines.")
            lines.append("- [ ] **Documentation Update**: Update release engineering and quality assurance guidelines.")
            lines.append("- [ ] **Testing Update**: Run full regression test suite with automated code coverage check.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Implementation Task**: Align software lifecycle procedures with IEC 62443 / IEC 82304.")
            lines.append("- [ ] **Documentation Update**: Document software functional safety architecture.")
            lines.append("- [ ] **Testing Update**: Execute static code analysis and boundary safety testing.")
        elif cat == "OWASP":
            lines.append("- [ ] **Implementation Task**: Validate codebase against OWASP MASVS and ASVS controls.")
            lines.append("- [ ] **Documentation Update**: Update application security verification checklist.")
            lines.append("- [ ] **Testing Update**: Run automated OWASP vulnerability scanners and dependency audit.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Implementation Task**: Implement Govern, Map, Measure, and Manage functions for AI.")
            lines.append("- [ ] **Documentation Update**: Publish NIST AI RMF compliance crosswalk.")
            lines.append("- [ ] **Testing Update**: Run AI output hallucination and robustness test cases.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Implementation Task**: Map incident response and security controls to NIST CSF 2.0.")
            lines.append("- [ ] **Documentation Update**: Update Cybersecurity Framework governance manual.")
            lines.append("- [ ] **Testing Update**: Execute simulated security incident response drills.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Implementation Task**: Apply CIS Level 1/2 hardening to build configurations.")
            lines.append("- [ ] **Documentation Update**: Document CIS benchmark compliance baseline.")
            lines.append("- [ ] **Testing Update**: Run automated CIS benchmark compliance auditing scripts.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all technical criteria for {cat} are checked.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation report updated successfully at: {output_filepath}")
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
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

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
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
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
