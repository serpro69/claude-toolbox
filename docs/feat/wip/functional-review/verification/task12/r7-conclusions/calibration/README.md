# Fresh grader calibration — 2026-10-13

Ten independent `eval-grader` roles, `fork_turns=none`, declared
`gpt-6.1-sol`/xhigh, used the [pinned grader](grader.md) with SHA-256
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
Exact dispatched messages and returned assertion rows are retained in
[dispatches.json](dispatches.json) and [results.json](results.json).

The controller copied the existing synthetic controls unchanged, validated all
48 manifest-listed workflow files, then dispatched each control to a fresh grader.
Workflow prompts supplied the manifest hash and read boundary, with revision 2
explicitly selected for receipt controls. Component prompts supplied only the
three assertions and reviewer text; one omitted the mode, one selected component.
Expected verdicts were not included in any grader prompt or read manifest.

**All ten controls match their expected outcomes: 14/14 assertion verdicts.**
Early edit, complete omission, denied-only read and omitted reviewer calls fail;
missing events/receipts remain partial; complete ordered reads and linked receipt/use
pass. Both component variants return PASS/PARTIAL/FAIL for L.1/L.2/L.3.
These expected negative grades establish calibration, not actor acceptance.
Receipt/use does not establish exact submitted prompt content; service-internal
model telemetry and OS read confinement are not claimed.
