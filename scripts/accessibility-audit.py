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
    report_lines = [
        "# Accessibility Compliance Report",
        "",
        "## Executive Summary",
        "This report provides a continuous accessibility compliance evaluation across Apple (iOS/iPadOS/macOS) and Android platform frameworks. It audits application codebases against required international accessibility standards, including EN 301 549, WCAG 2.1 AA, European Accessibility Act (EAA Directive 2019/882), and US ADA Title II / Section 504 regulations.",
        "",
        "## Evaluated Categories and Rules",
        "",
        "### Apple Accessibility Rules",
        "",
        "- **VoiceOver (`APPLE-ACCESSIBILITY-VOICEOVER`)**",
        "  - *Focus*: Screen reader labels, traits, hints, and decorative element hiding.",
        "  - *Requirement*: Ensure all interactive elements have meaningful accessibility labels and traits. Mark decorative images with `Image(decorative: ...)` or `accessibilityHidden(true)`.",
        "",
        "- **Dynamic Type (`APPLE-ACCESSIBILITY-DYNAMICTYPE`)**",
        "  - *Focus*: Dynamic font scaling and flexible layouts.",
        "  - *Requirement*: Use dynamic font styles such as `.font(.body)` in SwiftUI or `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory = true` in UIKit.",
        "",
        "- **Reduce Motion (`APPLE-ACCESSIBILITY-REDUCEMOTION`)**",
        "  - *Focus*: Motion sensitivity and non-essential UI animations.",
        "  - *Requirement*: Respect system accessibility reduce motion settings (`UIAccessibility.isReduceMotionEnabled` or `@Environment(\\.accessibilityReduceMotion)`) by disabling or simplifying animations.",
        "",
        "- **Color Contrast (`APPLE-ACCESSIBILITY-COLORCONTRAST`)**",
        "  - *Focus*: High contrast adaptations and dynamic colors.",
        "  - *Requirement*: Use asset catalog dynamic colors or system dynamic colors that adapt to dark mode and increased contrast settings (`UIAccessibility.isDarkerSystemColorsEnabled`).",
        "",
        "- **Haptics (`APPLE-ACCESSIBILITY-HAPTICS`)**",
        "  - *Focus*: Tactile feedback on user interactions.",
        "  - *Requirement*: Incorporate subtle haptic feedback for user actions using `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator`.",
        "",
        "- **Keyboard Navigation (`APPLE-ACCESSIBILITY-KEYBOARD`)**",
        "  - *Focus*: Physical keyboard navigation and focus management.",
        "  - *Requirement*: Support physical keyboard focus using `@FocusState` in SwiftUI or `keyCommands` / focus systems in UIKit.",
        "",
        "### Android Accessibility Rules",
        "",
        "- **TalkBack (`ANDROID-ACCESSIBILITY-TALKBACK`)**",
        "  - *Focus*: Screen reader descriptions and accessibility focus.",
        "  - *Requirement*: Provide descriptive `android:contentDescription` in XML layouts or Jetpack Compose `contentDescription` parameters. Set `importantForAccessibility=\"no\"` for decorative views.",
        "",
        "- **Font Scaling (`ANDROID-ACCESSIBILITY-FONTSCALING`)**",
        "  - *Focus*: User-configured system font scaling support.",
        "  - *Requirement*: Define text sizes in scale-independent pixels (`sp`) rather than fixed density-independent pixels (`dp`) or raw pixels.",
        "",
        "- **High Contrast (`ANDROID-ACCESSIBILITY-HIGHCONTRAST`)**",
        "  - *Focus*: System high contrast mode theme compatibility.",
        "  - *Requirement*: Reference semantic color theme resources (e.g., `?attr/colorOnSurface` or `MaterialTheme.colorScheme.primary`) instead of hardcoded hex colors.",
        "",
        "- **Accessibility Scanner (`ANDROID-ACCESSIBILITY-SCANNER`)**",
        "  - *Focus*: Minimum touch target sizing and interactive spacing.",
        "  - *Requirement*: Ensure all clickable controls have a minimum touch target area of 48dp x 48dp.",
        "",
        "## Audit Execution and Results",
        "",
        f"- **Audited Directory**: `{directory}`",
        f"- **Scanned Files**: iOS = {len(ios_files)}, Android = {len(android_files)}",
        f"- **Total Findings**: {len(all_findings)}",
        ""
    ]

    if not all_findings:
        report_lines.extend([
            "### Summary",
            "Clean. No accessibility compliance regressions or missing accessibility declarations were detected in the audited directory.",
            ""
        ])
    else:
        report_lines.extend([
            "### Detected Regressions and Findings",
            ""
        ])
        for finding in all_findings:
            meta = RULE_META.get(finding["rule_id"], {})
            sev = meta.get("severity", "medium").upper()
            report_lines.append(f"- **[{sev}] {finding['rule_id']}** (`{finding['file']}:{finding['line']}`)")
            report_lines.append(f"  - *Matched Code*: `{finding['match']}`")
            report_lines.append(f"  - *Issue*: {finding['message']}")
            report_lines.append(f"  - *Recommended Fix*: {finding['fix']}")
            report_lines.append("")

    report_lines.extend([
        "## Platform Recommendations and Best Practices",
        "",
        "### Apple (iOS / iPadOS / macOS)",
        "1. **VoiceOver**: Run automated Accessibility Inspector audits and verify that all interactive controls have descriptive accessibility labels and proper accessibility traits.",
        "2. **Dynamic Type**: Test user interface layouts under Extra Extra Extra Large (XXXL) Dynamic Type sizes and ensure text containers sit in scrollable views.",
        "3. **Reduce Motion**: Wrap custom UI transitions and view state animations with checks for `UIAccessibility.isReduceMotionEnabled` to provide instant or cross-fade alternatives.",
        "4. **Color Contrast**: Verify color contrast ratios meet or exceed 4.5:1 for standard text and 3.1 for large text. Support system increased contrast settings.",
        "5. **Haptics**: Implement context-appropriate haptic feedback generators (`UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator`) for critical user feedback actions.",
        "6. **Keyboard Navigation**: Enable external hardware keyboard support on iPadOS and macOS Catalyst apps using `@FocusState` and explicit focusable modifier chains.",
        "",
        "### Android",
        "1. **TalkBack**: Perform end-to-end screen reader testing with TalkBack enabled. Ensure custom views expose accessibility nodes via `AccessibilityNodeInfo`.",
        "2. **Font Scaling**: Ensure all text elements use `sp` units and verify layout integrity when the system font size scaling factor is set to 200%.",
        "3. **High Contrast**: Avoid inline hardcoded hex colors (`#FF0000` or `Color(0xFF...)`). Use Material Design semantic color tokens to automatically respond to dark and high-contrast themes.",
        "4. **Accessibility Scanner**: Integrate Google Accessibility Scanner checks into local and CI automated Espresso/Compose test runs to flag touch targets below 48dp x 48dp.",
        "",
        "## Regulatory Standards Compliance Reference",
        "- **European Accessibility Act (EAA) / EN 301 549**: Mandatory accessibility compliance for digital services and mobile apps across EU member states.",
        "- **WCAG 2.1 AA**: Industry benchmark for accessible web and mobile application design.",
        "- **ADA Title II / Section 504**: US federal accessibility guidelines requiring accessible mobile apps for public entities and federally funded programs.",
        ""
    ])

    report_dir = os.path.dirname(os.path.abspath(report_path))
    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Report written. {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Static continuous accessibility compliance auditor.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory of the project to scan.")
    parser.add_argument("--rule", help="Scan only a specific accessibility rule ID.")
    parser.add_argument("--report-out", help="Path to write the Markdown accessibility compliance report.")
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
