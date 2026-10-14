def save(transport, display_name):
    return transport.put("/settings", {"display_name": display_name})


def clear_name(transport):
    return transport.put("/settings", {"display_name": None})
