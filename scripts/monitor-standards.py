#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks changes across 10 key technical standards:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks.
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
        "isms", "annex a", "security controls", "information security governance"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "privacy information management system",
        "pims", "privacy extension", "pii controller", "pii processor"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "artificial intelligence management system",
        "aims", "ai management system", "ai risk assessment", "ai impact assessment"
    ],
    "ISO 31000": [
        "iso 31000", "risk management guidelines", "enterprise risk management",
        "erm", "risk treatment", "risk assessment framework", "risk identification"
    ],
    "ISO 9001": [
        "iso 9001", "quality management system", "qms", "quality policy",
        "continuous improvement", "quality audit", "quality objectives"
    ],
    "IEC standards": [
        "iec standards", "iec 62304", "iec 81001", "iec 62443", "iec 27001",
        "international electrotechnical commission", "medical device software", "industrial automation security"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "owasp masvs", "owasp mobile top 10",
        "owasp asvs", "open web application security project", "owasp top ten"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "nist ai risk management framework", "ai rmf",
        "govern map measure manage", "trustworthy ai", "ai risk management"
    ],
    "NIST CSF": [
        "nist csf", "nist cybersecurity framework", "identify protect detect respond recover",
        "csf 2.0", "cybersecurity framework 2.0"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis controls", "center for internet security",
        "cis hardened images", "cis benchmark", "cis critical security controls"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO_?27001", r"ISMS", r"security_policy", r"access_control", r"information_security"
    ],
    "ISO 27701": [
        r"ISO_?27701", r"PIMS", r"pii_protection", r"privacy_policy", r"data_protection"
    ],
    "ISO 42001": [
        r"ISO_?42001", r"AIMS", r"ai_governance", r"ai_risk", r"ai_impact"
    ],
    "ISO 31000": [
        r"ISO_?31000", r"risk_management", r"risk_assessment", r"risk_treatment"
    ],
    "ISO 9001": [
        r"ISO_?9001", r"QMS", r"quality_policy", r"quality_assurance"
    ],
    "IEC standards": [
        r"IEC_?62304", r"IEC_?62443", r"IEC_?81001", r"IEC_?STANDARDS"
    ],
    "OWASP": [
        r"OWASP", r"MASVS", r"ASVS", r"OWASP_TOP_10"
    ],
    "NIST AI RMF": [
        r"NIST_?AI_?RMF", r"AI_?RMF", r"trustworthy_ai", r"ai_risk_management"
    ],
    "NIST CSF": [
        r"NIST_?CSF", r"CSF_?2_?0", r"cybersecurity_framework"
    ],
    "CIS Benchmarks": [
        r"CIS_?BENCHMARK", r"CIS_?CONTROLS", r"cis_hardening"
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

# 10 Comprehensive Mock Announcements for all 10 categories + 1 unverified blog
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "ISO/IEC 27001 updates require mandatory alignment of technological Annex A controls, multi-factor authentication, threat intelligence integration, and cloud service security monitoring.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Standard",
        "description": "ISO/IEC 27701 updates mandate explicit PIMS documentation for PII controllers and processors, continuous privacy risk mapping, and strict data retention controls.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) Requirements",
        "description": "ISO/IEC 42001 establishes an Artificial Intelligence Management System (AIMS) framework requiring continuous AI risk assessment, fairness audits, transparency logging, and AI system life-cycle management.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Guidelines",
        "description": "ISO 31000 guidelines mandate structured risk treatment plans, quantitative risk assessment models, and continuous monitoring of cybersecurity and compliance risk vectors.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System (QMS) Software Assurance Update",
        "description": "ISO 9001 standards require robust continuous integration quality gates, automated testing coverage verification, and formal non-conformance remediation procedures in software engineering workflows.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 81001 Medical and Critical Software Safety Lifecycle Standards",
        "description": "IEC standards enforce strict software development lifecycle controls, architectural risk management, cybersecurity hardening, and formal hazard analysis for connected systems.",
        "link": "https://www.iec.ch/standards",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) Update",
        "description": "OWASP MASVS mandates strict storage encryption, hardware-backed keystores, certificate pinning for dynamic network calls, and robust application resilience against reverse engineering.",
        "link": "https://owasp.org/www-project-mobile-app-security",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Governance and Measurement Update",
        "description": "NIST AI RMF mandates four core functions (GOVERN, MAP, MEASURE, MANAGE) for trustworthy AI deployments, enforcing bias mitigation, explainability, and rigorous AI safety benchmarking.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Core Implementation Guidance",
        "description": "NIST CSF 2.0 expands cybersecurity governance to all organizations across six core functions: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER, emphasizing supply chain risk management.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Critical Security Controls and Hardening Benchmarks",
        "description": "CIS Benchmarks specify baseline security configurations, requiring container hardening, principle of least privilege access, automated patch management, and strict audit logging.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT"
    },
    # Unverified announcement to test blocking
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Industry Blog Rumors on ISO 27001 Changes",
        "description": "A random tech blog claims ISO 27001 is banning all password usage starting next week. This is an unverified industry blog rumor.",
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
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg", "apple.com", "android.com"
    ]
    p1_keywords = [
        "iso/iec", "international organization for standardization", "nist", "owasp",
        "center for internet security", "cis benchmark", "european commission", "enisa", "edpb", "cisa"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "ai generated summaries"]

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
        if ".gov" in combined or "iso.org" in combined or "nist.gov" in combined:
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
                    common_terms = {"iso", "nist", "owasp", "security", "framework", "benchmark"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
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
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html", ".sh", ".py"
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
    processed_categories = set()

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

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Align Information Security Management System (ISMS) controls with ISO/IEC 27001 Annex A controls and threat intelligence procedures."
            )
            impl_checklist.append("- [ ] Audit ISMS policies and map access control policies to ISO/IEC 27001 standards.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit failure for enterprise security certifications.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) documentation for PII controllers and processors."
            )
            impl_checklist.append("- [ ] Update PII processing logs and verify PIMS compliance controls.")
            risk_assessment.append(f"- *{cat}*: Privacy regulatory non-compliance and exposure under global privacy frameworks.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) risk assessment frameworks and fairness/transparency audit logs."
            )
            impl_checklist.append("- [ ] Implement AIMS continuous risk mapping and AI transparency disclosures.")
            risk_assessment.append(f"- *{cat}*: Failure to meet emerging AI management standards and EU AI Act governance expectations.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate ISO 31000 Enterprise Risk Management guidelines into technical security and release auditing."
            )
            impl_checklist.append("- [ ] Formulate quantitative risk treatment plans for technical vulnerability remediation.")
            risk_assessment.append(f"- *{cat}*: Unmanaged operational and technical security risks across component release lifecycles.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Upgrade Quality Management System (QMS) software assurance controls, CI/CD automated test verification, and defect tracking."
            )
            impl_checklist.append("- [ ] Configure automated quality gates and release non-conformance tracking.")
            risk_assessment.append(f"- *{cat}*: Regression vulnerabilities and quality degradation in production releases.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62304 and IEC 81001 software lifecycle safety, threat modeling, and hazard control procedures."
            )
            impl_checklist.append("- [ ] Perform architectural risk analysis and verify IEC software lifecycle compliance.")
            risk_assessment.append(f"- *{cat}*: Critical safety hazards or medical/industrial software certification blocks.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Update security verification controls to match OWASP MASVS and ASVS Level 2 requirements."
            )
            impl_checklist.append("- [ ] Verify OWASP MASVS controls for storage encryption, network pinning, and resilience.")
            risk_assessment.append(f"- *{cat}*: High susceptibility to mobile app exploitation, dynamic hooking, and credential harvesting.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF functions (GOVERN, MAP, MEASURE, MANAGE) across all generative AI components."
            )
            impl_checklist.append("- [ ] Deploy trustworthy AI evaluation metrics and continuous model monitoring controls.")
            risk_assessment.append(f"- *{cat}*: Unmitigated AI hallucinations, bias, and compliance violations.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Transition cybersecurity posture to NIST CSF 2.0 covering GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER."
            )
            impl_checklist.append("- [ ] Map technical security controls against NIST CSF 2.0 categories.")
            risk_assessment.append(f"- *{cat}*: Inadequate threat detection and incident response readiness.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Critical Security Controls and baseline hardening configurations across build scripts and deployments."
            )
            impl_checklist.append("- [ ] Enforce CIS hardening guidelines across container builds and CI environment scripts.")
            risk_assessment.append(f"- *{cat}*: Infrastructure misconfigurations and unauthorized privilege escalation.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards compliance."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces comprehensive updates to align the repository with modern global technical standards. It addresses ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
International standards bodies and cybersecurity frameworks periodically update governance and technical requirements. Continuous compliance monitoring ensures that our security management systems, software lifecycles, mobile controls, and AI risk management frameworks satisfy current industry baselines.

## 3. Regulatory change
- **ISO / IEC Standards**: Compliance updates for ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk Management (ISO 31000), QMS (ISO 9001), and IEC software lifecycles (IEC 62304 / 81001).
- **Security & AI Frameworks**: Alignment with OWASP MASVS/ASVS, NIST AI RMF 1.0, NIST CSF 2.0, and CIS Controls.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and audit risk if technical standards updates are not incorporated into production build and release processes.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes preserve backward compatibility. Minimum runtime requirements are maintained while hardening internal security and governance boundaries.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Execute repo-wide validation and audit scripts.

## 10. Testing checklist
- [ ] Verify that automated test suites pass without regression under ISO 9001 QMS criteria.
- [ ] Confirm OWASP MASVS storage and network pinning checks execute successfully.
- [ ] Validate NIST AI RMF governance logs for active AI integrations.
- [ ] Verify CIS hardening baseline configurations in CI environments.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with verified implementation status.
- [ ] Document technical standards mapping in development guidelines.
- [ ] Ensure AI risk assessments and privacy information management controls are documented.

## 12. Compliance impact
- **Audit Preparedness**: Maintains readiness for formal ISO/IEC certifications and third-party audits.
- **Security Posture**: Hardens codebase against OWASP and NIST identified vulnerability classes.
- **Regulatory Support**: Facilitates EU AI Act and GDPR compliance via standardized governance frameworks.

## 13. Breaking changes
- No functional breaking changes are introduced; security hardening measures enforce stricter runtime validation and build gates.

## 14. Review checklist
- [ ] Diff is 100% free of emojis or graphical symbols.
- [ ] All cited sources are Priority 1-3 or traceably verified.
- [ ] Implementation checklists reflect actionable technical updates.

## 15. Approver recommendations
Verify that the automated compliance guard and test suites pass completely, and confirm that all technical standards citations are traceably verified against official standardization body publications.
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
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across key technical standards.",
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

    processed_task_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            if f"{cat}_blocked" in processed_task_categories:
                continue
            processed_task_categories.add(f"{cat}_blocked")
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        if cat in processed_task_categories:
            continue
        processed_task_categories.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority technical standards requirement.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update ISMS access control policies to align with ISO/IEC 27001 Annex A.")
            lines.append("- [ ] **Task 2**: Conduct technical risk assessment on credential handling.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Document PIMS controls for PII controllers and processors.")
            lines.append("- [ ] **Task 2**: Implement continuous privacy impact assessment procedures.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Build AIMS risk mapping for generative AI features.")
            lines.append("- [ ] **Task 2**: Implement AI transparency and fairness audit logging.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Establish quantitative technical risk treatment framework.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Implement continuous integration quality gates and automated test checks.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Perform IEC 62304 / 81001 software lifecycle hazard analysis.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Verify OWASP MASVS Level 2 mobile storage and network controls.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Configure NIST AI RMF GOVERN, MAP, MEASURE, MANAGE functions.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Map technical controls against NIST CSF 2.0 categories.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Enforce CIS hardened baseline settings in CI scripts.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all platform criteria for {cat} are checked and handled.")
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
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/x/news.xml"))
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

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u)
            status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
            print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    if not args.json:
        print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
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
