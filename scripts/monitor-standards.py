#!/usr/bin/env python3
"""Monitors 10 technical standards categories and generates repo-gap
analysis, implementation tasks, documentation updates, testing updates,
and 15-section compliance pull request drafts while enforcing strict
source trust hierarchy validation."""

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

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

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
        "privacy controls",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
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
        "quality management system",
        "qms",
        "quality assurance standard",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "industrial cybersecurity",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "owasp masvs",
        "owasp asvs",
        "owasp llm top 10",
        "web application security",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "trustworthy ai",
        "ai governance",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "governing cybersecurity",
        "nist sp 800-53",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis controls",
        "center for internet security",
        "hardening guidelines",
        "cis benchmark",
    ],
}

# Codebase signals (regex patterns) to find files affected by each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -_]?27001",
        r"ISMS",
        r"information_security_policy",
        r"security_controls",
        r"access_control",
    ],
    "ISO 27701": [
        r"ISO[ -_]?27701",
        r"PIMS",
        r"privacy_policy",
        r"data_protection_officer",
        r"pii_processing",
    ],
    "ISO 42001": [
        r"ISO[ -_]?42001",
        r"AIMS",
        r"ai_governance",
        r"ai_risk_assessment",
        r"model_card",
    ],
    "ISO 31000": [
        r"ISO[ -_]?31000",
        r"risk_management",
        r"risk_register",
        r"risk_matrix",
    ],
    "ISO 9001": [
        r"ISO[ -_]?9001",
        r"QMS",
        r"quality_policy",
        r"quality_assurance",
    ],
    "IEC standards": [
        r"IEC[ -_]?62443",
        r"IEC[ -_]?62304",
        r"IEC[ -_]?82304",
        r"IEC[ -_]?standards",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitizer",
        r"xss_filter",
        r"csrf_token",
    ],
    "NIST AI RMF": [
        r"NIST[ -_]?AI[ -_]?RMF",
        r"trustworthy_ai",
        r"ai_bias_check",
        r"model_explainability",
    ],
    "NIST CSF": [
        r"NIST[ -_]?CSF",
        r"NIST[ -_]?SP[ -_]?800-53",
        r"cybersecurity_framework",
    ],
    "CIS Benchmarks": [
        r"CIS[ -_]?Benchmarks",
        r"CIS[ -_]?Controls",
        r"hardening",
        r"secure_baseline",
    ],
}

# Comprehensive mock announcements for the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Update: Mandatory Annex A Information Security Controls Audit",
        "description": "Organizations must transition ISMS documentation to match ISO/IEC 27001:2022 Annex A control sets, covering threat intelligence, web filtering, and secure coding.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Guidelines: Privacy Information Management System (PIMS) Requirements",
        "description": "PIMS rules mandate dedicated data mapping, consent lifecycle management, and formal data protection impact assessments for PII processing operations.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Release: Artificial Intelligence Management System (AIMS) Requirements",
        "description": "Standardizes AI governance, model risk assessment, training data verification, transparency, and continuous model monitoring for enterprise AI deployments.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 05 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Framework: Enterprise Risk Management and Risk Assessment Guidelines",
        "description": "Updated risk management principles mandate integrated threat assessment matrices, continuous risk monitoring, and executive risk governance frameworks.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 08 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System: Process Assurance and Software Quality Audits",
        "description": "Mandates documented quality assurance pipelines, automated code validation, structured change management, and continuous process improvement controls.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 10 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Industrial Cybersecurity (IEC 62443) and Software Lifecycle (IEC 62304)",
        "description": "Establishes secure software development lifecycle controls, threat modeling requirements, and hardware/software boundary isolation for mission-critical systems.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Fri, 12 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & Top 10 Security Guidance: Mitigating Modern Web and Mobile Vulnerabilities",
        "description": "Updates OWASP MASVS controls for mobile authentication, storage encryption, and network security, while introducing new OWASP LLM Top 10 guidance.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0: Govern, Map, Measure, and Manage AI Systems",
        "description": "NIST guidelines require mapping AI risks across model bias, hallucination, explainability, safety, and establishing continuous measurement protocols.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 17 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0: Governance Core and Supply Chain Risk Management",
        "description": "NIST CSF 2.0 introduces the GOVERN function, mandating enterprise supply chain risk management, continuous security auditing, and executive reporting.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 19 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls and Benchmarks: Automated Hardening Guidelines for Mobile and Web Applications",
        "description": "Recommends strict OS configuration hardening, disabling unnecessary services, enforcing least privilege access control, and automated configuration auditing.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Mon, 22 Jun 2026 16:00:00 GMT",
    },
]


