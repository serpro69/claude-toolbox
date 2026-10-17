def read_preferences(repository, key):
    return repository.read_resilient(key.strip())
