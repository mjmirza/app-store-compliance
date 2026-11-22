# Questions from X, answered

When the playbook spread on X in November 2026, about 300 people replied. These are the questions they asked about the tool itself, each answered in full here and as an accepted answer in the Q&A discussions, so you can reply with a correction or a follow-up.

Questions about one person's own rejection were left to that person. The patterns behind them are covered in the last answers below.

## Is the App Store Compliance guard safe to install and run?

Fair question, and stars prove nothing. Check it yourself in a few minutes.

- The guard is one Bash file. It reads your project, uses temporary scan buffers that it removes, makes no network call, and never changes your app. If `~/.claude/hooks/hook-log.sh` exists, it loads that helper to log errors and overrides.
- `scripts/install.sh` writes into `~/.claude` (or `$CLAUDE_CONFIG_DIR`). the hook, the skill folder, one command file, and a hook entry in `settings.json`. It backs up `settings.json` first as `settings.json.bak-<timestamp>`.
- `bash scripts/install.sh install --dry-run` prints every change and writes nothing. `doctor` checks the install, `uninstall` removes it.
- Neither the installer nor the guard calls curl or wget. `scripts/monitor.py` fetches Apple's public developer feed by default; pass `--mock`, `--simulate` or `--news-file` to stay offline. The Android, AI policy and privacy monitors fetch only with `--live`.
- Want more isolation? Run it in a container or a VM.

Section 8 of `docs/WHAT-THE-SCAN-PROVES.md` lists what each script touches.

