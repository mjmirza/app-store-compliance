# Pre Submission Checklist

Treat every unchecked box as a release blocker. Run this before any upload to App Store Connect or the Play Console. Each item is phrased as a verifiable check.

## Shared (both stores)

### Stability and completeness
- [ ] The app launches and runs without a crash on a real device, on the oldest supported OS and the newest.
- [ ] No placeholder text, lorem ipsum, dummy images, or temporary content anywhere in the build.
- [ ] Every link, button, and navigation path works. No dead ends, no broken URLs.
- [ ] The production backend is live and reachable for the entire review window.
- [ ] A working demo account is provided, or a demo mode exists, for any feature behind login.
- [ ] All in app purchases are live, visible, and complete a real transaction in the review build.

### Privacy and data
- [ ] A privacy policy is published, reachable from inside the app, and accurate.
- [ ] Every data collection has user consent before it happens.
- [ ] Every permission has a specific reason string that names the real feature using it.
- [ ] Account creating apps offer in app account deletion.
- [ ] Users can withdraw consent and the app still works for non core features.
- [ ] Every third party SDK and its data behavior is known and declared.

### Metadata and listing
- [ ] The app name, description, and screenshots match what the app actually does.
- [ ] Screenshots show the app in use, not a splash or login screen.
- [ ] No keyword stuffing in the name, subtitle, or description.
- [ ] The age or content rating questionnaire is answered honestly.
- [ ] No references to the other platform or to alternative marketplaces.

### Monetization
- [ ] Digital goods use the official store billing.
- [ ] Subscription terms, renewal, charges, and cancellation are disclosed before purchase.
- [ ] Loot boxes or random rewards disclose odds before purchase.

## Apple specific

- [ ] Notes for Review explains every non obvious feature and every in app purchase.
- [ ] Privacy nutrition labels match the app's real data collection and the SDKs.
- [ ] App Tracking Transparency prompt is implemented before any cross app tracking.
- [ ] Third party social login is paired with an equal privacy preserving alternative such as Sign in with Apple.
- [ ] No private APIs, no deprecated frameworks, current OS support.
- [ ] No downloaded code that changes app features. Server side changes are data, not code.
- [ ] Background modes declared match what the app actually does.
- [ ] The new age rating questionnaire (13 plus, 16 plus, 18 plus) is answered for every app.
- [ ] Any AI feature that can produce sensitive content has an age restriction.
- [ ] Any personal data shared with a third party AI has a consent modal naming the provider and data types.
- [ ] Regulated category apps are submitted under the legal entity and geo restricted where required.
- [ ] App name is 30 characters or fewer.

## Google Play specific

- [ ] The Data Safety form matches the app's real runtime data behavior, including every SDK. This is the top rejection cause.
- [ ] Every sensitive permission has a qualifying core use case and the required declaration.
- [ ] Background location, all files access, SMS, call log, and AccessibilityService each map to a visible core feature, or are removed.
- [ ] The app targets the current required Android API level.
- [ ] For a new personal developer account, the closed test of at least 12 testers over 14 consecutive days is complete.
- [ ] Play Billing is used for in app digital goods.
- [ ] The IARC content rating questionnaire is complete.
- [ ] The listing makes no claim the app cannot deliver.
- [ ] Apps for children follow the Families policy and use only Families certified ad SDKs.

## The two checks that prevent the most rejections

Two checks stop the majority of rejections across both stores. A working demo account with a live backend, and a privacy declaration that matches actual runtime behavior including SDKs. If you verify nothing else, verify these two.
