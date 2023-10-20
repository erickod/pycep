from typing import Protocol

from pycep.protocols.query_service import QueryService


class CEPServicesLoader(Protocol):
    def load(self) -> list[QueryService]:
        pass
