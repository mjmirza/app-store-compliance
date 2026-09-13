#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards categories (ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks),
scans the codebase for repository gaps, generates implementation tasks, documentation updates,
and testing updates, and drafts an emoji-free 15-section Pull Request proposal.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards categories
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
        "isms",
        "information security management",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management system",
        "ai risk assessment",
        "ai impact assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk assessment framework",
        "risk treatment plan",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality policy",
        "continuous improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "international electrotechnical commission",
    ],
    "OWASP": [
        "owasp",
        "top 10",
        "masvs",
        "asvs",
        "open web application security project",
        "api security top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
        "govern map measure manage",
    ],
    "NIST CSF": [
        "nist csf",
        "nist cybersecurity framework",
        "identify protect detect respond recover",
        "csf 2.0",
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
        r"ISO[ -_]?27001",
        r"ISMS",
        r"informationSecurityPolicy",
        r"accessControl",
        r"encryptionAtRest",
    ],
    "ISO 27701": [
        r"ISO[ -_]?27701",
        r"PIMS",
        r"piiProcessing",
        r"privacyByDesign",
        r"dataProtectionOfficer",
    ],
    "ISO 42001": [
        r"ISO[ -_]?42001",
        r"AIMS",
        r"aiGovernance",
        r"modelCard",
        r"algorithmicBias",
    ],
    "ISO 31000": [
        r"ISO[ -_]?31000",
        r"riskRegister",
        r"riskAssessment",
        r"riskMitigation",
    ],
    "ISO 9001": [
        r"ISO[ -_]?9001",
        r"qualityPolicy",
        r"auditLog",
        r"correctiveAction",
    ],
    "IEC standards": [
        r"IEC[ -_]?62304",
        r"IEC[ -_]?62443",
        r"IEC[ -_]?82304",
        r"medicalDeviceSoftware",
        r"industrialCybersecurity",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"inputValidation",
        r"outputEncoding",
    ],
    "NIST AI RMF": [
        r"NIST[ -_]?AI[ -_]?RMF",
        r"aiRiskManagement",
        r"trustworthyAI",
        r"modelTransparency",
    ],
    "NIST CSF": [
        r"NIST[ -_]?CSF",
        r"cybersecurityFramework",
        r"incidentResponse",
        r"threatDetection",
    ],
    "CIS Benchmarks": [
        r"CIS[ -_]?Benchmark",
        r"cisControls",
        r"systemHardening",
        r"secureConfiguration",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CISecurity, European Commission, FTC, CISA, BSI)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Mock Announcements for all 10 technical standards categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Controls Update",
        "description": "ISO releases revised Annex A controls emphasizing secure coding, threat intelligence, data masking, and web filtering mandatory for ISMS certifications.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 guidelines mandate explicit PII controller and processor role declarations, privacy impact assessments, and data deletion workflows.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Standard",
        "description": "ISO/IEC 42001 specifies requirements for establishing, implementing, and continually improving an Artificial Intelligence Management System (AIMS) with focus on AI safety and transparency.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Guidelines Refresh",
        "description": "ISO 31000 updates risk management guidelines to integrate cyber risk assessment, continuous risk treatment plans, and quantitative risk register metrics.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Digital Process Standard",
        "description": "ISO 9001 quality management rules mandate clear software change management, continuous quality metrics, and traceable audit logging across production pipelines.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 and IEC 62304 Functional Cybersecurity & Software Lifecycle Standards",
        "description": "IEC releases updated lifecycle and cybersecurity standards for software development, requiring strict threat modeling and automated static analysis.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 and Top 10 Security Verification Guidance",
        "description": "OWASP publishes updated Mobile Application Security Verification Standard (MASVS) controls for network communication, data storage, and resilient anti-tampering.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-AIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Guidance Update",
        "description": "NIST releases updated AI RMF guidelines structured around Govern, Map, Measure, and Manage functions to address generative AI risks and algorithmic bias.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 (CSF 2.0) Implementation Directive",
        "description": "NIST CSF 2.0 introduces the Governance function alongside Identify, Protect, Detect, Respond, and Recover, requiring enterprise-wide cybersecurity strategy integration.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls v8.1 and System Hardening Benchmarks",
        "description": "CIS publishes updated benchmarks for secure application deployment, TLS configuration, container hardening, and automated vulnerability remediation.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO 27001 Mandatory Quantum Encryption",
        "description": "A random tech blog claims ISO 27001 will require quantum-resistant encryption for all web applications by next week. This is an unverified industry blog post.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT",
    },
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
        "bsi.bund.de",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "center for internet security",
        "european commission",
        "eur-lex",
        "official journal",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
        "ico",
        "government publication",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = [
        "academic paper",
        "academic study",
        "university research",
        "peer-reviewed",
    ]

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

    priority = 4  # Default to 4 if nothing matches

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(
        kw in combined for kw in p4_keywords
    ):
        priority = 4
    elif (
        any(d in link for d in p3_domains)
        or any(kw in combined for kw in p3_keywords)
        or ".edu" in link
    ):
        priority = 3
    elif any(d in link for d in p2_domains) or any(
        kw in combined for kw in p2_keywords
    ):
        priority = 2

    if (
        any(d in link for d in p1_domains)
        or any(kw in combined for kw in p1_keywords)
        or ".gov" in link
    ):
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
                    common_terms = {"iso", "nist", "owasp", "security", "risk", "framework", "cis"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans codebase for files matching signals related to the 10 technical standards categories.
    """
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
    """
    Fetches and parses live RSS or Atom XML feeds.
    """
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
                f"- **{cat}**: Update Information Security Management System (ISMS) controls in compliance with Annex A requirements, including access controls and encryption at rest."
            )
            impl_checklist.append("- [ ] Audit and map ISMS controls against updated ISO 27001 Annex A standards.")
            risk_assessment.append(f"- *{cat}*: Non-conformity during external ISMS certification audits leading to loss of ISO 27001 compliance standing.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Update Privacy Information Management System (PIMS) controls, documenting PII controller/processor role matrices and PII deletion workflows."
            )
            impl_checklist.append("- [ ] Establish PIMS data mapping and document PII processor responsibilities.")
            risk_assessment.append(f"- *{cat}*: Privacy regulatory penalties and PIMS certification failure due to unmapped PII processing flows.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) controls, including AI impact assessments, algorithmic bias mitigations, and model cards."
            )
            impl_checklist.append("- [ ] Draft AI impact assessments and maintain model card documentation under AIMS.")
            risk_assessment.append(f"- *{cat}*: Algorithmic bias exposure and non-compliance with emerging AI management standards.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Update enterprise risk management frameworks, refreshing the risk register and implementing continuous risk treatment plans."
            )
            impl_checklist.append("- [ ] Refresh enterprise risk register and validate risk treatment controls.")
            risk_assessment.append(f"- *{cat}*: Unmitigated technical or operational risks leading to unaddressed compliance gaps.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Update Quality Management System (QMS) software lifecycle procedures, enforcing change management controls and audit logging."
            )
            impl_checklist.append("- [ ] Enforce QMS change management checks in production deployment pipelines.")
            risk_assessment.append(f"- *{cat}*: Software quality degradation and audit findings during QMS certification reviews.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Implement functional safety and cybersecurity software lifecycle processes in accordance with IEC 62304 and IEC 62443."
            )
            impl_checklist.append("- [ ] Execute software safety classification and threat modeling for IEC standards.")
            risk_assessment.append(f"- *{cat}*: Cybersecurity vulnerability in software lifecycle components violating IEC guidelines.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Enforce OWASP MASVS and ASVS controls, focusing on input validation, secure storage, network transport, and resilient code anti-tampering."
            )
            impl_checklist.append("- [ ] Verify OWASP MASVS Level 1 and Level 2 security verification requirements.")
            risk_assessment.append(f"- *{cat}*: Vulnerability exploitation (XSS, SQLi, broken auth) mapped in OWASP Top 10.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Align AI features with NIST AI RMF core functions (Govern, Map, Measure, Manage), establishing trustworthy AI benchmarks."
            )
            impl_checklist.append("- [ ] Implement NIST AI RMF transparency disclosures and model evaluation metrics.")
            risk_assessment.append(f"- *{cat}*: Hallucination, bias, or safety failures in deployed AI models violating NIST guidance.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Update security architectures to reflect NIST CSF 2.0, integrating Governance alongside Identify, Protect, Detect, Respond, and Recover."
            )
            impl_checklist.append("- [ ] Map technical controls against NIST CSF 2.0 sub-categories and governance framework.")
            risk_assessment.append(f"- *{cat}*: Increased mean time to detect (MTTD) and respond to security incidents.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Controls v8.1 system hardening benchmarks across operating systems, cloud containers, and network endpoints."
            )
            impl_checklist.append("- [ ] Run automated CIS benchmark hardening audit scripts against environment configurations.")
            risk_assessment.append(f"- *{cat}*: System compromise due to unhardened default configuration parameters.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic technical standards review."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into complete alignment with updated technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It establishes mandatory technical controls, documentation structures, and testing safeguards.

## 2. Background
Technical standards evolve to address emerging security vulnerabilities, privacy expectations, and AI governance requirements. Adherence to international standards (ISO/IEC), industry frameworks (NIST, CIS), and security verification criteria (OWASP) is essential for maintaining certification, audit readiness, and software integrity.

## 3. Regulatory change
- **ISO/IEC Standards**: Enforcement of updated ISMS (27001), PIMS (27701), AIMS (42001), Risk Management (31000), and Quality Management (9001) controls.
- **IEC & OWASP Frameworks**: Lifecycle cybersecurity (IEC 62443/62304) and mobile application security verification standards (OWASP MASVS).
- **NIST & CIS Guidelines**: Cybersecurity Framework 2.0 (NIST CSF 2.0), AI Risk Management Framework (NIST AI RMF 1.0), and CIS Hardening Benchmarks v8.1.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and audit risk if technical controls fail to align with recognized ISO/NIST/OWASP/CIS standards.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standards updates are non-breaking and fully backward-compatible. Technical controls add defense-in-depth safeguards without modifying existing public API signatures or schema definitions.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run repository compliance verification scripts locally.

## 10. Testing checklist
- [ ] Verify that access controls and data encryption meet ISO 27001 Annex A criteria.
- [ ] Run static security analysis checking OWASP MASVS vulnerability compliance.
- [ ] Validate CIS benchmark hardening rules in container and server build manifests.
- [ ] Confirm AI governance model evaluation logging functions as expected under NIST AI RMF.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed tasks and evidence logs.
- [ ] Maintain the enterprise risk register (ISO 31000) and QMS change documentation (ISO 9001).
- [ ] Document PII processor roles (ISO 27701) and AI model cards (ISO 42001).

## 12. Compliance impact
- **Audit Preparedness**: Ensures full compliance during ISO 27001 / ISO 27701 / ISO 42001 external audits.
- **Cybersecurity Resilience**: Satisfies NIST CSF 2.0 and CIS Benchmark hardening requirements.
- **AI Transparency & Safety**: Aligns AI capabilities with NIST AI RMF and ISO 42001 governance standards.

## 13. Breaking changes
- No breaking software API changes. Configuration default hardening is applied in accordance with CIS Benchmarks.

## 14. Review checklist
- [ ] Code and documentation diffs are 100% emoji-free.
- [ ] Official citations strictly comply with the source trust hierarchy rules.
- [ ] Hardening changes pass automated regression test suites.

## 15. Approver recommendations
Verify that all technical control mappings pass localized security checks. Confirm that the risk register (ISO 31000) and AI safety impact assessments (NIST AI RMF / ISO 42001) are approved by Information Security Lead prior to release authorization.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Generates identified repository gaps, implementation tasks, documentation updates,
    and testing updates for each matched standard change.
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
        lines.append("- **Regulatory Impact**: High priority technical standards compliance area.")

        # 1. Identify repository gaps
        files = scan_results.get(cat, [])
        lines.append("- **Repository Gaps Identified**:")
        if files:
            for f in files:
                lines.append(f"  - Matched signal in `{f['file']}` (line {f['line_num']}): pattern `{f['matched_pattern']}`")
        else:
            lines.append(f"  - No explicit signal matches found in codebase for {cat}. Repository configuration audit required.")

        # 2. Implementation tasks
        lines.append("- **Implementation Tasks**:")
        if cat == "ISO 27001":
            lines.append("  - [ ] Update ISMS access controls and encryption configurations.")
            lines.append("  - [ ] Implement Annex A threat intelligence and data masking controls.")
        elif cat == "ISO 27701":
            lines.append("  - [ ] Define PIMS roles (PII controller vs processor) across data pipelines.")
            lines.append("  - [ ] Implement automated user PII deletion workflows.")
        elif cat == "ISO 42001":
            lines.append("  - [ ] Build AI Management System (AIMS) governance controls.")
            lines.append("  - [ ] Implement AI algorithmic bias mitigations and model card tracking.")
        elif cat == "ISO 31000":
            lines.append("  - [ ] Refresh enterprise risk register with cyber risk vectors.")
            lines.append("  - [ ] Implement automated risk treatment tracking.")
        elif cat == "ISO 9001":
            lines.append("  - [ ] Integrate QMS software change management controls into CI/CD pipelines.")
            lines.append("  - [ ] Enforce traceable production audit logging.")
        elif cat == "IEC standards":
            lines.append("  - [ ] Establish IEC 62304 / IEC 62443 software lifecycle safety classifications.")
            lines.append("  - [ ] Integrate threat modeling into development sprints.")
        elif cat == "OWASP":
            lines.append("  - [ ] Audit application against OWASP MASVS L1/L2 security requirements.")
            lines.append("  - [ ] Enforce strict input validation and output encoding across API endpoints.")
        elif cat == "NIST AI RMF":
            lines.append("  - [ ] Implement NIST AI RMF core functions (Govern, Map, Measure, Manage).")
            lines.append("  - [ ] Deploy user transparency disclaimers for AI generative features.")
        elif cat == "NIST CSF":
            lines.append("  - [ ] Align enterprise cybersecurity posture with NIST CSF 2.0 Governance function.")
            lines.append("  - [ ] Update incident response protocols for Detect and Respond categories.")
        elif cat == "CIS Benchmarks":
            lines.append("  - [ ] Apply CIS Controls v8.1 system hardening benchmarks.")
            lines.append("  - [ ] Configure secure TLS 1.3 defaults and container security parameters.")
        else:
            lines.append(f"  - [ ] Implement technical standards controls for {cat}.")

        # 3. Documentation updates
        lines.append("- **Documentation Updates**:")
        lines.append(f"  - [ ] Update internal compliance documentation in `docs/STANDARDS-POLICY-MIGRATION.md` for {cat}.")
        lines.append(f"  - [ ] Record compliance verification evidence and risk register entries for {cat}.")

        # 4. Testing updates
        lines.append("- **Testing Updates**:")
        lines.append(f"  - [ ] Add automated unit and integration tests verifying security controls for {cat}.")
        lines.append(f"  - [ ] Execute static security analysis and regression test suite for {cat}.")

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
        description="Monitor Technical Standards Compliance (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS)"
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
        announcements.extend(parse_rss_feed("https://www.iso.org/contents/data/standard/rss.xml"))
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

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, scan_results, args.output_docs)

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
