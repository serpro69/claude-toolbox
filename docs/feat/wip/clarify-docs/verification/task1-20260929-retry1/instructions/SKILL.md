---
name: clarify-docs
description: |
  TRIGGER when: asked to clarify or improve the explanation in existing local human
  documentation, such as a guide, design document, or implementation plan. Grounds
  edits in requirements and source while preserving technical meaning. Not for code,
  config, generic response brevity, PR drafts, or agent instructions. Explicit
  instruction or SKILL.md targets receive a /kk:implement suggestion without edits
  or automatic handoff.
---

# Clarify Local Documentation

Improve an existing document so its intended reader can understand the underlying
work. Edit the selected artifact in place; success depends on comprehension and
fidelity, with no document-length target.

## Inputs and boundaries

Accept a selected local document or explicitly selected set, plus any audience,
purpose, requirements and source references. Examples:

- `/kk:clarify-docs docs/configuration.md for service owners; use src/config/`
- `/kk:clarify-docs docs/feat/wip/import/design.md for the implementing developer`

A directory permits discovery and selection, not a bulk rewrite. If selection is
consequentially ambiguous, ask which artifact to edit. Related requirements and
code may be read as evidence; only selected documentation may be changed.

Code, config, agent instructions (including `AGENTS.md` and `CLAUDE.md`), skill
instructions and PR drafts are outside this entry point's current scope. An
explicit instruction-editing request receives an explanation of this boundary and
a suggestion to use `/kk:implement`; do not invoke it or edit the target. Ordinary
code requests and generic requests for shorter answers do not activate this skill.

## Workflow

**Mandatory order — instructions before action.** Follow this flow strictly in
sequence. Load this file and the entire shared procedure before content-level
target/source reads, editing or verification. Only filenames and request keywords
may be used for early scope selection.

1. Load [shared-document-clarity.md](shared-document-clarity.md) in full.
2. Resolve the selected artifacts, reader, purpose and destination from the request
   and repository instructions. Reuse known answers; clarify consequential gaps.
3. Apply the shared procedure in order: understand the relevant work, establish
   protected meaning, edit for the reader, then verify comprehension and fidelity.
4. Report changed paths and material unresolved gaps briefly. If no edit was needed,
   say so. Produce no additional summary or claim-ledger file.

The shared procedure performs no profile detection and invokes no consumer skill.
Verification is an in-session check; the caller retains responsibility for normal
document review. This entry point adds no independent runtime review gate and makes
no external writes, publication, deployment or implementation changes.
