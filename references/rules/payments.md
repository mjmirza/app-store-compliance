# Rules. Payments, in app purchase, subscriptions

5 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

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
