#!/usr/bin/env bash
# Send one prompt to the Codex TUI in a tmux session, wait until the turn ends,
# and print the new hook-log lines and the visible pane.
#
# Usage: KKPROBE_ROOT=<root> tui-send.sh <tmux-session> <tag> [timeout-seconds]
# The prompt asks the model to run `echo KKPROBE_MARKER <tag>` exactly once.
set -uo pipefail
: "${KKPROBE_ROOT:?}"
session=${1:?tmux session}
tag=${2:?tag}
limit=${3:-120}
log=$KKPROBE_ROOT/hook.log
before=0
[ -f "$log" ] && before=$(wc -l <"$log")

prompt="Run exactly this shell command once, with no changes, no retries and no other commands, then report what happened in one line: echo KKPROBE_MARKER $tag"
tmux send-keys -t "$session" -l "$prompt"
sleep 0.5
tmux send-keys -t "$session" Enter

# Poll until the turn for this tag has ended (see the check below), or time out.
waited=0
sleep 5
while [ "$waited" -lt "$limit" ]; do
  pane=$(tmux capture-pane -t "$session" -p)
  # Done only when the pane is idle and the turn for this tag has ended: the
  # text from the first mention of the tag (the prompt) on contains Codex's
  # "Worked for" line.
  after_tag=$(printf '%s\n' "$pane" | awk -v tag="KKPROBE_MARKER $tag" '!seen && index($0, tag) {seen=1} seen {print}')
  # The turn must also show a tool outcome (ran, blocked or failed hook); a
  # text-only reply would otherwise look like a finished turn.
  if ! grep -qiE 'esc to interrupt|Working' <<<"$pane" && grep -q 'Worked for' <<<"$after_tag" \
     && grep -qE '(^|• )(Ran |Blocked by hook|Hook failed)' <<<"$after_tag"; then
    break
  fi
  sleep 2; waited=$((waited + 2))
done

if [ "$waited" -ge "$limit" ]; then
  echo "-- TIMEOUT after ${limit}s: the turn had not finished; an empty hook log below is inconclusive"
fi
echo "-- new hook log lines (tag $tag):"
tail -n +"$((before + 1))" "$log" 2>/dev/null \
  | jq -c '{ts, variant, version, hook_pwd, plugin_root, cmd: .payload.tool_input.command, payload_cwd: .payload.cwd}' \
  || true
echo "-- pane:"
tmux capture-pane -t "$session" -p | grep -v '^\s*$' | tail -25
