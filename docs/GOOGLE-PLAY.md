# Google Play Developer Program Policies. Rejection Map

Source. Google Play Developer Program Policy (play.google/developer-content-policy) and Play Console enforcement documentation (support.google.com/googleplay/android-developer). Empirical figures from Google's 2025 platform safety reporting.

Google blocked more than 1.75 million Play submissions in 2025 for policy violations and stopped over 255,000 apps from gaining excessive access to sensitive user data. The single most common rejection cause is a Data Safety declaration that does not match the app's real runtime behavior.

A critical difference from Apple. Google enforcement escalates against the developer account, not only the app. A rejection is mild, but repeated rejections, removals, or one egregious violation can suspend the account and then terminate it. After termination, registering a new account triggers immediate re termination.

## The four level enforcement ladder

| Level | What happens | Account impact | Common cause |
|---|---|---|---|
| Rejection | A new app or update is not published | None on account standing | Data Safety mismatch, crashes, broken privacy link, missing permission justification |
| Removal | The app and prior versions are taken offline | None immediately, but multiple removals lead to suspension | Repeat policy violation, false advertising in the listing |
| Suspension | The app is pulled, purchases stop, the code can no longer be used | Counts as a strike against the account | Egregious or multiple violations, repeated rejections or removals |
| Account termination | Every app removed, no new publishing, new accounts re terminated | Permanent | Malware, fraud, harm to users or devices, severe repeat violations |

## Policy categories and what triggers enforcement

### Restricted content

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Child endangerment | Any content that sexualizes or endangers minors | Zero tolerance design, proactive detection, reporting |
| Sexual content and nudity | Pornographic or sexually explicit content | Remove explicit content, gate mature content correctly |
| Hate speech | Content targeting protected groups | Moderate and remove hateful content |
| Violence and graphic content | Gore, realistic violence, glorification of harm | Remove or heavily restrict graphic content |
| Illegal activities | Promoting illegal acts, drugs, weapons sales | Remove content that promotes illegal acts |
| Real money gambling | Unlicensed gambling, outside permitted regions | License, geo restrict, follow the gambling program |
| Financial services | Unlicensed lending, deceptive financial products, personal loan disclosure gaps | Disclose APR and terms, hold licenses, follow the financial services policy |
| Health and medical | Unqualified or misleading medical claims | Substantiate claims, avoid unproven treatments |
| Blockchain and NFT | Deceptive crypto content, undisclosed risks | Disclose risk, follow gambling rules for tokenized chance |
| Unmoderated UGC | User content that contains prohibited content with no moderation | Add reporting, filtering, and blocking before launch |

### Impersonation and intellectual property

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Impersonation | Misrepresenting the developer, copying another app, false authorship | Use your own identity and original branding |
| Intellectual property | Copyright or trademark infringement, counterfeiting, plagiarism | Own or license every asset and brand reference |

### Privacy, deception, and device abuse

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| User data | Collecting personal data without clear disclosure, using data beyond stated purposes, sharing without consent, weak security | Disclose every collection and use, secure data, honor the stated purpose |
| Permissions and APIs | Requesting permissions beyond functional need, deceptive access to location, SMS, call log, contacts | Request the minimum, justify each sensitive permission |
| AccessibilityService misuse | Using accessibility APIs for data harvesting rather than accessibility | Use accessibility APIs only for genuine accessibility, declare the use |
| Background location | Background location without a clear core feature and disclosure | Use foreground location where possible, justify background use with a prominent disclosure |
| SMS and Call Log | Requesting SMS or Call Log without an approved core use case | Use the permissions declaration, drop the permission if not core |
| All files access | MANAGE_EXTERNAL_STORAGE without a qualifying use case | Use scoped storage, request all files access only when truly required |
| Health Connect | Accessing Health Connect without an appropriate use case and disclosure | Limit to declared health use, disclose in Data Safety |
| Data Safety section | A Data Safety form that does not match the app's real data behavior. This is the number one rejection cause | Audit runtime data flows and SDKs, declare every collection, sharing, and security practice accurately |
| Device and network abuse | Malware, botnets, resource hijacking, unauthorized system modification | Ship clean, well behaved code |
| Deceptive behavior and misrepresentation | False functionality claims, misleading descriptions or screenshots, fake system UI | Make the listing match the app exactly |

### SDK and target API requirements

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Third party SDKs | An SDK that violates policy through tracking, permissions, or malicious code. The developer is responsible for SDK behavior | Vet every SDK, keep them current, remove non compliant ones |
| Target API level | Failing to target the current required Android API level | Build against the current required target API before submission |

### Monetization and ads

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Payments | Deceptive billing, hidden charges, unauthorized transactions, ignoring refund rules. Play Billing required for in app digital goods, with regional alternatives where permitted | Use Play Billing for digital goods, disclose all charges |
| Subscriptions | Unclear terms, difficult cancellation, misleading trials, undisclosed auto renewal | Show full terms, easy cancellation, honest trials |
| Ads | Ads that mimic system UI, mislead, serve malware, or are intrusive and disruptive | Use compliant ad formats and placements |
| Families ads | Non compliant SDKs or behavioral advertising in apps for children | Use only Families certified ad SDKs, no behavioral ads to minors |

### Store listing and promotion

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Metadata | Spammy listings, misleading titles or descriptions, keyword stuffing, near identical repeat submissions | Write an accurate, clean listing, one app per concept |
| Ratings, reviews, installs | Fake reviews, artificial installs, incentivized reviews, rating manipulation | Never buy or incentivize ratings or installs |
| Content ratings | A missing or inaccurate content rating questionnaire | Complete the IARC content rating questionnaire honestly |

### Spam and minimum functionality

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Spam and minimum functionality | Minimal function, frequent crashes, unresponsive UI, broken features, duplicate or low effort submissions | Ship a stable app with real, working functionality |

### Malware and mobile unwanted software

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Malware | Spyware, ransomware, rootkits, credential theft, unauthorized system access | Ship clean code, scan dependencies |
| Ad fraud | Click injection, impression fraud, hidden ad networks | Use legitimate ad mediation only |
| Social engineering | Phishing, credential harvesting, deceptive permission prompts | Be honest in every prompt and flow |
| Hostile downloaders | Bundling or installing malicious software | Do not bundle or sideload other software |
| Unauthorized system imitation | Fake system alerts, spoofed dialogs, unauthorized dialer or SMS replacement | Never imitate system UI |

### Families and Designed for Families

| Policy | Triggers enforcement | Avoid by |
|---|---|---|
| Families program | Inappropriate content in child targeted apps, behavioral ads to minors, unclear parental controls, unsafe child data practices, COPPA noncompliance | Follow the Families policy, use compliant SDKs, comply with COPPA and local child law |

## The 12 tester rule for new personal accounts

New personal developer accounts created after the policy change must run a closed test with at least 12 testers for 14 consecutive days before they can apply for production access. Skipping or under populating this test blocks production. Plan the closed test window into the release schedule from day one. Organization accounts are treated differently, so the account type chosen at signup matters.

## The recurring Google failure mode

Most Google rejections are not about a forbidden feature. They are about a mismatch between what the app does and what the developer declared. The Data Safety form says no data is collected while an analytics SDK ships location. The listing promises a feature the app does not have. A permission is requested with no matching core feature. Close every one of these gaps by auditing actual runtime behavior, including every third party SDK, against every declaration before you submit.
