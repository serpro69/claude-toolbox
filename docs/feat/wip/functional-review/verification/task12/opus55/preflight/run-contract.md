# Opus 5.5 matrix: runtime preflight

Declared 2026-10-11 before new model launches. The user requested the full
functional-review matrix on Claude and Codex, all applicable modes, with two
fresh repetitions on each baseline/candidate side. This supersedes the earlier
R5-only scope and ordering-experiment stop; it does not authorize actor fixes.
The user explicitly retained the PAL deferral. Synthetic R8 report replays
remain in scope; unavailable live PAL receipt/use never counts as PASS.

This preliminary contract covers instruction-loading probes only, using the
existing reviewed successor transport. No probe is a behavioral measurement.
Freeze the final matrix controller and declaration separately before measured
runs. Preserve all old evidence and these probe attempts.

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate: `581dd0e11455398cb73e3d6ae5542854c016fe7f`.
- Claude Code 2.1.272: main and forced subagent `claude-opus-5-5`, high effort.
- Codex 0.162.1: main `gpt-6-astra`/xhigh; selected generated reviewer
  `gpt-6.1-sol`/xhigh. No model fallback.
- Capy 0.16.8; controller Python 3.12.11; actor Python 3.10.12; Linux.
- Existing tool policy, private unavailable vault, fresh empty run-local
  knowledge, filtered immutable bundles, credential redaction and sealed public
  evidence. No oracle or controller paths in actor inputs.
- The existing revision-2 rubric and pinned grader remain unchanged. Measured
  acceptance still requires every required candidate assertion to PASS twice;
  deferred PAL components and unknown evidence remain explicitly incomplete.

Expected core coverage is 192 sessions: 24 case/mode combinations, two
providers, two sides and two repetitions. Binding probes, grader calibration
and retained legacy controls are additional checks, never substitutes for these
sessions. Owner: implementing agent. On runtime failure, retain the failure,
complete independent preparation, and record the missing prerequisite and exact
resume action rather than claiming execution or acceptance.
