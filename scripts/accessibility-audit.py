#!/usr/bin/env python3
"""
Accessibility Compliance Audit Tool.
Performs static analysis on Apple (iOS) and Android codebases to identify accessibility regressions
and recommend improvements, covering VoiceOver, Dynamic Type, Reduce Motion, Color Contrast, Haptics,
Keyboard navigation, TalkBack, Font scaling, High contrast, and Accessibility Scanner guidelines.
"""

import os
import sys
import re
import argparse

# Avoid any emojis, emoticons, or graphical symbols in code, comments, or output!

EXCLUDE_DIRS = [
    "node_modules", "Pods", ".git", "build", "DerivedData",
    "vendor", ".dart_tool", "Carthage", "androidTest", "__tests__"
]

def get_files(root_dir, extensions):
    matched_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.endswith("Tests") and not d.endswith("Tests.xctest")]
        for f in files:
            if any(f.endswith(ext) for ext in extensions):
                matched_files.append(os.path.join(root, f))
    return matched_files

def check_apple_voiceover(path):
    files = get_files(path, [".swift", ".m", ".h", ".storyboard", ".xib"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()

                if f.endswith(".storyboard") or f.endswith(".xib"):
                    if ("<button" in content or "<imageView" in content) and "accessibility" not in content.lower():
                        issues.append({
                            "file": f,
                            "line": 1,
                            "code": "<button> or <imageView> found but no accessibility definitions in the file",
                            "severity": "high",
                            "fix": "Enable accessibility in the Storyboard/XIB or add accessibility labels/traits."
                        })
                else:
                    has_ui_elements = False
                    has_accessibility = False
                    for i, line in enumerate(lines, 1):
                        if any(elem in line for elem in ["UIButton", "Image(", "Button(", "ImageView"]):
                            has_ui_elements = True
                        if any(acc in line.lower() for acc in ["accessibilitylabel", "accessibilityhint", "accessibilitytraits", "isaccessibilityelement", "accessibilityvalue", "accessibilityaddtraits", "accessibilityaction", "accessibilityidentifier"]):
                            has_accessibility = True

                    if has_ui_elements and not has_accessibility:
                        for i, line in enumerate(lines, 1):
                            if any(elem in line for elem in ["UIButton", "Image(", "Button(", "ImageView"]):
                                issues.append({
                                    "file": f,
                                    "line": i,
                                    "code": line.strip(),
                                    "severity": "high",
                                    "fix": "Add accessibilityLabel or accessibilityHint to describe the visual/interactive elements for VoiceOver."
                                })
                                break
        except Exception:
            pass
    return issues

def check_apple_dynamic_type(path):
    files = get_files(path, [".swift", ".m", ".h"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "systemFont(ofSize:" in line or "UIFont(name:" in line or ".font(.system(size:" in line:
                        context_start = max(0, i - 3)
                        context_end = min(len(lines), i + 3)
                        context = "".join(lines[context_start:context_end])
                        if "adjustsFontForContentSizeCategory" not in context and "relativeTo" not in context:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "high",
                                "fix": "Add adjustsFontForContentSizeCategory = true for UIKit fonts or specify relativeTo parameter for .font(.system(size: ...)) in SwiftUI."
                            })
        except Exception:
            pass
    return issues

def check_apple_reduce_motion(path):
    files = get_files(path, [".swift", ".m", ".h"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if any(anim in line for anim in ["UIView.animate", "withAnimation(", "CABasicAnimation", "UIViewPropertyAnimator"]):
                        if "isReduceMotionEnabled" not in content and "accessibilityReduceMotion" not in content:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "medium",
                                "fix": "Check UIAccessibility.isReduceMotionEnabled or query @Environment(\\.accessibilityReduceMotion) to bypass/simplify animations when Reduce Motion is enabled."
                            })
        except Exception:
            pass
    return issues

def check_apple_color_contrast(path):
    files = get_files(path, [".swift", ".m", ".h"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if any(col in line for col in ["UIColor(red:", "Color(red:"]):
                        if "isDarkerSystemColorsEnabled" not in content and "darkerSystemColorsStatus" not in content and "UIColor.label" not in content and "Color.primary" not in content:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "medium",
                                "fix": "Use semantic colors or check UIAccessibility.isDarkerSystemColorsEnabled to provide a compliant color contrast ratio (at least 4.5:1)."
                            })
        except Exception:
            pass
    return issues

def check_apple_haptics(path):
    files = get_files(path, [".swift", ".m", ".h"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "addTarget" in line or "onTapGesture" in line:
                        if "UIFeedbackGenerator" not in content and "UINotificationFeedbackGenerator" not in content and "UIImpactFeedbackGenerator" not in content and "sensoryFeedback" not in content:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "medium",
                                "fix": "Provide haptic feedback on interactive button actions using UIFeedbackGenerator or sensoryFeedback."
                            })
        except Exception:
            pass
    return issues

def check_apple_keyboard(path):
    files = get_files(path, [".swift", ".m", ".h"])
    issues = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "canBecomeFocused" in line:
                        if "keyCommands" not in content and "UIKeyCommand" not in content:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "medium",
                                "fix": "Add standard keyCommands support for iPad or Mac Catalyst keyboard navigation."
                            })
        except Exception:
            pass
    return issues

