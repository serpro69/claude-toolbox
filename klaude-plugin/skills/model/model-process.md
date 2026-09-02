# `/kk:model` — production workflow

The authoritative seven-phase workflow. SKILL.md carries the one-line phase summary; this file carries the full procedure. Phases run **strictly in order** — each phase exists to prevent a recorded field failure (the F-numbers cited below; each guard file opens with its failure), and reordering re-creates the failure the order prevents.

Phases 1–2 touch no domain code. Phase 3 is the single point where domain source is read — the content-read step appears exactly once, there (ADR-0004). Phases 4–7 work from what phases 2–3 harvested; they re-open sources to check claims, never to widen scope.

<!-- Brownfield intake/close specifics are extended in M2 Task 4 (docs/wip/architect-skills/model/tasks.md). The greenfield path below is complete; brownfield is covered at the level SKILL.md states (read in full, deltas only, no unilateral marker flips). -->

## Phase 1 — Scope intake

Establish three things, in conversation with the user where the request leaves them open:

1. **The bounded context.** The domain slice being modelled — one kit (glossary + traps pair) serves one context. If the request spans several contexts, pick the one the forcing question lives in and say so.
2. **The forcing question.** The feature, ticket, or decision that makes modelling worth doing *now*. It bounds everything downstream: what archaeology reads, how many terms the glossary carries, which questions reach the decision queue. Model in service of the decision — a run with no forcing question boils the ocean, and an ocean-boiling model is sophistication nobody asked for. If the user names none, ask for one before proceeding.
3. **The mode.**
   - **Greenfield** — no kit exists for this context. Produce the initial two pages (+ the conventions index if the home has none), per [kit-contract.md](kit-contract.md).
   - **Brownfield** — an existing kit is found (check the homes in [kit-contract.md](kit-contract.md) §Homes-resolution precedence) or pointed at. Read it **in full** before anything else; it becomes the baseline and every change is a delta. Existing status markers are **never flipped unilaterally** — `proposed → canonical` requires a recorded human decision, which is out of this skill's scope.

Close intake with the capy knowledge search per [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md): query `kk:arch-decisions` and `kk:project-conventions` for prior modelling decisions and conventions in this area. Empty results are normal; contradicting results are raised with the user before proceeding.

## Phase 2 — Requirements-harvesting gate (F1)

Run [shared-requirements-harvesting.md](shared-requirements-harvesting.md) in full before any modelling:

- Enumerate every ticket, issue, spec, or document the request names, plus **one hop** of references out from each.
- Read them and **quote the actual asks verbatim** into the working notes, attributed to their source (ticket id, author, stakeholder). Paraphrase is where an invented brief creeps back in.
- Fabricated input only as a labeled last resort when a search has confirmed no real input exists — labeled at the point of use, naming the real input that would replace it.

The quoted asks are the spine the rest of the run hangs on: archaeology reads what the asks stress, the kit models what the asks need, and the decision queue routes what the asks leave open.

## Phase 3 — Archaeology

Read the domain source per [archaeology.md](archaeology.md): the **state → time → invariants** order, under **two-clock discipline** (code-clock facts are verifiable and citable; intent derived from code is a presumption that stays `proposed`), scoped by the forcing question. This is the run's only subject-matter reading step.

Working notes from this phase record, for every fact: the file/symbol it derives from (no line numbers), and which clock it sits on.

## Phase 4 — Draft the kit

Draft per [kit-contract.md](kit-contract.md) — it is the complete format authority:

- Resolve the **home** first, per the contract's precedence (brownfield location → user-declared home → propose `docs/architecture/` and **confirm before writing**).
- Produce the glossary page and the divergences/traps page; add the conventions index only if the home has none.
- Anything beyond the two pages (durable ERDs, standing model pages) triggers the contract's **kit-scope pushback** — name the maintenance cost before complying.

## Phase 5 — Verify (F4)

Two distinct passes, per [shared-open-question-pass.md](shared-open-question-pass.md):

1. **Confirm-pass** — re-check every drafted claim against its cited source. Catches drift and staleness; cannot catch omissions.
2. **Open-question pass** — re-walk the same sources asking **new questions**, with the confirm-pass results out of view: cardinalities, single-result lookups, unchecked writes, silent defaults, time and ordering. Anything surfaced that is not already a written claim is a finding — record it as a new claim, a traps entry, or a decision-queue question. Never discard it.

## Phase 6 — Conventions-bind-author self-check (F6)

Grade the produced pages against the checklist in [kit-contract.md](kit-contract.md) §Conventions-bind-author self-check — the author obeys the kit's own declared conventions (status markers justified, no line numbers, Derived-from complete, exactly one diagram, no schema mirror, ticket notes carry retirement conditions, both banners present). Fix violations before surfacing; a kit that breaks its own contract is not done.

## Phase 7 — Surface & close (F5, F2)

1. **Present the decision queue.** Each entry (RQ) is one **precise, decidable question** tagged with the **role** that can decide it — product owner, developer, stakeholder, customer — plus the person or ticket if known, and what the answer unblocks. Precise-and-decidable is the bar: a role holder reading the RQ can answer it in a sentence.

   > **RQ-1** — Does a hold expire if the patron never collects, and after how many days? — **Decider:** product owner — **Unblocks:** rule L4, term `Hold`.

   The queue is presented inline, and **appended to the active feature's `docs/wip/<feature>/design.md` under an "Open Questions" heading when that feature directory exists** (inline-only otherwise).
2. **Apply the contact-ratio guard** per [shared-contact-ratio-guard.md](shared-contact-ratio-guard.md): if this run brings the artifact-to-stakeholder-contact ratio to N:0, state plainly that the next unit of progress is a conversation, name the role (and person/ticket if known), and route the decision queue to them instead of producing more.
3. **Brownfield only — fact-flip propagation** per [shared-fact-flip-propagation.md](shared-fact-flip-propagation.md): any recorded fact this run contradicted is fixed at **every** occurrence across the workspace in this same session, not just where it was noticed.
4. **Index the rationale.** Per [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md), index non-obvious modelling rationale (why a term was scoped this way, why a status is `undecided`) to `kk:arch-decisions`. Skip anything self-evident from the kit pages themselves.
