# Runtime and instruction binding

All four fresh loading probes completed before measured sessions. The controller
validated retained source/cache manifests, generated Codex role bytes, selected
catalog identity, and sealed capture hashes. These are loading checks only.

| Provider / side | Evidence | Observed binding |
| --- | --- | --- |
| Claude baseline | [capture](preflight-upgraded/claude-binding-baseline/manifest.json) | Selected filtered c2d28c9e bundle; main messages and named reviewer result resolve `claude-opus-5-5`; successful instruction reads; exit 0. |
| Claude candidate | [capture](preflight-upgraded/claude-binding-candidate/manifest.json) | Selected filtered 581dd0e1 bundle; main messages and named reviewer result resolve `claude-opus-5-5`; instruction-packet/method reads; exit 0. |
| Codex baseline | [capture](binding-codex-baseline/manifest.json) | Only selected kk catalog, 206 filtered files and generated roles verified; linked code-reviewer thread uses `gpt-6.1-sol`/xhigh and successfully reads selected instructions; main `gpt-6-astra`; exit 0. |
| Codex candidate | [capture](binding-codex-candidate/manifest.json) | Only selected kk catalog, 212 filtered files and generated roles verified; linked code-reviewer thread uses `gpt-6.1-sol`; parent bootstrap and child methodology reads completed; main `gpt-6-astra`; exit 0. |

Codex parent/child identities are preserved in `thread-*.json`, `items-*.json`
and `subAgentActivity` records. Baseline child
`01a12a32-8591-7760-b129-e1dc0b060c7b` links to parent
`01a12a32-3d95-73d2-a75f-7fe90570cea7`; candidate child
`01a12a34-041e-78b2-8f69-69eb2f38fa27` links to parent
`01a12a33-b804-7ab0-b7b9-764682627a85`. Returned source contents, rather than the
parent's final report, provide read evidence. Exact submitted prompt parity
remains unverified under the existing revision-2 contract.

Temporary Codex plugin installations were uninstalled and owned project trust
restored to prior absence; see [baseline admin](admin/binding-codex-baseline/)
and [candidate admin](admin/binding-codex-candidate/). Both fresh
[knowledge-store probes](state-probe/summary.json) pass index/search and confirm
the other workspace's marker is absent; private vault access remains unavailable.

The original restricted-network attempt is incomplete. The original
network-enabled 2.1.272 attempt was sealed after the API rejected the CLI version.
Neither is reused as a measured session. Claude 2.1.296 enabled the successful
fresh probes above. PAL remains unavailable/user-deferred.

One Capy extraction request was rejected by automatic approval review as a
potential export of private trace data to an unverified destination. Remaining
model/linkage/seal verification used local file reads only; no permission waiver
or Capy retry was used. This does not affect actor inputs or grading rules.
