# Accessibility Compliance Report

This report outlines the continuous accessibility compliance audit process for our application across Apple (iOS) and Android platforms. It documents the evaluated rules, the simulated regressions used to verify our automated checkers, and recommendations for maintaining a high level of accessibility.

## 1. Evaluated Accessibility Rules

We continuously monitor and audit the application against ten critical platform accessibility standards split across Apple and Android environments.

### Apple (iOS) Platforms
1. **VoiceOver (APPLE-ACCESSIBILITY-VOICEOVER)**: Ensures all interactive views and informative elements have accessible screen-reader labels and traits, avoiding unlabelled elements.
2. **Dynamic Type (APPLE-ACCESSIBILITY-DYNAMICTYPE)**: Prevents text truncation and scale limitation by ensuring relative/system-preferred fonts scale with the user's system text size preferences.
3. **Reduce Motion (APPLE-ACCESSIBILITY-REDUCEMOTION)**: Monitors user motion preferences and automatically simplifies, scales down, or disables complex animations.
4. **Color Contrast (APPLE-ACCESSIBILITY-COLORCONTRAST)**: Enforces dynamic, adaptive, or system-integrated contrast modes to assist users with low vision.
5. **Haptics (APPLE-ACCESSIBILITY-HAPTICS)**: Enhances tactile interactive feedback on primary controls, gestures, and UI events.
6. **Keyboard Navigation (APPLE-ACCESSIBILITY-KEYBOARD)**: Facilitates full hardware keyboard usage and focus tracking for users who do not navigate via touch screens.

### Android Platforms
7. **TalkBack (ANDROID-ACCESSIBILITY-TALKBACK)**: Guarantees every ImageView, ImageButton, and Compose Image provides a descriptive content description or is explicitly hidden if decorative.
8. **Font Scaling (ANDROID-ACCESSIBILITY-FONTSCALING)**: Prohibits hardcoding text sizes in DP, enforcing SP units instead so Android's font scaling operates correctly.
9. **High Contrast (ANDROID-ACCESSIBILITY-HIGHCONTRAST)**: Bans hardcoded hex codes for background and text colors, requiring references to semantic theme colors that adapt to system-level contrast/accessibility theme overrides.
10. **Accessibility Scanner (ANDROID-ACCESSIBILITY-SCANNER)**: Ensures interactive controls maintain a minimum touch target threshold of 48dp x 48dp to support precise input.

---

## 2. Simulated Regressions and Verification

To ensure that our continuous compliance checks remain accurate and resilient, we maintain a test script ('scripts/accessibility-audit-test.sh') that dynamically generates mock files to test our rules. For each rule, we verify two scenarios:

### APPLE-ACCESSIBILITY-VOICEOVER
* **Regression (Non-Compliant)**: SwiftUI Image declarations without trailing accessibility modifiers, or UIKit UIButton/UIImageView definitions in files that completely omit any accessibility labeling.
* **Compliant**: Image declarations initialized with 'decorative' or 'systemName', or appending explicit '.accessibilityLabel()' modifiers.

### APPLE-ACCESSIBILITY-DYNAMICTYPE
* **Regression (Non-Compliant)**: SwiftUI components declaring hardcoded system font sizes via '.font(.system(size: ...))', or UIKit labels using static 'UIFont.systemFont(ofSize: ...)' without any adjustments.
* **Compliant**: Referencing relative dynamic text styles like '.font(.body)' and setting 'adjustsFontForContentSizeCategory = true' for UIKit views.

### APPLE-ACCESSIBILITY-REDUCEMOTION
* **Regression (Non-Compliant)**: Triggering complex 'withAnimation' transitions or 'UIView.animate' flows without verifying the user's Reduce Motion status.
* **Compliant**: Wrapping animations in conditional statements checking 'UIAccessibility.isReduceMotionEnabled' or 'accessibilityReduceMotion'.

### APPLE-ACCESSIBILITY-COLORCONTRAST
* **Regression (Non-Compliant)**: Hardcoding static RGB UIColor values that are non-adaptive and ignore contrast modes.
* **Compliant**: Introducing high-contrast branches checking 'UIAccessibility.isDarkerSystemColorsEnabled' or utilizing dynamic asset catalogs.

### APPLE-ACCESSIBILITY-HAPTICS
* **Regression (Non-Compliant)**: Interactive 'Button' elements or custom gestures that do not reference tactile feedback engines.
* **Compliant**: Referencing and instantiating 'UIImpactFeedbackGenerator' inside gesture or tap handlers to emit haptic cues.

### APPLE-ACCESSIBILITY-KEYBOARD
* **Regression (Non-Compliant)**: Defining '.focusable()' elements without keeping track of focused elements.
* **Compliant**: Tracking focus state programmatically using '@FocusState' and the '.focused()' modifier.

### ANDROID-ACCESSIBILITY-TALKBACK
* **Regression (Non-Compliant)**: XML 'ImageView' structures missing 'android:contentDescription', or Jetpack Compose 'Image' calls missing the 'contentDescription' parameter.
* **Compliant**: Explicitly populating 'android:contentDescription' in XML layouts and defining 'contentDescription' string references in Compose.

### ANDROID-ACCESSIBILITY-FONTSCALING
* **Regression (Non-Compliant)**: Declaring text size in DP inside XML layouts or Compose Text widgets.
* **Compliant**: Always expressing font sizes in scale-independent pixels (SP).

### ANDROID-ACCESSIBILITY-HIGHCONTRAST
* **Regression (Non-Compliant)**: Hardcoding RGB hex colors (e.g. '#FF0000' or 'Color(0xFFFF0000)') for critical text and background fields.
* **Compliant**: Referencing semantic theme colors like '?attr/colorOnSurface' or 'MaterialTheme.colorScheme.primary' which adjust dynamically.

### ANDROID-ACCESSIBILITY-SCANNER
* **Regression (Non-Compliant)**: Declaring click-responsive components under 48dp in size or using hardcoded smaller dimensions.
* **Compliant**: Keeping control sizes above 48dp (e.g. '.size(48.dp)') or utilizing wrap_content layout rules that automatically handle padding.

---

## 3. Recommendations for Continuous Compliance

To prevent regressions from ever reaching the App Store and Google Play, we recommend adopting the following practices:

1. **Pre-commit and CI Pipelines**: Regularly run 'python3 scripts/accessibility-audit.py .' as part of your local workflow and continuous integration checks to catch regressions prior to merging code.
2. **Dynamic Semantic Coloring**: Always decouple layouts from hardcoded coloring. Depend entirely on system asset catalogs and material color themes.
3. **Strict Linting for Spacing and Sizes**: Enforce linting rules that require a minimum touch target dimension of 48dp for all interactive nodes and views.
4. **Automated Integration Testing**: Use platform UI testing frameworks (such as XCUITest for iOS or Espresso/Compose Test for Android) with accessibility verification flags enabled to validate focus ordering and element labels.
