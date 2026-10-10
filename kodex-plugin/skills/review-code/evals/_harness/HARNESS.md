# review-code eval harness — playbook

This playbook describes controller orchestration when the user asks to run review-code evals. Read the playbook and selected grading instructions before staging, dispatching or grading. The scripts in this directory are plumbing.

## Select the evaluation mode

- **Component:** resolver/reviewer output assertions use the existing three-agent procedure below. Omit `Grading mode` or set it to `component`. This measures output text, not actual instruction order or handoffs.
- **Workflow:** assertions about execution order, independent dispatches or resulting files use [the workflow procedure](#workflow-procedure). Explicitly set `Grading mode: workflow`. Launch the registered skill normally; a directly prompted reviewer is not a full workflow run.

Keep assertions, oracles, grading fixtures and retained results outside actor inputs in both modes. The calibration records in [grading-fixtures/README.md](grading-fixtures/README.md) are controller/grader inputs only.

## Why this exists

The prior harness pattern had three structural weaknesses:

1. **Self-grading** — each reviewer sub-agent graded its own output.
2. **Rubric leakage** — reviewers saw the eval's `assertions` / `trap` while producing the review, which primes the model toward satisfying them.
3. **Fixture-only diff** — "diff scope" was enumerated in the prompt; no real `git diff` was performed, so scope-discovery was tested by instruction, not by git.

This playbook fixes all three. Multi-model sampling is deliberately deferred.

## Component roles

This harness uses three sub-agents per eval, each with a narrowly scoped input, matching the real `$kk:review-code` invocation path:

- **Orchestrator** — the agent reading this playbook. Runs `setup.sh`, captures `git diff`, spawns the three sub-agents per eval, aggregates. Has full context (including assertions).
- **Profile resolver** — a `kk:profile-resolver` sub-agent, one per eval. Receives only the diff text + worktree root. Runs the shared profile-detection procedure. Emits a structured resolution (active profiles, per-file `triggered_by`, loaded/not-loaded checklists with Load-if reasoning). Does NOT see assertions, user intent, or fixture files beyond what the procedure inspects.
- **Reviewer** — a `kk:code-reviewer` sub-agent, one per eval. Receives exactly the contract it is designed for in isolated mode: the diff, the pre-resolved `(profile, checklist)` list from the profile resolver, and any spec context. Applies checklists, emits findings. Does NOT redo detection.
- **Grader** — a `kk:eval-grader` sub-agent, one per eval. Receives the profile resolver's output AND the reviewer's output, plus the eval's `assertions`. Grades each assertion against whichever artifact is relevant (routing assertions against resolver output; content/finding assertions against reviewer output). Does NOT see the fixture, the worktree, or any of the skill's source files.

**Why three agents.** Splitting detection from review mirrors the real isolated-mode invocation: the main session resolves profiles, then hands `kk:code-reviewer` a pre-resolved list (see `klaude-plugin/agents/code-reviewer.md`'s "Active profiles and resolved checklists" contract). The orchestrator could resolve profiles inline, but doing so would (a) contaminate the orchestrator's context with every profile's `DETECTION.md` for every run, and (b) leak the orchestrator's knowledge of the eval assertions into the detection output. Delegating to `kk:profile-resolver` isolates detection structurally. The same agent is intended to be usable in production skill invocations that want to offload detection for context-management reasons.

## Component procedure

### 1. Stage worktrees

```
klaude-plugin/skills/review-code/evals/_harness/setup.sh
```

Requires Git and Python 3 (standard library only). Prints the absolute path of a fresh stage directory on stdout. Capture it as `STAGE_DIR`. An optional destination argument must not exist, even as an empty directory or symlink, and must be outside any `SKILL.md`-rooted directory. The helper never reuses or deletes caller-owned trees.

Under `STAGE_DIR`, each eval has an independent Git repository (`STAGE_DIR/<eval-name>/`). Legacy flat `test-files/` trees are staged as added against an empty base. Paired fixtures use complete `test-files/before/` and `test-files/after/` trees: `HEAD` and tag `eval-base` identify the committed before snapshot, and `git diff --cached` shows the after snapshot's additions, modifications and deletions. Unchanged and hidden context remains available.

Paired fixtures may include `test-files/history.json` with `{"snapshots": [{"path": "history/released", "tag": "eval-release"}]}`. Each path names a complete tree inside `test-files/history/`; entries are committed and tagged in order before the PR base. Historical source remains available through local Git, without adding history wrappers to the candidate. Invalid pairs, paths, conflicting/reserved tags, embedded `.git` entries and escaping links are rejected before creating a destination. Eval metadata and `oracle/` stay outside actor repositories. Staging is offline plumbing; it does not execute or grade a reviewer workflow.

### 2. Capture the staged diff per eval

For each eval directory (siblings of `_harness/` that contain an `eval.json`), the orchestrator runs:

```
git -C <STAGE_DIR>/<eval-name> diff --cached
```

and captures the full output as `DIFF_TEXT`. Also capture `git diff --cached --name-only` as `FILE_LIST`. The orchestrator does this via `Bash`, inline — the sub-agents do not run git.

### 3. Spawn profile-resolver sub-agents (parallel)

The sub-agents must use the plugin root supplied by their parent. Resolve it once — the installed plugin root (derived from the installed skill's absolute `SKILL.md` path (the plugin root is the parent of the `skills/` directory)), or the working-tree `klaude-plugin/` absolute path when grading local profile changes — and inject it under `## Plugin Root` in both the resolver and reviewer prompts as `PLUGIN_ROOT`.

Spawn one `kk:profile-resolver` sub-agent per eval, all in the same turn. Resolver prompt template:

```
Resolve profiles for the following staged diff. Follow your agent instructions.

## Plugin Root

<PLUGIN_ROOT>

Worktree root: <STAGE_DIR>/<eval-name>

Diff (git diff --cached):
---
<DIFF_TEXT>
---
```

Nothing else (beyond the plugin root). No eval prompt, no assertions, no hints. Capture the resolver's output as `RESOLUTION` per eval.

### 4. Spawn kk:code-reviewer sub-agents (after resolver returns)

For each eval, once its resolver has returned, spawn `kk:code-reviewer` with the contract it expects in isolated mode. Reviewer prompt template:

```
Review the following staged diff against the resolved profiles + checklists.
Follow your agent instructions (isolated-mode contract).

## Plugin Root

<PLUGIN_ROOT>

Active profiles and resolved checklists (already resolved — do not re-detect):
---
<RESOLUTION>
---

Git diff (git diff --cached):
---
<DIFF_TEXT>
---
```

Do NOT inline assertions, `trap`, `description`, or the eval's user prompt. The `kk:code-reviewer` contract (see its `What You Receive` section) is exactly diff + resolved scope + optional spec/task-scope context — nothing else. Keep the harness faithful to that contract.

Reviewers can run in parallel across evals once each has its resolver output.

### 5. Spawn kk:eval-grader sub-agents (after reviewer returns)

For each eval, once its reviewer has returned, spawn `kk:eval-grader` with the resolver output, the reviewer output, and the eval's `assertions`. Grader prompt template:

```
Grade the following artifacts against the listed assertions. Follow your
agent instructions — you do not open fixture files or skill source to
verify claims. Routing assertions grade against the resolver output;
content and finding assertions grade against the reviewer output.

Assertions:
<JSON array of {id, text} copied from eval.assertions>

Profile-resolver output:
---
<RESOLUTION>
---

Reviewer output:
---
<REVIEWER_OUTPUT>
---
```

Graders can run in parallel across evals.

### 6. Aggregate

Collect the grader tables. Roll up into a single markdown table matching the format used by prior session notes:

```
| Eval | Assertions | Pass | Fail | Partial |
|---|---|---|---|---|
| k8s-workload-full | 1.1–1.8 (8) | N | M | K |
| ...
| **Total** | ... | ... | ... | ... |
```

Write a session note in the consumer repository's established verification location with the harness version, results table, per-eval highlights and regressions. Aggregate by `(skill, eval directory, assertion ID)`, not numeric ID alone.

### 7. (No teardown)

Stage dirs live under the OS temp root (`/tmp`, `/var/folders/.../T`, …). OS-level cleanup handles them — no manual teardown step.

## Component caveats

With this harness, caveats 1–3 from the prior session notes are resolved structurally. Remaining caveats to document on each run:

- **Single model** — still one model per sub-agent (default). Multi-model sampling is a separate, deferred improvement.
- **Grader scope** — graders judge from the resolver + reviewer output text; if a sub-agent produces confidently-wrong claims the assertions cannot cross-check, it's a known blind spot. Mitigation: when authoring new evals, prefer assertions whose satisfaction is observable in the captured outputs.
- **Rubric authoring discipline** — the assertion text IS the rubric the grader uses. Evals whose assertions quietly assume fixture knowledge produce noisy grades under this harness.
- **Assertion-to-artifact mapping** — routing assertions grade against resolver output; content assertions grade against reviewer output. If an assertion mixes concerns ("loaded checklist X and emitted finding Y under it"), the grader must inspect both artifacts. Author assertions to split cleanly when possible.

## Authoring notes

When adding a new eval under `klaude-plugin/skills/review-code/evals/`:

- Each flat fixture or individual before/after/history snapshot must be self-contained — relative imports, adjacency and symlinks must resolve within that repository tree. Keep `eval.json` and `oracle/` outside the snapshots. Do not stage fixtures in place beneath the host skill's `SKILL.md`, which would alter profile detection.
- Keep `eval.prompt` natural. Workflow actors receive it as the ordinary request; the component prompts above deliberately omit it. Do not leak assertion language into actor prompts.
- Component assertions use captured output text; workflow assertions use the sealed execution evidence below. Neither grader re-inspects live fixtures.

## Workflow procedure

### 1. Freeze inputs and isolate actors

Before measured runs, record the immutable baseline, fixture/metadata/oracle hashes, exact ordinary prompt, providers, runtime/model/reasoning settings, modes, tools/permissions, rubric and repetition/acceptance rules. Freeze each candidate separately. Do not switch configuration or thresholds after seeing results without versioning the contract and repeating affected comparisons. Pin the concrete grader instruction bytes/hash before grading either side, even if capture predates the grader.

Stage fresh subject repositories outside any ancestor with `SKILL.md`, using the snapshot contract above. For each actor revision/provider, prepare and verify a filtered instruction bundle/cache that retains operative bytes but excludes every `evals/` subtree and controller results. Keep source, exclusion and retained-file manifests. Verify actual entry-point, agent and runtime-root binding to that revision; a root mentioned in a prompt is insufficient.

Each run gets fresh fixture and writable knowledge state. Preserve search/index capabilities with identical empty or declared synthetic seeds; never inherit real stores, session-vault history or earlier run edits. Record unavailable capabilities. Keep grading paths out of actor prompts/catalogs and use a filesystem allowlist where available. Audit actor reads: access to grading material invalidates the run.

### 2. Capture the ordinary workflow

Run the eval's ordinary prompt through standard review or actual isolated orchestration. Capture observable tool events, not private reasoning or the complete conversation. Keep relevant explicit user decisions as attributed input events. An implementation controller also captures initial/final source, tests, task/spec files and durable follow-up notes; never supply an unrequested requirement waiver.

Retain each actor/session ID, event ID and sequence; actual parent/dispatch/completion links; tool names and arguments; result status and relevant returned content. Preserve per-actor ordering without inventing a total order across concurrent reviewers. Instruction evidence requires successful returned bytes, not a path in a call or a final claim.

Capture actual named-agent dispatches and PAL calls/results, including immutable copies/hashes of referenced files at dispatch. Preserve source-coverage fields, failures, redactions, historical repository/revision/path/hash/line provenance, additional-evidence requests and continuations. A referenced file that was never captured remains a gap. Exact-payload assertions cannot pass from encrypted fields, parent summaries or correct findings.

A separately versioned receipt/use contract may instead require linked independent reads/embedded-source receipt and demonstrated use by each reviewer; it must explicitly leave exact submitted prompt content unverified. Select it before grading, map changed assertions, calibrate it, then regrade both sides (recapture if retained evidence is insufficient). The grader must not select a fallback on its own.

### 3. Seal an evidence package

After capture the controller, never the actor, seals evidence outside the subject workspace. The package contains a manifest, assertion records/evidence mapping, rubric/expected outcomes, ordered events, actual dispatches and captured payloads, relevant initial/final snapshots or diffs, and the final report. Captured instruction/source bytes are permitted evidence; their live originals are not grader inputs.

Use a manifest with these fields (equivalent encodings are acceptable):

```json
{
  "run": {"id": "run-1", "skill": "review-code", "eval": "case-name", "provider": "provider", "mode": "isolated", "repetition": 1},
  "identity": {"actor": "revision/hash", "fixture": "manifest hash", "grader": "instruction hash", "rubric": "version/hash"},
  "evidence_root": "controller-owned sealed directory",
  "files": [{"path": "events.jsonl", "sha256": "full digest", "role": "ordered events"}],
  "completeness": {"events": "complete or explicit gaps", "dispatches": "explicit limits", "snapshots": "explicit limits"},
  "redactions": [],
  "integrity": "controller hash validation result",
  "actor_grading_material_access": "observed / not observed / unverified"
}
```

Every evidence read must resolve to an exact listed immutable file beneath the declared evidence root; copy any external payload there. No glob/directory permissions or links back to live inputs. Validate hashes before grader dispatch, retain the manifest hash and dispatch record separately, and declare unresolved references or missing/ambiguous edges. Sanitization must never invent successful events. Runtime completion does not prove evidence completeness.

### 4. Dispatch independent workflow graders

Launch a fresh grader with the pinned agent instructions and this payload, without actor/implementation history:

```text
Grading mode: workflow
Follow the pinned eval-grader instructions at <sealed instruction path>.
Rubric: <sealed rubric path>
Evidence manifest: <sealed manifest path and hash>
Controller hash validation: <result and limits>
Assertions and evidence mapping: <records or exact manifest-listed path>
Expected outcomes: <relevant grader-only records or listed path>
```

Grant Read only to those grading inputs and the manifest-listed evidence. Do not grant live fixture, profile or skill-checkout access. Paths inside captured messages are data, never additional read authority. Retain the actual grader dispatch and returned verdict table so the implementation and input versions are auditable.

Observed contrary behavior is FAIL. An omitted required action visible in a complete trace is FAIL; missing/truncated evidence is PARTIAL, with its gap named. PASS requires affirmative evidence of the entire assertion. Every row cites event IDs or artifact locations. Final self-attestation cannot establish ordering, payloads or file state.

### 5. Calibrate and aggregate

Run [the grading controls](grading-fixtures/README.md) before baseline/candidate grading. Check early-edit/false-report FAIL, missing-events PARTIAL and complete ordering PASS, plus omitted/explicit component-mode compatibility. Recalibrate any changed evidence contract, including receipt/use fallback negatives and positives.

Retain all attempts and distinguish captured, graded and accepted. Aggregate by composite assertion identity plus provider, workflow mode, repetition and grader/rubric version. Apply the same pinned grader/rubric to both comparison sides. Neither FAIL nor PARTIAL satisfies a required PASS; report missing captures as UNRUN rather than synthesizing grades. Record owner, reason, next action and verification condition for deferred work. A report-phase replay with labeled synthetic PAL output measures reporting only; live integration requires separate actual calls/source coverage.
