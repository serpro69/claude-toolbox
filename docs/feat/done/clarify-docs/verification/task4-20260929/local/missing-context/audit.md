# Coordinator trace audit

The editor and two readers executed in separate fresh general-purpose sessions with `fork_turns="none"`. Their manifests, exact requests, actual metadata and visible traces are preserved.

Editor trace order is request, copied skill, full shared procedure, target and requirement plus an attempted read of the expressly allowed missing `retention.md`, selected-guide patch, and guide verification. The missing read returned a missing-file error. The editor did not create that file or invent a duration. Only `guide.md` changed according to recorded hashes. Each reader accessed only its request and own guide, without the missing reference, source-only requirement, oracle or other version. Captured calls have matching results.

Shared filesystem controls rely on prompt manifests and trace inspection. Initial request reads may run login-shell initialization before learning the `login:false` instruction; its denied logging warning shows no subject-content disclosure. AI-reader results do not establish human comprehension. Fidelity and question verdicts are reserved for the independent grader.
