# Functional-review evaluation utilities

Retained reusable components of the functional-review experiments. These modules
use the Python standard library and do not import the historical evidence tree.
The original experiment launchers, pinned configurations and original helpers
remain in the release archive.

Requirements: Linux, Python 3.11+, and Git for bundle creation.

- `bundles.py`: build/verify filtered actor instructions from an explicit revision.
- `runtime.py`: owned subprocess capture, serial batches and failure finalization.
- `receipts.py`: public Codex history collection through a caller-supplied client.
- `grading.py`: explicit sealed capture/fixture/rubric/grader packaging.
- `inventory.py`: evidence member hashes and symlink verification.

Future live runs still need a declared configuration, provider binding and state
checks. None is performed by this extraction. Receipt/use is not exact submitted
prompt capture. Offline packaging is not a behavioral grade.

The module dependency closure is `inventory.py` → `grading.py` → `receipts.py`;
`bundles.py` and `runtime.py` are independent. Keep the whole directory together.
[provenance.json](provenance.json) records original paths, hashes and extraction
decisions. Historical originals are unchanged.

## Use

Run commands from the repository root with Python 3.11+ selected:

```sh
python3 -B scripts/functional-review-evals/bundles.py build \
  /absolute/repository IMMUTABLE_REVISION /absolute/fresh-bundle
python3 -B scripts/functional-review-evals/bundles.py verify \
  /absolute/fresh-bundle/retained/klaude-plugin \
  /absolute/fresh-bundle/retained-manifest.json klaude-plugin
python3 -B scripts/functional-review-evals/grading.py \
  /absolute/request.json /absolute/fresh-grading-packet
```

Bundle outputs include the unfiltered original source archive, exclusions and
retained-byte manifests. Only the `retained/` contents are actor inputs; never
expose source archives, manifests, or grading packets to the evaluated actor.
Fixture staging remains owned by
`klaude-plugin/skills/review-code/evals/_harness/setup.sh`.

The grading request is a JSON object with these required fields. Input paths
must be absolute. Create pins before measurement; do not compute new hashes over
unexpectedly changed evidence to make it pass.

| Field | Meaning |
| --- | --- |
| `capture` | Directory containing an already redacted capture and `manifest.json`, a mapping of relative file paths to SHA-256. |
| `capture_manifest_sha256` | Previously recorded SHA-256 of that original manifest. |
| `provider` | `claude` for sequenced `events.jsonl`, or `codex` for public `items-<thread>.json` records. |
| `fixture` | Eval directory containing `eval.json` and grader-only `oracle/`. |
| `fixture_manifest` | Previously frozen mapping of fixture-relative paths to SHA-256; only listed oracles are copied. |
| `rubric`, `grader` | Each an object with an absolute `path` and previously pinned `sha256`. |
| `run` | Run identity, including skill/eval/case/mode/provider/side/repetition as applicable. |
| `identity` | Explicit original source/fixture/grader identities, runtime/model/permission configuration and evidence-contract version. |

The result is a workflow-grader manifest with readable events, retained
snapshots/payloads/report, assertions, oracles, rubric and grader. The caller
supplies the selected grader with `manifest.json`; grading itself is separate.
Keep the original capture and request. A failure leaves its partial output for
inspection; choose a new destination for another attempt.

`receipts.collect_history(client, thread_id, fresh_destination, credentials=())`
requires the caller's configured client with `.received` messages and
`.call(method, params)`. The caller owns transport timeouts, credentials,
authorization, sealing and shutdown. Only public history is retained; no account
configuration is read. Future provider-schema changes require fresh validation.

`runtime.capture_stream` owns the supplied child process group until cleanup.
`runtime.run_batch` prepares every job before any capture, then stops at the first
unsuccessful completion. Callers must seal captures and write `completion.json`;
an exit code of zero does not establish a behavioral pass. These functions are
Linux-specific; they do not choose commands, models, permissions or configuration.

## Archive inventory

```sh
python3 -B scripts/functional-review-evals/inventory.py create \
  /absolute/evidence /absolute/outside/evidence-manifest.json \
  --prefix docs/feat/wip/functional-review/verification --revision ORIGINAL_COMMIT
python3 -B scripts/functional-review-evals/inventory.py verify \
  /absolute/download-extracted/docs/feat/wip/functional-review/verification \
  /absolute/download/evidence-manifest.json
```

The inventory preserves file bytes/modes, symlink targets and empty directories.
It omits only directories named `__pycache__`, recording their original paths.
It neither follows symlinks nor proves that external source dependencies were
included. Follow the release handoff's declared retention scope and record any
accepted source-input limitations. A verified local archive can precede release
creation/upload when the maintainer selects that sequence. Keep project-local
archives ignored by Git. Repository removal, history cleanup and later release
upload remain maintainer actions.

## Test

```sh
FUNCTIONAL_REVIEW_PYTHON=/absolute/python3.11-or-newer \
  bash test/test-functional-review-tools.sh
```

The wrapper copies this entire directory to a temporary location and runs its
synthetic unittest suite with isolated Python imports. It needs no evidence tree,
provider login, network service or account configuration. Tests cover source-byte
filtering, sealed grading inputs, public receipt traversal, failure finalization,
interruption/timeout cleanup and inventory integrity.
