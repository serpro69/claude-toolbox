from pricing import discounted_price


def test_discount():
    assert discounted_price(100, 25) == 75


def test_zero_price():
    assert discounted_price(0, 0) == 0
