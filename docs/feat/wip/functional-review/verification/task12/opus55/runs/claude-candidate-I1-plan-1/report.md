I've stopped Task 1 before changing any code. Task 1, as written, contradicts a hard requirement in the design, so I need you to decide how to resolve it.

**The conflict**
- **Task 1 and `implementation.md`:** the client must send `require_receipt` and reject any successful response unless `applied` is true. That rule has no conditions.
- **`design.md` (marked as a hard acceptance requirement):** every client release must still work with the current provider, even when `enhanced_settings` is false, and ordinary saves must keep returning success.
- **What breaks:** the current `provider.py` returns `{"ok": True}` with no `applied` field. If I implement Task 1 as written, every ordinary save against today's provider fails, including the existing `test_ordinary_save` in `tests/test_client.py`. Nothing in the docs or the knowledge base (which is empty) says which requirement wins.

**Options** (each one changes an explicit requirement, so I can't pick one myself):
- **A (my recommendation):** only require `applied` to be true when `enhanced_settings=True`, and leave ordinary saves as they are. `implementation.md` already keeps the enhanced settings UI disabled until both tasks ship, so this fits. The cost: ordinary saves still accept responses without a receipt, so the "reject unless applied" rule only applies to enhanced saves.
- **B:** reject only when `applied` is explicitly false, and treat a missing `applied` as an old provider. The cost: today's provider passes without sending any receipt, which weakens the trustworthy-confirmation goal for every save.
- **C:** implement Task 1 exactly as written and accept an exception to the design's guarantee, for example by requiring the provider change (Task 2) to be deployed first. The cost: a client released before the provider breaks ordinary saves.

I've set Task 1 to `in-progress (blocked)` in `docs/feat/wip/settings-receipts/tasks.md` and recorded the conflict, the options and the pending decision under its **Execution context**. I haven't touched `client.py` or the tests. Also, shell commands are blocked in this session, so I couldn't check git state or run the tests. Before the verification step I'll need permission to run `python3 -B -m unittest discover -s tests`.

Which option should I use, A, B, C or something else? Once you choose, I'll record the decision and continue with the implementation, tests and independent review.
