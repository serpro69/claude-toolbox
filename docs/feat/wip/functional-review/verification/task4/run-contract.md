# Task 4 standard-review dry-run contract

Declared 2026-10-09 before launching this candidate. This is an intermediate Task 4 integration dry-run, not Task 12 acceptance and not a replacement for the unchanged baseline captures. Task 2 gate 2B stays open.

- Repository base: `236928ee6f41ad60416f9a28077e89482acfa752` plus [candidate.patch](candidate.patch), including new files.
- Frozen instruction snapshot: `6df37055f91dd2581fbb048baef4f3c72a9bc6e9`, committed only in a disposable controller repository. Its full canonical/generated/agent trees were copied byte-for-byte from the working tree; [identity](identity.json), [source manifest](source-manifest.json), [retained manifest](retained-manifest.json) and [exclusions](exclusions.json) bind the filtered actor input. No toolbox branch commit is created by freezing it.
- Provider/model: Claude Code `2.1.278`, `claude-opus-4-8[1m]`, effort `high`. Capy `0.16.8`; Python `3.14.8`. Same runtime versions and ordinary tool policy as the Task 2 Claude captures. PAL remains configured identically, though standard review need not invoke it.
- Scope: one fresh instruction-binding probe, then one fresh R1 standard run on the frozen Task 2 `functional-cleanup-ownership` fixture and ordinary prompt. No assertions, oracles or controller documents enter actor inputs. Both workspaces are outside any skill-root ancestor.
- Loading: `--plugin-dir ./plugins/kk`, run-specific `CPR_PLUGINS_FILE`, normal hooks and strict run-local MCP configuration. Verify the copied filtered bundle before and after launch. A separate probe checks the registered entry point, common-method reads and hook root without subject analysis.
- State: fresh absent run-local knowledge database per workspace, private unavailable vault and no probe state inherited by R1. Run fresh two-store Capy isolation checks using the existing controller before R1.
- Capture: reuse unchanged `capture-seeds.py` preparation/capture functions. For preparation only, set its in-process `BASELINE` selector to the frozen candidate revision so its identity guard checks this candidate; do not alter the frozen baseline, fixture or rubric. Rename the Claude registry marketplace to include the candidate revision before launch. Launch metadata explicitly labels candidate/probe purposes. The capture command and controller hash are retained with every attempt; private reasoning and configured credentials are excluded.
- Evidence: retain ordered public events, actual instruction reads, catalog/root evidence, initial/final subject files, report, denial/failure events and hashes. Audit actor reads for evaluator leakage. A final claim alone proves neither instruction loading nor functional correctness.
- Assessment: record observed R1 defect/coverage and instruction order against the frozen rubric. The concrete workflow grader remains Task 8 work; no formal paired PASS or general reliability claim is made. Candidate changes after this freeze require a new identified run; preserve all attempts.

Packaging checks additionally exercise regular-file replacement, wrong/broken symlink targets and both complete-file word ceilings in disposable copies. Results are in [mutation-checks.json](mutation-checks.json). Canonical plugin files remain the source of truth; generated copies are refreshed and checked for a stable second generation.

## External-verification authorization — 2026-10-09

The first launch was rejected by automatic approval review before execution, because external transmission of the prepared inputs was deemed insufficiently authorized. After the explicit request naming the prepared Claude/PAL verification, the user replied “go ahead.” This authorizes the declared Task 4 binding probe, synthetic R1 dry-run and external review; it changes no fixture, model, rubric or acceptance threshold. The prepared candidate identity and fresh workspaces remain the same.

## Binding-probe retry — 2026-10-09

The first executed probe loaded the selected skill and common method, but attempted `echo` to read the hook root. That command was outside the unchanged allowlist and was denied; the root was only inferred. Retain that incomplete attempt in `binding/`. Run one fresh binding retry with an explicit instruction to use the already-allowed `printenv TOOLBOX_PLUGIN_ROOT` command and to read all shared instruction dependencies. This changes only the loading-probe prompt; the R1 ordinary prompt, candidate bytes, runtime and measured tool policy remain unchanged. Do not treat the first probe's inferred root as observed evidence.

## Candidate 2 — declared before launch, 2026-10-09

The first R1 trace has an observed instruction-order failure: event 38 requests the behavioral diff (returned at 41), before the Python checklist reads at 49–56. It also enumerates only the obvious Python detection file. Retain `r1-standard-1/`; later checklist reads cannot repair that attempt's order.

Candidate `d0ab5f0122724c050c2ecbd4563bb6e6fce2b68c` adds a compact loading checkpoint backed by returned instruction contents, prohibits batching investigation with those reads, and explicitly requires every known detection file to be read. [Candidate 2 manifests and patch](candidate2/) bind this revision. Shared method/context bytes and budgets are unchanged. Generation and structure checks passed after the correction.

Run fresh `binding2/` with the successful exact-command probe prompt, then `r1-standard-2/` with the original ordinary R1 prompt. All other model, runtime, permission, fixture, rubric and isolation settings remain unchanged. This is a new candidate's single Task 4 integration dry-run, not a second repetition of the failed candidate or a two-run acceptance claim. The original baseline remains valid and immutable; Task 12 must pair the final candidate with it under the full matrix contract.
