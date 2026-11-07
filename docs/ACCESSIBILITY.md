# Accessibility for App Store and Google Play apps

Neither store rejects an app today for missing VoiceOver or TalkBack support, so accessibility is mostly a legal and quality duty rather than a review gate. The binding pressure comes from the law (the European Accessibility Act in the EU, the DOJ ADA Title II rule for US public entities, the Equality Act in the UK) and from what each store asks you to declare or shows you in its own test reports. This document covers the store-side declarations and checks, the per-platform implementation bar, the legal layer outside the EU, how to run the repo's static accessibility scan, and, in section 12, the accessibility of this repository itself.

Every item below was checked against a primary source on 7 November 2026. Anything that could not be confirmed is listed in section 11 and was left out of the body.

## 1. The EU layer in one table

The European Accessibility Act (Directive (EU) 2019/882) is covered in full in [section 4 of the EU regulatory document](EU-REGULATORY-2026.md#4-european-accessibility-act-eaa-directive-eu-2019882-hard-new-gap). The duties in short.

| Duty | What it means for an app | Where it is set |
|---|---|---|
| Applicability | In force for in-scope consumer services since 28 June 2025, including e-commerce, banking, e-books, transport booking, telecom, and audiovisual media access, delivered through websites and mobile apps | EU doc section 4.1 |
| Microenterprise exemption | Fewer than 10 employees and turnover or balance sheet not over 2,000,000 euro, services only (Article 4(5)) | EU doc section 4.2 |
| Technical bar | Harmonised standard EN 301 549 (V3.2.1 builds on WCAG 2.1 AA and adds Chapter 11 for non-web software). A WCAG-only audit does not cover Chapter 11 | EU doc section 4.3 |
| Accessibility information | Annex V information on how the service meets the Annex I requirements, published in the terms and conditions or an equivalent document (Article 13(2)) | EU doc section 4.3 |
| Penalties | Set per Member State. Germany up to 100,000 euro plus corrective measures or withdrawal | EU doc section 4.4 |

## 2. Apple Accessibility Nutrition Labels

Accessibility Nutrition Labels are a per-app declaration in App Store Connect that appears on the product page. Apple describes them this way. "The Accessibility Nutrition Labels help users learn if an app will be accessible to them before they download, and give developers the opportunity to better inform and educate their users on features that their app supports."

### 2.1 The nine features you can declare

| Feature | Platform note from Apple |
|---|---|
| VoiceOver | |
| Voice Control | Not supported on Apple TV and Apple Watch |
| Larger Text | Not supported on Mac |
| Dark Interface | |
| Differentiate Without Color Alone | |
| Sufficient Contrast | |
| Reduced Motion | |
| Captions | |
| Audio Descriptions | |

The labels appear on devices running iOS 26, iPadOS 26, macOS 26, tvOS 26, visionOS 26, and watchOS 26 or later. You answer per device your app supports.

### 2.2 Optional now, required later, no date

Apple states. "providing these labels will be voluntary to start." and "You'll be given ample time and evaluation resources before this is mandatory, but over time, you'll be required to share accessibility support details to submit new apps and app updates to the App Store." Apple publishes no date for the switch. Do not quote one.

### 2.3 The bar for claiming a feature

A feature may only be declared when it works across the whole app. Apple's text. "To indicate support for an accessibility feature in the Accessibility Nutrition Labels, users must be able to complete all of the common tasks of your app using that feature." Apple defines common tasks as the primary functionality users are expected to perform in the app, plus the functionality fundamental to using any app, namely the first launch experience, login, purchase, and settings. If known bugs would change the answer under these criteria, Apple says not to indicate support.

Treat an over-claim as a metadata accuracy problem. A declared feature that fails on the login or purchase screen is a false statement on your product page.

### 2.4 How to publish

- Role. Account Holder, Admin, Finance, App Manager, or Marketing.
- Path. Apps, select the app, App Accessibility in the sidebar, Get Started, add support per device, select the features, save as draft, then Publish.
- You can only publish support for devices that have a live version on the App Store.
- Published responses go live immediately and can take up to 24 hours to be visible to all users. Apple's help page does not say that publishing passes through App Review.
- An optional accessibility URL on the product page can carry more detail, such as in-app accessibility settings, caption languages, or areas of the app that do not support a feature.

Sources. [Overview of Accessibility Nutrition Labels](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/), [Manage Accessibility Nutrition Labels](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/manage-accessibility-nutrition-labels/).

## 3. Apple App Review Guidelines and accessibility

The current App Review Guidelines contain no guideline that requires an app to support VoiceOver, Dynamic Type, or any other assistive feature. The full text was searched for accessibility, accessible, VoiceOver, assistive, and disability. The only use of the word in the sense of disability is in Guideline 3.2.1(ii), which lists accessibility as an approved need for an app that collects third-party apps. "Displaying or recommending a collection of third-party apps that are designed for a specific approved need (such as health management, aviation, accessibility)."

The other hits use "accessible" to mean reachable, not usable by people with disabilities. Guideline 2.3.1(a) requires new features to be "accessible for review", and Guideline 5.1.1(i) requires the privacy policy link "within the app in an easily accessible manner".

So accessibility does not reach App Review as a feature requirement. It reaches the store through the Nutrition Labels in section 2 and through the law in sections 6 and 7.

Source. [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).

## 4. iOS and iPadOS implementation checklist

Figures and wording in this section come from the Apple Human Interface Guidelines accessibility page. API names were checked against Apple's documentation index.

| Area | What to do | APIs and figures |
|---|---|---|
| VoiceOver labels | Give every interactive element and every informative image a label that names its purpose. Mark decorative images so VoiceOver skips them | `accessibilityLabel`, `accessibilityHint`, `accessibilityTraits` (UIKit), `.accessibilityLabel(_:)`, `.accessibilityHint(_:)`, `.accessibilityAddTraits(_:)`, `.accessibilityHidden(_:)`, `Image(decorative:)` (SwiftUI) |
| Voice Control | Label elements so a spoken command can target them. Provide alternative names where the visible label is long or ambiguous | `accessibilityUserInputLabels` (UIKit), `.accessibilityInputLabels(_:)` (SwiftUI) |
| Larger Text | HIG asks you to let people enlarge text "by at least 200 percent (or 140 percent in watchOS apps)". Default and minimum system sizes on iOS and iPadOS are 17 pt and 11 pt | `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory`, SwiftUI text styles such as `.body` |
| Contrast | HIG minimum ratios. text up to 17 pt at 4.5 to 1, text 18 pt and up at 3 to 1, bold text at 3 to 1. If the default scheme falls short, provide a higher contrast scheme when Increase Contrast is on, and check both light and dark appearances | `UIAccessibility.isDarkerSystemColorsEnabled`, system and asset catalog colors |
| Color alone | Do not carry meaning by color only | `accessibilityDifferentiateWithoutColor` (SwiftUI environment) |
| Reduce Motion | When the setting is on, reduce "automatic and repetitive animations, including zooming, scaling, and peripheral motion". HIG suggests fades in place of x, y, and z transitions | `UIAccessibility.isReduceMotionEnabled`, `accessibilityReduceMotion` (SwiftUI environment) |
| Hit targets | HIG table for iOS and iPadOS. default control size 44x44 pt, minimum 28x28 pt. Add about 12 points of padding around bezeled elements and about 24 points around elements without a bezel | Layout constraints, `contentShape` |
| Captions and audio descriptions | Do not deliver dialogue or important information through audio alone. Offer captions, subtitles, and audio descriptions | AVFoundation media selection, `AVMediaCharacteristic.describesVideoForAccessibility` |

The 44x44 pt figure is the HIG default control size, and 28x28 pt is the HIG minimum. Plan for 44x44 pt on touch targets. WCAG 2.2 Success Criterion 2.5.8 Target Size (Minimum) sets 24 by 24 CSS pixels at Level AA, and WCAG 2.1 Success Criterion 2.5.5 Target Size sets 44 by 44 CSS pixels at Level AAA.

Test each declared feature end to end with the real assistive technology (VoiceOver, Voice Control, Larger Text at the largest sizes) through the first launch, login, purchase, and settings flows, since those are the common tasks Apple's label criteria name.

Sources. [Apple HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [WCAG 2.2 Understanding SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [WCAG 2.1 Understanding SC 2.5.5](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html).

## 5. Android and Google Play

### 5.1 Implementation

| Area | What Android's documentation says |
|---|---|
| Content labels | Describe each UI element's purpose, usually in `contentDescription`. Do not add a description to `Text` composables or `TextView`, since TalkBack reads the text. Do not include the element type ("Submit", not "Submit button"). Each description should be unique, including items in a list |
| Decorative elements | Compose. pass `null` as `contentDescription` for a purely decorative element, or use `hideFromAccessibility`. Views. set `android:importantForAccessibility="no"` (minSdkVersion 16 or higher) |
| Touch targets | At least 48dp x 48dp. In Views, `paddingLeft` plus `minWidth` plus `paddingRight` must reach 48dp, and the same for height, so the visible size can be smaller than the touch target. Many built-in Compose components such as `Button`, `IconButton`, and `ListItem` already enforce the minimum |
| Text size | The `sp` unit "is also scaled by the user's font size preference. It is recommend you use this unit when specifying font sizes" |
| Contrast | At least 4.5 to 1 for text smaller than 18sp, or bold text smaller than 14sp. At least 3 to 1 for all other text |

### 5.2 Testing tools

- TalkBack, the built-in screen reader. Swipe through each element and check that every element is reachable, that announcements convey purpose, and that the main workflows complete.
- Switch Access and Voice Access, for motor and voice input.
- Compose UI Check mode in Android Studio, which flags issues such as low color contrast in the problems panel.
- Accessibility Scanner, which uses the Accessibility Test Framework and checks content labels, clickable items, contrast, and more. Android notes that the framework in Android Studio cannot detect issues that only occur on a device.
- Compose testing APIs, which read the same semantics tree that accessibility services use.

### 5.3 Play pre-launch report

When you upload to a release track, Google Play runs accessibility tests with the Accessibility Test Framework and lists the results on the Accessibility tab of the pre-launch report. The categories are Touch target size, Low contrast, Content labeling, and Implementation (for example a traversal order that does not match the logical layout). The report also gives a launch recommendation. Neither page fetched states that accessibility findings block publishing, so treat them as findings to fix, not as a gate.

### 5.4 AccessibilityService policy

This is the one accessibility area where Google Play enforces policy. The rules, from the Play policy page "Use of the AccessibilityService API".

- Only services designed to help people with disabilities access their device may declare `isAccessibilityTool`. Supporting people with disabilities must be the primary purpose. Examples include screen readers, switch-based and voice-based input systems, and braille-based access systems.
- Apps that are not accessibility tools, such as antivirus software, automation tools, assistants, monitoring apps, cleaners, password managers, and launchers, may still use the API but must meet the prominent disclosure and consent requirements.
- The disclosure must be inside the app, not only in the store description, on a website, or in a privacy policy or terms of service. It must be a separate disclosure explaining why the app needs the API, and consent needs an affirmative user action such as a tap to accept or a ticked check box.
- Any use of the Accessibility API that enables an app to "autonomously initiate, plan, and execute actions or decisions is strictly prohibited". Deterministic, rule-based automation that follows a static, human-defined script is not prohibited. Verified accessibility tools are exempt when the function serves the core accessibility purpose. The page gives no effective date for this clause.
- Since 3 November 2021, apps targeting API level 31 that include an AccessibilityService must complete a declaration in Play Console. Accessibility tools describe a core feature, the disability types served, and the target users. Other apps explain why they need the API and whether they collect or share personal or sensitive data. Both provide a video showing the disclosure flow, the consent and non-consent paths, and a core feature. The `AccessibilityService_description` text does not replace the in-app disclosure.
- Changes to how the app uses the API require resubmitting the declaration. Deceptive or undeclared use can lead to suspension or account termination.

Sources. [Make apps more accessible](https://developer.android.com/guide/topics/ui/accessibility/apps), [Make apps more accessible (Views)](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views), [Dimension resources](https://developer.android.com/guide/topics/resources/more-resources), [Test your app's accessibility](https://developer.android.com/guide/topics/ui/accessibility/testing), [Pre-launch report](https://support.google.com/googleplay/android-developer/answer/9842757), [Use of the AccessibilityService API](https://support.google.com/googleplay/android-developer/answer/10964491).

## 6. United States

### 6.1 ADA Title II, state and local government apps (rule in force, dates extended)

The DOJ rule at 28 CFR Part 35 Subpart H requires web content and mobile apps that a state or local government "provides or makes available" to meet WCAG 2.1 Level AA. A commercial developer is reached when it builds or licenses an app for a public entity.

The compliance dates were extended by an interim final rule published in the Federal Register on 20 April 2026 (FR Doc. 2026-07663), effective the same day, with comments closing 22 June 2026.

| Public entity | Original date (2024 rule) | Current date |
|---|---|---|
| Total population 50,000 or more | 24 April 2026 | 26 April 2027 |
| Total population under 50,000, and every special district government | 26 April 2027 | 26 April 2028 |

The interim final rule states that it leaves the requirements of the 2024 final rule unchanged. Only the dates moved, and WCAG 2.1 Level AA is still the standard. Whether a final rule has since replaced the interim rule was not checked here, so re-verify the dates against the Federal Register before quoting them to a client.

### 6.2 ADA Title III, businesses open to the public (no technical regulation)

Title III applies to businesses open to the public, and DOJ states that "the ADA's requirements apply to all the goods, services, privileges, or activities offered by public accommodations", including those offered on the web. DOJ also states that it "does not have a regulation setting out detailed standards" and that businesses "have flexibility in how they comply". DOJ points to WCAG and the Section 508 Standards as helpful references. In practice the exposure for a consumer app comes through litigation, not a fixed technical rule. Treat WCAG 2.1 AA as the working target. No case law is summarised here because none was verified in this pass.

### 6.3 Section 508, federal agencies

Section 508 "applies to all federal agencies when they develop, procure, maintain, or use electronic and information technology." The Revised 508 Standards incorporate WCAG 2.0 Level A and Level AA by reference and apply them to software (E207.2), with listed exceptions for non-web software such as Success Criteria 2.4.1, 2.4.5, 3.2.3, and 3.2.4. An app sold to or built for a federal agency is in scope.

Sources. [ADA.gov web rule fact sheet](https://www.ada.gov/resources/2024-03-08-web-rule/), [Interim final rule, FR Doc. 2026-07663](https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07663.htm), [ADA.gov guidance on web accessibility](https://www.ada.gov/resources/web-guidance/), [Section508.gov laws and policies](https://www.section508.gov/manage/laws-and-policies/), [US Access Board ICT standards](https://www.access-board.gov/ict/).

## 7. United Kingdom and Canada

**United Kingdom.** The Equality Act 2010 section 29 applies to "A person (a "service-provider") concerned with the provision of a service to the public", who "must not discriminate against a person requiring the service by not providing the person with the service." Section 29(7) applies "A duty to make reasonable adjustments" to a service provider. The Act names no technical standard, so for an app serving the UK public WCAG 2.1 AA is the usual measure of a reasonable adjustment, not a statutory one.

**Canada.** The Accessible Canada Act (long title "An Act to ensure a barrier-free Canada") aims at "a Canada without barriers, on or before January 1, 2040." Section 7 applies it to federal bodies and to entities operating works within federal legislative authority, for example banks, telecom, and interprovincial transport. A general consumer app outside that scope is not covered by this Act. Provincial laws were not reviewed here.

Sources. [Equality Act 2010 section 29](https://www.legislation.gov.uk/ukpga/2010/15/section/29), [Accessible Canada Act](https://laws-lois.justice.gc.ca/eng/acts/a-0.6/page-1.html).

## 8. The repo's static accessibility scan

`scripts/accessibility-audit.py` is a static scan of source files. It does not build or run the app, computes no contrast ratio, and cannot see focus order or runtime behaviour. A clean result means none of its patterns matched, not that the app is accessible. Test with VoiceOver, TalkBack, Accessibility Inspector, and Accessibility Scanner as well.

### 8.1 How to run it

```bash
python3 scripts/accessibility-audit.py /path/to/your/app
python3 scripts/accessibility-audit.py /path/to/your/app --rule ANDROID-ACCESSIBILITY-SCANNER
bash scripts/accessibility-audit-test.sh
```

The directory defaults to the current directory. `--rule` runs one rule. The test script runs the fixture suite (51 cases at the time of writing), which CI also runs.

Behaviour worth knowing.

- It always exits 0 when it finds issues, since the findings are advisory. It exits 2 only for an unknown `--rule` value. A missing directory prints a message and exits 0, so do not rely on the exit code as a gate.
- It skips `node_modules`, `Pods`, `.git`, `build`, `DerivedData`, `vendor`, `.dart_tool`, `Carthage`, `androidTest`, `__tests__`, and any folder whose name ends in `Tests`.
- iOS files are `.swift`, `.m`, `.h`, `.plist`, `.storyboard`, and `.xib`. Android files are `.kt`, `.java`, and `.xml`. Only some rules read each type, as listed below. No rule reads `.java`, `.plist`, `.storyboard`, or `.xib` today.
- Output lists each finding with severity, rule ID, file and line, the matched text, a reason, and a fix, then a summary count by severity.

### 8.2 What each rule actually matches

| Rule ID | Severity | Files read | What triggers a finding |
|---|---|---|---|
| APPLE-ACCESSIBILITY-VOICEOVER | medium | `.swift` | A SwiftUI `Image(...)` that is not `decorative:` or `systemName:` and has no `accessibilityLabel`, `accessibilityIdentifier`, `accessibilityHidden`, or `accessibilityElement` in the next 300 characters of code. A possible icon-only `Button` whose label holds an `Image(systemName:)` with no `Text`, `Label`, or `accessibilityLabel`. A file that mentions `UIButton` or `UIImageView` but never `accessibilityLabel`, `accessibilityIdentifier`, or `isAccessibilityElement` (reported at line 1). Comments and string contents are excluded for the SwiftUI checks |
| APPLE-ACCESSIBILITY-DYNAMICTYPE | medium | `.swift`, `.m`, `.h` | Every `.system(size: N` font. Every `UIFont.systemFont(ofSize: N` in a file that never sets `adjustsFontForContentSizeCategory` |
| APPLE-ACCESSIBILITY-REDUCEMOTION | medium | `.swift`, `.m` | A file that uses `withAnimation` or `UIView.animate` and never reads `isReduceMotionEnabled` or `accessibilityReduceMotion` (one finding per file, line 1) |
| APPLE-ACCESSIBILITY-COLORCONTRAST | medium | `.swift`, `.m` | A `UIColor(red:` with a numeric value in a file that never references `isDarkerSystemColorsEnabled` or `darkerSystemColors`. It does not measure contrast |
| APPLE-ACCESSIBILITY-HAPTICS | low | `.swift` | `.onTapGesture` or a `Button` in a file with no `FeedbackGenerator`, `CoreHaptics`, or `CHHapticEngine`. Advisory only, the rule title notes haptics are not required by WCAG 2.2 or EN 301 549 |
| APPLE-ACCESSIBILITY-KEYBOARD | medium | `.swift` | A file containing `focusable` but neither `FocusState` nor `focused` |
| ANDROID-ACCESSIBILITY-TALKBACK | medium | `.xml`, `.kt` | An `<ImageView` or `<ImageButton` opening tag without `contentDescription`. A Compose `Image(...)` whose arguments lack `contentDescription` |
| ANDROID-ACCESSIBILITY-FONTSCALING | medium | `.xml`, `.kt` | `android:textSize` in `dp`. Compose `fontSize = N.dp` |
| ANDROID-ACCESSIBILITY-HIGHCONTRAST | medium | `.xml`, `.kt` | A hardcoded hex `android:textColor` or `android:background`. A Compose `Color(0xFF......)` literal |
| ANDROID-ACCESSIBILITY-SCANNER | medium | `.xml`, `.kt` | `layout_width`, `layout_height`, `minWidth`, or `minHeight` between 1dp and 47dp, skipped for the whole file if it contains any `wrap_content` width or height. A Compose `.size(N.dp)` below 48 |

Known gaps, read from the code.

- The XML TalkBack check looks only for `contentDescription`. A decorative `ImageView` correctly marked `android:importantForAccessibility="no"` is still reported.
- The touch target check reads each dimension alone and ignores padding, while Android counts padding toward the 48dp target (section 5.1). A 40dp `minWidth` with 4dp padding each side is reported even though it meets the Android recommendation. It also does not check whether the element is clickable.
- Several Apple rules are file level. One reference to the right API anywhere in a file clears every use in that file.
- The README lists further limits of the Button label heuristic and regex literal handling.

## 9. What reviewers and regulators actually check

| Who | What they check | Consequence |
|---|---|---|
| Apple App Review | No accessibility feature requirement in the guidelines. Nutrition Labels are voluntary today | None from review alone. A false label is a metadata accuracy problem |
| App Store product page | Your Accessibility Nutrition Labels, against the common-tasks criteria | Users see the claim. Over-claiming is a false statement on your listing |
| Google Play pre-launch report | Touch target size, low contrast, content labeling, implementation | Findings and a launch recommendation. No published statement that they block release |
| Google Play policy | AccessibilityService use, `isAccessibilityTool` eligibility, in-app disclosure and consent, the Play Console declaration, no autonomous actions | Rejection, suspension, or account termination for deceptive or undeclared use |
| EU market surveillance | EN 301 549 conformance and Annex V information for in-scope services | Fines per Member State, corrective measures, withdrawal |
| US DOJ (Title II) | WCAG 2.1 AA for apps a state or local government provides | Enforcement against the public entity, passed to the vendor through contract |
| US courts (Title III) | Whether the app gives full and equal enjoyment of the service | Litigation, no fixed technical rule |
| US federal procurement (Section 508) | WCAG 2.0 A and AA for ICT an agency uses | Procurement requirement |

## 10. Pre-ship checklist

- [ ] Every interactive element and informative image has a VoiceOver label and the right traits. Decorative images are hidden from VoiceOver.
- [ ] Every Android interactive element has a unique, purpose-based `contentDescription`, and decorative elements are excluded.
- [ ] Text scales with Larger Text and Dynamic Type on iOS (HIG asks for at least 200 percent) and uses `sp` on Android, and layouts hold at the largest sizes.
- [ ] Text contrast meets 4.5 to 1 (3 to 1 for large text) in light and dark appearances, and meaning never depends on color alone.
- [ ] Reduce Motion is honored and non-essential animation is reduced or replaced with fades.
- [ ] Touch targets are 44x44 pt on iOS and at least 48dp x 48dp on Android, padding included.
- [ ] Video and audio content has captions, and audio descriptions where visuals carry meaning.
- [ ] VoiceOver, Voice Control, and TalkBack complete first launch, login, purchase, and settings.
- [ ] Accessibility Nutrition Labels declare only features that pass the common-tasks bar, per device.
- [ ] The Play pre-launch report Accessibility tab was reviewed and its findings fixed or justified.
- [ ] Any AccessibilityService use has a correct `isAccessibilityTool` value, an in-app disclosure with affirmative consent where required, a current Play Console declaration, and no autonomous action.
- [ ] For EU in-scope services, the EN 301 549 and Annex V items in the [EU regulatory document](EU-REGULATORY-2026.md) are met.
- [ ] For apps built for a US state or local government, WCAG 2.1 AA conformance is planned against the current Title II date.
- [ ] `python3 scripts/accessibility-audit.py` was run and each finding fixed or recorded as a false positive.

## 11. Unverified and left out

- The date Apple Accessibility Nutrition Labels become mandatory. Apple publishes none.
- Whether App Review contacts developers about misleading Nutrition Labels, and under which guideline. Neither Apple help page fetched says so, so it is not stated above.
- Whether Play pre-launch report accessibility findings affect the launch recommendation or block release.
- The effective date of the Play clause banning autonomous actions through the Accessibility API.
- Whether a final ADA Title II rule has replaced the April 2026 interim final rule.
- ADA Title III case law and lawsuit volumes.
- UK public sector accessibility regulations and Canadian provincial laws.

## 12. Accessibility of this repository

GitHub reads an `ACCESSIBILITY.md` file from `.github`, the repository root, or `docs`, in that order, and shows it as an Accessibility tab on the repository. GitHub describes the file as a place for a project's "accessibility priorities, supported environments, known barriers", and the reporting process. This section is that page for this repository.

**What is published.** Markdown documents, a GitHub Pages site built from `docs/` with the Jekyll Primer theme, and command-line scripts in Python and Bash that print plain text.

**Priorities.** Every document reads in order as plain Markdown, with real headings, text links, and tables with header rows. Script output is line-based text with no color codes needed to understand a result.

**Known barriers.**

- Several documents use wide tables, which are slow to read with a screen reader and scroll sideways on a narrow screen.
- The Pages site and the script output have not been tested with VoiceOver, NVDA, or JAWS, and no WCAG conformance claim is made for either.

**Reporting a barrier.** Open an issue on [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance/issues). For a script, use the guard or monitor bug template and include the command and its output. Name the assistive technology you use if you are comfortable doing so.

Sources. [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [Adding an accessibility page to your repository](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-an-accessibility-page-to-your-repository).

## Sources

| Source | URL | Checked |
|---|---|---|
| Apple, Overview of Accessibility Nutrition Labels | https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/ | 2026-11-07 |
| Apple, Manage Accessibility Nutrition Labels | https://developer.apple.com/help/app-store-connect/manage-app-accessibility/manage-accessibility-nutrition-labels/ | 2026-11-07 |
| Apple, App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ | 2026-11-07 |
| Apple, Human Interface Guidelines, Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility | 2026-11-07 |
| Apple Developer Documentation (API names in section 4) | https://developer.apple.com/documentation/ | 2026-11-07 |
| W3C, Understanding SC 2.5.8 Target Size (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 2026-11-07 |
| W3C, Understanding SC 2.5.5 Target Size | https://www.w3.org/WAI/WCAG21/Understanding/target-size.html | 2026-11-07 |
| Android, Make apps more accessible | https://developer.android.com/guide/topics/ui/accessibility/apps | 2026-11-07 |
| Android, Make apps more accessible (Views) | https://developer.android.com/guide/topics/ui/accessibility/views/apps-views | 2026-11-07 |
| Android, Dimension resources | https://developer.android.com/guide/topics/resources/more-resources | 2026-11-07 |
| Android, Test your app's accessibility | https://developer.android.com/guide/topics/ui/accessibility/testing | 2026-11-07 |
| Google Play, Pre-launch report | https://support.google.com/googleplay/android-developer/answer/9842757 | 2026-11-07 |
| Google Play, Use of the AccessibilityService API | https://support.google.com/googleplay/android-developer/answer/10964491 | 2026-11-07 |
| ADA.gov, Title II web rule fact sheet | https://www.ada.gov/resources/2024-03-08-web-rule/ | 2026-11-07 |
| Federal Register, FR Doc. 2026-07663 (govinfo) | https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07663.htm | 2026-11-07 |
| ADA.gov, Guidance on web accessibility and the ADA | https://www.ada.gov/resources/web-guidance/ | 2026-11-07 |
| Section508.gov, Laws and policies | https://www.section508.gov/manage/laws-and-policies/ | 2026-11-07 |
| US Access Board, ICT standards and guidelines | https://www.access-board.gov/ict/ | 2026-11-07 |
| legislation.gov.uk, Equality Act 2010 section 29 | https://www.legislation.gov.uk/ukpga/2010/15/section/29 | 2026-11-07 |
| Justice Laws, Accessible Canada Act | https://laws-lois.justice.gc.ca/eng/acts/a-0.6/page-1.html | 2026-11-07 |
| GitHub Docs, Creating a default community health file | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file | 2026-11-07 |
| GitHub Docs, Adding an accessibility page to your repository | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-an-accessibility-page-to-your-repository | 2026-11-07 |
