# Functional-review run contract

Initial declaration: 2026-10-08, before launch-probe or measured results.
Task 1 probes are infrastructure checks, not behavioral acceptance runs.

## Fixed comparison

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61` (v0.23.0).
- Primary provider: Claude Code; full matrix in evaluation.md.
- Secondary provider: Codex; binding plus R1 standard, R3 isolated, I1 plan,
  I2 standalone. No full-provider-parity claim.
- Claude main: `claude-opus-4-8[1m]`, effort `high`; reviewer uses the unchanged
  baseline agent's same model declaration and inherited runtime effort.
- Codex main: `gpt-6-astra`, reasoning `xhigh`; code-reviewer:
  `gpt-6.1-sol`, reasoning `xhigh`, as declared in baseline generated TOML.
- PAL: `gemini-3.1-pro-preview`, thinking `max`, external full review, two-step
  protocol. Pin actual dispatches; no silent model substitution.
- Runtime inventory: Claude Code 2.1.278; Codex CLI 0.161.0; Capy 0.16.7;
  controller Python 3.14.8. Recheck before each capture batch.
- Repetitions: two fresh sessions per side, fixture and declared mode.
- Acceptance: every required assertion PASS in both candidate runs. FAIL,
  PARTIAL, missing traces and unavailable runtimes remain open gates. Keep every
  attempt; do not switch provider, fixture or threshold after failures.

## Inputs and evidence

`prepare-bundles.py` reads a full Git commit and preserves the selected source
trees in a controller-only archive. It records every source file's hash, every
exclusion, and every retained file/link. Both providers use the same path policy:
omit evals, oracle, grading-fixtures, verification, results and reports subtrees,
and standalone eval/expected-answer metadata. Retained bytes and executable modes
are unchanged. Links must resolve to retained files within the same bundle.
Cache verification requires exact file inventory, bytes and link semantics.
Archive inventory, blob object IDs and executable modes are independently
checked against the committed Git tree; export-ignore/export-subst cannot
silently alter the source identity. Disposable repository setup ignores global
Git configuration and inherited Git variables, disables hooks/templates and
verifies fixture bytes and worktree cleanliness.

Baseline and candidate-probe locations are distinct. The latter initially holds
another copy of the baseline solely to test loading; it is **not** a candidate
result. The actual candidate commit and source/generated hashes are pending.
Freeze a new manifest before each candidate batch, retaining previous attempts.

Task 2 owns fixture hashes, natural prompts and final seed assertions. No
measured run is permitted until those are frozen here. Grade using evaluation.md
Execution-evidence contract: contrary events FAIL, missing evidence PARTIAL,
complete required evidence PASS. Pin the concrete Task 8 grader implementation
before grading either side. A rubric change requires regrading both sides.

## Isolation and launch policy

Each probe and measured run gets a new repository outside the toolbox checkout
and any SKILL.md ancestor. Actor inputs contain only synthetic subject files,
filtered instructions and necessary runner configuration. Controller archives,
manifests, oracles and results are outside actor inputs. No resumed sessions.
Where runtime read confinement is unavailable, disclose it and audit reads;
any grading-material read invalidates the run.

Each Capy process uses `capy --project-dir <subject> serve`, an explicit local
store path, a synthetic database passphrase, and a fresh private vault path.
Remove inherited CAPY_VAULT_KEY and other Capy overrides. Knowledge starts empty;
knowledge search/index remain enabled, vault retrieval deliberately unavailable.
Main and children must use the same run-local service. Check `capy which`, verify
that indexing works, and prove A's marker is absent from B. Neither probe state
may seed a measured run. Do not alter real stores or credentials.

Claude uses `--plugin-dir`, a run-specific CPR_PLUGINS_FILE, ordinary hooks,
strict run-local MCP configuration and stream-json/hook/debug capture. Do not use
bare/safe mode. Capture host catalog identity, entry-point reads, agent identity
and hook-exported root. A root-variable override alone is not success.

Codex uses distinct local marketplace names, project enablement and the matching
generated project agents. Use supported installation/refresh, disable other kk
installations for the run, then compare installed cache with the retained
manifest. Capture effective skills and roles. Do not edit an existing installed
plugin cache. Incompatible loading or unavailable model/auth is an unrun gate.

Permission policy: subject writes and filtered instruction reads only; retain
normal hooks and tool restrictions. No deployment or production access. Exact
launch arguments and any runtime limitation are recorded with probe evidence
before those settings can be used for measured runs. A denied required tool
invalidates the corresponding coverage, rather than being worked around by
weakening the measured workflow.

## Documentation checked

- [Claude local plugin loading](https://code.claude.com/docs/en/plugins/create#load-a-plugin-for-one-session).
- [Codex local marketplaces and project enablement](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually).
- Installed CLI help is authoritative for the concrete commands exercised here.

## Open capture gates

Task 1 results and actual launch configuration are in [the verification
record](README.md), with source/cache manifests and observable host/tool traces.
The baseline archive SHA-256 is
`645174753421c14bfb525c8060c9d313b0bfa5a6f486413590444930fc937131`;
the retained manifest SHA-256 is
`0dedccb8cdb3825f3531d851b5fd83ac9938538c22a3d9c6e299a67b53edf230`.
Both loading locations used those same baseline bytes; neither is a behavioral
candidate result.

The user refreshed Claude authentication; both Claude locations passed actual
registered-skill and named-child loading. Codex persisted parent/child records
now prove named-role dispatch, exact generated role-body bytes, child reads and
run-local Capy access in both locations. See the verification record's completed
probe evidence. Codex's dispatch message field is encrypted: future assertions
about exact handoff content require plaintext capture at submission, independently
of the binding proof supplied by runtime role bytes and child tool events.

Final fixture hashes/prompts, exact measured-run tool configuration, rubric hash
and candidate identity remain pending until their respective batches. Task 1
probes do not count toward the two-run behavioral acceptance threshold.
