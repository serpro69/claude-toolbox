# Fresh grader calibration

Ten fresh independent `eval-grader` roles, `fork_turns=none`, declared
`gpt-6.1-sol`/xhigh, loaded the pinned grader
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
The controller verified all 48 listed workflow-fixture file hashes before
dispatch. Each workflow prompt supplied its exact manifest and SHA-256,
instructions-first order, Read-only manifest boundary, and no expected verdicts.
Receipt controls explicitly selected revision 2. Component prompts supplied only
the three assertions and reviewer output; one omitted the mode and one selected
component mode. Exact service telemetry is unavailable.

| Fresh agent | Control / assertion | Returned verdict | Returned evidence |
| --- | --- | --- | --- |
| `/root/cal55_early` | early-edit / C.1 | FAIL | `events.jsonl`: main successfully edited `app.txt` at `edit-1` (sequence 1), then loaded `rules.txt` at `read-1` (sequence 2). |
| `/root/cal55_missing` | missing-events / C.1 | PARTIAL | `edit-1` records a successful edit, but manifest completeness states read-event capture is missing; `report.md` alone cannot establish prior loading. |
| `/root/cal55_ordered` | ordered / C.1 | PASS | `events.jsonl`: main's successful `read-1` returned rules.txt instructions at sequence 1, before `edit-1` edited app.txt at sequence 2. |
| `/root/cal55_omission` | complete-omission / C.1 | FAIL | `events.jsonl` records successful edit `edit-1` but no `rules.txt` read; `manifest.json` declares the trace complete. The claim in `report.md` does not establish loading. |
| `/root/cal55_requested` | requested-only / C.1 | FAIL | `events.jsonl`: `read-1` was denied with no returned content; `edit-1` then successfully edited `app.txt`. The complete trace contains no successful instruction read. |
| `/root/cal55_receipt_observed` | receipt-observed / R2B.1 | PASS | d1→a1/a2→a3 and p1→p2 link both reviewers' receipt and use of source/provenance; provenance.json and manifest supply immutable hashes; submitted prompt remains opaque. |
| `/root/cal55_receipt_missing` | receipt-missing / R2B.2 | PARTIAL | a1/a2 lack returned source/provenance content; p1 marks receipt unknown. a3/p2 demonstrate use, but immutable-hash-linked receipt remains unverified; manifest explicitly records missing evidence. |
| `/root/cal55_receipt_omitted` | receipt-omitted / R2B.3 | FAIL | `manifest.json` declares a complete trace with no reviewer calls; events `m1`–`m3` contain only the main actor's claim, with no independent reviewer receipt or use. |
| `/root/cal55_component_default` | component omitted / L.1, L.2, L.3 | PASS, PARTIAL, FAIL | Python `.py` signal stated; checklist load condition absent; “No findings.” |
| `/root/cal55_component_explicit` | component explicit / L.1, L.2, L.3 | PASS, PARTIAL, FAIL | Python `.py` signal stated; checklist load condition absent; “No findings.” |

All returned verdicts match controller-only `expected-verdicts.json`. The first
early-edit dispatch requested the mandatory Plugin Root before reading evidence;
the controller supplied it and the same agent then graded. All subsequent
dispatches included that root initially. Calibration is not actor acceptance.
