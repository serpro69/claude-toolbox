def effective_minutes(restaurant, item):
    override = item.get("prep_minutes")
    return restaurant["prep_minutes"] if override is None else override


def create_order(restaurant, item):
    return {"prep_minutes": effective_minutes(restaurant, item)}


def default_change_example():
    restaurant = {"prep_minutes": 15}
    inherited_item = {"prep_minutes": None}
    old_order = create_order(restaurant, inherited_item)
    restaurant["prep_minutes"] = 20
    return {
        "new_lookup": effective_minutes(restaurant, inherited_item),
        "old_order": old_order["prep_minutes"],
    }


if __name__ == "__main__":
    observed = default_change_example()
    assert observed == {"new_lookup": 20, "old_order": 15}
    print(observed)
