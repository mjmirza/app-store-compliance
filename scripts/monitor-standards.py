#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks changes across 10 key technical standards:
1. ISO 27001
2. ISO 27701
3. ISO 42001
4. ISO 31000
5. ISO 9001
6. IEC standards
7. OWASP
8. NIST AI RMF
9. NIST CSF
10. CIS Benchmarks
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

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

CATEGORY_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso27001", "information security management", "isms", "27001:2022", "iso/iec 27001"],
    "ISO 27701": ["iso 27701", "iso27701", "privacy information management", "pims", "27701:2019", "iso/iec 27701"],
    "ISO 42001": ["iso 42001", "iso42001", "artificial intelligence management system", "aims", "42001:2023", "iso/iec 42001"],
    "ISO 31000": ["iso 31000", "iso31000", "risk management guidelines", "31000:2018", "risk management framework"],
    "ISO 9001": ["iso 9001", "iso9001", "quality management system", "qms", "9001:2015"],
    "IEC standards": ["iec standard", "iec 62304", "iec 81001", "iec 62443", "iec 62304:2006", "iec"],
    "OWASP": ["owasp", "owasp top 10", "owasp mobile top 10", "owasp masvs", "owasp mstg", "owasp asvs", "masvs"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "nist ai 100", "nist ai"],
    "NIST CSF": ["nist csf", "nist cybersecurity framework", "nist csf 2.0", "nist sp 800-53", "nist sp 800"],
    "CIS Benchmarks": ["cis benchmarks", "center for internet security", "cis benchmark", "cis controls", "cis benchmark v8"]
}

CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"iso27001",
        r"iso[ -_]?27001",
        r"isms",
        r"information security management system"
    ],
    "ISO 27701": [
        r"iso27701",
        r"iso[ -_]?27701",
        r"pims",
        r"privacy information management system"
    ],
    "ISO 42001": [
        r"iso42001",
        r"iso[ -_]?42001",
        r"aims",
        r"ai management system"
    ],
    "ISO 31000": [
        r"iso31000",
        r"iso[ -_]?31000",
        r"risk management framework",
        r"risk matrix"
    ],
    "ISO 9001": [
        r"iso9001",
        r"iso[ -_]?9001",
        r"qms",
        r"quality management system"
    ],
    "IEC standards": [
        r"iec[ -_]?62304",
        r"iec[ -_]?81001",
        r"iec[ -_]?62443",
        r"iec[ -_]?standards?"
    ],
    "OWASP": [
        r"owasp",
        r"masvs",
        r"mstg",
        r"asvs",
        r"owasp top 10"
    ],
    "NIST AI RMF": [
        r"nist[ -_]?ai[ -_]?rmf",
        r"ai risk management framework",
        r"nist[ -_]?ai"
    ],
    "NIST CSF": [
        r"nist[ -_]?csf",
        r"cybersecurity framework",
        r"nist[ -_]?sp[ -_]?800"
    ],
    "CIS Benchmarks": [
        r"cis[ -_]?benchmarks?",
        r"cis[ -_]?controls",
        r"center for internet security"
    ]
}

TRUST_HIERARCHY = {
    "Priority 1": "Official standards organizations & government agencies (ISO, IEC, NIST, CIS, OWASP, European Commission, FTC, ENISA, CISA, ICO)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Annex A Control Alignment Updates",
        "description": "ISO releases updated Annex A control guidance requiring enhanced threat intelligence, cloud services security, and secure coding practices across all certified Information Security Management Systems.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 18 May 2026 09:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements",
        "description": "ISO/IEC 27701 update specifies enhanced PIMS controls for PII controllers and processors, reinforcing data subject consent tracking and cross-border transfer controls.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 19 May 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Management System Standard Enforcement",
        "description": "ISO/IEC 42001 requirements specify mandatory governance, transparency, and risk impact assessments for organizations developing or deploying artificial intelligence systems.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 20 May 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Standard Refinement",
        "description": "ISO 31000 guidelines update provides structured methodologies for integrated cybersecurity, technological, and operational risk assessment matrices.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 21 May 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Software Quality Process Alignment",
        "description": "ISO 9001 QMS guidance updates emphasize continuous software release quality gates, automated regression testing, and customer satisfaction metrics.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 22 May 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 81001 Health Software Lifecycle and Cybersecurity Requirements",
        "description": "IEC releases updated guidance for software lifecycle processes (IEC 62304) and health software security (IEC 81001-5-1), mandating secure development lifecycles.",
        "link": "https://www.iec.ch/standards/62304",
        "pubDate": "Sat, 23 May 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS v2.1 and Mobile Top 10 Security Verification Standards",
        "description": "OWASP releases updated Mobile Application Security Verification Standard (MASVS v2.1) establishing baseline security controls for storage, crypto, auth, and network communication.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 24 May 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Profile Implementation Guidance",
        "description": "NIST publishes actionable profiles under NIST AI RMF 1.0, establishing GOVERN, MAP, MEASURE, and MANAGE functions for trustful and safe AI system deployment.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 25 May 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Governance and Supply Chain Security",
        "description": "NIST CSF 2.0 expands coverage with the GOVERN function, emphasizing supply chain risk management, continuous monitoring, and incident response readiness.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 26 May 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls v8.1 and Mobile Device Security Benchmarks",
        "description": "Center for Internet Security (CIS) releases CIS Controls v8.1 and updated mobile OS benchmarks requiring strict secure baseline configurations.",
        "link": "https://www.cisecurity.org/benchmark",
        "pubDate": "Wed, 27 May 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Rumor on ISO 27001 Mandatory Quantum Encryption",
        "description": "An unverified industry blog claims ISO 27001 will require quantum encryption for all mobile apps next week. This is an unverified industry blog rumor.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 28 May 2026 19:00:00 GMT"
    }
]


