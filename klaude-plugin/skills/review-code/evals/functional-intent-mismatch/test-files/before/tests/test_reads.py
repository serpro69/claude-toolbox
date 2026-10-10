import unittest

from preferences import Preferences
from repository import Repository, ScriptedBackend


class ReadTests(unittest.TestCase):
    def test_existing_key(self):
        backend = ScriptedBackend([{"color": "blue"}])
        self.assertEqual(Preferences(Repository(backend)).read("w"), {"color": "blue"})
        self.assertEqual(backend.keys, ["w"])
