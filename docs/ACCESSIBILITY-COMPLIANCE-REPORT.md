# Accessibility Compliance & Verification Report

## Executive Summary

This report establishes the continuous accessibility compliance audit and verification framework for mobile applications across iOS (Apple) and Android platforms. Meeting mobile accessibility requirements is essential to satisfy international legal frameworks (such as the European Accessibility Act Directive 2019/882 and EN 301 549 / WCAG 2.1 AA standards) and platform guidelines across App Store and Google Play ecosystems.

The repository provides continuous accessibility compliance guidelines and reference rules (`scripts/accessibility-audit.py` and `scripts/accessibility-audit-test.sh`), enabling teams to run static audits against iOS and Android application repositories.

---

## Audited Platform Domains

### 1. Apple (iOS / iPadOS)

#### VoiceOver
- **Verification Criteria:** Interactive controls and informative elements must declare accessibility labels (`accessibilityLabel`), traits (`accessibilityTraits`), and hints (`accessibilityHint`). Purely decorative elements must be marked decorative (`Image(decorative: ...)` in SwiftUI or `isAccessibilityElement = false` in UIKit) or hidden (`.accessibilityHidden(true)`).
- **Rule ID:** `APPLE-ACCESSIBILITY-VOICEOVER`
- **Common Regressions:** SwiftUI `Image("name")` instantiated without `.accessibilityLabel(...)` or non-decorative wrapper; custom UIKit controls missing `isAccessibilityElement = true`.
- **Recommended Remediation:** Ensure all custom UI elements and image views define explicit, localized accessibility strings. Group related text labels and icons into single logical accessibility elements using `.accessibilityElement(children: .combine)`.

#### Dynamic Type
- **Verification Criteria:** Text content must dynamically scale according to user system settings.
- **Rule ID:** `APPLE-ACCESSIBILITY-DYNAMICTYPE`
- **Common Regressions:** Hardcoded text sizes like `.font(.system(size: 14))` in SwiftUI or `UIFont.systemFont(ofSize: 14)` in UIKit without enabling `adjustsFontForContentSizeCategory = true`.
- **Recommended Remediation:** Utilize semantic system text styles such as `.font(.body)` or `UIFont.preferredFont(forTextStyle: .body)`. Ensure custom layouts do not clip or truncate text when scaled up to Accessibility Extra Large sizes.

#### Reduce Motion
- **Verification Criteria:** Applications must respect the user's Reduce Motion setting (`UIAccessibility.isReduceMotionEnabled` / `@Environment(\.accessibilityReduceMotion)`).
- **Rule ID:** `APPLE-ACCESSIBILITY-REDUCEMOTION`
- **Common Regressions:** Triggering auto-playing, high-frequency, or screen-spanning animations (via `withAnimation` or `UIView.animate`) without querying the system motion preference.
- **Recommended Remediation:** Gate complex spatial transitions or decorative animations behind a Reduce Motion check, falling back to simple cross-fades or static state changes when enabled.

#### Color Contrast
- **Verification Criteria:** Text and key visual components must achieve at least 4.5:1 contrast for normal text and 3:1 for large text / UI controls. High Contrast settings (`UIAccessibility.isDarkerSystemColorsEnabled`) must be supported.
- **Rule ID:** `APPLE-ACCESSIBILITY-COLORCONTRAST`
- **Common Regressions:** Hardcoding fixed RGB values (`UIColor(red:green:blue:alpha:)`) that do not adapt to Dark Mode or increased contrast settings.
- **Recommended Remediation:** Define colors using asset catalog dynamic color sets or system dynamic colors (`UIColor.label`, `UIColor.systemBackground`). Support high-contrast variants where appropriate.

#### Haptics
- **Verification Criteria:** Tactile feedback must accompany key interactions (such as button presses, selection changes, and error states) to assist vision-impaired or multi-sensory users.
- **Rule ID:** `APPLE-ACCESSIBILITY-HAPTICS`
- **Common Regressions:** Implementing custom gestures or tap handlers (`onTapGesture`, custom controls) without invoking haptic feedback generators.
- **Recommended Remediation:** Integrate `UIImpactFeedbackGenerator`, `UISelectionFeedbackGenerator`, or `UINotificationFeedbackGenerator` for primary user actions.

#### Keyboard Navigation
- **Verification Criteria:** Users operating physical keyboards or assistive switch hardware must be able to navigate, focus, and trigger all interactive elements.
- **Rule ID:** `APPLE-ACCESSIBILITY-KEYBOARD`
- **Common Regressions:** Custom interactive views that cannot receive focus or lack visible focus indicators and state tracking (`@FocusState` / `focusable()`).
- **Recommended Remediation:** Utilize SwiftUI `@FocusState` or UIKit `keyCommands` / `UIFocusSystem` to manage focus programmatically and highlight focused controls clearly.

---

### 2. Android (Google Play)

#### TalkBack
- **Verification Criteria:** All informative images, icons, and interactive views must expose meaningful `android:contentDescription` attributes in XML layouts or `contentDescription` parameters in Jetpack Compose.
- **Rule ID:** `ANDROID-ACCESSIBILITY-TALKBACK`
- **Common Regressions:** XML `<ImageView>` or Compose `Image(...)` components missing `contentDescription` or providing non-descriptive strings (e.g., "image", "button").
- **Recommended Remediation:** Provide concise, localized descriptions for informative elements and set `android:importantForAccessibility="no"` (or `contentDescription = null` in Compose) for purely decorative graphics.

