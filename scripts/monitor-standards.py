#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards: ISO 27001, ISO 27701, ISO 42001, ISO 31000,
ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Identifies repository gaps, generates implementation tasks, documentation updates,
and testing updates following the Source Trust Hierarchy.
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
    "CIS Benchmarks"
]

# Keywords used to classify incoming announcements/articles into the 10 standards
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001", "iso/iec 27001", "isms", "information security management",
        "annex a controls", "iso27001", "information security management system"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "pims", "privacy information management",
        "pii controller", "pii processor", "iso27701", "privacy information management system"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "aims", "artificial intelligence management system",
        "ai governance", "ai risk assessment", "iso42001", "ai management system"
    ],
    "ISO 31000": [
        "iso 31000", "iso/iec 31000", "risk management guidelines",
        "enterprise risk management", "risk assessment framework", "iso31000"
    ],
    "ISO 9001": [
        "iso 9001", "iso/iec 9001", "qms", "quality management system",
        "software quality assurance", "process control", "iso9001"
    ],
    "IEC standards": [
        "iec standards", "iec 62443", "iec 82304", "iec 62304",
        "industrial security", "medical device software", "functional safety", "iec"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "owasp masvs", "owasp asvs", "owasp llm",
        "top ten", "web application security project"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "nist ai 100",
        "govern map measure manage", "trustworthy ai", "nist ai"
    ],
    "NIST CSF": [
        "nist csf", "nist cybersecurity framework", "cybersecurity framework 2.0",
        "identify protect detect respond recover", "sp 800-53", "nist csf 2.0"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "center for internet security", "cis controls",
        "cis hardening", "cis benchmark", "cis level 1", "cis level 2"
    ]
}

