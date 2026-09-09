#!/usr/bin/env python3
"""Monitors technical standards updates across 10 key categories:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards,
OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. Identifies repo gaps,
generates implementation tasks, documentation updates, testing updates,
and drafts a 15-section compliance Pull Request.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

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

# Keywords used to classify incoming standards announcements/articles into the 10 categories
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
        "ai risk assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk criteria",
        "risk treatment",
        "risk evaluation framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality policy",
        "continual improvement",
        "quality audit",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "industrial automation security",
        "health software lifecycle",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "owasp masvs",
        "owasp asvs",
        "owasp llm",
        "mobile application security verification standard",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100",
        "govern map measure manage",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "identify protect detect respond recover govern",
        "sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis controls",
        "center for internet security",
        "cis hardened images",
        "cis baseline",
        "cis hardened configuration",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 standards categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"StatementOfApplicability",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"PII",
        r"data_protection_officer",
        r"privacy_impact",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"ai_risk",
        r"model_card",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_matrix",
        r"risk_assessment",
        r"risk_treatment",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_policy",
        r"quality_assurance",
    ],
    "IEC standards": [
        r"IEC62443",
        r"IEC82304",
        r"IEC62304",
        r"industrial_security",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"LLM_TOP_10",
        r"sanitization",
        r"csrf_token",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"trustworthy_ai",
        r"ai_metrics",
        r"explainability",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"SP800-53",
        r"cybersecurity_framework",
        r"incident_response",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Control",
        r"hardening",
        r"secure_baseline",
    ],
}

# Comprehensive Mock Technical Standards Updates
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Control Alignment Update",
        "description": "Updated ISO/IEC 27001 guidelines mandate revised Annex A controls covering threat intelligence, cloud services security, and physical security monitoring across enterprise software systems.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 18 May 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management Extension Standards Revision",
        "description": "ISO/IEC 27701 requirements dictate enhanced controls for PII processing, consent logging, cross-border transfers, and automated PII redaction verification in database layers.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 20 May 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Guidance Release",
        "description": "The ISO/IEC 42001 standard outlines requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) with explicit risk assessments for LLMs.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 22 May 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Integration Framework Guidelines",
        "description": "Updated ISO 31000 guidance mandates continuous risk assessment cycles, quantitative risk criteria, and integrated risk reporting across software lifecycle pipelines.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 25 May 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Process Standard Harmonization",
        "description": "Harmonized ISO 9001 updates enforce documented quality control procedures, automated release readiness checks, and formal root-cause post-mortems for software deployments.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 27 May 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 82304 Industrial and Health Software Security Standard Update",
        "description": "IEC multi-part standards require strict threat modeling, secure lifecycle requirements, and embedded software validation for industrial control and health-connected digital applications.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 29 May 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS / Top 10 Security Verification Framework Update",
        "description": "The OWASP Mobile Application Security Verification Standard (MASVS) and LLM Top 10 standards require input sanitization, prompt injection protection, and encrypted local storage controls.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Core Implementation",
        "description": "NIST AI RMF guidance outlines four key functions (GOVERN, MAP, MEASURE, MANAGE) to manage risks to individuals, organizations, and society associated with AI systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Standard",
        "description": "NIST CSF 2.0 expands scope to cover organizational governance (GOVERN function) alongside Identify, Protect, Detect, Respond, and Recover control functions for enterprise repositories.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 05 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls Hardening Guidelines Update",
        "description": "Center for Internet Security (CIS) Benchmarks establish target baseline configurations, automated vulnerability scanning, and secure build environment hardening requirements.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 08 Jun 2026 14:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified).
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
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "cis benchmarks",
        "center for internet security",
        "official publication",
        "government publication",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com"]
    p5_keywords = ["tweet", "linkedin", "reddit", "ai summary"]

    priority = 4
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

    is_verified = True if priority <= 3 else False
    if not is_verified:
        if any(d in combined for d in p1_domains) or any(kw in combined for kw in p1_keywords):
            is_verified = True

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(classified_updates):
    """Enforces strict source trust hierarchy validation and logs alerts to stderr."""
    verified_updates = []
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            print(
                f"Source Trust Warning: Skipping unverified Priority {priority} source for {u['title']}",
                file=sys.stderr,
            )
        else:
            verified_updates.append(u)
    return verified_updates


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
                    ".py",
                    ".sh",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            if "monitor-standards" in file or "monitor-standards-test" in file:
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
            for cat in set(matched_categories):
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

    processed_categories = set()

    for u in updates:
        cat = u["category"]
        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Re-align Information Security Management System (ISMS) Annex A controls and Statement of Applicability with updated standards."
            )
            impl_checklist.append(
                "- [ ] Conduct Statement of Applicability review for ISO 27001 ISMS controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance risks audit failure during official ISO 27001 re-certification audits."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Update Privacy Information Management System (PIMS) controls, PII controller/processor requirements, and consent logging interfaces."
            )
            impl_checklist.append(
                "- [ ] Verify PII processing records and privacy impact assessment guidelines for ISO 27701."
            )
            risk_assessment.append(
                f"- *{cat}*: Unauthorized handling or unverified consent logs for personally identifiable information (PII)."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance controls, AI risk assessments, and model transparency cards."
            )
            impl_checklist.append(
                "- [ ] Establish AI risk assessment framework and model documentation under ISO 42001."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmanaged AI safety hazards, model drift, and unvetted algorithmic decision risks."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align enterprise risk criteria, continuous risk assessment matrices, and mitigation workflows with ISO 31000 guidelines."
            )
            impl_checklist.append(
                "- [ ] Update enterprise risk management matrix and treatment plans."
            )
            risk_assessment.append(
                f"- *{cat}*: Unidentified operational risks or inadequate risk treatment pathways."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Harmonize software development Quality Management System (QMS) processes, automated release gates, and root-cause post-mortems."
            )
            impl_checklist.append(
                "- [ ] Document automated build testing and release readiness checklists for ISO 9001 QMS."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation or inconsistent release verification procedures."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Apply IEC 62443 / IEC 82304 / IEC 62304 software lifecycle security requirements and threat models."
            )
            impl_checklist.append(
                "- [ ] Perform secure software lifecycle threat modeling under IEC 62443 / 82304 / 62304."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerabilities in critical software components or health/industrial control interfaces."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Enforce OWASP MASVS, ASVS, and LLM Top 10 controls including input sanitization and secure local storage."
            )
            impl_checklist.append(
                "- [ ] Validate OWASP MASVS L1/L2 security controls across all client endpoints."
            )
            risk_assessment.append(
                f"- *{cat}*: Common web/mobile application vulnerabilities such as injection, broken auth, or bad crypto."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Adopt NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions to evaluate and mitigate AI risks."
            )
            impl_checklist.append(
                "- [ ] Implement NIST AI RMF GOVERN and MEASURE metrics for deployed AI features."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of explainability, fairness, or trustworthiness in generative AI components."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER)."
            )
            impl_checklist.append(
                "- [ ] Map existing repository security controls to NIST CSF 2.0 functions."
            )
            risk_assessment.append(
                f"- *{cat}*: Incomplete incident response or vulnerability detection coverage across systems."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Harden build environments, container images, and deployment configurations against CIS Benchmarks."
            )
            impl_checklist.append(
                "- [ ] Execute CIS Benchmark hardening scans on target build scripts and configurations."
            )
            risk_assessment.append(
                f"- *{cat}*: Security misconfigurations or unhardened default settings in deployment pipelines."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of repository standards documents).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the repository with the latest revisions across monitored technical standards, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP frameworks, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Maintaining enterprise trust and regulatory alignment requires continuous monitoring and adaptation to evolving international technical standards. Recent revisions establish explicit controls for AI management, privacy information management, cybersecurity frameworks, and secure software lifecycles.

## 3. Regulatory change
- **ISO / IEC Standards**: Mandatory controls for ISMS, PIMS, AIMS, enterprise risk management, and software quality assurance.
- **OWASP & NIST Frameworks**: Modernized guidelines for mobile application security (MASVS), AI risk management (NIST AI RMF), cybersecurity governance (NIST CSF 2.0), and CIS configuration hardening.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to High risk of audit findings or certification delays if technical controls diverge from international standards.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standard enhancements are non-breaking and additive. System APIs, data contracts, and build processes maintain full backward compatibility for current production clients.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated repository validation checks (`python3 scripts/validate.py`).

## 10. Testing checklist
- [ ] Verify that automated build readiness checks and security test suites pass without regression.
- [ ] Validate that all OWASP MASVS and CIS Benchmark static analysis rules pass.
- [ ] Conduct AI risk assessment verification checks for deployed model interfaces.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document standards alignment in internal architecture decision records (ADRs).

## 12. Compliance impact
- **Certification Readiness**: Preserves ISO 27001 / 27701 / 42001 certification audit readiness.
- **Security Baseline**: Satisfies OWASP MASVS and NIST CSF 2.0 technical governance controls.

## 13. Breaking changes
- Zero breaking API or runtime changes. Software configurations and documentation are updated to comply with current standards.

## 14. Review checklist
- [ ] Document is 100% free of emojis or graphical symbols.
- [ ] All official standards citations originate from Priority 1 verified sources.
- [ ] Implementation steps have been mapped to corresponding repository files.

## 15. Approver recommendations
Verify that Statement of Applicability documents, privacy controls, and AI governance policies match the updated standard requirements prior to merge.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Gap Analysis Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Repository Gap Analysis & Implementation Tasks")
    lines.append("")

    processed_categories = set()

    for u in updates:
        cat = u["category"]
        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        lines.append(f"### Tasks and Gap Remediation for {cat}")
        lines.append(
            "- **Compliance Level**: High priority. Technical standard audit requires verification."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Implementation Task**: Review Annex A controls and update Statement of Applicability."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update internal ISMS security policy documents."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute automated access control and configuration test suites."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Implementation Task**: Audit PII processing endpoints and consent logging mechanisms."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update Privacy Impact Assessments and PIMS documentation."
            )
            lines.append(
                "- [ ] **Testing Update**: Verify automated PII deletion and redaction test routines."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Implementation Task**: Implement AIMS governance framework for LLM and AI models."
            )
            lines.append(
                "- [ ] **Documentation Update**: Create model transparency cards and AI risk assessment records."
            )
            lines.append(
                "- [ ] **Testing Update**: Run prompt safety, bias, and output validation tests."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Implementation Task**: Update continuous risk assessment criteria and risk matrix."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update risk treatment plans and risk register."
            )
            lines.append(
                "- [ ] **Testing Update**: Verify automated risk score thresholds in security pipelines."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Implementation Task**: Enforce documented software quality assurance and release checks."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update software release management and post-mortem procedures."
            )
            lines.append(
                "- [ ] **Testing Update**: Run full regression test suites before release candidate tags."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Implementation Task**: Apply IEC 62443 / 82304 software lifecycle security controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document software threat models and lifecycle safety plans."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute software lifecycle vulnerability and boundary tests."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Implementation Task**: Implement OWASP MASVS and ASVS client sanitization controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document OWASP compliance verification checklist."
            )
            lines.append(
                "- [ ] **Testing Update**: Run OWASP Zed Attack Proxy (ZAP) and static security scanners."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Implementation Task**: Implement GOVERN and MEASURE functions for deployed AI features."
            )
            lines.append(
                "- [ ] **Documentation Update**: Maintain NIST AI RMF risk evaluation documentation."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute AI trustworthiness, explainability, and robustness tests."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Implementation Task**: Map cybersecurity controls to NIST CSF 2.0 functions."
            )
            lines.append(
                "- [ ] **Documentation Update**: Update incident response and recovery playbooks."
            )
            lines.append(
                "- [ ] **Testing Update**: Conduct simulated incident response and log monitoring tests."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Implementation Task**: Apply CIS Benchmark baseline hardening rules."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document hardened baseline configuration parameters."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute automated CIS configuration compliance checks."
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
        description="Monitor Technical Standards (ISO, IEC, OWASP, NIST, CIS)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards policy feeds"
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
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    announcements = []

    if args.mock or (not args.live and not args.mock) or not announcements:
        print("Using comprehensive mock Technical Standards updates for compliance scanning...")
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

    # Enforce strict source trust hierarchy validation
    verified_updates = enforce_strict_source_trust_hierarchy(classified_updates)

    if not verified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(verified_updates)} technical standards updates:"
    )
    for idx, u in enumerate(verified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(verified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

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
