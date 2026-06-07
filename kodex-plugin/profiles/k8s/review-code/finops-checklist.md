# Kubernetes — FinOps Checklist

Applied conditionally — load when the diff touches observability configuration, workload resources with cost-sensitive fields, or autoscaling resources (see `index.md`). Focuses on what a reviewer can catch in a diff that would cause avoidable cloud or vendor spend.

## Contents

- Observability cost traps (generic patterns, Datadog, Prometheus/Grafana, OpenTelemetry Collector)
- Resource right-sizing signals
- Autoscaling hygiene
- Storage lifecycle
- Namespace cost attribution
- Idle and orphaned resources

## Observability cost traps

The single largest surprise bill in Kubernetes clusters comes from observability tooling — not from compute. Metrics, logs, and traces are billed per volume ingested, and Kubernetes generates enormous volumes by default. The patterns below are vendor-neutral; vendor-specific signals follow in dedicated sub-sections.

### Generic patterns

- **Included vs billed metrics.** Most observability vendors distinguish between metrics included with infrastructure pricing and metrics billed per unique time series. The boundary varies by vendor (see sub-sections), but the pattern is universal: a component collected via the vendor's native/curated integration produces included metrics; the same component collected via a generic scrape mechanism produces billed metrics. Switching collection type — without changing what is monitored — can eliminate the billed-metrics line item entirely. Flag generic scrape configurations on components that have a native integration available as a P2 finding.
- **Auto-discovery leaks.** Blanket auto-discovery (scraping every pod that exposes a metrics endpoint) catches system pods the team did not intend to monitor — kube-dns, node-local-dns, CNI agents, cloud-provider controllers. Each scraped pod contributes billed metrics. Flag blanket auto-discovery without an explicit include/exclude filter as a P2 finding. Prefer disabling auto-discovery and using explicit per-component collection configuration.
- **Double collection.** A pod with both a vendor-specific collection annotation and a generic `prometheus.io/scrape: "true"` annotation may be scraped twice — once by the vendor's autodiscovery and once by a generic Prometheus scraper — producing duplicate metrics under different prefixes. Flag pods with both vendor-specific and generic scrape annotations as a P3 finding. Disable the generic annotation on pods that have explicit vendor-specific collection configured.
- **Metric include lists.** Generic scrape configurations should always specify an explicit metric include list limited to what monitors and dashboards actually reference. An open-ended scrape (no filter, or a catch-all like `.*`) collects every metric family the endpoint exposes. Components like Envoy, Istio sidecars, and API gateways emit hundreds of families with high tag cardinality. Flag open-ended scrape configs as P1 when the target is a known high-cardinality emitter, P2 otherwise.
- **Log volume.** Collect-all-logs configuration ships every container's stdout/stderr to the vendor. Verify that high-volume emitters (debug-level logs, proxy access logs, audit logs) are filtered at the agent level or excluded. Unfiltered log collection from a busy proxy can exceed the cost of the compute it runs on. If the vendor supports index tiers (hot vs cold storage, online vs archive), verify that low-urgency logs are routed to a cheaper tier. A diff that adds a new high-throughput workload without a log routing rule is a P3 finding.
- **Per-environment controls.** Non-production environments that mirror production's full observability config pay the same per-metric and per-log-byte cost for data nobody monitors. Flag identical observability config across environments as a P2 finding. Common pattern: disable metric collection in non-production, keep logs for debugging.

### Datadog

Datadog bills per host (infrastructure metrics included) plus per custom metric. The line between "integration metric" (free) and "custom metric" (billed) is the single most important cost lever.

