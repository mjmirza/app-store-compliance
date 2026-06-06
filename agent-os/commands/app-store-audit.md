---
description: Run an enterprise pre submission compliance audit on an iOS or Android app against Apple App Store and Google Play rejection rules. Pass a project path or run from the project root.
---

# App Store Audit

Run a full pre submission compliance audit on a mobile app project so it passes review on the first try. Use before any submission, or after a rejection to build the fix and appeal plan.

## What to do

1. Resolve the target. Use the path the user passed as an argument, otherwise the current working directory.

2. Run the automated guard against the project root and capture the ranked findings.

```
bash ~/.claude/hooks/app-store-compliance-guard.sh <project-path>
```

2b. Load the structured references for full context. From `~/.claude/skills/app-store-compliance/references/` load the by app type file that matches the app and the relevant rule category files, so the audit reasons from the full guideline set, not only the guard output. Offer the user `templates/REVIEW-NOTES-TEMPLATE.md` for a new submission.

2c. Run the metadata layer. If the user pulled the listing into a metadata directory, run `python3 ~/.claude/skills/app-store-compliance/scripts/metadata-audit.py <metadata-dir>` to audit the real store listing, and `--propose` to write suggested fixes. The pull step is `scripts/pull-metadata.sh apple`. A large share of rejections live in the listing text.

3. Run the human checks the scanner cannot see, from `~/.claude/skills/app-store-compliance/docs/PRE-SUBMISSION-CHECKLIST.md`.
   - The production backend is live and stays up during review.
   - A working demo account exists, with no 2FA the reviewer cannot pass, not expired, pre populated with data.
   - The Apple privacy nutrition labels and the privacy manifest, and the Google Data Safety form, match the real runtime behavior including every SDK.
   - Screenshots show the app in use, the listing claims only what the app does.
   - For a new Google personal account, the closed test of 12 testers over 14 days is complete.
   - The 2026 Apple age rating questionnaire is answered.

4. Produce a ranked findings table. The pattern id, the platform, the cited guideline, the severity, the concrete fix, and the file or setting to change. Order by severity. Mark every critical as a release blocker.

5. If the app was already rejected, find the matching pattern in `~/.claude/skills/app-store-compliance/data/rejection-patterns.json`, apply the fix, then follow the appeal playbook in the docs. Never resubmit an unchanged build.

6. Give a clear verdict. Clear to submit, or blocked with a numbered fix list. Never report clear while a critical finding stands.

## Reference

- Skill. `~/.claude/skills/app-store-compliance/`
- Guard. `~/.claude/hooks/app-store-compliance-guard.sh`
- Rule. `~/.claude/rules/app-store-compliance.md`
- Public playbook. https://github.com/mjmirza/app-store-compliance
