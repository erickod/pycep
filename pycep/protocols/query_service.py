from typing import Any, Protocol


class QueryService(Protocol):
    async def query_cep(self, cep: str) -> Any:
        pass