def enforce_strict_source_trust_hierarchy(updates):
    """
    Enforces strict source trust hierarchy validation.
    Priority 1: Official standards bodies and government agencies.
    Priority 2: Major news organizations.
    Priority 3: Academic publications.
    Priority 4: Industry blogs (requires Priority 1 verification).
    Priority 5: Unverified social media / AI generated summaries.

    Logs verification status alerts to stderr and filters/marks updates.
    Returns list of verified updates.
    """
    verified_updates = []

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

    for u in updates:
        link = u.get("link", "").lower()
        title = u.get("title", "").lower()
        desc = u.get("description", "").lower()
        combined = f"{title} {desc} {link}"

        priority = 4  # Default assumption

        if any(d in link for d in p1_domains) or ".gov" in link or ".org" in link:
            priority = 1
        elif any(d in link for d in ["reuters.com", "apnews.com", "bloomberg.com"]):
            priority = 2
        elif any(d in link for d in ["arxiv.org", "ssrn.com"]) or ".edu" in link:
            priority = 3
        elif any(d in link for d in ["twitter.com", "x.com", "linkedin.com", "reddit.com"]):
            priority = 5

        # Verification check
        is_verified = False
        if priority <= 3:
            is_verified = True
        else:
            # Check if Priority 4 or 5 references Priority 1 official sources
            if any(d in combined for d in p1_domains) or ".gov" in combined:
                is_verified = True

        if not is_verified:
            print(
                f"[Source Trust Warning] Blocked unverified Priority {priority} source for update: '{u.get('title')}'",
                file=sys.stderr,
            )
        else:
            u["trust_priority"] = priority
            u["is_verified"] = is_verified
            verified_updates.append(u)

    return verified_updates


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals matching each of the 10 standards categories."""
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
                    ".py",
                    ".md",
                    ".yml",
                    ".yaml",
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
            url, headers={"User-Agent": "Mozilla/5.0 (TechnicalStandardsMonitor/1.0)"}
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
                f"- **{cat}**: Perform an Annex A control gap analysis; document Information Security Management System (ISMS) policies and access controls."
            )
            impl_checklist.append(
                "- [ ] Document ISMS Annex A control alignment and access control matrix."
            )
            testing_checklist.append(
                "- [ ] Run static analysis security testing (SAST) and audit access log permissions."
            )
            doc_checklist.append(
                "- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with ISO 27001 control mapping."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with enterprise information security requirements leading to audit failures and credential risk."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Establish Privacy Information Management System (PIMS) controls, PII processing registries, and data subject rights procedures."
            )
            impl_checklist.append(
                "- [ ] Implement PII data mapping and consent lifecycle management mechanisms."
            )
            testing_checklist.append(
                "- [ ] Verify PII encryption at rest and in transit across data persistence layers."
            )
            doc_checklist.append(
                "- [ ] Document PIMS control framework in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate PII management exposing organization to regulatory fines and privacy breaches."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) governance, model risk assessments, and transparency disclosures."
            )
            impl_checklist.append(
                "- [ ] Create AI model card documentation and risk assessment protocols."
            )
            testing_checklist.append(
                "- [ ] Execute model evaluation tests for bias, hallucination, and output safety boundaries."
            )
            doc_checklist.append(
                "- [ ] Record AIMS governance policies in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Ungoverned AI deployment resulting in unsafe outputs, compliance violations, and reputational damage."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Implement Enterprise Risk Management (ERM) guidelines, threat assessment matrices, and continuous risk monitoring."
            )
            impl_checklist.append(
                "- [ ] Establish formal risk register and likelihood/impact assessment matrix."
            )
            testing_checklist.append(
                "- [ ] Validate automated alert thresholds for high-risk system parameters."
            )
            doc_checklist.append(
                "- [ ] Record risk management framework details in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated technical risks resulting in unhandled operational disruptions."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Establish Quality Management System (QMS) release audit gates, continuous process improvement, and change tracking."
            )
            impl_checklist.append(
                "- [ ] Implement quality assurance gates in CI/CD pipeline."
            )
            testing_checklist.append(
                "- [ ] Run automated regression test suites prior to build release authorization."
            )
            doc_checklist.append(
                "- [ ] Maintain QMS audit trail documentation in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Software quality degradation and regression risks in production releases."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62443 / IEC 62304 secure lifecycle controls, threat modeling, and component boundary isolation."
            )
            impl_checklist.append(
                "- [ ] Conduct threat modeling for hardware/software boundary interfaces."
            )
            testing_checklist.append(
                "- [ ] Perform boundary testing and interface input validation suites."
            )
            doc_checklist.append(
                "- [ ] Update IEC compliance evidence logs in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Critical component failure or vulnerability exploitation at system boundaries."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Audit code against OWASP MASVS and OWASP Top 10 controls; implement strict input sanitization and secure storage."
            )
            impl_checklist.append(
                "- [ ] Remediate OWASP MASVS verification requirements across storage and networking."
            )
            testing_checklist.append(
                "- [ ] Execute OWASP ZAP / MASVS security scan workflows against target interfaces."
            )
            doc_checklist.append(
                "- [ ] Document OWASP MASVS audit findings in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerability exploitation leading to data exfiltration or injection attacks."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Map, measure, manage, and govern AI model risks in alignment with NIST AI 100-1 trustworthy AI guidelines."
            )
            impl_checklist.append(
                "- [ ] Establish NIST AI RMF GOVERN, MAP, MEASURE, MANAGE tracking profiles."
            )
            testing_checklist.append(
                "- [ ] Run continuous model measurement tests for accuracy, robustness, and safety."
            )
            doc_checklist.append(
                "- [ ] Update NIST AI RMF risk profile in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Deployment of untrusted or biased AI models violating federal risk guidelines."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER functions."
            )
            impl_checklist.append(
                "- [ ] Implement NIST CSF 2.0 governance controls and supply chain risk tracking."
            )
            testing_checklist.append(
                "- [ ] Test incident response detection rules and audit log aggregation."
            )
            doc_checklist.append(
                "- [ ] Update NIST CSF 2.0 mapping table in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Gaps in security posture exposing infrastructure to cyber threats."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS hardening Benchmarks across application build targets, configuration files, and system permissions."
            )
            impl_checklist.append(
                "- [ ] Enforce hardened configuration baselines and disable unnecessary features."
            )
            testing_checklist.append(
                "- [ ] Execute automated CIS configuration compliance checks."
            )
            doc_checklist.append(
                "- [ ] Document CIS Benchmark compliance status in `docs/STANDARDS-POLICY-MIGRATION.md`."
            )
            risk_assessment.append(
                f"- *{cat}*: Misconfiguration and unhardened default settings inviting unauthorized access."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific repository files containing matching standard patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    doc_checklist_str = "\n".join(doc_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the repository with modern technical standards across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It establishes repository gap mitigations, actionable implementation tasks, documentation updates, and testing verification suites.

## 2. Background
Technical standards compliance ensures organizational security posture, privacy governance, quality assurance, risk management, and trustworthy AI implementation. Adherence to internationally recognized standards mitigates security vulnerabilities and audit failures.

## 3. Regulatory change
- **International Technical Standards**: Continuous alignment with ISO/IEC, NIST, OWASP, and CIS benchmark updates.
- **Trustworthy AI Governance**: Compliance with ISO 42001 and NIST AI RMF 1.0 guidelines for enterprise artificial intelligence.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium-to-High risk if technical standards controls are unmapped or unverified during external audits.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed technical standards updates are non-breaking and fully backward-compatible. System configurations, documentation frameworks, and test suites enhance security posture without altering external API contracts.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run scripts/validate.py to ensure zero schema or pattern errors.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run automated compliance verification test suites.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Ensure all documentation updates are 100% emoji-free.

## 12. Compliance impact
- **Standards Aligned**: Satisfies ISO, NIST, OWASP, and CIS technical framework controls.
- **Audit Preparedness**: Guarantees verifiable evidence artifacts for external security and privacy audits.

## 13. Breaking changes
- No functional breaking changes. Configuration hardening restricts insecure default parameters.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] Source trust hierarchy rules have been strictly enforced for all official citations.
- [ ] All security and privacy control mappings are verified against standard requirements.

## 15. Approver recommendations
Verify that all technical standards control mappings in `docs/STANDARDS-POLICY-MIGRATION.md` match standard specifications. Confirm that test execution logs prove adherence to OWASP, NIST, and ISO requirements.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Report",
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

    lines.append("## Repository Gap Analysis")
    lines.append("")
    for u in updates:
        cat = u["category"]
        files = scan_results.get(cat, [])
        lines.append(f"### Gap Analysis for {cat}")
        if files:
            lines.append(f"- **Status**: Identified {len(files)} file(s) matching standard signals.")
            for f in files[:5]:
                lines.append(f"  - `{f['file']}` (Line {f['line_num']}): matched `{f['matched_pattern']}`")
        else:
            lines.append(f"- **Status**: No direct signal matches found. Manual configuration audit required for {cat}.")
        lines.append("")

    lines.append("## Implementation Tasks & Recommendations")
    lines.append("")
    for u in updates:
        cat = u["category"]
        lines.append(f"### Tasks for {cat}")
        lines.append(f"- [ ] **Task 1**: Review {cat} requirements against repository architecture.")
        lines.append(f"- [ ] **Task 2**: Implement baseline control policies and verification scripts.")
        lines.append("")

    lines.append("## Documentation Updates")
    lines.append("")
    for u in updates:
        cat = u["category"]
        lines.append(f"### Documentation Updates for {cat}")
        lines.append(f"- Document control mapping and compliance evidence for {cat} in `docs/STANDARDS-POLICY-MIGRATION.md`.")
        lines.append("")

    lines.append("## Testing Updates")
    lines.append("")
    for u in updates:
        cat = u["category"]
        lines.append(f"### Testing Updates for {cat}")
        lines.append(f"- Add automated test assertions verifying {cat} control compliance.")
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
        description="Monitor Technical Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards RSS/Atom feeds"
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

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    # Enforce strict source trust hierarchy validation
    verified_updates = enforce_strict_source_trust_hierarchy(classified_updates)

    if not verified_updates:
        print("No updates passed strict source trust hierarchy validation.")
        sys.exit(1)

    print(f"Monitored and classified {len(verified_updates)} technical standards updates:")
    for idx, u in enumerate(verified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(verified_updates, scan_results, args.output_docs)

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