- **Native check vs `openmetrics`.** A component scraped via the Datadog agent's native integration check (e.g., `cert_manager`, `external_dns`, `envoy`, `argocd`) produces integration metrics — included with host pricing. The same component scraped via a generic `openmetrics` check annotation produces custom metrics — billed. Flag any `ad.datadoghq.com/<container>.checks` annotation using the `openmetrics` check type on a component that has a native Datadog integration as a P2 finding. Common candidates: cert-manager, external-dns, CoreDNS, Redis, nginx, ArgoCD, Envoy.
- **`prometheusScrape.enabled: true`.** Enables Prometheus auto-discovery — every pod with `prometheus.io/scrape: "true"` is scraped as custom metrics via a generic `openmetrics` check. This catches GKE/EKS system pods (kube-dns, node-local-dns, CNI agents like anetd) that the team never intended to monitor. Flag as P2 unless the diff also includes `containerExclude` / `containerExcludeMetrics` filters. Prefer `prometheusScrape.enabled: false` with explicit per-component `ad.datadoghq.com` annotations using native check types.
- **Double collection.** A pod with both `ad.datadoghq.com/*` and `prometheus.io/scrape: "true"` may be scraped twice — once by autodiscovery (native or openmetrics) and once by Prometheus auto-discovery. The autodiscovery annotation takes precedence for the Datadog check, but Prometheus auto-scrape fires independently. Flag as P3. Set `prometheus.io/scrape: "false"` on pods that have explicit Datadog annotations.
- **`metric_patterns` / `metrics` include lists.** When using native checks, some (e.g., `envoy`) collect all metrics from their curated set by default — use `metric_patterns.include` to limit to what monitors/dashboards reference. When using `openmetrics` checks, always provide an explicit `metrics` list; omitting it scrapes everything the endpoint exposes. Flag open-ended Datadog scrape configs as P1 for high-cardinality targets (Envoy, Istio, NGINX Ingress Controller), P2 otherwise.
- **KSM Core collector scope.** `kubeStateMetricsCore.enabled: true` collects Kubernetes state metrics for all resource types by default. KSM metrics are integration metrics (free with host pricing), so collector filtering has no billing impact — but reducing collector scope lowers agent memory and etcd load. Do NOT use `clusterAgent.confd` to override KSM Core config unless confirmed compatible with the chart version — it can conflict with the Helm-native auto-generated config and break cluster check dispatch.
- **`ignoreAutoConfig`.** Controls which auto-configured checks the agent skips. A component in `ignoreAutoConfig` will not be auto-discovered even if its container name matches the agent's built-in `auto_conf.yaml`. Conversely, removing a component from `ignoreAutoConfig` re-enables auto-discovery, which may create an unintended native check alongside an existing explicit annotation. Review changes to this list for unintended side effects.
- **Per-environment Helm values.** Datadog Helm charts support per-environment values files (`values-preview.yaml`, `values-production.yaml`). Non-production overrides that disable metric collection: `kubeStateMetricsCore.enabled: false`, `containerExcludeMetrics: "image:.*"`, `processAgent.enabled: false`, `prometheusScrape.enabled: false`. Flag environments that share the production `values.yaml` without overrides as P2.
- **`containerCollectAll: true`.** Ships all container logs. Verify high-volume log emitters are filtered via `containerExclude` / `containerExcludeLogs` or namespace-level exclusion rules. If Datadog Online Archives or Flex Logs is available, verify that low-urgency logs are routed to a cheaper tier.

### Prometheus / Grafana stack

In self-hosted Prometheus (or Grafana Cloud with usage-based billing), cost is driven by active time series count and storage retention. Grafana Cloud bills per active metric series and per log GB ingested.

- **ServiceMonitor / PodMonitor without `metricRelabelings`.** A `ServiceMonitor` that scrapes an endpoint without dropping unused metrics collects everything the target exports. Flag `ServiceMonitor` or `PodMonitor` resources without a `metricRelabelings` section as P3 for low-cardinality targets, P2 for known high-cardinality targets (Envoy, Istio, etcd). Use `action: keep` on `__name__` in `metricRelabelings` with an explicit regex to allowlist only the metric families referenced by alerts and dashboards.
- **Namespace-scoped vs cluster-wide selectors.** A `ServiceMonitor` with `namespaceSelector.any: true` or broad `matchLabels` can scrape targets the team did not intend to monitor. Prefer namespace-scoped monitors that explicitly name their target namespaces.
- **`scrape_interval` lower than needed.** A 5s scrape interval on a metric that only changes every minute produces 12x the time series churn with no information gain. Review `interval` overrides on `ServiceMonitor` and `PodMonitor` resources — the Prometheus global default (usually 30s or 60s) is appropriate for most workloads. Flag sub-15s intervals as P3 unless the metric feeds a latency-sensitive alert.
- **`PrometheusRule` recording rules and federation cardinality.** `PrometheusRule` resources that define recording rules aggregating by high-cardinality labels (`pod`, `container`, `instance`) without dropping those labels in the output produce time series at the same cardinality as the input — the rule adds storage cost with no cardinality reduction. Federation that pulls unaggregated metrics from leaf Prometheus instances to a central instance multiplies storage. Flag recording rules that preserve all input labels as P3.
- **Retention and storage class.** `prometheus.server.retention` and `prometheus.server.retentionSize` control how long data is kept. Long retention (>30d) on high-IOPS storage classes (SSD/gp3) is expensive. Verify that retention matches operational needs, and that the storage class matches the access pattern (cold data can use HDD/sc1).

