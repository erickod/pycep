from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class QueryService(Protocol):
    async def query_cep(self, cep: str) -> Any:
        pass
