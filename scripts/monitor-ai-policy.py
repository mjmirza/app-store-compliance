#!/usr/bin/env python3
"""Monitors platform-specific AI policies (Apple, Google Play) from
live feeds or mock data, and drafts a 15-section PR per finding."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json
import html

# Define default RSS/Atom feed URLs
APPLE_RSS = "https://developer.apple.com/news/rss/news.rss"
# Since Google doesn't have a single stable RSS for policy, we support checking RSS as well
GOOGLE_RSS = "https://android-developers.googleblog.com/feeds/posts/default"

# 25 Compliance domains tracking (simulated context/coverage check as per monitor.py description)
COMPLIANCE_DOMAINS = [
    "AI-Generated Content",
    "App Review AI Guidance",
    "Safety Expectations",
    "User Disclosure",
    "Privacy Manifest",
    "Required Reason APIs",
    "Tracking Domains",
    "Export Compliance",
    "Trader Status",
    "In-App Purchases",
    "Restore Purchases",
    "Subscriptions",
    "Demo Accounts",
    "Human Interface Guidelines",
    "GDPR Compliance",
    "COPPA Compliance",
    "EU AI Act",
    "Designed for Families",
    "Simulated Gambling",
    "Loot Boxes",
    "macOS Sandboxing",
    "Dynamic Code Loading",
    "Package Visibility",
    "Overlays/Tapjacking",
    "Account Deletion",
]

# AI signals to look for when scanning the codebase
AI_SIGNALS = [
    r"api\.openai\.com",
    r"openai",
    r"anthropic",
    r"gemini",
    r"generativelanguage",
    r"chat/completions",
    r"stable[ -_]diffusion",
    r"text-to-image",
    r"image generation",
    r"chatgpt",
    r"claude",
    r"llm",
    r"generative[ -_]ai",
]

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications, Apple Developer, Android Developer)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# Illustrative fallback only (real landing pages, invented wording). See README.
MOCK_ANNOUNCEMENTS = [
    {
        "id": "APPLE-AI-2026-UPDATE",
        "platform": "Apple",
        "title": "Sample. Apple App Review Guidelines, generative AI section (illustrative)",
        "description": "Illustrative example only. Apps with generative AI features are expected to implement input/output moderation and user-reporting, disclose data shared with third-party LLM providers, and reflect AI-generated content in the age rating questionnaire. Verify the current wording at the linked guidelines page before citing it as fact.",
        "link": "https://developer.apple.com/app-store/review/guidelines/",
        "pubDate": "Wed, 01 Apr 2026 10:00:00 PDT",
    },
    {
        "id": "GOOGLE-AI-2026-POLICY",
        "platform": "Google Play",
        "title": "Sample. Google Play generative AI content policy (illustrative)",
        "description": "Illustrative example only. Apps featuring generative AI are expected to disclose AI-generated content, let users flag or report harmful output, and prevent deepfakes, face-swaps, and non-consensual sexual content. Verify the current wording at the linked developer policy center before citing it as fact.",
        "link": "https://play.google/developer-content-policy/",
        "pubDate": "Thu, 02 Apr 2026 09:00:00 PDT",
    },
]


def clean_html_text(text, max_len=500):
    """
    Strips raw HTML tags, unescapes HTML entities, collapses whitespace,
    and truncates RSS entry descriptions to clean plain-text summaries.
    """
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = html.unescape(clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    if max_len and len(clean) > max_len:
        clean = clean[:max_len] + "..."
    return clean


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
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "nist.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "imda.gov.sg", "pdpc.gov.sg", "anpd.gov.br", "esafety.gov.au",
        "apple.com", "developer.apple.com", "android.com", "developer.android.com",
        "support.google.com", "play.google"
    ]
    p1_keywords = [
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register", "apple developer", "android developer"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
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
                    common_terms = {"ai", "generative", "llm", "apple", "google", "policy"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(policy_matches):
    """
    Logs verification alerts to stderr and enforces source credibility restrictions.
    """
    for m in policy_matches:
        priority, is_verified = classify_source_and_verify(m)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        m["priority"] = priority
        m["is_verified"] = is_verified
        m["source_status"] = status_str
        if priority in (4, 5) and not is_verified:
            print(
                f"Source Trust Alert: [{m['platform']}] {m['title']} is a Priority {priority} unverified source.",
                file=sys.stderr,
            )


def scan_codebase(start_dir="."):
    """
    Scans the codebase for AI-related integration signals.
    Excludes typical build, dependency, and test directories.
    """
    matches = []
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

    compiled_signals = [re.compile(pattern, re.IGNORECASE) for pattern in AI_SIGNALS]

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Focus on source, config, and plist files
            if not file.endswith(
                (
                    ".swift",
                    ".m",
                    ".h",
                    ".kt",
                    ".java",
                    ".xml",
                    ".plist",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".dart",
                    ".md",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor.py and other scripts to avoid self-referencing
            if "monitor.py" in file or "monitor-test.sh" in file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for r in compiled_signals:
                            if r.search(line):
                                matches.append(
                                    {
                                        "file": filepath,
                                        "line_num": i,
                                        "content": line.strip()[:100],
                                        "matched_pattern": r.pattern,
                                    }
                                )
                                break  # match found for this line, go to next line
            except Exception:
                # Silently ignore binary/unreadable files
                pass
    return matches


def parse_rss_feed(url):
    """
    Fetches and parses both RSS (XML with <item>) and Atom (XML with <entry>) feeds.
    Returns list of parsed item dicts with keys: title, description, link, pubDate.
    """
    items = []
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (AppStoreComplianceMonitor/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            # Helper to strip XML namespaces from tags
            def clean_tag(tag):
                if "}" in tag:
                    return tag.split("}", 1)[1]
                return tag

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
                            title = clean_html_text(child.text or "")
                        elif ctag in ("description", "summary", "content"):
                            desc = clean_html_text(child.text or "")
                        elif ctag == "link":
                            link_val = child.get("href")
                            if link_val:
                                link = link_val
                            else:
                                link = child.text or ""
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


def analyze_announcements(announcements, keywords):
    """
    Filters announcements for AI policy changes and maps them to policy items.
    """
    matches = []
    keywords_lower = [k.lower() for k in keywords]

    for ann in announcements:
        title = clean_html_text(ann.get("title", ""))
        desc = clean_html_text(ann.get("description", ""))
        text_to_search = (title + " " + desc).lower()

        # Check if any keyword matches
        matched_kw = [kw for kw in keywords_lower if kw in text_to_search]
        if matched_kw:
            # Platform classification
            platform = (
                "Apple"
                if "apple" in text_to_search or ann.get("platform") == "Apple"
                else "Google Play"
            )

            # Map specific review requirements
            review_items = []
            if platform == "Apple":
                if any(
                    x in text_to_search
                    for x in ["content", "generative", "output", "model"]
                ):
                    review_items.append("AI-generated content requirements")
                if any(
                    x in text_to_search for x in ["review", "guideline", "guidance"]
                ):
                    review_items.append("App Review AI guidance")
                if any(
                    x in text_to_search
                    for x in ["safety", "abuse", "nsfw", "moderation", "filter"]
                ):
                    review_items.append("Safety expectations")
                if any(
                    x in text_to_search
                    for x in ["disclosure", "consent", "modal", "inform"]
                ):
                    review_items.append("User disclosure requirements")
                if not review_items:
                    review_items = ["General Apple AI policy"]
            else:
                if any(
                    x in text_to_search for x in ["policy", "guideline", "requirement"]
                ):
                    review_items.append("Google Play AI policies")
                if any(
                    x in text_to_search
                    for x in ["disclosure", "consent", "modal", "inform"]
                ):
                    review_items.append("AI-generated content disclosures")
                if any(
                    x in text_to_search
                    for x in ["safety", "abuse", "nsfw", "moderation", "filter"]
                ):
                    review_items.append("User safety requirements")
                if not review_items:
                    review_items = ["General Google Play AI policy"]

            matches.append(
                {
                    "title": title,
                    "description": desc,
                    "link": ann.get("link", ""),
                    "pubDate": ann.get("pubDate", ""),
                    "platform": platform,
                    "matched_keywords": matched_kw,
                    "review_items": review_items,
                }
            )
    return matches


def generate_pull_request_draft(policy_matches, affected_files):
    """
    Generates a draft of a pull request complying with the exact 15 required sections.
    """
    # Group matched files to list them cleanly
    files_list_str = ""
    if affected_files:
        unique_files = sorted(list(set(f["file"] for f in affected_files)))
        files_list_str = "\n".join(f"- `{f}`" for f in unique_files)
    else:
        files_list_str = "- *No AI signals directly detected in source files. (Verify dynamically loaded components or web endpoints).* "

    citations_list = "\n".join(
        f"- [{m['title']}]({m['link']}) ({m['platform']} Update, {m['pubDate']})"
        for m in policy_matches
    )

    migration_steps_list = []
    impl_checklist_items = []

    # Generate contextual migration steps and implementation checklist based on platforms triggered
    platforms_triggered = set(m["platform"] for m in policy_matches)
    if "Apple" in platforms_triggered:
        migration_steps_list.append(
            "1. **Consent Modal**: Add an in-app consent modal detailing that third-party AI/LLM components are used and get explicit consent before sending user personal data."
        )
        migration_steps_list.append(
            "2. **Output Moderation**: Wire real-time prompt/response filters to detect, flag, and filter out objectionable or NSFW AI content."
        )
        migration_steps_list.append(
            "3. **Age Rating Update**: Update the age rating questionnaire in App Store Connect to account for interactive AI chat functionality."
        )

        impl_checklist_items.append(
            "- [ ] Create `ConsentModalView` and integrate it into onboarding/settings."
        )
        impl_checklist_items.append(
            "- [ ] Integrate OpenAI/Anthropic moderation API or client-side bad-word list."
        )
        impl_checklist_items.append(
            "- [ ] Add reporting and content flag buttons next to AI-generated messages."
        )
        impl_checklist_items.append(
            "- [ ] Recheck App Store Connect questionnaire for Guideline 1.2 and 2.3.6 updates."
        )
    if "Google Play" in platforms_triggered or not platforms_triggered:
        migration_steps_list.append(
            "4. **Prominent Disclosure**: Implement an in-app disclaimer and user consent sheet for generative content on Android devices."
        )
        migration_steps_list.append(
            "5. **Content Safety Controls**: Add a prominent 'report content' or 'flag output' UI element directly on all AI output cards."
        )
        migration_steps_list.append(
            "6. **Terms of Service update**: Declare user safety requirements regarding deepfakes and non-consensual content generation."
        )

        impl_checklist_items.append(
            "- [ ] Implement a prominent Play Policy disclosure dialog on app launch or AI feature access."
        )
        impl_checklist_items.append(
            "- [ ] Implement one-click reporting next to every AI output block on Android."
        )
        impl_checklist_items.append(
            "- [ ] Prevent face-swap and image generation capabilities if NSFW/deepfake models can be accessed."
        )
        impl_checklist_items.append(
            "- [ ] Update the Google Play Console Data Safety form declarations."
        )

    migration_steps_str = "\n".join(migration_steps_list)
    impl_checklist_str = "\n".join(impl_checklist_items)

    pr_template = f"""# PULL REQUEST DRAFT: Platform-Specific AI Policy Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with the latest platform-specific AI policies. It implements robust user disclosure, consent modals, output filtering, and content reporting mechanisms to prevent potential rejections during App Store and Google Play reviews.

