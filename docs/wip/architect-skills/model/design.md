# Milestone 2 — `/kk:model` — detailed design

**Status:** Design. Part of [../design.md](../design.md) (architect-supporting skills). Milestone 2.

**Deliverable:** a `/kk:model` producer skill (information architecture — the steady-state domain-reference kit), four shared producer guards under `klaude-plugin/skills/_shared/`, and three additive extensions to `/kk:review-architecture` (M1) that close the produce→review freshness loop.

This document is self-contained: the field evidence it builds on is summarized in §1; no external artifact is required to implement it.

---

## 1. Evidence base — one field workstream, encoded as falsifiable defaults

The design derives from the first real-world architect workstream run with AI assistance (2026-08-31, an external multi-repo product project; artifacts private). That workstream produced a field-tested two-page domain-reference kit, an adversarial process review with a ranked failure catalog, and a workflow protocol in which **every rule cites the concrete failure that motivated it**.

The recorded failures this design encodes against:

- **F1 — fabricated requirements.** Four working sessions modelled a feature against an invented stakeholder brief while the two real tickets — containing the actual asks, with named stakeholders — sat unread one query away. The invented brief was materially wrong about scope and direction.
- **F2 — non-propagated correction.** A recorded fact flipped (an enforcement table turned out deleted); the correction was applied to one low-traffic page while four auto-loaded context files kept asserting the stale fact.
- **F3 — canonical by decree.** Business rules reverse-engineered from code were presented as settled business intent, and a term coined during analysis was marked canonical by its own author. Code verification establishes *code-clock* facts only; intent claims derived from code are presumptions until a human ratifies them.
- **F4 — invisible invariant.** A load-bearing hidden invariant (a single-result query at read time vs. unenforced multiplicity at write time) survived four walks of the same file — because verification kept re-confirming previously written claims instead of asking new questions. Confirmation-seeking verification finds staleness, never omissions.
- **F5 — contact-ratio drift.** The workstream reached an artifact-to-stakeholder-contact ratio of N:0 — increasingly sophisticated models stacked on unratified models, with no conversation scheduled.
- **F6 — author-violated conventions.** The showcase artifact violated its author's own declared citation convention (no line numbers).
- **F7 — self-certified trust.** Pages claimed "verified/trusted" status although no human other than the AI-assisted author had reviewed them.

