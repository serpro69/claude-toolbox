# Local-document scenarios

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
