from service import greeting


async def test_greeting():
    assert await greeting() == "hello"
