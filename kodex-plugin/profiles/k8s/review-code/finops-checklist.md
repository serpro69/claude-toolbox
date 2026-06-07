# Kubernetes — FinOps Checklist

Applied conditionally — load when the diff touches observability configuration, workload resources with cost-sensitive fields, or autoscaling resources (see `index.md`). Focuses on what a reviewer can catch in a diff that would cause avoidable cloud or vendor spend.

## Contents

- Observability vendor cost traps
- Resource right-sizing signals
- Autoscaling hygiene
- Storage lifecycle
- Namespace cost attribution
- Idle and orphaned resources

## Observability vendor cost traps

The single largest surprise bill in Kubernetes clusters comes from observability tooling — not from compute. Metrics, logs, and traces are billed per volume ingested, and Kubernetes generates enormous volumes by default.

### Metric collection type matters

- **Native integration checks vs generic scraping.** Vendors like Datadog distinguish between integration metrics (included with host pricing) and custom metrics (billed per metric). A component scraped via a generic `openmetrics` / Prometheus check produces custom metrics; the same component scraped via the vendor's native integration check produces integration metrics (free). Switching check type — without changing what is monitored — can eliminate the entire custom metrics bill. Flag any generic `openmetrics` annotation on a component that has a native integration available as a P2 finding.
- **Prometheus auto-discovery leaks.** When `prometheusScrape.enabled: true` (or equivalent), every pod with `prometheus.io/scrape: "true"` is scraped — including system pods (kube-dns, node-local-dns, CNI agents) that the team did not intend to monitor. Each scraped pod contributes custom metrics. Flag `prometheusScrape.enabled: true` as a P2 finding unless the diff also includes an explicit include/exclude filter. Prefer disabling auto-discovery entirely and using explicit per-component check annotations.
- **Double collection.** A pod with both a vendor-specific annotation (`ad.datadoghq.com/*`) and a `prometheus.io/scrape: "true"` annotation may be scraped twice — once by autodiscovery and once by Prometheus auto-scrape — producing duplicate metrics under different prefixes. The vendor annotation takes precedence for autodiscovery, but Prometheus auto-scrape may still fire. Set `prometheus.io/scrape: "false"` on pods that have explicit vendor check annotations.
- **Metric include lists.** Generic scrape checks should always specify an explicit `metrics` include list (or `metric_patterns`) limited to what monitors and dashboards actually reference. A bare `metrics: [".*"]` or absent `metrics` key scrapes every metric family the endpoint exposes — components like Envoy emit hundreds of families with high cardinality. Flag open-ended scrape configs as P1 when the component is known to emit high-cardinality metrics (proxies, service meshes, API gateways), P2 otherwise.

### Log volume

- **`containerCollectAll: true`** ships every container's stdout/stderr. This is often correct, but verify that high-volume log emitters (debug-level application logs, access logs from proxies, audit logs) are either filtered at the agent level or excluded via container/namespace exclude rules. Unfiltered log collection from a busy proxy can exceed the cost of the compute it runs on.
- **Log index routing.** If the observability vendor supports index tiers (e.g., Datadog Online Archives vs Live), verify that high-volume, low-urgency logs (access logs, health-check logs) are routed to a cheaper index or excluded. A diff that adds a new workload emitting structured access logs without an index routing rule is a P3 finding.

### Per-environment controls

- Non-production environments that mirror production's full observability config pay the same per-metric and per-log-byte cost for data nobody monitors. Flag identical observability config across environments as a P2 finding. Common patterns: disable all metric collection in non-production (`containerExcludeMetrics: "image:.*"`, `kubeStateMetricsCore.enabled: false`), keep logs for debugging.

## Resource right-sizing signals

These are signals visible in a manifest diff — not runtime profiling. The goal is to catch obviously wrong or missing resource specifications before they reach a cluster.

- **No requests/limits at all.** Already covered by `quality-checklist.md` for correctness (BestEffort QoS, OOM risk). The FinOps angle: pods without `resources.requests` are invisible to cluster autoscaler sizing decisions and capacity planning tools. They consume resources that the autoscaler does not account for, leading to over-provisioned node pools.
- **Requests dramatically lower than limits.** A container with `requests.cpu: 10m` and `limits.cpu: 4` (400x ratio) is asking for almost nothing but reserving the right to burst to 4 cores. In clusters with bin-packing autoscalers, this causes nodes to appear full of low-request pods while actual utilization is far higher. Flag request-to-limit ratios above 10x as a P3 finding — the team should confirm whether the workload genuinely bursts or the requests are placeholder values.
- **Ephemeral storage without limits.** Pods writing to `emptyDir` or container filesystems without `resources.limits.ephemeral-storage` can exhaust node disk, triggering eviction storms and node-pool scaling. Already a correctness concern in `quality-checklist.md`; the cost angle is the cascading node scaling.

## Autoscaling hygiene

