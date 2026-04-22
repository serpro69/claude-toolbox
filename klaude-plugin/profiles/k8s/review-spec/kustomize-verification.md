# Kustomize-specific spec verification

Verification patterns for comparing Kustomize implementations against design specifications. Load alongside `type-mapping.md` when Kustomize signals are present in the diff.

## Base/overlay structure

The design's environment strategy dictates the expected directory layout:

- **Environments match overlays.** If the design names environments (dev, staging, production), each should have a corresponding overlay directory. A design-described environment with no overlay → `MISSING_IMPL`.
- **Base completeness.** Resources shared across all environments (per the design) should live in the base, not duplicated per overlay. A resource the design describes as common that only exists in one overlay → `SPEC_DEV` (wrong location, even if the resource exists).
- **Overlay minimality.** Overlays should contain only environment-specific deltas. A resource fully duplicated in an overlay (not patched, just copied) when the design describes it as shared → `SPEC_DEV`.

## Patch targets

For each per-environment override the design describes, verify a corresponding patch exists:

| Design override | Expected patch | Finding type if mismatch |
|---|---|---|
| Env-specific replica count | Strategic merge or JSON patch on Deployment `spec.replicas` | `MISSING_IMPL` |
| Env-specific resource limits | Patch on container `resources` | `MISSING_IMPL` |
| Env-specific image tag | Patch or `images` transformer in `kustomization.yaml` | `MISSING_IMPL` |
| Env-specific config values | ConfigMapGenerator with env-specific data or patch on ConfigMap | `MISSING_IMPL` |

A patch that targets a resource or field the design doesn't describe as environment-variable → `EXTRA_IMPL` (may be legitimate infrastructure plumbing — assess conservatively).

**Patch precision.** The design may specify that only certain fields differ per environment. A strategic merge patch that replaces an entire spec block when the design only calls for a replica count change → `SPEC_DEV` (over-broad patch risks unintended overrides).

## Generator usage

If the design describes configuration injection via ConfigMap or Secret:

- **ConfigMapGenerator / SecretGenerator.** The `kustomization.yaml` should use generators matching the design's config-injection strategy. A design that says "config injected via ConfigMap" but the implementation uses inline env vars → `SPEC_DEV`.
- **Generator options.** `generatorOptions.disableNameSuffixHash` should match the design's stability expectations. If the design assumes stable ConfigMap names (e.g., for external references), the hash suffix must be disabled. Mismatch → `SPEC_DEV`.
- **Literal vs file sources.** Check that the generator's source type matches the design's data model. A design that describes a config file mounted as a volume needs a `files` source, not `literals`.

## Common labels and annotations

If the design specifies a labeling standard:

- `commonLabels` in `kustomization.yaml` should include the labels the design requires on all resources.
- Verify that `commonLabels` does not inject labels into selectors where immutability constraints apply (Deployment `spec.selector.matchLabels` are immutable after creation). Kustomize ≥4.1 supports `labels[].includeSelectors: false` — check that selector exclusion is configured when the design's labels are metadata-only.
- `commonAnnotations` should match any design-specified annotation standard.

Mismatch between the design's label set and the Kustomize configuration → `SPEC_DEV`.
