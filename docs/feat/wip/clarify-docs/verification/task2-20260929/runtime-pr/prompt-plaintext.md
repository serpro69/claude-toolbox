# Plaintext prompts

Copied from the orchestrator’s live spawn calls. The encrypted transport is preserved separately; this transcription is attested, not cryptographically verified.

## editor_runtime

Use /kk:clarify-docs at /tmp/clarify-docs-task2-FRZOBXeu/instructions/SKILL.md to perform: '/kk:clarify-docs https://example.invalid/kitchen/pull/12 for repository reviewers. Work in the current feature docs/feat/wip/prep/. context.md contains the offline read-only PR response; use it and checkout/ without network access.' Workspace /tmp/clarify-docs-task2-FRZOBXeu/runtime-pr. Read allowlist: supplied SKILL.md and sibling shared-document-clarity.md; workspace context.md, remote-body.md, docs/feat/wip/prep/** and checkout/** including Git metadata. No snapshots/, originals, outside repository context, evals, oracles or other files. Read-only Git queries solely within checkout; no network. Write only the local draft authorized by the skill/request, via native edits; no testing/report files. Return normal brief result. You are not alone in shared filesystem; do not revert others’ work. Load full instructions before target/source reads. Use login:false for shell calls.

## reader_runtime_original

Read only /tmp/clarify-docs-task2-FRZOBXeu/originals/runtime-pr/remote-body.md. No other files, skills, sources, context, links, network, writes or delegation. You are a neutral documentation reader. Answer these five questions from that artifact only, citing wording or section and explicitly marking uncertainty for missing answers: 1. Why does this work exist? 2. What happens in a representative case? 3. What changes in the current increment? 4. What remains outside it? 5. What still needs a decision? Return concise numbered answers. Use login:false for shell calls.

## reader_runtime_revised

Read only /tmp/clarify-docs-task2-FRZOBXeu/runtime-pr/docs/feat/wip/prep/pr-12-draft.md. No other files, skills, sources, context, links, network, writes or delegation. You are a neutral documentation reader. Answer these five questions from that artifact only, citing wording or section and explicitly marking uncertainty for missing answers: 1. Why does this work exist? 2. What happens in a representative case? 3. What changes in the current increment? 4. What remains outside it? 5. What still needs a decision? Return concise numbered answers. Use login:false for shell calls.
