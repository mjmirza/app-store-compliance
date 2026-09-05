# Google Play Developer Program Policies. Rejection Map

Source. Google Play Developer Program Policy (play.google/developer-content-policy) and Play Console enforcement documentation (support.google.com/googleplay/android-developer). Empirical figures from Google's 2025 platform safety reporting.

Google blocked more than 1.75 million Play submissions in 2025 for policy violations and stopped over 255,000 apps from gaining excessive access to sensitive user data. The single most common rejection cause is a Data Safety declaration that does not match the app's real runtime behavior.

A critical difference from Apple. Google enforcement escalates against the developer account, not only the app. A rejection is mild, but repeated rejections, removals, or one egregious violation can suspend the account and then terminate it. After termination, registering a new account triggers immediate re termination.

## The four level enforcement ladder

| Level | What happens | Account impact | Common cause |
|---|---|---|---|
| Rejection | A new app or update is not published | None on account standing | Data Safety mismatch, crashes, broken privacy link, missing permission justification |
| Removal | The app and prior versions are taken offline | None immediately, but multiple removals lead to suspension | Repeat policy violation, false advertising in the listing |
| Suspension | The app is pulled, purchases stop, the code can no longer be used | Counts as a strike against the account | Egregious or multiple violations, repeated rejections or removals |
| Account termination | Every app removed, no new publishing, new accounts re terminated | Permanent | Malware, fraud, harm to users or devices, severe repeat violations |

## Policy categories and what triggers enforcement

### Restricted content

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Child endangerment | Any content that sexualizes or endangers minors | Zero tolerance design, proactive detection, reporting |
| Sexual content and nudity | Pornographic or sexually explicit content | Remove explicit content, gate mature content correctly |
| Hate speech | Content targeting protected groups | Moderate and remove hateful content |
| Violence and graphic content | Gore, realistic violence, glorification of harm | Remove or heavily restrict graphic content |
| Illegal activities | Promoting illegal acts, drugs, weapons sales | Remove content that promotes illegal acts |
| Real money gambling | Unlicensed gambling, outside permitted regions | License, geo restrict, follow the gambling program |
| Financial services | Unlicensed lending, deceptive financial products, personal loan disclosure gaps | Disclose APR and terms, hold licenses, follow the financial services policy |
| Health and medical | Unqualified or misleading medical claims | Substantiate claims, avoid unproven treatments |
| Blockchain and NFT | Deceptive crypto content, undisclosed risks | Disclose risk, follow gambling rules for tokenized chance |
| Unmoderated UGC | User content that contains prohibited content with no moderation | Add reporting, filtering, and blocking before launch |

### Impersonation and intellectual property

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Impersonation | Misrepresenting the developer, copying another app, false authorship | Use your own identity and original branding |
| Intellectual property | Copyright or trademark infringement, counterfeiting, plagiarism | Own or license every asset and brand reference |

### Privacy, deception, and device abuse

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| User data | Collecting personal data without clear disclosure, using data beyond stated purposes, sharing without consent, weak security | Disclose every collection and use, secure data, honor the stated purpose |
| Permissions and APIs | Requesting permissions beyond functional need, deceptive access to location, SMS, call log, contacts | Request the minimum, justify each sensitive permission |
| AccessibilityService misuse | Using accessibility APIs for data harvesting rather than accessibility | Use accessibility APIs only for genuine accessibility, declare the use |
| Background location | Background location without a clear core feature and disclosure | Use foreground location where possible, justify background use with a prominent disclosure |
| SMS and Call Log | Requesting SMS or Call Log without an approved core use case | Use the permissions declaration, drop the permission if not core |
| All files access | MANAGE_EXTERNAL_STORAGE without a qualifying use case | Use scoped storage, request all files access only when truly required |
| Health Connect | Accessing Health Connect without an appropriate use case and disclosure | Limit to declared health use, disclose in Data Safety |
| Data Safety section | A Data Safety form that does not match the app's real data behavior. This is the number one rejection cause | Audit runtime data flows and SDKs, declare every collection, sharing, and security practice accurately |
| Device and network abuse | Malware, botnets, resource hijacking, unauthorized system modification | Ship clean, well behaved code |
| Deceptive behavior and misrepresentation | False functionality claims, misleading descriptions or screenshots, fake system UI | Make the listing match the app exactly |

### SDK and target API requirements

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Third party SDKs | An SDK that violates policy through tracking, permissions, or malicious code. The developer is responsible for SDK behavior | Vet every SDK, keep them current, remove non compliant ones |
| Target API level | Failing to target the current required Android API level | Build against the current required target API before submission |

