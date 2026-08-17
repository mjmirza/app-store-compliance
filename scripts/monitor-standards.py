#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000,
ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).
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
    "CIS Benchmarks"
]

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001", "iso/iec 27001", "information security management",
        "isms", "annex a", "access control policy", "information security policy"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "privacy information management",
        "pims", "pii controller", "pii processor"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "artificial intelligence management",
        "aims", "ai risk assessment", "ai impact assessment"
    ],
    "ISO 31000": [
        "iso 31000", "risk management", "risk assessment framework",
        "risk treatment", "risk criteria"
    ],
    "ISO 9001": [
        "iso 9001", "quality management", "qms",
        "quality policy", "continuous improvement"
    ],
    "IEC standards": [
        "iec standards", "iec 62443", "iec 82304", "iec 62304",
        "functional safety", "industrial automation security"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "masvs", "asvs",
        "owasp mobile", "web security testing guide"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework",
        "govern map measure manage", "trustworthy ai"
    ],
    "NIST CSF": [
        "nist csf", "cybersecurity framework",
        "identify protect detect respond recover"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "center for internet security",
        "hardening guidelines", "cis controls"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS", r"iso27001", r"securityPolicy", r"accessControl", r"dataClassification"
    ],
    "ISO 27701": [
        r"PIMS", r"iso27701", r"piiController", r"piiProcessor", r"privacyImpactAssessment"
    ],
    "ISO 42001": [
        r"AIMS", r"iso42001", r"aiRiskAssessment", r"aiModelGovernance", r"aiImpactAssessment"
    ],
    "ISO 31000": [
        r"iso31000", r"riskManagement", r"riskAssessment", r"riskRegister", r"riskMitigation"
    ],
    "ISO 9001": [
        r"QMS", r"iso9001", r"qualityPolicy", r"qualityManagement", r"auditTrail"
    ],
    "IEC standards": [
        r"IEC62443", r"IEC82304", r"IEC62304", r"functionalSafety", r"industrialSecurity"
    ],
    "OWASP": [
        r"OWASP", r"MASVS", r"ASVS", r"injectionProtection", r"xssFilter", r"csrfProtection"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF", r"aiRiskFramework", r"trustworthyAI", r"modelBiasMitigation", r"aiExplainability"
    ],
    "NIST CSF": [
        r"NIST_CSF", r"cybersecurityFramework", r"incidentResponse", r"threatDetection", r"assetManagement"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark", r"cisControls", r"systemHardening", r"secureConfiguration", r"benchmarkAudit"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Management System Guideline Update",
        "description": "Updated ISO/IEC 27001 guidance mandates refined Annex A controls for cloud services, threat intelligence, and secure coding practices across digital development lifecycle.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Extension Mandate",
        "description": "ISO/IEC 27701 specifies operational requirements for PII controllers and processors, extending ISO 27001 to ensure comprehensive privacy governance and data subject rights enforcement.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Certification Standard",
        "description": "ISO/IEC 42001 establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organizations.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Principles and Implementation Guidelines",
        "description": "ISO 31000 provides principles, a framework, and a process for managing risk across technical infrastructure and operational decision-making processes.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Guidelines for Software Delivery",
        "description": "ISO 9001 updates outline quality management expectations, continuous improvement cycles, and standardized software build and delivery audit trails.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62443 and IEC 82304 Functional Safety and Cybersecurity Standards",
        "description": "IEC standards specify cybersecurity and functional safety requirements for industrial automation, health software, and connected device control systems.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS and Top 10 Application Security Standard Refinements",
        "description": "OWASP updates refine mobile and web application security standards (MASVS and ASVS), specifying mandatory controls against input injection, broken authentication, and unsafe API exposure.",
        "link": "https://owasp.org",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "NIST AI RMF provides structured guidelines across Govern, Map, Measure, and Manage functions to foster trustworthy AI systems and manage risks of algorithmic bias and opacity.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Directive",
        "description": "NIST CSF 2.0 expands cybersecurity guidance across Identify, Protect, Detect, Respond, Recover, and Govern functions for technology infrastructure.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "Center for Internet Security (CIS) Benchmarks and Controls Update",
        "description": "CIS Benchmarks specify prescriptive configuration hardening rules and controls to protect operating systems, cloud environments, and mobile platforms against cyber threats.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    # Unverified announcement for source trust testing
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "OWASP",
        "title": "Unverified Blog Claiming Complete OWASP Standard Overhaul",
        "description": "An unverified personal tech blog claims OWASP is replacing all security standards next month. No official OWASP or NIST sources cited.",
        "link": "https://randomblogsite.com/owasp-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 PDT"
    }
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
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg", "apple.com",
        "developer.apple.com", "android.com", "developer.android.com"
    ]
    p1_keywords = [
        "international organization for standardization", "iso", "iec", "nist",
        "owasp", "center for internet security", "cis benchmark", "european commission",
        "eur-lex", "official journal", "enisa", "edpb", "ftc", "cisa", "ico"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

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

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
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
                    common_terms = {"iso", "nist", "owasp", "security", "privacy", "risk", "benchmark"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards categories.
    Excludes typical build, dependency, and test directories.
    """
    matches = {cat: [] for cat in CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
        ".dart_tool", "Carthage", "androidTest", "__tests__", "dist"
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
                    ".kt", ".java", ".xml", ".gradle", ".kts", ".json", ".js",
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html", ".py", ".yml", ".yaml"
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
                f"- **{cat}**: Align Information Security Management System (ISMS) controls with ISO/IEC 27001:2022 Annex A requirements."
            )
            impl_checklist.append("- [ ] Audit ISMS access control policies and data classification schemes.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with information security controls risking audit findings and security breaches.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to a Privacy Information Management System (PIMS) for PII controller and processor obligations."
            )
            impl_checklist.append("- [ ] Implement PII processing documentation and privacy impact assessment workflows.")
            risk_assessment.append(f"- *{cat}*: Inadequate PII processing controls resulting in privacy regulation violations.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance and risk management procedures."
            )
            impl_checklist.append("- [ ] Implement AI risk assessments and model governance documentation.")
            risk_assessment.append(f"- *{cat}*: Unmitigated AI safety, bias, or transparency risks in automated decision systems.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate structured risk assessment, criteria evaluation, and treatment processes across tech operations."
            )
            impl_checklist.append("- [ ] Maintain updated risk registers and mitigation tracking matrices.")
            risk_assessment.append(f"- *{cat}*: Unidentified technical or operational risk vectors leading to service disruption.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Apply Quality Management System (QMS) principles to software development, build, and deployment lifecycles."
            )
            impl_checklist.append("- [ ] Establish continuous improvement metrics and software build audit trails.")
            risk_assessment.append(f"- *{cat}*: Inconsistent software quality and lack of structured release verification.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62443 / IEC 82304 functional safety and cybersecurity controls for software components."
            )
            impl_checklist.append("- [ ] Verify software functional safety boundaries and secure device interface controls.")
            risk_assessment.append(f"- *{cat}*: Safety critical or interface vulnerabilities in connected software components.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement OWASP MASVS and ASVS controls for input sanitization, authentication, and API security."
            )
            impl_checklist.append("- [ ] Validate input injection defenses, XSS filters, and CSRF tokens across API endpoints.")
            risk_assessment.append(f"- *{cat}*: Critical application vulnerabilities leading to unauthorized data access or exploitation.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI RMF Govern, Map, Measure, and Manage functions for trustworthy AI models."
            )
            impl_checklist.append("- [ ] Implement model explainability checks and bias mitigation testing.")
            risk_assessment.append(f"- *{cat}*: Deployment of non-trustworthy AI models with unquantified risk exposures.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls across Identify, Protect, Detect, Respond, Recover, and Govern domains."
            )
            impl_checklist.append("- [ ] Update incident response playbooks and automated threat detection rules.")
            risk_assessment.append(f"- *{cat}*: Delayed threat detection or recovery procedures during security incidents.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS hardening guidelines and configuration controls across build environments and servers."
            )
            impl_checklist.append("- [ ] Perform CIS benchmark audit checks on build configurations and container images.")
            risk_assessment.append(f"- *{cat}*: System misconfigurations leaving environment susceptible to automated exploitation.")

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
This pull request introduces critical configuration, documentation, and code adjustments to align the repository with modern technical standards. It addresses ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards provide rigorous frameworks for security, privacy, quality, risk, and AI management. Adherence ensures enterprise readiness, mitigates technical risks, and passes formal compliance audits. This PR systematically resolves identified repository gaps against updated standards.

## 3. Regulatory change
- **ISO Standards**: Updated ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk Management (ISO 31000), and QMS (ISO 9001) guidelines.
- **NIST & CIS Frameworks**: NIST Cybersecurity Framework 2.0, NIST AI Risk Management Framework 1.0, and CIS Controls hardening benchmarks.
- **OWASP & IEC Standards**: OWASP MASVS/ASVS security controls and IEC 62443/82304 functional safety guidelines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High audit and operational risk if technical standards guidelines are not systematically implemented.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed updates maintain full backward compatibility. System architectures, API interfaces, and existing user workflows remain fully operational.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
- [ ] Validate OWASP input sanitization and XSS protection filters.
- [ ] Verify NIST CSF logging and incident detection trigger mechanisms.
- [ ] Audit CIS Benchmark configuration compliance across deployment scripts.
- [ ] Execute automated unit and integration tests to confirm zero regressions.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Update internal security and risk management playbooks.
- [ ] Confirm ISO, NIST, and OWASP compliance mapping documents are current.

## 12. Compliance impact
- **Audit Preparedness**: Ensures full readiness for ISO, NIST, and OWASP compliance audits.
- **Security Posture**: Strengthens system hardening, vulnerability defenses, and risk governance.
- **Enterprise Trust**: Increases trust among enterprise clients by demonstrating certified standards alignment.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced security checks operate transparently.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Confirm security controls pass automated static analysis guards.

## 15. Approver recommendations
Verify that the technical risk assessment matrices and CIS benchmark audit logs are validated prior to merge, and confirm that all OWASP MASVS controls pass regression testing.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Requirements Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Standards Update Log",
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
            lines.append("- [ ] **Task 1**: Update ISMS access control policy documentation.")
            lines.append("- [ ] **Task 2**: Audit data classification and Annex A security controls.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Document PII controller/processor obligations in PIMS.")
            lines.append("- [ ] **Task 2**: Conduct Privacy Impact Assessments for personal data flows.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Establish Artificial Intelligence Management System (AIMS) risk register.")
            lines.append("- [ ] **Task 2**: Document AI model governance and algorithmic impact procedures.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Update enterprise risk evaluation criteria and treatment workflows.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Maintain software quality policy and release build audit logs.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Review IEC 62443 / IEC 82304 functional safety and software security rules.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Audit code against OWASP MASVS/ASVS input validation and authentication rules.")
            lines.append("- [ ] **Task 2**: Implement CSRF and XSS protection filters across all web endpoints.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Map AI model risks under NIST AI RMF Govern, Map, Measure, Manage functions.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align threat detection and incident response playbooks with NIST CSF 2.0.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Apply CIS hardening guidelines to deployment environments and container images.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all technical criteria for {cat} are checked and handled.")
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
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/news.xml"))
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

    print(f"Monitored and classified {len(classified_updates)} policy/requirement updates ({blocked_updates_count} blocked due to source trust validation):")
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
            report_data.append({
                "track": cat,
                "title": u["title"],
                "pubDate": u["pubDate"],
                "link": u["link"],
                "priority": priority,
                "verified": is_verified,
                "matches": scan_results.get(cat, [])
            })
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
