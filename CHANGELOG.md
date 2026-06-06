# Changelog

All notable changes to this playbook are recorded here. The format follows Keep a Changelog, adapted to plain punctuation.

## Unreleased

Nothing yet.

## 1.0.0 (2026-06-06)

### Added
- Apple App Store rejection map across guideline sections 1 through 5, every rule with its trigger and fix, plus the 2026 age rating and AI disclosure changes.
- Google Play rejection map across every policy, plus the four level enforcement ladder from rejection to account termination.
- Advanced 2026 layer. Privacy manifests, export compliance, payments and the DMA, the full legal layer (GDPR, EU AI Act, DSA, COPPA), gambling depth, AI content policy, and Android specifics.
- Mistake pattern taxonomy, the appeal playbook, and real rejection case studies.
- Cross store coverage. Huawei AppGallery, the Chinese stores, Samsung, Amazon, Microsoft, and RuStore.
- Open source patterns doc. The fastlane precheck rule set, the Android Play Policy Insights and security lints, and the Google Play pre-launch report.
- Competitive gap analysis of the other open source compliance repositories.
- A structured, AI loadable references tree. Rules by category and guidelines by app type, each rule carrying a concrete detection command, generated from the taxonomy.
- A machine readable rejection pattern taxonomy with 53 patterns and 46 detection recipes.
- A tested pre submission guard hook that blocks risky submission commands.
- A tested metadata audit engine that audits the live store listing with a propose and re validate loop, plus a pull wrapper for the asc CLI.
- A data validator that checks the taxonomy and recipes stay consistent, run in CI.
- A continuous integration pipeline that runs the validator, both test suites, and a references drift check on every push and pull request.
- An agent skill, a slash command, a review notes template, and a copy and paste install prompt.
- Apple and Android logos, a 2026 urgency section with current statistics, engagement calls to action, a contributor guide, four good first issues, and a credits file.
- Dual license. Code under MIT, content under CC BY 4.0, attribution compulsory.
