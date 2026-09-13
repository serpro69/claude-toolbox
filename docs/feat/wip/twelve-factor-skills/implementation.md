# Implementation: 12-Factor design-phase profile

> Design: [./design.md](./design.md)
> Issue: [serpro69/claude-toolbox#101](https://github.com/serpro69/claude-toolbox/issues/101)

Audience note: you are an experienced contributor new to this repo. Read
`AGENTS.md` §Profile Conventions before starting — it is the authoritative spec
for profile layout, the `DETECTION.md` schema, the `index.md` bidirectional
invariant, and registration.

## Orientation — files you will touch

- **New:** `klaude-plugin/profiles/twelve-factor/` (`DETECTION.md`, `overview.md`,
  `design/index.md`, `design/questions.md`, `design/sections.md`).
- **Edit:** `klaude-plugin/skills/_shared/profile-detection.md` (Known profiles
  list).
- **Edit:** `test/test-plugin-structure.sh` (`EXPECTED_PROFILES`).
- **Generated (do not hand-edit):** `kodex-plugin/profiles/twelve-factor/` — emitted
  by `make generate-kodex`.

Reference existing profiles as templates: `k8s/DETECTION.md` (Design signals
block, empty-section discipline), `k8s/design/sections.md` (grouped-section style
+ "omit none / justify N/A" rule), `k8s/design/index.md` and `go/design/index.md`
(index.md always-load/conditional format).

## Authoring rules that apply here

- Content under `profiles/**` is read at runtime via the `Read` tool, which does
  **not** substitute `${CLAUDE_PLUGIN_ROOT}`. Do not embed that token as a live
  path in profile prose. Prefer explicit factor names and plain paths.
- Plugin content must be **self-contained**: no references to this repo's `docs/`,
  no ADR citations. State rules in full inside the profile files.
- `DETECTION.md` must carry all three signal headings (`## Path signals`,
  `## Filename signals`, `## Content signals`) even when empty — the structure
  test asserts their presence. Add `## Design signals` below them.

## Build order

The order matters: create the profile files first, register last. Registering
`EXPECTED_PROFILES` before the files exist makes per-profile assertions fail.

### 1. Profile skeleton + DETECTION.md

Create `profiles/twelve-factor/DETECTION.md` with the three signal headings left
empty (a one-line note under each stating this profile does not do file-based
detection and why — code-level checks are deferred to approach B) and a populated
`## Design signals` section with `display_name` and the narrow token list from
design.md. → verify: `grep '## Design signals' …/DETECTION.md` and the three
required headings all present.

### 2. overview.md

Write `overview.md`: what the profile covers (classic 12 factors, design-phase
lens), when it activates (design-token match, confirm-gated; never in file-based
phases), and a compact enumeration of the 12 factors. Note: `overview.md` is
required by convention and serves the human/authoring role — the design flow does
**not** load it (it reads `DETECTION.md` for tokens and `design/index.md`
always-load entries), so the factor content the flow actually uses must live in
`questions.md` / `sections.md`. → verify: file exists; structure test's "each
profile has DETECTION.md and overview.md" assertion passes.

### 3. design/ content

Create `design/questions.md` (refinement-question pool, one entry per factor
cluster from design.md §questions.md). It MUST open with the skip-preamble (skip
questions already answered by the user, codebase, prior decisions, existing
`design.md`, **or another active profile**) and the co-active-profile deferral
rule (defer to `k8s` the factors it already covers). Use factor-accurate phrasing:
III = environment variables (or a named, justified deviation); IX = graceful
SIGTERM drain **and** sudden-death robustness + reentrant/idempotent jobs; II =
exact/version-pinned + isolated dependencies. Create `design/sections.md` (the
four grouped required sections + the one-line codebase/dependencies (I/II)
preamble + the "omit none / justify N/A" rule + the co-active merge/cross-reference
rule). Then create `design/index.md` listing `questions.md` and `sections.md`
under **Always load**, each as a markdown link + one-line description. → verify:
every link resolves (forward invariant) and no `.md` in `design/` is unreferenced
(reverse invariant) — both checked by the structure test; and `questions.md`
contains the skip-preamble, `sections.md` the I/II preamble.

### 4. Register in Known profiles

Append `- twelve-factor` to the **Known profiles** list in
`klaude-plugin/skills/_shared/profile-detection.md`. This is the runtime
enumeration `/kk:design` iterates; without it the profile is invisible to
detection. → verify: `grep twelve-factor …/profile-detection.md`.

### 5. Register in the structure test

Append `twelve-factor` to `EXPECTED_PROFILES` in `test/test-plugin-structure.sh`
(keep the array's existing ordering convention). → verify: `bash
test/test-plugin-structure.sh` is green (structure, DETECTION headings, presence-
conditional index, bidirectional invariant).

### 6. Regenerate codex output

Run `make generate-kodex`. It copies the profile into
`kodex-plugin/profiles/twelve-factor/` without plugin-root resolution but **with**
the `/kk:` → `$kk:` skill-prefix rewrite applied to Markdown
(`scripts/kodex-generate-manifest.yml`) — so any `/kk:` reference in the profile is
rewritten; keep such references intentional. Commit the generated files. →
verify: `make generate-kodex && git diff --exit-code kodex-plugin/ .codex/agents/`
produces no diff (the CI freshness gate).

### 7. Graph validation

Run `make plugin-graph` (runs the analyzer's tests and `plugin-graph validate`
against `klaude-plugin/` as a broken-link/orphan gate). → verify: validate passes
with no new broken links or orphans for the `twelve-factor` nodes.

### 8. Author `/kk:design` detection evals

Add eval scenarios under `klaude-plugin/skills/design/evals/` (per `AGENTS.md`
§Skill evaluations — one directory per eval, `eval.json` + `test-files/`, oracles
in a sibling `oracle/` never inside `test-files/`). Cover:

- a positive service-shaped prompt that must activate `twelve-factor` **and** whose
  graded design contains every required profile section;
- a negative library/CLI prompt that must NOT activate it (regression);
- an ambiguous-infra prompt (names no specific technology) that must hit the shared
  fallback;
- a `k8s` co-activation prompt that must ask/require overlapping factors once, not
  twice.

→ verify: eval directories present and self-contained; a manual grading pass over
each `eval.json` assertion set passes. No profile ships evals today, so these live
with the consuming skill (the `design` skill already has an `evals/` directory).

## Verification summary

- `bash test/test-plugin-structure.sh` — green.
- `make plugin-graph` — validate passes.
- `make generate-kodex && git diff --exit-code kodex-plugin/ .codex/agents/` — no diff.
- Detection evals (`klaude-plugin/skills/design/evals/`) grade pass: positive
  activation + required-section coverage, negative library/CLI regression,
  ambiguous fallback, and k8s co-activation-without-duplication.
- Detection dry run (sanity, backed by the evals above): "stateless service" /
  "backing service" prose surfaces the confirm prompt; a pure library/CLI idea does
  not; a `review-code`/file-based run never activates the profile.

## Assumptions

Carried from design.md — see [design.md §Assumptions](./design.md#assumptions).
The load-bearing one to validate first: a design-only profile with empty file
signals passes the structure test and activates only in the design phase.

## Not Doing

See [design.md §Not Doing](./design.md#not-doing). Notably: no code-level checks,
no skill-file edits, classic 12 factors only.

## Deferred / Future Work

Approach B (code-level factor checks + deployability gating) is deferred with open
questions — see [design.md §Deferred / Future Work](./design.md#deferred--future-work).
