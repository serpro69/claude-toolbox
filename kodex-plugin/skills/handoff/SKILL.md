---
name: handoff
description: |
  Explicitly invoke $kk:handoff to publish active-task context and a fresh-session
  starter prompt to a new secret GitHub gist. For restarting a conversation or
  switching providers or machines; requires the GitHub CLI. Not a local save.
disable-model-invocation: true
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Hand off the active task

Publish `handoff.md` and `prompt.md` in a fresh **secret (unlisted) GitHub gist**.
Anyone with the link can read it. Invoking `$kk:handoff` requests this publication;
normal host permissions still apply, with no extra recurring confirmation step.
Ordinary summary, continuation or review-context requests do not invoke this skill.

## Workflow

**Mandatory order — instructions before action.** Follow this workflow strictly
in sequence. Read this entire skill before inspecting task evidence, preparing
files or publishing. This file contains all operative instructions; no other
protocol is required. Only bounded routing inspection for a declared detection
predicate could precede instruction loading; this skill has no such predicate.

### 1. Establish the continuation context

Use the conversation actually available to identify the active task and relevant
earlier decisions. Follow ordinary explicit user instructions about scope; there
is no custom argument syntax. Make focused read-only project checks only when
needed to reconcile progress or establish identity. This is the investigation
entry point: do not run tests, conduct reviews, finish implementation, scan other
worktrees or collect the whole repository for a handoff.

Prepare a concise, self-contained Markdown record using the outline below. Omit
empty sections and repetition, without discarding context needed for the next
decision or imposing a word limit.

| Content | Include when relevant |
| --- | --- |
| Identity | Task/topic, creation time, repository identity, branch/worktree and relevant revision if known. Label local paths as source-machine paths. |
| Objective and constraints | User intent, corrections, accepted scope and operating constraints. |
| Decisions and rationale | Accepted choices and reasons; abandoned approaches worth avoiding. Distinguish user decisions from agent proposals. |
| Progress and evidence | Completed/pending work, repository-relative file references, attributed verification results and uncertainties. Remembered tests are recorded evidence, not newly run verification. |
| Continuation | Blockers, unanswered questions, dependencies and the next useful action. Do not execute it. |
| Supporting references | Useful project documents, issues and eligible existing Capy references, with a reason to follow each. |

State material context gaps, including earlier conversation lost to compaction.
Describe uncommitted work as local: a gist transfers neither worktree changes nor
patches, credentials or a Capy database. Essential context must remain usable
without optional references or source-machine paths.

**Existing Capy references only.** Include a reference only when the available
conversation already evidences prior indexing/retrieval or confirmed archival of
that specific relevant material. Tool availability, a familiar source label, a
bare current session ID or unrelated indexing is insufficient. Otherwise omit
Capy references; do not search merely to fill this section. For an eligible
reference, retain the known source label or archived session identifier, project
scope, a focused retrieval query/instruction and why it helps. Note destination
availability limits without copying or recreating the source.

**Never initiate indexing or archival during handoff.** This includes indexing,
fetch-and-index, vault import/reindex/archive, and indirect actions through tools,
other skills, agents or the starter prompt. Never repair a missing reference by
indexing it. Do not load a general Capy indexing protocol. This boundary governs
handoff-initiated actions; it does not disable independent host storage or hooks.

### 2. Prepare safe outgoing files

Allocate a unique temporary directory outside the working repository (for
example, `mktemp -d /tmp/kk-handoff.XXXXXXXX`). Retain its absolute path. Use native
file tools to write `handoff.md` and draft the starter-prompt wording there; keep
file bodies out of shell interpolation. Do not create a persistent local store,
write artifacts into the repository, stage or commit anything.

Prepare a gist description containing the project/topic and creation time.
Before sending **each** payload, read its local content and omit or redact
credentials, authentication tokens, credential-bearing connection strings and
unrelated private information. Check `handoff.md` and the description now; check
the completed `prompt.md` again before adding it. A relevant hostname alone is
not a credential. If a safe, useful payload cannot be prepared, stop before
uploading it and explain the problem without echoing sensitive values.

### 3. Publish in two writes

Use the existing authenticated `gh` CLI. Do not install it, change credentials or
permission configuration, or switch storage products. Normal host approval
requests remain available when required; honor denials. Quote paths, the
description and returned URL as shell arguments; never interpolate Markdown
bodies into commands.

1. Create a **new secret gist** with the prepared file:
   `gh gist create <absolute-handoff.md-path> --desc <description>`.
   Omit `--public`/`-p`. Retain the returned URL immediately; a local filename or
   directory name cannot replace the remote identifier.
2. Finish `prompt.md` with that actual URL and the exact filename `handoff.md`.
   Address the receiving agent: ask it to read that handoff, reconcile relevant
   current project state with the recorded evidence, and continue the intended
   task. Keep the prompt short and usable without a separate resume skill. Do not
   silently choose another handoff or instruct the recipient to index/archive
   anything. Apply the outgoing-content check to the finished prompt.
3. Add the file noninteractively to that same newly created gist:
   `gh gist edit <returned-gist-url> --add <absolute-prompt.md-path>`.
4. Successful responses from both publishing commands complete publication.
   Return the gist URL and the ready-to-paste starter prompt. **Do not inspect the
   remote gist afterward**: no `gh gist view`, API/metadata read, download or
   other publication check.

After success, remove only this invocation's temporary preparation files using
host-permitted file operations. If cleanup fails or is denied, report remaining
absolute paths separately: publication still succeeded and must not be retried.
Do not work around a deletion denial with another command or tool. Gists remain
until the user removes them.

### Failure and uncertainty

On a failed, denied or uncertain publishing command, stop; preserve prepared
local files and report their absolute paths with the concrete failure. Do not
inspect remote state or automatically retry.

- If creation may have succeeded but its response was lost, report an uncertain
  outcome without inventing a URL or creating a duplicate.
- If creation returned a URL but adding `prompt.md` failed or is uncertain,
  report that URL as partial/uncertain, along with the recovery files. Do not
  claim the complete two-file handoff was published.
- Missing CLI, rejected authentication, unavailable network or denied permission
  does not justify public publication, repository fallback, credential changes,
  deleting a partial gist or overwriting an older snapshot.
