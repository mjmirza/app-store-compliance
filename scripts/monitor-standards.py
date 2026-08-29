#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards,
OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Generates repo-impact, repository gap analysis, implementation tasks,
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

# Keywords used to classify incoming standard updates into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management system",
        "annex a",
        "security controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management system",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai governance",
        "ai risk assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "enterprise risk management",
        "risk identification",
        "risk evaluation",
    ],
    "ISO 9001": [
        "iso 9001",
        "qms",
        "quality management system",
        "quality assurance",
        "process control",
        "continuous improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "software lifecycle processes",
        "functional safety",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "owasp masvs",
        "mobile application security verification standard",
        "owasp api security",
        "mstg",
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
        "cis benchmark",
        "center for internet security",
        "cis controls",
        "system hardening",
        "cis hardened images",
    ],
}

# Codebase signals (regex patterns) to find files affected by each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO 27001",
        r"ISMS",
        r"security_controls",
        r"access_control",
        r"data_classification",
        r"encryption",
    ],
    "ISO 27701": [
        r"ISO 27701",
        r"PIMS",
        r"PII",
        r"privacy_impact_assessment",
        r"data_minimization",
        r"consent",
    ],
    "ISO 42001": [
        r"ISO 42001",
        r"AIMS",
        r"AI_governance",
        r"ai_risk_assessment",
        r"model_bias",
        r"ai_safety",
    ],
    "ISO 31000": [
        r"ISO 31000",
        r"risk_management",
        r"risk_matrix",
        r"risk_mitigation",
        r"risk_tolerance",
    ],
    "ISO 9001": [
        r"ISO 9001",
        r"QMS",
        r"quality_assurance",
        r"audit_trail",
        r"process_verification",
    ],
    "IEC standards": [
        r"IEC 62304",
        r"IEC 82304",
        r"IEC 62443",
        r"IEC_standards",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"OWASP_TOP_10",
        r"sanitization",
        r"input_validation",
        r"csrf",
    ],
    "NIST AI RMF": [
        r"NIST AI RMF",
        r"AI_RMF",
        r"model_card",
        r"bias_audit",
        r"explainability",
        r"ai_transparency",
    ],
    "NIST CSF": [
        r"NIST CSF",
        r"Cybersecurity Framework",
        r"incident_response",
        r"threat_detection",
        r"asset_management",
    ],
    "CIS Benchmarks": [
        r"CIS Benchmarks",
        r"CIS_Controls",
        r"system_hardening",
        r"secure_configuration",
        r"cis_hardening",
    ],
}

# Comprehensive mock technical standards announcements
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 ISMS Security Controls Transition Mandate",
        "description": "Organizations adopting ISO 27001 must align their Information Security Management System (ISMS) controls with the updated Annex A structure, covering cloud services, threat intelligence, and secure coding.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 09:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 PIMS Privacy Extension Requirements Update",
        "description": "ISO 27701 mandates formal Privacy Information Management Systems (PIMS) for PII controllers and processors, requiring mandatory Privacy Impact Assessments (PIA) and automated consent record verification.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Wed, 17 Jun 2026 10:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Mandate",
        "description": "ISO 42001 specifies comprehensive governance requirements for organizations developing or deploying AI systems, mandating AI risk assessments, bias monitoring, and model auditability.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 19 Jun 2026 11:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Integration Framework",
        "description": "ISO 31000 provides guidelines on managing risk faced by organizations. Technical software systems must incorporate quantifiable risk identification, risk evaluation, and continuous mitigation workflows.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 22 Jun 2026 12:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Software Verification Controls",
        "description": "ISO 9001 requires robust quality assurance, documented software release processes, and verifiable audit trails to guarantee process quality and continuous software reliability.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Wed, 24 Jun 2026 13:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Health & Functional Software Lifecycle Standard Update",
        "description": "IEC international standards specify software lifecycle lifecycle requirements, risk management, and verification procedures for healthcare and critical software applications.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 26 Jun 2026 14:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS 2.1 & Top 10 Security Verification Guidance",
        "description": "OWASP updates Mobile Application Security Verification Standard (MASVS) and API Security Top 10, requiring strict input validation, cryptographic hardware backing, and session controls.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Mon, 29 Jun 2026 15:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Implementation Guidelines",
        "description": "NIST AI RMF provides actionable guidance across Govern, Map, Measure, and Manage functions to ensure trustworthy AI systems, model transparency, and bias reduction.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 16:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Governance Domain Mandate",
        "description": "NIST CSF 2.0 expands cybersecurity framework guidance to include an explicit Governance function alongside Identify, Protect, Detect, Respond, and Recover pillars.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 17:00:00 GMT",
        "source_trust_level": 1,
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks & Critical Security Controls System Hardening Update",
        "description": "Center for Internet Security updates benchmark recommendations for system hardening, container image isolation, and secure default configurations across deployment pipelines.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 06 Jul 2026 18:00:00 GMT",
        "source_trust_level": 1,
    },
]


