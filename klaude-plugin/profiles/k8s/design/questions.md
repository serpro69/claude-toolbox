# Kubernetes — design question bank

Questions used during idea refinement when the `k8s` profile is active. Ask one per message, per the skill's rule. Order is risk-first — start with questions whose answers most constrain subsequent design choices (cluster topology usually does). Skip any question the user or the codebase has already answered (check `kk:arch-decisions`, `kk:project-conventions`, and any existing `design.md` before asking).

## Cluster topology

- Which Kubernetes minor versions must this feature support? Pin to the cluster's `kubeVersion` if `Chart.yaml` declares one; otherwise the team's shipping target. Name the minor (e.g., `1.29`) — "latest" is not a supported-version statement.
- Single cluster, multi-cluster, or multi-region? How does CI reach each cluster (kubeconfig secret, OIDC-federated token, bastion)?
- Managed (EKS, GKE, AKS, DOKS) or self-hosted? Any vendor addons the design must coexist with (AWS VPC CNI, GKE Autopilot constraints, Azure Policy, etc.)?

## GitOps and delivery

- GitOps stack: ArgoCD, Flux, or imperative (`kubectl apply` / `helm upgrade` from CI)? If GitOps, which `Application` / `Kustomization` / `HelmRelease` owns these manifests?
- Promotion model — per-env branches, per-env overlays, per-env values files, or an ApplicationSet with a single source of truth?
- Sync posture — prune-on-delete, sync waves / phases, rollback trigger (manual revert vs automated on health failure)?

## Secrets strategy

- Secret source: External Secrets Operator, Sealed Secrets, Vault Agent Injector, cluster-native `Secret` resources, or cloud-provider-integrated (IRSA / Workload Identity / Azure AD Workload Identity)?
- Rotation frequency and rotation owner — human-driven, operator-managed, or credential-less (workload identity)?
- Blast radius — per-namespace, per-cluster, cross-cluster? Who has read access to the decrypted secret at rest?

## Multi-tenancy

- Single namespace, namespace-per-tenant, or shared namespace with RBAC boundaries?
- NetworkPolicy posture — default-deny plus explicit allow edges, default-allow, or no NetworkPolicy (accepted risk)?
- Admission-time guardrails — `ResourceQuota` / `LimitRange` per namespace, PSA labels (`restricted` / `baseline` / `privileged`), policy engine (Kyverno, Gatekeeper) with enforced rules?

## Observability

- Logs — cluster-scoped collector (Fluent Bit, Vector) or per-app sidecar? JSON structured output required for the log pipeline to parse fields?
- Metrics — Prometheus scrape via `ServiceMonitor` / `PodMonitor`, annotation-based pull, or push to a collector? Custom metrics beyond the Go/JVM/Node defaults?
- Traces — OpenTelemetry SDK, vendor agent (Datadog, New Relic), or none? Sampling target and propagation format?
- Alerts — delivery channel (on-call rotation, Slack, paging) and runbook owner. An alert without a runbook is toil, not signal.

## Reliability and rollback

- SLO targets — explicit availability and latency numbers, or inherited from a parent service? How is SLO burn measured and alerted?
- Rollback trigger — `helm rollback`, GitOps sync disable + revert, canary flip, or blue-green cutover?
- Rollout tolerance — RollingUpdate `maxSurge` / `maxUnavailable`, PodDisruptionBudget `minAvailable`, graceful-shutdown window (`terminationGracePeriodSeconds`, `preStop` hook)?
- Failure modes designed against — which of (control-plane outage, single-node loss, zone loss, DNS failure, etcd degradation, noisy neighbor) are in scope, and which are explicitly accepted risks?
