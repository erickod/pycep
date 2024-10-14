from pycep.adapters.httpx_client import HttpxHttpClient
from pycep.cep_data import CepData
from pycep.protocols.http_client import HttpClient
from pycep.protocols.query_service import QueryService


class ViaCepService:
    def __init__(self, http_client: HttpClient = HttpxHttpClient()) -> None:
        self.__base_url = "https://viacep.com.br/ws/{cep}/json/"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> CepData:
        response = await self.__http_client.get(self.__base_url.format(cep=cep))
        response_asdict = response.json()
        cep_data = CepData(
            street=response_asdict.get("logradouro"),
            district=response_asdict.get("bairro"),
            city=response_asdict.get("localidade"),
            state=response_asdict.get("uf"),
            cep=cep,
            complement=response_asdict.get("complemento", ""),
            provider=self.__class__.__name__,
        )
        return cep_data


def make() -> QueryService:
    return ViaCepService()
