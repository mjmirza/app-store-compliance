#!/usr/bin/env python3
import os
import sys
import re
import argparse

# List of directory names to ignore during scan
IGNORE_DIRS = {
    "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
    ".dart_tool", "Carthage", "androidTest", "__tests__"
}

# Mapping of rule IDs to their detail
RULE_META = {
    "APPLE-ACCESSIBILITY-VOICEOVER": {
        "platform": "apple",
        "severity": "medium",
        "title": "VoiceOver support missing or incomplete",
        "fix": "Ensure all interactive components and decorative or informative images have correct accessibility labels, hints, and traits assigned."
    },
    "APPLE-ACCESSIBILITY-DYNAMICTYPE": {
        "platform": "apple",
        "severity": "medium",
        "title": "Dynamic Type support missing or overridden",
        "fix": "Use preferredFont(forTextStyle:) in UIKit and system/relative font styles in SwiftUI, ensuring adjustsFontForContentSizeCategory is enabled."
    },
    "APPLE-ACCESSIBILITY-REDUCEMOTION": {
        "platform": "apple",
        "severity": "medium",
        "title": "Reduce Motion accessibility setting ignored",
        "fix": "Check the Reduce Motion system status and disable or simplify non-essential animations when requested by the user."
    },
    "APPLE-ACCESSIBILITY-COLORCONTRAST": {
        "platform": "apple",
        "severity": "medium",
        "title": "Color Contrast and system settings ignored",
        "fix": "Use dynamic or system colors that automatically adapt, or monitor isDarkerSystemColorsEnabled to adjust contrast dynamically."
    },
    "APPLE-ACCESSIBILITY-HAPTICS": {
        "platform": "apple",
        "severity": "medium",
        "title": "Haptics tactile feedback missing on interactions",
        "fix": "Add haptic feedback to buttons, toggles, and swipe actions using UIImpactFeedbackGenerator or selection feedback."
    },
    "APPLE-ACCESSIBILITY-KEYBOARD": {
        "platform": "apple",
        "severity": "medium",
        "title": "Keyboard navigation and focus state support missing",
        "fix": "Support physical keyboard navigation by utilizing keyCommands in UIKit or focusable() and @FocusState in SwiftUI."
    },
    "ANDROID-ACCESSIBILITY-TALKBACK": {
        "platform": "google",
        "severity": "medium",
        "title": "TalkBack support missing or disabled",
        "fix": "Provide meaningful contentDescription values for all informative images and interactive views, and ensure importantForAccessibility is set correctly."
    },
    "ANDROID-ACCESSIBILITY-FONTSCALING": {
        "platform": "google",
        "severity": "medium",
        "title": "Font scaling disabled due to dp text sizing",
        "fix": "Always define text sizes in sp (scale-independent pixels) rather than dp to allow the system font scaling to work correctly."
    },
    "ANDROID-ACCESSIBILITY-HIGHCONTRAST": {
        "platform": "google",
        "severity": "medium",
        "title": "Hardcoded colors ignoring high contrast settings",
        "fix": "Reference semantic colors or color resources so the app automatically respects high contrast themes."
    },
    "ANDROID-ACCESSIBILITY-SCANNER": {
        "platform": "google",
        "severity": "medium",
        "title": "Touch target sizes below 48dp",
        "fix": "Ensure all interactive elements have a minimum touch target area of 48dp x 48dp by using padding, minWidth, and minHeight."
    }
}

def scan_files(directory):
    ios_files = []
    android_files = []
    for root, dirs, files in os.walk(directory):
        # In-place directory filtering to ignore unwanted folders
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith("Tests")]
        for file in files:
            path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in {".swift", ".m", ".h", ".plist", ".storyboard", ".xib"}:
                ios_files.append(path)
            elif ext in {".kt", ".java", ".xml"}:
                android_files.append(path)
    return ios_files, android_files

