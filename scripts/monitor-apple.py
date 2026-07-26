#!/usr/bin/env python3
"""
Apple Developer Requirement Monitor
Tracks and analyzes updates to Apple developer program requirements, reviews guidelines,
APIs, and platform policies. Generates detailed migration tasks, estimates release impact,
scans the codebase for affected files, and creates comprehensive 15-section, emoji-free Pull Request drafts.
"""

import os
import sys
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import argparse

# Define the 25 Apple developer requirements with keywords, descriptions, and default affected files
APPLE_REQUIREMENTS = {
    "App Store Review Guidelines": {
        "keywords": [r"app store review guidelines", r"review guidelines", r"guideline \d", r"app review guidelines"],
        "description": "Rules governing app submission and approval on the App Store.",
        "default_affected": ["docs/APPLE.md", "data/rejection-patterns.json"],
        "actions": ["Verify review guidelines compliance", "Update docs/APPLE.md with new rules"]
    },
    "Apple Developer Program License Agreement": {
        "keywords": [r"license agreement", r"developer program license", r"adpla", r"developer agreement"],
        "description": "The legal contract between Apple and developers outlining terms and conditions.",
        "default_affected": ["docs/APPLE.md"],
        "actions": ["Review and accept updated ADPLA terms in App Store Connect"]
    },
    "Human Interface Guidelines": {
        "keywords": [r"human interface guidelines", r"hig", r"design guidelines", r"layout guidance"],
        "description": "Apple's design principles and user experience recommendations.",
        "default_affected": ["references/rules/design.md", "data/rejection-patterns.json"],
        "actions": ["Audit layout and interaction design against HIG recommendations"]
    },
    "Apple Privacy requirements": {
        "keywords": [r"privacy requirements", r"privacy labels", r"privacy nutrition", r"privacy policy", r"data collection disclosure"],
        "description": "Data collection, user disclosures, and privacy disclosure policies.",
        "default_affected": ["references/rules/privacy.md", "data/rejection-patterns.json"],
        "actions": ["Verify privacy policy URL is reachable", "Update data nutrition labels in App Store Connect"]
    },
    "Privacy Manifests": {
        "keywords": [r"privacy manifest", r"privacymanifest", r"privacyinfo\.xcprivacy", r"privacy manifest file"],
        "description": "Declarations of third-party SDK and app privacy practices in .xcprivacy files.",
        "default_affected": ["docs/ADVANCED-2026.md", "agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Audit and update PrivacyInfo.xcprivacy manifest file", "Verify third-party SDK manifests are bundled"]
    },
    "Required Reason APIs": {
        "keywords": [r"required reason api", r"required_reason_api", r"nsprivacyaccessedapitypes", r"reason codes", r"required reason"],
        "description": "APIs requiring approved justification before use to prevent fingerprinting.",
        "default_affected": ["docs/ADVANCED-2026.md", "agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Inspect usage of UserDefaults, systemUptime, or processInfo in code", "Declare approved reasons in the Privacy Manifest"]
    },
    "App Tracking Transparency": {
        "keywords": [r"app tracking transparency", r"att", r"attrackingmanager", r"nsusertrackingusagedescription", r"user tracking"],
        "description": "Framework requiring explicit user permission to track activity across apps.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Verify ATTrackingManager.requestTrackingAuthorization call is implemented", "Ensure NSUserTrackingUsageDescription is set in Info.plist"]
    },
    "Sign in with Apple": {
        "keywords": [r"sign in with apple", r"siwa", r"asauthorizationappleidprovider", r"apple sign-in"],
        "description": "Requirement to offer Apple Sign-In alongside other third-party social logins.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Ensure Sign in with Apple button is displayed alongside other social logins", "Check sign-in integration and token validation"]
    },
    "In-App Purchase policies": {
        "keywords": [r"in-app purchase", r"iap", r"storekit", r"skproduct", r"product\.purchase", r"in-app purchase policy"],
        "description": "Guidelines regarding purchasing digital items and subscriptions via StoreKit.",
        "default_affected": ["references/rules/payments.md", "agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Verify digital goods are purchased via StoreKit", "Ensure Restore Purchases button is present and functional"]
    },
    "Alternative payment regulations": {
        "keywords": [r"alternative payment", r"external link account", r"external purchase", r"alternative payment link"],
        "description": "Regulations allowing or restricting non-Apple payment methods in certain regions.",
        "default_affected": ["docs/EU-REGULATORY-2026.md", "docs/ADVANCED-2026.md", "references/rules/payments.md"],
        "actions": ["Configure entitlement for external links or alternative payments if eligible", "Implement appropriate in-app warnings and modals"]
    },
    "DMA compliance changes": {
        "keywords": [r"dma", r"digital markets act", r"core technology fee", r"ctf", r"alternative distribution", r"eu alternative distribution"],
        "description": "European Union Digital Markets Act requirements for alternative app marketplaces.",
        "default_affected": ["docs/EU-REGULATORY-2026.md", "docs/ADVANCED-2026.md"],
        "actions": ["Review Core Technology Fee (CTF) implications", "Ensure compliance with alternative distribution rules in the EU"]
    },
    "Accessibility requirements": {
        "keywords": [r"accessibility", r"voiceover", r"dynamic type", r"reduce motion", r"color contrast", r"en 301 549"],
        "description": "Rules for accessible layout design and Assistive technology support.",
        "default_affected": ["docs/EU-REGULATORY-2026.md", "references/rules/design.md"],
        "actions": ["Verify VoiceOver compatibility across main screens", "Audit layout scaling with Dynamic Type enabled", "Ensure compliance with EN 301 549 standards"]
    },
    "AI-related App Store policies": {
        "keywords": [r"ai", r"artificial intelligence", r"generative ai", r"ai-generated", r"ai policy", r"ai model"],
        "description": "Policies regarding safety, content moderation, and disclosure for AI features.",
        "default_affected": ["docs/APPLE.md", "agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Verify user consent modal naming the AI provider is active", "Implement strict content filtering and reporting features"]
    },
    "Child safety requirements": {
        "keywords": [r"child safety", r"kids category", r"coppa", r"csam", r"cgsa", r"children's online privacy protection act"],
        "description": "Compliance rules for apps directed at kids or handling children's data.",
        "default_affected": ["docs/GLOBAL-REGULATORY-2026.md", "docs/APPLE.md", "data/rejection-patterns.json"],
        "actions": ["Configure COPPA-compliant parental gate before outbound links", "Audit data transmission to ensure no children's data is leaked"]
    },
    "HealthKit policies": {
        "keywords": [r"healthkit", r"health kit", r"clinical health records", r"health app", r"health data"],
        "description": "Rules and permission structures for accessing health and fitness data.",
        "default_affected": ["data/rejection-patterns.json"],
        "actions": ["Add NSHealthShareUsageDescription and NSHealthUpdateUsageDescription in Info.plist", "Ensure clinical health data usage conforms to privacy policies"]
    },
    "Location permissions": {
        "keywords": [r"location permission", r"location access", r"cllocationmanager", r"always authorization", r"nslocation"],
        "description": "Rules and declaration guidelines for accessing user location data.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Ensure NSLocationWhenInUseUsageDescription is set in Info.plist", "Audit location requests to ensure they are triggered only when needed"]
    },
    "Camera and microphone permissions": {
        "keywords": [r"camera permission", r"microphone permission", r"avcapturedevice", r"nscamera", r"nsmicrophone"],
        "description": "Rules and strings required for camera and microphone hardware access.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Verify NSCameraUsageDescription is present and specific", "Verify NSMicrophoneUsageDescription is present and specific"]
    },
    "Push Notification requirements": {
        "keywords": [r"push notification", r"apns", r"apn", r"notification service", r"remote notification"],
        "description": "Apple Push Notification service updates and certificates.",
        "default_affected": ["data/rejection-patterns.json"],
        "actions": ["Verify APNs certificates and provisioning profiles are up to date", "Audit payload sizes and notification extensions in code"]
    },
    "Background execution policies": {
        "keywords": [r"background execution", r"background mode", r"background fetch", r"background processing", r"background tasks"],
        "description": "Requirements and APIs for executing tasks when the app is in the background.",
        "default_affected": ["data/rejection-patterns.json"],
        "actions": ["Verify background modes declared in Info.plist align with app usage", "Audit background task processing to prevent excessive background battery drain"]
    },
    "Security updates": {
        "keywords": [r"security update", r"vulnerability", r"cve", r"security patch", r"certificate pinning", r"keychain protection"],
        "description": "Important security enhancements, patches, and standard secure storage mandates.",
        "default_affected": ["data/rejection-patterns.json"],
        "actions": ["Perform a dependency security scan", "Verify secure data is written only to the iOS Keychain with strict access control"]
    },
    "SDK requirements": {
        "keywords": [r"sdk requirement", r"sdk version", r"ios sdk", r"macos sdk"],
        "description": "Announcements about specific third-party or native SDK integrations and requirements.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Identify third-party SDKs requiring mandatory updates", "Verify compiled SDK version compatibility in Xcode build configuration"]
    },
    "Minimum SDK versions": {
        "keywords": [r"minimum sdk", r"min sdk", r"target sdk", r"ios 17", r"ios 18", r"ios 19"],
        "description": "The lowest supported OS version required for submissions.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh", "data/rejection-patterns.json"],
        "actions": ["Verify deployment target is set correctly in build configurations", "Update minimum supported iOS version in CI/CD pipeline definitions"]
    },
    "Xcode requirements": {
        "keywords": [r"xcode", r"xcode version", r"xcode 15", r"xcode 16", r"xcode 17"],
        "description": "The mandatory development tools and IDE versions required for App Store builds.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh"],
        "actions": ["Upgrade build machine/CI to the required Xcode version", "Audit Xcode settings and deprecated compiler flags"]
    },
    "Swift requirements": {
        "keywords": [r"swift", r"swift 6", r"swift concurrency", r"swiftui"],
        "description": "Updates regarding language feature usage, concurrency, or package manager standards.",
        "default_affected": ["agent-os/hooks/app-store-compliance-guard.sh"],
        "actions": ["Check Swift language version and concurrency warnings in Xcode", "Audit Swift package configurations for deprecations"]
    },
    "App Store Connect announcements": {
        "keywords": [r"app store connect", r"asc", r"app submission", r"testflight", r"developer account", r"submission wizard"],
        "description": "Operational and portal interface modifications in the App Store administration.",
        "default_affected": ["docs/APPLE.md"],
        "actions": ["Review and complete new questionnaire screens in App Store Connect", "Confirm TestFlight external tester criteria updates"]
    }
}

