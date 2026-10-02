# Document, PR and issue scenarios

Stage each scenario's test-files/ as its own workspace root, outside the plugin and
any SKILL.md ancestor. Load only the skill under test, its shared instructions and
the scenario prompt into a fresh editor session. Never stage eval.json or oracle/
with the editor: they contain grading expectations. For non-triggers, make the
skill description available for selection without preloading its body.

Cases 1–6 separate comprehension (the five neutral questions in oracle/expected.json)
from fidelity, source inspection and predeclared orientation/correctness defects.
Give fresh original and revised readers only the files in reader_manifest, with the
same questions and model/settings. A separate grader gets their answers, both
artifacts, requirements/source, the editor tool trace and oracle. Every assertion
needs PASS/FAIL/PARTIAL with evidence. Cases 7–10 grade routing and unchanged files;
reader comparison is not applicable.

Record staged hashes, exact allowed-file manifests, model/settings, raw tool traces,
answers and verdicts with the consuming project's verification evidence. Shared
filesystem access is not isolation: inspect traces for reads outside the manifest,
and invalidate leaked or incompletely traced runs. These are manual scenarios, not
an executable harness. Authored scenarios are not evidence of executed behavior.

## PR fixture setup

Cases 11–15 add PR increments, destination visibility and local output boundaries.
Cases 11–13 include `snapshots/base/` and `snapshots/head/`: before the editor runs,
create a separate staged Git repository at `checkout/`, commit the base snapshot
and name that revision `review-base`, then commit the head snapshot and name it
`review-head`. Leave head checked out. Preserve snapshot paths relative to each
snapshot root. Record the actual revision IDs and diff in the run evidence. These
are real local revisions; misleading stack labels in `context.md` are intentional.
The snapshots are staging inputs, not additional editor reading paths.

Give the editor staged non-snapshot files plus read-only access to `checkout/`,
including Git metadata for revision/diff queries. Never permit Git writes during
editing. URLs ending in `.invalid` and the PR bodies/access declarations are
synthetic read-only platform responses: do not contact a real service. Cases 12
and 15 use `remote-body.md` as immutable input; case 14 uses an immutable pasted
body capture. Case 12 includes an unrelated draft to test collision handling.

Cases 11–13 and 15 use original/revised readers. Resolve
`<produced-local-draft>` to the editor's actual output; `original_reader_manifest`
overrides `reader_manifest` for the original where present. Provide only the named
artifact: all five answers must be available there. Case 13's baseline answers
already pass; its declared disclosure defect still requires repair. Inspect the
editor's final report as well as its draft for private-fact leakage. Case 14 grades
clarification and unchanged files without a reader comparison. The separate grader
also receives the source snapshots, access declarations and actual Git evidence.

Case 13 requests a caller-only completion link to the selected local output by
absolute path. Grade that link separately from prohibited private source pointers;
the exception applies only to this completion message, never to the destination
draft or disclosure of restricted facts.

## Issue fixture setup

Cases 16–24 use supplied offline issue context, not PR base/head pairs. Stage only
each scenario's `test-files/` as an independent workspace. Do not initialize a PR
checkout, contact a tracker or expose the oracle to the editor. Editing cases
16–22 must not execute reproduction commands; execution cases 23/24 permit local
source checks as described below. Synthetic URLs and repository snapshots stand
in for read-only responses; they do not certify a live integration.

Case 16 identifies a private GitHub repository, its default-branch revision and
tracked snapshot files in `context.md`. It deliberately declares no alternative
audience. Preserve that setup: do not add a sharing declaration to make the case
easier. The explicit restriction on one tracked source still applies. The body
capture `remote-body.md` is immutable input; the existing feature draft is unrelated.
Authorize only one new draft within the established feature directory. Retain the
supplied title/type as context, distinct from editable description headings.

Case 17 explicitly selects `issue-draft.md` for in-place editing; requirements and
source remain read-only. Its commands are documentation, not test instructions.

