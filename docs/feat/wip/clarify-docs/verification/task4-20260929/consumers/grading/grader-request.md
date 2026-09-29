Act as a fresh independent general-purpose evaluation grader. Assess the five consumer scenarios under the evidence directory below. Read only this request, that evidence directory, and the frozen instructions. Do not use any other repository content, installed plugin copy or sessions. Do not write files, run tests or documented commands, access network, edit artifacts, or spawn agents. Python/read-only hash comparison and text inspection are allowed.

Allowed evidence root:
/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/consumers

Allowed operative instruction root:
/tmp/clarify-task4/instructions/skills
/tmp/clarify-task4/instructions/profiles

Scenarios:
- clarity-after-drafting
- clarity-refined-documents-only
- clarity-unchanged-resume
- clarity-preserves-profile
- implementation-mode-coverage

Read each scenario's eval.json and oracle/expected.json (where present), manifest.json, exact editor/reader request files, original/output/input artifacts, and COMPLETE visible traces. Raw *-trace.jsonl retains tool calls/results and visible assistant messages; *-trace.md is a readable rendering. A truncated tool result is preserved exactly; inspect whether the editor reread affected instructions before subject matter. Hidden reasoning and system boilerplate were intentionally omitted. Check the actual operative instruction files when grading instruction loading, handoff and completion routes. Do not assume the editor report proves ordering.

For clarity-after-drafting, original/ is the completed set of pre-pass drafts, not accepted.md. completed-drafts/ repeats this observational snapshot. For refinement and document, original/ comes from the original selected input, with the reader path declared in the oracle; document's completed-drafts/ is additional ordering evidence. For unchanged resume, compare the full unchanged docs. implementation-mode-coverage is only route inspection; original/revised readers and lifecycle execution are N/A.

Verify independently:
1. Every numbered eval assertion, giving PASS/FAIL/PARTIAL and concrete evidence pointers (trace record/source line, artifact line/heading, source path). PARTIAL and missing evidence are not pass. Do not weaken assertions.
2. For each reader scenario, all five original and revised answers against the predeclared oracle: grade individually and give original→revised score out of five. Keep comprehension distinct from source fidelity, structural requirements, orientation, and visibility.
3. Each protected claim and orientation expectation, including source evidence. Where all baseline answers pass, assess predeclared non-comprehension defects; if baseline is fully clean require no-op. Do not count shorter prose as comprehension evidence.
4. Exact permitted read/write paths against ALL tools in editor and reader traces, request isolation, no oracle/source-only/other-version reader access, source inspection and instruction ordering. A manifest restriction is not OS isolation. Invalidate any out-of-manifest content read or missing trace rather than grading it as success.
5. Same actual model/settings for original/revised readers, session IDs, complete source/output hashes, and preservation of attempts. Model build and temperature can be recorded as unexposed, never invented.

Return final JSON (no code fence) with:
{
 "scenarios": [
  {
   "name": "...",
   "overall": "PASS|FAIL|PARTIAL|INVALID",
   "assertions": [{"id":"...", "verdict":"PASS|FAIL|PARTIAL", "evidence":"..."}],
   "comprehension": {"original_score":0,"revised_score":0,"questions":[{"number":1,"original":"PASS|FAIL|PARTIAL","revised":"PASS|FAIL|PARTIAL","evidence":"..."}]},
   "protected_claims":[{"claim":"...", "verdict":"PASS|FAIL|PARTIAL", "evidence":"..."}],
   "orientation":[{"expectation":"...", "verdict":"PASS|FAIL|PARTIAL", "evidence":"..."}],
   "fidelity":{"verdict":"PASS|FAIL|PARTIAL","evidence":"..."},
   "isolation":{"verdict":"PASS|FAIL|PARTIAL","evidence":"..."},
   "limitations":["..."]
  }
 ],
 "aggregate":{"assertions":{"PASS":0,"FAIL":0,"PARTIAL":0},"limits":["..."]}
}
Use null comprehension and empty protected/orientation arrays for route inspection, explicitly limiting its result. Include any important additional observed fidelity or protocol failure even if not a numbered assertion. State AI-reader evidence cannot establish human-comprehension improvement.

