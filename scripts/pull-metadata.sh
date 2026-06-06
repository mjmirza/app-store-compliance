#!/usr/bin/env bash
# Pull live store metadata into ./metadata so metadata-audit.py can inspect the
# real listing, not only the source.
#
# Apple (asc CLI):
#   APP_ID=123456789 VERSION=1.2.0 bash pull-metadata.sh apple
#
# Google Play (Play Developer API, real pull):
#   PACKAGE_NAME=com.example.app bash pull-metadata.sh google
#   Auth: set GOOGLE_ACCESS_TOKEN, or have gcloud authenticated (the script will
#   call gcloud auth print-access-token). The service account or user must have
#   the Play Developer API enabled and access to the app.
#
# Then audit:
#   python3 scripts/metadata-audit.py ./metadata
set -uo pipefail
DIR="${DIR:-./metadata}"
target="${1:-apple}"

case "$target" in
  apple)
    if ! command -v asc >/dev/null 2>&1; then
      echo "asc CLI not found. Install with: brew install asc"
      echo "Then authenticate asc with your App Store Connect API key (issuer id, key id, .p8)."
      exit 1
    fi
    : "${APP_ID:?set APP_ID to your App Store Connect app id}"
    : "${VERSION:?set VERSION to the app version, e.g. 1.2.0}"
    mkdir -p "$DIR"
    echo "Pulling Apple metadata for app $APP_ID version $VERSION into $DIR"
    asc metadata pull --app "$APP_ID" --version "$VERSION" --dir "$DIR"
    echo "Done. Now run: python3 scripts/metadata-audit.py $DIR"
    ;;

  google|play)
    : "${PACKAGE_NAME:?set PACKAGE_NAME to your app package, e.g. com.example.app}"
    command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }
    command -v python3 >/dev/null 2>&1 || { echo "python3 is required"; exit 1; }
    TOKEN="${GOOGLE_ACCESS_TOKEN:-}"
    if [ -z "$TOKEN" ]; then
      if command -v gcloud >/dev/null 2>&1; then
        TOKEN="$(gcloud auth print-access-token 2>/dev/null)"
      fi
    fi
    if [ -z "$TOKEN" ]; then
      echo "No access token. Set GOOGLE_ACCESS_TOKEN or authenticate gcloud."
      echo "The token needs the androidpublisher scope and access to $PACKAGE_NAME."
      exit 1
    fi
    BASE="https://androidpublisher.googleapis.com/androidpublisher/v3/applications/$PACKAGE_NAME"
    mkdir -p "$DIR"
    echo "Creating a Play edit for $PACKAGE_NAME"
    EDIT="$(curl -fsS -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" "$BASE/edits" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("id",""))')"
    if [ -z "$EDIT" ]; then echo "Failed to create edit. Check token and package access."; exit 1; fi
    echo "Edit $EDIT. Fetching listings."
    LISTINGS="$(curl -fsS -H "Authorization: Bearer $TOKEN" "$BASE/edits/$EDIT/listings")"
    echo "$LISTINGS" | python3 - "$DIR" <<'PYIN'
import json, os, sys
dir = sys.argv[1]
data = json.load(sys.stdin)
for l in data.get("listings", []):
    lang = l.get("language", "default")
    d = os.path.join(dir, lang); os.makedirs(d, exist_ok=True)
    if l.get("title"): open(os.path.join(d,"name.txt"),"w").write(l["title"])
    if l.get("shortDescription"): open(os.path.join(d,"short_description.txt"),"w").write(l["shortDescription"])
    if l.get("fullDescription"): open(os.path.join(d,"full_description.txt"),"w").write(l["fullDescription"])
    print("wrote", lang)
PYIN
    echo "Deleting the edit (read only pull, nothing committed)."
    curl -fsS -X DELETE -H "Authorization: Bearer $TOKEN" "$BASE/edits/$EDIT" >/dev/null || true
    echo "Note. The Play privacy policy URL and Data Safety form are not in the listings API. Add the privacy policy URL to $DIR/meta.json as {\"privacy_policy_url\":\"...\"} and verify Data Safety in the Play Console."
    echo "Done. Now run: python3 scripts/metadata-audit.py $DIR"
    ;;
  *)
    echo "Usage: pull-metadata.sh [apple|google]"
    exit 1
    ;;
esac
