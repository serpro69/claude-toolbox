async def run(work, resource):
    try:
        return await work()
    finally:
        await resource.aclose()
