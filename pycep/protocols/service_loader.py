from typing import List

from typing_extensions import Protocol

from pycep.protocols.query_service import QueryService


class CEPServicesLoader(Protocol):
    def load(self) -> List[QueryService]:
        pass
