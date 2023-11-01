from pycep.cep_data import CepData
from pycep.protocols.query_service import QueryService
from pycep.services.correios import CorreiosService, make
from tests.helpers.fake_http_client import FakeHttpClient

post_output = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:consultaCEPResponse xmlns:ns2="http://cliente.bean.master.sigep.bsb.correios.com.br/"><return><bairro>Taguatinga Norte (Taguatinga)</bairro><cep>72120020</cep><cidade>Brasília</cidade><complemento2>SC</complemento2><end>QND 2</end><uf>DF</uf></return></ns2:consultaCEPResponse></soap:Body></soap:Envelope>'.encode()


async def test_make_returns_right_instance() -> None:
    sut = make()
    assert isinstance(sut, CorreiosService)


async def test_instance_implements_query_service() -> None:
    sut = make()
    assert isinstance(sut, QueryService)


async def test_querycep_returns_expected_value() -> None:
    http_client = FakeHttpClient(post_output=post_output)
    sut = CorreiosService(http_client=http_client)
    output = await sut.query_cep("72120020")
    assert http_client.post_is_called
    assert isinstance(output, CepData)
    assert output.district == "Taguatinga Norte (Taguatinga)"
    assert output.city == "Brasília"
    assert output.street == "QND 2 SC"
    assert output.state == "DF"
    assert output.provider == CorreiosService.__name__
