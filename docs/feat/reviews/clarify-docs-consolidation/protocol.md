# Consolidation checklist evaluation protocol

This standalone follow-up compares the released v0.22.2 procedure with a candidate
that makes its final verification a five-item checklist. The requested outcome is
better consolidation with preserved meaning, not a particular word count or outline.

## Predeclared checks

- Run case 25 once with each instruction version from identical original inputs.
- Run `already-clear`, `source-disagreement` and `cross-file-preservation` with the
  candidate to guard against unnecessary edits, hidden requirement changes and lost
  task state or links.
- Give fresh readers only their version's document(s) and the fixed oracle questions.
  Grade task discoverability, concrete consolidation and fidelity separately. Apply
  the same artifact-quality rubric to both case-25 outputs; only the candidate has
  an additional observable checklist obligation.
- A separate grader receives source fixtures, assertions/oracles, artifacts, reader
  answers and audited tool traces. Check actual output, not the editor's checkmarks.

## Isolation and evidence

Each editor starts with `fork_turns="none"`, the inherited default model/effort, two
explicit instruction files and one separately staged `test-files/` workspace under
a temporary directory. No oracle or eval definition is placed in an editor workspace.
Only selected documents are writable. Readers receive no skill, requirements, source,
other output or expected answer. The same model/effort is used for both case-25 editors
and all readers; actual metadata is recorded with results.

Requests are written before dispatch. Exact invocation text, instruction/input hashes,
visible outputs and tool calls/results are retained; hidden reasoning and standard
harness boilerplate are excluded. Shared filesystem access is constrained by explicit
manifests and audited traces, not represented as operating-system isolation. Any read
outside the allowed manifest or incomplete trace invalidates the affected run.

These are small manual trials. A pass demonstrates the observed behavior only; it does
not establish general reliability, human comprehension or a statistically measured gain.

## Focused follow-up

Independent grading of the initial trial found two partials relevant to the candidate:
the long-guide verification record omitted locations for its last two checks, and the
source-disagreement guide named an owner but no concrete reconciliation action. The
original artifacts and verdicts remain unchanged. The follow-up changes only the
recording format and the explicit owner/action requirement, then reruns those two cases
from their original inputs in fresh editor and reader sessions under the same rubric.
The already-clear and cross-file runs describe the initial candidate; their instructions
differ from the follow-up only in those two verification sentences.

The focused source-disagreement rerun passed all five assertions. The long guide
again passed all content checks but retained a partial verification record: its
last two notes named generic categories rather than precise passages. A final
focused trial makes the meaning of a location explicit (exact heading, anchor or
line reference), using unchanged inputs and the same rubric. Earlier artifacts and
verdicts remain preserved; this is an additional observed trial, not a replacement.
