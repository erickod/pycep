from typing import Any, Protocol, Union
from pycep.adapters.http_response import HttpResponse


class HttpClient(Protocol):
    async def get(self, url: str) -> HttpResponse:
        pass

    async def post(
        self,
        url: str,
        data: Union[dict[str, Any], bytes] = {},
        json: dict[str, Any] = {},
    ) -> HttpResponse:
        pass
