# `/kk:model` — production workflow

The authoritative seven-phase workflow. SKILL.md carries the one-line phase summary; this file carries the full procedure. Phases run **strictly in order** — each phase exists to prevent a recorded field failure (the F-numbers cited below; each guard file opens with its failure), and reordering re-creates the failure the order prevents.

Phases 1–2 touch no domain code. Phase 3 is the single point where domain source is read — the content-read step appears exactly once, there (ADR-0004). Phases 4–7 work from what phases 2–3 harvested; they re-open sources to check claims, never to widen scope.

## Phase 1 — Scope intake

Establish three things, in conversation with the user where the request leaves them open:

1. **The bounded context.** The domain slice being modelled — one kit (glossary + traps pair) serves one context. If the request spans several contexts, pick the one the forcing question lives in and say so.
2. **The forcing question.** The feature, ticket, or decision that makes modelling worth doing *now*. It bounds everything downstream: what archaeology reads, how many terms the glossary carries, which questions reach the decision queue. Model in service of the decision — a run with no forcing question boils the ocean, and an ocean-boiling model is sophistication nobody asked for. If the user names none, ask for one before proceeding.
3. **The mode.**
   - **Greenfield** — no kit exists for this context. Produce the initial two pages (+ the conventions index if the home has none), per [kit-contract.md](kit-contract.md).
   - **Brownfield** — an existing kit is found (check the homes in [kit-contract.md](kit-contract.md) §Homes-resolution precedence) or pointed at. Follow §Brownfield intake below.

### Brownfield intake

The existing kit is the **baseline**; the run updates it, never replaces it.

1. **Read the kit in full first** — glossary page, traps page, and the home's conventions index — before phase 2 runs. This is baseline-loading, not domain reading; phase 3 remains the run's only domain-source read. A delta computed against a half-read baseline is a rewrite wearing a delta's name.
2. **Every change is a delta.** The baseline's structure is the frame: entries the drift does not touch stay as they are, `D#`/`P#` numbers are never reset or reused, and the home's conventions index is never rewritten — the updated pages conform to it. If the baseline conflicts with [kit-contract.md](kit-contract.md), raise the conflict with the user; do not silently reformat.
3. **Status markers are never flipped unilaterally.** In particular, discovering that code **now enforces** a `proposed` rule updates the rule's *enforcement pointer*, not its status — enforcement is a code-clock fact, and `canonical` records a human ratification no code change can substitute for (F3). `proposed → canonical` requires a recorded human decision, out of this skill's scope.

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
3. **Brownfield only — fact-flip propagation** per [shared-fact-flip-propagation.md](shared-fact-flip-propagation.md): any recorded fact this run contradicted is fixed at **every** occurrence across the workspace in this same session, not just where it was noticed. The usual shapes of a contradicted fact in a kit update:
   - **A stale binding** — the symbol a kit entry cites was renamed or moved. Fix every page that asserts the old name: entry Bindings, traps-page prose, the rules table — a rename fixed in the glossary but still asserted on the traps page is F2 verbatim.
   - **A vanished enforcement** — code a rule's pointer cites no longer exists. Correct the pointer (declared-not-enforced, or a new `D#`), drop the path from the Derived-from footer, and route the question of whether the removal was deliberate to the decision queue — never silently drop the rule.
   - **A met retirement condition** — the divergence a traps entry describes has been fixed. Delete the entry in this update (self-limiting staleness), never reuse its number, and update the rule row that pointed at it.
4. **Index the rationale.** Per [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md), index non-obvious modelling rationale (why a term was scoped this way, why a status is `undecided`) to `kk:arch-decisions`. Skip anything self-evident from the kit pages themselves.
