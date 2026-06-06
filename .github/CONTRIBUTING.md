# Contributing

Contributions are welcome and wanted. App store rules change often, and a playbook like this stays useful only when many practitioners keep it current. If you have shipped iOS or Android apps and hit a rejection this playbook does not cover, your experience is exactly what improves it.

## Ways to contribute

- Open an issue for a rejection reason that is missing, out of date, or wrong.
- Open a pull request that adds or corrects a guideline, a mistake pattern, a checklist item, or a detection rule.
- Share a real rejection and how you recovered, so the appeal playbook gets sharper.
- Improve the guard so it catches more real issues with fewer false positives.

New contributors are encouraged. Look for issues labelled good first issue. If you want to help but are not sure where to start, open an issue and say so.

## The one standard that matters

Every factual claim must trace to a live canonical source.

- Apple claims trace to the App Store Review Guidelines or Apple developer news.
- Google claims trace to the Google Play Developer Program Policy or Play Console help.
- Never invent a guideline number, a policy name, or a statistic. If you cannot confirm it on the live source, mark it unverified rather than guessing.

A pull request that adds a guideline number without a source link will be asked for the source before merge.

## How to add a rejection pattern

1. Add the human facing entry to the matching doc in `docs/`.
2. Add a machine readable entry to `data/rejection-patterns.json` with an id, platform, guideline, severity, a concrete detection signal, and the fix.
3. If the pattern is automatable, add a check to `agent-os/hooks/app-store-compliance-guard.sh` and a case to `agent-os/hooks/app-store-compliance-guard-test.sh`.
4. Run the test suite and confirm it passes.

```
bash agent-os/hooks/app-store-compliance-guard-test.sh
```

## Style

- Plain, specific writing. No hype, no filler.
- Tables for rule maps. Each row carries the requirement, the trigger, and the fix.
- Keep severity honest. Critical means a real submission would be blocked.

## Pull request checklist

- Sources linked for every new factual claim.
- The guard test suite passes if you touched the guard.
- The doc, the JSON taxonomy, and the guard stay consistent with each other.
- A short description of what changed and why.

## License

By contributing you agree that your contributions are licensed under the MIT License in `LICENSE`.
