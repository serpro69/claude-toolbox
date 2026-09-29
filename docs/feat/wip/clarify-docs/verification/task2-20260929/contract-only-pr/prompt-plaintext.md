# Plaintext prompts

Copied from the orchestrator’s live spawn calls. The encrypted transport is preserved separately; this transcription is attested, not cryptographically verified.

## editor_contract

Use /kk:clarify-docs at /tmp/clarify-docs-task2-FRZOBXeu/instructions/SKILL.md to perform this request: '/kk:clarify-docs pr-draft.md for this repository’s reviewers. Use context.md and checkout/ as evidence; edit only pr-draft.md.' Workspace /tmp/clarify-docs-task2-FRZOBXeu/contract-only-pr. Read allowlist: the supplied SKILL.md and its sibling shared-document-clarity.md; workspace context.md, pr-draft.md, and checkout/** including Git metadata. Do not access snapshots/, originals, or other files, directories, repository context, eval definitions or oracles. Use read-only Git queries solely within checkout. No network. You may edit only workspace/pr-draft.md, using native edits. No testing/report files. Return your normal brief result. You are not alone in the shared filesystem; do not revert or edit others’ work. Read entire instructions before target/source reads. Use login:false for shell calls.

## reader_contract_original

Read only /tmp/clarify-docs-task2-FRZOBXeu/originals/contract-only-pr/pr-draft.md. No other files, skills, sources, conversation context, links, network, writes or delegation. You are a neutral documentation reader. Answer these five questions from that artifact only, citing its wording or section and explicitly marking uncertainty when an answer is missing: 1. Why does this work exist? 2. What happens in a representative case? 3. What changes in the current increment? 4. What remains outside it? 5. What still needs a decision? Return concise numbered answers. Use login:false for shell calls.

## reader_contract_revised

Read only /tmp/clarify-docs-task2-FRZOBXeu/contract-only-pr/pr-draft.md. No other files, skills, sources, context, links, network, writes or delegation. You are a neutral documentation reader. Answer these five questions from that artifact only, citing wording or section and explicitly marking uncertainty for missing answers: 1. Why does this work exist? 2. What happens in a representative case? 3. What changes in the current increment? 4. What remains outside it? 5. What still needs a decision? Return concise numbered answers. Use login:false for shell calls.
