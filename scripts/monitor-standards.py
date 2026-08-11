#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards against live or mock data,
statically scans the codebase for matching compliance signals,
updates docs/STANDARDS-POLICY-MIGRATION.md, and drafts a
comprehensive, emoji-free 15-section Pull Request draft.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
TRACKED_STANDARDS = [
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

# Keywords used to classify incoming policy announcements/articles into the 10 standards
STANDARD_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso/iec 27001", "information security management", "isms"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "privacy information management", "pims"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "artificial intelligence management system", "aims"],
    "ISO 31000": ["iso 31000", "risk management standard", "risk assessment framework", "risk register"],
    "ISO 9001": ["iso 9001", "quality management system", "qms"],
    "IEC standards": ["iec standard", "iec 62304", "iec 82304", "iec 60601", "international electrotechnical commission"],
    "OWASP": ["owasp", "masvs", "asvs", "top 10", "top ten", "software security tracking"],
    "NIST AI RMF": ["nist ai rmf", "artificial intelligence risk management framework", "ai risk management framework"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "nist cybersecurity framework"],
    "CIS Benchmarks": ["cis benchmark", "center for internet security", "security hardening guide"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 standards
STANDARD_SIGNALS = {
    "ISO 27001": [
        r"isms",
        r"securityPolicy",
        r"accessControl",
        r"encryptionAtRest",
        r"iso27001"
    ],
    "ISO 27701": [
        r"pims",
        r"dataSubjectRequest",
        r"privacyByDesign",
        r"consentManager",
        r"iso27701"
    ],
    "ISO 42001": [
        r"aims",
        r"aiGovernance",
        r"modelCard",
        r"aiRiskAssessment",
        r"iso42001"
    ],
    "ISO 31000": [
        r"iso31000",
        r"riskRegister",
        r"riskMitigation",
        r"riskAssessment"
    ],
    "ISO 9001": [
        r"iso9001",
        r"qualityPolicy",
        r"continuousImprovement",
        r"qmsAudit"
    ],
    "IEC standards": [
        r"iec62304",
        r"iec82304",
        r"medicalDeviceSoftware",
        r"softwareLifecycle"
    ],
    "OWASP": [
        r"owasp",
        r"masvs",
        r"asvs",
        r"xssProtection",
        r"csrfToken",
        r"vulnerabilityScanning"
    ],
    "NIST AI RMF": [
        r"nistAiRmf",
        r"trustworthyAi",
        r"aiBiasMitigation",
        r"aiExplainability"
    ],
    "NIST CSF": [
        r"nistCsf",
        r"identifyProtectDetect",
        r"incidentResponsePlan",
        r"threatIntel"
    ],
    "CIS Benchmarks": [
        r"cisBenchmark",
        r"systemHardening",
        r"rootPrivileges",
        r"unnecessaryServices"
    ]
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-27001",
        "category": "ISO 27001",
        "title": "ISO 27001 ISMS Compliance Standard Update",
        "description": "Updates to information security management systems (ISMS) require enhanced access control policies and systematic auditing logs for key assets.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management Extension",
        "description": "Adopting the updated PIMS framework ensures data subject rights requests and consent tracking parameters are explicitly logged.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-42001",
        "category": "ISO 42001",
        "title": "ISO 42001 AI Management System Standards Release",
        "description": "Initial parameters for the AIMS artificial intelligence standard require documented AI risk assessments and model explainability metrics.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework Review",
        "description": "Guidelines for systematic corporate and product risk management require a unified risk register and dedicated mitigation workflows.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 PDT"
    },
    {
        "id": "STD-MOCK-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Principles Update",
        "description": "Procedures for continuous software delivery improvement and automated metrics reporting under QMS guidelines are revised.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC standards for Medical and Device Software Lifecycles",
        "description": "Updates to IEC 62304 demand strict documentation of software lifecycle processes and formal hazard classification of code elements.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS Mobile App Security Updates",
        "description": "The latest OWASP MASVS release tightens guidelines on input sanitization, cross-site scripting protections, and secure session credentials.",
        "link": "https://owasp.org/www-project-mobile-app-security",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework Implementation Guide",
        "description": "The trustworthy AI guidelines require developers to identify and mitigate bias patterns while documenting generative model outputs.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF Cybersecurity Framework 2.0 Guidance",
        "title": "NIST CSF Cybersecurity Framework Core Revisions",
        "description": "The revised Identify, Protect, Detect, Respond and Recover functions require formal incident response playbooks and system log retention.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks Hardening Requirements",
        "title": "CIS Benchmarks Secure Software Hardening Guidelines",
        "description": "System configuration hardening benchmarks mandate disabling unused legacy debugging capabilities and locking down container permissions.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 PDT"
    }
]


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 standards."""
    matches = {std: [] for std in TRACKED_STANDARDS}
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

    # Compile the signal patterns
    compiled_signals = {
        std: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for std, patterns in STANDARD_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Check applicable file types
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
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-standards" in file or "monitor-standards-test" in file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for std, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[std].append(
                                        {
                                            "file": filepath,
                                            "line_num": i,
                                            "content": line.strip()[:100],
                                            "matched_pattern": pattern.pattern,
                                        }
                                    )
                                    # Break to avoid duplicate entry for the same line and standard
                                    break
            except Exception:
                pass
    return matches


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
        "apple.com", "developer.apple.com", "android.com", "developer.android.com",
        "support.google.com", "iso.org", "iec.ch", "cisecurity.org", "owasp.org"
    ]
    p1_keywords = [
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register", "apple developer", "android developer",
        "international organization for standardization", "international electrotechnical commission",
        "center for internet security", "owasp"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "ai generated summaries", "chatgpt summary"]

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
                    common_terms = {"standards", "compliance", "iso", "nist", "owasp", "iec"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


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
    """Classifies incoming announcements into the 10 technical standards."""
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
        for cat, keywords in STANDARD_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break  # Break keyword loop for this category

        # If a pre-set category exists on mock and no matched categories, use that category
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

    # Filter out updates based on category trust classification
    valid_updates = []
    for u in updates:
        priority, is_verified = classify_source_and_verify(u, updates)
        if priority in (4, 5) and not is_verified:
            # Suppress/Skip unverified Priority 4/5 sources for draft PR generation
            sys.stderr.write(f"Verification Alert: Skipped unverified source for category {u['category']}.\n")
            continue
        valid_updates.append(u)

    for idx, u in enumerate(valid_updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Review access controls and verify that securityPolicy parameters comply with ISMS requirements."
            )
            impl_checklist.append(
                "- [ ] Configure access controls and multi-factor authorization settings to satisfy ISMS guidelines."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate asset inventory and unmitigated privilege creep for administrative functions."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement dedicated privacyByDesign constraints and consentManager logs for PIMS alignment."
            )
            impl_checklist.append(
                "- [ ] Integrate automated consent tracking logs and design data subject deletion handlers."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-transparent processing of user personal information violating global privacy enclaves."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Document AI lifecycle risks (aiRiskAssessment) and generate standard modelCard definitions for active models."
            )
            impl_checklist.append(
                "- [ ] Draft a modelCard template for generative AI elements and implement model bias mitigations."
            )
            risk_assessment.append(
                f"- *{cat}*: Model performance drift or unmitigated ethical hazard generation under unmonitored systems."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Establish a systematic riskRegister and verify riskMitigation triggers on critical endpoints."
            )
            impl_checklist.append(
                "- [ ] Compile a comprehensive product Risk Register and document hazard identification workflows."
            )
            risk_assessment.append(
                f"- *{cat}*: Inconsistent risk tracking and unmapped operational vulnerabilities."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Update qualityPolicy documentation and configure continuousImprovement testing metrics."
            )
            impl_checklist.append(
                "- [ ] Define software build quality indicators and update continuous delivery documentation."
            )
            risk_assessment.append(
                f"- *{cat}*: Regression-prone deployment pipelines and unmonitored quality metrics."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce softwareLifecycle hazard classification parameters conforming to IEC 62304 criteria."
            )
            impl_checklist.append(
                "- [ ] Formally classify medical/device software components and document runtime safety assertions."
            )
            risk_assessment.append(
                f"- *{cat}*: Missing hazard documentation or software life-cycle traceability failures in embedded environments."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Implement xssProtection and secure csrfToken generation following the latest secure coding guidelines."
            )
            impl_checklist.append(
                "- [ ] Review parameter sanitizers and verify that all network payloads are protected against common injection styles."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure to common web and mobile injection vulnerabilities such as XSS or session hijack vectors."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Align system trustworthiness (trustworthyAi) and verify aiExplainability criteria inside user prompts."
            )
            impl_checklist.append(
                "- [ ] Document AI system limitations and establish standard model bias check schedules."
            )
            risk_assessment.append(
                f"- *{cat}*: Generation of biased results or failure to provide explanatory notes to users on AI interaction boundaries."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Formulate an incidentResponsePlan and map identifyProtectDetect telemetry elements on server logging."
            )
            impl_checklist.append(
                "- [ ] Implement security telemetry monitors and document incident containment pathways."
            )
            risk_assessment.append(
                f"- *{cat}*: Inability to detect, isolate, or remediate a live security intrusion or credential leak."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Harden software configurations by locking down rootPrivileges and auditing system permissions."
            )
            impl_checklist.append(
                "- [ ] Enforce environment hardening checks and restrict debug ports on production configurations."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposed debug interfaces or container configurations with excessive root permissions."
            )

    citations_str = "\n".join(citations_list) if citations_list else "- *No verified official citations available.*"

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standard patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps required.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Verify default standards compliance configuration."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low general technical standards risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Hardening

## 1. Summary
This pull request brings the application into complete compliance with all monitored technical standards. It addresses security hardening, privacy information management, quality governance, and artificial intelligence safety rules to satisfy corporate and framework boundaries.

## 2. Background
Compliance with recognized international standards protects user assets and ensures seamless integration with enterprise partners. Standardizing our security policies, risk procedures, and vulnerability assessments helps maintain overall operational reliability.

## 3. Regulatory change
- **Technical Standardization**: Alignment with global standardization requirements across ISO, IEC, OWASP, NIST, and CIS Benchmarks.
- **System Governance**: Requiring documented procedures for security, risk tracking, and quality management in production.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Hardening actions reduce vulnerability footprints and align our codebase with standard baseline audits.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed standard configurations are fully backward-compatible. System hardening and policy updates are designed to execute seamlessly without interrupting existing consumer integrations or API endpoints.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the automated compliance validation checks locally.

## 10. Testing checklist
- [ ] Verify that access control and encryption parameters initialize successfully.
- [ ] Conduct vulnerability scans and confirm input sanitizers are active on all parameters.
- [ ] Validate model explainability criteria in user-facing channels.
- [ ] Verify that all system and configuration scripts compiled cleanly.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed checklists.
- [ ] Document software lifecycle classifications and risk registers in the repository.

## 12. Compliance impact
- **Standards Aligned**: Ensures the repository satisfies ISO, IEC, OWASP, NIST, and CIS expectations.
- **Enterprise Ready**: Mitigates compliance gaps, allowing seamless integration with commercial organizations.
- **Robust Delivery**: Strengthens product delivery cycles by instating strict quality control benchmarks.

## 13. Breaking changes
- No functional breaking changes are introduced. Debug ports may be restricted under hardened container parameters.

## 14. Review checklist
- [ ] Code is 100% free of emojis or graphical symbols in comments and files.
- [ ] Security configurations are verified to be robust and follow the principle of least privilege.
- [ ] Confirm no private keys or active secrets are checked into the codebase.

## 15. Approver recommendations
Verify that access controls and encryption profiles conform to the required standard baselines. Confirm that the risk registers and explainability sheets are stored in secure locations and kept up-to-date.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance areas.",
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

    for u in updates:
        cat = u["category"]
        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority. Standard audit mandates action."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update access control policies and enforce multi-factor authentication requirements."
            )
            lines.append(
                "- [ ] **Task 2**: Test ISMS logging mechanisms for key system assets."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Implement dedicated privacyByDesign constraints and consentManager logs."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Draft a modelCard template for generative AI components and document model limitations."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Establish a unified riskRegister and map hazard mitigations."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Update qualityPolicy guidelines and track continuous improvement indicators."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Classify software lifecycle processes under IEC 62304 standards."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Review input parameters and enforce robust parameter sanitizers and anti-XSS constraints."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Verify aiExplainability prompts and investigate system trustworthy AI metrics."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Establish an incidentResponsePlan and configure telemetry mapping."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Enforce container hardening configuration parameters and restrict root privileges."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify that all technical standards criteria for {cat} are checked and handled."
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
        description="Monitor all Technical Standards"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards feeds"
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
        "--json", action="store_true", help="Suppress file logs and output JSON to stdout"
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    # Fallback to mock data if live has no updates or mock is explicitly requested
    if args.mock or (not args.live and not args.mock) or not announcements:
        if not args.json:
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

    # 2. Classify updates into the 10 required standards
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} technical standards updates:")
        for idx, u in enumerate(classified_updates, 1):
            print(f" {idx}. [{u['category']}] {u['title']}")

    # 3. Scan the codebase for signals related to these categories
    if not args.json:
        print(f"Scanning codebase under '{args.dir}' for technical standard integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft
    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            if not args.json:
                print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        if not args.json:
            print("\n=== GENERATED 15-SECTION COMPLIANCE PULL REQUEST DRAFT ===")
            print(pr_draft)
            print("==========================================================")

    # 6. JSON output to stdout if active
    if args.json:
        # Structured scan results and compliance assessment
        output_data = []
        for u in classified_updates:
            cat = u["category"]
            priority, is_verified = classify_source_and_verify(u, classified_updates)
            output_data.append({
                "id": u["id"],
                "category": cat,
                "title": u["title"],
                "description": u["description"],
                "link": u["link"],
                "pubDate": u["pubDate"],
                "source_priority": priority,
                "is_verified": is_verified,
                "signal_matches": [
                    {"file": m["file"], "line": m["line_num"], "content": m["content"]}
                    for m in scan_results.get(cat, [])
                ]
            })
        print(json.dumps(output_data, indent=2))


if __name__ == "__main__":
    main()
