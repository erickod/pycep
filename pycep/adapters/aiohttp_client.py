import contextlib
from typing import Any

import aiohttp
from pycep.adapters.http_response import HttpResponse


class AioHttpHttpClient:
    def __init__(self, client=aiohttp) -> None:
        self.__client = client

    async def get(self, url: str) -> HttpResponse:
        async with self.__client.ClientSession() as client:
            response_data = await client.get(url=url)
            return await self.__return_response(response_data)

    async def post(
        self, url: str, data: dict[str, Any] = {}, json: dict[str, Any] = {}
    ) -> HttpResponse:
        async with self.__client.ClientSession() as client:
            if json:
                response_data = await client.post(url=url, json=json)
                return await self.__return_response(response_data)
            if data:
                response_data = await client.post(url=url, data=data)
                return await self.__return_response(response_data)
        response_data = await client.post(url=url)
        return await self.__return_response(response_data)

    async def __return_response(self, response_data: Any) -> HttpResponse:
        with contextlib.suppress(aiohttp.client_exceptions.ContentTypeError):
            return HttpResponse(response_data.status, await response_data.json(), await response_data.text())
        return HttpResponse(text_data=await response_data.text(), status=response_data.status)
