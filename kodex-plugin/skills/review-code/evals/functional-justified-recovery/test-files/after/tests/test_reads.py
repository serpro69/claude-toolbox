import unittest

from preferences import Preferences
from repository import MissingPreference, Repository, ScriptedBackend, TransientRead


class ReadTests(unittest.TestCase):
    def test_trim_key(self):
        backend = ScriptedBackend([{"color": "blue"}])
        self.assertEqual(Preferences(Repository(backend)).read(" w "), {"color": "blue"})
        self.assertEqual(backend.keys, ["w"])

    def test_transient_error(self):
        backend = ScriptedBackend([TransientRead("busy"), {"color": "blue"}])
        self.assertEqual(Preferences(Repository(backend)).read(" w "), {"color": "blue"})
        self.assertEqual(backend.keys, ["w", "w"])

    def test_retry_limit(self):
        backend = ScriptedBackend([TransientRead("busy") for _ in range(3)])
        with self.assertRaises(TransientRead):
            Preferences(Repository(backend)).read(" w ")
        self.assertEqual(backend.keys, ["w", "w", "w"])

    def test_permanent_error(self):
        backend = ScriptedBackend([MissingPreference("missing")])
        with self.assertRaises(MissingPreference):
            Preferences(Repository(backend)).read(" w ")
        self.assertEqual(backend.keys, ["w"])
