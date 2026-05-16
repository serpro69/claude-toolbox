# Skills

The kk plugin ships 10 workflow skills that form a complete development pipeline.

## The Pipeline

```
/design → /review-design → /implement → /review-code → /test → /document
```

1. **design** — turns an idea into design docs, an implementation plan, and a task list
2. **review-design** — evaluates design docs for completeness and technical soundness
3. **implement** — executes tasks with review checkpoints between batches
4. **review-code** — reviews code for SOLID violations, security risks, and quality issues
5. **test** — generates tests and runs the full suite
6. **document** — updates architecture docs and records ADRs

## Skill Reference

| Skill | What it does |
|-------|-------------|
| **design** | Turns an idea into design docs, an implementation plan, and a task list in `docs/wip/`. Asks refinement questions, then documents everything a developer needs to start coding. |
| **implement** | Executes a task list from `docs/wip/` with batched steps and code review checkpoints between batches. Updates task status as it goes. |
| **test** | Generates tests following project conventions: table-driven, integration, mocking, property-based. Runs the full suite and reports coverage. |
| **document** | Updates ARCHITECTURE.md, TESTING.md, and records ADRs for non-obvious decisions made during implementation. |
| **review-code** | Reviews git changes for SOLID violations, security risks, and code quality. Language-specific checklists for Go, Java, JS/TS, Kotlin, and Python. Standard and isolated modes. |
| **review-design** | Pre-implementation review gate. Evaluates design docs for completeness, internal consistency, and technical soundness before code is written. |
| **review-spec** | Compares implemented code against design/implementation docs. Finds spec deviations, missing implementations, and outdated docs — in both directions. |
| **dependency-handling** | Fires before calling a library/SDK/API or adding a dependency. Forces a capy/context7 lookup instead of guessing signatures or behavior. |
| **merge-docs** | Merges two competing design docs for the same feature into one unified document, resolving conflicts and preserving the best of both. |
| **chain-of-verification** | Makes Claude fact-check its own answers. Standard mode (prompt-based) or isolated mode (independent sub-agents). For high-stakes accuracy. |

## Commands

Commands are skill variants invoked with explicit mode selection:

| Command | Invocation | Description |
|---------|-----------|-------------|
| Code Review (isolated) | `/kk:review-code:isolated` | SOLID code review with independent sub-agents |
| CoVe (standard) | `/kk:chain-of-verification:default [question]` | Chain-of-Verification with prompt-based isolation |
| CoVe (isolated) | `/kk:chain-of-verification:isolated [--explore] [--haiku] [question]` | CoVe with true sub-agent isolation |
| Spec Review | `/kk:review-spec:default [feature]` | Verify code matches design/implementation docs |
| Spec Review (isolated) | `/kk:review-spec:isolated [feature]` | Spec conformance review with independent sub-agent |
| Design Review | `/kk:review-design [feature] [scope]` | Review design docs for quality and technical soundness |
| Design Review (isolated) | `/kk:review-design:isolated [feature] [scope]` | Design review with independent sub-agents |
| Template Sync | `/kk:template:sync [--version vX.Y.Z] [--dry-run]` | Sync repo with upstream template |

## Utility Skills

**dependency-handling** is pulled in automatically during implementation whenever you touch an external library, SDK, or API — it routes through capy/context7 instead of guessing.

**review-spec** verifies code matches design/spec and detects deviations — use during or after implementation.

**merge-docs** reconciles competing design docs into one unified document.

**chain-of-verification** adds self-verification for high-stakes accuracy at any stage.
