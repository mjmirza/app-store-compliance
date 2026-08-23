#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards: ISO 27001, ISO 27701, ISO 42001, ISO 31000,
ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
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
    "ISO 27001": [
        "iso 27001", "iso/iec 27001", "information security management system",
        "isms", "iso27001"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "privacy information management system",
        "pims", "iso27701"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "artificial intelligence management system",
        "aims", "iso42001"
    ],
    "ISO 31000": [
        "iso 31000", "risk management guidelines", "enterprise risk management",
        "iso31000"
    ],
    "ISO 9001": [
        "iso 9001", "quality management system", "qms", "iso9001"
    ],
    "IEC standards": [
        "iec 62304", "iec 82304", "iec 62443", "iec standards", "iec standard",
        "international electrotechnical commission"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "masvs", "asvs", "owasp llm", "top ten"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "nist ai 100", "nist ai"
    ],
    "NIST CSF": [
        "nist csf", "nist cybersecurity framework", "csf 2.0", "sp 800-53"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis benchmark", "center for internet security",
        "cis controls", "cis hardened images"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO-?27001",
        r"ISMS",
        r"InformationSecurityPolicy"
    ],
    "ISO 27701": [
        r"ISO-?27701",
        r"PIMS",
        r"PrivacyInformationManagement"
    ],
    "ISO 42001": [
        r"ISO-?42001",
        r"AIMS",
        r"AIManagementSystem"
    ],
    "ISO 31000": [
        r"ISO-?31000",
        r"RiskManagementFramework",
        r"RiskAssessment"
    ],
    "ISO 9001": [
        r"ISO-?9001",
        r"QualityManagement",
        r"QMS"
    ],
    "IEC standards": [
        r"IEC-?62304",
        r"IEC-?82304",
        r"IEC-?62443",
        r"IECStandards"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"Top10"
    ],
    "NIST AI RMF": [
        r"NIST-?AI-?RMF",
        r"AIRiskManagement",
        r"NIST_AI"
    ],
    "NIST CSF": [
        r"NIST-?CSF",
        r"CybersecurityFramework",
        r"SP800-53"
    ],
    "CIS Benchmarks": [
        r"CIS-?Benchmark",
        r"CISControls",
        r"CIS_Benchmark"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and agencies (ISO, IEC, NIST, OWASP, CIS Center for Internet Security, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements for all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 ISMS Controls Framework Transition Update",
        "description": "Organizations must align information security management systems with updated ISO/IEC 27001 Annex A controls including threat intelligence, web filtering, and secure coding requirements.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 guidelines update PIMS requirements for data controllers and processors, mandating explicit personal data handling controls and privacy impact assessments.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Certification Standard",
        "description": "ISO/IEC 42001 specifies requirements for establishing, implementing, and continually improving an AI Management System (AIMS) with rigorous risk assessment for machine learning models.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Guidelines Refresh",
        "description": "ISO 31000 provides updated principles and generic guidelines on risk management, requiring integrated risk identification, evaluation, and mitigation processes across technical infrastructure.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Software Lifecycle Integration",
        "description": "ISO 9001 QMS standards mandate continuous quality assurance, systematic software release controls, and documented change management procedures.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Software Lifecycle & Functional Safety Guidance",
        "description": "International Electrotechnical Commission releases updated functional safety and medical device software lifecycle standards, enforcing rigorous risk management and verification testing.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10, MASVS, and ASVS Security Controls Refresh",
        "description": "OWASP releases updated MASVS (Mobile Application Security Verification Standard) and ASVS requirements, mandating cryptographic storage, API authorization checks, and dynamic protection.",
        "link": "https://owasp.org",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "NIST AI RMF establishes core functions (Govern, Map, Measure, Manage) to address risks in AI systems, requiring continuous monitoring, bias mitigation, and model provenance tracking.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Guidelines",
        "description": "NIST CSF 2.0 expands coverage across six core functions (Govern, Identify, Protect, Detect, Respond, Recover), mandating enterprise supply chain risk management and continuous control auditing.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls and Benchmarks Security Configuration Update",
        "description": "Center for Internet Security updates benchmark recommendations for operating systems, cloud environments, and container runtimes to enforce strict hardening and baseline configuration checks.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    # Unverified announcement to test blocking
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Tech Blog Speculation on ISO 27001 Revision",
        "description": "A personal tech blog claims ISO 27001 is banning all cloud databases starting next week. This is an unverified industry blog rumor.",
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

    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "apple.com", "developer.apple.com", "android.com", "developer.android.com"
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "open web application security project",
        "center for internet security",
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "cisa", "ico", "government publication"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "ai generated summaries", "chatgpt summary"]

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
                    common_terms = {"iso", "nist", "owasp", "cis", "security", "framework"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


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
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    doc_checklist = []
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
            migration_steps.append(f"- **{cat}**: Update Annex A controls mapping and realign information security policy documentation with ISO/IEC 27001:2022.")
            impl_checklist.append("- [ ] Audit threat intelligence and secure coding controls for ISO 27001 compliance.")
            testing_checklist.append("- [ ] Verify automated security scanning gates validate ISO 27001 control compliance.")
            doc_checklist.append("- [ ] Update ISMS policy documentation to reflect ISO 27001 controls.")
            risk_assessment.append(f"- *{cat}*: Non-conformity during external ISMS audit leading to loss of certification.")
        elif cat == "ISO 27701":
            migration_steps.append(f"- **{cat}**: Integrate Privacy Information Management System (PIMS) controls into existing data processor and controller workflows.")
            impl_checklist.append("- [ ] Review PIMS data handling policies and map data subject request handlers.")
            testing_checklist.append("- [ ] Execute privacy impact assessment verification tests for data subjects.")
            doc_checklist.append("- [ ] Publish updated PIMS procedures in repository compliance docs.")
            risk_assessment.append(f"- *{cat}*: Privacy regulatory penalties and failure to satisfy partner PIMS requirements.")
        elif cat == "ISO 42001":
            migration_steps.append(f"- **{cat}**: Implement AI Management System (AIMS) governance controls for artificial intelligence models and automated workflows.")
            impl_checklist.append("- [ ] Conduct AI risk assessment and establish model lineage monitoring under ISO 42001.")
            testing_checklist.append("- [ ] Run model validation tests to verify AI risk controls and bias boundaries.")
            doc_checklist.append("- [ ] Document AIMS risk assessment methodologies and AI governance framework.")
            risk_assessment.append(f"- *{cat}*: Ungoverned AI deployment resulting in algorithmic liability or regulatory breach.")
        elif cat == "ISO 31000":
            migration_steps.append(f"- **{cat}**: Align technical risk matrices and vulnerability prioritization with ISO 31000 risk management guidelines.")
            impl_checklist.append("- [ ] Update enterprise risk evaluation matrices and register technical risk vectors.")
            testing_checklist.append("- [ ] Perform simulated risk assessment scenarios on critical system components.")
            doc_checklist.append("- [ ] Update technical risk register and risk mitigation guidelines.")
            risk_assessment.append(f"- *{cat}*: Unmitigated operational risks causing unexpected downtime or breach.")
        elif cat == "ISO 9001":
            migration_steps.append(f"- **{cat}**: Implement formal Quality Management System (QMS) release controls and automated verification pipelines.")
            impl_checklist.append("- [ ] Establish formal QMS change approval procedures for codebase modifications.")
            testing_checklist.append("- [ ] Run automated regression and release gate test suites.")
            doc_checklist.append("- [ ] Document QMS quality assurance guidelines and release procedures.")
            risk_assessment.append(f"- *{cat}*: Quality regressions causing customer dissatisfaction and audit non-compliance.")
        elif cat == "IEC standards":
            migration_steps.append(f"- **{cat}**: Enforce IEC 62304 / IEC 82304 software lifecycle verification and hazard analysis protocols.")
            impl_checklist.append("- [ ] Update software lifecycle hazard controls and architectural risk classifications.")
            testing_checklist.append("- [ ] Execute unit, integration, and safety hazard validation tests.")
            doc_checklist.append("- [ ] Update IEC software lifecycle traceability matrix and safety documentation.")
            risk_assessment.append(f"- *{cat}*: Failure to meet medical device or functional safety software standards.")
        elif cat == "OWASP":
            migration_steps.append(f"- **{cat}**: Implement OWASP MASVS/ASVS controls for client-side encryption, API auth, and input sanitization.")
            impl_checklist.append("- [ ] Remediate code against OWASP Top 10 and MASVS L1/L2 security requirements.")
            testing_checklist.append("- [ ] Run SAST/DAST scanners and OWASP MASVS compliance verification scripts.")
            doc_checklist.append("- [ ] Update security architecture documentation with OWASP MASVS mappings.")
            risk_assessment.append(f"- *{cat}*: Exploitation of common web/mobile vulnerabilities by malicious actors.")
        elif cat == "NIST AI RMF":
            migration_steps.append(f"- **{cat}**: Execute NIST AI RMF core functions (Govern, Map, Measure, Manage) across AI/ML integration pipelines.")
            impl_checklist.append("- [ ] Map AI model inputs/outputs and measure bias and safety thresholds.")
            testing_checklist.append("- [ ] Perform adversarial testing and output safety evaluations on AI models.")
            doc_checklist.append("- [ ] Update `docs/AI-POLICY-MIGRATION.md` with NIST AI RMF governance logs.")
            risk_assessment.append(f"- *{cat}*: AI safety failure, hallucination risks, or non-compliance with federal AI directives.")
        elif cat == "NIST CSF":
            migration_steps.append(f"- **{cat}**: Realign cybersecurity controls across NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover).")
            impl_checklist.append("- [ ] Verify supply chain risk management controls and continuous threat detection.")
            testing_checklist.append("- [ ] Test incident response procedures and detection rule alerts.")
            doc_checklist.append("- [ ] Update cybersecurity framework documentation and control mappings.")
            risk_assessment.append(f"- *{cat}*: Security control gaps leaving infrastructure vulnerable to cyber attacks.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(f"- **{cat}**: Enforce CIS Benchmarks configuration baselines across container, server, and application setups.")
            impl_checklist.append("- [ ] Harden OS, dockerfiles, and cloud configurations against CIS Benchmarks.")
            testing_checklist.append("- [ ] Run automated CIS compliance benchmark auditing tools.")
            doc_checklist.append("- [ ] Document CIS benchmark compliance baselines and hardening steps.")
            risk_assessment.append(f"- *{cat}*: System misconfigurations leading to unauthorized access or privilege escalation.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Execute standard test suites to verify technical compliance."
    doc_checklist_str = "\n".join(doc_checklist) if doc_checklist else "- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with updated controls."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces critical configuration, structural, and documentation modifications to bring the repository into complete compliance with updated technical standards. It addresses ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards evolve to address emerging security vulnerabilities, AI governance requirements, and enterprise compliance requirements. Ensuring continuous alignment with ISO, IEC, NIST, OWASP, and CIS frameworks prevents compliance drift and maintains audit readiness.

## 3. Regulatory change
- **ISO Standards**: Updated ISMS, PIMS, AIMS, Risk Management, and QMS control expectations.
- **IEC & OWASP**: Enhanced software lifecycle safety, MASVS mobile security, and ASVS web controls.
- **NIST & CIS**: Expansion of NIST CSF 2.0 functions, NIST AI RMF risk management, and CIS Benchmarks system hardening.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and regulatory risk if technical standards are not continuously maintained and verified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All modifications preserve full backward compatibility with existing platform features while strengthening control baselines and audit evidence collection.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated compliance guard scripts.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Verify that all automated test scripts pass without regression.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Confirm technical standards mapping documentation is up to date in `docs/STANDARDS-POLICY-MIGRATION.md`.

## 12. Compliance impact
- **Audit Readiness**: Ensures total alignment with international ISO, IEC, NIST, OWASP, and CIS certification requirements.
- **Security Posture**: Eliminates technical compliance gaps and reduces attack surface.
- **Governance**: Guarantees structured AI governance and enterprise risk management.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced security controls and validation gates apply to system operations.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official citations are verified Priority 1-3 sources.
- [ ] Verify that test cases cover all updated standards.

## 15. Approver recommendations
Verify that updated controls match current enterprise certification scopes and confirm all automated compliance checks pass in CI.
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
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across technical standards.",
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
        lines.append("- **Regulatory Impact**: High priority technical standard compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Implementation Task 1**: Audit Annex A controls mapping against ISO/IEC 27001:2022.")
            lines.append("- [ ] **Documentation Update**: Update ISMS policy documentation and control procedures.")
            lines.append("- [ ] **Testing Update**: Add automated checks to verify ISMS control implementation.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Implementation Task 1**: Review PIMS data processor/controller controls.")
            lines.append("- [ ] **Documentation Update**: Document privacy information management procedures.")
            lines.append("- [ ] **Testing Update**: Implement PIMS compliance test cases.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Implementation Task 1**: Establish AI Management System (AIMS) governance framework.")
            lines.append("- [ ] **Documentation Update**: Document AI model risk assessment and lineage procedures.")
            lines.append("- [ ] **Testing Update**: Add AI model bias and boundary validation tests.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Implementation Task 1**: Align enterprise risk matrix with ISO 31000 guidelines.")
            lines.append("- [ ] **Documentation Update**: Update technical risk register and mitigation protocols.")
            lines.append("- [ ] **Testing Update**: Verify technical risk simulation scenarios.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Implementation Task 1**: Integrate QMS release controls into software development workflows.")
            lines.append("- [ ] **Documentation Update**: Document QMS change management and quality assurance rules.")
            lines.append("- [ ] **Testing Update**: Execute QMS automated regression suites prior to release.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Implementation Task 1**: Audit software lifecycle hazard controls under IEC 62304 / IEC 82304.")
            lines.append("- [ ] **Documentation Update**: Update software safety and traceability documentation.")
            lines.append("- [ ] **Testing Update**: Run IEC functional safety verification test cases.")
        elif cat == "OWASP":
            lines.append("- [ ] **Implementation Task 1**: Remediate code against OWASP MASVS/ASVS requirements.")
            lines.append("- [ ] **Documentation Update**: Document OWASP control mappings and security architecture.")
            lines.append("- [ ] **Testing Update**: Run SAST/DAST security test suites for OWASP controls.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Implementation Task 1**: Implement NIST AI RMF core functions (Govern, Map, Measure, Manage).")
            lines.append("- [ ] **Documentation Update**: Document AI risk management framework compliance in `docs/AI-POLICY-MIGRATION.md`.")
            lines.append("- [ ] **Testing Update**: Implement AI model safety and adversarial robustness tests.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Implementation Task 1**: Realign cybersecurity controls with NIST CSF 2.0 functions.")
            lines.append("- [ ] **Documentation Update**: Update CSF control mappings and incident response plans.")
            lines.append("- [ ] **Testing Update**: Run incident detection rule and control validation tests.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Implementation Task 1**: Harden system baselines in accordance with CIS Benchmarks.")
            lines.append("- [ ] **Documentation Update**: Document CIS benchmark configuration baselines.")
            lines.append("- [ ] **Testing Update**: Execute automated CIS benchmark audit checks.")
        else:
            lines.append(f"- [ ] **Implementation Task**: Verify that all criteria for {cat} are checked.")
            lines.append(f"- [ ] **Documentation Update**: Document compliance requirements for {cat}.")
            lines.append(f"- [ ] **Testing Update**: Add verification test suite for {cat}.")
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
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

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
