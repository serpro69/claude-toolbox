#!/bin/bash
# Test-only interpreter stand-in. Never evaluates the submitted tool command.
[[ "$1" == -I ]] || exit 90
[[ "$2" == -S ]] || exit 90
shift 2
if [[ "$1" == -c ]]; then
    [[ "$GUARD_FIXTURE_MODE" != broken ]]
    exit $?
fi
case "$GUARD_FIXTURE_MODE" in
    payload) cmp -s - "$GUARD_EXPECTED_INPUT" ;;
    warning) printf '%s\n' '{"systemMessage":"invalid test config"}' ;;
    broken) exit 127 ;;
    missing-capture) rm -f -- "$GUARD_CAPTURE_DIR"/kk-guard.*/"$GUARD_CAPTURE_STREAM" ;;
    crash) printf 'partial engine output\n'; exit 1 ;;
    signal) kill -TERM "$$" ;;
    stdin-error)
        # Exercise the real engine's read outside main's try block.
        exec "$GUARD_TEST_PYTHON" -I -S -c '
import runpy, sys
engine = runpy.run_path(sys.argv[1])
sys.stdin.close()
engine["main"]()
' "$1" ;;
    emitter-error)
        # Exercise an actual BrokenPipeError outside the engine's recovery.
        exec "$GUARD_TEST_PYTHON" -I -S -c '
import runpy, sys
engine = runpy.run_path(sys.argv[1])
class BrokenOutput:
    def write(self, value):
        raise BrokenPipeError("test emitter failure")
    def flush(self):
        pass
sys.stdout = BrokenOutput()
engine["main"]()
' "$1" ;;
    malformed) printf 'not JSON\n' ;;
    malformed-deny) printf 'not JSON\n'; printf 'reason\n' >&2; exit 2 ;;
    empty-deny) exit 2 ;;
    no-stderr)
        printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"test denial"}}'
        exit 2 ;;
    multi-json) printf '%s\n' '{"systemMessage":"one"}' '{"systemMessage":"two"}' ;;
    allow-decision)
        printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}' ;;
    *) exit 91 ;;
esac
