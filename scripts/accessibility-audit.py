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
        # SwiftUI Image without accessibility modifiers, or UIKit views without accessibility attributes
        # Scan SwiftUI Images: e.g. Image("name") or Image(systemName: "...")
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            # Find SwiftUI Image usages
            for match in re.finditer(r"\bImage\s*\(([^)]+)\)", content):
                expr = match.group(1)
                # Ignore images explicitly defined as decorative or having system accessibility labels/hidden
                if "decorative:" in expr or "systemName:" in expr:
                    continue
                # Simple parsing check: does the immediate context (within 5 lines) have accessibility modifiers?
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

            # Look for UIButton / UIImageView declarations in UIKit swift without accessibility properties
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
        # Check SwiftUI hardcoded system fonts, e.g. .font(.system(size: ...))
        # Or UIKit Font declarations like UIFont.systemFont(ofSize: ...)
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
                # Check if adjustsFontForContentSizeCategory is present in the file
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
        # Find transition, withAnimation or UIView.animate without checking reduce motion
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
        # Find hardcoded UIColors or SwiftUI Colors without dynamic adaptivity or isDarkerSystemColorsEnabled
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            # Flag static CGColors or UIColors using hardcoded color specs without dynamic checking
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
        # Scan for interactive actions/handlers without feedback generator references
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
        # Scan for customized controls or keyboard handling missing proper focus or keyCommands
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
        # Look for XML layout elements or Compose Image without contentDescription
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Find ImageView or ImageButton
                for match in re.finditer(r"<ImageView\b|<ImageButton\b", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    # Check if this element block (up to next >) has contentDescription
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
                # Find Jetpack Compose Image usages
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
        # Search for XML textSize with dp units, or Compose fontSize with dp units
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
        # Scan for hardcoded background or text colors using hex code values directly in XML or Compose
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
        # Scan XML and Compose layouts for touch target dimensions or paddings under 48dp
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Match layout_width or layout_height with dimensions below 48dp (e.g. 10dp to 47dp)
                # Let's match layout_width or layout_height or minWidth or minHeight under 48dp
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
                # Match clickable elements that may be too small
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

def generate_markdown_report(directory, ios_files, android_files, all_findings, report_path):
    lines = []
    lines.append("# Mobile Accessibility Compliance Verification Report")
    lines.append("")
    lines.append(f"Target Directory: {directory}")
    lines.append(f"Scanned Files: iOS ({len(ios_files)} files), Android ({len(android_files)} files)")
    status_str = "COMPLIANT (PASSED)" if not all_findings else "REGRESSIONS DETECTED (ACTION REQUIRED)"
    lines.append(f"Overall Accessibility Status: {status_str}")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("This report documents the automated continuous accessibility audit verifying compliance across iOS (VoiceOver, Dynamic Type, Reduce Motion, Color Contrast, Haptics, Keyboard Navigation) and Android (TalkBack, Font Scaling, High Contrast, Accessibility Scanner Recommendations) platforms in accordance with WCAG 2.1 AA, EN 301 549, and platform guidelines.")
    lines.append("")

    lines.append("## Domain Verification Matrix")
    lines.append("")
    lines.append("| Platform | Domain / Requirement | Rule ID | Audit Status | Guidance & Best Practices |")
    lines.append("| --- | --- | --- | --- | --- |")

    domain_mapping = [
        ("Apple iOS / iPadOS", "VoiceOver Screen Reader Support", "APPLE-ACCESSIBILITY-VOICEOVER", "Provide explicit accessibilityLabel and accessibilityHint on interactive elements; mark decorative graphics as decorative or hidden."),
        ("Apple iOS / iPadOS", "Dynamic Type Text Scaling", "APPLE-ACCESSIBILITY-DYNAMICTYPE", "Use relative text styles (.font(.body) or preferredFont(forTextStyle:)) and enable adjustsFontForContentSizeCategory."),
        ("Apple iOS / iPadOS", "Reduce Motion System Setting", "APPLE-ACCESSIBILITY-REDUCEMOTION", "Respect UIAccessibility.isReduceMotionEnabled and @Environment(\\.accessibilityReduceMotion) to disable or simplify non-essential animations."),
        ("Apple iOS / iPadOS", "Color Contrast & Dynamic System Colors", "APPLE-ACCESSIBILITY-COLORCONTRAST", "Use dynamic asset catalog colors or respect UIAccessibility.isDarkerSystemColorsEnabled to meet WCAG 4.5:1 contrast ratio."),
        ("Apple iOS / iPadOS", "Haptic Tactile Feedback", "APPLE-ACCESSIBILITY-HAPTICS", "Provide haptic tactile feedback for primary actions using UIImpactFeedbackGenerator or UISelectionFeedbackGenerator."),
        ("Apple iOS / iPadOS", "Keyboard Navigation & Focus Traversal", "APPLE-ACCESSIBILITY-KEYBOARD", "Support hardware keyboard navigation via keyCommands in UIKit or focusable() and @FocusState in SwiftUI."),
        ("Android / Google Play", "TalkBack Screen Reader Support", "ANDROID-ACCESSIBILITY-TALKBACK", "Define meaningful android:contentDescription attributes for informative images/views, or set importantForAccessibility=\"no\" for decorative views."),
        ("Android / Google Play", "Font Scaling (sp vs dp)", "ANDROID-ACCESSIBILITY-FONTSCALING", "Always declare text sizes in scale-independent pixels (sp) rather than density-independent pixels (dp) to support user font scaling."),
        ("Android / Google Play", "High Contrast & Semantic Color System", "ANDROID-ACCESSIBILITY-HIGHCONTRAST", "Reference Material theme attributes (?attr/colorOnSurface, MaterialTheme.colorScheme) rather than hardcoded hex color values."),
        ("Android / Google Play", "Accessibility Scanner Touch Target Area", "ANDROID-ACCESSIBILITY-SCANNER", "Ensure all interactive controls meet or exceed the mandatory 48dp x 48dp minimum touch target size threshold."),
    ]

    rule_finding_counts = {r_id: 0 for _, _, r_id, _ in domain_mapping}
    for f in all_findings:
        r_id = f["rule_id"]
        if r_id in rule_finding_counts:
            rule_finding_counts[r_id] += 1

    for platform, domain, rule_id, guidance in domain_mapping:
        count = rule_finding_counts.get(rule_id, 0)
        status = "PASSED (0 Issues)" if count == 0 else f"REGRESSION ({count} Issue(s))"
        lines.append(f"| {platform} | {domain} | {rule_id} | {status} | {guidance} |")

    lines.append("")

    lines.append("## Accessibility Regressions & Findings")
    lines.append("")
    if not all_findings:
        lines.append("Zero accessibility regressions detected. All scanned codebase assets comply with automated accessibility standards.")
        lines.append("")
    else:
        lines.append("| Severity | Rule ID | File & Line | Context | Issue Description | Remediation |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for f in all_findings:
            sev = RULE_META[f["rule_id"]]["severity"].upper()
            file_loc = f"{f['file']}:{f['line']}"
            context = f"`{f['match']}`"
            msg = f["message"]
            fix = f["fix"]
            lines.append(f"| {sev} | {f['rule_id']} | {file_loc} | {context} | {msg} | {fix} |")
        lines.append("")

    lines.append("## Platform Recommendations & Strategic Improvements")
    lines.append("")
    lines.append("### Apple (iOS / iPadOS / macOS)")
    lines.append("1. **VoiceOver Accessibility Tree:** Audit custom SwiftUI components and ensure complex view hierarchies use `.accessibilityElement(children: .combine)` to group related UI elements logically.")
    lines.append("2. **Dynamic Type Layout Flexibility:** Ensure scroll views and auto-layout constraints allow containers to expand gracefully when text sizes scale up to 310% under Larger Accessibility Sizes.")
    lines.append("3. **Reduce Motion Compliance:** Implement conditional fallback logic for layout transitions and video autoplay whenever `isReduceMotionEnabled` evaluates to `true`.")
    lines.append("4. **Color Contrast Verification:** Audit all custom brand colors against light and dark backgrounds using WCAG 2.1 AA 4.5:1 ratio targets for standard body text and 3:1 for large text.")
    lines.append("5. **Haptic Feedback:** Ensure interactive controls (buttons, segmented controls, custom switches) trigger subtle haptic feedback using `UIImpactFeedbackGenerator` or `CoreHaptics`.")
    lines.append("6. **Keyboard Navigation & Hardware Controls:** Verify full hardware keyboard navigation support via `@FocusState` and explicit keyboard shortcut bindings for power users.")
    lines.append("")
    lines.append("### Android (Google Play)")
    lines.append("1. **TalkBack Traversal Order:** Test screen reader focus ordering in complex XML and Jetpack Compose layouts using `traversalIndex` and `isTraversalGroup` modifiers.")
    lines.append("2. **Font Scaling Resilience:** Ensure layouts do not truncate or clip text when the system font scaling factor is set to 200%. Avoid fixed height containers (`height = 40.dp`) around text views.")
    lines.append("3. **High Contrast Mode Support:** Avoid hardcoded hex color codes in layouts. Utilize semantic Material 3 tokens (`MaterialTheme.colorScheme.onSurface`) so the app adapts seamlessly to Android High Contrast text modes.")
    lines.append("4. **Accessibility Scanner Integration:** Target a standard minimum touch area of 48dp x 48dp for all clickable controls using `Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)` or layout padding.")
    lines.append("")

    lines.append("## Summary Statistics")
    crit = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "critical")
    high = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "high")
    med = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "medium")
    low = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "low")
    lines.append(f"- Critical Issues: {crit}")
    lines.append(f"- High Severity Issues: {high}")
    lines.append(f"- Medium Severity Issues: {med}")
    lines.append(f"- Low Severity Issues: {low}")
    lines.append(f"- Total Findings: {len(all_findings)}")

    report_dir = os.path.dirname(os.path.abspath(report_path))
    if report_dir and not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Accessibility report successfully saved to: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Static continuous accessibility compliance auditor.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory of the project to scan.")
    parser.add_argument("--rule", help="Scan only a specific accessibility rule ID.")
    parser.add_argument("--report-out", help="Path to output a comprehensive Markdown accessibility compliance report.")
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

    print("== Accessibility Compliance Audit ==")
    print(f"Audited directory. {args.directory}")
    print(f"Scanned files. iOS={len(ios_files)} Android={len(android_files)}")
    print("")

    if args.report_out:
        generate_markdown_report(args.directory, ios_files, android_files, all_findings, args.report_out)

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

    # Exit with 0 on advisory findings since accessibility represents medium store risk
    return 0

if __name__ == "__main__":
    sys.exit(main())
