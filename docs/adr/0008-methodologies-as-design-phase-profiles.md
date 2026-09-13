# ADR 0008 — Cross-cutting methodologies are adopted as design-phase profiles

- **Status:** Accepted
- **Date:** 2026-09-13
- **Originated in:** [docs/feat/wip/twelve-factor-skills/design.md](https://github.com/serpro69/claude-toolbox/blob/master/docs/feat/wip/twelve-factor-skills/design.md)
- **Related:** [ADR 0001](0001-profile-detection-model.md), [ADR 0002](0002-profile-content-organization.md)

## Context

The 12-factor methodology ([12factor.net](https://12factor.net/)) was proposed for
adoption into the `kk` skills (issue #101). 12-factor is representative of a broader
class of inputs: **cross-cutting methodologies** — bodies of principles that apply
across a codebase (12-factor, and future candidates such as domain-driven design,
security frameworks, accessibility standards). They share three properties that
distinguish them from the domains profiles were built for (programming languages,
IaC DSLs, config schemas):

1. **No reliable file-detection signal.** A language profile activates on file
   extension; an IaC profile on filename/content anchors. A methodology has no
   `*.twelvefactor` file — it is a lens over decisions and code, not a file type.
2. **Two distinct enforcement altitudes.** Some concerns are architectural
   decisions best raised *before code exists* (config strategy, backing services,
   statelessness, disposability). Others are code-level checks that only make sense
   for a subset of files (a deployable service, not a library) and therefore need a
   gating mechanism that does not yet exist.
3. **Passive-context risk.** Loading a whole methodology into every relevant phase
   inflates context on runs where it does not apply.

The profile system ([ADR 0001](0001-profile-detection-model.md),
[ADR 0002](0002-profile-content-organization.md)) already provides per-phase content
loading, a confirm-gated design-phase detection path (`## Design signals` matched
against idea prose), and per-phase population "as needed." The question was how to
fit a methodology into these primitives without a new mechanism and without bloat.

Alternatives considered:

- **Monolithic multi-phase profile** with fuzzy file detection — inflates context
  and misfires, since methodologies have no dependable file signal.
- **Dedicated opt-in review skill** (e.g. `/kk:review-12factor`) — zero passive
  cost, but a compliance gate that lives outside the design→implement→review flow
  rather than shaping decisions where they are cheapest to change.
- **Baking the lens into `/kk:design`'s generic reference files** — always-on
  constant cost and untargeted.

## Decision

Cross-cutting methodologies are adopted as **confirm-gated design-phase profiles**:

- The profile's `DETECTION.md` carries the three mandatory signal headings
  (`## Path signals`, `## Filename signals`, `## Content signals`) left **empty**,
  plus a populated `## Design signals` block with **narrow** tokens. Empty file
  signals guarantee the profile never activates in file-based phases
  (`review-code`, `implement`, `test`, `document`, `review-spec`); the narrow token
  set (excluding generic words like `config`/`service`/`deployment`) keeps
  design-phase activation from misfiring, deferring ambiguous infra ideas to the
  shared detection fallback prompt.
- The profile populates only `design/` (`index.md`, `questions.md`, `sections.md`),
  feeding the `/kk:design` refinement-question pool and required design-doc
  sections. It participates through the existing detection machinery — no
  `/kk:design` skill files change.
- **Code-level enforcement is a separate, later concern.** Distributing method
  checks into language/IaC profiles for the implement/review phases requires a
  *deployability gate* (a check applies to a deployable service, not a library or
  CLI) that does not exist today. That work is explicitly out of scope of the
  design-phase adoption and is taken on only after the gating design is settled.

The first application is the `twelve-factor` profile (classic 12 factors); the
code-level distribution (approach "B") is deferred with its open gate question
recorded in the originating design doc.

## Consequences

- **Passive context cost is bounded and metadata-only** (not literal zero). No
  activation-gated content (questions, required sections) loads unless an idea
  matches the narrow tokens and the user confirms activation. The one
  unconditional cost is reading the compact `DETECTION.md` metadata during
  design-phase token collection — the same per-run cost every registered profile
  already incurs, since the detection algorithm reads every known profile's
  `DETECTION.md` to build the token union. Keeping `DETECTION.md` compact keeps
  this negligible. This preserves the intent of issue #101 (adopt without
  inflating context) without overstating the guarantee.
- **The methodology shapes decisions upstream**, where they are cheapest to change,
  rather than only flagging violations after code is written.
- **Enforcement is not automatic.** A design-phase-only adoption raises the
  concerns but does not verify the resulting code complies. Closing that gap
  depends on the deferred deployability-gate work; until then, compliance rests on
  the design conversation and human review.
- **A reusable archetype is established:** the "design-only profile" (empty file
  signals + `## Design signals` only). This is a consequence of already-documented
  profile conventions rather than a new mechanism; it is noted in `AGENTS.md`
  §Profile Conventions so future methodology adoptions follow the same shape.
- **Token tuning is the recurring maintenance cost.** Each methodology profile's
  token set trades recall (real ideas caught directly) against precision (no
  false-positive prompts); the fallback prompt is the safety net for under-broad
  tokens.
