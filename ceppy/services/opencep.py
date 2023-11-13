from ceppy.adapters.aiohttp_client import AioHttpHttpClient
from ceppy.cep_data import CepData
from ceppy.protocols.http_client import HttpClient
from ceppy.protocols.query_service import QueryService


class OpenCepService:
    def __init__(self, http_client: HttpClient = AioHttpHttpClient()) -> None:
        self.__base_url = "https://opencep.com/v1/{cep}.json"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> CepData:
        response = await self.__http_client.get(self.__base_url.format(cep=cep))
        response_asdict = response.json()
        return CepData(
            street=response_asdict.get("logradouro"),
            district=response_asdict.get("bairro"),
            city=response_asdict.get("localidade"),
            state=response_asdict.get("uf"),
            cep=cep,
            provider=self.__class__.__name__,
        )


def make() -> QueryService:
    return OpenCepService()
    return OpenCepService()