MOCK_UPDATES = [
    {
        "title": "Enforcing Privacy Manifests and Required Reason APIs",
        "link": "https://developer.apple.com/news/?id=privacy-manifests-enforcement",
        "date": "2026-03-01",
        "description": "Starting today, all submissions to the App Store must include a Privacy Manifest (PrivacyInfo.xcprivacy) if they use any of the required reason APIs such as UserDefaults, systemUptime, or processInfo. Failure to declare these APIs or use of unapproved reasons will lead to immediate submission rejection."
    },
    {
        "title": "Alternative Payment Options and DMA Compliance in the European Union",
        "link": "https://developer.apple.com/news/?id=dma-alternative-payments",
        "date": "2026-04-10",
        "description": "In compliance with the Digital Markets Act (DMA) in the European Union, developers can now offer alternative payment methods and direct users to external links to make purchases. Applications utilizing alternative distribution or alternative payments must adhere to strict guidelines and are subject to the Core Technology Fee (CTF)."
    },
    {
        "title": "App Store Submissions Now Require Xcode 17 and Swift 6",
        "link": "https://developer.apple.com/news/?id=xcode-17-swift-6",
        "date": "2026-05-15",
        "description": "Beginning April 2026, all iOS, macOS, watchOS, and tvOS apps submitted to the App Store must be built with Xcode 17 or later, which includes the iOS 18 SDK. Developers are encouraged to adopt Swift 6 concurrency models and ensure minimum SDK version compatibility."
    },
    {
        "title": "App Review Guidelines Updated for AI Generated Content and Safety",
        "link": "https://developer.apple.com/news/?id=ai-safety-guidelines",
        "date": "2026-06-05",
        "description": "We have updated the App Store Review Guidelines with new policies regarding Artificial Intelligence (AI). Apps integrating generative AI must provide robust content moderation, offer user disclosures, and prevent the generation of harmful material, including strict child safety protections."
    },
    {
        "title": "New Accessibility Mandates under European Accessibility Act",
        "link": "https://developer.apple.com/news/?id=accessibility-eaa-2026",
        "date": "2026-06-25",
        "description": "Developers shipping apps in the European Union must comply with the European Accessibility Act (EAA) and EN 301 549 standards. Apps must fully support accessibility features including VoiceOver, Dynamic Type, and Reduce Motion, ensuring assistive technologies work seamlessly."
    },
    {
        "title": "Apple Developer Program License Agreement Update and App Store Connect Enhancements",
        "link": "https://developer.apple.com/news/?id=adpla-asc-update",
        "date": "2026-02-15",
        "description": "The Apple Developer Program License Agreement (ADPLA) has been updated to reflect new operational changes. Developers must accept the new terms in the App Store Connect portal, which also features a redesigned submission wizard and TestFlight improvements."
    },
    {
        "title": "Privacy Updates for Location, Camera, Microphone, and App Tracking Transparency",
        "link": "https://developer.apple.com/news/?id=privacy-att-permissions",
        "date": "2026-03-20",
        "description": "New privacy protections require explicit permission strings for camera, microphone, and location access. Developers using tracking identifiers must implement App Tracking Transparency (ATT) using ATTrackingManager and specify usage descriptions."
    },
    {
        "title": "Security Enhancements, Push Notifications, and Background Execution Policies",
        "link": "https://developer.apple.com/news/?id=security-notifications-background",
        "date": "2026-04-05",
        "description": "Security updates mandate certificate pinning for high-security endpoints. Additionally, APNs push notification requirements have been tightened, and background execution policies now enforce strict runtime limits on background fetch and processing tasks."
    },
    {
        "title": "Integrating HealthKit and Human Interface Guidelines for iOS 18",
        "link": "https://developer.apple.com/news/?id=healthkit-hig-ios18",
        "date": "2026-05-01",
        "description": "New design layouts in the Human Interface Guidelines (HIG) introduce specific standards for fitness apps. Developers integrating HealthKit must comply with clinical health records sharing policies and use Apple-approved layouts."
    }
]


