# Task 2 evaluation runs — 2026-10-24

Component-mode grading of the four new design-review scenarios under
`klaude-plugin/skills/review-design/evals/`. This record covers the runs made
during Task 2 on the Claude host. The bounded verification that remains
(Codex-host routing scenarios, live document smoke review) belongs to Task 3.2.

## Setup

- Toolbox working tree at `d2d4ecb` plus the uncommitted Task 2 changes. The
  instruction bundle the actors used (`/tmp/kk-bundle-design.J8rMPV/klaude-plugin`,
  `klaude-plugin/` with every `evals/` subtree excluded, symlinks preserved)
  was built from the working tree after all Task 2 instruction edits except one
  later one-clause SKILL.md wording change (see below). Working-tree hashes at
  bundle time, SHA-256 prefixes: `_shared/design-review-criteria.md`
  `a0cd42cd1df6ff96`, `_shared/external-review-invocation.md` `86810188e5e40ae8`
  (unchanged since Task 1), `review-design/review-isolated.md`
  `80944f6f04a0f8fa`, `agents/design-reviewer.md` `f79fea01b552ac62`.
- Fixtures staged by copying each scenario's `test-files/` to
  `/tmp/review-design-evals.4oIAZM/<scenario>/`, outside any `SKILL.md`
  ancestor. The review-code staging helper cannot stage this directory (its
  evals root is derived from its own location) and document review needs no
  Git repository, so a plain copy is the staging contract for design scenarios.
- Actor: one `general-purpose` Claude Code sub-agent per scenario, given the
  eval's ordinary prompt, the staged fixture as project root and the bundle as
  plugin root. PAL MCP tools and the Agent tool were declared unavailable; the
  fixtures' synthetic `discovery.json`, `external-results/*.json` and
  `independent-review.md` stood in for their results, as each `checkpoint.md`
  states. Actors were told not to read outside the fixture and bundle and not
  to edit; no fixture edits were observed. Actor model: the session default
  (not pinned).
- Grader: one `kk:eval-grader` per scenario in component mode, reading only
  the saved actor output. The raw actor outputs (four first-pass runs plus
  the eval 1 rerun recorded below) are kept
  out of Git in the ignored local archive
  `.local-archives/feature-evidence/clink-isolated-reviews-task2-20261024/actor-output/`
  with a SHA-256 inventory alongside (`actor-output.sha256`). Grader
  instructions: the installed plugin's `agents/eval-grader.md` (kk 0.24.0 cache).
- This measures instruction routing and reporting on synthetic replays. It does
  not exercise live MCP transport, real discovery, the real `design-reviewer`
  sub-agent, concurrency or source receipt.

## Results

| Eval | Assertions | Pass | Fail | Partial | Notes |
|---|---|---|---|---|---|
| 1 external-api-runtime-failure | 1.1–1.4 (4) | 4 | 0 | 0 | API selected; zero clink after continuation failure |
| 2 external-clink-document-scope | 2.1–2.4 (4) | 4 | 0 | 0 | missing tasks.md disclosed; planned file annotated |
| 3 external-all-reviewers-fail | 3.1–3.4 (4) | 4 | 0 | 0 | non-completion; standard mode suggested, not run |
| 4 standard-mode-regression | 4.1–4.3 (3) | 3 | 0 | 0 | regression control; no PAL call, tasks-only scope |
| **Total** | **15** | **15** | **0** | **0** | single sample per scenario |

Material outcomes (all PASS): the API branch sent the document manifest
(three documents, related source, both criteria files) with document-review
framing and made zero clink requests after the expert-stage timeout; the clink
branch excluded the authoring provider, treated the executable-missing
duplicate as a non-candidate, sent one fresh `role: default`,
`allow_edits: false`, full-manifest, model-free request per provider, disclosed
the missing `tasks.md` to the user and in every request, corroborated the retry
inconsistency with the internal reviewer and claude/Anthropic only, and kept
agy's "missing implementation" finding about the planned file as an attributed,
planned-work-annotated item rather than a defect; the all-fail scenario
reported non-completion and suggested `/kk:review-design` without running it;
standard mode made no external call, reviewed only `tasks.md` and used its own
report format.

**Quality observation (not material).** Both isolated actors that had the
full SKILL.md also read `review-process.md` (the standard-mode process) before
any subject document. This broke no ordering rule but is a wasted read. After
grading, SKILL.md's isolated-mode paragraph was changed by one clause to say
that `review-isolated.md` replaces the standard-mode process file in that mode.
That clause postdates the graded bundle and has no recorded run.

**Author-sourced findings.** The two isolated actors with a successful internal
reviewer each produced author-sourced observations during annotation (for
example, that nothing in the fixture design specifies the read side of "within
one sync interval"). These are labeled correctly and are not graded.

## Post-review changes and rerun (2026-10-24, later the same day)

The isolated code review of this task (independent `kk:code-reviewer`; PAL
external review unavailable because the connected PAL is provider-free with no
API model and no operator-declared clink provider mapping) returned COMMENT
with one P2 and four P3 findings. The P2: eval 1's model-visible
`test-files/discovery.json` carried a provenance note stating the expected
backend decision ("An API model is available, so the API branch is selected;
the clink clients below must not be used"), an answer leak that the eval
conventions forbid. The note was reduced to the neutral form the other
scenarios use. The P3 fixes changed the shared criteria's self-check (the
"Could I be misreading the document?" question restored), the design
workflow's authoring-provider sentence (aligned with the shared protocol:
this session's context counts when it produced the documents; a later,
separate review session's host CLI does not), SKILL.md (the isolated-only
shared files are named in prose rather than linked, so standard mode is not
invited to load them) and eval 4's assertion 4.1 (narrowed to "no PAL call or
plan and no reviewer sub-agent"; the "protocol not loaded" clause is now a
quality observation rather than a graded requirement).

The first-pass grades above therefore predate those bytes. One targeted rerun
against the refreshed bundle (same bundle path, resynced; worktree hashes at
rerun time: `_shared/design-review-criteria.md` `b6448a1beed72f0b`,
`review-design/review-isolated.md` `30b0ad7ee90703e0`,
`review-design/SKILL.md` `f6c4d25e2482f61e`, eval 1 `discovery.json`
`049858fd403cea61`) exercised the fixed scenario: eval 1 (rerun) 4/4 PASS,
with the same routing outcome as the contaminated first pass (API frozen,
zero clink, failure disclosed, nothing corroborated). This actor also did
not load the standard-mode process file. Actor output:
`1-external-api-runtime-failure.rerun.actor.md` in the local archive. Evals
2–4 were not rerun: the changed bytes do not touch the decisions they grade,
and eval 4's narrowed assertion is a strict subset of the assertion its
recorded run passed.

## Not run in Task 2 (owner: Task 3.2, bounded verification)

The Codex host for scenarios 1 and 2 (the two discovery-routing scenarios), one
live document smoke review against the verified PAL build, and any run of the
final SKILL.md bytes. Workflow-mode sealed-evidence grading is unrun; this
record is Claude-host, component-mode only, single sample per scenario.
