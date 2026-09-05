# Rules. Payments, in app purchase, subscriptions

10 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-3.1.1-EXTERNAL-PAYMENT

- Title. Digital goods sold outside in app purchase
- Platform. apple
- Guideline or policy. 3.1.1
- Severity. critical
- What triggers it. A web checkout or external payment SDK is used for digital content rather than StoreKit.
- How to fix it. Route all digital goods through StoreKit in app purchase unless the app is a documented exempt category.
- Detection signals. Stripe, PayPal, checkout, WKWebView payment, buy now
- Present means handled. StoreKit, SKProduct, Product.purchase, in app purchase

How to detect.

```bash
grep -rn 'Stripe\|PayPalCheckout\|braintree\|razorpay' --include='*.swift' . && ! grep -rn 'StoreKit\|SKProduct\|Product.purchase' --include='*.swift' .
```

## APPLE-GAMBLING-BRAZIL-LICENSE

- Title. Missing Brazilian fixed-odds betting license
- Platform. apple
- Guideline or policy. 3.1.1
- Severity. critical
- What triggers it. An app that indicates gambling/betting features but does not provide a valid fixed-odds betting license from the Secretariat of Prizes and Bets (SPA) in its App Review Information section when distributing on the Brazil storefront.
- How to fix it. Select 'Yes' to the gambling question in the age rating questionnaire (which automatically sets the Brazil age rating to A18), provide a valid fixed-odds betting license from the Secretariat of Prizes and Bets (SPA) in the App Review Information field, and submit a new app version for verification. A new app version must be submitted to start licence verification, editing App Review Information alone does not (Apple Developer news x4eyetnp, 8 May 2026).
- Detection signals. gambling, fixed-odds betting, Secretariat of Prizes and Bets, SPA license

How to detect.

```bash
grep -rni 'gambling\|fixed-odds\|betting' --include='*.swift' .   # then verify the SPA license is provided in App Review Information for Brazil storefront
```

## GOOGLE-PLAY-BILLING

- Title. Digital goods sold without Play Billing
- Platform. google
- Guideline or policy. Payments
- Severity. critical
- What triggers it. A web checkout or third party payment SDK is used for in app digital goods rather than Play Billing.
- How to fix it. Use Play Billing for in app digital goods, with regional alternatives only where Google permits.
- Detection signals. Stripe, PayPal, checkout, razorpay
- Present means handled. BillingClient, Play Billing, com.android.billingclient

How to detect.

```bash
grep -rn 'Stripe\|PayPal\|razorpay' --include='*.kt' --include='*.java' . && ! grep -rn 'BillingClient\|com.android.billingclient' .
```

## APPLE-3.1.2-MISLEADING-PRICING

- Title. Subscription shows the per month price more prominently than the billed amount
- Platform. apple
- Guideline or policy. 3.1.2
- Severity. high
- What triggers it. Manual paywall check. An annual subscription shows a small per month figure large and the actual billed total small.
- How to fix it. Show the actual amount the user will be charged at least as prominently as any per month figure. Source. truongduy2611 misleading_pricing rule.

How to detect.

```bash
python3 scripts/metadata-audit.py ./metadata
```

## APPLE-RESTORE-PURCHASES-MISSING

- Title. Non consumable purchase without a Restore Purchases control
- Platform. apple
- Guideline or policy. 3.1.1
- Severity. high
- What triggers it. StoreKit purchases are present but no restore path is found.
- How to fix it. Add a visible Restore Purchases control. It is required for non consumables and non renewing subscriptions.
- Detection signals. SKProduct, Product.purchase, StoreKit
- Present means handled. restorePurchases, restoreCompletedTransactions, AppStore.sync, Restore Purchases

How to detect.

```bash
grep -rn 'SKProduct\|Product.purchase\|StoreKit' --include='*.swift' . && ! grep -rn 'restorePurchases\|restoreCompletedTransactions\|AppStore.sync' --include='*.swift' .
```

## BOTH-LOOTBOX-ODDS

- Title. Random reward mechanic without disclosed odds
- Platform. both
- Guideline or policy. Apple 3.1.1, Google gambling
- Severity. high
- What triggers it. Loot box, gacha, or random reward purchase present without odds disclosed before purchase.
- How to fix it. Disclose the odds for every random reward before the user purchases.
- Detection signals. lootbox, loot box, gacha, random reward, mystery box

How to detect.

```bash
grep -rni 'lootbox\|loot box\|gacha\|mystery box\|random reward' .
```

## BOTH-SUBSCRIPTION-HARD-CANCEL

