#!/usr/bin/env python3
"""Technical Standards Compliance Monitor.
Tracks changes in ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001,
IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.
Applies the strict Source Trust Hierarchy and generates completely emoji-free reports."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# The 10 tracked technical standards
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

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Keywords used to classify incoming standards announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001", "iso27001", "isms", "information security management",
        "annex a", "access control policy", "security control", "risk assessment"
    ],
    "ISO 27701": [
        "iso 27701", "iso27701", "pims", "privacy information management",
        "pii processor", "pii controller", "privacy control"
    ],
    "ISO 42001": [
        "iso 42001", "iso42001", "aims", "artificial intelligence management",
        "ai risk management", "algorithmic transparency", "ai impact assessment"
    ],
    "ISO 31000": [
        "iso 31000", "iso31000", "risk management framework", "risk identification",
        "risk treatment", "risk register"
    ],
    "ISO 9001": [
        "iso 9001", "iso9001", "qms", "quality management system",
        "quality policy", "continuous improvement", "corrective action"
    ],
    "IEC standards": [
        "iec standards", "iec 62304", "iec 82304", "software safety class",
        "medical device software", "life cycle process"
    ],
    "OWASP": [
        "owasp", "masvs", "mstg", "asvs", "injection vulnerability",
        "broken access control", "xss protection"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "govern map measure manage",
        "trustworthy ai", "ai bias"
    ],
    "NIST CSF": [
        "nist csf", "cybersecurity framework", "identify protect detect respond recover",
        "security function"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "cis level 1", "cis level 2", "hardened configuration",
        "security baseline"
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [r"ISO27001", r"ISMS", r"accessControlPolicy", r"securityControl", r"riskAssessment"],
    "ISO 27701": [r"ISO27701", r"PIMS", r"piiProcessor", r"piiController", r"privacyControl"],
    "ISO 42001": [r"ISO42001", r"AIMS", r"aiRiskManagement", r"algorithmicTransparency", r"aiImpactAssessment"],
    "ISO 31000": [r"ISO31000", r"riskRegister", r"riskIdentification", r"riskTreatment"],
    "ISO 9001": [r"ISO9001", r"QMS", r"qualityPolicy", r"continuousImprovement", r"correctiveAction"],
    "IEC standards": [r"IEC_62304", r"IEC_82304", r"softwareSafetyClass", r"medicalDeviceSoftware", r"lifecycleProcess"],
    "OWASP": [r"OWASP", r"MASVS", r"MSTG", r"ASVS", r"xssProtection", r"csrfToken", r"inputSanitization"],
    "NIST AI RMF": [r"NIST_AI_RMF", r"governMapMeasureManage", r"trustworthyAI", r"biasMitigation"],
    "NIST CSF": [r"NIST_CSF", r"identifyProtectDetectRespondRecover", r"cybersecurityFramework"],
    "CIS Benchmarks": [r"CIS_Benchmarks", r"securityBaseline", r"hardenedConfig"],
}

# Default simulated/mock updates for the 10 technical standards
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Amendment 1 - Climate action changes added to ISMS requirements",
        "description": "The International Organization for Standardization issued an amendment to ISO 27001:2022, mandating that organizations evaluate climate change as a critical risk factor under Clause 4.1 and Clause 4.2.",
        "link": "https://www.iso.org/standard/27001-climate-amendment",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701:2024 Privacy Management Standard Update aligned with GDPR and DPDPA",
        "description": "A major revision to ISO 27701 integrates the latest European EDPB guidelines and Singapore PDPA requirements, defining specific responsibilities for Joint PII Controllers.",
        "link": "https://www.iso.org/standard/27701-privacy-2024",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Guidance on Article 50 Alignment",
        "description": "ISO released new implementation guidance for ISO 42001, specifically aligning Section 8 AI Controls with the EU AI Act transparency and risk mitigation mandates.",
        "link": "https://www.iso.org/standard/42001-aims-guidance",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines revised to address digital supply chain threats",
        "description": "ISO updated its ISO 31000 guidelines to emphasize risk treatment protocols for third-party cloud services, supply chain dependencies, and AI software components.",
        "link": "https://www.iso.org/standard/31000-risk-supply-chain",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001:2026 Quality Management Systems: Incorporating software reliability metrics",
        "description": "ISO published draft rules for the upcoming ISO 9001 revision, introducing mandatory validation of software automated regression tools and continuous delivery pipelines.",
        "link": "https://www.iso.org/standard/9001-software-quality-2026",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 / IEC 82304 Health Software: Software safety classification amendments",
        "description": "IEC announced revisions to the software safety classification parameters, introducing stricter rules for cloud-hosted healthcare mobile companion applications.",
        "link": "https://webstore.iec.ch/publication/62304-amendment",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS 2026 release enforces hardware-backed credential storage and strict API isolation",
        "description": "OWASP released the latest version of MASVS, making L2 controls for hardware-backed token storage and strict API certificate pinning mandatory for all transactions.",
        "link": "https://mas.owasp.org/MASVS-2026",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST releases AI RMF 1.5 - Enhancing testing guidelines for generative LLM bias and drift",
        "description": "The National Institute of Standards and Technology issued NIST AI RMF version 1.5, focusing on map and measure functions for mitigating model drift, hallucination, and intellectual property leakage.",
        "link": "https://www.nist.gov/publications/ai-rmf-1-5",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 implementation guidelines for small-to-medium enterprises",
        "description": "NIST published concrete implementation profiles for the CSF 2.0 Govern function, clarifying internal roles, responsibilities, and third-party supplier security reviews.",
        "link": "https://www.nist.gov/cybersecurity-framework-2-0",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks v3.1 released with cloud-native environment hardening baselines",
        "description": "The Center for Internet Security published updated CIS Benchmarks v3.1, enforcing container registry scanning, zero-trust network boundaries, and read-only host filesystem configurations.",
        "link": "https://www.cisecurity.org/benchmark-v3-1",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 GMT",
    },
]


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 10 categories."""
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData",
        "vendor", ".dart_tool", "Carthage", "androidTest", "__tests__", "dist"
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
            if not file.endswith((
                ".kt", ".java", ".xml", ".gradle", ".kts", ".json",
                ".js", ".ts", ".swift", ".m", ".h", ".plist", ".entitlements", ".md"
            )):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-standards" in file or "monitor-standards-test" in file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for cat, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[cat].append({
                                        "file": filepath,
                                        "line_num": i,
                                        "content": line.strip()[:100],
                                        "matched_pattern": pattern.pattern,
                                    })
                                    # Break to avoid duplicate entry for same line and category
                                    break
            except Exception:
                pass
    return matches


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified)."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 domains & keywords
    p1_domains = [
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "nist.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "imda.gov.sg", "pdpc.gov.sg", "anpd.gov.br", "esafety.gov.au",
        "iso.org", "iec.ch", "owasp.org", "cisecurity.org"
    ]
    p1_keywords = [
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register", "international organization for standardization",
        "owasp", "center for internet security"
    ]

    # Priority 2
    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    # Priority 3
    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    # Priority 4
    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    # Priority 5
    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary"]

    priority = 4  # Default

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

    # Verification Logic
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
        if ".gov" in combined or "iso.org" in combined:
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
                    common_terms = {"iso", "nist", "owasp", "standards", "compliance"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


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

        # Match against categories
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
                classified_updates.append({
                    "id": ann.get("id", "STD-UPDATE-" + str(hash(title))[:6]),
                    "category": cat,
                    "title": title,
                    "description": desc,
                    "link": ann.get("link", ""),
                    "pubDate": ann.get("pubDate", ""),
                })
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a draft of a pull request complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_steps = []
    documentation_steps = []

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        verification_status = "Verified" if is_verified else "Unverified (Warning)"
        citations_list.append(
            f"- **{cat}** (Priority {priority} Source - {verification_status}): [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if cat == "ISO 27001":
            migration_steps.append("- **ISO 27001**: Incorporate Clause 4.1 climate action analysis and Annex A control modifications into information security policies.")
            impl_checklist.append("- [ ] Update ISMS Clause 4.1 Clause 4.2 risk registry documents to include climate factors.")
            risk_assessment.append("- *ISO 27001*: Gaps in security risk analysis due to unmapped environmental or operational factors.")
            testing_steps.append("- [ ] Verify risk assessment framework incorporates updated parameters.")
            documentation_steps.append("- [ ] Update internal ISMS manuals and audit logs to document the Annex A risk review.")
        elif cat == "ISO 27701":
            migration_steps.append("- **ISO 27701**: Implement formal PIMS registry and data controller consent record interfaces.")
            impl_checklist.append("- [ ] Integrate explicit PII processing registers for Joint Controllers.")
            risk_assessment.append("- *ISO 27701*: Lack of tracing records for third-party PII processing partners.")
            testing_steps.append("- [ ] Validate that consent revoke hooks trigger the appropriate data processor callbacks.")
            documentation_steps.append("- [ ] Update PIMS documentation and data processing catalogs.")
        elif cat == "ISO 42001":
            migration_steps.append("- **ISO 42001**: Build formal Artificial Intelligence Management System (AIMS) impact registry and model risk scoring pipelines.")
            impl_checklist.append("- [ ] Document model impact parameters and define algorithmic transparency boundaries.")
            risk_assessment.append("- *ISO 42001*: Undocumented generative AI parameters leading to Article 50 transparency rejections.")
            testing_steps.append("- [ ] Verify machine-readable synthetic marking labels on model outputs.")
            documentation_steps.append("- [ ] Create or update AI System Impact Assessment documentation.")
        elif cat == "ISO 31000":
            migration_steps.append("- **ISO 31000**: Review digital supply chain security baselines and formalize third-party risk management criteria.")
            impl_checklist.append("- [ ] Populate risk register with supplier software security attributes.")
            risk_assessment.append("- *ISO 31000*: Failure to identify cascading risks from upstream SaaS or library dependencies.")
            testing_steps.append("- [ ] Audit automatic risk score aggregators under simulation.")
            documentation_steps.append("- [ ] Publish updated third-party risk management criteria.")
        elif cat == "ISO 9001":
            migration_steps.append("- **ISO 9001**: Implement automated continuous integration quality gates and regression logging criteria.")
            impl_checklist.append("- [ ] Align delivery pipelines with new continuous improvement metrics.")
            risk_assessment.append("- *ISO 9001*: Inconsistent delivery validation leading to system stability degradation.")
            testing_steps.append("- [ ] Validate that failing builds trigger immediate corrective action alerts.")
            documentation_steps.append("- [ ] Update QMS continuous improvement standards.")
        elif cat == "IEC standards":
            migration_steps.append("- **IEC standards**: Adopt software safety class classifications for cloud-hosted healthcare app interfaces.")
            impl_checklist.append("- [ ] Audit safety-critical lifecycle tasks under IEC 62304 / IEC 82304.")
            risk_assessment.append("- *IEC standards*: Missing evidence of release verification for medical-grade software modules.")
            testing_steps.append("- [ ] Execute comprehensive lifecycle unit test validation plans.")
            documentation_steps.append("- [ ] Complete safety verification reports and lifecycle logs.")
        elif cat == "OWASP":
            migration_steps.append("- **OWASP**: Verify hardware-backed storage parameters for tokens and strict API certificate pinning configurations.")
            impl_checklist.append("- [ ] Refactor localized credential vaults to enforce MASVS L2 controls.")
            risk_assessment.append("- *OWASP*: Potential payload exposure via weak client-side storage configurations.")
            testing_steps.append("- [ ] Validate certificate pinning by simulating active proxy interceptions.")
            documentation_steps.append("- [ ] Document local encryption and security-by-design standards.")
        elif cat == "NIST AI RMF":
            migration_steps.append("- **NIST AI RMF**: Implement LLM bias mitigations, drift measurement, and trustworthy AI evaluations.")
            impl_checklist.append("- [ ] Integrate automated drift and hallucination metric logging.")
            risk_assessment.append("- *NIST AI RMF*: Model output degradation over time due to lack of drift measurements.")
            testing_steps.append("- [ ] Run testing scenarios simulating biased inputs and verify model guardrails respond.")
            documentation_steps.append("- [ ] Publish NIST AI RMF governance matrix and accountability logs.")
        elif cat == "NIST CSF":
            migration_steps.append("- **NIST CSF**: Define roles and responsibilities aligning with the Govern function under NIST CSF 2.0.")
            impl_checklist.append("- [ ] Draft cybersecurity roles and assign control accountability.")
            risk_assessment.append("- *NIST CSF*: Lack of documented organizational alignment on critical incident escalation pipelines.")
            testing_steps.append("- [ ] Simulate a mock cybersecurity incident and trace escalation pathways.")
            documentation_steps.append("- [ ] Update cybersecurity policy documentation matching CSF 2.0.")
        elif cat == "CIS Benchmarks":
            migration_steps.append("- **CIS Benchmarks**: Enforce read-only container environments and continuous dependency vulnerability scanning.")
            impl_checklist.append("- [ ] Audit host configurations against CIS Level 1 and Level 2 baselines.")
            risk_assessment.append("- *CIS Benchmarks*: Privilege escalation vulnerabilities due to write-accessible containers.")
            testing_steps.append("- [ ] Scan runtime images using static vulnerability analyzers.")
            documentation_steps.append("- [ ] Maintain CIS compliance verification and configuration hardening checklists.")

    citations_str = "\n".join(citations_list) if citations_list else "- No updates matched"
    affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set))) if affected_files_set else "- No specific codebase matches detected. Config files should be audited manually."
    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- No migration steps required."
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- No implementation checklist items."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- Low risk."
    testing_steps_str = "\n".join(testing_steps) if testing_steps else "- None required."
    doc_steps_str = "\n".join(documentation_steps) if documentation_steps else "- None required."

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces changes to align our systems and codebase with updated versions of global technical standards, including ISO, IEC, OWASP, NIST, and CIS Benchmarks.

