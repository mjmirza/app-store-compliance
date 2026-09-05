# Gap analysis, September 2026

<!-- freshness: 60d -->

What was checked, what changed on the platforms and in law since the previous sweep, what developers are reporting in public, and what this playbook added or corrected in response. Verified against primary sources on 5 September 2026. Anything that could not be read from a primary source is listed under Unverified, not folded into a rule.

## 1. Method

- Apple. every App Store Connect, App Review, and Developer Program announcement since 1 June 2026 was fetched and read, with the June 8 guideline text diffed against the previous revision. 88 percent of items were read on developer.apple.com itself, the rest on Apple support pages.
- Google. every Play Console Help policy announcement and Android Developers Blog post since 1 June 2026, plus the Android 17 (API 37) behaviour-change pages.
- Regulation. five regional passes (EU, UK, US federal, APAC, and Canada, Australia, Brazil), each returning only dated items with a quoted sentence from the instrument. federalregister.gov, ecfr.gov, congress.gov, ofcom.org.uk, ico.org.uk, and meity.gov.in blocked scripted fetches. those items were read through govinfo bulk data, a headed browser session, or a mirror, and are marked as such.
- Community. a 30-day sweep across Reddit, Hacker News, GitHub, and YouTube on App Store and Play rejections, plus a targeted sweep of r/appledevelopers on developer verification. Reddit rate-limited the sweep after 15 items and blocked every direct fetch, so Reddit coverage is partial and stated as partial.
- Repo. every finding was diffed against `data/rejection-patterns.json`, `data/regulatory-deadlines.json`, the guard, and the docs before anything was written.

## 2. What developers are saying (the pains behind the gaps)

Each item below produced a pattern, a deadline, or a doc change. Quotes are verbatim from the saved raw files under `~/Documents/Last30Days/`.

- Play chargebacks now land on the developer. r/androiddev, "Google Play's chargeback/dispute changes cost you $28.50 on a $5 sale". Verified on Play Console Help answer 17068375. orders after 3 August 2026 shift the disputed purchase amount to the developer, and the Review Refund API is the only way to contest one. Added GOOGLE-PLAY-CHARGEBACK-LIABILITY plus a guard check for Play Billing without refund-review handling.
- Donation links are a Payments rejection. AnkiDroid issue 21656 (921 points on Hacker News). Google's own line, quoted in the issue, "501(c)(6) status does not suffice because user donations are not tax-exempt." Added GOOGLE-PAYMENTS-DONATION-LINK and a guard check for Open Collective, Ko-fi, Patreon, and similar links in an Android build.
- External purchase links are a US-only carve-out. Multiple implementation reports say the same link UI shipped worldwide is rejected under 3.1.1 outside the United States and to "budget two rejection rounds". Added APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING with a storefront-gating counter-signal.
- Android developer verification confuses per-bundle-id setups. r/expo, "my app was automatically verified by Android for the new policy ... However, I do have separate bundle identifiers." Added GOOGLE-PLAY-APP-REGISTRATION-MISSING (register every distributed package name by 30 September 2026) and the account-readiness checklist.
- Vibe-coded apps discover review late. "I thought being able to build was enough to launch an app. I was wrong." The pre-submission checklist gained an account and program readiness section so the blockers that sit before review are visible before the first build.
- React Native and Expo builds flagged "App optimization: Low". Two separate r/reactnative threads. Traced to the February 2027 technical-quality requirement (R8 at 25 percent minimum coverage). Added ANDROID-R8-OPTIMIZATION-MISSING with a Gradle check.

## 3. The r/appledevelopers verification question, validated

The ask was how many people on r/appledevelopers report actually getting verified, and whether the playbook covers those steps.

