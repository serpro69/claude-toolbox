# Skills

The kk plugin ships 13 workflow skills that form a complete development pipeline.

## The Pipeline

```
/kk:design → /kk:review-design → /kk:implement → /kk:review-code → /kk:test → /kk:document
```

1. **/kk:design** — turns an idea into design docs, an implementation plan, and a task list
2. **/kk:review-design** — evaluates design docs for completeness and technical soundness
3. **/kk:implement** — executes tasks with review checkpoints between batches
4. **/kk:review-code** — reviews code for SOLID violations, security risks, and quality issues
5. **/kk:test** — generates tests and runs the full suite
6. **/kk:document** — updates architecture docs and records ADRs

## Skill Reference

| Skill | What it does |
|-------|-------------|
| **/kk:design** | Turns an idea into design docs, an implementation plan, and a task list in `docs/wip/`. Asks refinement questions, then documents everything a developer needs to start coding. |
| **/kk:implement** | Executes a task list from `docs/wip/` with batched steps and code review checkpoints between batches. Updates task status as it goes. |
| **/kk:test** | Generates tests following project conventions: table-driven, integration, mocking, property-based. Runs the full suite and reports coverage. |
| **/kk:document**  | Updates project documentation and records ADRs for non-obvious decisions made during implementation.                                                                     |
| **/kk:review-code** | Reviews git changes for SOLID violations, security risks, and code quality. Domain-specific checklists for Go, Java, JS/TS, Kotlin, Python, Kubernetes, K8s Operator, and agent skills. Standard and isolated modes. |
| **/kk:review-design** | Pre-implementation review gate. Evaluates design docs for completeness, internal consistency, and technical soundness before code is written. |
| **/kk:review-spec** | Compares implemented code against design/implementation docs. Finds spec deviations, missing implementations, and outdated docs — in both directions. |
| **/kk:model** | Produces or updates a domain-reference kit — a durable glossary + divergences/traps page pair per bounded context, with concept-to-code bindings. Its primary output is a decision queue of precise, role-tagged questions only a human can close. Runs upstream of `/kk:design` as the first producer of the architecture flow. |
| **/kk:review-architecture** | Reviews a written architecture artifact (ADR, architecture doc, a design doc's architecture section, or a domain-reference kit — glossary + traps pages reviewed as one composite artifact) against the system it describes. Claim-driven: extracts an inspectable claim-set, verifies mechanism existence/topology across seven dimensions, and grades decision soundness, reversibility, and provenance (self-certification of reverse-engineered claims). Security architecture is delegated to PAL `secaudit`. |
| **/kk:dependency-handling** | Fires before calling a library/SDK/API or adding a dependency. Forces a capy/context7 lookup instead of guessing signatures or behavior. |
| **/kk:diff-skill** | Compares two versions of a skill's markdown instructions to detect degradations and complexity increases. Asymmetric — only regressions count. |
| **/kk:merge-docs** | Merges two competing design docs for the same feature into one unified document, resolving conflicts and preserving the best of both. |
| **/kk:chain-of-verification** | Makes Claude fact-check its own answers. Standard mode (prompt-based) or isolated mode (independent sub-agents). For high-stakes accuracy. |

## Commands

Commands are skill variants invoked with explicit mode selection:

| Command | Invocation | Description |
|---------|-----------|-------------|
| Code Review (isolated) | `/kk:review-code:isolated` | SOLID code review with independent sub-agents |
| CoVe (standard) | `/kk:chain-of-verification:default [question]` | Chain-of-Verification with prompt-based isolation |
| CoVe (isolated) | `/kk:chain-of-verification:isolated [--explore] [--haiku] [question]` | CoVe with true sub-agent isolation |
| Spec Review | `/kk:review-spec:default [feature]` | Verify code matches design/implementation docs |
| Spec Review (isolated) | `/kk:review-spec:isolated [feature]` | Spec conformance review with independent sub-agent |
| Template Sync | `/kk:template:sync [--version vX.Y.Z] [--dry-run]` | Sync repo with upstream template |

## Utility Skills

**/kk:dependency-handling** is pulled in automatically during implementation whenever you touch an external library, SDK, or API — it routes through capy/context7 instead of guessing.

**/kk:review-spec** verifies code matches design/spec and detects deviations — use during or after implementation.

**/kk:model** produces the domain-reference kit (glossary + traps pages) and a role-tagged decision queue for a bounded context — use before feature design when the domain's concepts, code bindings, or open questions need mapping.

**/kk:review-architecture** reviews an ADR, architecture doc, or domain-reference kit against the codebase it claims to describe — use after an architecture artifact is written, before or during implementation.

**/kk:merge-docs** reconciles competing design docs into one unified document.

**/kk:chain-of-verification** adds self-verification for high-stakes accuracy at any stage.
