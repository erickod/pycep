from typing import Any
from dataclasses import dataclass, field


@dataclass
class HttpResponse:
    status: int
    json_data: dict[str, Any] = field(default_factory=dict)
    text_data: str = ""

    def json(self) -> dict[str, Any]:
        return self.json_data

    def text(self) -> str:
        return self.text_data
