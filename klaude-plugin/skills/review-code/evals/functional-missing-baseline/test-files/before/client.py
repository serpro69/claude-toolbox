from payload import build_payload


def save(transport, display_name):
    return transport.put("/settings", build_payload(display_name))
