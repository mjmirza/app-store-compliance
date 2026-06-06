# Review Notes Template

Most recoverable App Store rejections come down to incomplete review notes. Copy the block below into the App Review Information notes field in App Store Connect, or into `metadata/review_information/notes.txt` for fastlane, and fill every section before you submit. All six sections matter for a new submission.

Adopted from the open source app-store-preflight-skills project (MIT), credited in `docs/CREDITS.md`.

```text
1. SCREEN RECORDING
Demo video URL: <paste link to a screen recording captured on a physical device>
The recording shows:
- App launch and onboarding
- Core feature 1
- Core feature 2
- Account registration, login, and account deletion (if the app has accounts)
- Purchase or subscription flow (if the app sells anything)
- User generated content posting, reporting, and blocking (if the app has UGC)
- Every permission prompt the app shows (location, camera, microphone, contacts)

2. APP PURPOSE
Problem it solves: <one or two sentences>
Value it provides: <who it is for and why it helps>

3. ACCESS INSTRUCTIONS AND TEST CREDENTIALS
Steps to reach the core features: <numbered steps>
Test account username: <demo_username>
Test account password: <demo_password>
Note: this account stays active and free of 2FA until <date at least two weeks out>.

4. EXTERNAL SERVICES
Service / Purpose
<e.g. Firebase Auth / user authentication>
<e.g. Stripe / payment processing>
<e.g. OpenAI API / AI feature>
<e.g. AWS S3 / media storage>

5. REGIONAL DIFFERENCES
<Either> This app works the same in every region.
<Or> These features vary by region: <list region and difference>

6. REGULATED INDUSTRY DOCUMENTATION (only if applicable)
<For health, finance, gambling, insurance, or legal apps, attach or link the licenses, permissions, or authorizations that let you operate.>
```

## For an app update

An update needs less, but it needs the right thing. State exactly what changed, and attach a screenshot of any new feature, any new purchase or restore or delete account control, and anything a reviewer must see to clear compliance. Keep the What's New text accurate per localization.