def check_android_talkback(path):
    issues = []
    xml_files = get_files(path, [".xml"])
    for f in xml_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                tag_patterns = [r"<ImageView\b[^>]*>", r"<ImageButton\b[^>]*>"]
                for pattern in tag_patterns:
                    for match in re.finditer(pattern, content, re.DOTALL):
                        tag_str = match.group(0)
                        if "android:contentDescription" not in tag_str and "android:importantForAccessibility=\"no\"" not in tag_str:
                            line_no = content[:match.start()].count("\n") + 1
                            issues.append({
                                "file": f,
                                "line": line_no,
                                "code": tag_str.splitlines()[0],
                                "severity": "high",
                                "fix": "Add android:contentDescription attribute, or set android:importantForAccessibility=\"no\" if the element is decorative."
                            })
        except Exception:
            pass

    kt_files = get_files(path, [".kt"])
    for f in kt_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "Image(" in line or "Icon(" in line:
                        context_start = max(0, i - 1)
                        context_end = min(len(lines), i + 4)
                        context = "".join(lines[context_start:context_end])
                        if "contentDescription" not in context:
                            issues.append({
                                "file": f,
                                "line": i,
                                "code": line.strip(),
                                "severity": "high",
                                "fix": "Define contentDescription parameter in Jetpack Compose Image or Icon call."
                            })
        except Exception:
            pass
    return issues

def check_android_font_scaling(path):
    issues = []
    xml_files = get_files(path, [".xml"])
    for f in xml_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "android:textSize=" in line:
                        match = re.search(r'android:textSize=["\']([^"\']+)["\']', line)
                        if match:
                            val = match.group(1)
                            if any(val.endswith(unit) for unit in ["dp", "dip", "px"]):
                                issues.append({
                                    "file": f,
                                    "line": i,
                                    "code": line.strip(),
                                    "severity": "high",
                                    "fix": f"Change textSize unit from '{val}' to sp (scale-independent pixel) to support font scaling."
                                })
        except Exception:
            pass

    kt_files = get_files(path, [".kt"])
    for f in kt_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                lines = file_obj.readlines()
                for i, line in enumerate(lines, 1):
                    if "fontSize = " in line and ".dp" in line:
                        issues.append({
                            "file": f,
                            "line": i,
                            "code": line.strip(),
                            "severity": "high",
                            "fix": "Always use sp (e.g. 16.sp) instead of dp for fontSize in Jetpack Compose to allow user text scaling."
                        })
        except Exception:
            pass
    return issues

def check_android_high_contrast(path):
    issues = []
    xml_files = get_files(path, [".xml"])
    for f in xml_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "android:textColor=" in line:
                        match = re.search(r'android:textColor=["\']#([^"\']+)["\']', line)
                        if match:
                            if "isHighTextContrastEnabled" not in content:
                                issues.append({
                                    "file": f,
                                    "line": i,
                                    "code": line.strip(),
                                    "severity": "medium",
                                    "fix": "Avoid hardcoded text colors. Reference theme/semantic attributes like '?attr/colorOnBackground' or check isHighTextContrastEnabled()."
                                })
        except Exception:
            pass
    return issues

