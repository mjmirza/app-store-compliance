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

## APPLE-ACCESSIBILITY-VOICEOVER

- Title. VoiceOver support missing or incomplete
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Interactive views or images without accessibilityLabel, accessibilityIdentifier, isAccessibilityElement, or accessibilityElement(children:) properties.
- How to fix it. Ensure all interactive components and decorative or informative images have correct accessibility labels, hints, and traits assigned.
- Detection signals. UIAccessibility, accessibilityLabel, accessibilityIdentifier, isAccessibilityElement

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-VOICEOVER
```

## APPLE-ACCESSIBILITY-DYNAMICTYPE

- Title. Dynamic Type support missing or overridden
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Hardcoded font sizes or styles used without matching scaling or preferredFont APIs, or adjustsFontForContentSizeCategory set to false.
- How to fix it. Use preferredFont(forTextStyle:) in UIKit and system/relative font styles in SwiftUI, ensuring adjustsFontForContentSizeCategory is enabled.
- Detection signals. UIFont.systemFont, preferredFont, adjustsFontForContentSizeCategory

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-DYNAMICTYPE
```

## APPLE-ACCESSIBILITY-REDUCEMOTION

- Title. Reduce Motion accessibility setting ignored
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Custom animations or transitions without checks for UIAccessibility.isReduceMotionEnabled or environment accessibilityReduceMotion.
- How to fix it. Check the Reduce Motion system status and disable or simplify non-essential animations when requested by the user.
- Detection signals. isReduceMotionEnabled, accessibilityReduceMotion

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-REDUCEMOTION
```

## APPLE-ACCESSIBILITY-COLORCONTRAST

- Title. Color Contrast and system settings ignored
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Hardcoded custom colors used without supporting dark/light mode, high-contrast settings, or checking isDarkerSystemColorsEnabled.
- How to fix it. Use dynamic or system colors that automatically adapt, or monitor isDarkerSystemColorsEnabled to adjust contrast dynamically.
- Detection signals. isDarkerSystemColorsEnabled, darkerSystemColors

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-COLORCONTRAST
```

## APPLE-ACCESSIBILITY-HAPTICS

- Title. Haptics tactile feedback missing on interactions
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Interactive elements, buttons, or custom controls lacking feedback generators or CoreHaptics calls.
- How to fix it. Add haptic feedback to buttons, toggles, and swipe actions using UIImpactFeedbackGenerator or selection feedback.
- Detection signals. UIImpactFeedbackGenerator, UINotificationFeedbackGenerator, UISelectionFeedbackGenerator, CHHapticEngine

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-HAPTICS
```

## APPLE-ACCESSIBILITY-KEYBOARD

- Title. Keyboard navigation and focus state support missing
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Custom text editors or complex navigation flows missing keyCommands, focusState, or focusable modifiers.
- How to fix it. Support physical keyboard navigation by utilizing keyCommands in UIKit or focusable() and @FocusState in SwiftUI.
- Detection signals. keyCommands, UIKeyCommand, FocusState, focusable

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-KEYBOARD
```
