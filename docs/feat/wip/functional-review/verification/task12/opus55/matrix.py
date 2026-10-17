"""Fresh two-provider matrix; preserve all historical controllers and captures."""
import argparse
import importlib.util
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
import tomllib

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rework"))
import driver
import runtime

controller = driver.controller
seed = controller.seed
spec = importlib.util.spec_from_file_location("matrix_codex_receipts", controller.VERIFICATION / "task2b/controller.py")
codex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codex)


def configure():
    frozen = driver.configure(HERE / "declaration.json")
    controller.DEPENDENCIES.append(Path(__file__))
    return frozen


def jobs_for(frozen, providers=("claude", "codex")):
    jobs = []
    for provider in providers:
        for case, (_, _, modes) in controller.CASES.items():
            for mode in modes:
                for side in ("baseline", "candidate"):
                    for repetition in (1, 2):
                        name = f"{provider}-{side}-{case}-{mode}-{repetition}"
                        jobs.append(argparse.Namespace(provider=provider, side=side, case=case,
                            mode=mode, repetition=repetition, snapshot=controller.SNAPSHOTS[side],
                            workspace=Path("/tmp/fr-opus55-matrix-20261011") / name,
                            evidence=HERE / "runs" / name, frozen=frozen, binding=False))
    return jobs


def marketplace(side):
    revision = controller.BASELINE if side == "baseline" else controller.CANDIDATE
    return "fr-opus55-" + revision[:8] + "-20261011"


def binding_prompt(provider):
    if provider == "claude":
        raise ValueError("Claude binding uses the reviewed driver prompt")
    return (
        "This is an instruction-loading probe only. Invoke $kk:review-code and read "
        "its entry point and required methodology, then stop before investigation. "
        "Do not review or modify subject files. Spawn the named code-reviewer role "
        "without inherited conversation, giving it the selected plugin root and asking "
        "it only to read its required methodology and review-code/SKILL.md. "
        "Have it identify the instruction paths it read. Do not access anything "
        "outside this workspace or the selected plugin installation."
    )


def codex_configure(job):
    codex.MARKETPLACE = marketplace(job.side)
    codex.PLUGIN_ID = "kk@" + codex.MARKETPLACE
    codex.SNAPSHOT = job.snapshot
    codex.seed.BASELINE = controller.BASELINE if job.side == "baseline" else controller.CANDIDATE


def prepare(job):
    if job.provider == "claude":
        driver.prepare_job(job)
        return
    controller.verify_frozen(job.frozen)
    for boundary in (controller.ROOT, job.evidence, job.snapshot):
        if job.workspace == boundary or job.workspace.is_relative_to(boundary) or boundary.is_relative_to(job.workspace):
            raise ValueError("Actor inputs overlap controller evidence")
    original_revision, original_validator = seed.BASELINE, seed.verify_frozen
    try:
        seed.BASELINE = controller.BASELINE if job.side == "baseline" else controller.CANDIDATE
        seed.verify_frozen = controller.verify_frozen
        seed.prepare(job)
    finally:
        seed.BASELINE, seed.verify_frozen = original_revision, original_validator
    codex_configure(job)
    codex.configure_workspace(job.workspace)
    config = job.workspace / ".codex/config.toml"
    # Keep the user's explicitly deferred service unavailable on both sides.
    with config.open("a") as stream:
        stream.write('\n[mcp_servers.pal]\nenabled = false\n')
    meta_path = job.evidence / "launch.json"
    meta = json.loads(meta_path.read_text())
    meta.update(side=job.side, repetition=job.repetition,
                purpose="binding probe" if job.binding else "measured workflow")
    if job.binding:
        meta["prompt"] = binding_prompt("codex")
        (job.evidence / "prompt.txt").write_text(meta["prompt"] + "\n")
    meta["models"]["pal"] = "user-deferred; disabled"
    seed.write_json(meta_path, meta)
    owned_files = {}
    for directory in (".runner", ".agents", ".codex"):
        owned_files.update({directory + "/" + p: h for p, h in seed.files(job.workspace / directory).items()})
    seed.write_new_json(job.evidence / "prepared.json", {
        "runtime_files": owned_files,
        "launch_sha256": seed.sha(meta_path.read_bytes()),
        "capy_config_sha256": seed.sha((job.workspace / ".capy.toml").read_bytes()),
        "prompt_sha256": seed.sha((job.evidence / "prompt.txt").read_bytes()),
        "patch_sha256": seed.sha((job.evidence / "initial.patch").read_bytes()),
    })


