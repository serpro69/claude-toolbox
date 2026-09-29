# source-disagreement: PASS

AI-reader comprehension: **2/5 → 5/5**. Only PASS counts; PARTIAL is not a pass. Scores use the fixed [oracle](oracle/expected.json).

## Assertions

- **2.1 — PASS.** [revised/guide.md](revised/guide.md):10-18 explicitly contrasts required next-day behavior with immediate current lookup, preserving earlier order 15; [revised-reader-output.md](revised-reader-output.md) answers 1-5 match [oracle/expected.json](oracle/expected.json).
- **2.2 — PASS.** [revised/guide.md](revised/guide.md):11-13 and :20-24 calls the next-day rule mandatory and still binding while describing immediate code behavior, without changing either evidence source.
- **2.3 — PASS.** [editor-trace.jsonl](editor-trace.jsonl) ordinals 19-27 load full instructions; 29-34 inspect guide, requirements and implementation; the patch follows at 38.
- **2.4 — PASS.** [revised/guide.md](revised/guide.md):20-24 names the feature maintainer and concrete reconciliation options: implement accepted timing or obtain an explicit requirements decision. It retains the unresolved scheduling boundary and claims no implementation fix.
- **2.5 — PASS.** Recomputed original/ and revised/ hash maps differ only for `guide.md`; [editor-trace.jsonl](editor-trace.jsonl) ordinals 38-46 show only its native patch and readback.

## Original reader

1. **PASS: Why does this work exist?** [original-reader-output.md](original-reader-output.md) answer 1 identifies defaults with item exceptions.
2. **FAIL: When a restaurant default changes from 15 to 20, what happens to new inherited lookups and existing orders?** [original-reader-output.md](original-reader-output.md) answer 2 presents new inherited lookups remaining 15 until tomorrow as current behavior. [oracle/expected.json](oracle/expected.json) requires distinguishing intent from the current immediate return of 20; the original guide does not expose that discrepancy.
3. **PARTIAL: What changes in the current increment?** [original-reader-output.md](original-reader-output.md) answer 3 identifies lookup and order snapshots but does not identify their timing mismatch. Answer 4's scheduling ambiguity is not a statement of the actual intent/code disagreement.
4. **PASS: What remains outside it?** [original-reader-output.md](original-reader-output.md) answer 4 correctly excludes scheduling.
5. **PARTIAL: What still needs a decision?** [original-reader-output.md](original-reader-output.md) answer 5 preserves Product's badge decision but omits the feature maintainer's timing-reconciliation responsibility required by [oracle/expected.json](oracle/expected.json).

## Revised reader

1. **PASS: Why does this work exist?** [revised-reader-output.md](revised-reader-output.md) answer 1 states the default/item-exception purpose.
2. **PASS: When a restaurant default changes from 15 to 20, what happens to new inherited lookups and existing orders?** [revised-reader-output.md](revised-reader-output.md) answer 2 states required next-day 15 versus immediate implemented 20 and old order 15.
3. **PASS: What changes in the current increment?** [revised-reader-output.md](revised-reader-output.md) answer 3 states lookup and snapshots; answer 2 explicitly supplies the oracle's timing-mismatch qualification. Evaluated as a whole.
4. **PASS: What remains outside it?** [revised-reader-output.md](revised-reader-output.md) answer 4 excludes scheduling and preserves the unresolved boundary.
5. **PASS: What still needs a decision?** [revised-reader-output.md](revised-reader-output.md) answer 5 states Product's badge decision and the maintainer's reconciliation action without discarding the requirement.

## Fidelity: PASS

[revised/guide.md](revised/guide.md) preserves mandatory next-day intent, zero overrides and unchanged snapshots against [original/requirements.md](original/requirements.md); [original/prep.py](original/prep.py) supports the separately described immediate current behavior.

The owner and next step remain explicit, source links resolve within the captured file set, and the document neither changes requirements nor claims code has been fixed. The predeclared factual discrepancy justifies the revision.

## Isolation: PASS

[editor-trace.jsonl](editor-trace.jsonl) has six paired calls/results; each reader trace has two. Full shared instructions return before all three allowed subject files. The native patch and readback affect only the selected guide.

Both readers read only their own request and guide, leaving the guide's evidence links unfollowed as required. Final output preservation and all trace/request/snapshot hashes match; no missing result or out-of-manifest subject read was found.

## Limitations and recorded settings

- These are single AI-reader observations, not proof of improved human comprehension; text length is not a success measure.
- Isolation is assessed from prompt manifests and complete captured visible traces on a shared filesystem, not OS-enforced separation; shared cwd metadata does not establish subject-content access.
- Initial request reads used default login-shell startup and returned denied navi log-initialization warnings before the request's login:false instruction was available. Later subject reads used login:false. No out-of-manifest subject content appeared.
- Session metadata records gpt-6-astra, xhigh effort, default collaboration mode, OpenAI provider and CLI 0.159.0; temperature and an exact model build are not recorded.

Settings are supported by [editor session metadata](editor-session.json) and the trace metadata; applicable reader sessions agree. No temperature or exact build is inferred. Complete JSONL call/result sequences were audited, including nested calls. Exact repeated file contents were byte-compared when compacting the audit display; no missing or truncated trace was treated as complete.
