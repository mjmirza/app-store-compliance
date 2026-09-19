#!/usr/bin/env bash
# Runs every policy monitor test suite and fails if any of them fails.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

status=0
for t in monitor-ai-policy monitor-android monitor-security monitor-privacy monitor-simulated-notice; do
  if bash "scripts/${t}-test.sh"; then
    echo "OK    ${t}"
  else
    echo "FAIL  ${t}"
    status=1
  fi
done
exit "$status"
