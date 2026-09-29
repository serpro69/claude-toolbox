# dense-source: PASS

AI-reader comprehension: **5/5 → 5/5**. Only PASS counts; PARTIAL is not a pass. Scores use the fixed [oracle](oracle/expected.json).

## Assertions

- **1.1 — PASS.** [revised/guide.md](revised/guide.md):3-31 supports purpose, the complete example, resolution/snapshot increment, scheduling exclusion and Product's badge decision; [revised-reader-output.md](revised-reader-output.md) answers 1-5 pass.
- **1.2 — PASS.** [revised/guide.md](revised/guide.md):7-10 retains missing/null inheritance and explicit zero; :17-23 preserves live lookup and saved orders; :25-31 preserves owner, identifiers and exclusions, consistent with [original/requirements.md](original/requirements.md) and [original/prep.py](original/prep.py).
- **1.3 — PASS.** [editor-trace.jsonl](editor-trace.jsonl) ordinals 19-27 load complete skill/shared instructions before subject reads at 29-34; both `requirements.md` and `prep.py` return before the edit at 38.
- **1.4 — PASS.** [revised/guide.md](revised/guide.md) opens with owner-facing purpose, works through 15→20 with inherited value, zero and earlier order, and defines snapshot/materialization where those terms first appear at :30-31.
- **1.5 — PASS.** original/ and revised/ complete hash maps in [manifest.json](manifest.json) match independently recomputed files except `guide.md`; [editor-trace.jsonl](editor-trace.jsonl) ordinals 38-48 show the sole write and readback, with no added artifact.

## Original reader

1. **PASS: Why does this work exist?** [original-reader-output.md](original-reader-output.md) answer 1 identifies restaurant default plus item exceptions ([original/guide.md](original/guide.md):6-7).
2. **PASS: What happens in a representative case?** [original-reader-output.md](original-reader-output.md) answer 2 supplies initial 15 and zero, says changing to 20 updates inherited reads, and keeps copied order values. Read semantically, the previously specified copied value remains 15 and the explicit zero override persists; no contrary behavior is stated.
3. **PASS: What changes in the current increment?** [original-reader-output.md](original-reader-output.md) answer 3 identifies resolution and copying into each new order ([original/guide.md](original/guide.md):6-9).
4. **PASS: What remains outside it?** [original-reader-output.md](original-reader-output.md) answer 4 excludes scheduling.
5. **PASS: What still needs a decision?** [original-reader-output.md](original-reader-output.md) answer 5 assigns the inheritance-badge decision to the product owner.

## Revised reader

1. **PASS: Why does this work exist?** [revised-reader-output.md](revised-reader-output.md) answer 1 identifies one default with item exceptions.
2. **PASS: What happens in a representative case?** [revised-reader-output.md](revised-reader-output.md) answer 2 gives initial 15/zero, later inherited lookup and new orders at 20, and earlier order 15; answer 3's explicit-value override rule supplies the persistent zero qualification. The answer is evaluated as a whole.
3. **PASS: What changes in the current increment?** [revised-reader-output.md](revised-reader-output.md) answer 3 identifies resolution and saving the resolved value at creation.
4. **PASS: What remains outside it?** [revised-reader-output.md](revised-reader-output.md) answer 4 excludes scheduling.
5. **PASS: What still needs a decision?** [revised-reader-output.md](revised-reader-output.md) answer 5 preserves product-owner ownership and the unresolved badge decision.

## Fidelity: PASS

All protected claims are present in [revised/guide.md](revised/guide.md) and agree with [original/requirements.md](original/requirements.md) and [original/prep.py](original/prep.py); the heading remains intact and no executable example, link or task state was removed.

Both readers score 5/5. [oracle/expected.json](oracle/expected.json) predeclares independent orientation defects: storage before purpose, late definition of materialization, and implicit scenario results. Those defects are present in [original/guide.md](original/guide.md) and addressed in the revision; the edit is justified without claiming a comprehension-score gain.

## Isolation: PASS

[editor-trace.jsonl](editor-trace.jsonl): six calls/six results; [original-reader-trace.jsonl](original-reader-trace.jsonl) and [revised-reader-trace.jsonl](revised-reader-trace.jsonl): two calls/two results each. Every call, nested exec operation and returned subject text stays within its [editor-request.md](editor-request.md) or reader request manifest.

Reader traces show only each reader's own request and guide; no opposite version, source-only files, oracle or skill access. All three visible final messages exactly match their output files; trace/request hashes and session settings match the captured metadata.

## Limitations and recorded settings

- These are single AI-reader observations, not proof of improved human comprehension; text length is not a success measure.
- Isolation is assessed from prompt manifests and complete captured visible traces on a shared filesystem, not OS-enforced separation; shared cwd metadata does not establish subject-content access.
- Initial request reads used default login-shell startup and returned denied navi log-initialization warnings before the request's login:false instruction was available. Later subject reads used login:false. No out-of-manifest subject content appeared.
- Session metadata records gpt-6-astra, xhigh effort, default collaboration mode, OpenAI provider and CLI 0.159.0; temperature and an exact model build are not recorded.
- [editor-trace.jsonl](editor-trace.jsonl) ordinal 38 used a shell heredoc for the staged guide instead of native apply_patch. The first [editor-request.md](editor-request.md) did not yet explicitly require native apply_patch; record this execution-method limitation separately from content isolation.

Settings are supported by [editor session metadata](editor-session.json) and the trace metadata; applicable reader sessions agree. No temperature or exact build is inferred. Complete JSONL call/result sequences were audited, including nested calls. Exact repeated file contents were byte-compared when compacting the audit display; no missing or truncated trace was treated as complete.
