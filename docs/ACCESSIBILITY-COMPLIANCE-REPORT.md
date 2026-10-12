# Mobile Accessibility Compliance Report

This report documents continuous accessibility compliance verification and recommendations across iOS/iPadOS (Apple) and Android platforms in accordance with App Store guidelines, Google Play policies, EN 301 549 standards, WCAG 2.1 AA criteria, and the European Accessibility Act (EAA Directive EU 2019/882).

---

## Executive Summary

Continuous accessibility evaluation verifies that all user interface components support assistive technologies, adapt to user system preferences, maintain sufficient contrast, and provide alternative sensory cues.

Automated static auditing via `scripts/accessibility-audit.py` scans the repository for 10 platform-specific accessibility rules.

| Platform | Domain / Requirement | Rule Identifier | Status | Findings | Risk Severity |
|---|---|---|---|---|---|
| Apple | VoiceOver | `APPLE-ACCESSIBILITY-VOICEOVER` | Verified | 0 Regressions | Medium |
| Apple | Dynamic Type | `APPLE-ACCESSIBILITY-DYNAMICTYPE` | Verified | 0 Regressions | Medium |
| Apple | Reduce Motion | `APPLE-ACCESSIBILITY-REDUCEMOTION` | Verified | 0 Regressions | Medium |
| Apple | Color Contrast | `APPLE-ACCESSIBILITY-COLORCONTRAST` | Verified | 0 Regressions | Medium |
| Apple | Haptics | `APPLE-ACCESSIBILITY-HAPTICS` | Verified | 0 Regressions | Medium |
| Apple | Keyboard Navigation | `APPLE-ACCESSIBILITY-KEYBOARD` | Verified | 0 Regressions | Medium |
| Android | TalkBack | `ANDROID-ACCESSIBILITY-TALKBACK` | Verified | 0 Regressions | Medium |
| Android | Font Scaling | `ANDROID-ACCESSIBILITY-FONTSCALING` | Verified | 0 Regressions | Medium |
| Android | High Contrast | `ANDROID-ACCESSIBILITY-HIGHCONTRAST` | Verified | 0 Regressions | Medium |
| Android | Accessibility Scanner | `ANDROID-ACCESSIBILITY-SCANNER` | Verified | 0 Regressions | Medium |

---

## Platform Detailed Audits & Recommendations

### 1. Apple Platform Accessibility Requirements

#### VoiceOver
* **Requirement:** All interactive controls, informative images, and grouped containers must declare accurate accessibility labels, traits, values, and hints. Decorative elements must be hidden from assistive technology.
* **Verification Logic:** Audits SwiftUI `Image` declarations for missing `.accessibilityLabel(...)` or `Image(decorative: ...)` parameters, and UIKit controls (`UIButton`, `UIImageView`) for missing `accessibilityLabel` properties.
* **Implementation Standard:**
  * SwiftUI: `Image("graphic").accessibilityLabel(Text("Account Overview"))` or `Image(decorative: "background")`.
  * UIKit: `button.accessibilityLabel = "Close screen"` or `imageView.isAccessibilityElement = false`.
* **Recommended Improvement:** Ensure dynamic content changes (such as async loading states or form errors) post screen reader notifications via `UIAccessibility.post(notification: .announcement, argument: "Error updated")` or SwiftUI `AccessibilityNotification.Announcement`.

#### Dynamic Type
* **Requirement:** Text size must automatically scale when users adjust System Text Size or Dynamic Type accessibility settings, without clipping text, overlapping views, or breaking layout containers.
* **Verification Logic:** Checks SwiftUI fonts for hardcoded size declarations like `.font(.system(size: 16))` and UIKit `UIFont.systemFont(ofSize: 16)` missing `adjustsFontForContentSizeCategory = true`.
* **Implementation Standard:**
  * SwiftUI: Use relative typography styles like `.font(.body)`, `.font(.title)`, or `@ScaledMetric`.
  * UIKit: `label.font = UIFont.preferredFont(forTextStyle: .body)` and `label.adjustsFontForContentSizeCategory = true`.
