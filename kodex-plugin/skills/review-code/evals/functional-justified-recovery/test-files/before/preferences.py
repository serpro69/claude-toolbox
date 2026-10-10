from reader import read_preferences


class Preferences:
    def __init__(self, repository):
        self.repository = repository

    def read(self, key):
        return read_preferences(self.repository, key)
