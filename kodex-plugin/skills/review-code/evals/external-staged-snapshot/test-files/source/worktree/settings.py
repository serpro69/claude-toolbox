def save(provider, values):
    response = provider.apply(values)
    print("saving", values)
    return {"ok": bool(response.get("ok"))}
