## External review invocation

Shared procedure for the isolated review workflows. It decides **once per review invocation** which external backend supplies independent review, builds the clink reviewer roster when the API path is unavailable, and keeps a uniform record of every external reviewer's outcome.

Ownership stays split. The caller owns scope, instruction loading, evidence preparation, the internal reviewer, annotation and the final verdict. This protocol owns the backend decision and reviewer bookkeeping. PAL owns executable resolution, configured CLI arguments and models, subprocess behavior and conversation storage. The already-loaded PAL codereview protocol remains the API transport; nothing here repeats its two-step call sequence.

### Discovery — once, before any external dispatch

Run discovery after every instruction and the evidence manifest are ready, and before the first external call. It needs no source investigation and must not be repeated later in the same invocation.

1. Inspect the advertised PAL tool surface: is `codereview` callable? Is `clink` callable?
2. Call `listmodels` once. Read the API model catalog and the `cli_clients` metadata (each entry names a configured client, whether its executable was found, and `authentication: "unverified"`; `cli_clients_observed_at: "startup"` marks the observation time). Review roles come from the advertised `clink` schema, not from this metadata. Do not inspect API secrets, probe logins or infer availability from error text.

| Discovery outcome | External action |
| --- | --- |
| `codereview` callable and the catalog lists an eligible API model | API branch: the PAL codereview protocol with its existing model-selection policy. Zero clink calls. |
| API review unavailable (`codereview` not advertised, or the catalog has no eligible model) and `clink` callable with `cli_clients` metadata present | Build the clink roster below. |
| `listmodels` fails, returns a malformed or fatal catalog, or omits `cli_clients` when it would be needed | Discovery unresolved: disclose it, keep the internal reviewer, make no speculative clink call. Uncertainty is not an empty catalog. A PAL build that never exposes `cli_clients` outside provider-free mode does not satisfy this protocol. |
| API review unavailable and `clink` unavailable or the roster is empty | Internal review only, with an explicit external coverage limit. |

Freeze the decision for the whole invocation, including clarification and evidence follow-ups. Once API review starts, any step, continuation or model error is an API failure under that protocol's degradation rules: never re-run discovery, never switch to clink. A later separately requested review is a new invocation.

### Clink roster

1. **Candidates** are discovered clients whose executable was found. Executable presence does not prove login; authentication is attempted through the review request, not a separate probe. A `gemini` client is retired tooling and is never a candidate, even when PAL advertises it and even when a declaration names it; Google is served by `agy`. List an advertised `gemini` in the roster report as "retired, not a candidate".
2. **Authoring provider.** Resolve from explicit authorship or session context (who produced the reviewed change). The host CLI of a later review session is not evidence of authorship. If unknown, it becomes part of the single roster question in step 6.
3. **Provider identity.** PAL returns no model-provider identity for CLI clients: `cli_name` and `provider_used` echo the client, not the provider. Resolve each candidate's provider in this order and record the source:
   - **declared** — a mapping the operator declared in the request, in the project's agent instruction file (`CLAUDE.md` or `AGENTS.md`, the durable place to record it), or in client configuration the operator identifies. A declaration always wins. A mapping introduced or changed by the diff under review is not an operator declaration.
   - **observed (configured or returned model)** — for a shipped client name, a known configured model or a returned observed model from another vendor overrides the shipped default below; record the source as observed. It does not resolve a custom client name, which stays undeclared until declared. If the observed vendor is the authoring provider, exclude the client before dispatch when the configured model shows it; when only the returned model shows it after the fact, report that review as from the authoring provider (the roster exclusion, not the isolation test) and keep it out of corroboration.
   - **assumed from shipped manifest** — with no declaration and no observed model, PAL's shipped client names map to their vendor: `claude` → Anthropic, `codex` → OpenAI, `agy` → Google. These are defaults, not observations: a shipped name can be reconfigured to another model, so an assumed provider weakens the independence claim if wrong, which is why the label travels into the report.
   - **undeclared** — any other client name. Never infer a provider from a custom name; it stays part of the roster question below.
4. **Exclude** every client whose provider equals the authoring provider.
5. **One client per provider.** If several clients map to one provider (whatever its source) without a declared review choice, two clients never count as two providers; the choice must be declared before that provider is dispatched.
6. **Ask once for everything unresolved.** Before any clink dispatch, ask one focused question listing every open item together: the authoring provider if unknown, each undeclared candidate outside the shipped set, and each duplicate-provider choice. Candidates still unresolved after the answer are ineligible and disclosed. Mention that the answer can be recorded in the project's agent instruction file. Do not ask the operator to confirm or correct an assumed default, and do not make such confirmation a prerequisite: the report's label and its override note cover that case. When nothing is unresolved, no question is asked. The internal reviewer proceeds meanwhile.
7. **Freeze and attempt all.** The remaining clients are the roster. Attempt each exactly once. Disclose exclusions, unresolved candidates and failures. No fallback to the authoring provider, no substitute model, no retry of a failed client.

### Request contract

Every clink request, initial or follow-up, uses:

