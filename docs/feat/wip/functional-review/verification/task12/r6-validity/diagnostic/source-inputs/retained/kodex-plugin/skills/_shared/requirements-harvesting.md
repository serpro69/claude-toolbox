# Requirements-harvesting gate

A shared producer guard. Any producer skill that models, decides, or documents against stated requirements runs this gate before producing.

## Motivating failure (F1 — fabricated requirements)

In the field, four working sessions modelled a feature against an **invented stakeholder brief** while the two real tickets — carrying the actual asks and named stakeholders — sat unread, one query away. The invented brief was materially wrong about both scope and direction, so every artifact built on it inherited the error. The cost was not a modelling mistake; it was modelling the wrong thing well.

The lesson: an LLM will confabulate a plausible brief rather than go find the real one, because a plausible brief is cheaper than a search. The guard removes the shortcut.

## The rule — harvest before you produce

This is a **mandatory workflow step**, executed before any modelling, decision, or drafting touches the subject matter:

1. **Enumerate the real inputs.** List every linked ticket, issue, spec, or referenced document the request names or points at. Follow **one hop** of references out from each (a ticket that cites another ticket, a spec that links a decision record).
2. **Read them, then quote the asks.** Read each input in full and copy the **actual asks — verbatim — into your working notes**, attributed to their source (ticket id, author, stakeholder). Quoting, not paraphrasing: a paraphrase is where the invented brief creeps back in.
3. **Only now produce.** Modelling, decisions, and drafts derive from the quoted asks, not from a reconstruction of what the asks probably were.

## When real input genuinely does not exist

Fabricated input is permitted **only as a labeled last resort**, and only when a search has confirmed no real input exists. When you must invent:

- **Label it as invented** at the point of use — never let a fabricated ask read as a harvested one.
- **State what real input would replace it** — the ticket, the role, or the conversation that, once available, supersedes the placeholder.

A labeled fabrication is honest and actionable; a silent one reproduces F1.

## Self-check

- Did I enumerate the linked inputs and follow one hop — or did I start from the code / my own reconstruction?
- Are the asks in my notes **quoted from a named source**, or paraphrased?
- Is every fabricated input explicitly labeled, with its real-input replacement named?
