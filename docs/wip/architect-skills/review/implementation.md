# Milestone 1 — `/kk:review-architecture` — implementation plan

**Design:** [design.md](design.md). **Umbrella:** [../design.md](../design.md).

Audience: a skilled contributor with **zero context** on this codebase. Read [design.md](design.md) fully first; read `CLAUDE.md` (root) §Skill & Command Naming Conventions, §Skill workflow ordering, §Skill evaluations, and §Profile Conventions before touching files. `klaude-plugin/` is the canonical source; Codex output is generated.

---

## Orientation — study these existing analogues first

The reviewer triad is the template. Before writing anything, read:

- `klaude-plugin/skills/review-code/SKILL.md` and its linked process/rubric files — the workflow-ordering pattern (ADR 0004), delegation to a read-only agent, and how profiles are (conditionally) consulted.
- `klaude-plugin/skills/review-spec/SKILL.md` — closest analogue: it grades an implementation against a spec (claim-vs-reality), which is structurally what Pass 1 does.
- `klaude-plugin/agents/code-reviewer.md` and `spec-reviewer.md` — read-only tool sets (`Read`/`Grep`/`Glob`/`capy_search`), role-named, `## Plugin Root` injection pattern.
- `klaude-plugin/skills/review-code/evals/` — the `evals/<name>/{eval.json,test-files/}` layout and `eval.json` schema.
- `klaude-plugin/commands/` — note the family is split: `review-code`/`review-spec` expose `default.md`/`isolated.md` command pairs, `review-design` does not. **Decision: M1 ships standard mode only — no command pair.** The skill already delegates verification to the read-only agent, so an isolated variant adds nothing yet; revisit a default/isolated split after M1 is proven.

## File inventory (all under `klaude-plugin/`, the canonical source)

**Skill** — `klaude-plugin/skills/review-architecture/`:

- `SKILL.md` — entry point. Frontmatter `name`/`description` (trigger keywords first, ≤1024 soft/1536 hard chars). Workflow section with the **mandatory-order directive** (ADR 0004): load ALL instructions — this SKILL.md, `input-contract.md`, `output-contract.md`, `pass0-extraction.md`, `pass1-topology.md`, `pass2-soundness.md` — before reading any artifact content. Describes delegation to the `architecture-reviewer` agent and resolves `${TOOLBOX_PLUGIN_ROOT}`.
- `input-contract.md` — acceptance rules (§2a of design): what artifacts are accepted, the single-artifact-per-invocation rule (multi-artifact rejected with guidance to run per artifact), diagram-with-prose rule, verbal/diagram-only rejection with an actionable message.
- `output-contract.md` — invocation/scope rules, report structure (Claim Set section, verdicts by dimension, Not Reviewed section, Pass 2 findings), verdict vocabulary, and the verdict→severity mapping (design §7).
- `pass0-extraction.md` — the extraction procedure, the full claim schema (`id`/`claim`/`source_span`/`dimension`/`tense`/`evidence_class`), the repo-blind rule, the four grading sub-metrics framing, and the structural-slot heuristics per artifact type.
- `pass1-topology.md` — the six dimensions with **inline evidence-gathering examples** per dimension (the profile-substitute, §7), the anchor-rule mode decision (tense + anchor existence → reality / internal-soundness / dangling-anchor), and per-dimension claim/evidence/fallback spec.
- `pass2-soundness.md` — the internal-soundness/appropriateness/reversibility procedure.
- `evals/<name>/{eval.json,test-files/}` — see Eval fixtures below.

**Agent** — `klaude-plugin/agents/architecture-reviewer.md`:

- Role-named, read-only (`Read`, `Grep`, `Glob`, `mcp__capy__capy_search`). Its own workflow must **re-state the instruction-before-action rule** (ADR 0004 applies to delegated sub-agents — payload order is not sufficient). References plugin-root content by repo-relative path or via the injected `## Plugin Root` heading (read-only agents have no shell to resolve `${TOOLBOX_PLUGIN_ROOT}`).

**Commands** — none in M1 (decided; see Orientation). `EXPECTED_COMMANDS` stays untouched.

**Tests** — `test/test-plugin-structure.sh`: add `review-architecture` to `EXPECTED_SKILLS`; add commands to `EXPECTED_COMMANDS` if created; ensure the agent is covered.

**Codex parity** — regenerate via `make generate-kodex` (produces `kodex-plugin/` transformed skill + `.codex/agents/architecture-reviewer.toml`). Do NOT hand-edit generated output.