**Epistemic status: n=1.** These practices are field-tested once, not field-proven. The design therefore encodes them as **explicit defaults, each citing its motivating failure** (the ADR-0004 pattern: rules that cite their failure survive; rules that don't, drift), kept cheap to revise when a second workstream falsifies one. One candidate was already falsified during this design session: a proposed "session-close state-rewrite" guard was judged a false-positive finding by the user and is deliberately absent from this design.

## 2. Positioning and success metric

`/kk:model` is the first producer of the architecture flow: it emits artifacts that `/kk:review-architecture` verifies. It runs at information-architecture altitude — *what the domain's concepts are, where they bind to code, and which questions about them only a human can close* — upstream of feature `/kk:design` and never called by it (the seam stays a one-directional artifact hand-off, per the umbrella design).

**The primary output is the decision queue, not the model.** The highest-value product of a modelling run is a queue of precise, decidable questions ("RQs"), each tagged with the **role** that can decide it (product owner, developer, stakeholder, customer). Mapping and delta work should compress to hours; surfacing the decidable questions is the value chain, and it only counts once the questions reach someone who can decide.

**Success for M2:** a `/kk:model` run ends with (a) a provenance-clean kit and (b) a decision queue whose entries are decidable by their tagged roles — and the produced artifacts are usable as discussion instruments per audience: definitions carry the business conversation with product roles; bindings carry the technical conversation with developers. Artifact count and model sophistication are explicitly not the metric (F5).

## 3. Output contract — the steady-state kit

Per bounded context, `/kk:model` produces **exactly two durable pages**:

1. **Glossary page** (`<context>.md`) —
   - Summary + one **conceptual-altitude** diagram (entities, relationships, only load-bearing attributes — shape, not a field dump; text-based, e.g. Mermaid).
   - Business rules folded in as a compact numbered table (`L1…Ln`), headed by a provenance banner: reverse-engineered rules are **presumptions of intent, `proposed` until ratified**.
   - Per-term entries with dual-audience fields: **Definition** (for product; business clock) / **Bindings** (for engineering; code clock — directory, collection/constant, field, symbol) / **Status** / **Aliases** / **Not to be confused with** / **Notes**.
   - Status markers: `canonical` / `proposed` / `undecided` / `deprecated-alias` / `overloaded`.
   - **Derived-from footer** listing every source path a recorded domain fact derives from (a file read that contributed no fact — e.g. a bare `go.mod` — is not required), so any binding can be re-checked at its source.
   - Term count: **typically 10–20 for a first greenfield slice — a guideline, not a requirement**; the forcing question, the mode (greenfield vs brownfield), and feature scope set the actual count.
   - **Ticket-note retirement discipline:** any note citing a ticket states what retires it, or the durable page rots as tickets ship.
   - **No line numbers in citations** (lines rot before they're read; cite file or symbol).
2. **Divergences & traps page** (`<context>-traps.md`) —
   - Only facts **no single file reveals**: where code diverges from the stated rules (`D#`), and cross-file hazards (`P#`). Numbering is stable; retired numbers are not reused.
   - **Never a schema mirror** — the code is the schema reference; a mirrored schema is wrong by default.
   - **Self-limiting staleness:** each entry dies exactly when its divergence is fixed — delete it in that PR.

Plus, **once per home** (not per context): a conventions index (`index.md`) declaring the entry fields, status markers, the two-clock rule, citation rules, and the freshness model — so every kit page in that home reads under the same contract. The **home** is the durable-docs root the kit pages live in (e.g. `docs/architecture/`, or a knowledge repo's domain-reference directory) — kits sit in it as context-named files, so one `index.md` serves every context in that home.

**Everything else is disposable.** Scoped diagrams, delta models, ERDs, standing logical/physical model pages are *not produced*; they are drawn per-feature inside design docs. If asked to produce one as a durable artifact, the skill **pushes back and names the maintenance cost** before complying (kit-scope pushback; the rejected four-layer alternative in §Rejected Alternatives).

**Freshness banner.** Every produced page states: (a) it is `proposed` until a human other than the author reviews it (F7 — no self-certification), and (b) staleness is checked by **re-running `/kk:review-architecture` against the page's Derived-from anchors at consumption time** — the freshness mechanism is a skill run, not a reviewer social contract (see §6).

**Artifact homes** (resolves the umbrella §6 question for `model`): the skill is **home-agnostic**, with resolution precedence:

1. Brownfield — wherever the existing kit already lives.
2. A user-declared home — covers cross-repo domains kept in a dedicated knowledge repo.
3. Otherwise propose `docs/architecture/` as the single-repo default home — kit pages as `<context>.md` / `<context>-traps.md` directly in it — and confirm with the user.

The cross-repo-domain question is thereby answered as a deployment detail: the org picks the home; the skill asks, never assumes.

## 4. Workflow — seven phases, strictly sequential

ADR-0004 ordering applies: SKILL.md, the process file, the archaeology reading-method reference, all four shared guards, the shared capy knowledge protocol, and the kit-conventions reference are fully loaded before any subject-matter action. Minimal early scope (a directory listing, a keyword scan of the request) is permitted only to drive mode detection.

1. **Scope intake.** Establish the bounded context, the **forcing question** (the feature/ticket that bounds what is worth modelling — model in service of the decision, never boil the ocean), and the **mode**:
   - **Greenfield** — no kit exists for this context; produce the initial two pages (+ conventions index if the home has none).
   - **Brownfield** — an existing kit is found or pointed at. Read it in full first; it becomes the baseline and all changes are deltas. Existing status markers are **never flipped unilaterally** — `proposed → canonical` requires a recorded human decision (the recording mechanism is `decide`'s scope, M2.1).

   Intake also runs the capy knowledge-base search per the shared protocol (`kk:arch-decisions`, `kk:project-conventions`) for prior modelling decisions and conventions in the area.
2. **Requirements-harvesting gate** *(shared guard; F1)*. Read every linked ticket plus one hop of references; quote the actual asks into the working notes **before any modelling**. Fabricated input only as a labeled last resort when no real input exists, stating what real input would replace it.
3. **Archaeology.** Read the code in the order **state → time → invariants**: which states/transitions are actually enforced (vs declared); where time enters the lifecycle; what the system silently assumes and which assumptions the forcing question stresses. Two-clock discipline throughout: code-clock facts are verifiable; intent derived from code stays `proposed` (F3).
4. **Draft the kit** per §3.
5. **Verify.** At least one confirm-pass over drafted claims **plus at least one open-question pass** *(shared guard; F4)* — re-walk the source asking new questions (cardinalities, single-result lookups, unchecked writes, silent defaults), not re-confirming written claims.
6. **Self-check** *(F6)*. Conventions-bind-author lint: check the produced pages against the kit's own declared conventions (status markers present and justified, no line numbers, Derived-from complete, one diagram, traps page not a schema mirror, ticket notes carry retirement conditions).
7. **Surface & close.** Present the **decision queue**: each RQ precise, decidable, tagged with its role decider. Apply the **contact-ratio guard** *(shared guard; F5)*: if the ratio of artifacts produced to stakeholder inputs consumed reaches N:0, state that the next unit of progress is a conversation, naming the role (and person/ticket if known). In brownfield mode, any contradicted recorded fact triggers **fact-flip propagation** *(shared guard; F2)*: search the whole workspace for assertions of the old fact and fix every occurrence in the same session. The queue is presented inline and appended to the active feature's `docs/wip/<feature>/design.md` under an **Open Questions** heading when the feature directory exists (inline-only otherwise). Close by indexing non-obvious modelling rationale to `kk:arch-decisions` per the capy protocol — skip what is self-evident from the kit pages.

## 5. Shared producer guards

Four files in `klaude-plugin/skills/_shared/` (bare basenames), consumed by `/kk:model` via per-skill `shared-` symlinks and designed for reuse by `decide` (M2.1) and later producers. Each file opens by citing the failure it prevents:

| File | Rule | Failure |
| --- | --- | --- |
| `requirements-harvesting.md` | Read every linked ticket + one hop; quote the asks before modelling; labeled fabrication only as last resort | F1 |
| `open-question-pass.md` | Verification alternates confirm-passes with new-question passes; ships the question checklist | F4 |
| `fact-flip-propagation.md` | On a contradicted recorded fact, search the whole workspace and fix every assertion in-session | F2 |
| `contact-ratio-guard.md` | Track artifact-to-stakeholder-contact ratio; at N:0 declare a conversation the next unit of progress, naming the role | F5 |

Single-consumer content stays inside `/kk:model` (not `_shared/`) until a second producer needs it: kit-scope pushback, the conventions-bind-author self-check, and the state→time→invariants reading method.

`/kk:model` also consumes the **existing** shared capy knowledge protocol (`_shared/capy-knowledge-protocol.md`) via the standard symlink — searched at intake, indexed at close (§4) — like every other kk skill that reads or writes durable decisions.

The register split is deliberate: workflow **mechanics** live as skill steps (portable, eval-able, loaded only when relevant); mentor **tone/register** stays project-local CLAUDE.md prose. The toolbox ships no mentor-mode skill.

## 6. M1 additive extensions — closing the freshness loop

**Frozen vs additive.** M1's architecture is frozen: the altitude line (topology, never behavior), the three-pass shape, the anchor rule, the six existing dimensions, and the severity model do not change. One Pass 2 **clarification** rides along (surfaced by the clean-kit regression eval in Task 7): Check A grades decisions the artifact *makes or proposes* — a descriptive artifact's honestly documented divergence (an enforcement pointer citing a traps entry that carries its retirement condition) is never re-derived as an appropriateness clash. This sharpens Check A's existing intent for decision-bearing artifacts rather than narrowing it; the no-regression claim is verified by re-running M1 eval 7 (`pass2-inappropriate-mechanism`) after the change (Task 8). The three extensions below are additive and exist because `/kk:model`'s output contract requires them — without them the reviewer cannot verify the kit, and the kit's freshness model collapses back into the social contract that failed in the field (near-zero adoption probability for cross-repo reviewer obligations).

1. **`provenance` on the Pass 0 claim schema.** New field, orthogonal to `tense`: `harvested` (from a cited stakeholder/product source) / `reverse-engineered` (derived from code) / `fabricated-labeled` (explicitly marked invented input). Pass 0 stays repo-blind — provenance is derivable from the artifact's own text (status markers, provenance banners, source citations). Payoff: the **self-certification check** — a claim presented as `canonical`/ratified whose provenance is reverse-engineered with no cited ratification record is a mechanically detectable finding (F3/F7); a `fabricated-labeled` claim presented as settled is the same P2 (invented input can no more self-ratify than reverse-engineered intent). **Division of labor:** Pass 0 only *records* provenance per claim (extraction stays single-purpose — each M1 pass does one job); the check **executes in Pass 2** as its third check, provenance consistency, alongside appropriateness and reversibility — Pass 2 is already internal-soundness-only and whole-artifact, and no repo access is needed. **Report home:** a **Provenance** subsection under the report's Pass 2 findings section; the severity-mapping table gains a row — self-certification (`canonical` by decree) → P2. Its original deferral condition — "revisit when M1's evals are green" — has been met.
2. **Input contract: domain-reference artifacts accepted.** The glossary + traps pair is accepted as **one composite artifact** — a deliberate, bounded amendment to M1's single-artifact rule, justified because the pair is authored as one unit with hard cross-references (rules table → `P#`/`D#` entries); reviewing one page alone would sever claims from their cited divergences. **Invocation mechanics:** the user passes **either page's path** — one path, preserving the existing CLI shape; the reviewer resolves the counterpart by the sibling naming convention (`<context>.md` ↔ `<context>-traps.md` in the same directory), falling back to the pages' explicit cross-links for brownfield kits that don't follow the convention. Two explicit paths remain rejected; the single-artifact rejection message gains a kit clause (pass one page — the counterpart is auto-discovered). **A single-page kit is accepted solo**, with a loud report note that cross-page references are unresolvable; a rules-table enforcement pointer citing an entry in the missing counterpart is graded `ill-formed` (its required supporting element is absent), never silently skipped. The two kit evals' prompts must mirror this one-path invocation. All other acceptance rules (committed text, falsifiable claims) unchanged.
3. **Dimension 7 — Domain Binding.** Claim class: "concept X is bound to code element Y (directory / collection constant / field / symbol)." **The Pass 0 routing set rides along** — without it the extension is inert (binding claims would honor Pass 0's "do not force-fit" rule and land `unrouted` → Not Reviewed): the `dimension` token enum in `pass0-extraction.md` extends to `7`, §Dimension routing gains a Domain Binding row (route here when the claim asserts where a domain concept lives in code), and the artifact-type mining table gains a **domain-reference kit** row (per-term Bindings → dimension 7; rules-table enforcement pointers → dimension 7; rule *intent* → provenance-labeled, not truth-verified; status markers → tense/provenance signals). Evidence: the named element exists at the cited location — pure existence-and-topology, Grep/Glob-able. The altitude line holds: whether the code's *behavior* matches the definition is `/kk:review-code` / `/kk:review-spec` territory. The anchor rule applies unchanged, in M1's verdict vocabulary: `Bindings: none yet` is `internally-sound` (`future`); a `future` binding claim naming no code-element kind at all (e.g. "will be represented in code", with neither element kind nor location class) is `ill-formed` — dimension 7 defines both fallback outcomes, like every M1 dimension; a binding citing a nonexistent file is `dangling-anchor`; a missing symbol inside an existing anchor is `violated`. Business-rule intent claims (the `L#` table) are **not** truth-verified — their *enforcement pointers* are dimension-7 binding claims; their intent-truth is exactly what provenance labels defer to humans.

**Surface updates ride along.** The M1 skill's user-facing wording repeats what the extensions change and is part of the edit scope: `review-architecture/SKILL.md` (frontmatter description — add the domain-reference-kit artifact type and glossary/domain-kit trigger keywords, extend the dimension enumeration, re-check the ≤1024 budget; Phase 1 acceptance text and the Invocation section — composite-kit wording) and `agents/architecture-reviewer.md` (the description's artifact-type enumeration; the "path to the single accepted artifact" payload line).

Each extension ships with its own eval (§7), same bar as every M1 task.

**Inherited loose end folded in:** M1's post-completion eval-8 fixes (escalation coupling, verbatim relay) are recorded as deliberately unverified; the M1-extension work touches the same files, so the eval-8 re-run happens there (see tasks).

## 7. Eval strategy

Evals live at `klaude-plugin/skills/model/evals/<name>/` and `klaude-plugin/skills/review-architecture/evals/<name>/` per the toolbox convention (one directory per eval; real fixtures; grader-only `oracle/` siblings). Producer evals are new ground — all existing evals grade reviewers — so each eval grades exactly one workflow seam:

**`/kk:model` evals:**

- `requirements-gate` — fixture with ticket files present; trap: modelling straight from code or inventing a brief. Asserts the asks are quoted before any model content appears (F1).
- `kit-format` — small code slice in; asserts the structural conventions: all intent claims `proposed`, no line numbers, Derived-from footer present and complete, exactly one diagram, traps page contains no schema mirror (F3/F6). Mechanically gradeable.
- `hidden-invariant` — the code slice hides a single-result-lookup-class trap no single file reveals; asserts the open-question pass surfaces it (F4).
- `brownfield-update` — existing kit + code that has drifted; asserts delta update, fact-flip propagation fires across all seeded stale assertions, and no unilateral `proposed → canonical` flip (F2/F3).
- `scope-pushback` (regression) — prompt asks for a full ERD/schema mirror as a durable artifact; asserts the skill pushes back naming the maintenance cost instead of complying.

**M1-extension evals (under `review-architecture/evals/`):**

- `pass0-provenance` / self-certification — a canonical-by-decree artifact (ratified-status claims, reverse-engineered provenance, no ratification source); asserts the P2 finding fires (in the report's Pass 2 Provenance subsection), and does not fire for a properly `proposed`-labeled twin claim. Assertions split the seams: provenance field assignment (Pass 0) vs. the finding (Pass 2), mirroring M1's artifact-seeded eval convention.
- `pass1-domain-binding` — an anonymized two-page kit (adapted from the field workstream's, re-skinned to a fictional domain) + code slice with pre-verified violations; prompt passes one page's path (composite counterpart auto-discovered); asserts extraction routes binding claims to dimension 7 (none `unrouted`) and verdicts discriminate `verified` / `violated` / `dangling-anchor` / `internally-sound` (`future` — `Bindings: none yet`), with an `ill-formed` future binding (no code-element kind named) as the fallback-arm negative control.
- `regression-clean-kit` — a sound kit matching its code slice; asserts zero findings (the composite acceptance + dimension 7 do not over-fire).

Fixtures must be checked against procedure inline examples for instruction contamination — including counterfactual branches (established M1 lesson, indexed in `kk:review-findings`).

## 8. Open questions (deferred, documented)

- **Ratification record home** — glossary-entry metadata (`ratified-by`/`date`) vs. ADRs stretched to domain semantics. Blocks `decide`; deferred to M2.1. `/kk:model` sidesteps it by never flipping statuses.
- **Guard adoption by `/kk:design`** — the requirements-harvesting gate is a natural fit; out of scope per the M2 constraint that `/kk:design` stays untouched.
- **Profile enrichment for archaeology** — deferred with the M4 profile question; archaeology is language-agnostic in M2.

## Assumptions

- The two-page steady-state kit generalizes beyond the originating workstream — falsified if workstream #2 needs a third standing page (or fewer).
- Binding claims are verifiable via **additive** M1 extension only — falsified if binding verification turns out to require behavioral analysis, which would break the altitude line.
- The field kit anonymizes into eval fixtures without losing its trap structure (hidden invariant, type-union gap, ad-hoc enforcement).
- Rules encoded as workflow steps citing their motivating failure stay cheap to revise when a second workstream falsifies one (the session-close guard's falsification is the first data point that this works).

## Not Doing (M2)

- `decide` producer (ADR generation, ratification records) — M2.1.
- `decompose` producer — M2.2+, pending redefinition as an on-demand, per-decision-slice diagram/decomposition producer; standing C4 artifacts contradict the disposable-diagram verdict.
- M3 hand-off mechanics — the field workstream's glossary-to-design seam prototype is the M3 reference.
- Process-review skill — stays a documented practice.
- Profile `architecture/` phase and profile detection (M4); any `/kk:design` change; freshness CI/automation; a session-close/handoff guard (falsified — see §1).

## Rejected Alternatives

- **All three producers in one milestone** — over-builds on n=1 evidence; `decompose` has zero field evidence and triples the eval surface before any producer survives a second workstream.
- **`decide`-first slice** — cheapest review-loop closure (ADRs are already M1-reviewable), but bets the milestone on the least-evidenced producer (no ADR was produced in the field; the ratification gap was observed, not solved) while the field-tested `model` contract idles.
- **The maintained four-layer artifact stack** (glossary → logical → physical → seam) — built in the field, judged org-mismatched, dissolved same day; the physical layer is a copy of the code that is wrong by default.
- **Freshness as a maintenance social contract** (cross-repo reviewer obligations) — field-falsified: near-zero adoption probability without CI/PR-template backing; replaced by re-verification at consumption time (§6).
- **Producer as a read-only sub-agent** — producers must write files and interact with the user mid-flow (mode confirmation, decision queues); the read-only agent pattern stays reviewer-only.
- **Generic "canonical data model / data flow / lineage" contract for `model`** (the umbrella's original sketch) — replaced by the field-tested kit: bounded, conventions-bearing, and reviewable.
