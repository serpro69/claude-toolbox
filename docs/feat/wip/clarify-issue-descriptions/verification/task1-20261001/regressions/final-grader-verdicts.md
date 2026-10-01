Both clean retries are **valid**, and all 11 assertions **PASS**.

| Assertion | Verdict | Concrete evidence |
|---|---|---|
| 1.1 | PASS | Revised guide alone supports purpose, complete 15→20 example, resolution/order snapshot increment, scheduling exclusion, and badge decision. |
| 1.2 | PASS | Preserves missing/null inheritance, explicit zero, live lookup, unchanged existing orders, all three identifiers, exclusion, and product-owner ownership. Claims agree with requirements and `prep.py`. |
| 1.3 | PASS | Editor trace ordinals 14–17 load both complete instructions; 19–22 read guide, requirements, and implementation; first edit is ordinal 26. |
| 1.4 | PASS | Owner purpose leads; materialization is defined at its first occurrence; example explicitly covers inherited item, zero, and an existing order across 15→20. |
| 1.5 | PASS | Before/after hashes show only `guide.md` changed; no additions or removals. |
| 12.1 | PASS | Revised reader answers all five questions consistently with the oracle through `pr-12-draft.md`. |
| 12.2 | PASS | Draft distinguishes new resolver/tests from inherited contract; preserves null/zero, future work, badge decision, and three-assertion/deployment limits. |
| 12.3 | PASS | Trace ordinals 25–28 resolve actual commits and read their diff; 32–36 inspect requirements, contract, resolver at both revisions, and head tests. |
| 12.4 | PASS | Exactly one draft added under the requested feature directory. Remote capture and unrelated draft retain identical hashes; no network or remote-write attempt appears. |
| 12.5 | PASS | Opening explains restaurant defaults and 15/null, zero, and positive cases; review pointers target `resolve.py` and `test_resolve.py`; contract is explicitly inherited. |
| 12.6 | PASS | Complete instructions precede source reads. All 27 existing files, including 20 Git metadata members, remain byte-identical; no ledger or extra summary appears. |

Reader comparison against the unchanged oracle:

| Question | Dense original → revised | Runtime original → revised |
|---|---|---|
| Purpose | PASS → PASS | FAIL → PASS: original says unspecified. |
| Representative case | PASS → PASS | PARTIAL → PASS: original supplies only unspecified sentinel/default routing. |
| Current increment | PASS → PASS | FAIL → PASS: original incorrectly presents the schema as newly added. |
| Exclusions | PASS → PASS | PARTIAL → PASS: original names separate work but omits deployment-evidence limits. |
| Open decision | PASS → PASS | PARTIAL → PASS: original identifies owner/badges without specifying inheritance display. |

Dense-source demonstrates improved orientation and explicitness, **not improved answer accuracy**: both readers answered correctly. Runtime-pr demonstrates improved oracle agreement.

**Dense-source validity: PASS.** Every observed read matches its manifest: editor instructions plus the three supplied files; each reader only its guide version. The sole mutation is the authorized guide patch. Its completion accurately reports the change and retained decision. No blocked ambient initialization, outside-scope content read, network attempt, or extra artifact appears.

**Runtime-pr validity: PASS.** Editor reads stay within instructions, supplied PR context/captures, and the authorized checkout. All Git queries use `--no-optional-locks`. The `rg` listing was blocked by a hook before execution; it produced no content read or mutation. Subsequent authorized Git queries supplied the needed evidence. The only write uses exclusive creation for the new draft, then rereads it. Readers access only their respective artifacts. The completion accurately identifies the output and retained limits.

Across both scenarios:

- All **78 final-manifest hashes**, prompt hashes, participant-manifest hashes, and complete input/output inventories verify.
- Both archive hashes and all member hashes verify; archived Git member bytes are identical before/after. Actual commit trees match the grader-only source snapshots.
- Instruction outputs exactly match both frozen instruction files in full.
- All visible calls have matching results and completed sessions; saved completions/answers match trace finals. No output is truncated.
- Fresh sessions use identical actual `gpt-6-astra`/`xhigh` settings and no inherited conversation. Reader prompts have identical questions and instructions, differing only where the artifact path requires it.
- No editor/reader oracle or grader-snapshot access appears. Actual reader output hashes match their permitted artifacts. No oracle leakage or missing visible tool evidence invalidates either run.