# Codebase signals (regex patterns) to find files affected by each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS", r"iso_27001", r"access_control", r"encryption_at_rest", r"security_policy"
    ],
    "ISO 27701": [
        r"PIMS", r"iso_27701", r"pii_data", r"privacy_policy", r"data_retention"
    ],
    "ISO 42001": [
        r"AIMS", r"iso_42001", r"ai_governance", r"ai_risk", r"model_card", r"ai_audit"
    ],
    "ISO 31000": [
        r"iso_31000", r"risk_register", r"risk_assessment", r"risk_matrix", r"mitigation_plan"
    ],
    "ISO 9001": [
        r"QMS", r"iso_9001", r"quality_assurance", r"qa_process", r"version_control"
    ],
    "IEC standards": [
        r"IEC_62443", r"IEC_82304", r"IEC_62304", r"iec_standard", r"safety_integrity"
    ],
    "OWASP": [
        r"OWASP", r"MASVS", r"ASVS", r"xss_protection", r"csrf_token", r"input_sanitization"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF", r"ai_rmf", r"govern_map_measure_manage", r"bias_mitigation", r"model_explainability"
    ],
    "NIST CSF": [
        r"NIST_CSF", r"csf_protect", r"csf_detect", r"csf_respond", r"asset_inventory"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark", r"cis_hardening", r"cis_controls", r"secure_baseline"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, CISA, FTC)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements covering all 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management System Controls Update",
        "description": "Updated Annex A guidance mandates strict access controls, dynamic threat intelligence integration, and mandatory cloud service security baselines for all ISMS certified systems.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Enhancement",
        "description": "Expanded PIMS controls require granular PII controller mapping, automated data subject request processing, and explicit processor data transfer auditing.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System Standard Requirements",
        "description": "Mandates continuous AI system risk assessments, algorithmic impact audits, dataset provenance tracking, and model lifecycle governance for artificial intelligence systems.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework Application Guidelines",
        "description": "Guidelines require continuous risk identification, formal risk registers, quantitative impact evaluations, and systematic mitigation review schedules.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Software Engineering Guidelines",
        "description": "Requires formalized software quality assurance, rigorous change control procedures, automated release testing gates, and systematic defect tracking.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC Standards Update: Security and Reliability in Software Lifecycles",
        "description": "IEC 62443 and IEC 82304 standards mandate secure component integration, threat modeling, system integrity checks, and software safety verification.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Security Verification Standard Guidelines Update",
        "description": "Updated OWASP MASVS and Top 10 standards require robust input sanitization, memory safety, anti-tampering verification, and secure API integration.",
        "link": "https://owasp.org/www-project-top-ten/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework Implementation Guidance",
        "description": "NIST AI RMF 1.0 guidelines require organizations to GOVERN, MAP, MEASURE, and MANAGE AI risks, focusing on fairness, transparency, explainability, and bias mitigation.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Governance and Security Guidance",
        "description": "NIST CSF 2.0 introduces the GOVERN function alongside Identify, Protect, Detect, Respond, and Recover, emphasizing supply chain risk management and continuous control auditing.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls Level 1 and Level 2 Baseline Hardening",
        "description": "Updated CIS Benchmarks enforce secure system configurations, disabling unneeded network services, automated vulnerability scanning, and strict access control baselines.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Post Rumors on Technical Standards Changes",
        "description": "An unverified industry blog claims technical standards are changing overnight without public consultation. This is an unverified blog post.",
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
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk"
    ]
    p1_keywords = [
        "iso standard", "iec standard", "nist", "owasp", "cis benchmark",
        "european commission", "eur-lex", "enisa", "cisa", "ftc"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai generated summary", "chatgpt summary"]

    priority = 4  # Default to 4 if unspecified

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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "framework"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards.
    Excludes build, vendor, node_modules, and test directories.
    """
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
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
                    ".py", ".kt", ".java", ".xml", ".gradle", ".kts", ".json",
                    ".js", ".ts", ".md", ".sh", ".yaml", ".yml", ".swift", ".m"
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
    """Generates a draft of a pull request complying with the exact 15 required sections."""
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
                f"- **{cat}**: Align Information Security Management System (ISMS) controls with updated Annex A requirements."
            )
            impl_checklist.append("- [ ] Audit access controls and encryption at rest for ISMS compliance.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with ISMS audit requirements leading to certification risk.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Implement Privacy Information Management System (PIMS) PII controller and processor requirements."
            )
            impl_checklist.append("- [ ] Update PII data inventory and processor agreement verifications.")
            risk_assessment.append(f"- *{cat}*: Inadequate PII processing controls resulting in privacy regulation violations.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance and risk management workflows."
            )
            impl_checklist.append("- [ ] Deploy model cards and conduct AI algorithmic impact assessments.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI model deployment leading to algorithmic bias or safety failures.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Maintain formal enterprise risk register and structured risk mitigation matrix."
            )
            impl_checklist.append("- [ ] Update repository risk register and quantitative impact scoring.")
            risk_assessment.append(f"- *{cat}*: Unidentified operational or security risks causing unexpected breaches.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize Software Quality Assurance (SQA) processes and change management controls."
            )
            impl_checklist.append("- [ ] Enforce automated CI/CD quality gates and release documentation.")
            risk_assessment.append(f"- *{cat}*: Process defects and lack of audit trails impacting software deliverable quality.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Apply IEC 62443 / IEC 82304 secure software lifecycle and safety integrity requirements."
            )
            impl_checklist.append("- [ ] Perform threat modeling and secure component integrity checks.")
            risk_assessment.append(f"- *{cat}*: Vulnerabilities in software lifecycle components exposing functional safety.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Verify adherence to OWASP Top 10, MASVS, and ASVS security verification standards."
            )
            impl_checklist.append("- [ ] Sanitize user inputs and enforce anti-tampering verification controls.")
            risk_assessment.append(f"- *{cat}*: Exploitable web or mobile security vulnerabilities (XSS, Injection, BOLA).")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Apply NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions across AI integrations."
            )
            impl_checklist.append("- [ ] Execute AI trustworthiness evaluation and bias mitigation testing.")
            risk_assessment.append(f"- *{cat}*: Unmanaged AI trustworthiness risks resulting in regulatory scrutiny.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST CSF 2.0 GOVERN, Identify, Protect, Detect, Respond, and Recover controls."
            )
            impl_checklist.append("- [ ] Update asset inventory and incident response playbooks.")
            risk_assessment.append(f"- *{cat}*: Security control gaps during threat detection or incident response.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Controls Level 1 and Level 2 baseline configuration hardening."
            )
            impl_checklist.append("- [ ] Validate operating environment against CIS Benchmark automated checks.")
            risk_assessment.append(f"- *{cat}*: Misconfigured system services exposing infrastructure to automated exploits.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the codebase and architecture into alignment with updated international technical standards, covering ISO, IEC, OWASP, NIST, and CIS Benchmarks.

## 2. Background
Technical standards evolve to address emerging security vulnerabilities, AI governance imperatives, and quality management baselines. Proactively implementing these standard controls ensures enterprise compliance and system resilience.

## 3. Regulatory change
- **ISO / IEC Standards**: Compliance updates across ISO 27001 (ISMS), ISO 27701 (PIMS), ISO 42001 (AIMS), ISO 31000 (Risk), ISO 9001 (QMS), and IEC security lifecycles.
- **Security & AI Frameworks**: OWASP verification standard alignment, NIST AI RMF trustworthy AI controls, NIST CSF 2.0 governance, and CIS Benchmarks baseline hardening.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and security risk if technical standards baselines are allowed to drift.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes adhere to strict backward compatibility. Standard controls enhance security boundaries and process governance without breaking runtime API interfaces.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run repository compliance validation script.

## 10. Testing checklist
- [ ] Run security regression test suites and static analysis tools.
- [ ] Conduct automated CIS hardening check on target environment.
- [ ] Verify AI model output explainability and fairness metrics.
- [ ] Validate ISMS access control rules and PIMS PII handling flows.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed tasks.
- [ ] Record updated risks in the project risk register.
- [ ] Document security baseline configurations in developer guidelines.

## 12. Compliance impact
- **Audit Readiness**: Ensures audit readiness for ISO/IEC certifications and NIST compliance audits.
- **Security Resilience**: Strengthens application defenses against OWASP top vulnerabilities and CIS hardening gaps.
- **AI Governance**: Satisfies ISO 42001 and NIST AI RMF trustworthy AI requirements.

## 13. Breaking changes
- Non-compliant legacy configurations or unencrypted channels are disabled, requiring compliant transport security.

## 14. Review checklist
- [ ] Code is 100% free of emojis or graphical symbols.
- [ ] Citations point to verified Priority 1 official standards publications.
- [ ] All implementation, documentation, and testing tasks are verified.

## 15. Approver recommendations
Verify that access control rules and encryption baselines pass automated scanning before approving deployment. Confirm that AI model cards and risk assessments are attached for all deployed machine learning services.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath, quiet=False):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
        "",
        "## Monitored Standards Update Log",
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

    lines.append("## Repository Gap Analysis")
    lines.append("")

    for u in updates:
        cat = u["category"]
        files = scan_results.get(cat, [])
        lines.append(f"### Repository Gaps for {cat}")
        if files:
            lines.append(f"- **Matching Signal Files ({len(files)})**:")
            for f in files[:5]:
                lines.append(f"  - `{f['file']}:{f['line_num']}` - {f['content']}")
            if len(files) > 5:
                lines.append(f"  - ... and {len(files) - 5} more matching references.")
        else:
            lines.append("- **Repository Status**: No matching signal keywords found in codebase. Manual verification required to establish baseline.")
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
        lines.append("- **Regulatory Impact**: High priority technical standard requirement.")
        lines.append(f"- [ ] **Implementation Task**: Align code and system architecture with {cat} specification requirements.")
        lines.append(f"- [ ] **Documentation Update**: Update `docs/STANDARDS-POLICY-MIGRATION.md` and standard operating procedure guides for {cat}.")
        lines.append(f"- [ ] **Testing Update**: Add automated regression tests and security checks for {cat} compliance.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        if not quiet:
            print(f"Technical standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
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
        "--dir", "--project", type=str, default=".", help="Codebase directory to scan"
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
        "--simulate",
        type=str,
        help="Simulate standard track evaluation for a specific standard or query",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        if not args.json:
            print("Fetching live Technical Standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

    if args.mock or (not args.live and not args.mock) or not announcements:
        if not args.json:
            print("Using comprehensive mock Technical Standards updates for compliance scanning...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                if not args.json:
                    print(
                        f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.",
                        file=sys.stderr,
                    )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # 2. Filter / Classify updates
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    if args.simulate:
        keywords_filter = [args.simulate]

    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        if not args.json:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u, classified_updates)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
            if not args.json:
                print(f"ALERT: Blocked unverified secondary source update: {u['title']}", file=sys.stderr)
        else:
            verified_updates.append(u)

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u, classified_updates)
            status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
            print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    # 3. Scan codebase
    target_dir = getattr(args, "dir", None) or getattr(args, "project", ".")
    if not args.json:
        print(f"Scanning codebase under '{target_dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(target_dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    # 4. Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, scan_results, args.output_docs, quiet=args.json)

    # 5. Generate PR draft using verified updates
    pr_draft = None
    if verified_updates:
        pr_draft = generate_pull_request_draft(verified_updates, scan_results)
        if args.pr_output:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            try:
                with open(args.pr_output, "w", encoding="utf-8") as f:
                    f.write(pr_draft)
                if not args.json:
                    print(f"PR draft written successfully to: {args.pr_output}")
            except Exception as e:
                if not args.json:
                    print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    # 6. JSON output
    if args.json:
        report_data = {
            "monitored_standards": TRACKED_CATEGORIES,
            "classified_updates_count": len(classified_updates),
            "verified_updates_count": len(verified_updates),
            "blocked_updates_count": blocked_updates_count,
            "signal_matches_count": total_matches,
            "proposed_pull_request": pr_draft,
            "updates": []
        }
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u, classified_updates)
            cat = u["category"]
            report_data["updates"].append({
                "category": cat,
                "title": u["title"],
                "pubDate": u["pubDate"],
                "link": u["link"],
                "priority": priority,
                "verified": is_verified,
                "signal_matches": scan_results.get(cat, [])
            })
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
