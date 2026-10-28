# Implement the manual handoff skill

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: pending implementation

## Starting point

Read [the accepted design](design.md) and the repository's [plugin development guide](../../../contributing/plugin-development.md). `klaude-plugin/` is canonical; `kodex-plugin/` is generated. The new skill is a single manual workflow implemented in instructions, using the source agent's file tools and existing GitHub CLI. It does not require changes to hooks, manifests, the generator, agent definitions or runtime dependencies.

The decisive additional constraint is [Capy eligibility and the indexing prohibition](design.md#capy-references-and-the-indexing-prohibition). Prior indexed material can be referenced; creation of any new Capy knowledge or archive is forbidden throughout handoff production. Do not inherit an indexing step from another workflow merely because it uses Capy.

## Files and responsibilities

| Path | Change |
| --- | --- |
| `klaude-plugin/skills/handoff/SKILL.md` | Add the trigger, boundaries, mandatory instruction-before-action order, content outline, publication steps and failure reporting. |
| `klaude-plugin/skills/handoff/evals/README.md` | Describe bounded scenario execution, permitted fixture writes, synthetic GitHub responses and semantic grading. |
| `klaude-plugin/skills/handoff/evals/<scenario>/` | Add `eval.json`, real `test-files/` fixtures and optional grader-only `oracle/` material for the cases below. |
| `test/test-plugin-structure.sh` | Add `handoff` to `EXPECTED_SKILLS` after the skill exists; reuse existing discovery and generated-output checks. |
| `docs/user-guide/skills.md` | Add the skill reference and explain explicit publication/loading, two files, unlisted access, optional existing Capy references and failure outcomes. |
| `README.md`, `klaude-plugin/README.md`, `docs/contributing/architecture.md` | Update the skill inventories/counts and short descriptions where applicable; keep the detailed workflow in the user guide. |
| `kodex-plugin/skills/handoff/` and any other generator outputs | Regenerate from canonical content with `make generate-kodex`; inspect rather than hand-edit. |

No change to `EXPECTED_COMMANDS` is needed: a skill is already invokable without a command wrapper. Do not add a shared reference or template merely to split a small file. If the actual instruction body becomes unwieldy, a directly linked local reference is acceptable, with the same instruction-loading rule.

## Implement the complete manual path

### Entry and context

Create a trigger-first description for an explicit request to create a handoff for a fresh session. Make GitHub publication apparent in the description. A generic request to summarize a discussion or continue work must not trigger gist creation. Follow the existing naming, description-budget and workflow-order conventions; re-check the linked upstream skill-description guidance when authoring the new description.

Place the mandatory-order directive at the beginning of Workflow. There should be one investigation entry point after all operative instructions load. The workflow identifies the active task and relevant earlier decisions, reads only useful evidence and prepares the record. It does not execute the recorded next action.

Include the content outline from the design without turning it into a rigid schema. Distinguish user decisions, proposals, observed state, remembered verification and unresolved gaps. Use source-machine path labels and repository-relative references where relevant; explicitly identify local uncommitted work that the gist does not transfer.

Step → verify: a scenario with a superseded proposal, an unrelated earlier topic, a remembered test result and unfinished work yields a faithful active-task handoff with an actionable continuation and no new test execution or repository changes.

### Existing Capy material

Make the eligibility decision from evidence already present in the conversation. Successful prior indexing, an already retrieved indexed source, or confirmed archival can establish that the specific relevant material exists. Tool availability and a bare session ID cannot. Omit the optional references when that evidence is absent.

For eligible material, record a useful source label/session identifier and retrieval query or instruction, explaining when it would help. Do not expand eligibility from an unrelated earlier index operation. Do not add a discovery search, index operation, fetch-and-index call, vault import/reindex, or delegated indexing as a convenience. The starter prompt must not ask the receiver to create missing sources.

Do not link the general Capy knowledge protocol into this workflow; express this small, read-only reference convention locally so its indexing guidance cannot become a runtime step.

Step → verify: evaluate both tool-available/no-prior-indexing and relevant-prior-indexing inputs. Inspect the full tool trace, handoff and starter prompt for indexing attempts, fabricated references and indirect indexing instructions. A previously indexed but inaccessible source remains optional; the summary still carries essential context.

### Publish and return the handoff

Use a uniquely allocated temporary directory outside the working repository, with file bodies written through native file tools. Keep file content out of shell interpolation. No new persistent local store or storage helper is part of this implementation.

The verified CLI surface is `gh gist create`, `gh gist edit --add`, `gh gist view --filename --raw`, and `gh api` for reading the known gist's metadata. Local CLI 2.103.3 help matched the current manual during design. This is an observed version, not a new package pin or a proven minimum version. Re-check the installed CLI interface if it differs; do not install or upgrade it as part of a handoff.

Prepare `handoff.md`, create the secret gist without `--public`, retain the returned URL, finish `prompt.md` with that real URL and add it to the same gist. A filename or local directory name never substitutes for the returned remote identifier. Use the file-add operation noninteractively, without opening an editor.

Read the final known gist and check its `public` value is false, the two named files exist, and the prompt names the correct gist and handoff file. If an API response is truncated, do not treat the truncated content as complete verification; use the returned raw-file location or report the limit. Return the URL and the ready-to-paste prompt only with an accurate completion state.

After successful verification, remove only this invocation's temporary preparation files. On failure, keep them and report their absolute paths. A partial gist stays identified by its known URL. A timeout with an unknown creation outcome is reported without blindly retrying creation. Do not silently publish publicly, replace an older gist, edit GitHub authentication, delete a partial gist or fall back to writing inside the repository.

Step → verify: a controlled GitHub interaction creates a fresh secret gist, adds the URL-bearing prompt, reads both files back and leaves a pre-existing handoff and the working repository unchanged. A failed prompt-add operation returns the partial URL and recovery files rather than a second gist or a success claim.

### Registration, documentation and generation

Add the completed skill to `EXPECTED_SKILLS`. Update the user guide and inventory counts together so the shipped entry is discoverable and the upload effect is clear. Explain the manual consumption workflow, anyone-with-the-link access, optional Capy references and the absence of indexing. This documentation is sufficient for the scoped feature; it does not need a new cross-feature ADR.

Run `make generate-kodex` after canonical edits. The manifest's `include_all: true` already handles the new skill and its instruction transformations. Check that the new generated directory is present, prefixes are transformed, and the publication and Capy boundaries survive unchanged. The target already runs generator tests and both structure suites; avoid rerunning the same checks without a reason.

Step → verify: generation succeeds, the skill is registered in both distributions, and `make plugin-graph` accepts the operative instruction links. The skill must not link back to this feature directory.

## Verification

### Representative scenarios

Use the repository's existing `eval.json` schema, one directory per case, with real fixtures under `test-files/`. Keep expected outputs, grading instructions and future replies in sibling `oracle/` material. Do not copy the large scenario matrix of an unrelated feature.

| Scenario | Consequential outcome |
| --- | --- |
| `active-task-handoff` | Multiple conversation threads and a corrected decision produce a focused, accurate handoff and a usable two-file secret gist. Capy tools are advertised but no prior indexing is evidenced: no Capy references or indexing. A bare current session ID is not advertised as an archive. An existing handoff remains unchanged. |
| `prior-indexed-context` | Prior successful indexing/retrieval and a confirmed archive yield targeted, useful references. Unrelated indexed sources are omitted. Essential context remains in the handoff, and the trace and starter prompt contain no indexing or archival action. |
| `partial-publication` | Creation returns a URL but adding `prompt.md` fails or has an uncertain outcome. The agent reports the partial/uncertain state, retains local content and does not create another gist. |
| `unavailable-github` | A missing CLI, rejected authentication or denied publication is represented by one concrete configured failure. The agent names the failure and available local recovery content without a fabricated URL, credential changes or repository fallback. |
| `summary-non-trigger` | A request for a conversational recap follows ordinary summarization behavior with no handoff publication or indexing. Expose competing normal skill descriptions so this tests selection rather than classification by name. |

Before execution, state the fixture inputs, synthetic tool responses, permitted writes and decision criteria. Use synthetic conversations and a controlled GitHub substitute; do not upload real session content to test the skill. A live synthetic-content smoke run is optional when explicitly authorized and available, and its evidence must be labeled separately from simulated runs.

Initially run the five scenarios against the canonical instructions and the generated instructions, recording the actual provider/model and instruction variant separately. Do not claim that canonical instructions tested on Codex establish Claude Code host behavior. One run per scenario/variant is an initial bounded sample, not a reliability estimate. A change driven by a failure should be compared with its immediate predecessor under the same conditions, retaining earlier traces. Broaden only for a named material uncertainty; do not require exact phrasing, a particular optional heading or repeated runs until one passes.

For each run retain the supplied input, instruction version, tool calls/results, local and simulated remote file state, final response, assertion results and limitations. Inspect attempted prohibited operations even if the execution environment rejected them. A sandboxed indexing attempt is still a failure of the indexing boundary. If tools or traces cannot be supplied, record execution as unavailable rather than claiming that authored fixtures are observed behavior.

### Repository checks

- `make generate-kodex`: generator tests plus canonical/generated structure checks.
- `make plugin-graph`: analyzer tests and operative broken-link/orphan validation. Preserve intentional broken eval-fixture links.
- `make docs-build`: the applicable strict docs gate after user-facing documentation changes; run through the configured captured execution path.
- Check generation freshness against the candidate's recorded generated outputs, including new files. Do not mistake legitimate uncommitted feature output for stale generation; compare a second generation to the candidate snapshot when necessary.
- Keep the existing release requirements in [the testing guide](../../../contributing/testing.md#validation-before-release) when a release is undertaken. This design task does not authorize a release.

Route routine builds and tests through the configured capture tools. Generation/structure checks cannot establish summary quality or absence of behavioral indexing; the scenario traces provide that evidence. Conversely, a good summary does not excuse a broken generated distribution.

### Completion

The final task invokes `/kk:test`, `/kk:document`, `/kk:review-code` with Markdown/agent-skill context, and `/kk:review-spec` for this feature. Record actual evidence and unresolved limits in `tasks.md`. Missing runtime evidence is not silently treated as a pass; assess whether the unobserved behavior is material to the acceptance decision. Preserve explicit repository gates.

No further production work is intentionally deferred inside v1. Automation, private access controls and the other items in [Not Doing](design.md#not-doing) are excluded scope, not pending tasks. If implementation discovers a material unresolved issue, record the specific problem, reason it remains open and concrete next action alongside the affected task.
