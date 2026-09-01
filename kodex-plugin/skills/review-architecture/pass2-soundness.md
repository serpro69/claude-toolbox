# Pass 2 — Decision Soundness & Reversibility

Grades the artifact's **reasoning** against the artifact's **own stated context**. Unlike Pass 1, this pass has **no reality branch** — it never resolves an anchor, greps the repo, or opens a source file. It runs in **internal-soundness mode only**, on the whole-artifact context Pass 1's per-claim map-reduce cannot see. Two checks: **appropriateness** (is each chosen mechanism a fit for the constraints the document itself states?) and **reversibility** (are one-way vs two-way doors identified, and do irreversible decisions carry proportional justification?).

## Why this is a separate pass, not a seventh dimension

Pass 1 is a strict `extract → locate bounded evidence → grade` loop. Pass 2 has no greppable evidence: "is a write-through cache appropriate for a write-heavy workload" is a judgment about the artifact's reasoning, not a mechanism you can Grep for. Forcing it into Pass 1's schema wrecks the check — the model starts hunting a repo path for a philosophical trade-off and hallucinates to fill the gap. Keeping it separate also keeps the eval seams clean: **Pass 1 evals test extraction + topology verification; Pass 2 evals test judgment.**

## The stated-context rule (load-bearing)

**Grade only against the constraints the artifact itself states.** The yardstick is the document's own Context / Status / stated NFRs / workload characterization — never outside knowledge of what the real workload is, and never the repo. True appropriateness (is the system *actually* write-heavy in production) needs live profiling the reviewer cannot do; scoping to *stated* context is what keeps this pass gradeable instead of an open-ended "I'd have chosen differently" critique.

**This rule governs Check A (appropriateness); Check B (reversibility) is scoped differently.** Classifying a decision as a one-way vs two-way door draws on general knowledge of the *mechanism's* reversal cost (resharding a live store is expensive; adding a replica is not) — an artifact rarely states its own reversal cost, so requiring a quoted constraint there would suppress every reversibility finding. What Check B grades against the artifact's own words is only whether an irreversible decision carries *proportional justification*. So: appropriateness needs a quotable stated constraint; reversibility needs a door classification (general mechanism knowledge) **plus** a justification check (artifact words).

The consequence cuts both ways:

- **No finding without a quotable constraint.** An appropriateness finding must quote the stated constraint it violates **and** the mechanism it clashes with. If the artifact states no constraint the mechanism contradicts, there is no finding — you may not manufacture the yardstick.
- **A well-formed claim can still be inappropriate.** Pass 1 internal-soundness checks *well-formedness* (does the claim name a mechanism and a quantified target); Pass 2 checks *fit* (is that mechanism right for the stated context). A claim can be `internally-sound` in Pass 1 and still flagged here — the two passes grade different things, on purpose.

## Inputs

Pass 2 reads more of the claim-set than Pass 1's per-claim loop does:

- **Every decision-bearing claim**, whatever dimension it routed to — the *mechanism* each dimension-1–6 claim names is a decision, and its appropriateness is Pass 2's business. Pass 2 is not limited to `pass2`-routed claims.
- **The `pass2`-routed claims** ([pass0-extraction.md](pass0-extraction.md)) — claims that are *purely* rationale / trade-off / reversibility with no topological mechanism of their own.
- **The artifact's stated context** — the Context section, the Status (tense default), the stated NFRs and workload characterization. This is the yardstick both checks measure against.

## Check A — Appropriateness

For each chosen mechanism, ask: *given the constraints the document itself states, is this mechanism a fit?*

A finding requires an explicit, quotable clash between a **stated constraint** and the **known character of the mechanism**:

- The document characterizes the workload one way but the mechanism optimizes for the opposite (a read-optimizing cache taxing a write-heavy path; a strongly-consistent store where the doc states it needs partition-tolerant availability).
- The document states a hard constraint the mechanism structurally cannot honor (a write-behind cache that acknowledges before durable persistence, under a stated "acknowledged writes must never be lost").

The clash must be derivable from the artifact's own words. If honoring the constraint would need a mechanism the doc does not have (e.g. the stated constraint needs stale-read mitigation and none is specified), name the *missing* element — that is still a stated-context finding.

**Severity: P1.** Report the finding, the quoted stated constraint, and the quoted mechanism.

> **Inline example.** Context states "the ingest path must stay available for writes even when one region is unreachable." Decision states "commit every write synchronously across all three regional replicas via two-phase commit before acknowledging." Two-phase commit is a strong-consistency mechanism that blocks — and fails the write — the moment any participant is unreachable, so it sacrifices exactly the write-availability-under-partition the artifact says it must keep (a CP mechanism where the stated need is AP). Stated-context clash → **inappropriate mechanism, P1**. Grade what the artifact says it needs, not what you imagine the real partition rate to be.