Discussion. [#2344](https://github.com/mjmirza/app-store-compliance/discussions/2344)

## Does it cover Google Play and Android, or only the App Store?

Both stores. Of the 124 rejection patterns, 62 are Apple, 43 are Google Play, 13 apply to both, and 6 are web.

On an Android project the guard checks, among others.
- Sensitive permissions. background location, all files access, SMS and call log, accessibility service, and photo and video access, each flagged so you can justify it. The guard cannot see your Play Console declarations.
- Play Billing for digital goods, Billing Library below version 8, and donation links.
- Target API level below the current floor, and 64-bit ABIs missing next to 32-bit ones.
- Analytics or ad SDKs that mean your Data safety form needs a second look.
- A debuggable release build, and a `specialUse` foreground service missing its subtype property.

What no scan can check. whether your Play screenshots match the build, and the 12 testers for 14 days rule for new personal accounts. Both are in `docs/GOOGLE-PLAY.md` and the pre-submission checklist.

Discussion. [#2345](https://github.com/mjmirza/app-store-compliance/discussions/2345)

## Does it check Mac App Store, watchOS, tvOS or visionOS apps?

Partly, and honestly less than iOS.

- The guard has no macOS, watchOS, tvOS or visionOS specific checks. Code shared with an iOS target is scanned the same way, and a watchOS-only or visionOS-only workspace is treated as iOS.
- The Mac App Store rules from Guideline 2.4.5 (sandboxing, self-contained packaging, no auto launch, no root escalation, no downloading other code) are documented in `docs/BY-APP-TYPE.md` and `references/guidelines/by-app-type/macos-and-the-mac-app-store.md`, as a checklist you apply by hand.
- Notarization for apps shipped outside the Mac App Store, and the visionOS, watchOS and tvOS specifics, are in `docs/PLATFORM-MECHANICS-2026.md`.

If Mac checks matter to you, open an issue with the rejection you hit. Real cases decide what gets automated next.

Discussion. [#2346](https://github.com/mjmirza/app-store-compliance/discussions/2346)

## Does every finding cite the exact guideline number and the file and line?

File and line mostly yes, guideline number not on every finding yet.

- Each finding prints its severity, an ID, a title, and a fix line. Most checks also print `file. path:line`, the first place the risky code was found. Project-wide checks, such as a missing privacy policy URL, have no single line to point at.
- Many IDs carry the guideline number, for example `APPLE-5.1.1-NO-ACCOUNT-DELETION`, and some fix lines quote it, such as Apple 5.1.1(v).
- Every pattern in `data/rejection-patterns.json` has a `guideline` field, but the guard does not print it on the finding yet, and not every pattern maps to one numbered rule.

Printing the guideline on every finding is a fair request and is on the list. Until then, look up the ID in `data/rejection-patterns.json` or the docs.

Discussion. [#2347](https://github.com/mjmirza/app-store-compliance/discussions/2347)

## Does it check the privacy policy and account data, or only the code?

It covers the parts that leave a trace in the project, and asks you to confirm the rest.

What the guard checks.
- A privacy policy reference in the scanned source, for Apple and Google Play. Whether the link in the app opens and works is a manual check.
- Account deletion inside the app when the app creates accounts, and a weak version of it (only a mailto link or a deactivate button).
- A privacy manifest when required reason APIs are used, and its contents, with `scripts/validate-privacy-manifest.py`.
- Tracking SDKs without App Tracking Transparency, and SDKs that mean your Apple privacy labels or Play Data safety form need review.

What only you can confirm. that the policy text is accurate, that the privacy labels match what the app really sends, and that deletion works on a real device. Check the policy text with the pre-submission checklist. Since 2.5.0 the readiness file `.app-review-readiness.json` records the privacy labels against runtime and account deletion on a real device, and a check marked fail blocks the submit.

Discussion. [#2348](https://github.com/mjmirza/app-store-compliance/discussions/2348)

## Can the guard catch subtle design guideline violations?

Mostly the second kind, and here is the honest line.

- Design checks it does run. Sign in with Apple offered next to other social logins, relay email handling, thin web wrappers (4.2), social login without a privacy-friendly option (4.8), and a set of accessibility checks. Live Activity spam is documented with a manual detection recipe, and the guard does not check it.
- Some heuristics flag risks that are easy to miss, for example a button titled Allow before the permission prompt, HealthKit used in an app that also uses iCloud storage, or an iOS deployment target below 13. The HealthKit finding asks you to confirm by hand that no health data reaches iCloud (5.1.3(ii)).
- What it cannot judge. layout, visual polish, whether screens look consistent, and iPad layout. Those need a person on a device.

`docs/WHAT-THE-SCAN-PROVES.md` section 5 lists reported rejections and marks each as caught, partial, or not covered.

Discussion. [#2349](https://github.com/mjmirza/app-store-compliance/discussions/2349)

## How many of the rules can a static scan actually check?

That is exactly right, and the tool is built around saying so.

- 113 of the 124 patterns have a detection recipe in `data/detection-recipes.json`. Some of the rest, such as device frames in a preview video or the Play 12-tester rule, cannot be seen in code at all. A few are checked by the guard directly, without a recipe.
- Having a recipe does not mean the guard runs it. Some recipes are guidance for a person.
- For what a scan cannot prove, 2.5.0 added `.app-review-readiness.json`. You record seven checks (demo account, live backend, review notes, screenshots of this build, deletion on a real device, privacy labels against runtime, a reachable purchase). A fail blocks, and with no file the report lists what it could not see.
- A scan that could not run says NOT CHECKED instead of passing. Set `APP_STORE_GUARD_BLOCK_UNCHECKED=1` to make that block too, and `APP_STORE_GUARD_REQUIRE_READINESS=1` (or `"enforce": true` in the readiness file) to make an open readiness check block. Some unavailable checks, such as a missing manifest validator, stay warnings.

The honesty you mention is the point. The tool reports what it could not verify instead of hiding it.

Discussion. [#2350](https://github.com/mjmirza/app-store-compliance/discussions/2350)

## Does it check different things depending on the type of app?

There is no app type setting. Checks fire on what is in your code, so a game, a health app and a VPN get different findings.

- Examples. loot boxes and gambling for games, HealthKit with iCloud for health apps, betting code, and organization registration for VPN, health and finance apps on Google Play.
- `docs/BY-APP-TYPE.md` lists what reviewers expect for ten types. every app, subscriptions and in-app purchase, social and user content, kids, health, games, macOS, AI, crypto and finance, and VPN. Each has a longer guide in `references/guidelines/by-app-type/`.

How it runs. the guard reads your project, detects the platform and framework (native, Flutter, React Native, Expo, Ionic, Unity), runs the matching checks, and sorts the code findings by severity. As a hook it runs automatically before a submit command.

Discussion. [#2351](https://github.com/mjmirza/app-store-compliance/discussions/2351)

## Can it scan permissions requested inside third-party SDKs?

Partly.

- The guard finds known SDKs by name in scanned files (package.json, Gradle files, source imports) and flags the ones with known consequences, such as tracking SDKs that need App Tracking Transparency or SDKs that change your Data safety answers.
- An SDK declared only in a Podfile is not detected.
- The main source scan skips `Pods`, `node_modules` and vendored folders, and the guard does not fully audit transitive SDK permissions or each SDK's own privacy manifest. That is the vendor's job, but you are the one rejected if it is wrong.
- To see which dependency added an Android permission, check the merged manifest. See the Q&A on which dependency added a sensitive permission to the merged manifest.

Section 5 of `docs/WHAT-THE-SCAN-PROVES.md` rates SDK permissions as partial for this reason.

Discussion. [#2352](https://github.com/mjmirza/app-store-compliance/discussions/2352)

## Does the hook run before fastlane, or only when an AI agent submits?

Only on commands your AI agent runs. A command you type in a terminal, or one your CI runs, never passes through the hook.

- The hook matches submit-shaped commands the agent is about to run, such as `fastlane deliver`, `fastlane pilot`, `eas submit`, `xcrun altool`, `xcodebuild archive`, Gradle `bundleRelease`, and `flutter build ipa`.
- For your own fastlane lane or CI, call the guard yourself before the upload, for example `sh("bash path/to/app-store-compliance-guard.sh .")` in a `before_all` block. It exits 2 on a critical finding, so the lane stops.
- Exit codes. 0 clear, 2 blocked, 1 not checked when run by hand.

Section 7 of `docs/WHAT-THE-SCAN-PROVES.md` has the CI and fastlane recipe.

Discussion. [#2353](https://github.com/mjmirza/app-store-compliance/discussions/2353)

## Does it cover Huawei AppGallery and the Chinese Android stores?

As documentation, not as automated checks.

- `docs/OTHER-STORES.md` covers Huawei AppGallery and the Chinese Android stores, including the MIIT app filing, the ICP filing, and how long ICP filing takes.
- `docs/GLOBAL-REGULATORY-2026.md` tracks China deadlines, including Apple's new China mainland App Compliance declarations due by 31 January 2027 for existing apps.
- The guard has no checks specific to the Chinese stores. You apply those gates by hand.

If you ship to these stores and can share a rejection reason, open an issue. That is how a manual gate becomes a check.

Discussion. [#2354](https://github.com/mjmirza/app-store-compliance/discussions/2354)

## When Apple or Google change the rules, how fast does the playbook follow?

It checks a dated snapshot, and tells you how old it is.

- Every report opens with a `Rule pack.` line, the version and the oldest and newest date its sources were verified. Past 60 days it prints `Rule pack STALE`.
- Every deadline in `data/regulatory-deadlines.json` records its source URL and the day it was verified, and its `source_note` says plainly when the source is secondary or the primary text was not read. `scripts/verify-citations.py` checks that cited pages respond and are not soft 404s, and reports blocked or failing pages for follow-up.
- New rules have shipped within days. 2.5.0 added Apple's November developer emails, and 2.5.1 adds Apple's China mainland compliance declarations.
- To update, run `git pull` in the repo, then the same install command again.

There is no scheduled job that rewrites rules automatically, on purpose. Every change is read by a person first.

Discussion. [#2355](https://github.com/mjmirza/app-store-compliance/discussions/2355)

## Has the guard been tested on real App Store submissions?

Honest answer. it is tested heavily as software, and the real-world evidence so far is reports, not a published study.

- The guard has regression tests covering many of its checks and the failure shapes people reported, and CI runs the suite on every pull request to main and every push to main.
- `evals/gold-cases.json` scores the Fleet Sweep, Waiver Ledger and Ruling Register against fixed expected verdicts. Those are synthetic cases, not real apps.
- People have reported first-try approvals after running it, and others reported rejections it would not have caught. Those reports shaped 2.5.0.
- A clear result is not an approval. It means no critical risk was found. High and medium findings can still be listed.

If you run it before a submission, please post the outcome either way. A published record of real results is the next thing worth building.

Discussion. [#2356](https://github.com/mjmirza/app-store-compliance/discussions/2356)

## How long does App Store review take, and can I get reviewed faster?

Apple says at least half of submissions are reviewed in under 24 hours and 90 percent in under 48 hours. Developers report anything from the same day to five weeks, longest for a first app and for the round after a rejection.

What actually helps.
- Do not resubmit while waiting. It can send you to the back of the queue.
- For a critical bug fix, request an expedited review in App Store Connect with the steps to reproduce the bug.
- Avoid the round after a rejection. A working demo account and clear review notes remove the most common reasons.

The tool cannot speed up the queue. It can make it less likely you join it twice. See also [#2230](https://github.com/mjmirza/app-store-compliance/discussions/2230).

Discussion. [#2357](https://github.com/mjmirza/app-store-compliance/discussions/2357)

## What should App Review notes say so the reviewer actually uses them?

Reviewers have a few minutes per app, so notes that need reading fail. Notes that give steps work.

- Lead with what to tap. a numbered path to each feature the reviewer must see, not a description of the feature.
- A demo account that works on the release build, without 2FA, plus any code or hardware it needs.
- A short screen recording of the non-obvious flow. It beats paragraphs, especially after a rejection.
- Say what is unique and who it is for in two lines. That is the part that answers 4.3 questions.

The template is `templates/REVIEW-NOTES-TEMPLATE.md`, and the appeal steps are in `docs/MISTAKE-PATTERNS.md`. See also [#2232](https://github.com/mjmirza/app-store-compliance/discussions/2232).

Discussion. [#2358](https://github.com/mjmirza/app-store-compliance/discussions/2358)

## After a rejection, should I change the binary, the listing, or the account?

Change the thing the rejection names, and nothing else at the same time.

- Read the guideline number in the rejection. 2.3 is the listing (screenshots, description, metadata), 5.1 is privacy and data, 3.1 is payments, 4.x is the app itself. That tells you where to look.
- Never resubmit unchanged. Fix it, or reply in Resolution Center if you think the reviewer misread the app, with steps and a screen recording.
- On Google Play, when the rejection cites a Data safety mismatch or an SDK or permission, correct the form or remove the offending SDK or permission before you resubmit, rather than arguing.
- Do not resubmit in parallel, and do not create a new account to get around a rejection. An account-level action can only be appealed, never worked around.

The appeal playbook in `docs/MISTAKE-PATTERNS.md` has the steps for both stores.

Discussion. [#2359](https://github.com/mjmirza/app-store-compliance/discussions/2359)

## How do I show free trial text only to users still eligible for the intro offer?

Check eligibility before the paywall renders, and only then say free trial.

- StoreKit 2. `Product.SubscriptionInfo.isEligibleForIntroOffer`, or `isEligibleForIntroOffer(for:)` on the subscription group.
- RevenueCat on iOS. `checkTrialOrIntroDiscountEligibility(product: package.storeProduct)`, and show trial wording only for `.eligible`.
- An ineligible user sees the full price. Telling them free trial when they would be charged is a misleading pricing rejection under 3.1.2.
- The billed amount must also be at least as prominent as any per-month breakdown.

The guard does not scan for this. It is a line in `docs/PRE-SUBMISSION-CHECKLIST.md` and guidance in `docs/WHAT-THE-SCAN-PROVES.md` section 5.

Discussion. [#2360](https://github.com/mjmirza/app-store-compliance/discussions/2360)

## Does it catch device frames in App Preview videos?

It is documented, but no scan can check it, because the video is not in your code.

- Pattern `APPLE-2.3.4-DEVICE-FRAMES-PREVIEW`. App Previews must show captured app footage only, without device frames, hands, or footage from outside the app.
- It is listed in `docs/BY-APP-TYPE.md` and `references/rules/metadata.md`.
- The pre-submission checklist names it directly next to the screenshot items, because developers reported exactly this rejection.

Since 2.5.0, `screenshots_match_build` in `.app-review-readiness.json` is where you record that your screenshots and previews are current and clean.

Discussion. [#2361](https://github.com/mjmirza/app-store-compliance/discussions/2361)

## What does the OpenRoots ORA 2.3 license mean for me?

In plain words, from the `LICENSE` pointer file.

- Free and unconditional for any individual, nonprofit, school, or government body at any size, and for any company at or below USD 20,000,000 annual revenue.
- Above that threshold, 0.5 percent of the amount by which attributable revenue exceeds the threshold, capped at USD 250,000 per year, self-reported quarterly.
- AI training is not granted by either tier. It needs a separate licence.

The canonical licence text, linked from `LICENSE`, is the one that applies. This summary is not legal advice.

Discussion. [#2362](https://github.com/mjmirza/app-store-compliance/discussions/2362)

## What do people actually get rejected for, and would this have caught it?

From the rejections people described in the replies, the most common were.

- Permission wording. an onboarding button saying Allow before the system prompt. Caught by `APPLE-5.1.1-PRE-PROMPT-ALLOW-BUTTON` since 2.5.0.
- Missing permission purpose strings. Caught for the APIs the guard knows. Whether a purpose string is specific enough is a manual check.
- A demo account that did not work, or a backend that was down during review. Not visible in code, so it goes in `.app-review-readiness.json`.
- 4.3 spam or duplicate app. No scan can decide it. See [#2340](https://github.com/mjmirza/app-store-compliance/discussions/2340).
- Device frames in a preview video, and screenshots from an older build. Manual items on the checklist.

Section 5 of `docs/WHAT-THE-SCAN-PROVES.md` maps each reported rejection to the check that catches it, or marks it as a gap. If yours is not there, reply with the guideline number.

Discussion. [#2363](https://github.com/mjmirza/app-store-compliance/discussions/2363)

## Which checks run first, and is there a rule that screenshots match the app one to one?

There is no single first rule. The guard runs every check and sorts the code findings by severity, critical first. Readiness findings follow in their own block.

The order it scans in. it lists the project files, detects the platforms and framework, then runs the iOS, Android and web checks that apply.

If by 1:1 you mean screenshots and the UI matching the real app exactly, that is a real review rule, and it is not something a code scan can see. It is a manual item. record it as `screenshots_match_build` in `.app-review-readiness.json`, where a fail blocks the submit.

Discussion. [#2367](https://github.com/mjmirza/app-store-compliance/discussions/2367)
