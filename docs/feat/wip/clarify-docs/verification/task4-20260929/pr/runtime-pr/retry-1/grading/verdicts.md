# Independent runtime PR retry grading and prior-case applicability

The runtime retry is **VALID within the recorded shared-filesystem protocol** and **PASS: 6 PASS, 0 PARTIAL, 0 FAIL assertions**. Observed reader accuracy is **ORIGINAL 0/5 → REVISED 5/5**. Fidelity, review-increment grounding, destination handling and observed isolation pass independently.

Prior-case applicability is **3 RETAIN PASS, 1 RERUN REQUIRED, 0 UNCERTAIN**. `destination-visibility` requires a fresh run because the revised procedure explicitly requires validation results, while its preserved draft names JSON parsing without reporting the outcome. This does not reverse its original pass. None of the four earlier cases executed the revised procedure.

The [initial grading](../../../grading/verdicts.md) remains history: runtime assertion 12.1 was PARTIAL, with 0/5 → 4/5 reader accuracy; the initial five-case total was 24 PASS, 1 PARTIAL, 0 FAIL. This correction-based retry is a separate observation, not a replacement of that record.

## Runtime assertions

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 12.1 | PASS | [Revised answers](../revised-output.md), Q1–Q5, recover every unchanged [oracle](../scenario/oracle/expected.json) answer through the produced draft. Q3 explicitly identifies both runtime resolution and added `test_resolve.py`, with the contract unchanged. See the question table below. |
| 12.2 | PASS | [Revised artifact](../revised-artifact.md), opening, “What changes in this PR,” “Review and validation,” and “Open decision”: new resolver versus inherited schema, null inheritance, explicit zero, 0–90 integer contract, future persistence/scheduling/UI, product-owner badge decision, three assertion cases and no deployment validation all survive. The artifact accurately separates selection from range enforcement. |
| 12.3 | PASS | [Editor trace](../editor-trace.md), calls 32 and 39/results 37 and 45, resolves actual base/head IDs, reads changed-file status and head membership, then reads requirements, the resolver/test diff, base contract and head resolver. [Git evidence](../git-evidence.txt) corroborates `08e5cd169c65117c509ec3b58bebdd229df194a0` → `af341ff761181751094e5ed58ee7fde3cf6ef65d`: `resolve.py` changes and `test_resolve.py` is added. The inherited schema and misleading stack title do not determine the increment. |
| 12.4 | PASS | Trace call 25 reads the unrelated existing draft; 51 checks the chosen alternate path is unused; 56 creates only `docs/feat/wip/prep/pr-12-draft.md`; 61 rereads both. Independently recomputed [before/after hashes](../manifest.json) and [changes](../changes.json) show the original draft and `remote-body.md` byte-identical. No network or remote-write call appears. |
| 12.5 | PASS | The revised artifact leads with avoiding repeated item preparation values, then gives default 15/null→15, zero→0 and seven→7. Its review path directs readers to `resolve.py`, then the new assertions in `test_resolve.py`; `contract.json` is explicitly inherited. |
| 12.6 | PASS | Full frozen entry and shared instructions return at trace result 23, before the first subject read at call 25. The sole authored patch creates the selected local draft. Snapshot comparison shows no source, ledger or extra-summary change. |

## Five-question comparison

One point requires a fully correct oracle-backed answer. PARTIAL receives zero points. An honest statement that an original document omits a known answer does not recover that answer; it is not counted as a hallucination either. Unknowns earn credit when the evidence supports unknown as the required answer. No document-length criterion is used.

| Question | Original | Revised | Evidence and scoring reason |
| --- | --- | --- | --- |
| Q1: Why does this work exist? | FAIL, 0 | PASS, 1 | Original Q1 says the purpose is not established. Revised Q1 explains that restaurant defaults avoid repeating preparation times and allow item overrides, citing the opening paragraph. |
| Q2: Representative case | FAIL, 0 | PASS, 1 | Original Q2 cannot establish concrete inputs/results. Revised Q2 gives all three runtime results: `(15, None)`→15, `(15, 0)`→0, `(15, 7)`→7, citing paragraph two. |
| Q3: Current increment | FAIL, 0 | PASS, 1 | Original Q3 incorrectly presents nullable `prep_minutes` as added. Revised Q3 identifies the replacement of `NotImplementedError` with resolution, addition of `test_resolve.py`, and unchanged contract, citing “What changes in this PR.” |
| Q4: Outside scope | PARTIAL, 0 | PASS, 1 | Original Q4 identifies persistence/scheduling/UI but omits the lack of deployment proof. Revised Q4 includes these exclusions and no recorded persistence/deployment validation; its additional range-validation limitation is source-supported. |
| Q5: Remaining decision | PARTIAL, 0 | PASS, 1 | Original Q5 says the product owner must choose badges but cannot establish that this concerns displaying badges for inherited values. Revised Q5 states that exact decision and owner, citing “Open decision.” |
| **Total** | **0/5** | **5/5** | **Five fully correct revised answers; no partial answer counted as a pass.** |

