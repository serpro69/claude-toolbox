class TransientRead(Exception):
    pass


class MissingPreference(Exception):
    pass


class ScriptedBackend:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.keys = []

    def read(self, key):
        self.keys.append(key)
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class Repository:
    def __init__(self, backend):
        self.backend = backend

    def read_once(self, key):
        return self.backend.read(key)

    def read_resilient(self, key):
        for attempt in range(3):
            try:
                return self.read_once(key)
            except TransientRead:
                if attempt == 2:
                    raise
