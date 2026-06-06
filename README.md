<div align="center">

<img src="assets/apple.png" alt="Apple" height="64" />&nbsp;&nbsp;&nbsp;<img src="assets/android.png" alt="Android" height="64" />

# App Store Compliance Playbook

Stop getting your iOS and Android apps rejected. The enterprise reference and automated guard that turns App Store and Google Play rejection into a designed out failure mode.

[![Apple App Store](https://img.shields.io/badge/Apple_App_Store-000000?logo=apple&logoColor=white)](https://developer.apple.com/app-store/review/guidelines/)
[![Google Play](https://img.shields.io/badge/Google_Play-414141?logo=googleplay&logoColor=white)](https://play.google/developer-content-policy/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-ready-000000?logo=anthropic&logoColor=white)](#how-you-actually-use-this)
[![MIT License](https://img.shields.io/badge/License-MIT-2ea44f)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-2ea44f)](.github/CONTRIBUTING.md)

[![Stars](https://img.shields.io/github/stars/mjmirza/app-store-compliance?style=social)](https://github.com/mjmirza/app-store-compliance/stargazers)
[![Forks](https://img.shields.io/github/forks/mjmirza/app-store-compliance?style=social)](https://github.com/mjmirza/app-store-compliance/fork)
[![Follow mjmirza](https://img.shields.io/github/followers/mjmirza?label=Follow&style=social)](https://github.com/mjmirza)

**If this saves you even one rejection, leave a star, fork it, and follow along. That is the whole ask.**

[Star this repo](https://github.com/mjmirza/app-store-compliance) &nbsp;|&nbsp; [Fork it](https://github.com/mjmirza/app-store-compliance/fork) &nbsp;|&nbsp; [Follow on GitHub](https://github.com/mjmirza) &nbsp;|&nbsp; [Follow on X](https://twitter.com/MirzaJhanzaib) &nbsp;|&nbsp; [next8n.com](https://next8n.com)

</div>

## Paste this into Claude Code, Codex, or any AI coding tool

No setup effort. Copy the block below, paste it into your AI coding tool, and it installs the whole playbook and wires the guard into your flow.

```
Set up the App Store Compliance Playbook from https://github.com/mjmirza/app-store-compliance so that from now on any iOS or Android app I build is automatically checked against Apple App Store and Google Play rejection rules before I submit it.

Steps:
1. Clone https://github.com/mjmirza/app-store-compliance into ~/repositories/app-store-compliance. If you cannot clone, read the files over the GitHub raw URLs instead.
2. Install the audit skill: copy agent-os/skill/SKILL.md plus the docs/ and data/ folders into your agent's skills directory. For Claude Code that is ~/.claude/skills/app-store-compliance/.
3. Install the pre-submission guard: copy agent-os/hooks/app-store-compliance-guard.sh into your hooks directory (for Claude Code, ~/.claude/hooks/), make it executable, and register it as a PreToolUse hook on the Bash tool in settings.json so it runs before app submission commands (fastlane, eas submit, gradle bundleRelease, xcrun altool, bundletool, xcodebuild archive) and blocks on a critical rejection risk.
4. Add a standing instruction to your agent config: for any iOS or Android work, always adhere to the Apple App Store Review Guidelines and Google Play policies, run the audit before submission, and never say an app is clear to submit while a critical risk stands.
5. Run the guard against my current project and show me the ranked findings:
   bash ~/.claude/hooks/app-store-compliance-guard.sh /path/to/my/app
6. Tell me exactly what you installed and how I run an audit any time.
```

Want only a one time check, no install? Paste this instead.

```
Read https://github.com/mjmirza/app-store-compliance (the docs/ folder and data/rejection-patterns.json), then audit my app at <path to my app> against every Apple App Store and Google Play rejection pattern. Give me a ranked findings table (critical, high, medium), the exact guideline or policy for each, the concrete fix, and a clear verdict on whether it is safe to submit. Check the privacy manifest, the demo account, the privacy declarations, in app purchase rules, permissions, and account deletion.
```

If you are inside this setup already, the slash command `/app-store-audit` runs the same audit.

## Found this useful? Three taps that help a lot

- **Star** the repo so more developers find it before they get rejected.
- **Fork** it and adapt the checklist to your own stack.
- **Follow** for more practitioner grade playbooks. GitHub [@mjmirza](https://github.com/mjmirza), X [@MirzaJhanzaib](https://twitter.com/MirzaJhanzaib), and [next8n.com](https://next8n.com).

Sharing it with one teammate who is about to submit an app is the highest compliment.

## Why this is urgent right now (2026)

AI coding tools changed the math. Anyone can build a mobile app in an afternoon now, and they are. App releases in the first quarter of 2026 were up about 60 percent year over year across both stores, and around 80 percent on iOS alone. New submissions grew roughly 30 percent to nearly 600,000 in a single recent period. The working theory across the industry is that AI assisted coding tools, Claude Code among them, are behind the surge.

Here is the trap. The stores did not loosen the rules to match the flood. They tightened them. Many AI built apps now fail before they ever reach a user.

- Apple reviewed about 7.77 million submissions in a recent year and rejected roughly 1.93 million of them, nearly one in four.
- In one year Apple rejected more than 320,000 submissions for spam, copying, or being misleading, removed over 17,000 for bait and switch, and stopped more than 37,000 potentially fraudulent apps.
- Google blocked more than 1.75 million Play submissions in 2025 for policy violations and stopped over 255,000 apps from gaining excessive access to sensitive data.
- Since late 2025, an app that sends personal data to an external AI without a consent modal naming the provider is rejected. No disclosure, no approval.
- The top modern Apple upload rejection is a missing privacy manifest, enforced since 2024, and most people building fast with AI have never heard of it.

You can ship an app in an afternoon. You can also burn a week of rejection cycles, or a suspended developer account, the same afternoon. This playbook is the difference.

Sources. [TechCrunch on the AI driven surge](https://techcrunch.com/2026/04/18/the-app-store-is-booming-again-and-ai-may-be-why/), [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/), [Google Play policy center](https://play.google/developer-content-policy/), and the rejection statistics cited inline in the docs.

## How you actually use this

This works whether you write code or not.

### If you are not a developer

You are about to submit an app, maybe one an agency or an AI tool built for you, and you do not want it bounced.

1. Open `docs/PRE-SUBMISSION-CHECKLIST.md`.
2. Treat every unchecked box as a reason you will be rejected. Answer each one honestly.
3. The two that catch most people. A working demo account with a live backend, and a privacy form that matches what the app really does.
4. Read `docs/MISTAKE-PATTERNS.md` for the appeal playbook if a rejection already landed.

### If you use Claude Code or another AI coding tool

The playbook installs as an agent skill plus a guard, so your tool carries the rules for you and stops a bad submission before it leaves your machine.

```
Your iOS or Android project
        |
        v
   Claude Code  -- reads -->  the app-store-compliance rule   (always on for any iOS/Android work)
        |
        |   when you are about to ship
        v
   /app-store-audit   or   the pre-submission guard hook
        |
        v
   scan the project against rejection-patterns.json
        |
        +-- critical rejection risk found -->  BLOCKED, with the exact guideline and fix
        |
        +-- clean -------------------------->  clear to submit
```

The guard fires automatically before submission commands such as fastlane, eas submit, gradle bundleRelease, and xcrun altool. If it finds a critical risk, it stops the upload and tells you the exact fix. Your AI tool now refuses to help you ship a rejection.

Run a manual audit any time.

```
bash agent-os/hooks/app-store-compliance-guard.sh /path/to/your/app
```

## What is inside

| Path | What it holds |
|---|---|
| `docs/APPLE.md` | Apple rejection map, sections 1 to 5, every guideline with the trigger and the fix, plus the 2026 age rating and AI disclosure changes |
| `docs/GOOGLE-PLAY.md` | Google Play rejection map across every policy, plus the four level enforcement ladder from rejection to account termination |
| `docs/ADVANCED-2026.md` | The modern upload time layer (privacy manifests, export compliance), payments and DMA depth, the full legal layer (GDPR, EU AI Act, DSA, COPPA), gambling depth, AI content policy, and Android specifics |
| `docs/OPEN-SOURCE-PATTERNS.md` | What the community already codified. The fastlane precheck metadata rule set, community rejection repositories, and the Google Play pre-launch report, folded in |
| `docs/OTHER-STORES.md` | Huawei AppGallery, the Chinese stores, Samsung, Amazon, Microsoft, and RuStore, plus the cross store patterns worth adopting |
| `docs/MISTAKE-PATTERNS.md` | The eight root cause patterns, the top mistakes, and the appeal playbook |
| `docs/PRE-SUBMISSION-CHECKLIST.md` | Exhaustive pre submission checklists for both stores, every item a verifiable check |
| `data/rejection-patterns.json` | Machine readable taxonomy of rejection patterns with detection signals and fixes. Drives the guard |
| `agent-os/skill/SKILL.md` | An agent skill that runs a full pre submission compliance audit |
| `agent-os/hooks/app-store-compliance-guard.sh` | The tested pre submission guard, usable standalone or as an agent hook |

## The first principle

Treat the store reviewer as an adversarial integration test that runs once, on a real device, with no access to your intentions and no patience for setup. Everything the reviewer needs has to be present, working, and obvious at submission time. A missing demo account, a backend that is not live, a permission string with no real reason, a privacy form that does not match runtime behavior. Each is a deterministic rejection, and each is preventable before you press submit.

## Contributing

Contributions are welcome and wanted. App store rules change constantly, and this playbook stays accurate only when many practitioners keep it current. Open an issue or a pull request, and look for issues labelled good first issue. See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). The one standard. every factual claim traces to a live Apple or Google source, and no guideline number or statistic is ever invented.

## Credits

Apple and Android logos in this README are by [Flaticon](https://www.flaticon.com/) under the Flaticon free license. The Apple logo and the Android robot are trademarks of their respective owners and are used here only to indicate the platforms this playbook covers.

## License

MIT. See [LICENSE](LICENSE).

<div align="center">

If you read this far, you are exactly who this is for. Leave a star, fork it, and follow [@mjmirza](https://github.com/mjmirza).

</div>
