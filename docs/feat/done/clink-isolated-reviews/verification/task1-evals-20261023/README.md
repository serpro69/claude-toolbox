# Task 1 evaluation runs — 2026-10-23

Component-mode grading of the new code-review scenarios under
`klaude-plugin/skills/review-code/evals/external-*`. This record covers the
runs made during Task 1. The bounded verification that remains belongs to
Task 3.2 (see the criterion change recorded in `tasks.md`, 2026-10-23).

**Scenario set reduced after grading (2026-10-23, user-approved).** Applying
the repository's proportionate-verification policy, the shipped set was cut
from 18 one-per-matrix-row scenarios to 11 decision-relevant ones. Removed:
26 codereview-omitted (duplicate of 25), 28 no-eligible-provider (exclusion
already exercised by 25/29/40), 34 continuation-evidence (transport verified
in Task 0; instruction rule is simple), and 30/31/32/33/35, whose decisions
were folded into 25 (partial failure: agy now fails) and the new 41
`external-receipt-limits` (denied criteria read with plausible citations,
missing telemetry, truncation, inherited permissions). Wording and layout
assertions were dropped: the shared `.1` assertion now checks load order only,
and former 23.4 (report-line layout) is gone. Grades below were recorded
against the earlier assertion text; they are retained unchanged as history.

## Setup

- Toolbox working tree at `49b73b0` plus the uncommitted Task 1 changes. The
  instruction bundle the actors used (`/tmp/kk-bundle.0p37Ks/klaude-plugin`,
  `klaude-plugin/` with every `evals/` subtree excluded) hashes identical to the
  working tree for `skills/_shared/external-review-invocation.md`
  (`8eaa3a27…d3f57`) and `skills/review-code/review-isolated.md` (`68832d1e…a32e5`).
- Fixtures staged with `evals/_harness/setup.sh` into `/tmp/review-code-evals.haj9ivbi`
  (first pass) and `/tmp/review-code-evals.bdhkbq9k` (corroboration rerun), both
  outside any `SKILL.md` ancestor.
- Actor: one `general-purpose` Claude Code sub-agent per scenario, given the
  eval's ordinary prompt, the fixture repository and the bundle root. PAL MCP
  tools and the Agent tool were declared unavailable; the fixtures' synthetic
  `discovery.json` and `external-results/*.json` stood in for their results, as
  each `checkpoint.md` states. Actors were told not to read outside the fixture
  and bundle; no fixture edits were observed. Actor model: the session default
  (not pinned).
- Grader: one `kk:eval-grader` per scenario in component mode, reading only the
  saved actor output. The eleven raw actor transcripts (123,396 bytes) are kept
  out of Git in the ignored local archive
  `.local-archives/feature-evidence/clink-isolated-reviews-task1-20261023/actor-output/`
  with a SHA-256 inventory alongside; this record carries the verdicts. Grader instructions: the installed
  plugin's `agents/eval-grader.md` (kk 0.24.0 cache).
- This measures instruction routing and reporting on synthetic replays. It does
  not exercise live MCP transport, real discovery, concurrency or source receipt.

## Results

| Eval | Assertions | Pass | Fail | Partial | Notes |
|---|---|---|---|---|---|
| 23 external-api-available | 23.1–23.5 (5) | 4 | 0 | 1 | 23.1 partial: labelling clause (see below) |
| 24 external-api-runtime-failure | 24.1–24.5 (5) | 4 | 0 | 1 | 24.1 partial: labelling clause |
| 25 external-clink-roster | 25.1–25.5 (5) | 4 | 0 | 1 | 25.1 partial: labelling clause |
| 27 external-discovery-error | 27.1–27.4 (4) | 3 | 0 | 1 | 27.1 partial: labelling clause |
| 29 external-unknown-identity | 29.1–29.4 (4) | 4 | 0 | 0 | |
| 37 external-corroboration (rerun) | 37.1–37.4 (4) | 4 | 0 | 0 | graded after the fixture fix below |
| 38 external-all-reviewers-fail | 38.1–38.4 (4) | 3 | 0 | 1 | 38.1 partial: labelling clause |
| 39 external-standard-mode-regression | 39.1–39.3 (3) | 3 | 0 | 0 | regression control |
| **Total (first pass)** | **34** | **29** | **0** | **5** | |
| 29 external-unknown-identity (rerun, post-review bytes) | 29.1–29.4 (4) | 4 | 0 | 0 | assertions 29.2/29.3 as reworded for the single combined question |
| 40 external-undeclared-mapping (new, post-review bytes) | 40.1–40.4 (4) | 4 | 0 | 0 | covers the second review finding |
| **Total (all graded runs)** | **42** | **37** | **0** | **5** | |

