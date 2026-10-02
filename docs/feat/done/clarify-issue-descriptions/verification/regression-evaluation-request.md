Coordinate the required Task 1 smoke regressions dense-source (1) and runtime-pr
(12) using the final Task 1 instruction snapshot supplied by the parent. You own
only evidence under docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/regressions/
and staging under /tmp/clarify-issue-task1/regressions/. You are not alone in the
workspace; do not modify production files, eval specs, or other contributors' work.

Read klaude-plugin/skills/clarify-docs/evals/README.md in full before staging, then
the two eval.json and oracle/expected.json files. Follow their unchanged assertions.
Stage only test-files/ contents outside any SKILL.md ancestor. For runtime-pr create
the actual local Git base/head revisions described in README, record SHAs/diff, and
exclude snapshots from editor access. No tracker network calls or external writes.

Follow the feature's manual Execution and evidence protocol: exact prompts saved
BEFORE dispatch, full allowed-file manifests, instruction/input/output hashes,
before/after artifacts, actual session settings and complete tool traces. Spawn
independent general-purpose editor, original-reader and revised-reader sessions
with fork_turns=none, no model overrides. Only the named frozen instructions may
be loaded; the installed older clarity skill must not substitute. Editors receive
only their instructions, exact eval prompt and neutral stage/read-write manifest.
Readers see only their respective artifact and oracle-declared reading path, with
identical fixed questions/settings. Neither editors nor readers see the oracle,
eval specs, other runs or grading. Do not prime the intended answers.

A separate general-purpose fixture-capable grader receives oracles, artifacts,
source evidence, reader answers and actual tool traces; never use the eval-grader
role. Audit all file reads/writes against manifests. Missing trace evidence or
leaked oracle content invalidates the run. Every assertion receives PASS/FAIL/PARTIAL
with evidence. Preserve failures and report them to the parent; do not weaken the
scenario. Capture trace data from the sessions' rollout JSONL files under
/Users/sergio/.codex/sessions/, preserving actual tool calls/results and visible
messages but excluding hidden reasoning and system boilerplate. Capture plaintext
prompts before spawn; do not reconstruct encrypted transport prompts later.

Use native apply_patch for authored records and cp for snapshots/raw transcripts.
Keep at most one child active at a time because issue evaluations run concurrently.
Summarize results and trace/manifest audit in run.md in your evidence directory.
Do not change parent tasks.md. This is an explicitly required independent manual
evaluation from the active /kk:implement plan, not implementation delegation.
