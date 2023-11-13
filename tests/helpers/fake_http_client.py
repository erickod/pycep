from typing import Any

from ceppy.adapters.aiohttp_client import HttpResponse


class FakeHttpClient:
    def __init__(
        self,
        get_output: dict[str, Any] | str | bytes = {},
        post_output: dict[str, Any] | str | bytes = {},
        response_class: Any = HttpResponse,
    ) -> None:
        self.get_output = get_output
        self.post_output = post_output
        self.get_is_called: bool = False
        self.post_is_called: bool = False
        self.response_class = response_class

    async def get(self, *args, **kwargs) -> Any:
        self.get_is_called = True
        return self.response_class(json_data=self.get_output, text_data=self.get_output)

    async def post(self, *args, **kwargs) -> Any:
        self.post_is_called = True
        return self.response_class(
            json_data=self.post_output, text_data=self.post_output
        )
