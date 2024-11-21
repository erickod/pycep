from typing import Any, Dict
from dataclasses import dataclass, field


@dataclass
class HttpResponse:
    status: int
    json_data: Dict[str, Any] = field(default_factory=dict)
    text_data: str = ""

    def json(self) -> Dict[str, Any]:
        return self.json_data

    def text(self) -> str:
        return self.text_data
