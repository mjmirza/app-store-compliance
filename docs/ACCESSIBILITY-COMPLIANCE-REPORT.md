# Accessibility Compliance Report (2026)

## Executive Summary

This report presents a comprehensive evaluation of accessibility compliance across Apple (iOS/iPadOS/macOS) and Android platforms. To ensure compliance with global accessibility regulations—including Directive (EU) 2019/882 (European Accessibility Act) and EN 301 549 standards—applications must support core accessibility features and pass automated and manual accessibility audits.

Continuous static auditing is implemented via `scripts/accessibility-audit.py` and validated by `scripts/accessibility-audit-test.sh`.

---

## Apple Accessibility Requirements

### 1. VoiceOver
- **Requirement:** Every interactive component, custom view, and informative image must expose descriptive labels, traits, and hints. Decorative graphics must be explicitly hidden or marked as decorative to avoid cluttering screen reader navigation.
- **Rule ID:** `APPLE-ACCESSIBILITY-VOICEOVER`
- **SwiftUI Guidance:** Use `Image(decorative: ...)` for visual elements or add `.accessibilityLabel(...)`, `.accessibilityHint(...)`, and `.accessibilityAddTraits(...)`.
- **UIKit Guidance:** Set `isAccessibilityElement = true`, `accessibilityLabel`, and `accessibilityTraits` for custom controls. Exclude decorative images by setting `isAccessibilityElement = false`.

### 2. Dynamic Type
- **Requirement:** Text elements must respond seamlessly to user font size preferences and Large Text accessibility settings without truncating, overlapping, or breaking layout structures.
- **Rule ID:** `APPLE-ACCESSIBILITY-DYNAMICTYPE`
- **SwiftUI Guidance:** Use semantic text styles such as `.font(.body)` or `.font(.title)`. Avoid fixed point sizes (`.font(.system(size: 16))`) unless wrapped in scalable dynamic metrics.
- **UIKit Guidance:** Use `UIFont.preferredFont(forTextStyle:)` and set `adjustsFontForContentSizeCategory = true` on labels and text fields.

### 3. Reduce Motion
- **Requirement:** Applications must respect the user's system-level Reduce Motion setting (`UIAccessibility.isReduceMotionEnabled` or `@Environment(\.accessibilityReduceMotion)`). Custom animations, screen transitions, and parallax effects must be disabled or converted to subtle fades.
- **Rule ID:** `APPLE-ACCESSIBILITY-REDUCEMOTION`
- **SwiftUI Guidance:** Check `accessibilityReduceMotion` before invoking `withAnimation` or applying transition modifiers.
- **UIKit Guidance:** Query `UIAccessibility.isReduceMotionEnabled` before running `UIView.animate` or complex keyframe animations.

### 4. Color Contrast
- **Requirement:** Text and essential visual UI elements must satisfy minimum WCAG 2.1 AA color contrast ratios (4.5:1 for standard text, 3:1 for large text). Applications must support Dark Mode dynamically and adapt when Differentiate Without Color or Increase Contrast options are active.
- **Rule ID:** `APPLE-ACCESSIBILITY-COLORCONTRAST`
- **SwiftUI Guidance:** Use dynamic asset catalog colors or standard semantic colors (`Color.primary`, `Color(UIColor.systemBackground)`).
- **UIKit Guidance:** Use dynamic `UIColor` initializers (`UIColor { traitCollection in ... }`) and monitor `UIAccessibility.isDarkerSystemColorsEnabled`.

### 5. Haptics
- **Requirement:** Physical feedback provided through haptic engines must complement visual and auditory feedback on interactive controls (buttons, switches, refresh gestures), enhancing accessibility for visual or auditory impaired users.
- **Rule ID:** `APPLE-ACCESSIBILITY-HAPTICS`
- **Implementation Guidance:** Use `UIImpactFeedbackGenerator`, `UISelectionFeedbackGenerator`, or CoreHaptics (`CHHapticEngine`) on key user interactions.

### 6. Keyboard Navigation
- **Requirement:** Applications running on iPadOS/macOS or used with hardware keyboards must support full keyboard focus, predictable tab ordering, and explicit focus visual indicators.
- **Rule ID:** `APPLE-ACCESSIBILITY-KEYBOARD`
- **SwiftUI Guidance:** Leverage `.focusable()` and `@FocusState` to manage and programmatically change input focus.
- **UIKit Guidance:** Override `keyCommands` on responder classes to handle physical key events and custom shortcuts.

---

## Android Accessibility Requirements

