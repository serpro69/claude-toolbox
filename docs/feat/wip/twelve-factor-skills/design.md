# Design: 12-Factor design-phase profile

> Issue: [serpro69/claude-toolbox#101](https://github.com/serpro69/claude-toolbox/issues/101)
> Status: design
> Created: 2026-09-13

## Problem (HMW)

How might we make the `kk` skills produce 12-factor-aligned apps — surfacing the
architectural factors at design time — **without** inflating passive context load
or firing on code where the factors don't apply (libraries, CLIs)?

The [12-factor methodology](https://12factor.net/) is a cross-cutting set of
principles for deployable services, not a language or DSL. It does not map onto
the profile system's file-pattern detection. Its highest-leverage moment in this
project's workflow is the **design phase**, where architectural decisions (config
strategy, backing services, statelessness, disposability, dev/prod parity) are
cheap to change.

## Chosen approach

Adopt the classic 12 factors (12factor.net) as a **design-only profile** consumed
by `/kk:design` through the *existing* profile-detection machinery. Approach
labels from the issue discussion:

- **E (in scope):** a new `twelve-factor` profile contributing only `design/`
  content. It activates via design-token matching (confirm-gated) and seeds the
  `/kk:design` refinement-question pool and required design-doc sections. No
  activation-gated content (questions, required sections) loads until the idea
  matches and the user confirms; the only passive cost is reading the compact
  `DETECTION.md` metadata during token collection — a bounded, metadata-only cost
  that every registered profile already incurs on each `/kk:design` run (this is
  not literal zero cost).
- **B (deferred):** distributing code-level factor checks (config-in-env,
  logs-as-streams, port-binding, statelessness) into language/k8s profiles for the
  implement/review phases. Deferred — see [§Deferred / Future Work](#deferred--future-work).

`/kk:review-architecture` is explicitly **out of scope**: it operates at a higher
altitude (existence/topology of mechanisms). 12-factor is a design-phase concern
in this project's workflow.

The general stance this feature establishes — cross-cutting methodologies are
adopted as confirm-gated design-phase profiles rather than review-phase profiles or
dedicated skills — is recorded as a cross-feature decision in
[ADR 0008](../../../adr/0008-methodologies-as-design-phase-profiles.md). The
design-only profile archetype it relies on is noted in `AGENTS.md` §Profile
Conventions.

## Why a design-only profile fits

The profile system already supports this shape:

- `DETECTION.md` requires three signal headings (`Path` / `Filename` / `Content`)
  but they may be **empty**. Empty file signals mean file-based phases
  (`review-code`, `implement`, `test`, …) never activate the profile — exactly
  right, since code-level checks are deferred to B.
- `## Design signals` (optional in the schema) drives design-phase activation via
  the `/kk:design` interaction pattern in
  `klaude-plugin/skills/_shared/profile-detection.md`.
- Phase subdirectories are populated "as needed" — `skill-md` is precedent for a
  profile that does not populate every phase. `twelve-factor` populates only
  `design/`.
- `test/test-plugin-structure.sh` per-phase assertions are presence-conditional:
  they only fire on directories that exist. A design-only profile passes.
- No `/kk:design` skill files change — detection iterates the **Known profiles**
  list and auto-loads each active profile's `design/` always-load entries.

## Structure

```
klaude-plugin/profiles/twelve-factor/
  DETECTION.md      # empty Path/Filename/Content headings + populated Design signals
  overview.md       # human/authoring reference (required by convention); NOT
                    #   loaded by the design flow — factor content the flow uses
                    #   lives in questions.md / sections.md
  design/
    index.md        # Always load: questions.md, sections.md
    questions.md    # refinement-question pool (seeds /kk:design Step 3)
    sections.md     # required design-doc sections (enforced at /kk:design Step 5)
```

### Naming

`twelve-factor` (spelled out) over `12factor` — avoids a leading-digit edge case
in tooling and matches the upstream `twelve-factor/twelve-factor` repo name.

### DETECTION.md — Design signals

```
display_name: 12-Factor App
tokens:
  - 12-factor
  - twelve-factor
  - SaaS
  - cloud-native app
  - stateless service
  - backing service
  - dev/prod parity
  - horizontally scalable
  - deployable service
```

Tokens are deliberately **narrow**. Generic words (`config`, `service`,
`deployment`) are excluded — they would cause noisy false positives. Ambiguous
infrastructure ideas that name no specific technology (e.g. "deploy to
production") are caught by the shared detection **fallback** prompt, not by broad
tokens. Detection is additive: co-activation with `k8s` on a Kubernetes-shaped
SaaS idea is expected and correct.

### design/questions.md — refinement-question pool

One question per design-relevant factor cluster. `/kk:design` asks one per
message and integrates answers into the design doc.

`questions.md` opens with the same skip-preamble the `k8s` question bank carries:
skip any question already answered by the user, the codebase, prior decisions
(`kk:arch-decisions`, `kk:project-conventions`), an existing `design.md`, **or
another active profile**. When a domain profile (e.g. `k8s`) is co-active, defer
the factors it already covers to it rather than re-asking — `k8s` already asks the
rollback trigger, the graceful-shutdown window (`terminationGracePeriodSeconds` /
`preStop` / drain), structured logs, and secrets/config; `twelve-factor` must not
re-ask these when `k8s` is present.

Coverage of the 12 factors:

- **Config (III):** Is config stored in **environment variables** (the strict
  factor-III form), not in committed config files? If a deviation is used (secret
  manager, mounted config, config service), name it and justify it. Where does
  config live per environment?
- **Backing services (IV):** Which backing services (DB, cache, queue, object
  store, SMTP) attach, and are all swappable via config with no code change
  between a local and a managed instance?
- **Build / release / run (V):** How is a release identified (immutable version),
  and how do you roll back?
- **Processes / statelessness (VI):** Is the process share-nothing? Where does
  session/user state live (never in-memory or on local disk)?
- **Concurrency (VIII):** Scale-out model — which process types (web / worker /
  cron), scaled via replicas?
- **Disposability (IX):** Fast startup and graceful shutdown on SIGTERM (drain
  in-flight work) **and** robustness against sudden death (crash-only design)? Are
  worker jobs reentrant / idempotent so they can be safely retried after an abrupt
  exit?
- **Dev / prod parity (X):** What differs between dev and prod, and why?
- **Admin processes (XII):** How are one-off tasks (migrations, scripts) run in
  the same release/env as the long-running processes?
- **Port binding (VII) / Logs (XI):** Self-contained port binding; logs as
  unbuffered event streams to stdout?
- **Codebase / dependencies (I / II):** One codebase tracked in VCS, many deploys;
  dependencies **explicitly and exactly declared** (version-pinned) **and
  isolated** (no reliance on system-wide packages)? (light — usually a given)

### design/sections.md — required design-doc sections

Grouped sections (following the `k8s/design/sections.md` style — a few grouped
sections, not 12 tiny ones), with the same rule: **omit none; if a section
genuinely does not apply, state so with a one-line justification.**

1. **Config & backing services** (III, IV) — config-source strategy; enumerated
   attached resources and their swappability.
2. **Process model & concurrency** (VI, VIII, VII) — statelessness, process
   types, replica scaling, port binding.
3. **Release & disposability** (V, IX, XII) — build/release/run separation,
   versioning/rollback, graceful shutdown/fast startup, admin/one-off handling.
4. **Parity & observability** (X, XI) — dev/prod parity gaps, logs-as-streams.

Codebase/dependencies (I/II) fold into a one-line deployment-context preamble
rather than a standalone section.

**Co-active domain profiles:** when another profile (e.g. `k8s`) is active and its
required sections already cover an overlapping concern (disposability, config,
secrets, rollout/rollback), merge rather than duplicate — cover the factor once
and cross-reference the domain profile's section, while ensuring every factor
remains visibly addressed somewhere in the document.

## Registration

The profile is inert until registered in both authoritative lists:

- `test/test-plugin-structure.sh` → append `twelve-factor` to `EXPECTED_PROFILES`
  (only after the profile files exist, or per-profile assertions fail).
- `klaude-plugin/skills/_shared/profile-detection.md` → append `twelve-factor` to
  the **Known profiles** list (the runtime enumeration `/kk:design` iterates;
  filesystem discovery is deliberately not used).

## Generated artifacts

Codex generation copies `profiles/` into `kodex-plugin/profiles/` **without
plugin-root resolution** (the `${CLAUDE_PLUGIN_ROOT}` convention text must stay
literal), but it **does** apply the `/kk:` → `$kk:` skill-prefix rewrite to
profile Markdown (`scripts/kodex-generate-manifest.yml`). The copy is therefore
not byte-for-byte verbatim: any `/kk:` reference in the profile is rewritten. After
adding the profile, `make generate-kodex` must run and the generated
`kodex-plugin/profiles/twelve-factor/` must be committed — CI enforces freshness
via `make generate-kodex && git diff --exit-code`.

## Assumptions

- A profile with empty file signals + populated Design signals activates in
  `/kk:design` but never in file-based phases. _Validate:_ `bash
  test/test-plugin-structure.sh` green and a design-token dry run activates it
  while a `review-code` run does not.
- `test/test-plugin-structure.sh` accepts a design-only profile (per-phase
  assertions are presence-conditional). _Validate:_ test green.
- The narrow token set activates on genuine SaaS/service ideas and stays quiet on
  library/CLI/tooling ideas. _Validate:_ manual token dry runs against
  representative prompts.
- k8s `design/sections.md` already covers disposability/port-binding/config.
  Duplication under co-activation is mitigated at runtime by the skip-preamble and
  the merge/cross-reference rule in `questions.md` / `sections.md` — not only by an
  author-time review. _Validate:_ the k8s co-activation eval shows overlapping
  factors asked/required once, not twice.
- Detection/routing behavior — activation on service ideas, non-activation on
  libraries/CLIs, the ambiguous-infra fallback, k8s co-activation without
  duplication, and required-section coverage in the produced design — is verified
  by `/kk:design` eval scenarios under `klaude-plugin/skills/design/evals/`,
  including a regression non-activation eval, not only by a manual dry run.
  _Validate:_ evals present, self-contained, and graded pass.

## Not Doing

- No `twelve-factor` `review-code` / `implement` / `test` / `document` phases —
  design-only.
- No changes to `/kk:design`, `/kk:review-architecture`, `/kk:review-spec`,
  `/kk:review-code`, `/kk:implement`, `/kk:test`, `/kk:document` skill files.
- Not adopting the three factors from *Beyond the Twelve-Factor App* (Kevin
  Hoffman, O'Reilly) — API First, Telemetry, and Security (Authentication &
  Authorization) — i.e. the 15-factor extension. Separately, the evolving official
  `twelve-factor/twelve-factor` `next` branch is also out of scope for this pass.
  Classic 12factor.net factors only.
- No new detection mechanism — reuse the existing design-token + fallback pattern.

## Deferred / Future Work

**Release boundary.** This feature is **Phase 1**: design-phase adoption only. It
raises the 12-factor concerns where architectural decisions are made, but it does
not by itself verify that the resulting code is 12-factor-aligned — that is
approach B. Issue #101 (end-to-end adoption) therefore **remains open** after this
ships; approach B below is the tracked follow-up that closes it. "End-to-end" is
not claimed by Phase 1.

**Approach B — code-level 12-factor checks (implement/review phases).**
Deferred pending exploration. Open questions to resolve before implementing:

- **Deployability gate.** Language profiles (`go`, `python`, `java`, `js_ts`,
  `kotlin`) activate on any source file, including libraries and CLIs where
  service factors (config-in-env, logs-as-streams, port-binding, statelessness)
  do not apply. A gate is needed — candidate: a conditional checklist loaded only
  when a deployability signal (Dockerfile / Procfile / k8s manifest) is present in
  the diff or repo, **with a fallback to clarifying with the user when the signal
  is ambiguous** (reusing the clarification pattern that already exists in the
  flow). The precise Load-if clause and who runs the clarification (main skill vs.
  the read-only `code-reviewer` sub-agent) are unresolved.
- **k8s overlap.** `k8s`/`k8s-operator` are inherently "deployed" and their
  `design/sections.md` already encodes disposability, port-binding, and config.
  For these profiles B is mostly *labeling* existing checks as 12-factor, not
  adding new ones — scope accordingly.
- **Alternative approaches.** Whether to distribute checks per-profile at all
  vs. a shared checklist referenced conditionally, or an opt-in review skill,
  remains open.

Do not implement B without closing the gate question first.

## Rejected Alternatives

- **Monolithic `12factor` profile carrying all phases (approach A)** — rejected:
  12-factor has no reliable file-detection signal, so file-based activation is
  fuzzy, and bundling all phases inflates context.
- **Always-load code-level bullets in language profiles** — rejected: fires
  service-only checks on library/CLI code, contradicting the HMW.
- **k8s-profiles-only for the code-level factors** — rejected: misses non-k8s
  services (bare Docker, PaaS). (This is part of the deferred B decision space.)
- **Baking the design lens into `/kk:design`'s generic `frameworks.md` /
  `refinement-criteria.md`** — rejected: always-on constant context cost and less
  targeted than a confirm-gated profile.
- **Editing `/kk:review-architecture`** — rejected: it does not consult profiles
  (inline, claim-driven, altitude-constrained) and operates above the design
  altitude where 12-factor lives here.
