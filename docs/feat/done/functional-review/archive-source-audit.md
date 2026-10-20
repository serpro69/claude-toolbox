# Source-input retention audit

> Assessed: 2026-10-20 at `73c8b69ad5bea7bffff7d4d60f4e6a67072d83b0`
> Scope: Task 13.7 preparation; original evidence unchanged
> Current disposition: unavailable temporary inputs accepted as an exact-replay limitation; recovery gate retired
> Owner: maintainer cleanup verified; local preparation and user-requested draft upload are verified

## Accepted retention decision — 2026-10-20

The user confirmed that the temporary workspaces are unavailable and approved
archiving the retained evidence with that limitation documented. The initial
audit made recovery a cleanup prerequisite without establishing a material need
for exact replay of these older experiments. That prerequisite is retired.

Preserve all retained attempts, grades, decisions, manifests and original
identities. Export the still-available core source input described below. Record
the missing early inputs as unavailable; do not claim recovery or exact
reproducibility. No search of the old host or reconstruction is required.
Archive checksum/member verification remains required before cleanup; the later
local-first decision selects an ignored project-local archive for that check.
Those checks and maintainer cleanup are now verified in the
[completed handoff](release-archive-handoff.md); temporary-input recovery remains
outside the accepted scope.

The inventory and missing-hash findings below remain historical observations.

The full evidence tree is present: **73,099 regular files, 66 symlinks,
9,537 directories, 730,127,674 regular-file bytes**, excluding five cache
directories. Its membership matches the preceding handoff inventory. This is
not proof that all originally external source inputs were copied into it.

A read-only scan of `identity.json`, `launch.json`, `freeze.json`,
`declaration.json` and Task 2 frozen records found **28 distinct
(revision, archive SHA-256) identities**. Twelve have matching retained raw tar
bytes (including decompression of the closure source archives); one can be
reproduced from local Git; fifteen early identities have neither a matching
retained tar nor their temporary commit in this checkout.

## Recoverable core input

The core candidate `581dd0e11455398cb73e3d6ae5542854c016fe7f` still exists in Git.
A read-only `git archive` stream over `klaude-plugin`, `kodex-plugin` and
`.codex/agents` exactly matched the original SHA-256:

`c7e56b46c89b28f6ae0c9cca42e4997e2e8acd7a238709de1489de957b032765`.

Export those bytes outside Git tracking and include them in the locally verified
archive before purging the original history; attach that archive to the later
release. The command sequence in
[the handoff](release-archive-handoff.md) includes this export. No archive file was
created by this assessment.

## Unavailable early inputs — retained audit findings

Paths below are relative to the historical `verification/` tree. Each identity
record has its original revision/archive checksum, a sibling
`source-manifest.json`, and a retained `candidate.patch`. The original source
locations are in `origin.json` or `candidate-origin.json`; these refer to the
previous macOS controller directories under `/private/tmp/`.

| Identity record | Original revision |
| --- | --- |
| `task4/identity.json` | `6df37055f91dd2581fbb048baef4f3c72a9bc6e9` |
| `task4/candidate2/identity.json` | `d0ab5f0122724c050c2ecbd4563bb6e6fce2b68c` |
| `task5/identity.json` | `e7dd888235d7817c63733336afe983cca857bcb2` |
| `task5/candidate2/identity.json` | `93f7e0749052a5b0f908c0966354a704ff038bd0` |
| `task5/candidate3/identity.json` | `64f6bd2995c2af2dd618699e09c1d1ab8bd65571` |
| `task5/candidate4/identity.json` | `9db633e600678014980b0e5cf6d1865957bc53c5` |
| `task5/candidate5/identity.json` | `e21b907074ba8da43a59c8ccfc4d86078313ca2f` |
| `task5/candidate6/identity.json` | `b87def5bc67a7b066f3910378b06b743b7b5763e` |
| `task5/candidate7/identity.json` | `33ba4a2697cdfcb5f48a701f39e45bf347e08c53` |
| `task6/identity.json` | `31269c67ee11dd1d6d1f0f2ea7f218e40f86812a` |
| `task6/candidate2/identity.json` | `4ddc5c2a7c1db8cc900d22019c8fe19dc4f57bdf` |
| `task6/candidate3/identity.json` | `82e73ff69d5d3a7ef7f6f209d3cc070f41c43365` |
| `task6/candidate4/identity.json` | `68ea9c6e619ab2696f9e8315a90a4179fd14093d` |
| `task6/candidate5/identity.json` | `0250f822126c4b15fec822e9e2ab8f38d951c095` |
| `task6/candidate6/identity.json` | `10463ff31d654520b5712f1dc053407fccf48e9b` |

