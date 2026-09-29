# Overlay preparation

The release team needs a stable location for the future catalog workload. This
increment creates an empty Kustomize input. It declares no resources, patches,
generators, namespaces, permissions, pods, images, policies, CRDs or feature gates.
Nothing is deployed, and no cluster compatibility check has run.

Workload design, measurements, cluster support and a deployment rollback procedure
are future work. Owner: release team. Next step: supply the workload design and its
validation evidence before populating the overlay. For the preparation-only change,
reverting the empty input has no cluster effect; no runtime rollback command applies.

The platform network policy is inherited as a future prerequisite from
../docs/platform.md, which is shared with these operators. It is not implemented by
this overlay. Document that distinction. No new ADR is needed: this is an already
accepted directory preparation task, with no newly chosen technical alternative.
