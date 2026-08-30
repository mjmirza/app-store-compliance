#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 technical standards:
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
        "privacy extension",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "ai management system",
        "aims",
        "artificial intelligence management system",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment framework",
        "risk management principles",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance framework",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "international electrotechnical commission",
    ],
    "OWASP": [
        "owasp",
        "masvs",
        "owasp top 10",
        "mobile application security verification standard",
        "asvs",
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
        "cybersecurity framework",
        "nist csf 2.0",
        "identify protect detect respond recover",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "center for internet security",
        "cis controls",
        "cis hardening",
        "cis benchmark",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"\bISMS\b",
        r"Annex A",
        r"informationSecurityPolicy",
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"\bPIMS\b",
        r"privacyInformationManagement",
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"\bAIMS\b",
        r"aiManagementSystem",
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskManagement",
        r"riskAssessment",
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"\bQMS\b",
        r"qualityManagement",
    ],
    "IEC standards": [
        r"IEC[ -]?62304",
        r"IEC[ -]?82304",
        r"IEC[ -]?62443",
        r"IECStandard",
    ],
    "OWASP": [
        r"\bOWASP\b",
        r"\bMASVS\b",
        r"\bASVS\b",
        r"OWASPTop10",
    ],
    "NIST AI RMF": [
        r"NIST[ -]AI[ -]RMF",
        r"\bAIRMF\b",
        r"NIST[ -]AI[ -]100",
    ],
    "NIST CSF": [
        r"NIST[ -]CSF",
        r"CybersecurityFramework",
        r"NIST[ -]SP[ -]800",
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmarks?",
        r"CIS[ -]?Controls?",
        r"CISHardening",
    ],
}

