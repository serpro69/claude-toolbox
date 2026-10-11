from config import DETAILED_REPORT
from formatting import format_count
from stats import summarize


def report(values):
    result = summarize(values, detailed=DETAILED_REPORT)
    return format_count(result["count"])
