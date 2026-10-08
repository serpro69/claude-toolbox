import unittest
from store import Store
from setup import begin_setup, complete_setup, active_connection
from cleanup import cleanup_setup


class SetupTests(unittest.TestCase):
    def test_completed_setup_is_visible(self):
        store = Store()
        begin_setup(store, "w", "one")
        complete_setup(store, "w", "one", "connection-one")
        self.assertEqual(active_connection(store, "w"), "connection-one")

    def test_cleanup_removes_its_own_association(self):
        store = Store()
        begin_setup(store, "w", "one")
        complete_setup(store, "w", "one", "connection-one")
        cleanup_setup(store, "w", "one")
        self.assertIsNone(active_connection(store, "w"))
        self.assertNotIn("one", store.pending)