Across these source manifests, **827 of 845 distinct file-content hashes** are
already present in loose evidence or members of retained `.tar`/`.tar.gz`
archives. Eighteen remain unmatched by that search. This does not prove the bytes
are irrecoverable: patches, returned instruction text, another clone or the
original host may supply them. It does mean archiving the directory alone cannot
yet be represented as complete source preservation.

The following are representative original paths for the unmatched hashes.
Some hashes serve more than one generated/shared path; each original
`source-manifest.json` remains authoritative for the complete path mapping.

| Original path | Required SHA-256 |
| --- | --- |
| `klaude-plugin/skills/implement/evals/functional-standalone-patch-contract/eval.json` | `f5f7c0c0beae10397d3e015360e49e9cdb9176f1ee18312bb055e842f80f7c14` |
| `klaude-plugin/skills/review-code/evals/functional-disabled-provider-history/eval.json` | `dac932fee94e509fddf209ebf71dfbb901de44bd5eb3df0fc58002e3a57875ff` |
| `kodex-plugin/skills/implement/evals/functional-standalone-patch-contract/eval.json` | `528bcba5065d0bbbdd8bc9ab248eae7d878a81f21af1b5c4860efc83edafd594` |
| `kodex-plugin/skills/review-code/evals/functional-disabled-provider-history/eval.json` | `f2a8e2fbf907421a76f17858e8af4debbea9d794c7343d1c44497c2708c9c4f9` |
| `klaude-plugin/skills/review-code/SKILL.md` | `46de59474b4a010bedf44c1f136232d082c2b471c41e87ebf1dcd77a6b74ffb4` |
| `kodex-plugin/skills/review-code/SKILL.md` | `03d13ae594453a9c8b834019d14d13b9aa82b46a070bf4ac2283272fcbe65098` |
| `.codex/agents/code-reviewer.toml` | `61f2869170d02ab3438f31107068f48abf6f36f8e85d1461bad2ac3e35bf6004` |
| `klaude-plugin/commands/review-code/isolated.md` | `e2cc83e244e26249599b0905714e521f791e79b84e4c12f328cf9a3ffc8745a3` |
| `kodex-plugin/skills/_shared/pal-codereview-invocation.md` | `4e9beeeb599dac1da9729a7d08f2509f21a0145c3489d177f69458ae52680b62` |
| `klaude-plugin/skills/implement/SKILL.md` | `b013a4e813d3f29a69f901208522fcbc6e48ee5766e0fb6a626cbb74082c113e` |
| `klaude-plugin/skills/implement/plan-mode.md` | `efd4ca3af918c77cb8cf9bc5e9fad9c71b25e028c704099bdabb5215b2c311d8` |
| `klaude-plugin/skills/implement/standalone-mode.md` | `78489c2899f1b8885b87a726afe43c6ef9a7be4d692191d85235cc0903a4b69e` |
| `kodex-plugin/skills/implement/SKILL.md` | `e3143f8bbb1513aae825f7d290fbec79bd61f42b07ec2a4269fa19f410660313` |
| `kodex-plugin/skills/implement/plan-mode.md` | `6ef90fde1675a03ee0df831414dc5ebf0d20c7d1cd77c3cca4c61591e2f05434` |
| `kodex-plugin/skills/implement/SKILL.md` | `fd221e9fdbf29619af8330d5016dab2a6fbe62039d56c5570c3fccc9fd619356` |
| `kodex-plugin/skills/implement/plan-mode.md` | `c358858e44524b0fc7d57549727e1c8f51b9dc338881b81847b8a14494ae7d60` |
| `kodex-plugin/skills/implement/SKILL.md` | `8a4c923b126e46189338cc9ace555e0dd4f99aa7fe5d895adb11cf6d9d2541c3` |
| `kodex-plugin/skills/implement/SKILL.md` | `edef958dcb7ad1c7e67a71fc21c7ba97bf2c819b47182c55fd0f10146ad390e0` |

## Next action and completion condition

The retained evidence and available core export have been locally archived and
verified, with this limitation documented. The subsequent user-requested draft
release upload and downloaded checksum/member verification are also complete;
see the [handoff](release-archive-handoff.md). Do not require missing temporary
inputs to appear in the archive. The maintainer's evidence/history cleanup is now
verified, with original IDs retained in the rewrite maps. Publication of the draft
was not performed.
The decision changes retention requirements, not historical grades or feature
behavioral acceptance.
