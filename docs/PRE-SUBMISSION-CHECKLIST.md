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

## EU specific (legal layer, if the app reaches EU users)

Passing App Review does not make an app EU-legal. The full hard rules and sources are in docs/EU-REGULATORY-2026.md.

- [ ] DSA trader status is declared and verified in App Store Connect. A missing declaration removes the app from the EU App Store (Apple enforced 17 February 2025).
- [ ] Any AI feature reaching EU users shows an in-app notice that the user is interacting with AI, at or before first interaction (EU AI Act Article 50(1), in force 2 August 2026).
- [ ] AI-generated audio, image, video, or text carries a machine-readable and visible AI-generated marking (Article 50(2) and 50(4)).
- [ ] A short AI-literacy record exists for the team building or operating the AI feature (Article 4, live since 2 February 2025).
- [ ] No prohibited AI practice ships (manipulation, banned emotion inference, biometric categorisation) (Article 5, live since 2 February 2025).
- [ ] Personal data shared with a third-party AI has a consent modal naming the provider and data types, shown before data leaves the device (Apple Guideline 5.1.2(i), 13 November 2025).
- [ ] The app meets EN 301 549 and WCAG 2.1 AA and publishes an accessibility statement (European Accessibility Act, in force 28 June 2025). VoiceOver labels, Dynamic Type, contrast, and Reduce Motion are covered.
- [ ] If the app promotes external offers in the EU, the external-purchase entitlement is declared, every external link calls the disclosure sheet, IAP and external offers are not mixed on one storefront, and reporting is wired (DMA).

## Global specific (USA and other markets, if the app reaches those users)

The full hard rules and sources are in docs/GLOBAL-REGULATORY-2026.md. This is legal, on top of App Review. Several dates are under active litigation, so re-verify each against the cited source.

- [ ] Child-directed or under-13 data. COPPA verifiable parental consent, a separate opt-in for ad or third-party disclosure, a written retention policy and a written security program (general compliance date 22 April 2026).
- [ ] US state App Store Accountability Acts (Utah, Texas, Louisiana, Alabama). the app requests an age category from the store, confirms parental consent for a minor, and re-requests on a major change, wired through the Declared Age Range API.
- [ ] Age rating set to 4-plus, 9-plus, 13-plus, 16-plus, or 18-plus, never Unrated, questionnaire re-answered by 31 January 2026.
- [ ] US storefront external links are allowed with no entitlement and no disclosure sheet, no in-app alternative payment, and the commission question is treated as unsettled.
- [ ] California and US state privacy. a privacy policy, notice at collection, know, delete, correct, "Do Not Sell or Share", "Limit Use of Sensitive PI", and honoring Global Privacy Control.
- [ ] Biometric. written consent before capture, a public retention and destruction schedule, and no sale (Illinois BIPA, Texas CUBI).
- [ ] Health app. the HIPAA gate, else the FTC Health Breach Notification Rule with a 60-day breach notice.
- [ ] 18-plus download gating handled for Brazil, Australia, and Singapore for the Apple block of 24 February 2026.
- [ ] UK Online Safety Act Highly Effective Age Assurance and the Children's-Code defaults for a likely-child service.
- [ ] Australia under-16 age assurance for an age-restricted social media platform.
- [ ] South Korea Korea-only binary with an approved payment provider if alternative billing is used.
- [ ] China MIIT app filing with a local entity, plus PIPL and a Banhao license for a game.

## The two checks that prevent the most rejections

Two checks stop the majority of rejections across both stores. A working demo account with a live backend, and a privacy declaration that matches actual runtime behavior including SDKs. If you verify nothing else, verify these two.
