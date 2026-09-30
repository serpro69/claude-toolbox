1. **Why this exists:** Restaurant owners need a default preparation time with exceptions for individual items. Null or missing `prep_minutes` inherits the default; an explicit value, including zero, overrides it. (§ “Preparation updates,” paragraph 1.)

2. **When the default changes from 15 to 20:** The described implementation immediately returns 20 for new inherited lookups. The accepted requirement instead requires those lookups to remain 15 until the next day. Existing orders retain their stored snapshot of 15 under both. (§ “Preparation updates,” paragraphs 2–3.)

3. **Current increment:** It delivers preparation-time lookup and order snapshots, with each snapshot storing the effective preparation time at order creation. The guide does not specify which parts are newly added versus already implemented. (§ “Preparation updates,” paragraphs 1–2.)

4. **Outside the increment:** Scheduling is explicitly excluded. How that exclusion accommodates the accepted next-day requirement remains unresolved; no other exclusions are stated. (§ “Preparation updates,” paragraphs 1 and 4.)

5. **Remaining decisions:** The feature maintainer must reconcile immediate lookup behavior with the accepted next-day requirement and clarify its relationship to the scheduling exclusion. The requirement itself remains accepted. Product must decide whether and how inherited values should be indicated. (§ “Preparation updates,” paragraphs 4–5.)
