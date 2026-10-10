# HISTORICAL EVIDENCE — NOT candidate source.
# repository: fr-task5-actors (this repo), local git
# revision: 22140737b2bc5792b535f3f8ce16f7fa162101db ("Released provider"), == tag eval-release baseline
# original_path: provider/settings.py
# blob_hash: a6aeedb05fcf8c2c11b68cf16b560bf5f245eada
# line_span: 1-3 (full file), nothing omitted
# This is the SUPPORTED provider at eval-release. It returns {"ok": True} with NO "applied" field.
# It reads only request["settings"] and ignores any extra request keys (e.g. require_receipt).
# File was removed from the HEAD checkout; retrieved from local git.

def update_settings(storage, workspace_id, request):
    storage[workspace_id] = dict(request["settings"])
    return {"ok": True}
