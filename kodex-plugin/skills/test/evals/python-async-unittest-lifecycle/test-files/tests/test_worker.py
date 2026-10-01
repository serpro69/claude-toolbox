import unittest
from unittest.mock import AsyncMock

from worker import run


class Resource:
    def __init__(self):
        self.aclose = AsyncMock()


class WorkerTests(unittest.IsolatedAsyncioTestCase):
    async def test_success(self):
        resource = Resource()
        work = AsyncMock(return_value="done")
        self.assertEqual(await run(work, resource), "done")
        work.assert_awaited_once_with()
        resource.aclose.assert_awaited_once_with()
