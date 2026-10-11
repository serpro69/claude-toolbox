I haven't started task 1 (`tasks.md` still says `pending`, no code changed). The plan conflicts with a hard requirement in the design, so I need your call first.

**The conflict:**
- **Task 1 as written:** the client sends `require_receipt` and treats a response as a failure unless it contains `applied: true`.
- **The current provider** (`provider.py:3`) stores the settings and returns only `{"ok": True}`. It has no `applied` field and ignores `require_receipt`. Applied receipts don't arrive until task 2.
- **`design.md`:** every merged client increment must work with the current provider, including when `enhanced_settings` is false, and ordinary saves must keep succeeding once values are applied. The design calls this a hard acceptance requirement.

So if task 1 ships as planned, every save against today's provider would report failure even though the values were stored. Mocked client tests with an applied receipt would pass and hide this.

**Options:**
1. **Accept responses without a receipt for now (recommended).** The client sends `require_receipt`, accepts `applied: true` as confirmed, rejects `applied: false`, and treats a response with no `applied` field as an ordinary save that still succeeds. The tests would cover all three cases, including the exact response today's provider returns. Strict enforcement waits until the provider supports receipts, after task 2. I'd update `implementation.md` and the task 1 checkbox to match.
2. **Swap the order.** Do task 2 (provider receipts) first, then task 1. The catch: the two are released separately, so a new client can still meet an older provider in the field. This only works if you can guarantee release order.
3. **Proceed as written.** This breaks the independent-delivery requirement, so I'd advise against it.

Which do you want? If it's option 1, I'll update the plan docs and then implement task 1.
