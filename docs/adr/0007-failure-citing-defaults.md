# ADR 0007: Producer Rules Are Failure-Citing, Falsifiable Defaults

## Status

Accepted (2026-09-03)

## Context

The producer skills of the architecture flow (`/kk:model` in Milestone 2;
`decide` and later producers to follow) encode workflow rules derived
from field evidence — initially a **single** real-world architect
workstream (n=1). Rules generalized from one data point risk two failure
modes: silently ossifying into ceremony nobody can justify, or being
deleted wholesale when one of them proves wrong.

ADR 0004 is the nearest precedent in kind — it grounds its rule in
recorded failure transcripts rather than assertion, and that grounding
is what kept it revisable. Milestone 2 extends the producer surface substantially
(four shared guards, a seven-phase workflow, kit conventions), all on
n=1 evidence, so the encoding discipline itself needed deciding.

## Decision

Producer rules derived from field evidence are encoded as **explicit
defaults that each cite their motivating failure**, and are treated as
**falsifiable**: when a later workstream contradicts a rule, the rule is
revised or deleted — cheaply, because the citation makes its purpose
checkable.

Concretely, each shared producer guard
(`klaude-plugin/skills/_shared/requirements-harvesting.md`,
`open-question-pass.md`, `fact-flip-propagation.md`,
`contact-ratio-guard.md`) opens with the recorded failure it prevents
(F1/F4/F2/F5 in the M2 design's evidence base) before stating the rule.

**First falsification recorded:** a proposed fifth guard — a
"session-close state-rewrite" step — was judged a false-positive finding
during design review and is deliberately absent from M2. It was dropped
at design time with zero code cost. Do not re-introduce a
session-close/handoff guard without new field evidence.

## Consequences

- Every producer guard is auditable: a reader can check whether the
  cited failure still motivates the rule, and a second workstream that
  contradicts one identifies exactly which rule to revise.
- The evidence base stays honest about its size — n=1 defaults are
  labeled as such in the design docs, not presented as proven practice.
- Revision is expected, not exceptional: the session-close guard's
  falsification is the first data point that this keeps change cheap.
- New producer rules without a citable motivating failure need explicit
  justification — "seems prudent" is not an admission criterion for a
  guard.
- Evidence base and per-failure catalog:
  `docs/wip/architect-skills/model/design.md` §1 (frozen into
  `docs/done/` on completion).
