---
name: solid-code-review
description: |
  Code review of current git changes with an expert senior-engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements.
  Use when performing code reviews.
---

# SOLID Code Review

## Overview

Perform a structured review of the current git changes with focus on SOLID, architecture, removal candidates, and security risks. Default to review-only output unless the user asks to implement changes.

## Conventions

Read capy knowledge base conventions at [capy-knowledge-protocol.md](../_shared/capy-knowledge-protocol.md).

## Review Modes

### Standard Mode (`/kk:solid-code-review`)

Reviews code in the main conversation context. Fast, single-pass review using the workflow below.

### Isolated Mode (`/kk:solid-code-review:isolated`)

Delegates detection to independent reviewers that did not write the code, then annotates their findings with author context. Two parallel reviewers: a `code-reviewer` sub-agent and `pal codereview` (external model in native format). Produces a report organized by agreement level with corroborated findings highlighted.

- **Cost**: Higher (sub-agent + external model + annotation)
- **Isolation**: True — reviewers have zero authorship bias or session context
- **Degradation**: Graceful — if one reviewer fails, proceeds with the other; if both fail, suggests standard mode fallback
- **Best for**: When extra rigor is worth the cost (pre-merge, high-stakes changes)

See [review-isolated.md](./review-isolated.md) for the isolated workflow.

## Severity Levels

| Level  | Name     | Description                                                      | Action                             |
| ------ | -------- | ---------------------------------------------------------------- | ---------------------------------- |
| **P0** | Critical | Security vulnerability, data loss risk, correctness bug          | Must block merge                   |
| **P1** | High     | Logic error, significant SOLID violation, performance regression | Should fix before merge            |
| **P2** | Medium   | Code smell, maintainability concern, minor SOLID violation       | Fix in this PR or create follow-up |
| **P3** | Low      | Style, naming, minor suggestion                                  | Optional improvement               |

## Workflow

**Phases:**

1. Preflight context — scope changes, re-read changed files, search prior findings
2. Detect primary language — load language-specific reference checklists
3. SOLID + architecture smells
4. Removal candidates + iteration plan
5. Security and reliability scan
6. Code quality scan
7. Self-check and confidence assessment
8. Present results with next steps

See [review-process.md](./review-process.md) for the detailed step-by-step process.

## Invocation

Standard mode:

```
/kk:solid-code-review
```

Isolated mode with independent sub-agents:

```
/kk:solid-code-review:isolated
```