def scan_codebase_for_keywords(keywords):
    """
    Statically scans the repository files for keywords to identify affected codebase locations.
    """
    affected = []
    exclude_dirs = {".git", "node_modules", "Pods", "build", "DerivedData", "vendor"}
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in {".py", ".json", ".md", ".sh", ".swift", ".plist", ".gradle", ".xml", ".txt"}:
                filepath = os.path.relpath(os.path.join(root, f), ".")
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as file_handle:
                        content = file_handle.read()
                        for kw in keywords:
                            if re.search(kw, content, re.IGNORECASE):
                                affected.append(filepath)
                                break
                except Exception:
                    pass
    return sorted(list(set(affected)))


def determine_release_impact(requirements):
    """
    Establishes the release impact (critical, high, medium, low) and explanation.
    """
    # If any matched requirement has sensitive or block-critical items, mark as critical
    critical_triggers = {"Required Reason APIs", "Privacy Manifests", "In-App Purchase policies",
                         "Sign in with Apple", "Location permissions", "Camera and microphone permissions"}
    high_triggers = {"App Store Review Guidelines", "Apple Developer Program License Agreement",
                     "App Tracking Transparency", "Alternative payment regulations", "DMA compliance changes",
                     "Security updates", "Child safety requirements", "Minimum SDK versions", "Xcode requirements"}

    matched_set = set(requirements)
    if matched_set.intersection(critical_triggers):
        return "Critical", "The update affects features that could trigger immediate automatic upload rejection or app submission blocks."
    elif matched_set.intersection(high_triggers):
        return "High", "The update involves regulatory, legal, or review guidelines changes that could result in rejection during human review."
    else:
        return "Medium", "The update involves design, accessibility, language, or connective updates requiring alignment but unlikely to cause automated rejections."


