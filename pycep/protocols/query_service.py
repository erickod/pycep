from typing import Any, Protocol


class QueryService(Protocol):
    def query_cep(self, cep: str) -> Any:
        pass
