from typing import Any


class DummyResponse:
    def __init__(
        self, response_data: dict[str, Any] | str | bytes, *args, **kwargs
    ) -> None:
        self.response_data = response_data

    def json(self) -> dict[str, Any]:
        return self.response_data

    @property
    def text(self) -> str:
        return self.response_data


class FakeHttpClient:
    def __init__(
        self,
        get_output: dict[str, Any] | str | bytes = {},
        post_output: dict[str, Any] | str | bytes = {},
        response_class: Any = DummyResponse,
    ) -> None:
        self.get_output = get_output
        self.post_output = post_output
        self.get_is_called: bool = False
        self.post_is_called: bool = False
        self.response_class = response_class

    def get(self, *args, **kwargs) -> Any:
        self.get_is_called = True
        return self.response_class(response_data=self.get_output)

    def post(self, *args, **kwargs) -> Any:
        self.post_is_called = True
        return self.response_class(response_data=self.post_output)
