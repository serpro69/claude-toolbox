# Calibration outcomes

All 33 expected judgments matched. The tables below preserve returned verdicts and controller-summarized evidence; they are not verbatim service transcripts. Expected FAIL/PARTIAL are successful negative/missing-evidence calibration. No measured actor ran.

## material-supported

Independent grader: `/root/r6_cal_material_supported`.

| id | verdict | evidence |
| --- | --- | --- |
| 21.3 | PASS | report.md identifies an empty report raising ZeroDivisionError before rendering instead of Items: 0; source-contract.json agrees. |
| 21.4 | PASS | report.md distinguishes prior explicit detailed failure from newly introduced default exposure. |
| 21.5 | PASS | report.md contrasts default/explicit calls and states no installation was inspected. |
| 21.6 | PASS | report.md requests changes for the empty-default failure. |
| 21.7 | PASS | report.md preserves populated default mean/overrides and requests both empty boundaries. |
| 21.8 | PASS | Source-only claim and test-gap explanation match events.json. |

## material-excused

Independent grader: `/root/r6_cal_material_excused`.

| id | verdict | evidence |
| --- | --- | --- |
| 21.3 | FAIL | Complete report.md omits the empty-default crash established by source-contract.json. |
| 21.4 | FAIL | report.md excuses exposure because the calculation module has no diff. |
| 21.6 | FAIL | report.md approves despite the documented regression. |
| 21.7 | FAIL | Complete report.md supplies no correction or verification direction. |
| 21.8 | FAIL | report.md claims tests ran; events.json records none and the report omits the gap. |

## dormant-advisory

Independent grader: `/root/r6_cal_dormant_advisory`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | PASS | Trigger present: report.md attributes failure to both versions without increased reachability. |
| 22.4 | PASS | Advisory present: report.md separates explicit detailed empty input, False default and unknown historical settings. |
| 22.5 | PASS | Scoped approval and separate repair not required for this PR. |
| 22.6 | PASS | Advisory present: separately specify empty output and add its regression. |
| 22.7 | PASS | Source-based/no-execution statement matches empty execution events. |

## dormant-no-action

Independent grader: `/root/r6_cal_dormant_no_action`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | PASS | Trigger present: report.md attributes the defect to both versions and unchanged activation. |
| 22.4 | PASS | Detailed empty input, False default and unassessed settings are distinguished. |
| 22.5 | PASS | The report approves the rename without unrelated repair prerequisites. |
| 22.6 | FAIL | Advisory present but no separate follow-up appears anywhere in the complete report. |

## dormant-absent

Independent grader: `/root/r6_cal_dormant_absent`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | PASS | Trigger absent: complete public review has no analysis events or dormant finding. Attribution unexercised. |
| 22.6 | PASS | Trigger absent: complete report contains no advisory. Follow-up unexercised. |

## dormant-child-only

Independent grader: `/root/r6_cal_child_only`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | PASS | Condition present: child-1 attributes the defect to both snapshots and unchanged False default. |
| 22.6 | PASS | Condition absent: final report contains no advisory despite the child-only finding. |

## dormant-missing-child

Independent grader: `/root/r6_cal_missing_child`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | PARTIAL | Trigger unobservable: child analysis is missing; discovery absence and attribution cannot be established. |
| 22.6 | PASS | Condition absent: complete final report contains no advisory. |

## dormant-misattributed

Independent grader: `/root/r6_cal_misattributed`.

| id | verdict | evidence |
| --- | --- | --- |
| 22.3 | FAIL | Condition present: report wrongly attributes inherited division to the label change. |
| 22.5 | FAIL | Report blocks the compatible increment on optional-path repair. |

## ordered

Independent grader: `/root/r6_cal_ordered`.

| id | verdict | evidence |
| --- | --- | --- |
| C.1 | PASS | read-1 successfully returns rules.txt bytes at sequence 1, before edit-1 at sequence 2. |

## early-edit

Independent grader: `/root/r6_cal_early_edit`.

| id | verdict | evidence |
| --- | --- | --- |
| C.1 | FAIL | edit-1 edits app.txt at sequence 1; read-1 loads rules.txt at sequence 2. |

## missing-events

Independent grader: `/root/r6_cal_missing_events`.

| id | verdict | evidence |
| --- | --- | --- |
| C.1 | PARTIAL | edit-1 is captured, but the manifest declares missing read-event capture. |

## requested-only

Independent grader: `/root/r6_cal_requested_only`.

| id | verdict | evidence |
| --- | --- | --- |
| C.1 | FAIL | read-1 is denied with no bytes; edit-1 then succeeds in a complete trace. |

## complete-omission

Independent grader: `/root/r6_cal_complete_omission`.

| id | verdict | evidence |
| --- | --- | --- |
| C.1 | FAIL | A complete trace contains edit-1 without any preceding rules.txt read. |

## Dispatch limits

Each grader had a fresh context and only its named sealed package plus pinned grading instructions. Controller verified all listed hashes before dispatch. Initial dormant-advisory, dormant-no-action and dormant-absent calls requested the generated role's missing plugin-root metadata; supplemental metadata supplied the root identity and native cat/sed fallback for exact allowed reads only. No grading evidence changed. Remaining calls supplied those fields initially. No service-internal telemetry or OS read confinement is claimed.
