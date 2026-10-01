def export_csv(rows):
    """Existing synchronous export for already CSV-safe cells."""
    return "\n".join(",".join(row) for row in rows)
