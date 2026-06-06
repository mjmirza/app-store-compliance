# Credits and Sources

This playbook stands on the shoulders of the open source community. The patterns below were learned from the repositories listed here, and we credit every one. Where a project uses a license that requires attribution, this page is that attribution. Where a project is permissively licensed, we credit anyway because it is the right thing to do.

If you maintain one of these and want the wording changed or a link corrected, open an issue.

## Repositories we learned from

| Project | Author | License | What we adopted |
|---|---|---|---|
| [app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills) | truongduy2611 | MIT | The app type checklist structure, the macOS coverage, the review notes template and its six section completeness, the unused entitlements check, the Sign in with Apple UX rules, the unnecessary personal data rule, the subscription disclosure detail, and the idea of pulling live App Store Connect metadata with the asc CLI |
| [appstore-submission-checklist](https://github.com/lukylab/appstore-submission-checklist) | lukylab | CC BY 4.0 | The split between a new app checklist and an update checklist, and concrete items such as hiding debug features, the StoreKit configuration in the scheme, deploying the CloudKit schema to production, keyword field formatting, and phased release |
| [app-store-rejections](https://github.com/andrewmcwattersandco/app-store-rejections) | andrewmcwattersandco | see repo | The real named rejection case studies in the mistake patterns doc |
| [app-rejection-fixes](https://github.com/jaywcjlove/app-rejection-fixes) | jaywcjlove | MIT | Confirmation of rejection reasons paired with their fixes |
| [AppStoreReviewsAndRejected](https://github.com/hnxyzhw/AppStoreReviewsAndRejected) | hnxyzhw | see repo | The real Apple rejection email wording, the user generated content 24 hour action rule, and the finance app company account rule |
| [Appstore-Review-Guidelines](https://github.com/aashishtamsya/Appstore-Review-Guidelines) | aashishtamsya | see repo | An early curated guideline structure |

## Tools and references we point at

| Source | What it gives |
|---|---|
| [fastlane precheck](https://docs.fastlane.tools/actions/precheck/) | The open source App Store metadata rule set, adopted as our metadata checks |
| [Play Policy Insights](https://developer.android.com/studio/publish/insights) | Google's own policy lint in Android Studio |
| [google/android-security-lints](https://github.com/google/android-security-lints) | Google's open source security lint checks |
| [App Store Review Guidelines History](https://www.appstorereviewguidelineshistory.com/) | A tracker of how the guidelines changed over time |
| [lukylab/ios-permissions-descriptions](https://github.com/lukylab/ios-permissions-descriptions) | Sample permission purpose strings |

## Primary canonical sources

Every factual claim in this playbook traces to one of these.

- [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Apple developer news](https://developer.apple.com/news/)
- [Google Play Developer Program Policy](https://play.google/developer-content-policy/)
- [Google Play Console help](https://support.google.com/googleplay/android-developer)
