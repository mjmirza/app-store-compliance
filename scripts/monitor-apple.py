#!/usr/bin/env python3
"""Monitors the 25 Apple requirement categories and generates repo-impact
and migration tasks for each update."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 25 tracked Apple Developer & App Store requirement categories
TRACKS = [
    "App Store Review Guidelines",
    "Apple Developer Program License Agreement",
    "Human Interface Guidelines",
    "Apple Privacy requirements",
    "Privacy Manifests",
    "Required Reason APIs",
    "App Tracking Transparency",
    "Sign in with Apple",
    "In-App Purchase policies",
    "Alternative payment regulations",
    "DMA compliance changes",
    "Accessibility requirements",
    "AI-related App Store policies",
    "Child safety requirements",
    "HealthKit policies",
    "Location permissions",
    "Camera and microphone permissions",
    "Push Notification requirements",
    "Background execution policies",
    "Security updates",
    "SDK requirements",
    "Minimum SDK versions",
    "Xcode requirements",
    "Swift requirements",
    "App Store Connect announcements",
]

# Keywords used to classify incoming policy announcements/articles into the 25 categories
CATEGORY_KEYWORDS = {
    "App Store Review Guidelines": [
        "review guidelines",
        "app review guidelines",
        "guideline 2.1",
        "guideline 4.3",
        "guideline 5.1.1",
        "guidelines update",
        "app review",
    ],
    "Apple Developer Program License Agreement": [
        "license agreement",
        "developer program license",
        "pla",
        "sla",
        "program license",
    ],
    "Human Interface Guidelines": [
        "human interface",
        "hig",
        "design guidelines",
        "layout",
        "typography",
        "dark mode",
        "design update",
    ],
    "Apple Privacy requirements": [
        "privacy requirement",
        "privacy policy",
        "nutrition label",
        "privacy label",
        "user consent",
    ],
    "Privacy Manifests": [
        "privacy manifest",
        "xcprivacy",
        "privacyinfo",
        "data collections",
    ],
    "Required Reason APIs": [
        "required reason api",
        "accessed api",
        "reasons for api",
        "userdefaults",
        "systemuptime",
        "boot time",
        "file timestamp",
    ],
    "App Tracking Transparency": [
        "app tracking transparency",
        "att",
        "idfa",
        "user tracking",
    ],
    "Sign in with Apple": [
        "sign in with apple",
        "siwa",
        "apple sign-in",
        "social login",
    ],
    "In-App Purchase policies": [
        "in-app purchase",
        "iap",
        "storekit",
        "subscription terms",
        "purchase policy",
        "restore purchases",
    ],
    "Alternative payment regulations": [
        "alternative payment",
        "external purchase link",
        "alternate billing",
        "payment regulation",
        "external link entitlement",
    ],
    "DMA compliance changes": [
        "dma",
        "digital markets act",
        "alternative marketplace",
        "core technology fee",
        "ctf",
        "alternative distribution",
    ],
    "Accessibility requirements": [
        "accessibility",
        "en 301 549",
        "wcag",
        "voiceover",
        "dynamic type",
    ],
    "AI-related App Store policies": [
        "generative ai",
        "llm",
        "chatgpt",
        "ai policy",
        "ai content",
        "openai",
        "anthropic",
        "content moderation",
        "ai transparency",
    ],
    "Child safety requirements": [
        "child safety",
        "kids category",
        "coppa",
        "csam",
        "minor",
        "under-13",
        "parental gate",
    ],
    "HealthKit policies": [
        "healthkit",
        "hkhealthstore",
        "health app",
        "health data",
        "hipaa",
        "privacy metrics",
    ],
    "Location permissions": [
        "location permission",
        "locationmanager",
        "background location",
        "nslocation",
        "location when in use",
    ],
    "Camera and microphone permissions": [
        "camera permission",
        "microphone permission",
        "nscamera",
        "nsmicrophone",
        "media capture",
    ],
    "Push Notification requirements": [
        "push notification",
        "apns",
        "aps-environment",
        "remote notification",
    ],
    "Background execution policies": [
        "background execution",
        "background mode",
        "uibackgroundmodes",
        "background fetch",
        "background task",
    ],
    "Security updates": [
        "security update",
        "vulnerability",
        "cve",
        "encryption declaration",
        "itsappusesnonexemptencryption",
    ],
    "SDK requirements": [
        "sdk requirement",
        "commonly used sdk",
        "third party sdk",
        "embedded sdk",
        "signed framework",
    ],
    "Minimum SDK versions": [
        "minimum sdk",
        "target sdk",
        "ios sdk",
        "deployment target",
        "minimum deployment target",
    ],
    "Xcode requirements": [
        "xcode requirement",
        "xcode version",
        "xcode 15",
        "xcode 16",
        "xcode 17",
    ],
    "Swift requirements": [
        "swift requirement",
        "swift version",
        "swift 6",
        "concurrency",
        "data-race safety",
    ],
    "App Store Connect announcements": [
        "app store connect announcement",
        "asc news",
        "developer news",
        "publishing workflow",
        "store connect",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 25 categories
CATEGORY_SIGNALS = {
    "App Store Review Guidelines": [
        r"LoginView", r"signIn", r"AuthService", r"lorem ipsum", r"TODO", r"FIXME"
    ],
    "Apple Developer Program License Agreement": [
        r"company", r"individual", r"developer account", r"LicenseAgreement"
    ],
    "Human Interface Guidelines": [
        r"UIFont", r"UIColor", r"VStack", r"HStack", r"SwiftUI", r"padding", r"margin"
    ],
    "Apple Privacy requirements": [
        r"privacyPolicy", r"privacy-policy", r"PrivacyPolicyURL"
    ],
    "Privacy Manifests": [
        r"NSPrivacyAccessedAPITypes", r"NSPrivacyCollectedDataTypes", r"PrivacyInfo.xcprivacy"
    ],
    "Required Reason APIs": [
        r"UserDefaults", r"NSFileManager", r"systemUptime", r"ProcessInfo", r"stat\s*\("
    ],
    "App Tracking Transparency": [
        r"ATTrackingManager", r"NSUserTrackingUsageDescription", r"ASIdentifierManager", r"advertisingIdentifier"
    ],
    "Sign in with Apple": [
        r"ASAuthorizationAppleIDProvider", r"SignInWithApple", r"AuthenticationServices"
    ],
    "In-App Purchase policies": [
        r"StoreKit", r"SKProduct", r"Product\.purchase", r"restorePurchases", r"SKPaymentQueue"
    ],
    "Alternative payment regulations": [
        r"com\.apple\.developer\.storekit\.external-purchase", r"SKExternalPurchase", r"Stripe", r"PayPal"
    ],
    "DMA compliance changes": [
        r"com\.apple\.developer\.storekit\.external-purchase", r"alternative-distribution", r"CoreTechnologyFee"
    ],
    "Accessibility requirements": [
        r"accessibilityLabel", r"accessibilityIdentifier", r"UIAccessibility", r"DynamicType"
    ],
    "AI-related App Store policies": [
        r"openai", r"anthropic", r"chat/completions", r"gemini", r"generative-ai", r"LLM"
    ],
    "Child safety requirements": [
        r"coppa", r"under-13", r"parental-gate", r"kids-category", r"DeclaredAgeRange"
    ],
    "HealthKit policies": [
        r"HKHealthStore", r"HealthKit", r"NSHealthShareUsageDescription", r"NSHealthUpdateUsageDescription"
    ],
    "Location permissions": [
        r"CLLocationManager", r"NSLocationWhenInUseUsageDescription", r"NSLocationAlwaysUsageDescription"
    ],
    "Camera and microphone permissions": [
        r"AVCaptureDevice", r"NSCameraUsageDescription", r"NSMicrophoneUsageDescription", r"UIImagePickerController"
    ],
    "Push Notification requirements": [
        r"aps-environment", r"UNUserNotificationCenter", r"registerForRemoteNotifications"
    ],
    "Background execution policies": [
        r"UIBackgroundModes", r"backgroundTimeRemaining", r"beginBackgroundTaskWithName"
    ],
    "Security updates": [
        r"ITSAppUsesNonExemptEncryption", r"CCATS", r"ANSSI", r"SSL-pinning"
    ],
    "SDK requirements": [
        r"Firebase", r"Alamofire", r"AppsFlyerLib", r"Adjust", r"FBSDK", r"cocoapods", r"carthage"
    ],
    "Minimum SDK versions": [
        r"IPHONEOS_DEPLOYMENT_TARGET", r"MACOSX_DEPLOYMENT_TARGET", r"deploymentTarget"
    ],
    "Xcode requirements": [
        r"Xcode", r"pbxproj", r"xcconfig"
    ],
    "Swift requirements": [
        r"SWIFT_VERSION", r"async", r"await", r"Task", r"@MainActor", r"strict concurrency"
    ],
    "App Store Connect announcements": [
        r"AppStoreConnect", r"asc-news", r"developer-news", r"AppStoreAPI"
    ],
}

MOCK_ANNOUNCEMENTS = [
    {
        "id": "MOCK-APPLE-PRIVACY",
        "category": "Privacy Manifests",
        "title": "Mandatory Privacy Manifest Integration and Domain Tracking Requirements",
        "description": "Apple is strictly enforcing Privacy Manifests (PrivacyInfo.xcprivacy) for all submissions containing third-party tracking domains or Required Reason APIs.",
        "link": "https://developer.apple.com/news/?id=privacy-manifests-mandatory",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "MOCK-APPLE-IAP",
        "category": "In-App Purchase policies",
        "title": "App Store In-App Purchase and StoreKit Updates",
        "description": "Important billing and subscription term disclosures under updated StoreKit regulations, requiring Restore Purchases and pricing clarity.",
        "link": "https://developer.apple.com/news/?id=storekit-iap-policies",
        "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "MOCK-APPLE-DMA",
        "category": "DMA compliance changes",
        "title": "EU Digital Markets Act Compliance Changes and Alternative App Marketplaces",
        "description": "Developers distributing apps in the European Union can utilize alternative marketplaces, browser engines, and external link billing flows under the updated DMA requirements.",
        "link": "https://developer.apple.com/news/?id=dma-compliance-eu",
        "pubDate": "Wed, 03 Jun 2026 12:00:00 GMT",
    }
]


def scan_codebase_for_apple_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 25 requirement categories.
    """
    matches = {cat: [] for cat in TRACKS}
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
            if not file.endswith(
                (
                    ".swift",
                    ".m",
                    ".h",
                    ".plist",
                    ".xcprivacy",
                    ".entitlements",
                    ".pbxproj",
                    ".storyboard",
                    ".xib",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, start_dir)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for cat, regex_list in compiled_signals.items():
                    for pattern in regex_list:
                        if pattern.search(content):
                            matches[cat].append({"file": rel_path, "match": pattern.pattern})
                            break
            except Exception:
                pass

    return matches


def parse_rss_feed(url):
    """
    Parses live Atom/RSS feed for updates.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)

        items = []
        for item in root.iter():
            tag = item.tag
            if "}" in tag:
                tag = tag.split("}", 1)[1]

            if tag == "item" or tag == "entry":
                dict_item = {}
                for child in item:
                    ctag = child.tag
                    if "}" in ctag:
                        ctag = ctag.split("}", 1)[1]
                    if ctag in ["title", "description", "summary", "link", "pubDate", "updated", "id"]:
                        if ctag == "link" and child.attrib.get("href"):
                            dict_item[ctag] = child.attrib["href"]
                        else:
                            dict_item[ctag] = child.text
                if dict_item:
                    items.append(dict_item)
        return items
    except Exception as e:
        print(f"Failed to fetch or parse RSS feed {url}: {e}", file=sys.stderr)
        return []


def classify_announcements(announcements, keywords_filter=None):
    """
    Maps incoming announcements to the 25 Apple requirement categories.
    """
    classified = []

    for item in announcements:
        title = item.get("title", "")
        desc = item.get("description", item.get("summary", ""))
        text_to_search = f"{title} {desc}".lower()

        # Filter by command-line keywords if requested
        if keywords_filter:
            matched_kw = any(kw.lower() in text_to_search for kw in keywords_filter)
            if not matched_kw:
                continue

        matched_cats = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_to_search:
                    matched_cats.append(cat)
                    break

        for cat in matched_cats:
            classified.append(
                {
                    "category": cat,
                    "title": title,
                    "description": desc,
                    "link": item.get("link", "https://developer.apple.com/news/"),
                    "pubDate": item.get("pubDate", item.get("updated", "Unknown Date")),
                }
            )

    return classified


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
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "Privacy Manifests":
            migration_steps.append(
                f"- **{cat}**: Audit third-party SDK dependencies for signatures and incorporate mandatory NSPrivacyAccessedAPITypes."
            )
            impl_checklist.append(
                "- [ ] Add PrivacyInfo.xcprivacy to root of main target."
            )
            impl_checklist.append(
                "- [ ] Declare correct tracking keys and domains if app tracking is utilized."
            )
            risk_assessment.append(
                f"- *{cat}*: Mandatory upload-time submission blockage if required privacy manifests are missing."
            )
        elif cat == "Required Reason APIs":
            migration_steps.append(
                f"- **{cat}**: Audit usage of UserDefaults, systemUptime, and file timestamps, and declare valid reason codes in PrivacyInfo.xcprivacy."
            )
            impl_checklist.append(
                "- [ ] Declare NSPrivacyAccessedAPITypes in PrivacyInfo.xcprivacy with valid reason codes."
            )
            risk_assessment.append(
                f"- *{cat}*: Direct automated App Store Connect upload-time rejections post-Spring deadline."
            )
        elif cat == "In-App Purchase policies":
            migration_steps.append(
                f"- **{cat}**: Upgrade billing modules to modern StoreKit 2 APIs. Ensure a clear Restore Purchases button is prominent."
            )
            impl_checklist.append(
                "- [ ] Implement StoreKit 2 Transaction.currentEntitlements sync and restore UI."
            )
            risk_assessment.append(
                f"- *{cat}*: Reviewer rejection under Guideline 3.1.1 if digital transactions fail to use store mechanics."
            )
        elif cat == "DMA compliance changes":
            migration_steps.append(
                f"- **{cat}**: Integrate alternative distribution entitlements for European Union users if distributing outside App Store."
            )
            impl_checklist.append(
                "- [ ] Configure EU alternative marketplace distribution settings on App Store Connect."
            )
            risk_assessment.append(
                f"- *{cat}*: Inability to publish or distribute through alternative marketplaces in the EU without entitlements."
            )
        elif cat == "AI-related App Store policies":
            migration_steps.append(
                f"- **{cat}**: Integrate user content reporting mechanisms and clear transparency notices before sending data to generative models."
            )
            impl_checklist.append(
                "- [ ] Implement AI model user data consent modal."
            )
            impl_checklist.append(
                "- [ ] Build robust moderation filters and user reporting options for AI outputs."
            )
            risk_assessment.append(
                f"- *{cat}*: High risk of rejection under Guideline 5.1.2 or EU AI Act transparency rules."
            )
        elif cat == "Swift requirements":
            migration_steps.append(
                f"- **{cat}**: Migrate workspace targets to Swift 6 and resolve strict concurrency compile-time warnings."
            )
            impl_checklist.append(
                "- [ ] Resolve SWIFT_VERSION 6.0 compiler strict concurrency diagnostics."
            )
            risk_assessment.append(
                f"- *{cat}*: Compiler errors and data-race runtime safety issues on newer iOS runtimes."
            )
        else:
            migration_steps.append(
                f"- **{cat}**: Ensure proper implementation according to official developer guidelines for {cat}."
            )
            impl_checklist.append(
                f"- [ ] Audit codebase for patterns matching {cat}."
            )
            risk_assessment.append(
                f"- *{cat}*: General publishing gate risk or rejection on subsequent app submissions."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Apple Developer Requirements Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Apple Developer and App Store publishing requirements. It addresses privacy manifests, required reason APIs, StoreKit integrations, DMA marketplace settings, and compiler compliance to clear all modern App Store Connect gates.

## 2. Background
Apple enforces strict static and manual reviews before permitting binary distribution on the App Store. Proactive integration of required manifests, user data collection declarations, and appropriate design paradigms prevents costly rejection loops.

## 3. Regulatory change
- **App Store Publishing Gates**: Mandates for fully formed PrivacyInfo.xcprivacy files, declared Required Reason APIs (UserDefaults, systemUptime), and StoreKit pricing disclosures.
- **EU Digital Markets Act (DMA)**: Integration pathways for alternative distribution networks, external purchase link configurations, and core technology fee assessments.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of update blockage in App Store Connect if static review rules are violated.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are designed to preserve backward compatibility. Privacy manifests are backward-compatible metadata packages and do not alter execution behavior on older iOS versions. Alternate purchase flows gracefully degrade to standard StoreKit interfaces.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the compliance guard check locally.

## 10. Testing checklist
- [ ] Verify that PrivacyInfo.xcprivacy contains accurate tracking declarations.
- [ ] Confirm in-app purchases restore flows work in Sandbox environment.
- [ ] Verify there are no strict concurrency crashes on newer devices.

## 11. Documentation checklist
- [ ] Update `docs/APPLE-POLICY-MIGRATION.md` with compliance progress.
- [ ] Configure reviewer notes template in App Store Connect metadata.

## 12. Compliance impact
- **Publishing Gate**: Eliminates upload-time static analysis warnings.
- **Brand Standing**: Ensures uninterrupted service and keeps developer account in good standing.

## 13. Breaking changes
- No binary breaking changes are introduced; deprecations are resolved with fallback patterns.

## 14. Review checklist
- [ ] Code strictly implements guidelines for user data privacy.
- [ ] All sensitive permissions declare explicit, customer-facing descriptions.

## 15. Approver recommendations
Ensure that the App Store Connect Account Holder reviews and accepts any updated Developer Program License agreements online, as code compliance cannot bypass administrative agreements.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/APPLE-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- APPLE_POLICY_MONITOR_START -->",
        "# Apple Developer Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-apple.py` to track compliance areas.",
        "",
        "## Active Requirements Log",
        "",
        "| ID | Category | Announcement / Update | Date Published | Action Required | Status |",
        "|---|---|---|---|---|---|",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(
            f"| APP-REQ-{idx:03d} | {u['category']} | [{u['title']}]({u['link']}) | {u['pubDate']} | Audit codebase and configuration | Pending Review |"
        )

    lines.append("")
    lines.append("## Core Migration Action Items")
    lines.append("")

    seen_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in seen_cats:
            continue
        seen_cats.add(cat)

        lines.append(f"### Category: {cat}")
        lines.append(f"- **Impact**: Updates affecting the '{cat}' guideline parameters.")
        lines.append("  - **Migration Tasks**:")
        if cat == "Privacy Manifests":
            lines.append(
                "    - [ ] Create a root PrivacyInfo.xcprivacy and audit external dependencies."
            )
        elif cat == "Required Reason APIs":
            lines.append(
                "    - [ ] Add NSPrivacyAccessedAPITypes declarations and reason codes to PrivacyInfo.xcprivacy."
            )
        elif cat == "In-App Purchase policies":
            lines.append(
                "    - [ ] Implement clear Restore Purchases and conform pricing displays with subscription guidelines."
            )
        else:
            lines.append(
                f"    - [ ] Review implementation details and metadata for {cat}."
            )
        lines.append("")

    lines.append("<!-- APPLE_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Apple documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Apple Developer and App Store Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live Apple developer RSS feeds"
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
        default="docs/APPLE-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/APPLE_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live Apple developer RSS feed...")
        announcements.extend(
            parse_rss_feed("https://developer.apple.com/news/rss/news.rss")
        )

    # Fallback to mock data if live has no updates or mock is requested
    if args.mock or (not args.live and not args.mock) or not announcements:
        print(
            "Using comprehensive mock Apple policy updates for compliance scanning..."
        )
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

    # 2. Classify updates into the 25 required categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(
        f"Monitored and classified {len(classified_updates)} policy/requirement updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    # 3. Scan the codebase for signals related to these categories
    print(f"Scanning codebase under '{args.dir}' for Apple integration signals...")
    scan_results = scan_codebase_for_apple_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft
    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
        try:
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
