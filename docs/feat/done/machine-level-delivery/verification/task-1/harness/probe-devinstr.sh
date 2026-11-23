#!/usr/bin/env bash
# Probe 1.9: how large a multi-line `-c developer_instructions=…` value Codex
# accepts next to a profile, and which value wins in a trusted project that
# sets its own developer_instructions. No model call: `codex debug prompt-input`.
#
# Usage: KKPROBE_ROOT=<fresh dir> probe-devinstr.sh
set -uo pipefail
: "${KKPROBE_ROOT:?set KKPROBE_ROOT to a fresh directory}"
export CODEX_HOME=$KKPROBE_ROOT/home
proj=$KKPROBE_ROOT/proj
plain=$KKPROBE_ROOT/plain
mkdir -p "$CODEX_HOME" "$proj/.codex" "$plain"
(cd "$proj" && git init -q) ; (cd "$plain" && git init -q)

cat >"$CODEX_HOME/config.toml" <<EOF
[projects."$proj"]
trust_level = "trusted"
EOF
cat >"$CODEX_HOME/kkp.config.toml" <<'EOF'
developer_instructions = "KKPROBE-PROFILE-DI"
EOF
cat >"$proj/.codex/config.toml" <<'EOF'
developer_instructions = "KKPROBE-PROJECT-DI"
EOF

# Developer messages whose text contains a KKPROBE marker, with their length.
show() {
  jq -r '.[] | select(.role=="developer") | [.content[]?.text] | join("")
         | select(test("KKPROBE")) | "  marker=\(capture("(?<m>KKPROBE-[A-Z-]+)").m) chars=\(length)"'
}

# A multi-line value of N bytes as a TOML basic string with \n escapes, the
# shape kk's serialiser produces for one long string.
value_of() {
  python3 -I -c '
import json, sys
n = int(sys.argv[1])
line = "KKPROBE-ARG-DI " + "x" * 63 + "\n"
body = (line * (n // len(line) + 1))[:n]
sys.stdout.write(json.dumps(body))' "$1"
}

echo "== codex $(codex --version 2>/dev/null); $(uname -sr); getconf ARG_MAX=$(getconf ARG_MAX)"

echo; echo "== precedence, plain (untrusted, no project config) dir"
cd "$plain" || exit 1
echo "profile only:"; codex --profile kkp debug prompt-input hi 2>/dev/null | show
echo "profile + -c:"; codex --profile kkp debug prompt-input -c 'developer_instructions="KKPROBE-ARG-DI"' hi 2>/dev/null | show

echo; echo "== precedence, trusted project with its own developer_instructions"
cd "$proj" || exit 1
echo "no profile:"; codex debug prompt-input hi 2>/dev/null | show
echo "profile only:"; codex --profile kkp debug prompt-input hi 2>/dev/null | show
echo "profile + -c:"; codex --profile kkp debug prompt-input -c 'developer_instructions="KKPROBE-ARG-DI"' hi 2>/dev/null | show

echo; echo "== size, next to --profile kkp in the trusted project"
for kib in 64 96 120 124 125 126 127 128 256; do
  n=$((kib * 1024))
  v=$(value_of "$n")
  out=$(codex --profile kkp debug prompt-input -c "developer_instructions=$v" hi 2>&1)
  status=$?
  if [ $status -eq 0 ]; then
    printf '%5s KiB value (argv element %s bytes): exit 0\n' "$kib" "$(( ${#v} + 23 ))"
    printf '%s' "$out" | grep -v '^WARNING' | show
  else
    printf '%5s KiB value (argv element %s bytes): exit %s: %s\n' "$kib" "$(( ${#v} + 23 ))" "$status" \
      "$(printf '%s' "$out" | grep -v '^WARNING' | tail -1)"
  fi
done
