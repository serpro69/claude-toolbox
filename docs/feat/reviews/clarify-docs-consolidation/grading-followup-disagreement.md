# Independent follow-up grading: source-disagreement

The focused rerun receives **5 PASS, 0 PARTIAL, 0 FAIL** on unchanged assertions 2.1–2.5. The earlier partial result is retained in `grading-regressions.md`; this report assesses a new run under the follow-up instructions, not a replacement verdict for the original run.

The rerun closes the observed 2.4 gap: it gives the feature maintainer a concrete review-and-record sequence while explicitly keeping the next-day requirement accepted pending an approved decision. It does not claim that the implementation or requirements have been fixed.

## Assertion grades

I reread the unchanged eval and oracle, the original guide/requirements/source, the follow-up instructions and requests, the final snapshot, and both follow-up traces and completions. Evidence paths below are relative to this report. Snapshot line numbers preserve the runtime `guide.md` contents; trace line numbers refer to physical JSONL records.

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 2.1 — Distinguish accepted next-day intent from current immediate lookup behavior; other reader answers match | PASS | `evidence/consolidation_reader_followup_disagreement.txt` answer 2 distinguishes immediate 20 in the implementation from the accepted next-day delay and preserves old-order 15. Answers 1, 3, 4, and 5 correctly give defaults with exceptions, lookup and snapshot scope, scheduling exclusion, and the maintainer/product responsibilities. The mismatch is explicit in answers 2 and 5; answer 3 need not repeat it. |
| 2.2 — Retain mandatory next-day requirement and inspected immediate behavior without silently choosing a winner | PASS | `snapshots/followup-source-disagreement.txt` lines 8–11 describe immediate lookup; lines 19–20 say the accepted requirements mandate next-day activation and the implementation does not satisfy it. Lines 23–24 expressly retain that accepted requirement until an approved decision changes it. Lines 8–9 preserve missing/null inheritance and zero override; lines 13–15 preserve existing snapshots. No requirement is waived or rewritten as current behavior. |
| 2.3 — Inspect requirements and implementation before revising claims | PASS | `evidence/consolidation_followup_disagreement.jsonl` line 7/ordinal 23 returns both complete instructions. Line 9/ordinal 30 returns the complete original guide, requirements, and source. The source includes `effective_minutes`, `create_order`, and the 15-to-20 example. The first edit follows at line 11/ordinal 38. |
| 2.4 — Record discrepancy, owner, concrete next step, and no claim of fixing code/requirements | PASS | Snapshot lines 19–24 identify the disagreement and feature maintainer, then require reviewing the delay and scheduling exclusion with Product and recording an implementation plan or an explicitly approved requirement/scope change. These are concrete actions beyond “reconcile the conflict.” The paragraph does not select either outcome and explicitly retains accepted intent in the meantime. Neither the guide nor the editor completion claims a source or requirement fix. |
| 2.5 — Only guide changes | PASS | The only mutation is the single `guide.md` patch at trace line 11. `followup-manifest.json` lists the same three workspace filenames as the original fixture; requirements and source hashes match their unchanged originals. The final guide's hash matches the snapshot and the reader's full guide read. |

## Reader comparison

The comparison uses the fixed oracle questions and the two response files `evidence/consolidation_reader_original_disagreement.txt` and `evidence/consolidation_reader_followup_disagreement.txt`. As in the initial grading, clarification elsewhere in the same numbered response is considered; a reader is not required to repeat the timing mismatch in every answer.

| Question | Original | Follow-up | Evidence against the oracle |
| --- | --- | --- | --- |
| 1. Why the work exists | PASS | PASS | Both identify restaurant defaults with item exceptions. |
| 2. Change from 15 to 20 | FAIL | PASS | Original presents next-day activation as current behavior. Follow-up distinguishes inspected immediate 20 from required next-day activation and retains old-order 15. |
| 3. Current increment | PARTIAL | PASS | Original names lookup and snapshots but exposes no mismatch anywhere in its response. Follow-up names that increment and the mismatch is explicit in answers 2 and 5. |
| 4. Exclusion | PASS | PASS | Both identify scheduling. |
| 5. Open decisions | PARTIAL | PASS | Original identifies only product-owned badges. Follow-up also states the maintainer's review-and-record action and that next-day intent remains accepted. |

