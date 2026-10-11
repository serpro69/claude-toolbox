I've stopped Task 1 before changing any code. As written, it conflicts with a hard acceptance requirement in the design.

**The conflict**
- **The task and implementation plan say:** `client.py` must send `require_receipt` and reject any successful response unless `applied` is true. That's unconditional.
- **The design's hard requirement says:** every merged client change must keep working with the current `provider.py`, even when `enhanced_settings` is false. Ordinary saves must keep returning success once the values are applied.
- **Where they collide:** today's `provider.py` saves the values and returns `{"ok": True}` with no `applied` field. Task 1 as written would raise `RuntimeError` on that response, and the design says it must succeed. The existing `test_ordinary_save` would fail too.

**Options.** Each one changes a written requirement, so I need your decision:
- **A. Only enforce for enhanced saves:** send `require_receipt` and require `applied` only when `enhanced_settings=True`. Ordinary saves behave as they do now. The downside is that ordinary saves never get the receipt guarantee unless a later task removes this condition.
- **B. Move enforcement out of Task 1 (my recommendation):** Task 1 only adds `require_receipt` to the request. The current provider ignores keys it doesn't know, so nothing breaks. A new task, run after Task 2's provider is released, makes `applied` mandatory for every save. This keeps the final guarantee unconditional and doesn't break any current flow. It does add a task and depends on knowing when the provider has shipped.
- **C. Accept a missing `applied`:** reject only when `applied` is present and not true. This is the weakest: any provider that never sends receipts always passes, which undercuts "trustworthy save confirmation".

**What changed:** only `docs/feat/wip/settings-receipts/tasks.md`. Task 1 is now `in-progress (blocked)`, with an Execution context section that records the conflict, the example above, the three options and the pending decision. I named you (by email) as the owner of that decision; change it if you'd rather it say something else. The Capy knowledge base was empty, so there was no earlier decision to go on. No code changed and no tests ran.

Which option do you want, A, B, C or something else? I'll record your decision in `tasks.md` and then implement, test and send it for independent review.
