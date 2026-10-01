# Complete-candidate budget decision

Recorded before operative instruction edits or candidate behavioral grading on
2026-10-01, against repository `283f8da4606db7b1ad109b597f193bc9c0399377`.

Retain approach A. The complete shared procedure is **1,297 whitespace-delimited
words**, with no mandatory instruction dependencies. Set the ceiling to **1,297**,
an increase of **97** over 1,200. The separate entry point is **616 words**.
Counts use `wc -w`; they include headings, list markers and code spans.

| Initial candidate | SHA256 at Task 1 preflight |
| --- | --- |
| [Shared procedure](document-clarity-candidate.md) | `07395ff2f6d05afcf20e0d522f56a1e67fb74a354e784c85a881d2daf41b2b45` |
| [Entry point](clarify-docs-entry-candidate.md) | `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189` |

This is a size and preservation check, not a behavioral pass. Both the operative
procedure and this complete candidate must fit this ceiling independently. Future
wording changes require updated hashes/counts; increases repeat this preflight
before operative changes and require affected behavioral reruns.

## Coverage and deduplication

| Rule / existing safeguard | Complete-candidate location |
| --- | --- |
| Local/pasted/remote issues; GitHub/Linear optional; editorial action versus implement/fix/work; ambiguous URL | Entry: description and Inputs and boundaries |
| Selected draft only; immutable captures; bounded feature destination; missing destination; collision protection | Entry: destination paragraph; procedure Understand: gap paragraph |
| Read-only titles/types; no replacement titles; editable description headings | Entry: title paragraph |
| No external updates/comments/messages, implementation, reproduction-command execution or extra ledger | Entry: final paragraph; procedure Understand, Edit and Verify |
| Instruction-before-content order, bounded discovery, single source-read phase | Entry: Workflow; procedure introduction and Understand |
| Full artifact/evidence reads, bounded references, session revision checks, tests limited to exercised cases | Understand: original paragraphs retained |
| PR actual base/head/diff, inherited increment, contract/runtime distinction, validation outcomes | Understand: PR paragraph; Edit: PR paragraph retained |
| Issue context/comments; reported/verified and suspected/established distinctions; older revision; no required PR/future implementation | Understand: issue paragraph |
| Missing body versus missing support; accessible investigation first; next action and known/unknown owner | Understand: common and issue gap paragraphs |
| All five original protected-meaning categories; requirement/source disagreements; conclusive corrections | Establish: inventory and conflict paragraph retained |
| Explicit restrictions precede tracking; bounded GitHub default; default branch; private same-repo needs no audience question | Establish: visibility rules 1–2 |
| PR-head scope; different audience/repository, aggregator/untracked exclusions; other trackers; common org/credentials insufficient | Establish: visibility rules 2–3 |
| Facts as well as pointers; no uncited leaks; accessible task references; caller-only output-link exception | Establish: rule 4 and following paragraph retained |
| Five applicable reader questions; orientation, terminology, evidence-backed examples; no universal template | Edit: opening paragraphs retained |
| Bug reproduction/environment/conditions; feature scope/criteria/unknowns; other issue purposes; no invented criteria/decisions | Edit: issue paragraph |
| Scope, headings, anchors, inbound/cross-file links, executable examples | Edit: reorganization paragraph retained |
| Leave already-correct baseline unchanged, including factual/disclosure exceptions; no length objective | Edit: baseline paragraph retained |
| Independent comprehension/fidelity checks; lost qualifications, unsupported facts, state/topics/examples, disclosure, source conflict | Verify: existing checks plus issue-specific checklist |
| Local paths and gaps only; in-session verification limits and caller's review responsibility | Entry: Workflow; Verify: report paragraph |

Deduplication reuses the existing gap/ownership, evidence, fidelity, destination and
no-execution rules rather than repeating them for each issue type. The visibility
list replaces its existing PR/external paragraphs instead of appending a competing
policy. All existing four stages remain; no additional instruction file is loaded.
The remaining 97 words above the initial ceiling are needed to distinguish private
same-repository access from restriction overrides, issue evidence from PR evidence,
and absent body from absent support, while retaining bug details and proposal
uncertainty. Removing those distinctions would weaken the agreed contract.

## Slice application

Task 1 applies the entry point, issue evidence paragraph, GitHub audience default,
bug-report portion of Edit, and issue fidelity checks. Tasks 2–3 apply the reserved
feature/other-type and gap details and execute their dedicated scenarios. Shared
audience wording is kept coherent when applying the default; Task 2 still owns
different-audience and Linear behavioral verification. No later task is marked
complete by this preflight.

Task 2 application (2026-10-01): after both new baseline editors completed, apply
the prepared feature/other-type paragraph exactly. The operative procedure is now
**1,248 words**, SHA256
`cb06c670408be43198453ae324471661be22dfb325e862c6b25300c5ef894ecd`.
The complete candidate and entry point keep the counts and hashes recorded above;
no ceiling increase is needed. Only the 49-word issue-gap paragraph remains
unapplied for Task 3. Existing audience rules needed no additional wording; Task 2
owns their Linear/different-audience behavioral verification.

Task 2 PR regression correction (2026-10-01), recorded before operative editing:
the first destination-visibility draft names JSON parsing but omits the supplied
successful outcome required by unchanged assertion 13.8. Clarify the PR sentence
to require supplied outcomes in the draft itself. This preserves focused review
pointers, passed/failed/unavailable states, limits, and the prohibition on
substituting check names or completion reports. Both old and new sentences are
21 words; no other candidate rule changes. The entire refreshed candidate remains
**1,297 words**, SHA256
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
The ceiling stays **1,297** and the entry candidate is unchanged. Retain the first
behavioral attempts, then rerun affected PR cases 11/13 on the corrected operative
revision. Issue behavior is unchanged, but final issue runs will also use the final
instruction snapshot. This is a preservation preflight, not a behavioral pass.

Task 3 pre-application check (2026-10-01): all five new baseline editors have
finished before operative editing. Apply the remaining 49-word gap paragraph
without changing the complete candidate. The resulting procedure will match the
candidate byte-for-byte: **1,297 words**, SHA256
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
The ceiling remains **1,297**; no mandatory dependency, entry-point change or
description revision is needed. Coverage remains the full mapping above, including
missing body versus missing support, accessible investigation, destination and
ownership. Final behavioral runs follow this application; baseline observations
do not establish final-instruction acceptance.

## Provider description check

Rechecked [Claude Code skill documentation](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short)
on 2026-10-01: combined description/when-to-use text has a default 1,536-character
cap; the listing budget is 1% of context and both settings are configurable.
The candidate remains below the repository's stricter 1,024-character portability
budget: 449 characters, including the YAML block's trailing newline.
