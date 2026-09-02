# `$kk:model` — archaeology reading method

How phase 3 reads domain source. The method exists because unordered reading produces a term inventory; ordered reading produces the facts a kit needs — what is enforced, what merely declared, and what silently assumed.

## Scope — model in service of the decision

The forcing question from intake bounds the read. Start from the entry points the question names (the feature's handlers, the ticket's modules) and follow references outward only while they bear on the question. A file the decision never touches is out of scope no matter how interesting — breadth is the ocean-boiling failure the forcing question exists to prevent. If mid-read the question turns out to stress a module outside the original scope, widen deliberately and say so; never widen by drift.

## Reading order — state → time → invariants

Three passes over the scoped source, each asking one kind of question. Keep them separate: mixing them is how a reader confirms structure while missing behavior.

1. **State.** What are the domain's states and transitions — and which are **actually enforced** versus merely declared? A status enum declares states; only the code that guards a transition enforces one. Record where each state lives (field, constant, collection) and, for every declared rule, whether any code path enforces it. Declared-but-unenforced is a finding, not a detail — it is traps-page material.
2. **Time.** Where does time enter the lifecycle? Timestamps, expiries, schedules, auto-transitions, background sweeps. For each: what fires it, and what it mutates. Time-driven mutations are where states drift out from under readers — a transition no user action triggers is exactly the kind of fact no single file reveals.
3. **Invariants.** What does the system silently assume? Uniqueness, cardinality, ordering, non-overlap, "exactly one result". For each assumption: is it enforced at the write path, or merely expected at the read path? Focus on the assumptions the forcing question stresses. This pass seeds phase 5's open-question checklist — an assumption noticed here and confirmed nowhere is a question, not a fact.

## Two-clock discipline

Every fact recorded from archaeology sits on one of two clocks, and the working notes say which:

- **Code clock** — what the code verifiably does. Citable to a file or symbol (never a line number); `$kk:review-architecture` can re-check it mechanically.
- **Business clock** — what the business *means*. Never derivable from code alone: code establishes code-clock facts only. Intent reverse-engineered from code — "this limit exists, so the business must want it" — is a **presumption**, recorded as `proposed` until a human with domain authority ratifies it (F3). The presumption is honest; presenting it as settled intent is the failure.

A code fact never ratifies a business intent. When the two clocks disagree — the code does X, a stated rule says Y — that disagreement is a divergence for the traps page and usually a decision-queue question, not something to reconcile silently in either direction.
