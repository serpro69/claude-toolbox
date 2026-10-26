# ADR 0012: Single Declaration for the Permission Guard

## Status

Accepted, 2026-10-26. Records the implemented permission-guard decision;
feature release verification and the measured performance shortfall remain open.
Partially supersedes [ADR 0005](0005-codex-hook-enforcement-gap.md).

## Context

The original permission settings and shell hook mixed three concerns: secrets,
context noise, and project-specific data. The substring-based shell hook
rejected benign paths and prose, while native file-tool rules alone could not
protect shell reads. Multiple hand-maintained lists could disagree.

Template sync union-merged deny arrays. Commit `e0036b2a2bc74566601107b56ecf0552111397f8`
removed upstream restrictions on logs and `node_modules`, but an additive merge
kept those restrictions in downstream projects. Removing an upstream rule was
therefore insufficient to deliver the intended behavior.

The audience is developers operating their own repositories. A cloned project
may add restrictions; the machine owner needs scoped exceptions for workflows
such as infrastructure administration. Secrets must not become an exception
category. Plugin-only Claude installs also need a baseline: they receive no
template `permissions` settings.

The approved feature design and per-task decisions are recorded in
`docs/feat/wip/permission-guard/design.md` and `tasks.md`. This ADR preserves
those choices; runtime observations qualify them rather than confer acceptance.
Task 9's live checks verified Claude bypass denial and Codex relative patch
resolution with explicit hooks, while exposing a performance shortfall and a
project-hook discovery evidence gap.

## Decision

Keep one canonical declaration at
`klaude-plugin/scripts/guard/guard-rules.json`. It defines secrets globs,
destructive categories/rules, temporary roots and self-modification paths.
`scripts/generate-guard.sh` renders:

- `.claude/settings.json`'s `permissions.deny`, as native secrets `Read(...)` rules;
- `.codex/rules/default.rules`, containing only unconditional literal forbids;
- `.codex/scripts/guard/`, as byte-identical engine/wrapper/declaration/license copies;
- the marked rules tables in `docs/user-guide/configuration.md`.

The runtime wrapper `klaude-plugin/scripts/guard/guard.sh` invokes `guard.py`
under isolated Python. It preserves payload bytes and validates engine output.
Denial uses JSON, a stderr reason and exit 2; interpreter failures, crashes and
malformed output also deny. Claude's registration in
`klaude-plugin/hooks/hooks.json` adds `onFailure: "block"` and a 15-second
timeout. That declaration requires Claude Code 2.1.295+; runtime prerequisites
are Bash, `jq` and Python 3.8+.

The engine serves Claude's file tools and Bash, intercepted Codex patch
headers, and capy's three execution tools. Codex's `pretooluse-bash.sh`,
`pretooluse-patch.sh` and `pretooluse-mcp.sh` adapters export the repository root
and delegate to the shared copy. Project-root policy and execution cwd remain
distinct. Capy's own hook registrations and routing responsibilities are
preserved; guard checks run independently of routing handoff.

Project `.claude/kk-guard.json` only adds restrictions and is excluded from
template sync. User `~/.claude/kk-guard.json` may disable destructive
categories, exempt individual simple commands, or enable `disable_selfmod`.
The user scope combines `*` with the single longest matching physical
project-path prefix. Neither layer removes secrets. Invalid optional
configuration is reported without weakening the baseline.

Destructive decisions are flat denies in every permission mode. The hook
exempts literal `rm` targets beneath temporary roots when no secrets or
protected configuration are affected. Generated Codex native forbids are
limited to `rm`, `shred`, `sudo`, `su` and `doas`: most-restrictive-wins native
rules would otherwise make user exceptions for `git` and `infra` ineffective.
These five native forbids still outrank the hook's temp exemption and user
exceptions on Codex.

Template sync replaces `permissions.deny` from upstream, reports removed
entries and keeps `permissions.allow` union-merged. Projects add guard policy
in their own config; those requiring independent native settings can use
`sync_exclusions`. Generated freshness and structure checks enforce the
declaration/projection relationship.

## Consequences

Policy maintenance has one source and generated projections. Plugin-only
Claude installs receive the runtime baseline without additional files. Ordinary
logs, dependencies, build output and `.env.example` are allowed by that
baseline. Context reduction belongs to the harness/capy; project-data
restrictions belong to project configuration.

Plugin updates and template sync remain separate delivery channels. Updating
the plugin first leaves old extra settings denies until sync; syncing first
leaves the old shell hook until the plugin updates. Full new coverage requires
both channels. Neither generated metadata nor a passing payload test establishes
that an installed harness loaded its hooks.

Accepted costs and limits:

- With Claude hooks disabled, template users retain the native secrets baseline
  but lose destructive and self-modification protection. The former settings
  `Bash(rm:*)` deny is intentionally removed so the hook can support temp cleanup
  and user category exceptions. Plugin-only users have no native fallback.
- Settings edits, including adding allow entries, are self-modifications. Agent
  maintenance of this repository requires a user-scoped `disable_selfmod` entry.
- No working Python means matched calls, including reads, block until repaired.
- Codex native reads remain advisory in this integration; specialized paths can
  bypass hooks. Native forbids also prevent the five listed commands from being
  loosened through guard configuration. See the [parity table](../providers/codex.md#permission-guard).
- Static inspection cannot cover every dynamically assembled interpreter path,
  search-result contents, or unregistered execution channel. A new channel needs
  a payload mapping and registration before it has guard coverage.
- The macOS Task 9 measurement missed the 30/50 ms targets and the 60 ms Read
  gate. Performance acceptance remains open; the user's acceptance of recording
  the measurements did not waive that requirement. Ordinary Codex project-hook
  discovery also remains unverified in that probe setup.

Rejected alternatives were a hand-maintained sync retirement list, asking every
consumer to remove stale settings manually, a pure Bash matcher, three lists
kept in sync only by tests, and project-level loosening. A read-tool fast path
was rejected because plugin-only installations would lose their only protection.
Blanket Codex native forbids were rejected because they defeat user exceptions.
Mode-aware ask decisions were deferred in favor of predictable flat denial.

Revisit flat denial if its friction outweighs its value; `permission_mode`
could then select a supervised ask policy. Revisit native read enforcement
when the supported Codex integration provides an enforceable mapping or
filesystem profile. Resolve performance with measurements or an explicit
acceptance change before feature completion. User controls and current limits
are documented in [Guard Configuration](../user-guide/configuration.md#guard-configuration).