def run_rule_scan(rule_id, ios_files, android_files):
    findings = []

    if rule_id == "APPLE-ACCESSIBILITY-VOICEOVER":
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            for match in re.finditer(r"\bImage\s*\(([^)]+)\)", content):
                expr = match.group(1)
                if "decorative:" in expr or "systemName:" in expr:
                    continue
                start_idx = match.start()
                context = content[start_idx:start_idx + 300]
                if not any(kw in context for kw in ["accessibilityLabel", "accessibilityIdentifier", "accessibilityHidden", "accessibilityElement"]):
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "SwiftUI Image used without accessibilityLabel or decorative initialization.",
                        "fix": "Initialize decorative images as Image(decorative: ...) or add an explicit .accessibilityLabel(...) modifier."
                    })

            if "UIButton" in content or "UIImageView" in content:
                if not any(kw in content for kw in ["accessibilityLabel", "accessibilityIdentifier", "isAccessibilityElement"]):
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "UIButton / UIImageView declaration",
                        "message": "UIKit components found but no accessibility attributes (accessibilityLabel, isAccessibilityElement) are references in the file.",
                        "fix": "Assign meaningful accessibilityLabel properties to interactive UIKit components."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-DYNAMICTYPE":
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m") or f.endswith(".h")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            for match in re.finditer(r"\.system\(size:\s*\d+", content):
                start_idx = match.start()
                line_no = content.count("\n", 0, start_idx) + 1
                findings.append({
                    "file": f,
                    "line": line_no,
                    "rule_id": rule_id,
                    "match": match.group(0),
                    "message": "Hardcoded system font size detected which prevents Dynamic Type scaling.",
                    "fix": "Use SwiftUI relative text styles like .font(.body) or wrap custom font sizes in dynamic-type scaled modifiers."
                })

            for match in re.finditer(r"UIFont\.systemFont\(ofSize:\s*\d+", content):
                start_idx = match.start()
                line_no = content.count("\n", 0, start_idx) + 1
                if "adjustsFontForContentSizeCategory" not in content:
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Hardcoded UIFont used without adjusting for content size category.",
                        "fix": "Use UIFont.preferredFont(forTextStyle:) and set adjustsFontForContentSizeCategory = true on your labels."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-REDUCEMOTION":
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            if "withAnimation" in content or "UIView.animate" in content:
                if "isReduceMotionEnabled" not in content and "accessibilityReduceMotion" not in content:
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "Animation usage",
                        "message": "Animations used without checking Reduce Motion state.",
                        "fix": "Check UIAccessibility.isReduceMotionEnabled or SwiftUI's accessibilityReduceMotion environment variable to disable or simplify animations."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-COLORCONTRAST":
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            for match in re.finditer(r"UIColor\s*\(\s*red:\s*\d+", content):
                if "isDarkerSystemColorsEnabled" not in content and "darkerSystemColors" not in content:
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Static UIColor with raw RGB values does not support custom high-contrast modes.",
                        "fix": "Utilize asset-catalog named dynamic colors or respect UIAccessibility.isDarkerSystemColorsEnabled."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-HAPTICS":
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            if "onTapGesture" in content or "Button" in content:
                if not any(kw in content for kw in ["FeedbackGenerator", "CoreHaptics", "CHHapticEngine"]):
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "Interactive controls without haptics",
                        "message": "Interactive taps or gestures used but no haptic feedback generator referenced.",
                        "fix": "Incorporate UIImpactFeedbackGenerator or UISelectionFeedbackGenerator for interactive feedback."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-KEYBOARD":
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            if "focusable" in content and "FocusState" not in content and "focused" not in content:
                findings.append({
                    "file": f,
                    "line": 1,
                    "rule_id": rule_id,
                    "match": "focusable",
                    "message": "Focusable elements used without focus state tracking.",
                    "fix": "Use @FocusState to track and programmatically move keyboard focus for accessibility keyboard users."
                })

    elif rule_id == "ANDROID-ACCESSIBILITY-TALKBACK":
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"<ImageView\b|<ImageButton\b", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    elem_block = content[start_idx:content.find(">", start_idx) + 1]
                    if "contentDescription" not in elem_block:
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": elem_block.split("\n")[0],
                            "message": "XML image view missing contentDescription attribute.",
                            "fix": "Add an android:contentDescription attribute with descriptive text, or set android:importantForAccessibility=\"no\" if decorative."
                        })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"\bImage\s*\(([^)]+)\)", content):
                    expr = match.group(1)
                    if "contentDescription" not in expr:
                        start_idx = match.start()
                        line_no = content.count("\n", 0, start_idx) + 1
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": match.group(0),
                            "message": "Compose Image element missing contentDescription parameter.",
                            "fix": "Provide a descriptive contentDescription or pass null explicitly if decorative."
                        })

    elif rule_id == "ANDROID-ACCESSIBILITY-FONTSCALING":
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"android:textSize\s*=\s*\"(\d+dp)\"", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": f"Text size specified in dp ({match.group(1)}) instead of sp.",
                        "fix": "Change text size unit from dp to sp (scale-independent pixels) so font scaling is supported."
                    })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"fontSize\s*=\s*(\d+)\.dp", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose text fontSize specified in dp instead of sp.",
                        "fix": "Change Jetpack Compose text font size unit to sp (e.g. 16.sp)."
                    })

    elif rule_id == "ANDROID-ACCESSIBILITY-HIGHCONTRAST":
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"android:(textColor|background)\s*=\s*\"(#[0-9A-Fa-f]{6,8})\"", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": f"Hardcoded hex color value ({match.group(2)}) ignored high contrast theme settings.",
                        "fix": "Use semantic theme references or color resources (e.g. ?attr/colorOnSurface) rather than static hex strings."
                    })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"Color\s*\(\s*0xFF[0-9A-Fa-f]{6}\s*\)", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose Color declared with hardcoded hex code.",
                        "fix": "Reference semantic colors from your app Theme material colors scheme instead of hardcoded values."
                    })

    elif rule_id == "ANDROID-ACCESSIBILITY-SCANNER":
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"android:(layout_width|layout_height|minWidth|minHeight)\s*=\s*\"([1-3][0-9]|4[0-7]|[1-9])dp\"", content):
                    if "layout_width=\"wrap_content\"" not in content and "layout_height=\"wrap_content\"" not in content:
                        start_idx = match.start()
                        line_no = content.count("\n", 0, start_idx) + 1
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": match.group(0),
                            "message": f"Component dimension ({match.group(0)}) is below the recommended 48dp touch target threshold.",
                            "fix": "Increase interactive component width and height to at least 48dp or add layout padding."
                        })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"\.size\s*\(\s*([1-3][0-9]|4[0-7]|[1-9])\.dp\s*\)", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose view size is below the recommended 48dp touch target threshold.",
                        "fix": "Enlarge the touch target size of the clickable control to at least 48dp x 48dp."
                    })

    return findings