def check_android_scanner(path):
    issues = []
    xml_files = get_files(path, [".xml"])
    for f in xml_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                tag_patterns = [r"<Button\b[^>]*>", r"<ImageButton\b[^>]*>", r"<CheckBox\b[^>]*>", r"<RadioButton\b[^>]*>"]
                for pattern in tag_patterns:
                    for match in re.finditer(pattern, content, re.DOTALL):
                        tag_str = match.group(0)
                        w_match = re.search(r'android:layout_width=["\']([^"\']+)["\']', tag_str)
                        h_match = re.search(r'android:layout_height=["\']([^"\']+)["\']', tag_str)
                        has_small_dim = False

                        for dim_match in [w_match, h_match]:
                            if dim_match:
                                val = dim_match.group(1)
                                if val.endswith("dp"):
                                    try:
                                        num_val = int(val.replace("dp", ""))
                                        if num_val < 48:
                                            has_small_dim = True
                                    except ValueError:
                                        pass
                                elif val.endswith("dip"):
                                    try:
                                        num_val = int(val.replace("dip", ""))
                                        if num_val < 48:
                                            has_small_dim = True
                                    except ValueError:
                                        pass

                        if has_small_dim:
                            min_w_match = re.search(r'android:minWidth=["\']([^"\']+)["\']', tag_str)
                            min_h_match = re.search(r'android:minHeight=["\']([^"\']+)["\']', tag_str)
                            is_min_ok = True
                            for min_match in [min_w_match, min_h_match]:
                                if not min_match:
                                    is_min_ok = False
                                else:
                                    min_val = min_match.group(1)
                                    try:
                                        min_num = int(min_val.replace("dp", "").replace("dip", ""))
                                        if min_num < 48:
                                            is_min_ok = False
                                    except ValueError:
                                        is_min_ok = False

                            if not is_min_ok:
                                line_no = content[:match.start()].count("\n") + 1
                                issues.append({
                                    "file": f,
                                    "line": line_no,
                                    "code": tag_str.splitlines()[0],
                                    "severity": "high",
                                    "fix": "Ensure touch target size is at least 48dp by setting android:minWidth=\"48dp\" and android:minHeight=\"48dp\"."
                                })
        except Exception:
            pass

    kt_files = get_files(path, [".kt"])
    for f in kt_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_obj:
                lines = file_obj.readlines()
                for i, line in enumerate(lines, 1):
                    if "clickable" in line and any(f"size({size}.dp" in line for size in range(1, 48)):
                        issues.append({
                            "file": f,
                            "line": i,
                            "code": line.strip(),
                            "severity": "high",
                            "fix": "Set minimum size of clickable elements to at least 48.dp to satisfy Google's touch target standard."
                        })
        except Exception:
            pass
    return issues

MAP_CHECKS = {
    "APPLE-ACCESSIBILITY-VOICEOVER": check_apple_voiceover,
    "APPLE-ACCESSIBILITY-DYNAMIC-TYPE": check_apple_dynamic_type,
    "APPLE-ACCESSIBILITY-REDUCE-MOTION": check_apple_reduce_motion,
    "APPLE-ACCESSIBILITY-COLOR-CONTRAST": check_apple_color_contrast,
    "APPLE-ACCESSIBILITY-HAPTICS": check_apple_haptics,
    "APPLE-ACCESSIBILITY-KEYBOARD": check_apple_keyboard,
    "ANDROID-ACCESSIBILITY-TALKBACK": check_android_talkback,
    "ANDROID-ACCESSIBILITY-FONT-SCALING": check_android_font_scaling,
    "ANDROID-ACCESSIBILITY-HIGH-CONTRAST": check_android_high_contrast,
    "ANDROID-ACCESSIBILITY-SCANNER": check_android_scanner
}

def main():
    parser = argparse.ArgumentParser(description="App Store & Google Play Accessibility Audit Tool")
    parser.add_argument("path", nargs="?", default=".", help="Project root path to scan")
    parser.add_argument("--check", help="Run a specific accessibility pattern check")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed scan logs")
    args = parser.parse_args()

    target_path = args.path
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    all_issues = {}

    if args.check:
        if args.check not in MAP_CHECKS:
            print(f"Error: Unknown accessibility check '{args.check}'.")
            sys.exit(1)
        issues = MAP_CHECKS[args.check](target_path)
        if issues:
            print(f"Accessibility Check FAILED: {args.check}")
            for issue in issues:
                print(f"  File: {issue['file']}:{issue['line']}")
                print(f"    Code: {issue['code']}")
                print(f"    Severity: {issue['severity']}")
                print(f"    Fix: {issue['fix']}")
            sys.exit(2)
        else:
            print(f"Accessibility Check PASSED: {args.check}")
            sys.exit(0)

    # Run all audits
    for name, func in MAP_CHECKS.items():
        issues = func(target_path)
        if issues:
            all_issues[name] = issues

    total_issues = sum(len(issues) for issues in all_issues.values())

    print("=== Accessibility Compliance Audit Report ===")
    print(f"Path: {os.path.abspath(target_path)}")
    print(f"Total issues found: {total_issues}")
    print("")

    if total_issues == 0:
        print("No accessibility regressions found. All checks PASSED.")
        sys.exit(0)

    for check_id, issues in all_issues.items():
        print(f"[{check_id}] - {len(issues)} issues found:")
        for issue in issues:
            print(f"  File: {issue['file']}:{issue['line']}")
            print(f"    Code: {issue['code']}")
            print(f"    Severity: {issue['severity']}")
            print(f"    Fix: {issue['fix']}")
        print("")

    # Exit with 0 since this is a general report, but pre-submission hooks will decide whether to block on critical/high.
    sys.exit(0)

if __name__ == "__main__":
    main()
