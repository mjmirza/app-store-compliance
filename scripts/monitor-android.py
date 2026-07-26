#!/usr/bin/env python3
"""Monitors the 19 Android/Google Play categories in TRACKED_CATEGORIES
below, and generates repo-impact and migration tasks for each update."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 19 tracked Android & Google Play requirement categories
TRACKED_CATEGORIES = [
    "Google Play Developer Policies",
    "Play Console announcements",
    "Target SDK requirements",
    "Minimum SDK requirements",
    "Android API deprecations",
    "Android permission model",
    "Background execution restrictions",
    "Foreground service policies",
    "Privacy Sandbox",
    "Play Integrity API",
    "Play Billing",
    "User Data policy",
    "Data Safety section",
    "AI-generated content policies",
    "Accessibility requirements",
    "Device compatibility requirements",
    "Security Bulletins",
    "Android Enterprise requirements",
    "Firebase policy updates",
]

# Keywords used to classify incoming policy announcements/articles into the 19 categories
CATEGORY_KEYWORDS = {
    "Google Play Developer Policies": [
        "developer policy",
        "developer policies",
        "program policy",
        "google play policy",
        "policy center",
        "violat",
        "enforce",
    ],
    "Play Console announcements": [
        "play console",
        "console announcement",
        "developer console",
        "identity verification",
        "verification",
        "announc",
    ],
    "Target SDK requirements": [
        "target sdk",
        "targetsdkversion",
        "targetsdk",
        "api level requirement",
        "target api level",
        "android 15",
        "android 16",
        "android 17",
    ],
    "Minimum SDK requirements": [
        "minimum sdk",
        "minsdkversion",
        "minsdk",
        "api level support",
        "legacy android",
        "min_sdk",
    ],
    "Android API deprecations": [
        "deprecation",
        "deprecated api",
        "deprecated class",
        "deprecat",
        "legacy api",
        "safetynet retirement",
    ],
    "Android permission model": [
        "android permission",
        "runtime permission",
        "permission model",
        "sensitive permission",
        "uses-permission",
        "requestpermissions",
    ],
    "Background execution restrictions": [
        "background execution",
        "background work",
        "workmanager",
        "jobscheduler",
        "exact alarm",
        "alarmmanager",
        "wakelock",
    ],
    "Foreground service policies": [
        "foreground service",
        "fgs type",
        "foregroundservice",
        "startforeground",
        "foregroundservicetype",
    ],
    "Privacy Sandbox": [
        "privacy sandbox",
        "sandbox",
        "topics api",
        "protected audience",
        "sdk runtime",
        "attribution reporting",
    ],
    "Play Integrity API": [
        "play integrity",
        "integrity api",
        "safetynet attestation",
        "attestation check",
        "integrity manager",
    ],
    "Play Billing": [
        "play billing",
        "billing library",
        "billing client",
        "billing v8",
        "billing v9",
        "com.android.billingclient",
    ],
    "User Data policy": [
        "user data",
        "data safety",
        "data deletion",
        "personal data",
        "privacy policy url",
        "account deletion",
    ],
    "Data Safety section": [
        "data safety",
        "datasafety",
        "safety section",
        "data declaration",
        "data collection",
        "data sharing",
    ],
    "AI-generated content policies": [
        "ai-generated",
        "generative ai",
        "ai content",
        "chatbot",
        "deepfake",
        "face-swap",
        "llm",
        "openai",
        "gemini",
    ],
    "Accessibility requirements": [
        "accessibility",
        "talkback",
        "accessibility service",
        "wcag",
        "touch target",
        "content description",
        "bind_accessibility_service",
    ],
    "Device compatibility requirements": [
        "device compatibility",
        "screen size",
        "tablet support",
        "compatible devices",
        "uses-feature",
        "foldable",
        "multi-window",
    ],
    "Security Bulletins": [
        "security bulletin",
        "cve-",
        "vulnerability",
        "keystore",
        "ssl pinning",
        "key store",
        "biometrics",
        "cve",
    ],
    "Android Enterprise requirements": [
        "android enterprise",
        "work profile",
        "managed device",
        "device policy manager",
        "device-admin",
        "deviceadminreceiver",
    ],
    "Firebase policy updates": [
        "firebase",
        "google services",
        "crashlytics",
        "admob",
        "google-services.json",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 19 categories
CATEGORY_SIGNALS = {
    "Google Play Developer Policies": [
        r"Designed for Families",
        r"DesignedForFamilies",
        r"IARC",
        r"IARC_RATING",
    ],
    "Play Console announcements": [r"play-console", r"developer-console"],
    "Target SDK requirements": [r"targetSdkVersion", r"targetSdk", r"target_sdk"],
    "Minimum SDK requirements": [r"minSdkVersion", r"minSdk", r"min_sdk"],
    "Android API deprecations": [
        r"SafetyNet",
        r"com.google.android.gms.ads.identifier",
        r"UIWebView",
    ],
    "Android permission model": [
        r"requestPermissions",
        r"checkSelfPermission",
        r"Manifest\.permission",
        r"uses-permission",
    ],
    "Background execution restrictions": [
        r"JobScheduler",
        r"WorkManager",
        r"AlarmManager",
        r"JobInfo",
        r"BroadcastReceiver",
    ],
    "Foreground service policies": [
        r"FOREGROUND_SERVICE",
        r"startForeground",
        r"foregroundServiceType",
    ],
    "Privacy Sandbox": [
        r"PrivacySandbox",
        r"AdSelectionManager",
        r"TopicsManager",
        r"ad-services",
        r"AdServicesOutlet",
    ],
    "Play Integrity API": [
        r"PlayIntegrity",
        r"IntegrityManager",
        r"play-services-safetynet",
        r"IntegrityTokenRequest",
    ],
    "Play Billing": [
        r"BillingClient",
        r"billingclient",
        r"billing-client",
        r"com\.android\.billingclient",
    ],
    "User Data policy": [
        r"privacyPolicy",
        r"privacy-policy",
        r"privacy_policy",
        r"User Data",
        r"deleteAccount",
        r"delete_account",
    ],
    "Data Safety section": [
        r"Data Safety",
        r"firebase-analytics",
        r"appsflyer",
        r"adjust",
        r"com\.facebook",
    ],
    "AI-generated content policies": [
        r"api\.openai\.com",
        r"openai",
        r"gemini",
        r"generative",
        r"chat/completions",
        r"text-to-image",
        r"llm",
    ],
    "Accessibility requirements": [
        r"AccessibilityService",
        r"BIND_ACCESSIBILITY_SERVICE",
        r"TalkBack",
        r"contentDescription",
    ],
    "Device compatibility requirements": [
        r"uses-feature",
        r"uses-configuration",
        r"support-screens",
        r"supports-screens",
    ],
    "Security Bulletins": [
        r"Security Bulletin",
        r"Android Keystore",
        r"KeyStore",
        r"biometrics",
        r"security-bulletin",
    ],
    "Android Enterprise requirements": [
        r"device-admin",
        r"DeviceAdminReceiver",
        r"DevicePolicyManager",
        r"enterprise",
    ],
    "Firebase policy updates": [
        r"firebase-",
        r"google-services\.json",
        r"crashlytics",
        r"FirebaseApp",
    ],
}

# Rich mock announcements representing policy updates/bulletins for ALL 19 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "ANDROID-MOCK-GP-DEV-POL",
        "category": "Google Play Developer Policies",
        "title": "Google Play Enforcement Process",
        "description": "Google Play's enforcement process for policy violations covers rejection, removal, suspension, limited visibility, and account termination, based on app metadata, in-app experience, and account information.",
        "link": "https://support.google.com/googleplay/android-developer/answer/9899234",
        "pubDate": "Wed, 10 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-CONSOLE-ANNC",
        "category": "Play Console announcements",
        "title": "New Play Console Mandatory Identity Verification for Personal Accounts",
        "description": "To foster user trust, Google Play requires all personal developer accounts created before recent policy updates to complete mandatory identity verification by September 30, 2026. Failure to verify will result in update blockages and eventual listing removals.",
        "link": "https://support.google.com/googleplay/android-developer/answer/113289",
        "pubDate": "Mon, 15 Jun 2026 09:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-TARGET-SDK",
        "category": "Target SDK requirements",
        "title": "Google Play Target SDK Policy: Support Android 16 (API 36) by August 31, 2026",
        "description": "Google Play is updating its Target SDK requirements. Starting August 31, 2026, all new apps and updates to existing apps must target Android 16 (API 36) or higher. Submissions failing to meet this threshold will be blocked by the publishing gate.",
        "link": "https://developer.android.com/google/play/requirements/target-sdk",
        "pubDate": "Sun, 01 Mar 2026 08:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-MIN-SDK",
        "category": "Minimum SDK requirements",
        "title": "Minimum SDK Requirement Policy Change for Android 5.0 Deprecation",
        "description": "To maintain high security and performance across the Google Play ecosystem, apps must set a minSdkVersion of 23 (Android 6.0) or higher to receive updates, formally deprecating support for legacy Android 5.0 and 5.1 (API 21/22).",
        "link": "https://developer.android.com/about/versions",
        "pubDate": "Thu, 12 Mar 2026 11:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-DEPRECATION",
        "category": "Android API deprecations",
        "title": "Legacy SafetyNet Attestation APIs Deprecation & Shutdown Schedule",
        "description": "As announced previously, the Legacy SafetyNet Attestation APIs are fully deprecated and shut down. All anti-abuse, security check, and integrity verification flows must migrate to the modern Play Integrity API.",
        "link": "https://developer.android.com/google/play/integrity/deprecation-guide",
        "pubDate": "Fri, 20 Mar 2026 12:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-PERMISSION",
        "category": "Android permission model",
        "title": "Android Permission Model Update: Scoped Media and Storage Consent",
        "description": "Under the updated User Data and Android Permission Model, apps requesting READ_MEDIA_IMAGES and READ_MEDIA_VIDEO face stricter verification. Broad photo access is restricted, and developers are urged to migrate to the native Android Photo Picker.",
        "link": "https://developer.android.com/guide/topics/permissions/overview",
        "pubDate": "Mon, 23 Mar 2026 14:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-BACKGROUND",
        "category": "Background execution restrictions",
        "title": "Strict Restrictions on Android Background execution and Exact Alarms",
        "description": "To conserve system battery life and improve device performance, Android is introducing tighter runtime checks. Tighter limitations on exact alarms (SCHEDULE_EXACT_ALARM) and background wake locks will trigger automatic job throttling.",
        "link": "https://developer.android.com/about/versions/14/changes/schedule-exact-alarms",
        "pubDate": "Fri, 27 Mar 2026 15:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-FOREGROUND",
        "category": "Foreground service policies",
        "title": "New Foreground Service Type Declaration Mandate on Play Console",
        "description": "All applications targeting API 34+ that run foreground services must declare valid foregroundServiceType attributes in their manifest, hold matching FOREGROUND_SERVICE permissions, and submit a detailed Play Console foreground service declaration and video.",
        "link": "https://developer.android.com/guide/components/foreground-services",
        "pubDate": "Tue, 31 Mar 2026 16:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-PRIVACY-SANDBOX",
        "category": "Privacy Sandbox",
        "title": "Google Play Privacy Sandbox Beta Rollout and Advertising ID Phase-Out",
        "description": "Google is expanding the Privacy Sandbox Beta on Android, initiating the gradual phase-out of the legacy persistent Advertising ID (GAID) in favor of the privacy-preserving Topics API, Attribution Reporting, and SDK Runtime environments.",
        "link": "https://developer.android.com/design-guidelines/privacy/sandbox",
        "pubDate": "Wed, 01 Apr 2026 10:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-INTEGRITY",
        "category": "Play Integrity API",
        "title": "Play Integrity API Update: Nonce Verification and Integrity Token Enforcement",
        "description": "To mitigate man-in-the-middle replay attacks, Google Play Integrity API now enforces server-side cryptographic nonce verification and strict integrity token checks before dispensing secure payloads.",
        "link": "https://developer.android.com/google/play/integrity",
        "pubDate": "Mon, 06 Apr 2026 11:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-BILLING",
        "category": "Play Billing",
        "title": "Play Billing Library v8.0 Mandatory Migration Deadline",
        "description": "By August 31, 2026, all new apps and updates to existing apps must migrate to the Play Billing Library version 8.0 or higher. Apps attempting to publish using earlier Billing Library versions (including v7.x or below) will be automatically blocked.",
        "link": "https://developer.android.com/google/play/billing/deprecation-faq",
        "pubDate": "Wed, 08 Apr 2026 12:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-USER-DATA",
        "category": "User Data policy",
        "title": "Google Play User Data Deletion and Web URL Mandate Update",
        "description": "All apps permitting in-app account creation must provide users with both an in-app account deletion flow and a public web-based data deletion URL. Unreachable or broken deletion URLs will trigger automated store rejections.",
        "link": "https://support.google.com/googleplay/android-developer/answer/13327111",
        "pubDate": "Fri, 10 Apr 2026 13:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-DATASAFETY",
        "category": "Data Safety section",
        "title": "Data Safety Mismatch Enforcement: Automatic Static SDK Scanning",
        "description": "Google Play is introducing enhanced static scanning for compiled binaries. The system will auto-scan for analytics (Firebase, Facebook, AppsFlyer) and advertising SDKs, rejecting any submission whose Data Safety declarations fail to match active tracking behavior.",
        "link": "https://support.google.com/googleplay/android-developer/answer/10787469",
        "pubDate": "Mon, 13 Apr 2026 14:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-AI-POLICY",
        "category": "AI-generated content policies",
        "title": "Google Play Generative AI Safeguards and In-App Reporting Requirements",
        "description": "Applications integrating generative AI or conversational LLMs must provide robust user-safety controls, including prominent disclosures, an in-app content reporting/flagging mechanism, user blocking, and safeguards preventing deepfake/NSFW outputs.",
        "link": "https://support.google.com/googleplay/android-developer/answer/14747720",
        "pubDate": "Thu, 16 Apr 2026 15:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-ACCESSIBILITY",
        "category": "Accessibility requirements",
        "title": "Google Play Accessibility Service Misuse and Touch Target Audit",
        "description": "Google Play will flag and reject non-accessibility apps requesting the BIND_ACCESSIBILITY_SERVICE permission. Additionally, apps face strict audits ensuring a minimum 48dp touch target size and content descriptions for all interactive elements.",
        "link": "https://support.google.com/googleplay/android-developer/answer/10964491",
        "pubDate": "Tue, 21 Apr 2026 16:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-COMPATIBILITY",
        "category": "Device compatibility requirements",
        "title": "Device Compatibility and Foldable Layout Guidelines Update",
        "description": "Android releases update guidelines enforcing screen and aspect-ratio compatibility across multi-window systems, tablets, and foldable devices. Apps must support dynamic resizing and avoid fixed orientation limits where feasible.",
        "link": "https://developer.android.com/guide/topics/large-screens/foldable-devices",
        "pubDate": "Fri, 24 Apr 2026 17:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-SECURITY",
        "category": "Security Bulletins",
        "title": "Android Security Bulletin: Cryptographic Keystore Isolation Mandate",
        "description": "An Android Security Bulletin addresses high-severity vulnerabilities (CVE-2026-X). App developers are mandated to isolate sensitive user secrets and credentials inside the hardware-backed Android Keystore system and enforce biometrics.",
        "link": "https://source.android.com/docs/security/bulletin",
        "pubDate": "Mon, 27 Apr 2026 10:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-ENTERPRISE",
        "category": "Android Enterprise requirements",
        "title": "Android Enterprise Work Profile Security Policy Enhancements",
        "description": "Google announces new Android Enterprise standards for corporate and work profile apps. Enhanced controls under the DevicePolicyManager allow secure data boundaries, blocking side-loading and personal app data leakage.",
        "link": "https://developer.android.com/work",
        "pubDate": "Thu, 30 Apr 2026 11:00:00 PDT",
    },
    {
        "id": "ANDROID-MOCK-FIREBASE",
        "category": "Firebase policy updates",
        "title": "Firebase Policy Update: Mandatory Dynamic Links Deprecation and Privacy Rules",
        "description": "Firebase is sunsetting Dynamic Links, requiring developers to migrate to Firebase Hosting Deep Links, App Links, or universal links. Additionally, updated Realtime Database and Cloud Firestore rules enforce strict authorization boundaries.",
        "link": "https://firebase.google.com/support/privacy",
        "pubDate": "Mon, 04 May 2026 09:00:00 PDT",
    },
]


def scan_codebase_for_android_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 19 requirement categories.
    """
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
                    ".kt",
                    ".java",
                    ".xml",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".md",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-android" in file or "monitor-android-test" in file:
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
                                    # Break to avoid duplicate entry for the same line and category
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
            url, headers={"User-Agent": "Mozilla/5.0 (AndroidComplianceMonitor/1.0)"}
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
    Classifies incoming announcements into the 19 Android and Google Play requirement categories.
    """
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        # If keywords_filter is supplied, verify if any filter matches
        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Match against categories
        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break  # Break keyword loop for this category

        # If a pre-set category exists on mock and no matched categories, use that category
        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "ANDROID-UPDATE-" + str(hash(title))[:6]),
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

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific migration details
        if cat == "Target SDK requirements":
            migration_steps.append(
                f"- **{cat}**: Update targetSdkVersion and compileSdkVersion in all build.gradle or build.gradle.kts files to API 36 (Android 16) before the August 31, 2026 deadline."
            )
            impl_checklist.append(
                "- [ ] Update targetSdkVersion in build.gradle files to 36."
            )
            impl_checklist.append(
                "- [ ] Verify all API 36 runtime behavioral changes do not impact application functionality."
            )
            risk_assessment.append(
                f"- *{cat}*: Publishing gate blockage for new submissions and updates if SDK target level is below requirement."
            )
        elif cat == "Minimum SDK requirements":
            migration_steps.append(
                f"- **{cat}**: Set minSdkVersion to 23 (Android 6.0) or higher to deprecate legacy API 21/22 support."
            )
            impl_checklist.append(
                "- [ ] Update minSdkVersion to 23 in Gradle build configs."
            )
            risk_assessment.append(
                f"- *{cat}*: Deprecation of legacy devices leading to minor decrease in active user base."
            )
        elif cat == "Android API deprecations":
            migration_steps.append(
                f"- **{cat}**: Fully remove all legacy SafetyNet Attestation code references and complete migration to the Play Integrity SDK."
            )
            impl_checklist.append(
                "- [ ] Remove 'com.google.android.gms:play-services-safetynet' dependency."
            )
            impl_checklist.append(
                "- [ ] Implement Play Integrity token request flows on the client."
            )
            risk_assessment.append(
                f"- *{cat}*: Zero response/payload delivery for anti-abuse checks if legacy SafetyNet APIs are invoked."
            )
        elif cat == "Android permission model":
            migration_steps.append(
                f"- **{cat}**: Implement Scoped Media storage handling. Avoid broad READ_MEDIA_IMAGES/VIDEO requests; adopt the native Android Photo Picker instead."
            )
            impl_checklist.append(
                "- [ ] Implement the native Android Photo Picker API wrapper."
            )
            impl_checklist.append(
                "- [ ] Update AndroidManifest permissions; remove unnecessary broad media permissions."
            )
            risk_assessment.append(
                f"- *{cat}*: Runtime crash or automated play store rejection under the restricted user data policies."
            )
        elif cat == "Background execution restrictions":
            migration_steps.append(
                f"- **{cat}**: Ensure all WorkManager, JobScheduler, and AlarmManager tasks stay strictly within execution time limits. Validate SCHEDULE_EXACT_ALARM use cases."
            )
            impl_checklist.append(
                "- [ ] Audit exact alarm declarations; replace with inexact alarms unless qualifies for exemption."
            )
            risk_assessment.append(
                f"- *{cat}*: Automated background service thottling or foreground service crash on target devices."
            )
        elif cat == "Foreground service policies":
            migration_steps.append(
                f"- **{cat}**: Declare precise foregroundServiceType properties on all <service> nodes in AndroidManifest.xml. Secure Play Console approval."
            )
            impl_checklist.append(
                "- [ ] Declare correct foregroundServiceType in AndroidManifest.xml."
            )
            impl_checklist.append(
                "- [ ] Draft play console foreground service declaration and record verification demo video."
            )
            risk_assessment.append(
                f"- *{cat}*: Missing console declarations will block release updates under Device and Network Abuse policy."
            )
        elif cat == "Privacy Sandbox":
            migration_steps.append(
                f"- **{cat}**: Migrate marketing/analytics workflows from legacy Advertising ID (GAID) tracking to the modern Privacy Sandbox Topics and Attribution APIs."
            )
            impl_checklist.append(
                "- [ ] Update third-party tracking dependencies; configure privacy sandbox topics opt-in."
            )
            risk_assessment.append(
                f"- *{cat}*: Gradual tracking disruption as GAID is sunset across modern Android devices."
            )
        elif cat == "Play Integrity API":
            migration_steps.append(
                f"- **{cat}**: Implement secure server-side cryptographic nonce generation and verification for Play Integrity tokens."
            )
            impl_checklist.append(
                "- [ ] Implement server-side Play Integrity token verification endpoint with cryptographic nonce checks."
            )
            risk_assessment.append(
                f"- *{cat}*: Vulnerability to replay attacks if integrity verdicts are not bound to a transaction-specific nonce."
            )
        elif cat == "Play Billing":
            migration_steps.append(
                f"- **{cat}**: Migrate billing modules to Google Play Billing Library version 8.0 or higher. Remove legacy BillingClient v7 or lower dependencies."
            )
            impl_checklist.append(
                "- [ ] Upgrade billing client dependency 'com.android.billingclient:billing' to v8.0+."
            )
            risk_assessment.append(
                f"- *{cat}*: Blocked app updates post-August 31, 2026 if using outdated billing libraries."
            )
        elif cat == "User Data policy":
            migration_steps.append(
                f"- **{cat}**: Implement prominent user account and data deletion path in-app and publish a public, accessible web data deletion URL."
            )
            impl_checklist.append("- [ ] Build in-app 'Delete Account' UI option.")
            impl_checklist.append(
                "- [ ] Publish public web data deletion form and enter URL in Play Console store listing."
            )
            risk_assessment.append(
                f"- *{cat}*: Rejection or store listing removal for failure to comply with the mandatory deletion url policy."
            )
        elif cat == "Data Safety section":
            migration_steps.append(
                f"- **{cat}**: Audit all integrated SDKs (Firebase, Facebook, AppsFlyer) and update the Google Play Console Data Safety questionnaire to exactly align with runtime actions."
            )
            impl_checklist.append(
                "- [ ] Audit runtime network traffic from third-party SDKs."
            )
            impl_checklist.append(
                "- [ ] Update Play Console Data Safety questionnaire declarations."
            )
            risk_assessment.append(
                f"- *{cat}*: Data Safety mismatch is the top Google Play rejection cause, threatening developer account health."
            )
        elif cat == "AI-generated content policies":
            migration_steps.append(
                f"- **{cat}**: Integrate content filters and prominent in-app disclosures for AI features. Provide one-click report/flag controls next to generated outputs."
            )
            impl_checklist.append(
                "- [ ] Implement a prominent Play Policy disclosure dialog prior to accessing AI features."
            )
            impl_checklist.append(
                "- [ ] Add flagging/reporting buttons directly adjacent to all generative AI content blocks."
            )
            risk_assessment.append(
                f"- *{cat}*: Immediate rejection or app suspension under Google Play's AI-generated content guidelines."
            )
        elif cat == "Accessibility requirements":
            migration_steps.append(
                f"- **{cat}**: Ensure all touch targets measure at least 48dp in physical size, and provide contentDescription tags on all interactive image elements."
            )
            impl_checklist.append(
                "- [ ] Audit layout XML; verify all interactive targets measure >= 48dp."
            )
            impl_checklist.append(
                "- [ ] Add contentDescription attributes on all ImageViews and ImageButtons."
            )
            risk_assessment.append(
                f"- *{cat}*: Increased store rejection risk and potential litigation under global digital accessibility laws."
            )
        elif cat == "Device compatibility requirements":
            migration_steps.append(
                f"- **{cat}**: Support dynamic window resizing, multi-window layout scaling, and foldable display orientations."
            )
            impl_checklist.append(
                "- [ ] Configure android:resizeableActivity=true in manifest."
            )
            risk_assessment.append(
                f"- *{cat}*: Degraded UI experience and compatibility warnings on tablet/foldable devices."
            )
        elif cat == "Security Bulletins":
            migration_steps.append(
                f"- **{cat}**: Secure sensitive user secrets and credentials inside the hardware-backed Android Keystore system. Fix any outstanding vulnerability CVEs."
            )
            impl_checklist.append(
                "- [ ] Implement cryptographic token storage wrapper backed by Android Keystore."
            )
            risk_assessment.append(
                f"- *{cat}*: Exposure of sensitive local storage secrets to side-channel extraction attacks."
            )
        elif cat == "Android Enterprise requirements":
            migration_steps.append(
                f"- **{cat}**: Secure managed device compliance. Implement DevicePolicyManager controls for work profiles."
            )
            impl_checklist.append(
                "- [ ] Implement Work Profile boundaries; secure inter-profile communication."
            )
            risk_assessment.append(
                f"- *{cat}*: Non-compliance with corporate enterprise device management architectures."
            )
        elif cat == "Firebase policy updates":
            migration_steps.append(
                f"- **{cat}**: Migrate deprecated Firebase Dynamic Links configurations to Firebase Hosting deep links, App Links, or universal links."
            )
            impl_checklist.append(
                "- [ ] Remove Firebase Dynamic Links dependency; migrate scheme to standard App Links."
            )
            risk_assessment.append(
                f"- *{cat}*: App onboarding or link share redirection failure post-sunset of dynamic links."
            )
        else:
            # Generic category
            migration_steps.append(
                f"- **{cat}**: Verify that all play console guidelines for {cat} are followed."
            )
            impl_checklist.append(
                f"- [ ] Double check Play Console compliance dashboard for {cat} notifications."
            )
            risk_assessment.append(f"- *{cat}*: Standard policy non-compliance risk.")

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

    pr_template = f"""# PULL REQUEST DRAFT: Android and Google Play Regulatory Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored Android and Google Play developer requirements. It addresses target SDK versions, API deprecations, foreground service type updates, billing integrations, permission models, data safety declarations, and accessibility standards to satisfy modern Google Play publishing gates.

