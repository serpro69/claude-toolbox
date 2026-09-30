# ADR 0009: Optional Document Clarification

## Status

Accepted (2026-09-30)

## Context

The original [clarify-docs design](../feat/done/clarify-docs/design.md) integrated
an automatic final editorial pass into `/kk:design` and `/kk:document`. Both loaded
the shared procedure on every invocation, including invocations with no edits.

That avoided a separate invocation but bundled additional source investigation and
document rewriting into ordinary writing workflows. During review, Sergio chose
to make this separate pass an explicit user decision, similar to design review.
Clear, accurate drafting remains the writing skills' responsibility.

## Decision

The writing skills suggest `/kk:clarify-docs` after creating or materially revising
documents, naming only those output paths. They do not load or execute the shared
clarification procedure automatically. Unchanged resumes and documentation
invocations with no substantive outputs omit the suggestion.

Design presents optional clarification before its existing `/kk:review-design`
recommendation so a user choosing both can review the final wording. Clarification
does not replace review or become a required gate before implementation.

Operative instructions live in the [design entry point](../../klaude-plugin/skills/design/SKILL.md),
its [fresh-idea](../../klaude-plugin/skills/design/idea-process.md) and
[resume](../../klaude-plugin/skills/design/existing-task-process.md) workflows,
and the [document entry point](../../klaude-plugin/skills/document/SKILL.md).

## Consequences

- Users control whether to incur the additional editorial work; fewer documents
  may receive the separate pass.
- The consumers no longer load the clarification instructions or need their
  per-skill symlinks. The standalone skill and shared procedure retain their behavior.
- `/kk:implement` plan completion still calls `/kk:document`, which may suggest
  clarification. Neither implementation mode gains an automatic clarification call.
- Integration evals now check recommendations, absence of automatic loading and
  execution, and preservation of ordinary drafting requirements. Historical eval
  results and the archived design remain records of the earlier behavior.
