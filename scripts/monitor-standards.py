#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks 10 key technical standards: ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF,
and CIS Benchmarks. Identifies repository gaps, generates implementation
tasks, documentation updates, and testing updates.
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
        "iso 27001", "iso/iec 27001", "isms", "information security management system",
        "annex a controls", "iso27001", "information security policy"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "pims", "privacy information management system",
        "pii controller", "pii processor", "privacy extension"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "aims", "artificial intelligence management system",
        "ai management system", "ai risk assessment", "ai impact assessment"
    ],
    "ISO 31000": [
        "iso 31000", "risk management guidelines", "risk assessment framework",
        "risk treatment", "risk evaluation", "iso31000"
    ],
    "ISO 9001": [
        "iso 9001", "qms", "quality management system", "quality policy",
        "quality control", "iso9001", "continuous improvement"
    ],
    "IEC standards": [
        "iec standards", "iec 62304", "iec 81001", "iec 62443", "iec 82304",
        "medical device software", "functional safety", "electrotechnical"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "masvs", "mastg", "asvs", "samm",
        "owasp api security", "mobile application security verification"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "nist ai",
        "trustworthy ai", "govern map measure manage", "nist.ai"
    ],
    "NIST CSF": [
        "nist csf", "nist csf 2.0", "cybersecurity framework", "identify protect detect",
        "csf core", "nist sp 800"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis controls", "cis hardened images", "center for internet security",
        "cis benchmark", "cis benchmark compliance"
    ]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"informationSecurity",
        r"accessControl",
        r"assetManagement",
        r"securityPolicy"
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacyInformation",
        r"PII",
        r"dataController",
        r"dataProcessor"
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"aiGovernance",
        r"algorithmicImpact",
        r"aiRiskAssessment",
        r"modelTransparency"
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"riskManagement",
        r"riskAssessment",
        r"riskEvaluation",
        r"riskTreatment",
        r"riskRegister"
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"qualityManagement",
        r"qualityPolicy",
        r"continuousImprovement",
        r"processControl"
    ],
    "IEC standards": [
        r"IEC[ -]?62304",
        r"IEC[ -]?81001",
        r"IEC[ -]?62443",
        r"IEC[ -]?82304",
        r"softwareLifecycle",
        r"functionalSafety"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MASTG",
        r"ASVS",
        r"SAMM",
        r"top10",
        r"apiSecurity"
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"trustworthyAI",
        r"aiGovern",
        r"aiMap",
        r"aiMeasure",
        r"aiManage"
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"cybersecurityFramework",
        r"identifyProtect",
        r"detectRespond",
        r"csf2",
        r"governanceCore"
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"cisHardening",
        r"cisControl",
        r"benchmarkCheck",
        r"securityBaseline"
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

# Mock Announcements covering all 10 Technical Standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 ISMS Update: Access Control and Threat Intelligence Controls",
        "description": "ISO/IEC 27001 mandates updated Annex A controls for information security management systems, emphasizing threat intelligence, cloud services security, physical security monitoring, and secure coding practices.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 PIMS Privacy Extension: Enforcing PII Controller and Processor Controls",
        "description": "ISO/IEC 27701 extends ISO 27001 for Privacy Information Management Systems (PIMS). Organizations must document explicit PII processing purposes, user consent records, and automated data subject request mechanisms.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AIMS: AI Management System Standard for Algorithmic Risk Governance",
        "description": "ISO/IEC 42001 establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS), focusing on AI risk management, system transparency, and data quality.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management: Updated Principles and Risk Assessment Guidelines",
        "description": "ISO 31000 guidelines mandate structured risk identification, risk evaluation, and risk treatment plans across technical repositories and operational pipelines.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 QMS Guidelines: Quality Management Systems in Software Engineering",
        "description": "ISO 9001 mandates continuous quality management, process control documentation, verification checklists, and audit trail maintenance across software release lifecycles.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62304 & IEC 81001-5-1 Health Software Security and Lifecycle Management",
        "description": "IEC health software standards enforce rigorous software lifecycle processes, risk management for health software, functional safety checks, and secure software development lifecycle (SDLC) controls.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS & MASTG Update: Mobile Application Security Verification Standard",
        "description": "OWASP publishes updated MASVS controls for network communication, storage security, cryptography, dynamic analysis resistance, and authentication enforcement across iOS and Android builds.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework: Govern, Map, Measure, Manage Core Update",
        "description": "NIST AI RMF specifies trustworthy AI characteristics including safety, security, resilience, explainability, privacy, and fairness across generative and predictive model deployments.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0: Integrating Governance and Continuous Auditing",
        "description": "NIST CSF 2.0 expands cybersecurity outcomes across Identify, Protect, Detect, Respond, Recover, and Governance functions, mandating automated security controls and supply chain risk management.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Hardening Standards: Container, OS, and Cloud Security Controls",
        "description": "CIS Benchmarks provide consensus-based best practice controls for hardening operating systems, cloud environments, containers, and web servers against unauthorized access and privilege escalation.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT"
    },
    # Unverified announcement to test Source Trust Hierarchy blocking
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Speculation on ISO 27001 Certification",
        "description": "A random industry blog claims ISO 27001 certification requires mandatory dark theme interfaces. This is an unverified industry blog post.",
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

    # Priority 1 official domains and keywords
    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "owasp.org", "cisecurity.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg"
    ]
    p1_keywords = [
        "iso standard", "iso/iec", "nist", "owasp", "cis benchmark",
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
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

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
        # Priority 4 or 5 must be verified by a Priority 1 official source reference
        has_p1_ref = any(d in combined for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in combined
        if has_p1_ref:
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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "privacy", "risk", "quality"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards.
    Returns matching files, line numbers, matched patterns, and contents.
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
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html",
                    ".yaml", ".yml", ".sh"
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
    testing_checklist = []

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
                f"- **{cat}**: Update Information Security Management System (ISMS) policies, access controls, and asset management declarations."
            )
            impl_checklist.append("- [ ] Audit Annex A controls and verify access control policy compliance.")
            risk_assessment.append(f"- *{cat}*: Non-compliance risks audit failure and loss of enterprise security certification.")
            testing_checklist.append("- [ ] Verify access control rules and confirm zero unauthorized access paths in integration tests.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Establish Privacy Information Management System (PIMS) controls for PII processing, user consent logs, and controller/processor requirements."
            )
            impl_checklist.append("- [ ] Map PII data flows and update controller/processor privacy agreements.")
            risk_assessment.append(f"- *{cat}*: Inadequate PII processing controls risk regulatory fines under global privacy laws.")
            testing_checklist.append("- [ ] Test automated PII deletion and export handlers for privacy subject requests.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement Artificial Intelligence Management System (AIMS) risk governance, model transparency disclosures, and algorithmic impact assessments."
            )
            impl_checklist.append("- [ ] Establish AI risk assessment framework and log model impact parameters.")
            risk_assessment.append(f"- *{cat}*: Unmonitored AI models present hallucination, bias, and regulatory non-compliance risks.")
            testing_checklist.append("- [ ] Run model output verification tests to confirm transparent disclosures on AI interactions.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Implement formal risk identification, evaluation, and treatment processes within technical development pipelines."
            )
            impl_checklist.append("- [ ] Maintain central risk register and assign risk treatment owners.")
            risk_assessment.append(f"- *{cat}*: Unhandled operational risks lead to security incidents and service disruptions.")
            testing_checklist.append("- [ ] Validate risk mitigation controls through automated boundary condition testing.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Document Quality Management System (QMS) software engineering processes, verification checklists, and audit trail records."
            )
            impl_checklist.append("- [ ] Implement automated build verification checklists and release quality gates.")
            risk_assessment.append(f"- *{cat}*: Process inconsistency increases defect rates and customer dissatisfaction.")
            testing_checklist.append("- [ ] Confirm CI test suite enforcement across all pull requests before merge authorization.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62304 / IEC 81001-5-1 software lifecycle security processes and functional safety verifications."
            )
            impl_checklist.append("- [ ] Conduct functional safety assessment and enforce secure software lifecycle gating.")
            risk_assessment.append(f"- *{cat}*: Safety-critical software flaws risk product recall and health software regulatory blocks.")
            testing_checklist.append("- [ ] Execute static code analysis and unit tests covering all safety-critical code paths.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align mobile and web components with OWASP MASVS, MASTG, ASVS, and Top 10 security verifications."
            )
            impl_checklist.append("- [ ] Run static security scans against OWASP MASVS/ASVS controls.")
            risk_assessment.append(f"- *{cat}*: Known OWASP vulnerabilities (injection, insecure storage, broken auth) expose applications to exploit.")
            testing_checklist.append("- [ ] Run automated vulnerability scanners and verify zero high/critical OWASP findings.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Integrate NIST AI RMF core functions (Govern, Map, Measure, Manage) across AI model deployments."
            )
            impl_checklist.append("- [ ] Document trustworthy AI metrics covering safety, explainability, and fairness.")
            risk_assessment.append(f"- *{cat}*: Non-alignment with NIST AI RMF increases exposure to algorithmic liability and federal scrutiny.")
            testing_checklist.append("- [ ] Execute bias, robustness, and safety evaluations on AI component inputs and outputs.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST Cybersecurity Framework 2.0 outcomes across Identify, Protect, Detect, Respond, Recover, and Govern functions."
            )
            impl_checklist.append("- [ ] Update cybersecurity risk management controls and supply chain verification.")
            risk_assessment.append(f"- *{cat}*: Gaps in threat detection or incident response increase breach detection latency.")
            testing_checklist.append("- [ ] Perform incident response simulation tests and verify security event logging pipelines.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply CIS Benchmark hardening controls for containers, operating systems, cloud environments, and configuration files."
            )
            impl_checklist.append("- [ ] Run CIS Benchmark compliance scripts against infrastructure and build configurations.")
            risk_assessment.append(f"- *{cat}*: Unhardened systems expose unnecessary attack surface and default configuration flaws.")
            testing_checklist.append("- [ ] Execute automated configuration audits to verify compliance with CIS hardened baselines.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"
    testing_checklist_str = "\n".join(testing_checklist) if testing_checklist else "- [ ] Execute regression test suite."

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request brings the repository into alignment with updated technical standards across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. It establishes verified security, privacy, quality, and governance controls.

## 2. Background
Technical standards provide globally recognized frameworks for cybersecurity, privacy, AI governance, quality management, and system hardening. Keeping technical implementations aligned with current international standards protects organizational assets and ensures compliance with enterprise procurement and certification criteria.

## 3. Regulatory change
- **ISO / IEC Frameworks**: Adoption of updated ISMS, PIMS, AIMS, QMS, and software lifecycle controls.
- **NIST & OWASP Security Baselines**: Alignment with NIST CSF 2.0, NIST AI RMF, and OWASP MASVS/ASVS controls.
- **CIS Hardening Guidelines**: Enforcement of CIS Benchmarks across build and operational configurations.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational and audit risk if technical controls fall out of alignment with international standards.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes maintain backward compatibility. Infrastructure configuration hardening and compliance checks do not break public application APIs or operational dependencies.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run repository-wide technical standards validation checks.

## 10. Testing checklist
{testing_checklist_str}

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation and testing tasks.
- [ ] Document technical controls in developer onboarding guidelines.

## 12. Compliance impact
- **Certification Readiness**: Ensures repository passes ISO 27001 / ISO 27701 / ISO 42001 audits.
- **Cybersecurity & AI Resilience**: Satisfies OWASP, NIST CSF, NIST AI RMF, and CIS Benchmark requirements.

## 13. Breaking changes
- Non-compliant configurations or unencrypted storage defaults are deprecated and removed.

## 14. Review checklist
- [ ] Verify diff is 100% emoji-free.
- [ ] Confirm official standards citations are verified.
- [ ] Verify test suite coverage across all modified security and governance paths.

## 15. Approver recommendations
Verify that all mandatory security and privacy controls are verified in CI/CD pipelines before merge.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Contains update logs, repository gap analysis, implementation tasks, and testing updates.
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

    lines.append("## Repository Gap Analysis")
    lines.append("")

    for cat in CATEGORIES:
        files = scan_results.get(cat, [])
        lines.append(f"### Gap Analysis for {cat}")
        if files:
            lines.append(f"- **Detected Code Signals**: {len(files)} match(es) found in codebase.")
            for f in files[:5]:  # Limit output
                lines.append(f"  - `{f['file']}` (Line {f['line_num']}): `{f['content']}`")
        else:
            lines.append(f"- **Detected Code Signals**: Zero matching signals found. Manual policy review required.")
        lines.append("")

    lines.append("## Actionable Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Source is unverified)")
            lines.append("- **Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Implementation Tasks for {cat}")
        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update ISMS access control policies and asset inventory.")
            lines.append("- [ ] **Task 2**: Implement threat intelligence monitoring controls.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Document PII controller and processor roles.")
            lines.append("- [ ] **Task 2**: Deploy privacy information management request handlers.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Conduct AI system risk assessment and log algorithmic impacts.")
            lines.append("- [ ] **Task 2**: Implement user interaction disclosures for AI subsystems.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Populate enterprise risk register and assign risk treatment owners.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Implement continuous quality management checks in software pipelines.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Audit software lifecycle safety and functional safety verifications.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Audit codebase against OWASP MASVS / ASVS verification controls.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Document Govern, Map, Measure, Manage functions for deployed AI models.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align security controls with NIST CSF 2.0 Governance and Protect functions.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Apply CIS hardened configuration baselines across containers and cloud settings.")
        else:
            lines.append(f"- [ ] **Task**: Verify compliance criteria for {cat}.")
        lines.append("")

    lines.append("## Automated Testing Updates")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            continue

        lines.append(f"### Testing Checklist for {cat}")
        lines.append(f"- [ ] **Test 1**: Verify functional test suite passes for all {cat} compliance controls.")
        lines.append(f"- [ ] **Test 2**: Run automated static analysis and confirm zero policy violations.")
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

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates "
        f"({blocked_updates_count} blocked due to source trust validation):"
    )
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
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
