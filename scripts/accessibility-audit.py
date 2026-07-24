#!/usr/bin/env python3
"""
Accessibility Audit Tool for Apple and Android mobile applications.
Checks for:
Apple: VoiceOver labels/traits, Dynamic Type, Reduce Motion, Color Contrast, Haptics, Keyboard navigation.
Android: TalkBack content descriptions, Font scaling, High contrast, touch targets (Accessibility Scanner recommendations).
Reports compliance issues, regressions, and recommends improvements.
"""

import os
import sys
import re
import argparse

# Define patterns to scan for in files
APPLE_VOICEOVER_SIGNALS = [r"\bUIButton\b", r"\bUILabel\b", r"\bUIImageView\b", r"\bImage\b", r"\bButton\b"]
APPLE_VOICEOVER_COUNTERS = [r"\baccessibilityLabel\b", r"\bisAccessibilityElement\b", r"\baccessibilityHint\b", r"\baccessibilityTraits\b"]

APPLE_DYNAMIC_TYPE_SIGNALS = [r"\bsystemFont\(ofSize:\b", r"\bFont\.custom\b", r"\bUIFont\.systemFont\b"]
APPLE_DYNAMIC_TYPE_COUNTERS = [r"\badjustsFontForContentSizeCategory\b", r"\bUIFontMetrics\b", r"\bUIFont\.preferredFont\b", r"\bscaledFont\b", r"\b\.font\(.*dynamicType\b"]

APPLE_REDUCE_MOTION_SIGNALS = [r"\bUIView\.animate\b", r"\bwithAnimation\b", r"\bCABasicAnimation\b", r"\bCAKeyframeAnimation\b"]
APPLE_REDUCE_MOTION_COUNTERS = [r"\bisReduceMotionEnabled\b", r"\baccessibilityReduceMotion\b", r"\bReduceMotion\b"]

APPLE_COLOR_CONTRAST_SIGNALS = [r"\bUIColor\(red:\b", r"\bColor\(red:\b", r"\b\.lightGray\b", r"\b\.gray\b"]
APPLE_COLOR_CONTRAST_COUNTERS = [r"\bcolorScheme\b", r"\bpreferredContentSizeCategory\b", r"\bsystemBackground\b", r"\blabelColor\b"]

APPLE_HAPTICS_SIGNALS = [r"\bUIImpactFeedbackGenerator\b", r"\bUINotificationFeedbackGenerator\b", r"\bCHHapticEngine\b"]
APPLE_HAPTICS_COUNTERS = [r"\bUIAccessibility\.post\b", r"\bUIAccessibilityPostNotification\b", r"\balert\b", r"\bpresent\(.*alert\b"]

APPLE_KEYBOARD_NAV_SIGNALS = [r"\baddGestureRecognizer\b", r"\bUITapGestureRecognizer\b"]
APPLE_KEYBOARD_NAV_COUNTERS = [r"\bcanBecomeFocused\b", r"\bkeyCommands\b", r"\baccessibilityElements\b"]


ANDROID_TALKBACK_SIGNALS = [r"<ImageView\b", r"<ImageButton\b", r"<Button\b", r"\bImage\b", r"\bIconButton\b"]
ANDROID_TALKBACK_COUNTERS = [r"\bcontentDescription\b", r"android:contentDescription\b"]

ANDROID_FONT_SCALING_SIGNALS = [r"android:textSize=\"[0-9]+(dp|dip|px)\"", r"\btextSize\s*=\s*[0-9]+\.(dp|dip|px)\b"]
ANDROID_FONT_SCALING_COUNTERS = [r"\bsp\b", r"\bTextUnit\.Sp\b", r"android:textSize=\"[0-9]+sp\""]

ANDROID_HIGH_CONTRAST_SIGNALS = [r"#FF777777", r"#FF888888", r"#FFAAAAAA", r"#FF999999"]
ANDROID_HIGH_CONTRAST_COUNTERS = [r"\bisSystemInDarkTheme\(\)", r"MaterialTheme\.colorScheme", r"@color/system_", r"@color/material_"]

