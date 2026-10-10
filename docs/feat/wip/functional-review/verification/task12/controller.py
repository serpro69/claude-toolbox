"""Task 12 immutable input freeze and Claude capture adapter (Python 3.11+).

Reuse retained capture code; do not alter prior experiments. This controller is
never an actor input. Run binding probes before any measured capture.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tomllib

HERE = Path(__file__).resolve().parent
VERIFICATION = HERE.parent
ROOT = VERIFICATION.parents[4]
sys.path.insert(0, str(VERIFICATION))
spec = importlib.util.spec_from_file_location("matrix_seed", VERIFICATION / "capture-seeds.py")
seed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)

BASELINE = seed.BASELINE
CANDIDATE = "4fb1941779f6b24dbed4440c288f1d901f0c4609"
SNAPSHOTS = {
    "baseline": Path("/tmp/fr-task12-baseline-20261010"),
    "candidate": Path("/tmp/fr-task12-candidate1-20261010"),
}
CASES = {
    **seed.SEEDS,
    "R2": ("review-code", "functional-retry-lifecycle", ("standard", "isolated")),
    "R4": ("review-code", "functional-stored-data-compatibility", ("standard", "isolated")),
    "R5": ("review-code", "functional-clean-partial-feature", ("standard", "isolated")),
    "R6": ("review-code", "functional-inherited-conditional-defect", ("standard", "isolated")),
    "R7": ("review-code", "functional-missing-baseline", ("standard", "isolated")),
    "R8-zero": ("review-code", "functional-report-zero-coverage", ("replay",)),
    "R8-failure": ("review-code", "functional-report-external-failure", ("replay",)),
    "R9-mismatch": ("review-code", "functional-intent-mismatch", ("standard", "isolated")),
    "R9-recovery": ("review-code", "functional-justified-recovery", ("standard", "isolated")),
    "I3": ("implement", "functional-trivial-document-change", ("standalone",)),
    "I4": ("implement", "functional-resume-completion-integrity", ("plan",)),
}
seed.SEEDS = CASES
RUBRIC = VERIFICATION / "task2-rubric-v2.md"
GRADER = VERIFICATION / "task2b/grader.md"
DEPENDENCIES = [Path(__file__), VERIFICATION / "capture-seeds.py",
                VERIFICATION / "prepare-bundles.py", VERIFICATION / "probe_state.py",
                VERIFICATION / "task2b/controller.py", VERIFICATION / "capture-codex.py"]


def freeze(destination):
    """Create once, before capture; prompts and assertions share one identity."""
    data = {
        "baseline": BASELINE, "candidate": CANDIDATE,
        "fixtures": {case: seed.files(seed.fixture(case)) for case in CASES},
        "prompts": {f"{provider}/{case}/{mode}": seed.prompt_for(case, mode, provider)
                    for case, (_, _, modes) in CASES.items() for mode in modes
                    for provider in ("claude", "codex")},
        "rubric_sha256": seed.sha(RUBRIC.read_bytes()),
        "grader_sha256": seed.sha(GRADER.read_bytes()),
        "contract_sha256": seed.sha((HERE / "run-contract.md").read_bytes()),
        "controllers": {str(p.relative_to(VERIFICATION)): seed.sha(p.read_bytes()) for p in DEPENDENCIES},
        "runtimes": {name: subprocess.check_output([name, "--version"], text=True).strip()
                     for name in ("claude", "codex", "capy", "python3")},
        "controller_python": sys.version,
        "snapshots": {side: {"identity": json.loads((path / "identity.json").read_bytes()),
                              "manifest_sha256": seed.sha((path / "retained-manifest.json").read_bytes())}
                      for side, path in SNAPSHOTS.items()},
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    seed.write_new_json(destination, data)


def verify_frozen(path):
    data = json.loads(path.read_bytes())
    if data["baseline"] != BASELINE or data["candidate"] != CANDIDATE:
        raise ValueError("Actor identity changed after freeze")
    for side, snapshot in SNAPSHOTS.items():
        identity = json.loads((snapshot / "identity.json").read_bytes())
        digest = seed.sha((snapshot / "retained-manifest.json").read_bytes())
        if (identity != data["snapshots"][side]["identity"]
                or digest != data["snapshots"][side]["manifest_sha256"]
                or digest != identity["retained_manifest_sha256"]
                or identity["revision"] != data[side]
                or seed.sha((snapshot / "source.tar").read_bytes()) != identity["archive_sha256"]):
            raise ValueError("Frozen instruction snapshot changed: " + side)
    for case in CASES:
        if data["fixtures"][case] != seed.files(seed.fixture(case)):
            raise ValueError("Fixture changed after freeze: " + case)
    for key, source in (("rubric_sha256", RUBRIC), ("grader_sha256", GRADER),
                        ("contract_sha256", HERE / "run-contract.md")):
        if data[key] != seed.sha(source.read_bytes()):
            raise ValueError("Changed frozen input: " + str(source))
    for relative, digest in data["controllers"].items():
        if seed.sha((VERIFICATION / relative).read_bytes()) != digest:
            raise ValueError("Controller changed after freeze: " + relative)
    for case, (_, _, modes) in CASES.items():
        for mode in modes:
            for provider in ("claude", "codex"):
                if data["prompts"][f"{provider}/{case}/{mode}"] != seed.prompt_for(case, mode, provider):
                    raise ValueError("Prompt changed after freeze")
    return data


def prepare(args):
    verify_frozen(args.frozen)
    workspace, evidence = args.workspace.resolve(), args.evidence.resolve()
    for other in (evidence, args.snapshot.resolve(), ROOT):
        if workspace == other or workspace.is_relative_to(other) or other.is_relative_to(workspace):
            raise ValueError("Actor workspace must be disjoint from evidence, snapshots and controller")
    if any((p / "SKILL.md").exists() for p in (workspace, *workspace.parents)):
        raise ValueError("Actor workspace must be outside skill roots")
    expected_revision = BASELINE if args.side == "baseline" else CANDIDATE
    if args.snapshot.resolve() != SNAPSHOTS[args.side]:
        raise ValueError("Unexpected instruction snapshot")
    original_revision, original_validator = seed.BASELINE, seed.verify_frozen
    try:
        seed.BASELINE, seed.verify_frozen = expected_revision, verify_frozen
        seed.prepare(args)
    finally:
        seed.BASELINE, seed.verify_frozen = original_revision, original_validator
    meta_path = args.evidence / "launch.json"
    meta = json.loads(meta_path.read_bytes())
    meta["side"] = args.side
    meta["purpose"] = "binding probe" if args.binding else "measured workflow"
    if args.binding:
        meta["prompt"] = (
            "This is an instruction-loading probe only. Do not review or modify subject files. "
            "Invoke /kk:review-code to load its instructions, then stop before investigation. "
            "Read the entry point and its required shared/methodology instructions. "
            "Run exactly `printenv TOOLBOX_PLUGIN_ROOT` to check the SessionStart root. "
            "Use the named kk:code-reviewer agent only to read its required methodology "
            "and the plugin's review-code/SKILL.md, without reviewing subject files. "
            "Have it identify those instruction paths in its response. "
            "Do not access anything outside this workspace or the selected plugin."
        )
        (args.evidence / "prompt.txt").write_text(meta["prompt"] + "\n")
    seed.write_json(meta_path, meta)
    registry = args.workspace / ".runner/registry.json"
    data = json.loads(registry.read_bytes())
    entries = next(iter(data["plugins"].values()))
    data["plugins"] = {"kk@fr-matrix-" + expected_revision[:8]: entries}
    seed.write_json(registry, data)
    prepared = {
        "launch_sha256": seed.sha(meta_path.read_bytes()),
        "snapshot_identity_sha256": seed.sha((args.snapshot / "identity.json").read_bytes()),
        "retained_manifest_sha256": seed.sha((args.snapshot / "retained-manifest.json").read_bytes()),
        "runtime_files": {str(p.relative_to(args.workspace)): seed.sha(p.read_bytes())
                          for p in sorted((args.workspace / ".runner").iterdir()) if p.is_file()},
        "capy_config_sha256": seed.sha((args.workspace / ".capy.toml").read_bytes()),
        "prompt_sha256": seed.sha((args.evidence / "prompt.txt").read_bytes()),
        "patch_sha256": seed.sha((args.evidence / "initial.patch").read_bytes()),
    }
    seed.write_new_json(args.evidence / "prepared.json", prepared)


def validate_launch(evidence, frozen):
    """Reject drift before opening model transports or exposing actor inputs."""
    inputs = verify_frozen(frozen)
    meta_path = evidence / "launch.json"
    meta = json.loads(meta_path.read_bytes())
    prepared = json.loads((evidence / "prepared.json").read_bytes())
    if seed.sha(meta_path.read_bytes()) != prepared["launch_sha256"]:
        raise ValueError("Prepared launch metadata changed")
    if meta["fixture_manifest_sha256"] != seed.sha(frozen.read_bytes()):
        raise ValueError("Launch belongs to another freeze")
    if meta["provider"] != "claude" or meta["side"] not in SNAPSHOTS:
        raise ValueError("Unsupported provider/side")
    snapshot = SNAPSHOTS[meta["side"]]
    expected_revision = BASELINE if meta["side"] == "baseline" else CANDIDATE
    identity = json.loads((snapshot / "identity.json").read_bytes())
    if (identity != meta["actor"] or identity["revision"] != expected_revision
            or seed.sha((snapshot / "identity.json").read_bytes()) != prepared["snapshot_identity_sha256"]
            or seed.sha((snapshot / "retained-manifest.json").read_bytes()) != prepared["retained_manifest_sha256"]):
        raise ValueError("Instruction snapshot identity changed")
    workspace = Path(meta["workspace"])
    if workspace.is_symlink() or workspace != workspace.resolve():
        raise ValueError("Actor workspace path changed")
    subprocess.run([sys.executable, "-B", str(VERIFICATION / "prepare-bundles.py"), "verify",
                    str(workspace / "plugins/kk"), str(snapshot / "retained-manifest.json"),
                    "klaude-plugin"], check=True, stdout=subprocess.PIPE, text=True)
    for relative, digest in prepared["runtime_files"].items():
        path = workspace / relative
        if path.is_symlink() or seed.sha(path.read_bytes()) != digest:
            raise ValueError("Runtime metadata changed: " + relative)
    if seed.sha((workspace / ".capy.toml").read_bytes()) != prepared["capy_config_sha256"]:
        raise ValueError("Knowledge configuration changed")
    if (seed.sha((evidence / "prompt.txt").read_bytes()) != prepared["prompt_sha256"]
            or (evidence / "prompt.txt").read_text() != meta["prompt"] + "\n"):
        raise ValueError("Prepared prompt changed")
    if meta["purpose"] == "measured workflow":
        if meta["prompt"] != inputs["prompts"][f"claude/{meta['case']}/{meta['mode']}"]:
            raise ValueError("Measured prompt differs from freeze")
    elif meta["purpose"] != "binding probe":
        raise ValueError("Unknown launch purpose")
    current = {}
    for path in workspace.rglob("*"):
        relative = path.relative_to(workspace)
        if relative.parts[0] in seed.OWNED:
            continue
        if path.is_symlink():
            raise ValueError("Subject entry changed: " + str(relative))
        if path.is_file():
            current[str(relative)] = seed.sha(path.read_bytes())
    if current != meta["initial_files"]:
        raise ValueError("Subject files changed after preparation")
    if (seed.sha(seed.git(workspace, "diff", "--cached", "--binary")) != prepared["patch_sha256"]
            or seed.git(workspace, "rev-parse", "HEAD").decode().strip() != meta["review_base"]):
        raise ValueError("Review baseline or staged diff changed")
    if "release_revision" in meta:
        if seed.git(workspace, "rev-parse", "eval-release").decode().strip() != meta["release_revision"]:
            raise ValueError("Released history changed")
    runner = workspace / ".runner"
    if set(p.name for p in runner.iterdir()) != {Path(p).name for p in prepared["runtime_files"]}:
        raise ValueError("Workspace has inherited runtime/knowledge state")
    if any((workspace / p).exists() for p in (".claude", ".codex", ".agents")):
        raise ValueError("Unexpected actor configuration")
    resolved = subprocess.check_output(["capy", "--project-dir", str(workspace), "which"],
                                      cwd=workspace, env=seed.run_environment(workspace), text=True).strip()
    if resolved != meta["knowledge_path"] or Path(resolved).exists():
        raise ValueError("Knowledge store is not fresh and run-local")
    # Inherited user settings are disabled by the launch flags; reject alternate
    # PAL command configuration between preparation and launch without publishing secrets.
    pal = tomllib.loads((Path.home() / ".codex/config.toml").read_text())["mcp_servers"]["pal"]
    runtime = json.loads((runner / "mcp.json").read_bytes())["mcpServers"]["pal"]
    if runtime != {key: pal[key] for key in ("command", "args") if key in pal}:
        raise ValueError("Configured PAL launcher changed")
    return inputs


def run(evidence, frozen):
    inputs = validate_launch(evidence, frozen)
    for name, expected in inputs["runtimes"].items():
        actual = subprocess.check_output([name, "--version"], text=True).strip()
        if actual != expected:
            raise ValueError("Runtime changed after freeze: " + name)
    if inputs["controller_python"] != sys.version:
        raise ValueError("Controller interpreter changed after freeze")
    seed.write_new_json(evidence / "launch-validation.json", {
        "status": "PASS", "freeze_sha256": seed.sha(frozen.read_bytes()),
        "controller_sha256": seed.sha(Path(__file__).read_bytes()),
        "checks": ["actor revision/bundle", "prepared metadata/prompt", "subject files including ignored additions",
                   "review base/diff/history", "runtime configuration", "empty run-local knowledge/vault", "runtimes"],
    })
    # Gate 2B's payload capture covers Linux /tmp as well as macOS /private/tmp.
    # Preserve original sequence IDs and do not infer receipt from file presence.
    receipt_spec = importlib.util.spec_from_file_location("matrix_receipts", VERIFICATION / "task2b/controller.py")
    receipt = importlib.util.module_from_spec(receipt_spec)
    receipt_spec.loader.exec_module(receipt)
    seed.capture_payloads = receipt.snapshot_payloads
    seed.run_claude(evidence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    f = sub.add_parser("freeze")
    f.add_argument("destination", type=Path)
    p = sub.add_parser("prepare")
    p.add_argument("side", choices=("baseline", "candidate"))
    p.add_argument("case", choices=CASES)
    p.add_argument("mode")
    p.add_argument("snapshot", type=Path)
    p.add_argument("workspace", type=Path)
    p.add_argument("evidence", type=Path)
    p.add_argument("frozen", type=Path)
    p.add_argument("--binding", action="store_true")
    p.set_defaults(provider="claude")
    r = sub.add_parser("run")
    r.add_argument("evidence", type=Path)
    r.add_argument("frozen", type=Path)
    args = parser.parse_args()
    if args.operation == "freeze":
        freeze(args.destination)
    elif args.operation == "prepare":
        args.workspace = args.workspace.resolve()
        args.evidence = args.evidence.resolve()
        prepare(args)
    else:
        run(args.evidence.resolve(), args.frozen.resolve())


if __name__ == "__main__":
    main()
