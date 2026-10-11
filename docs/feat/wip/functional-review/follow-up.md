# Functional review: next-session handoff

> Updated: 2026-10-11
> Status: recommendations awaiting severity/cost assessment; no new fix selected
> Owner: implementing agent, [Task 12.11](tasks.md#severity-and-instruction-cost-assessment--next-session)
> Evidence: [completed matrix](verification/task12/opus55/README.md), [Claude](verification/task12/opus55/claude-results.md), [Codex](verification/task12/opus55/codex-results.md)

## Start here

Resume with `/kk:implement task 12.11 of functional-review`. Read this handoff,
the current Task 12 status, [design](design.md), [implementation](implementation.md)
and [evaluation contract](evaluation.md), then the individual grades linked from
the provider summaries. Check the current worktree before proposing edits.
This task assesses the remaining issues and records a bounded next step; it
does not automatically implement every failed assertion or launch another matrix.

The user's latest constraint is explicit: fixing minor issues by overloading
instructions can make the skills worse overall. Assess severity before adding
more obligations. A small, contained correction remains worthwhile when its
benefit is clear and it does not materially increase instruction burden.
Keep this assessment in repository planning documents; it is not a new runtime
checklist for every skill invocation.

## Established result and open gates

The complete comparison ran **192 fresh sessions**: both providers, all 24
applicable case/mode combinations, baseline and candidate, twice each. Baseline
is `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; candidate is
`581dd0e11455398cb73e3d6ae5542854c016fe7f`. Claude Code 2.1.296 used Opus 5.5/high;
Codex 0.162.1 used gpt-6-astra/xhigh with gpt-6.1-sol/xhigh as named reviewer.
The [frozen contract](verification/task12/opus55/run-contract.md) is authoritative
for the complete configuration.

Both candidates improve overall assertion counts, but acceptance remains unmet.
R5 standard and both synthetic R8 variants pass twice on both providers. Two
repetitions are descriptive evidence, not a reliability estimate. Historical
runtime/model configurations differ; do not attribute every improvement to the
Opus change or pool those runs.

Task 12.1 capture is complete. Task 12.2 is partial: R8 is complete, live PAL
remains explicitly user-deferred, and legacy routing/pre-write controls remain
unrun. Task 12.3 grading is complete but its acceptance condition is not.
Task 13 remains pending. Preserve sealed captures, grades, corrections and old
failed checkpoints. Deferring a fix does not change a FAIL/PARTIAL to PASS or
complete a required gate. Any requirement or evidence-contract amendment must
be explicit, versioned and prospective.

## Decide whether a change is worth making

For each distinct issue, record a short decision containing:

- **Evidence and impact:** case/assertion/run links, observed behavior versus
  unavailable evidence, practical consequence, affected provider/mode, recurrence
  and confidence. A severe bug inside a fixture does not automatically make an
  instruction change high priority. Use existing severity conventions, with a
  reason tied to skill users rather than the number of red assertions.
- **Smallest useful correction and cost:** likely files/consumers; whether
  existing guidance can be removed, replaced or consolidated; added always-loaded
  words and transitive content; new mandatory steps, branches, tool calls,
  coordination or state; expected latency and regression exposure. A short diff
  can still impose a large new obligation. Retain the existing 800/1,200-word
  budgets; staying below them alone does not demonstrate proportionality.
- **Disposition and verification:** fix, investigate, defer or no change, with
  rationale and acceptance consequence. Deferred items need an owner and revisit
  trigger. A selected fix needs an affected comparison set, adjacent regression
  controls and a condition for rejecting/reverting it.

Material behavioral impact can justify a broader correction when expected value
outweighs its cost. A minor issue can justify a local wording replacement or
tooling correction with low regression risk and no material added load. A minor
issue that needs another mandatory phase, duplicated protocol or broad mechanism
should normally be deferred. Missing evidence first calls for capture diagnosis,
not extra actor instructions to manufacture an observable read.

## Provisional investigation inventory

These are assessment candidates, **not an approved priority order or fix list**.
Account for every remaining candidate FAIL/PARTIAL from the provider grade
indexes, grouping common causes without losing assertion-to-evidence links.

| Area | Observed distinction | Decision to resolve |
| --- | --- | --- |
| R6 inherited defect | Codex standard misses the inherited empty detailed-input defect in both candidate runs and both baselines. Claude standard finds it but omits bounded follow-up in both candidates, regressing from baseline. Codex isolated also omits follow-up once after surfacing it. | Assess missed detection separately from closure wording. A local closure correction may be cheap; it must preserve R5's clean no-action outcome and R9's justified recovery mechanism. |
| Claude evidence acquisition | Several isolated/implementation traces treat a denied shell request as general Bash unavailability, then omit diffs, history or executed tests. R3 isolated includes an early stop. | Establish whether command selection/tool-policy interpretation is the cause and how broadly it matters. Unattempted permitted Git commands are not evidence that Git was denied. Prefer correct use of resolved paths and available tools; do not silently broaden permissions. |
| Unsupported conclusions and verification | Claude R7 retains unsupported compatibility claims; I2 verification and some I4 test execution remain unestablished. | Distinguish misleading conclusions from missing capture, and inspect overlap with acquisition failures before prescribing another instruction. These may matter more than report completeness. |
| I4 sequencing | Codex candidate repetition 1 starts a source read before task/design/implementation context finishes loading. | Assess a local sequencing correction. This is a later context-before-source dependency, not the original instruction-before-investigation failure; the proposed preparation guard may not cover it. |
| I4 final qualification | Claude candidates and one Codex candidate omit the final production-state qualification. The Codex candidates preserve the hard specification and reopen the failed task. | Judge whether the omission materially misleads the reader, considering linked evidence. Do not equate it with silently waiving a hard requirement. Prefer an existing report location if a correction is justified. |
| Other report omissions | Codex R2 standard finds defects but omits the test-gap explanation once; other individual grades identify coverage/report gaps. | Assess effect on a user's decision. Do not add a mandatory section for every missed phrase; consider a contained replacement or defer. |
| Evidence gaps | Some Codex SKILL.md deliveries and I3/I4 submitted handoff arguments are not captured. Other grades distinguish unobserved pre-edit assessment from demonstrated failures. | Diagnose instrumentation before actor behavior. The receipt/use fallback is limited to R3 7.5/7.6 and I2 9.5; extending it requires an explicit prospective contract decision. |

For a selected issue, follow the relevant grade into its sealed evidence before
claiming a root cause. Likely investigation targets are the canonical
`klaude-plugin/skills/review-code/` files (`review-process.md`,
`review-isolated.md`, `functional-review.md`, `packet-preparation.md`,
`scripts/prepare_instructions.py`), `klaude-plugin/skills/implement/` files
(`plan-mode.md`, `standalone-mode.md`),
`klaude-plugin/skills/_shared/change-context.md`, and
`klaude-plugin/agents/code-reviewer.md`.
Capture questions start with `verification/task12/opus55/matrix.py` and its
declared helpers. These are investigation targets, not instructions to edit all
of them. Load the applicable implementation/profile instructions first.

### Conditional ordering proposal

[Task 12.10 and its proposal](ordering.md) remain available but are not the
default next action. Their original candidate-6 R5 failure did not recur in this
matrix. That observation neither proves ordering solved nor establishes a need
for a guard. Re-select the bounded feasibility probe only if triage demonstrates
a material remaining problem the mechanism actually addresses, with acceptable
cost. Revalidate capabilities against the exact runtimes then selected; old
hook-documentation research is not runtime proof. Preserve the probe's GO/NO-GO
limits and design review before any production integration.

## Produce and verify the next bounded step

Task 12.11 completes with a compact disposition record covering remaining
candidate failures/gaps, plus at most one selected next implementation task with
concrete files, limits and verification. Add the decisions as a dated assessment
section in this file and link it from Task 12.11; record the selected next task
in tasks.md. If no fix has favorable value/cost,
record that outcome and the still-open acceptance obligations. Do not accumulate
speculative fixes just to make the matrix green.

For a later selected change, freeze its source and evaluation configuration;
preserve the immutable baseline and use fresh affected baseline/candidate pairs,
two runs each, under matching declarations. Keep fixtures and grading unchanged
unless a separate contract revision is explicitly adopted. Never encode fixture
names, hidden defects or expected counts into operative instructions.

Judge the net effect using the target cases and nearby negative controls:
R6 closure changes need R5 and R9 checks; shared changes need affected providers
and modes; routing/pre-write changes need their legacy controls. Include I3's
proportionality when adding common obligations. Complete relevant static checks
and generated parity after operative edits. A narrow improvement that worsens
broader behavior or adds unjustified instruction burden should be rejected or
reverted. A full 192-session rerun is not the default for a small correction;
targeted evidence still does not replace the remaining feature acceptance gates.
