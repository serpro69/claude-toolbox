# Loading evidence — 2026-10-13

All four declared loading processes completed with exit 0 before measurement.
The controller verified capture seals, model/role linkage, root identity and
successful returned instruction bytes. Details: [Claude audit](binding-claude-audit.json)
and [Codex audit](binding-codex-audit.json). [Independent evidence review](binding-review.md)
approves opening the declared measurement; behavioral acceptance remains pending.

| Provider/side | Captured receipt | Limits and observations |
| --- | --- | --- |
| Claude baseline | Skill delivery, three required main methodology files, named child entry point; Opus 5.5 parent/child; selected hook root | Pre-feature baseline does not contain candidate common-method/context files. No subject read or mutation. |
| Claude candidate | Skill delivery plus 20 successful source reads across parent/child; shared method/context complete; Opus 5.5 | Bootstrap wrote packets in `/tmp`, then parent used complete direct-read fallback. Shared aliases are byte-identical. No subject mutation. |
| Codex baseline | Eight main/child required-source receipts; declared Astra parent and Sol code-reviewer child with parent linkage; catalog/generated role bytes verified | Child's lookup of a nonexistent plugin `agents/` directory failed; required source reads succeeded. Exact submitted handoff remains unverified. |
| Codex candidate | Six completely returned packet parts reconstruct all 15 original main sources; child reads complete common sources; declared role/model linkage | Packet framing was removed only after each returned part's exact bytes/hash matched. Only instruction-packet files were added to the probe workspace; original subjects are unchanged. |

Capy is connected/ready, PAL absent on both sides/providers. Codex's built-in
`codex_apps` service is also ready on both sides; no Apps tool call occurred.
This platform service is recorded rather than claiming that Capy was the sole
available Codex service. No evaluator-material access was observed in these
instruction-only calls; no OS-wide read confinement is claimed.

Temporary Codex trust, plugin registration and installed cache were removed on
both sides and verified absent. Probe workspaces and source snapshots remain
owned preparation artifacts, separate from all 48 freshly prepared measurement
workspaces. The baseline/candidate source and runtime freeze remains unchanged.
