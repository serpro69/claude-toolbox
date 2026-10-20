# Kubernetes support retention

Archive the entire `docs/feat/done/kubernetes-support/` directory. Preserve its
nested `kubernetes-support/.sessions/` path exactly: six design/review/plugin-root
probe transcripts total 340,093 bytes. Flattening it would break provenance.

Keep root design/implementation/tasks, repository ADRs 0001–0004, the successor
`kubernetes-support-v2` planning record, and current maintained profile/detection/
test assets in Git. They carry the durable architectural decisions and follow-up.

The original task record marks all phases and the post-close amendment handoff
done. Task 18 records 32 structure-test cases/134 assertions and explains which
checks were structural or earlier synthetic smoke coverage. Preserve those
specific claims; this archival operation neither reruns Kubernetes tools nor
certifies deployment behavior. Original pending/deferred narratives retain their
dated context; Task 20 records their transfer to the v2 feature.

The six transcripts are historical discussion and substitution-probe evidence.
There is no standalone runtime helper to extract. The current profile convention
and ADRs retain the operative lesson about plugin-root substitution rather than
depending on readers rediscovering it from a transcript.

Locator:
`payload/docs/feat/done/kubernetes-support/kubernetes-support/.sessions/`.
That nested session directory is an eventual capture-cleanup candidate, while
the plans, ADRs and maintained profiles/tests should remain.
