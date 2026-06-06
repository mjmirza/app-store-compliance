# Beyond Apple and Google. Other App Stores and the Patterns Worth Adopting

The base playbook covers Apple and Google because they carry most of the world's app distribution. But a serious mobile strategy ships to more stores, and those stores publish their own review rules. This document captures what Huawei AppGallery, the Chinese Android stores, Samsung Galaxy Store, Amazon Appstore, the Microsoft Store, and RuStore enforce, then distils the cross cutting patterns worth adopting so the same mistake never repeats on a new store.

Sourced from each platform's own developer documentation. Confirm the current detail on the source before relying on it.

## Huawei AppGallery

The dominant store on Huawei devices, which ship without Google Mobile Services. The official AppGallery Review Guidelines are organized into four areas.

| Area | What it covers |
|---|---|
| App Information | Metadata, listing accuracy, app name and description |
| App Security | Malware, data handling, security review criteria |
| App Functions | Functional completeness, no crashes, the app does what it claims |
| App Content | Content policy, restricted content, age appropriateness |

The pattern that catches Android developers. An app built only against Google Mobile Services breaks on Huawei devices. Push, maps, in app purchase, and location must use Huawei Mobile Services equivalents, or the app fails on review and at runtime. Source. [AppGallery Review Guidelines](https://developer.huawei.com/consumer/en/doc/app/50104).

## The Chinese Android stores (Huawei, Tencent, Xiaomi, OPPO, vivo)

China has no single Google Play. Distribution is spread across many stores, and they share a set of national legal gates that have nothing to do with the app's content. Miss any one and the app cannot publish on any of them.

| Gate | What it is |
|---|---|
| MIIT app filing | Mandatory registration of every app with the Ministry of Industry and Information Technology, required before publication since 1 September 2023 |
| Software Copyright Certificate | Government certification of the app's copyright, required for submission. Government fees run roughly 2,200 to 3,200 CNY |
| ICP filing | Every domain the app contacts must hold a valid ICP filing |
| Approved hosting | App backends must run on approved Chinese cloud providers |
| Domestic legal entity | Only a domestic legal entity can publish. An overseas company sets up a Chinese entity or partners with a licensed distributor |
| Processing time | ICP filing alone takes around 20 working days |

The pattern. In China the binding constraint is market entry compliance, not the build. A perfect app with no filing, no copyright certificate, and no domestic entity cannot ship. Sources. [AppInChina app filing guide](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/), [TMO Group ICP guide](https://www.tmogroup.asia/insights/china-icp-license/).

## Samsung Galaxy Store

| Rule | Trigger |
|---|---|
| No copying | Copying aspects of a published app |
| No in app downloads of other apps | Offering downloads of other apps from inside the app |
| No Samsung identifiers | Displaying Samsung identifiers or implying a relationship with Samsung |
| Local legal compliance | Not observing the legal requirements and local customs of each country published in |
| User generated content | UGC without content filtering, an intellectual property resolution path, and a way for users to report content |

Source. [Samsung Galaxy Store distribution guide](https://developer.samsung.com/galaxy-store/distribution-guide.html).

## Amazon Appstore

| Rule | Trigger |
|---|---|
| Real value | An app that is a thin website, song, movie, or book with no added value |
| Stability | Fails to launch, crashes frequently, or has obvious defects |
| Automated plus manual review | Automated checks for malware and policy, followed by a manual content and functionality review |

Amazon publishes a presubmission checklist and test criteria, the same shape as the Apple and Google checklists. Sources. [Amazon presubmission checklist](https://developer.amazon.com/docs/app-submission/presubmission-checklist.html), [Amazon test criteria](https://developer.amazon.com/docs/app-testing/test-criteria.html).

## Microsoft Store

| Rule | Trigger |
|---|---|
| Certification standards | A product that does not meet the Store certification standards |
| Useful and a good fit | A product that is not genuinely useful or a good fit for the Store |
| Certification report | On failure, Microsoft returns a certification report stating the technical or policy reason |

Certification takes up to about three business days. Source. [Avoid common certification failures](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/avoid-common-certification-failures).

## RuStore (Russia)

A state backed Android store that Russian law increasingly requires devices to support.

| Rule | Trigger |
|---|---|
| Language | The app must use Russian or English, or offer a switch to one. Otherwise moderation cannot review it and the request is declined |
| Device adaptation | Errors or broken layout on modern devices |
| User generated content | UGC without a definition of inappropriate content and pre moderation or complaint based post moderation |
| Prohibited permissions | A permission with protection level not for use by third party applications is rejected on upload |
| Sensitive permissions | Sensitive permissions need a stated reason per permission |
| Security scan | Apps are scanned with Kaspersky plus a manual moderation step. Moderation is usually within about an hour |

Source. [RuStore app review guidelines](https://www.rustore.ru/help/en/developers/publishing-and-verifying-apps/requirement-apps).

## The cross cutting patterns we adopt

These are the lessons every store teaches, folded back into the way we build for any platform.

1. Market entry is a separate gate from the build. China makes this explicit with app filing, a copyright certificate, ICP filing, and a domestic entity. Before targeting a new market, list its legal gates first.
2. One binary rarely passes every store. Huawei needs Huawei Mobile Services in place of Google Mobile Services. Plan per store SDK swaps from the start.
3. Localization can be a review gate, not a nicety. RuStore declines apps it cannot read. Provide the store's accepted language.
4. Never display or imply a relationship with the store vendor. Samsung bans Samsung identifiers, Apple bans implied Apple endorsement. Treat this as universal.
5. Every store wants a per permission reason. RuStore and Huawei make it explicit. The same minimization and justification discipline serves all stores.
6. Every store returns a reason on rejection. Microsoft's certification report, Apple's Resolution Center, Google's policy email. Read the cited reason, fix that, and reply once. Never blind resubmit.
7. User generated content always needs filtering, reporting, and blocking. Apple, Google, Samsung, and RuStore all require it. Build moderation once and it satisfies every store.
8. Real added value over a thin wrapper is universal. Apple 4.2, Google minimum functionality, and Amazon all reject a thin website in a shell.

## How this feeds the guard

The Apple and Google checks stay the core of the automated guard, because they cover the most apps. The patterns above are documented here so that when a project targets Huawei, a Chinese store, Samsung, Amazon, Microsoft, or RuStore, the team applies the matching gate by hand and, where a check is automatable, it can be added to the rejection pattern taxonomy over time. Contributions that add per store detection are welcome.
