def save(transport, display_name):
    return transport.put("/settings", {"display_name": display_name.strip()})
