# Catalog overlay

This change reserves a stable location for the future catalog workload. Nothing
is deployed: [the Kustomize input](../infra/kustomization.yaml) contains
`resources: []`, with no resources, patches or generators. The
[accepted preparation decision](../infra/decision.md) defines this scope and the
remaining work; this increment makes no new architecture decision.

## RBAC decision rationale

N/A — the overlay declares no identities, permissions or namespaces, so there are
no RBAC subjects, scopes, verbs, resources, escalation permissions or alternatives
to explain. Pod Security Standards levels, version labels, warning/audit modes and
exceptions are N/A because this increment creates or occupies no namespace.

## Rollback runbook

N/A — nothing is deployed, so there are no runtime rollback triggers, commands or
cluster-state verification targets. Reverting the empty input has no cluster
effect, downstream runtime impact or irreversible runtime step.

The release team owns this change. A deployment rollback procedure and validation
remain future work; the supplied sources support no runtime rollback command.

## Resource-baseline documentation

N/A — the overlay declares no pods or images, so there are no CPU or memory
baselines, headroom choices, requests/limits, quality-of-service (QoS) class,
replicas, autoscaling, manual scaling triggers or out-of-memory recovery behavior
to document. Workload measurements and capacity planning remain future work.

## Cluster-compat matrix

N/A — the empty input declares no cluster resources, Kubernetes API versions,
custom resource definitions (CRDs) or feature gates. No cluster compatibility
check has run, so no supported Kubernetes minor-version range can be stated.

API stability and deprecation dates, minimum CRD operator versions, feature-gate
stability, admission configuration and cluster-runtime requirements are not
established. Cluster support and validation evidence remain future work.

## NetworkPolicy / egress posture

The inherited [platform rule](platform.md) requires a reviewed network policy
before future workloads deploy. The platform team owns enforcement details. This
overlay implements no policy. Preparation grants no exception and provides no
evidence of an installed policy for the future catalog workload.

N/A — this increment declares no workload or policy to describe. The supplied
sources do not establish default traffic posture, ingress selectors, DNS or
managed-service egress, metadata endpoint access, network-plugin (CNI)
enforcement, service-mesh interaction or unrestricted traffic paths. Resolve these
details with the platform team for the future workload.

## Next step

The release team must supply the workload design and its validation evidence
before populating the overlay. That future work includes measurements, cluster
support and the deployment rollback procedure, alongside the inherited network
policy prerequisite.
