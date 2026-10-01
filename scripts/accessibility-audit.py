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

def generate_report(directory, ios_files, android_files, all_findings, report_path):
    crit = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "critical")
    high = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "high")
    med = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "medium")
    low = sum(1 for f in all_findings if RULE_META[f["rule_id"]]["severity"] == "low")

    lines = []
    lines.append("# Accessibility Compliance Report")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("This report details the continuous accessibility compliance audit performed across the codebase. Evaluation covers mandatory accessibility requirements under the European Accessibility Act (EAA / EN 301 549), WCAG 2.1 AA, Apple App Store Review Guidelines, and Google Play Accessibility Guidelines.")
    lines.append("")
    lines.append(f"- **Audited Directory**: `{directory}`")
    lines.append(f"- **Scanned Files**: {len(ios_files)} iOS files, {len(android_files)} Android files")
    lines.append(f"- **Total Findings**: {len(all_findings)} (Critical: {crit}, High: {high}, Medium: {med}, Low: {low})")
    lines.append(f"- **Compliance Status**: {'Passed' if not all_findings else 'Action Required'}")
    lines.append("")
    lines.append("## Evaluated Accessibility Rules")
    lines.append("")
    lines.append("### Apple (iOS / iPadOS / macOS)")
    lines.append("")
    lines.append("1. **VoiceOver (`APPLE-ACCESSIBILITY-VOICEOVER`)**")
    lines.append("   - **Requirement**: Informative images and interactive components must have clear accessibility labels, hints, and traits assigned. Decorative images must be explicitly hidden or marked decorative.")
    lines.append("   - **Best Practice**: Use `Image(decorative: ...)` in SwiftUI or set `isAccessibilityElement = false` in UIKit for decorative elements. Ensure all buttons and controls have descriptive `accessibilityLabel` properties.")
    lines.append("")
    lines.append("2. **Dynamic Type (`APPLE-ACCESSIBILITY-DYNAMICTYPE`)**")
    lines.append("   - **Requirement**: App text must dynamically scale in response to user text size settings without layout clipping or text truncation.")
    lines.append("   - **Best Practice**: Use relative text styles such as `.font(.body)` in SwiftUI or `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory = true` in UIKit instead of hardcoded point sizes.")
    lines.append("")
    lines.append("3. **Reduce Motion (`APPLE-ACCESSIBILITY-REDUCEMOTION`)**")
    lines.append("   - **Requirement**: Respect user preference for reduced motion by disabling or simplifying screen transitions, parallax effects, and complex animations.")
    lines.append("   - **Best Practice**: Check `UIAccessibility.isReduceMotionEnabled` or SwiftUI `@Environment(\\.accessibilityReduceMotion)` before executing non-essential UI animations.")
    lines.append("")
    lines.append("4. **Color Contrast (`APPLE-ACCESSIBILITY-COLORCONTRAST`)**")
    lines.append("   - **Requirement**: Maintain WCAG 2.1 AA minimum contrast ratios (4.5:1 for standard text) and adapt dynamically to high-contrast accessibility settings.")
    lines.append("   - **Best Practice**: Use Asset Catalog dynamic colors or system dynamic UIColors. Monitor `UIAccessibility.isDarkerSystemColorsEnabled` to boost contrast when requested.")
    lines.append("")
    lines.append("5. **Haptics (`APPLE-ACCESSIBILITY-HAPTICS`)**")
    lines.append("   - **Requirement**: Provide tactile feedback on user actions to reinforce visual and audible UI states for sensory accessibility.")
    lines.append("   - **Best Practice**: Trigger `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator` on key button presses, toggles, and state changes.")
    lines.append("")
    lines.append("6. **Keyboard Navigation (`APPLE-ACCESSIBILITY-KEYBOARD`)**")
    lines.append("   - **Requirement**: All interactive elements must be focusable and operable using external physical keyboards or assistive navigation devices.")
    lines.append("   - **Best Practice**: Implement `@FocusState` and `.focusable()` in SwiftUI or `keyCommands` in UIKit with distinct visual focus rings.")
    lines.append("")
    lines.append("### Android")
    lines.append("")
    lines.append("1. **TalkBack (`ANDROID-ACCESSIBILITY-TALKBACK`)**")
    lines.append("   - **Requirement**: All interactive views and informative images must expose meaningful content descriptions to screen readers.")
    lines.append("   - **Best Practice**: Provide `android:contentDescription` in XML layouts and `contentDescription` parameters in Jetpack Compose `Image` calls. Set `null` explicitly for purely decorative views.")
    lines.append("")
    lines.append("2. **Font Scaling (`ANDROID-ACCESSIBILITY-FONTSCALING`)**")
    lines.append("   - **Requirement**: Text sizing must adapt to Android system font scale and display size preferences.")
    lines.append("   - **Best Practice**: Define all text sizes using `sp` (scale-independent pixels) rather than `dp`. Avoid capping or disabling max font scale.")
    lines.append("")
    lines.append("3. **High Contrast (`ANDROID-ACCESSIBILITY-HIGHCONTRAST`)**")
    lines.append("   - **Requirement**: App colors must support high-contrast theme overrides and night/dark mode dynamic contrast.")
    lines.append("   - **Best Practice**: Reference Material Theme semantic attributes (`?attr/colorOnSurface`, `MaterialTheme.colorScheme`) rather than hardcoded hex color strings.")
    lines.append("")
    lines.append("4. **Accessibility Scanner Recommendations (`ANDROID-ACCESSIBILITY-SCANNER`)**")
    lines.append("   - **Requirement**: Interactive touch targets must meet minimum size standards to accommodate motor impairments.")
    lines.append("   - **Best Practice**: Ensure interactive elements have a minimum physical touch target size of 48dp x 48dp through padding or `minWidth`/`minHeight` layout attributes.")
    lines.append("")
    lines.append("## Findings & Regressions")
    lines.append("")

    if not all_findings:
        lines.append("No accessibility regressions found in the scanned files.")
        lines.append("")
    else:
        lines.append(f"Found {len(all_findings)} accessibility regression(s):")
        lines.append("")
        lines.append("| Rule ID | Platform | File | Line | Issue | Recommended Fix |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for f in all_findings:
            meta = RULE_META[f["rule_id"]]
            plat = meta["platform"].capitalize()
            rel_file = os.path.relpath(f["file"], directory)
            lines.append(f"| `{f['rule_id']}` | {plat} | `{rel_file}` | {f['line']} | {f['message']} | {f['fix']} |")
        lines.append("")

    lines.append("## Recommended Improvements")
    lines.append("")
    lines.append("1. **Continuous Automated Auditing**: Run `python3 scripts/accessibility-audit.py` in CI workflows on every pull request.")
    lines.append("2. **Manual Assistive Tech Testing**: Perform manual testing using physical iOS devices with VoiceOver and Android devices with TalkBack and Accessibility Scanner.")
    lines.append("3. **Regulatory Alignment**: Maintain compliance with European Accessibility Act (EAA) EN 301 549 standards and WCAG 2.1 Level AA criteria across all release candidates.")
    lines.append("")

    report_content = "\n".join(lines)
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

def main():
    parser = argparse.ArgumentParser(description="Static continuous accessibility compliance auditor.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory of the project to scan.")
    parser.add_argument("--rule", help="Scan only a specific accessibility rule ID.")
    parser.add_argument("--report-out", help="Output path for Markdown accessibility report.")
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
        generate_report(args.directory, ios_files, android_files, all_findings, args.report_out)
        print(f"Report generated at: {args.report_out}")

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

    # Exit with 0 on advisory findings since accessibility represents medium store risk
    return 0

if __name__ == "__main__":
    sys.exit(main())