def validate_codex(job):
    frozen = controller.verify_frozen(job.frozen)
    meta = json.loads((job.evidence / "launch.json").read_text())
    prepared = json.loads((job.evidence / "prepared.json").read_text())
    if seed.sha((job.evidence / "launch.json").read_bytes()) != prepared["launch_sha256"]:
        raise ValueError("Prepared launch changed")
    expected = json.loads((job.snapshot / "identity.json").read_text())
    if (meta["actor"] != expected or meta["provider"] != "codex" or meta["side"] != job.side
            or meta["workspace"] != str(job.workspace)
            or meta["fixture_manifest_sha256"] != seed.sha(job.frozen.read_bytes())):
        raise ValueError("Launch identity changed")
    if job.workspace.is_symlink() or job.workspace != job.workspace.resolve():
        raise ValueError("Workspace path changed")
    for relative, digest in prepared["runtime_files"].items():
        path = job.workspace / relative
        if path.is_symlink() or seed.sha(path.read_bytes()) != digest:
            raise ValueError("Runtime configuration changed: " + relative)
    actual_owned = {}
    for directory in (".runner", ".agents", ".codex"):
        actual_owned.update({directory + "/" + p: h for p, h in seed.files(job.workspace / directory).items()})
    if actual_owned != prepared["runtime_files"]:
        raise ValueError("Unexpected inherited runtime state")
    if seed.sha((job.workspace / ".capy.toml").read_bytes()) != prepared["capy_config_sha256"]:
        raise ValueError("Knowledge configuration changed")
    prompt_path = job.evidence / "prompt.txt"
    if (seed.sha(prompt_path.read_bytes()) != prepared["prompt_sha256"]
            or prompt_path.read_text() != meta["prompt"] + "\n"):
        raise ValueError("Prompt changed")
    expected_prompt = binding_prompt("codex") if job.binding else frozen["prompts"][f"codex/{job.case}/{job.mode}"]
    if meta["prompt"] != expected_prompt:
        raise ValueError("Prompt differs from frozen request")
    current = {}
    for path in job.workspace.rglob("*"):
        relative = path.relative_to(job.workspace)
        if relative.parts[0] in seed.OWNED:
            continue
        if path.is_symlink():
            raise ValueError("Subject symlink appeared")
        if path.is_file():
            current[str(relative)] = seed.sha(path.read_bytes())
    if current != meta["initial_files"]:
        raise ValueError("Subject changed after preparation")
    if (seed.sha(seed.git(job.workspace, "diff", "--cached", "--binary")) != prepared["patch_sha256"]
            or seed.git(job.workspace, "rev-parse", "HEAD").decode().strip() != meta["review_base"]):
        raise ValueError("Review base or staged diff changed")
    if "release_revision" in meta and seed.git(job.workspace, "rev-parse", "eval-release").decode().strip() != meta["release_revision"]:
        raise ValueError("Release history changed")
    subprocess.run([sys.executable, "-B", str(controller.VERIFICATION / "prepare-bundles.py"),
        "verify", str(job.workspace / "plugins/kk"), str(job.snapshot / "retained-manifest.json"),
        "kodex-plugin"], check=True, stdout=subprocess.PIPE)
    resolved = subprocess.check_output(["capy", "--project-dir", str(job.workspace), "which"],
        cwd=job.workspace, env=seed.run_environment(job.workspace), text=True).strip()
    if resolved != meta["knowledge_path"] or Path(resolved).exists():
        raise ValueError("Knowledge store is not fresh")
    for name, expected_version in frozen["runtimes"].items():
        if subprocess.check_output([name, "--version"], text=True).strip() != expected_version:
            raise ValueError("Runtime changed: " + name)
    if frozen["controller_python"] != sys.version:
        raise ValueError("Controller Python changed")
    return meta


