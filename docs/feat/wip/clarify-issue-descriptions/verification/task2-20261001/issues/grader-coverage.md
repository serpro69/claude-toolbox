# Final grader read-coverage audit

The complete raw editor/reader traces have no truncated tool-result content.
The final graders' own traces contain three capped batches. Their required
instruction, specification, oracle, participant-trace and protocol coverage is
complete before the verdicts; no participant or grading rerun is needed.

| Final grader trace result | Capped content | Required coverage and recovery |
| --- | --- | --- |
| `linear-issue-feature/final-grading/trace.jsonl:8` | Combined design/implementation read omits the design tail around line 266 onward and the implementation opening through roughly line 70. | The accepted read-versus-execute decision at design lines 147–149 is visible before the cap. The expressly required execution/evidence protocol at implementation lines 222–250 is visible in the retained tail, including the encrypted-transport rule. The omitted portions are background assumptions/exclusions and repository-map/build-order/budget context, not missing scenario expectations or required audit instructions. |
| `linear-issue-feature/final-grading/trace.jsonl:12` | Combined instruction-snapshot read omits part of the first-revised shared procedure, around lines 11–75. | Call/result at lines 13–14 explicitly rereads first-revised shared-procedure lines 1–87 completely before source/output review. The participant traces are later read completely at results 21, 23 and 25, and content-identity checks independently confirm full instruction/source bytes. |
| `issue-destination-visibility/final-grading/trace.jsonl:8` | Combined design/implementation read omits the design tail around line 259 onward and implementation opening through roughly line 80. | Call/result at lines 9–10 completely rereads design lines 250–310 and the required implementation execution/evidence section at lines 222–257 before scenario auditing. The only unrecovered portion is the implementation's background repository-map/build-order/budget opening, outside the requested execution-protocol read. |

The precise final-grader request requires reading the implementation's
“Execution and evidence protocol” section before auditing. It does not require
re-reading every background page in full. Scenario 18 additionally requires
auditing the narrow spec correction against the accepted design; its relevant
read/execute boundary is fully visible. The unread optional background is not
treated as independently inspected evidence for the verdicts.

All fixed spec/oracle reads, source artifacts, reader answers, and seven
participant traces per final grader have complete visible coverage. The graders
also recompute source/reader hashes, compare returned instruction/source bytes,
match every call/result/final and audit prompt receipts and file effects. No
uncaptured participant result is substituted with a hash summary.

This audit preserves both final reports and every original result. It adds no
new grading expectation, transport requirement or inferred filesystem isolation.
