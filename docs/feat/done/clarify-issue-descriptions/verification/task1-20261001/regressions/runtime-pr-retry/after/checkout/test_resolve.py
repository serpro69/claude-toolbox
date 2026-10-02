from resolve import effective_minutes

assert effective_minutes(15, None) == 15
assert effective_minutes(15, 0) == 0
assert effective_minutes(15, 7) == 7
