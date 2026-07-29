#!/usr/bin/env python3
"""Apple Developer Requirements Monitor: tracks 25 Apple requirement
categories against live/mock news, scans the codebase for impact,
updates docs/APPLE-POLICY-MIGRATION.md, and drafts docs/APPLE_COMPLIANCE_PR_DRAFT.md.
Strict emoji-free policy is enforced across code, logs, and generated files."""

import os
import sys
import re
import json
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# The 25 specified tracking areas (the "tracks")
TRACKED_CATEGORIES = [
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

MOCK_ANNOUNCEMENTS = [
    {
        "title": "Upcoming Requirements for Privacy Manifests and Required Reason APIs",
        "description": "Starting late spring, all new apps and app updates submitted to the App Store must include a Privacy Info manifest declaring reasons for accessing specific APIs such as UserDefaults or systemUptime.",
        "pubDate": "Wed, 15 May 2026 10:00:00 GMT",
        "link": "https://developer.apple.com/news/?id=privacy-requirements",
        "category": "Privacy Manifests",
    },
    {
        "title": "Updates to In-App Purchase Policies and Alternative Payment Options",
        "description": "To comply with recent global regulations, developers can now direct users to external purchase options on their website. Ensure transparent billing disclosures and subscription terms are met.",
        "pubDate": "Mon, 01 Jun 2026 09:00:00 GMT",
        "link": "https://developer.apple.com/news/?id=iap-updates",
        "category": "In-App Purchase policies",
    },
    {
        "title": "App Store Review Guidelines and 4.3 Saturated Categories Update",
        "description": "App Review Guideline 4.3 has been updated. Low-quality apps or duplicates in saturated categories like flashlight or wallpaper will face direct rejection unless they offer distinct user value.",
        "pubDate": "Tue, 09 Jun 2026 14:00:00 GMT",
        "link": "https://developer.apple.com/news/?id=review-guidelines-update",
        "category": "App Store Review Guidelines",
    },
    {
        "title": "Xcode 26 and Minimum iOS SDK Requirements for Submission",
        "description": "From April 28, 2026, all iOS, watchOS, and tvOS apps submitted to the App Store must be built with Xcode 26 and target the iOS 26 SDK or later.",
        "pubDate": "Mon, 03 Feb 2026 08:00:00 GMT",
        "link": "https://developer.apple.com/news/upcoming-requirements/?id=xcode-26",
        "category": "Xcode requirements",
    },
]


def parse_rss_feed(url):
    """Fetches and parses live RSS or Atom XML feeds."""
    items = []
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (AppleComplianceMonitor/1.0)"}
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


def scan_codebase_for_apple_signals(start_dir="."):
    """Scans the codebase for files containing signals related to each of the 25 requirement categories."""
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
        cat: re.compile(meta["detect_regex"], re.IGNORECASE)
        for cat, meta in TRACK_METADATA.items()
    }

    compiled_file_patterns = {}
    for cat, meta in TRACK_METADATA.items():
        patterns = []
        for pat in meta["detect_files"]:
            if pat.startswith("*."):
                patterns.append(re.compile(r".*\." + re.escape(pat[2:]) + "$"))
            else:
                patterns.append(re.compile(r".*" + re.escape(pat) + "$"))
        compiled_file_patterns[cat] = patterns

    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referential matches
            if "monitor-apple" in file or "monitor-test" in file:
                continue

            try:
                for cat in TRACKED_CATEGORIES:
                    # Check if file matches any patterns for this category
                    file_matched = False
                    for pat in compiled_file_patterns[cat]:
                        if pat.match(file) or pat.match(filepath):
                            file_matched = True
                            break

                    if file_matched:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if compiled_signals[cat].search(content):
                                # Just add unique filenames
                                if filepath not in [m["file"] for m in matches[cat]]:
                                    matches[cat].append(
                                        {
                                            "file": filepath,
                                            "matched_pattern": TRACK_METADATA[cat]["detect_regex"],
                                        }
                                    )
            except Exception:
                pass
    return matches


def classify_announcements(announcements, keywords_filter=None):
    """Classifies incoming announcements into the 25 Apple requirement categories."""
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        matched_categories = []
        for cat, meta in TRACK_METADATA.items():
            # Keyword direct check
            kw_match = False
            for kw in meta["keywords"]:
                if kw in text_to_search:
                    kw_match = True
                    break
            if kw_match:
                matched_categories.append(cat)
                continue

            # Pattern regex check
            pat_match = False
            for pat in meta["patterns"]:
                if re.search(pat, text_to_search, re.IGNORECASE):
                    pat_match = True
                    break
            if pat_match:
                matched_categories.append(cat)

        # Fallback to pre-set category if exists
        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "APPLE-UPDATE-" + str(hash(title))[:6]),
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": ann.get("link", ""),
                        "pubDate": ann.get("pubDate", ""),
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a comprehensive 15-section, emoji-free compliance Pull Request description."""
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

        meta = TRACK_METADATA[cat]
        migration_steps.append(f"- **{cat}**: {meta['impact_desc']}")
        for step in meta["migration_steps"]:
            migration_steps.append(f"  * {step}")

        impl_checklist.append(f"- [ ] Audit project elements for {cat}")
        impl_checklist.append(f"  * Scan for regex signature: `{meta['detect_regex']}`")

        risk_assessment.append(
            f"- *{cat}* ({meta['release_impact']} Impact): Failure leads to storefront review rejection or upload blocks."
        )

    citations_str = "\n".join(citations_list) if citations_list else "- No active citations compiled."
    affected_files_str = (
        "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
        if affected_files_set
        else "- *No specific files containing matching category patterns were automatically detected.*"
    )
    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- No specific migration tasks are triggered."
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- No implementation checklist items."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- Low direct compliance risks detected."

    pr_template = f"""# PULL REQUEST DRAFT: Apple Developer and App Store Policy Compliance Update