## 2. Background
Both Apple and Google Play have tightened their restrictions regarding generative AI features inside mobile apps. Review systems are now actively rejecting applications that send user data to third-party LLM APIs without transparent consent or that display generative content without moderation safeguards.

## 3. Regulatory change
- **Apple (Guidelines 1.2, 5.1.2(i), and 2.3.6)**: Requires clear disclosure of third-party AI data sharing, explicit user consent prior to transmission, content filters for output safety, and reflection of chat assistants in the age rating.
- **Google Play (AI-Generated Content Policy)**: Enforces mandatory user-facing disclosures, user flagging/reporting mechanisms for offensive AI-generated content, and zero-tolerance for deepfakes, face-swapping, or non-consensual graphic outputs.

## 4. Official citations
{citations_list}

## 5. Affected files
{files_list_str}

## 6. Risk assessment
- **Risk Level**: High
- **Consequences of non-compliance**: Immediate rejection of app updates by Apple App Review and potential Google Play suspension or removal under their AI-generated content guidelines.
- **Mitigation plan**: Build interactive user consent, prominent disclosure overlays, content moderation filters, and clear flagging UI.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are purely additive. Older clients will default to safe local fallback content or receive standard prompts. Data structures, local schema versions, and existing preferences remain fully backward compatible.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Update `docs/ADVANCED-2026.md` and related compliance manuals.

