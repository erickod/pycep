import asyncio

from pycep.cep_data import CepData
from pycep.protocols.query_service import QueryService


class FakeQueryService:
    def __init__(
        self,
        street: str = "Rua dos bobos",
        district: str = "Centro",
        city: str = "Cidade Lateral",
        state: str = "GO",
        cep: str = "72120020",
        provider="",
    ) -> None:
        self.street = street
        self.district = district
        self.city = city
        self.state = state
        self.cep = cep
        self.provider = provider or self.__class__.__name__

    async def query_cep(self, cep: str) -> CepData:
        return CepData(
            street=self.street,
            district=self.district,
            city=self.city,
            state=self.state,
            cep=self.cep,
            provider=self.provider,
        )


def make() -> QueryService:
    return FakeQueryService()


class SlowQueryService(FakeQueryService):
    def __init__(self, delay: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self.delay = delay

    async def query_cep(self, cep: str) -> CepData:
        await asyncio.sleep(self.delay)
        return await super().query_cep(cep)


class EmptyQueryService:
    """Answers immediately without finding the CEP (e.g. ViaCEP `{"erro": "true"}`)."""

    async def query_cep(self, cep: str) -> CepData:
        return CepData(cep=cep, street=None, city=None, provider="EmptyQueryService")


class FailingQueryService:
    async def query_cep(self, cep: str) -> CepData:
        raise ConnectionError("provider down")