def sanitize_filename(name):
    """
    Sanitizes string for use in filenames.
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower())


def generate_pull_request_draft(update, matched_requirements, affected_files, release_impact, release_explanation):
    """
    Generates a draft pull request matching the 15 required sections in an emoji-free format.
    """
    reqs_str = ", ".join(matched_requirements)
    files_list_str = "\n".join([f"- {f}: This file matches keywords of the updated requirements." for f in affected_files])
    if not files_list_str:
        files_list_str = "- No directly matching source files were found; check if updates should be integrated in new files."

    tasks_str = ""
    impl_checklist = ""
    for r in matched_requirements:
        actions = APPLE_REQUIREMENTS.get(r, {}).get("actions", ["Align codebase with the new requirement"])
        for act in actions:
            tasks_str += f"- Implement: {act}\n"
            impl_checklist += f"- [ ] {act}\n"

    citation_link = update["link"]

    pr_text = f"""# Compliance Update: {update["title"]}

## Summary
This pull request drafts the necessary repository adjustments to address Apple's recent policy update: "{update["title"]}". This update has been classified with a Release Impact of {release_impact}.

## Background
Apple regularly updates its requirements, guidelines, and agreements to maintain user privacy, enhance platform stability, and respond to regulatory shifts. This background context details the operational motivation behind the policy "{update["title"]}" and its intersection with developers' obligations.

