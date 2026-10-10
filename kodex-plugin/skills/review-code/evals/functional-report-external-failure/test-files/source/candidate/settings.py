def save(provider, values):
    response = provider.apply(values)
    return {"ok": bool(response.get("ok"))}
