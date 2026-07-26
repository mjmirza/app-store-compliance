#!/usr/bin/env python3
"""
Accessibility compliance auditor for iOS and Android mobile app projects.

Performs static analysis of iOS (Swift, Objective-C, plist) and Android
(Kotlin, Java, XML) source files for accessibility compliance.
Reports regressions, highlights potential policy risks, and recommends fixes.

Usage:
    accessibility-audit.py <project-dir>
    accessibility-audit.py .

Exit codes: 0 clean, 2 if any critical accessibility regression is found.
"""
import os
import sys
import re

# Severity mapping for summary counts
ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

# Exclusion patterns for scanning
EXCLUDE_DIRS = {
    "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
    ".dart_tool", "Carthage", "androidTest", "__tests__"
}

# Regex definitions for non-XML scans (Apple platform & general files)
REGEX_RULES = {
    # --- APPLE PLATFORM ---
    "ACC-APPLE-VOICEOVER-EMPTY-LABEL": {
        "platform": "apple",
        "category": "VoiceOver",
        "severity": "critical",
        "pattern": re.compile(r'\.accessibilityLabel\(\s*""\s*\)|\.accessibilityLabel\(\s*nil\s*\)|accessibilityLabel\s*=\s*""|accessibilityLabel\s*=\s*nil', re.IGNORECASE),
        "message": "Empty or nil accessibility label found in iOS code.",
        "fix": "Provide a descriptive, non-empty, localized string for the accessibility label so screen readers can describe the element."
    },
    "ACC-APPLE-VOICEOVER-EMPTY-HINT": {
        "platform": "apple",
        "category": "VoiceOver",
        "severity": "medium",
        "pattern": re.compile(r'\.accessibilityHint\(\s*""\s*\)|accessibilityHint\s*=\s*""', re.IGNORECASE),
        "message": "Empty accessibility hint found in iOS code.",
        "fix": "Remove the empty hint modifier or populate it with brief directions on what happens when the element is activated."
    },
    "ACC-APPLE-DYNAMIC-TYPE-SYSTEM-FONT": {
        "platform": "apple",
        "category": "Dynamic Type",
        "severity": "high",
        "pattern": re.compile(r'\.font\(\s*\.system\(\s*size:\s*\d+|Font\.system\(\s*size:\s*\d+|UIFont\.(systemFont|boldSystemFont|italicSystemFont)\(\s*ofSize:', re.IGNORECASE),
        "message": "Hardcoded system font size used without dynamic scaling.",
        "fix": "Use SwiftUI's .font(.body) or relativeTo: text styles, or use UIFontMetrics in UIKit to ensure fonts scale with system settings."
    },
    "ACC-APPLE-DYNAMIC-TYPE-FIXED-LINE-LIMIT": {
        "platform": "apple",
        "category": "Dynamic Type",
        "severity": "medium",
        "pattern": re.compile(r'\.lineLimit\(\s*[12]\s*\)|numberOfLines\s*=\s*[12]', re.IGNORECASE),
        "message": "Fixed line limit (1 or 2) detected on text element, which may clip text when scaled.",
        "fix": "Ensure labels can wrap to accommodate scaled text, or verify that clipping does not occur at maximum dynamic sizes."
    },
    "ACC-APPLE-REDUCE-MOTION-MISSING-CHECK": {
        "platform": "apple",
        "category": "Reduce Motion",
        "severity": "medium",
        "pattern": re.compile(r'\.repeatForever|CABasicAnimation|CAKeyframeAnimation|UIView\.animate', re.IGNORECASE),
        "message": "Animation or infinite transition detected without a Reduce Motion check.",
        "fix": "Verify if UIAccessibility.isReduceMotionEnabled is checked before triggering intense animations, or use a custom modifier to respect motion preferences."
    },
    "ACC-APPLE-CONTRAST-HARDCODED-HEX": {
        "platform": "apple",
        "category": "Color Contrast",
        "severity": "medium",
        "pattern": re.compile(r'Color\(hex:|UIColor\(hex:', re.IGNORECASE),
        "message": "Hardcoded custom hexadecimal color used without a semantic provider.",
        "fix": "Use semantic/system colors (e.g. Color(.label), UIColor.label) or asset catalog dynamic colors to ensure proper contrast in light, dark, and high-contrast modes."
    },
    "ACC-APPLE-HAPTICS-GESTURE-WITHOUT-FEEDBACK": {
        "platform": "apple",
        "category": "Haptics",
        "severity": "low",
        "pattern": re.compile(r'\.onTapGesture|UITapGestureRecognizer', re.IGNORECASE),
        "message": "Gesture recognizer or custom tap gesture without haptic feedback generator.",
        "fix": "Consider triggering UIImpactFeedbackGenerator or UINotificationFeedbackGenerator on custom interactive elements to provide tactile feedback."
    },
    "ACC-APPLE-KEYBOARD-NAV": {
        "platform": "apple",
        "category": "Keyboard navigation",
        "severity": "low",
        "pattern": re.compile(r'canBecomeFocused|keyCommands|UIKeyCommand|@FocusState|\.focusable\(', re.IGNORECASE),
        "message": "Keyboard focus or navigation control found (Verify implementation).",
        "fix": "Ensure custom interactive elements are fully focusable and reachable using a hardware keyboard or VoiceOver navigation swipe gestures."
    }
}


