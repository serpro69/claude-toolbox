# Codex automatic review extra policy diagnosis

On 2026-10-26, the external Claude review was rejected because the standing
authorization added in commit `6af5479a` was absent from the approval reviewer's
actual instructions. The configuration key is valid and loads correctly. The
selected `codex-auto-review` model supplied a policy template without the
`{{ extra_policy }}` placeholder, and Codex 0.164.0 silently omitted that text
while rendering the reviewer prompt.

This diagnoses the approval rejection in
[issue #184](https://github.com/serpro69/claude-toolbox/issues/184). The earlier
300-second Claude CLI timeouts are a separate, unresolved execution problem.

## Evidence

| Check | Result |
|---|---|
| Installed CLI and running app-server | Both 0.164.0 |
| Project trust | Toolbox is trusted |
| Fresh `config/read` with the project cwd | Loads all 1,167 characters of the scoped authorization from `.codex/config.toml`; origin is the project layer |
| Fresh `configRequirements/read` | No managed requirements; no managed extra-policy override observed |
| Actual rejected review | Model `codex-auto-review`; decision reports high risk, low user authorization and deny |
| Cached reviewer template | One `{{ tenant_policy_config }}` slot and zero `{{ extra_policy }}` slots |
| Saved instructions for that rejected review | Neither the authorization heading nor its complete text is present |
| Rendering comparison | The cached template with the catalog's main policy substituted is an **exact prefix** of the saved reviewer instructions |

The final captured model catalog was fetched at `2026-10-26T12:50:12.105484Z`
for client 0.164.0. An earlier catalog observation at 12:43:05 had the same
template hash. The template is 9,734 characters, SHA256
`f47fbb2bdba5e7528bfae7f5e2844a7d45a3a922fa74b718f22b22917376cfcf`.
The saved review instructions are 18,446 characters, SHA256
`f893abed23f18900cb5dd8fe34e2aa616634efcd1792ec38cd7241972dacfd8b`.

The decisive record is `guardian_review_feedback` entry
`01a1782a-c05c-7232-aee2-73aadcc1414a` in the local Codex state database,
for thread `01a17811-cf45-79f2-b6f2-f984b6560104`. Inspection used a read-only
SQLite connection and reported only identifiers, decision metadata, hashes and
presence/equality checks. Raw reviewer instructions and session history are not
copied into this repository or sent to an external reviewer.

## Why the valid setting had no effect

The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
defines `auto_review.extra_policy` as additional reviewer policy; a managed
`guardian_extra_policy`, when present, takes precedence. The versioned
[reviewer configuration builder](https://github.com/openai/codex/blob/rust-v0.164.0/codex-rs/core/src/guardian/reviewer_config.rs)
passes the resolved extra policy and selected model template into
`GuardianPolicyInstructions`.

The [0.164.0 renderer](https://github.com/openai/codex/blob/rust-v0.164.0/codex-rs/prompts/src/guardian_instructions.rs)
substitutes the two placeholders where they occur. It neither appends extra
policy when its placeholder is absent nor reports that omission. Consequently,
changing the wording of the project's `extra_policy` cannot affect this
template's rendered instructions. The approved-recipient exception was never
present as reviewer policy, so the denial is not evidence that the reviewer
ignored an instruction it had received.

The previous change verified configuration support but missed the final
rendered-prompt contract.

## Local repair and upstream follow-up

The local interim option is `auto_review.experimental_policy_template`, which
the [configuration schema](https://learn.chatgpt.com/docs/config-schema.json)
supports as a full template override. Preserve the complete current template
and insert `{{ extra_policy }}` immediately after its existing
`{{ tenant_policy_config }}` slot, retaining the project's current scoped
`extra_policy`. This changes where the configured authorization is rendered;
the remaining template and default main policy stay intact.

The user explicitly authorized applying this local repair on 2026-10-26.
`.codex/config.toml` now contains the full template override with exactly the
20-character insertion. Removing that insertion reproduces the original
template byte-for-byte. All other parsed configuration, including the existing
scoped authorization, equals the pre-fix configuration. Rendering includes
both the complete default main policy and the complete project authorization
with no unresolved policy placeholders.

A fresh app-server `config/read` loads the 9,754-character repaired template
from the project layer, SHA256
`37441097e4e825e0b195c32c985817ea07da15bb5c20fa753d87b22e2fe47e73`.
`auto_review.policy` remains unset. `test/test-codex-structure.sh` passes
16 cases / 29 assertions; whitespace checks pass. The temporary native-test
routing exception was removed and `.capy.toml` restored byte-for-byte.

This verifies configuration loading and prompt composition, not an actual
external approval after starting a new session. Start a fresh session to use
the override, then verify its reviewer instructions before claiming the export
is automatically authorized. The override pins the full template; owner
unassigned: remove it once the catalog/renderer fix is verified.

An existing upstream report,
[openai/codex#50309](https://github.com/openai/codex/issues/50309), describes
the exact failure on 0.160.0. The requested upstream submission was published
as a [0.164.0 confirmation with actual-review evidence](https://github.com/openai/codex/issues/50309#issuecomment-6417174286)
on 2026-10-26. The published body was read back and matches the reviewed draft.
The public payload contains version/platform facts, placeholder counts, the
template digest and verification outcomes; no raw reviewer prompts, private
source, account data or session identifiers.

Independent `code-reviewer` review approved the configuration repair and
report with no P0–P3 findings or outstanding evidence requests. It inspected
the prior/current configs, complete catalog template, sanitized verification,
public draft, and versioned upstream config-to-renderer path. The reviewer ran
no tests; execution results above are author-attributed. External Claude review
was not retried after the earlier rejection. No systemic findings or new
undocumented conventions required indexing. Changes remain uncommitted.

Owner: unassigned, upstream Codex/model-template integration. The correction
belongs in the supplied review template and renderer: include the extra-policy
slot and make a nonempty configured policy impossible to omit silently. A
regression should exercise a catalog-supplied template missing the slot and
verify either explicit failure or inclusion of the policy while preserving the
existing base policy. Verify the resulting actual reviewer instructions before
claiming the external-review authorization works.

During the original diagnosis, no approval configuration or managed policy was
edited, no model cache was manually replaced, and no running server was
restarted. The subsequent user-authorized repair above changes only the local
template override. The rejected export was not retried. Explicit
authorization remains necessary before any otherwise-blocked export; this
finding itself is not an approval override. The live control-socket
configuration query timed out, so the configuration-layer observations above
come from a fresh read-only app-server query. The saved review record provides
the direct evidence of what the failing reviewer actually received.

Local diagnostic scripts and sanitized output are retained at
`/private/tmp/kk-auto-review-diagnosis-20261026/`, including
`inspect_config.py` and `check_rendering.py`.
