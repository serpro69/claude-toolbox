# cross-file-preservation: PASS

AI-reader comprehension: **5/5 → 5/5**. Only PASS counts; PARTIAL is not a pass. Scores use the fixed [oracle](oracle/expected.json).

## Assertions

- **4.1 — PASS.** [revised/design.md](revised/design.md) Context and Consequences plus [revised/tasks.md](revised/tasks.md) support all oracle answers; [revised-reader-output.md](revised-reader-output.md) answers 1-5 preserve planned preview, complete parsing and pending counting.
- **4.2 — PASS.** [revised/design.md](revised/design.md) retains Context, Decision, Deployment gate and Consequences; Decision preserves MUST id,name, MAY diagnostics and Mira's 2026-09-01 acceptance; the support gate and Product-owned duplicate policy remain.
- **4.3 — PASS.** [original/tasks.md](original/tasks.md) and [revised/tasks.md](revised/tasks.md) have identical task statuses (in-progress/pending), checkbox states ([x], [ ], [ ]) and dependencies (—/Task 1). Only the unchecked counting task's explanatory wording adds zero-write behavior; its state and obligation remain.
- **4.4 — PASS.** [revised/entry.md](revised/entry.md) retains `tasks.md`#task-1-preview and `design.md`#deployment-gate; design→tasks and tasks→design links target unchanged headings. `entry.md` and `requirements.md` are byte-identical to originals; [editor-trace.jsonl](editor-trace.jsonl) ordinal 46 independently checks these anchors.
- **4.5 — PASS.** [revised/design.md](revised/design.md) Context opens with planned operator preview, removes unexplained admission-observation jargon, gives two valid/one invalid/zero writes, and Consequences explicitly keeps counting pending.

## Original reader

1. **PASS: Why does this work exist?** [original-reader-output.md](original-reader-output.md) answer 1 gives the operator error-detection purpose.
2. **PASS: What happens in a representative case?** [original-reader-output.md](original-reader-output.md) answer 2 gives two valid, one invalid and zero writes; answer 3 explicitly says counts remain unfinished, supplying the planned-status qualification. Evaluated as a whole.
3. **PASS: What changes in the current increment?** [original-reader-output.md](original-reader-output.md) answer 3 states preview-only delivery, complete column acceptance and unfinished counts.
4. **PASS: What remains outside it?** [original-reader-output.md](original-reader-output.md) answer 4 keeps Apply disabled and future.
5. **PASS: What still needs a decision?** [original-reader-output.md](original-reader-output.md) answer 5 identifies Product's duplicate policy; answer 3 explicitly states support-owner walkthrough approval as the enablement prerequisite, while answer 5 correctly treats approval status as unspecified.

## Revised reader

1. **PASS: Why does this work exist?** [revised-reader-output.md](revised-reader-output.md) answer 1 gives the purpose of catching mistakes before applying.
2. **PASS: What happens in a representative case?** [revised-reader-output.md](revised-reader-output.md) answer 2 says preview should report two valid/one invalid/zero writes; answer 3 confirms counting is pending.
3. **PASS: What changes in the current increment?** [revised-reader-output.md](revised-reader-output.md) answer 3 identifies preview-only scope, complete parsing and pending counting.
4. **PASS: What remains outside it?** [revised-reader-output.md](revised-reader-output.md) answer 4 excludes Apply and preserves dependency and disabled status.
5. **PASS: What still needs a decision?** [revised-reader-output.md](revised-reader-output.md) answer 5 preserves Product's duplicate-policy decision and support-owner walkthrough approval before enablement.

## Fidelity: PASS

All required sections, decision provenance, mandatory/optional language, deployment gate and duplicate-policy ownership survive in [revised/design.md](revised/design.md). No supplied implementation is claimed verified.

Task statuses, checkbox states and dependencies are preserved in [revised/tasks.md](revised/tasks.md); zero-write wording repeats the existing accepted contract. All four original links resolve, and unselected `entry.md` and `requirements.md` remain unchanged.

Original comprehension is 5/5 when read as a whole. [oracle/expected.json](oracle/expected.json) predeclares the unexplained admission-observation language before purpose; [original/design.md](original/design.md) contains it and the revision repairs it without a claimed score gain.

## Isolation: PASS

[editor-trace.jsonl](editor-trace.jsonl) has six paired calls/results: full instructions precede four allowed subject reads; one native patch changes only `design.md`/`tasks.md`; the verification script reads only those four allowed files.

Each reader trace has two paired calls/results and reads only its own request, `design.md`, `tasks.md` and `entry.md`. Requirements, oracle, skill and other version remain unread. Final-output preservation and complete trace/request/snapshot hashes match.

## Limitations and recorded settings

- These are single AI-reader observations, not proof of improved human comprehension; text length is not a success measure.
- Isolation is assessed from prompt manifests and complete captured visible traces on a shared filesystem, not OS-enforced separation; shared cwd metadata does not establish subject-content access.
- Initial request reads used default login-shell startup and returned denied navi log-initialization warnings before the request's login:false instruction was available. Later subject reads used login:false. No out-of-manifest subject content appeared.
- Session metadata records gpt-6-astra, xhigh effort, default collaboration mode, OpenAI provider and CLI 0.159.0; temperature and an exact model build are not recorded.

Settings are supported by [editor session metadata](editor-session.json) and the trace metadata; applicable reader sessions agree. No temperature or exact build is inferred. Complete JSONL call/result sequences were audited, including nested calls. Exact repeated file contents were byte-compared when compacting the audit display; no missing or truncated trace was treated as complete.
