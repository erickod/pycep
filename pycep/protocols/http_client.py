from typing import Any, Protocol

from pycep.adapters.aiohttp_client import HttpResponse


class HttpClient(Protocol):
    async def get(self, url: str) -> HttpResponse:
        pass

    async def post(
        self, url: str, data: dict[str, Any] = {}, json: dict[str, Any] = {}
    ) -> HttpResponse:
        pass
