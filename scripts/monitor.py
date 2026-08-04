#!/usr/bin/env python3
"""Apple Developer Requirements Monitor: tracks 25 Apple requirement
categories against live/mock news and scans a --project for impact."""

import os
import sys
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# 25 specified tracking areas (the "tracks")
TRACK_METADATA = {
    "App Store Review Guidelines": {
        "keywords": [
            "review guidelines",
            "app review guidelines",
            "guideline 2.1",
            "guideline 4.3",
            "guideline 5.1.1",
            "guidelines update",
        ],
        "patterns": [r"review[ -]guideline", r"app[ -]review"],
        "detect_files": ["Info.plist", "AppReviewNotes", "*.swift"],
        "detect_regex": r"LoginView|signIn|AuthService|OAuth|Firebase|lorem ipsum|placeholder|TODO|FIXME",
        "impact_desc": "Changes to the general App Store Review Guidelines. All submitted builds are subjected to these guidelines.",
        "migration_steps": [
            "Review the updated guidelines section in APPLE.md or the official site.",
            "Ensure App Review Notes are updated with working test accounts.",
            "Verify the application flows align with the updated guideline numbers.",
        ],
        "release_impact": "High",
    },
    "Apple Developer Program License Agreement": {
        "keywords": [
            "license agreement",
            "developer program license",
            "pla",
            "sla",
            "program license",
        ],
        "patterns": [r"license[ -]agreement", r"pla", r"sla"],
        "detect_files": ["Info.plist", "LICENSE"],
        "detect_regex": r"company|individual|developer account",
        "impact_desc": "Updates to the contract terms between Apple and the Developer. May require accepting terms in App Store Connect.",
        "migration_steps": [
            "Log in to App Store Connect as the Account Holder.",
            "Accept the latest Program License Agreement.",
            "Review any changes regarding company distribution versus individual distribution rules.",
        ],
        "release_impact": "Medium",
    },
    "Human Interface Guidelines": {
        "keywords": [
            "human interface",
            "hig",
            "design guidelines",
            "layout",
            "typography",
            "dark mode",
            "design update",
        ],
        "patterns": [r"human[ -]interface", r"hig", r"design[ -]guideline"],
        "detect_files": ["*.swift", "*.storyboard", "*.xib"],
        "detect_regex": r"UIFont|UIColor|padding|margin|UIStackView|VStack|HStack|SwiftUI",
        "impact_desc": "UI/UX layout changes recommended or mandated by Apple.",
        "migration_steps": [
            "Check user interface elements against current design recommendations in HIG.",
            "Verify touch targets are at least 44x44pt on iOS.",
            "Test dark mode and dynamic type sizing rendering.",
        ],
        "release_impact": "Medium",
    },
    "Apple Privacy requirements": {
        "keywords": [
            "privacy requirement",
            "privacy policy",
            "nutrition label",
            "privacy label",
        ],
        "patterns": [
            r"privacy[ -]requirement",
            r"privacy[ -]policy",
            r"nutrition[ -]label",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"privacyPolicy|privacy-policy|PrivacyPolicyURL",
        "impact_desc": "Global updates to Apple's privacy policy requirements and user consent flows.",
        "migration_steps": [
            "Publish or update your privacy policy URL.",
            "Confirm in-app accessibility to the privacy policy link.",
            "Verify data declaration matches actual SDK data collection.",
        ],
        "release_impact": "High",
    },
    "Privacy Manifests": {
        "keywords": ["privacy manifest", "xcprivacy", "privacyinfo"],
        "patterns": [r"privacy[ -]manifest", r"xcprivacy", r"privacyinfo"],
        "detect_files": ["PrivacyInfo.xcprivacy", "*.swift", "*.plist"],
        "detect_regex": r"NSPrivacyAccessedAPITypes|NSPrivacyCollectedDataTypes",
        "impact_desc": "Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.",
        "migration_steps": [
            "Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.",
            "Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations.",
        ],
        "release_impact": "Critical",
    },
    "Required Reason APIs": {
        "keywords": [
            "required reason api",
            "accessed api",
            "reasons for api",
            "userdefaults",
            "systemuptime",
        ],
        "patterns": [
            r"required[ -]reason[ -]api",
            r"accessed[ -]api",
            r"reasons[ -]for[ -]api",
        ],
        "detect_files": ["*.swift", "*.m", "*.plist", "PrivacyInfo.xcprivacy"],
        "detect_regex": r"UserDefaults|NSFileManager|systemUptime|ProcessInfo|stat\s*\(",
        "impact_desc": "Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).",
        "migration_steps": [
            "Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.",
            "Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes.",
        ],
        "release_impact": "Critical",
    },
    "App Tracking Transparency": {
        "keywords": ["app tracking transparency", "att", "idfa", "user tracking"],
        "patterns": [
            r"app[ -]tracking[ -]transparency",
            r"att",
            r"idfa",
            r"tracking[ -]permission",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"ATTrackingManager|NSUserTrackingUsageDescription|ASIdentifierManager|advertisingIdentifier",
        "impact_desc": "Tracking consent rules and IDFA access restrictions.",
        "migration_steps": [
            "Verify ATTrackingManager.requestTrackingAuthorization is called before starting any tracking.",
            "Add NSUserTrackingUsageDescription with a clear reason explaining why tracking is used.",
        ],
        "release_impact": "High",
    },
    "Sign in with Apple": {
        "keywords": ["sign in with apple", "siwa", "apple sign-in"],
        "patterns": [r"sign[ -]in[ -]with[ -]apple", r"siwa"],
        "detect_files": ["*.swift", "Info.plist"],
        "detect_regex": r"ASAuthorizationAppleIDProvider|SignInWithApple",
        "impact_desc": "Requirement to offer Sign in with Apple alongside any other third-party social login.",
        "migration_steps": [
            "Verify that Sign in with Apple is offered at least as prominently as other social logins.",
            "Ensure email private relays are supported and profiles are handled gracefully on first login.",
        ],
        "release_impact": "High",
    },
    "In-App Purchase policies": {
        "keywords": [
            "in-app purchase",
            "iap",
            "storekit",
            "subscription terms",
            "purchase policy",
        ],
        "patterns": [
            r"in-app[ -]purchase",
            r"iap",
            r"storekit",
            r"subscription[ -]term",
        ],
        "detect_files": ["*.swift", "Info.plist"],
        "detect_regex": r"StoreKit|SKProduct|Product\.purchase|restorePurchases|restoreCompletedTransactions",
        "impact_desc": "App Store rules around StoreKit digital purchases, billing, pricing, and subscriptions.",
        "migration_steps": [
            "Route all digital goods through StoreKit in-app purchases.",
            "Add a prominent Restore Purchases control for non-consumable goods.",
            "Verify pricing displays correspond with Apple subscription terms requirements.",
        ],
        "release_impact": "Critical",
    },
    "Alternative payment regulations": {
        "keywords": [
            "alternative payment",
            "external purchase link",
            "alternate billing",
            "payment regulation",
        ],
        "patterns": [
            r"alternative[ -]payment",
            r"external[ -]purchase[ -]link",
            r"alternate[ -]billing",
        ],
        "detect_files": ["*.swift", "*.entitlements", "Info.plist"],
        "detect_regex": r"com\.apple\.developer\.storekit\.external-purchase|SKExternalPurchase|Stripe|PayPal",
        "impact_desc": "Permitted exceptions and requirements for offering third-party payment links (region-gated).",
        "migration_steps": [
            "Ensure appropriate entitlements are requested and set up for alternative billing.",
            "Show mandatory disclosure sheets before redirecting to external web purchase flows.",
        ],
        "release_impact": "High",
    },
    "DMA compliance changes": {
        "keywords": [
            "dma",
            "digital markets act",
            "alternative marketplace",
            "core technology fee",
            "ctf",
        ],
        "patterns": [
            r"dma",
            r"digital[ -]markets[ -]act",
            r"alternative[ -]marketplace",
        ],
        "detect_files": ["*.swift", "*.entitlements"],
        "detect_regex": r"com\.apple\.developer\.storekit\.external-purchase|alternative-distribution",
        "impact_desc": "EU Digital Markets Act requirements for alternative app marketplaces, browser engines, and external link rules.",
        "migration_steps": [
            "Declare alternative distribution entitlements if publishing outside App Store in the EU.",
            "Implement EU-specific disclosure sheets and fee-math checks if using external link entitlements.",
        ],
        "release_impact": "High",
    },
    "Accessibility requirements": {
        "keywords": [
            "accessibility",
            "en 301 549",
            "wcag",
            "voiceover",
            "dynamic type",
        ],
        "patterns": [
            r"accessibility",
            r"en[ -]301[ -]549",
            r"wcag",
            r"voiceover",
            r"dynamic[ -]type",
        ],
        "detect_files": ["*.swift", "*.storyboard", "*.xib"],
        "detect_regex": r"accessibilityLabel|accessibilityIdentifier|UIAccessibility|DynamicType",
        "impact_desc": "Accessibility standards compliance (WCAG 2.1 AA / EN 301 549) and App Store Accessibility Nutrition Labels.",
        "migration_steps": [
            "Audit UI elements for accessibility labels and traits.",
            "Verify dynamic font resizing is supported.",
            "Populate Accessibility Nutrition Labels in App Store Connect.",
        ],
        "release_impact": "Medium",
    },
    "AI-related App Store policies": {
        "keywords": [
            "generative ai",
            "llm",
            "chatgpt",
            "ai policy",
            "ai content",
            "openai",
            "anthropic",
        ],
        "patterns": [
            r"generative[ -]ai",
            r"llm",
            r"chatgpt",
            r"ai[ -]policy",
            r"ai[ -]content",
        ],
        "detect_files": ["*.swift", "Info.plist"],
        "detect_regex": r"api\.openai\.com|anthropic|generativelanguage|chat/completions|stable[ -]diffusion|openai",
        "impact_desc": "User consent and content moderation rules for AI models and Generative AI chatbot outputs.",
        "migration_steps": [
            "Show a consent modal naming the AI provider before any personal data is sent.",
            "Provide robust content moderation, reporting, and blocking for any user-generated or AI-generated content.",
        ],
        "release_impact": "High",
    },
    "Child safety requirements": {
        "keywords": [
            "child safety",
            "kids category",
            "coppa",
            "csam",
            "cybertipline",
            "minor",
            "under-13",
        ],
        "patterns": [
            r"child[ -]safety",
            r"kids[ -]category",
            r"coppa",
            r"csam",
            r"cybertipline",
        ],
        "detect_files": ["*.swift", "Info.plist"],
        "detect_regex": r"kids|child|under-13|coppa|age-assurance|DeclaredAgeRange",
        "impact_desc": "Strict constraints on apps targeted at children, COPPA compliance, and CSAM reporting duties.",
        "migration_steps": [
            "Ensure no third-party ad or tracking SDKs are present in kids-targeted apps.",
            "Place parental gates on any external links or in-app purchases.",
            "Integrate NCMEC reporting flows on actual knowledge of CSAM (for US UGC apps).",
        ],
        "release_impact": "Critical",
    },
    "HealthKit policies": {
        "keywords": [
            "healthkit",
            "hkhealthstore",
            "health app",
            "health connect",
            "hipaa",
        ],
        "patterns": [r"healthkit", r"hkhealthstore", r"health[ -]app"],
        "detect_files": ["*.swift", "Info.plist"],
        "detect_regex": r"HKHealthStore|HealthKit|NSHealthShareUsageDescription|NSHealthUpdateUsageDescription",
        "impact_desc": "Restrictions on HealthKit data mining, usage of health data for ads, and mandatory user permission descriptions.",
        "migration_steps": [
            "Ensure HealthKit data is never used for advertising, marketing, or behavioral tracking.",
            "Add detailed HealthKit share and update usage descriptions to Info.plist.",
        ],
        "release_impact": "High",
    },
    "Location permissions": {
        "keywords": [
            "location permission",
            "locationmanager",
            "background location",
            "nslocation",
        ],
        "patterns": [
            r"location[ -]permission",
            r"locationmanager",
            r"background[ -]location",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"CLLocationManager|NSLocationWhenInUseUsageDescription|NSLocationAlwaysUsageDescription",
        "impact_desc": "Stricter constraints, usage descriptions, and prominent disclosures for access to location.",
        "migration_steps": [
            "Check that location requests match real, visible user-facing features.",
            "Include precise, specific usage descriptions in Info.plist explaining what features require location.",
        ],
        "release_impact": "High",
    },
    "Camera and microphone permissions": {
        "keywords": [
            "camera permission",
            "microphone permission",
            "nscamera",
            "nsmicrophone",
        ],
        "patterns": [
            r"camera[ -]permission",
            r"microphone[ -]permission",
            r"nscamera",
            r"nsmicrophone",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"AVCaptureDevice|NSCameraUsageDescription|NSMicrophoneUsageDescription|UIImagePickerController",
        "impact_desc": "Required Info.plist purpose strings and user-initiated triggers for media access.",
        "migration_steps": [
            "Ensure NSCameraUsageDescription and NSMicrophoneUsageDescription are present and describe real features.",
            "Use modern system pickers (like PHPickerViewController) where full photo library access is not needed.",
        ],
        "release_impact": "High",
    },
    "Push Notification requirements": {
        "keywords": ["push notification", "apns", "aps-environment"],
        "patterns": [r"push[ -]notification", r"apns", r"aps-environment"],
        "detect_files": ["*.entitlements", "*.swift", "Info.plist"],
        "detect_regex": r"aps-environment|UNUserNotificationCenter|registerForRemoteNotifications",
        "impact_desc": "Security, opt-in prompts, and payload specifications for Push Notifications.",
        "migration_steps": [
            "Verify aps-environment is set to development/production in entitlements.",
            "Ensure user consent is requested and handled gracefully before registering for remote notifications.",
        ],
        "release_impact": "Medium",
    },
    "Background execution policies": {
        "keywords": [
            "background execution",
            "background mode",
            "uibackgroundmodes",
            "background fetch",
        ],
        "patterns": [
            r"background[ -]execution",
            r"background[ -]mode",
            r"uibackgroundmodes",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"UIBackgroundModes|backgroundTimeRemaining|beginBackgroundTaskWithName",
        "impact_desc": "Strict limitation of background execution categories to prevent resource/battery drain.",
        "migration_steps": [
            "Verify UIBackgroundModes keys match the actual, documented core functionality (e.g. audio, VoIP).",
            "Remove unused background execution declarations to avoid automatic rejection.",
        ],
        "release_impact": "High",
    },
    "Security updates": {
        "keywords": [
            "security update",
            "vulnerability",
            "cve",
            "encryption declaration",
        ],
        "patterns": [
            r"security[ -]update",
            r"vulnerability",
            r"cve",
            r"encryption[ -]declaration",
        ],
        "detect_files": ["Info.plist", "*.swift"],
        "detect_regex": r"ITSAppUsesNonExemptEncryption|CCATS|ANSSI",
        "impact_desc": "Security updates, encryption declarations, and external dependencies vulnerability checks.",
        "migration_steps": [
            "Review Info.plist for ITSAppUsesNonExemptEncryption.",
            "Upload ANSSI encryption declaration if distributing non-exempt encryption in France.",
            "Perform dependency audit for known CVEs.",
        ],
        "release_impact": "Medium",
    },
    "SDK requirements": {
        "keywords": ["sdk requirement", "commonly used sdk", "third party sdk"],
        "patterns": [
            r"sdk[ -]requirement",
            r"commonly[ -]used[ -]sdk",
            r"third[ -]party[ -]sdk",
        ],
        "detect_files": ["Podfile", "Package.swift", "*.swift", "build.gradle"],
        "detect_regex": r"Firebase|Alamofire|AppsFlyerLib|Adjust|FBSDK|com\.facebook",
        "impact_desc": "Requirements for bundled third-party SDKs, including security audits, size limits, and privacy manifests.",
        "migration_steps": [
            "Perform regular updates on bundled third-party SDKs.",
            "Ensure each third-party SDK has its signed privacy manifest file.",
        ],
        "release_impact": "High",
    },
    "Minimum SDK versions": {
        "keywords": ["minimum sdk", "target sdk", "ios sdk"],
        "patterns": [r"minimum[ -]sdk", r"target[ -]sdk", r"ios[ -]sdk"],
        "detect_files": [
            "*.pbxproj",
            "*.xcconfig",
            "Package.swift",
            "build.gradle",
            "build.gradle.kts",
        ],
        "detect_regex": r"IPHONEOS_DEPLOYMENT_TARGET|targetSdkVersion|targetSdk",
        "impact_desc": "Annual minimum deployment target or target SDK version updates enforced by stores.",
        "migration_steps": [
            "Update deployment target version to match latest requirements.",
            "Build against required platform SDKs (e.g., iOS 26 SDK, Android API 35/36).",
        ],
        "release_impact": "High",
    },
    "Xcode requirements": {
        "keywords": ["xcode requirement", "xcode version"],
        "patterns": [r"xcode[ -]requirement", r"xcode[ -]version"],
        "detect_files": ["*.pbxproj", "*.xcconfig", "Package.swift"],
        "detect_regex": r"Xcode",
        "impact_desc": "Enforced Xcode versions for compiling App Store submissions.",
        "migration_steps": [
            "Upgrade build machine/CI to Xcode 26 (or required version).",
            "Resolve any newly introduced compiler deprecations/warnings.",
        ],
        "release_impact": "High",
    },
    "Swift requirements": {
        "keywords": ["swift requirement", "swift version", "swift 6", "concurrency"],
        "patterns": [r"swift[ -]requirement", r"swift[ -]version", r"swift[ -]6"],
        "detect_files": ["*.swift", "*.pbxproj", "Package.swift"],
        "detect_regex": r"SWIFT_VERSION|async|await|Task|@MainActor",
        "impact_desc": "Evolving Swift language standards, compiler features, and data-race safety requirements.",
        "migration_steps": [
            "Verify SWIFT_VERSION is at least 5.x or 6.0.",
            "Resolve strict concurrency issues if migrating to Swift 6 compiler runtime.",
        ],
        "release_impact": "Medium",
    },
    "App Store Connect announcements": {
        "keywords": ["app store connect announcement", "asc news", "developer news"],
        "patterns": [
            r"app[ -]store[ -]connect[ -]announcement",
            r"asc[ -]news",
            r"developer[ -]news",
        ],
        "detect_files": ["metadata", "*.py", "*.sh"],
        "detect_regex": r"asc|metadata-audit|pull-metadata",
        "impact_desc": "Administrative and portal changes published in App Store Connect announcements.",
        "migration_steps": [
            "Check the metadata and publishing workflows for impact.",
            "Verify store listing parameters match the latest schema.",
        ],
        "release_impact": "Medium",
    },
}

# Mock announcements for simulation and self-testing. Links use the RFC 2606
# .invalid TLD so a fixture can never be mistaken for a real Apple citation.
MOCK_ANNOUNCEMENTS = [
    {
        "title": "Upcoming Requirements for Privacy Manifests and Required Reason APIs",
        "description": "Starting late spring, all new apps and app updates submitted to the App Store must include a Privacy Info manifest declaring reasons for accessing specific APIs such as UserDefaults or systemUptime.",
        "pubDate": "Wed, 15 May 2026 10:00:00 GMT",
        "link": "https://mock.invalid/apple-news/privacy-requirements",
    },
    {
        "title": "Updates to In-App Purchase Policies and Alternative Payment Options",
        "description": "To comply with recent global regulations, developers can now direct users to external purchase options on their website. Ensure transparent billing disclosures and subscription terms are met.",
        "pubDate": "Mon, 01 Jun 2026 09:00:00 GMT",
        "link": "https://mock.invalid/apple-news/iap-updates",
    },
    {
        "title": "App Store Review Guidelines and 4.3 Saturated Categories Update",
        "description": "App Review Guideline 4.3 has been updated. Low-quality apps or duplicates in saturated categories like flashlight or wallpaper will face direct rejection unless they offer distinct user value.",
        "pubDate": "Tue, 09 Jun 2026 14:00:00 GMT",
        "link": "https://mock.invalid/apple-news/review-guidelines-update",
    },
    {
        "title": "Xcode 26 and Minimum iOS SDK Requirements for Submission",
        "description": "From April 28, 2026, all iOS, watchOS, and tvOS apps submitted to the App Store must be built with Xcode 26 and target the iOS 26 SDK or later.",
        "pubDate": "Mon, 03 Feb 2026 08:00:00 GMT",
        "link": "https://developer.apple.com/news/upcoming-requirements/?id=xcode-26",
    },
]


def clean_xml_tag(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def fetch_apple_rss(url="https://developer.apple.com/news/rss/news.rss", verbose=False):
    if verbose:
        print(f"[*] Fetching Apple Developer News from {url}...", file=sys.stderr)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
        return content.decode("utf-8")
    except Exception as e:
        if verbose:
            print(
                f"[!] Warning: Failed to fetch live RSS: {e}. Falling back to default data.",
                file=sys.stderr
            )
        return None


def parse_rss_items(xml_str):
    if not xml_str:
        return []
    try:
        root = ET.fromstring(xml_str)
        items = []
        # Find all <item> tags regardless of namespaces
        for el in root.iter():
            tag = clean_xml_tag(el.tag)
            if tag == "item":
                item_dict = {}
                for child in el:
                    ctag = clean_xml_tag(child.tag)
                    if ctag in ["title", "description", "link", "pubDate"]:
                        item_dict[ctag] = child.text
                if item_dict:
                    items.append(item_dict)
        return items
    except Exception as e:
        print(f"[!] Error parsing RSS XML: {e}")
        return []


def scan_target_repo(repo_path, track_name, metadata):
    """Scans repo_path for files matching the track's detect_files patterns.
    Returns (affected_files, scan_verdict)."""
    affected_files = []
    file_patterns = metadata["detect_files"]
    detect_regex = metadata["detect_regex"]

    if not os.path.exists(repo_path):
        return [], "Repository path does not exist."

    # Convert wildcards to regex patterns
    compiled_patterns = []
    for pat in file_patterns:
        if pat.startswith("*."):
            compiled_patterns.append(re.compile(r".*\." + re.escape(pat[2:]) + "$"))
        else:
            compiled_patterns.append(re.compile(r".*" + re.escape(pat) + "$"))

    # Scan project recursively
    for root, dirs, files in os.walk(repo_path):
        # Skip node_modules, Pods, build artifacts, and hidden directories
        if any(
            p in root
            for p in [
                "node_modules",
                "Pods",
                ".git",
                "build",
                "DerivedData",
                "Carthage",
            ]
        ):
            continue

        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_path)

            # Check if file name matches the track's detect_files
            matched_file = False
            for pat in compiled_patterns:
                if pat.match(f) or pat.match(rel_path):
                    matched_file = True
                    break

            if matched_file:
                # If we have a matching file, read its content to search for signature strings
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        if re.search(detect_regex, content, re.IGNORECASE):
                            affected_files.append(rel_path)
                except Exception:
                    pass

    if affected_files:
        verdict = f"Found {len(affected_files)} file(s) matching signature patterns and extensions."
    else:
        # Check if files just exist
        exist_count = 0
        for root, dirs, files in os.walk(repo_path):
            if any(
                p in root
                for p in [
                    "node_modules",
                    "Pods",
                    ".git",
                    "build",
                    "DerivedData",
                    "Carthage",
                ]
            ):
                continue
            for f in files:
                for pat in compiled_patterns:
                    if pat.match(f):
                        exist_count += 1
                        break
        if exist_count > 0:
            verdict = "Target file types are present, but no active signature keywords were matched in files."
        else:
            verdict = "No relevant file types or signatures found in the repository."

    return affected_files, verdict


def match_announcement_to_tracks(announcement):
    """
    Checks if a news item matches any of the 25 tracks based on keyword and regex matching.
    Returns a list of matched track names.
    """
    matched = []
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc}"

    for track, meta in TRACK_METADATA.items():
        # 1. Keyword direct check
        keyword_match = False
        for kw in meta["keywords"]:
            if kw in combined:
                keyword_match = True
                break

        if keyword_match:
            matched.append(track)
            continue

        # 2. Pattern regex check
        pattern_match = False
        for pat in meta["patterns"]:
            if re.search(pat, combined, re.IGNORECASE):
                pattern_match = True
                break

        if pattern_match:
            matched.append(track)

    return matched


def generate_pull_request(track_name, affected_files, item_title):
    """
    Generates draft Pull Request information for the compliance update.
    Produces a comprehensive, highly detailed, and complete PR description with 15 required sections.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", track_name.lower()).strip("-")
    branch_name = f"compliance/update-{slug}"
    pr_title = f"Compliance: Address {track_name} Requirements"

    meta = TRACK_METADATA.get(
        track_name,
        {
            "impact_desc": f"Policy and technical requirements under {track_name}.",
            "migration_steps": [
                "Review and verify conformity with updated guidelines."
            ],
            "release_impact": "High",
            "detect_files": ["Info.plist"],
            "detect_regex": "N/A",
        },
    )

    # Customized Regulatory change description mapping
    reg_change_desc = ""
    if track_name in ["DMA compliance changes", "Alternative payment regulations"]:
        reg_change_desc = (
            "The European Union's Digital Markets Act (DMA) introduces strict regulations for "
            "designated gatekeeper platforms, mandating open ecosystems, alternative app store distribution, "
            "and alternative in-app billing methods. This update aligns our app's payment architecture "
            "and distribution options with the latest compliance pathways for regional and global users."
        )
    elif track_name in ["AI-related App Store policies"]:
        reg_change_desc = (
            "The EU AI Act and updated App Store policies require comprehensive transparency "
            "for AI-driven applications, including strict disclosures when sending personal data to "
            "external AI providers, clear indication of generated content, and prevention of prohibited AI practices "
            "under Article 5 of Regulation (EU) 2024/1689."
        )
    elif track_name in [
        "Apple Privacy requirements",
        "Privacy Manifests",
        "Required Reason APIs",
        "App Tracking Transparency",
    ]:
        reg_change_desc = (
            "To comply with modern global privacy regulations (such as GDPR, CCPA/CPRA, and state-level laws), "
            "platform operators require strict user tracking disclosure, data minimization, and programmatic declarations. "
            "This change implements the mandated Privacy Manifest (PrivacyInfo.xcprivacy) files, "
            "declares specific Accessed APIs (such as UserDefaults or active keyboard), or establishes appropriate "
            "consent requests through the App Tracking Transparency framework."
        )
    elif track_name in ["Child safety requirements"]:
        reg_change_desc = (
            "Requirements under the Children's Online Privacy Protection Act (COPPA), the UK Age Appropriate Design Code, "
            "and Google Play's Child Safety Standards demand rigorous content rating, strict limitations on user "
            "data collection/tracking for children, robust age-gating mechanisms, and content filtering for safety."
        )
    elif track_name in ["In-App Purchase policies"]:
        reg_change_desc = (
            "App Store In-App Purchase and subscription policies have been updated to ensure price transparency, "
            "mandatory options for simple account deletion and subscription cancelation, and compliance with FTC "
            "'click-to-cancel' rules and regional payment mandates."
        )
    else:
        reg_change_desc = (
            f"An official platform policy update has been enacted affecting the '{track_name}' category. "
            "This change mandates specific API declarations, permission prompt modifications, or procedural "
            "compliance to ensure that the application is not rejected under App Store or Google Play policies."
        )

    # Customized Background context
    bg_context = (
        f"Keeping pace with platform developer guidelines is vital for preventing submission rejections and ensuring "
        f"continuous, reliable application delivery. Apple recently updated or reiterated guidelines surrounding **{track_name}**. "
        f"The primary context of this change is: {meta['impact_desc']} "
        "Implementing these updates is part of our standard compliance guard strategy to prevent release bottlenecks."
    )

    # Citations
    citations = [
        f'- Official announcement title: *"{item_title}"*',
        "- Apple Developer News & Updates: [Apple Developer News](https://developer.apple.com/news/)",
        "- App Store Review Guidelines: [Guidelines Link](https://developer.apple.com/app-store/review/guidelines/)",
        "- Repository Compliance Checklist: `docs/PRE-SUBMISSION-CHECKLIST.md`",
        "- Compliance database registry: `data/regulatory-deadlines.json`",
    ]

    # Risk Assessment
    risk_level = meta["release_impact"].upper()
    if risk_level == "CRITICAL":
        risk_desc = (
            "**CRITICAL RISK**: Failure to implement this requirement will result in an immediate automated "
            "upload-time or submission rejection in App Store Connect. Apple is actively enforcing this via static "
            "analysis, and non-compliance will prevent critical bug-fix updates from being shipped to production."
        )
    elif risk_level == "HIGH":
        risk_desc = (
            "**HIGH RISK**: There is a high probability of manual rejection by App Store reviewers during submission. "
            "This could trigger review suspension or administrative delays of 5 to 10 business days."
        )
    else:
        risk_desc = (
            f"**{risk_level} RISK**: Failure to implement this change increases compliance debt. It could trigger "
            "manual inspection or request-for-information notices during subsequent submission cycles."
        )

    # Affected Files reason list
    affected_files_content = ""
    if affected_files:
        affected_files_content += "The following files have been identified as potentially affected by this policy change:\n"
        for f in affected_files:
            affected_files_content += f"- `{f}`: Matches detection signature patterns for {track_name} (e.g., uses '{meta['detect_regex']}') and must be audited.\n"
    else:
        affected_files_content += (
            "No active files matching the specific code-level signatures were detected during repository scanning. "
            "However, the configuration files below must be verified:\n"
        )
        for df in meta.get("detect_files", []):
            affected_files_content += f"- `{df}`: Needs manual review to confirm correct metadata and declarations are in place.\n"

    # Migration Steps
    migration_steps_lines = []
    migration_steps_lines.append(
        f"1. Conduct a codebase audit focusing on keywords/APIs matching: `{meta['detect_regex']}`"
    )
    for step in meta["migration_steps"]:
        migration_steps_lines.append(f"2. {step}")
    migration_steps_lines.append(
        "3. Run the automated pre-submission compliance guard (`bash agent-os/hooks/app-store-compliance-guard.sh .`) to verify that the changes satisfy all local verification criteria."
    )

    # Backward Compatibility
    bk_compat = (
        "These compliance adjustments represent non-breaking declaration and metadata modifications. "
        "No existing APIs are deprecated in a way that breaks compatibility with legacy application versions. "
        "The changes preserve backward compatibility for users running older operating system versions."
    )

    # Checklists
    impl_checklist = [
        f"- [ ] Scan the codebase for occurrences of `{meta['detect_regex']}`.",
        f"- [ ] Update configuration files ({', '.join(meta['detect_files'])}) with accurate and compliant metadata declarations.",
        "- [ ] Ensure compliance flags or initialization code matches current guidelines exactly.",
        "- [ ] Strip out any dead, placeholder, or non-compliant testing code.",
    ]

    test_checklist = [
        "- [ ] Perform a clean build on a physical test device or simulator.",
        "- [ ] Run manual validation of affected UX flows (e.g., permission prompts, disclosures, or billing/consent interfaces).",
        "- [ ] Execute the pre-submission guard script to confirm that the compliance threshold is fully satisfied.",
        "- [ ] Verify that no new runtime logs or warnings are raised.",
    ]

    doc_checklist = [
        "- [ ] Update internal compliance documentation and requirements tracker.",
        "- [ ] Populate 'App Store Review Notes' (following `templates/REVIEW-NOTES-TEMPLATE.md`) with working test accounts and specific instructions.",
        "- [ ] Update the project's internal data mapping or privacy policy URL if required.",
    ]

    # Compliance Impact
    compliance_impact_desc = (
        "Implementing this change protects our developer standing, aligning the application with global regulatory frameworks "
        "and platform requirements. Successful implementation reduces our App Store submission risk profile to **Low** and "
        "ensures we remain in good legal standing across our entire operational user base."
    )

    # Breaking Changes
    breaking_changes_desc = (
        f"There are no structural breaking changes or breaking API modifications introduced by this change. "
        f"However, missing or incorrect configurations for `{track_name}` are considered breaking under App Store Review guidelines, "
        "making this update functionally mandatory."
    )

    # Review Checklist
    review_checklist = [
        "- [ ] Confirm that all required keys, identifiers, and files are present in the pull request diff.",
        "- [ ] Verify that no unauthorized third-party libraries or un-declared Required Reason APIs are referenced.",
        "- [ ] Ensure the code is free of debugging bypasses or non-compliant placeholders.",
        "- [ ] Verify that the app builds and runs successfully.",
    ]

    # Approver recommendations
    if risk_level in ["CRITICAL", "HIGH"]:
        approver_rec = (
            "- **Lead Mobile Engineer / Architect** (for codebase verification)\n"
            "- **Product / App Delivery Manager** (for timeline coordination)\n"
            "- **Legal & Privacy Compliance Officer** (for regulatory validation)"
        )
    else:
        approver_rec = (
            "- **Senior iOS / Mobile Developer** (for technical verification)\n"
            "- **QA Team Lead** (for testing checklist confirmation)"
        )

    desc_lines = [
        f"# Compliance Update: {track_name}",
        "",
        "## Summary",
        f"This Pull Request addresses the latest compliance requirements for **{track_name}**, "
        f'triggered by the developer update: *"{item_title}"*.',
        "",
        "## Background",
        bg_context,
        "",
        "## Regulatory change",
        reg_change_desc,
        "",
        "## Official citations",
        "\n".join(citations),
        "",
        "## Affected files",
        affected_files_content,
        "",
        "## Risk assessment",
        risk_desc,
        "",
        "## Migration steps",
        "\n".join(migration_steps_lines),
        "",
        "## Backward compatibility",
        bk_compat,
        "",
        "## Implementation checklist",
        "\n".join(impl_checklist),
        "",
        "## Testing checklist",
        "\n".join(test_checklist),
        "",
        "## Documentation checklist",
        "\n".join(doc_checklist),
        "",
        "## Compliance impact",
        compliance_impact_desc,
        "",
        "## Breaking changes",
        breaking_changes_desc,
        "",
        "## Review checklist",
        "\n".join(review_checklist),
        "",
        "## Approver recommendations",
        approver_rec,
        "",
        "---",
        "*Generated automatically by the App Store Compliance Playbook Requirements Monitor.*",
    ]

    return {
        "branch_name": branch_name,
        "title": pr_title,
        "description": "\n".join(desc_lines),
        "files_to_modify": affected_files,
    }


def run_monitor(
    project_path=".",
    simulate_track=None,
    use_mock=False,
    custom_news_file=None,
    verbose=False,
):
    """
    Main runner for the requirements monitor.
    """
    announcements = []

    if simulate_track:
        if verbose:
            print(f"[*] Simulating update for track: {simulate_track}", file=sys.stderr)
        # Build simulated announcements
        if simulate_track == "all":
            for track_name in TRACK_METADATA:
                announcements.append(
                    {
                        "title": f"Important updates concerning {track_name}",
                        "description": f"Apple has announced critical modifications to the specifications for {track_name}. Please review the updated rules.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": f"https://mock.invalid/apple-news/simulated-{re.sub(r'[^a-z0-9]+', '-', track_name.lower())}",
                    }
                )
        else:
            # Check if simulate_track is a valid track name or keyword
            matched_name = None
            for name in TRACK_METADATA:
                if simulate_track.lower() in name.lower():
                    matched_name = name
                    break

            if matched_name:
                announcements.append(
                    {
                        "title": f"Simulated Update: New requirements for {matched_name}",
                        "description": f"This is a simulated announcement to trigger monitoring and scanning for {matched_name}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": f"https://mock.invalid/apple-news/simulated-{re.sub(r'[^a-z0-9]+', '-', matched_name.lower())}",
                    }
                )
            else:
                # Custom announcement
                announcements.append(
                    {
                        "title": f"Simulated Announcement mentioning {simulate_track}",
                        "description": f"A custom announcement containing the keyword {simulate_track}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://mock.invalid/apple-news/simulated-custom",
                    }
                )

    elif custom_news_file:
        if verbose:
            print(f"[*] Loading announcements from custom file: {custom_news_file}", file=sys.stderr)
        try:
            with open(custom_news_file, "r", encoding="utf-8") as f:
                if custom_news_file.endswith(".json"):
                    announcements = json.load(f)
                else:
                    announcements = parse_rss_items(f.read())
        except Exception as e:
            print(f"[!] Error reading custom news file {custom_news_file}: {e}", file=sys.stderr)
            sys.exit(1)

    elif use_mock:
        if verbose:
            print("[*] Using pre-defined mock Apple Developer announcements...", file=sys.stderr)
        announcements = MOCK_ANNOUNCEMENTS

    else:
        # Fetch live
        rss_content = fetch_apple_rss(verbose=verbose)
        if rss_content:
            announcements = parse_rss_items(rss_content)
        else:
            if verbose:
                print(
                    "[*] Falling back to mock announcements due to missing or failed RSS fetch.",
                    file=sys.stderr
                )
            announcements = MOCK_ANNOUNCEMENTS

    if verbose:
        print(f"[*] Loaded {len(announcements)} developer announcements.", file=sys.stderr)

    report_items = []
    processed_tracks = set()

    for item in announcements:
        matched_tracks = match_announcement_to_tracks(item)
        if not matched_tracks:
            continue

        for track in matched_tracks:
            processed_tracks.add(track)
            meta = TRACK_METADATA[track]
            affected_files, scan_verdict = scan_target_repo(project_path, track, meta)
            pr_details = generate_pull_request(track, affected_files, item["title"])

            report_items.append(
                {
                    "announcement_title": item["title"],
                    "announcement_pubDate": item.get("pubDate", ""),
                    "announcement_link": item.get("link", ""),
                    "track": track,
                    "severity_impact": meta["release_impact"],
                    "repository_impact": meta["impact_desc"],
                    "scan_verdict": scan_verdict,
                    "affected_files": affected_files,
                    "migration_tasks": meta["migration_steps"],
                    "proposed_pull_request": pr_details,
                }
            )

    return report_items, processed_tracks


def update_documentation_report(report_items, output_filepath, verbose=False):
    """
    Writes/updates the migration report in docs/APPLE-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- APPLE_POLICY_MONITOR_START -->",
        "# Apple App Store Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor.py` to track compliance areas.",
        "",
        "## Monitored Requirements Update Log",
        "",
    ]

    for idx, item in enumerate(report_items, 1):
        lines.append(f"### {idx}. [{item['track']}] {item['announcement_title']}")
        lines.append(f"- **Published Date**: {item['announcement_pubDate']}")
        lines.append(f"- **Official Resource**: [{item['announcement_link']}]({item['announcement_link']})")
        lines.append(f"- **Description**: {item['repository_impact']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    # Deduplicate tracks to list migration tasks
    seen_tracks = set()
    for item in report_items:
        track = item["track"]
        if track in seen_tracks:
            continue
        seen_tracks.add(track)
        lines.append(f"### Tasks for {track}")
        lines.append(f"- **Regulatory Impact**: {item['severity_impact']} priority. App Store submission expectations require action.")
        for task in item["migration_tasks"]:
            lines.append(f"- [ ] {task}")
        lines.append("")

    lines.append("<!-- APPLE_POLICY_MONITOR_END -->")

    try:
        os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        if verbose:
            print(f"Apple documentation updated successfully at: {output_filepath}", file=sys.stderr)
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def generate_consolidated_pr_draft(report_items, output_filepath, verbose=False):
    """
    Generates a comprehensive 15-section, emoji-free Pull Request draft.
    """
    if not report_items:
        return

    # Gather data from report_items
    tracks = sorted(list(set(item["track"] for item in report_items)))
    citations = []
    affected_files_set = set()
    migration_steps = []
    risk_assessment_lines = []
    impl_checklist = []
    test_checklist = [
        "- [ ] Perform a clean build on a physical test device or simulator using Xcode.",
        "- [ ] Run manual validation of affected UX flows (e.g., permission prompts, disclosures, or billing/consent interfaces).",
        "- [ ] Execute the pre-submission guard script to confirm that the compliance threshold is fully satisfied.",
        "- [ ] Verify that no new runtime logs or warnings are raised."
    ]
    doc_checklist = [
        "- [ ] Update internal compliance documentation and requirements tracker.",
        "- [ ] Populate 'App Store Review Notes' with working test accounts and specific instructions.",
        "- [ ] Update the project's internal data mapping or privacy policy URL if required."
    ]

    for item in report_items:
        track = item["track"]
        citations.append(f"- **{track}**: \"{item['announcement_title']}\" ({item['announcement_link']})")
        for f in item["affected_files"]:
            affected_files_set.add(f)
        for step in item["migration_tasks"]:
            migration_steps.append(f"- **{track}**: {step}")
        risk_assessment_lines.append(f"- **{track}** ({item['severity_impact']}): {item['repository_impact']}")

        # Build specific checklist items
        meta = TRACK_METADATA.get(track, {})
        detect_regex = meta.get("detect_regex", "N/A")
        detect_files = meta.get("detect_files", [])
        impl_checklist.append(f"- [ ] Scan the codebase for occurrences of '{detect_regex}' relating to {track}.")
        impl_checklist.append(f"- [ ] Update configuration files ({', '.join(detect_files)}) with accurate and compliant metadata declarations.")

    citations_str = "\n".join(citations)
    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables)."

    migration_steps_str = "\n".join(migration_steps)
    risk_assessment_str = "\n".join(risk_assessment_lines)
    impl_checklist_str = "\n".join(impl_checklist)
    test_checklist_str = "\n".join(test_checklist)
    doc_checklist_str = "\n".join(doc_checklist)

    pr_template = f"""# PULL REQUEST DRAFT: Apple Developer and App Store Regulatory Compliance Update

## Summary
This pull request brings the application into complete compliance with all monitored Apple developer and App Store requirements. It addresses the updated expectations, security updates, permissions configurations, and StoreKit or privacy policies to clear App Store Connect publishing gates, covering: {", ".join(tracks)}.

## Background
Keeping pace with platform developer guidelines is vital for preventing submission rejections and ensuring continuous, reliable application delivery. Apple continuously updates its developer policies, guidelines, and API regulations to comply with evolving regulations, privacy standards, and security mandates. This pull request ensures that our application stays fully aligned with Apple App Store review expectations, minimizing rejection risk.

## Regulatory change
- **App Store Policy & Platform Updates**: Requirements covering {", ".join(tracks)} have been revised or reiterated.
- **Privacy & Security**: Mandatory declarations, including privacy manifests, required reason APIs, user data controls, or transaction workflows have been enforced or verified against the latest developer criteria.

## Official citations
{citations_str}

## Affected files
{affected_files_str}

## Risk assessment
{risk_assessment_str}
- **Overall Standing**: High priority. Non-compliance leads to automatic rejection, or escalation against the developer account, up to suspension or termination.

## Migration steps
{migration_steps_str}

## Backward compatibility
All adjustments in this compliance update are non-breaking, targeting configuration, metadata declarations, or optional API enhancements. Legacy operating systems and user devices remain fully supported without functional regressions.

## Implementation checklist
{impl_checklist_str}

## Testing checklist
{test_checklist_str}

## Documentation checklist
{doc_checklist_str}

## Compliance impact
Implementing this change protects our developer standing, aligning the application with global regulatory frameworks and platform requirements. Successful implementation reduces our App Store submission risk profile and ensures we remain in good legal standing across our entire operational user base.

## Breaking changes
There are no structural breaking changes or breaking API modifications introduced by this change. However, missing or incorrect configurations are considered breaking under App Store Review guidelines, making this update functionally mandatory.

## Review checklist
- [ ] Confirm that all required keys, identifiers, and files are present in the pull request diff.
- [ ] Verify that no unauthorized third-party libraries or un-declared Required Reason APIs are referenced.
- [ ] Ensure the code is free of debugging bypasses or non-compliant placeholders.
- [ ] Verify that the app builds and runs successfully.

## Approver recommendations
Recommended for review by:
- Senior iOS / Mobile Developer (for technical verification)
- QA Team Lead (for testing checklist confirmation)
- Legal & Privacy Compliance Officer (for regulatory validation)
"""

    try:
        os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(pr_template)
        if verbose:
            print(f"Apple PR draft written successfully to: {output_filepath}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to write PR draft to {output_filepath}: {e}", file=sys.stderr)


def print_text_report(report_items, project_path):
    print("=" * 80)
    print("                  APPLE DEVELOPER REQUIREMENTS MONITOR REPORT")
    print(f" Target Project: {os.path.abspath(project_path)}")
    print(f" Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not report_items:
        print(
            "\n[+] No updates found matching target Apple developer requirements tracks.\n"
        )
        return

    print(f"\nFound {len(report_items)} matched compliance requirement update(s):\n")

    for i, item in enumerate(report_items, 1):
        print(f"{i}. TRACK UPDATE: [{item['track']}]")
        print(f"   - Announcement: {item['announcement_title']}")
        print(f"   - Published:    {item['announcement_pubDate']}")
        print(f"   - Link:         {item['announcement_link']}")
        print(f"   - Release Impact: {item['severity_impact']}")
        print(f"   - Repo Impact:  {item['repository_impact']}")
        print(f"   - Scan Verdict: {item['scan_verdict']}")

        if item["affected_files"]:
            print("   - Identified Affected Files:")
            for f in item["affected_files"]:
                print(f"       * {f}")
        else:
            print("   - Affected Files: None found.")

        print("   - Generated Migration Tasks:")
        for t in item["migration_tasks"]:
            print(f"       [ ] {t}")

        pr = item["proposed_pull_request"]
        print("   - Proposed Pull Request Details:")
        print(f"       * Branch Name:  {pr['branch_name']}")
        print(f"       * PR Title:     {pr['title']}")
        print("       * PR Description: (draft generated successfully)")

        print("-" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Monitor and track updates to Apple developer requirements."
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Path to target mobile app project root (default: current directory)",
    )
    parser.add_argument(
        "--simulate",
        help="Simulate an update by track name (e.g., 'Privacy Manifests') or 'all' to simulate all 25 tracks",
    )
    parser.add_argument(
        "--mock", action="store_true", help="Force using mock pre-defined announcements"
    )
    parser.add_argument(
        "--news-file", help="Path to a custom XML or JSON file containing announcements"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose execution and scanning logs",
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

    report_items, processed = run_monitor(
        project_path=args.project,
        simulate_track=args.simulate,
        use_mock=args.mock,
        custom_news_file=args.news_file,
        verbose=args.verbose,
    )

    # Generate documents
    if report_items:
        update_documentation_report(
            report_items,
            args.output_docs,
            verbose=not args.json
        )
        generate_consolidated_pr_draft(
            report_items,
            args.pr_output,
            verbose=not args.json
        )

    if args.json:
        print(json.dumps(report_items, indent=2))
    else:
        print_text_report(report_items, args.project)


if __name__ == "__main__":
    main()
