import asyncio
from pycep.adapters.httpx_client import HttpxHttpClient
from pycep.cep_data import CepData
from pycep.protocols.http_client import HttpClient
from pycep.protocols.query_service import QueryService


class BrasilAPIService:
    def __init__(self, http_client: HttpClient = HttpxHttpClient()) -> None:
        self._base_url = "https://cdn.apicep.com/file/apicep/{cep}.json"
        self._http_client = http_client

    async def query_cep(self, cep: str) -> CepData:
        response = await self._http_client.get(self._base_url.format(cep=self.__format_cep(cep)))
        response_asdict = response.json()
        if response.status != 200:
            await asyncio.sleep(10)
        return CepData(
            street=response_asdict.get("address"),
            district=response_asdict.get("district"),
            city=response_asdict.get("city"),
            state=response_asdict.get("state"),
            cep=cep,
            complement=response_asdict.get("complemento", ""),
            provider=self.__class__.__name__,
        )
    def __format_cep(self, cep: str) -> str:
        return f"{cep[0:-3]}-{cep[5:]}"


def make() -> QueryService:
    return BrasilAPIService()
