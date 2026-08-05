#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards (ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF,
and CIS Benchmarks) against live or mock data.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
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
    "ISO 27001": ["iso 27001", "iso27001", "isms", "information security management"],
    "ISO 27701": ["iso 27701", "iso27701", "pims", "privacy information management"],
    "ISO 42001": ["iso 42001", "iso42001", "aims", "artificial intelligence management"],
    "ISO 31000": ["iso 31000", "iso31000", "risk management", "risk assessment"],
    "ISO 9001": ["iso 9001", "iso9001", "qms", "quality management"],
    "IEC standards": ["iec standards", "iec 62304", "iec 82304", "medical device software"],
    "OWASP": ["owasp", "masvs", "asvs", "top 10", "web security testing"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management", "nist ai"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "nist sp 800-53"],
    "CIS Benchmarks": ["cis benchmarks", "cis benchmark", "cis controls", "critical security controls"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS",
        r"InformationSecurityPolicy",
        r"SecurityControls",
        r"access_control"
    ],
    "ISO 27701": [
        r"PIMS",
        r"PIIData",
        r"DataProcessor",
        r"PrivacyInformationManagement"
    ],
    "ISO 42001": [
        r"AIMS",
        r"AIGovernance",
        r"AITrustworthiness",
        r"AISafetyPolicy"
    ],
    "ISO 31000": [
        r"RiskRegister",
        r"RiskAssessment",
        r"RiskMitigation",
        r"RiskManagement"
    ],
    "ISO 9001": [
        r"QMS",
        r"QualityPolicy",
        r"ContinuousImprovement",
        r"customer_satisfaction"
    ],
    "IEC standards": [
        r"IEC[ -]62304",
        r"IEC[ -]82304",
        r"IECStandards",
        r"SoftwareLifecycle"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"WSTG",
        r"SQLInjection",
        r"CrossSiteScripting"
    ],
    "NIST AI RMF": [
        r"NIST[ -]AI[ -]RMF",
        r"AIRiskManagement",
        r"AIBiasMitigation",
        r"AISafety"
    ],
    "NIST CSF": [
        r"NIST[ -]CSF",
        r"CybersecurityFramework",
        r"SP800-53",
        r"identify_protect_detect"
    ],
    "CIS Benchmarks": [
        r"CIS[ -]Benchmarks?",
        r"CISControls",
        r"Hardening",
        r"SecureConfiguration"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications, ISO, IEC, OWASP, CIS)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Revision",
        "description": "ISO releases key updates to ISO/IEC 27001 requirements, mandating advanced information security management controls, continuous risk auditing, and strict access controls.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "ISO updates the PIMS standard, establishing mandatory guidelines for processing personally identifiable information (PII) and maintaining privacy compliance.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Mandate",
        "description": "ISO publishes ISO/IEC 42001, a revolutionary international standard specifying requirements for establishing, implementing, and maintaining an AI management system (AIMS).",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Update",
        "description": "ISO updates its risk management guidelines to enforce systematic risk assessment frameworks, risk mitigation policies, and integrated risk logs.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Standards Release",
        "description": "ISO revises ISO 9001 to mandate systematic quality management policies, continuous process improvement, and rigorous customer satisfaction auditing.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62304 Medical Device Software Lifecycle Processes Update",
        "description": "IEC introduces updated requirements for software lifecycle processes in medical device software, detailing strict design validation and configuration controls.",
        "link": "https://www.iec.ch",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard MASVS Update",
        "description": "OWASP releases a comprehensive update to the MASVS security verification standard, reinforcing protections against credential storage leaks and reverse engineering.",
        "link": "https://owasp.org",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework Guidelines 2.0",
        "description": "NIST releases updated guidelines under the AI RMF, focusing on managing trustworthiness, mitigating algorithmic bias, and validating safety controls.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework CSF 2.0 Core Implementation",
        "description": "NIST implements CSF 2.0, establishing updated core functions (Identify, Protect, Detect, Respond, Recover) for comprehensive enterprise cybersecurity management.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Critical Security Controls Hardening Guideline",
        "description": "CIS publishes new benchmarks and hardening controls, defining strict secure configuration baselines for mobile and cloud application environments.",
        "link": "https://www.cisecurity.org",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Industry Blog Rumors on ISO 27001 Fines",
        "description": "A random industry blog claims ISO 27001 is being updated next week to fine everyone who does not have purple servers.",
        "link": "https://randomblogsite.com/iso27001-rumor",
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

    # Priority 1 official domains and keywords
    p1_domains = [
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "nist.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "imda.gov.sg", "pdpc.gov.sg", "anpd.gov.br", "esafety.gov.au",
        "iso.org", "iec.ch", "owasp.org", "cisecurity.org"
    ]
    p1_keywords = [
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register", "international organization for standardization",
        "iec", "owasp", "cis controls", "cis benchmarks"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

    priority = 4  # Default to 4 if nothing matches

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
                    common_terms = {"standards", "iso", "iec", "nist", "security", "framework", "owasp"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 standards.
    Excludes typical build, dependency, and test directories.
    """
    matches = {cat: [] for cat in CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
        ".dart_tool", "Carthage", "androidTest", "__tests__", "dist"
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
                    ".kt", ".java", ".xml", ".gradle", ".kts", ".json", ".js",
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html"
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
                                    break  # match found for this line and category, proceed
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
    Classifies incoming announcements into the 10 standards categories.
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
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break  # Break keyword loop for this category

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

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Review the updated Information Security Management System guidelines to ensure strict access controls, logs, and continuous vulnerability verification mechanisms are in place."
            )
            impl_checklist.append("- [ ] Align access control structures and system logs with the latest ISO 27001 revision.")
            risk_assessment.append(f"- *{cat}*: Non-conformity in the annual audit, risking loss of certifications and compliance clearance.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Audit privacy information management controls (PIMS), confirming the classification, storage, and processing rules of personally identifiable information (PII)."
            )
            impl_checklist.append("- [ ] Verify that PII data models and processing mechanisms meet the ISO 27701 expectations.")
            risk_assessment.append(f"- *{cat}*: Regulatory and organizational privacy non-compliance, with potential breaches in user information lifecycle.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Configure the AI Management System (AIMS) structures to verify continuous model evaluation, system auditability, and safety protocols."
            )
            impl_checklist.append("- [ ] Establish AI system registries and continuous trustworthiness evaluation metrics.")
            risk_assessment.append(f"- *{cat}*: Risks of untrustworthy AI processing, bias propagation, and non-compliance with global algorithmic standards.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Synchronize the repository risk management processes with the risk assessment register, defining mitigation and continuous tolerance criteria."
            )
            impl_checklist.append("- [ ] Update the integrated organizational risk registers and assign mitigation criteria.")
            risk_assessment.append(f"- *{cat}*: Undetected engineering or operational risks propagating to production without mitigation plans.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Document quality manual parameters, integrating QA validation checks and customer satisfaction feedback loops into delivery flows."
            )
            impl_checklist.append("- [ ] Establish Quality Management System (QMS) code gates and QA audit logging.")
            risk_assessment.append(f"- *{cat}*: Degraded code delivery quality and process inefficiencies due to missing systematic QA controls.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62304/82304 Software Lifecycle processes, detailing strict software configuration validation and architectural unit tests."
            )
            impl_checklist.append("- [ ] Run unit testing and architectural compliance audits to clear safety-critical requirements.")
            risk_assessment.append(f"- *{cat}*: Operational failures in critical environments due to inadequate unit testing coverage and design validations.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Validate implementation blocks against common OWASP vulnerabilities, and verify MASVS L1 and L2 guidelines on local storage and reverse engineering."
            )
            impl_checklist.append("- [ ] Implement strict static audits against SQL injections and Cross-Site Scripting (XSS).")
            risk_assessment.append(f"- *{cat}*: Exploitable security vulnerabilities in web or mobile components, compromising system endpoints.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Align algorithmic processes with NIST AI Risk Management guidelines, conducting rigorous bias profiling and robustness checks."
            )
            impl_checklist.append("- [ ] Implement algorithmic validation pipelines to measure trustworthiness and mitigate bias.")
            risk_assessment.append(f"- *{cat}*: Exposure to legal liabilities and reputational damage due to unmonitored automated decisions.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map structural controls to NIST CSF 2.0 Core functions (Identify, Protect, Detect, Respond, Recover) to verify robust defense-in-depth."
            )
            impl_checklist.append("- [ ] Conduct comprehensive audits mapping configurations to cybersecurity core parameters.")
            risk_assessment.append(f"- *{cat}*: Inadequate response readiness and vulnerability exposure during critical cybersecurity incidents.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Audit system configurations against CIS Benchmarks, applying recommended server, database, and system hardening guidelines."
            )
            impl_checklist.append("- [ ] Execute baseline configuration hardening scripts to eliminate insecure defaults.")
            risk_assessment.append(f"- *{cat}*: Unauthorized system access via unhardened configuration variables and default credentials.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of the technical standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to bring the repository and deployment environments into complete compliance with modern technical standards. It addresses security, privacy, quality, risk, and specialized AI/cybersecurity standards.

## 2. Background
Adhering to international standards ensures the safety, security, and quality of our software platforms. Standard validators and compliance auditors scan for aligned processes, systematic controls, and documented procedures. This PR proactively clears identified gaps.

## 3. Regulatory change
- **Security & Privacy (ISO 27001, ISO 27701, OWASP, NIST CSF, CIS Benchmarks)**: Full implementation of information security management, privacy details, secure baseline hardening, and threat protections.
- **AI Trustworthiness (ISO 42001, NIST AI RMF)**: Robust lifecycle governance, bias mitigation, and safety controls for integrated models.
- **Quality & Safety (ISO 9001, ISO 31000, IEC Standards)**: Structured lifecycle management, quality verification, and systematic risk management frameworks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High compliance risk and audit failures if technical standards and hardening controls remain unaligned.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. System interfaces and configuration options are extended to align with standards without disrupting active consumer features or breaking existing deployment scripts.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated validation checks.

## 10. Testing checklist
- [ ] Verify that static configuration audits check for unhardened variables.
- [ ] Validate that unit test suites cover standard unit checks.
- [ ] Verify that audit logs and system monitoring flags capture access control violations.
- [ ] Perform risk assessments on newly added modules and verify they are recorded.

## 11. Documentation checklist
- [ ] Update structural guidelines and development playbooks.
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed actions.
- [ ] Confirm quality manual and security controls reflect current production baselines.

## 12. Compliance impact
- **Certification Readiness**: Facilitates clean passages through ISO and NIST compliance audits.
- **Improved Security Posture**: Mitigates typical OWASP and CIS risks, creating robust security gates.
- **Customer Assurance**: Builds deep institutional trust by providing certified, standardized compliance declarations.

## 13. Breaking changes
- No functional breaking changes are introduced. Baseline configurations are hardened to secure defaults.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that baseline configuration variables are hardened.

## 15. Approver recommendations
Verify that the certification scope and audit logs align with the active profiles before submitting changes for final release approval.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
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
            lines.append("- [ ] **Task 1**: Update information security controls and continuous auditing logs.")
            lines.append("- [ ] **Task 2**: Establish formal access control reviews.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Document personal data processing models under the PIMS guidelines.")
            lines.append("- [ ] **Task 2**: Implement explicit consent managers for PII lifecycle auditing.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Integrate continuous model monitoring and trustworthiness evaluation gates.")
            lines.append("- [ ] **Task 2**: Formulate structured risk mitigation checklists for automated tools.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Align active risk registers with the continuous risk tolerance guidelines.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Formulate formal QA code checklists and continuous delivery validation gates.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Audit unit testing coverage and lifecycle validations for safety software.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Enforce static checks against common vulnerabilities (injections, XSS, broken auth).")
            lines.append("- [ ] **Task 2**: Align code modules with MASVS client-side storage standards.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Set up bias validation pipelines and algorithmic transparency logs.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Map critical infrastructure and security profiles to CSF Core functions.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Enforce hardening scripts on environment baseline variables and configurations.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all standard criteria for {cat} are checked and handled.")
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

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/cybersecurity/rss.xml"))

    # Fallback to mock data if live has no updates, or mock is explicitly requested (default)
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

    # Sort classified updates to keep them structured
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

    print(f"Monitored and classified {len(classified_updates)} policy/requirement updates ({blocked_updates_count} blocked due to source trust validation):")
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    # 3. Scan the codebase for signals related to these categories
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
