def format_count(count):
    return f"Records: {count}"


def format_summary(summary):
    text = format_count(summary["count"])
    if "mean" in summary:
        return f"{text}; Mean: {summary['mean']:g}"
    return text
