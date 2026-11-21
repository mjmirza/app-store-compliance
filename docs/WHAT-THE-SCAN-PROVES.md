# What the scan proves, and what it cannot

<!-- freshness: 60d -->

This page answers the questions developers asked most after the playbook spread on X in November 2026. About 300 replies were read and sorted by theme on 19 November 2026. Every answer points at a file in this repo, so you can check it rather than trust it.

## 1. The two halves of being ready

A clean scan and a ready submission are different things. The guard reads your project. A reviewer reads your running build, your store listing, and your review notes. Most painful rejections live in the second half.

| Half | What it covers | How you prove it |
|---|---|---|
| Proven by the scan | Source code, Info.plist and purpose strings, the privacy manifest, AndroidManifest permissions, Gradle and Xcode build settings, SDK names in your dependencies, placeholder text, payment code paths | `bash agent-os/hooks/app-store-compliance-guard.sh "/path/to/app"` |
| Only a person can prove | A demo account that signs in, a backend that is live and holds test data, review notes that say where each feature is, screenshots of this build on every device you support, account deletion working on a real device, privacy labels that match real traffic, an in-app purchase the reviewer can reach | `.app-review-readiness.json`, read by the same guard |

Since version 2.5.0 the guard prints both halves on every run. With no readiness file it says plainly which checks it could not see. Copy [the template](../templates/app-review-readiness.json) to your project root, test each item on the release build, and write `pass`, `fail`, `n/a`, or `todo`.

- A check marked `fail` always blocks, so a broken demo login stops the submission the same way a missing purpose string does.
- Set `"enforce": true` in the file, or `APP_STORE_GUARD_REQUIRE_READINESS=1`, and any check still `todo` blocks too. Use this in CI.
- A file whose `checked_on` is older than 30 days is flagged, because a pass on last month's build says nothing about this one.

The full manual walk is [the pre-submission checklist](PRE-SUBMISSION-CHECKLIST.md). For the review notes themselves, use [the review notes template](../templates/REVIEW-NOTES-TEMPLATE.md).

## 2. How current are the rules

A stale checklist gives false confidence, and several people said that is worse than none. So every report now opens with a line like this.

```
Rule pack. v2.5.0, sources last verified 2026-11-21 (0 days ago). The checks run against this dated snapshot, not the live guideline pages.
```

- The checks are a snapshot, not a live read of Apple's or Google's pages. Each deadline in [data/regulatory-deadlines.json](../data/regulatory-deadlines.json) carries the `source_url` it was read from and the `verified_on` day.
- Past 60 days the guard prints `Rule pack STALE` and the command to update. Change the window with `APP_STORE_GUARD_STALE_DAYS`.
- Sweeps run about every two months and are written up as gap analyses, the latest [November 2026](GAP-ANALYSIS-2026-11.md). Between sweeps the monitors in `scripts/monitor*.py` watch Apple's news feed and the Play policy pages.

## 3. Both stores, at similar depth

The playbook covers the Apple App Store and Google Play. People asked whether Play is an afterthought. It is not, as the counts below show (taken from this repo on 21 November 2026).

| | Apple | Google Play | Both |
|---|---|---|---|
| Rejection patterns in `data/rejection-patterns.json` | 61 | 43 | 13 |
| Distinct code checks in the guard | 34 | 38 (20 Play policy, 18 Android build) | 5 |
| Rule map | [APPLE.md](APPLE.md) | [GOOGLE-PLAY.md](GOOGLE-PLAY.md) | [MISTAKE-PATTERNS.md](MISTAKE-PATTERNS.md) |

On Play, the guard reads every `AndroidManifest.xml` for sensitive permissions (background location, SMS and call log, all files, accessibility, photos and videos, foreground service special use), checks target SDK and 64-bit ABIs in Gradle, looks for Play Billing on digital goods, and flags analytics or ad SDKs so you verify the Data Safety form. A screenshot that does not match the build is a manual check on both stores.

The Mac App Store shares Apple's guidelines and is covered where the code is shared. Notarization and Developer ID for apps outside the store are in [PLATFORM-MECHANICS-2026.md](PLATFORM-MECHANICS-2026.md).

## 4. Guideline 4.3 spam and 4.2 minimum functionality, honestly

Many replies asked about 4.3, often after eight or ten rejections. A static scan cannot decide 4.3. Apple judges it on whether your binary, metadata, and concept look like apps already in the store, including apps from other developers, and that store is not in your repo.

What the playbook does for 4.3 and 4.2.