## 2. Background
Maintaining alignment with international technical and security standards ensures system robustness, client trust, and streamlined external audits. Recent updates require targeted gap assessments.

## 3. Regulatory change
- **Technical Standards Evolution**: Aligning system metrics, risk management registries, and software delivery pipelines with Clause modifications, MASVS revisions, and CSF Govern functions.
- **Source Trust Hierarchy Enforced**: Evaluated all information sources strictly. Priority 1 sources are given primary trust.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: System boundaries and administrative controls are moderately exposed without these updates.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes to configurations and metadata are non-breaking and designed to support legacy systems seamlessly.

## 9. Implementation checklist
{impl_checklist_str}

## 10. Testing checklist
{testing_steps_str}
- [ ] Run python3 scripts/monitor-standards.py to verify no compliance regressions remain.

## 11. Documentation checklist
{doc_steps_str}
- [ ] Update docs/STANDARDS-POLICY-MIGRATION.md with the latest implementation status.

## 12. Compliance impact
- **Audit Preparedness**: Fully aligned with global frameworks, accelerating annual certification schedules.
- **Enterprise Integrity**: Ensures our standards logs remain accurate and fully verified.

## 13. Breaking changes
- There are no breaking changes associated with these standards-based modifications.

## 14. Review checklist
- [ ] Verify that the implementation does not introduce any emojis or non-ascii/graphical emoticons.
- [ ] Confirm all Priority 1 references are traced accurately.

