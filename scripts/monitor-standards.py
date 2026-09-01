#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards:
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
        "iso 27001", "iso/iec 27001", "isms", "information security management system", "annex a controls"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "pims", "privacy information management", "pii controller", "pii processor"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "aims", "ai management system", "artificial intelligence management system"
    ],
    "ISO 31000": [
        "iso 31000", "risk management guidelines", "risk assessment framework", "risk criteria"
    ],
    "ISO 9001": [
        "iso 9001", "quality management system", "qms", "quality policy", "process control"
    ],
    "IEC standards": [
        "iec standards", "iec 62304", "iec 82304", "iec 62443", "functional safety", "electrotechnical"
    ],
    "OWASP": [
        "owasp", "masvs", "asvs", "owasp top 10", "mobile top 10", "api security top 10"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "nist ai", "govern map measure manage"
    ],
    "NIST CSF": [
        "nist csf", "nist cybersecurity framework", "csf 2.0", "identify protect detect respond recover"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis benchmark", "center for internet security", "hardening guidelines", "cis controls"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001", r"ISMS", r"securityPolicy", r"accessControl", r"encryptionPolicy"
    ],
    "ISO 27701": [
        r"ISO27701", r"PIMS", r"piiProcessing", r"dataProtectionPolicy", r"privacyManagement"
    ],
    "ISO 42001": [
        r"ISO42001", r"AIMS", r"aiGovernance", r"aiRiskAssessment", r"modelAudit"
    ],
    "ISO 31000": [
        r"ISO31000", r"riskAssessment", r"riskRegistry", r"riskMitigation"
    ],
    "ISO 9001": [
        r"ISO9001", r"QMS", r"qualityPolicy", r"qualityAssurance", r"processControl"
    ],
    "IEC standards": [
        r"IEC62304", r"IEC82304", r"IEC62443", r"IECStandard", r"functionalSafety"
    ],
    "OWASP": [
        r"OWASP", r"MASVS", r"ASVS", r"securityControl", r"sanitizeInput"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF", r"AIRiskManagement", r"aiTrustworthiness", r"modelGovernance"
    ],
    "NIST CSF": [
        r"NIST_CSF", r"CybersecurityFramework", r"incidentResponse", r"eventLogging"
    ],
    "CIS Benchmarks": [
        r"CISBenchmark", r"CISControl", r"systemHardening", r"secureConfig"
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

# 10 Comprehensive Mock Announcements for all 10 categories plus 1 unverified
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "ISO releases updated ISMS control requirements targeting cloud access control, key management, and mandatory threat intelligence integration in Annex A.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Enhancement",
        "description": "ISO/IEC 27701 updates PIMS guidelines for PII controllers and processors, reinforcing mandatory data minimization and privacy impact assessment logging.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Requirements Release",
        "description": "ISO/IEC 42001 establishes AIMS requirements for responsible AI development, algorithmic transparency, automated decision lineage tracking, and AI risk controls.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Alignment",
        "description": "ISO 31000 framework update provides structured methodologies for risk identification, evaluation, and continuous monitoring across software engineering lifecycles.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System (QMS) Software Process Control Update",
        "description": "ISO 9001 updates software quality assurance standards, mandating documented testing coverage, continuous integration quality gates, and process verification.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62304 and IEC 62443 Functional Safety and Cybersecurity Revision",
        "description": "IEC standards committee updates software lifecycle requirements (IEC 62304) and industrial cybersecurity (IEC 62443) controls for secure software development.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS and ASVS Security Controls Revision",
        "description": "OWASP updates Mobile Application Security Verification Standard (MASVS) and Application Security Verification Standard (ASVS), reinforcing input sanitization and token security.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Governance Revision",
        "description": "NIST releases updated AI RMF guidelines across Govern, Map, Measure, and Manage functions to establish trustworthy, bias-mitigated, and safe AI systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Update",
        "description": "NIST CSF 2.0 expands cybersecurity controls with the new Govern function alongside Identify, Protect, Detect, Respond, and Recover pillars for enterprise applications.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Hardening and Configuration Controls Update",
        "description": "Center for Internet Security issues updated CIS Benchmarks for containerized environments, cloud infrastructure, and mobile OS hardening guidelines.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "OWASP",
        "title": "Unverified Blog Claim on OWASP Standard Changes",
        "description": "A random industry tech blog claims OWASP will deprecate all SQL databases in favor of unencrypted text files next week. Unverified secondary blog source.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT"
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
        "apple.com", "developer.apple.com", "android.com", "developer.android.com", "support.google.com"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p3_domains = ["arxiv.org", "ssrn.com"]
    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]

    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    # Classify priority by link domain first
    priority = 4  # Default to 4 (Industry material)

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(kw in combined for kw in p4_keywords):
        priority = 4
    elif any(d in link for d in p3_domains) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains):
        priority = 2

    if any(d in link for d in p1_domains) or ".gov" in link:
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4 or 5: Must be verified by an explicit Priority 1 official source
        has_p1_ref_in_text = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref_in_text = True
                break
        if not has_p1_ref_in_text and ".gov" in combined:
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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcements):
    """
    Evaluates source trust hierarchy for announcements, logs verification alerts to stderr,
    and returns verified updates while filtering out unverified Priority 4/5 updates.
    """
    verified = []
    blocked_count = 0
    for ann in announcements:
        priority, is_verified = classify_source_and_verify(ann, announcements)
        if priority in (4, 5) and not is_verified:
            blocked_count += 1
            print(
                f"Source Trust Alert: Blocking unverified Priority {priority} source: {ann.get('title')} ({ann.get('link')})",
                file=sys.stderr
            )
        else:
            verified.append(ann)
    return verified, blocked_count


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
    Classifies incoming announcements into the 10 technical standards categories using word boundaries.
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
                # Use word boundaries for keyword matching to avoid matching substrings like "claims" for "aims"
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
                f"- **{cat}**: Align Information Security Management System (ISMS) policies with Annex A control updates, enforcing strict access controls and encrypted data at rest."
            )
            impl_checklist.append("- [ ] Audit ISMS access controls and encryption policies against updated ISO 27001 Annex A standards.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with ISMS audit requirements leading to certification revocation and unmitigated security risks.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS to Privacy Information Management System (PIMS) controls, documenting PII processing roles and data protection impact assessments."
            )
            impl_checklist.append("- [ ] Update PIMS documentation and verify PII processing controls.")
            risk_assessment.append(f"- *{cat}*: Regulatory fines and privacy audit failures due to inadequate PII processor controls.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance, documenting algorithmic decision lineage and model risk assessments."
            )
            impl_checklist.append("- [ ] Implement AIMS model risk assessment procedures and logging for AI features.")
            risk_assessment.append(f"- *{cat}*: Algorithmic bias and regulatory non-compliance under EU AI Act and ISO 42001 AIMS frameworks.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Update enterprise risk management framework to systematically identify, evaluate, and mitigate software security risks."
            )
            impl_checklist.append("- [ ] Refresh risk registry and risk treatment plans in accordance with ISO 31000.")
            risk_assessment.append(f"- *{cat}*: Unidentified operational and security risks resulting in system vulnerabilities.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Formalize software Quality Management System (QMS) controls, ensuring automated CI/CD quality gates and process verification."
            )
            impl_checklist.append("- [ ] Verify continuous integration quality gates and automated test coverage thresholds.")
            risk_assessment.append(f"- *{cat}*: Quality degradation and QMS audit findings.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Update software lifecycle practices under IEC 62304 and cybersecurity controls under IEC 62443."
            )
            impl_checklist.append("- [ ] Audit software lifecycle documentation against IEC 62304 / IEC 62443 requirements.")
            risk_assessment.append(f"- *{cat}*: Safety and functional security compliance gaps in regulated software systems.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Remediate top application security vulnerabilities matching OWASP MASVS and ASVS control requirements."
            )
            impl_checklist.append("- [ ] Enforce OWASP MASVS input validation and token handling controls.")
            risk_assessment.append(f"- *{cat}*: Exploitable security vulnerabilities such as injection, broken access control, and insecure storage.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI Risk Management Framework across Govern, Map, Measure, and Manage functions for integrated AI components."
            )
            impl_checklist.append("- [ ] Complete NIST AI RMF trustworthiness and bias evaluation checklists for active models.")
            risk_assessment.append(f"- *{cat}*: AI safety hazards, model hallucinations, and failure to meet NIST trustworthiness guidelines.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 pillars (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append("- [ ] Review event logging, threat detection, and incident response procedures against NIST CSF 2.0.")
            risk_assessment.append(f"- *{cat}*: Security control gaps leading to undetected breaches or delayed incident response.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Implement CIS Benchmark hardening guidelines across containers, cloud infrastructure, and mobile client targets."
            )
            impl_checklist.append("- [ ] Validate container and build environment configurations against CIS hardening standards.")
            risk_assessment.append(f"- *{cat}*: Insecure default configurations exposing infrastructure and client runtimes to exploitation.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of standard controls."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the repository and system configuration with updated international technical standards and frameworks, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Adherence to global technical standards ensures operational resilience, information security, privacy governance, artificial intelligence safety, and software quality. Continuous monitoring of standards body revisions ensures the repository remains audit-ready and resilient against emerging security threats.

## 3. Regulatory change
- **ISO/IEC Standards**: Alignment with updated ISMS (27001), PIMS (27701), AIMS (42001), Risk Management (31000), QMS (9001), and IEC software lifecycle controls.
- **Security & AI Frameworks**: Compliance with OWASP MASVS/ASVS, NIST AI RMF 1.0, NIST CSF 2.0, and CIS Benchmarks hardening rules.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Moderate-to-high risk of compliance audit failure, security vulnerability exposure, or AI governance non-compliance if technical standards revisions are unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes preserve backward compatibility. Control frameworks and quality gates are integrated into build and workflow scripts without breaking existing application APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Execute repository compliance verification scripts.

## 10. Testing checklist
- [ ] Run static code analysis and verify OWASP security controls pass.
- [ ] Validate automated quality gates and unit/integration test coverage.
- [ ] Conduct AI model risk assessment and verify logging of AI decision outputs.
- [ ] Verify event logging and incident response triggers against NIST CSF recommendations.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document ISMS, PIMS, and AIMS governance updates in developer reference guides.
- [ ] Update security architecture diagrams reflecting NIST CSF and OWASP controls.

## 12. Compliance impact
- **Audit Readiness**: Ensures full alignment with external ISO, IEC, NIST, OWASP, and CIS audit expectations.
- **Risk Mitigation**: Reduces attack surface and establishes clear AI safety and privacy boundaries.
- **Quality Assurance**: Enforces strict software lifecycle quality controls.

## 13. Breaking changes
- Non-compliant configurations or missing security headers will fail build integration gates.

## 14. Review checklist
- [ ] Output is 100% emoji-free.
- [ ] Official citations are sourced from Priority 1-3 verified entities.
- [ ] Codebase signals and affected files are correctly mapped.

## 15. Approver recommendations
Verify that all CI/CD pipeline quality gates pass, confirm that AI governance documentation is attached for any active LLM integrations, and ensure that security controls match OWASP MASVS and CIS Benchmark requirements before merging.
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
        lines.append("- **Regulatory Impact**: High priority technical standards compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Audit ISMS access controls and encryption implementations.")
            lines.append("- [ ] **Documentation Task 2**: Update ISMS security policy in docs.")
            lines.append("- [ ] **Testing Task 3**: Verify encryption and access control unit tests pass.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Audit PII processing controls and consent mechanisms.")
            lines.append("- [ ] **Documentation Task 2**: Document PIMS roles and data flow mappings.")
            lines.append("- [ ] **Testing Task 3**: Run privacy data protection impact test suite.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Implement AI decision logging and model governance hooks.")
            lines.append("- [ ] **Documentation Task 2**: Publish AIMS risk assessment and model lineage report.")
            lines.append("- [ ] **Testing Task 3**: Execute AI safety and transparency verification tests.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Audit software risk treatment controls.")
            lines.append("- [ ] **Documentation Task 2**: Maintain updated enterprise risk registry.")
            lines.append("- [ ] **Testing Task 3**: Test fallback and error-handling pathways under risk scenarios.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Enforce automated build quality gates in CI/CD pipeline.")
            lines.append("- [ ] **Documentation Task 2**: Document software QMS process controls and verification steps.")
            lines.append("- [ ] **Testing Task 3**: Ensure test suite coverage meets QMS thresholds.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Audit software lifecycle and functional safety controls.")
            lines.append("- [ ] **Documentation Task 2**: Document IEC 62304 / IEC 62443 compliance mappings.")
            lines.append("- [ ] **Testing Task 3**: Run functional safety regression test suite.")
        elif cat == "OWASP":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Remediate OWASP MASVS/ASVS security findings in codebase.")
            lines.append("- [ ] **Documentation Task 2**: Update OWASP threat matrix and remediation guide.")
            lines.append("- [ ] **Testing Task 3**: Execute OWASP security vulnerability scanner test suite.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Integrate NIST AI RMF Govern/Map/Measure/Manage controls.")
            lines.append("- [ ] **Documentation Task 2**: Document AI trustworthiness and bias mitigation strategies.")
            lines.append("- [ ] **Testing Task 3**: Run AI bias and model accuracy validation tests.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Implement event logging and threat detection mechanisms.")
            lines.append("- [ ] **Documentation Task 2**: Update incident response playbook under NIST CSF 2.0.")
            lines.append("- [ ] **Testing Task 3**: Simulate security incident detection and logging response tests.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Repository Gap / Code Task 1**: Harden container and environment configuration parameters.")
            lines.append("- [ ] **Documentation Task 2**: Publish CIS Benchmark hardening checklist.")
            lines.append("- [ ] **Testing Task 3**: Run CIS Benchmark compliance automated audit script.")
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

    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/cybersecurity/rss.xml"))
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

    verified_updates, blocked_count = enforce_strict_source_trust_hierarchy(classified_updates)

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_count} blocked due to source trust validation):")
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u)
            status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
            print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

        print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")

    scan_results = scan_codebase_for_standards_signals(args.dir)

    if not args.json:
        total_matches = sum(len(matches) for matches in scan_results.values())
        print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
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
