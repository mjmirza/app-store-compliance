#!/usr/bin/env bash
# Proves check-docs.py fails on each kind of broken instruction and passes a clean tree.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }
CHECK="$PWD/scripts/check-docs.py"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/docs" "$T/scripts" "$T/assets"
printf '#!/usr/bin/env bash\necho ok\n' > "$T/scripts/install.sh"
printf 'import argparse\np = argparse.ArgumentParser()\np.add_argument("--files")\n' > "$T/scripts/tool.py"
printf '# Guide\n\n## First step\n\ntext\n' > "$T/docs/GUIDE.md"
: > "$T/assets/a.png"
run() { DOCS_ROOT="$T" python3 "$CHECK" 2>&1; }
expect_fail() {
  printf '%s\n' "$2" > "$T/README.md"
  OUT="$(run)"; RC=$?
  [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "$3" && ok "$1" || bad "$1 (rc=$RC)"
}

printf '# T\n\n[guide](docs/GUIDE.md#first-step) and `docs/GUIDE.md`.\n\n<img src="assets/a.png" alt="a" />\n\n```\npython3 scripts/tool.py --files docs/\n```\n' > "$T/README.md"
OUT="$(run)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "0 problem" && ok "a clean tree passes" || bad "a clean tree passes (rc=$RC)"

expect_fail "a link to a missing file fails" '[x](docs/NOPE.md)' "docs/NOPE.md"
expect_fail "a link to a missing heading fails" '[x](docs/GUIDE.md#no-such-part)' "no-such-part"
expect_fail "a missing image fails" '<img src="assets/gone.png" alt="x" />' "assets/gone.png"
expect_fail "a path named in prose that does not exist fails" 'Open `docs/MISSING.md` first.' "docs/MISSING.md"
expect_fail "a command naming a missing script fails" 'Run `python3 scripts/absent.py`.' "scripts/absent.py"
expect_fail "a flag the script does not accept fails" 'Run `python3 scripts/tool.py --nope docs/`.' "\-\-nope"

printf '# T\n\nSee https://example.org/docs/NOPE.md and `~/other/docs/x.md`.\n' > "$T/README.md"
OUT="$(run)"; RC=$?
[ "$RC" -eq 0 ] && ok "a web URL and a path outside the repo are left alone" || bad "a web URL and a path outside the repo are left alone (rc=$RC)"

printf '# T\n\n[x](<docs/GUIDE.md#first-step>) and [y][g].\n\n[g]: docs/GUIDE.md\n' > "$T/README.md"
OUT="$(run)"; RC=$?
[ "$RC" -eq 0 ] && ok "an angle-bracket link and a reference link to real files pass" || bad "an angle-bracket link and a reference link to real files pass (rc=$RC)"
expect_fail "a reference link to a missing file fails" "$(printf '[y][g]\n\n[g]: other/NOPE.md\n')" "other/NOPE.md"

OUT="$(python3 "$CHECK" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ok "the real repository passes" || bad "the real repository passes (rc=$RC)"

echo ""
echo "check-docs-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