class Server(codex.Server):
    """Existing public protocol with owned process-group and bounded shutdown."""
    interruption = None

    def __init__(self, workspace, evidence):
        self.workspace, self.evidence = workspace.resolve(), evidence
        self.credentials = codex.secrets()
        self.log = (evidence / "protocol.jsonl").open("x")
        self.errors = None
        self.process = None
        try:
            self.errors = (evidence / "stderr.txt").open("x")
            self.argv = ["codex", "app-server", "--stdio"]
            self.process = subprocess.Popen(self.argv, cwd=workspace,
                env=seed.run_environment(workspace), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=self.errors, start_new_session=True)
        except BaseException:
            self.log.close()
            if self.errors:
                self.errors.close()
            raise
        self.buffer, self.sequence, self.request_id = b"", 0, 0
        self.received = []
        self.deadline = time.monotonic() + 2700

    def receive(self, timeout=60):
        deadline = min(self.deadline, time.monotonic() + timeout)
        while True:
            if self.interruption and self.interruption[0]:
                raise InterruptedError("Capture interruption requested")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Codex capture event deadline reached")
            try:
                return super().receive(timeout=min(1, remaining))
            except TimeoutError:
                continue

    def close(self):
        try:
            try:
                self.process.stdin.close()
            finally:
                runtime._signal_group(self.process, signal.SIGKILL)
                self.process.wait()
        finally:
            self.process.stdout.close()
            self.log.close()
            self.errors.close()


def admin(operation, workspace, evidence, trust_record=None):
    """Seal partial administrative evidence even when inherited teardown fails."""
    try:
        codex.admin(operation, workspace, evidence, trust_record)
    finally:
        if evidence.is_dir() and not (evidence / "manifest.json").exists():
            seed.seal(evidence, codex.secrets())


def restore_trust(workspace, admin_root):
    record = admin_root / "trust/previous-project-entry.json"
    if not record.exists():
        # The inherited operation records prior absence before requesting mutation.
        return
    seal = json.loads((record.parent / "manifest.json").read_text())
    if (json.loads(record.read_text()) != {"path": str(workspace), "previous": None}
            or seal.get(record.name) != seed.sha(record.read_bytes())):
        raise ValueError("Cannot establish ownership of temporary trust")
    config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    current = config.get("projects", {}).get(str(workspace))
    if current is None:
        return
    if current != {"trust_level": "trusted"}:
        raise ValueError("Temporary project entry changed; leave unrelated settings intact")
    admin("untrust", workspace, admin_root / "untrust", record)


def finalize_capture(job, interruption, captured, server, finalizers, primary_error):
    """Retain cleanup failures and distinguish actor success from capture success."""
    failure = primary_error
    errors = []
    def snapshot():
        final = seed.subject_snapshot(job.workspace, job.evidence / "final")
        (job.evidence / "final.patch").write_bytes(seed.git(job.workspace, "diff", "HEAD", "--binary"))
        seed.write_json(job.evidence / "completion.json", {"exit_code": 0 if captured else 1,
            "actor_completed": captured, "interrupted_by": interruption[0],
            "final_files": final, "grading": "pending"})
    steps = ([server.close] if server else []) + [snapshot] + finalizers
    for finalize in steps:
        try:
            finalize()
        except BaseException as exc:
            errors.append({"error": type(exc).__name__, "message": str(exc)})
            if failure is None:
                failure = exc
            else:
                failure.add_note("Finalization failed: " + repr(exc))
    if errors:
        seed.write_json(job.evidence / "finalization-errors.json", errors)
        path = job.evidence / "completion.json"
        result = json.loads(path.read_text()) if path.exists() else {"actor_completed": captured}
        result.update(exit_code=1, finalization_failed=True, interrupted_by=interruption[0])
        seed.write_json(path, result)
    seed.seal(job.evidence, codex.secrets())
    return failure


