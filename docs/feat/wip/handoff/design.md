# Manual handoff through a secret gist

> Status: ready for implementation; review findings reconciled
> Created: 2026-10-28
> Issue: [#102](https://github.com/serpro69/claude-toolbox/issues/102)
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)

## Problem and intended outcome

A developer using Claude Code or Codex needs to restart a long conversation, switch providers or machines, or return to unfinished work later. A fresh agent can inspect the repository, but that does not recover the user's corrections, decisions and their rationale, abandoned approaches, or the intended next action.

`/kk:handoff` creates a portable continuation record for the active task. Success means a destination session, given the resulting starter prompt, can identify the objective, relevant constraints, current progress and next useful action without asking the user to reconstruct facts already established in the source conversation. It must distinguish observations from assumptions and preserve unresolved questions rather than invent answers.

The feature is a small, instructions-only skill. It uses ordinary agent file tools and the GitHub CLI; it adds no runtime helper, service or storage framework. The user explicitly selected this approach after comparing it with a bundled storage helper.

## Confirmed decisions

- Creation requires explicit skill invocation. Claude Code and Codex invocation metadata disable implicit selection. Loading the resulting handoff is explicit in the destination session. There are no lifecycle hooks or handoff discovery.
- The default scope is the active task, with earlier context included when it affects continuation. There is no special override protocol or argument parser for ordinary user instructions.
- Each invocation produces a new secret GitHub gist containing `prompt.md` and `handoff.md`. Concurrent conversations never update a shared latest handoff.
- Successful `gh` publication completes the producer workflow. There is no post-publication download, read-back, metadata inspection or additional verification.
- Secret means anyone with the link can read it. The user explicitly accepted that access model for v1 after GitHub's distinction between secret and private was explained. The feature must call it secret or unlisted, not private.
- Handoff artifacts are not written into, staged in, or committed to the working repository. Temporary local preparation outside the repository is allowed.
- Capy references are eligible only when prior indexing or archival of the referenced material is already evidenced. **The handoff process must never index or archive anything.**
- Gists remain until the user removes them. There is no automatic retention or cleanup service.

The gist decision supersedes the earlier proposal to retain local files in `~/.local/state/kk/handoffs/`. The original issue's session-end hook suggestion is outside the accepted first iteration.

## User flow

1. The user invokes `/kk:handoff` in the source conversation.
2. The agent loads the skill instructions, identifies the active task and assembles a concise continuation record. It uses focused read-only checks when needed to establish repository identity or reconcile recorded progress with current state.
3. The agent prepares the files in a unique temporary directory outside the working repository, removes credentials and unrelated private content from outgoing material, then publishes a new secret gist through the user's existing GitHub CLI authentication.
4. When `gh` reports successful publication of the files, the agent returns the gist URL plus the ready-to-paste starter prompt.
5. The user supplies that prompt to the destination session. The receiving agent reads the named handoff, checks relevant current project state, and continues the active task. No installation of a separate resume skill is required.

Invoking the skill requests publication to GitHub; it is not a local-save command with an unexpected upload afterward. Its description and user documentation must make that effect clear. Normal host permissions still apply. The skill adds no recurring confirmation step, changes no credentials or permissions, and reports a denied operation accurately.

## Manual-only invocation

Set `disable-model-invocation: true` in the canonical `SKILL.md` frontmatter for Claude Code. Add `agents/openai.yaml` inside the same canonical skill directory with `policy.allow_implicit_invocation: false` for Codex. These are the hosts' documented invocation controls: [Claude Code](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill), [Codex](https://learn.chatgpt.com/docs/build-skills#optional-metadata). The sidecar is skill metadata, not a sub-agent definition. The generator already copies nested YAML unchanged.

Keep the description concise and explicit about publishing a gist, but use host metadata to enforce manual selection. Ordinary requests to summarize work, continue a task or refresh a review handoff must not implicitly activate the skill. Existing workflow steps do not authorize publication merely by using the word “handoff.”