Case 18 supplies a Linear feature proposal with confirmed sharing for its intended
audience. Preserve the immutable title/body capture and authorize only a new
`issue-draft.md`. Existing synchronous source is evidence of current behavior;
no future implementation or PR checkout is required. Comments distinguish an
unaccepted mechanism from accepted intent and the pending owner's decision.

Case 19 selects a local GitHub issue draft for an explicitly different audience:
external integration partners. Keep the supplied access declarations, including
the distinction between shared references, restricted tracked facts, merely
tracked internal material, and credential-only or unknown-access sources.
Its caller-only completion link is permitted only for the selected local output;
it does not permit private source pointers or facts in either output.

Cases 16–19 and 21 use fresh original/revised readers with the fixed questions and
manifests in `oracle/expected.json`. Resolve `<produced-local-draft>` after editing;
readers receive only their respective artifact. Grade fidelity and audience access
separately from reader answers. Inspect draft and completion message for restricted
facts and source pointers, including uncited paraphrases, and compare all other
files byte-for-byte. Record baseline and revised-instruction runs separately with
their actual instruction hashes, exact prompts, manifests, traces and verdicts.

Case 20 supplies an immutable pasted-body capture and accessible requirements,
without a destination or feature scope. Authorize no writes; grade the context
inspection, destination question and unchanged files instead of a revised reader.

Case 21 supplies an immutable pasted body and a definitive offline failure for its
supporting source. Authorize only the new `drafts/issue-21.md`. The draft can clarify
the reported behavior while retaining verification limits, Mina's source-retrieval
step and the unassigned reproduction/cause owner. No source checkout is needed.

Case 22 supplies an access failure with a cached title but no issue body or alternate
copy. A destination is specified; it does not authorize inventing a description or
writing a placeholder. Grade the request for body text/access and unchanged files;
reader comparison is not applicable.

Cases 23/24 use ordinary implement/fix requests and small source fixtures. Expose
only the skill's description in the selection catalog; do not preload its body or
shared procedure, tell the editor which skill to reject, or substitute a request
to classify intent. Make the normal skill-loading path available so mistaken
activation is observable in the trace. Permit normal source edits and local checks
within the staged fixture. Grade editorial non-activation and unchanged issue text,
not source implementation correctness. No original/revised readers are needed.

## Long integration-guide scenario

Case 25 starts with a clear purpose and worked example. Its later sections mix
consumer instructions, implementation evidence and obsolete review history, with
related qualifications scattered across the document. Adding another introduction
does not address the declared defect. The warehouse service and its history are
synthetic; no production repository or external service is needed.

Stage only `test-files/` as a separate workspace, with `guide.md` as the sole writable
artifact. The Python file is a small behavioral model, not an HTTP service or proof
of database isolation. The editor reads it as evidence, without executing it.
Give fresh original/revised readers only their respective `guide.md` and the same
practical questions from `oracle/expected.json`. Require answers with section
pointers; do not give readers requirements, source, defect labels or expected answers.
The grader receives those sources plus both guides, reader answers and editor trace.
Grade task discoverability and fidelity separately: merely answering the opening
orientation questions is insufficient, and shorter output cannot offset a lost
qualification. Record word counts as context only, never as a pass threshold.
Use the oracle's concrete consolidation checks to distinguish a full repeated policy
from a useful local reminder. Moving the same obsolete narrative into an appendix
does not pass. Grade the resulting document independently of the editor's checklist;
for instruction versions with the checklist, also inspect its recorded locations and
results. Keep the same output-quality rubric for baseline and revised runs.

Run the existing `already-clear`, `source-disagreement` and `cross-file-preservation`
scenarios alongside this case when evaluating changed instructions. They guard
against unnecessary rewrites, removal of unresolved requirements and broken links.
As with the earlier cases, record actual model runs separately from fixture checks;
valid JSON and executable source do not establish improved reader comprehension.
