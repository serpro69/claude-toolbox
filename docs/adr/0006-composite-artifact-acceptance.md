# ADR 0006: Composite-Artifact Acceptance for Domain-Reference Kits

## Status

Accepted (2026-09-03)

## Context

`/kk:review-architecture` (Milestone 1) was designed around a strict
single-artifact input contract: the user passes exactly one committed
artifact path; two explicit paths are rejected. The rule keeps acceptance
deterministic and the review scope inspectable.

`/kk:model` (Milestone 2) produces a domain-reference kit that is
authored as **one unit split across two pages**: a glossary page
(`<context>.md`) and a divergences/traps page (`<context>-traps.md`),
with hard cross-references between them (the glossary's rules table
cites `P#`/`D#` entries in the traps page). Reviewing one page alone
severs claims from their cited divergences, making several claim classes
ungradeable.

Options considered:

- Keep the single-artifact rule literal and review kit pages
  independently — severs cross-references; the reviewer would grade
  half a contract.
- Accept two explicit paths for kits — breaks the one-path CLI shape,
  reopens the "which artifacts may be combined?" question M1
  deliberately closed, and invites arbitrary artifact bundling.
- Accept the pair as **one composite artifact resolved from a single
  path** — preserves the CLI shape and bounds the amendment to a
  single, structurally-defined artifact type.

## Decision

The glossary + traps page pair is accepted as **one composite
artifact** — a deliberate, bounded amendment to the single-artifact
rule, applying only to domain-reference kits.

Invocation mechanics:

- The user passes **either page's path** (one path, CLI shape
  preserved). The reviewer resolves the counterpart by the sibling
  naming convention (`<context>.md` ↔ `<context>-traps.md` in the same
  directory), falling back to the pages' explicit cross-links for
  brownfield kits that don't follow the convention. The fallback is a
  bounded pattern-match lookup, not prose reading — shape, not claims.
- Two explicit paths remain rejected; the rejection message names the
  kit clause (pass one page — the counterpart is auto-discovered).
- A single-page kit is accepted solo with a loud report note that
  cross-page references are unresolvable; an enforcement pointer citing
  an entry in the missing counterpart is graded `ill-formed`, never
  silently skipped.

## Consequences

- `/kk:model`'s two-page output contract is reviewable as authored;
  the produce→review freshness loop (re-verification at consumption
  time) works without manual artifact stitching.
- The single-artifact rule survives for every other artifact type;
  future producers wanting multi-file artifacts must justify their own
  bounded amendment here rather than inheriting this one.
- Sibling naming becomes load-bearing: renaming one kit page without
  the other silently degrades review to solo-page mode (with the loud
  note as the safety net).
- Operative mechanics live in
  `klaude-plugin/skills/review-architecture/input-contract.md`
  (§The composite-kit amendment); design rationale in
  `docs/wip/architect-skills/model/design.md` §6.2 (frozen into
  `docs/done/` on completion).
