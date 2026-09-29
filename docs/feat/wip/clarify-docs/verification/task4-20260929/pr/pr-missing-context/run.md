# pr-missing-context: executed run

Executed 2026-09-29 against frozen canonical instructions. The exact model/settings
and session IDs are recorded in the [manifest](manifest.json) and role metadata.
Final assertion verdicts and comprehension scores are in the
[independent grading report](../grading/verdicts.md).

- [Scenario assertions](scenario/eval.json).
- [Editor request](editor-request.md), [dispatch receipt](editor-dispatch.jsonl), [spawn text](editor-spawn.txt), and [session metadata](editor-metadata.json).
- [Editor completion](editor-output.md), [all visible messages](editor-messages.md), [readable trace](editor-trace.md), and [raw trace](editor-trace.jsonl).
- [Input hashes](input-hashes.json), [output hashes](output-hashes.json), [changed-file inventory](changes.json), and [instruction snapshot hashes](instruction-hashes.json).
- [Coordinator trace audit](audit.md) and [shared evidence limitations](../evidence-notes.md).

Reader comparison is not applicable: this scenario checks clarification and no
unauthorized output. The [original pasted capture](before/pasted-body.md) and
[unchanged capture after execution](after/pasted-body.md) remain available.

No assigned case is authored-but-unrun. The reader comparisons describe observed AI
reader answers, without a human-comprehension generalization.