def scan_xml_tags(filepath, content, lines, findings):
    """Parses Android layout XML elements, supporting multi-line tags securely."""
    # Matches <TagName ... > including nested/multiline bodies
    tag_pattern = re.compile(r'<([a-zA-Z0-9_.]+)([^>]*)>', re.DOTALL)
    for m in tag_pattern.finditer(content):
        tag_name = m.group(1)
        tag_body = m.group(2)

        # Calculate line number of the tag start
        char_idx = m.start()
        line_no = content[:char_idx].count("\n") + 1
        matched_line = lines[line_no - 1].strip()

        # Determine properties of the tag
        is_image_or_button = tag_name in {"ImageView", "ImageButton", "Button", "Image"}
        is_clickable = "android:clickable=\"true\"" in tag_body

        # 1. TalkBack: contentDescription validation
        if is_image_or_button or is_clickable:
            desc_match = re.search(r'android:contentDescription\s*=\s*"([^"]*)"', tag_body)
            if desc_match:
                desc_val = desc_match.group(1)
                if desc_val == "" or desc_val == "@null":
                    findings.append({
                        "id": "ACC-AND-TALKBACK-EMPTY-DESC",
                        "filepath": filepath,
                        "line": line_no,
                        "matched_text": matched_line,
                        "platform": "google",
                        "category": "TalkBack",
                        "severity": "critical",
                        "message": "Empty or null contentDescription found on interactive/image element.",
                        "fix": "Add a descriptive, non-empty, localized string to the contentDescription attribute so TalkBack can read it to visually-impaired users."
                    })
            elif tag_name in {"ImageView", "ImageButton"}:
                findings.append({
                    "id": "ACC-AND-TALKBACK-EMPTY-DESC",
                    "filepath": filepath,
                    "line": line_no,
                    "matched_text": matched_line,
                    "platform": "google",
                    "category": "TalkBack",
                    "severity": "critical",
                    "message": "Missing contentDescription on ImageView/ImageButton.",
                    "fix": "Add a descriptive contentDescription to describe this visual element to screen readers."
                })

        # 2. Font scaling: Hardcoded textSize inside TextView
        if "TextView" in tag_name or is_image_or_button:
            # Check textSize units
            size_match = re.search(r'android:textSize\s*=\s*"([^"]*)"', tag_body)
            if size_match:
                size_val = size_match.group(1)
                if any(unit in size_val for unit in {"dp", "dip", "px"}):
                    findings.append({
                        "id": "ACC-AND-FONTSCALING-DP",
                        "filepath": filepath,
                        "line": line_no,
                        "matched_text": matched_line,
                        "platform": "google",
                        "category": "Font scaling",
                        "severity": "critical",
                        "message": "Hardcoded font size using dp, dip, or px instead of sp: " + size_val,
                        "fix": "Change text size unit to 'sp' (scale-independent pixels) so that system font scaling preferences are honored."
                    })

            # Check for container height constraint on a text container
            height_match = re.search(r'android:layout_height\s*=\s*"([^"]*)"', tag_body)
            if height_match:
                height_val = height_match.group(1)
                if any(unit in height_val for unit in {"dp", "dip", "px"}) and height_val not in {"wrap_content", "match_parent"}:
                    findings.append({
                        "id": "ACC-AND-FONTSCALING-CONTAINER-HEIGHT",
                        "filepath": filepath,
                        "line": line_no,
                        "matched_text": matched_line,
                        "platform": "google",
                        "category": "Font scaling",
                        "severity": "medium",
                        "message": "Fixed-height TextView container detected: " + height_val,
                        "fix": "Use wrap_content or minHeight instead of fixed layouts to prevent text clipping when users enlarge the system font size."
                    })

        # 3. High contrast: hardcoded colors in XML elements
        color_match = re.search(r'(android:textColor|android:background)\s*=\s*"([^"]*)"', tag_body)
        if color_match:
            color_val = color_match.group(2)
            if color_val.startswith("#"):
                findings.append({
                    "id": "ACC-AND-HIGH-CONTRAST-HARDCODED",
                    "filepath": filepath,
                    "line": line_no,
                    "matched_text": matched_line,
                    "platform": "google",
                    "category": "High contrast",
                    "severity": "medium",
                    "message": "Hardcoded color literal used instead of dynamic theme reference: " + color_val,
                    "fix": "Use semantic theme attributes (e.g. ?attr/colorOnSurface, MaterialTheme.colorScheme.onSurface) to adapt automatically to high-contrast or dark-mode settings."
                })

        # 4. Accessibility Scanner: small touch targets on interactive components
        if tag_name in {"Button", "ImageButton"} or is_clickable:
            width_match = re.search(r'android:layout_width\s*=\s*"([^"]*)"', tag_body)
            height_match = re.search(r'android:layout_height\s*=\s*"([^"]*)"', tag_body)

            under_48 = False
            found_dim = ""
            for match in (width_match, height_match):
                if match:
                    dim_val = match.group(1)
                    # Extract numeric digits
                    num_match = re.match(r'^([0-9.]+)', dim_val)
                    if num_match:
                        val = float(num_match.group(1))
                        if ("dp" in dim_val or "dip" in dim_val) and val < 48:
                            under_48 = True
                            found_dim = dim_val
                            break
            if under_48:
                findings.append({
                    "id": "ACC-AND-SCANNER-SMALL-TARGET",
                    "filepath": filepath,
                    "line": line_no,
                    "matched_text": matched_line,
                    "platform": "google",
                    "category": "Accessibility Scanner recommendations",
                    "severity": "high",
                    "message": "Clickable control or button has a dimension under 48dp: " + found_dim,
                    "fix": "Enlarge touch targets to a minimum of 48dp by 48dp to accommodate users with motor skill difficulties."
                })


