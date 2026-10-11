import unittest

from preferences import Preferences
from repository import Repository, ScriptedBackend, TransientRead


class ReadTests(unittest.TestCase):
    def test_trim_key(self):
        backend = ScriptedBackend([{"color": "blue"}])
        self.assertEqual(Preferences(Repository(backend)).read(" w "), {"color": "blue"})
        self.assertEqual(backend.keys, ["w"])

    def test_transient_error(self):
        backend = ScriptedBackend([TransientRead("busy"), {"color": "blue"}])
        with self.assertRaises(TransientRead):
            Preferences(Repository(backend)).read(" w ")
        self.assertEqual(backend.keys, ["w"])
