from typing import Any, Dict, Union

from typing_extensions import Protocol

from pycep.adapters.http_response import HttpResponse


class HttpClient(Protocol):
    async def get(self, url: str) -> HttpResponse:
        pass

    async def post(
        self,
        url: str,
        data: Union[Dict[str, Any], bytes] = {},
        json: Dict[str, Any] = {},
    ) -> HttpResponse:
        pass
