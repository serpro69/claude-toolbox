# Task 3 consumer integration run

Date: 2026-09-29. Base revision: `38fe9bd` (Task 2 completion).
Tested instructions are identified by [SHA-256 hashes](instruction-hashes.txt).
The routing inspection's unchanged implement instructions have a
[separate hash manifest](implementation-instruction-hashes.txt).
Inputs, snapshots, requests, traces, checks and review reports are identified by
[artifact hashes](manifest-hashes.txt).

Five fresh general-purpose Codex sessions ran with `fork_turns="none"`, model
`gpt-6-astra`, reasoning `xhigh`, as recorded in their trace metadata. Model build
and sampling temperature are not exposed. No author conversation was inherited.

Each session's exact spawn message was:

> Carry out the evaluation request in /tmp/clarify-docs-task3-08Xji4xM/CASE/request.md. Read only that request, the instruction tree and case workspace it permits. Follow its execution boundaries; do not inspect the repository or other cases.

`CASE` was replaced with the scenario directory name below. The actual request
files were written before dispatch. Committed copies omit only the terminal blank
line for whitespace checks; the runtime text remains verbatim in each read trace.
They contain the user prompt and allowed input/write boundaries. They also request
pre-pass draft snapshots outside the user workspace, for observation only.

| Scenario | Execution type | Evidence directory |
| --- | --- | --- |
| Fresh design | Drafting and final pass | [clarity-after-drafting](clarity-after-drafting/) |
| WIP refinement | Refinement and final pass | [clarity-refined-documents-only](clarity-refined-documents-only/) |
| Unchanged WIP | Resume without editing | [clarity-unchanged-resume](clarity-unchanged-resume/) |
| Documentation rubric | Drafting and final pass | [clarity-preserves-profile](clarity-preserves-profile/) |
| Implementation modes | Read-only instruction-route inspection | [implementation-mode-coverage](implementation-mode-coverage/) |

The instruction tree was copied from canonical `klaude-plugin/` with all `evals/`
directories excluded. Each workspace received only its scenario's `test-files/`.
No oracle was created or supplied for these procedural assertions; graders receive
the eval assertions and source fixtures separately. Shared filesystem access is
constrained by the allowed-file manifest in each request and audited through tool
calls, not by separate OS sandboxes. Traces retain tool calls/results, visible
assistant messages and model/session metadata; hidden reasoning and standard
harness boilerplate are excluded. Tool traces are the basis for judging observed
instruction order and access, not a claim of enforced filesystem isolation.

These runs test consumer ordering, editing boundaries, rubric/structure fidelity
and mode routing. They do not include separate original/revised comprehension
readers, do not certify human comprehension, and do not execute a full implementation
completion lifecycle. Task 4 owns the full reader/fidelity protocol at the combined
feature revision; Task 5 owns release checks. Those tasks remain pending.