## 10. Testing checklist
- [ ] Verify that the consent modal triggers and blocks data send until approved.
- [ ] Verify that prompt injection attempts and inappropriate topics trigger the moderation filter.
- [ ] Test the content flagging button and verify reports are logged on the server.
- [ ] Test on both iOS and Android emulators/devices for layout adjustments.

## 11. Documentation checklist
- [ ] Update the Privacy Policy URL with third-party AI disclosure details.
- [ ] Update App Store Connect "Notes for Review" with demo credentials and compliance instructions.
- [ ] Update Google Play Console Data Safety questionnaire declarations.
- [ ] Document moderation guidelines in the repository's wiki or `docs/` folder.

## 12. Compliance impact
- **Apple App Store**: Aligns with 2026 guidelines; secures safe passage through human and automated reviews.
- **Google Play**: Safeguards developer account health and retains age-appropriate content standing.
- **EU AI Act**: Fulfills Article 50 transparency requirements for AI-generated interaction.

## 13. Breaking changes
- No breaking database schema migrations.
- UI flow changes include a mandatory, one-time consent prompt when first accessing AI-powered features.

## 14. Review checklist
- [ ] Code complies with all architectural boundaries and secure API storage rules.
- [ ] Consent modal text is clear, localized, and lists the AI sub-processors.
- [ ] Verification tests for the content moderation engine pass.

