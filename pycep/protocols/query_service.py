from typing import Protocol, runtime_checkable

from pycep.cep_data import CepData


@runtime_checkable
class QueryService(Protocol):
    async def query_cep(self, cep: str) -> CepData:
        pass
