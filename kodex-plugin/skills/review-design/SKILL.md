---
name: review-design
description: |
  Review design, implementation, and task documents produced by design. Evaluates document quality, internal consistency, and technical soundness.
  Use after design completes and before starting implement.
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Design Review

## Conventions

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Read verification policy** at [shared-verification-policy.md](shared-verification-policy.md).

## Overview

Pre-implementation review gate that evaluates design documents produced by `$kk:design` before code is written. Sits between `$kk:design` (creates docs) and `$kk:implement` (executes them). Reviews tree distinct dimensions

- document quality/structure (completeness, internal consistency, clarity, convention adherence)
- technical soundness (architectural viability, edge cases, failure modes, trade-off analysis)
- feature value (Does the feature improve things for end-users? Is it useful? Is it correct in _how_ it tries to solve the problem?)

## Review Modes

### Standard Mode (`$kk:review-design`)

Reviews design documents in the main conversation context. Fast, single-pass review using the workflow below.

### Isolated Mode (`$kk:review-design:isolated`)

Delegates detection to independent reviewers that did not participate in the design, then annotates their findings with author context. One internal `design-reviewer` sub-agent plus external review chosen **once at discovery**: `pal codereview` (document-review branch) when an API model is available, otherwise one `pal clink` CLI review per eligible non-authoring provider using its configured model (variable count; on the clink roster the provider that authored the documents is excluded and each client's provider must be declared by the operator, for example in the project's `CLAUDE.md`). Every reviewer applies the same shared design-review criteria and verification policy, framed as document review so planned implementation is not reported as missing code. Produces a report organized by agreement level with corroborated findings highlighted.

- **Cost**: Higher (sub-agent + one or more external reviews + annotation); clink cost scales with the roster size
- **Isolation**: True — reviewers have zero authorship bias or session context; each external reviewer gets a fresh conversation
- **Degradation**: Graceful — a failed reviewer is disclosed and the others proceed; an API runtime failure never switches to clink; if every reviewer fails, suggests standard mode fallback
- **Requires**: a PAL build whose `listmodels` exposes CLI client observations in every mode for the clink path; unresolved discovery keeps the internal review with an explicit external coverage limit
- **Scope**: the same default all-documents scope and explicit `design` / `implementation` / `tasks` subsets as standard mode; missing requested documents are disclosed, not substituted
- **Best for**: When extra rigor is worth the cost (before starting implementation of high-stakes features)

See [review-isolated.md](./review-isolated.md) for the isolated workflow; it replaces the standard-mode process file in that mode and is the only place that loads the isolated-only shared files (the design-review criteria, the PAL codereview protocol and the external-review protocol). Standard mode does not read them.

## Finding Types

| Type                   | Code           | Description                                                                              |
| ---------------------- | -------------- | ---------------------------------------------------------------------------------------- |
| Incomplete Spec        | `INCOMPLETE`   | Section lacks sufficient detail for implementation                                       |
| Internal Inconsistency | `INCONSISTENT` | Two parts of the docs contradict each other                                              |
| Technical Risk         | `TECH_RISK`    | Architecture choice has unaddressed failure modes, scalability concerns, or edge cases   |
| Missing Concern        | `MISSING`      | Cross-cutting concern is absent (error handling, migration, backwards compatibility)     |
| Ambiguity              | `AMBIGUOUS`    | Requirements can be interpreted multiple ways, likely to cause implementation divergence |
| Structure Issue        | `STRUCTURE`    | Document doesn't follow project conventions — missing sections, vague subtasks           |

## Severity Levels

| Level  | Name     | Description                                                                              | Action                           |
| ------ | -------- | ---------------------------------------------------------------------------------------- | -------------------------------- |
| **P0** | Critical | Fundamental flaw — design will not work as described, or critical requirement is missing | Must fix before implementation   |
| **P1** | High     | Significant gap — likely to cause rework or wrong implementation                         | Should fix before implementation |
| **P2** | Medium   | Moderate concern — ambiguity or missing detail that could cause confusion                | Fix or create follow-up          |
| **P3** | Low      | Minor — style, structure, or nitpick                                                     | Optional                         |

## Workflow

**Mandatory order — methodology before evaluation.** The flow below is strictly sequential. Load this SKILL.md, the selected process file and shared protocols before reading or evaluating subject documents. Only bounded inspection for a declared routing predicate may precede remaining instruction loads. The review methodology and rubric precede the design documents they assess.

**Phases:**

1. Load documents — parse scope, locate feature directory, read in-scope docs
2. Capy search — search `kk:arch-decisions` and `kk:review-findings` for prior context
3. Document quality review — completeness, clarity, consistency, convention adherence
4. Technical soundness review — viability, edge cases, trade-offs, scalability, testing strategy
5. Self-check and confidence assessment — re-read, question assumptions, assign confidence
6. Present findings with next steps

See [review-process.md](./review-process.md) for the detailed step-by-step process.

## Invocation

**Post-design gate.** This is the recommended review step after `$kk:design` completes and before `$kk:implement` begins. The default scope reviews all documents, including task-format checks.

Standard mode — reviews all documents by default:

```
$kk:review-design [feature-name]
```

Standard mode with scope — review specific documents:

```
$kk:review-design [feature-name] design
$kk:review-design [feature-name] implementation
$kk:review-design [feature-name] tasks
```

| Scope            | Documents reviewed                             |
| ---------------- | ---------------------------------------------- |
| _(none)_         | `design.md` + `implementation.md` + `tasks.md` |
| `design`         | `design.md` only                               |
| `implementation` | `implementation.md` only                       |
| `tasks`          | `tasks.md` only                                |

Isolated mode with independent sub-agents:

```
$kk:review-design:isolated [feature-name]
$kk:review-design:isolated [feature-name] tasks
```