def scan_file(filepath, findings):
    """Scans a single file against the defined rules."""
    ext = os.path.splitext(filepath)[1].lower()

    # Determine which platform rules apply
    is_apple_file = ext in {".swift", ".m", ".h", ".storyboard", ".xib", ".plist"}
    is_android_file = ext in {".kt", ".java", ".xml"}
    is_hybrid_file = ext in {".js", ".ts", ".jsx", ".tsx", ".dart"}

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return

    content = "".join(lines)

    # Use tag-based scanner for Android XML files to correctly parse multi-line tags
    if ext == ".xml":
        scan_xml_tags(filepath, content, lines, findings)
        return

    # Check non-XML rules (Swift, Kotlin/Java, Compose, Hybrid)
    for rule_id, rule in REGEX_RULES.items():
        if rule["platform"] == "apple" and not (is_apple_file or is_hybrid_file):
            continue
        if rule["platform"] == "google" and not (is_android_file or is_hybrid_file):
            continue

        matches = list(rule["pattern"].finditer(content))
        if matches:
            for m in matches:
                char_idx = m.start()
                line_no = content[:char_idx].count("\n") + 1
                matched_line = lines[line_no - 1].strip()

                findings.append({
                    "id": rule_id,
                    "filepath": filepath,
                    "line": line_no,
                    "matched_text": matched_line,
                    "platform": rule["platform"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "fix": rule["fix"]
                })

    # Extra Compose & Hybrid checks for Android
    if is_android_file or is_hybrid_file:
        # TalkBack Compose Empty Description Check
        desc_pattern = re.compile(r'contentDescription\s*=\s*""|contentDescription\s*=\s*null', re.IGNORECASE)
        for m in desc_pattern.finditer(content):
            char_idx = m.start()
            line_no = content[:char_idx].count("\n") + 1
            findings.append({
                "id": "ACC-AND-TALKBACK-EMPTY-DESC",
                "filepath": filepath,
                "line": line_no,
                "matched_text": lines[line_no - 1].strip(),
                "platform": "google",
                "category": "TalkBack",
                "severity": "critical",
                "message": "Empty or null contentDescription found in Compose code.",
                "fix": "Add a descriptive, non-empty, localized string to the contentDescription attribute so TalkBack can read it."
            })

        # High Contrast Compose Hardcoded Check
        color_pattern = re.compile(r'Color\(\s*0xFF[0-9a-fA-F]+\s*\)', re.IGNORECASE)
        for m in color_pattern.finditer(content):
            char_idx = m.start()
            line_no = content[:char_idx].count("\n") + 1
            findings.append({
                "id": "ACC-AND-HIGH-CONTRAST-HARDCODED",
                "filepath": filepath,
                "line": line_no,
                "matched_text": lines[line_no - 1].strip(),
                "platform": "google",
                "category": "High contrast",
                "severity": "medium",
                "message": "Hardcoded Color literal used in Compose layout.",
                "fix": "Use MaterialTheme.colorScheme dynamic colors to support system-wide high-contrast themes."
            })


def run_audit(project_dir):
    """Recursively audits files under project_dir."""
    findings = []

    for root, dirs, files in os.walk(project_dir):
        # Prune excluded directories in place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            filepath = os.path.join(root, file)
            scan_file(filepath, findings)

    return findings


def print_report(findings, project_dir):
    """Prints a clear report grouped by category without any emojis or graphical symbols."""
    grouped = {"apple": {}, "google": {}}

    for f in findings:
        plat = f["platform"]
        cat = f["category"]
        if cat not in grouped[plat]:
            grouped[plat][cat] = []
        grouped[plat][cat].append(f)

    print("== Accessibility Compliance Report ==")
    print("Project Directory: " + str(project_dir))
    print("")

    # 1. Apple Platform Report
    print("--- APPLE PLATFORM ACCESSIBILITY ---")
    apple_cats = ["VoiceOver", "Dynamic Type", "Reduce Motion", "Color Contrast", "Haptics", "Keyboard navigation"]
    for cat in apple_cats:
        print("Category: " + cat)
        items = grouped["apple"].get(cat, [])
        if not items:
            print("  Status: No regressions detected.")
        else:
            for item in items:
                rel_path = os.path.relpath(item["filepath"], project_dir)
                print("  [" + item["severity"].upper() + "] " + item["id"])
                print("    File: " + rel_path + " (Line " + str(item["line"]) + ")")
                print("    Issue: " + item["message"])
                print("    Code: " + item["matched_text"][:80])
                print("    Recommendation: " + item["fix"])
        print("")

    # 2. Android Platform Report
    print("--- ANDROID PLATFORM ACCESSIBILITY ---")
    android_cats = ["TalkBack", "Font scaling", "High contrast", "Accessibility Scanner recommendations"]
    for cat in android_cats:
        print("Category: " + cat)
        items = grouped["google"].get(cat, [])
        if not items:
            print("  Status: No regressions detected.")
        else:
            for item in items:
                rel_path = os.path.relpath(item["filepath"], project_dir)
                print("  [" + item["severity"].upper() + "] " + item["id"])
                print("    File: " + rel_path + " (Line " + str(item["line"]) + ")")
                print("    Issue: " + item["message"])
                print("    Code: " + item["matched_text"][:80])
                print("    Recommendation: " + item["fix"])
        print("")

    # Summary Counts
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    print("--- SUMMARY ---")
    print("Critical Issues: " + str(severity_counts["critical"]))
    print("High Issues: " + str(severity_counts["high"]))
    print("Medium Issues: " + str(severity_counts["medium"]))
    print("Low Issues: " + str(severity_counts["low"]))
    print("")

    return severity_counts


def main():
    if len(sys.argv) > 1:
        project_dir = sys.argv[1]
    else:
        project_dir = "."

    if not os.path.isdir(project_dir):
        print("Error: Target directory " + str(project_dir) + " does not exist.")
        return 1

    findings = run_audit(project_dir)
    findings.sort(key=lambda f: (ORDER.get(f["severity"], 9), f["id"], f["filepath"], f["line"]))

    counts = print_report(findings, project_dir)

    if counts["critical"] > 0:
        print("Result: BLOCKED. Critical accessibility regressions found.")
        return 2
    else:
        print("Result: PASS. No critical accessibility regressions found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
