# Accessibility Compliance Report (2026)

This document provides a comprehensive continuous accessibility compliance evaluation across Apple iOS/iPadOS/macOS and Android platforms in accordance with WCAG 2.1 AA / EN 301 549 guidelines, App Store Review Guidelines, and Google Play Accessibility Policies.

## Overview and Audit Summary

The repository includes automated static compliance checkers (`scripts/accessibility-audit.py`) and test suites (`scripts/accessibility-audit-test.sh`) that scan codebases for accessibility compliance regressions across ten core platform areas.

### Platform Summary

| Platform | Verification Category | Rule ID | Audit Status | Severity |
| --- | --- | --- | --- | --- |
| Apple | VoiceOver | APPLE-ACCESSIBILITY-VOICEOVER | Verified / Monitored | Medium |
| Apple | Dynamic Type | APPLE-ACCESSIBILITY-DYNAMICTYPE | Verified / Monitored | Medium |
| Apple | Reduce Motion | APPLE-ACCESSIBILITY-REDUCEMOTION | Verified / Monitored | Medium |
| Apple | Color Contrast | APPLE-ACCESSIBILITY-COLORCONTRAST | Verified / Monitored | Medium |
| Apple | Haptics | APPLE-ACCESSIBILITY-HAPTICS | Verified / Monitored | Medium |
| Apple | Keyboard Navigation | APPLE-ACCESSIBILITY-KEYBOARD | Verified / Monitored | Medium |
| Android | TalkBack | ANDROID-ACCESSIBILITY-TALKBACK | Verified / Monitored | Medium |
| Android | Font Scaling | ANDROID-ACCESSIBILITY-FONTSCALING | Verified / Monitored | Medium |
| Android | High Contrast | ANDROID-ACCESSIBILITY-HIGHCONTRAST | Verified / Monitored | Medium |
| Android | Accessibility Scanner | ANDROID-ACCESSIBILITY-SCANNER | Verified / Monitored | Medium |

---

## Apple Accessibility Requirements

### 1. VoiceOver
- **Requirement**: All interactive elements (buttons, links, form fields) and informative images must provide succinct, meaningful accessibility labels, hints, and traits. Decorative images must be excluded from accessibility focus.
- **Rule ID**: `APPLE-ACCESSIBILITY-VOICEOVER`
- **SwiftUI Mechanics**: Use `Image(decorative: ...)` for decorative assets. Pass `.accessibilityLabel(...)`, `.accessibilityHint(...)`, and `.accessibilityValue(...)` to custom interactive views.
- **UIKit Mechanics**: Set `isAccessibilityElement = true`, `accessibilityLabel = "..."`, and appropriate `accessibilityTraits` (e.g. `.button`, `.header`).
- **Audit Verification**: Static audit checks SwiftUI `Image` declarations and UIKit `UIButton`/`UIImageView` instances to confirm label coverage.

### 2. Dynamic Type
- **Requirement**: Text content must automatically scale according to the user's preferred text size setting set in system preferences. Text layouts must not clip or truncate when text is scaled up to Accessibility Large sizes.
- **Rule ID**: `APPLE-ACCESSIBILITY-DYNAMICTYPE`
- **SwiftUI Mechanics**: Use relative semantic text styles such as `.font(.body)`, `.font(.headline)`, or custom relative dynamic type fonts. Avoid fixed hardcoded `.font(.system(size: 14))`.
- **UIKit Mechanics**: Use `UIFont.preferredFont(forTextStyle:)` and enable `label.adjustsFontForContentSizeCategory = true`.
- **Audit Verification**: Static audit flags hardcoded font size initializers that omit dynamic content size scaling support.

### 3. Reduce Motion
- **Requirement**: Apps must respect the `UIAccessibility.isReduceMotionEnabled` setting by eliminating or simplifying non-essential UI animations, large transition slides, and auto-playing motion graphics.
- **Rule ID**: `APPLE-ACCESSIBILITY-REDUCEMOTION`
- **SwiftUI Mechanics**: Read `@Environment(\.accessibilityReduceMotion) var reduceMotion` and conditionally skip or simplify `withAnimation` calls.
- **UIKit Mechanics**: Query `UIAccessibility.isReduceMotionEnabled` prior to calling `UIView.animate(...)` or applying CoreAnimation keyframes.
- **Audit Verification**: Audit identifies animation blocks that fail to check the Reduce Motion setting before executing transitions.

### 4. Color Contrast
- **Requirement**: Text and essential graphical elements must maintain a contrast ratio of at least 4.5:1 against their background (3:1 for large text). Apps must respect system high contrast preferences (`UIAccessibility.isDarkerSystemColorsEnabled`).
- **Rule ID**: `APPLE-ACCESSIBILITY-COLORCONTRAST`
- **SwiftUI Mechanics**: Use Asset Catalog dynamic colors or System Colors (`Color.primary`, `Color.secondary`) that automatically adjust for light, dark, and high contrast modes.
- **UIKit Mechanics**: Utilize dynamic `UIColor` providers or check `UIAccessibility.isDarkerSystemColorsEnabled` to boost contrast when enabled.
- **Audit Verification**: Audit flags hardcoded `UIColor(red:green:blue:)` declarations that ignore custom high-contrast mode adjustments.

