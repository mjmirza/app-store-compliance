---
name: app-store-compliance
description: Run an enterprise pre submission compliance audit on a mobile app project before uploading to the Apple App Store or Google Play. Use when the user is about to submit, ship, or release an iOS or Android app, when an app was rejected and needs a fix plan, when reviewing App Store Review Guidelines or Google Play policy compliance, or when the user mentions App Store rejection, Play Console rejection, Resolution Center, Data Safety form, privacy nutrition labels, account deletion requirement, in app purchase rules, or app review.
---

# App Store Compliance Audit

This skill runs a full pre submission compliance audit against the Apple App Store Review Guidelines and the Google Play Developer Program Policies, then produces a fix plan ranked by severity. It exists because roughly one in four App Store submissions is rejected and Google blocked over 1.75 million Play submissions in 2025, almost always for the same handful of preventable causes.

## When to run it

- Before any upload to App Store Connect or the Play Console.
- After a rejection, to build the exact fix and appeal plan.
- During a release review, as a release blocker gate.

## How to run it

### Step 1. Locate the project and the reference

The compliance reference lives in the `app-store-compliance` repo. The key files are.

- `data/rejection-patterns.json` the machine readable taxonomy.
- `docs/APPLE.md` and `docs/GOOGLE-PLAY.md` the full rejection maps.
- `docs/PRE-SUBMISSION-CHECKLIST.md` the verifiable checklist.
- `docs/MISTAKE-PATTERNS.md` root causes, the appeal playbook, and real rejection case studies.
- `docs/BY-APP-TYPE.md` the rejection map routed by app type. Load the section that matches the app.
- `docs/ADVANCED-2026.md` the modern upload time and legal layer.
- `references/` the structured, AI loadable tree. Load `references/guidelines/by-app-type/<type>.md` for the app at hand and the relevant `references/rules/<category>.md` files for full context before judging.
- `templates/REVIEW-NOTES-TEMPLATE.md` the review notes template to hand the user for a new submission.
- `agent-os/hooks/app-store-compliance-guard.sh` the automated scanner.

For the strongest audit, also pull the live App Store Connect metadata and inspect the words in the real listing, not only the source. The asc CLI (`brew install asc`, then `asc metadata pull`) or the App Store Connect API gives the live title, subtitle, keywords, description, and review notes. A large share of rejections live in the listing text, so checking the real metadata catches what a source scan cannot.

### Step 2. Run the automated scan

Run the guard against the project root.

```
bash <repo>/agent-os/hooks/app-store-compliance-guard.sh /path/to/app/project
```

It detects iOS and Android, scans for the rejection patterns, and prints findings ranked critical, high, medium. It exits 2 when a critical risk is present.

### Step 3. Run the human checks the scanner cannot see

Some rejection causes are not visible in code. Walk these by hand against the project.

- Is the production backend live and will it stay up during the entire review window.
- Is a working demo account provided in the Notes for Review or the Play test instructions.
- Do the privacy nutrition labels (Apple) and the Data Safety form (Google) match the real runtime behavior including every third party SDK. This is the single biggest cause on both stores.
- Do the screenshots show the app in use, not a splash or login screen.
- Does the listing claim only what the app actually does.
- For a new Google personal account, is the closed test of 12 testers over 14 days complete.
- Are the 2026 Apple age rating questions answered.

### Step 4. Produce the fix plan

For every finding, output a table row. The pattern id, the platform, the cited guideline, the severity, the concrete fix, and the file or setting to change. Order by severity. Mark each critical as a release blocker.

### Step 5. If the app was already rejected

Read the exact guideline number the store cited, find the matching pattern in `data/rejection-patterns.json`, apply the fix, then follow the appeal playbook in `docs/MISTAKE-PATTERNS.md`. Never resubmit an unchanged build. On Google, a careless resubmit moves the account toward suspension.

## The two checks that matter most

If time is short, verify these two first, because they cause the majority of rejections across both stores.

1. A working demo account with a live backend.
2. A privacy declaration that matches actual runtime behavior, including every SDK.

## Output contract

The audit ends with a ranked findings table and a clear verdict. Clear to submit, or blocked with a numbered fix list. Never report clear while a critical finding stands.
