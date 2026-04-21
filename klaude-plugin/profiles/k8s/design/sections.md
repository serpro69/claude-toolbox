# Kubernetes — required design sections

Every `design.md` for a K8s-shaped feature must include the five sections below. Omit none; if a section genuinely does not apply, state so explicitly with a one-line justification — silent omissions hide scope gaps, and a reviewer (or `review-spec`) cannot tell absence-by-intent from absence-by-oversight.

Section order is not mandated; the sections must all be present. Cross-reference between sections liberally where a decision in one drives a constraint in another (e.g., a PSA level in **Security posture** constrains `readOnlyRootFilesystem` defaults in **Reliability posture**).

## Cluster-compat matrix

- Minimum and maximum Kubernetes minor versions supported, with rationale. Pin to a specific minor (`1.28` / `1.29`) — "latest" is not a support statement.
- Required in-cluster addons with pinned minimum versions (e.g., `cert-manager ≥ 1.13`, `metrics-server ≥ 0.7`, `CNI with NetworkPolicy support`).
- Third-party CRDs the feature installs or consumes, with exact installed versions. CRD schemas are version-pinned per operator release.
- Deprecation horizon — which API versions used by the feature are already `Deprecated` in the target minor, and the planned migration path before they are removed.

## Resource budget

- Workload sizing — replica count range, requests and limits per container (CPU, memory, ephemeral-storage where relevant). Justify the request (baseline steady-state) and the limit (burst ceiling / OOM guard) separately.
- Autoscaling bounds — HPA `minReplicas` / `maxReplicas` with scale signal (CPU, memory, custom metric); VPA mode (`Off` / `Auto` / `Initial`) if enabled.
- Storage — `PersistentVolumeClaim` class, size, access mode; expected growth rate; backup/restore SLO for stateful data.
- Blast-radius estimate — if this feature consumes its whole budget (bad deploy, autoscaling runaway), which other workloads in the cluster starve first? Name them or declare the headroom.

## Reliability posture

- `PodDisruptionBudget` declaration — `minAvailable` / `maxUnavailable` value and the rationale tying it to the SLO.
- Probes — `readinessProbe`, `livenessProbe`, and (for slow-starting workloads) `startupProbe` with thresholds. Distinguish the three roles: readiness gates traffic; liveness restarts; startup delays liveness enforcement until the app is up.
- Graceful shutdown — `terminationGracePeriodSeconds` value and `preStop` hook semantics (drain, flush, deregister).
- Spreading — pod anti-affinity rules and `topologySpreadConstraints` across zones / nodes for multi-replica workloads.
- Rollout strategy — `RollingUpdate` with `maxSurge` / `maxUnavailable` tuned for the workload, or `Recreate` with declared downtime window. Include rollback procedure and the signal that confirms rollback success.

## Security posture

- RBAC — ServiceAccount scope (namespace, cluster); enumerated Role/ClusterRole verbs with a one-line justification per verb; explicit list of rejected over-privileged alternatives (e.g., "not granting `*` on `secrets` because X").
- NetworkPolicy — default-deny baseline plus explicit allowed edges; cross-namespace allows called out individually; egress policy for external-facing traffic (DNS, vendor APIs).
- Pod Security — PSA level (prefer `restricted`); non-root UID; `readOnlyRootFilesystem`; dropped capabilities (`drop: [ALL]` + minimal `add:`); `seccompProfile` (`RuntimeDefault` preferred).
- Secrets — source (ESO / Sealed / native / workload identity); rotation frequency and owner; read access at rest (who / what service accounts).
- Supply chain — image digest-pinning policy; signature verification (cosign, notary); base-image selection and CVE-gating workflow; admission-time enforcement (if any).

## Failure-mode narrative

- At least three concrete failure modes the feature must survive. For each: expected user-visible impact, detection signal (metric, log, alert), recovery path, and the person or team on the hook.
  - Examples: one node drained during rollout; one zone lost; stateful backend latency spike; CRD controller unreachable; image-pull throttling at registry.
- Explicit out-of-scope failure modes — what the feature does NOT promise to handle, with the risk accepted and by whom.
- Rollback procedure — who triggers it (on-call, release engineer), how (GitOps revert, `helm rollback`, canary flip), and the observable signal that confirms rollback succeeded. "Revert the commit" is not a rollback procedure; name the mechanism and the verification.
