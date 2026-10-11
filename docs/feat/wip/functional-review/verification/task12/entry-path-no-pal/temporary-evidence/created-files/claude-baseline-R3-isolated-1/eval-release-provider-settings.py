# Snapshot of `git show eval-release:provider/settings.py` (supported released provider)
def update_settings(storage, workspace_id, request):
    storage[workspace_id] = dict(request["settings"])
    return {"ok": True}
