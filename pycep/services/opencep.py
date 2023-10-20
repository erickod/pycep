from typing import Any

import httpx

from pycep.protocols.query_service import QueryService


class OpenCepService:
    def __init__(self, http_client=httpx) -> None:
        self.__base_url = "https://opencep.com/v1/{cep}.json"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> Any:
        response = self.__http_client.get(self.__base_url.format(cep=cep))
        return response.json()


def make() -> QueryService:
    return OpenCepService()