* **Recommended Improvement:** Support dynamic line limits and flexible scroll views (`ScrollView`) so large text sizes accommodate up to 310 percent scaling under Dynamic Type / Larger Accessibility Text settings.

#### Reduce Motion
* **Requirement:** Non-essential or disruptive UI animations, transitions, auto-playing video clips, and parallax effects must be disabled or simplified when the system Reduce Motion setting is enabled.
* **Verification Logic:** Audits SwiftUI `withAnimation` calls and UIKit `UIView.animate` blocks for missing checks against `UIAccessibility.isReduceMotionEnabled` or `@Environment(\.accessibilityReduceMotion)`.
* **Implementation Standard:**
  * SwiftUI: Check `@Environment(\.accessibilityReduceMotion) var reduceMotion` and swap complex transitions (`.slide`) for standard cross-fades (`.opacity`).
  * UIKit: Check `UIAccessibility.isReduceMotionEnabled` before triggering spatial animations.
* **Recommended Improvement:** Provide explicit app settings or automatic fallbacks for custom particle systems, interactive gestures, and complex screen transitions.

#### Color Contrast
* **Requirement:** Text and essential graphical UI elements must maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text / graphical controls against their background under WCAG 2.1 AA / EN 301 549. Information must never be conveyed by color alone.
* **Verification Logic:** Flags hardcoded static RGB color definitions (`UIColor(red:green:blue:alpha:)`) that fail to monitor `UIAccessibility.isDarkerSystemColorsEnabled` or utilize dynamic asset catalog colors.
* **Implementation Standard:**
  * Define semantic color palettes using Asset Catalog Named Colors configured for light, dark, and high contrast variations.
  * Check `UIAccessibility.isDarkerSystemColorsEnabled` or `UIAccessibility.isDifferentiateWithoutColorEnabled` when displaying status indicators (e.g., adding text labels or icons alongside color-coded badges).
* **Recommended Improvement:** Execute automated WCAG contrast checks during design and CI/CD pipelines to ensure dynamic theme variations remain compliant.

#### Haptics
* **Requirement:** Provide tactile feedback for key user interactions (such as button selections, state toggles, refresh triggers, and error events) to reinforce visual and auditory feedback loops.
* **Verification Logic:** Scans interactive gestures and button targets for references to `UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator`, `UISelectionFeedbackGenerator`, or `CoreHaptics`.
* **Implementation Standard:**
  * Trigger haptics on user actions: `let generator = UIImpactFeedbackGenerator(style: .medium); generator.impactOccurred()`.
* **Recommended Improvement:** Ensure haptics can be toggled off in user settings for users sensitive to physical device vibrations.

#### Keyboard Navigation
* **Requirement:** Hardware keyboard users (including iPad external keyboards or Bluetooth controllers) must be able to navigate all interactive elements, switch focus sequentially, and activate controls.
* **Verification Logic:** Audits custom focusable components in SwiftUI for proper `@FocusState` tracking and focus indicators.
* **Implementation Standard:**
  * SwiftUI: Bind interactive elements with `.focusable()` and track state using `@FocusState`.
  * UIKit: Implement `UIKeyCommand` handlers and manage `preferredFocusEnvironments`.
* **Recommended Improvement:** Ensure visible focus indicators (focus rings or border highlights) are clearly rendered around the currently focused control during hardware keyboard navigation.

---

### 2. Android Platform Accessibility Requirements

#### TalkBack
* **Requirement:** All interactive controls, image buttons, and informative graphics must have clear `contentDescription` attributes in XML layouts or Jetpack Compose files. Decorative graphics must explicitly hide accessibility.
* **Verification Logic:** Audits Android XML layout files for `<ImageView>` or `<ImageButton>` elements missing `android:contentDescription`, and Jetpack Compose `Image` composables missing `contentDescription`.
* **Implementation Standard:**
  * XML: `android:contentDescription="@string/submit_button_description"` or `android:importantForAccessibility="no"`.
  * Compose: `Image(painter = ..., contentDescription = stringResource(R.string.logo_description))` or `contentDescription = null` for decorative icons.
