def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
