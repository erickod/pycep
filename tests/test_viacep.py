from ceppy.cep_data import CepData
from ceppy.protocols.query_service import QueryService
from ceppy.services.viacep import ViaCepService, make
from tests.helpers.fake_http_client import FakeHttpClient

expected_get_output = {
    "cep": "72120-020",
    "logradouro": "Quadra QND 2",
    "complemento": "SC",
    "bairro": "Taguatinga Norte (Taguatinga)",
    "localidade": "Brasília",
    "uf": "DF",
    "ibge": "5300108",
}


async def test_make_returns_right_instance() -> None:
    sut = make()
    assert isinstance(sut, ViaCepService)


async def test_instance_implements_query_service() -> None:
    sut = make()
    assert isinstance(sut, QueryService)


async def test_querycep_returns_expected_value() -> None:
    http_client = FakeHttpClient(get_output=expected_get_output)
    sut = ViaCepService(http_client=http_client)
    output = await sut.query_cep("72120020")
    assert http_client.get_is_called
    assert isinstance(output, CepData)
    assert output.district == "Taguatinga Norte (Taguatinga)"
    assert output.city == "Brasília"
    assert output.street == "Quadra QND 2 SC"
    assert output.state == "DF"
    assert output.provider == ViaCepService.__name__