- **HPA without resource requests.** `HorizontalPodAutoscaler` targeting CPU or memory utilization requires `resources.requests` on the target container — the utilization percentage is calculated as `current / request`. Missing requests make the HPA metric undefined. Kubernetes fills in `limits` as `requests` when only limits are set, but the intent should be explicit.
- **HPA `minReplicas` higher than needed.** An HPA with `minReplicas: 10` on a workload that idles at 2% utilization keeps 10 pods running around the clock. Flag `minReplicas` values without evident rationale (cold-start latency, PDB requirements, traffic minimums) as P3. This is a judgment call — the reviewer should ask "why this minimum?", not mandate a number.
- **Cluster Autoscaler (CA) / Karpenter configuration.** Node pool sizing (`minNodeCount`, `maxNodeCount`) in IaC (Terraform, Pulumi) or in-cluster provisioner resources is a FinOps concern. Flag node-pool minimum counts set above 1 without documented rationale (HA requirements, minimum capacity for system pods) as P3.
- **VPA in `Auto` mode.** `VerticalPodAutoscaler` with `updateMode: Auto` modifies running pod resources. Not directly a cost concern, but an unreviewed VPA can right-size DOWN below what the workload needs under peak load, causing OOMKills and restart storms that trigger node scaling. Flag VPA `Auto` on workloads without established baseline profiling as P3.

## Storage lifecycle

- **PersistentVolumeClaim without `storageClassName`.** Omitting the class falls back to the cluster's default, which on GKE is `standard-rwo` (pd-standard). If the workload needs SSD (`premium-rwo`), the omission is a performance bug; if it doesn't need SSD and someone later changes the default, it's an accidental cost increase. Always explicit.
- **PVC `reclaimPolicy: Retain`.** PVs with `Retain` survive PVC deletion — the disk persists in the cloud provider and continues to be billed until manually deleted. This is the correct choice for data you must preserve, but flag it as a P3 finding when the workload is ephemeral or disposable (CI runners, batch jobs, pre-prod environments).
- **`emptyDir` with `sizeLimit` absent.** A large `emptyDir` (especially with `medium: Memory`) consumes node resources without a visible bound. The `sizeLimit` field caps usage and triggers eviction instead of silent node pressure. Flag missing `sizeLimit` on `medium: Memory` emptyDir as P2 (directly consumes node RAM); on default-backed emptyDir as P3.
- **VolumeSnapshot scheduling.** Snapshot scheduling resources (Velero `Schedule`, Kasten `Policy`, or equivalent vendor CRD) without a retention policy accumulate snapshots indefinitely. Each snapshot is billed at the provider's snapshot storage rate. Flag missing retention/expiry on snapshot schedules as P2.

## Namespace cost attribution

- **Workloads missing cost-attribution labels.** Cluster cost allocation tools (Kubecost, OpenCost, cloud provider cost reports) group by labels. Workloads without `app.kubernetes.io/part-of`, a team label, or an environment label cannot be attributed to a cost center. Already partially covered by `quality-checklist.md` for the recommended label set; the FinOps angle is that unlabeled workloads become unattributable spend. Flag workloads without at least one of `app.kubernetes.io/part-of`, `team`, `cost-center`, or project-equivalent label as P3.
- **Missing `ResourceQuota` or `LimitRange` on shared namespaces.** A namespace shared by multiple teams or workloads without a `ResourceQuota` has no spend ceiling — a single runaway pod can trigger unbounded node scaling. Flag shared namespaces without `ResourceQuota` as P2.

## Idle and orphaned resources

- **Jobs without `ttlSecondsAfterFinished`.** Completed Jobs and their Pods persist in etcd and, depending on log collection config, continue generating log volume. Already covered by `reliability-checklist.md` for correctness; the cost angle is the continued log ingestion and etcd bloat.
- **CronJob execution frequency and log/API churn.** A CronJob running every minute executes 1,440 times per day. Default history limits (3/1) prevent etcd accumulation, but this high-frequency lifecycle generates significant log volume, API churn, and container creation overhead. Flag minute-interval CronJobs without clear operational necessity as P3.
- **LoadBalancer Services that could be ClusterIP.** Each `type: LoadBalancer` Service provisions a cloud load balancer (billed hourly + per-GB processed). Internal-only services that do not need external reachability should use `ClusterIP` or `type: LoadBalancer` with an internal annotation (cloud-provider-specific). Flag `LoadBalancer` Services without a documented external-access requirement as P2.
- **Orphaned PVCs.** A diff that deletes a StatefulSet or Deployment without addressing its PVCs leaves persistent disks running. StatefulSet PVCs are not garbage-collected on scale-down or deletion — they must be explicitly deleted. Flag StatefulSet removal without PVC cleanup as P2.

## Questions to ask

- "What is the monthly cost of the observability config in this diff?" — surfaces metric/log volume assumptions.
- "What happens to this resource's cost when nobody is using it? Does it scale to zero?" — tests idle-cost awareness.
- "If I deploy this to a non-production environment, does it carry the same observability cost as production?" — tests per-environment controls.
- "Who pays for this workload, and can they see the bill?" — tests cost attribution.
