---
name: review-architecture
description: |
  Review a written architecture artifact — an ADR (docs/adr/), a broader architecture doc, or the architecture section of a design doc — against the system it claims to describe. Verifies the EXISTENCE and TOPOLOGY of declared mechanisms (structural boundaries, data ownership, NFR mechanisms, failure isolation, state consistency, evolution/versioning) plus decision soundness and reversibility. Use after an ADR or architecture doc is written, before or during implementation. NOT for behavioral/runtime correctness (that is $kk:review-code and $kk:review-spec). Security architecture is out of scope — delegate threat modeling to the PAL secaudit tool (mcp__pal__secaudit).
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Architecture Review

## Overview

Review a single committed architecture artifact against the system it describes. The review is **claim-driven**: the artifact is normalized into an explicit, inspectable claim-set (Pass 0), each claim is verified for the existence and topology of the mechanism it names (Pass 1), and the artifact's decisions are graded against its own stated context (Pass 2). Verification is delegated to the read-only `architecture-reviewer` agent; this skill owns acceptance and presentation.

**The altitude line — the load-bearing constraint.** This skill verifies that declared mechanisms *exist* and are wired into the right *topology* — "is there an idempotency-key column / a circuit breaker targeting dependency D / a `/v2/` route." It never verifies behavioral correctness ("does the code *use* the key correctly under retries") — that belongs to `$kk:review-code` and `$kk:review-spec`. Every dimension, the input contract, and the eval strategy are consequences of this line. Do not let a dimension expand into whole-system behavioral reasoning.

**Security architecture is delegated OUT** to the PAL `secaudit` tool (`mcp__pal__secaudit`). There is no `kk:` security skill. Trust boundaries, authN/authZ enforcement, and data-classification flow drag the reviewer into runtime analysis — surface such claims under Not Reviewed with a `secaudit` pointer (see [output-contract.md](output-contract.md)).

## Conventions

Profiles are **not** consulted in M1 — evidence-gathering mechanics ship as inline examples in the pass procedures. Profile detection and an `architecture/` profile phase are deferred (see the review design §8).

## Required Outputs

Before declaring the review complete, verify all outputs are delivered:

- [ ] Claim Set (the Pass 0 output) presented verbatim as the inspectable intermediate artifact
- [ ] Per-claim verdicts by dimension, a Not Reviewed section, and Pass 2 findings — all per [output-contract.md](output-contract.md)
- [ ] Next steps confirmation from user

## Workflow

### Mandatory ordering — instructions before artifact

The workflow below is strictly sequential. **Do not read the artifact's content, extract claims, or form any verdict until you have loaded every instruction file: this SKILL.md, [input-contract.md](input-contract.md), and [output-contract.md](output-contract.md).** Your only early contact with the input is the artifact *path(s)* passed on invocation — enough to apply the acceptance contract, not enough to pattern-match claims. The pass procedures (`pass0-extraction.md`, `pass1-topology.md`, `pass2-soundness.md`) are the delegated agent's to load; the agent restates the same instruction-before-action rule on its own side.

This ordering is load-bearing (ADR 0004), not stylistic: with the artifact text in context before the contracts are loaded, the model has enough to emit plausible claims and verdicts and will optimize away the methodology.

**Phases:**

1. **Acceptance** — apply [input-contract.md](input-contract.md) to the invocation path(s): exactly one committed written artifact per invocation; diagrams count only with accompanying prose; verbal/diagram-only or multi-artifact inputs are rejected with an actionable message. No path given → list candidate artifacts (`docs/adr/`, `docs/wip/*/design.md`) and ask. This is the only phase the main agent performs against the input directly, and it reads the artifact's *shape*, not its claims.

2. **Delegate to `architecture-reviewer`** — spawn the read-only `architecture-reviewer` agent (via the Agent tool) to run Pass 0 → Pass 1 → Pass 2. The agent has no shell, so resolve the plugin root yourself first (`echo "${TOOLBOX_PLUGIN_ROOT:-NOT_SET}"`) and inject the absolute path under a `## Plugin Root` heading. Pass the agent:
   - the accepted artifact path (and, for a design doc, the scoping heading);
   - the procedure files to read, by plugin-root path: `../../skills/review-architecture/pass0-extraction.md`, `../../skills/review-architecture/pass1-topology.md`, `../../skills/review-architecture/pass2-soundness.md`, and `../../skills/review-architecture/output-contract.md`;
   - the resolved `## Plugin Root` absolute path.

3. **Present** — relay the agent's report **verbatim** per [output-contract.md](output-contract.md) — do not summarize, compress, or re-narrate it: the full Claim Set table, per-dimension verdicts, the Not Reviewed section (`delegated`/`unrouted` claims), and Pass 2 findings, with the verdict→severity mapping applied. A summarized relay destroys the inspectable intermediate artifact the Claim Set exists to be (the read-only agent has no other home for it). Then confirm next steps with the user.

## Invocation

```
$kk:review-architecture <artifact-path>
```

Exactly one artifact per invocation. For a design doc, an optional heading argument scopes the review to its architecture section. See [output-contract.md](output-contract.md) for full invocation/scope rules.
