# Plugin Dependency Graph

The complete dependency graph of `klaude-plugin/`, built by [`cmd/plugin-graph`](architecture.md) and regenerated on every docs build, so it always reflects the current plugin.

!!! note "Reference, not orientation"
    This is the full graph — every node and edge (~90 nodes). It is meant for **exploration**, not first-contact orientation. Use the pan/zoom controls to navigate. For the conceptual model of how the artifact types relate, start with [Architecture → Plugin Graph Analysis](architecture.md), which collapses the six edge types onto a handful of artifact types.

!!! info "Generated"
    This diagram is produced by `make plugin-graph-docs`. Don't edit it by hand — change the plugin (or the tool) and regenerate.

--8<-- "contributing/_generated/plugin-graph-full.md"