### 1. TalkBack
- **Requirement:** Screen reader accessibility requires all interactive elements and informative graphic components to specify clean, localized `contentDescription` attributes.
- **Rule ID:** `ANDROID-ACCESSIBILITY-TALKBACK`
- **XML Layout Guidance:** Define `android:contentDescription="@string/..."` for `ImageView` and `ImageButton`. Set `android:importantForAccessibility="no"` for purely decorative elements.
- **Jetpack Compose Guidance:** Supply `contentDescription` parameter in `Image`, `Icon`, and `IconButton` composables, or pass `null` for decorative visuals.

### 2. Font Scaling
- **Requirement:** Layouts must accommodate user-selected text magnification up to 200% without text clipping, overlap, or line truncations.
- **Rule ID:** `ANDROID-ACCESSIBILITY-FONTSCALING`
- **XML Layout Guidance:** Always specify `android:textSize` using scale-independent pixels (`sp`) rather than density-independent pixels (`dp`).
- **Jetpack Compose Guidance:** Always specify font sizes using `.sp` units (e.g. `16.sp`).

### 3. High Contrast
- **Requirement:** Text and UI elements must adapt to high contrast theme settings and system dark mode without hardcoding fixed color hex values that ignore contrast themes.
- **Rule ID:** `ANDROID-ACCESSIBILITY-HIGHCONTRAST`
- **XML Layout Guidance:** Use semantic theme attributes (e.g. `android:textColor="?attr/colorOnSurface"`) instead of hardcoded hex values (e.g. `#000000`).
- **Jetpack Compose Guidance:** Reference colors from `MaterialTheme.colorScheme` (e.g. `MaterialTheme.colorScheme.primary`).

### 4. Accessibility Scanner Recommendations
- **Requirement:** Interactive elements must meet minimum touch target dimensions of 48dp x 48dp to ensure usability for users with motor impairments.
- **Rule ID:** `ANDROID-ACCESSIBILITY-SCANNER`
- **XML Layout Guidance:** Ensure interactive components have `android:minWidth="48dp"` and `android:minHeight="48dp"`, or add surrounding layout padding.
- **Jetpack Compose Guidance:** Use `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)` or standard button composables with default padding.

---

## Audit & Verification Matrix

| Rule ID | Domain | Platform | Target Standards | Severity |
| --- | --- | --- | --- | --- |
| `APPLE-ACCESSIBILITY-VOICEOVER` | VoiceOver | Apple | WCAG 2.1 AA / EN 301 549 | Medium |
| `APPLE-ACCESSIBILITY-DYNAMICTYPE` | Dynamic Type | Apple | WCAG 2.1 AA / EN 301 549 | Medium |
| `APPLE-ACCESSIBILITY-REDUCEMOTION` | Reduce Motion | Apple | Apple Human Interface Guidelines | Medium |
| `APPLE-ACCESSIBILITY-COLORCONTRAST` | Color Contrast | Apple | WCAG 2.1 AA / EN 301 549 | Medium |
| `APPLE-ACCESSIBILITY-HAPTICS` | Haptics | Apple | Apple Human Interface Guidelines | Medium |
| `APPLE-ACCESSIBILITY-KEYBOARD` | Keyboard Navigation | Apple | WCAG 2.1 AA / EN 301 549 | Medium |
| `ANDROID-ACCESSIBILITY-TALKBACK` | TalkBack | Android | WCAG 2.1 AA / EN 301 549 | Medium |
| `ANDROID-ACCESSIBILITY-FONTSCALING` | Font Scaling | Android | Google Accessibility Guidelines | Medium |
| `ANDROID-ACCESSIBILITY-HIGHCONTRAST` | High Contrast | Android | WCAG 2.1 AA / EN 301 549 | Medium |
| `ANDROID-ACCESSIBILITY-SCANNER` | Touch Target Size | Android | Google Accessibility Scanner | Medium |

---

## Automated Verification & Regression Prevention

Automated regression detection is enforced via continuous integration:
1. `scripts/accessibility-audit.py`: Scans iOS (`.swift`, `.m`, `.h`) and Android (`.kt`, `.java`, `.xml`) files against all 10 accessibility rule definitions.
2. `scripts/accessibility-audit-test.sh`: Runs unit tests against mock compliant and non-compliant code fixtures to ensure rule accuracy.
3. `scripts/release-audit.py`: Incorporates accessibility compliance as part of pre-release audit gates.

### Remediation Workflow for Regressions
When `scripts/accessibility-audit.py` reports findings:
1. Locate the file and line number indicated in the audit output.
2. Review the recommended fix for the specific rule ID.
3. Update source code following platform-specific dynamic scaling, accessibility labeling, or layout sizing guidelines.
4. Re-run `python3 scripts/accessibility-audit.py` to confirm resolution.
