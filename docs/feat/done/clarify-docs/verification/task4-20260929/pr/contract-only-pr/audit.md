# Coordinator trace audit

Observed editor calls remain within its request, two frozen instruction files, selected draft, and checkout. Instruction loading occurs at trace ordinal 19 before subject reads at 24. Ref log/tree reads at 24 and diff plus both-revision source reads at 30 establish the actual contract-only increment. The native patch attempt at 47 failed without changing a file; the corrected patch at 53 succeeded. Verification reread occurs at 58.

The original reader reads only its request (10) and artifact (19); the revised reader reads only its request (10) and artifact (19). Reader artifacts are verbatim copies of the corresponding frozen before/after draft. Both reader metadata files report gpt-6-astra, xhigh, summary none; temperature/build are unrecorded. All tool calls/results and visible assistant messages are retained. No oracle, outside-file content, source-only reader evidence, or network call appears in those traces.

Only pr-draft.md changes according to changes.json and before/after hashes. Shared-filesystem manifest enforcement is not OS isolation. The first shell calls use default login startup and include a failed ambient navi logging message; no subject-matter content outside the manifests is returned. This audit does not grade the assertions; the independent verdict follows separately.