* **Recommended Improvement:** Utilize `TraversalGroup` or `semantics { traversalIndex = ... }` in Jetpack Compose to explicitly manage logical TalkBack focus order across complex card layouts.

#### Font Scaling
* **Requirement:** All text dimensions must be declared in scale-independent pixels (`sp`) rather than density-independent pixels (`dp`) or fixed physical units, allowing system font scaling up to 200 percent.
* **Verification Logic:** Audits XML `android:textSize` and Compose `fontSize` declarations for usage of `dp` instead of `sp`.
* **Implementation Standard:**
  * XML: `android:textSize="16sp"`.
  * Compose: `Text(text = "Sample", fontSize = 16.sp)`.
* **Recommended Improvement:** Test layouts against Android 14+ non-linear font scaling (which scales smaller text up to 200 percent while preventing already-large text from clipping) to verify text container flexibility.

#### High Contrast
* **Requirement:** Custom view components, backgrounds, and text elements must reference semantic theme attributes (`?attr/colorOnSurface`, `MaterialTheme.colorScheme.primary`) rather than hardcoded hex color codes (`#FF0000`, `Color(0xFF...)`).
* **Verification Logic:** Detects hardcoded hex color strings assigned to XML `android:textColor` or `android:background`, and static `Color(0xFF...)` objects in Jetpack Compose.
* **Implementation Standard:**
  * XML: `android:textColor="?attr/colorOnSurface"`.
  * Compose: `Text(text = "Label", color = MaterialTheme.colorScheme.onBackground)`.
* **Recommended Improvement:** Verify that custom themes correctly adapt when the Android system High Contrast Text setting is enabled in Accessibility Settings.

#### Accessibility Scanner Recommendations
* **Requirement:** Touch target sizes for all interactive elements must meet or exceed the minimum threshold of 48dp x 48dp (with at least 8dp spacing between targets) to ensure ease of tapping.
* **Verification Logic:** Scans XML layout dimensions (`layout_width`, `layout_height`, `minWidth`, `minHeight`) and Compose `Modifier.size(...)` or `clickable` bounds under 48dp.
* **Implementation Standard:**
  * XML: Set `android:minWidth="48dp"` and `android:minHeight="48dp"` on touch targets.
  * Compose: Apply `Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)` or use Material 3 components that automatically enforce 48dp minimum targets.
* **Recommended Improvement:** Run the Google Accessibility Scanner app during manual device QA and continuous integration tests to catch small touch targets or low-contrast text elements before release.

---

## Continuous Audit Execution & Verification

To verify accessibility compliance across the repository at any time, execute the static audit utility:

```bash
python3 scripts/accessibility-audit.py .
```

To run the automated test suite verifying rule detection accuracy:

```bash
bash scripts/accessibility-audit-test.sh
```

---

## References & Authority Sourcing

1. **EN 301 549 / WCAG 2.1 AA Standards:** Harmonised European Standard for ICT accessibility compliance under the European Accessibility Act (Directive EU 2019/882).
2. **Apple Human Interface Guidelines - Accessibility:** Official Apple guidance covering VoiceOver, Dynamic Type, Reduce Motion, and App Store Accessibility Nutrition Labels.
3. **Google Android Accessibility Guidelines:** Official Google Play guidelines covering TalkBack, font scaling, touch targets (48dp x 48dp), and Accessibility Scanner requirements.
4. **App Store & Google Play Rejection Rules:** `data/rejection-patterns.json` (`GOOGLE-PERM-ACCESSIBILITY-MISUSE`, `EU-EAA-ACCESSIBILITY-MISSING`).
