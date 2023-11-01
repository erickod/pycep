from unittest.mock import AsyncMock

from pycep.adapters.aiohttp_client import AioHttpHttpClient, HttpResponse


class FakeAioHttp:
    def __init__(self, *, output_value) -> None:
        self._amock = AsyncMock()
        self._amock.__aenter__.return_value = self._amock
        self._amock.get.return_value = self._amock
        self._amock.post.return_value = self._amock
        self._amock.json.return_value = output_value
        self._amock.data.return_value = output_value
        self._amock.text.return_value = output_value
        self.output_value = output_value

    def ClientSession(self) -> "FakeAioHttp":
        return self._amock

    def __aenter__(self, *args):
        return self._amock

    def __aexit__(self, *args):
        return


async def test_get_method() -> None:
    client = FakeAioHttp(output_value="any valid output")
    sut = AioHttpHttpClient(client=client)
    output = await sut.get("https://acme.co")
    assert isinstance(output, HttpResponse)
    assert output.json() == client.output_value


async def test_post_method_with_json_input() -> None:
    client = FakeAioHttp(output_value="any valid output")
    sut = AioHttpHttpClient(client=client)
    output = await sut.post("https://acme.co", json={"value": 1})
    assert isinstance(output, HttpResponse)
    assert output.json() == client.output_value


async def test_post_method_with_data_input() -> None:
    client = FakeAioHttp(output_value="any valid output")
    sut = AioHttpHttpClient(client=client)
    output = await sut.post("https://acme.co", data={"value": 1})
    assert isinstance(output, HttpResponse)
    assert output.json() == client.output_value


async def test_post_method_with_no_input() -> None:
    client = FakeAioHttp(output_value="any valid output")
    sut = AioHttpHttpClient(client=client)
    output = await sut.post("https://acme.co")
    assert isinstance(output, HttpResponse)
    assert output.json() == client.output_value
