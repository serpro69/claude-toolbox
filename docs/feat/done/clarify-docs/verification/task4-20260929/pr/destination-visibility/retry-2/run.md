# destination-visibility: explicit-placement instruction run

This run uses shared instruction SHA256
624f14dd7e033c729b116cc65f93af79c4663dff6ca9e34b2b5c24bd89198b5d.
The [rationale](rationale.md) and [instruction diff](instruction-diff.diff) explain
why it follows the preserved earlier attempts. Fixtures, questions and oracle stay
unchanged. The [independent verdict](grading/verdicts.md) covers all seven assertions,
full procedure compliance and applicability of the other latest passing PR runs.

This attempt passed its seven assertions and retained 5/5 reader answers, but
**failed full procedure compliance** because the destination omits the validation
outcome. [Retry-3](../retry-3/run.md) preserves this result and tests a more explicit
instruction plus new regression assertion 13.8.

- [Manifest](manifest.json), [input hashes](input-hashes.json), [output hashes](output-hashes.json), [changes](changes.json), [instruction hashes](instruction-hashes.json), and [audit](audit.md).
- [Assertions](scenario/eval.json), [oracle](scenario/oracle/expected.json), [Git refs](git-refs.json), [diff](git-diff.txt), and [Git evidence](git-evidence.txt).
- [Editor request](editor-request.md), [completion](editor-output.md), [messages](editor-messages.md), [readable trace](editor-trace.md), [raw trace](editor-trace.jsonl), [dispatch](editor-dispatch.jsonl), [spawn](editor-spawn.txt), and [metadata](editor-metadata.json).
- [Original artifact](original-artifact.md), [request](original-request.md), [answers](original-output.md), [readable trace](original-trace.md), [raw trace](original-trace.jsonl), [dispatch](original-dispatch.jsonl), [spawn](original-spawn.txt), and [metadata](original-metadata.json).
- [Revised artifact](revised-artifact.md), [request](revised-request.md), [answers](revised-output.md), [readable trace](revised-trace.md), [raw trace](revised-trace.jsonl), [dispatch](revised-dispatch.jsonl), [spawn](revised-spawn.txt), and [metadata](revised-metadata.json).
- [Grader request](grading/grader-request.md), [verdicts](grading/verdicts.md), [completion](grading/grader-output.md), [readable trace](grading/grader-trace.md), [raw trace](grading/grader-trace.jsonl), [dispatch](grading/grader-dispatch.jsonl), [spawn](grading/grader-spawn.txt), and [metadata](grading/grader-metadata.json).

Observed model/settings and thread IDs are recorded for all fresh sessions.
Shared-filesystem manifest controls are not OS isolation. AI-reader results do not
establish human comprehension or statistical reliability. Prior results are retained.
