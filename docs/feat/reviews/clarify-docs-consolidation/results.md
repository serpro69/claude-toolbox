# /kk:clarify-docs consolidation checklist

This follow-up replaces the general final-pass prose with five explicit checks:
reader tasks, repeated explanations, history/evidence, protected meaning, and
structure/visibility. Each requires a brief result and document locations. Useful
local reminders and required self-contained sections remain allowed; there is no
word-count target, independent review gate or extra report-file requirement.

The long-guide rubric now distinguishes a repeated full policy from a local reminder
and rejects merely relocating obsolete narrative. Source fixtures are unchanged.

## Behavioral evidence

The [protocol](protocol.md), [requests](requests.json), [manifest](manifest.json),
instruction snapshots and filtered traces record the initial trials. Editors and
readers used fresh sessions with `gpt-6-astra` / `max`; the build and sampling
temperature were not exposed. Readers received only their document(s) and fixed
questions. Oracles were available only to graders. Trace review found no
agent-directed subject reads outside the allowed manifests or source execution.
This is audited shared-filesystem access, not operating-system isolation.

| Initial trial | Independent result |
| --- | --- |
| Released v0.22.2 on the long guide | 6 PASS, 1 PARTIAL |
| Initial checklist on the same long guide | 6 PASS, 1 PARTIAL |
| Already-clear document | 4 PASS; document unchanged byte-for-byte |
| Source disagreement | 4 PASS, 1 PARTIAL |
| Cross-file preservation | 5 PASS |

The [long-guide grading](grading-long.md) found both artifacts faithful and well
consolidated. The original had 2,062 words, baseline output 1,602, and candidate
output 1,616. These counts are descriptive; this trial demonstrates no candidate
advantage in artifact quality. The checklist produced a more visible verification
record, but its last two checks lacked supporting locations. Baseline verification
also had observable-record gaps, assessed under its own instructions.

The [regression grading](grading-regressions.md) found that the source-disagreement
guide preserved the accepted requirement, implementation mismatch and owner, but
its next action was only a generic reconciliation objective. The other two cases
passed without loss of task state, links, scope or no-op behavior.

The next wording specified a result/evidence format for all five checks and a
concrete next action for unresolved disagreements. The focused
[source-disagreement rerun](grading-followup-disagreement.md) passed all five
assertions. The [long-guide rerun](grading-followup-long.md) passed all content
checks but again left generic categories in its last two verification notes.

The final wording defines a location as an exact heading, anchor or line reference,
distinguishing it from a preservation claim. The
[final fresh long-guide trial](grading-precise-long.md) passed all seven assertions,
including all five location-supported verification records. Its 1,575 words are
descriptive only. These trials supplement, not replace, the initial results. The
already-clear and cross-file runs apply to the initial candidate; later instruction
changes concern recording precision and concrete follow-up actions.

## Implementation verification

- All nine shell suites passed: 604 assertions, zero failures or skips.
- `make generate-kodex` passed its Go and structure tests, including regeneration
  after the final wording refinement. Changed Codex files match source transforms.
- `make plugin-graph` passed its Go tests and found no broken edges or orphans;
  its cycle warning remains.
- Evaluation JSON, assertion numbering, fixture paths and operative-diff whitespace
  checks passed. Verbatim reader captures retain their original Markdown hard breaks.
- Independent code review approved the initial change and the final wording
  refinement with no findings. No systemic P0/P1 findings or new project conventions
  required indexing.
- PAL/Gemini reported two low-priority suggestions but zero embedded files, limiting
  its evidence. The suggested automated-oracle schema update is inapplicable: these
  are manual scenarios with no such runner/schema. The suggested checklist formatting
  change was optional; the observed candidate followed all five checks in order.

These small trials do not establish general reliability or human comprehension.
The concrete production-document comparison motivated the change; reproducing a
better production rewrite is not claimed by these synthetic trials.
Before making that broader claim, the skill maintainer should repeat the final
instructions on unseen long guides and the production baseline, retaining the same
fidelity criteria and recording unsuccessful runs as well as successful ones. This
remains future validation because the present trials are small and adaptive.
