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

Cases 16–19 use supplied offline issue context, not PR base/head pairs. Stage only
each scenario's `test-files/` as an independent workspace. Do not initialize a PR
checkout, contact a tracker, run reproduction commands or expose the oracle to the
editor. Synthetic URLs and repository snapshots stand in for read-only responses;
they do not certify a live integration.

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

All four cases use fresh original/revised readers with the fixed questions and
manifests in `oracle/expected.json`. Resolve `<produced-local-draft>` after editing;
readers receive only their respective artifact. Grade fidelity and audience access
separately from reader answers. Inspect draft and completion message for restricted
facts and source pointers, including uncited paraphrases, and compare all other
files byte-for-byte. Record baseline and revised-instruction runs separately with
their actual instruction hashes, exact prompts, manifests, traces and verdicts.
