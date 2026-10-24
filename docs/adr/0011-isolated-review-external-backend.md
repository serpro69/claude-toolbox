# ADR 0011: External Review Backend for Isolated Reviews

## Status

Accepted (design confirmed 2026-10-11; corrections authorized 2026-10-21 and
2026-10-24 during implementation of
[clink isolated reviews](../feat/done/clink-isolated-reviews/design.md)).

## Context

`/kk:review-code:isolated` and `/kk:review-design:isolated` paired one internal
reviewer sub-agent with one external review through PAL's `codereview` tool.
That tool needs an API-backed model. Operators who run PAL provider-free (no API
key, only installed CLIs such as Claude Code, Codex and Antigravity) lost
external coverage entirely, although PAL's `clink` tool could drive those CLIs.

PAL returns no model-provider identity for CLI clients: `cli_name` echoes the
client, not the vendor behind it. Independence from the authoring provider
therefore cannot be read from discovery alone. Requiring every consumer
repository to declare the vendor of PAL's shipped clients proved to be opt-in
ceremony for the common case.

## Decision

1. **One backend decision per review, at discovery.** Before any external call,
   the skill inspects PAL's advertised tools and calls `listmodels`. An eligible
   API model keeps the existing `codereview` flow; otherwise, with `clink`
   available and CLI metadata present, the skill builds a CLI roster; failed or
   ambiguous discovery yields no external review. The decision is frozen: an
   API runtime failure never switches to clink. Runtime fallback was rejected
   because it multiplies branches and recovery state in the main agent.
2. **Every eligible non-authoring provider, configured models.** The roster is
   every discovered client with a found executable, minus the authoring
   provider, one client per provider, each attempted exactly once with no retry
   or substitute. The skill never names a model; PAL and the CLI configuration
   own model selection.
3. **Provider identity by declaration, then shipped defaults.** An operator
   declaration (request, project `CLAUDE.md`/`AGENTS.md`, identified client
   configuration) always wins. A configured or returned model that shows another vendor for a shipped
   name is recorded as *observed* and overrides the default. Without either, PAL's shipped client names map to
   their vendor (`claude` → Anthropic, `codex` → OpenAI, `agy` → Google) and the
   report labels the source as *assumed from shipped manifest*. Custom names are
   never guessed; one focused question covers every unresolved item before
   dispatch. `gemini` is retired and never a candidate.
4. **Contract verified before authoring.** A dedicated Task 0 verified the PAL
   contract (discovery states, roles, no-edit controls, continuation, failure
   semantics, receipt reporting) against a specific PAL revision before any
   plugin instruction was written. The minimum PAL revision is
   `c73dab7d8cf9d791961b84614a0e082b74ee5569`.
5. **Honest coverage over telemetry.** `allow_edits=false` plus a no-edit prompt
   is a behavior contract, not an enforced sandbox. Receipt counts only with
   observable read evidence; findings from clients that return none are kept
   with receipt unverified and cannot corroborate. Missing telemetry limits the
   claim and is not a prerequisite.

The operative plugin files are `klaude-plugin/skills/_shared/external-review-invocation.md`
(discovery, roster, request contract, reviewer record, aggregation),
`klaude-plugin/skills/_shared/design-review-criteria.md` (shared document
criteria for the internal and external design reviewers), and the two
`review-isolated.md` workflows that consume them. The existing
`pal-codereview-invocation.md` remains the API transport.

## Consequences

- Provider-free PAL installations regain external review; reviewer count and
  cost now vary with the roster (two CLI reviews for a Claude-authored change
  with the three shipped clients).
- Operators must grant each CLI read access outside the project root (plugin
  installation and OS temp directory) or accept reduced coverage; the plugin
  never bypasses permissions. The plugin README documents the verified setups.
- A wrong shipped default weakens, rather than breaks, the independence claim,
  and the report makes it visible; a declaration restores certainty.
- Corroboration is rarely reachable on the clink path: only Claude returns read
  traces, and for an Anthropic-authored change the `claude` client is excluded,
  so with the shipped clients external findings stay attributed but
  uncorroborated. The internal reviewer supports a finding through its
  source-tied report and can corroborate only with an external reviewer that
  returned receipt.
- Review policy stays in the plugin and execution in PAL: no toolbox CLI
  registry, launcher, model catalog or orchestration service was added, and
  older PAL builds are unsupported rather than shimmed.
