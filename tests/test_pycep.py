from pycep import Cep
from tests.helpers import FakeCEPServicesLoader


def test_ensure_cep_is_callalbe_and_int_conversible() -> None:
    sut = Cep("72120020")
    assert int(sut) == 72120020


def test_load_method_from_cep_services_is_called_at_PyCEP_instantiation_time() -> None:
    cep_services_loader = FakeCEPServicesLoader()
    Cep("72120020", cep_services_loader=cep_services_loader)
    assert cep_services_loader.load_is_called
