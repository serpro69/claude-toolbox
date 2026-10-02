# Catalog overlay

The `infra/` directory reserves a stable location for the future catalog workload.
The current [Kustomize input](../infra/kustomization.yaml) contains `resources: []`;
it declares no resources, patches or generators. As recorded in the
[preparation decision](../infra/decision.md), nothing is deployed by this increment.

The release team owns this preparation step. Before populating the overlay, it must
supply the workload design and validation evidence. Workload measurements, cluster
support and a deployment rollback procedure remain future work.

## Permissions and namespace security

N/A — This empty overlay creates no identities, permissions, pods or namespaces, so there are no RBAC grants or scope decisions, escalation permissions, or Pod Security Standards settings to document for this increment.

## Rollback

Reverting the empty input has no cluster effect. The release team owns this
preparation change; it has no deployed resources or downstream runtime changes to
roll back.

N/A — Runtime rollback triggers, commands, verification targets and irreversible steps do not apply because nothing is deployed. A rollback procedure for the future workload is not yet supplied.

## Resource baseline

N/A — With no pods or images declared, this increment has no CPU or memory requests, limits, headroom, QoS class, replicas, autoscaling or OOM behavior to document. Workload measurements and capacity assumptions are not yet supplied.

## Cluster compatibility

No cluster compatibility check has run. The supplied evidence establishes no
supported Kubernetes version range or validation matrix.

N/A — The empty input declares no Kubernetes resource API versions, CRD dependencies or feature gates, so it has no resource API deprecation horizon to document.

Admission-configuration and cluster-runtime requirements for the future workload
are not specified by the supplied evidence.

## Network policy and egress

The inherited [platform rule](platform.md) requires future workloads to have a
reviewed network policy before deployment. The platform team owns enforcement
details. This preparation task grants no exception and does not implement that
policy or establish that one is already installed for the future catalog workload.

The supplied evidence does not specify the default network posture, allowed ingress
or egress, DNS rules, managed-service destinations, metadata-endpoint access, CNI
enforcement, service-mesh interaction or known traffic gaps. These details remain
unresolved for the future workload.
