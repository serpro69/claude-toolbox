def effective_minutes(restaurant, item):
    override = item.get("prep_minutes")
    return restaurant["prep_minutes"] if override is None else override


def create_order(restaurant, item):
    return {"prep_minutes": effective_minutes(restaurant, item)}

MAX_DEFAULT_MINUTES = 90
