from pycep import Cep
from pycep.pycep import PyCEP
from tests.helpers import FakeCEPServicesLoader
from tests.helpers.fake_query_service import FakeQueryService


def test_is_created_with_waiting_query_status() -> None:
    sut = PyCEP(
        "72120020",
        cep_services_loader=FakeCEPServicesLoader(output_services=[]),
    )
    assert sut.status == "waiting_query"


def test_load_method_from_cep_services_is_called_at_PyCEP_instantiation_time() -> None:
    cep_services_loader = FakeCEPServicesLoader(output_services=[FakeQueryService()])
    assert not cep_services_loader.load_is_called
    sut = Cep("72120020", cep_services_loader=cep_services_loader)
    assert cep_services_loader.load_is_called
    assert sut.status == "query_done"


def test_cep_acess_attributes() -> None:
    street = "Rua dos bobos"
    district = "Centro"
    city = "Cidade Lateral"
    state = "GO"
    cep = "72120020"
    output_services = [FakeQueryService(street, district, city, state, cep)]
    cep_services_loader = FakeCEPServicesLoader(output_services=output_services)
    sut = Cep(cep, cep_services_loader=cep_services_loader)
    assert sut.number == cep
    assert sut.street == street
    assert sut.district == district
    assert sut.city == city
    assert sut.state == state
    assert sut.query_service == FakeQueryService.__name__


def test_cep_acess_attributes_with_index_syntax() -> None:
    street = "Rua dos bobos"
    district = "Centro"
    city = "Cidade Lateral"
    state = "GO"
    cep = "72120020"
    output_services = [FakeQueryService(street, district, city, state, cep)]
    cep_services_loader = FakeCEPServicesLoader(output_services=output_services)
    sut = Cep(cep, cep_services_loader=cep_services_loader)
    assert sut["number"] == cep
    assert sut["street"] == street
    assert sut["district"] == district
    assert sut["city"] == city
    assert sut["state"] == state
    assert sut["query_service"] == FakeQueryService.__name__


def test_repr_implementation() -> None:
    street = "Rua dos bobos"
    district = "Centro"
    city = "Cidade Lateral"
    state = "GO"
    cep = "72120020"
    output_services = [FakeQueryService(street, district, city, state, cep)]
    cep_services_loader = FakeCEPServicesLoader(output_services=output_services)
    sut = Cep(cep, cep_services_loader=cep_services_loader)
    assert str(sut) == "PyCEP(cep=72120020)"


def test_access_items_using_numeric_indexes() -> None:
    street = "Rua dos bobos"
    district = "Centro"
    city = "Cidade Lateral"
    state = "GO"
    cep = "72120020"
    output_services = [FakeQueryService(street, district, city, state, cep)]
    cep_services_loader = FakeCEPServicesLoader(output_services=output_services)
    sut = Cep(cep, cep_services_loader=cep_services_loader)
    assert sut[0] == ("street", "Rua dos bobos")
    assert sut[1] == ("district", "Centro")
    assert sut[2] == ("city", "Cidade Lateral")
    assert sut[3] == ("state", "GO")
    assert sut[4] == ("cep", "72120020")
    assert sut[5] == ("provider", "FakeQueryService")


def test_access_items_using_keys() -> None:
    street = "Rua dos bobos"
    district = "Centro"
    city = "Cidade Lateral"
    state = "GO"
    cep = "72120020"
    output_services = [FakeQueryService(street, district, city, state, cep)]
    cep_services_loader = FakeCEPServicesLoader(output_services=output_services)
    sut = Cep(cep, cep_services_loader=cep_services_loader)
    assert sut["street"] == "Rua dos bobos"
    assert sut["district"] == "Centro"
    assert sut["city"] == "Cidade Lateral"
    assert sut["state"] == "GO"
    assert sut["cep"] == "72120020"
    assert sut["provider"] == "FakeQueryService"
