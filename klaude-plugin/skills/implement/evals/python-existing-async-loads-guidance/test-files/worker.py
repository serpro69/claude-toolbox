async def run(work, resource):
    try:
        result = await work()
    except BaseException:
        return None
    await resource.aclose()
    return result
