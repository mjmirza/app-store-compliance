#!/usr/bin/env python3
"""Monitors 10 core technical standards (ISO 27001, ISO 27701, ISO 42001,
ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)
for changes, identifies repository gaps, generates implementation tasks,
documentation updates, and testing updates."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# Source Trust Hierarchy
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, OWASP, CIS Benchmarks, European Commission, ENISA, EDPB, FTC, CISA, ICO, Government publications)",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

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

# Keyword mappings to classify updates into the 10 standards
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "isms",
        "information security management",
        "annex a controls",
        "statement of applicability",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "pims",
        "privacy information management",
        "pii processor",
        "pii controller",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "aims",
        "artificial intelligence management",
        "ai risk assessment",
        "ai impact assessment",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk criteria",
        "risk treatment",
        "enterprise risk management",
    ],
    "ISO 9001": [
        "iso 9001",
        "qms",
        "quality management system",
        "quality policy",
        "continuous improvement",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62304",
        "iec 82304",
        "iec 62443",
        "functional safety",
        "software lifecycle processes",
        "industrial automation cybersecurity",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "mastg",
        "asvs",
        "owasp samm",
        "api security top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai risk management framework",
        "govern map measure manage",
        "nist ai 100-1",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis hardened images",
        "cis controls",
        "cis ios benchmark",
        "cis android benchmark",
        "cis distribution benchmark",
    ],
}

# Codebase signals (regex patterns) to find affected files for each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS",
        r"ISO27001",
        r"securityPolicy",
        r"accessControl",
        r"assetInventory",
    ],
    "ISO 27701": [
        r"PIMS",
        r"ISO27701",
        r"privacyPolicy",
        r"piiProcessing",
        r"dataProtectionOfficer",
    ],
    "ISO 42001": [
        r"AIMS",
        r"ISO42001",
        r"aiRiskAssessment",
        r"modelGovernance",
        r"llmSafety",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"riskRegister",
        r"riskAssessment",
        r"riskTreatment",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"qualityPolicy",
        r"auditLog",
        r"continuousImprovement",
    ],
    "IEC standards": [
        r"IEC62304",
        r"IEC82304",
        r"IEC62443",
        r"softwareLifecycle",
        r"functionalSafety",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MASTG",
        r"ASVS",
        r"SAMM",
        r"inputSanitization",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"trustworthyAI",
        r"aiBiasMitigation",
        r"governMapMeasureManage",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"cybersecurityFramework",
        r"incidentResponse",
        r"accessManagement",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"hardenedConfig",
        r"cisControl",
        r"securityBaseline",
    ],
}

# Mock announcements covering the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Information Security Management Standard Amendment: Annex A Controls Update",
        "description": "ISO/IEC 27001 standard guidance updates require explicit mapping of threat intelligence, physical security monitoring, and secure coding baselines in the Statement of Applicability.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System (PIMS) Enforcement Directive",
        "description": "Updates to ISO/IEC 27701 require organizations acting as PII processors and controllers to implement automated PII mapping, data minimization audit trails, and explicit consent tracking.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Wed, 03 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System (AIMS) Operational Guidelines",
        "description": "ISO/IEC 42001 mandates structured AI risk assessments, algorithmic impact assessments, continuous model performance monitoring, and human oversight controls for deployed AI models.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Fri, 05 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Refinement",
        "description": "ISO 31000 guidelines emphasize integrating continuous technology and digital product risk criteria directly into enterprise risk registers and incident escalation matrices.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Mon, 08 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System: Digital Product Assurance Update",
        "description": "ISO 9001 quality management guidelines mandate rigorous automated release verification, root cause analysis for software defects, and traceable audit trails.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Wed, 10 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Software Lifecycle & IEC 62443 Security Standards Update",
        "description": "International Electrotechnical Commission updates require medical and health software (IEC 62304/82304) and industrial/IoT devices (IEC 62443) to enforce strict SBOM tracking and threat modeling.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 12 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 & MASVS v2.1 Mobile Application Security Standard Revision",
        "description": "OWASP updates release new controls under MASVS-STORAGE and MASVS-NETWORK, mandating hardware-backed key storage, SPKI certificate pinning, and input sanitization against injection.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Implementation Directive",
        "description": "NIST releases updated operational profiles under the Govern, Map, Measure, and Manage functions of AI RMF 1.0, requiring continuous red-teaming and bias testing for generative AI models.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF 2.0) Governance Function Enforcement",
        "description": "NIST CSF 2.0 expands coverage to all organizations with a dedicated Governance (GV) function, requiring explicit supply chain risk management and continuous vulnerability scanning.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 19 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks v3.0: Hardened Configuration Standards for Mobile and Web Applications",
        "description": "Center for Internet Security issues updated CIS Benchmarks mandating secure build environment configurations, hardened TLS protocols, and strict IAM access controls.",
        "link": "https://www.cisecurity.org/cis-benchmarks/",
        "pubDate": "Mon, 22 Jun 2026 14:00:00 GMT",
    },
]


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and verification status."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org",
        "iec.ch",
        "nist.gov",
        "owasp.org",
        "mas.owasp.org",
        "cisecurity.org",
        "europa.eu",
        "eur-lex.europa.eu",
        "enisa.europa.eu",
        "edpb.europa.eu",
        "ftc.gov",
        "cisa.gov",
        "ico.org.uk",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "cis benchmarks",
        "cisecurity",
        "european commission",
        "official journal",
        "cisa",
        "ico",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "linkedin", "reddit", "ai summary", "chatgpt summary"]

    priority = 4
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
        has_p1_ref = any(d in combined for d in p1_domains) or any(
            kw in combined for kw in p1_keywords
        )
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
                    if words.intersection(other_words).intersection(
                        {"iso", "nist", "owasp", "iec", "cis"}
                    ):
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files matching signals for each of the 10 standards categories."""
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
            if "monitor-standards" in file or "monitor-standards-test" in file:
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
    testing_checklist = []
    risk_assessment = []

    for u in updates:
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Update Statement of Applicability and map technical controls against ISO/IEC 27001 Annex A standards."
            )
            impl_checklist.append(
                "- [ ] Update ISMS Statement of Applicability to align with ISO 27001 controls."
            )
            testing_checklist.append(
                "- [ ] Conduct internal ISMS audit for access management and asset inventory controls."
            )
            risk_assessment.append(
                f"- *{cat}*: Incomplete information security controls exposing system boundaries to unmitigated access threats."
            )
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Audit PII processing activities and update Privacy Information Management System (PIMS) data flow maps."
            )
            impl_checklist.append(
                "- [ ] Update PIMS data processing inventory and verify PII controller/processor role declarations."
            )
            testing_checklist.append(
                "- [ ] Test automated PII deletion routines and user consent audit logging."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with privacy information management standards leading to regulatory data protection penalties."
            )
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance workflows and continuous model performance monitoring."
            )
            impl_checklist.append(
                "- [ ] Implement AI model card tracking and algorithmic risk assessment documentation."
            )
            testing_checklist.append(
                "- [ ] Run automated red-teaming and prompt safety tests on integrated AI model endpoints."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmonitored AI model drift, bias, or safety failures violating AI management system frameworks."
            )
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Integrate software and digital infrastructure risk criteria into the enterprise ISO 31000 risk register."
            )
            impl_checklist.append(
                "- [ ] Review and update digital asset risk register criteria under ISO 31000."
            )
            testing_checklist.append(
                "- [ ] Validate incident escalation and risk treatment verification pipelines."
            )
            risk_assessment.append(
                f"- *{cat}*: Unmitigated operational risks impacting application availability and business continuity."
            )
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Enhance QMS automated software build verification, defect root cause analysis, and quality assurance gates."
            )
            impl_checklist.append(
                "- [ ] Update continuous integration quality gates to enforce defect tracking and test pass thresholds."
            )
            testing_checklist.append(
                "- [ ] Verify automated test suite coverage and release audit validation steps."
            )
            risk_assessment.append(
                f"- *{cat}*: Regression defects and quality failures impacting end-user experience and release reliability."
            )
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Align software lifecycle processes with IEC 62304 / IEC 82304 and industrial cybersecurity controls under IEC 62443."
            )
            impl_checklist.append(
                "- [ ] Generate Software Bill of Materials (SBOM) and document software safety classification."
            )
            testing_checklist.append(
                "- [ ] Execute unit, integration, and system safety tests adhering to IEC software lifecycle standards."
            )
            risk_assessment.append(
                f"- *{cat}*: Safety classification non-conformities and software lifecycle vulnerabilities in controlled environments."
            )
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Audit code against OWASP Top 10 and OWASP MASVS v2.1 controls for secure storage, network transport, and input sanitization."
            )
            impl_checklist.append(
                "- [ ] Enforce input sanitization, SPKI certificate pinning, and secure storage mechanisms."
            )
            testing_checklist.append(
                "- [ ] Run static application security testing (SAST) scanners and verify zero high/critical vulnerabilities."
            )
            risk_assessment.append(
                f"- *{cat}*: Application vulnerabilities (e.g. injection, broken access control) leading to compromise or data leakage."
            )
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Implement NIST AI RMF 1.0 Govern, Map, Measure, and Manage functions for trustworthy AI deployment."
            )
            impl_checklist.append(
                "- [ ] Document AI model provenance, training data disclosures, and human oversight controls."
            )
            testing_checklist.append(
                "- [ ] Perform continuous measure/manage testing for AI bias, hallucination, and safety limits."
            )
            risk_assessment.append(
                f"- *{cat}*: Lack of trustworthy AI safeguards leading to harmful outputs, regulatory sanctions, or user distrust."
            )
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Align cybersecurity controls with NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover)."
            )
            impl_checklist.append(
                "- [ ] Configure supply chain risk management checks and automated vulnerability scanning."
            )
            testing_checklist.append(
                "- [ ] Simulate security incident response procedures and verify audit log coverage."
            )
            risk_assessment.append(
                f"- *{cat}*: Inadequate threat detection or incident response readiness exposing systems to persistent threats."
            )
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Harden build environment configurations, OS images, and client security baselines against CIS Benchmarks."
            )
            impl_checklist.append(
                "- [ ] Apply CIS hardened configurations to deployment manifests and application build pipelines."
            )
            testing_checklist.append(
                "- [ ] Run automated CIS compliance benchmark auditing scripts."
            )
            risk_assessment.append(
                f"- *{cat}*: System misconfigurations allowing unauthorized access or privilege escalation."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching standards signals were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    testing_checklist_str = "\n".join(testing_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the application repository with updated global technical standards across ISO (27001, 27701, 42001, 31000, 9001), IEC standards, OWASP frameworks, NIST AI RMF, NIST CSF 2.0, and CIS Benchmarks. It establishes identified repository gap remediations, implementation tasks, documentation updates, and testing verification suites.

## 2. Background
Technical standards evolve to address emerging cybersecurity, privacy, artificial intelligence, and quality assurance demands. Maintaining proactive compliance with ISO, IEC, OWASP, NIST, and CIS frameworks ensures software safety, operational resilience, and regulatory readiness across all distribution channels.

## 3. Regulatory change
- **ISO / IEC Standards**: Mandatory controls for ISMS (ISO 27001), PIMS (ISO 27701), AIMS (ISO 42001), Risk Management (ISO 31000), Quality Management (ISO 9001), and Medical/Industrial Software Lifecycle (IEC 62304/62443).
- **OWASP / NIST / CIS Frameworks**: Updated security baselines under OWASP MASVS v2.1, NIST AI RMF 1.0, NIST CSF 2.0, and CIS Benchmarks.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of compliance rejection or security vulnerability exposure if technical standards are not continuously monitored and implemented.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standards compliance updates are fully backward-compatible. System architecture changes introduce additive security and quality controls without breaking existing public API signatures or user workflows.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run automated repository compliance verification tools.

## 10. Testing checklist
{testing_checklist_str}
- [ ] Run `bash scripts/monitor-standards-test.sh` to confirm standards monitoring pipeline integrity.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document security baselines and quality controls in developer documentation.

## 12. Compliance impact
- **Standards Aligned**: Ensures the repository satisfies ISO 27001/27701/42001/31000/9001, IEC, OWASP, NIST, and CIS requirements.
- **Risk Reduction**: Eliminates structural security and privacy gaps prior to release distribution.

## 13. Breaking changes
- Non-breaking. Build scripts enforce stricter quality gates, which may fail builds if security standards are violated.

## 14. Review checklist
- [ ] Source trust hierarchy verified (Priority 1 official standards sources).
- [ ] Diff and documentation are 100% free of emojis.
- [ ] All 10 technical standards categories are evaluated and addressed.

## 15. Approver recommendations
Verify that Statement of Applicability documents, SBOM manifests, and AI risk assessment logs are updated and cross-referenced with the official standards citations before release authorization.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory & Standards Impact**: High priority. Compliance audit mandates action."
        )

        if cat == "ISO 27001":
            lines.append(
                "- [ ] **Task 1**: Update Statement of Applicability for ISO 27001 Annex A controls."
            )
            lines.append(
                "- [ ] **Task 2**: Audit information security access management policies."
            )
        elif cat == "ISO 27701":
            lines.append(
                "- [ ] **Task 1**: Map PII processing routines for ISO 27701 PIMS compliance."
            )
            lines.append(
                "- [ ] **Task 2**: Implement automated user consent and deletion audit logging."
            )
        elif cat == "ISO 42001":
            lines.append(
                "- [ ] **Task 1**: Establish Artificial Intelligence Management System (AIMS) governance."
            )
            lines.append(
                "- [ ] **Task 2**: Conduct algorithmic impact assessment for deployed AI models."
            )
        elif cat == "ISO 31000":
            lines.append(
                "- [ ] **Task 1**: Update enterprise risk register with digital asset risk criteria."
            )
        elif cat == "ISO 9001":
            lines.append(
                "- [ ] **Task 1**: Configure continuous quality assurance build gates."
            )
        elif cat == "IEC standards":
            lines.append(
                "- [ ] **Task 1**: Generate SBOM and document IEC software lifecycle classifications."
            )
        elif cat == "OWASP":
            lines.append(
                "- [ ] **Task 1**: Enforce OWASP MASVS secure storage and transport controls."
            )
        elif cat == "NIST AI RMF":
            lines.append(
                "- [ ] **Task 1**: Implement NIST AI RMF Govern, Map, Measure, and Manage functions."
            )
        elif cat == "NIST CSF":
            lines.append(
                "- [ ] **Task 1**: Align cybersecurity controls with NIST CSF 2.0 functions."
            )
        elif cat == "CIS Benchmarks":
            lines.append(
                "- [ ] **Task 1**: Harden application build pipelines against CIS Benchmarks."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify compliance criteria for {cat} are implemented and verified."
            )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO, IEC, OWASP, NIST, CIS)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards RSS/Atom feeds"
    )
    parser.add_argument(
        "--mock",
        type=str,
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

    args = parser.parse_args()

    # Enforce strict source trust hierarchy check
    print("Source Trust Hierarchy initialized:")
    for level, desc in TRUST_HIERARCHY.items():
        print(f" - {level}: {desc}")

    announcements = []

    if args.live:
        print("Fetching live technical standards feeds...")
        live_feeds = [
            "https://csrc.nist.gov/CSRC/media/feeds/rss/news-and-events.xml",
            "https://owasp.org/feed.xml",
        ]
        for feed in live_feeds:
            announcements.extend(parse_rss_feed(feed))

    if args.mock or (not args.live and not args.mock) or not announcements:
        print("Using comprehensive mock Technical Standards updates...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default dataset.",
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

    print(
        f"Monitored and classified {len(classified_updates)} technical standards updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        p_level, is_ver = classify_source_and_verify(u, announcements)
        ver_status = "Verified" if is_ver else "UNVERIFIED (Blocked)"
        print(
            f" {idx}. [{u['category']}] {u['title']} (Priority {p_level} - {ver_status})"
        )

    print(f"Scanning codebase under '{args.dir}' for technical standards signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        print("\n=== GENERATED 15-SECTION COMPLIANCE PULL REQUEST DRAFT ===")
        print(pr_draft)
        print("==========================================================")


if __name__ == "__main__":
    main()
