# Local evaluation run — 2026-09-29

**Executed: 10/10 scenarios. Verdict: 10 PASS, 0 FAIL, 0 PARTIAL; 40/40 assertions PASS.** Six cases have original and revised reader sessions; four routing cases have no applicable reader comparison. There are no authored-but-unrun scenarios in this assigned batch. One environment-blocked initial attempt is retained and excluded from the ten valid executions.

The fixed original-reader answers scored **23/30**, and revised-reader answers scored **30/30**. These are single AI-reader observations, not evidence of improved comprehension for humans generally. Dense-source and cross-file preservation already scored 5/5; their predeclared orientation defects justify the edits. Clear-factual-error also scored 5/5 before editing; its predeclared reference error was corrected. Already-clear remained byte-for-byte unchanged.

| Scenario | Status | Original → revised | Assertions | Verdict |
| --- | --- | --- | --- | --- |
| [dense-source](#dense-source) | executed | 5/5 → 5/5 | 5/5 | [PASS](dense-source/verdict.md) |
| [source-disagreement](#source-disagreement) | executed | 2/5 → 5/5 | 5/5 | [PASS](source-disagreement/verdict.md) |
| [missing-context](#missing-context) | executed | 1/5 → 5/5 | 5/5 | [PASS](missing-context/verdict.md) |
| [cross-file-preservation](#cross-file-preservation) | executed | 5/5 → 5/5 | 5/5 | [PASS](cross-file-preservation/verdict.md) |
| [already-clear](#already-clear) | executed | 5/5 → 5/5 | 4/4 | [PASS](already-clear/verdict.md) |
| [clear-factual-error](#clear-factual-error) | executed | 5/5 → 5/5 | 4/4 | [PASS](clear-factual-error/verdict.md) |
| [skill-instruction-target](#skill-instruction-target) | executed | N/A — routing | 3/3 | [PASS](skill-instruction-target/verdict.md) |
| [agent-instruction-target](#agent-instruction-target) | executed | N/A — routing | 3/3 | [PASS](agent-instruction-target/verdict.md) |
| [code-non-trigger](#code-non-trigger) | executed | N/A — routing | 3/3 | [PASS](code-non-trigger/verdict.md) |
| [brevity-non-trigger](#brevity-non-trigger) | executed | N/A — routing | 3/3 | [PASS](brevity-non-trigger/verdict.md) |

## Provenance and controls

Inputs were copied from the canonical fixtures without changes. Questions, expected answers, protected claims and observable defects were fixed in their existing oracles before editor dispatch. The original repository HEAD was `9a7ad32eef89a3b8c9b366292ac1f4776c7d005f`. Operative instructions came from the frozen `/tmp/clarify-task4/instructions/` snapshot, not installed copies; [instruction SHA256s](instruction-hashes.json) identify that snapshot.

All active editor, reader and grader sessions are fresh default general-purpose agents with `fork_turns="none"`; only one local child ran at a time. [Exact delegation calls and results](spawn-events.md) ([JSONL](spawn-events.jsonl)) record the actual dispatches. There are 22 active editor/reader sessions, one independent batch grader, and one additional blocked initial editor attempt.

Actual session metadata records `gpt-6-astra`, `xhigh` effort, default collaboration mode, OpenAI provider, CLI `0.159.0`, and `comp_hash=3000`. An exact model build and temperature were not exposed and are not inferred. Each scenario manifest links its session IDs/settings and input/output hashes. The grader has its own [request](_grading/grader-request.md), [session record](_grading/grader-session.json), [final output](_grading/grader-output.md) and [complete visible trace](_grading/grader-trace.md) ([JSONL](_grading/grader-trace.jsonl)). Per-scenario `evidence-hashes.json` covers the saved evidence files.

Editors received only the fixture files and copied instruction paths. Readers received only their own artifact version, its explicitly allowed reading path, and five neutral questions. Source-only evidence, oracles and the other version stayed outside reader manifests. Complete captured tool calls/results, including nested calls inside `functions.exec`, were audited. No out-of-manifest subject-content reads or missing call/results were found. Snapshot hash checks found only permitted changes.

## Limits and preserved failures

- Prompt manifests and trace audits are shared-filesystem controls, not OS isolation. Traces exclude hidden reasoning and system boilerplate while preserving exact tool calls/results, visible assistant messages and relevant actual metadata.
- Initial request reads often used the default login shell before seeing the request's `login:false` instruction, resulting in denied navi log initialization. No subject content outside the allowed paths appeared.
- The first dense-source editor used a shell heredoc rather than native `apply_patch`. Its exact request and trace remain unchanged. Later edit requests explicitly required native `apply_patch`.
- The skill-instruction-target request initially hit an environment hook on its directory name, then read the same allowed request by relative filename. The agent-instruction-target initial session stopped at that hook; [the entire blocked attempt](agent-instruction-target/blocked-attempt-1/audit.md) is preserved. A fresh retry used a fully restaged, byte-identical fixture in a neutral directory; [relocation hashes](agent-instruction-target/relocation.json) record the change. No oracle, assertion or fixture content was relaxed.
- The grader's final direct-path report readback also hit that directory-name hook. Its earlier evidence inspection was complete; the coordinator separately checked all final verdict schemas, assertion IDs and links. [Grader audit](_grading/audit.md) records this and recovered display/patch errors.
- Reader scores measure answer support on this fixed reading path. Text length was not a success criterion. PARTIAL answers were not counted as passes.

## Scenario evidence

### dense-source

- [Manifest](dense-source/manifest.json), [coordinator audit](dense-source/audit.md), [evidence hashes](dense-source/evidence-hashes.json), [verdict](dense-source/verdict.md) ([JSON](dense-source/verdict.json)).
- Editor: [exact request](dense-source/editor-request.md), [spawn text](dense-source/editor-spawn.txt), [session](dense-source/editor-session.json), [report](dense-source/editor-output.md), [trace](dense-source/editor-trace.md) ([JSONL](dense-source/editor-trace.jsonl)).
- Original artifacts: [guide.md](dense-source/original/guide.md). Reader: [request](dense-source/original-reader-request.md), [answers](dense-source/original-reader-output.md), [session](dense-source/original-reader-session.json), [trace](dense-source/original-reader-trace.md) ([JSONL](dense-source/original-reader-trace.jsonl)).
- Revised artifacts: [guide.md](dense-source/revised/guide.md). Reader: [request](dense-source/revised-reader-request.md), [answers](dense-source/revised-reader-output.md), [session](dense-source/revised-reader-session.json), [trace](dense-source/revised-reader-trace.md) ([JSONL](dense-source/revised-reader-trace.jsonl)).

### source-disagreement

- [Manifest](source-disagreement/manifest.json), [coordinator audit](source-disagreement/audit.md), [evidence hashes](source-disagreement/evidence-hashes.json), [verdict](source-disagreement/verdict.md) ([JSON](source-disagreement/verdict.json)).
- Editor: [exact request](source-disagreement/editor-request.md), [spawn text](source-disagreement/editor-spawn.txt), [session](source-disagreement/editor-session.json), [report](source-disagreement/editor-output.md), [trace](source-disagreement/editor-trace.md) ([JSONL](source-disagreement/editor-trace.jsonl)).
- Original artifacts: [guide.md](source-disagreement/original/guide.md). Reader: [request](source-disagreement/original-reader-request.md), [answers](source-disagreement/original-reader-output.md), [session](source-disagreement/original-reader-session.json), [trace](source-disagreement/original-reader-trace.md) ([JSONL](source-disagreement/original-reader-trace.jsonl)).
- Revised artifacts: [guide.md](source-disagreement/revised/guide.md). Reader: [request](source-disagreement/revised-reader-request.md), [answers](source-disagreement/revised-reader-output.md), [session](source-disagreement/revised-reader-session.json), [trace](source-disagreement/revised-reader-trace.md) ([JSONL](source-disagreement/revised-reader-trace.jsonl)).

### missing-context

- [Manifest](missing-context/manifest.json), [coordinator audit](missing-context/audit.md), [evidence hashes](missing-context/evidence-hashes.json), [verdict](missing-context/verdict.md) ([JSON](missing-context/verdict.json)).
- Editor: [exact request](missing-context/editor-request.md), [spawn text](missing-context/editor-spawn.txt), [session](missing-context/editor-session.json), [report](missing-context/editor-output.md), [trace](missing-context/editor-trace.md) ([JSONL](missing-context/editor-trace.jsonl)).
- Original artifacts: [guide.md](missing-context/original/guide.md). Reader: [request](missing-context/original-reader-request.md), [answers](missing-context/original-reader-output.md), [session](missing-context/original-reader-session.json), [trace](missing-context/original-reader-trace.md) ([JSONL](missing-context/original-reader-trace.jsonl)).
- Revised artifacts: [guide.md](missing-context/revised/guide.md). Reader: [request](missing-context/revised-reader-request.md), [answers](missing-context/revised-reader-output.md), [session](missing-context/revised-reader-session.json), [trace](missing-context/revised-reader-trace.md) ([JSONL](missing-context/revised-reader-trace.jsonl)).

### cross-file-preservation

- [Manifest](cross-file-preservation/manifest.json), [coordinator audit](cross-file-preservation/audit.md), [evidence hashes](cross-file-preservation/evidence-hashes.json), [verdict](cross-file-preservation/verdict.md) ([JSON](cross-file-preservation/verdict.json)).
- Editor: [exact request](cross-file-preservation/editor-request.md), [spawn text](cross-file-preservation/editor-spawn.txt), [session](cross-file-preservation/editor-session.json), [report](cross-file-preservation/editor-output.md), [trace](cross-file-preservation/editor-trace.md) ([JSONL](cross-file-preservation/editor-trace.jsonl)).
- Original artifacts: [design.md](cross-file-preservation/original/design.md), [tasks.md](cross-file-preservation/original/tasks.md), [entry.md](cross-file-preservation/original/entry.md). Reader: [request](cross-file-preservation/original-reader-request.md), [answers](cross-file-preservation/original-reader-output.md), [session](cross-file-preservation/original-reader-session.json), [trace](cross-file-preservation/original-reader-trace.md) ([JSONL](cross-file-preservation/original-reader-trace.jsonl)).
- Revised artifacts: [design.md](cross-file-preservation/revised/design.md), [tasks.md](cross-file-preservation/revised/tasks.md), [entry.md](cross-file-preservation/revised/entry.md). Reader: [request](cross-file-preservation/revised-reader-request.md), [answers](cross-file-preservation/revised-reader-output.md), [session](cross-file-preservation/revised-reader-session.json), [trace](cross-file-preservation/revised-reader-trace.md) ([JSONL](cross-file-preservation/revised-reader-trace.jsonl)).

### already-clear

- [Manifest](already-clear/manifest.json), [coordinator audit](already-clear/audit.md), [evidence hashes](already-clear/evidence-hashes.json), [verdict](already-clear/verdict.md) ([JSON](already-clear/verdict.json)).
- Editor: [exact request](already-clear/editor-request.md), [spawn text](already-clear/editor-spawn.txt), [session](already-clear/editor-session.json), [report](already-clear/editor-output.md), [trace](already-clear/editor-trace.md) ([JSONL](already-clear/editor-trace.jsonl)).
- Original artifacts: [guide.md](already-clear/original/guide.md). Reader: [request](already-clear/original-reader-request.md), [answers](already-clear/original-reader-output.md), [session](already-clear/original-reader-session.json), [trace](already-clear/original-reader-trace.md) ([JSONL](already-clear/original-reader-trace.jsonl)).
- Revised artifacts: [guide.md](already-clear/revised/guide.md). Reader: [request](already-clear/revised-reader-request.md), [answers](already-clear/revised-reader-output.md), [session](already-clear/revised-reader-session.json), [trace](already-clear/revised-reader-trace.md) ([JSONL](already-clear/revised-reader-trace.jsonl)).

### clear-factual-error

- [Manifest](clear-factual-error/manifest.json), [coordinator audit](clear-factual-error/audit.md), [evidence hashes](clear-factual-error/evidence-hashes.json), [verdict](clear-factual-error/verdict.md) ([JSON](clear-factual-error/verdict.json)).
- Editor: [exact request](clear-factual-error/editor-request.md), [spawn text](clear-factual-error/editor-spawn.txt), [session](clear-factual-error/editor-session.json), [report](clear-factual-error/editor-output.md), [trace](clear-factual-error/editor-trace.md) ([JSONL](clear-factual-error/editor-trace.jsonl)).
- Original artifacts: [guide.md](clear-factual-error/original/guide.md). Reader: [request](clear-factual-error/original-reader-request.md), [answers](clear-factual-error/original-reader-output.md), [session](clear-factual-error/original-reader-session.json), [trace](clear-factual-error/original-reader-trace.md) ([JSONL](clear-factual-error/original-reader-trace.jsonl)).
- Revised artifacts: [guide.md](clear-factual-error/revised/guide.md). Reader: [request](clear-factual-error/revised-reader-request.md), [answers](clear-factual-error/revised-reader-output.md), [session](clear-factual-error/revised-reader-session.json), [trace](clear-factual-error/revised-reader-trace.md) ([JSONL](clear-factual-error/revised-reader-trace.jsonl)).

### skill-instruction-target

- [Manifest](skill-instruction-target/manifest.json), [coordinator audit](skill-instruction-target/audit.md), [evidence hashes](skill-instruction-target/evidence-hashes.json), [verdict](skill-instruction-target/verdict.md) ([JSON](skill-instruction-target/verdict.json)).
- Editor: [exact request](skill-instruction-target/editor-request.md), [spawn text](skill-instruction-target/editor-spawn.txt), [session](skill-instruction-target/editor-session.json), [report](skill-instruction-target/editor-output.md), [trace](skill-instruction-target/editor-trace.md) ([JSONL](skill-instruction-target/editor-trace.jsonl)).
- Original artifacts: [SKILL.md](skill-instruction-target/original/SKILL.md). Reader: N/A.
- Revised artifacts: [SKILL.md](skill-instruction-target/revised/SKILL.md). Reader: N/A.

### agent-instruction-target

- [Manifest](agent-instruction-target/manifest.json), [coordinator audit](agent-instruction-target/audit.md), [evidence hashes](agent-instruction-target/evidence-hashes.json), [verdict](agent-instruction-target/verdict.md) ([JSON](agent-instruction-target/verdict.json)).
- Editor: [exact request](agent-instruction-target/editor-request.md), [spawn text](agent-instruction-target/editor-spawn.txt), [session](agent-instruction-target/editor-session.json), [report](agent-instruction-target/editor-output.md), [trace](agent-instruction-target/editor-trace.md) ([JSONL](agent-instruction-target/editor-trace.jsonl)).
- Original artifacts: [AGENTS.md](agent-instruction-target/original/AGENTS.md). Reader: N/A.
- Revised artifacts: [AGENTS.md](agent-instruction-target/revised/AGENTS.md). Reader: N/A.

### code-non-trigger

- [Manifest](code-non-trigger/manifest.json), [coordinator audit](code-non-trigger/audit.md), [evidence hashes](code-non-trigger/evidence-hashes.json), [verdict](code-non-trigger/verdict.md) ([JSON](code-non-trigger/verdict.json)).
- Editor: [exact request](code-non-trigger/editor-request.md), [spawn text](code-non-trigger/editor-spawn.txt), [session](code-non-trigger/editor-session.json), [report](code-non-trigger/editor-output.md), [trace](code-non-trigger/editor-trace.md) ([JSONL](code-non-trigger/editor-trace.jsonl)).
- Original artifacts: [prep.py](code-non-trigger/original/prep.py). Reader: N/A.
- Revised artifacts: [prep.py](code-non-trigger/revised/prep.py). Reader: N/A.

### brevity-non-trigger

- [Manifest](brevity-non-trigger/manifest.json), [coordinator audit](brevity-non-trigger/audit.md), [evidence hashes](brevity-non-trigger/evidence-hashes.json), [verdict](brevity-non-trigger/verdict.md) ([JSON](brevity-non-trigger/verdict.json)).
- Editor: [exact request](brevity-non-trigger/editor-request.md), [spawn text](brevity-non-trigger/editor-spawn.txt), [session](brevity-non-trigger/editor-session.json), [report](brevity-non-trigger/editor-output.md), [trace](brevity-non-trigger/editor-trace.md) ([JSONL](brevity-non-trigger/editor-trace.jsonl)).
- Original artifacts: [notes.md](brevity-non-trigger/original/notes.md). Reader: N/A.
- Revised artifacts: [notes.md](brevity-non-trigger/revised/notes.md). Reader: N/A.

