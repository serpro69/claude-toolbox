#!/usr/bin/env bash
# Probe 1.6 (assumption 5): precedence of `--profile kkp` against the base user
# config and a trusted project's config, with every key the baseline would carry
# (taken from this repository's .codex/config.toml, MCP entries excluded) plus
# the three opt-in keys. No model call.
#
# Usage: KKPROBE_ROOT=<fresh dir> probe-profile.sh
set -uo pipefail
: "${KKPROBE_ROOT:?set KKPROBE_ROOT to a fresh directory}"
export CODEX_HOME=$KKPROBE_ROOT/home
trusted=$KKPROBE_ROOT/trusted-proj
untrusted=$KKPROBE_ROOT/untrusted-proj
plain=$KKPROBE_ROOT/plain
mkdir -p "$CODEX_HOME" "$trusted/.codex" "$untrusted/.codex" "$plain"
for d in "$trusted" "$untrusted" "$plain"; do (cd "$d" && git init -q); done

# Base user config: a different value for every key.
cat >"$CODEX_HOME/config.toml" <<EOF
model = "user-model"
model_reasoning_effort = "low"
model_context_window = 111111
model_auto_compact_token_limit = 111111
project_doc_max_bytes = 1111
approval_policy = "never"
approvals_reviewer = "user"
sandbox_mode = "danger-full-access"
developer_instructions = "USER-DI"

[features]
hooks = false

[agents]
max_threads = 1
max_depth = 2

[tui]
status_line = ["current-dir"]
terminal_title = ["project"]
whimsy = true
animations = true

[projects."$trusted"]
trust_level = "trusted"
EOF

# The profile: every baseline key with the template's values, plus the opt-ins.
cat >"$CODEX_HOME/kkp.config.toml" <<'EOF'
model = "gpt-6.2-astra"
model_reasoning_effort = "xhigh"
model_context_window = 1000000
model_auto_compact_token_limit = 1000000
project_doc_max_bytes = 65536
approval_policy = "on-request"
approvals_reviewer = "user"
sandbox_mode = "read-only"
developer_instructions = "PROFILE-DI"

[features]
hooks = true

[agents]
max_threads = 6
max_depth = 1

[tui]
status_line = ["model-with-reasoning", "current-dir", "git-branch", "context-used", "used-tokens", "weekly-limit", "approval-mode", "session-id"]
terminal_title = ["project", "git-branch", "status", "thread", "task-progress"]
whimsy = false
animations = false
EOF

# A project config that sets a subset of the keys.
for d in "$trusted" "$untrusted"; do
  cat >"$d/.codex/config.toml" <<'EOF'
model = "project-model"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"
developer_instructions = "PROJECT-DI"

[agents]
max_threads = 3
EOF
done

# `codex app-server` rejects --profile on 0.170.0, and a legacy `profile = "…"`
# config key is an error, so config/read cannot show the profile layer. Read the
# effective values instead from the header `codex exec` prints before its model
# call (no credentials needed: the call fails after the header), and the
# sandbox/approval text in `codex debug prompt-input` (the interactive path).
# With approval_policy = never the prompt says "Approval policy is currently
# never"; with on-request it instead explains how to request approval for
# commands that need escalated privileges.
hdr() {
  (cd "$1" && shift && timeout 8 codex "$@" exec --skip-git-repo-check x </dev/null 2>&1 \
    | grep -E '^(model|approval|sandbox|reasoning effort):' | tr '\n' ' ')
  echo
}
perm() {
  (cd "$1" && shift && codex "$@" debug prompt-input hi 2>/dev/null \
    | jq -r '.[] | select(.role=="developer") | [.content[]?.text] | join("")' \
    | grep -oE 'sandbox_mode` is `[a-z-]+`|Approval policy is currently [a-z-]+|To request approval to execute a command that will require escalated privileges' \
    | sort -u | tr '\n' '|')
  echo
}
di() {
  (cd "$1" && shift && codex "$@" debug prompt-input hi 2>/dev/null \
    | jq -r '.[] | select(.role=="developer") | [.content[]?.text] | join("")' \
    | grep -oE '(USER|PROFILE|PROJECT)-DI' | sort -u | tr '\n' ' ')
  echo
}

echo "== codex $(codex --version 2>/dev/null)"
for case in "plain:" "plain:--profile kkp" "untrusted-proj:--profile kkp" "trusted-proj:--profile kkp"; do
  d=${case%%:*}; a=${case#*:}
  echo "== $d, ${a:-no profile}"
  # shellcheck disable=SC2086
  printf '  exec header:  %s\n' "$(hdr "$KKPROBE_ROOT/$d" $a)"
  # shellcheck disable=SC2086
  printf '  prompt-input: %s\n' "$(perm "$KKPROBE_ROOT/$d" $a)"
  # shellcheck disable=SC2086
  printf '  developer_instructions source: %s\n' "$(di "$KKPROBE_ROOT/$d" $a)"
done

echo; echo "== negative controls: does a profile reject bad values?"
cp "$CODEX_HOME/kkp.config.toml" "$CODEX_HOME/bad1.config.toml"
sed -i 's/model_reasoning_effort = "xhigh"/model_reasoning_effort = "bogus"/' "$CODEX_HOME/bad1.config.toml"
cp "$CODEX_HOME/kkp.config.toml" "$CODEX_HOME/bad2.config.toml"
sed -i 's/max_threads = 6/max_threads = "six"/' "$CODEX_HOME/bad2.config.toml"
cp "$CODEX_HOME/kkp.config.toml" "$CODEX_HOME/bad3.config.toml"
printf 'totally_unknown_key = 1\n' >>"$CODEX_HOME/bad3.config.toml"
for p in kkp bad1 bad2 bad3; do
  (cd "$plain" && codex --profile "$p" debug prompt-input hi >/dev/null 2>"$KKPROBE_ROOT/$p.err")
  printf '  %s: exit=%s %s\n' "$p" "$?" "$(grep -v 'WARNING: proceeding' "$KKPROBE_ROOT/$p.err" | head -1)"
done
printf '  bad1 effective effort: %s\n' "$(hdr "$plain" --profile bad1)"
