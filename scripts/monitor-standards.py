#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 distinct technical standards categories:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates.
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

# Keywords used to classify incoming standards updates/announcements
CATEGORY_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso/iec 27001", "isms", "information security management system", "annex a controls"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "pims", "privacy information management system", "privacy controls"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "aims", "artificial intelligence management system", "ai management system"],
    "ISO 31000": ["iso 31000", "risk management guidelines", "enterprise risk management", "risk assessment framework"],
    "ISO 9001": ["iso 9001", "qms", "quality management system", "quality management controls"],
    "IEC standards": ["iec standards", "iec 62443", "iec 82304", "iec 62304", "international electrotechnical commission"],
    "OWASP": ["owasp", "owasp top 10", "masvs", "asvs", "owasp LLM top 10", "owasp API top 10", "samms"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "nist ai 100", "govern map measure manage", "trustworthy ai"],
    "NIST CSF": ["nist csf", "nist csf 2.0", "cybersecurity framework", "identify protect detect respond recover govern"],
    "CIS Benchmarks": ["cis benchmarks", "center for internet security", "cis controls", "cis hardened images", "cis benchmark controls"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"securityPolicy",
        r"accessControl",
        r"assetManagement"
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacyImpactAssessment",
        r"dataRetentionPolicy",
        r"consentManagement"
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"aiGovernance",
        r"modelRiskManagement",
        r"aiSafety"
    ],
    "ISO 31000": [
        r"ISO31000",
        r"riskRegister",
        r"riskAssessment",
        r"riskMitigation"
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"qualityControl",
        r"auditLog",
        r"processControl"
    ],
    "IEC standards": [
        r"IEC62443",
        r"IEC62304",
        r"IEC82304",
        r"medicalDeviceSoftware",
        r"industrialControl"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sqlInjection",
        r"xssFilter",
        r"csrfToken"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"aiRiskManagement",
        r"biasMitigation",
        r"explainability",
        r"modelValidation"
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurityFramework",
        r"incidentResponse",
        r"threatDetection"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"cisControl",
        r"hardeningConfig",
        r"secureBaseline"
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

# 10 Comprehensive Mock Announcements covering all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STANDARDS-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Revision",
        "description": "International Organization for Standardization updates ISO/IEC 27001 Annex A controls, requiring enhanced threat intelligence, cloud services security management, physical security monitoring, and secure coding practices.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Update",
        "description": "Updates to ISO/IEC 27701 establish rigorous guidelines for PII controllers and processors, mandating explicit consent records, automated PII mapping, cross-border transfer documentation, and Privacy Impact Assessments (PIAs).",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Standard Guidance",
        "description": "The ISO/IEC 42001 standard specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS), including AI risk assessments and continuous impact monitoring.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 03 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines for Technical Infrastructure",
        "description": "ISO 31000 updates enterprise risk management principles, mandating systematic risk identification, probability/impact evaluation matrices, automated mitigation workflows, and continuous risk register auditing.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 04 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Development Controls Alignment",
        "description": "ISO 9001 updates emphasize software quality control processes, rigorous release gating, traceability of requirements to code, automated continuous integration testing, and defect root-cause analysis.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 05 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 62304 Cybersecurity and Software Lifecycle Standards",
        "description": "The International Electrotechnical Commission updates security and lifecycle standards for connected software systems, mandating secure boot verification, component inventory SBOMs, and safe fallback handling.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 06 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 and MASVS Security Controls Revision",
        "description": "OWASP updates Top 10 vulnerability categories and Mobile Application Security Verification Standard (MASVS), emphasizing anti-tampering, secure data storage at rest, network transport security, and LLM prompt injection defenses.",
        "link": "https://owasp.org/www-project-top-ten/",
        "pubDate": "Sun, 07 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-NIST-AIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Companion Guidelines",
        "description": "NIST issues updated AI RMF guidelines across GOVERN, MAP, MEASURE, and MANAGE functions, establishing technical requirements for AI trustworthiness, bias detection, explainability, and post-deployment monitoring.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 08 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Implementation Core Directives",
        "description": "NIST CSF 2.0 expands coverage to all organizational sectors, introducing the GOVERN function alongside Identify, Protect, Detect, Respond, and Recover, with explicit software supply chain risk management rules.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 09 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STANDARDS-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Center for Internet Security Configuration Rules",
        "description": "Center for Internet Security releases updated CIS Benchmarks and CIS Controls, mandating strict OS hardening baselines, automated configuration drift detection, secure container builds, and minimal permission profiles.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 10 Jun 2026 19:00:00 GMT"
    },
    # Unverified announcement sample to test trust hierarchy blocking
    {
        "id": "STANDARDS-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO 27001 Changes",
        "description": "An unverified blog claims ISO 27001 is banning all cloud servers next month. This is an unverified blog post.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 11 Jun 2026 20:00:00 GMT"
    }
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified).
    """
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 official domains and keywords
    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg"
    ]
    p1_keywords = [
        "iso/iec", "international organization for standardization",
        "international electrotechnical commission", "national institute of standards and technology",
        "open worldwide application security project", "center for internet security",
        "european commission", "enisa", "edpb", "ftc", "cisa", "ico", "government publication"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

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
        has_p1_ref = any(d in combined for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in combined
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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "framework"}
                    if words.intersection(other_words).intersection(common_terms):
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards categories.
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
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html", ".py", ".sh"
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
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_checklist = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        cite_key = (cat, u['title'], u['link'])
        if cite_key not in seen_citations:
            seen_citations.add(cite_key)
            citations_list.append(
                f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
            )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        if cat == "ISO 27001":
            migration_steps.append(f"- **{cat}**: Audit ISMS controls against revised Annex A provisions, updating threat intelligence policies and secure coding guidelines.")
            impl_checklist.append("- [ ] Align Annex A controls with ISO 27001 ISMS provisions.")
            risk_assessment.append(f"- *{cat}*: Non-conformity during external ISMS certification audit.")
            testing_checklist.append("- [ ] Run automated threat intelligence policy audit checks.")
        elif cat == "ISO 27701":
            migration_steps.append(f"- **{cat}**: Update Privacy Information Management System (PIMS) documentation, verifying automated PII inventory mapping.")
            impl_checklist.append("- [ ] Update PIMS data processing inventory and consent logging.")
            risk_assessment.append(f"- *{cat}*: Potential privacy breach liabilities and PIMS non-compliance finding.")
            testing_checklist.append("- [ ] Execute automated PII scanning across database schemas and log buffers.")
        elif cat == "ISO 42001":
            migration_steps.append(f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance controls for interactive models.")
            impl_checklist.append("- [ ] Implement AIMS model risk assessment and impact monitoring controls.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI model behavior violating enterprise governance boundaries.")
            testing_checklist.append("- [ ] Verify continuous AI model output evaluation test suites pass.")
        elif cat == "ISO 31000":
            migration_steps.append(f"- **{cat}**: Refresh risk management matrix and ensure automated risk registration for technical infrastructure.")
            impl_checklist.append("- [ ] Update technical risk register and probability/impact evaluation matrix.")
            risk_assessment.append(f"- *{cat}*: Unmitigated infrastructure risk resulting in unexpected operational outages.")
            testing_checklist.append("- [ ] Audit infrastructure risk score calculations against ISO 31000 criteria.")
        elif cat == "ISO 9001":
            migration_steps.append(f"- **{cat}**: Enhance software development QMS process controls and traceability matrix from requirements to release.")
            impl_checklist.append("- [ ] Verify requirements-to-code traceability and QMS release gates.")
            risk_assessment.append(f"- *{cat}*: Quality management audit findings due to untracked software defects.")
            testing_checklist.append("- [ ] Confirm CI/CD automated release gate tests execute cleanly.")
        elif cat == "IEC standards":
            migration_steps.append(f"- **{cat}**: Review IEC 62443 / IEC 62304 lifecycle controls, verifying Software Bill of Materials (SBOM) generation.")
            impl_checklist.append("- [ ] Generate and validate SBOM inventory for compiled release builds.")
            risk_assessment.append(f"- *{cat}*: Undetected vulnerable third-party library dependencies in production.")
            testing_checklist.append("- [ ] Run automated SBOM vulnerability scan on build artifacts.")
        elif cat == "OWASP":
            migration_steps.append(f"- **{cat}**: Update application security controls against OWASP Top 10 and MASVS requirements.")
            impl_checklist.append("- [ ] Implement OWASP MASVS anti-tampering and secure storage controls.")
            risk_assessment.append(f"- *{cat}*: Exploitation of top application vulnerabilities by malicious actors.")
            testing_checklist.append("- [ ] Execute OWASP ZAP and static security scanning suites.")
        elif cat == "NIST AI RMF":
            migration_steps.append(f"- **{cat}**: Integrate NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions into AI pipelines.")
            impl_checklist.append("- [ ] Implement NIST AI RMF trustworthiness and bias detection controls.")
            risk_assessment.append(f"- *{cat}*: Algorithmic bias and lack of explainability in AI-driven features.")
            testing_checklist.append("- [ ] Run model bias evaluation and explainability test scripts.")
        elif cat == "NIST CSF":
            migration_steps.append(f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 GOVERN and supply chain risk directives.")
            impl_checklist.append("- [ ] Update incident response playbooks and supply chain risk controls.")
            risk_assessment.append(f"- *{cat}*: Supply chain security compromise or delayed incident response times.")
            testing_checklist.append("- [ ] Simulate cybersecurity incident response and recovery workflows.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(f"- **{cat}**: Apply CIS Benchmarks OS and container hardening configurations to build environments.")
            impl_checklist.append("- [ ] Apply CIS hardening configuration benchmarks to deployment scripts.")
            risk_assessment.append(f"- *{cat}*: Container escape or server compromise due to unhardened configurations.")
            testing_checklist.append("- [ ] Execute automated CIS configuration compliance scans.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform general review of standards documentation."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Verify standards compliance tests execute successfully."

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into alignment with updated international technical standards and cybersecurity frameworks. It introduces implementation tasks, documentation updates, and testing verification controls across ISO, IEC, OWASP, NIST, and CIS standards.

## 2. Background
Maintaining compliance with established technical standards ensures robust governance, risk management, cybersecurity resilience, and software quality. Continuous monitoring of technical standards updates ensures that organizational processes and codebases adapt to evolving international security baselines.

## 3. Regulatory change
- **ISO/IEC Standards**: Alignment with revised ISO 27001 (ISMS), ISO 27701 (PIMS), ISO 42001 (AIMS), ISO 31000 (Risk Management), ISO 9001 (QMS), and IEC standards.
- **Security & Risk Frameworks**: Implementation of updated OWASP Top 10/MASVS controls, NIST AI RMF 1.0 companion rules, NIST CSF 2.0 directives, and CIS Benchmarks hardening rules.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit findings and security vulnerabilities if technical standards controls remain unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards updates introduce procedural, configuration, and structural enhancements without breaking existing application APIs or data formats.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Ensure all automated standards compliance test suites execute without failure.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Update technical architecture diagrams and risk management policy documentation.

## 12. Compliance impact
- **Audit Readiness**: Ensures clean passage during ISO/IEC certification and external cybersecurity audits.
- **Cyber Resilience**: Strengthens application defenses against OWASP-identified vulnerability vectors.
- **Governance Integrity**: Fulfills NIST AI RMF and CSF 2.0 organizational governance directives.

## 13. Breaking changes
- No functional breaking changes. Standard hardening configurations and release gating requirements apply to future builds.

## 14. Review checklist
- [ ] Verify that the pull request description is 100% free of emojis.
- [ ] Confirm all official citations originate from Priority 1-3 verified sources.
- [ ] Verify that automated tests pass cleanly across all supported platforms.

## 15. Approver recommendations
Verify that the technical risk register and SBOM inventory generation steps execute cleanly before authorizing deployment. Ensure that all security hardening profiles reflect the latest CIS Benchmarks.
"""
    return pr_template


SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Re-run the monitor with `--live` against the real feeds before treating anything here",
    "> as an actual requirement.",
    "",
]


def update_documentation_report(updates, output_filepath, is_simulated=False):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ])

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

    processed_task_categories = set()
    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        task_key = (cat, is_verified)
        if task_key in processed_task_categories:
            continue
        processed_task_categories.add(task_key)

        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Standards Impact**: High priority technical governance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Review Annex A information security control mappings.")
            lines.append("- [ ] **Task 2**: Update threat intelligence and secure coding guidelines.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Update Privacy Information Management System (PIMS) documentation.")
            lines.append("- [ ] **Task 2**: Verify automated PII mapping and data retention controls.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Establish Artificial Intelligence Management System (AIMS) policies.")
            lines.append("- [ ] **Task 2**: Conduct AI risk assessments and continuous impact monitoring.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Refresh enterprise infrastructure risk register.")
            lines.append("- [ ] **Task 2**: Establish automated risk score evaluation matrices.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Update software Quality Management System release gates.")
            lines.append("- [ ] **Task 2**: Ensure requirements-to-code traceability across build pipelines.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Verify IEC 62443 / IEC 62304 software lifecycle compliance.")
            lines.append("- [ ] **Task 2**: Automate Software Bill of Materials (SBOM) generation.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Conduct OWASP Top 10 / MASVS vulnerability audit.")
            lines.append("- [ ] **Task 2**: Implement anti-tampering and secure storage controls.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Map AI features to NIST AI RMF GOVERN/MAP/MEASURE/MANAGE functions.")
            lines.append("- [ ] **Task 2**: Implement model bias detection and explainability checks.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align cybersecurity framework with NIST CSF 2.0 GOVERN function.")
            lines.append("- [ ] **Task 2**: Update supply chain risk management directives.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Apply CIS Benchmarks OS and container hardening templates.")
            lines.append("- [ ] **Task 2**: Run automated configuration drift detection tools.")
        else:
            lines.append(f"- [ ] **Task**: Verify technical standards criteria for {cat}.")
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
        description="Monitor Technical Standards Compliance Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards RSS feeds"
    )
    parser.add_argument(
        "--mock",
        type=str,
        default=None,
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
        default=None,
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default=None,
        help="Filepath to save the drafted PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    announcements = []

    out_dest = sys.stderr if args.json else sys.stdout

    if args.live:
        print("Fetching live technical standards RSS feeds...", file=out_dest)
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print("Data. sample announcements built into this script, not live news.", file=out_dest)
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
    else:
        print("Data. live feeds, fetched just now.", file=out_dest)

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

    out_dest = sys.stderr if args.json else sys.stdout

    print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):", file=out_dest)
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}", file=out_dest)

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...", file=out_dest)
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.", file=out_dest)

    if not args.json:
        if args.output_docs:
            os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
            update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock)
        else:
            print("No file written. Pass --output-docs <path> to save this report.")

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

    if not args.json:
        if args.pr_output:
            try:
                os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
                with open(args.pr_output, "w", encoding="utf-8") as f:
                    f.write(pr_draft)
                print(f"PR draft written successfully to: {args.pr_output}")
            except Exception as e:
                print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
        else:
            print("No PR draft written. Pass --pr-output <path> to save it.")

    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u)
            cat = u["category"]
            report_data.append({
                "category": cat,
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