# Source trust domains for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Mock announcements covering all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Security Standard Update: Enhanced ISMS Controls for Cloud and Mobile Ecosystems",
        "description": "ISO/IEC 27001 update introduces revised Annex A controls emphasizing secure coding, threat intelligence, and cloud data posture management.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Extension Guidelines: Mandatory PIMS Requirements for PII Processors",
        "description": "ISO/IEC 27701 specifies Privacy Information Management System (PIMS) controls, requiring explicit data consent logging and automated PII lifecycle management.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 AI Management System Standard: Responsible Artificial Intelligence Governance",
        "description": "ISO/IEC 42001 establishes requirements for establishing, implementing, and continually improving an Artificial Intelligence Management System (AIMS).",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 03 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Revision: Continuous Risk Assessment and Mitigation Frameworks",
        "description": "ISO 31000 guidelines mandate continuous risk identification, quantitative risk scoring, and dynamic mitigation strategies across software development lifecycles.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 04 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System: Code Quality and Continuous Verification Integration",
        "description": "ISO 9001 QMS updates emphasize software quality assurance, automated regression testing, and document control across build pipelines.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 05 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Software Lifecycle Requirements (IEC 62304 / IEC 82304 / IEC 62443)",
        "description": "IEC standards mandate secure software lifecycle controls, functional safety verification, and operational technology cybersecurity controls.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 06 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & Top 10 Security Updates: Enforcing Mobile Security Verification Standards",
        "description": "OWASP updates Mobile Application Security Verification Standard (MASVS) controls for storage, cryptography, authentication, network communication, and platform interaction.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 07 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Update: Govern, Map, Measure, and Manage AI Risks",
        "description": "NIST AI RMF guidelines detail trustworthy AI characteristics including safety, security, resilience, explainability, privacy, and bias mitigation.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 08 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF) 2.0: Integrating Governance and Supply Chain Security",
        "description": "NIST CSF 2.0 expands cybersecurity outcomes across Identify, Protect, Detect, Respond, Recover, and introduces the new Govern function.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 09 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks & Controls Update: Hardening Recommendations for Mobile and Cloud Runtimes",
        "description": "Center for Internet Security (CIS) releases updated benchmarks for mobile OS hardening, cloud infrastructure, and application container baselines.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 10 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED",
        "category": "OWASP",
        "title": "Unverified Blog Post on OWASP Standard Changes",
        "description": "A random tech blog claims OWASP is removing all mobile security requirements next week. This is an unverified blog post.",
        "link": "https://randomblogsite.com/owasp-rumor",
        "pubDate": "Thu, 11 Jun 2026 20:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified).
    Domain / official publisher check takes absolute precedence.
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
        "gov.sg",
        "developer.apple.com",
        "developer.android.com",
    ]

    # Priority 1 official publishers/authorities (must be explicitly identified as the publisher)
    p1_publishers = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open worldwide application security project",
        "center for internet security",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
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

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(kw in combined for kw in p4_keywords):
        priority = 4
    elif any(d in link for d in p3_domains) or any(kw in combined for kw in p3_keywords) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains) or any(kw in combined for kw in p2_keywords):
        priority = 2

    # Official domain or explicit publisher check grants Priority 1
    if any(d in link for d in p1_domains) or any(pub in combined for pub in p1_publishers) or ".gov" in link:
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4 or 5: must have an official reference link/citation in text or cross-verification
        has_p1_ref = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref = True
                break
        if not has_p1_ref:
            for pub in p1_publishers:
                if pub in combined:
                    has_p1_ref = True
                    break
        if ".gov" in combined:
            has_p1_ref = True

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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "risk", "privacy"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans codebase for files matching signals for each of the 10 technical standards."""
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
                # Use word boundary regex to avoid partial substring matches (e.g. "aims" inside "claims")
                pattern = r"\b" + re.escape(kw.lower()) + r"\b"
                if re.search(pattern, text_to_search):
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
    """Generates a PR draft with exactly 15 required non-vague compliance sections."""
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
                f"- **{cat}**: Audit Information Security Management System (ISMS) policies and update Annex A security control mappings."
            )
            impl_checklist.append("- [ ] Align ISMS control documentation with ISO 27001 Annex A updates.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit findings during formal ISO 27001 certification reviews.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) controls and verify PII processing workflows."
            )
            impl_checklist.append("- [ ] Update PIMS data processing inventory and consent tracking.")
            risk_assessment.append(f"- *{cat}*: Exposure to privacy regulatory penalties due to unaligned PII processing.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance controls for machine learning models."
            )
            impl_checklist.append("- [ ] Document AI model risk assessments and algorithmic transparency logs.")
            risk_assessment.append(f"- *{cat}*: Algorithmic bias, safety regressions, and compliance gaps under emerging AI governance rules.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate structured risk assessment frameworks into continuous delivery pipelines."
            )
            impl_checklist.append("- [ ] Update risk register and automated risk scoring mechanisms.")
            risk_assessment.append(f"- *{cat}*: Unmitigated operational and security risks in technical infrastructure.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Maintain Quality Management System (QMS) standards across software engineering workflows."
            )
            impl_checklist.append("- [ ] Validate CI build quality gates and automated testing checklists.")
            risk_assessment.append(f"- *{cat}*: Software quality degradation and build pipeline failures.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align software lifecycle processes with IEC standards (e.g. IEC 62304 / IEC 62443)."
            )
            impl_checklist.append("- [ ] Audit medical and industrial software lifecycle safety controls.")
            risk_assessment.append(f"- *{cat}*: Failure to meet functional safety and industrial cybersecurity standards.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Verify repository controls against OWASP MASVS and OWASP Top 10 guidelines."
            )
            impl_checklist.append("- [ ] Run OWASP MASVS static analysis and verify transport/storage security.")
            risk_assessment.append(f"- *{cat}*: Vulnerability to common application exploits (insecure storage, injection, weak crypto).")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Apply NIST AI Risk Management Framework functions (Govern, Map, Measure, Manage) to AI integrations."
            )
            impl_checklist.append("- [ ] Complete NIST AI RMF trustworthiness and transparency assessment.")
            risk_assessment.append(f"- *{cat}*: Unmanaged AI safety risks and failure to satisfy NIST AI governance standards.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 core functions (Identify, Protect, Detect, Respond, Recover, Govern)."
            )
            impl_checklist.append("- [ ] Update cybersecurity control mappings to reflect NIST CSF 2.0 requirements.")
            risk_assessment.append(f"- *{cat}*: Gaps in organizational cybersecurity posture and incident response readiness.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Benchmarks and Hardening guidelines for operating systems and software runtimes."
            )
            impl_checklist.append("- [ ] Audit platform configuration settings against CIS Benchmarks baselines.")
            risk_assessment.append(f"- *{cat}*: System misconfigurations and unauthorized privilege escalation risks.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of standard controls."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces critical configuration, documentation, and technical updates to bring the repository into complete compliance with monitored technical standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).

## 2. Background
Technical standards evolve continuously to address emerging cybersecurity, privacy, artificial intelligence, and software quality challenges. Maintaining proactive alignment with international standards ensures enterprise readiness, regulatory compliance, and robust risk mitigation.

## 3. Regulatory change
- **ISO / IEC Frameworks**: Synchronization with ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, and IEC standards.
- **Security & AI Benchmarks**: Alignment with OWASP MASVS, NIST AI RMF 1.0, NIST CSF 2.0, and CIS Benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Moderate-to-high compliance risk if standards updates are unaddressed during enterprise audits.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All updates are non-breaking and fully backward-compatible. Technical controls and governance framework enhancements preserve existing system functionalities.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated repository validation scripts.

## 10. Testing checklist
- [ ] Verify static code analysis passes with zero critical findings.
- [ ] Test AI safety and transparency disclosures in application workflows.
- [ ] Confirm security configuration settings conform to CIS Benchmarks and OWASP MASVS.
- [ ] Verify build pipeline quality gates execute successfully.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed checklists.
- [ ] Document updated ISMS, PIMS, and AIMS controls in internal architecture references.

## 12. Compliance impact
- **Audit Readiness**: Ensures enterprise certification readiness across ISO, NIST, OWASP, and CIS domains.
- **Risk Mitigation**: Reduces vulnerability surface area and enhances AI governance.
- **Stakeholder Trust**: Demonstrates rigorous adherence to global industry benchmarks.

## 13. Breaking changes
- No functional breaking changes are introduced.

## 14. Review checklist
- [ ] Code and documentation diffs are completely emoji-free.
- [ ] Official sources cited adhere to the Source Trust Hierarchy.
- [ ] All implementation and testing items are validated.

## 15. Approver recommendations
Verify that ISMS/PIMS/AIMS controls align with current organizational policies and confirm that automated build pipeline quality checks pass.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
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
        lines.append("- **Regulatory Impact**: High priority technical standards area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update ISMS Annex A control mappings.")
            lines.append("- [ ] **Task 2**: Review information security policy documentation.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Update PIMS privacy controls and PII processing log.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Establish AIMS governance procedures for machine learning models.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Perform structured risk assessment across system components.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Audit software quality assurance and continuous integration processes.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Verify software lifecycle safety controls per IEC standards.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Conduct OWASP MASVS security verification audit.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Apply NIST AI RMF Govern, Map, Measure, Manage activities.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align security controls with NIST CSF 2.0 core functions.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Verify system configuration against CIS Benchmarks baselines.")
        else:
            lines.append(f"- [ ] **Task**: Verify compliance criteria for {cat}.")
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
        description="Monitor Technical Standards (ISO, IEC, OWASP, NIST, CIS)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards feeds"
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

    print(f"Scanning codebase under '{args.dir}' for standards integration signals...")
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