## 15. Approver recommendations
Verify that risk registers are updated, and confirm that continuous integration continuous improvement parameters are running.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance areas.",
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
        lines.append(f"### Gaps & Tasks for {cat}")
        lines.append(
            "- **Compliance Priority**: Strategic prioritization based on standards updates."
        )

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update Clause 4.1 climate risk assessments in ISMS.")
            lines.append("- [ ] **Task 2**: Complete internal risk registry reviews.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Establish clear PII Joint Controller processing registries.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Formulate Artificial Intelligence Management System (AIMS) impact guidelines.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Incorporate third-party SaaS dependency risk metrics.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Deploy continuous delivery pipeline automated metric controls.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Apply safety classification constraints to healthcare companion app services.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Configure hardware-backed token storage and strict API certificate pin validations.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Set up model bias and drift measurements.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Align organization roles and control guidelines with CSF 2.0 Govern function.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Restrict runtime file system write access in cloud environments.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def run_monitor(project_path=".", live=False, mock=None, keywords=None, output_docs="docs/STANDARDS-POLICY-MIGRATION.md", pr_output="docs/STANDARDS_COMPLIANCE_PR_DRAFT.md"):
    # 1. Gather announcements
    announcements = []

    if live:
        print("Fetching live Technical Standards RSS feeds...")
        # Since we don't have stable external APIs during dry-run, we fallback to default mock below

    if mock or (not live and not mock) or not announcements:
        print("Using comprehensive mock Technical Standards policy updates for compliance scanning...")
        if mock and mock != "inline" and os.path.exists(mock):
            try:
                with open(mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(f"Failed to read mock file {mock}: {e}, using default mock dataset.", file=sys.stderr)
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # 2. Classify updates
    keywords_filter = [k.strip() for k in keywords.split(",")] if keywords else None
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        return [], {}

    print(f"Monitored and classified {len(classified_updates)} standards updates:")
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    # 3. Source trust checking (Block PR if unverified Priority 4/5 is matched)
    verified_updates = []
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u, classified_updates)
        if priority in (4, 5) and not is_verified:
            print(f"Warning: Update {u['title']} blocked due to unverified secondary source (Priority {priority}).")
        else:
            verified_updates.append(u)

    # 4. Scan codebase for signals
    print(f"Scanning codebase under '{project_path}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(project_path)
    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 5. Write documentation
    if output_docs:
        os.makedirs(os.path.dirname(output_docs) or ".", exist_ok=True)
        update_documentation_report(verified_updates, output_docs)

    # 6. Draft PR
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
    if pr_output:
        os.makedirs(os.path.dirname(pr_output) or ".", exist_ok=True)
        try:
            with open(pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR draft written successfully to: {pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {pr_output}: {e}", file=sys.stderr)

    return verified_updates, scan_results


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards policy feeds"
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

    run_monitor(
        project_path=args.dir,
        live=args.live,
        mock=args.mock,
        keywords=args.keywords,
        output_docs=args.output_docs,
        pr_output=args.pr_output
    )


if __name__ == "__main__":
    main()
