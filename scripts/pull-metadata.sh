#!/usr/bin/env bash
# Pull live store metadata into ./metadata so metadata-audit.py can inspect the
# real listing, not only the source. Apple uses the asc CLI. Google Play has no
# one line CLI pull, so this prints the API path to use.
#
# Apple usage:
#   APP_ID=123456789 VERSION=1.2.0 bash pull-metadata.sh apple
#   needs: brew install asc, and asc auth set up with your App Store Connect API key
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
    echo "Google Play has no single CLI pull. Two options."
    echo "1. Export the store listing fields from the Play Console and drop them as .txt files in $DIR (name.txt, short_description.txt, full_description.txt) plus a meta.json with privacy_policy_url."
    echo "2. Use the Google Play Developer API edits.listings.get endpoint to fetch the listing, then write the fields into $DIR."
    echo "Then run: python3 scripts/metadata-audit.py $DIR"
    ;;
  *)
    echo "Usage: pull-metadata.sh [apple|google]"
    exit 1
    ;;
esac
