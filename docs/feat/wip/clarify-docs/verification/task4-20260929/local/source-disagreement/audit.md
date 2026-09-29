# Coordinator trace audit

Editor and both readers executed as fresh default general-purpose agents with `fork_turns="none"`, one local child at a time. Requests and session records preserve exact boundaries and observed model/settings.

The editor loaded the copied skill and full shared procedure before reading `guide.md`, `requirements.md` and `prep.py`. It then patched only `guide.md` and read that revision back. Both readers read only their request and own guide; neither followed the guide's source links beyond its allowed reading path. No source-only context, oracle or other version was accessed. Tool calls and results are paired in the captured traces.

Original/revised hashes show only the selected guide changed, with no extra artifact. The guide retains the mandatory requirement while documenting the inspected behavior and assigning reconciliation. The grader assesses semantic fidelity and question scores independently.

Limits: prompt manifests plus trace review provide shared-filesystem controls, not OS isolation. Initial request reads can invoke login-shell startup before seeing the `login:false` instruction; denied navi logging produces no subject-content evidence. Reader results describe AI-reader behavior only.
