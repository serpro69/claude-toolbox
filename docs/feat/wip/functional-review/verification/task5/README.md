# Task 5 verification

Status: **done**, with independent APPROVE scoped to the implementation and one R3 integration review plus a supplemental provenance repair. This is not full workflow/matrix acceptance.

The [run contract](run-contract.md) records candidates and launches before execution. Final actor `33ba4a2697cdfcb5f48a701f39e45bf347e08c53` is bound by [candidate7 identity](candidate7/identity.json), source/retained manifests and its patch against repository base `76f37a0104488580a6de17de3266b90ab53b91d0`. No repository branch commit was created. Task 2's baseline, frozen fixtures and rubric are unchanged.

## Implemented behavior

The isolated workflow loads instructions before investigation, prepares actual historical source, reconciles complete criteria manifests for both reviewers, resolves evidence requests and qualifies reporting by observed coverage. The agent supports absolute/legacy checklist paths and source-only reporting. PAL code review stages the diff first and the full source/criteria bundle at the expert continuation; document review retains its existing inputs. The command summary mirrors the workflow.

## Local checks

- Final rerun of all nine shell suites: **640 passing assertions, no skips**. [Check summary](check-summary.json); raw logs are in checks/. Initial schema checks lacked uv cache access and template-sync skipped network cases; complete retries passed. Fixture commits used per-command signing disabled, without changing persistent Git configuration.
- Final generation (generator tests plus plugin/Codex structure suites) and plugin graph validation pass. The graph's cycle warning is retained in its log.
- [Second-generation freshness](freshness-candidate7.json): 684 generated files unchanged; 1,379 source entries match frozen candidate7.
- Fresh two-store Capy probes passed indexing/search, absent foreign markers and unavailable vault. Independent initial runs inherited no probe state. Supplements explicitly retain only the same R3 review's own state.
- [Capture integrity](completed-capture-integrity.json), [initial R3 checks](candidate7-integrity.json), and [supplement checks](provenance-followup-integrity.json) verify seals, unchanged subjects/bundles and corrected provenance. Original records are preserved.

## Captures and corrections

| Capture | Disposition |
| --- | --- |
| binding through binding7 | Selected registered skill/root/common/agent reads observed for each frozen candidate. |
| r3-isolated; r3-isolated3 | Prepared only; superseded before launch. |
| r3-isolated2 | Failed parent ordering and unsupported corroboration with unverified PAL receipt. |
| r3-isolated4 | Failed ordering: full diff misclassified as bounded routing. Historical/PAL observations retained separately. |
| r3-isolated5 | Historical comparison and applicable instruction order supported, but PAL omitted two required criteria; full Known-profile enumeration also skipped. |
| r3-isolated6 | Complete rule reads/order supported; failed historical-source discovery, unresolved source request and omitted knowledge protocol. |
| r3-isolated7 | Complete rule reads, applicable instruction ordering, criteria parity and historical comparison supported. Blob-hash placeholder required supplemental completion. |
| r3-provenance-followup | Failed command execution: echo-prefixed Bash and Capy fallback denied under unchanged tool policy. |
| r3-provenance-followup2 | Actual hash obtained with directly allowed Git commands; corrected provenance delivered and reviewed through explicit reinvocation. Completes the remaining Task 5 condition. |

Failures are never relabeled as passes. Binding probes' unsubstantiated prose about shared-file layout is not source evidence; the manifests contain the actual shared files/symlinks. Temporary evidence retained outside sealed runs is separately mapped to its captured Write contents before any cleanup.

## R3 evidence and bounded closure

See [initial events](r3-isolated7/events.jsonl), [dispatches](r3-isolated7-dispatches.json), [initial report](r3-isolated7/report.md), and [independent audit](review.md):

- All eight detection rules returned. Parent checklists returned71–77, checkpoint84 preceded first diff85. Child common/profile returns188–212 preceded checkpoint214 and evidence215.
- README107 identified local release history. Lookup115/result118 resolved the tag; source132/result135 returned the provider implementation, absent from candidate files and diff hunks.
- Agent180 and PAL240 received the source and all eight common/profile criteria. Child historical read226/result228 and PAL253's15 newly embedded files plus source comparison establish receipt/use within the stated transport limits.
- Both reviewers identified the reachable flag-off incompatibility and returned REQUEST_CHANGES. No fixture source changed.

The initial manifest had a command placeholder instead of the actual blob hash. Its omission remains recorded. The [supplement](r3-provenance-followup2/events.jsonl) completes that condition:

- Git requests93/97 returned matching actual blob hashes at96/100; Write149 created [corrected provenance](r3-provenance-followup2-bundle/manifest.corrected.json), preserving the original.
- The child loaded all eight criteria and read the correction at221/result223. PAL258 received corrected provenance/source and all criteria; result259 embedded12 new files and reconfirmed the comparison.
- The expired PAL continuation at239 was explicitly replaced by planning247/expert258. Each reviewer received only its own prior findings. The [supplemental report](r3-provenance-followup2/report.md) discloses reinvocation and unchanged review scope.

The independent audit returned **APPROVE for Task 5 closure**, with no remaining hard slice blocker. No systemic P0/P1 implementation finding requires indexing. Its approval concerns the review implementation, not the deliberately defective fixture client.

## Remaining acceptance

The supplement is neither a retroactive initial-run pass nor a fresh matrix repetition. Native P0/P1 and CRITICAL/HIGH severity remains uncalibrated. Private PAL expert prompts and full provider parity were not inspected. Document-review compatibility was verified at source level, not through a full design-review runtime run.

Owner: implementing agent in Tasks 8/12. Pin the workflow grader, run every required fresh baseline/candidate pair and routing/reporting control, and verify all required assertions twice under the selected contract, including complete provenance before handoff and impact-based severity. Retain failed attempts and fix/recapture affected cases. Task 2 gate2B and remaining feature work stay open; no reliability guarantee follows from these observations.
