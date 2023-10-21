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