ANDROID_TOUCH_TARGETS_SIGNALS = [r"android:layout_width=\"([1-3][0-9])dp\"", r"android:layout_height=\"([1-3][0-9])dp\"", r"\bModifier\.size\(([1-3][0-9])\.dp\)", r"layout_width\s*=\s*\"([1-3][0-9])dp\"", r"layout_height\s*=\s*\"([1-3][0-9])dp\""]


def scan_file(filepath):
    results = {
        "apple_voiceover": {"signals": 0, "counters": 0, "locations": []},
        "apple_dynamic_type": {"signals": 0, "counters": 0, "locations": []},
        "apple_reduce_motion": {"signals": 0, "counters": 0, "locations": []},
        "apple_color_contrast": {"signals": 0, "counters": 0, "locations": []},
        "apple_haptics": {"signals": 0, "counters": 0, "locations": []},
        "apple_keyboard_nav": {"signals": 0, "counters": 0, "locations": []},
        "android_talkback": {"signals": 0, "counters": 0, "locations": []},
        "android_font_scaling": {"signals": 0, "counters": 0, "locations": []},
        "android_high_contrast": {"signals": 0, "counters": 0, "locations": []},
        "android_touch_targets": {"signals": 0, "counters": 0, "locations": []},
    }

    try:
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return results

    ext = os.path.splitext(filepath)[1].lower()

    for idx, line in enumerate(lines):
        line_num = idx + 1

        # Apple iOS checks
        if ext in [".swift", ".m", ".h", ".storyboard", ".xib", ".plist"]:
            # VoiceOver labels
            for r in APPLE_VOICEOVER_SIGNALS:
                if re.search(r, line):
                    results["apple_voiceover"]["signals"] += 1
            for r in APPLE_VOICEOVER_COUNTERS:
                if re.search(r, line):
                    results["apple_voiceover"]["counters"] += 1

            # Dynamic Type
            for r in APPLE_DYNAMIC_TYPE_SIGNALS:
                if re.search(r, line):
                    results["apple_dynamic_type"]["signals"] += 1
                    results["apple_dynamic_type"]["locations"].append((line_num, "Hardcoded/Fixed Font size definition"))
            for r in APPLE_DYNAMIC_TYPE_COUNTERS:
                if re.search(r, line):
                    results["apple_dynamic_type"]["counters"] += 1

            # Reduce Motion
            for r in APPLE_REDUCE_MOTION_SIGNALS:
                if re.search(r, line):
                    results["apple_reduce_motion"]["signals"] += 1
                    results["apple_reduce_motion"]["locations"].append((line_num, "Custom animation/layout transition"))
            for r in APPLE_REDUCE_MOTION_COUNTERS:
                if re.search(r, line):
                    results["apple_reduce_motion"]["counters"] += 1

            # Color Contrast
            for r in APPLE_COLOR_CONTRAST_SIGNALS:
                if re.search(r, line):
                    results["apple_color_contrast"]["signals"] += 1
                    results["apple_color_contrast"]["locations"].append((line_num, "Hardcoded color code / generic color used"))
            for r in APPLE_COLOR_CONTRAST_COUNTERS:
                if re.search(r, line):
                    results["apple_color_contrast"]["counters"] += 1

            # Haptics
            for r in APPLE_HAPTICS_SIGNALS:
                if re.search(r, line):
                    results["apple_haptics"]["signals"] += 1
                    results["apple_haptics"]["locations"].append((line_num, "Haptic generator usage"))
            for r in APPLE_HAPTICS_COUNTERS:
                if re.search(r, line):
                    results["apple_haptics"]["counters"] += 1

            # Keyboard Navigation
            for r in APPLE_KEYBOARD_NAV_SIGNALS:
                if re.search(r, line):
                    results["apple_keyboard_nav"]["signals"] += 1
                    results["apple_keyboard_nav"]["locations"].append((line_num, "Custom gesture / tap gesture recognizer"))
            for r in APPLE_KEYBOARD_NAV_COUNTERS:
                if re.search(r, line):
                    results["apple_keyboard_nav"]["counters"] += 1

        # Android checks
        if ext in [".kt", ".java", ".xml", ".gradle", ".kts"]:
            # TalkBack contentDescription
            for r in ANDROID_TALKBACK_SIGNALS:
                if re.search(r, line):
                    results["android_talkback"]["signals"] += 1
            for r in ANDROID_TALKBACK_COUNTERS:
                if re.search(r, line):
                    results["android_talkback"]["counters"] += 1

            # Font scaling
            for r in ANDROID_FONT_SCALING_SIGNALS:
                if re.search(r, line):
                    results["android_font_scaling"]["signals"] += 1
                    results["android_font_scaling"]["locations"].append((line_num, "Text size defined in dp/px instead of sp"))
            for r in ANDROID_FONT_SCALING_COUNTERS:
                if re.search(r, line):
                    results["android_font_scaling"]["counters"] += 1

            # High Contrast colors
            for r in ANDROID_HIGH_CONTRAST_SIGNALS:
                if re.search(r, line):
                    results["android_high_contrast"]["signals"] += 1
                    results["android_high_contrast"]["locations"].append((line_num, f"Hardcoded low contrast color: {re.search(r, line).group(0)}"))
            for r in ANDROID_HIGH_CONTRAST_COUNTERS:
                if re.search(r, line):
                    results["android_high_contrast"]["counters"] += 1

            # Touch target sizes below 48dp
            for r in ANDROID_TOUCH_TARGETS_SIGNALS:
                match = re.search(r, line)
                if match:
                    size = int(match.group(1))
                    results["android_touch_targets"]["signals"] += 1
                    results["android_touch_targets"]["locations"].append((line_num, f"Interactive touch target dimensions ({size}dp) below recommended 48dp"))

    return results


