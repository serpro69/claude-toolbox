# Catalog overlay

This preparation-only change gives the release team a stable location for the
future catalog workload. The [Kustomize input](../infra/kustomization.yaml) contains
`resources: []` and declares no resources, patches or generators. Nothing is
deployed. The [preparation decision](../infra/decision.md) records the accepted
scope; no new technical alternative was chosen and no new ADR is needed.

## RBAC decision rationale

N/A — the empty overlay creates no identities, permissions or namespace.
There are no permission subjects, scopes, verbs, resources or escalation-shaped
grants to justify, and no RBAC alternatives were selected. Pod Security Standards
enforcement, version, warning and audit labels are N/A because this increment
neither creates nor occupies a namespace.

## Rollback runbook

N/A — nothing is deployed, so runtime rollback triggers, commands, verification
targets, downstream blast radius and irreversible runtime steps do not apply.
Reverting the empty input has no cluster effect. The release team owns the future
deployment rollback procedure; workload design and validation evidence are required
before the overlay is populated. No runtime rollback command is supplied for this
preparation task.

## Resource-baseline documentation

N/A — this increment defines no pods, images or workload resources.
Measured CPU and memory baselines, headroom, requests and limits, QoS class,
capacity and scaling assumptions, and OOM behavior or recovery are not established.
Workload design and measurements remain future work owned by the release team.

## Cluster-compat matrix

No cluster compatibility check has run, and no supported Kubernetes minor-version
range is established. Cluster support and validation evidence remain future work
owned by the release team.

N/A — this empty overlay declares no cluster resource API versions, CRDs or feature
gates, so their version and deprecation requirements do not apply to this increment.
Admission-configuration and cluster-runtime dependencies are not established for
the future workload.

## NetworkPolicy / egress posture narrative

The [platform rule](platform.md) is inherited as a future deployment prerequisite:
future workloads require a reviewed network policy before deployment. The platform
team owns enforcement details. This preparation task grants no exception and does
not implement or establish that a policy is installed for the catalog workload.

N/A — the empty overlay declares no policies or workloads whose traffic it controls.
The future default posture, allowed ingress, DNS and managed-service egress,
metadata-endpoint treatment, CNI enforcement, service-mesh interaction and any
intentional traffic gaps are not specified in the supplied evidence. Enforcement
details remain with the platform team for the required policy review.

## Before populating the overlay

The release team must supply the workload design and its validation evidence.
The future work includes measurements, cluster support and a deployment rollback
procedure. The inherited network-policy prerequisite must be met before deployment.
