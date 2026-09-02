# Contact-ratio guard

A shared producer guard. Any producer skill that emits artifacts intended to be ratified by humans tracks the artifact-to-contact ratio and stops stacking when it reaches N:0.

## Motivating failure (F5 — contact-ratio drift)

In the field, a workstream reached an artifact-to-stakeholder-contact ratio of **N:0** — increasingly sophisticated models were stacked on top of earlier, still-unratified models, with **no conversation ever scheduled**. Each artifact looked like progress. None of it had been checked against a human who could say whether it was right, so the whole stack was sophistication built on an unverified base. The more that was produced, the more expensive the eventual correction became.

The lesson: **artifact count is not progress.** A producer left to run compounds models against models because producing is cheap and a conversation is not. The value of a modelling or decision run is realized only when its output reaches someone who can ratify or refute it — and that moment has to be forced, because the producer will never reach it on its own.

## The rule — at N:0, the next unit of progress is a conversation

Track two counts across the run:

- **N — artifacts produced / models stacked** since the last human contact.
- **Contacts — stakeholder inputs consumed or decisions ratified** in the same window.

When the ratio reaches **N:0** — any number of artifacts produced, zero human contact against them — **stop stacking and declare that the next unit of progress is a conversation**:

1. **State it plainly.** Say that further modelling adds sophistication, not confidence, until a human weighs in.
2. **Name the role.** Identify **who** must be in that conversation — product owner, developer, stakeholder, customer — by the role that can decide, and the **person or ticket** if known.
3. **Route the decidable questions to them.** Hand off the queue of precise, role-tagged questions (this is what makes the conversation cheap and the ratio recoverable), rather than producing one more artifact.

The guard does not forbid producing more than one artifact between contacts — it forbids letting the contact count sit at **zero** while N climbs.

## Self-check

- What is my current artifact-to-contact ratio for this run?
- If contacts is 0, have I **stopped** and named the role who must be consulted next — or am I about to produce one more artifact?
- Is the handoff a set of **decidable, role-tagged questions**, or another model that needs its own ratification?
