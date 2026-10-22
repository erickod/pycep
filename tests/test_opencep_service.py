from pycep.protocols.query_service import QueryService
from pycep.services.opencep import OpenCepService, make
from tests.helpers.fake_http_client import FakeHttpClient


def test_make_returns_a_query_service() -> None:
    sut = make()
    assert isinstance(sut, OpenCepService)
    assert isinstance(sut, QueryService)


async def test_given_found_cep_when_query_then_maps_provider_fields() -> None:
    sut = OpenCepService(http_client=FakeHttpClient(get_output={'logradouro': 'Rua A', 'bairro': 'Centro', 'localidade': 'Anápolis', 'uf': 'GO'}))
    output = await sut.query_cep("75140070")
    assert (output.street, output.district) == ('Rua A', 'Centro')
    assert (output.city, output.state) == ("Anápolis", "GO")
    assert output.provider == "OpenCepService"
    assert output.is_useful()


async def test_given_http_error_when_query_then_returns_without_waiting() -> None:
    http_client = FakeHttpClient(get_output={"message": "not found"}, status_output=404)
    sut = OpenCepService(http_client=http_client)
    output = await sut.query_cep("99999999")
    assert not output.is_useful()
    assert output.provider == "OpenCepService"
