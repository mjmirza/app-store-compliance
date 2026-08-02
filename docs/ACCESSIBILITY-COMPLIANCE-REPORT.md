# Accessibility Compliance Report

This report outlines the continuous digital accessibility compliance standards, evaluated rules, simulated regressions, and recommended improvements for mobile applications built using this playbook. In accordance with the European Accessibility Act (EAA Directive 2019/882), harmonised standard EN 301 549, WCAG 2.1 AA, and Apple/Google developer policies, continuous verification of accessibility is a mandatory release gate.

The static continuous accessibility compliance auditor script (located at `scripts/accessibility-audit.py`) scans application source code to detect high-frequency regressions across six key Apple iOS domains and four Google Play Android domains.

---

## Evaluated Platforms and Compliance Rules

The continuous auditing framework evaluates the following ten rules to identify and prevent user-experience regressions prior to release:

### Apple iOS (VoiceOver, Dynamic Type, Reduce Motion, Color Contrast, Haptics, Keyboard Navigation)

1. **VoiceOver Support (APPLE-ACCESSIBILITY-VOICEOVER)**
   - **Evaluated Rule:** Verification that interactive UI elements (such as SwiftUI buttons, custom controls, or UIKit UIImageView and UIButton instances) contain explicit accessibility labels, traits, or identifiers, and that non-decorative SwiftUI Image views are not defined without accessibility properties.
   - **Simulated Regression:** An Image view initialized with a raw asset name that is missing any `.accessibilityLabel()`, `.accessibilityElement()`, or decorative markers.
   - **Remediation Recommendation:** Mark purely decorative images using `Image(decorative: "asset-name")`. For informative images or controls, assign `.accessibilityLabel("Description")` or equivalent UIKit properties.

2. **Dynamic Type Support (APPLE-ACCESSIBILITY-DYNAMICTYPE)**
   - **Evaluated Rule:** Detection of hardcoded font sizes that override user system text preferences, which breaks readability for visually impaired users.
   - **Simulated Regression:** Declaring fonts using fixed points like `.font(.system(size: 24))` or UIKit's `UIFont.systemFont(ofSize: 24)` without setting `adjustsFontForContentSizeCategory = true`.
   - **Remediation Recommendation:** Use semantic system font styles such as `.font(.body)` or `.font(.title)`, or dynamically scale custom fonts by using relative text styles.

3. **Reduce Motion Settings (APPLE-ACCESSIBILITY-REDUCEMOTION)**
   - **Evaluated Rule:** Verification that animations or transitions are conditional on the user's system-level motion reduction settings to avoid triggering vestibular or balance issues.
   - **Simulated Regression:** Running `withAnimation` blocks or `UIView.animate` calls without referencing `UIAccessibility.isReduceMotionEnabled` or SwiftUI's `accessibilityReduceMotion` environment.
   - **Remediation Recommendation:** Wrap animation blocks in conditional checks, and substitute simple fades or immediate state updates when motion reduction is requested.

4. **Color Contrast Adaptivity (APPLE-ACCESSIBILITY-COLORCONTRAST)**
   - **Evaluated Rule:** Avoidance of hardcoded RGB color declarations that do not adapt dynamically to high-contrast accessibility settings or dark/light mode switches.
   - **Simulated Regression:** Instantiating UIColors with hardcoded static values like `UIColor(red: 0.1, green: 0.2, blue: 0.3, alpha: 1.0)` without monitoring `isDarkerSystemColorsEnabled` or using Dynamic Colors.
   - **Remediation Recommendation:** Define and load colors from the Asset Catalog with light, dark, and high-contrast variants, or programmatically adjust contrast in response to accessibility state updates.

5. **Haptic Tactile Feedback (APPLE-ACCESSIBILITY-HAPTICS)**
   - **Evaluated Rule:** Verification that important user actions, gestures, and button triggers provide complementary tactile sensations to support visually or hearing-impaired users.
   - **Simulated Regression:** Adding custom `onTapGesture` handlers or `Button` elements to SwiftUI views without referencing any feedback generator or haptic framework.
   - **Remediation Recommendation:** Instatiate and trigger a `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator` when executing custom taps and primary interactions.

6. **Keyboard Navigation & Focus States (APPLE-ACCESSIBILITY-KEYBOARD)**
   - **Evaluated Rule:** Verification that custom focusable controls support keyboard focus states, allowing external hardware keyboard users to navigate efficiently.
   - **Simulated Regression:** Marking a custom component as `.focusable()` without defining focus state variables or focus tracking.
   - **Remediation Recommendation:** Implement focus states using SwiftUI's `@FocusState` and `.focused(_:equals:)` modifiers to guide programmatic navigation.

### Google Play Android (TalkBack, Font Scaling, High Contrast, Touch Targets)

7. **TalkBack Support (ANDROID-ACCESSIBILITY-TALKBACK)**
   - **Evaluated Rule:** Static scan of layout resources (`.xml`) and Compose elements (`.kt`) to ensure that all non-decorative images and custom interactive views have descriptive labels.
   - **Simulated Regression:** An XML `<ImageView>` tag missing the `android:contentDescription` attribute, or a Compose `Image(...)` missing its `contentDescription` parameter.
   - **Remediation Recommendation:** Set `android:contentDescription` in XML, or pass a localized string description in Compose. Use `contentDescription = null` or `android:importantForAccessibility="no"` exclusively for purely decorative assets.

