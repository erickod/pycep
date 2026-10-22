from pycep.services.viacep import ViaCepService
from tests.helpers.fake_http_client import FakeHttpClient


async def test_given_erro_payload_when_query_then_result_is_not_useful() -> None:
    sut = ViaCepService(http_client=FakeHttpClient(get_output={"erro": "true"}))
    output = await sut.query_cep("99999999")
    assert not output.is_useful()
    assert output.city == ""
