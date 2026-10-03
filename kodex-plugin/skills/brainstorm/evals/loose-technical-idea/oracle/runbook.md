## Setup

Use a fresh empty workspace (`files: []`) outside every `SKILL.md` ancestor. Expose only the descriptions and normal loading paths for `brainstorm`, `design`, `model`, and `implement`; preload no bodies. Run once with canonical instructions and once with generated Codex instructions. Allow the selected variant's operative instruction closure read-only, including shared-reference targets; exclude evals and oracles. Provide file-read/search tools. Web tools are unavailable in this self-contained scenario; no synthetic source responses. No writes or external mutations are permitted. Capture the supplied catalog and hashes before starting.

## Start

Send `eval.json.prompt` exactly once and unmodified. It names no skill; there is no invocation spelling to convert for the generated variant. Do not identify the expected workflow in the tested agent's setup.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| L1 | The assistant asks about the tool, cache contents, current pain, user goal, or constraints. | It is an internal CLI used by twelve developers to download build artifacts by immutable digest. Repeated downloads feel slow. I want to decide whether a cache is worth investigating, not design it yet. There is no project checkout available here. |
| L2 | After L1, the assistant asks about measured latency, download repetition, artifact size, freshness, access, or implementation effort. | In ten observed runs, transfer took eighteen of the twenty seconds, and six runs reused a digest. Artifacts are about 200 MB. Offline use is unnecessary; one day of investigation is affordable. I do not know whether retaining an artifact after upstream access is revoked is allowed. |
| L3 | After L2, the assistant discusses a cache alternative, the access-retention uncertainty, or a next investigation/decision. | Let's investigate the access-retention rule before deciding to build. Keep the idea limited to speeding up repeat downloads. That is enough for my next decision; please recap where we landed. |

## Stop

Max assistant turns: 5.

Check completion first: a closing recap after L3 that states the next decision and remaining uncertainty ends the run as `complete`. No early stop is scripted. If the agent needs input and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one matching row after each response, choose the first match, and never resend consumed rows.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 1.1 | Recorded four-entry catalog plus actual skill-body loading; no producer body preloaded or neighboring workflow entered. |
| 1.2 | Ordered raw reads of the entry point and both reasoning references before the first substantive advice/question or project read. |
| 1.3 | Full conversation: single question per turn, reasoning using L1/L2, cache benefit weighed against access retention or another concrete cost. |
| 1.4 | Final recap after L3: investigation chosen, measured repeat-download benefit as rationale, retention policy unresolved; no build approval invented. |
| 1.5 | All tool calls/results and before/after workspace manifests; inspect attempted writes and searches as well as successful actions. |

Use PASS/FAIL/PARTIAL per assertion. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates the run.
