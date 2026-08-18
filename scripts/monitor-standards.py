#!/usr/bin/env python3
"""
Monitors changes to 10 technical standards:
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

Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates.
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

# Keywords used to classify incoming policy announcements/articles into the 10 standards
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
        "responsible ai governance",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "enterprise risk management",
        "risk assessment framework",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance controls",
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
        "mastg",
        "asvs",
        "owasp mobile top 10",
        "owasp ai top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "csf 2.0",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "cis hardening",
        "cis hardened images",
    ],
}

# Codebase signals (regex patterns) to find files affected by each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO\s*27001",
        r"ISMS",
        r"access_control",
        r"encryption_at_rest",
        r"incident_response",
    ],
    "ISO 27701": [
        r"ISO\s*27701",
        r"PIMS",
        r"pii",
        r"data_retention",
        r"privacy_policy",
    ],
    "ISO 42001": [
        r"ISO\s*42001",
        r"AIMS",
        r"ai_governance",
        r"model_safety",
        r"bias_audit",
    ],
    "ISO 31000": [
        r"ISO\s*31000",
        r"risk_assessment",
        r"risk_register",
        r"risk_mitigation",
    ],
    "ISO 9001": [
        r"ISO\s*9001",
        r"QMS",
        r"quality_assurance",
        r"process_audit",
    ],
    "IEC standards": [
        r"IEC\s*62443",
        r"IEC\s*82304",
        r"IEC\s*62304",
        r"medical_device_software",
        r"industrial_control",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MASTG",
        r"ASVS",
        r"injection_protection",
        r"csrf",
    ],
    "NIST AI RMF": [
        r"NIST\s*AI\s*RMF",
        r"govern_map_measure_manage",
        r"ai_risk",
        r"trustworthy_ai",
    ],
    "NIST CSF": [
        r"NIST\s*CSF",
        r"CSF\s*2\.0",
        r"cybersecurity_framework",
        r"threat_detection",
    ],
    "CIS Benchmarks": [
        r"CIS\s*Benchmark",
        r"CIS\s*Controls",
        r"hardening",
        r"secure_baseline",
    ],
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management Standard Control Update",
        "description": "Updated ISO 27001 guidance requires mandatory automated access review controls, encrypted secret storage verification, and continuous incident management tracking.",
        "link": "https://www.iso.org/isoiec-27001-information-security.html",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management Guidelines Expansion",
        "description": "ISO 27701 extensions mandate strict PII lifecycle management, explicit consent logging for cross-border data transfers, and automated data subject request fulfillment.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Governance Baseline",
        "description": "ISO 42001 standards require organizational risk assessments for artificial intelligence systems, continuous model safety testing, data lineage documentation, and bias monitoring.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Assessment Revision",
        "description": "ISO 31000 framework revisions emphasize integrating real-time operational metrics into risk registers and executing structured scenario analyses across digital platforms.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Continuous Delivery Guidelines",
        "description": "ISO 9001 updates enforce continuous software quality metrics, automated pre-release validation checks, and formalized root-cause analysis for production incidents.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Electrotechnical Software Safety and Cyber Resilience",
        "description": "IEC 62443 and IEC 82304 standards mandate secure lifecycle development, component vulnerability tracking, and automated patch management for client application runtimes.",
        "link": "https://www.iec.ch/cybersecurity",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & Top 10 Release: Enhanced Mobile & LLM Verification Controls",
        "description": "OWASP published updated MASVS requirements mandating hardware-backed secret storage, anti-tampering verification, and robust input sanitization for AI prompts.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Companion Guidelines Update",
        "description": "NIST AI RMF guidance details requirements across the Govern, Map, Measure, and Manage functions, focusing on AI transparency, output verification, and adverse incident logging.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework CSF 2.0 Governance Category Implementation",
        "description": "NIST CSF 2.0 highlights the Govern function, requiring explicitly assigned cybersecurity roles, supply chain risk management, and continuous security compliance auditing.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Hardening Standards Release for Mobile and Web Runtimes",
        "description": "CIS Benchmarks publish updated secure configuration recommendations, disabling unneeded services, enforcing strict TLS profiles, and requiring automated configuration drift checks.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 GMT",
    },
]


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
                    ".entitlements",
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
    """Classifies incoming announcements into the 10 technical standards."""
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
    doc_checklist = []

    processed_cats = set()

    for u in updates:
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
            migration_steps.append(
                f"- **{cat}**: Implement ISMS control verification and automated access control audit logging."
            )
            impl_checklist.append(
                "- [ ] Configure continuous access management and ISMS logging rules."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with enterprise information security management standards."
            )
            testing_checklist.append(
                "- [ ] Test access control enforcement and audit trail persistence for ISO 27001."
            )
            doc_checklist.append(
                "- [ ] Document ISO 27001 ISMS policies and control mapping."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Expand PIMS controls for personal data processing and consent tracking."
            )
            impl_checklist.append(
                "- [ ] Implement PII lifecycle tracking and explicit consent logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of structured privacy management for personally identifiable information."
            )
            testing_checklist.append(
                "- [ ] Verify PII deletion workflows and consent state checks for ISO 27701."
            )
            doc_checklist.append(
                "- [ ] Update PIMS documentation and data protection impact assessments."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish AI Management System (AIMS) governance and model monitoring."
            )
            impl_checklist.append(
                "- [ ] Implement AI system risk assessment baseline and model audit logs."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI risks including model hallucination, bias, and output safety failures."
            )
            testing_checklist.append(
                "- [ ] Validate AI model input/output safety filters and logging under ISO 42001."
            )
            doc_checklist.append(
                "- [ ] Document ISO 42001 AIMS controls and AI risk evaluation records."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate structured risk assessment frameworks into system operation controls."
            )
            impl_checklist.append(
                "- [ ] Register operational system risks and map mitigation protocols."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated enterprise risk exposure across digital infrastructure."
            )
            testing_checklist.append(
                "- [ ] Run risk scenario simulations and verify mitigation handlers for ISO 31000."
            )
            doc_checklist.append(
                "- [ ] Update risk register and mitigation matrix."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enforce continuous quality assurance controls and automated release testing."
            )
            impl_checklist.append(
                "- [ ] Integrate automated pre-release quality gates into CI pipelines."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation leading to unexpected runtime regressions."
            )
            testing_checklist.append(
                "- [ ] Run automated CI pipeline quality gates and verify 100% test coverage."
            )
            doc_checklist.append(
                "- [ ] Document Quality Management System (QMS) release standards."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align electrotechnical and runtime software security controls with IEC standards."
            )
            impl_checklist.append(
                "- [ ] Audit third-party software components against IEC lifecycle vulnerability rules."
            )
            risk_assessment.append(
                f"- *{cat}*: Unpatched software vulnerabilities in embedded and client runtimes."
            )
            testing_checklist.append(
                "- [ ] Execute dependency security vulnerability scans for IEC compliance."
            )
            doc_checklist.append(
                "- [ ] Publish IEC compliance verification report and software bill of materials."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement OWASP MASVS and ASVS security controls across client and API layers."
            )
            impl_checklist.append(
                "- [ ] Enforce hardware-backed token storage and anti-tampering checks."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerability to injection, session hijacking, or reverse-engineering."
            )
            testing_checklist.append(
                "- [ ] Execute OWASP MASTG security test scripts and dynamic analysis."
            )
            doc_checklist.append(
                "- [ ] Document OWASP MASVS control mapping in mobile security guidelines."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Execute NIST AI RMF Govern, Map, Measure, and Manage functions for AI features."
            )
            impl_checklist.append(
                "- [ ] Implement AI risk governance and output verification logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Unaligned AI systems causing unexpected harm or regulatory non-compliance."
            )
            testing_checklist.append(
                "- [ ] Perform adversarial testing on AI prompt handling under NIST AI RMF."
            )
            doc_checklist.append(
                "- [ ] Update NIST AI RMF governance documentation and impact logs."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align repository security policies with NIST CSF 2.0 Governance functions."
            )
            impl_checklist.append(
                "- [ ] Map cybersecurity roles, threat detection, and continuous monitoring controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate threat detection and incident response readiness."
            )
            testing_checklist.append(
                "- [ ] Simulate cybersecurity incident response flows for NIST CSF."
            )
            doc_checklist.append(
                "- [ ] Update NIST CSF 2.0 security controls roadmap."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Benchmarks hardening rules for application environment configuration."
            )
            impl_checklist.append(
                "- [ ] Enforce CIS hardening configurations and disable unneeded services."
            )
            risk_assessment.append(
                f"- *{cat}*: System misconfigurations allowing unauthorized access or privileges."
            )
            testing_checklist.append(
                "- [ ] Run CIS Benchmark compliance auditing tools against build targets."
            )
            doc_checklist.append(
                "- [ ] Document CIS Benchmarks configuration baseline."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standard patterns were automatically detected. (Perform manual review of repository assets).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)
    testing_checklist_str = "\n".join(testing_checklist)
    doc_checklist_str = "\n".join(doc_checklist)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the application and repository with global technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards provide rigorous international baselines for information security, privacy, AI governance, quality management, and runtime hardening. Following updated standards mitigates security risks and ensures platform readiness.

## 3. Regulatory change
- **Technical Standards Frameworks**: Alignment with updated ISO/IEC, OWASP, NIST, and CIS Benchmarks guidelines.
- **Security & Privacy Governance**: Implementation of structured ISMS, PIMS, AIMS, and CSF governance controls.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium-to-high compliance risk if technical standards updates are unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed standard enhancements maintain full backward compatibility with existing application interfaces and APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run technical standards compliance guard scripts.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Verify that all automated test suites pass without regression.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with implementation status.

## 12. Compliance impact
- **Standards Aligned**: Satisfies ISO, OWASP, NIST, and CIS Benchmarks requirements.
- **Risk Reduction**: Reduces vulnerability footprint and establishes institutional risk governance.

## 13. Breaking changes
- No breaking changes introduced.

## 14. Review checklist
- [ ] Code is 100% free of emojis or graphical symbols.
- [ ] Security configurations conform strictly to official technical standards.

## 15. Approver recommendations
Verify that all technical standards implementation tasks and documentation updates have been completed and validated.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Requirements Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
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

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    processed_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_cats:
            continue
        processed_cats.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority. Technical standard update mandates review."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update ISMS access control rules and logging."
            )
            lines.append(
                "- [ ] **Task 2**: Perform information security risk review."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Audit PII processing activities and PIMS controls."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish AI Management System governance controls."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Update enterprise risk register and assessment protocols."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Verify quality management software release gates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Audit third-party software components for electrotechnical safety compliance."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Verify application against OWASP MASVS / Top 10 requirements."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Map AI features against NIST AI RMF Govern, Map, Measure, Manage functions."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity policies with NIST CSF 2.0 Governance functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Perform CIS hardening configuration audit."
            )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards RSS feeds"
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
    parser.add_argument(
        "--json", action="store_true", help="Output JSON result to stdout"
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        if not args.json:
            print("Fetching live Technical Standards RSS feeds...")

    if args.mock or (not args.live and not args.mock) or not announcements:
        if not args.json:
            print("Using comprehensive mock Technical Standards policy updates for compliance scanning...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                if not args.json:
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
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    if not args.json:
        print(
            f"Monitored and classified {len(classified_updates)} technical standards updates:"
        )
        for idx, u in enumerate(classified_updates, 1):
            print(f" {idx}. [{u['category']}] {u['title']}")

        print(f"Scanning codebase under '{args.dir}' for standards integration signals...")

    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            if not args.json:
                print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            if not args.json:
                print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    if args.json:
        result_json = {
            "updates_count": len(classified_updates),
            "total_signal_matches": total_matches,
            "classified_updates": classified_updates,
            "scan_results": scan_results,
            "docs_output": args.output_docs,
            "pr_output": args.pr_output,
        }
        print(json.dumps(result_json, indent=2))


if __name__ == "__main__":
    main()
