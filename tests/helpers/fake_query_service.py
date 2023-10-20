from typing import Any

from pycep.protocols.query_service import QueryService


class FakeQueryService:
    async def query_cep(self, cep: str) -> Any:
        return


def make() -> QueryService:
    return FakeQueryService()
