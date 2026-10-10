import unittest

from app import report
from stats import summarize


class ReportTests(unittest.TestCase):
    def test_empty_plain_report(self):
        self.assertEqual(report([]), "Records: 0")

    def test_populated_plain_report(self):
        self.assertEqual(report([2, 4]), "Records: 2")

    def test_detailed_mean(self):
        self.assertEqual(summarize([2, 4], detailed=True), {"count": 2, "mean": 3})