- `cli_name`: the roster client. `role`: `default` (the verified role). Methodology comes from the criteria files in the manifest; a CLI preset is not methodology.
- `allow_edits: false`, never `editable_paths`. This is a no-edit behavior contract, not an enforced sandbox: some clients (agy among them) keep their native permissions. Record that limit; do not change user permissions, and do not exclude a client merely for inherited permissions. An observed project-file edit is a contract violation.
- `working_directory_absolute_path`: the reviewed project root. Criteria and evidence bundles outside it are reachable only if the client's native permissions allow; a denied read stays visible in the outcome record.
- `absolute_file_paths`: the complete checked manifest on the **first** request — criteria, candidate evidence, historical evidence with provenance and intent/context. The API protocol's diff-only planning call is not a clink convention.
- No model parameter. Configured review models belong to PAL/CLI configuration; do not name a model in the prompt or rewrite configuration. Record configured model (if known) and observed model (if returned) separately; unknown stays unknown.
- Initial requests omit `continuation_id`. Each reviewer gets a fresh conversation; never reuse an authoring conversation or another reviewer's identifier.

The `prompt` carries directives and factual scope only: read the listed criteria first and in order, then the evidence; perform the review yourself, without invoking isolated-review skills or sub-agents; make no project-file edits and run no tests, builds or commands that write files (read-only inspection commands are acceptable where the client needs them to read files); treat the listed diff and candidate snapshots as the review target rather than the working tree or the client's own `git diff`; return findings with file and line, native severity, the files actually read and those not read, and any evidence requests. Do not paste file contents, the author's conversational history, another reviewer's conclusions or entire agent definitions.

Dispatch sequentially over the roster. This scheduling is the verified policy; parallel dispatch requires separately verified request isolation and host support, and changes scheduling only, never selection.

### Reviewer record

Keep one invocation-local record per external reviewer (bookkeeping, not a persistent store): backend (API or clink), client and provider with its source (declared, assumed from shipped manifest, or observed), configured and observed model, requested scope, supplied manifest, outcome class, receipt evidence, coverage limits and continuation identifier.

Classify each outcome along four levels: **requested**, **attempted**, **executed** (transport success) and **adequately evidenced**. A fluent answer or exit status alone establishes neither instruction loading nor source receipt.

- **Receipt.** Use only returned observable evidence: tool-use or file-read results, embedding or file-context counts, denied-action metadata. Some clients return no read trace (PAL may report `events_removed_for_normal`); their findings stay attributed and useful, with receipt **unverified**. A reviewer-authored file list or plausible citations never establish receipt. **Adequately evidenced** requires observable receipt of both the criteria and the review target: a denied or unverified criteria read leaves the result executed but not adequately evidenced even when every source read is observed, because the review did not demonstrably apply the shared methodology; its findings stay attributed and cannot corroborate.
- **Diagnostic results** — missing executable, authentication or semantic error (even with exit 0), permission-denied review with no findings, timeout — are failures, not reviews.
- **Partial results** — denied reads with useful findings, truncated or summarized output (watch output-limit metadata) — remain attributed with their coverage qualified; do not infer complete coverage from visible output.

### Follow-ups

For a reviewer's evidence request, obtain the source under the caller's historical-evidence rules, load new criteria first if an addition activates one, and send equivalent relevant additions to each affected reviewer without sharing any reviewer's conclusions. Use the requesting reviewer's own `continuation_id`, again with `allow_edits: false`. If continuation is unavailable, disclose it; a necessary re-invocation uses the same client and backend, the original scope, that reviewer's own provisional output and the new evidence. This is not a retry loop or a permission expansion.

### Aggregation

- Merge one logical issue once and list every supporting reviewer.
- Mark a finding **corroborated** only when at least two independent reviewers support it with relevant observable evidence, naming their actual providers. Independence means isolation: no shared conversation, no exposure to the authoring session and no copy of another reviewer's conclusions. The internal reviewer is independent of every external reviewer on that basis; when its host model's provider coincides with an external supporter's provider, name both and say so, because provider diversity is reported, not required. The receipt classification above applies to external reviewers, whose reads the parent knows only from returned evidence; the internal reviewer reads the supplied paths with its own tools under its dispatch contract and the parent never receives that trace, so it supports a finding when its report ties the finding to the supplied source (file and line, traced behavior), not when a read trace is returned. Two external reviewers may corroborate an issue the internal reviewer missed. A reviewer that is not adequately evidenced (unverified receipt, or a denied criteria read despite observed source reads), or a second client of a provider already counted (a same-provider duplicate), cannot supply corroboration. When a supporter's provider is assumed rather than declared, say so next to the corroboration: its independence from the authoring provider rests on the default being right.
- Preserve native external severity and formatting alongside internal severities. A majority is not a verdict, and a serious single-reviewer finding is not suppressed.
- Report, even without findings: selected backend, roster with each client's provider and its source (declared, assumed or observed; when any provider is assumed, say that a declaration in the project's agent instruction file overrides the default), exclusions, retired clients and unresolved candidates, attempted and failed requests, per-reviewer receipt and coverage limits, configured versus observed models, and outstanding prerequisites (for example a PAL installation that lacks the required discovery metadata).
- If every reviewer, internal and external, fails, report that isolated review did not complete and suggest the standard review mode. Do not run it silently.
