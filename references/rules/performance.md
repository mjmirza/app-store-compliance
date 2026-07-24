# Rules. Performance and completeness

14 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-2.1-MISSING-DEMO-ACCOUNT

- Title. Account based app without demo credentials
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. Login or auth code present (SignInWithApple, OAuth, Auth, login view) but no demo account note found in review metadata or fastlane review_information.
- How to fix it. Add a working demo account and a live test path to the Notes for Review field before submission.
- Detection signals. LoginView, signIn, AuthService, OAuth, Firebase Auth

How to detect.

```bash
grep -rn 'signIn\|LoginView\|OAuth\|FirebaseAuth' --include='*.swift' .   # then confirm a demo account is in the review notes
```

## APPLE-2.1-STAGING-BACKEND

- Title. Backend points at staging or localhost
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. API base URL in the release config contains localhost, 127.0.0.1, staging, dev, or ngrok.
- How to fix it. Point the release build at the live production backend and confirm it stays up during review.
- Detection signals. localhost, 127.0.0.1, staging., dev., ngrok, http://

How to detect.

```bash
grep -rn 'localhost\|127.0.0.1\|staging\.\|ngrok\|http://' --include='*.swift' --include='*.plist' . | grep -v https
```

## APPLE-2.1-CLOUD-NOT-IN-PRODUCTION

- Title. iCloud or CloudKit schema not deployed to production
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. The app uses CloudKit or iCloud but the schema and containers are only in the development environment, so the feature fails for the reviewer on the production build.
- How to fix it. Deploy the CloudKit schema and containers to production before submitting. Source. lukylab checklist.
- Detection signals. CKContainer, CloudKit, NSUbiquitousKeyValueStore, iCloud

How to detect.

```bash
grep -rn 'CKContainer\|CloudKit\|NSUbiquitousKeyValueStore' --include='*.swift' .   # then confirm the CloudKit schema is deployed to production in the CloudKit console
```

## APPLE-2.1-PLACEHOLDER-CONTENT

- Title. Placeholder content in the build
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. Strings such as lorem ipsum, TODO, FIXME, placeholder, dummy, test data, example.com found in shipped resources.
- How to fix it. Replace all placeholder text and assets with real content before submission.
- Detection signals. lorem ipsum, placeholder, TODO, FIXME, dummy, example.com

How to detect.

```bash
grep -rni 'lorem ipsum\|placeholder\|TODO\|FIXME\|example.com' --include='*.swift' --include='*.strings' .
```

## APPLE-2.5.1-PRIVATE-API

- Title. Private API or deprecated framework use
- Platform. apple
- Guideline or policy. 2.5.1
- Severity. high
- What triggers it. References to known private API selectors or deprecated frameworks found in the binary or code.
- How to fix it. Use only documented public APIs and current frameworks.
- Detection signals. respondsToSelector private, UIWebView, performSelector hidden

How to detect.

```bash
grep -rn 'UIWebView\|performSelector\|valueForKey' --include='*.swift' --include='*.m' .   # review any reflection or deprecated framework use
```

## BOTH-SDK-SUPPLY-CHAIN

- Title. Third party SDK violates policy on the developer's behalf
- Platform. both
- Guideline or policy. SDK responsibility
- Severity. high
- What triggers it. A bundled SDK requests permissions, tracks users, or behaves in ways the app does not declare. The developer is responsible for SDK behavior.
- How to fix it. Vet every SDK, keep them current, and remove any that collect or share data the app does not declare.

## APPLE-2.1-DEBUG-FEATURES

- Title. Debug or test features shipped in the production build
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. Debug menus, test logins, or developer backdoors left visible in the release build rather than gated behind a debug only flag.
- How to fix it. Hide debug and test features behind a debug only compile flag so they never ship in production. Source. lukylab checklist.
- Detection signals. debug menu, debugMenu, test login, skip login, bypass auth, DEBUG_BYPASS

How to detect.

```bash
grep -rni 'debug menu\|debugMenu\|skip login\|bypass auth\|DEBUG_BYPASS' --include='*.swift' .
```

## APPLE-2.1-REVIEW-NOTES-INCOMPLETE

- Title. Review notes missing a required section for a new submission
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. New submission review notes omit one of the six sections. Screen recording on a physical device, app purpose, access instructions and test credentials, external services list, regional differences, and regulated industry documentation.
- How to fix it. Fill all six review notes sections using templates/REVIEW-NOTES-TEMPLATE.md. Source. truongduy2611 review_notes rules.

How to detect.

```bash
use templates/REVIEW-NOTES-TEMPLATE.md and fill all six sections
```

## APPLE-A11Y-VOICEOVER-LABELS