Material outcomes (all PASS): API-available and API-runtime-failure produced
zero clink requests and no discovery retry; the clink roster excluded the
authoring provider and the executable-missing duplicate, sent one fresh
`role: default`, `allow_edits: false`, full-manifest request per provider,
sequentially, with no model parameter; discovery error stayed unresolved with
no speculative dispatch; unknown identity and the duplicate-provider choice
produced one focused question before any Google dispatch; all-reviewers-fail
reported non-completion and suggested standard mode without running it;
standard mode made no external call and used its own report format.

**Labelling PARTIALs (quality observation, not material).** The original
`.1` assertion asked the actor to "label this as a synthetic dispatch-phase
replay rather than live PAL integration". Every actor described the run as a
replay and never claimed live transport, but graders marked PARTIAL because the
word "synthetic" or an explicit "not live" sentence was absent. The assertion
mixed load order (material, PASS everywhere) with a wording demand; it was
reworded in the shipped `eval.json` files to "does not claim that this replay
validates live PAL transport or that the fixed reviewer artifacts were live
calls". The retained grades above are against the original wording.

**Corroboration fixture fix.** The first run of eval 37 (`actor-output/37-external-corroboration.actor.md`,
not graded) correctly refused to count agy as a corroborating supporter because
the fixture gave agy no returned read trace, which the shared protocol forbids.
The fixture was corrected to return an observable trace for both external
reviewers, and the rerun passed 4/4. Retained as evidence that the receipt rule
is applied as written.

**Other fixture adjustments after the first pass.** The synthetic API model in
evals 23/24 was changed from an OpenAI model to a Google model so the API
routing scenarios carry no authoring-provider confound (the actors had disclosed
the confound correctly; the design keeps the API branch's existing model policy
and does not apply the clink roster exclusion there). The claude read trace now
lists the resolved profile checklists so receipt covers the full criteria set.
Neither change affects the graded routing assertions.

## Not run in Task 1 (owner: Task 3.2, bounded verification)

Against the final bytes: every scenario except the two reruns above. Never run
at all: 25 in its merged form (agy failure), 36 staged-snapshot and 41
receipt-limits. Both host variants and workflow-mode sealed-evidence grading
are unrun; this record is Claude-host, component-mode only, single sample per
scenario. Task 3.2's bounded gate: the eleven scenarios once on the Claude
host, scenarios 23 and 25 on the Codex host, and one live clink smoke review.

## Post-review changes and reruns (2026-10-23, later the same day)

The isolated code review of this task (independent `kk:code-reviewer`; PAL
external review unavailable, provider-free) returned COMMENT with two P2 and
five P3 findings. The fixes changed the shared protocol (single combined roster
question covering authoring provider, undeclared mappings and duplicate
choices; `CLAUDE.md`/`AGENTS.md` named as the durable place to declare
mappings; `cli_clients` description corrected; command bound and snapshot
authority added to the prompt directives), the isolated workflow's prompt
template and discovery sentence, SKILL.md wording, eval 29's assertions
29.2/29.3, eval 37's agy trace provenance label, and added eval 40.

The eight first-pass grades above therefore predate those bytes. Two targeted
reruns against a second filtered bundle (`/tmp/kk-bundle2.EK5DJk/klaude-plugin`,
built after the P2 fixes; stage `/tmp/review-code-evals.v34p9ihd`) exercised
exactly the changed behavior: eval 29 (rerun) and eval 40 (new), both 4/4.
Actor outputs: `29-external-unknown-identity.rerun.actor.md` and
`40-external-undeclared-mapping.actor.md` in the local archive above. Two later wording-only
edits from the re-review ("before any clink dispatch" instead of "affected";
the command-bound and snapshot directives repeated in the shared protocol's
prompt-directive list; a note that a mapping introduced by the reviewed diff is
not an operator declaration) and the checkpoint wording about absent
`external-results/` postdate those reruns and have no recorded run. The
re-review confirmed both P2 and all prior P3 findings resolved.
