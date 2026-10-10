def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    store.active.pop(workspace_id, None)
