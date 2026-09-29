# Catalog overlay

The release team needs a stable location for the future catalog workload. This
preparation-only change creates an empty Kustomize input at
[`infra/kustomization.yaml`](../infra/kustomization.yaml), containing `resources: []`.
It deploys nothing. For example, reverting this empty input changes no cluster
resources, so there is no runtime rollback command for this increment.

The [preparation decision](../infra/decision.md) assigns the release team the next
step: supply the workload design and its validation evidence before populating the
overlay. Workload design, measurements, cluster support and a deployment rollback
procedure remain future work. No cluster compatibility check has run.

## RBAC decision rationale

N/A — the empty overlay declares no permissions, ServiceAccounts or namespaces.
There are no RBAC subjects, scopes, verbs, resources or escalation-shaped grants
to explain, and no narrower permission alternative was selected or rejected in
this preparation task. Pod Security Standards posture is N/A because the overlay
neither creates nor occupies a namespace.

## Rollback runbook

N/A — nothing is deployed, so runtime trigger conditions, rollback commands and
post-rollback cluster verification do not apply. Reverting the empty input has no
cluster effect, downstream runtime blast radius or irreversible runtime step.
The release team owns the future deployment rollback procedure; the supplied
evidence does not establish its commands, triggers or verification targets.

## Resource-baseline documentation

N/A — no pods or images are declared, so there are no CPU or memory requests,
limits, headroom choices, QoS class, replicas, autoscaler or manual scaling trigger
for this increment. OOM behavior and recovery are also N/A without a workload.
There is no measured workload baseline in the supplied evidence. The release team
must provide workload design and validation evidence before populating the overlay.

## Cluster-compat matrix

No Kubernetes minor version is claimed as supported or validated: no cluster
compatibility check has run. Establishing cluster support is future work owned by
the release team and requires validation evidence before the overlay is populated.

N/A — the empty input declares no cluster resources or API versions, so there is
no API deprecation horizon or CRD dependency for this increment. It declares no
feature gates; admission-configuration and cluster-runtime dependencies are not
established for the future workload by the supplied evidence.

## NetworkPolicy / egress posture

The inherited [platform rule](platform.md), shared with operators, requires a
reviewed network policy before future workloads deploy. The platform team owns
enforcement details. This preparation task grants no exception and does not
implement or claim an installed policy for the future catalog workload.

N/A — the empty overlay has no workloads or policies whose current ingress or
egress rules can be described. The supplied platform reference does not specify a
default posture, allowed ingress, DNS or managed-service egress, metadata-endpoint
handling, CNI enforcement, service-mesh interaction or known traffic gaps. These
details remain unsupported; the platform team must supply the enforcement details
needed for the required policy review before future deployment.
