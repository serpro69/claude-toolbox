---
name: clarify-docs
description: |
  TRIGGER when: asked to clarify or improve existing documentation, PR drafts or
  issue descriptions, including URLs and pasted bodies. Saves results locally,
  grounded in requirements and source while preserving meaning. Not for requests
  to implement, fix or work on an issue, code, config, generic response brevity,
  or agent instructions. Explicit instruction or SKILL.md targets receive a
  $kk:implement suggestion without edits or automatic handoff.
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Clarify Documentation, PR Drafts and Issue Descriptions

Improve an existing document so its intended reader can understand the underlying
work. Produce a local edit; success depends on comprehension and fidelity, with no
document-length target.

## Inputs and boundaries

Accept local documentation, PR or issue-description drafts, remote PR/issue URLs
or pasted bodies, plus audience, purpose, requirements and source references.
GitHub and Linear are examples, not required integrations. Examples:

- `$kk:clarify-docs docs/configuration.md for service owners; use src/config/`
- `$kk:clarify-docs docs/feat/wip/import/design.md for the implementing developer`
- `$kk:clarify-docs pr-draft.md for repository reviewers; use the actual PR base/head`
- `$kk:clarify-docs <PR URL>; save the revised body to docs/feat/wip/import/pr-draft.md`
- `$kk:clarify-docs issue-draft.md; preserve the reported reproduction details`
- `$kk:clarify-docs <issue URL>; save to docs/feat/wip/import/issue-draft.md`

A directory permits discovery and selection, not a bulk rewrite. If selection is
consequentially ambiguous, ask which artifact to edit. Related requirements and
code may be read as evidence; only selected documentation may be changed.

Edit an explicitly selected local draft in place. A capture of pasted/remote input
is not automatically that draft. For remote or pasted input, use the caller's
destination or name a local draft under the clearly established current feature
directory. If neither is clear, ask before writing. Check for an existing file:
overwrite only the selected draft, never unrelated content; otherwise choose an
unused name within that feature scope or clarify the destination. Obtain remote
bodies and relevant context through available read-only tools or supplied text
during the shared procedure's source-reading phase. Reading grants no publishing
authority.

Issue tracker titles and types are read-only context: preserve a supplied title
when included in a local draft and propose no replacement title. Description
headings remain editable. Title editing requires a separately scoped request.

Code, config, agent instructions (including `AGENTS.md` and `CLAUDE.md`), skill
instructions are outside this entry point's scope. An
explicit instruction-editing request receives an explanation of this boundary and
a suggestion to use `$kk:implement`; do not invoke it or edit the target. Ordinary
code requests and generic requests for shorter answers do not activate this skill.
Route by the requested action: implementing, fixing or working on an issue belongs
to `$kk:implement`, not description editing. A URL alone establishes no editorial
intent; clarify consequential ambiguity before selecting a task.

## Workflow

**Mandatory order — instructions before action.** Follow this flow strictly in
sequence. Load this file and the entire shared procedure before content-level
target/source reads, editing or verification. Only filenames and request keywords
may be used for early scope selection.

1. Load [shared-document-clarity.md](shared-document-clarity.md) in full.
2. Resolve the selected artifacts, reader, purpose and destination from the request
   and repository instructions. Reuse known answers; investigate accessible context
   in the shared procedure before asking about consequential gaps.
3. Apply the shared procedure in order: understand the relevant work, establish
   protected meaning, edit the full reading path for the reader, then verify
   reader tasks and consolidation with its checklist before checking fidelity separately.
4. Report changed paths and material unresolved gaps briefly. If no edit was needed,
   say so. Produce no additional summary or claim-ledger file.

The shared procedure performs no profile detection and invokes no consumer skill.
Verification is an in-session check; the caller retains responsibility for normal
document review. This entry point adds no independent runtime review gate and makes
no external writes, publication, deployment or implementation changes.
PR/issue updates, comments and messages remain separate actions outside this workflow.