## Eval fixtures (build alongside each pass, TDD)

- `pass0-extraction-recall` — artifact + `gold-claims.json` in `test-files/`; `assertions[]` bullets reference gold entries; assert precision/recall/evidence-class/routing.
- `pass1-boundary-violation` — claim-set + `test-files/` with a real forbidden dependency in a manifest; assert caught.
- `pass1-greenfield-fallback` — forward-looking (`future`-tense) claims, no code; assert internal-soundness mode, not a false "unverified" failure.
- `pass1-brownfield-proposed` — existing codebase slice + claim-set mixing a `future` proposal, a `present` violated claim, and a `present` claim naming a nonexistent component; assert internal-soundness / violation / dangling-anchor respectively (the anchor rule discriminates all three).
- `pass2-inappropriate-mechanism` — artifact stating write-heavy + a write-through cache; assert flagged. (As built: the clash is read-optimizer-vs-write-heavy — a write-through cache taxes every append to serve a minority read path — **not** stale reads. Write-through writes cache and store synchronously, so it cannot serve stale reads and is durable; assertion 6.8 guards against the durability misreading.)
- `regression-clean-artifact` — a sound artifact matching its `test-files/`; assert no findings (proves the skill does not over-fire).

## Build order (vertical slices — each ends in a runnable review + green eval)

Each step names its verification.

1. **Skill skeleton + acceptance & output contracts + agent stub** (contract-first — defines both boundaries). Skill runs end-to-end, classifies an input as accepted/rejected, and emits the report skeleton per `output-contract.md`. → *verify:* invoke on a verbal-only "artifact" → rejected with actionable message; invoke on two ADRs at once → rejected (single-artifact rule); invoke on a real ADR → accepted; `bash test/test-plugin-structure.sh` green after `EXPECTED_SKILLS` update.
2. **Pass 0 extraction + `pass0-extraction-recall` eval.** → *verify:* run the eval; extractor produces a claim-set, grader checks each `gold-claims.json` entry PASS/FAIL via the referencing `assertions[]`; precision/recall/evidence-class/routing reported.
3. **Pass 1 engine (anchor-rule mode decision) + dimensions 1–3 (Boundaries, Data Ownership, NFR) + `pass1-boundary-violation`, `pass1-greenfield-fallback`, `pass1-brownfield-proposed` evals.** → *verify:* boundary-violation caught against a manifest; greenfield `future` claims fall back to internal-soundness; the brownfield fixture discriminates violation vs proposal vs dangling-anchor.
4. **Pass 1 dimensions 4–6 (Failure Isolation, State Consistency, Evolution).** → *verify:* a fixture with circuit-breaker-present-but-no-idempotency scores dim 4 pass / dim 5 fail independently (proves 4/5 are not blended).
5. **Pass 2 soundness + `pass2-inappropriate-mechanism` eval.** → *verify:* the write-heavy/write-through mismatch is flagged; a context-appropriate choice is not.
6. **Regression eval + Codex parity + docs.** → *verify:* `regression-clean-artifact` produces no findings; `make generate-kodex && git diff --exit-code kodex-plugin/ .codex/agents/` clean; `make plugin-graph` (link/orphan gate) green; run `/kk:document`.

## Conventions checklist (do not skip)

- **ADR 0004 ordering** in both SKILL.md and the agent — instructions fully loaded before artifact content is read; content-read instruction appears exactly once, after instruction-load.
- **Naming** — `/kk:review-architecture` (family-consistent); agent `architecture-reviewer` (role, not skill).
- **`${TOOLBOX_PLUGIN_ROOT}` rules** — brace form only in plugin-load files (SKILL.md, agent); files read at runtime via `Read` must not forward the literal token; inject the resolved path into the read-only agent under `## Plugin Root`.
- **Description budget** — trigger keywords first; detail lives in the body.
- **Capy** — after the design is stable, index only non-obvious rationale as `kk:arch-decisions` (skip if self-evident from these docs).

## Assumptions (validate during build)

- LLM reliably greps static manifests for topology evidence given inline examples — if dim 1/6 evals are flaky, that assumption is failing → add a profile (M4) sooner.
- A per-eval `gold-claims.json` is enough oracle for recall/routing grading — if graders disagree, the claim schema needs tightening.

## Not Doing / Rejected Alternatives

Carried from [design.md](design.md) — see §Not Doing and §Rejected Alternatives there. Notably: no producer skills, no profile detection (M4), no behavioral verification, security delegated to PAL `secaudit`.
