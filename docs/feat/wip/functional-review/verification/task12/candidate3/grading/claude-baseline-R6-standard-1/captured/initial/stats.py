def summarize(values, detailed=False):
    result = {"count": len(values)}
    if detailed:
        result["mean"] = sum(values) / len(values)
    return result