Answer evidence is [original-output.md](../original-output.md), [revised-output.md](../revised-output.md), and the unchanged [oracle](../scenario/oracle/expected.json). Reader citations refer to their own allowed artifact, not source-only evidence.

## Fidelity and scope, assessed separately

| Check | Verdict | Independent basis |
| --- | --- | --- |
| Review increment | PASS | Actual Git diff modifies the resolver and adds tests; base/head contract and requirements blobs are identical. The draft states all three distinctions. |
| Protected semantics | PASS | [Head requirements](../scenario/test-files/snapshots/head/requirements.md), [contract](../scenario/test-files/snapshots/head/contract.json), [resolver](../scenario/test-files/snapshots/head/resolve.py) and [tests](../scenario/test-files/snapshots/head/test_resolve.py) support null inheritance, explicit zero, integer 0–90 requirements, and the 15/0/7 cases. The resolver selects values without enforcing the range; the draft preserves both intent and implementation. |
| Validation limits | PASS | [Context](../before/context.md) supplies a record that three assertions passed at head and no persistence/deployment validation occurred. The draft attributes that result to the supplied record and does not claim this editor reran tests. It also correctly says the assertions do not cover range validation. |
| Future work and decision | PASS | Persistence, scheduling and UI remain separate; the product owner retains the unresolved inheritance-badge decision. No product decision is silently settled. |
| Destination collision and local-only writing | PASS | The unrelated `pr-draft.md` is preserved; the alternate named draft is checked before creation. The patch and recomputed snapshots show one authorized local output and no other authored change. |
| Destination visibility | PASS | Context expressly allows tracked checkout material for established repository reviewers. Trace 32 verifies head membership. The destination contains no absolute workspace path or private source pointer. The caller-only completion links the selected local output. |

## Trace, manifest and evidence integrity

**Observed isolation: PASS. Retained trace completeness and internal consistency: PASS.** These are manifest-and-trace findings on a shared filesystem, not OS isolation or a claim to have audited inaccessible native session stores.

I inspected the exact [editor request](../editor-request.md), [original-reader request](../original-request.md), [revised-reader request](../revised-request.md), spawn texts, raw JSONL traces and readable traces. Every observed read and write is accounted for below. The coordinator [audit](../audit.md) was checked against this evidence, not adopted as a verdict.

| Role / trace calls | Observed operation | Manifest assessment |
| --- | --- | --- |
| Editor 10 | Reads its request. | Allowed. |
| Editor 19 → result 23 | Reads the complete frozen `SKILL.md` and shared procedure. | Allowed; both returned texts match the frozen files in full. No linked additional instruction exists. |
| Editor 25 → 30 | Reads context, remote body and unrelated existing local draft. | All three are expressly allowed; first subject reads occur after complete instructions. |
| Editor 32 → 37 | Reads checkout revision IDs, changed-file names and head membership. | Read-only Git inspection within allowed checkout. |
| Editor 39 → 45 | Reads head requirements, actual resolver/test diff, base contract and head resolver. | Read-only Git inspection within allowed checkout. |
| Editor 51 → 54 | Checks alternate output existence. | Destination collision check within the authorized feature scope; no content read or write. |
| Editor 56 → 59 | One native `apply_patch` creates the alternate draft. | Sole authorized mutation. Result reports script completion; the subsequent reread and snapshots independently establish the exact resulting content. |
| Editor 61 → 65 | Rereads its new output and the existing unrelated draft. | Both allowed. |
| Original reader 10/19 → 13/22 | Reads only its request and original artifact, with line numbering. | No source, oracle, revised version, other-case read or write. |
| Revised reader 10/19 → 13/22 | Reads only its request and revised artifact. | No source, oracle, original version, other-case read or write. |

There are **12 retained outer calls and 12 matching results**: eight editor calls and two per reader. The nested operations comprise 16 editor shell calls, one editor patch, and four reader shell calls. All raw call IDs pair with results in order; readable trace ordinals match the raw records. No retained result reports truncation. Final messages match their separate output exports. No network, external mutation, delegation or runtime-test execution appears. The only shell-startup anomaly is the recorded failed ambient `navi` logging initialization on initial default-login reads; it returns no additional subject content and is not an authored output.

Independent SHA-256 recomputation confirms every retry input/output inventory, manifest input/output/request/artifact hash, and all three instruction-hash entries, including the shared-file alias. The entry instruction hash is `5d9d6886c0c0195ed182ee3e2761eae66095e507ade5366f7d81289ccf3fd4d0`; the revised shared procedure hash is `566d92f3ece7700cb1659cc0b480f1a4a72e75a434bf186c8a042d0d3133a3e9`. The original artifact equals the remote-body snapshot; the revised artifact equals the selected after snapshot and authored patch. Their actual reader tool results reproduce those contents. Recomputed changes equal `changes.json` exactly.

The retry's entire `scenario/` and `before/` trees match the initial runtime attempt byte-for-byte. Thus fixtures, assertions, oracle and questions are unchanged. `git-refs.json`, `git-diff.txt` and `git-evidence.txt` are also byte-identical. Independently computed Git blob IDs for all seven base/head fixture files match the captured trees. Every request matches its initial equivalent after substituting only workspace and frozen-instruction prefixes. The frozen entry instructions are unchanged, and the calculated old/new shared-procedure diff equals [instruction-diff.diff](../instruction-diff.diff) exactly.

