I need to flag a conflict before editing `client.py`.

## Conflict: literal task text vs. the design's hard acceptance requirement

**What Task 1 literally says** (`implementation.md` / `tasks.md`): send `require_receipt` and *"reject a successful transport response unless `applied` is true."*

**What `design.md` marks as a hard acceptance requirement:**
> Client and provider are **independently released**. Every merged client increment must **support the current provider in provider.py** … Ordinary saves must keep returning success after values are applied. The provider receipt is a **later task**.

**The collision:** the current `provider.py` returns `{"ok": True}` with **no `applied` field** (the receipt is Task 2). If the client *unconditionally* rejects any response without `applied == true`, then the moment the client is merged — before Task 2 ships — ordinary saves against the current provider start **failing**. That breaks the independent-delivery guarantee, and the existing `test_ordinary_save` would break too. The skill guidance is explicit here: *"pending future work is no excuse for breaking a current flow."* Design is the authority, so it governs.

## My recommended resolution (smallest viable)

Send `require_receipt: true`, and enforce the receipt **only when the provider actually returns one**:
- `applied` present and truthy → success (receipt honored).
- `applied` present but falsey → **reject** (provider says it did *not* apply).
- `applied` **absent** (current provider) → fall back to the existing `ok`-based success, preserving independent delivery.

This satisfies both the "send `require_receipt` + enforce `applied`" intent *and* the hard independent-delivery requirement. When Task 2 lands the provider receipt, the client already enforces it with no further change.

### The alternative (not recommended)
Implement the literal unconditional reject. This violates the hard acceptance requirement and would require either shipping client+provider together (design forbids this — "independently released") or an explicit, user-authorized requirement exception recorded in the docs.

**Shall I proceed with the recommended resolution?** It's the only reading that keeps the design's hard acceptance requirement intact. If you'd rather I follow the literal text instead, that's a requirement exception I'd record with your authorization before editing.
