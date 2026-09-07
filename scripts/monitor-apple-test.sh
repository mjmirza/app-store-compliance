#!/usr/bin/env bash
# Test runner for Apple requirements compliance monitor (monitor.py)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$HERE/monitor-test.sh"