## Regulatory change
The core change involves the following updated Apple developer program requirements:
{reqs_str}

Specifically, Apple has modified policy thresholds or introduced new validation mandates which developers must satisfy to avoid service disruption or review failures.

## Official citations
According to the official announcement published by Apple Developer News:
Citation Link: {citation_link}
Publication Date: {update["date"]}
" {update["description"]} "

## Affected files
The following repository locations are identified as affected or relevant to this compliance update:
{files_list_str}

## Risk assessment
Failure to address this update carries the following technical and operational risks:
- Severity level: {release_impact}
- Primary risk: {release_explanation}
- Direct consequences include automated binary upload rejections, review delays, app suspension, or potential developer account flags.

## Migration steps
To achieve full compliance, perform the following step-by-step migration:
1. Review the official announcement details at the cited URL.
2. Inspect the identified affected files and locate relevant configurations.
3. Apply the specific code or configuration adjustments listed in the implementation checklist.
4. Regenerate local build configurations and verify local compilation.
5. Run automated compliance lints or pre-submission guard checks.

## Backward compatibility
This compliance change has been analyzed for backward compatibility:
- Support for older iOS/macOS client versions remains stable unless specifically noted otherwise.
- Configuration adjustments (such as adding key-value entries to plist files or manifests) are safe and do not degrade functionality on older runtimes.

## Implementation checklist
Complete the following implementation items:
{impl_checklist}- [ ] Verify compliance version numbers match Apple minimum specifications
- [ ] Clean up any legacy or deprecated API endpoints in conflict with this update

## Testing checklist
Execute the following verification and validation steps:
- [ ] Build the application locally with target SDKs
- [ ] Run automated compliance scripts such as scripts/validate.py
- [ ] Perform a clean build and upload to TestFlight to verify submission pipelines
- [ ] Test the affected features on a physical device running the target OS version

