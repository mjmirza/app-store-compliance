# PULL REQUEST DRAFT: Platform-Specific AI Policy Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with the latest platform-specific AI policies. It implements robust user disclosure, consent modals, output filtering, and content reporting mechanisms to prevent potential rejections during App Store and Google Play reviews.

## 2. Background
Both Apple and Google Play have tightened their restrictions regarding generative AI features inside mobile apps. Review systems are now actively rejecting applications that send user data to third-party LLM APIs without transparent consent or that display generative content without moderation safeguards.

## 3. Regulatory change
- **Apple (Guidelines 1.2, 5.1.2(i), and 2.3.6)**: Requires clear disclosure of third-party AI data sharing, explicit user consent prior to transmission, content filters for output safety, and reflection of chat assistants in the age rating.
- **Google Play (AI-Generated Content Policy)**: Enforces mandatory user-facing disclosures, user flagging/reporting mechanisms for offensive AI-generated content, and zero-tolerance for deepfakes, face-swapping, or non-consensual graphic outputs.

## 4. Official citations
- [Get ready for new creative assets on the App Store](https://developer.apple.com/news/?id=kug6m2ea) (Apple Update, Wed, 05 Aug 2026 08:00:58 PDT)
- [Age rating questionnaire now includes social media questions](https://developer.apple.com/news/?id=tlur8uvi) (Apple Update, Thu, 09 Jul 2026 15:00:01 PDT)
- [Hello Developer: July 2026](https://developer.apple.com/news/?id=grx7lcto) (Apple Update, Tue, 07 Jul 2026 09:00:15 PDT)
- [Design kits for iOS, iPadOS, and macOS 27 are here](https://developer.apple.com/news/?id=e2lxw9l1) (Apple Update, Tue, 23 Jun 2026 14:00:01 PDT)
- [Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=umq9wxmm) (Apple Update, Thu, 18 Jun 2026 07:30:54 PDT)
- [Changes to iOS in Brazil](https://developer.apple.com/news/?id=dhwadr2x) (Apple Update, Thu, 18 Jun 2026 07:30:05 PDT)
- [New domain for Sign in with Apple and iCloud+ Hide My Email](https://developer.apple.com/news/?id=sus6t6ab) (Apple Update, Mon, 15 Jun 2026 15:00:28 PDT)
- [WWDC26 survey](https://developer.apple.com/news/?id=15wishue) (Apple Update, Thu, 11 Jun 2026 07:00:32 PDT)
- [Find out what's new for Apple developers](https://developer.apple.com/news/?id=8rgqj83s) (Apple Update, Mon, 08 Jun 2026 11:20:01 PDT)
- [Introducing Time Allowances](https://developer.apple.com/news/?id=0d2gpmml) (Apple Update, Mon, 08 Jun 2026 11:19:33 PDT)
- [Updated Apple Developer Program License Agreement and App Review Guidelines now available](https://developer.apple.com/news/?id=a233fmpw) (Apple Update, Mon, 08 Jun 2026 11:18:33 PDT)
- [Update for Apps Distributed in Texas](https://developer.apple.com/news/?id=sg176nne) (Apple Update, Wed, 03 Jun 2026 10:00:22 PDT)
- [Apple Developer Centers are expanding to Berlin](https://developer.apple.com/news/?id=f0jfy9py) (Apple Update, Wed, 03 Jun 2026 05:00:13 PDT)
- [Introducing the 2026 Apple Design Award winners](https://developer.apple.com/news/?id=vbvsocwh) (Apple Update, Tue, 02 Jun 2026 08:50:09 PDT)
- [All systems glow](https://developer.apple.com/news/?id=q7tgn1rr) (Apple Update, Mon, 01 Jun 2026 07:00:22 PDT)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=tu7pk9oy) (Apple Update, Tue, 26 May 2026 11:00:14 PDT)
- [Upcoming changes to age ratings in Australia and Vietnam](https://developer.apple.com/news/?id=yrrb45pw) (Apple Update, Thu, 21 May 2026 13:01:22 PDT)
- [Introducing the 2026 Apple Design Award finalists](https://developer.apple.com/news/?id=8t3j66i7) (Apple Update, Mon, 18 May 2026 08:50:09 PDT)
- [Coming bright up](https://developer.apple.com/news/?id=7lcnqgxp) (Apple Update, Mon, 18 May 2026 08:00:22 PDT)
- [Hello Developer: May 2026](https://developer.apple.com/news/?id=qtzr82f0) (Apple Update, Tue, 12 May 2026 09:00:16 PDT)
- [Get the most out of your Apple Developer account](https://developer.apple.com/news/?id=sw8ldfjk) (Apple Update, Tue, 12 May 2026 06:00:26 PDT)
- [Brazilian betting license requirement for App Store availability](https://developer.apple.com/news/?id=x4eyetnp) (Apple Update, Fri, 08 May 2026 09:30:46 PDT)
- [To those who build community](https://developer.apple.com/news/?id=9lhp8vcj) (Apple Update, Mon, 04 May 2026 17:31:09 PDT)
- [Now Available: Monthly Subscriptions with a 12-Month Commitment](https://developer.apple.com/news/?id=agq42lxe) (Apple Update, Mon, 27 Apr 2026 06:00:33 PDT)
- [Lykke Studios: In pursuit of puffy perfection](https://developer.apple.com/news/?id=5t9gew40) (Apple Update, Fri, 24 Apr 2026 06:00:15 PDT)
- [Hello Developer: April 2026](https://developer.apple.com/news/?id=e1ssia6m) (Apple Update, Tue, 07 Apr 2026 06:00:16 PDT)
- [How Infold Games fashioned an open world for Infinity Nikki](https://developer.apple.com/news/?id=9mgkwjnm) (Apple Update, Fri, 03 Apr 2026 09:02:01 PDT)
- [Q&amp;A: How Plane Finder set itself up for the long haul](https://developer.apple.com/news/?id=cmd9p4g7) (Apple Update, Fri, 03 Apr 2026 09:00:01 PDT)
- [Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=fwswmjcn) (Apple Update, Mon, 30 Mar 2026 18:00:15 PDT)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=z8vzrgzx) (Apple Update, Mon, 30 Mar 2026 07:00:14 PDT)
- [Update on regulated medical device apps in the European Economic Area, United Kingdom, and United States](https://developer.apple.com/news/?id=nyqbfz1y) (Apple Update, Thu, 26 Mar 2026 15:05:24 PDT)
- [New In-App Purchase and subscription data now available in Analytics](https://developer.apple.com/news/?id=hh6v4b55) (Apple Update, Wed, 25 Mar 2026 06:10:49 PDT)
- [WWDC26: June 8-12, 2026](https://developer.apple.com/news/?id=yi8qj25k) (Apple Update, Mon, 23 Mar 2026 09:45:37 PDT)
- [Adjustments to the China storefront of the App Store on iOS and iPadOS](https://developer.apple.com/news/?id=dadukodv) (Apple Update, Thu, 12 Mar 2026 18:00:21 PDT)
- [Hello Developer: March 2026](https://developer.apple.com/news/?id=zmqipz05) (Apple Update, Tue, 03 Mar 2026 06:00:16 PST)
- [Age requirements for apps distributed in Brazil, Australia, Singapore, Utah, and Louisiana](https://developer.apple.com/news/?id=f5zj08ey) (Apple Update, Tue, 24 Feb 2026 10:00:48 PST)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=xgkk9w83) (Apple Update, Mon, 16 Feb 2026 07:00:14 PST)
- [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=d75yllv4) (Apple Update, Fri, 06 Feb 2026 08:00:56 PST)
- [Price updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=gvnljl3f) (Apple Update, Thu, 29 Jan 2026 11:00:26 PST)
- [Update on age requirements for apps distributed in Texas](https://developer.apple.com/news/?id=8jzbigf4) (Apple Update, Tue, 23 Dec 2025 16:00:04 PST)
- [Changes to iOS in Japan](https://developer.apple.com/news/?id=074b3wzz) (Apple Update, Wed, 17 Dec 2025 15:00:21 PST)
- [Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=76371du6) (Apple Update, Wed, 17 Dec 2025 08:00:15 PST)
- [New Requirements for Social Media Apps in Australia](https://developer.apple.com/news/?id=y1bckxf8) (Apple Update, Mon, 08 Dec 2025 06:00:16 PST)
- [App Store Award winners announced](https://developer.apple.com/news/?id=id45s69d) (Apple Update, Thu, 04 Dec 2025 05:00:25 PST)
- [App Store Award finalists announced](https://developer.apple.com/news/?id=2d301eoy) (Apple Update, Wed, 19 Nov 2025 01:00:55 PST)
- [Introducing the App Store Mini Apps Partner Program](https://developer.apple.com/news/?id=xcz1s7cz) (Apple Update, Thu, 13 Nov 2025 07:20:24 PST)
- [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=ey6d8onl) (Apple Update, Thu, 13 Nov 2025 07:00:11 PST)
- [Hello Developer: November 2025](https://developer.apple.com/news/?id=38c9vryd) (Apple Update, Thu, 06 Nov 2025 05:00:16 PST)
- [Next steps for apps distributed in Texas](https://developer.apple.com/news/?id=2ezb6jhj) (Apple Update, Tue, 04 Nov 2025 08:00:48 PST)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=8atty4sp) (Apple Update, Tue, 04 Nov 2025 07:00:14 PST)
- [Price updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=nomqoqfm) (Apple Update, Thu, 30 Oct 2025 06:00:46 PDT)
- [Enhancements to help you submit and market your apps and games](https://developer.apple.com/news/?id=gf6mgrs6) (Apple Update, Wed, 29 Oct 2025 06:00:28 PDT)
- [New requirement for apps using Sign in with Apple for account creation](https://developer.apple.com/news/?id=j9zukcr6) (Apple Update, Thu, 09 Oct 2025 05:00:09 PDT)
- [Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=fnkpd51y) (Apple Update, Wed, 08 Oct 2025 06:00:12 PDT)
- [New requirements for apps available in Texas](https://developer.apple.com/news/?id=btkirlj8) (Apple Update, Wed, 08 Oct 2025 05:00:09 PDT)
- [Hello Developer: October 2025](https://developer.apple.com/news/?id=glqa1owr) (Apple Update, Tue, 07 Oct 2025 05:00:16 PDT)
- [Upcoming Currency Change in Bulgaria](https://developer.apple.com/news/?id=rbfp3bpb) (Apple Update, Thu, 25 Sep 2025 09:00:46 PDT)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=4uj8znqq) (Apple Update, Mon, 22 Sep 2025 07:00:14 PDT)
- [App Store submissions now open for the latest OS releases](https://developer.apple.com/news/?id=6lxhtioi) (Apple Update, Tue, 09 Sep 2025 05:00:09 PDT)
- [Hello Developer: September 2025](https://developer.apple.com/news/?id=6zd7a3al) (Apple Update, Tue, 02 Sep 2025 05:00:16 PDT)
- [Tax and Price Updates for Apps, In-App Purchases, and Subscriptions](https://developer.apple.com/news/?id=yo2104n5) (Apple Update, Thu, 21 Aug 2025 06:00:46 PDT)
- [Updated age ratings in App Store Connect](https://developer.apple.com/news/?id=ks775ehf) (Apple Update, Thu, 24 Jul 2025 06:00:43 PDT)
- [iOS and iPadOS 26 design kits are here](https://developer.apple.com/news/?id=pnfbj8je) (Apple Update, Fri, 18 Jul 2025 10:00:15 PDT)
- [Updates for apps in the European Union](https://developer.apple.com/news/?id=awedznci) (Apple Update, Thu, 26 Jun 2025 08:24:33 PDT)
- [Today @ WWDC25: Day 5](https://developer.apple.com/news/?id=k2rqp041) (Apple Update, Fri, 13 Jun 2025 07:00:56 PDT)
- [Today @ WWDC25: Day 4](https://developer.apple.com/news/?id=8kawba5a) (Apple Update, Thu, 12 Jun 2025 08:00:56 PDT)
- [Today @ WWDC25: Day 3](https://developer.apple.com/news/?id=m43490d3) (Apple Update, Wed, 11 Jun 2025 07:00:56 PDT)
- [Today @ WWDC25: Day 2](https://developer.apple.com/news/?id=wobdp2bq) (Apple Update, Tue, 10 Jun 2025 01:00:45 PDT)
- [Updated agreements and guidelines now available](https://developer.apple.com/news/?id=r9dcmrvs) (Apple Update, Mon, 09 Jun 2025 06:00:12 PDT)
- [Today @ WWDC25: Day 1](https://developer.apple.com/news/?id=9q6q24m5) (Apple Update, Wed, 04 Jun 2025 16:59:40 PDT)
- [Introducing the 2025 Apple Design Award winners and finalists](https://developer.apple.com/news/?id=zjpafj4y) (Apple Update, Tue, 03 Jun 2025 08:00:56 PDT)
- [Hello Developer: June 2025](https://developer.apple.com/news/?id=4hac2w7l) (Apple Update, Tue, 03 Jun 2025 08:00:16 PDT)
- [Sleek peek.](https://developer.apple.com/news/?id=ccuxfzqc) (Apple Update, Mon, 02 Jun 2025 07:00:09 PDT)
- [Tax and Price updates for Apps, In-App Purchases, and Subscriptions](https://developer.apple.com/news/?id=wim4cztw) (Apple Update, Fri, 16 May 2025 07:00:46 PDT)
- [Hello Developer: May 2025](https://developer.apple.com/news/?id=p2nk9tnh) (Apple Update, Tue, 06 May 2025 09:00:59 PDT)
- [Random access memories: Inside the time-shifting narrative of The Wreck](https://developer.apple.com/news/?id=wt9blabn) (Apple Update, Tue, 06 May 2025 08:00:31 PDT)
- [Updated guidelines now available](https://developer.apple.com/news/?id=9txfddzf) (Apple Update, Thu, 01 May 2025 08:33:58 PDT)
- [Hello Developer: April 2025](https://developer.apple.com/news/?id=ytujvuu3) (Apple Update, Tue, 08 Apr 2025 07:55:43 PDT)
- [Rooms at the top: How this ADA-winning team built a title that defies description](https://developer.apple.com/news/?id=sqd5xv4n) (Apple Update, Tue, 08 Apr 2025 06:00:03 PDT)
- [WWDC25: June 9-13, 2025](https://developer.apple.com/news/?id=a425w48j) (Apple Update, Tue, 25 Mar 2025 07:00:37 PDT)
- [Assassin’s Creed Shadows comes to Mac](https://developer.apple.com/news/?id=q2zte70j) (Apple Update, Tue, 04 Mar 2025 09:00:11 PST)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=9s0rgdy9) (Apple Update, Fri, 21 Feb 2025 07:00:14 PST)
- [New features for APNs token authentication are now available](https://developer.apple.com/news/?id=wy4tb0uo) (Apple Update, Mon, 17 Feb 2025 07:00:16 PST)
- [Upcoming changes to offers and trials for subscriptions in South Korea](https://developer.apple.com/news/?id=bo1b122z) (Google Play Update, Fri, 14 Feb 2025 08:00:06 PST)
- [Tax and price updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=bdl07n0d) (Apple Update, Thu, 06 Feb 2025 07:00:51 PST)
- [Game distribution on the App Store in Vietnam](https://developer.apple.com/news/?id=06h4gf33) (Apple Update, Tue, 04 Feb 2025 12:00:38 PST)
- [The good news bears: Inside the adorably unorthodox design of Bears Gratitude](https://developer.apple.com/news/?id=i74v3f4r) (Apple Update, Tue, 04 Feb 2025 08:00:26 PST)
- [Reminder: Upcoming Changes to the App Store Receipt Signing Intermediate Certificate](https://developer.apple.com/news/?id=rzloycgp) (Apple Update, Thu, 16 Jan 2025 07:00:48 PST)
- [Algorithm changes to server connections for Apple Pay on the Web](https://developer.apple.com/news/?id=2x8awlvm) (Apple Update, Thu, 09 Jan 2025 08:00:14 PST)
- [Hello Developer: January 2025](https://developer.apple.com/news/?id=yijdyfo4) (Apple Update, Tue, 07 Jan 2025 08:00:19 PST)
- [Walk this way: How Oko leverages AI to make street crossings more accessible](https://developer.apple.com/news/?id=58c4urmu) (Apple Update, Tue, 07 Jan 2025 08:00:06 PST)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=rcvik60x) (Apple Update, Mon, 16 Dec 2024 11:31:12 PST)
- [App Store Award winners announced](https://developer.apple.com/news/?id=t9ha5xqc) (Apple Update, Wed, 11 Dec 2024 09:00:25 PST)
- [Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=edbw1dhq) (Apple Update, Fri, 06 Dec 2024 07:00:11 PST)
- [Get your apps and games ready for the holidays](https://developer.apple.com/news/?id=iwvebnw2) (Apple Update, Mon, 02 Dec 2024 07:00:45 PST)
- [App Store Award finalists announced](https://developer.apple.com/news/?id=ek82tlh0) (Apple Update, Mon, 25 Nov 2024 05:00:55 PST)
- [Price and tax updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=onjo01rj) (Apple Update, Thu, 14 Nov 2024 14:00:47 PST)
- [New Broadcast Push Notification Metrics Now Available in the Push Notifications Console](https://developer.apple.com/news/?id=106dpbzt) (Apple Update, Mon, 11 Nov 2024 07:00:29 PST)
- [Coding in the kitchen: How Devin Davies whipped up the tasty recipe app Crouton](https://developer.apple.com/news/?id=9x75y43e) (Apple Update, Mon, 04 Nov 2024 08:00:36 PST)
- [Upcoming changes to the App Store Receipt Signing Intermediate Certificate](https://developer.apple.com/news/?id=b6tejt6f) (Apple Update, Thu, 31 Oct 2024 07:00:39 PDT)
- [TestFlight enhancements to help you reach testers](https://developer.apple.com/news/?id=fps422ld) (Apple Update, Thu, 24 Oct 2024 06:00:41 PDT)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=qs5bol0g) (Apple Update, Wed, 23 Oct 2024 06:00:15 PDT)
- [Updated agreements now available](https://developer.apple.com/news/?id=g6ycjsnl) (Apple Update, Wed, 23 Oct 2024 05:50:17 PDT)
- [Apple Push Notification service server certificate update](https://developer.apple.com/news/?id=09za8wzy) (Apple Update, Thu, 17 Oct 2024 09:00:41 PDT)
- [Masters of puppets: How ROUND8 Studio carved out a niche for Lies of P](https://developer.apple.com/news/?id=jimo1g6z) (Apple Update, Thu, 10 Oct 2024 08:00:50 PDT)
- [Announcing the Swift Student Challenge 2025](https://developer.apple.com/news/?id=hu2iq38q) (Apple Update, Tue, 08 Oct 2024 05:01:37 PDT)
- [Update on iPadOS 18 apps distributed in the European Union](https://developer.apple.com/news/?id=4sn7e783) (Apple Update, Fri, 13 Sep 2024 00:00:18 PDT)
- [Win-back offers for auto-renewable subscriptions now available](https://developer.apple.com/news/?id=8utnewzk) (Apple Update, Tue, 10 Sep 2024 07:00:08 PDT)
- [App Store submissions now open for the latest OS releases](https://developer.apple.com/news/?id=utw4yhtp) (Apple Update, Mon, 09 Sep 2024 08:00:34 PDT)
- [Hello Developer: September 2024](https://developer.apple.com/news/?id=myu3gpem) (Apple Update, Tue, 03 Sep 2024 07:00:47 PDT)
- [Behind the Design: The rhythms of Rytmos](https://developer.apple.com/news/?id=34m9vbvv) (Apple Update, Tue, 03 Sep 2024 06:59:53 PDT)
- [Price and tax updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=rob1vlg0) (Apple Update, Thu, 29 Aug 2024 07:00:52 PDT)
- [Upcoming changes to the browser choice screen, default apps, and app deletion for EU users](https://developer.apple.com/news/?id=zglax7gc) (Apple Update, Thu, 22 Aug 2024 07:00:36 PDT)
- [Updates to the StoreKit External Purchase Link Entitlement](https://developer.apple.com/news/?id=szrqxadx) (Apple Update, Thu, 08 Aug 2024 07:00:20 PDT)
- [Inside Android Skills - Built for deprecation](https://android-developers.googleblog.com/2026/08/android-skills-philosophy.html) (Google Play Update, 2026-08-06T09:02:37.620-07:00)
- [Delivering safer, age-appropriate experiences on Google Play](https://android-developers.googleblog.com/2026/07/google-play-age-signals-api-safer-experiences.html) (Google Play Update, 2026-07-29T11:28:04.581-07:00)
- [Celebrating 5 years of Jetpack Compose](https://android-developers.googleblog.com/2026/07/five-years-of-jetpack-compose.html) (Google Play Update, 2026-07-30T07:41:41.322-07:00)
- [How R8 made Kotlin Coroutines on Android 2x faster](https://android-developers.googleblog.com/2026/07/how-r8-made-kotlin-coroutines-2x-faster.html) (Google Play Update, 2026-07-27T21:48:52.868-07:00)
- [Optimize your apps for the next generation of Samsung Galaxy devices](https://android-developers.googleblog.com/2026/07/optimize-galaxy-screen-sizes.html) (Google Play Update, 2026-07-22T12:06:26.700-07:00)
- [Build intelligent Android apps: Cloud and hybrid inference](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html) (Google Play Update, 2026-07-21T09:58:09.514-07:00)
- [Build intelligent Android apps: Integrate into Android's intelligence system using AppFunctions](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html) (Google Play Update, 2026-07-23T11:47:25.264-07:00)
- [Build intelligent Android apps: Introduction to Jetpacker](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html) (Google Play Update, 2026-07-21T09:57:02.378-07:00)
- [Build intelligent Android apps: On-device inference](https://android-developers.googleblog.com/2026/07/android-on-device-inference.html) (Google Play Update, 2026-07-21T09:57:46.319-07:00)
- [Upcoming Changes to the Nearby Connections API](https://android-developers.googleblog.com/2026/07/upcoming-changes-nearby-connections-api.html) (Google Play Update, 2026-07-20T09:00:55.199-07:00)
- [Android Studio Quail 2 is Stable: Multi-task with the Android Studio AI agent](https://android-developers.googleblog.com/2026/06/android-studio-quail-2-stable-features.html) (Google Play Update, 2026-07-14T06:44:50.199-07:00)
- [Evolving how LLMs are measured for Android: the next era of Android Bench](https://android-developers.googleblog.com/2026/07/android-bench-llm-measurement.html) (Google Play Update, 2026-07-08T08:59:12.713-07:00)
- [Google Play launches the first Indie Games Fund in Africa](https://android-developers.googleblog.com/2026/07/Indie-Games-Fund-Africa.html) (Google Play Update, 2026-07-06T09:05:49.653-07:00)
- [Eclipsa Video: HDR That Looks Right on Every Screen](https://android-developers.googleblog.com/2026/06/eclipsa-video-hdr-review.html) (Apple Update, 2026-06-29T15:56:50.754-07:00)
- [Expanded billing choice and lower fees on Google Play](https://android-developers.googleblog.com/2026/06/play-expanded-billing.html) (Google Play Update, 2026-06-24T10:19:34.133-07:00)
- [Android developer verification: Building a safer ecosystem together](https://android-developers.googleblog.com/2026/06/android-developer-verification.html) (Google Play Update, 2026-07-15T10:02:26.669-07:00)
- [Building a Mixed-Reality Tour Guide with Android XR, the Geospatial API, and Gemini](https://android-developers.googleblog.com/2026/06/android-xr-geospatial-api-gemini.html) (Google Play Update, 2026-07-16T09:53:34.323-07:00)
- [Android 17 is here](https://android-developers.googleblog.com/2026/06/Android-17.html) (Google Play Update, 2026-06-16T12:44:08.241-07:00)
- [What’s New in Android XR: Tooling, Engine Support, and Ecosystem Updates](https://android-developers.googleblog.com/2026/06/what-is-new-android-xr.html) (Google Play Update, 2026-06-22T12:52:22.553-07:00)
- [Top 3 updates for Android developer productivity](https://android-developers.googleblog.com/2026/06/android-developer-productivity-updates.html) (Google Play Update, 2026-06-09T17:19:04.176-07:00)
- [Datadog delivers millions of in-depth performance insights with ProfilingManager](https://android-developers.googleblog.com/2026/06/datadog-profilingmanager-performance-insights.html) (Google Play Update, 2026-06-08T09:51:11.835-07:00)
- [Prioritizing Memory Efficiency: Essential Steps for Android 17](https://android-developers.googleblog.com/2026/06/prioritizing-memory-efficiency-steps-for-android-17.html) (Google Play Update, 2026-06-15T11:44:25.503-07:00)
- [Building Premium Android Experiences at Google I/O ‘26](https://android-developers.googleblog.com/2026/06/building-premium-android-experiences-google-io-26.html) (Google Play Update, 2026-06-02T10:00:27.240-07:00)
- [Top AI on Android updates for building intelligent experiences from Google I/O ‘26](https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html) (Google Play Update, 2026-05-26T10:51:34.948-07:00)
- [17 Things to know for Android developers at Google I/O](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html) (Google Play Update, 2026-05-21T09:08:56.044-07:00)

## 5. Affected files
- `./AGENTS.md`
- `./CHANGELOG.md`
- `./README.md`
- `./agent-os/commands/app-store-audit.md`
- `./data/detection-recipes.json`
- `./data/rejection-patterns.json`
- `./docs/ADVANCED-2026.md`
- `./docs/AI-POLICY-MIGRATION.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/COMPETITIVE-GAP-ANALYSIS.md`
- `./docs/EU-REGULATORY-2026.md`
- `./docs/REGULATORY-GAP-REPORT-2026.md`
- `./references/guidelines/by-app-type/ai-and-generative-apps.md`
- `./references/rules/metadata.md`
- `./references/rules/privacy.md`
- `./references/rules/safety.md`
- `./templates/REVIEW-NOTES-TEMPLATE.md`

## 6. Risk assessment
- **Risk Level**: High
- **Consequences of non-compliance**: Immediate rejection of app updates by Apple App Review and potential Google Play suspension or removal under their AI-generated content guidelines.
- **Mitigation plan**: Build interactive user consent, prominent disclosure overlays, content moderation filters, and clear flagging UI.

## 7. Migration steps
1. **Consent Modal**: Add an in-app consent modal detailing that third-party AI/LLM components are used and get explicit consent before sending user personal data.
2. **Output Moderation**: Wire real-time prompt/response filters to detect, flag, and filter out objectionable or NSFW AI content.
3. **Age Rating Update**: Update the age rating questionnaire in App Store Connect to account for interactive AI chat functionality.
4. **Prominent Disclosure**: Implement an in-app disclaimer and user consent sheet for generative content on Android devices.
5. **Content Safety Controls**: Add a prominent 'report content' or 'flag output' UI element directly on all AI output cards.
6. **Terms of Service update**: Declare user safety requirements regarding deepfakes and non-consensual content generation.

## 8. Backward compatibility
All changes are purely additive. Older clients will default to safe local fallback content or receive standard prompts. Data structures, local schema versions, and existing preferences remain fully backward compatible.

## 9. Implementation checklist
- [ ] Create `ConsentModalView` and integrate it into onboarding/settings.
- [ ] Integrate OpenAI/Anthropic moderation API or client-side bad-word list.
- [ ] Add reporting and content flag buttons next to AI-generated messages.
- [ ] Recheck App Store Connect questionnaire for Guideline 1.2 and 2.3.6 updates.
- [ ] Implement a prominent Play Policy disclosure dialog on app launch or AI feature access.
- [ ] Implement one-click reporting next to every AI output block on Android.
- [ ] Prevent face-swap and image generation capabilities if NSFW/deepfake models can be accessed.
- [ ] Update the Google Play Console Data Safety form declarations.
- [ ] Update `docs/ADVANCED-2026.md` and related compliance manuals.

## 10. Testing checklist
- [ ] Verify that the consent modal triggers and blocks data send until approved.
- [ ] Verify that prompt injection attempts and inappropriate topics trigger the moderation filter.
- [ ] Test the content flagging button and verify reports are logged on the server.
- [ ] Test on both iOS and Android emulators/devices for layout adjustments.

## 11. Documentation checklist
- [ ] Update the Privacy Policy URL with third-party AI disclosure details.
- [ ] Update App Store Connect "Notes for Review" with demo credentials and compliance instructions.
- [ ] Update Google Play Console Data Safety questionnaire declarations.
- [ ] Document moderation guidelines in the repository's wiki or `docs/` folder.

## 12. Compliance impact
- **Apple App Store**: Aligns with 2026 guidelines; secures safe passage through human and automated reviews.
- **Google Play**: Safeguards developer account health and retains age-appropriate content standing.
- **EU AI Act**: Fulfills Article 50 transparency requirements for AI-generated interaction.

## 13. Breaking changes
- No breaking database schema migrations.
- UI flow changes include a mandatory, one-time consent prompt when first accessing AI-powered features.

## 14. Review checklist
- [ ] Code complies with all architectural boundaries and secure API storage rules.
- [ ] Consent modal text is clear, localized, and lists the AI sub-processors.
- [ ] Verification tests for the content moderation engine pass.

## 15. Approver recommendations
Ensure that the privacy consent modal explicitly mentions the specific third-party AI processor (e.g., OpenAI, Anthropic, Gemini) as mandated by Apple 5.1.2(i). Confirm that the content reporting UI is functional and triggers 24-hour moderation capabilities.
