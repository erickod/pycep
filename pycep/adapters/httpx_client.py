import contextlib
import json
from typing import Any, Union
import httpx
from .http_response import HttpResponse


class HttpxHttpClient:
    def __init__(self, client=httpx) -> None:
        self.__client = client

    async def get(self, url: str) -> HttpResponse:
        async with self.__client.AsyncClient() as client:
            response_data = await client.get(url=url)
            return await self.__return_response(response_data)

    async def post(
        self,
        url: str,
        data: Union[dict[str, Any], bytes] = {},
        json: dict[str, Any] = {},
    ) -> HttpResponse:
        async with self.__client.AsyncClient() as client:
            if json:
                response_data = await client.post(url=url, json=json)
                return await self.__return_response(response_data)
            if data:
                response_data = await client.post(url=url, data=data)
                return await self.__return_response(response_data)
        response_data = await client.post(url=url)
        return await self.__return_response(response_data)

    async def __return_response(self, response_data: Any) -> HttpResponse:
        with contextlib.suppress(json.decoder.JSONDecodeError):
            return HttpResponse(response_data.status_code, response_data.json(), response_data.text)
        return HttpResponse(text_data=response_data.text, status=response_data.status_code)