## 1. Summary
This pull request introduces critical configuration adjustments and codebase compliance pathways to conform with the latest Apple Developer Program and App Store requirement updates.

## 2. Background
Apple enforces strict storefront reviews and automated app submission gates. Maintaining conformity with the latest Developer Program License Agreements, App Store Review Guidelines, and specialized technical specifications is essential to avoid submission rejection or distribution blockages.

## 3. Regulatory change
The updates address core compliance requirements, including:
- Access control guidelines and Required Reason API declarations.
- App privacy requirements, third-party data-sharing transparency, and Privacy Manifest integration.
- Target SDK, minimum development targets, and Xcode compiling rules.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Submission Security**: Failure to address high or critical impact updates blocks App Store Connect upload processing.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes represent non-breaking declaration updates, Info.plist purpose strings, or Privacy Info manifest configurations. There is zero deprecation of core functional APIs, and compatibility with older deployed iOS versions is preserved.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the pre-submission compliance guard checks locally.

## 10. Testing checklist
- [ ] Perform a clean compile using Xcode on a development machine.
- [ ] Verify that privacy manifest files are properly linked inside the compiled bundle.
- [ ] Walk through affected user flows (such as permission dialogs or privacy disclosures) to ensure visual and operational compliance.

## 11. Documentation checklist
- [ ] Update APP-STORE-COMPLIANCE or APPLE-POLICY-MIGRATION reference docs.
- [ ] Update App Review Notes in App Store Connect with valid demo account credentials and layout descriptions.

## 12. Compliance impact
- **Submission Security**: Minimizes manual rejection risks and clears automated publishing gates.
- **Enterprise Standing**: Protects developer organization status under the latest License Agreements.

## 13. Breaking changes
No technical API breaking changes are introduced. However, failing to comply with platform requirements makes previous app builds effectively non-distributable.

## 14. Review checklist
- [ ] Ensure the pull request contains zero emojis or graphical symbols.
- [ ] Confirm that all added plist keys and purpose strings are non-empty and accurate.
- [ ] Verify that no private or undocumented APIs are referenced in the codebase.

## 15. Approver recommendations
Ensure that senior iOS engineers and compliance officers review the technical implementation of Privacy Manifests and Required Reason APIs, as missing declarations can block submissions post-deadline.
"""
    return pr_template


def update_documentation_report(updates, output_filepath, scan_results):
    """Overwrites or updates the migration report in docs/APPLE-POLICY-MIGRATION.md."""
    lines = [
        "<!-- APPLE_POLICY_MONITOR_START -->",
        "# Apple Developer and App Store Policy Migration & Requirements Report",
        "",
        "This report is continuously updated by the Apple Developer Requirements Monitor.",
        "",
        "## Monitored Requirements Update Log",
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
        meta = TRACK_METADATA[cat]
        lines.append(f"### Tasks for {cat}")
        lines.append(f"- **Severity/Release Impact**: {meta['release_impact']}")
        lines.append(f"- **Description**: {meta['impact_desc']}")

        matched_files = scan_results.get(cat, [])
        if matched_files:
            lines.append("- **Detected Affected Files**:")
            for mf in matched_files:
                lines.append(f"  * `{mf['file']}` (pattern matched: `{mf['matched_pattern']}`)")

        for step_idx, step in enumerate(meta["migration_steps"], 1):
            lines.append(f"- [ ] **Task {step_idx}**: {step}")
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
        "--live", action="store_true", help="Fetch live Apple Developer news RSS feed"
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

    announcements = []

    if args.live:
        print("Fetching live Apple Developer News RSS feed...")
        announcements.extend(
            parse_rss_feed("https://developer.apple.com/news/rss/news.rss")
        )

    # Fallback to mock data if live has no updates or mock is explicitly requested
    if args.mock or (not args.live and not args.mock) or not announcements:
        print("Using comprehensive mock Apple policy updates for compliance scanning...")
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

    classified_updates = classify_announcements(announcements, args.keywords)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(f"Monitored and classified {len(classified_updates)} policy/requirement updates:")
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for Apple integration signals...")
    scan_results = scan_codebase_for_apple_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs, scan_results)

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