- Subreddit evidence. the last30days sweep of r/appledevelopers returned four threads in the window (a Team Name change on an Individual account, a Guideline 5.6 removal for features hidden during review, a timer app launch, and a Private Cloud Compute entitlement question). None is a verification thread. Reddit returned HTTP 429 partway through and blocked every direct fetch, including a headless browser session, so this is partial coverage and not proof the topic is absent.
- Forum evidence, which is where the pain actually shows. Apple Developer Forums thread 817247 has five replies on Developer Program enrollment stuck in identity verification. four still pending, one approved after about a month, one refunded. Thread 816626 reports the identity-upload link failing with "Sorry, you don't have access. Your account isn't authorized to upload files" for more than 45 days. Threads 816864, 817185, 813667, 821680, 814930, and 767809 report the same shape, and one individual-to-organization migration has been open for 61 days. Sources. [thread 817247](https://developer.apple.com/forums/thread/817247), [thread 816626](https://developer.apple.com/forums/thread/816626).
- Was the playbook tackling it. No. Enrollment and account readiness appeared only as a VPN organization-enrollment row and a Health organization-migration line. Nothing said that the account can block a launch for weeks before review starts, and Guideline 5.6 existed only as a table row.
- What changed. APPLE-ENROLLMENT-VERIFICATION-PENDING (manual pattern, six-week enrollment lead time, ADPLA attachment acceptance, migration a quarter ahead), the account and program readiness section in `docs/PRE-SUBMISSION-CHECKLIST.md`, and the account-readiness line in the Apple 2026 changes list. The honest count from the evidence read. of six enrollment reports with a stated outcome, one verified, one refunded, four still pending.

## 4. Apple, verified deltas

| Change | Source | Repo action |
|---|---|---|
| Social media capability declaration is a submission gate since September 2026, minimum 13+, Declared Age Range for under-13 | [0d2gpmml](https://developer.apple.com/news/?id=0d2gpmml), [tlur8uvi](https://developer.apple.com/news/?id=tlur8uvi) | APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION, deadline, APPLE.md row |
| Sign in with Apple relay addresses also arrive from private.icloud.com | [1ptvdtcm](https://developer.apple.com/news/?id=1ptvdtcm) | APPLE-4.0-SIWA-RELAY-DOMAIN, guard check |
| Age assurance requires the iOS 26.2 SDK and handling RESCIND_CONSENT | [Age assurance support](https://developer.apple.com/support/age-assurance) | APPLE-5.1.1-RESCIND-CONSENT-UNHANDLED, guard check |
| Guideline 1.2 UGC escalation and 4.5.3 Live Activities named (8 June 2026) | [Guidelines](https://developer.apple.com/app-store/review/guidelines/) | Pattern updates, APPLE-4.5.3-LIVE-ACTIVITY-SPAM |
| On-Demand Resources deprecated from the 27 OS family | [WWDC26 App Store guide](https://developer.apple.com/wwdc26/guides/app-store/) | APPLE-ODR-DEPRECATED-27, guard check |
| App Store Connect API 4.3 and 4.4 removed the old age-rating endpoints | [API 4.4 notes](https://developer.apple.com/documentation/appstoreconnectapi/app-store-connect-api-4-4-release-notes) | APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED, guard check |
| macOS 27 is the last release with Rosetta | [w5ngl9k2](https://developer.apple.com/news/?id=w5ngl9k2) | APPLE-MACOS-ROSETTA-SUNSET |
| EU unified terms from 1 October 2026, CTC replaces CTF, Attachment 14 | [gmws0jgp](https://developer.apple.com/news/?id=gmws0jgp), [0cgo95n6](https://developer.apple.com/news/?id=0cgo95n6) | EU-DMA-UNIFIED-TERMS-2026, EU-REGULATORY section 2.3 rewritten |
| Brazil alternative distribution from iOS 26.5, Attachment 12 by 6 July 2026 | [dhwadr2x](https://developer.apple.com/news/?id=dhwadr2x), [umq9wxmm](https://developer.apple.com/news/?id=umq9wxmm) | Deadline, GLOBAL-REGULATORY section 3.3 |
| Australia 15+ removed, Vietnam Decree 147 rating, Korea descriptor move | [yrrb45pw](https://developer.apple.com/news/?id=yrrb45pw), [oj3r9pvw](https://developer.apple.com/news/?id=oj3r9pvw) | Deadline, GLOBAL-REGULATORY sections 3.2, 3.5, 3.10 |
| Brazil betting licence check needs a new binary | [x4eyetnp](https://developer.apple.com/news/?id=x4eyetnp) | APPLE-GAMBLING-BRAZIL-LICENSE fix text |

Stale entries corrected. `docs/PLATFORM-MECHANICS-2026.md` cited the wrong announcement id for the June 2026 Guideline 4.3 tightening (now a233fmpw) and still said API 35 (now API 36 with the 1 November 2026 extension). `docs/EU-REGULATORY-2026.md` section 2.3 said the unified fee model was not implemented. it is, from 1 October 2026.

## 5. Google Play and Android, verified deltas

| Change | Source | Repo action |
|---|---|---|
| Chargeback cost shift, 3 August 2026 | [Play Console Help 17068375](https://support.google.com/googleplay/android-developer/answer/17068375) | GOOGLE-PLAY-CHARGEBACK-LIABILITY, guard check, deadline, GOOGLE-PLAY.md row |
| Donation links under the Payments policy | [Payments policy](https://support.google.com/googleplay/android-developer/answer/9992660) | GOOGLE-PAYMENTS-DONATION-LINK, guard check |
| Organization account for regulated categories, 30 September 2026 | [Play Console requirements](https://support.google.com/googleplay/android-developer/answer/10788890) | GOOGLE-ORG-REGISTRATION-REQUIRED, guard check, deadline |
| Register every package name for developer verification, 30 September 2026 | [15 July 2026 announcement](https://support.google.com/googleplay/android-developer/answer/17134731) | GOOGLE-PLAY-APP-REGISTRATION-MISSING, deadline |
| READ_CALL_LOG no longer permitted for call verification, 26 August 2026 | same | GOOGLE-PERM-SMS-CALLLOG detection updated |
| Anonymous and random chat apps in scope of Child Safety Standards | [17036597](https://support.google.com/googleplay/android-developer/answer/17036597) | GOOGLE-ANON-CHAT-MINOR-BLOCK, guard check |
| Generative AI NCII controls, 25 August 2026 | [Android Developers Blog](https://android-developers.googleblog.com/2026/08/ensuring-safety-genai-preventing-non-consensual-intimate-content.html) | GOOGLE-GENAI-NCII-CONTROLS, guard check |
| Unrated apps not allowed, third-party AI in the User Data policy | [17134731](https://support.google.com/googleplay/android-developer/answer/17134731) | GOOGLE-UNRATED-APP-BANNED |
| API 37 targets. Contact Picker, location button, geofencing out of foreground services (27 January 2027) | [16909972](https://support.google.com/googleplay/android-developer/answer/16909972), [16965181](https://support.google.com/googleplay/android-developer/answer/16965181) | Three patterns, TSDK-gated guard block, deadline |
| Technical quality, February 2027 (R8, memory) and Restore Credentials, April 2027 | [17492799](https://support.google.com/googleplay/android-developer/answer/17492799) | ANDROID-R8-OPTIMIZATION-MISSING, ANDROID-RESTORE-CREDENTIALS-REQUIRED, deadlines |
| Android 17 ACCESS_LOCAL_NETWORK, read-only native libraries, per-app memory limits | [Behavior changes 17](https://developer.android.com/about/versions/17/behavior-changes-17) | ANDROID-LOCAL-NETWORK-PERMISSION, ANDROID-DYNAMIC-CODE-LOADING updated |
| Target API 36 with 1 November 2026 extension, Billing v8 ladder to 2028 | [Target SDK](https://developer.android.com/google/play/requirements/target-sdk) | Deadline text updated, GOOGLE-TARGET-API updated |
| US alternative billing reporting from 1 October 2026, Play Catalog Access default from 22 July 2026 | [16497028](https://support.google.com/googleplay/android-developer/answer/16497028), [17117200](https://support.google.com/googleplay/android-developer/answer/17117200) | Deadlines, GOOGLE-PLAY.md section |

## 6. Regulation, verified deltas

Thirty-eight deadlines were added and eight corrected. The full dated list is in `data/regulatory-deadlines.json` and the compiled view in `docs/REGULATORY-TIMELINE.md`.

- United States. DOJ ADA Title II and HHS Section 504 mobile-app accessibility dates were extended by 2026 interim final rules to 26 April 2027 and 11 May 2027 (large entities) and 26 April 2028 and 10 May 2028 (small). The FTC COPPA age-verification policy statement (25 February 2026) is a live safe harbour. COPPA 2.0 passed the Senate and the KIDS Act passed the House, neither is law. The COPPA section 312.11 carve-outs bind Safe Harbor programs, not developers, a correction to the earlier text.
- United Kingdom. DUAA commenced 5 February 2026 with the complaints process on 19 June 2026. ICO storage and access guidance published 29 April 2026. DMCCA subscription regime moves to January 2027 (earlier estimate was spring 2027). Under-16 social media ban regulations laid by end of 2026 for spring 2027, with an 18+ floor for AI romantic companions. Ofcom app stores report due by January 2027.
- European Union. Regulation (EU) 2026/1744 is in force, so the Annex III and Annex I high-risk dates (2 December 2027, 2 August 2028) are law, and 2 December 2026 brings the marking retrofit and the NCII and CSAM prohibition. Data Act 12 September 2026 is access-by-design, not switching (switching charges hit zero 12 January 2027). Product Liability Directive applies from 9 December 2026. eIDAS wallet acceptance by 24 December 2027. CSAM ePrivacy derogation expires 3 April 2028. There is no general EAA 2027 date.
- Asia-Pacific. Korea PIPA amendment effective 11 September 2026. China AI anthropomorphic services measures effective 15 July 2026 (no companion services to minors). Singapore OSRAA partially commenced 29 June 2026. India Consent Managers tranche 13 November 2026. Japan APPI amendment effective by 16 July 2028 with an under-16 threshold.
- Canada, Australia, Brazil. Australia's App Distribution Services Code age-assurance duty bites 9 September 2026 (read from an archived copy, re-confirm live), Privacy Act automated-decision disclosure and the Children's Online Privacy Code land 10 December 2026. Brazil's Decreto 12.880 (18 March 2026) puts age signals on stores and operating systems, with ANPD enforcement from January 2027. Canada has no new dated app obligation.
- US states. Utah moved to 6 May 2027 (HB 498), Louisiana to 1 July 2027 (HB 977), Texas is in force since 1 January 2026 after the Supreme Court left the Fifth Circuit stay in place, Alabama is confirmed for 1 January 2027. New 2027 dates for California (AB 1043, SB 976, AB 56, CPPA automated decision-making), New York SAFE for Kids (25 January 2027), Vermont, Washington, Oklahoma, and Colorado (2028).

## 7. Process improvements shipped with this sweep

- Account and program readiness is now the first section a submitter reads, because the community evidence shows the account, not the binary, is what blocks a first launch in 2026.
- Every deadline that has passed carries `absorbed_into`, so `scripts/deadline-checker.py` points at the pattern or doc section that now owns it instead of shouting overdue.
- The guard gauntlet grew from 26 to 42 cases and its silent-case checks now match the finding line, so a deadline that names a pattern id can no longer false-fail a silence test.
- A missing explicit project path now fails open in the guard instead of silently scanning the working directory.

## 8. Unverified, deliberately not encoded

- The exact day in September 2026 the social media declaration gate opened, the exact February and April 2027 days for Play technical quality and Restore Credentials, and the exact January 2027 day for the DMCCA regime. Tracked as the first of the month with the wording quoted.
- The global rollout date for Android developer verification beyond Brazil, Indonesia, Singapore, and Thailand. Google has not published it.
- Whether the DOJ ADA interim final rule has been finalised, and whether the FTC AI-accuracy policy statement was adopted after 31 July 2026.
- Japan APPI law number and the six-month penalty commencement, Korea mandatory certification (1 July 2027), Korea MyData expansion dates. secondary sources only.
- The India DPDP Rules Gazette text was confirmed from a mirror because meity.gov.in returned 403.
- r/appledevelopers coverage is partial. the Reddit sweep was rate-limited after 15 items and every direct fetch was blocked.