### OpenTelemetry Collector

The OTel Collector is a vendor-neutral pipeline — cost depends on what flows through it and where it lands. The Collector itself has no billing, but the backends it exports to do.

- **Missing `filter` processor.** A Collector pipeline without a `filter` processor forwards everything the receiver collects. For a `prometheus` or `kubeletstats` receiver, "everything" includes all system metrics from every scraped target. Flag pipelines without a `filter` processor as P3. Use `filter/metrics` with `exclude` rules to drop metric families not referenced by downstream dashboards/alerts.
- **`batch` and `memory_limiter` processors.** The `memory_limiter` processor prevents the Collector from OOMKilling under high load; `batch` processor reduces export API call volume (and therefore cost for pay-per-request backends). A pipeline without `memory_limiter` risks node OOM; a pipeline without `batch` pays per-event API costs. Flag the absence of either as P2.
- **Exporter endpoint costs.** Each exporter destination has its own billing model. A pipeline with multiple exporters (e.g., `otlp` to Grafana Cloud + `datadog` to Datadog) pays both vendors for the same data. Flag multi-exporter pipelines as P3 — verify the team intends to pay for parallel ingestion.
- **`k8sattributes` processor cardinality.** The `k8sattributes` processor enriches telemetry with Kubernetes metadata (pod name, namespace, node, labels). Extracting high-cardinality attributes (e.g., all pod labels, all annotations) inflates time series count at the backend. Only extract attributes referenced by downstream queries.

## Resource right-sizing signals

These are signals visible in a manifest diff — not runtime profiling. The goal is to catch obviously wrong or missing resource specifications before they reach a cluster.

- **No requests/limits at all.** Already covered by `quality-checklist.md` for correctness (BestEffort QoS, OOM risk). The FinOps angle: pods without `resources.requests` are invisible to cluster autoscaler sizing decisions and capacity planning tools. They consume resources that the autoscaler does not account for, leading to over-provisioned node pools.
- **Requests dramatically lower than limits.** A container with `requests.cpu: 10m` and `limits.cpu: 4` (400x ratio) is asking for almost nothing but reserving the right to burst to 4 cores. In clusters with bin-packing autoscalers, this causes nodes to appear full of low-request pods while actual utilization is far higher. Flag request-to-limit ratios above 10x as a P3 finding — the team should confirm whether the workload genuinely bursts or the requests are placeholder values.
- **Ephemeral storage without limits.** Pods writing to `emptyDir` or container filesystems without `resources.limits.ephemeral-storage` can exhaust node disk, triggering eviction storms and node-pool scaling. Already a correctness concern in `quality-checklist.md`; the cost angle is the cascading node scaling.

## Autoscaling hygiene

- **HPA without resource requests.** `HorizontalPodAutoscaler` targeting CPU or memory utilization requires `resources.requests` on the target container — the utilization percentage is calculated as `current / request`. Missing requests make the HPA metric undefined. Kubernetes fills in `limits` as `requests` when only limits are set, but the intent should be explicit.
- **HPA `minReplicas` higher than needed.** An HPA with `minReplicas: 10` on a workload that idles at 2% utilization keeps 10 pods running around the clock. Flag `minReplicas` values without evident rationale (cold-start latency, PDB requirements, traffic minimums) as P3. This is a judgment call — the reviewer should ask "why this minimum?", not mandate a number.
- **Cluster Autoscaler (CA) / Karpenter configuration.** When this checklist is already loaded via another trigger (HPA, VPA, observability config), review node pool sizing (`minNodeCount`, `maxNodeCount`) in IaC or in-cluster provisioner resources. Flag node-pool minimum counts set above 1 without documented rationale (HA requirements, minimum capacity for system pods) as P3. For Karpenter, consolidation is the primary cost-savings driver — flag `NodePool` resources with consolidation disabled (`consolidationPolicy: WhenEmpty` without `consolidateAfter`, or missing `disruption` block entirely) as P2 unless justified.
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
