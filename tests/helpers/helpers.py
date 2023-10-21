from typing import Any, List

from pycep.protocols.query_service import QueryService


class FakeCEPServicesLoader:
    def __init__(self, output_services: List[QueryService] = []) -> None:
        self.load_is_called: bool = False
        self.output_services = output_services

    def load(self) -> Any:
        self.load_is_called = True
        return self.output_services
