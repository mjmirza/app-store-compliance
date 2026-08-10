#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards and maps codebase gaps and migration tasks.
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
    "ISO 27001": ["iso 27001", "iso/iec 27001", "information security management", "isms", "annex a"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "privacy information management", "pims", "privacy information"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "artificial intelligence management", "aims", "ai management system"],
    "ISO 31000": ["iso 31000", "risk management guidelines", "risk assessment framework", "risk treatment"],
    "ISO 9001": ["iso 9001", "quality management system", "qms", "quality principles"],
    "IEC standards": ["iec standards", "iec 62304", "iec 82304", "software life cycle", "electro-technical"],
    "OWASP": ["owasp", "masvs", "asvs", "top 10", "owasp top ten"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "nist ai", "trustworthy ai"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "nist cybersecurity", "csf 2.0"],
    "CIS Benchmarks": ["cis benchmarks", "cis compliance", "cis standard", "hardening guidelines"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO 27001",
        r"ISMS",
        r"Annex A",
        r"Information Security Management System"
    ],
    "ISO 27701": [
        r"ISO 27701",
        r"PIMS",
        r"Privacy Information Management System",
        r"privacyStatement",
        r"privacyConsent"
    ],
    "ISO 42001": [
        r"ISO 42001",
        r"AIMS",
        r"AI Management System",
        r"ai-ethics",
        r"ai-model-card"
    ],
    "ISO 31000": [
        r"ISO 31000",
        r"Risk Management",
        r"risk_assessment",
        r"risk_mitigation"
    ],
    "ISO 9001": [
        r"ISO 9001",
        r"Quality Management",
        r"qms_policy",
        r"quality_audit"
    ],
    "IEC standards": [
        r"IEC 62304",
        r"IEC 82304",
        r"IEC-standards",
        r"medical-software"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"OWASP Top 10",
        r"TopTen"
    ],
    "NIST AI RMF": [
        r"NIST AI RMF",
        r"NIST-AI",
        r"AI Risk Management",
        r"trustworthy-ai"
    ],
    "NIST CSF": [
        r"NIST CSF",
        r"Cybersecurity Framework",
        r"NIST-CSF",
        r"csf-controls"
    ],
    "CIS Benchmarks": [
        r"CIS Benchmark",
        r"CIS-Hardening",
        r"cis-controls"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CISA, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STAND-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO 27001 ISMS Standard Update on Information Security Controls",
        "description": "The revised ISO/IEC 27001:2022 standard introduces updated Annex A information security management controls, requiring organisations to restructure their ISMS.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 specifies requirements and guidelines for establishing and continuously improving a Privacy Information Management System (PIMS).",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System (AIMS) Certification",
        "description": "ISO/IEC 42001 specifies requirements for establishing, implementing, and continually improving an artificial intelligence management system.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines for Corporate Risk Assessments",
        "description": "ISO 31000 provides principles, a framework, and a process for managing risk to assist organizations in making decisions and treating vulnerabilities.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Principles and Standards",
        "description": "The ISO 9001 standard outlines requirements for quality management systems (QMS), emphasizing customer satisfaction and continuous improvement.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Managing Software Lifecycle in Medical Devices",
        "description": "The International Electrotechnical Commission publishes updated guidelines under IEC 62304 and IEC 82304 for software lifecycle and safety requirements.",
        "link": "https://www.iec.ch",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile App Security Verification Standard (MASVS) Framework",
        "description": "OWASP introduces updated verification standards under the MASVS and ASVS frameworks to mitigate top security vulnerabilities.",
        "link": "https://owasp.org",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-NIST-AI",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (NIST AI RMF 1.0) Guidance",
        "description": "The National Institute of Standards and Technology releases updated guidelines under the NIST AI Risk Management Framework to cultivate trustworthy AI systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (NIST CSF 2.0) Implementation Guidelines",
        "description": "NIST finalizes the Cybersecurity Framework 2.0, extending cybersecurity controls, functions (Identify, Protect, Detect, Respond, Recover, Govern), and profiles.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 UTC"
    },
    {
        "id": "STAND-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Hardening Controls for Secure Infrastructure",
        "description": "The Center for Internet Security (CIS) issues new benchmarks and controls for secure systems configuration, hardening, and database protection.",
        "link": "https://www.cisecurity.org",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 UTC"
    },
    # Unverified announcements to test blocking
    {
        "id": "STAND-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Industry Blog Rumors on ISO 27001 Fines",
        "description": "A random tech blog claims ISO 27001 rules are being changed next week to fine all websites without an immediate dark mode. This is an unverified blog post.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 PDT"
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
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "imda.gov.sg", "pdpc.gov.sg", "anpd.gov.br", "esafety.gov.au",
        "apple.com", "developer.apple.com", "android.com", "developer.android.com", "support.google.com"
    ]
    p1_keywords = [
        "international organization for standardization", "iec", "nist", "owasp",
        "center for internet security", "european commission", "eur-lex", "official journal",
        "enisa", "edpb", "ftc", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register"
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
                    common_terms = {"standards", "iso", "iec", "nist", "owasp", "cis"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcement, priority, is_verified):
    """Logs verification alerts to stderr following strict Source Trust Hierarchy rules."""
    if priority >= 4 and not is_verified:
        sys.stderr.write(
            f"ALERT: Unverified secondary source detected (Priority {priority}): {announcement.get('title')}. "
            "PR generation and implementation task inclusion will be blocked.\n"
        )
    else:
        sys.stderr.write(
            f"INFO: Source trust verified (Priority {priority}): {announcement.get('title')}.\n"
        )


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
        sys.stderr.write(f"Warning: Failed to fetch live feed {url}: {e}\n")
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
                        "id": ann.get("id", "STAND-UPDATE-" + str(hash(title))[:6]),
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

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Update security controls registry to reflect ISO 27001 Annex A changes, establishing compliant ISMS configurations."
            )
            impl_checklist.append("- [ ] Align the repository ISMS controls mapping file with ISO 27001 Annex A updates.")
            testing_checklist.append("- [ ] Run the automated security policy scan to ensure continuous Annex A compliance.")
            risk_assessment.append(f"- *{cat}*: Non-conformance in operational ISMS audits leading to certification suspension.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Establish PIMS controls, integrating specialized privacy consents and data minimization policies."
            )
            impl_checklist.append("- [ ] Implement PIMS documentation and map privacy workflows to ISO 27701 guidelines.")
            testing_checklist.append("- [ ] Perform verification tests on privacy consent data pipelines.")
            risk_assessment.append(f"- *{cat}*: Inadequate privacy protections triggering regulatory fines and data management failures.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Integrate AI management system procedures, documenting algorithmic transparency and model risk cards."
            )
            impl_checklist.append("- [ ] Deploy standard AI model cards and implement algorithmic safeguards matching ISO 42001.")
            testing_checklist.append("- [ ] Audit AI content moderation filters and verify compliance metrics.")
            risk_assessment.append(f"- *{cat}*: Uncontrolled AI models violating national policy guidelines and transparent auditing limits.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Conduct system risk assessments, mapping threats and defining clear, documented risk treatment plans."
            )
            impl_checklist.append("- [ ] Establish a formal risk evaluation matrix aligned with ISO 31000 principles.")
            testing_checklist.append("- [ ] Run a simulation of key risk mitigations and log responses.")
            risk_assessment.append(f"- *{cat}*: Failure to register critical infrastructure operational risks in the system directory.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize the software delivery life cycle, formulating quality metrics and continuous improvement criteria."
            )
            impl_checklist.append("- [ ] Configure continuous integration build triggers to trace and log delivery quality standards.")
            testing_checklist.append("- [ ] Review automated build success ratios and verify regression logs.")
            risk_assessment.append(f"- *{cat}*: Degradation in software product quality and lack of structured release verification pipelines.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Formalize medical-grade or lifecycle standards software verification procedures under IEC 62304 and 82304."
            )
            impl_checklist.append("- [ ] Update software architecture documentation to list lifecycle safety classes.")
            testing_checklist.append("- [ ] Run unit and regression coverage tests to prove comprehensive safety compliance.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with safety-critical software engineering frameworks in medical or industrial environments.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Conduct structural validation against OWASP Top 10 web vulnerabilities and MASVS requirements."
            )
            impl_checklist.append("- [ ] Scan repository for secrets leakage and harden endpoints against injection vulnerabilities.")
            testing_checklist.append("- [ ] Execute static application security testing (SAST) to detect OWASP vulnerabilities.")
            risk_assessment.append(f"- *{cat}*: Increased susceptibility to common application-level security threats and system breaches.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Incorporate AI trust profiles, checking fairness, safety, and security metrics for intelligent agents."
            )
            impl_checklist.append("- [ ] Configure AI safety metrics and document model output validations.")
            testing_checklist.append("- [ ] Test generative output boundaries for bias or unsafe content generation.")
            risk_assessment.append(f"- *{cat}*: Deployment of untrusted model workflows that fail to fulfill ethical or governance expectations.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map security practices across Identify, Protect, Detect, Respond, Recover, and Govern profiles."
            )
            impl_checklist.append("- [ ] Update cybersecurity profiles file to document response strategies.")
            testing_checklist.append("- [ ] Validate threat detection and log alert handling performance.")
            risk_assessment.append(f"- *{cat}*: Insufficient cybersecurity defenses leaving infrastructure unmonitored during incident cycles.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce system configuration hardening guidelines and secure default infrastructure variables."
            )
            impl_checklist.append("- [ ] Configure secure host environment and database access variables.")
            testing_checklist.append("- [ ] Validate container configurations and database encryption benchmarks.")
            risk_assessment.append(f"- *{cat}*: Default server settings allowing brute force attacks or plain configuration exposures.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Run system verification tests."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and documentation modifications to bring the repository into alignment with international technical standards and frameworks. It addresses security, privacy, and quality standards to ensure continuous compliance.

## 2. Background
Adherence to standardized frameworks represents an essential requirement for enterprise deployments, risk management, and software security. Operating without structured compliance mappings exposes the organization to technical debt and security vulnerabilities. This PR proactively resolves identified implementation gaps.

## 3. Regulatory change
- **Information Security Standards**: Alignment with modern ISO 27001, NIST CSF, and CIS Benchmarks hardening guidelines.
- **Privacy Standards**: Incorporation of ISO 27701 privacy requirements.
- **AI and Quality Standards**: Conformance with ISO 42001, NIST AI RMF, and ISO 9001 quality management guidelines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Significant regulatory and audit exposure if standard-specific checklists and practices are omitted.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards updates involve additions of checks, metadata profiles, and security constraints, without altering existing client-facing APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide compliance audit to verify standards compliance.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run newly created technical standards test suites.

## 11. Documentation checklist
- [ ] Update standard policy migration documents to reflect completed mappings.
- [ ] Verify security guidelines are fully updated in the repository docs.

## 12. Compliance impact
- **Audit Preparedness**: Demonstrates strict tracking and verification of international standards, simplifying compliance certification.
- **Vulnerability Minimization**: Reduces surface area risks by implementing OWASP controls and CIS hardening.
- **Security Posture**: Establishes continuous tracking of critical technical standards updates.

## 13. Breaking changes
- No functional breaking changes are introduced. Enhanced configuration boundaries may require local environment variables updates.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that security profiles match requirements.

## 15. Approver recommendations
Ensure that the security policy migration report matches the changes in this PR, and confirm that all automated checks pass successfully on local workspaces.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
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

    lines.append("## Identified Repository Gaps")
    lines.append("")

    gaps_found = False
    for cat in CATEGORIES:
        files = scan_results.get(cat, [])
        if files:
            gaps_found = True
            lines.append(f"### Gap identified for {cat}")
            lines.append(f"Files containing compliance signals for {cat}:")
            for f in files:
                lines.append(f"- `{f['file']}` (Line {f['line_num']}: `{f['content']}`)")
            lines.append("")

    if not gaps_found:
        lines.append("No active codebase files containing signals were detected. This indicates a potential gap where no implementation of the standard has been declared.")
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
            lines.append("- [ ] **Task 1**: Review Annex A physical and technological controls mapping.")
            lines.append("- [ ] **Task 2**: Establish access validation and authorization registers.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Draft a privacy information management workflow.")
            lines.append("- [ ] **Task 2**: Deploy privacy consent handlers inside user interface views.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Create AI model cards detailing data usage and boundaries.")
            lines.append("- [ ] **Task 2**: Formulate algorithmic risk mitigation guidelines.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Formulate risk evaluation and mitigation checklists.")
            lines.append("- [ ] **Task 2**: Log threat scenarios and mitigation results.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Set up release quality gates and verify compile logs.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Map safety lifecycle classes and check architecture files.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Conduct static code analysis against injection and data leaks.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Complete safety validations on intelligent agent configurations.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align network monitoring profiles with threat profiles.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Configure secure environments and secure container options.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all standard criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("## Testing Updates & Verifications")
    lines.append("")
    for cat in CATEGORIES:
        lines.append(f"### Testing Requirements for {cat}")
        lines.append(f"- [ ] Test coverage verification for {cat} integration.")
        lines.append(f"- [ ] Validate system boundaries and test inputs for {cat} controls.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        sys.stderr.write(f"Standards documentation report updated successfully at: {output_filepath}\n")
    except Exception as e:
        sys.stderr.write(f"Error writing documentation to {output_filepath}: {e}\n")


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
        sys.stderr.write("Fetching live standards RSS feeds...\n")
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/cybersecurity/rss"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

    # Fallback to mock data if live has no updates, or mock is explicitly requested (default)
    if args.mock or (not args.live and not args.mock) or not announcements:
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                sys.stderr.write(f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.\n")
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # 2. Classify updates into the 10 required categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    # Sort classified updates to keep them structured
    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    # Filter out announcements with unverified sources for PR generation
    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u)
        enforce_strict_source_trust_hierarchy(u, priority, is_verified)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    if not args.json:
        sys.stderr.write(f"Monitored and classified {len(classified_updates)} policy/requirement updates ({blocked_updates_count} blocked due to source trust validation):\n")
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u)
            status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
            sys.stderr.write(f" {idx}. [{u['category']}] {u['title']} - {status_str}\n")

    # 3. Scan the codebase for signals related to these categories
    if not args.json:
        sys.stderr.write(f"Scanning codebase under '{args.dir}' for standards integration signals...\n")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        sys.stderr.write(f"Found {total_matches} signal matches in code.\n")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, scan_results, args.output_docs)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    # Save drafted PR
    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
            sys.stderr.write(f"PR draft written successfully to: {args.pr_output}\n")
    except Exception as e:
        sys.stderr.write(f"Failed to write PR draft to {args.pr_output}: {e}\n")

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