- Title. Interactive elements missing VoiceOver accessibility labels or traits
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Interactive visual components (buttons, custom controls, image links) lack accessibilityLabel, accessibilityTraits, or accessibilityHint set in code.
- How to fix it. Ensure every interactive control has a descriptive, non-empty accessibilityLabel, and correct accessibilityTraits (e.g., .isButton).
- Detection signals. UIButton, Image, Button, Label, accessibilityLabel, accessibilityIdentifier, accessibilityTraits
- Present means handled. accessibilityLabel, isAccessibilityElement = true

How to detect.

```bash
grep -rn 'UIButton\|Image\|Button\|Label' --include='*.swift' --include='*.storyboard' --include='*.xib' . && ! grep -rn 'accessibilityLabel' .
```

## APPLE-A11Y-DYNAMIC-TYPE

- Title. Text views missing Dynamic Type or font scaling support
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Hardcoded font sizes (UIFont.systemFont(ofSize:)) used without dynamically scaled fonts (UIFontMetrics) or adjustsFontForContentSizeCategory = true in Swift or custom SwiftUI views.
- How to fix it. Use preferredFont(forTextStyle:) or UIFontMetrics to scale custom fonts, and enable adjustsFontForContentSizeCategory = true.
- Detection signals. systemFont(ofSize:, font:, adjustsFontForContentSizeCategory
- Present means handled. adjustsFontForContentSizeCategory = true, UIFontMetrics, DynamicType, Font.custom, UIFont.preferredFont

How to detect.

```bash
grep -rn 'systemFont(ofSize:' --include='*.swift' . && ! grep -rn 'adjustsFontForContentSizeCategory\|preferredFont' .
```

## APPLE-A11Y-REDUCE-MOTION

- Title. Animations ignore UIAccessibility.isReduceMotionEnabled setting
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Custom layout transitions or intensive animations are run without checking if UIAccessibility.isReduceMotionEnabled is true.
- How to fix it. Wrap intensive animations or transitions in a conditional check for UIAccessibility.isReduceMotionEnabled and provide a cross-dissolve fallback.
- Detection signals. UIView.animate, withAnimation, CABasicAnimation, CAKeyframeAnimation
- Present means handled. isReduceMotionEnabled, accessibilityReduceMotion, Reduce Motion

How to detect.

```bash
grep -rn 'UIView.animate\|withAnimation\|CABasicAnimation' --include='*.swift' . && ! grep -rn 'isReduceMotionEnabled\|accessibilityReduceMotion' .
```

## APPLE-A11Y-COLOR-CONTRAST

- Title. Hardcoded or low-contrast text colors
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Text elements using fixed custom low-contrast foreground colors that do not adapt to system Dark Mode or respect color contrast guidelines.
- How to fix it. Use system dynamic semantic colors (e.g., labelColor, secondaryLabelColor) and verify against WCAG 2.1 AA contrast ratio (4.5:1 for normal text).
- Detection signals. UIColor(red:, Color(red:, UIColor.lightGray, UIColor.gray
- Present means handled. preferredContentSizeCategory, colorScheme, labelColor, systemBackground

How to detect.

```bash
grep -rn 'UIColor(red:\|Color(red:\|lightGray' --include='*.swift' .
```

## APPLE-A11Y-HAPTICS

- Title. No audio/visual fallback for critical haptic feedback
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Using UIImpactFeedbackGenerator, UINotificationFeedbackGenerator, or CHHapticEngine for critical system alerts without an accompanying visual or auditory modal or fallback.
- How to fix it. Provide standard accessibility notifications (UIAccessibility.post(notification:argument:)) or alert popups as fallbacks for haptic-only alerts.
- Detection signals. UIImpactFeedbackGenerator, UINotificationFeedbackGenerator, CHHapticEngine, haptic
- Present means handled. alert, sound, UIAccessibility.post

How to detect.

```bash
grep -rn 'UIImpactFeedbackGenerator\|UINotificationFeedbackGenerator' --include='*.swift' .
```

## APPLE-A11Y-KEYBOARD-NAV

- Title. Interactive views missing keyboard or switch navigation focus
- Platform. apple
- Guideline or policy. Design (Accessibility)
- Severity. medium
- What triggers it. Custom gestures or non-standard interactive UI controls are not focusable via external keyboard or Switch Control.
- How to fix it. Ensure custom interactive views set isAccessibilityElement = true, override canBecomeFocused, or respond to keyCommands.
- Detection signals. addGestureRecognizer, UITapGestureRecognizer
- Present means handled. keyCommands, accessibilityElements, canBecomeFocused

How to detect.

```bash
grep -rn 'addGestureRecognizer\|UITapGestureRecognizer' --include='*.swift' .
```
