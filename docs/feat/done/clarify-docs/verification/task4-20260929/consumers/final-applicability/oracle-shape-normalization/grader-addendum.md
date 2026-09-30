# Additional oracle-shape normalization audit

The canonical consumer oracles changed again after this audit started. Prior snapshots remain immutable. This directory preserves before.json, after.json and exact delta.diff for each of the four document-producing consumer cases, plus hashes in manifest.json.

Inspect all four changes independently. Determine whether baseline_defects changed from a scalar string to a one-element array whose element equals the previous string exactly, and whether every other field is unchanged relative to the preserved before version. The before files for the two WIP cases are the corrected-source snapshots already supplied to this audit; the other two before files are their executed oracles.

Add an oracle_shape_normalization verdict with per-case evidence and any effect on comprehension, protected claims, orientation, acceptance and prior-result applicability. Do not assume this is metadata-only from its description. No editor or reader ran against these normalized oracle bytes. Continue the original WIP-answer and shared-source applicability assessment, preserving initial failures and all prior grades. Do not replace any previous snapshot with the after file.