- Title. Subscription cancellation requires a phone call, mail, or in-person visit while sign-up is a single tap
- Platform. both
- Guideline or policy. Apple 3.1.2 subscription terms, US FTC Section 5 / ROSCA, state subscription-cancellation statutes (California, New York, Massachusetts)
- Severity. high
- What triggers it. A subscription billed outside Apple in-app purchase or Google Play Billing (a web or account-settings cancellation path) directs the person to call, mail, or visit in person to cancel, instead of a self-service in-app or web cancel action. The federal FTC click-to-cancel rule was vacated in 2025 but California, New York, and Massachusetts have their own negative-option statutes in force, and the FTC retains Section 5 and ROSCA authority regardless.
- How to fix it. Provide a self-service cancellation path (in-app button or account-settings web page) that is at least as easy as sign-up. Never require a phone call, a mailed letter, or an in-person visit to cancel a subscription billed outside the app stores' own billing.
- Detection signals. call us to cancel, call to cancel, cancel your subscription by calling, mail a letter to cancel, write to cancel, cancel in person, visit a store to cancel

How to detect.

```bash
grep -rniE 'subscri(be|ption)|auto.renew|membership' --include='*.swift' --include='*.kt' --include='*.java' --include='*.html' --include='*.md' . 2>/dev/null | grep -iE 'call.{0,25}cancel|cancel.{0,25}call|mail.{0,25}cancel|write.{0,25}cancel|cancel.{0,15}(in.person|by.phone|by.mail)'
```

## BOTH-WITHDRAWAL-BUTTON-MISSING

- Title. Prominent contract withdrawal button or function missing for EU consumer contracts
- Platform. both
- Guideline or policy. Apple Guideline 3.1.2, Directive (EU) 2023/2673 Distance Marketing of Financial Services Directive
- Severity. high
- What triggers it. Apps offering digital subscriptions or distance contracts to EU consumers that fail to provide a prominent, easily accessible 'withdrawal button' or 'withdrawal function' on their online user interface to cancel/withdraw within 14 days.
- How to fix it. Add a prominent, dedicated, and easily accessible withdrawal button or function on the user interface, allowing consumers to withdraw from contracts/subscriptions without undue friction.
- Detection signals. withdrawal button, withdrawal function, withdraw from contract, distance contract withdrawal, revoke contract, cancel subscription

How to detect.

```bash
grep -rniE 'withdrawal button|withdrawal function|withdraw from contract|distance contract' . 2>/dev/null
```

## APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING

- Title. External purchase link shown on every storefront
- Platform. apple
- Guideline or policy. 3.1.1 and 3.1.3 external purchase links. US-storefront carve-out only (Apple guideline update 1 May 2025, developer.apple.com/news/?id=9txfddzf)
- Severity. high
- What triggers it. An external purchase link, button, or call to action ships to all regions. The no-entitlement carve-out applies to the United States storefront only. The same UI is still a 3.1.1 violation in Japan, Canada, Australia, the UK, and most other storefronts, and App Review evaluates per region. Developers report budgeting two rejection rounds for this in 2026.
- How to fix it. Gate the external link UI on the current storefront (StoreKit Storefront.current, countryCode) and show it only where you hold the entitlement or the US carve-out applies. Outside the US keep the entitlement path and the disclosure sheet.
- Detection signals. ExternalPurchaseLink, ExternalLink, external-purchase-link, openExternalPurchaseLink
- Present means handled. Storefront, storefront, countryCode

How to detect.

```bash
grep -rqn 'ExternalPurchaseLink\|external-purchase-link\|openExternalPurchaseLink' . && ! grep -rqn 'Storefront\|storefront\|countryCode' .
```

## ANDROID-RESTORE-CREDENTIALS-REQUIRED

- Title. Sign-in state not restored on a new device
- Platform. google
- Guideline or policy. Play Console technical quality requirements, Zero-Tap Sign-In (Play Console Help answer 17492799)
- Severity. medium
- What triggers it. From April 2027 any app with user sign-in, optional or mandatory, must restore the sign-in state when the user moves to a new Android device using the Restore Credentials API. Games are currently out of scope. An app with a login flow and no RestoreCredential integration will miss the requirement.
- How to fix it. Create a restore credential on successful sign-in through Credential Manager, restore it on first launch after device transfer, and clear it on sign-out.
- Detection signals. signInWith, CredentialManager, FirebaseAuth, LoginActivity
- Present means handled. RestoreCredential, createRestoreCredential

How to detect.

```bash
grep -rqn 'signInWith\|CredentialManager\|FirebaseAuth\|LoginActivity' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' . && ! grep -rqn 'RestoreCredential' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' .
```
