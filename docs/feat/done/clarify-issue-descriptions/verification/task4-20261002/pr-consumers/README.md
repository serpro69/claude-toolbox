# Task 4: PR and current consumer behavioral evidence

This cohort covers current PR scenarios 11–15 and the five current design/document
consumer regressions. It uses the canonical instruction snapshot in `instructions/`,
with hashes in `instruction-hashes.json` and source revision in `source-revision.json`.
Consumer cases test ordinary drafting and optional clarification recommendations.

Executed: ten scenarios, ten accepted fresh editors and eight fresh PR readers.
The independent fixture-capable grader confirmed **46 PASS, 0 FAIL, 0 PARTIAL**.
The [grading summary](grader/summary.md) records the decision and evidence limits;
each case below contains its assertion-level verdicts and scope/trace audit.

| Skill | Scenario | Assertions | Verdicts |
| --- | --- | ---: | --- |
| `/kk:clarify-docs` | Contract-only PR, 11 | 5 | [PASS](contract-only-pr/verdicts.json) |
| `/kk:clarify-docs` | Runtime PR, 12 | 6 | [PASS](runtime-pr/verdicts.json) |
| `/kk:clarify-docs` | Destination visibility, 13 | 8 | [PASS](destination-visibility/verdicts.json) |
| `/kk:clarify-docs` | Missing PR context, 14 | 3 | [PASS](pr-missing-context/verdicts.json) |
| `/kk:clarify-docs` | Unavailable PR source, 15 | 4 | [PASS](pr-unavailable-source/verdicts.json) |
| `/kk:design` | Clarification suggestion after drafting, 5 | 5 | [PASS](clarity-after-drafting/verdicts.json) |
| `/kk:design` | Refined documents only, 6 | 4 | [PASS](clarity-refined-documents-only/verdicts.json) |
| `/kk:design` | Unchanged resume, 7 | 3 | [PASS](clarity-unchanged-resume/verdicts.json) |
| `/kk:document` | Profile preservation, 1 | 5 | [PASS](clarity-preserves-profile/verdicts.json) |
| `/kk:document` | Unchanged document, 3 | 3 | [PASS](clarity-unchanged-document/verdicts.json) |

Each case has an exact read/write manifest, immutable `before/` snapshot and hashes,
an `after/` snapshot and file effects once executed, and complete visible native
editor tool/message records. PR 11–13 additionally have actual local base/head revisions and their diff
in `git-evidence.json`; their staging snapshots are not editor-readable paths.
PR 11–13 and 15 get separate fresh original/revised readers; case 14 and all
consumer cases are graded directly from artifacts and traces.

For repository portability, each nested `.git` directory in a captured snapshot
is represented losslessly by `checkout/git-metadata-export.json`: original
relative filenames, SHA-256 hashes, and base64 bytes. `git-metadata-portability.json`
records the mapping. The hashes for original `.git/...` paths in before/after
manifests refer to those decoded bytes, not to the JSON wrapper. The actual staged
checkouts remain intact under the temporary workspace. Readable base/head source
snapshots also appear under `source-snapshots/`. No embedded Git repository needs
to be staged as a gitlink, and `git check-ignore --no-index` found no ignored
required evidence files at the portability check.

All agent runs use the default role, `fork_turns=none`, no model/effort override,
and no delegation. Actual model settings are captured from each native session.
Prompt plaintext is saved with native apply_patch before dispatch and hashed.
Later prompts also have JSON captures whose decoded message bytes match the text
capture. Native encrypted dispatch records and receipts link those prompts to
their child sessions. Transport encryption limits direct payload decryption; it
does not replace the retained plaintext or tool/message audit.

The initial short pre-dispatch windows omitted several earlier plaintext echoes.
`prompt-provenance-index.json` and each role's `prompt-provenance.json` now retain
lossless existing native call/output records for all 18 accepted editor/reader
prompts. The grader independently decoded and matched every echo byte/hash,
call/output ID, and pre-dispatch timestamp/ordinal. This resolves the missing-window
coverage; it does not decrypt native transport or reconstruct an unavailable prompt.

One editor output was truncated: `clarity-after-drafting` record 29 clipped part of
`frameworks.md`. Record 37 reread the complete file before subject-matter reading.
The grader verified that recovery. All other accepted editor/reader tool outputs
had no truncation markers; every recorded tool call has a matching result.

Durable session exports preserve every tool call/result and visible assistant
commentary/final message, submitted-task transport, and minimal runtime metadata.
They exclude system/developer harness boilerplate and hidden reasoning. Each
`capture.json` retains the source native-session path/hash and the separate visible
export hash; original native logs remain unchanged outside this evidence tree.

Staging is under `/private/tmp/t4-prc-20261002/`, outside every SKILL.md ancestor.
This is a shared filesystem with manifest restrictions, not OS isolation. Network,
external services, source mutation and reproduction commands are forbidden.
Synthetic provider fixtures do not certify any live connector.

Preserved invalid setup/capture attempts:

- `staging-attempt-1/`: inherited Git signing prevented initial fixture setup;
  see `staging-note.md`. No behavioral dispatch used that setup.
- `contract-only-pr/capture-attempt-1/`: saved prompt had an extra trailing LF;
  excluded from acceptance and rerun with byte-identical prompt capture.

The coordinator loaded `/kk:test` and its shared detection/knowledge protocols.
Skill-root inputs activate skill-md, which supplies no test phase. The current
Kubernetes document rubric is staged for the profile-preservation consumer case.
No repository validators are owned by this cohort; the parent task runs them.

`run-index.json` identifies the accepted editor/reader sessions and grader with hashes.
`coverage-index.json` validates all 46 fixed assertion IDs/texts and verdicts.
The [grader trace audit](grader/trace-audit.md) records the independent grader's
complete tool/result coverage, its separate instruction-read recovery and authorized
outputs. `portability-check.json` records the final no-ignore/no-gitlink check.
`canonical-input-integrity.json` confirms that 67 scenario inputs and 36 instruction
files match current canonical source. `snapshot-integrity.json` verifies all
captured before/after bytes, including decoded Git metadata. The staged workspace
checks in `staging-location-check.json` found no SKILL.md ancestor and no staged
eval specification or oracle. These packaging checks complement the independent
behavioral verdicts; they are not substitutes for them.
