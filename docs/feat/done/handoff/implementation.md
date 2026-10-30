# Implement the manual handoff skill

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: done; behavioral evidence and review closure recorded alongside this plan

## Starting point

Read [the accepted design](design.md) and the repository's [plugin development guide](../../../contributing/plugin-development.md). `klaude-plugin/` is canonical; `kodex-plugin/` is generated. The new skill is a single manual workflow implemented in instructions, using the source agent's file tools and existing GitHub CLI. It does not require changes to hooks, manifests, the generator, agent definitions or runtime dependencies.

The decisive additional constraint is [Capy eligibility and the indexing prohibition](design.md#capy-references-and-the-indexing-prohibition). Prior indexed material can be referenced; creation of any new Capy knowledge or archive is forbidden throughout handoff production. Do not inherit an indexing step from another workflow merely because it uses Capy.

## Files and responsibilities

| Path | Change |
| --- | --- |
| `klaude-plugin/skills/handoff/SKILL.md` | Add the trigger, boundaries, mandatory instruction-before-action order, content outline, publication steps and failure reporting. |
| `klaude-plugin/skills/handoff/agents/openai.yaml` | Add Codex's manual-only invocation policy; the existing generator copies this sidecar unchanged. |
| `klaude-plugin/skills/handoff/evals/README.md` | Describe bounded scenario execution, permitted fixture writes, synthetic GitHub responses and semantic grading. |
| `klaude-plugin/skills/handoff/evals/_support/gh` | Add a small executable, test-only GitHub CLI substitute using the Python standard library. No new general runner or production helper. |
| `klaude-plugin/skills/handoff/evals/<scenario>/` | Add `eval.json`, real `test-files/` fixtures and optional grader-only `oracle/` material for the cases below. |
| `test/test-plugin-structure.sh` | Register `handoff` and check the two invocation-policy fields in canonical and generated output; reuse existing discovery and structure checks. |
| `klaude-plugin/skills/implement/SKILL.md`, `klaude-plugin/skills/design/{SKILL.md,existing-task-process.md}`, `klaude-plugin/skills/clarify-docs/SKILL.md` | Make the small terminology changes specified below; preserve their workflows. |
| `docs/user-guide/skills.md` | Add the skill reference and explain explicit publication/loading, two files, unlisted access, optional existing Capy references and failure outcomes. |
| `README.md`, `klaude-plugin/README.md`, `docs/contributing/architecture.md` | Update the skill inventories/counts and short descriptions where applicable; keep the detailed workflow in the user guide. |
| `kodex-plugin/skills/handoff/` and any other generator outputs | Regenerate from canonical content with `make generate-kodex`; inspect rather than hand-edit. |

No change to `EXPECTED_COMMANDS` is needed: a skill is already invokable without a command wrapper. Do not add a shared reference or template merely to split a small file. If the actual instruction body becomes unwieldy, a directly linked local reference is acceptable, with the same instruction-loading rule.

## Implement the complete manual path

### Entry and context

Configure manual-only invocation first: `disable-model-invocation: true` in `SKILL.md`, and `policy.allow_implicit_invocation: false` in the canonical skill's `agents/openai.yaml`. Keep the description clear about the fresh-session use case and GitHub publication. A natural-language request alone must not cause implicit selection; the user explicitly invokes the skill. Follow the existing naming, description-budget and workflow-order conventions; re-check the linked upstream skill-description guidance when authoring or changing descriptions.

Apply these narrow terminology edits to live canonical instructions, then regenerate their Codex copies:

| Location | Replacement |
| --- | --- |
| `implement/SKILL.md`, Step 3.1 | “Refresh the handoff” → “Refresh the review context.” |
| `design/SKILL.md`, Workflow step 6 | “implementation handoff” → “implementation recommendation.” |
| `design/existing-task-process.md`, step 4 | Name the heading “Recommend next steps before implementation”; say “recommend `/kk:implement` when ready” and “stop before implementation” in the matching prose. |
| `clarify-docs/SKILL.md`, description | Say instruction-file targets receive a `/kk:implement` suggestion “without edits or invoking implementation.” |

Preserve behavior, skill names and workflow ordering. Do not rename historical fixture files, change frozen completed designs or remove ordinary uses of the word throughout the repository.

Place the mandatory-order directive at the beginning of Workflow. There should be one investigation entry point after all operative instructions load. The workflow identifies the active task and relevant earlier decisions, reads only useful evidence and prepares the record. It does not execute the recorded next action.

Include the content outline from the design without turning it into a rigid schema. Distinguish user decisions, proposals, observed state, remembered verification and unresolved gaps. Use source-machine path labels and repository-relative references where relevant; explicitly identify local uncommitted work that the gist does not transfer.

Step → verify: a scenario with a superseded proposal, an unrelated earlier topic, a remembered test result and unfinished work yields a faithful active-task handoff with an actionable continuation and no new test execution or repository changes.

Step → verify: structure checks read both manual-only fields from canonical and generated output. Run the explicit success case and the implicit-selection control through normal host loading with that metadata; injecting the skill body or advertising an implicitly selectable description would not test the policy.

### Existing Capy material

Make the eligibility decision from evidence already present in the conversation. Successful prior indexing, an already retrieved indexed source, or confirmed archival can establish that the specific relevant material exists. Tool availability and a bare session ID cannot. Omit the optional references when that evidence is absent.

For eligible material, record a useful source label/session identifier and retrieval query or instruction, explaining when it would help. Do not expand eligibility from an unrelated earlier index operation. Do not add a discovery search, index operation, fetch-and-index call, vault import/reindex, or delegated indexing as a convenience. The starter prompt must not ask the receiver to create missing sources.

Do not link the general Capy knowledge protocol into this workflow; express this small, read-only reference convention locally so its indexing guidance cannot become a runtime step.

Step → verify: evaluate both tool-available/no-prior-indexing and relevant-prior-indexing inputs. Inspect the full tool trace, handoff and starter prompt for indexing attempts, fabricated references and indirect indexing instructions. A previously indexed but inaccessible source remains optional; the summary still carries essential context.

### Publish and return the handoff

Use a uniquely allocated temporary directory outside the working repository, with file bodies written through native file tools. Keep file content out of shell interpolation. No new persistent local store or storage helper is part of this implementation.

The publishing CLI surface is `gh gist create` and `gh gist edit --add`. Local CLI 2.103.3 help matched the current manual during design. This is an observed version, not a new package pin or a proven minimum version. Re-check the installed CLI interface if it differs; do not install or upgrade it as part of a handoff.

Prepare `handoff.md`, the description and prompt wording. Before each file or description is uploaded, read that outgoing content and omit or redact credentials/authentication material and unrelated private content, following [Outgoing content](design.md#outgoing-content). If that cannot be done while retaining a useful payload, stop before sending it and explain the problem without repeating the credential. Do not add a scanner dependency or routine confirmation prompt.

Create the secret gist without `--public`, retain the returned URL, finish `prompt.md` with that real URL, apply the content check to the finished prompt and add it to the same gist. A filename or local directory name never substitutes for the returned remote identifier. Use the file-add operation noninteractively, without opening an editor.

When both publishing commands report success, return the URL and ready-to-paste prompt. Do not follow successful writes with `gh gist view`, a metadata/API read, a download or another publication check. The agent uses the CLI outcome as its completion signal.

After successful publication, remove only this invocation's temporary preparation files. A local cleanup failure is reported separately with remaining paths; it does not change the publication result or justify another upload. On a failed or uncertain publishing command, keep the preparation files and report their absolute paths and any known gist URL. Stop without remote inspection or automatic retries. Do not silently publish publicly, replace an older gist, edit GitHub authentication, delete a partial gist or fall back to writing inside the repository.

Step → verify: inspect the evaluation's submitted payloads and tool trace: the agent submits both files through secret-gist publishing commands, returns the URL-bearing prompt after successful command responses and leaves a pre-existing handoff and the working repository unchanged. It performs no post-publication inspection. A failed prompt-add operation returns the partial URL and recovery files rather than a second gist or a success claim.

Step → verify: a nonfunctional fixture credential introduced in a prior turn as authentication material is absent from every uploaded file and gist description, while relevant non-secret task context remains. The evaluator knows it is synthetic; do not describe it to the actor as a harmless example that may be published. Credential names and redaction placeholders are acceptable. Inspect submitted bytes, not only a final state from which an earlier leak could have been removed.

### Registration, documentation and generation

Add the completed skill to `EXPECTED_SKILLS`. Update the user guide and inventory counts together so the shipped entry is discoverable and the upload effect is clear. Explain the manual consumption workflow, anyone-with-the-link access, optional Capy references and the absence of indexing. This documentation is sufficient for the scoped feature; it does not need a new cross-feature ADR.

Run `make generate-kodex` after canonical edits. The manifest's `include_all: true` already handles the new skill and its instruction transformations; `copyFile` leaves YAML unchanged. Check that the new generated directory and policy sidecar are present, prefixes are transformed, and manual-only invocation, publication and Capy boundaries survive unchanged. Inspect generated terminology changes as well. The target already runs generator tests and both structure suites; avoid rerunning the same checks without a reason.

Step → verify: generation succeeds, the skill is registered in both distributions, and `make plugin-graph` accepts the operative instruction links. The skill must not link back to this feature directory.

## Verification

### Representative scenarios

Use the repository's existing `eval.json` schema, one directory per case, with real fixtures under `test-files/`. Keep expected outputs, grading instructions and future replies in sibling `oracle/` material. Do not copy the large scenario matrix of an unrelated feature.

| Scenario | Consequential outcome |
| --- | --- |
| `active-task-handoff` | Actual prior turns contain multiple topics, a corrected decision and a nonfunctional fixture value presented as authentication material. Explicit invocation produces a focused handoff; the credential value is absent from every upload and description. Successful command responses lead directly to the URL and starter prompt, without remote inspection. Capy tools are advertised but no prior indexing is evidenced: no Capy references or indexing. A bare current session ID is not advertised as an archive. An existing handoff remains unchanged. |
| `prior-indexed-context` | Prior successful indexing/retrieval and a confirmed archive yield targeted, useful references. Unrelated indexed sources are omitted. Essential context remains in the handoff, and the trace and starter prompt contain no indexing or archival action. |
| `partial-publication` | Creation returns a URL but adding `prompt.md` fails or has an uncertain outcome. The agent reports the partial/uncertain state, retains local content and stops without remote inspection or automatic retries. |
| `unavailable-github` | A missing CLI, rejected authentication or denied publication is represented by one concrete configured failure. The agent names the failure and available local recovery content without a fabricated URL, credential changes or repository fallback. |
| `manual-only-invocation` | Under normal host discovery with the manual-only metadata, a request to refresh a review handoff follows ordinary review-context preparation without invoking `/kk:handoff` or publishing a gist. Use the ambiguous wording from the existing workflow as the control input; do not preload the new skill or expose it as implicitly selectable. Explicit activation is covered by the success case. |

### Conversation and GitHub setup

Use a manual multi-turn runbook for each scenario. Keep the ordered seed messages, configured tool outcomes and grading expectations in its evaluator-only `oracle/runbook.md`. Start a fresh actor session, deliver the scripted user turns one at a time and let ordinary actor replies and fixture reads become real conversation history. The success run establishes an initial approach, supplies a correction and a separate topic, and includes the fixture credential in an authentication context before the final explicit `/kk:handoff` invocation. Use only an invented, never-valid value; its lack of real privileges is evaluator setup information, not an instruction to the actor that it is safe to publish. For `prior-indexed-context`, an earlier user turn supplies a successful prior indexing/archive receipt and asks the actor to read the matching synthetic reference fixture through its ordinary file tools. This establishes the case's prior-source evidence without an indexing call or custom tool-response injection. Record every delivered turn and actual response. Do not give the actor a transcript file with an instruction to summarize it, and do not expose future replies or expected answers.

Stage project fixtures in a fresh workspace outside the plugin tree. Place the executable `evals/_support/gh` first on the PATH actually used by the actor's shell and confirm that lookup in the evaluation setup. Keep scenario configuration and expected outcomes evaluator-only; the executable itself must contain no answer oracle. Inspect the trace for accidental oracle exposure. Use an environment without real GitHub credentials or outbound GitHub access, and block Capy mutations if its tools are advertised. A rejected indexing attempt still fails the behavior assertion. A PATH stub by itself is not that isolation, and unsupported setup must be recorded as unavailable execution.

The stub supports the skill's selected `gh gist create` and `gh gist edit --add` calls, plus help/version probes. It logs arguments and snapshots every uploaded file and description before returning the configured result. Successful creation records a unique synthetic gist ID/URL and submitted visibility; adding a file updates that same simulated gist. Configure a deterministic file-add failure for `partial-publication` and one concrete publication failure for `unavailable-github`. Never fall through to the real CLI, silently correct a public flag or discard an unexpected call. Unknown commands fail visibly and remain in the trace. Producer runs need no remote-read interface.

For the fresh-session leg only, the same stub supports `gh gist view <id-or-url> --filename <name> --raw`, reading the saved uploaded bytes by exact synthetic gist ID and filename. It returns an error for an unknown gist or file. Enable this read in the consumer setup; producer read attempts remain visible as unexpected operations. This test-only mode needs no HTTP server or separate fixture endpoint. Check the stub's payload recording, configured failure and named-file read with direct fixture calls before evaluating agents. An otherwise legitimate CLI call outside the stub's implemented surface is a harness coverage limit to repair and rerun, not automatic evidence of a skill defect.

The stub and runbook are narrow test support, not a new multi-provider runner or a helper used by the shipped skill. Existing capture utilities may be reused where compatible, but the plan does not depend on building transport/history-injection infrastructure. Canonical and generated runs must load the appropriate files and invocation metadata through the tested host. Record unsupported host-policy testing as a coverage limit rather than replacing it with a skill-name classification question.

### Fresh-session usability exercise

Attach one consumer leg to the successful `active-task-handoff` run for each instruction variant. Start a fresh session without the source conversation and give it the actual generated starter prompt. Its available shell uses the same `gh` stub in consumer mode to serve the saved uploaded files, and ordinary file tools can read the destination repository. Keep real network-fetch tools unavailable in this isolated exercise, and tell the actor that GitHub CLI access is available without directing its exact command sequence. The production skill does not implement a downloader or prescribe the receiving host's tool choice. No real gist is fetched.

Provide a destination repository with a deliberate relevant difference from the source state, such as an uncommitted fix absent from the destination or a changed file invalidating a recorded test result. Add a test stop condition asking the receiving agent to assess current state and state the next action before making changes. Grade whether it can identify the objective and constraints, distinguish recorded evidence from current state, notice the relevant difference and give a justified next action without asking the user to reconstruct supplied context. Do not substitute an ideal hand-written handoff for the producer's output or grade a particular retrieval command.

This is implementation-time evidence of artifact usefulness. It adds no receiver implementation, producer download, post-publication inspection or permanent restriction on the receiving session's unrelated tools. The no-indexing requirement is graded against producer actions and generated instructions; do not revive withdrawn F1 as a consumer-routing gate.

### Execution and evidence

Before execution, state the fixture inputs, synthetic tool responses, permitted writes and decision criteria. Do not upload real session content to test the skill. A live synthetic-content smoke run is optional when explicitly authorized and available, and its evidence must be labeled separately from simulated runs.

The evaluator may inspect captured upload payloads and simulated state to grade the producer. This is test evidence, not an instruction for the producer to verify GitHub after publication. Do not restore the retired read-back requirement through an assertion or completion criterion.

Initially run the five producer scenarios against the canonical instructions and the generated instructions, with one fresh-session consumer leg attached to each variant's success case. Record the actual provider/model and instruction variant separately. Use the corresponding host when checking provider-specific invocation policy; canonical instructions on Codex do not certify Claude Code metadata behavior. One run per scenario/variant and one consumer leg per success case are bounded initial evidence, not a reliability estimate. A change driven by a failure should be compared with its immediate predecessor under the same conditions, retaining earlier traces. Broaden only for a named material uncertainty; do not require exact phrasing, a particular optional heading or repeated runs until one passes.

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
