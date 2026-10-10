# Functional and operational review

Apply this common method after loading all instructions and resolved profile guidance. It complements SOLID, security and domain checklists on every change, including libraries, CLIs, infrastructure and agent instructions. Operational assessment applies where deployment, activation, persistence, startup, configuration or inter-component contracts are affected.

## Trace the affected behavior

1. Establish or reconstruct the record in [shared-change-context.md](shared-change-context.md). Locate and read the affected component's README or contract documentation before tracing behavior, when available. Record explicit outcomes, preserved invariants and delivery constraints with source locations; do not replace documented requirements with test expectations or invite a product decision already settled there. Label inferred intent when no contract exists. Use [shared-review-scope-protocol.md](shared-review-scope-protocol.md) to distinguish current work from genuinely pending functionality.
2. Describe relevant behavior before and after the change. Trace changed entry points/callers through meaningful dependencies to responses, side effects or durable state. Include unchanged consumers whose expectations may now fail. Read adjacent source to answer an identified contract/impact question; stop expanding once its contract and consequence are established, or name the uncovered boundary. A failed compound command does not establish source unavailability: retry permitted individual reads, while honoring explicit access denials; an isolated reviewer can request those reads through its parent. A file-count cap must not silently cut off a necessary trace.
3. Exercise that model with concrete success and boundary scenarios. Where applicable, include partial failure, retries, edits between attempts, cleanup and later reuse. Trace the documented scenario's actual state transitions through the unchanged consumer; a similar hypothetical sequence does not establish the documented failure/recovery path. For required transitions, cover the initial, relevant intermediate and final states against available fixtures; finding a failure in one state does not verify the others. Check which tests actually exercise the claimed contract and failure path. Green implementation-shaped tests or successful transport/status responses do not prove a successful business operation. Distinguish inspected source, executed tests and unverified assumptions; do not claim execution from source-only access.
4. Compare the approach with requirements and existing conventions. Challenge complexity by naming its cost and a simpler alternative preserving required behavior. Trace the proposed correction against documented invariants, including completed-operation/idempotent paths; retain necessary retry/recovery guarantees. Recommend work only for a demonstrated issue or specific uncovered requirement; do not duplicate existing test coverage. More abstraction is not inherently better; a hypothetical race is not automatically a new requirement.
5. Assess relevant compatibility combinations below, then apply profile expertise and substantiate findings. One issue spanning several lenses remains one finding.

Keep a compact scenario record as you trace: **contract/source → initial state → operation or transition → expected result → candidate result → evidence/limit**. Populate it from the actual requirements before deciding which paths are covered; a finding does not complete unrelated required rows. Carry the relevant rows into the report, including supported controls and intermediate states. Small changes may use one sentence. For instruction changes, consumers may be another skill, an agent payload, a generator or a parser.

## Compatibility and delivery

Identify combinations required by the actual delivery policy: for example, new consumer/old provider, old consumer/new provider, partly migrated data, disabled configuration, mixed versions or rollback. Select relevant combinations rather than an indiscriminate Cartesian product. Apply the shared context's historical-evidence rules when the decisive source is absent locally from the candidate.

Deployment, activation and migration are distinct operations. A flag supports safety only after checking all affected startup, read, write and consumer paths obey it. Pending tasks cannot excuse a broken current flow. Conversely, unreachable unfinished paths need not be implemented for an otherwise compatible increment to ship. A documented prerequisite does not satisfy an explicit independently-releasable-main requirement.

Assess the reviewed increment first. Expand to a production-to-candidate comparison only when a requested release assessment or relevant inherited change requires it and the baseline is available. Attribute inherited defects separately; distinguish introduced or worsened failures from pre-existing ones and supported reachability from hypothetical incidents. Bound any release conclusion when the full candidate cannot be assessed.

For each applicable dimension, state:

- **Supported:** named scenarios and a named baseline support compatibility within stated evidence limits.
- **Blocked:** demonstrated incompatibility or a known unmet delivery requirement prevents the stated release.
- **Unknown:** material baseline, environment, consumer or data evidence is missing; name it and the next action.
- **Not applicable:** no consequence for that dimension, with a reason.

Supported is not a production guarantee. Missing evidence is not an invented code defect. Preserve existing P0–P3 severity according to actual impact; do not create a separate severity taxonomy.

Reserve P0 for demonstrated critical consequences needing immediate mitigation. A scoped regression or recoverable wrong value does not establish catastrophic or irreversible loss. Hard acceptance violations still require changes when their impact merits P1 or P2.

## Verdict mapping

| Evidence | Code-review verdict | Release assessment |
| --- | --- | --- |
| In-scope incompatibility caused or worsened by the change | One impact-rated finding. REQUEST_CHANGES for P0/P1 or a violated hard acceptance/delivery requirement; otherwise COMMENT for an actionable nonblocking issue. | Blocked for the affected required combination. |
| Known external rollout prerequisite, no demonstrated code defect | Assess code on its merits; APPROVE may be scoped explicitly to code. | Blocked until the prerequisite is met; document the dependency. |
| Unknown evidence essential to task acceptance or an explicitly requested release conclusion | COMMENT absent a defect warranting REQUEST_CHANGES. Never unconditionally approve the unverified requirement. | Unknown; name missing evidence and next action. |
| Unknown operational detail outside the requested/required assessment | Does not automatically downgrade a supported, explicitly scoped code verdict. | Unknown for that unassessed environment. |
| Supported or Not applicable | Apply existing severity/finding rules; neither overrides another defect. | Retain named baseline and limits. |

Code approval with conditional release readiness cannot bypass a hard independent-delivery requirement. An unmet hard requirement stays open unless the user explicitly changes it or accepts an exception, recorded with rationale and prerequisites.

## Evidence-qualified reporting

Every report, including one with findings, identifies intent, actual scope/base/candidate, inspected paths and important evidence limits. Include a compact behavior/compatibility assessment with applicable conclusions. For each behavioral finding provide trigger, affected path, expected/actual result, consequence and correction; preserve confidence reasoning, severity and profile/checklist labels. Separate inherited findings and author-attributed inputs.

Before presenting, reconcile every claimed inspection or execution with successful returned tool results. Denied reads, unread source and truncated results belong under missing coverage. A supported finding does not establish that the full diff was inspected or tests ran; remove unsupported coverage claims, including copied template wording.

Record outstanding evidence or release/migration/activation prerequisites and next actions; name their durable tracking location when deferred. Preserve disagreement and uncertainty. Reviewer agreement never replaces source evidence. In isolated reporting, retain native external findings and annotations, disclose failures or zero/incomplete source coverage, and do not claim corroboration or broad safety from an underfed external result. Useful available findings remain reportable.