- Flags a WebView, Capacitor, or Cordova shell with almost no native features (IONIC-4.2-THIN-WRAPPER). It is a heuristic, not a verdict.
- Names the process causes behind 4.3 in [MISTAKE-PATTERNS.md](MISTAKE-PATTERNS.md). Many near identical apps from one account, template or reseller apps, duplicate bundle IDs for variations, and a low effort entry in a saturated niche.
- Gives the reply that works in [the appeal playbook](MISTAKE-PATTERNS.md#the-appeal-playbook). Do not resubmit blind. Answer App Review point by point in Resolution Center, say what is unique and who it is for, and attach a short screen recording of the feature that makes the difference.

What it cannot do. Tell you that your concept is too close to someone else's. Treat any tool that claims it can with suspicion.

## 5. Rejections people reported, and whether this catches them

Taken from rejection reasons developers described in public replies in November 2026. They are the developers' own accounts, not verified rejection letters. Where a reason was vague, the row says so.

| Reported reason | Caught by | Strength |
|---|---|---|
| Missing privacy manifest, purpose strings that did not match | Guard. APPLE-PRIVACY-MANIFEST-MISSING and APPLE-5.1.1-MISSING-USAGE-DESCRIPTION, plus `scripts/validate-privacy-manifest.py` | Scan, critical |
| Onboarding button said "Allow permissions" before the location prompt, Apple wanted "Continue" | Guard. APPLE-5.1.1-PRE-PROMPT-ALLOW-BUTTON, new in 2.5.0 | Scan, high |
| Reviewer could not log in | Guard. APPLE-2.1-STAGING-BACKEND for a staging or localhost backend, plus `demo_account` in the readiness file | Scan flags part, a person proves the rest |
| Reviewer could not find the in-app purchase | `iap_reachable_by_reviewer` and `review_notes` in the readiness file | Person |
| Five of six rejections were account information and the privacy policy | Guard. APPLE-5.1.1-MISSING-PRIVACY-POLICY and GOOGLE-MISSING-PRIVACY-POLICY, `scripts/metadata-audit.py` for the listing URL | Partial |
| Naming Google Play or an Android API inside the iOS app | `scripts/metadata-audit.py` APPLE-2.3-CROSS-PLATFORM-REFERENCE on listing text. Strings inside the binary are not checked | Partial |
| AI-built web wrapper bounced under 4.2 | Guard. IONIC-4.2-THIN-WRAPPER for WebView shells | Scan, heuristic |
| 4.3(a) and 4.3(b) spam, duplicate app, saturated niche | Not decidable by a scan. See section 4 | Guidance only |
| UI not "1:1 and consistent across screens" | Not covered. The reason as reported is too vague to map to one guideline | None |
| iPad layout and iPad screenshots | `screenshots_match_build` in the readiness file. Layout on iPad is not scanned | Person |
| Trial or intro offer text shown to an Apple ID that already used it | Not scanned. Check `Product.SubscriptionInfo.isEligibleForIntroOffer` (StoreKit 2) before you show trial wording, and state what is charged after the trial (3.1.2(a)) | Guidance only |
| Account deletion that let the account sign back in | Guard. APPLE-5.1.1-NO-ACCOUNT-DELETION and APPLE-ACCOUNT-DELETION-WEAK, plus `account_deletion_device_test` in the readiness file | Scan finds the flow, a person proves it works |
| Permissions pulled in by a third-party SDK | Guard. APPLE-5.1.2-MISSING-ATT for tracking SDKs, APPLE-PRIVACY-MANIFEST-MISSING for required reason SDKs, GOOGLE-DATASAFETY-MISMATCH for analytics and ad SDKs | Partial |

Rows marked None or Guidance only are the honest gaps. If you were rejected for one of them, [open an issue](https://github.com/mjmirza/app-store-compliance/issues) with the guideline number from the letter and it becomes a check or a documented pattern.

## 6. A clear scan is not an approval

`CLEAR.` means no critical risk in what the scan can see. It does not mean Apple or Google will approve. Reviewers are people, and a submission can still be rejected on a judgment call. What the playbook saves is the extra round after a rejection you could have prevented, not the queue time itself.

On queue time, Apple's App Review page says at least 50 percent of submissions are reviewed in under 24 hours and 90 percent in under 48 hours ([Apple](https://developer.apple.com/distribute/app-review/)). Developers in the replies saw anything from same day to five weeks, longest for new apps and for the round after a rejection. If a critical bug fix is stuck, Apple accepts expedited review requests with the steps to reproduce the bug.

## 7. Is it safe to run

Read the scripts before you trust them, whatever the star count. Here is what to look for.

- The guard is one Bash file, [agent-os/hooks/app-store-compliance-guard.sh](../agent-os/hooks/app-store-compliance-guard.sh). It reads your project and writes only its own temporary files, which it deletes on exit. It never edits, moves, or deletes a file in your app.
- The guard makes no network call. It runs `python3` only for local helpers in this repo (the deadline list, the readiness file, a manifest parser).
- The monitors in `scripts/monitor*.py` do fetch Apple and Google pages, and only when you run them.
- `scripts/install.sh` writes to your AI tool's config folder and backs up any settings file it changes. Run `bash scripts/install.sh --dry-run` first to see every write.
- To be stricter, run the guard in a container or a throwaway VM with your project mounted read only.

Found a security issue in the scripts? Report it privately as described in [SECURITY.md](../.github/SECURITY.md).
