from typing import Any


class FakeCEPServicesLoader:
    def __init__(self) -> None:
        self.load_is_called: bool = False

    def load(self) -> Any:
        self.load_is_called = True
