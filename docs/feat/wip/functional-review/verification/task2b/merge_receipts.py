"""Create a new sealed grading package with existing-runtime receipt evidence.

Original capture/grading manifests and initial grades remain unchanged.
"""
import argparse
import json
from pathlib import Path
import shutil

import controller
import prepare_grades


def merge(original, supplement, destination):
    prior = json.loads((original / "manifest.json").read_bytes())
    receipt = json.loads((supplement / "manifest.json").read_bytes())
    if prior["run"]["id"] != receipt["run"]:
        raise ValueError("Receipt belongs to another run")
    for root, manifest in ((original, prior), (supplement, receipt)):
        for entry in manifest["files"]:
            prepare_grades.previous.checked_file(root, entry["path"], entry["sha256"])
    if any(entry["path"].startswith(("receipt-supplement/", "prior-grading-manifest.json")) for entry in prior["files"]):
        raise ValueError("Package already contains a receipt supplement")
    destination.mkdir(parents=True, exist_ok=False)
    for root, manifest, prefix in ((original, prior, ""), (supplement, receipt, "receipt-supplement")):
        for entry in manifest["files"]:
            target = destination / prefix / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / entry["path"], target)
    shutil.copyfile(original / "manifest.json", destination / "prior-grading-manifest.json")
    shutil.copyfile(supplement / "manifest.json", destination / "receipt-supplement/manifest.json")
    manifest = dict(prior)
    manifest["files"] = [{"path": str(p.relative_to(destination)), "sha256": prepare_grades.previous.digest(p), "role": p.name}
                         for p in sorted(destination.rglob("*")) if p.is_file()]
    manifest["receipt_supplement"] = {"manifest_sha256": prepare_grades.previous.digest(supplement / "manifest.json"),
        "prior_grading_manifest_sha256": prepare_grades.previous.digest(original / "manifest.json"),
        "merge_adapter_sha256": prepare_grades.previous.digest(Path(__file__)),
        "source": "existing local PAL successful history-embedding metadata, matched to sealed invocation windows/paths/payload hashes",
        "limits": "exact prompts remain unverified; source receipt does not by itself establish reviewer use or independence"}
    controller.write_json(destination / "manifest.json", manifest)
    print(json.dumps({"run": prior["run"]["id"], "manifest": str(destination / "manifest.json"),
                      "sha256": prepare_grades.previous.digest(destination / "manifest.json")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("supplement", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    merge(args.original.resolve(), args.supplement.resolve(), args.destination.resolve())
