# Accessibility Compliance Report

This report evaluates and documents the continuous accessibility compliance frameworks for mobile and web platforms, specifically targeting Apple iOS and Google Android. It outlines the specific accessibility rules monitored, details the simulated regressions and testing suite that ensures our compliance engine functions correctly, and provides concrete recommendations for development teams to ensure high standards of digital inclusivity.

## 1. Executive Summary

Digital accessibility is not only a crucial usability attribute but also a strict regulatory mandate. With major legislation such as the European Accessibility Act, Directive (EU) 2019/882, coming into full force since 28 June 2025, mobile applications and digital services must meet harmonized accessibility standards.

This playbook establishes a robust static-analysis system, implemented in `scripts/accessibility-audit.py` and validated by `scripts/accessibility-audit-test.sh`. This continuous auditing framework maps specific codebase implementation signals against major accessibility rules, catching regressions before production releases.

## 2. Scope and Platform Focus

The continuous compliance monitor evaluates key accessibility requirements across two primary target platforms: Apple (iOS/iPadOS/macOS) and Android (Google Play ecosystem).

The core verification domains include:

- **Apple Platform:**
  - VoiceOver Support
  - Dynamic Type Compatibility
  - Reduce Motion Responsiveness
  - Color Contrast Adaptivity
  - Haptic Feedback Integration
  - Keyboard Navigation & Focus Tracking

- **Android Platform:**
  - TalkBack Reader Support
  - Font Scaling Compliance
  - High Contrast System Theme Adaptivity
  - Accessibility Scanner Target Thresholds

## 3. Apple Accessibility Verifications

### 3.1. VoiceOver
VoiceOver is the gesture-based screen reader built into Apple operating systems. It enables blind or visually impaired users to interact with applications.
- **Rules Evaluated:** SwiftUI image initializations must specify accessibility attributes or be explicitly marked as decorative. For UIKit, custom controls and views like `UIButton` or `UIImageView` must reference accessibility properties.
- **Common Triggers:** Raw `Image("logo")` calls without trailing accessibility modifiers, or UIKit view classes declaring interactive components without setting `accessibilityLabel` or `isAccessibilityElement = true`.

### 3.2. Dynamic Type
Dynamic Type allows users to customize the size of on-screen text to suit their viewing preferences.
- **Rules Evaluated:** Avoid hardcoded system font sizes in SwiftUI and UIKit.
- **Common Triggers:** Using `.font(.system(size: 14))` in SwiftUI or `UIFont.systemFont(ofSize: 14)` in UIKit without accompanying `adjustsFontForContentSizeCategory = true` configurations.

### 3.3. Reduce Motion
Reduce Motion is an accessibility setting that minimizes screen movement, transitions, and zoom effects.
- **Rules Evaluated:** Ensure animations check the user's motion preference prior to rendering transitions.
- **Common Triggers:** Using `withAnimation` in SwiftUI or `UIView.animate` in UIKit without verifying `UIAccessibility.isReduceMotionEnabled` or using the `accessibilityReduceMotion` environment variable.

### 3.4. Color Contrast and Darker System Colors
Color contrast ensures text and graphical elements remain readable to users with low vision or color-blindness.
- **Rules Evaluated:** Hardcoded raw colors must support high-contrast alternatives or dynamically adapt to system accessibility modes.
- **Common Triggers:** Static RGB definitions such as `UIColor(red: 255, green: 0, blue: 0, alpha: 1)` when the codebase lacks references to system properties like `UIAccessibility.isDarkerSystemColorsEnabled` or `darkerSystemColors`.

### 3.5. Haptics
Tactile feedback reinforces visual interactions and provides secondary indicators for user actions.
- **Rules Evaluated:** Ensure interactive elements provide corresponding physical feedback using platform-compliant feedback generators.
- **Common Triggers:** Interactive gestures or buttons implemented in custom controls without importing or invoking `UIImpactFeedbackGenerator`, `UISelectionFeedbackGenerator`, or `CHHapticEngine`.

### 3.6. Keyboard Navigation
Users with physical or motor disabilities navigate applications using connected hardware keyboards or switch controls.
- **Rules Evaluated:** Focusable elements must implement proper focus state tracking.
- **Common Triggers:** Custom interactive items declaring `.focusable()` in SwiftUI without incorporating `@FocusState` property wrappers to manage programmatic key-focus transitions.

## 4. Android Accessibility Verifications

### 4.1. TalkBack
TalkBack is the Google screen reader included on Android devices, providing spoken feedback for eyes-free device navigation.
- **Rules Evaluated:** Graphical elements (XML `ImageView` and Compose `Image` declarations) must supply a descriptive content description or be explicitly hidden from screen readers.
- **Common Triggers:** Missing `android:contentDescription` attributes in layout files or omiting the `contentDescription` parameter inside Jetpack Compose `Image()` composites.