The original reader accurately repeated an inadequate document; its oracle failures are documentation failures. The follow-up's five answers are supported by its guide without consulting the linked source or requirements.

## Execution and evidence audit

| Check | Result and evidence |
| --- | --- |
| Complete instructions before subject reads | PASS. Both archived follow-up instruction texts occur in full in editor trace line 7, exactly matching the archived files. Subject reads occur afterward at lines 8–9. No truncated or search-only instruction read substitutes for loading the procedure. |
| Same original inputs | PASS. All three full subject strings returned at editor trace line 9 exactly match the original `source-disagreement/test-files/` fixtures, including the original misleading guide. The rerun did not start from the earlier candidate output. |
| Editor path isolation | PASS for recorded operations. The editor reads only its staged request, the two permitted instruction files, and the three case files, then rereads its edited guide. Its patch targets only the assigned guide. No repository, oracle, other-case, or installed-skill source read appears. |
| Reader isolation | PASS for recorded operations. Reader trace lines 3–6 show only the assigned reader request and final guide. The request contains the five unchanged questions. The reader does not follow the guide's links to requirements/source or inspect another version. |
| Trace completeness | PASS within the supplied format. The editor has five matched call/result pairs; the reader has two. Both traces end in the recorded final answer. Both `.txt` completion files equal their corresponding final response plus an archival newline. |
| No fixture execution or external service | PASS. Shell calls display files using `cat` or `nl -ba`; the edit uses `apply_patch`. No fixture import/execution, test run, network call, publishing action, or external service appears. The guide and completion make no claim of successful execution. |
| Write scope and artifact identity | PASS. The manifest's final workspace set is exactly `guide.md`, `requirements.md`, and `prep.py`; only guide differs from the original inputs. The final snapshot hash and reader-returned full guide agree. |
| Verification checklist | PASS for the observable reporting obligation. Editor trace line 15 records all five checks in order using the requested result/evidence form, with named guide sections or the retained title. The artifact and source comparison above independently support the assertion grades; the editor's checkmarks were not treated as proof. |
| Metadata | CONSISTENT. Both traces identify `gpt-6-astra` at `max` effort. The follow-up manifest records `fork_turns: none`. Hidden reasoning and operating-system confinement are not established by these visible traces. |

Both initial request reads contain the same failed shell-startup logging warning seen in the first trial. No successful out-of-scope write or returned subject matter from that location appears. As before, the path audit concerns recorded agent operations and the manifest, not an operating-system access trace.

The following bytes and SHA-256 hashes match `followup-manifest.json`:

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| Follow-up SKILL instruction | 4,648 | `0500399bc4ac48c663f53f423dbd99edba8db105924bc39ccd09ca4c88e3fe39` |
| Follow-up shared procedure | 11,519 | `a8bbbb4a8bfa25e743929e4a2c5f34a2c5b1c5a26bb4823e0000a6d77a429ba2` |
| Final guide snapshot | 1,376 | `7ccd240d93042cf9c34f825da80b1638556eac606075b0a50b84de75ab833989` |
| Unchanged requirements | 416 | `312b3dde2055c265f0077658f32741f2ed7ebc84166e1a1268fc5a60b9d10ee9` |
| Unchanged source | 747 | `b3cb7423756f8ee9b3a823cae3a9a1113e614baf1bfdfdbd616818359ddc80d2` |

The archived editor request also matches its manifest hash; the reader request recovered from its trace matches its manifest hash. Final unchanged source/requirements hashes are recorded runtime evidence, checked against the original fixture bytes and complete editor read results.

## Remaining limits

No remaining gap was found against assertions 2.1–2.5 in this rerun. The timing conflict, the scheduling exclusion, and the badge decision remain real unresolved feature work, correctly represented by the document. Reviewing possible requirement or scope changes does not itself authorize such a change: the guide explicitly requires approval and keeps the existing intent accepted meanwhile.

This focused rerun demonstrates that the observed next-action omission was corrected in this case. It does not retroactively convert the initial partial result to a pass or establish performance on cases that were not rerun. No input, prior report, fixture source, or other agent's file was changed during this grading; only this report was written.