## 2. Background
Google Play enforces strict publishing gates, requiring target SDK levels to remain up-to-date and billing, permissions, and data sharing activities to be fully and accurately declared. Non-compliance leads to automatic rejection, or escalation against the developer account, up to suspension or termination.

## 3. Regulatory change
- **Google Play Developer Policies & Core Updates**: Target SDK 36 mandate by August 31, 2026, Play Billing Library v8+ enforcement, strict foreground service type rules on API 34+, and mandatory web deletion URL configuration.
- **Privacy & Security**: Mandatory migration from legacy SafetyNet to Play Integrity API, scoped media permissions enforcement, and static scanning verification of Data Safety declarations against runtime SDK tracking.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of update blockage or account warnings if publishing gates are not proactively cleared.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Minimum SDK requirements have been raised to 23 to secure modern API integrations while preserving support for 99%+ of active devices. Fallback flows are utilized on older devices for scoped storage and photo pickers.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the automated compliance guard checks locally.

## 10. Testing checklist
- [ ] Run deep integration tests verifying Play Billing Library checkout transacts smoothly.
- [ ] Confirm foreground services initialize without crashing on Android 14+ (API 34/35) devices.
- [ ] Run the Accessibility Scanner tool on all key application views.
- [ ] Verify that server-side Play Integrity checks validate payloads successfully.

