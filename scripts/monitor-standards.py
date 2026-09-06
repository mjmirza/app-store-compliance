#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards categories:
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

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso/iec 27001", "information security management", "isms", "annex a controls"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "privacy information management", "pims"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "ai management system", "aims", "ai governance"],
    "ISO 31000": ["iso 31000", "risk management framework", "risk assessment process", "risk treatment"],
    "ISO 9001": ["iso 9001", "quality management system", "qms", "quality policy"],
    "IEC standards": ["iec standards", "iec 62304", "iec 82304", "iec 62443", "functional safety", "medical device software", "industrial cybersecurity"],
    "OWASP": ["owasp", "owasp top 10", "owasp masvs", "owasp asvs", "mobile application security verification"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "govern map measure manage", "trustworthy ai"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "identify protect detect respond recover", "nist csf 2.0"],
    "CIS Benchmarks": ["cis benchmarks", "center for internet security", "cis hardened images", "cis os hardening", "cis control"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"information_security_policy",
        r"AnnexA"
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_management_system"
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"ai_risk_assessment"
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_assessment",
        r"risk_matrix",
        r"risk_treatment"
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_policy",
        r"quality_management"
    ],
    "IEC standards": [
        r"IEC62304",
        r"IEC82304",
        r"IEC62443",
        r"IEC_standard",
        r"functional_safety"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"top_10"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"AI_RMF",
        r"trustworthy_ai",
        r"govern_map_measure_manage"
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"CSF_2\.0",
        r"identify_protect_detect_respond_recover"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Control",
        r"cis_hardening"
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

# 10 Comprehensive Mock Announcements for all 10 categories + 1 unverified announcement
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STANDARDS-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Management System Controls Alignment Update",
        "description": "ISO/IEC 27001 updates require organizational alignment of Annex A security controls including threat intelligence, web filtering, and secure coding practices across all software development lifecycles.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Extension Requirements",
        "description": "ISO/IEC 27701 extends ISO/IEC 27001 for privacy management. Organizations acting as PII controllers and processors must document privacy controls, PII principal rights mechanisms, and privacy impact assessments.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Governance Framework Release",
        "description": "ISO/IEC 42001 provides requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS). It mandates AI risk assessment, impact assessments, and data quality management.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Integration in Software Engineering",
        "description": "ISO 31000 provides principles and framework for managing risk. Modern engineering teams must integrate formal risk identification, risk evaluation, and continuous risk monitoring into release candidate evaluation.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Process Standard Compliance Update",
        "description": "ISO 9001 QMS standard emphasizes customer satisfaction, continuous process improvement, and rigorous software validation testing pipelines to prevent operational defects.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Software Lifecycle Processes and Safety Critical Verification",
        "description": "IEC standards mandate rigorous software lifecycle processes, risk management, design verification, and automated regression test validation for safety-related and health-related applications.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) v2.1 Standards Release",
        "description": "OWASP MASVS establishes baseline security requirements for mobile applications across storage, cryptography, authentication, network communication, platform interaction, and resilience testing.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Core Functions Guidance",
        "description": "NIST AI RMF outlines four core functions (GOVERN, MAP, MEASURE, MANAGE) to manage risks to individuals, organizations, and society associated with artificial intelligence systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Tier Guidelines",
        "description": "NIST CSF 2.0 expands coverage beyond critical infrastructure to all organizations, adding GOVERN to IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER functions.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STANDARDS-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks OS and Container Hardening Standards Updates",
        "description": "Center for Internet Security (CIS) Benchmarks deliver consensus-based best-practice security configuration guidelines for operating systems, cloud environments, and container runtimes.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    # Unverified announcement to test blocking
    {
        "id": "STANDARDS-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Post Rumors on ISO 27001 Automatic Revocations",
        "description": "An unverified personal blog claims that ISO 27001 certificates will be revoked automatically for all repos without an immediate dark mode. No official bodies were referenced.",
        "link": "https://randomblogsite.com/iso-rumor",
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
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg"
    ]
    p1_keywords = [
        "iso/iec", "international organization for standardization", "nist",
        "owasp", "center for internet security", "cis benchmark",
        "european commission", "official journal", "enisa", "edpb", "ftc",
        "cisa", "ico", "government publication"
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
                    common_terms = {"iso", "nist", "owasp", "iec", "cis", "standards", "security"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcement, all_announcements=None):
    """
    Enforces strict source trust hierarchy validation.
    Logs alerts to stderr and returns True if allowed for PR generation, False if blocked.
    """
    priority, is_verified = classify_source_and_verify(announcement, None)
    if priority in (4, 5) and not is_verified:
        print(
            f"ALERT [Source Trust Hierarchy]: Unverified Priority {priority} source detected: '{announcement.get('title')}'. PR generation blocked.",
            file=sys.stderr
        )
        return False
    return True


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards.
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
                    ".py", ".kt", ".java", ".xml", ".gradle", ".kts", ".json", ".js",
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html", ".sh", ".yml", ".yaml"
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
            url, headers={"User-Agent": "Mozilla/5.0 (TechnicalStandardsComplianceMonitor/1.0)"}
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
                        "id": ann.get("id", "STANDARDS-UPDATE-" + str(hash(title))[:6]),
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
    testing_checklist = []
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
                f"- **{cat}**: Align information security management systems (ISMS) controls with updated Annex A guidance."
            )
            impl_checklist.append("- [ ] Document threat intelligence and secure coding guidelines in ISO 27001 ISMS playbook.")
            testing_checklist.append("- [ ] Verify automated security vulnerability scanners pass against ISO 27001 control criteria.")
            risk_assessment.append(f"- *{cat}*: Audit non-compliance during annual ISMS recertification.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Update Privacy Information Management System (PIMS) controls and PII principal rights mechanisms."
            )
            impl_checklist.append("- [ ] Update PIMS documentation and PII processing log formats.")
            testing_checklist.append("- [ ] Conduct privacy impact test suites on user data deletion and export endpoints.")
            risk_assessment.append(f"- *{cat}*: Regulatory fines and loss of ISO 27701 privacy accreditation.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance and risk management processes."
            )
            impl_checklist.append("- [ ] Formulate ISO 42001 AIMS risk assessment and AI system impact assessment templates.")
            testing_checklist.append("- [ ] Execute automated model evaluation test cases for AI transparency and output safety.")
            risk_assessment.append(f"- *{cat}*: Unregulated AI deployment exposing the enterprise to AI Act liabilities.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate formal ISO 31000 risk management principles into release evaluation workflows."
            )
            impl_checklist.append("- [ ] Update risk treatment plan registers and risk assessment matrices.")
            testing_checklist.append("- [ ] Perform automated risk threshold verifications in release readiness pipelines.")
            risk_assessment.append(f"- *{cat}*: Unidentified risk vectors causing production regressions.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Reinforce Quality Management System (QMS) processes and continuous validation workflows."
            )
            impl_checklist.append("- [ ] Establish QMS quality metrics and automated code quality gates.")
            testing_checklist.append("- [ ] Run comprehensive unit and integration test coverage checks (minimum 80% coverage).")
            risk_assessment.append(f"- *{cat}*: Quality audit findings and process non-conformities.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Ensure compliance with IEC 62304 / 82304 / 62443 functional safety and software lifecycle requirements."
            )
            impl_checklist.append("- [ ] Document software hazard analysis and safety class requirements.")
            testing_checklist.append("- [ ] Execute safety-critical regression tests and fault injection test suites.")
            risk_assessment.append(f"- *{cat}*: Safety classification failures and regulatory blockages.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align mobile and web codebases with OWASP MASVS and ASVS security verification standards."
            )
            impl_checklist.append("- [ ] Audit mobile binary security controls against OWASP MASVS criteria.")
            testing_checklist.append("- [ ] Execute static analysis (SAST) and dynamic security test scripts.")
            risk_assessment.append(f"- *{cat}*: Security vulnerabilities leading to exploitation or data breaches.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF core functions (GOVERN, MAP, MEASURE, MANAGE) across AI pipelines."
            )
            impl_checklist.append("- [ ] Document AI system mapping and governance roles per NIST AI RMF.")
            testing_checklist.append("- [ ] Run NIST AI RMF measurement scripts evaluating model bias, robustness, and drift.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI system failure modes and loss of trustworthiness.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER)."
            )
            impl_checklist.append("- [ ] Map technical safeguards to NIST CSF 2.0 implementation tiers.")
            testing_checklist.append("- [ ] Execute incident response tabletop simulations and detection alert automated tests.")
            risk_assessment.append(f"- *{cat}*: Ineffective threat detection or delayed incident response times.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Benchmarks configuration guidelines across operating system, cloud, and container configurations."
            )
            impl_checklist.append("- [ ] Harden container image specifications according to CIS Benchmarks.")
            testing_checklist.append("- [ ] Execute automated CIS compliance audit scanners against target environments.")
            risk_assessment.append(f"- *{cat}*: Misconfiguration vulnerabilities in production deployments.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of technical standards configurations).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards compliance."
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Execute standard test suites."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to align the repository with updated technical standards across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards define industry best practices for security management, privacy information, AI governance, risk management, quality control, functional safety, and cybersecurity frameworks. Maintaining continuous alignment ensures organizational readiness and mitigates operational risk.

## 3. Regulatory change
- **ISO / IEC Standards**: Mandatory controls alignment across ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk (ISO 31000), QMS (ISO 9001), and Software Safety (IEC 62304/82304).
- **OWASP & CIS Frameworks**: Application security verification (OWASP MASVS/ASVS) and operating environment hardening (CIS Benchmarks).
- **NIST AI RMF & CSF 2.0**: Operationalization of AI risk management and enterprise cybersecurity governance.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to High risk of audit findings, certification gaps, or security vulnerabilities if standards updates are not implemented.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards updates modify operational controls, documentation, testing protocols, and configuration baselines without breaking existing user features.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated standards compliance guard.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run automated compliance test scripts and verify all assertions pass.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed actions.
- [ ] Maintain up-to-date technical standards mapping tables across all affected repository sections.

## 12. Compliance impact
- **Certification Readiness**: Preserves ISO and IEC certification readiness.
- **Security Posture**: Strengthens security posture against OWASP, NIST, and CIS baselines.
- **Governance**: Ensures AI transparency and risk governance under NIST AI RMF and ISO 42001.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced quality and safety checks enforce strict validation prior to build acceptance.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified against Priority 1 sources.
- [ ] Verify that testing updates cover all modified standards components.

## 15. Approver recommendations
Verify that the technical standards controls documentation is complete and that all automated testing pipelines pass successfully before approving the compliance merge.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Includes identification of gaps, implementation tasks, documentation updates, and testing updates.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Standards Requirements Update Log",
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
        lines.append("- **Regulatory Impact**: High priority technical standards compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1 (Implementation)**: Update ISMS controls documentation and secure coding policies.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Run automated security scans verifying ISO 27001 control compliance.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1 (Implementation)**: Document PIMS privacy controls and PII processing log specifications.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Execute automated privacy test suites for PII handling endpoints.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1 (Implementation)**: Establish AIMS governance roles and AI risk assessment procedures.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Run AI model evaluation tests checking for safety and output transparency.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1 (Implementation)**: Incorporate ISO 31000 risk treatment matrices in engineering playbooks.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Validate automated risk threshold checks in deployment pipelines.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1 (Implementation)**: Define QMS process metrics and continuous improvement guidelines.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Run full regression and test coverage suites to satisfy QMS criteria.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1 (Implementation)**: Document software safety classification and hazard analysis under IEC 62304/82304.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Execute fault injection and safety-critical automated test scripts.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1 (Implementation)**: Audit codebase against OWASP MASVS and ASVS control requirements.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Run static analysis (SAST) and dynamic security test suites.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1 (Implementation)**: Map AI components to NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Execute measurement scripts for model bias, accuracy, and robustness.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1 (Implementation)**: Map technical safeguards to NIST CSF 2.0 functions.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Test incident response notification triggers and threat detection alerts.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1 (Implementation)**: Apply CIS hardening guidelines to environment configuration files.")
            lines.append("- [ ] **Task 2 (Testing Update)**: Execute automated CIS compliance audit scripts against target baselines.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all technical standards criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("## Testing Updates Summary")
    lines.append("")
    lines.append("1. **Security & Vulnerability Testing**: Run static analysis and automated vulnerability scanners for ISO 27001, OWASP, and CIS Benchmarks.")
    lines.append("2. **Privacy Testing**: Execute user data lifecycle and PII endpoint test suites for ISO 27701.")
    lines.append("3. **AI Safety Testing**: Run automated AI model evaluation and risk measurement scripts for ISO 42001 and NIST AI RMF.")
    lines.append("4. **Safety-Critical Testing**: Execute fault injection and safety lifecycle verification tests for IEC standards.")
    lines.append("5. **Quality & Risk Testing**: Run unit, integration, and risk-threshold automated checks for ISO 9001, ISO 31000, and NIST CSF.")
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
        "--live", action="store_true", help="Fetch live technical standards RSS/Atom feeds"
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
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
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
        if not enforce_strict_source_trust_hierarchy(u, announcements):
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(f"Monitored and classified {len(classified_updates)} standards updates ({blocked_updates_count} blocked due to source trust validation):")
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