### 5. Haptics
- **Requirement**: Provide subtle tactile haptic feedback for user interactions (e.g., button presses, toggle switches, selection changes, destructive actions) to reinforce visual and auditory cues.
- **Rule ID**: `APPLE-ACCESSIBILITY-HAPTICS`
- **SwiftUI Mechanics**: Trigger haptic feedback via `.sensoryFeedback(...)` in iOS 17+ or invoke `UIImpactFeedbackGenerator`/`UISelectionFeedbackGenerator`.
- **UIKit Mechanics**: Instantiate and prepare `UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator`, or `UISelectionFeedbackGenerator` on interactive handlers.
- **Audit Verification**: Audit checks tap and button gesture handlers for corresponding feedback generator invocations.

### 6. Keyboard Navigation
- **Requirement**: Apps on iPadOS and macOS (or iOS with attached physical keyboards) must support keyboard focus state management, logical tab ring navigation, and hardware keyboard shortcuts.
- **Rule ID**: `APPLE-ACCESSIBILITY-KEYBOARD`
- **SwiftUI Mechanics**: Annotate custom controls with `.focusable()` and manage active focus programmatically using `@FocusState`.
- **UIKit Mechanics**: Override `keyCommands` on custom view controllers and handle `UIFocusSystem` focus environment updates.
- **Audit Verification**: Audit flags views marked as `.focusable()` without corresponding `@FocusState` tracking.

---

## Android Accessibility Requirements

### 1. TalkBack
- **Requirement**: Screen readers must receive accurate visual context through `android:contentDescription` on XML views or `contentDescription` parameters in Jetpack Compose composables. Decorative graphics must explicitly hide from screen readers.
- **Rule ID**: `ANDROID-ACCESSIBILITY-TALKBACK`
- **Compose Mechanics**: Pass explicit `contentDescription = "Descriptive string"` to `Image(...)` or set `contentDescription = null` for decorative icons.
- **XML Layout Mechanics**: Assign `android:contentDescription="@string/desc"` on `ImageView` and `ImageButton`, or set `android:importantForAccessibility="no"`.
- **Audit Verification**: Audit scans XML layouts and Compose files for unlabelled image views.

### 2. Font Scaling
- **Requirement**: All text dimension attributes must use scale-independent pixels (`sp`) rather than density-independent pixels (`dp`) or fixed pixels (`px`), allowing system font scaling preferences (up to 200%) to take effect.
- **Rule ID**: `ANDROID-ACCESSIBILITY-FONTSCALING`
- **Compose Mechanics**: Define `fontSize` in `sp` (e.g., `fontSize = 16.sp`). Avoid `fontSize = 16.dp`.
- **XML Layout Mechanics**: Set `android:textSize="16sp"`. Avoid `android:textSize="16dp"`.
- **Audit Verification**: Audit scans XML layouts and Compose code for `textSize` or `fontSize` declared with `dp` units.

### 3. High Contrast
- **Requirement**: App layouts must support high-contrast display modes and custom dark/light themes by utilizing semantic theme color attributes (`?attr/colorOnSurface`, `MaterialTheme.colorScheme.primary`) instead of hardcoded hex values.
- **Rule ID**: `ANDROID-ACCESSIBILITY-HIGHCONTRAST`
- **Compose Mechanics**: Derive colors from `MaterialTheme.colorScheme` rather than instantiating hardcoded `Color(0xFF...)`.
- **XML Layout Mechanics**: Reference theme attributes (`android:textColor="?attr/colorOnSurface"`) or color resources rather than hardcoded hex color values (`#FF0000`).
- **Audit Verification**: Audit identifies hardcoded hex colors in XML attributes and Compose files that bypass high contrast theme settings.

### 4. Accessibility Scanner Recommendations
- **Requirement**: All interactive controls, touch targets, and clickable elements must meet the minimum physical touch target size of 48dp x 48dp to ensure usability for individuals with motor impairments.
- **Rule ID**: `ANDROID-ACCESSIBILITY-SCANNER`
- **Compose Mechanics**: Ensure clickable composables have minimum dimensions using `Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)` or `Modifier.size(48.dp)`.
- **XML Layout Mechanics**: Specify `android:minWidth="48dp"` and `android:minHeight="48dp"` or adequate padding on `Button`, `ImageButton`, and clickable layouts.
- **Audit Verification**: Audit identifies fixed component widths or heights below 48dp on clickable controls.

---

## Automated Verification and Continuous Testing

Continuous accessibility compliance is enforced automatically via script execution in local pre-commit checks and GitHub Actions CI pipelines (`.github/workflows/ci.yml`).

### Command Line Audit Tools
```bash
# Scan the repository or target application directory for accessibility regressions
python3 scripts/accessibility-audit.py .

# Run full test suite verifying rule detection accuracy across compliant and non-compliant samples
bash scripts/accessibility-audit-test.sh
```

### Compliance Verification Workflow
1. **Static Analysis**: `scripts/accessibility-audit.py` scans source files (`.swift`, `.m`, `.kt`, `.java`, `.xml`) against defined rule patterns.
2. **Regression Detection**: Any pattern match outputs file paths, line numbers, contextual matches, root causes, and recommended fixes.
3. **CI Pipeline Gate**: The accessibility test suite runs on every pull request and push to ensure ongoing compliance.

---

## Recommended Compliance Improvements

1. **Pre-Submission Audits**: Run `python3 scripts/accessibility-audit.py <path_to_app>` as part of every app release review before store submission.
2. **Automated UI Tests**: Integrate VoiceOver accessibility element assertions in XCTest UI tests and TalkBack accessibility checks using `AccessibilityChecks.enable()` in Espresso tests.
3. **Dynamic Type Layout Audits**: Verify layout behavior at 200% font scaling across all core screens in simulator previews.
4. **Color Contrast Inspections**: Verify all custom theme color pairs using automated contrast ratio calculators during design phase.
