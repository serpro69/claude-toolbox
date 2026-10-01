# Execution and evidence protocol

The repository has no built-in behavioral eval runner. Follow the existing manual
protocol, extending its README for issue setup rather than adding automation.

- Stage each `test-files/` as a separate workspace root outside a `SKILL.md`
  ancestor. Exclude `eval.json` and `oracle/` from editor and reader access.
- Provide synthetic provider identity, body/access responses, and audience
  declarations in readable fixtures. Use clearly synthetic URLs and explicitly
  prohibit network calls. Do not set up PR revision pairs for issue scenarios.
- Before editing, fix applicable neutral comprehension questions, expected answers,
  protected claims, and specific defects in the oracle. Unknowns can be correct
  answers; irrelevant topics are N/A with a reason.
- Run an editor with the target instructions and exact allowed-file manifest.
  Run separate original/revised readers with no inherited conversation and only
  their respective artifact and declared accessible sources. Use identical reader
  settings. A separate fixture-capable general-purpose grader sees the oracle,
  sources, artifacts, answers, and editor trace; the repository's `eval-grader`
  role cannot substitute because it is prohibited from opening fixtures.
- Capture exact prompts at submission, model/settings, source revision/hashes,
  allowed-file manifests, before/after files, raw tool traces, reader answers,
  and per-assertion PASS/FAIL/PARTIAL with evidence. Shared filesystem access is
  not isolation: audit reads against manifests and invalidate leaks or incomplete
  traces. Do not reconstruct unavailable prompt evidence after the run.
- When native dispatch payloads are encrypted, retain the exact pre-dispatch
  plaintext, its hash, the dispatch receipt and linkage to the resulting run.
  Audit complete tool/message records against the manifests. Opaque transport
  alone is a recorded limitation, not proof of missing evidence; absent,
  reconstructed or mismatched required records still invalidate the run.
- Create `verification.md` in this feature directory when runs begin, indexing
  evidence under `verification/<run-id>/<scenario>/`. Mark unrun cases explicitly.
  Record authored/executed status separately and retain failed attempts.

Synthetic response success does not certify a live GitHub or Linear connector.
No comparison of approaches A and B is promised; the evals establish whether the
selected implementation meets its stated contract.

