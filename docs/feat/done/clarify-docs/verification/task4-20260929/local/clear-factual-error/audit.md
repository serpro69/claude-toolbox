# Coordinator trace audit

All three sessions were fresh default general-purpose agents with `fork_turns="none"`, executed serially within the local batch. The editor read the copied skill, full shared procedure, guide, requirement and source in that order before using native `apply_patch`. Its sole change replaced the maximum default of 60 with 90, then it read the guide back. Hashes show all other files unchanged and no new artifact.

Original and revised readers read only their own request and guide. Neither accessed the source-only files, oracle, skill or other version. Captured tool calls have matching results. Exact metadata and final outputs are saved; no settings were inferred. The grader will score the fixed questions and predeclared factual defect independently.

Limits: prompt manifests and trace inspection operate on a shared filesystem, not an OS-isolated one. Initial request reads can trigger denied login-shell logging before the `login:false` instruction is available; no subject content outside the manifests was observed. Results concern AI-reader behavior only.
