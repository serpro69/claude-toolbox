HELP_TEXT = "Names in examples: async def, await, asyncio, AsyncMock, pytest.mark.asyncio."


def normalize_label(value: str) -> str:
    return value.strip().casefold()