### 4.2. Font Scaling
Android users can adjust the display font size globally across the system.
- **Rules Evaluated:** Text sizes must be specified using scale-independent pixels (sp) instead of density-independent pixels (dp) or raw pixels.
- **Common Triggers:** Hardcoding text sizes as `android:textSize="16dp"` in XML or `fontSize = 16.dp` in Jetpack Compose layouts.

### 4.3. High Contrast Theme Adaptivity
High contrast text and UI components assist users with low vision to differentiate UI elements.
- **Rules Evaluated:** Hardcoded color specifications should be replaced with semantic color references that adapt dynamically to themes.
- **Common Triggers:** Using raw color codes like `android:textColor="#FF0000"` in XML or hardcoded color constants like `Color(0xFFFF0000)` in Compose.

### 4.4. Accessibility Scanner Target Thresholds
Google's Accessibility Scanner checks apps for touch target size, contrast ratio, and other accessibility attributes.
- **Rules Evaluated:** Touch targets must meet a minimum size of 48dp x 48dp to prevent activation errors.
- **Common Triggers:** Hardcoding clickable item sizes below 48dp, such as layout dimensions like `android:minWidth="40dp"` in XML or `.size(40.dp)` modifiers in Jetpack Compose.

## 5. Automated Regression Detection

To enforce compliance continuously, our codebase includes a static compliance engine.

### 5.1. Static Compliance Auditor (`scripts/accessibility-audit.py`)
This script acts as a localized, fast-running static scanner that parses files in-place and matches syntax patterns representing accessibility failures. It supports targeted checks:
- It excludes build directories, external dependencies, and test resources (`node_modules`, `build`, etc.) to minimize noise.
- It parses Swift and Objective-C files for Apple-specific rules, and Kotlin, Java, and XML layout resources for Android-specific rules.

### 5.2. Verification Suite (`scripts/accessibility-audit-test.sh`)
To verify that our compliance scanner never drifts or fails to detect real issues, we utilize a dedicated test runner.
- The test suite generates dynamic, temporary mock directories containing:
  1. **Compliant Case Files:** Fully annotated code blocks utilizing proper accessibility parameters (e.g., `Image(decorative: ...)`, `sp` units, dynamic color adapters, focus states).
  2. **Regression Case Files:** Codeblocks deliberately stripped of mandatory attributes to represent realistic regression scenarios.
- The suite runs the auditor against both directories and asserts:
  - Zero warnings on compliant code.
  - Correct and specific rule-flagging on all 10 non-compliant regression blocks.

## 6. Actionable Recommendations for Development Teams

To prevent common accessibility rejections and regulatory violations, development teams should adopt these practices:

1. **Integrate the Audit in Pre-Release Workflows:** Run `python3 scripts/accessibility-audit.py` as an advisory pre-push step or integrate it into pull request CI checks to catch regressions before they reach QA.
2. **Standardize Component Libraries:** Create wrapped widgets or components (such as accessible image containers and dynamic buttons) that enforce mandatory properties (like `contentDescription` and minimum 48dp layouts) by default.
3. **Establish Design System Semantics:** Avoid raw hex-code declarations or static RGB values. Implement dynamic, named assets or semantic system attributes (e.g., dynamic colors, typography styles) to ensure contrast and font-scaling adjustments occur globally and automatically.
4. **Conduct Regular Audits on Hardware:** Supplement automated static scans with manual screen reader testing (using VoiceOver on iOS and TalkBack on Android) during major feature cycles to ensure logical screen navigation and clean announcements.

## 7. Priority 1 Official Citations and Legal References

These guidelines are built upon official, authoritative industry standards and legislative documentation:

- **European Accessibility Act (EAA):** Directive (EU) 2019/882 on the accessibility requirements for products and services.
  Source: [European Commission EAA](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)
- **Web Content Accessibility Guidelines (WCAG) 2.1 AA:**
  Source: [W3C WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- **ETSI EN 301 549 Standard:** Accessiblity requirements for ICT products and services, including mobile applications.
  Source: [ETSI EN 301 549 chapter 11 on mobile apps](https://auditsu.com/resources/en-301-549-chapter-11-mobile-apps)
- **Apple iOS Accessibility Guidelines:** VoiceOver labels, traits, and accessibility attributes.
  Source: [Apple Accessibility Support](https://developer.apple.com/accessibility/)
- **Android Accessibility Testing Manual:** Manual and automated testing recommendations for TalkBack, Font scaling, and touch target sizing.
  Source: [Android Accessibility Testing Guide](https://developer.android.com/guide/topics/ui/accessibility/testing)
