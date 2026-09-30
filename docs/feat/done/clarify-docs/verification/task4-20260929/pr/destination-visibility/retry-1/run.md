# destination-visibility: first updated-instruction run

This fresh run uses the same source/fixtures, Git refs, prompt, questions and oracle
as the initial passing visibility run, but uses the updated shared instruction.
The [rationale](rationale.md) explains the changed validation-outcome obligation.
Its independent results appear in [the grader report](grading/verdicts.md).

This attempt passes all seven original assertions but **fails updated-procedure
compliance**: its destination draft lacks the successful validation outcome.
[Retry-2](../retry-2/run.md) tests an explicit destination-placement instruction;
this result remains preserved.

- [Manifest](manifest.json), [input hashes](input-hashes.json), [output hashes](output-hashes.json), [changes](changes.json), [instruction hashes](instruction-hashes.json), [instruction diff](instruction-diff.diff), and [coordinator audit](audit.md).
- [Assertions](scenario/eval.json), [oracle](scenario/oracle/expected.json), [Git refs](git-refs.json), [diff](git-diff.txt), and [commit/tree evidence](git-evidence.txt).
- [Editor request](editor-request.md), [completion](editor-output.md), [visible messages](editor-messages.md), [readable trace](editor-trace.md), [raw trace](editor-trace.jsonl), [dispatch](editor-dispatch.jsonl), [spawn text](editor-spawn.txt), and [metadata](editor-metadata.json).
- [Original artifact](original-artifact.md), [reader request](original-request.md), [answers](original-output.md), [readable trace](original-trace.md), [raw trace](original-trace.jsonl), [dispatch](original-dispatch.jsonl), [spawn text](original-spawn.txt), and [metadata](original-metadata.json).
- [Revised artifact](revised-artifact.md), [reader request](revised-request.md), [answers](revised-output.md), [readable trace](revised-trace.md), [raw trace](revised-trace.jsonl), [dispatch](revised-dispatch.jsonl), [spawn text](revised-spawn.txt), and [metadata](revised-metadata.json).
- [Grader request](grading/grader-request.md), [verdicts](grading/verdicts.md), [completion](grading/grader-output.md), [readable trace](grading/grader-trace.md), [raw trace](grading/grader-trace.jsonl), [dispatch](grading/grader-dispatch.jsonl), [spawn text](grading/grader-spawn.txt), and [metadata](grading/grader-metadata.json).

All sessions are fresh general-purpose agents. Observed model/settings and thread
IDs are preserved; temperature/build are unavailable. Shared-filesystem manifest
controls are not OS isolation. Results describe AI readers without claims about
human comprehension or statistical reliability. Earlier outcomes remain intact.
