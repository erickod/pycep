import httpx

from pycep.cep_data import CepData
from pycep.protocols.query_service import QueryService


class OpenCepService:
    def __init__(self, http_client=httpx) -> None:
        self.__base_url = "https://opencep.com/v1/{cep}.json"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> CepData:
        response = self.__http_client.get(self.__base_url.format(cep=cep))
        response_asdict = response.json()
        return CepData(
            street=response_asdict.get("logradouro"),
            district=response_asdict.get("bairro"),
            city=response_asdict.get("localidade"),
            state=response_asdict.get("uf"),
            cep=response_asdict.get(cep),
            provider=self.__class__.__name__,
        )


def make() -> QueryService:
    return OpenCepService()
