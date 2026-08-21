# Continuous Accessibility Review Report (2026)

## Executive Summary

This document presents a comprehensive evaluation of continuous accessibility compliance across Apple iOS/iPadOS and Google Android platforms. Mobile accessibility compliance is required both under store review guidelines (Apple App Review Guidelines section 2.5.8 and Google Play Accessibility Policies) and European Accessibility Act (EAA) directive requirements enforced in 2026.

The static continuous auditor (`scripts/accessibility-audit.py`) and test suite (`scripts/accessibility-audit-test.sh`) verify 10 core accessibility domains across iOS (UIKit/SwiftUI) and Android (XML/Jetpack Compose) codebases.

---

## Evaluated Accessibility Domains

### Apple Platform Domains

1. VoiceOver
   - Rule ID: `APPLE-ACCESSIBILITY-VOICEOVER`
   - Description: Evaluates interactive controls and images for missing accessibility labels, hints, traits, or decorative initializations.
   - Requirement: Ensure all interactive components have descriptive `accessibilityLabel` properties and decorative images use `Image(decorative:)` or `.accessibilityHidden(true)`.

2. Dynamic Type
   - Rule ID: `APPLE-ACCESSIBILITY-DYNAMICTYPE`
   - Description: Checks for hardcoded font sizes that inhibit dynamic system font scaling.
   - Requirement: Use preferred font styles (`UIFont.preferredFont(forTextStyle:)` or SwiftUI `.font(.body)`) with `adjustsFontForContentSizeCategory = true`.

3. Reduce Motion
   - Rule ID: `APPLE-ACCESSIBILITY-REDUCEMOTION`
   - Description: Detects animation blocks that do not check system motion reduction preferences.
   - Requirement: Query `UIAccessibility.isReduceMotionEnabled` or SwiftUI `@Environment(\.accessibilityReduceMotion)` to disable or simplify non-essential movement.

4. Color Contrast
   - Rule ID: `APPLE-ACCESSIBILITY-COLORCONTRAST`
   - Description: Checks for hardcoded RGB colors that fail to adapt to system dark mode or increased contrast settings.
   - Requirement: Use asset catalog dynamic colors or adapt colors based on `UIAccessibility.isDarkerSystemColorsEnabled`.

5. Haptics
   - Rule ID: `APPLE-ACCESSIBILITY-HAPTICS`
   - Description: Identifies interactive controls lacking tactile sensory feedback.
   - Requirement: Incorporate `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator` on key interactions.

6. Keyboard Navigation
   - Rule ID: `APPLE-ACCESSIBILITY-KEYBOARD`
   - Description: Verifies physical keyboard focus navigation and state tracking.
   - Requirement: Utilize `@FocusState` in SwiftUI or `keyCommands` in UIKit to ensure complete keyboard focus traversal.

### Android Platform Domains

7. TalkBack
   - Rule ID: `ANDROID-ACCESSIBILITY-TALKBACK`
   - Description: Evaluates layout elements and Compose views for missing content descriptions.
   - Requirement: Provide explicit `android:contentDescription` in XML or `contentDescription` in Compose, or set `importantForAccessibility="no"` for purely decorative elements.

8. Font Scaling
   - Rule ID: `ANDROID-ACCESSIBILITY-FONTSCALING`
   - Description: Scans for fixed dimension font sizes specified in `dp` instead of `sp`.
   - Requirement: Always define text sizes in scale-independent pixels (`sp`) in XML layouts and Compose text components.

9. High Contrast
   - Rule ID: `ANDROID-ACCESSIBILITY-HIGHCONTRAST`
   - Description: Detects hardcoded hex color values that ignore high-contrast system themes.
   - Requirement: Reference semantic theme attributes (e.g., `?attr/colorOnSurface`) or Material theme color schemes.

10. Accessibility Scanner Recommendations (Touch Target Size)
    - Rule ID: `ANDROID-ACCESSIBILITY-SCANNER`
    - Description: Evaluates interactive target sizes against Google Play Accessibility Scanner standards.
    - Requirement: Maintain minimum touch target dimensions of 48dp x 48dp with appropriate layout padding.

---

## Static Audit Findings and Regressions

### Repository Scan Results
- Scanned iOS files: 0 (Repository consists of compliance guidelines, scripts, and automation assets)
- Scanned Android files: 0
- Regressions detected in repository root: 0 (Clean)

### Simulated Regression Validation Summary
When tested against simulated regression fixtures in `scripts/accessibility-audit-test.sh`, the auditor accurately flagged all 10 target accessibility regression patterns:
- Flagged `APPLE-ACCESSIBILITY-VOICEOVER` on unlabelled SwiftUI Image constructs.
- Flagged `APPLE-ACCESSIBILITY-DYNAMICTYPE` on hardcoded system font declarations.
- Flagged `APPLE-ACCESSIBILITY-REDUCEMOTION` on unconditioned animations.
- Flagged `APPLE-ACCESSIBILITY-COLORCONTRAST` on static raw RGB color definitions.
- Flagged `APPLE-ACCESSIBILITY-HAPTICS` on tap gestures without feedback generators.
- Flagged `APPLE-ACCESSIBILITY-KEYBOARD` on focusable views lacking `@FocusState`.
- Flagged `ANDROID-ACCESSIBILITY-TALKBACK` on Image views missing content descriptions.
- Flagged `ANDROID-ACCESSIBILITY-FONTSCALING` on text sizes specified in `dp`.
- Flagged `ANDROID-ACCESSIBILITY-HIGHCONTRAST` on hardcoded hex background/text colors.
- Flagged `ANDROID-ACCESSIBILITY-SCANNER` on interactive elements sized below 48dp.

---

## Recommended Improvements

### Implementation Recommendations for Mobile Developers

1. Automated Pre-commit Auditing
   - Integrate `python3 scripts/accessibility-audit.py` into local Git pre-commit hooks and CI pipelines to prevent non-compliant UI components from being merged.

2. Automated UI Accessibility Testing
   - On iOS, run XCTest accessibility audits (`XCUIApplication().performAccessibilityAudit()`) as part of UI test suites.
   - On Android, integrate `AccessibilityChecks.enable()` in Espresso UI tests to catch TalkBack and touch target regressions automatically.

3. Design Token Standardization
   - Enforce semantic design tokens across iOS and Android themes so text styles automatically inherit dynamic type scaling and high-contrast theme variations.

4. Manual Assistive Technology Testing
   - Perform routine manual verification using VoiceOver on physical iOS devices and TalkBack on Android devices for all new UI flows.