def classify_source_and_verify(announcement, all_announcements=None):
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "cisecurity.org", "owasp.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk"
    ]
    p1_keywords = [
        "iso", "iec", "nist", "cis controls", "owasp", "european commission",
        "official journal", "enisa", "edpb", "ftc", "cisa", "ico", "government publication"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

    priority = 4

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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "privacy", "risk"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
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
    citations_list = []
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    testing_checklist = []
    risk_assessment = []
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
            migration_steps.append("- **ISO 27001**: Align information security management policies, access control rules, and secure coding practices with Annex A controls.")
            impl_checklist.append("- [ ] Audit Information Security Management System (ISMS) controls against ISO 27001 Annex A.")
            testing_checklist.append("- [ ] Conduct vulnerability scanning and static code analysis for ISO 27001 compliance.")
            risk_assessment.append("- *ISO 27001*: Non-compliance risks failure of security audits and certification loss.")
        elif cat == "ISO 27701":
            migration_steps.append("- **ISO 27701**: Extend ISMS controls to Privacy Information Management System (PIMS) for PII controller/processor roles.")
            impl_checklist.append("- [ ] Maintain PII processing inventories and document consent management controls.")
            testing_checklist.append("- [ ] Verify automated PII deletion and consent validation test suites.")
            risk_assessment.append("- *ISO 27701*: Inadequate PIMS controls increase regulatory privacy penalty exposure.")
        elif cat == "ISO 42001":
            migration_steps.append("- **ISO 42001**: Establish Artificial Intelligence Management System (AIMS) governance, risk assessment, and transparency measures.")
            impl_checklist.append("- [ ] Implement AI model risk assessments and transparent system disclosures.")
            testing_checklist.append("- [ ] Run prompt injection, hallucination, and AI model boundary testing.")
            risk_assessment.append("- *ISO 42001*: AI management non-compliance violates emerging global AI governance standards.")
        elif cat == "ISO 31000":
            migration_steps.append("- **ISO 31000**: Reconcile enterprise risk management framework matrices and risk evaluation criteria.")
            impl_checklist.append("- [ ] Update enterprise risk matrices to incorporate cyber and software supply chain risks.")
            testing_checklist.append("- [ ] Validate risk threshold evaluations during release review simulations.")
            risk_assessment.append("- *ISO 31000*: Unmitigated risk exposures lead to unexpected operational disruptions.")
        elif cat == "ISO 9001":
            migration_steps.append("- **ISO 9001**: Update Quality Management System (QMS) software quality gates and automated CI testing pipelines.")
            impl_checklist.append("- [ ] Integrate QMS automated quality gates into release workflows.")
            testing_checklist.append("- [ ] Run automated end-to-end regression test suites for zero-defect verification.")
            risk_assessment.append("- *ISO 9001*: Quality process gaps lead to software regressions and compliance audit failures.")
        elif cat == "IEC standards":
            migration_steps.append("- **IEC standards**: Apply IEC 62304 software lifecycle processes and IEC 81001-5-1 health software cybersecurity controls.")
            impl_checklist.append("- [ ] Document software lifecycle classification and cybersecurity controls under IEC standards.")
            testing_checklist.append("- [ ] Execute static code verification and safety-critical unit tests.")
            risk_assessment.append("- *IEC standards*: Non-compliance halts deployment in healthcare and safety-regulated sectors.")
        elif cat == "OWASP":
            migration_steps.append("- **OWASP**: Implement OWASP MASVS (Mobile Application Security Verification Standard) and OWASP Top 10 controls.")
            impl_checklist.append("- [ ] Audit mobile binary against OWASP MASVS storage, network, and crypto requirements.")
            testing_checklist.append("- [ ] Run OWASP ZAP and dynamic penetration testing suites.")
            risk_assessment.append("- *OWASP*: OWASP security gaps expose mobile and web applications to exploitation.")
        elif cat == "NIST AI RMF":
            migration_steps.append("- **NIST AI RMF**: Deploy GOVERN, MAP, MEASURE, and MANAGE functions for AI risk management.")
            impl_checklist.append("- [ ] Complete NIST AI RMF profile documentation for generative AI components.")
            testing_checklist.append("- [ ] Test AI model outputs for safety, bias, and unexpected behavior.")
            risk_assessment.append("- *NIST AI RMF*: Absence of AI risk management breaches federal and enterprise guidelines.")
        elif cat == "NIST CSF":
            migration_steps.append("- **NIST CSF**: Integrate NIST Cybersecurity Framework 2.0 GOVERN function and supply chain risk management.")
            impl_checklist.append("- [ ] Verify Software Bill of Materials (SBOM) generation and supply chain scanning.")
            testing_checklist.append("- [ ] Run dependency vulnerability scanners (e.g. OWASP Dependency-Check).")
            risk_assessment.append("- *NIST CSF*: Supply chain and governance gaps expose repository to zero-day vulnerabilities.")
        elif cat == "CIS Benchmarks":
            migration_steps.append("- **CIS Benchmarks**: Enforce CIS Controls v8 and mobile OS secure baseline configurations.")
            impl_checklist.append("- [ ] Validate OS level baseline security configurations against CIS Benchmarks.")
            testing_checklist.append("- [ ] Execute automated CIS configuration compliance checks.")
            risk_assessment.append("- *CIS Benchmarks*: Deviations from CIS Benchmarks leave underlying OS configurations vulnerable.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Run standard unit and integration test suites."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and procedural modifications to align the codebase with modern technical standards including ISO, IEC, OWASP, NIST, and CIS frameworks.

## 2. Background
Compliance with recognized international technical standards is essential to guarantee information security, quality management, risk governance, AI trustworthiness, and mobile application security. This PR addresses identified gaps across the 10 monitored technical standards categories.

## 3. Regulatory change
- **ISO Standards (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001)**: Annex A controls, PIMS privacy rules, AIMS AI governance, risk management frameworks, and QMS quality gates.
- **IEC & OWASP**: Health software lifecycle controls (IEC 62304 / IEC 81001) and mobile security verification (OWASP MASVS / Top 10).
- **NIST & CIS**: NIST AI RMF 1.0 profiles, NIST CSF 2.0 governance/supply chain security, and CIS Controls v8 benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to High risk of audit failure or security exposure if technical standards requirements are unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. No breaking API changes or schema disruptions are introduced to existing consumer systems.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run automated compliance guard scripts.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run full automated test suites to ensure zero regressions.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed compliance milestones.
- [ ] Confirm internal risk matrices and governance policies reflect updated standards.

## 12. Compliance impact
- **Audit Preparedness**: Elevates organizational readiness for external ISO, NIST, and OWASP compliance audits.
- **Security & Quality**: Ensures robust software quality, supply chain integrity, and AI safety.

## 13. Breaking changes
- Zero breaking API or interface changes.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that official citations originate from trusted Priority 1-3 sources.
- [ ] Verify that all implementation and testing tasks are complete.

## 15. Approver recommendations
Verify that SBOM pipeline checks pass and confirm that ISO 27001 / ISO 42001 governance controls are documented before authorizing release.
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


def update_documentation_report(updates, output_filepath, is_simulated=False, scan_results=None):
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Requirements Migration & Gap Analysis Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across key technical standards.",
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

    lines.append("## Identified Repository Gaps & Tasks")
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
        lines.append("- **Standards Classification**: High priority technical standards domain.")

        matches = scan_results.get(cat, []) if scan_results else []
        if matches:
            lines.append(f"- **Repository Gap Analysis**: Found {len(matches)} signal match(es) in codebase.")
        else:
            lines.append("- **Repository Gap Analysis**: No active signal matched in code. Controls must be implemented.")

        lines.append("#### Implementation Tasks")
        lines.append(f"- [ ] **Task 1**: Review and update configuration controls for {cat}.")
        lines.append(f"- [ ] **Task 2**: Establish policy compliance controls for {cat}.")

        lines.append("#### Testing Updates")
        lines.append(f"- [ ] **Test Task 1**: Add automated unit and integration tests verifying {cat} controls.")
        lines.append(f"- [ ] **Test Task 2**: Conduct compliance regression checks for {cat}.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO, IEC, OWASP, NIST, CIS)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards feeds"
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

    # Log printer that redirects to stderr if --json is active
    def log(msg):
        if args.json:
            print(msg, file=sys.stderr)
        else:
            print(msg)

    announcements = []

    if args.live:
        log("Fetching live technical standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        log("Data. sample announcements built into this script, not live news.")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                log(f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.")
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        log("Data. live feeds, fetched just now.")

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        log("No classified updates matched the current filters.")
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

    log(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        log(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    log(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    log(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        if update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock, scan_results=scan_results):
            log(f"Technical standards documentation report updated successfully at: {args.output_docs}")
    else:
        log("No file written. Pass --output-docs <path> to save this report.")

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            log(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            log(f"Failed to write PR draft to {args.pr_output}: {e}")
    else:
        log("No PR draft written. Pass --pr-output <path> to save it.")

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