def generate_markdown_report(directory, ios_files, android_files, all_findings, report_filepath):
    lines = []
    lines.append("# Continuous Accessibility Compliance Audit Report")
    lines.append("")
    lines.append(f"Target Directory: {os.path.abspath(directory)}")
    lines.append(f"Scanned Files: iOS ({len(ios_files)} files), Android ({len(android_files)} files)")

    crit = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "critical")
    high = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "high")
    med = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "medium")
    low = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "low")

    overall_status = "BLOCKED" if crit > 0 or high > 0 else ("ADVISORY" if all_findings else "PASSED")
    lines.append(f"Overall Compliance Status: {overall_status}")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("This report documents the findings and recommendations from the static continuous accessibility audit across iOS (Apple) and Android platforms. The evaluation covers mandatory accessibility domains aligned with European Accessibility Act (EAA Directive 2019/882 / EN 301 549 Chapter 11), US ADA Title II (28 CFR Part 35), and mobile store platform design guidelines.")
    lines.append("")
    lines.append(f"Summary: critical={crit} high={high} medium={med} low={low}")
    lines.append("")

    lines.append("## Evaluated Accessibility Rules Summary")
    lines.append("")
    lines.append("| Platform | Rule ID | Title | Severity | Status |")
    lines.append("| --- | --- | --- | --- | --- |")

    for rule_id, meta in RULE_META.items():
        rule_findings = [f for f in all_findings if f["rule_id"] == rule_id]
        status = "REGRESSION" if rule_findings else "PASSED"
        platform_name = "Apple (iOS)" if meta["platform"] == "apple" else "Android"
        lines.append(f"| {platform_name} | {rule_id} | {meta['title']} | {meta['severity'].upper()} | {status} |")
    lines.append("")

    lines.append("## Detailed Platform Requirements and Audit Findings")
    lines.append("")

    lines.append("### Apple (iOS / iPadOS) Accessibility Requirements")
    lines.append("")
    apple_rules = [rid for rid, m in RULE_META.items() if m["platform"] == "apple"]
    for rid in apple_rules:
        meta = RULE_META[rid]
        r_findings = [f for f in all_findings if f["rule_id"] == rid]
        lines.append(f"#### {rid}: {meta['title']}")
        lines.append(f"- Platform: Apple (iOS)")
        lines.append(f"- Severity: {meta['severity'].upper()}")
        lines.append(f"- Remediation: {meta['fix']}")
        lines.append(f"- Status: {'REGRESSION DETECTED (' + str(len(r_findings)) + ' issue(s))' if r_findings else 'PASSED (0 issues)'}")
        lines.append("")
        if r_findings:
            lines.append("| File | Line | Context | Issue Description | Fix Recommendation |")
            lines.append("| --- | --- | --- | --- | --- |")
            for f in r_findings:
                rel = os.path.relpath(f["file"], directory)
                ctx = f["match"].replace("|", "\\|").replace("\n", " ")
                msg = f["message"].replace("|", "\\|")
                fix = f["fix"].replace("|", "\\|")
                lines.append(f"| {rel} | {f['line']} | `{ctx}` | {msg} | {fix} |")
            lines.append("")

    lines.append("### Android Accessibility Requirements")
    lines.append("")
    android_rules = [rid for rid, m in RULE_META.items() if m["platform"] == "google"]
    for rid in android_rules:
        meta = RULE_META[rid]
        r_findings = [f for f in all_findings if f["rule_id"] == rid]
        lines.append(f"#### {rid}: {meta['title']}")
        lines.append(f"- Platform: Android")
        lines.append(f"- Severity: {meta['severity'].upper()}")
        lines.append(f"- Remediation: {meta['fix']}")
        lines.append(f"- Status: {'REGRESSION DETECTED (' + str(len(r_findings)) + ' issue(s))' if r_findings else 'PASSED (0 issues)'}")
        lines.append("")
        if r_findings:
            lines.append("| File | Line | Context | Issue Description | Fix Recommendation |")
            lines.append("| --- | --- | --- | --- | --- |")
            for f in r_findings:
                rel = os.path.relpath(f["file"], directory)
                ctx = f["match"].replace("|", "\\|").replace("\n", " ")
                msg = f["message"].replace("|", "\\|")
                fix = f["fix"].replace("|", "\\|")
                lines.append(f"| {rel} | {f['line']} | `{ctx}` | {msg} | {fix} |")
            lines.append("")

    lines.append("## Platform Mechanics and Best Practices")
    lines.append("")
    lines.append("### Apple Accessibility Features")
    lines.append("1. VoiceOver: Ensure all interactive views declare `accessibilityLabel`, `accessibilityHint`, and traits. Decorative graphics should use `Image(decorative: ...)` or `isAccessibilityElement = false`.")
    lines.append("2. Dynamic Type: Use dynamic text styles like `.font(.body)` in SwiftUI and `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory = true` in UIKit to allow font resizing.")
    lines.append("3. Reduce Motion: Check `UIAccessibility.isReduceMotionEnabled` or SwiftUI `@Environment(\\.accessibilityReduceMotion)` to disable or simplify non-essential animations.")
    lines.append("4. Color Contrast: Support system dark/light modes and dynamic colors. Observe `UIAccessibility.isDarkerSystemColorsEnabled` for high-contrast adjustments.")
    lines.append("5. Haptics: Provide subtle tactile haptic feedback on interactive buttons and actions using `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator`.")
    lines.append("6. Keyboard Navigation: Support full hardware keyboard navigation by using `@FocusState` in SwiftUI or `keyCommands` in UIKit.")
    lines.append("")

    lines.append("### Android Accessibility Features")
    lines.append("1. TalkBack: Provide meaningful `contentDescription` attributes on all XML `ImageView`/`ImageButton` elements and Compose `Image` components, or set `importantForAccessibility=\"no\"` on decorative elements.")
    lines.append("2. Font Scaling: Always declare text sizes using scale-independent pixels (`sp`) rather than fixed density pixels (`dp`) so font scaling preferences are honored.")
    lines.append("3. High Contrast: Reference theme attributes (e.g. `?attr/colorOnSurface` or `MaterialTheme.colorScheme.primary`) rather than hardcoded hex colors to adapt to contrast themes.")
    lines.append("4. Accessibility Scanner: Ensure all touch targets meet or exceed the recommended minimum size of 48dp x 48dp using layout padding or `minWidth`/`minHeight` constraints.")
    lines.append("")

    lines.append("## Strategic Recommendations for Ongoing Compliance")
    lines.append("1. Automated CI Integration: Incorporate `scripts/accessibility-audit.py` into continuous integration pipelines to catch accessibility regressions before PR merge.")
    lines.append("2. Accessibility Testing Tools: Utilize Apple Accessibility Inspector (Xcode) and Android Accessibility Scanner on physical devices during release QA cycles.")
    lines.append("3. Regulatory Deadlines Alignment: Ensure compliance with EAA (Directive EU 2019/882 / EN 301 549) mandatory requirements and US ADA Title II mobile application standards.")
    lines.append("")

    os.makedirs(os.path.dirname(os.path.abspath(report_filepath)), exist_ok=True)
    with open(report_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Static continuous accessibility compliance auditor.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory of the project to scan.")
    parser.add_argument("--rule", help="Scan only a specific accessibility rule ID.")
    parser.add_argument("--report-out", "--output-report", help="Path to write Markdown accessibility compliance report.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Directory not found: {args.directory}")
        return 0

    ios_files, android_files = scan_files(args.directory)

    rules_to_scan = [args.rule] if args.rule else list(RULE_META.keys())

    all_findings = []
    for rule in rules_to_scan:
        if rule not in RULE_META:
            continue
        findings = run_rule_scan(rule, ios_files, android_files)
        all_findings.extend(findings)

    # Sort findings by rule ID and file path
    all_findings.sort(key=lambda x: (x["rule_id"], x["file"], x["line"]))

    if args.report_out:
        generate_markdown_report(args.directory, ios_files, android_files, all_findings, args.report_out)
        print(f"Accessibility report written successfully to: {args.report_out}")

    print("== Accessibility Compliance Audit ==")
    print(f"Audited directory. {args.directory}")
    print(f"Scanned files. iOS={len(ios_files)} Android={len(android_files)}")
    print("")

    if not all_findings:
        print("Clean. No accessibility compliance regressions found.")
        print("")
        print("Summary. critical=0 high=0 medium=0 low=0")
        return 0

    # Print detailed findings
    crit = 0
    high = 0
    med = 0
    low = 0

    for f in all_findings:
        meta = RULE_META[f["rule_id"]]
        sev = meta["severity"]
        if sev == "critical":
            crit += 1
        elif sev == "high":
            high += 1
        elif sev == "medium":
            med += 1
        else:
            low += 1

        print(f"  [{sev.upper()}] {f['rule_id']}  ({f['file']}:{f['line']})")
        print(f"      context: {f['match']}")
        print(f"      reason:  {f['message']}")
        print(f"      fix:     {f['fix']}")
        print("")

    print(f"Summary. critical={crit} high={high} medium={med} low={low}")
    print("Reference. docs/EU-REGULATORY-2026.md and docs/PLATFORM-MECHANICS-2026.md")

    return 0

if __name__ == "__main__":
    sys.exit(main())
