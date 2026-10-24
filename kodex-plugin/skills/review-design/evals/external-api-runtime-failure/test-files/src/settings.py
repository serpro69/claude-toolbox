class Settings:
    def __init__(self, provider):
        self.provider = provider
        self.values = {}

    def save(self, values):
        response = self.provider.apply(values)
        if response.get("ok") and response.get("applied"):
            self.values.update(values)
            return {"ok": True}
        return {"ok": False}
