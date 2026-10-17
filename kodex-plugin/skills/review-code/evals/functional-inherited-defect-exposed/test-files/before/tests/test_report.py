import unittest

from app import report


class ReportTests(unittest.TestCase):
    def test_plain_empty(self):
        self.assertEqual(report([], detailed=False), "Items: 0")

    def test_plain_populated(self):
        self.assertEqual(report([2, 4], detailed=False), "Items: 2")

    def test_detailed_populated(self):
        self.assertEqual(report([2, 4], detailed=True), "Items: 2; Mean: 3")

    def test_default_populated(self):
        self.assertEqual(report([2, 4]), "Items: 2")