## Check B — Reversibility

For each decision-bearing claim, classify the **door** and check the **justification is proportional to the cost of reversing it**:

- **One-way door** — irreversible, or expensive/disruptive to reverse (a shard-key choice on a live datastore, a public API contract, a data-format commitment, a vendor lock-in). Requires **proportional justification**: the harder to reverse, the more the artifact must show for it — the forces weighed, the alternatives considered, the scale/analysis behind the specific choice.
- **Two-way door** — cheap to reverse (a tunable limit, an added-then-removable replica, an internal implementation detail). Needs little justification; a bare mention is fine.

Findings:

- An irreversible decision the artifact makes **without acknowledging its irreversibility**, or **without proportional justification** → **finding, P2**.
- A decision the artifact **explicitly identifies as a one-way door and justifies commensurately** → **sound, no finding.** Reward the artifact for naming the door.
- Two-way doors are not findings.

> **Inline example.** Decision states "expose the public mobile API over gRPC." Committing an unmanaged external client population to a wire protocol is a one-way door — migrating millions of already-installed apps off it later is slow and disruptive. If the ADR neither acknowledges the irreversibility nor justifies gRPC specifically (no payload/latency analysis, no alternatives weighed) → **reversibility finding, P2**. Had it said "this is a one-way door; gRPC cuts payload 40% at our scale and forced-update lets us control client rollout," that is proportional justification → no finding.

## Coupling to Pass 1 — the P1→P0 escalation

Reversibility is where a Pass 1 `violated` verdict can escalate. When a claim graded `violated` in Pass 1 rests on a decision Pass 2 classifies as a **one-way door**, the violation's severity escalates **P1 → P0** (per [output-contract.md](output-contract.md)): shipping the wrong irreversible mechanism is materially worse than shipping the wrong reversible one. Flag the escalation explicitly, naming both the Pass 1 claim and the door classification.

**Which decision a violated claim "rests on."** The governing decision is the one the claimed mechanism exists to enforce, contain, or implement — never the enforcement convention itself. Trace the violated claim to the artifact decision it protects, and classify *that* decision's door. This matters most for containment and isolation claims: repairing the guard is almost always cheap (an import to reroute, a convention to re-apply), so classifying the guard's own repair cost makes every containment violation look like a two-way door and the escalation never fires — an inversion of the rule. A breached guard around a one-way door is exactly the P0 case: the violation is silently widening a commitment the artifact itself says cannot be walked back, and the cheapness of the repair is an argument for fixing it now, not for downgrading it.

## Self-check before emitting a Pass 2 finding

- **Appropriateness:** can you quote the stated constraint *and* the mechanism? If you cannot quote the constraint from the artifact, drop the finding — you are importing an outside assumption, not grading stated context.
- **Reversibility:** did you first classify the door? A two-way door is never a finding, however thin its justification. Only one-way doors demand proportional justification.
- **Escalation coupling:** for each Pass 1 `violated` verdict, did you trace the claim to the decision its mechanism protects — not the enforcement convention — and check that decision's door classification before settling the severity?
- **Coverage:** does every `pass2`-routed claim from the claim-set appear somewhere in your output? A `pass2` claim Pass 1 skipped by design and Pass 2 never mentions has silently fallen through both passes.
- **Altitude:** did you open a source file or resolve a repo path? If so you have left Pass 2 — this pass grades the artifact's reasoning against its own words, nothing else.

## Output

Feed the results into the report's **Pass 2 — Decision Soundness & Reversibility** section ([output-contract.md](output-contract.md)):

- **Appropriateness** — mechanism-vs-stated-context findings (each with the quoted constraint + mechanism, P1), or "no mismatch found."
- **Reversibility** — for each decision-bearing claim, its **door classification** (one-way / two-way) — record findings *and* sound doors alike, so a justified one-way door leaves an auditable trace. Then the findings (irreversible decisions lacking proportional justification, P2) and any P1→P0 escalation of a Pass 1 `violated` verdict whose decision this pass classified a one-way door. Use "n/a" only when the artifact makes no decisions to classify.

**Account for every `pass2`-routed claim explicitly.** Each one appears at least once in this section — as a door classification, an appropriateness note, or an explicit "consistent with stated context — no finding." Pass 1 skips these claims by design, so a `pass2` claim this section never mentions has been reviewed by nobody; fail-loud forbids that silence.

These are findings and door classifications, not per-claim topology verdicts — do not emit `verified`/`violated`/etc. here.
