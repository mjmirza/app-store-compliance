#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards categories: ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
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
    "ISO 27001": ["iso 27001", "iso/iec 27001", "isms", "information security management system", "annex a"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "pims", "privacy information management system"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "aims", "artificial intelligence management system", "ai management system"],
    "ISO 31000": ["iso 31000", "risk management framework", "risk assessment framework", "risk treatment"],
    "ISO 9001": ["iso 9001", "quality management system", "qms", "quality assurance process"],
    "IEC standards": ["iec 62443", "iec 62304", "iec 82304", "iec standards", "electrotechnical standard"],
    "OWASP": ["owasp", "owasp top 10", "owasp mobile", "owasp api", "masvs", "mstg", "asvs"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "nist ai 100-1", "govern map measure manage"],
    "NIST CSF": ["nist csf", "nist csf 2.0", "cybersecurity framework", "nist sp 800-53", "nist sp 800-171"],
    "CIS Benchmarks": ["cis benchmarks", "cis controls", "center for internet security", "hardened configuration", "cis benchmark"]
}

# Codebase signals (regex patterns) to find repository gaps for each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"encryption_at_rest",
        r"incident_response"
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_policy",
        r"data_controller",
        r"data_processor",
        r"pii_inventory"
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"model_card",
        r"model_bias",
        r"ai_risk"
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_register",
        r"risk_assessment",
        r"risk_matrix",
        r"contingency_plan"
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_assurance",
        r"defect_tracking",
        r"audit_log"
    ],
    "IEC standards": [
        r"IEC62443",
        r"IEC62304",
        r"medical_device",
        r"industrial_control",
        r"functional_safety"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"xss_protection",
        r"csrf_protection",
        r"sqli_prevention"
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"ai_govern",
        r"ai_map",
        r"ai_measure",
        r"ai_manage"
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"NIST_800_53",
        r"cybersecurity_framework",
        r"identify_protect_detect"
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Controls",
        r"security_hardening",
        r"cis_compliance"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and government agencies (ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed journals",
    "Priority 4": "Industry blogs and vendor publications",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Information Security Management System Controls Update",
        "description": "ISO/IEC 27001 mandates updated Annex A controls including threat intelligence, information security for cloud services, ICT readiness for business continuity, and physical security monitoring.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 10 Aug 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management Extension Guidance",
        "description": "ISO/IEC 27701 extends ISO 27001 for privacy management (PIMS), requiring clear data mapping, data subject request workflows, and joint controller/processor contractual clauses.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 11 Aug 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Management System Standard",
        "description": "ISO/IEC 42001 specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) with rigorous risk controls for machine learning models.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 12 Aug 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines for Enterprise Systems",
        "description": "ISO 31000 provides principles and generic guidelines on enterprise risk management, emphasizing iterative risk identification, treatment plans, and continuous risk monitoring across digital assets.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 13 Aug 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management Systems Requirements Revisions",
        "description": "ISO 9001 mandates structured process control, risk-based thinking, defect monitoring, and continuous quality improvement in software engineering and deployment pipelines.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 14 Aug 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 62304 Cybersecurity and Software Lifecycle Standards",
        "description": "IEC standards mandate secure software lifecycle practices (IEC 62304) for healthcare applications and industrial automation cybersecurity (IEC 62443) with verified secure boot and patch mechanisms.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 15 Aug 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) v2.1",
        "description": "OWASP MASVS v2.1 establishes unified verification requirements for mobile security, covering data storage, cryptography, authentication, network communication, platform interaction, and resilience.",
        "link": "https://owasp.org/www-project-mobile-app-security/",
        "pubDate": "Sun, 16 Aug 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "NIST AI RMF provides structured guidelines across four core functions: Govern, Map, Measure, and Manage to foster trustworthy and responsible AI system deployment.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 17 Aug 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Implementation Update",
        "description": "NIST CSF 2.0 expands cybersecurity outcomes across six core functions: Govern, Identify, Protect, Detect, Respond, and Recover, requiring supply chain risk management and continuous control assessments.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 18 Aug 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks and Critical Security Controls v8.1 Guidelines",
        "description": "CIS Benchmarks provide prescriptive configuration baselines and hardened platform guidelines for mobile operating systems, server environments, and cloud infrastructure.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 19 Aug 2026 19:00:00 GMT"
    },
    # Unverified announcement to test blocking
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Tech Blog Rumor on ISO 27001 Certification Changes",
        "description": "An unverified personal blog claims ISO 27001 will discontinue audits next month. No official standards body or official source was cited.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 20 Aug 2026 20:00:00 GMT"
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
        "apple.com", "developer.apple.com", "android.com", "developer.android.com"
    ]
    p1_keywords = [
        "iso", "iec", "nist", "owasp", "cisecurity", "center for internet security",
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "cisa", "ico", "government publication", "imda", "pdpc"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "ieee.org", "acm.org"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

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
                    common_terms = {"iso", "nist", "owasp", "security", "privacy", "risk"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 standards categories.
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
    Generates a draft of a pull request complying strictly with the exact 15 required sections.
    Ensures complete absence of emojis or graphical unicode emoticons.
    """
    citations_list = []
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    processed_categories = set()

    for u in updates:
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
            migration_steps.append(f"- **{cat}**: Establish an Information Security Management System (ISMS) policy and configure Annex A controls for access control, encryption, and incident response.")
            impl_checklist.append("- [ ] Document ISMS policies and verify access control and encryption at rest.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit failure for enterprise security certifications.")
        elif cat == "ISO 27701":
            migration_steps.append(f"- **{cat}**: Extend the ISMS into a Privacy Information Management System (PIMS), mapping PII roles and data subject request mechanisms.")
            impl_checklist.append("- [ ] Create PII inventory and define data controller/processor operational workflows.")
            risk_assessment.append(f"- *{cat}*: Privacy management gaps leading to regulatory penalties under global privacy frameworks.")
        elif cat == "ISO 42001":
            migration_steps.append(f"- **{cat}**: Implement an Artificial Intelligence Management System (AIMS) with model cards, bias testing, and risk controls for generative AI components.")
            impl_checklist.append("- [ ] Create AI model cards and establish continuous model safety and bias evaluation tasks.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI model deployments causing compliance blocks under the EU AI Act and ISO standards.")
        elif cat == "ISO 31000":
            migration_steps.append(f"- **{cat}**: Formulate enterprise risk management registers and iterative risk assessment matrices across infrastructure assets.")
            impl_checklist.append("- [ ] Maintain centralized risk registers and update contingency plans.")
            risk_assessment.append(f"- *{cat}*: Unmitigated operational risks threatening service level agreements and data integrity.")
        elif cat == "ISO 9001":
            migration_steps.append(f"- **{cat}**: Formalize Quality Management System (QMS) processes, automated testing pipelines, and defect tracking protocols.")
            impl_checklist.append("- [ ] Configure automated regression testing and defect logging workflows.")
            risk_assessment.append(f"- *{cat}*: Inconsistent software quality and release delays due to unstandardized quality assurance.")
        elif cat == "IEC standards":
            migration_steps.append(f"- **{cat}**: Align software lifecycle practices with IEC 62304 and industrial/embedded security with IEC 62443 requirements.")
            impl_checklist.append("- [ ] Establish safe boot, patch management, and medical/industrial safety compliance checks.")
            risk_assessment.append(f"- *{cat}*: Safety critical system failure and regulatory non-compliance in specialized domains.")
        elif cat == "OWASP":
            migration_steps.append(f"- **{cat}**: Harden applications against OWASP Top 10 and OWASP Mobile MASVS recommendations including input sanitization and secure storage.")
            impl_checklist.append("- [ ] Run static analysis for XSS, SQLi, and insecure storage patterns.")
            risk_assessment.append(f"- *{cat}*: Vulnerability to exploitation, data exfiltration, and mobile platform rejections.")
        elif cat == "NIST AI RMF":
            migration_steps.append(f"- **{cat}**: Apply NIST AI Risk Management Framework functions (Govern, Map, Measure, Manage) to all machine learning pipelines.")
            impl_checklist.append("- [ ] Implement AI governance documentation and map risks across training and deployment phases.")
            risk_assessment.append(f"- *{cat}*: High risk of regulatory scrutiny regarding AI safety, fairness, and transparency.")
        elif cat == "NIST CSF":
            migration_steps.append(f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover).")
            impl_checklist.append("- [ ] Review asset management, threat detection logging, and incident response procedures.")
            risk_assessment.append(f"- *{cat}*: Increased exposure to security incidents and non-alignment with federal standards.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(f"- **{cat}**: Apply CIS Benchmark hardening guidelines to operating systems, containers, and deployment configurations.")
            impl_checklist.append("- [ ] Verify OS and container configurations against CIS benchmark recommendations.")
            risk_assessment.append(f"- *{cat}*: Security misconfigurations exposing infrastructure to automated exploitation.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Requirements Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to bring the repository into complete alignment with updated international technical standards and security frameworks. It addresses gaps identified across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Modern enterprise software deployments and mobile storefront ecosystems demand strict adherence to international security, quality, privacy, and risk management standards. Automated scanners and enterprise compliance audits evaluate software repositories for alignment with these industry benchmarks. This PR resolves identified gaps and establishes automated guardrails.

## 3. Regulatory change
- **ISO Security & Privacy Standards (27001, 27701, 42001, 31000, 9001)**: Mandates formal ISMS, PIMS, AIMS AI governance, risk registers, and quality management processes.
- **Engineering & Security Frameworks (IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)**: Enforces software lifecycle safety, OWASP Top 10 / MASVS hardening, NIST CSF 2.0 cybersecurity controls, and CIS OS/container hardening baselines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of enterprise audit failure or security vulnerability exposure if these technical standards controls are not satisfied.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standards updates introduce additive security controls, hardened configurations, and enhanced governance procedures without disrupting existing software features.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
- [ ] Verify that static analysis scans pass for OWASP MASVS security recommendations.
- [ ] Validate that AI model evaluation scripts pass for ISO 42001 and NIST AI RMF fairness/bias controls.
- [ ] Perform security logging verification against NIST CSF 2.0 detection requirements.
- [ ] Confirm CIS benchmark hardening scripts pass on deployment targets.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed actions.
- [ ] Document ISMS, PIMS, and AIMS policies in internal compliance playbooks.
- [ ] Confirm risk registers reflect current technical assets.

## 12. Compliance impact
- **Enterprise Certifications**: Ensures repository readiness for ISO 27001, ISO 27701, and ISO 42001 audits.
- **Cybersecurity Resilience**: Minimizes attack surfaces in accordance with OWASP, NIST CSF, and CIS Benchmarks.
- **AI Safety & Quality**: Establishes transparent AI management in line with NIST AI RMF and ISO 42001.

## 13. Breaking changes
- No functional breaking changes are introduced. Security hardening and compliance checks operate seamlessly alongside business logic.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that technical standards configurations meet specification requirements.

## 15. Approver recommendations
Verify that internal ISMS documentation matches the updated codebase controls before authorizing release tag creation, and ensure that all OWASP vulnerability scan findings are remediated.
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
        "# Technical Standards Compliance Requirements Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across 10 key technical standards categories.",
        "",
        "## Monitored Standards Update Log",
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

    lines.append("## Automated Implementation, Documentation, and Testing Tasks")
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
        lines.append("- **Regulatory Impact**: High priority technical standards area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Implementation Task**: Implement Annex A access controls and encryption at rest.")
            lines.append("- [ ] **Documentation Task**: Update ISMS policy documentation and incident response procedures.")
            lines.append("- [ ] **Testing Task**: Run security scans for access control enforcement.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Implementation Task**: Configure PIMS data controller/processor data flows.")
            lines.append("- [ ] **Documentation Task**: Document PII inventory and data subject rights procedures.")
            lines.append("- [ ] **Testing Task**: Verify PII extraction and deletion API endpoints.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Implementation Task**: Integrate AI model cards and bias monitoring safeguards.")
            lines.append("- [ ] **Documentation Task**: Update AIMS governance policies for generative components.")
            lines.append("- [ ] **Testing Task**: Run automated bias, toxicity, and model safety test suites.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Implementation Task**: Maintain centralized digital risk registers.")
            lines.append("- [ ] **Documentation Task**: Publish updated enterprise risk assessment guidelines.")
            lines.append("- [ ] **Testing Task**: Simulate disaster recovery and contingency failover scenarios.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Implementation Task**: Wire automated defect logging into CI/CD pipelines.")
            lines.append("- [ ] **Documentation Task**: Document QMS process standards and quality metrics.")
            lines.append("- [ ] **Testing Task**: Validate code coverage and continuous integration build gates.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Implementation Task**: Implement IEC 62304/62443 lifecycle and secure boot controls.")
            lines.append("- [ ] **Documentation Task**: Document safety-critical component architectures.")
            lines.append("- [ ] **Testing Task**: Conduct functional safety and patch management validation tests.")
        elif cat == "OWASP":
            lines.append("- [ ] **Implementation Task**: Enforce OWASP MASVS secure storage and transport controls.")
            lines.append("- [ ] **Documentation Task**: Maintain OWASP security compliance checklists.")
            lines.append("- [ ] **Testing Task**: Execute static and dynamic vulnerability scans for OWASP Top 10.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Implementation Task**: Integrate Govern, Map, Measure, Manage controls into ML pipelines.")
            lines.append("- [ ] **Documentation Task**: Create NIST AI RMF risk mapping documentation.")
            lines.append("- [ ] **Testing Task**: Execute model performance and fairness measurement benchmarks.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Implementation Task**: Implement NIST CSF 2.0 threat detection and response controls.")
            lines.append("- [ ] **Documentation Task**: Update cybersecurity response playbooks.")
            lines.append("- [ ] **Testing Task**: Audit security event logging and incident response triggers.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Implementation Task**: Apply CIS hardened configuration scripts to environment assets.")
            lines.append("- [ ] **Documentation Task**: Maintain CIS benchmark baseline documentation.")
            lines.append("- [ ] **Testing Task**: Run CIS compliance audit scripts against build images.")
        else:
            lines.append(f"- [ ] **Task**: Verify that technical requirements for {cat} are checked and handled.")
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

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print("Data. sample announcements built into this script, not live news.")
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
        print("Data. live feeds, fetched just now.")

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

    print(f"Scanning codebase under '{args.dir}' for standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock)

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
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