### Monetization and ads

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Payments | Deceptive billing, hidden charges, unauthorized transactions, ignoring refund rules. Play Billing required for in app digital goods, with regional alternatives where permitted | Use Play Billing for digital goods, disclose all charges |
| Subscriptions | Unclear terms, difficult cancellation, misleading trials, undisclosed auto renewal | Show full terms, easy cancellation, honest trials |
| Payments, donations | An in-app link to Open Collective, Ko-fi, Patreon, Buy Me a Coffee, GitHub Sponsors, or a PayPal donate page. Google reads the Payments policy exception literally, only donations to a tax-exempt charity (501(c)(3)-class) may bypass Play billing, a 501(c)(6) or an unincorporated project does not qualify. Open-source apps are the usual casualty ([AnkiDroid, August 2026](https://github.com/ankidroid/Anki-Android/issues/21656)) | Remove the donation entry point from the Play build, sell it as a one-time Play billing product, or document the charity's tax-exempt status in the review notes. Source. [Payments policy](https://support.google.com/googleplay/android-developer/answer/9992660) |
| Payments, chargebacks | Not a rejection, a cost shift. For orders placed after 3 August 2026 the developer bears the purchase price less the service fee plus the card-network chargeback fee, Google Play covers only its service fee. An app that never handles the refund-review notification loses every fraudulent dispute by default | Handle `PendingRefundReviewNotification` and call the Review Refund API within 24 hours with the refund preference and usage evidence. Source. [Play Console Help](https://support.google.com/googleplay/android-developer/answer/17068375), [Review Refund API](https://developer.android.com/google/play/billing/provide-refund-and-chargeback-suggestions) |
| Ads | Ads that mimic system UI, mislead, serve malware, or are intrusive and disruptive | Use compliant ad formats and placements |
| Families ads | Non compliant SDKs or behavioral advertising in apps for children | Use only Families certified ad SDKs, no behavioral ads to minors |

### Store listing and promotion

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Metadata | Spammy listings, misleading titles or descriptions, keyword stuffing, near identical repeat submissions | Write an accurate, clean listing, one app per concept |
| Ratings, reviews, installs | Fake reviews, artificial installs, incentivized reviews, rating manipulation | Never buy or incentivize ratings or installs |
| Content ratings | A missing or inaccurate content rating questionnaire | Complete the IARC content rating questionnaire honestly |

### Spam and minimum functionality

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Spam and minimum functionality | Minimal function, frequent crashes, unresponsive UI, broken features, duplicate or low effort submissions | Ship a stable app with real, working functionality |

### Malware and mobile unwanted software

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Malware | Spyware, ransomware, rootkits, credential theft, unauthorized system access | Ship clean code, scan dependencies |
| Ad fraud | Click injection, impression fraud, hidden ad networks | Use legitimate ad mediation only |
| Social engineering | Phishing, credential harvesting, deceptive permission prompts | Be honest in every prompt and flow |
| Hostile downloaders | Bundling or installing malicious software | Do not bundle or sideload other software |
| Unauthorized system imitation | Fake system alerts, spoofed dialogs, unauthorized dialer or SMS replacement | Never imitate system UI |

### Families and Designed for Families

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Families program | Inappropriate content in child targeted apps, behavioral ads to minors, unclear parental controls, unsafe child data practices, COPPA noncompliance | Follow the Families policy, use compliant SDKs, comply with COPPA and local child law |

## The 12 tester rule for new personal accounts

New personal developer accounts created after the policy change must run a closed test with at least 12 testers for 14 consecutive days before they can apply for production access. Skipping or under populating this test blocks production. Plan the closed test window into the release schedule from day one. Organization accounts are treated differently, so the account type chosen at signup matters.

## The recurring Google failure mode

Most Google rejections are not about a forbidden feature. They are about a mismatch between what the app does and what the developer declared. The Data Safety form says no data is collected while an analytics SDK ships location. The listing promises a feature the app does not have. A permission is requested with no matching core feature. Close every one of these gaps by auditing actual runtime behavior, including every third party SDK, against every declaration before you submit.

## 2026 policy rounds you must act on (verified 5 September 2026)

Google restructured the Developer Program Policy on 26 August 2026 into one consolidated document with a standalone AI-generated content and blockchain section. Re-anchor policy links to the new pages. Every item below was read on Google's own page.

| Deadline | Change | What to do | Source |
|---|---|---|---|
| 30 September 2026 | Organization account required for financial products, health apps, VpnService apps, and government apps, with a D-U-N-S number matching the Dun and Bradstreet profile | Migrate the app to an organization account through the official Transfer ownership workflow (7-day cool-down) | [Play Console requirements](https://support.google.com/googleplay/android-developer/answer/10788890?hl=en), [preview](https://support.google.com/googleplay/android-developer/answer/17125096?hl=en) |
| 30 September 2026 | Register every Play app package name in Play Console for Android developer verification. Global, separate from the Brazil, Indonesia, Singapore, Thailand sideloading leg. Non-registration risks global removal | Complete developer verification and register each distributed applicationId | [Policy announcement, 15 July 2026](https://support.google.com/googleplay/android-developer/answer/17134731) |
| 1 October 2026 | US alternative billing and external links. transaction and download reporting plus the Play service fee begin | Wire reporting before the date if enrolled | [US alternative billing](https://support.google.com/googleplay/android-developer/answer/16497028?hl=en) |
| 22 July 2026 (live) | Play Catalog Access. registered third-party US stores list your app by default | Opt out in Play Console, Settings, Catalog Settings, if you do not want third-party distribution | [Play Catalog Access Program](https://support.google.com/googleplay/android-developer/answer/17117200?hl=en) |
| 30 June 2026 (live) | Service fee restructure in the US, UK, and EEA. 10 percent service plus 5 percent billing fee, split by new versus existing install | Re-model revenue per region | [Lower service fees](https://support.google.com/googleplay/android-developer/answer/16954621?hl=en), [blog](https://android-developers.googleblog.com/2026/06/play-expanded-billing.html) |
| 26 August 2026 (live) | Random and anonymous chat apps must block minors, may not target children, and are in scope of the Child Safety Standards | Enable minor blocking, publish CSAE standards, add reporting and a child-safety contact | [Age-Restricted Content](https://support.google.com/googleplay/android-developer/answer/17036597), [Families](https://support.google.com/googleplay/android-developer/answer/17122218), [Child Safety Standards](https://support.google.com/googleplay/android-developer/answer/14747720?hl=en) |
| 26 August 2026 (live) | READ_CALL_LOG no longer permitted for phone-call account verification | Use the Digital Credentials API or the SMS Retriever API | [Policy announcement, 15 July 2026](https://support.google.com/googleplay/android-developer/answer/17134731) |
| 26 August 2026 (live) | User Data policy explicitly covers third-party AI integrations. Unrated apps are not allowed. Earned Wage Access is a named financial sub-category (no interest, low flat fee, US APR under 36 percent) | Add the AI disclosure and consent, complete the content rating, file the EWA declaration | [Policy announcement](https://support.google.com/googleplay/android-developer/answer/17134731), [Financial Services](https://support.google.com/googleplay/android-developer/answer/9876821) |
| 25 August 2026 (live) | Generative AI. non-consensual intimate content enforcement. full-access test account, documented safety prompts and edge cases, customized input and output moderation. Suspended apps lose monetization and ads across Google | Add moderation and the review-notes evidence | [Android Developers Blog](https://android-developers.googleblog.com/2026/08/ensuring-safety-genai-preventing-non-consensual-intimate-content.html) |
| 27 October 2026 | Pre-review checks in Play Console flag contacts and location permission issues | Run them before submitting | [Android Developers Blog, April 2026](https://android-developers.googleblog.com/2026/04/giving-users-clearer-choice-and-everyone-a-safer-more-trusted-app-ecosystem.html) |
| 27 January 2027 | API 37 targets. READ_CONTACTS only when the Contact Picker is insufficient (declaration required), the location button with onlyForLocationButton, geofencing removed as a foreground service use case | Adopt the Contact Picker, the location button, and the Geofence API | [Permissions and APIs preview](https://support.google.com/googleplay/android-developer/answer/16909972?hl=en), [Foreground service preview](https://support.google.com/googleplay/android-developer/answer/16965181?hl=en) |
| February 2027 | Technical quality. R8 optimization at 25 percent minimum coverage, no bitmaps held in non-visible states, memory bad-behavior thresholds. Failure affects visibility and publishing | Enable R8 and profile memory now | [Technical quality requirements](https://support.google.com/googleplay/android-developer/answer/17492799?hl=en) |
| April 2027 | Zero-Tap Sign-In. apps with sign-in must restore state on a new device with the Restore Credentials API (games out of scope) | Integrate Credential Manager restore credentials | [Technical quality requirements](https://support.google.com/googleplay/android-developer/answer/17492799?hl=en) |
| Android 17 (API 37, 16 June 2026) | Resizability opt-out removed, ACCESS_LOCAL_NETWORK mandatory, SMS OTP three-hour delay for non-recipient apps, native libraries must be read-only for System.load, CP2 PII columns restricted, background audio hardened, per-app memory limits | Test on Android 17 with API 37 before the 2027 target bump | [Behavior changes, API 37](https://developer.android.com/about/versions/17/behavior-changes-17), [all apps](https://developer.android.com/about/versions/17/behavior-changes-all), [memory limits](https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html) |
| Target API and Billing ladder | API 36 by 31 August 2026 (extension to 1 November 2026, Wear and Automotive 35, TV and XR 34). Billing Library 8 for new submissions by 31 August 2026 (extension to 1 November 2026), for all apps by 31 August 2027, v9 by 31 August 2028 | Plan the annual bump | [Target API](https://developer.android.com/google/play/requirements/target-sdk), [Billing deprecation FAQ](https://developer.android.com/google/play/billing/deprecation-faq) |
| Account transfers, 27 May 2026 (live) | The official Transfer ownership workflow is the only permitted method, with a 7-day cool-down. News and magazine apps need the Play Console self-declaration or are removed | Use the workflow, file the declaration | [Policy announcement, 15 April 2026](https://support.google.com/googleplay/android-developer/answer/16926792?hl=en), [News declaration](https://support.google.com/googleplay/android-developer/answer/16189314?hl=en) |

Checked and unchanged in this window. the 12-tester closed testing rule, Play Integrity (Automatic Integrity Protection stays opt-in), Photo and Video permissions, Data Safety form structure, SDK Console thresholds, the VpnService declaration form. Play Age Signals remains optional, rolled out to Brazil, Australia, and Canada with every market by the end of 2026.

