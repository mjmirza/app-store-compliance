# Open Source Patterns. What the Community Already Codified

Other people have already turned hard won App Store and Google Play rejections into open source tools and lists. This document captures those patterns, down to the minor metadata rules, and folds them into this playbook so nothing the community learned is lost. Where a pattern is automatable, it is added to the rejection pattern taxonomy and the guard.

## fastlane precheck. The open source metadata rule set

`fastlane precheck` is the most widely used open source tool for catching App Store metadata rejections before submission. Its rules are the community's codified list of what Apple flags in metadata. Every rule defaults to error. A team can set a rule to warn or skip. We adopt the full rule set as metadata checks.

| precheck rule | What it catches | Maps to |
|---|---|---|
| `curse_words` | Profanity in the app metadata | Apple 2.3.1 accurate and appropriate metadata |
| `future_functionality` | Describing features that do not exist yet, coming soon, beta, placeholder promises | Apple 2.3.1 hidden or dormant functionality |
| `negative_apple_sentiment` | Mentioning an iOS bug, or negative or insensitive references to Apple | Apple 2.3.1 and the Developer Code of Conduct |
| `other_platforms` | Mentioning Android, Google Play, or another platform or marketplace in metadata or keywords | Apple 2.3.10 |
| `unreachable_urls` | Broken or unreachable URLs in the metadata, support URL, or marketing URL | Apple 1.5 and 2.1 |
| `placeholder_text` | Lorem ipsum or template text left in the listing | Apple 2.1 and 2.3.1 |
| `test_words` | Words such as test, demo, sample left in a production listing | Apple 2.1 |
| `copyright_date` | A copyright date that is out of date | Apple 2.3.1 |
| `free_stickers` | The word free misused in a sticker or app name | Apple 2.3.7 metadata |
| `custom_text` | Any word or phrase the team chooses to flag | Team defined |

Source. [fastlane precheck docs](https://docs.fastlane.tools/actions/precheck/) and [the precheck introduction](https://krausefx.com/blog/introducing-fastlane-precheck).

The lesson. A large share of rejections are caused by the words in the store listing, not the code. Most of these are cheap to detect with a string scan before submission.

## Community rejection pattern repositories worth mining

These open source repositories are real developers documenting the rejections they hit and the fixes that cleared them. They are living lists, and contributions to our playbook can pull from them.

| Repository | What it gathers |
|---|---|
| [aashishtamsya/Appstore-Review-Guidelines](https://github.com/aashishtamsya/Appstore-Review-Guidelines) | A curated pre submission guideline list, including category, location data, platform mentions, and misleading content |
| [jaywcjlove/app-rejection-fixes](https://github.com/jaywcjlove/app-rejection-fixes) | Documented rejection reasons paired with the solution that resolved each |
| [hnxyzhw/AppStoreReviewsAndRejected](https://github.com/hnxyzhw/AppStoreReviewsAndRejected) | An iOS review and rejection issues summary |
| [andrewmcwattersandco/app-store-rejections](https://github.com/andrewmcwattersandco/app-store-rejections) | A community collection of real App Store rejections |
| [lukylab/appstore-submission-checklist](https://github.com/lukylab/appstore-submission-checklist) | Practical pre submission checklists for new apps and updates |
| [truongduy2611/app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills) | An AI agent skill that scans iOS and macOS projects for rejection patterns before submission, the same idea as this playbook's skill |
| [github/awesome-copilot apple-appstore-reviewer](https://github.com/github/awesome-copilot/blob/main/skills/apple-appstore-reviewer/SKILL.md) | A published reviewer persona skill for an AI coding tool |

The pattern. The whole industry keeps relearning the same rejections in private. Capturing them in one open playbook with an automated guard is the gap this project fills.

## Google Play pre-launch report. The built in open check

When an app bundle is uploaded to a testing or production track, Google installs it on real devices in a test lab, launches it, and crawls it for several minutes. The pre-launch report is the closest thing Google has to an automated pre submission check, and it is free to every developer. Treat a clean pre-launch report as a release gate.

| Area | What it finds |
|---|---|
| Stability | Crashes captured by the automated crawl across many real devices |
| Compatibility | Use of APIs that are not in the public Android SDK |
| Security and privacy | Vulnerabilities in the app and its SDKs that an attacker could exploit |
| Accessibility | Accessibility problems surfaced by the crawl |
| Performance | Performance issues on the test lab devices |

Source. [Pre-launch report help](https://support.google.com/googleplay/android-developer/answer/9842757) and [understand your pre-launch report](https://support.google.com/googleplay/android-developer/answer/9844487).

The lesson. Run the closed testing track and read the pre-launch report before production. It catches device specific crashes, non public API use, and security holes that a single device test misses.

## What we adopted into the guard

From these open source patterns, the guard and the taxonomy gained metadata level checks that mirror fastlane precheck, in addition to the code level checks already present.

- Future functionality language in the listing, such as coming soon, beta, or a promised feature that does not ship in this build.
- Negative Apple sentiment, such as naming an iOS bug in the listing.
- Other platform mentions, already covered, reinforced here.
- Placeholder and test words in shipped resources, already covered.

The rest of the precheck rules, such as curse words and copyright date, are documented here as a manual metadata pass, because a safe automated word list belongs in each team's own configuration rather than hard coded in a shared guard.

## The Android side. Google's own and open source tooling

The Apple side has fastlane precheck. The Android side has its own equivalents, some from Google itself.

| Tool | What it does |
|---|---|
| Play Policy Insights in Android Studio | Google's own policy lint, surfaced as lint checks in recent Android Studio releases. It flags likely policy issues before you submit, the closest Android equivalent of a pre review check. Source. [Play Policy Insights](https://developer.android.com/studio/publish/insights) |
| [google/android-security-lints](https://github.com/google/android-security-lints) | Google's open source security focused custom lint checks, more security oriented and experimental than the built in lint |
| Google Play pre-launch report | The test lab crawl on real devices, covered in the section above |

Three Android facts worth pinning, gathered from the community checklists.

- Target API level. From 31 August 2026, new apps and updates must target Android 16, API level 36, or higher. Below the threshold is an automatic rejection.
- The package name, the applicationId, is permanent once published. Choose it carefully.
- Enable R8 or ProGuard. It shrinks the app and makes it harder to reverse engineer, which also helps the security review.

## How to use this with fastlane

If a team already uses fastlane, wire precheck into the lane before deliver, and keep this playbook for the code level, privacy, and policy checks that precheck does not cover. The two are complementary. precheck guards the words in the listing, this playbook guards the app, the privacy posture, and the submission settings.
