# App Store Compliance Playbook

Enterprise grade reference for getting iOS and Android apps approved on the first submission. Built from the live canonical Apple App Store Review Guidelines and the Google Play Developer Program Policies, cross checked against published enforcement statistics and developer post mortems, then stress tested by ten adversarial reviewer personas.

This is not a getting started guide. It is the reference a mobile lead, a compliance officer, and a release engineer use to make rejection a designed out failure mode rather than a surprise.

## Why this exists

Apple reviewed roughly 7.77 million submissions in 2024 and rejected about 1.93 million of them. Nearly one in four submissions fails review, and performance issues alone accounted for more than 1.2 million of those rejections. Google blocked more than 1.75 million Play submissions in 2025 for policy violations and stopped over 255,000 apps from gaining excessive access to sensitive user data.

Rejection is not random. The same handful of guideline numbers cause the overwhelming majority of failures, year after year, because the root causes are process gaps, not knowledge gaps. This playbook names every rejection trigger, the recurring mistake behind it, and the concrete pre submission check that catches it.

## What is inside

| Path | What it holds |
|---|---|
| `docs/APPLE.md` | Full Apple App Store Review Guidelines rejection map, sections 1 through 5, with the exact trigger and fix for every numbered guideline, plus the 2026 age rating and AI disclosure changes |
| `docs/GOOGLE-PLAY.md` | Full Google Play policy rejection map across every policy category, plus the four level enforcement ladder from rejection to account termination |
| `docs/MISTAKE-PATTERNS.md` | The root cause taxonomy. Why developers repeatedly fail, the top mistakes ranked by impact, and the resolution center and appeal playbook |
| `docs/PRE-SUBMISSION-CHECKLIST.md` | Exhaustive pre submission checklists for Apple and Google, every item phrased as a verifiable check |
| `data/rejection-patterns.json` | Machine readable taxonomy of rejection patterns with detection signals and fixes. Drives the automated guard |
| `agent-os/skill/SKILL.md` | An agent skill that runs a full pre submission compliance audit on a project |
| `agent-os/hooks/app-store-compliance-guard.sh` | A pre submission guard that scans a mobile project and flags likely rejection issues before a build is uploaded |

## How to use it

1. During build, keep `docs/PRE-SUBMISSION-CHECKLIST.md` open and treat every unchecked box as a release blocker.
2. Before any upload to App Store Connect or the Play Console, run the guard in `agent-os/hooks/` against the project root, or invoke the audit skill.
3. When a rejection does land, go to `docs/MISTAKE-PATTERNS.md` for the matching pattern and the appeal playbook before you resubmit. Resubmitting without addressing the cited guideline is how a single rejection becomes an account strike.

## The first principle

Treat the store reviewer as an adversarial integration test that you cannot see the logs for. Everything the reviewer needs to approve the app has to be present, working, and obvious at submission time. A missing demo account, a backend that is not live, a permission string that does not name a real reason, a Data Safety form that does not match runtime behavior. Each of these is a deterministic rejection, and each is preventable before you ever press submit.

## Sources

Every fact in this playbook traces to a live canonical source. Primary sources are Apple's App Store Review Guidelines and developer news, and Google Play's Developer Program Policy and Play Console enforcement documentation. Empirical statistics are cited inline in the docs. This repository is maintained as a living reference and is regenerated as the guidelines change.

## Contributing

Contributions are welcome and wanted. App store rules change constantly, and this playbook stays accurate only when many practitioners keep it current. If you have shipped iOS or Android apps and hit a rejection this playbook does not cover, open an issue or a pull request. New contributors are encouraged, look for issues labelled good first issue. See `.github/CONTRIBUTING.md` for the standard, which is simple. Every factual claim traces to a live Apple or Google source, and no guideline number or statistic is ever invented.

## License

MIT. See `LICENSE`.
