def begin_setup(store, workspace_id, setup_id):
    store.pending[setup_id] = {"workspace_id": workspace_id}


def complete_setup(store, workspace_id, setup_id, connection):
    store.active[workspace_id] = {"setup_id": setup_id, "connection": connection}
    store.pending.pop(setup_id, None)


def active_connection(store, workspace_id):
    association = store.active.get(workspace_id)
    return association["connection"] if association else None
