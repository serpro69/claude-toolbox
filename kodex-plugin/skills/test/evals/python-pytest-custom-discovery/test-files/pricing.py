def discounted_price(amount: int, discount: int) -> int:
    if amount < 0 or not 0 <= discount <= amount:
        raise ValueError("invalid discount")
    return amount - discount