#### Font Scaling
- **Verification Criteria:** Text sizes must use scale-independent pixels (`sp`) to allow system font scaling up to 200% without breaking layouts.
- **Rule ID:** `ANDROID-ACCESSIBILITY-FONTSCALING`
- **Common Regressions:** Defining `android:textSize` with `dp` units in XML or `fontSize = 16.dp` in Jetpack Compose.
- **Recommended Remediation:** Replace all text size `dp` units with `sp`. Test layouts at maximum system font scale (200%) to ensure text container expansion and scrollability.

#### High Contrast
- **Verification Criteria:** Color schemes must support high-contrast display modes and user-selected dark/light themes.
- **Rule ID:** `ANDROID-ACCESSIBILITY-HIGHCONTRAST`
- **Common Regressions:** Hardcoded hex color codes (`#FF0000` or `Color(0xFF000000)`) for text and element backgrounds.
- **Recommended Remediation:** Reference Material Design theme color tokens (e.g., `?attr/colorOnSurface` or `MaterialTheme.colorScheme.primary`) so colors automatically adapt to system contrast settings and theme modes.

#### Accessibility Scanner Recommendations
- **Verification Criteria:** Interactive controls must meet minimum touch target dimensions (48dp x 48dp) to facilitate reliable user selection.
- **Rule ID:** `ANDROID-ACCESSIBILITY-SCANNER`
- **Common Regressions:** Clickable buttons, icons, or list items with width or height under 48dp (e.g. 24dp or 32dp icons without touch padding).
- **Recommended Remediation:** Increase view layout dimensions or apply internal padding / `TouchDelegate` / `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)` to ensure all touchable areas meet or exceed 48dp x 48dp.

---

## Static Audit Rules Reference

| Rule ID | Platform | Severity | Domain | Automated Scan Trigger | Recommended Fix |
| --- | --- | --- | --- | --- | --- |
| `APPLE-ACCESSIBILITY-VOICEOVER` | Apple | Medium | VoiceOver | `Image` without label/decorative or UIKit without `accessibilityLabel` | Add localized `accessibilityLabel` or initialize as decorative. |
| `APPLE-ACCESSIBILITY-DYNAMICTYPE` | Apple | Medium | Dynamic Type | Fixed `.system(size:)` font or `UIFont.systemFont` without content size adjustment | Use relative styles like `.font(.body)` or `preferredFont`. |
| `APPLE-ACCESSIBILITY-REDUCEMOTION` | Apple | Medium | Reduce Motion | Animations called without `isReduceMotionEnabled` check | Disable or simplify transitions when Reduce Motion is set. |
| `APPLE-ACCESSIBILITY-COLORCONTRAST` | Apple | Medium | Contrast | Static RGB UIColors without dynamic adaptivity or contrast checks | Use asset catalog dynamic colors or check `isDarkerSystemColorsEnabled`. |
| `APPLE-ACCESSIBILITY-HAPTICS` | Apple | Medium | Haptics | Taps or custom controls missing haptic feedback generator calls | Implement `UIImpactFeedbackGenerator` or `UISelectionFeedbackGenerator`. |
| `APPLE-ACCESSIBILITY-KEYBOARD` | Apple | Medium | Keyboard | Focusable elements missing focus state management | Manage focus programmatically using `@FocusState` or `keyCommands`. |
| `ANDROID-ACCESSIBILITY-TALKBACK` | Android | Medium | TalkBack | XML `ImageView` or Compose `Image` missing `contentDescription` | Provide descriptive `contentDescription` or set decorative explicitly. |
| `ANDROID-ACCESSIBILITY-FONTSCALING` | Android | Medium | Font Scaling | Text size specified in `dp` instead of `sp` | Specify text sizes in scale-independent pixels (`sp`). |
| `ANDROID-ACCESSIBILITY-HIGHCONTRAST` | Android | Medium | High Contrast | Hardcoded hex color codes ignoring theme attributes | Utilize Material theme semantic colors and dynamic color attributes. |
| `ANDROID-ACCESSIBILITY-SCANNER` | Android | Medium | Touch Targets | Interactive element dimensions below 48dp threshold | Enlarge touch bounds to at least 48dp x 48dp using padding or layout constraints. |

---

## Continuous Verification Workflow

1. **Automated Static Audits:** Execute `python3 scripts/accessibility-audit.py <path_to_app>` as part of local development and CI pipelines.
2. **Regression Testing:** Run `bash scripts/accessibility-audit-test.sh` to confirm scanner accuracy against positive and negative test cases.
3. **Platform Testing:**
   - **iOS:** Test with Accessibility Inspector in Xcode, enable VoiceOver in Simulator, and toggle Dynamic Type / Reduce Motion in Accessibility settings.
   - **Android:** Run Google Accessibility Scanner on live builds, activate TalkBack in test settings, and inspect touch target overlays.

---

## References & Official Guidance

- **European Accessibility Act (Directive (EU) 2019/882):** [EUR-Lex Directive 2019/882](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882)
- **Apple Accessibility Guidelines:** [Apple Accessibility Overview](https://developer.apple.com/accessibility/)
- **Android Accessibility Guidance:** [Android Accessibility Testing](https://developer.android.com/guide/topics/ui/accessibility/testing)
