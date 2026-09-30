# destination-visibility: explicit validation-outcome regression

This run uses shared instruction SHA256
5908c353733671baffd74e0e8e17bfac2b9c3eb62bd3423643896613b7590e35.
The [rationale](rationale.md) explains its source correction and added assertion13.8.
Earlier outcomes remain preserved. The [independent report](grading/verdicts.md)
covers eight assertions, full procedure compliance and applicability of the four
other latest passing PR runs.

- [Manifest](manifest.json), [input hashes](input-hashes.json), [output hashes](output-hashes.json), [changes](changes.json), [instruction hashes](instruction-hashes.json), and [audit](audit.md).
- [Assertions](scenario/eval.json), [oracle](scenario/oracle/expected.json), [instruction diff](instruction-diff.diff), [assertion diff](assertion-diff.diff), [oracle diff](oracle-diff.diff), [Git refs](git-refs.json), [review diff](git-diff.txt), and [Git evidence](git-evidence.txt).
- [Editor request](editor-request.md), [completion](editor-output.md), [messages](editor-messages.md), [readable trace](editor-trace.md), [raw trace](editor-trace.jsonl), [dispatch](editor-dispatch.jsonl), [spawn](editor-spawn.txt), and [metadata](editor-metadata.json).
- [Original artifact](original-artifact.md), [request](original-request.md), [answers](original-output.md), [readable trace](original-trace.md), [raw trace](original-trace.jsonl), [dispatch](original-dispatch.jsonl), [spawn](original-spawn.txt), and [metadata](original-metadata.json).
- [Revised artifact](revised-artifact.md), [request](revised-request.md), [answers](revised-output.md), [readable trace](revised-trace.md), [raw trace](revised-trace.jsonl), [dispatch](revised-dispatch.jsonl), [spawn](revised-spawn.txt), and [metadata](revised-metadata.json).
- [Grader request](grading/grader-request.md), [verdicts](grading/verdicts.md), [completion](grading/grader-output.md), [readable trace](grading/grader-trace.md), [raw trace](grading/grader-trace.jsonl), [dispatch](grading/grader-dispatch.jsonl), [spawn](grading/grader-spawn.txt), and [metadata](grading/grader-metadata.json).

Recorded settings are gpt-6-astra/xhigh/summary-none; build and temperature are
unrecorded. The final original/revised readers ran concurrently under the parent's
expanded two-slot authorization, each in a fresh session with only its own reading
manifest. Shared-filesystem controls are not OS isolation. AI-reader observations
do not demonstrate human comprehension or statistical reliability.