The [editor metadata](../editor-metadata.json), [original metadata](../original-metadata.json) and [revised metadata](../revised-metadata.json) record distinct thread `id` and context-window IDs. The shared root `session_id` is not mistaken for a reader thread ID. Actual recorded settings agree: **`gpt-6-astra`, `xhigh`, `summary: none`**; both initial runtime readers use the same settings. Spawn messages contain only the corresponding request path. Standard harness/AGENTS context remains present in these fresh sessions. Temperature and model build are unrecorded. Native rollout paths and their claimed source hashes are metadata only here: those stores are outside the allowed manifest and were not independently opened or rehashed.

## Applicability of the four earlier passes

The exact instruction change replaces “explain the problem, behavior and increment” with “explain purpose, behavior and increment, identifying newly added tests,” and replaces “meaningful validation with its limits” with “validation results and their limits.” It also drops an article before “indiscriminate file inventory.” The preceding requirement to lead with purpose, and the rules for evidence, uncertainty, visibility, destinations and local-only scope, are unchanged. The correction about added tests is narrow, but the explicit validation-result wording must also be assessed.

I checked each preserved editor trace's full instruction result against the [old frozen entry](../../../instructions/SKILL.md) and [old shared procedure](../../../instructions/document-clarity.md), inspected the relevant original sources/diffs and produced artifacts, and recomputed each case's before/after hash inventories. These are initial-version executions only. Retention means the preserved evidence remains applicable to this focused change; it does not mean the updated procedure was executed or that its future behavior is guaranteed.

| Prior case | Applicability verdict | Concrete rationale and evidence |
| --- | --- | --- |
| `contract-only-pr` | **RETAIN PASS** | The [actual diff](../../../contract-only-pr/git-diff.txt) changes only `contract.json`, so there are no newly added tests to identify. The [draft](../../../contract-only-pr/revised-artifact.md) already leads with purpose, distinguishes contract from runtime, and explicitly reports **successful JSON parsing**, with no runtime tests or deployment. Its [reader answers](../../../contract-only-pr/revised-output.md) recover that result. The revised wording creates no unmet obligation in this case. |
| `destination-visibility` | **RERUN REQUIRED** | The [diff](../../../destination-visibility/git-diff.txt) has no added tests, and visibility rules are unchanged. However, the [preserved draft](../../../destination-visibility/revised-artifact.md), lines 6–7, says only “validation is JSON parsing only,” followed by limits. This identifies a method, not its outcome. Successful parsing is available in [context](../../../destination-visibility/before/context.md) and the [editor trace](../../../destination-visibility/editor-trace.md), call 43/result 47, but remains outside the reader's artifact; the [revised reader](../../../destination-visibility/revised-output.md), Q3, likewise reports coverage only. The caller-only completion cannot supply the result to destination readers. A fresh execution is needed to satisfy the newly explicit result obligation while preserving the disclosure repair. The original 7/7 assertion pass remains valid under its original instructions. |
| `pr-missing-context` | **RETAIN PASS** | [Context](../../../pr-missing-context/before/context.md) supplies neither destination nor repository/revisions/source. The unchanged destination/evidence rules require clarification before producing a draft. The [final question](../../../pr-missing-context/editor-output.md) requests destination, actual revisions/diff and test results; [changes](../../../pr-missing-context/changes.json) remain empty. Added-test identity and validation results cannot be established, and the new PR-writing sentence does not authorize fabrication or override this necessary clarification. |
| `pr-unavailable-source` | **RETAIN PASS** | [Context](../../../pr-unavailable-source/before/context.md) supplies an authorized output and confirmed contract but no revisions/diff/source/test results. The [draft](../../../pr-unavailable-source/revised-artifact.md) already states that test results and the actual increment are unavailable, preserves confirmed purpose/behavior, and assigns the PR author the concrete evidence action. [Reader Q3](../../../pr-unavailable-source/revised-output.md) recovers the supported unknown and owner. Newly added tests cannot be identified without the missing evidence; unchanged uncertainty rules govern, so no supported obligation is left unmet. |

## Limits and counts

This is one fresh editor and one reader per version after an instruction correction. It establishes observed AI-reader behavior, not improved human comprehension, statistical reliability or runtime correctness. The retry did not execute tests or deployment; passing assertions remain an attributed fixture validation record. Retained exports permit an internal consistency audit, not proof of unobserved filesystem activity or a complete independently retrieved native session history. Shared-filesystem controls, standard harness context and unrecorded build/temperature limit isolation and reproducibility claims.

- Runtime retry: **6 PASS / 0 PARTIAL / 0 FAIL**; reader answers **0/5 → 5/5**.
- Separate fidelity and observed-isolation verdicts: **PASS**.
- Earlier-case applicability: **3 RETAIN PASS / 1 RERUN REQUIRED / 0 UNCERTAIN**.
- Initial runtime PARTIAL and all initial evidence remain preserved; no input was edited during grading.