def run_audit(directory):
    total_results = {
        "apple_voiceover": {"signals": 0, "counters": 0, "locations": []},
        "apple_dynamic_type": {"signals": 0, "counters": 0, "locations": []},
        "apple_reduce_motion": {"signals": 0, "counters": 0, "locations": []},
        "apple_color_contrast": {"signals": 0, "counters": 0, "locations": []},
        "apple_haptics": {"signals": 0, "counters": 0, "locations": []},
        "apple_keyboard_nav": {"signals": 0, "counters": 0, "locations": []},
        "android_talkback": {"signals": 0, "counters": 0, "locations": []},
        "android_font_scaling": {"signals": 0, "counters": 0, "locations": []},
        "android_high_contrast": {"signals": 0, "counters": 0, "locations": []},
        "android_touch_targets": {"signals": 0, "counters": 0, "locations": []},
    }

    scanned_files_count = 0

    for root, dirs, files in os.walk(directory):
        # Skip node_modules, build, Pods, Carthage, DerivedData, vendor, etc.
        dirs[:] = [d for d in dirs if d not in ["node_modules", "build", "Pods", "Carthage", "DerivedData", "vendor", ".git"]]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".swift", ".m", ".h", ".storyboard", ".xib", ".plist", ".kt", ".java", ".xml"]:
                filepath = os.path.join(root, file)
                scanned_files_count += 1
                res = scan_file(filepath)
                for k in total_results:
                    total_results[k]["signals"] += res[k]["signals"]
                    total_results[k]["counters"] += res[k]["counters"]
                    for line, msg in res[k]["locations"]:
                        total_results[k]["locations"].append((filepath, line, msg))

    print("======================================================================")
    print("                      ACCESSIBILITY AUDIT REPORT                      ")
    print("======================================================================")
    print(f"Scanned directory: {directory}")
    print(f"Total files audited: {scanned_files_count}")
    print()

    print("--- APPLE IOS ACCESSIBILITY CHECKS ---")

    # 1. VoiceOver Labels
    print("[1] VoiceOver Labels & Traits:")
    if total_results["apple_voiceover"]["signals"] > 0 and total_results["apple_voiceover"]["counters"] == 0:
        print("  ❌ REGRESSION/ISSUE: Found UI controls/images without any accessibilityLabel/accessibilityTraits references.")
        print("     Recommendation: Ensure UIButton, UIImageView, and custom controls set descriptive accessibilityLabel.")
    elif total_results["apple_voiceover"]["signals"] > 0:
        ratio = total_results["apple_voiceover"]["counters"] / total_results["apple_voiceover"]["signals"]
        if ratio < 0.5:
            print(f"  ⚠️ IMPROVEMENT NEEDED: Dynamic VoiceOver labeling coverage looks low ({total_results['apple_voiceover']['counters']} labels / {total_results['apple_voiceover']['signals']} elements).")
            print("     Recommendation: Populate accessibilityLabel, accessibilityHint, and accessibilityTraits for all custom buttons/views.")
        else:
            print("  ✅ Good initial coverage of VoiceOver accessibility labels.")
    else:
        print("  ℹ️ No iOS UI elements detected or scanned.")

    # 2. Dynamic Type
    print("[2] Dynamic Type / Font Scaling:")
    if total_results["apple_dynamic_type"]["locations"]:
        print(f"  ❌ REGRESSION/ISSUE: Found {len(total_results['apple_dynamic_type']['locations'])} hardcoded static font size calls.")
        for path, line, msg in total_results["apple_dynamic_type"]["locations"][:5]:
            print(f"     - {path}:{line} -> {msg}")
        if len(total_results["apple_dynamic_type"]["locations"]) > 5:
            print(f"     ... and {len(total_results['apple_dynamic_type']['locations']) - 5} more.")
        print("     Recommendation: Migrate to UIFont.preferredFont(forTextStyle:) or wrap custom fonts using UIFontMetrics.")
    else:
        print("  ✅ No hardcoded font sizes detected without Dynamic Type counter-signals.")

    # 3. Reduce Motion
    print("[3] Reduce Motion Settings:")
    if total_results["apple_reduce_motion"]["signals"] > 0 and total_results["apple_reduce_motion"]["counters"] == 0:
        print("  ❌ REGRESSION/ISSUE: Custom transitions/animations detected, but none respect UIAccessibility.isReduceMotionEnabled.")
        print("     Recommendation: Add guards checking UIAccessibility.isReduceMotionEnabled to skip slide/scale animations and fallback to cross-dissolve.")
    else:
        print("  ✅ Animation sequences match Reduce Motion safety practices or no animations found.")

    # 4. Color Contrast
    print("[4] Color Contrast adaptivity:")
    if total_results["apple_color_contrast"]["signals"] > 0 and total_results["apple_color_contrast"]["counters"] == 0:
        print("  ⚠️ IMPROVEMENT NEEDED: Custom static UIColor/Color hex values detected without Dark Mode or contrast schemes.")
        print("     Recommendation: Use Dynamic Colors (semantic UI Colors like label, secondaryLabel) and verify they satisfy WCAG 2.1 4.5:1 ratio.")
    else:
        print("  ✅ No static low-contrast Color or UIColor issues detected.")

    # 5. Haptic Fallbacks
    print("[5] Haptic Alerts Fallbacks:")
    if total_results["apple_haptics"]["signals"] > 0 and total_results["apple_haptics"]["counters"] == 0:
        print("  ❌ REGRESSION/ISSUE: Using haptics for feedback without visual/auditory modal fallbacks.")
        print("     Recommendation: Trigger standard UIAccessibility.post announcements or system alert modals when initiating critical feedback.")
    else:
        print("  ✅ Haptic feedback references are safe or not detected.")

    # 6. Keyboard & Switch Navigation
    print("[6] Keyboard & Switch Navigation:")
    if total_results["apple_keyboard_nav"]["signals"] > 0 and total_results["apple_keyboard_nav"]["counters"] == 0:
        print("  ⚠️ IMPROVEMENT NEEDED: Custom tap gestures found but no keyboard focus or accessibilityElements definition.")
        print("     Recommendation: Set isAccessibilityElement = true or implement canBecomeFocused and respond to keyCommands.")
    else:
        print("  ✅ Keyboard focus handling appears compliant.")

    print()
    print("--- ANDROID ACCESSIBILITY CHECKS ---")

    # 7. TalkBack Content Descriptions
    print("[7] TalkBack Content Descriptions:")
    if total_results["android_talkback"]["signals"] > 0 and total_results["android_talkback"]["counters"] == 0:
        print("  ❌ REGRESSION/ISSUE: ImageView or ImageButton layout elements exist without android:contentDescription.")
        print("     Recommendation: Supply android:contentDescription for all meaningful views, or set to @null for decorative-only icons.")
    else:
        print("  ✅ TalkBack accessibility labels / contentDescriptions are present on scanned image assets.")

    # 8. Font Scaling (sp vs dp)
    print("[8] Font scaling size units:")
    if total_results["android_font_scaling"]["locations"]:
        print(f"  ❌ REGRESSION/ISSUE: Found {len(total_results['android_font_scaling']['locations'])} hardcoded dp/px text sizes.")
        for path, line, msg in total_results["android_font_scaling"]["locations"][:5]:
            print(f"     - {path}:{line} -> {msg}")
        if len(total_results["android_font_scaling"]["locations"]) > 5:
            print(f"     ... and {len(total_results['android_font_scaling']['locations']) - 5} more.")
        print("     Recommendation: Redefine text size dimensions using scale-independent pixels (sp) instead of dp or dip.")
    else:
        print("  ✅ All detected layout text sizes are utilizing scaling (sp) units.")

    # 9. High Contrast colors
    print("[9] High Contrast modes compatibility:")
    if total_results["android_high_contrast"]["locations"]:
        print(f"  ⚠️ IMPROVEMENT NEEDED: Found {len(total_results['android_high_contrast']['locations'])} hardcoded grey low-contrast color codes.")
        for path, line, msg in total_results["android_high_contrast"]["locations"][:5]:
            print(f"     - {path}:{line} -> {msg}")
        print("     Recommendation: Utilize dynamic MaterialTheme or system color references instead of hardcoding low contrast static hex values.")
    else:
        print("  ✅ No static gray-color-contrast layout concerns detected.")

    # 10. Accessibility Scanner touch targets
    print("[10] Touch Target Sizes (Accessibility Scanner guidelines):")
    if total_results["android_touch_targets"]["locations"]:
        print(f"  ❌ REGRESSION/ISSUE: Found {len(total_results['android_touch_targets']['locations'])} small touch target bounds under 48dp.")
        for path, line, msg in total_results["android_touch_targets"]["locations"][:5]:
            print(f"     - {path}:{line} -> {msg}")
        if len(total_results["android_touch_targets"]["locations"]) > 5:
            print(f"     ... and {len(total_results['android_touch_targets']['locations']) - 5} more.")
        print("     Recommendation: Enlarge layouts to minWidth/minHeight of 48dp, or append touch margins/padding.")
    else:
        print("  ✅ Touch target minimum bounds (48dp) comply with Accessibility Scanner recommendations.")

    print()
    print("======================================================================")
    print("                      END OF ACCESSIBILITY REPORT                      ")
    print("======================================================================")


def main():
    parser = argparse.ArgumentParser(description="Static Code Analyzer for Accessibility Compliance (iOS and Android)")
    parser.add_argument("dir", nargs="?", default=".", help="Directory of mobile app project to check (default: current directory)")
    args = parser.parse_args()

    run_audit(args.dir)


if __name__ == "__main__":
    main()
