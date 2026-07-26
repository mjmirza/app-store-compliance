# Changelog

All notable changes to this playbook are recorded here. The format follows Keep a Changelog, adapted to plain punctuation.

## Unreleased

### Added

- AGENTS.md. Release review guidelines for AI agents (a 14-item checklist) plus a strict source trust hierarchy and verification rules every monitor script follows before citing a claim as fact.
- scripts/monitor-regulatory.py. The Regulatory Intelligence Agent, tracking EU/UK/US/CA/AU/SG regulatory developments through a source trust hierarchy classifier, with its own test suite.
- scripts/monitor-android.py and docs/ANDROID-POLICY-MIGRATION.md. Android and Google Play requirements compliance monitoring, with its own test suite.
- scripts/monitor-ai-policy.py and docs/AI-POLICY-MIGRATION.md. Platform-specific generative AI policy monitoring (Apple and Google), with its own test suite.
- scripts/deadline-checker.py and data/regulatory-deadlines.json. A timezone-aware regulatory deadline checker over a 90-day window, wired into the guard hook automatically.
- scripts/release-audit.py. A release readiness compliance audit engine that writes RELEASE-READINESS-REPORT.md into the audited project (gitignored, never a committed fixture).
- scripts/accessibility-audit.py. A continuous accessibility compliance audit (VoiceOver, Dynamic Type, Reduce Motion, contrast, TalkBack, touch targets), runnable standalone and deliberately not wired into the guard hook.
- Mobile and web privacy compliance monitoring, folded into the guard hook and the pattern taxonomy.
- docs/MOBILE-SECURITY-2026.md. A mobile security requirements playbook and matching guard checks (secure storage, insecure backup, unsafe deep links).
- Brazil SPA fixed-odds betting license and Google Play Age Signals compliance checks in the guard hook and pattern taxonomy.
- Apple accessibility guard checks (VoiceOver, Dynamic Type, Reduce Motion, color contrast, haptics, keyboard focus) and privacy nutrition label checks.
- docs/EU-REGULATORY-2026.md. The EU legal hard rules with dated sources and Apple developer citations. the EU AI Act (Article 50 transparency by 2 August 2026, Article 4 AI literacy, Article 5 prohibited practices, Article 99 penalties, provider versus deployer), the Digital Markets Act (distribution channels, notarization, external purchase entitlement and disclosure sheet, the Core Technology Fee and Core Technology Commission, the 500 million euro anti-steering fine), DSA trader status (Apple removal from 17 February 2025), the European Accessibility Act (in force 28 June 2025, EN 301 549 and WCAG 2.1 AA), and the Apple 2025 and 2026 platform changes (age rating deadline 31 January 2026, Guideline 5.1.2(i) third-party-AI consent, the Declared Age Range API, mini apps 4.7, Xcode 26 SDK deadline 28 April 2026).
- docs/GLOBAL-REGULATORY-2026.md. The USA and other-global legal hard rules with dated sources. US COPPA and the amended rule, the state app-store age-verification laws, the external-link rules after the Epic injunction, US state privacy laws, plus the UK Online Safety Act and Children's Code, Australia, Brazil, Canada, South Korea, India, and other jurisdictions, and what Apple tells developers to do per region.
- An EU legal gate section in docs/PRE-SUBMISSION-CHECKLIST.md.
- Pointers from the Advanced 2026 legal layer and the README docs index to the new EU and global legal docs.
- docs/PLATFORM-MECHANICS-2026.md. The platform-mechanics and newer-policy hard rules with dated sources and Apple, Google, and statutory citations. Apple (macOS notarization with notarytool and stapler, Guideline 4.2 minimum functionality and 4.3 spam or duplicate with the June 2026 saturation tightening, the reader-app External Link Account Entitlement, the France ANSSI encryption declaration matrix, the content-rights declaration, visionOS App Motion and Developer Capture, the watchOS and tvOS 26 SDK deadline, In-App Events and Custom Product Pages and the submission-concurrency limit), Android (developer verification with the 30 September 2026 country deadlines, Foreground Service types, the Play Integrity move off SafetyNet, Play Billing Library v8 by 31 August 2026, target API 35 now and 36 by August 2026, disruptive-ads and interstitial rules, Health Connect, real-money games, and the Photo Picker and deletion-URL rules), and cross-cutting (CSAM and NCMEC reporting, UGC controls and the Google Play Child Safety Standards, accessibility as a review dimension, account-and-data deletion URLs, OFAC sanctions, ADA Title III, and PSD2 SCA and PCI DSS).
- A platform mechanics gate section in docs/PRE-SUBMISSION-CHECKLIST.md, and pointers to the new doc from the Advanced 2026 layer, the README docs index, the agent skill, and the audit command.

### Fixed

- 53 duplicate PRs from a scheduled bot regenerating the same ~11 features were deep-reviewed, deduplicated to one verified merge per feature, and closed with a recorded verdict naming the superseding merge. Two PRs were disqualified outright for citing fabricated Apple/Google announcement URLs (live-verified against the real sources); one was disqualified for a reproducible hang bug from wiring an unbounded directory scan into the guard hook with no timeout.
- deadline-checker.py's regulatory-deadlines path resolution silently skipped the whole deadline section when the guard hook is installed under the flat `~/.claude/hooks/` layout instead of the nested repo layout. Now resolves under both.
- The Brazil Digital ECA effective date was corrected from an unverified 2025-03-17 to the live-confirmed 2025-09-17.

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
