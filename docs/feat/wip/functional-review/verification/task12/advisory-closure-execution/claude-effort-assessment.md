# Claude reviewer effort: preflight blocker

> Date: 2026-10-17
> Scope: the four completed Task 12.21 bindings; no replacement probe or runtime change
> Disposition: keep Claude child effort unverified; do not attest overall preflight PASS

## Observed evidence

The frozen contract declares Claude parent and named reviewer at high effort.
Both captured parent commands use `--effort high`. Both captured child results
resolve the intended `claude-opus-5-5` model. Codex's public thread/activity
metadata separately confirms its declared parent/child xhigh settings.

The frozen Claude agent definitions differ: baseline `code-reviewer.md` has no
effort field; candidate declares `effort: xhigh`. The inherited capture launcher
forces the child model through `CLAUDE_CODE_SUBAGENT_MODEL` and
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, but does not pin or record a child-effort
override. Its `command.json` model-environment record contains only those two
model keys. The launch metadata therefore cannot establish matching child effort.

No resolved child-effort field exists in the retained public event structures;
the only effort-related field is the initialization's boolean
`per_turn_effort_active`. The captured Agent calls supply no effort parameter.
A bounded lookup of the known owned subagent transcript/task-output paths found
them absent. No private reasoning or unrelated session history was read or copied.
The current shell does not expose `CLAUDE_CODE_EFFORT_LEVEL`; that observation
does not prove its state in an earlier launched process.

## Authoritative configuration rule

The installed Claude Code 2.1.296 help describes `--effort` as a current-session
setting. Its [official subagent documentation](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level)
states that a definition's effort takes precedence over the session setting, a
per-invocation effort can override the definition, and `CLAUDE_CODE_EFFORT_LEVEL`
takes precedence over both. The [environment reference](https://code.claude.com/docs/en/env-vars)
also documents that variable's precedence over the CLI effort flag. These public
sources were checked on 2026-10-17; they are configuration evidence, not telemetry
for the completed probes.

Consequently the parent flag and model-force variables are insufficient to prove
the declared child setting. Under documented precedence, the candidate definition
selects xhigh unless a higher-priority override applies. The captured evidence does
not establish such an override, so do not claim the candidate actually ran high or
assert an unobserved effective value as fact.

## Concrete follow-up

Owner: implementing agent. Prepare a separately reviewed successor runtime that
enforces the already-declared high effort at the Claude process-launch boundary
and records that selected environment alongside the model settings. A supported
candidate mechanism is `CLAUDE_CODE_EFFORT_LEVEL=high`, verified against the
installed runtime before implementation. Preserve both frozen actor bundles and
all current evidence; do not edit an agent's source merely to make the probe pass.

The successor must consistently govern binding and later measured launches, pin
its changed configuration/adapter identity and declare how existing calibration
evidence relates to that change. Run fresh affected Claude baseline/candidate
bindings under that reviewed declaration. Do not reuse the current Claude captures
as proof of the corrected configuration or silently revise this freeze. Keep the
good Codex/state observations with their actual source/configuration identity.

No replacement attempt is selected or executed by this assessment. The source,
instruction-receipt, state-isolation and cleanup evidence remains useful; it does
not close the missing runtime-policy condition. No measured comparison, adoption,
historical regrading or acceptance waiver follows.
