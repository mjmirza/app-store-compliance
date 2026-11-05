# Ruling Register

A code scan cannot tell you that India wants your lending app on an RBI list, that Australia wants under-16s kept off your social feed, or that the EU wants a 24 hour vulnerability report. The Ruling Register holds those release requirements as data, says how strongly each one binds today, and says how it is proven, so a missing finding is never mistaken for a pass.

## What you get

- Legal standing on every requirement. `in_force`, `in_force_later` (with the date it starts), `store_policy`, `proposed`, or `guidance`. Only verified law or store policy that is in force today can block a release. A proposed law or a guidance note never can.
- How it is proven. `automated` (a check can see it), `owner_attested` (only you can confirm it), or `mixed` (both). An owner-attested requirement asks for your signed attestation, because a scan finding nothing proves nothing here.
- A quoted source for every premise. Each source carries the URL, the date it was checked, a verbatim quote, and `supports`, which says whether it proves the obligation, the start date, or both. A rule blocks only when quoted sources cover the obligation and, if it has one, the start date. A source that could not be re-read is marked `unverified` with the reason, and a rule missing a quoted premise is listed as "confirm the source" and never blocks.
- Applies only where it should. Each entry names its jurisdiction (an ISO country code, `EU`, or `GLOBAL`), an optional store, and the app features it covers (`lending`, `crypto`, `medical`, `generative_ai`, `personal_data`, `subscriptions`, `social`, `marketplace`, `children`). A rule with no features applies to every app in that place.
- Built into Fleet Sweep. Every app declares its `platforms`, `regions` and `features`, and leaving one out is an error, because an unknown scope would silently drop rules. Any verified, in-force rule that applies and has no valid attestation makes the app `BLOCKED`.

## From install to first answer

1. Ask what applies to an app.

   ```bash
   python3 scripts/ruling-register.py due --regions DE,AU,US --stores apple --features social,personal_data
   ```

   Each line says `BLOCKS`, `WATCH`, or `CONFIRM-SOURCE`, and whether it needs your attestation.
2. Add `regions`, `features` and, once you have checked a requirement, an attestation to the app in your fleet file.

   ```json
   "attestations": {
     "RR-AU-APP1-PRIVACY-POLICY": {
       "attested_by": "Your Name",
       "attested_on": "2026-11-05",
       "outcome": "compliant",
       "revision": 1,
       "covers": ["auto-1", "owner-2"],
       "regions": ["AU"],
       "evidence": "Policy linked in app and listing, reviewed against APP 1 in the October release notes"
     }
   }
   ```

   An attestation is accepted only when `outcome` is `compliant`, `revision` matches the rule's current revision, `covers` lists every proof item id of the rule (including the automated ones, with the check result as evidence), and `regions` lists every country of yours the rule reaches. It cannot be dated in the future and expires after a year. Raise a rule's `revision` when it changes, and every attestation for it has to be made again.
3. Run Fleet Sweep. The register is read by default. Pass `--no-register` to leave it out.

## Add or change a requirement

1. Edit `data/ruling-register.json`. Give a new rule a new `RR-` id and `revision` 1. Never reuse an id for a different rule, and raise `revision` when an existing rule's meaning changes.
2. Quote the primary source verbatim and record the date you read it. Never paste a URL you have not opened.
3. Run `python3 scripts/ruling-register.py validate` and fix every error.
4. To hand the register to another tool, run `python3 scripts/ruling-register.py export`. It writes `exports/ruling-register-v<version>.json`, stamped with the commit and the date.

## How the results are measured

`python3 scripts/eval-scorecard.py` scores Fleet Sweep, the Waiver Ledger and the Ruling Register against the gold scenarios in `evals/gold-cases.json`. Each case checks the verdict, the exit code, that the fleet and app verdicts agree, and which rule ids must and must not appear, so a change that keeps the verdict but loses the reason still fails. It prints the false passes (something unsafe called ready) and the false blocks per feature, and fails on any miss or any unknown category. The false-pass count must stay at zero.

## The first entries

The first 14 entries came from an adversarial gap review of this playbook. Google Play lending in India and crypto in the EU, US medical device software and the DOJ data rule, China's AI filing and labelling rules, Indonesia's operator registration, the EU withdrawal function, DSA notice and action and CRA reporting, Vietnam's account authentication, and Australia's privacy policy, under-16 social media and Children's Online Privacy Code rules. Every source was opened on 5 November 2026. The EU withdrawal entry is marked unverified because EUR-Lex refused automated reads that day. The Australian minimum-age obligation is quoted from the Act, but the Act sets its start date by ministerial instrument and the eSafety page carrying that date did not load, so that rule is flagged to confirm rather than blocking.
