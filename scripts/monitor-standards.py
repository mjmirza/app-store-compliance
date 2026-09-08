#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 distinct technical standards: ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
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

# Keywords used to classify incoming announcements/articles into the 10 standards
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        r"\biso 27001\b", r"\biso/iec 27001\b", r"\binformation security management system\b",
        r"\bisms\b", r"\bannex a\b", r"\biso27001\b"
    ],
    "ISO 27701": [
        r"\biso 27701\b", r"\biso/iec 27701\b", r"\bprivacy information management system\b",
        r"\bpims\b", r"\bpii processor\b", r"\bpii controller\b", r"\biso27701\b"
    ],
    "ISO 42001": [
        r"\biso 42001\b", r"\biso/iec 42001\b", r"\bartificial intelligence management system\b",
        r"\baims\b", r"\bai risk management standard\b", r"\biso42001\b"
    ],
    "ISO 31000": [
        r"\biso 31000\b", r"\brisk management framework\b",
        r"\benterprise risk management\b", r"\biso31000\b"
    ],
    "ISO 9001": [
        r"\biso 9001\b", r"\bquality management system\b", r"\bqms\b", r"\bquality assurance framework\b",
        r"\biso9001\b"
    ],
    "IEC standards": [
        r"\biec standards\b", r"\biec 62443\b", r"\biec 82304\b", r"\biec 62304\b",
        r"\bmedical device software\b", r"\bindustrial automation security\b"
    ],
    "OWASP": [
        r"\bowasp\b", r"\bowasp top 10\b", r"\bmasvs\b", r"\bmstg\b",
        r"\bopen web application security project\b"
    ],
    "NIST AI RMF": [
        r"\bnist ai rmf\b", r"\bai risk management framework\b", r"\bnist ai 100-1\b",
        r"\btrustworthy ai\b"
    ],
    "NIST CSF": [
        r"\bnist csf\b", r"\bnist csf 2.0\b", r"\bcybersecurity framework\b", r"\bnist sp 800-53\b"
    ],
    "CIS Benchmarks": [
        r"\bcis benchmarks\b", r"\bcenter for internet security\b", r"\bcis controls\b",
        r"\bcis benchmark\b"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 standards
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"SecurityPolicy",
        r"access_control",
        r"data_classification",
        r"audit_log"
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"data_protection_officer",
        r"dpo",
        r"pii_handling"
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"model_card",
        r"ai_impact_assessment",
        r"llm_audit"
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_assessment",
        r"risk_register",
        r"risk_matrix",
        r"risk_mitigation"
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_management",
        r"process_audit",
        r"continuous_improvement"
    ],
    "IEC standards": [
        r"IEC62443",
        r"IEC62304",
        r"IEC82304",
        r"software_lifecycle",
        r"functional_safety"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MSTG",
        r"sanitization",
        r"sql_injection",
        r"csrf_protection"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"trustworthy_ai",
        r"bias_mitigation",
        r"explainability",
        r"model_monitoring"
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurity_framework",
        r"incident_response",
        r"threat_hunting",
        r"asset_management"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Control",
        r"hardening",
        r"benchmark_config",
        r"secure_baseline"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# Mock announcements covering all 10 standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Information Security Management System Controls Update",
        "description": "Updated ISO 27001 Annex A guidance mandates strict cloud security posture management, threat intelligence integration, and automated logging for access controls.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System Requirements Enhancement",
        "description": "ISO 27701 specifies updated operational requirements for PII controllers and processors, mandating automated privacy impact assessments and data minimization protocols.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System Certification Standards",
        "description": "ISO 42001 establishes global requirements for AI management systems, enforcing model cards, bias mitigation testing, transparency disclosures, and AI risk governance.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Guidelines",
        "description": "ISO 31000 risk management guidelines mandate continuous risk evaluation, updated risk register schemas, and formal risk treatment reporting across all software pipelines.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Process Standard Refinement",
        "description": "ISO 9001 standards require documented software quality assurance pipelines, automated release audits, and continuous customer feedback verification loops.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC standards IEC 62443 and IEC 62304 Security and Lifecycle Guidance",
        "description": "IEC standards mandate secure software lifecycle processes, strict component isolation, threat modeling, and formal validation testing for distributed and embedded software.",
        "link": "https://www.iec.ch/",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 and MASVS (Mobile Application Security Verification Standard) Update",
        "description": "OWASP issues revised MASVS guidelines for mobile and web security, tightening controls on network security, authentication storage, code hardening, and API endpoint verification.",
        "link": "https://owasp.org/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Companion Guidelines",
        "description": "NIST AI RMF releases updated sub-categories across GOVERN, MAP, MEASURE, and MANAGE functions, requiring trustworthy AI metrics, red-teaming benchmarks, and safety evaluation suites.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Implementation Standard",
        "description": "NIST CSF 2.0 introduces the GOVERN function alongside Identify, Protect, Detect, Respond, and Recover, requiring enterprise supply chain risk management and automated incident reporting.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Controls Baseline Security Guidance",
        "description": "Center for Internet Security (CIS) Benchmarks update baseline hardening guidelines, mandating encrypted transport configurations, strict container isolation, and disabled legacy protocols.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-RUMOR",
        "category": "OWASP",
        "title": "Unverified Blog Rumors on OWASP Security Guidance",
        "description": "An unverified personal blog claims OWASP will deprecate password logins. This is an unverified blog post.",
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
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg"
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
    Scans the codebase for files containing signals related to each of the 10 standards categories.
    Identifies repository gaps and affected files.
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
        for cat, patterns in CATEGORY_KEYWORDS.items():
            for pat in patterns:
                if re.search(pat, text_to_search, re.IGNORECASE):
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
    Deduplicates details by category.
    """
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    test_checklist = []
    doc_checklist = []
    risk_assessment = []

    processed_categories = set()

    for u in updates:
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
                f"- **{cat}**: Update Information Security Management System (ISMS) controls, access control policies, and logging mechanisms."
            )
            impl_checklist.append("- [ ] Audit ISMS Annex A controls and align access control logging.")
            test_checklist.append("- [ ] Verify automated access control and security audit log generation.")
            doc_checklist.append("- [ ] Update ISMS policy documentation in docs/STANDARDS-POLICY-MIGRATION.md.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with information security management standard controls.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Extend ISMS controls to Privacy Information Management System (PIMS) for PII controller/processor requirements."
            )
            impl_checklist.append("- [ ] Implement PIMS data minimization and PII controller controls.")
            test_checklist.append("- [ ] Conduct privacy impact assessment validation tests.")
            doc_checklist.append("- [ ] Document PIMS controller/processor responsibilities.")
            risk_assessment.append(f"- *{cat}*: Privacy information management non-compliance and exposure of PII.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Deploy AI Management System (AIMS) governance controls, model cards, and AI risk assessments."
            )
            impl_checklist.append("- [ ] Create AI model cards and implement bias mitigation checks.")
            test_checklist.append("- [ ] Execute AI model transparency and red-teaming safety tests.")
            doc_checklist.append("- [ ] Document AIMS governance frameworks and risk disclosures.")
            risk_assessment.append(f"- *{cat}*: AI safety and governance non-compliance under ISO 42001.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align risk assessment matrix and risk register schemas with ISO 31000 principles."
            )
            impl_checklist.append("- [ ] Update enterprise risk register and risk mitigation workflows.")
            test_checklist.append("- [ ] Validate automated risk assessment matrix evaluation scripts.")
            doc_checklist.append("- [ ] Publish ISO 31000 risk management guidelines.")
            risk_assessment.append(f"- *{cat}*: Unmitigated enterprise technical risk exposure.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize software quality management system (QMS) processes and release verification checks."
            )
            impl_checklist.append("- [ ] Configure QMS quality assurance pipeline checks.")
            test_checklist.append("- [ ] Run automated quality gate and regression test suites.")
            doc_checklist.append("- [ ] Document QMS process audit procedures.")
            risk_assessment.append(f"- *{cat}*: Quality assurance failure and process audit non-conformance.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Implement IEC 62443 / IEC 62304 software lifecycle security and component isolation protocols."
            )
            impl_checklist.append("- [ ] Enforce IEC software lifecycle security controls and threat modeling.")
            test_checklist.append("- [ ] Verify software component isolation and functional safety bounds.")
            doc_checklist.append("- [ ] Update software lifecycle compliance records.")
            risk_assessment.append(f"- *{cat}*: Software lifecycle security and functional safety gaps.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align mobile and web codebases with OWASP Top 10 and MASVS security verification controls."
            )
            impl_checklist.append("- [ ] Sanitize input parsers and harden authentication storage according to OWASP MASVS.")
            test_checklist.append("- [ ] Execute OWASP MASVS security verification test suites.")
            doc_checklist.append("- [ ] Document OWASP security controls in developer guidelines.")
            risk_assessment.append(f"- *{cat}*: Vulnerability to OWASP Top 10 exploits and MASVS audit failures.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE trustworthy AI controls."
            )
            impl_checklist.append("- [ ] Integrate NIST AI RMF metrics for explainability, fairness, and safety.")
            test_checklist.append("- [ ] Run model red-teaming and bias measurement test suites.")
            doc_checklist.append("- [ ] Document NIST AI RMF safety evaluation benchmarks.")
            risk_assessment.append(f"- *{cat}*: Trustworthy AI failure and unmitigated model risk under NIST AI RMF.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Adopt NIST CSF 2.0 GOVERN function alongside Identify, Protect, Detect, Respond, and Recover."
            )
            impl_checklist.append("- [ ] Configure supply chain risk management and incident response controls.")
            test_checklist.append("- [ ] Test threat detection and automated incident response pipelines.")
            doc_checklist.append("- [ ] Update NIST CSF 2.0 governance and incident response playbooks.")
            risk_assessment.append(f"- *{cat}*: Cybersecurity framework non-alignment and delayed incident response.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Enforce CIS Benchmarks and CIS Controls for system, container, and network hardening."
            )
            impl_checklist.append("- [ ] Apply CIS hardening configurations across build and deployment targets.")
            test_checklist.append("- [ ] Execute CIS Benchmark compliance audit scanners.")
            doc_checklist.append("- [ ] Document CIS hardening configurations and baseline controls.")
            risk_assessment.append(f"- *{cat}*: Sub-optimal hardening configurations violating CIS baselines.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of standards compliance."
    test_checklist_str = "\n".join(test_checklist) if test_checklist else "- [ ] Run standard verification tests."
    doc_checklist_str = "\n".join(doc_checklist) if doc_checklist else "- [ ] Update technical standards documentation."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to bring the repository into complete compliance with monitored technical standards, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards establish international baselines for information security, privacy, artificial intelligence management, quality assurance, cybersecurity framework governance, and system hardening. Maintaining continuous compliance ensures enterprise integrity, audit readiness, and zero compliance gaps.

## 3. Regulatory change
- **ISO Standards (27001, 27701, 42001, 31000, 9001)**: Alignment with international information security, privacy, AI governance, enterprise risk management, and quality assurance standards.
- **IEC & OWASP Frameworks**: Adoption of software lifecycle security, component isolation, and OWASP Top 10 / MASVS verification controls.
- **NIST & CIS Guidelines**: Implementation of NIST AI RMF trustworthy AI functions, NIST CSF 2.0 governance, and CIS Benchmarks system hardening baselines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance audit failure or security vulnerability if technical standards are not continuously maintained and verified.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards controls and configuration baselines maintain full compatibility with existing systems and public API signatures.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Execute repository-wide static analysis and standards validation.

## 10. Testing checklist
{test_checklist_str}
- [ ] Run python3 scripts/validate.py to ensure configuration integrity.

## 11. Documentation checklist
{doc_checklist_str}
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.

## 12. Compliance impact
- **Audit Readiness**: Ensures total alignment with ISO, IEC, NIST, OWASP, and CIS technical standards.
- **Security Posture**: Strengthens system hardening, AI governance, and vulnerability mitigation.
- **Enterprise Integrity**: Provides verified evidence and audit trails for compliance stakeholders.

## 13. Breaking changes
- No functional breaking changes are introduced. Security and governance controls are enforced strictly within system configurations and build pipelines.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all citations originate from Priority 1-3 trusted sources.
- [ ] Verify that all standards gaps have corresponding implementation, testing, and documentation updates.

## 15. Approver recommendations
Verify that all technical standards controls pass static analysis verification before approving the compliance merge, and ensure that AI safety benchmarks and CIS hardening baselines are active in release targets.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Generates implementation tasks, documentation updates, and testing updates.
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

    processed_categories = set()

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)

        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority technical standards compliance area.")
        lines.append("- **Implementation Tasks**:")

        if cat == "ISO 27001":
            lines.append("  - [ ] **Task 1**: Update ISMS access control and logging configurations.")
            lines.append("  - [ ] **Task 2**: Conduct threat intelligence and cloud security posture audit.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Update ISMS policy documentation in docs/STANDARDS-POLICY-MIGRATION.md.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Execute access control and audit log verification tests.")
        elif cat == "ISO 27701":
            lines.append("  - [ ] **Task 1**: Implement PIMS PII controller and processor controls.")
            lines.append("  - [ ] **Task 2**: Configure automated data minimization workflows.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document PIMS controller/processor responsibilities and data flows.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Run automated privacy impact assessment tests.")
        elif cat == "ISO 42001":
            lines.append("  - [ ] **Task 1**: Implement AI Management System (AIMS) governance controls.")
            lines.append("  - [ ] **Task 2**: Generate AI model cards and bias mitigation pipelines.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document AIMS model cards and transparency guidelines.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Execute AI model red-teaming and safety evaluation suites.")
        elif cat == "ISO 31000":
            lines.append("  - [ ] **Task 1**: Align enterprise risk register with ISO 31000 principles.")
            lines.append("  - [ ] **Task 2**: Update risk treatment and mitigation workflows.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document ISO 31000 risk management procedures.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Validate risk matrix calculation and reporting scripts.")
        elif cat == "ISO 9001":
            lines.append("  - [ ] **Task 1**: Configure software Quality Management System (QMS) release controls.")
            lines.append("  - [ ] **Task 2**: Automate process audit checks in release pipelines.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document QMS software quality assurance protocols.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Execute QMS release gate and regression test suites.")
        elif cat == "IEC standards":
            lines.append("  - [ ] **Task 1**: Enforce IEC 62443 / IEC 62304 software lifecycle security controls.")
            lines.append("  - [ ] **Task 2**: Implement component isolation and threat modeling.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Update IEC software lifecycle compliance records.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Verify functional safety bounds and component isolation.")
        elif cat == "OWASP":
            lines.append("  - [ ] **Task 1**: Audit codebase against OWASP Top 10 and MASVS requirements.")
            lines.append("  - [ ] **Task 2**: Harden input sanitization and secure token storage.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document OWASP security controls in developer guidelines.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Run OWASP MASVS security verification test suites.")
        elif cat == "NIST AI RMF":
            lines.append("  - [ ] **Task 1**: Implement NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions.")
            lines.append("  - [ ] **Task 2**: Configure trustworthy AI metrics and bias controls.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document NIST AI RMF safety evaluation benchmarks.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Execute model red-teaming and trustworthy AI tests.")
        elif cat == "NIST CSF":
            lines.append("  - [ ] **Task 1**: Implement NIST CSF 2.0 GOVERN and supply chain risk controls.")
            lines.append("  - [ ] **Task 2**: Configure automated threat detection and incident response.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Update NIST CSF 2.0 governance and incident response playbooks.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Run incident response and threat detection tests.")
        elif cat == "CIS Benchmarks":
            lines.append("  - [ ] **Task 1**: Apply CIS Benchmarks system and container hardening configurations.")
            lines.append("  - [ ] **Task 2**: Disable unapproved legacy protocols and insecure transports.")
            lines.append("- **Documentation Updates**:")
            lines.append("  - [ ] **Doc 1**: Document CIS hardening configurations and baseline controls.")
            lines.append("- **Testing Updates**:")
            lines.append("  - [ ] **Test 1**: Run CIS Benchmark compliance audit scanners.")
        else:
            lines.append(f"  - [ ] **Task**: Verify that all technical standards criteria for {cat} are met.")
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
        print("Fetching live standards regulatory RSS feeds...")
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

    print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
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
