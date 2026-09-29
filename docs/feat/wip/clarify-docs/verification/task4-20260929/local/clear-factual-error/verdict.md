# clear-factual-error: PASS

AI-reader comprehension: **5/5 → 5/5**. Only PASS counts; PARTIAL is not a pass. Scores use the fixed [oracle](oracle/expected.json).

## Assertions

- **6.1 — PASS.** [original-reader-output.md](original-reader-output.md) and [revised-reader-output.md](revised-reader-output.md) pass all five fixed oracle questions. Those questions omit the maximum; [oracle/expected.json](oracle/expected.json) predeclares the separate reference-threshold defect, so their passing scores do not justify leaving it.
- **6.2 — PASS.** [original/requirements.md](original/requirements.md) requires 90 and [original/prep.py](original/prep.py) declares MAX_DEFAULT_MINUTES = 90; [revised/guide.md](revised/guide.md) Reference corrects the original 60 to 90.
- **6.3 — PASS.** The only byte difference in `guide.md` is 60→90; all existing orientation, behavior, uncertainty, headings and identifiers remain unchanged.
- **6.4 — PASS.** [editor-trace.jsonl](editor-trace.jsonl) ordinals 29-34 inspect all three subject files after full instruction loading; native patch at 38 changes only `guide.md`. Complete file-map comparison verifies all other files unchanged.

## Original reader

1. **PASS: Why does this work exist?** [original-reader-output.md](original-reader-output.md) answer 1 explains a restaurant default with item exceptions.
2. **PASS: What happens in a representative case?** [original-reader-output.md](original-reader-output.md) answer 2 supplies inherited 15, explicit zero, changed default 20 affecting subsequent inherited lookups and old order 15. 'Explicit zero stays/remains zero' is read as the persistent override rule, not a time-limited value.
3. **PASS: What changes in the current increment?** [original-reader-output.md](original-reader-output.md) answer 3 identifies lookup through effective_minutes and order snapshot through create_order.
4. **PASS: What remains outside it?** [original-reader-output.md](original-reader-output.md) answer 4 excludes scheduling.
5. **PASS: What still needs a decision?** [original-reader-output.md](original-reader-output.md) answer 5 assigns the open badge decision to the product owner.

## Revised reader

1. **PASS: Why does this work exist?** [revised-reader-output.md](revised-reader-output.md) answer 1 explains a restaurant default with item exceptions.
2. **PASS: What happens in a representative case?** [revised-reader-output.md](revised-reader-output.md) answer 2 supplies inherited 15, explicit zero, changed default 20 affecting subsequent inherited lookups and old order 15. 'Explicit zero stays/remains zero' is read as the persistent override rule, not a time-limited value.
3. **PASS: What changes in the current increment?** [revised-reader-output.md](revised-reader-output.md) answer 3 identifies lookup through effective_minutes and order snapshot through create_order.
4. **PASS: What remains outside it?** [revised-reader-output.md](revised-reader-output.md) answer 4 excludes scheduling.
5. **PASS: What still needs a decision?** [revised-reader-output.md](revised-reader-output.md) answer 5 assigns the open badge decision to the product owner.

## Fidelity: PASS

The sole edit is the predeclared reference error in [original/guide.md](original/guide.md); both accepted requirements and the source constant support 90. The editor does not invent a new validation implementation or claim its runtime enforcement was tested.

All other guide bytes and source files are unchanged. Both readers' 5/5 scores measure retained comprehension, not the correctness repair itself; that repair is assessed separately against [oracle/expected.json](oracle/expected.json) and the inspected sources.

## Isolation: PASS

[editor-trace.jsonl](editor-trace.jsonl) has six paired calls/results and each reader trace has two. Full instruction reads precede guide/requirements/source inspection; the sole mutation is native apply_patch for `guide.md`.

Readers access only their own request and guide, without source-only evidence, oracle, skill or the other version. All recorded results, final messages and trace/request/snapshot hashes match; no out-of-manifest subject read was found.

## Limitations and recorded settings

- These are single AI-reader observations, not proof of improved human comprehension; text length is not a success measure.
- Isolation is assessed from prompt manifests and complete captured visible traces on a shared filesystem, not OS-enforced separation; shared cwd metadata does not establish subject-content access.
- Initial request reads used default login-shell startup and returned denied navi log-initialization warnings before the request's login:false instruction was available. Later subject reads used login:false. No out-of-manifest subject content appeared.
- Session metadata records gpt-6-astra, xhigh effort, default collaboration mode, OpenAI provider and CLI 0.159.0; temperature and an exact model build are not recorded.

Settings are supported by [editor session metadata](editor-session.json) and the trace metadata; applicable reader sessions agree. No temperature or exact build is inferred. Complete JSONL call/result sequences were audited, including nested calls. Exact repeated file contents were byte-compared when compacting the audit display; no missing or truncated trace was treated as complete.
