# runtime-pr: corrected-instruction retry

Executed 2026-09-29. This retry preserves the original scenario, questions, oracle,
fixtures and Git revisions and changes only the shared instruction snapshot. See
[why the retry was necessary](rationale.md) and the [instruction diff](instruction-diff.diff).
The initial [PARTIAL result](../../grading/verdicts.md) remains recorded separately.

The [independent retry verdict](grading/verdicts.md) also assesses whether the other
four initial PR passes remain applicable to the focused instruction correction.

- [Manifest and session IDs](manifest.json), [input hashes](input-hashes.json), [output hashes](output-hashes.json), [changes](changes.json), [instruction hashes](instruction-hashes.json), and [audit](audit.md).
- [Scenario assertions](scenario/eval.json), [oracle](scenario/oracle/expected.json), [Git refs](git-refs.json), [diff](git-diff.txt), and [commit/tree evidence](git-evidence.txt).
- [Editor request](editor-request.md), [completion](editor-output.md), [readable trace](editor-trace.md), [raw trace](editor-trace.jsonl), [dispatch](editor-dispatch.jsonl), [spawn text](editor-spawn.txt), and [metadata](editor-metadata.json).
- [Original artifact](original-artifact.md), [reader request](original-request.md), [answers](original-output.md), [readable trace](original-trace.md), [raw trace](original-trace.jsonl), [dispatch](original-dispatch.jsonl), [spawn text](original-spawn.txt), and [metadata](original-metadata.json).
- [Revised artifact](revised-artifact.md), [reader request](revised-request.md), [answers](revised-output.md), [readable trace](revised-trace.md), [raw trace](revised-trace.jsonl), [dispatch](revised-dispatch.jsonl), [spawn text](revised-spawn.txt), and [metadata](revised-metadata.json).
- [Grader request](grading/grader-request.md), [verdicts](grading/verdicts.md), [completion](grading/grader-output.md), [readable trace](grading/grader-trace.md), [raw trace](grading/grader-trace.jsonl), [dispatch](grading/grader-dispatch.jsonl), [spawn text](grading/grader-spawn.txt), and [metadata](grading/grader-metadata.json).

The run uses fresh general-purpose agents and records actual model settings.
Shared-filesystem manifest enforcement is not OS isolation. Results measure AI
reader responses without claiming human-comprehension improvement or statistical
reliability. No assigned PR scenario is authored-but-unrun.