8. **Font Scaling (ANDROID-ACCESSIBILITY-FONTSCALING)**
   - **Evaluated Rule:** Search for text size declarations defined in fixed density-independent pixels (`dp`) rather than scale-independent pixels (`sp`), which blocks device-wide font scaling.
   - **Simulated Regression:** Using `android:textSize="16dp"` in layout XML files, or setting Compose fontSize using `16.dp`.
   - **Remediation Recommendation:** Replace all text-related size measurements with `sp` (e.g., `android:textSize="16sp"` or `fontSize = 16.sp`).

9. **High Contrast Themes (ANDROID-ACCESSIBILITY-HIGHCONTRAST)**
   - **Evaluated Rule:** Detection of hardcoded hexadecimal color specifications that ignore user high-contrast preferences or night mode settings.
   - **Simulated Regression:** Setting background or text colors directly to hardcoded values like `android:textColor="#FFFFFF"` in XML, or using `Color(0xFFFFFFFF)` in Compose.
   - **Remediation Recommendation:** Utilize semantic color resource attributes (e.g., `?attr/colorOnSurface`) or reference Material Theme colors instead of writing absolute hex values.

10. **Accessibility Touch Target Sizes (ANDROID-ACCESSIBILITY-SCANNER)**
    - **Evaluated Rule:** Enforcement of Google's Accessibility Scanner guidelines that require all interactive components (buttons, links, text inputs) to have a minimum touch target size of 48dp x 48dp.
    - **Simulated Regression:** Defining layout width or height explicitly to values below 48dp (such as `android:layout_width="32dp"` or a Compose `.size(32.dp)` modifier) on interactive elements.
    - **Remediation Recommendation:** Configure interactive views with at least 48dp dimension bounds, or increase the interactive target surface area by adding layout padding.

---

## Summary of Simulated Regressions and Remediation

Below is a tabular reference of simulated accessibility regressions caught by the static compliance scanner, accompanied by their severity level and corresponding remediation pathways.

| Rule ID | Domain | Severity | Common Cause | Recommended Solution |
| :--- | :--- | :--- | :--- | :--- |
| APPLE-ACCESSIBILITY-VOICEOVER | VoiceOver | Medium | SwiftUI `Image` missing accessibility modifier; UIKit layout lacking labels. | Add `.accessibilityLabel` or set `isAccessibilityElement = true`. |
| APPLE-ACCESSIBILITY-DYNAMICTYPE | Dynamic Type | Medium | Overriding text with fixed `.system(size:)` or raw `systemFont(ofSize:)`. | Use `.font(.body)` or wrap in native dynamic-type scaling. |
| APPLE-ACCESSIBILITY-REDUCEMOTION | Reduce Motion | Medium | Triggering standard animations without verifying `isReduceMotionEnabled`. | Check reduction flag, omit or simplify the transitions if active. |
| APPLE-ACCESSIBILITY-COLORCONTRAST | Contrast | Medium | Using static hex color values that ignore standard dark/light contrast adjustments. | Use dynamic semantic asset-catalog colors. |
| APPLE-ACCESSIBILITY-HAPTICS | Haptics | Medium | Interactive elements lacking touch or selection feedback signals. | Trigger `UIImpactFeedbackGenerator` on tap execution. |
| APPLE-ACCESSIBILITY-KEYBOARD | Keyboard Navigation | Medium | Custom focusable layouts omitting focus state monitoring. | Use `@FocusState` to bind and guide hardware focus transitions. |
| ANDROID-ACCESSIBILITY-TALKBACK | TalkBack | Medium | Missing `contentDescription` on Kotlin Compose Image or layout XML ImageView. | Provide a descriptive string or explicitly set to null if decorative. |
| ANDROID-ACCESSIBILITY-FONTSCALING | Font Scaling | Medium | Hardcoding text size in density-independent pixels (`dp`) instead of `sp`. | Migrate all text sizes to scale-independent pixels (`sp`). |
| ANDROID-ACCESSIBILITY-HIGHCONTRAST | High Contrast | Medium | Static background or text hex color definitions ignoring contrast toggles. | Reference Material Theme color schemes or attributes. |
| ANDROID-ACCESSIBILITY-SCANNER | Touch Targets | Medium | Interactive control sizes designed under 48dp without padding buffers. | Expand touch targets to a minimum of 48dp x 48dp using padding. |

---

## Continuous Compliance Workflow

To maintain zero-regression standards:
1. **Developer Pre-Submission Checks:** Developers should run the standalone accessibility auditor on local code changes:
   ```bash
   python3 scripts/accessibility-audit.py .
   ```
2. **Automated CI Validation:** The automated compliance pipeline executes the verification test runner `scripts/accessibility-audit-test.sh` to validate the scanner itself on mock regression files, preventing internal logic decay.
3. **Continuous Manual Reviews:** Ensure that complex interactive components are reviewed on physical devices with VoiceOver and TalkBack enabled, confirming focus order and screen-reader flow consistency.
