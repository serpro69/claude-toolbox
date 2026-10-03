# Equipment lending brief

The operations owner asks: "Before we add checkout validation, determine whether one physical item may have multiple active loans." This is an unresolved business decision, not an approved uniqueness rule.

An item is a physical piece of equipment identified by an inventory tag. A loan records one person borrowing one item. A loan without returned_at is currently active. The data snapshot is evidence of stored records only; no runtime code or enforcement implementation is supplied. The domain kit should expose the decision to the operations owner before anyone changes checkout.
