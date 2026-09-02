---
name: model
description: |
  Produce or update a domain-reference kit — the durable glossary + divergences/traps pages for a bounded context. Use for domain modelling, information architecture, building a domain glossary or domain model, mapping domain concepts to code (bindings), or surfacing the decidable questions stakeholders must close before design. Runs upstream of feature $kk:design as the first producer of the architecture flow, and emits artifacts $kk:review-architecture verifies. Triggers: "model the domain", "build a glossary", "domain reference", "bounded context", "what are the concepts here". NOT for behavioral code review or writing a feature design doc.
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Domain Modelling — the steady-state kit

**Goal: produce a provenance-clean domain-reference kit and, above all, a decision queue of precise, role-tagged questions a human can close.** The queue is the primary output — artifact count and model sophistication are explicitly not the metric.

`$kk:model` is the first **producer** of the architecture flow: it runs at information-architecture altitude (what the domain's concepts are, where they bind to code, and which questions about them only a human can close), upstream of feature `$kk:design` and never called by it. It writes files and interacts with you mid-flow — it is a main-session skill, not a read-only reviewer.

## Conventions

- **Capy knowledge base** — read [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md); searched at intake (`kk:arch-decisions`, `kk:project-conventions`), indexed at close.
- **Shared producer guards** — four workflow guards, each citing the field failure it prevents. Load all four before acting:
  - [shared-requirements-harvesting.md](shared-requirements-harvesting.md) — quote the real asks before modelling (F1).
  - [shared-open-question-pass.md](shared-open-question-pass.md) — verification asks new questions, not just re-confirms (F4).
  - [shared-fact-flip-propagation.md](shared-fact-flip-propagation.md) — a contradicted fact is fixed everywhere in-session (F2).
  - [shared-contact-ratio-guard.md](shared-contact-ratio-guard.md) — at N:0 artifacts-to-contacts, the next step is a conversation (F5).
- **Profiles are not consulted** — `$kk:model` is language-agnostic in M2; archaeology reads code directly. Profile enrichment is deferred (design §8).

## Workflow

**Mandatory order — instructions before subject matter.** The flow is strictly sequential. Do **not** read code to model it, draft any kit page, or engage the domain beyond a mode-detecting directory/keyword scan until every instruction file is loaded: this SKILL.md, the process file [model-process.md](model-process.md), the reading method [archaeology.md](archaeology.md), the output contract [kit-contract.md](kit-contract.md), all four shared guards above, and the shared capy protocol. This ordering is load-bearing (ADR 0004): with domain code in context before the contracts load, the model emits plausible terms and skips the methodology that makes them trustworthy.

1. **Load instructions.** Read [model-process.md](model-process.md) (the detailed seven-phase workflow), [archaeology.md](archaeology.md), [kit-contract.md](kit-contract.md), all four shared guards — [shared-requirements-harvesting.md](shared-requirements-harvesting.md), [shared-open-question-pass.md](shared-open-question-pass.md), [shared-fact-flip-propagation.md](shared-fact-flip-propagation.md), [shared-contact-ratio-guard.md](shared-contact-ratio-guard.md) — and [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md). Minimal early scope — a directory listing or a keyword scan of the request — is permitted only to drive mode detection.
2. **Execute the seven phases** per [model-process.md](model-process.md):
   1. **Scope intake** — establish the bounded context, the **forcing question** (the feature/ticket that bounds what is worth modelling), and the **mode** (greenfield: no kit exists → produce the two pages; brownfield: an existing kit is read in full first and all changes are deltas, status markers never flipped unilaterally). Run the capy knowledge search.
   2. **Requirements-harvesting gate** *(guard, F1)* — read every linked ticket + one hop; quote the actual asks into working notes before any modelling.
   3. **Archaeology** — read code **state → time → invariants** per [archaeology.md](archaeology.md); two-clock discipline (code-clock facts verifiable, intent stays `proposed`).
   4. **Draft the kit** per [kit-contract.md](kit-contract.md) — glossary page + divergences/traps page (+ conventions index if the home has none).
   5. **Verify** — at least one confirm-pass **plus at least one open-question pass** *(guard, F4)*.
   6. **Self-check** — conventions-bind-author lint: the produced pages obey the kit's own declared conventions.
   7. **Surface & close** — present the **decision queue** (each RQ precise, decidable, role-tagged); apply the **contact-ratio guard** *(F5)*; in brownfield, **fact-flip propagation** *(F2)* on any contradicted recorded fact; index non-obvious rationale to `kk:arch-decisions`.

## Required Outputs

- [ ] The two durable kit pages (glossary + traps) for the context, provenance-clean, per [kit-contract.md](kit-contract.md) (+ conventions index if the home lacked one).
- [ ] The **decision queue** — precise, decidable, role-tagged questions — presented inline and appended to the active feature's `docs/wip/<feature>/design.md` under an **Open Questions** heading when that directory exists.
- [ ] Contact-ratio guard applied; brownfield fact-flips propagated across the workspace.
- [ ] Non-obvious modelling rationale indexed to `kk:arch-decisions`.