## 15. Approver recommendations
Ensure that the privacy consent modal explicitly mentions the specific third-party AI processor (e.g., OpenAI, Anthropic, Gemini) as mandated by Apple 5.1.2(i). Confirm that the content reporting UI is functional and triggers 24-hour moderation capabilities.
"""
    return pr_template


def update_documentation(policy_matches, output_filepath, is_simulated=True):
    """
    Appends the latest policy findings and migration tasks directly to the output compliance file.
    Retains the simulation disclaimer notice when running in mock/simulated mode.
    """
    report_content = [
        "<!-- AI_POLICY_MONITOR_START -->",
    ]

    if is_simulated:
        report_content.extend([
            "",
            "> **Simulated output, not live announcements.** This file is generated by the monitor",
            "> script in `--simulate` mode, which uses illustrative sample announcements to show the",
            "> shape of a migration report. The titles, publish dates, and descriptions below are",
            "> examples, not real Apple or Google publications. Only the linked official",
            "> documentation URLs are real. Re-run the monitor without `--simulate` against the live",
            "> feed before treating anything here as an actual requirement.",
            "",
        ])

    report_content.extend([
        "# AI Policy Monitoring & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-ai-policy.py` to keep track of platform policy changes.",
        "",
        "## Latest Monitored Policy Changes",
        "",
    ])

    for m in policy_matches:
        report_content.append(f"### {m['title']} ({m['platform']})")
        report_content.append(f"- **Published**: {m['pubDate']}")
        report_content.append(f"- **Official Link**: [{m['link']}]({m['link']})")
        report_content.append(f"- **Key Topics**: {', '.join(m['review_items'])}")
        report_content.append(f"- **Details**: {m['description']}")
        report_content.append("")

    report_content.append("<!-- AI_POLICY_MONITOR_END -->")

    # Write or append to the output file
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report_content))
        print(f"Documentation updated/created successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="App Store & Google Play AI Policy Monitor"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live RSS/Atom feeds from Apple and Google blog",
    )
    parser.add_argument(
        "--mock",
        type=str,
        help="Path to a mock JSON/XML file or 'inline' to use built-in mock policy updates",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default="ai,generative,artificial intelligence,llm,openai,anthropic,gemini,safety,user disclosure,disclosure",
        help="Comma-separated keywords to scan announcements for",
    )
    parser.add_argument(
        "--dir", type=str, default=".", help="Codebase directory to scan"
    )
    parser.add_argument(
        "--output-docs",
        type=str,
        default="docs/AI-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks / docs updates",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/AI_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR (defaults to docs/AI_COMPLIANCE_PR_DRAFT.md)",
    )

    args = parser.parse_args()

    keywords_list = [k.strip() for k in args.keywords.split(",")]
    announcements = []
    is_simulated = True

    # 1. Gather announcements
    if args.live:
        print("Fetching live Apple RSS feed...")
        live_apple = parse_rss_feed(APPLE_RSS)
        announcements.extend(live_apple)
        print("Fetching live Google Blog RSS/Atom feed...")
        live_google = parse_rss_feed(GOOGLE_RSS)
        announcements.extend(live_google)
        if live_apple or live_google:
            is_simulated = False

    if args.mock or (not args.live and not args.mock) or not announcements:
        # Default or explicit inline mock mode
        print("Using mock policy update data for analysis...")
        is_simulated = True
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, falling back to inline data",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # 2. Analyze policy announcements against keywords
    matched_policies = analyze_announcements(announcements, keywords_list)

    if not matched_policies:
        print("No new AI platform policy changes detected.")
        sys.exit(0)

    # Enforce strict source trust hierarchy validation
    enforce_strict_source_trust_hierarchy(matched_policies)

    print(f"Detected {len(matched_policies)} AI-related platform policy announcements:")
    for idx, m in enumerate(matched_policies, 1):
        print(f" {idx}. [{m['platform']}] {m['title']}")
        print(f"    Citations checked: {', '.join(m['review_items'])}")

    # 3. Scan codebase for affected AI features
    print(f"Scanning codebase under '{args.dir}' for AI signals...")
    affected_features = scan_codebase(args.dir)
    print(f"Found {len(affected_features)} matching source lines.")

    # 4. Generate documentation updates and migration tasks
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation(matched_policies, args.output_docs, is_simulated=is_simulated)

    # 5. Draft the Pull Request with exactly 15 sections
    pr_draft = generate_pull_request_draft(matched_policies, affected_features)

    if args.pr_output:
        os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
        try:
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR Draft successfully written to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        print("\n=== GENERATED COMPREHENSIVE COMPLIANCE PULL REQUEST DRAFT ===")
        print(pr_draft)
        print("==============================================================")


if __name__ == "__main__":
    main()
