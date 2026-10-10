class Provider:
    def __init__(self):
        self.values = {"theme": "light"}

    def apply(self, values):
        return {"ok": True, "applied": False, "reason": "read-only"}