Clarify ambiguous live instructions alongside the new skill: name implementation's review preparation “Refresh the review context,” describe design's transition as recommending implementation, and say that clarification suggests `/kk:implement` without invoking it. This is targeted wording cleanup, not a repository-wide replacement or a change to historical fixtures. The concrete files and replacements are listed in [the implementation plan](implementation.md#entry-and-context).

## Handoff content

`handoff.md` is readable Markdown with a compact outline, not a full transcript or a machine-validated schema. Omit empty sections and repetitive boilerplate. Preserve the information needed to make the next decision; do not impose an arbitrary word count that discards necessary context.

| Content | Purpose |
| --- | --- |
| Identity | Task/topic, creation time, repository identity when applicable, branch/worktree and relevant revision if known. Local paths are identified as source-machine paths. |
| Objective and constraints | User intent, corrections, accepted scope and relevant operating constraints. |
| Decisions and rationale | Chosen approaches, reasons, and abandoned approaches that would otherwise be repeated. Distinguish user decisions from agent proposals. |
| Progress and evidence | Completed and pending work; meaningful file references; attributed verification results; explicit uncertainty. A remembered successful test is not a newly executed test. |
| Continuation | Blockers, open questions and the next useful action, including dependencies on unavailable information. |
| Supporting references | Relevant project documents, issues and eligible Capy references, each explaining what additional information it supplies. |

The skill uses the conversation it actually has. If earlier context has been compacted away, it states the resulting gap rather than claiming complete transcript coverage. It does not run tests, perform a review, finish implementation, scan unrelated worktrees or collect every project file to create the handoff.

Prefer repository-relative paths and known repository/revision identifiers for portable references. Uncommitted changes are described as local and are not assumed to exist on the destination machine. Publishing a handoff does not transfer a worktree, patches, credentials or a Capy database. Essential context must remain understandable when an optional reference cannot be opened. Do not include credentials or unrelated conversation content in the uploaded files.

`prompt.md` contains a short instruction addressed to the receiving agent, the actual gist URL, the exact `handoff.md` filename and the intended continuation. It asks the recipient to read the handoff and reconcile relevant current state before continuing. It does not replay every decision, silently select another handoff or treat the source agent's observations as current verification.

## Outgoing content

Before each upload, read the outgoing local content and omit or redact credentials, authentication tokens, credential-bearing connection strings and unrelated private information. This applies to `handoff.md` and the gist description before creation, and to the completed `prompt.md` before its file-add operation. Preserve useful task context; a task-relevant hostname is not automatically a credential. If a safe, useful payload cannot be prepared, stop before uploading that payload and explain the specific problem without echoing the secret.

This is a small content-preparation step, not a new scanner dependency, approval workflow or post-publication inspection. An evaluation with a nonfunctional fixture credential presented in credential-bearing context checks that the exclusion is applied; it does not establish comprehensive secret-detection guarantees.

## Capy references and the indexing prohibition

Eligibility comes from evidence already available to the source conversation: for example, a successful earlier indexing result, a previously retrieved indexed source, or a confirmed earlier session archive. Capy being installed, a familiar source label, or knowledge of the current session ID is insufficient. An earlier unrelated indexing event does not make a new or unrelated source eligible.

For an eligible reference, retain the known source label or session identifier, project scope when relevant, a focused query or retrieval instruction, and a sentence explaining why to follow it. A knowledge reference can direct the recipient to an already indexed `kk:arch-decisions` source for a particular decision. A transcript reference can identify a previously archived session. A session ID without evidence of archival must not be presented as a retrievable transcript.

The producer reuses existing reference information; it does not search Capy merely to populate an optional section. If prior indexing cannot be established, omit Capy references and continue with the self-contained summary. If an eligible source may be inaccessible from the destination, say so without attempting to copy or recreate it.

The prohibition includes direct indexing, fetch-and-index tools, vault import/reindex/archive operations, and delegating those actions to another skill, agent or the starter prompt. Creating a handoff never repairs a missing source by indexing it. Do not load the shared Capy protocol wholesale into this skill: its indexing conventions are unnecessary here and could contradict this boundary. Express the small reference convention directly in the skill.

This boundary applies to actions initiated by `/kk:handoff`; it does not claim to disable independently configured host transcript storage or hooks.

## Gist storage and publication

GitHub supports multiple files per gist. Secret gists are omitted from public discovery but remain accessible to anyone with the URL. The selected interface is the existing `gh` CLI. No SDK, direct HTTP publishing client or new package dependency is needed. See [GitHub visibility](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists) and [gist creation](https://cli.github.com/manual/gh_gist_create).

Use a descriptive gist title containing the project/topic and creation time. A unique temporary directory avoids collisions between simultaneous invocations; the gist ID distinguishes remote snapshots. Within each gist, the filenames remain exactly `prompt.md` and `handoff.md`.

The starter prompt needs the gist URL, which is returned by creation. Use this small ordered sequence:

1. Prepare `handoff.md`, the gist description and the starter-prompt wording locally. Apply the outgoing-content check before publication.
2. Create a secret gist containing `handoff.md`, without the public flag. Retain the returned URL immediately.
3. Complete `prompt.md` with that URL, apply the outgoing-content check to the finished prompt, and add it to the same gist using the CLI's noninteractive file-add operation.
4. When both publishing commands succeed, return the gist URL and starter prompt. Their success responses are sufficient; do not inspect the remote gist afterward.

The second write uses the documented [file-add operation](https://cli.github.com/manual/gh_gist_edit) so the saved starter prompt can contain the real URL. No `gh gist view`, metadata request or other read-after-write step is part of the producer workflow.

Keep local preparation files until the publishing commands finish. After success, remove only this invocation's temporary files; after publication failure, preserve them and report their paths for recovery. If local cleanup fails, report the remaining paths separately; successful publication stays successful and must not be retried. Do not create a persistent local handoff registry. The gist is the completed artifact; local preparation files are not the earlier local-state storage design.

## Failure behavior

| Condition | Required outcome |
| --- | --- |
| GitHub CLI, authentication, network access or a host permission is unavailable | Explain the concrete failure. Preserve any prepared content outside the repository; do not claim a gist exists or silently switch storage products. |
| Creation succeeds but adding the prompt fails or has an uncertain outcome | Report the partial or uncertain state, the known gist URL and local files. Stop rather than inspect the remote gist or create another gist as automatic recovery. |
| Creation may have succeeded but the response was lost | Report the uncertain outcome and retain the local content. Do not blindly repeat creation and produce duplicates. Resolving an unknown gist is a follow-up, not automatic discovery. |

These are ordinary failure reports, not a new recovery daemon or retry framework.

## Architecture and repository integration

The canonical implementation belongs at `klaude-plugin/skills/handoff/SKILL.md`, with its Codex invocation policy in `agents/openai.yaml` and representative scenarios under `evals/`. The skill needs no agent definition, command wrapper, hook, shared storage helper or new profile. A test-only GitHub CLI substitute supports evaluation without becoming a runtime helper. `skill-md` was confirmed during design; the installed profile contributes no design-phase content.

`scripts/kodex-generate-manifest.yml` already includes all skills. Run the existing generator to produce the Codex variant; never edit generated copies directly. Add the skill to the structure-test registry and user-facing skill documentation. Shipped skill prose must be self-contained and must not reference these toolbox design documents.

## Assumptions

- A source session can use an authenticated GitHub CLI with permission to create gists. Failure to meet this condition is reported; the skill does not install or authenticate the CLI itself.
- The destination can retrieve a supplied gist URL using its available tools or the user can provide the files. This is a user-driven transfer, not automatic session discovery.
- The source conversation contains enough relevant intent to produce a useful summary. Material omissions are reported when this assumption fails.
- Anyone-with-the-link access is acceptable for the handoff content in v1. This acceptance does not make secret gists access-controlled or authorize inclusion of credentials.
- Existing Capy references may be local to one machine or project. They are optional and cannot be prerequisites for understanding the basic continuation.
- Instruction-based file handling is sufficient for this small workflow. A helper should only be reconsidered if observed failures establish a concrete need.

## Not Doing

- Session-end or compaction hooks, background capture, automatic loading and discovery: explicitly removed from the first iteration.
- Post-publication inspection or verification: successful publishing commands are the accepted completion signal.
- Indexing or archiving any material during handoff: explicitly prohibited, including indirect calls and missing-source repair.
- Whole-conversation exports: the deliverable is active-task context with relevant history.
- Access-controlled private storage or encryption: the user accepted secret gist visibility for v1.
- A local handoff store, latest pointer, retention scheduler or cleanup command: snapshots live in separate gists and are manually managed.
- Worktree transfer, automatic code changes, testing, staging or committing: generating context is the entire producer task.
- A separate resume skill, helper program, override language or argument parser: ordinary prompts and existing tools cover the accepted workflow.

These are scope exclusions, not promises of later implementation.

## Rejected Alternatives

| Alternative | Why it was not selected |
| --- | --- |
| A single-file gist created in one write | Retaining both `prompt.md` and `handoff.md` keeps a ready-to-paste starter prompt recoverable from the gist independently of the source chat. Embedding its real gist URL costs a second write and the corresponding partial-publication case; that bounded trade-off is accepted. |
| Bundled storage helper | More deterministic file handling does not yet justify a script and its maintenance. |
| Retained files under `~/.local/state/kk/handoffs/` | Initially accepted, then superseded by the user's portability requirement. |
| A single repository `handoff.md` | Risks mixing concurrent sessions and makes local conversation state part of the worktree. |
| Lifecycle hooks and automatic discovery | The user identified them as brittle and unnecessary for v1. |
| A private repository for handoffs | Offers different access controls, but the user accepted anyone-with-the-link access and chose gists. |

## Acceptance and evidence limits

The meaningful checks are a faithful active-task summary, correct submission of both files through secret-gist publishing commands, a usable prompt, preservation of concurrent snapshots and the working repository, accurate failure reporting, and zero handoff-initiated indexing or archival. Successful `gh` writes are sufficient for the agent to report publication; evaluations must not require a remote read-back or treat its absence as incomplete work. Test the absence of Capy references when tools are present but prior indexing is not evidenced, as well as inclusion of useful references when it is.

Use representative semantic evaluations and the existing generation/structure/link checks. Verify both hosts' invocation metadata and observe explicit invocation alongside a benign implicit-selection control. Seed producer context through actual prior turns and controlled tool results, and use a test-only `gh` substitute to record upload payloads and return scripted outcomes.

One bounded fresh-session exercise uses the successful producer's actual artifacts with a changed destination repository to check continuation readiness. This evaluates the output's usefulness; it adds no receiver code, retrieval policy or publication gate to the producer. The receiving session's retrieval method is not graded as a contract of this skill.

Do not grade exact prose, optional headings or arbitrary output length. A demonstrated producer indexing attempt, credential-bearing upload, implicit publication, public publication, fabricated reference, repository mutation or false success is a material failure. Lack of a live GitHub or provider run limits the verification claim; it is not proof that the instruction workflow works or fails. The bounded scenario plan is in [implementation.md](implementation.md#verification).

External behavior was checked against official GitHub documentation and local GitHub CLI 2.103.3 help during design on 2026-10-28. No live gist was created. This is a proposed implementation, not runtime verification.