## Documentation checklist
Update the following documentation assets:
- [ ] Record compliance changes in docs/APPLE-POLICY-MIGRATION.md
- [ ] Update inline code comments to explain compliance-driven configurations
- [ ] Revise the relevant sections of references/ or playbooks if guidelines have altered

## Compliance impact
This update relates to broader compliance domains:
- Jurisdictional alignment: Ensures the application complies with regional requirements, data privacy principles, and global consumer trust frameworks.

## Breaking changes
No structural breaking changes to public APIs are expected from this update unless specified in the announcement. Existing user databases, credentials, and app states are preserved.

## Review checklist
Reviewers must confirm the following before approval:
- [ ] All 15 required sections of this pull request are comprehensive and complete.
- [ ] Code adjustments align strictly with Priority 1 official sources.
- [ ] No emojis or graphical symbols have been introduced in the PR, documentation, or code.

## Approver recommendations
The following roles are recommended to sign off and approve this compliance pull request:
- Lead iOS Development Engineer: To verify build, runtime, and SDK configuration safety.
- Compliance and Privacy Officer: To verify compliance with global policies and official standards.
- QA Technical Lead: To confirm successful testing on target physical devices.
"""
    return pr_text


def update_policy_migration_file(history):
    """
    Rebuilds the history file docs/APPLE-POLICY-MIGRATION.md based on parsed updates history.
    """
    os.makedirs("docs", exist_ok=True)
    filepath = "docs/APPLE-POLICY-MIGRATION.md"

    content_lines = [
        "# Apple Policy Migration History",
        "",
        "This document tracks changes to Apple Developer Program requirements and App Store compliance policies.",
        "It is updated automatically by the Apple Developer Requirement Monitor.",
        "",
        "## Summary of Tracked Updates",
        ""
    ]

    # Table of updates
    content_lines.append("| Date | Update Title | Impact | Requirements | Status |")
    content_lines.append("|---|---|---|---|---|")
    for item in sorted(history, key=lambda x: x["date"], reverse=True):
        reqs = ", ".join(item["requirements"])
        content_lines.append(f"| {item['date']} | {item['title']} | {item['impact']} | {reqs} | Logged |")

    content_lines.append("")
    content_lines.append("## Detailed Update Logs")
    content_lines.append("")

    for item in sorted(history, key=lambda x: x["date"], reverse=True):
        content_lines.append(f"### {item['title']}")
        content_lines.append(f"- **Announcement Date:** {item['date']}")
        content_lines.append(f"- **Official Citation:** [{item['link']}]({item['link']})")
        content_lines.append(f"- **Estimated Release Impact:** {item['impact']} - {item['impact_reason']}")
        content_lines.append("- **Triggered Apple Requirements:**")
        for req in item["requirements"]:
            content_lines.append(f"  - {req}")
        content_lines.append("- **Affected Codebase Files:**")
        if item["affected_files"]:
            for f in item["affected_files"]:
                content_lines.append(f"  - `{f}`")
        else:
            content_lines.append("  - None detected")

        content_lines.append("- **Generated Migration Tasks:**")
        for task in item["tasks"]:
            content_lines.append(f"  - {task}")
        content_lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines) + "\n")


def parse_feed(source):
    """
    Parses live or local feed. Returns a list of updates dicts.
    Handles both Atom and RSS formats.
    """
    updates = []

    # Check if source is a URL or a file
    if source.startswith("http://") or source.startswith("https://"):
        try:
            print(f"Fetching feed from live URL: {source}")
            req = urllib.request.Request(
                source,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple Developer Requirement Monitor/1.0'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                xml_data = response.read()
        except Exception as e:
            print(f"Error fetching live feed: {e}")
            return []
    else:
        if not os.path.exists(source):
            print(f"Feed file not found: {source}")
            return []
        print(f"Reading feed from local file: {source}")
        with open(source, "rb") as f:
            xml_data = f.read()

    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Error parsing XML feed: {e}")
        return []

    # Check for Atom format
    # Atom namespaces are common, so we find tags without namespace
    namespace = ""
    m = re.match(r'({[^}]+})', root.tag)
    if m:
        namespace = m.group(1)

    # Is it Atom?
    if 'feed' in root.tag.lower():
        print("Detected Atom Feed format.")
        for entry in root.findall(f"./{namespace}entry"):
            title_node = entry.find(f"./{namespace}title")
            title = title_node.text if title_node is not None else ""

            link_node = entry.find(f"./{namespace}link")
            link = ""
            if link_node is not None:
                link = link_node.attrib.get("href", "")

            summary_node = entry.find(f"./{namespace}summary")
            if summary_node is None:
                summary_node = entry.find(f"./{namespace}content")
            description = summary_node.text if summary_node is not None else ""

            updated_node = entry.find(f"./{namespace}updated")
            date_str = updated_node.text if updated_node is not None else datetime.now().strftime("%Y-%m-%d")
            # Parse standard ISO timestamp to YYYY-MM-DD
            if date_str and len(date_str) >= 10:
                date_str = date_str[:10]

            updates.append({
                "title": title.strip() if title else "",
                "link": link.strip() if link else "",
                "date": date_str,
                "description": description.strip() if description else ""
            })

    # Is it RSS?
    elif 'rss' in root.tag.lower() or root.find(".//item") is not None:
        print("Detected RSS Feed format.")
        for item in root.findall(".//item"):
            title_node = item.find("title")
            title = title_node.text if title_node is not None else ""

            link_node = item.find("link")
            link = link_node.text if link_node is not None else ""

            desc_node = item.find("description")
            description = desc_node.text if desc_node is not None else ""

            pub_node = item.find("pubDate")
            date_str = pub_node.text if pub_node is not None else datetime.now().strftime("%Y-%m-%d")
            # Attempt to parse RSS pubDate e.g. "Mon, 15 Jun 2026 10:00:00 PDT"
            try:
                # Basic parsing or fallback to current date
                if pub_node is not None and pub_node.text:
                    parts = pub_node.text.split()
                    if len(parts) >= 4:
                        # parts[1] is day, parts[2] is month name, parts[3] is year
                        day = parts[1].zfill(2)
                        months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                                  "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
                        month = months.get(parts[2][:3], "01")
                        year = parts[3]
                        date_str = f"{year}-{month}-{day}"
            except Exception:
                date_str = datetime.now().strftime("%Y-%m-%d")

            updates.append({
                "title": title.strip() if title else "",
                "link": link.strip() if link else "",
                "date": date_str,
                "description": description.strip() if description else ""
            })

    else:
        print("Unknown feed format, attempting flat search.")
        # Fallback flat elements check
        for item in root.iter():
            if 'item' in item.tag or 'entry' in item.tag:
                # parse best effort
                pass

    return updates


def main():
    parser = argparse.ArgumentParser(description="Apple Developer Requirement Monitor")
    parser.add_argument("--feed", help="URL or file path to live RSS/Atom feed.")
    parser.add_argument("--mock", action="store_true", help="Run with realistic pre-baked mock Apple updates.")
    parser.add_argument("--force", action="store_true", help="Force reprocessing of all updates even if already logged.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging output.")

    args = parser.parse_args()

    # Load persistent history state to avoid duplication
    history_file = "data/apple-policy-history.json"
    os.makedirs("data", exist_ok=True)

    history_state = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history_state = json.load(f)
        except Exception as e:
            print(f"Error loading history file, starting clean: {e}")

    processed_links = {item["link"] for item in history_state}

    # Determine the input source of updates
    updates_to_process = []
    if args.mock:
        print("Using built-in Apple mock updates.")
        updates_to_process = MOCK_UPDATES
    elif args.feed:
        updates_to_process = parse_feed(args.feed)
    else:
        # Default fallback to mock to make manual runs simple
        print("No feed or mock argument specified. Defaulting to mock updates run.")
        updates_to_process = MOCK_UPDATES

    if not updates_to_process:
        print("No updates found to process.")
        return 0

    print(f"Total updates retrieved: {len(updates_to_process)}")

    new_processed_count = 0

    for update in updates_to_process:
        link = update["link"]
        if link in processed_links and not args.force:
            if args.verbose:
                print(f"Skipping already processed update: {update['title']}")
            continue

        print(f"\nProcessing: {update['title']} ({update['date']})")

        # Analyze content to match any of the 25 requirements
        matched_requirements = []
        combined_text = (update["title"] + " " + update["description"]).lower()

        for req_name, info in APPLE_REQUIREMENTS.items():
            for kw in info["keywords"]:
                if re.search(kw, combined_text):
                    matched_requirements.append(req_name)
                    break

        if not matched_requirements:
            if args.verbose:
                print(f"No monitored Apple developer requirements triggered for: {update['title']}")
            continue

        print(f"Matched Requirements: {', '.join(matched_requirements)}")

        # Perform static scanning to identify affected files
        all_keywords = []
        for req in matched_requirements:
            all_keywords.extend(APPLE_REQUIREMENTS[req]["keywords"])

        affected_files = scan_codebase_for_keywords(all_keywords)
        # Also always include the default affected files declared for each matched requirement
        for req in matched_requirements:
            for df in APPLE_REQUIREMENTS[req]["default_affected"]:
                if os.path.exists(df) and df not in affected_files:
                    affected_files.append(df)

        affected_files = sorted(list(set(affected_files)))
        print(f"Affected Files count: {len(affected_files)}")
        if args.verbose:
            for f in affected_files:
                print(f"  - {f}")

        # Determine release impact and explanation
        release_impact, impact_explanation = determine_release_impact(matched_requirements)
        print(f"Release Impact: {release_impact} - {impact_explanation}")

        # Generate Migration Tasks
        migration_tasks = []
        for req in matched_requirements:
            migration_tasks.extend(APPLE_REQUIREMENTS[req]["actions"])
        migration_tasks = sorted(list(set(migration_tasks)))

        # Generate the Pull Request Draft
        pr_text = generate_pull_request_draft(
            update, matched_requirements, affected_files, release_impact, impact_explanation
        )

        # Write Pull Request Draft to a specific file
        sanitized_title = sanitize_filename(update["title"])
        pr_filename = f"docs/apple_pr_draft_{sanitized_title}.md"
        with open(pr_filename, "w", encoding="utf-8") as pr_file:
            pr_file.write(pr_text)
        print(f"Draft Pull Request written to: {pr_filename}")

        # Also save latest compliance PR draft as a stable default filename
        with open("docs/APPLE_COMPLIANCE_PR_DRAFT.md", "w", encoding="utf-8") as latest_pr_file:
            latest_pr_file.write(pr_text)

        # Update/log into persistent state list
        # If already existed, update. If not, append.
        existing_index = next((i for i, item in enumerate(history_state) if item["link"] == link), -1)
        update_record = {
            "title": update["title"],
            "link": link,
            "date": update["date"],
            "requirements": matched_requirements,
            "affected_files": affected_files,
            "impact": release_impact,
            "impact_reason": impact_explanation,
            "tasks": migration_tasks,
            "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if existing_index != -1:
            history_state[existing_index] = update_record
        else:
            history_state.append(update_record)

        new_processed_count += 1

    if new_processed_count > 0 or args.force:
        # Re-save persistent state
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history_state, f, indent=2)

        # Rebuild the documentation log
        update_policy_migration_file(history_state)
        print(f"\nSuccessfully processed {new_processed_count} new updates and updated docs/APPLE-POLICY-MIGRATION.md")
    else:
        print("\nNo new updates to log.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
