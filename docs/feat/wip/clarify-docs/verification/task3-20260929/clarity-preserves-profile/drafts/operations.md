# Catalog overlay

The catalog overlay reserves a stable location for the future catalog workload.
This is a preparation-only change: [the Kustomize input](../infra/kustomization.yaml)
contains `resources: []` and declares no resources, patches or generators. Nothing
is deployed. The [accepted preparation decision](../infra/decision.md) records the
scope and follow-up work; this increment makes no new architecture decision.

## RBAC decision rationale

N/A — the empty overlay declares no identities, permissions or namespaces. There
are no permission subjects, scopes, verbs, resources or escalation-shaped grants to
explain, and no narrower RBAC alternative was selected. Pod Security Standards
enforcement, version, warning and audit labels and exceptions are N/A because this
increment creates or occupies no namespace.

## Rollback runbook

N/A — nothing is deployed, so this increment has no runtime rollback triggers,
commands or cluster-state verification targets. Reverting the empty input has no
cluster effect, downstream runtime impact or irreversible runtime step.

The release team owns the preparation change. A deployment rollback procedure and
its validation are future work to accompany the workload design; no runtime
rollback command is supported by the current evidence.

## Resource-baseline documentation

N/A — the overlay declares no pods or images. There are no measured CPU or memory
baselines, headroom choices, resource requests or limits, QoS class, replicas,
autoscaler, manual scaling trigger or workload OOM recovery behavior to document.
Workload measurements and capacity planning remain future work.

## Cluster-compat matrix

N/A — the empty input declares no cluster resources, Kubernetes API versions,
CRDs or feature gates. No Kubernetes minor version has been validated for this
workload, and no supported range can be stated. API graduation and deprecation
horizons, minimum CRD operator versions, feature-gate graduation, admission
configuration and cluster-runtime requirements are not established by this
preparation task. Cluster support and validation evidence remain future work.

## NetworkPolicy / egress posture

The inherited [platform rule](platform.md) requires a reviewed network policy
before future workloads deploy. The platform team owns enforcement details. This
overlay implements no network policy, and preparation grants no exception or
evidence that a policy is installed for the future catalog workload.

N/A — this increment declares no workload or policy whose default posture,
ingress selectors, DNS or managed-service egress, metadata endpoint access, CNI
enforcement, service-mesh interaction or unrestricted traffic paths can be
described. Those details are unsupported by the supplied sources and must be
resolved with the platform team for the future workload.

## Next step

The release team must supply the workload design and its validation evidence
before populating the overlay. That future work includes measurements, cluster
support and the deployment rollback procedure, alongside the inherited network
policy prerequisite.