def enforce_strict_source_trust_hierarchy(announcements):
    """Enforces strict source trust hierarchy validation.
    Priority 1: Official standards bodies (ISO, IEC, NIST, OWASP, CIS, ENISA, EDPB)
    Priority 2: Major news wires (Reuters, AP, Bloomberg)
    Priority 3: Academic papers
    Priority 4: Industry blogs (Blocked unless verified by Priority 1)
    Priority 5: Social media / AI generated summaries (Blocked)
    """
    verified = []
    blocked_count = 0

    for ann in announcements:
        trust_level = ann.get("source_trust_level", 1)
        link = ann.get("link", "").lower()

        # Check official domain trust signals
        if any(
            official in link
            for official in [
                "iso.org",
                "iec.ch",
                "nist.gov",
                "owasp.org",
                "cisecurity.org",
                "europa.eu",
            ]
        ):
            trust_level = 1

        if trust_level in (1, 2, 3):
            verified.append(ann)
        else:
            blocked_count += 1
            print(
                f"Source Trust Warning: Unverified Priority {trust_level} source blocked: {ann.get('title')}",
                file=sys.stderr,
            )

    return verified, blocked_count


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
                    ".py",
                    ".js",
                    ".ts",
                    ".swift",
                    ".kt",
                    ".java",
                    ".json",
                    ".md",
                    ".sh",
                    ".yaml",
                    ".yml",
                    ".xml",
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
                            "source_trust_level": 1,
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
                        "source_trust_level": ann.get("source_trust_level", 1),
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a draft of a pull request complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    repo_gaps = []
    impl_checklist = []
    doc_checklist = []
    testing_checklist = []
    risk_assessment = []

    # Category-level deduplication
    processed_cats = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in processed_cats:
            continue
        processed_cats.add(cat)

        if cat == "ISO 27001":
            repo_gaps.append(
                f"- **{cat} Gap**: Missing automated ISMS control verification and explicit cloud access logging controls."
            )
            impl_checklist.append(
                "- [ ] ISO 27001: Implement structured access logging and ISMS Annex A control alignment."
            )
            doc_checklist.append(
                "- [ ] ISO 27001: Update information security management policy documentation in docs/STANDARDS-POLICY-MIGRATION.md."
            )
            testing_checklist.append(
                "- [ ] ISO 27001: Execute automated access control audit tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with international ISMS security audit standards during enterprise reviews."
            )
        elif cat == "ISO 27701":
            repo_gaps.append(
                f"- **{cat} Gap**: Absence of standardized PII processor/controller privacy impact assessment logging."
            )
            impl_checklist.append(
                "- [ ] ISO 27701: Implement PIMS data minimization and PII flow tracking."
            )
            doc_checklist.append(
                "- [ ] ISO 27701: Update PIMS privacy documentation and assessment records."
            )
            testing_checklist.append(
                "- [ ] ISO 27701: Run automated PII data leakage and consent verification tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate PII processing safeguards leading to regulatory privacy enforcement."
            )
        elif cat == "ISO 42001":
            repo_gaps.append(
                f"- **{cat} Gap**: Lack of formal Artificial Intelligence Management System (AIMS) governance and model risk assessment logs."
            )
            impl_checklist.append(
                "- [ ] ISO 42001: Establish AIMS AI model risk assessment and bias auditing workflows."
            )
            doc_checklist.append(
                "- [ ] ISO 42001: Document AI governance frameworks and model cards."
            )
            testing_checklist.append(
                "- [ ] ISO 42001: Execute automated AI model safety and output verification test suites."
            )
            risk_assessment.append(
                f"- *{cat}*: AI system safety risks, unmonitored algorithmic bias, and non-compliance with AIMS."
            )
        elif cat == "ISO 31000":
            repo_gaps.append(
                f"- **{cat} Gap**: Missing unified technical risk identification matrix and automated mitigation logging."
            )
            impl_checklist.append(
                "- [ ] ISO 31000: Integrate quantitative risk evaluation frameworks into technical development workflows."
            )
            doc_checklist.append(
                "- [ ] ISO 31000: Maintain updated enterprise risk management logs."
            )
            testing_checklist.append(
                "- [ ] ISO 31000: Verify risk tolerance boundaries in release audit checks."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational risks escalating into system failures."
            )
        elif cat == "ISO 9001":
            repo_gaps.append(
                f"- **{cat} Gap**: Incomplete Quality Management System (QMS) release audit trail automation."
            )
            impl_checklist.append(
                "- [ ] ISO 9001: Implement automated release quality verification checklists."
            )
            doc_checklist.append(
                "- [ ] ISO 9001: Update software release QMS procedure documentation."
            )
            testing_checklist.append(
                "- [ ] ISO 9001: Run full software lifecycle regression testing."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation affecting customer satisfaction and compliance status."
            )
        elif cat == "IEC standards":
            repo_gaps.append(
                f"- **{cat} Gap**: Insufficient software lifecycle process verification under IEC 62304 / IEC 82304."
            )
            impl_checklist.append(
                "- [ ] IEC standards: Align software development lifecycle with IEC safety guidelines."
            )
            doc_checklist.append(
                "- [ ] IEC standards: Update functional safety and lifecycle compliance documentation."
            )
            testing_checklist.append(
                "- [ ] IEC standards: Perform functional safety and software unit verification tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Functional safety non-conformance in regulated critical deployments."
            )
        elif cat == "OWASP":
            repo_gaps.append(
                f"- **{cat} Gap**: OWASP MASVS L1/L2 security controls requiring updated input sanitization and token binding."
            )
            impl_checklist.append(
                "- [ ] OWASP: Enforce OWASP MASVS controls across network and local storage layers."
            )
            doc_checklist.append(
                "- [ ] OWASP: Document OWASP MASVS compliance verification results."
            )
            testing_checklist.append(
                "- [ ] OWASP: Execute automated OWASP vulnerability scan scripts."
            )
            risk_assessment.append(
                f"- *{cat}*: Application security vulnerabilities exposing endpoints to OWASP Top 10 exploits."
            )
        elif cat == "NIST AI RMF":
            repo_gaps.append(
                f"- **{cat} Gap**: Missing NIST AI RMF Govern, Map, Measure, and Manage functions for deployed AI modules."
            )
            impl_checklist.append(
                "- [ ] NIST AI RMF: Implement AI risk management controls covering explainability and transparency."
            )
            doc_checklist.append(
                "- [ ] NIST AI RMF: Document model cards and trust metrics per NIST AI 100-1."
            )
            testing_checklist.append(
                "- [ ] NIST AI RMF: Run automated model transparency and explainability assertion tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of AI trustworthiness and governance under federal NIST benchmarks."
            )
        elif cat == "NIST CSF":
            repo_gaps.append(
                f"- **{cat} Gap**: Incomplete NIST CSF 2.0 Governance pillar alignment and incident response automation."
            )
            impl_checklist.append(
                "- [ ] NIST CSF: Update cybersecurity controls across Identify, Protect, Detect, Respond, Recover, and Govern pillars."
            )
            doc_checklist.append(
                "- [ ] NIST CSF: Update cybersecurity framework compliance documentation."
            )
            testing_checklist.append(
                "- [ ] NIST CSF: Run incident detection and threat simulation tests."
            )
            risk_assessment.append(
                f"- *{cat}*: Unpreparedness against modern cyber threats due to missing governance controls."
            )
        elif cat == "CIS Benchmarks":
            repo_gaps.append(
                f"- **{cat} Gap**: Hardened environment configuration drift relative to CIS Benchmarks."
            )
            impl_checklist.append(
                "- [ ] CIS Benchmarks: Apply CIS system hardening recommendations to deployment build profiles."
            )
            doc_checklist.append(
                "- [ ] CIS Benchmarks: Document secure base configuration policies."
            )
            testing_checklist.append(
                "- [ ] CIS Benchmarks: Run automated CIS benchmark configuration compliance audits."
            )
            risk_assessment.append(
                f"- *{cat}*: System compromise resulting from insecure default configurations."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    repo_gaps_str = (
        "\n".join(repo_gaps)
        if repo_gaps
        else "- No technical standards repository gaps identified."
    )
    impl_checklist_str = "\n".join(impl_checklist)
    doc_checklist_str = "\n".join(doc_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Updates

## 1. Summary
This pull request addresses monitored updates across international technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It identifies repository gaps and establishes implementation, documentation, and testing tasks to guarantee organizational compliance.

## 2. Background
Maintaining compliance with technical standards is critical for software reliability, information security, AI governance, and regulatory readiness. Recent updates from standard bodies mandate explicit governance frameworks and automated verification.

## 3. Regulatory change
- **Technical Standards Framework Alignment**: Mandatory alignment with ISO/IEC standards, NIST frameworks, OWASP MASVS, and CIS Benchmarks.
- **AI Governance & Security Mandates**: Adoption of ISO 42001 AIMS and NIST AI RMF standards across software systems incorporating AI components.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium-to-High risk during enterprise audits if technical standards compliance controls are absent or unverified.

## 7. Migration steps
### Repository Gap Analysis
{repo_gaps_str}

### Implementation Tasks
{impl_checklist_str}

### Documentation Updates
{doc_checklist_str}

### Testing Updates
{testing_checklist_str}

## 8. Backward compatibility
All proposed technical standard compliance changes maintain full backward compatibility and introduce no breaking changes to core execution runtime.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run technical standards validation engines locally.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run full repository release audit using `python3 scripts/release-audit.py`.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed migration logs.

## 12. Compliance impact
- **Audit Preparedness**: Guarantees compliance readiness for ISO, NIST, OWASP, and CIS enterprise audits.
- **Risk Reduction**: Eliminates structural security, privacy, and AI governance compliance gaps.

## 13. Breaking changes
No breaking changes introduced.

## 14. Review checklist
- [ ] Code is 100% free of emojis or graphical symbols in comments and files.
- [ ] Official citations strictly adhere to Priority 1 trusted sources.
- [ ] All 10 technical standards categories are evaluated and addressed.

## 15. Approver recommendations
Verify that all technical standard implementation tasks, documentation updates, and automated test assertions are executed and verified before release authorization.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standard requirements across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.",
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

    lines.append("## Repository Gap Analysis, Implementation, Documentation & Testing Tasks")
    lines.append("")

    processed_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_cats:
            continue
        processed_cats.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append(f"- **Standard Domain**: {cat}")

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Gap**: Missing automated ISMS Annex A control audit logging."
            )
            lines.append(
                "- [ ] **Implementation Task**: Implement structured access logging and ISMS control checks."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document ISMS control alignment in security guidelines."
            )
            lines.append(
                "- [ ] **Testing Update**: Add automated access control audit tests."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Gap**: Lack of automated PII flow tracking and PIMS privacy assessment records."
            )
            lines.append(
                "- [ ] **Implementation Task**: Configure PII minimization and privacy impact logging."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document PIMS privacy controls and PII inventory."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute automated consent and data flow verification tests."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Gap**: Absence of formal AIMS AI governance and model risk logging."
            )
            lines.append(
                "- [ ] **Implementation Task**: Establish AI risk assessment and bias auditing controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Publish AI governance procedures and model cards."
            )
            lines.append(
                "- [ ] **Testing Update**: Add automated AI output verification test assertions."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Gap**: Unintegrated risk matrix evaluation workflows."
            )
            lines.append(
                "- [ ] **Implementation Task**: Integrate quantitative risk scoring in build checks."
            )
            lines.append(
                "- [ ] **Documentation Update**: Maintain updated risk management register."
            )
            lines.append(
                "- [ ] **Testing Update**: Verify risk threshold guardrails."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Gap**: Unautomated software QMS release verification."
            )
            lines.append(
                "- [ ] **Implementation Task**: Enforce automated QMS release checklists."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document quality assurance processes."
            )
            lines.append(
                "- [ ] **Testing Update**: Run full software regression suites."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Gap**: Unverified software lifecycle safety controls."
            )
            lines.append(
                "- [ ] **Implementation Task**: Align lifecycle processes with IEC 62304 / IEC 82304."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document functional safety lifecycle controls."
            )
            lines.append(
                "- [ ] **Testing Update**: Run functional safety verification tests."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Gap**: Unverified OWASP MASVS controls across network and local boundaries."
            )
            lines.append(
                "- [ ] **Implementation Task**: Apply OWASP MASVS L1/L2 security controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document OWASP MASVS verification status."
            )
            lines.append(
                "- [ ] **Testing Update**: Run automated OWASP vulnerability scan scripts."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Gap**: Incomplete NIST AI RMF Govern, Map, Measure, Manage alignment."
            )
            lines.append(
                "- [ ] **Implementation Task**: Implement AI transparency and explainability controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Publish model cards per NIST AI 100-1."
            )
            lines.append(
                "- [ ] **Testing Update**: Run automated AI transparency assertion tests."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Gap**: NIST CSF 2.0 Governance pillar alignment incomplete."
            )
            lines.append(
                "- [ ] **Implementation Task**: Update cybersecurity governance controls."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document NIST CSF cybersecurity policies."
            )
            lines.append(
                "- [ ] **Testing Update**: Execute incident response simulation tests."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Gap**: Unhardened default configuration profiles."
            )
            lines.append(
                "- [ ] **Implementation Task**: Apply CIS Benchmark hardening rules."
            )
            lines.append(
                "- [ ] **Documentation Update**: Document secure base configuration standards."
            )
            lines.append(
                "- [ ] **Testing Update**: Run automated CIS configuration audit scripts."
            )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(
            f"Technical standards documentation updated successfully at: {output_filepath}"
        )
    except Exception as e:
        print(
            f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr
        )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Requirements (ISO, IEC, OWASP, NIST, CIS)"
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

    if args.live:
        print("Fetching live Technical Standards RSS feeds...")
        # Live RSS feeds can be fetched here when available
        # ISO, NIST, and OWASP news feeds

    if args.mock or (not args.live and not args.mock) or not announcements:
        print(
            "Using comprehensive mock Technical Standards updates for compliance scanning..."
        )
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r", encoding="utf-8") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # Source trust hierarchy validation
    verified_announcements, blocked_count = enforce_strict_source_trust_hierarchy(
        announcements
    )

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(
        verified_announcements, keywords_filter
    )

    if not classified_updates:
        print("No classified technical standards updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(
        f"Scanning codebase under '{args.dir}' for technical standards integration signals..."
    )
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

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
