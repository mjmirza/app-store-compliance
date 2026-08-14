# Accessibility Compliance Report

This document reports on the continuous accessibility compliance audit of the repository, evaluating both Apple and Android platform rules. It details the evaluated rules, simulated regressions, continuous verification pipeline, and platform-specific recommendations.

Last updated: 2026-08-12 UTC

## 1. Executive Summary

Accessibility is not just a user experience differentiator; it is a critical regulatory requirement. With the European Accessibility Act (EAA), Directive (EU) 2019/882, coming into force, mobile applications that facilitate commerce, finance, travel, and more must achieve strict compliance with harmonised standard EN 301 549 Chapter 11 (which builds on WCAG 2.1 Level AA). In the United States, ADA Title III digital accessibility litigation similarly anchors WCAG 2.1 Level AA as the de facto standard.

This report establishes the baseline accessibility verification status for our target platforms: Apple (iOS/iPadOS) and Android. Using static code analysis via `scripts/accessibility-audit.py` and regression testing via `scripts/accessibility-audit-test.sh`, we systematically scan source code to identify and mitigate accessibility gaps before submission to the app stores.

## 2. Core Accessibility Mandates and Standards

### 2.1 European Accessibility Act (EAA) and EN 301 549

- **Directive:** Directive (EU) 2019/882.
- **Applicability:** Mandatory for in-scope digital products and services in the European Union.
- **Technical Standard:** EN 301 549 Chapter 11. This standard governs non-web software, including native mobile apps, and establishes roughly 64 specific clauses beyond the core web accessibility guidelines.
- **Legal Risk:** High. Non-compliant apps face substantial fines (up to 100,000 euro under Germany's national implementing legislation) and potential market withdrawal orders.

### 2.2 Americans with Disabilities Act (ADA) Title III

- **Scope:** Public accommodations in the United States.
- **Standard:** WCAG 2.1 Level AA.
- **Legal Risk:** High. Digital accessibility lawsuits continue to increase year-over-year, and maintaining automated checks is a key defense to avoid settlement costs.

## 3. Evaluated Accessibility Rules and Requirements

The compliance scanner evaluates the codebase against ten distinct rules split across Apple and Android platforms.

### 3.1 Apple iOS/iPadOS Rules

#### Rule 1: APPLE-ACCESSIBILITY-VOICEOVER
- **Description:** Screen reader support for VoiceOver. Interactive elements and informational images must be accessible.
- **Checks:**
  - SwiftUI: Images must be initialized with `Image(decorative: ...)` or carry explicit accessibility modifiers (`.accessibilityLabel(...)`, `.accessibilityIdentifier(...)`, `.accessibilityHidden(...)`, `.accessibilityElement(...)`).
  - UIKit: Custom buttons (`UIButton`) or image views (`UIImageView`) must reference accessibility properties (`accessibilityLabel`, `isAccessibilityElement`) in their file declaration.

#### Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE
- **Description:** Text size scaling. Users must be able to scale text using system-level font size preferences.
- **Checks:**
  - SwiftUI: Flags hardcoded fonts defined via `.font(.system(size: ...))`.
  - UIKit: Flags usages of `UIFont.systemFont(ofSize: ...)` where the property `adjustsFontForContentSizeCategory` is not enabled in the same file.

#### Rule 3: APPLE-ACCESSIBILITY-REDUCEMOTION
- **Description:** Accessibility settings for motion and animation must be respected.
- **Checks:**
  - Scans for animations utilizing `withAnimation` (SwiftUI) or `UIView.animate` (UIKit) without checking the system-level reduce motion status (`UIAccessibility.isReduceMotionEnabled` or `@Environment(\.accessibilityReduceMotion)`).

#### Rule 4: APPLE-ACCESSIBILITY-COLORCONTRAST
- **Description:** Adaptive contrast and system settings must be respected.
- **Checks:**
  - Flags hardcoded custom colors (e.g., `UIColor(red:green:blue:alpha:)` or direct RGB values) where high-contrast settings (`UIAccessibility.isDarkerSystemColorsEnabled`) are not referenced or respected.

#### Rule 5: APPLE-ACCESSIBILITY-HAPTICS
- **Description:** Interactive events must provide tactile feedback.
- **Checks:**
  - Flags files containing interactive gestures/controls (`onTapGesture` or `Button`) that do not import or reference any standard iOS tactile generator classes (such as `UIImpactFeedbackGenerator`, `UISelectionFeedbackGenerator`, or `CoreHaptics`).

#### Rule 6: APPLE-ACCESSIBILITY-KEYBOARD
- **Description:** Physical keyboard navigation and focus state tracking.
- **Checks:**
  - Flags components using `focusable()` in SwiftUI without tracking the focus state using `@FocusState` or `focused(_:)` to programmatically control keyboard selection.

---

### 3.2 Android Platform Rules

#### Rule 7: ANDROID-ACCESSIBILITY-TALKBACK
- **Description:** Screen reader support for TalkBack.
- **Checks:**
  - XML Layouts: Screens for `<ImageView>` or `<ImageButton>` declarations missing the `android:contentDescription` attribute.
  - Jetpack Compose: Screens for `Image(...)` function calls missing the `contentDescription` parameter.

#### Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING
- **Description:** Font scaling. Large text must adapt to system preferences.
- **Checks:**
  - XML Layouts: Flags layout elements setting `android:textSize` using density-independent pixels (`dp` or `dip`) instead of scale-independent pixels (`sp`).
  - Jetpack Compose: Flags text size parameters specified with `.dp` units instead of `.sp`.

#### Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST
- **Description:** Theme dynamic adaptive contrast.
- **Checks:**
  - XML Layouts: Flags hardcoded hex colors (e.g., `android:textColor="#FF0000"`) applied directly on views instead of referencing theme-aware resources or attributes (such as `?attr/colorOnSurface`).
  - Jetpack Compose: Flags hardcoded Color values (e.g., `Color(0xFFFF0000)`) instantiated in-place instead of utilizing dynamic material colors from the active theme.

#### Rule 10: ANDROID-ACCESSIBILITY-SCANNER
- **Description:** Touch target dimensions. All interactive views must be large enough to be easily tapped.
- **Checks:**
  - XML Layouts: Flags views with explicit width or height attributes under 48dp on clickable views.
  - Jetpack Compose: Flags Modifier instances with `.size` set under 48.dp (e.g., 40.dp) on interactive controls.

## 4. Simulated Regressions and Test Coverage

To guarantee the reliability of our static analysis tools, we run a simulated regression test suite using `scripts/accessibility-audit-test.sh`. This test runner programmatically generates mock code blocks representing both compliant and non-compliant codebases.

### 4.1 Regression Simulation Mechanics

1. **Clean Baseline Generation:** The script creates a temporary folder populated with compliant source code that properly implements accessibility (e.g., utilizing `Image(decorative: ...)`, `sp` font sizes, `UIImpactFeedbackGenerator`, `@FocusState`, etc.).
2. **Regression Generation:** A separate temporary folder is populated with non-compliant source code containing intentional accessibility violations (such as raw text sizes in dp, missing contentDescriptions, hardcoded UIColors, and animation blocks without reduce motion guards).
3. **Scanner Verification:**
   - On the clean baseline, the runner verifies that `scripts/accessibility-audit.py` returns exactly 0 findings.
   - On the regression folder, the runner verifies that the static scanner successfully flags all 10 platform rules.

This regression pipeline prevents compliance drift. If any scanning logic or regex rules are modified, running this script ensures we do not break detection capability.

## 5. Continuous Accessibility Monitoring Pipeline

We enforce continuous accessibility review through our automated release check pipeline:

1. **Pre-Submission Hook:** Before an app submission command is executed (e.g., Fastlane, EAS, xcodebuild, or Gradle release tasks), the pre-submission guard (`agent-os/hooks/app-store-compliance-guard.sh`) is called. It scans files and lists impending warnings.
2. **Release Auditing:** The script `scripts/release-audit.py` runs validation checks, scans for compliance gaps, and compiles a comprehensive release readiness report before authorization.
3. **Local Audit Execution:** Developers can run the scanner manually on their current directory by executing:
   ```bash
   python3 scripts/accessibility-audit.py .
   ```

## 6. Actionable Platform-Specific Remediation Recommendations

When a regression or violation is flagged by the static scanner, developers must implement the following remediations:

### 6.1 Apple iOS Remediation Examples

#### SwiftUI VoiceOver & Dynamic Type
```swift
import SwiftUI

struct CompliantProductRow: View {
    let productName: String
    let productImageName: String

    var body: some View {
        HStack {
            // Mark decorative assets explicitly
            Image(decorative: "bullet_point")

            // Provide localized accessibility labels on informational images
            Image(productImageName)
                .accessibilityLabel(Text("Photo of \(productName)"))

            // Use relative font styles instead of hardcoded sizes to support Dynamic Type
            Text(productName)
                .font(.body)
        }
    }
}
```

#### UIKit Dynamic Type
```swift
import UIKit

class CompliantDetailsController: UIViewController {
    let titleLabel = UILabel()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    func setupUI() {
        // Use preferred fonts for text styles
        titleLabel.font = UIFont.preferredFont(forTextStyle: .headline)

        // Ensure automatic scaling is turned on
        titleLabel.adjustsFontForContentSizeCategory = true
    }
}
```

#### UIKit / SwiftUI Reduce Motion Guard
```swift
import SwiftUI

struct CompliantAnimationButton: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Button("Tap to Animate") {
            if reduceMotion {
                // Instantly update state without motion for users who prefer reduced movement
                scale = scale == 1.0 ? 1.2 : 1.0
            } else {
                // Apply visual animation only when user has not requested reduced motion
                withAnimation(.spring()) {
                    scale = scale == 1.0 ? 1.2 : 1.0
                }
            }
        }
        .scaleEffect(scale)
    }
}
```

---

### 6.2 Android Remediation Examples

#### XML Layout TalkBack & Text Sizing
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal">

    <!-- Always supply an android:contentDescription for informative images -->
    <ImageView
        android:id="@+id/img_profile"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:contentDescription="@string/desc_profile_picture"
        android:src="@drawable/ic_avatar" />

    <!-- Always specify textSize in sp units -->
    <TextView
        android:id="@+id/txt_username"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textSize="16sp"
        android:textColor="?attr/colorOnSurface" />

</LinearLayout>
```

#### Jetpack Compose TalkBack & Touch Targets
```kotlin
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun CompliantUserIcon(onIconClick: () -> Unit) {
    Box(
        modifier = Modifier
            // Touch targets must be at least 48dp x 48dp
            .size(48.dp)
            .clickable(onClick = onIconClick)
    ) {
        Image(
            painter = painterResource(id = R.drawable.ic_user),
            // Provide explicit descriptive labels or set to null if decorative
            contentDescription = "User profile options"
        )
    }
}
```
