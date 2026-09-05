# Changelog

All notable changes to this playbook are recorded here. The format follows Keep a Changelog, adapted to plain punctuation.

## Unreleased

### Added

- September 2026 gap analysis, docs/GAP-ANALYSIS-2026-09.md. 22 rejection patterns (Apple social media declaration gate, Sign in with Apple relay domain, RESCIND_CONSENT, external purchase link region gating, Live Activities, On-Demand Resources deprecation, removed App Store Connect age-rating endpoints, Rosetta sunset, Play chargeback liability, donation links, organization registration, package registration, Contact Picker and location button and geofence rules for API 37, ACCESS_LOCAL_NETWORK, R8 optimization, Restore Credentials, generative AI NCII controls, anonymous chat minor blocking, unrated apps, developer account enrollment readiness), 20 regulatory deadlines (US ADA Title II and HHS 504 extensions, FTC COPPA age-verification policy, UK DUAA, ICO storage guidance, DMCCA subscriptions, under-16 ban, Ofcom app stores report, EU AI Act marking retrofit, Product Liability Directive, Data Act switching, eIDAS wallet, CSAM derogation expiry, Korea PIPA, China AI companion measures, Singapore OSRAA, India Consent Managers, Japan APPI), 16 new guard checks with 16 gauntlet cases, and an account and program readiness section in the pre-submission checklist.
- Licence. The whole repository moved from a dual MIT and CC BY 4.0 grant to the OpenRoots Agent License 2.3 (via ORA 1.0 on 24 August 2026, then 2.3 on 27 August 2026). One licence now covers code, docs, data, the skill, and the guard. Releases before 24 August 2026 keep MIT and CC BY 4.0 irrevocably. LICENSE is a pointer to the canonical text at openroots.org.

### Fixed

- docs/PLATFORM-MECHANICS-2026.md cited the wrong announcement id for the June 2026 Guideline 4.3 tightening and still said API 35. Now a233fmpw and API 36 with the 1 November 2026 extension.
- docs/EU-REGULATORY-2026.md section 2.3 said the EU unified fee model was not implemented. It applies from 1 October 2026 (Core Technology Commission, Attachment 14).
- Past-dated deadlines added in this sweep carry absorbed_into, so the deadline checker points at the owning pattern or doc section instead of reporting them overdue.
- The guard scanned the working directory when an explicit project path did not exist. It now fails open.
- The gauntlet's silent-case checks matched a bare pattern id anywhere in the output, so a deadline line naming that id could fail a silence test. They now match the finding line.
- README, NOTICE, CITATION.cff, and CONTRIBUTING.md still described MIT, CC BY 4.0, or the retired ORA 1.0 sunset terms after the licence change. All four now state the same licence as LICENSE.
- README listed no entry for docs/CROSS-PLATFORM-FRAMEWORKS.md, docs/PRIVACY-POLICY-MIGRATION.md, docs/SECURITY-POLICY-MIGRATION.md, docs/REGULATORY-TIMELINE.md, or the per-script test suites.
- CHANGELOG claimed the README install prompt stars the repo and follows the author through the GitHub CLI. That step was removed in #140 and the prompt now explicitly forbids acting on the user's GitHub account.

- scripts/verify-citations.py and its 10-case gauntlet. A citation provenance verifier. An HTTP 200 is not proof a page is real, because developer.apple.com serves a byte-identical news index for any unknown article id. The verifier fetches a deliberately bogus control id per host and flags any citation whose content fingerprint matches that control. It separates bot-blocked 4xx and host-fault 5xx from genuine fabrication so the gate stays signal rather than noise. Found and fixed six dead or fabricated citations already present in the repo.
- scripts/monitor-privacy.py and its test suite. Mobile and web privacy requirements monitoring across Apple, Google, and EU sources. Selected from eight competing implementations on citation integrity, the five-way majority version carried nine fabricated citations each.
- scripts/monitor-security.py and its test suite. Seventeen mobile security requirements, matched against real API symbols in your code rather than prose keywords. Selected over a longer rival that detected nothing against a fixture of real API symbols.
- scripts/generate-timeline.py and its test. Compiles a chronological regulatory timeline from data/regulatory-deadlines.json, cross-referenced into the playbook's own docs. Additive over deadline-checker.py, which only prints a rolling 90-day window.
- scripts/accessibility-audit-test.sh. A test suite for the existing accessibility audit, proven to go red when a rule is mutated.
- data/regulatory-deadlines.json. EU e-Evidence Regulation (EU) 2023/1543, applying 18 August 2026, and the Distance Marketing of Financial Services Directive (EU) 2023/2673 withdrawal button, applying 19 June 2026. Both verified against EUR-Lex.

### Fixed

- source.android.com/security/bulletin.xml returned 404. A live feed monitor-android.py and monitor-security.py fetched on every run, silently receiving nothing. Android Security Bulletins publish no RSS feed, so the dead call was removed and the canonical page cited instead.
- masvs.owasp.org was a dead domain. Corrected to mas.owasp.org/MASVS.
- Three developer.android.com paths returned 404 (privacy sandbox, Play Integrity deprecation guide, foldable devices). Corrected against live documentation.
- support.google.com answer/113289 returned 404. Corrected to answer/10788890.
- Two EDPB general guidance links returned 404. Corrected to the live guidelines page.
- monitor.py mock announcements used realistic developer.apple.com/news links. Moved to the RFC 2606 .invalid TLD so a simulation fixture can never be mistaken for a real citation, which is how fabricated citations enter the corpus.
- release-audit.py flagged its own generated readiness report as an affected file.
- monitor-regulatory.py trust hierarchy strings drifted from AGENTS.md. Realigned.

### Added

- docs/GLOBAL-REGULATORY-2026.md section 2.7 and data/rejection-patterns.json BOTH-SUBSCRIPTION-HARD-CANCEL. US subscription cancellation (negative option) coverage was completely absent. Live-verified the federal FTC click-to-cancel rule's vacatur by the Eighth Circuit (8 July 2025) and its reopened rulemaking (ANPRM, 11 March 2026), documented that California, New York, and Massachusetts have their own binding negative-option statutes regardless, and that the FTC retains Section 5 and ROSCA authority. Added a matching guard check and detection recipe for a subscription flow that requires a phone call, mail, or an in-person visit to cancel.
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