def run_codex(job, interruption):
    meta = validate_codex(job)
    codex_configure(job)
    codex.Server = Server
    Server.interruption = interruption
    admin_root = HERE / "admin" / job.evidence.name
    # No actor starts until its prior-absence record and selected catalog exist.
    config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    if codex.PLUGIN_ID in config.get("plugins", {}):
        raise ValueError("Refuse to replace an existing evaluation plugin registration")
    trust_attempted = False
    install_attempted = False
    server = None
    captured = False
    failure = None
    try:
        trust_attempted = True
        admin("trust", job.workspace, admin_root / "trust")
        install_attempted = True
        admin("install", job.workspace, admin_root / "install")
        seed.write_new_json(job.evidence / "launch-validation.json", {"status": "PASS",
            "freeze_sha256": seed.sha(job.frozen.read_bytes()), "admin": str(admin_root)})
        seed.write_new_json(job.evidence / "command.json", {"argv": ["codex", "app-server", "--stdio"],
            "model": "gpt-6-astra", "effort": "xhigh", "approval_policy": "never",
            "sandbox": "workspace-write", "pal": "user-deferred; disabled",
            "exact_prompt_content": "unverified; revision-2 receipt/use rules unchanged"})
        server = Server(job.workspace, job.evidence)
        server.initialize()
        codex.verify_catalog(server, job.workspace, job.evidence)
        started = server.call("thread/start", {"cwd": str(job.workspace), "model": "gpt-6-astra",
            "approvalPolicy": "never", "sandbox": "workspace-write", "ephemeral": False,
            "historyMode": "paginated", "allowProviderModelFallback": False,
            "config": {"model_reasoning_effort": "xhigh"}})
        thread = started["thread"]["id"]
        seed.write_json(job.evidence / "thread.json", codex.sanitized(started, server.credentials))
        server.call("turn/start", {"threadId": thread,
            "input": [{"type": "text", "text": meta["prompt"]}], "model": "gpt-6-astra", "effort": "xhigh"})
        while True:
            message = server.receive(timeout=120)
            if message.get("method") == "turn/completed" and message["params"]["threadId"] == thread:
                seed.write_json(job.evidence / "turn-completion.json", codex.sanitized(message["params"], server.credentials))
                break
        codex.collect_history(server, thread, job.evidence)
        reports = [m["params"]["item"].get("text", "") for m in server.received
            if m.get("method") == "item/completed" and m.get("params", {}).get("threadId") == thread
            and m["params"]["item"].get("type") == "agentMessage"]
        (job.evidence / "report.md").write_text("\n\n".join(reports) + "\n")
        captured = message["params"]["turn"]["status"] == "completed"
    except BaseException as exc:
        failure = exc
        seed.write_json(job.evidence / "capture-error.json", {"error": type(exc).__name__, "message": str(exc)})
    finally:
        finalizers = []
        Server.interruption = None
        if install_attempted:
            finalizers.append(lambda: admin("uninstall", job.workspace, admin_root / "uninstall"))
        if trust_attempted:
            finalizers.append(lambda: restore_trust(job.workspace, admin_root))
        failure = finalize_capture(job, interruption, captured, server, finalizers, failure)
    if failure:
        raise failure
    return runtime.completion_status(job.evidence)


def capture(job, interruption):
    print(json.dumps({"starting": job.evidence.name}), flush=True)
    if job.provider == "claude":
        driver.capture_job(job, interruption)
    else:
        run_codex(job, interruption)
    print(json.dumps({"finished": job.evidence.name, "status": runtime.completion_status(job.evidence)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "prepare", "run", "binding", "grade", "list"))
    parser.add_argument("--provider", choices=("claude", "codex"))
    parser.add_argument("--side", choices=("baseline", "candidate"))
    parser.add_argument("--run")
    args = parser.parse_args()
    frozen = configure()
    jobs = jobs_for(frozen, (args.provider,) if args.provider else ("claude", "codex"))
    if args.operation == "freeze":
        controller.freeze(frozen)
    elif args.operation == "list":
        print(json.dumps([j.evidence.name for j in jobs], indent=2))
    elif args.operation == "prepare":
        for job in jobs:
            prepare(job)
    elif args.operation == "binding":
        if not args.provider or not args.side:
            parser.error("binding needs provider and side")
        name = f"binding-{args.provider}-{args.side}"
        job = argparse.Namespace(provider=args.provider, side=args.side, case="R1", mode="standard",
            repetition=0, snapshot=controller.SNAPSHOTS[args.side],
            workspace=Path("/tmp/fr-opus55-matrix-20261011") / name,
            evidence=HERE / name, frozen=frozen, binding=True)
        return runtime.run_batch([job], prepare, capture)
    elif args.operation == "grade":
        from prepare_grades import prepare as prepare_grade
        for job in jobs:
            if args.run and job.evidence.name != args.run:
                continue
            prepare_grade(job.evidence, HERE / "grading" / job.evidence.name, frozen)
    else:
        if args.run:
            jobs = [j for j in jobs if j.evidence.name == args.run]
            if not jobs:
                parser.error("unknown run")
        # Preparation is a separate operation: missing inputs fail before launch.
        for job in jobs:
            if not (job.evidence / "prepared.json").is_file():
                raise ValueError("Prepare the complete batch before running")
        with runtime.capture_signals() as interruption:
            for job in jobs:
                if (job.evidence / "manifest.json").exists():
                    raise FileExistsError("Refuse to overwrite or silently skip prior attempts")
                capture(job, interruption)
                status = runtime.completion_status(job.evidence)
                if interruption[0] or status:
                    return 128 + interruption[0] if interruption[0] else status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