## 11. Documentation checklist
- [ ] Publish the data deletion web portal and link it in the Play Console listing.
- [ ] Update `docs/ANDROID-POLICY-MIGRATION.md` with completed tasks.
- [ ] Update store listing metadata descriptions and privacy policy links.

## 12. Compliance impact
- **Publishing Gate**: Guarantees uninterrupted app submissions by meeting the Target SDK 36 and Billing Library v8 thresholds.
- **Account Health**: Mitigates compliance strikes, protecting the developer organization account against suspension.
- **Accessibility**: Aligns with TalkBack standards, improving general store content ratings.

## 13. Breaking changes
- Raising the minSdkVersion to 23 removes support for Android API levels 21/22.
- The removal of Firebase Dynamic Links sunsets legacy invite URLs.

## 14. Review checklist
- [ ] Code complies with Google Play's Restricted Permissions and Device and Network Abuse policies.
- [ ] Play Console declarations for foreground service types match the active manifest attributes.
- [ ] Third-party SDK compiled dependencies are fully updated and secure.

## 15. Approver recommendations
Ensure that the Play Console account owner has completed the personal/organization identity verification by the stated deadline, as failure to do so will block publishing regardless of code-level compliance. Double-check that billing client initialization flows align with the Billing v8 SDK specifications.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/ANDROID-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- ANDROID_POLICY_MONITOR_START -->",
        "# Android and Google Play Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-android.py` to track compliance areas.",
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
        lines.append(f"### Tasks for {cat}")
        lines.append(
            "- **Regulatory Impact**: High priority. Publishing gates require action."
        )

        if cat == "Target SDK requirements":
            lines.append(
                "- [ ] **Task 1**: Update `targetSdkVersion` in build.gradle files to 36."
            )
            lines.append(
                "- [ ] **Task 2**: Test target API level 36 behaviors on devices."
            )
        elif cat == "Play Billing":
            lines.append(
                "- [ ] **Task 1**: Migrate project dependencies to Billing Library version 8.0."
            )
            lines.append(
                "- [ ] **Task 2**: Perform test transactions on Google Play console sandbox."
            )
        elif cat == "User Data policy":
            lines.append(
                "- [ ] **Task 1**: Publish a public account and data deletion URL."
            )
            lines.append(
                "- [ ] **Task 2**: Connect the URL to the Play Console User Data safety form."
            )
        elif cat == "Foreground service policies":
            lines.append(
                "- [ ] **Task 1**: Specify foregroundServiceType inside the manifest service tags."
            )
            lines.append(
                "- [ ] **Task 2**: Register foreground service type video verification demo on Play Console."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Verify that all platform criteria for {cat} are checked and handled."
            )
        lines.append("")

    lines.append("<!-- ANDROID_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Android documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Android and Google Play Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live Google Play policy feeds"
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
        default="docs/ANDROID-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        help="Filepath to save the drafted PR (outputs to stdout if omitted)",
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live Google Play developer RSS feed...")
        # Android developers blog posts
        announcements.extend(
            parse_rss_feed(
                "https://android-developers.googleblog.com/feeds/posts/default"
            )
        )
        # Android security bulletin feed
        announcements.extend(
            parse_rss_feed("https://source.android.com/security/bulletin.xml")
        )

    # Fallback to mock data if live has no updates or mock is explicitly requested
    if args.mock or (not args.live and not args.mock) or not announcements:
        print(
            "Using comprehensive mock Android policy updates for compliance scanning..."
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

    # 2. Classify updates into the 19 required categories
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
    print(f"Scanning codebase under '{args.dir}' for Android integration signals...")
    scan_results = scan_codebase_for_android_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 5. Generate Pull Request draft
    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
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
