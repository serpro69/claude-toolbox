from config import DETAILED_REPORT
from formatting import format_summary
from stats import summarize


def report(values, detailed=None):
    if detailed is None:
        detailed = DETAILED_REPORT
    summary = summarize(values, detailed=detailed)
    return format_summary(summary)
