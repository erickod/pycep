from typing import Any, Protocol


class CEPServicesLoader(Protocol):
    def load(self) -> Any:
        pass
