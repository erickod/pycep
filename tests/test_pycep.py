import tests
from pycep import Cep
from pycep.cep_service_loader import CepQueryServiceLoader
from pycep.pycep import PyCEP
from tests.helpers import FakeCEPServicesLoader


def test_is_created_with_waiting_query_status() -> None:
    sut = PyCEP(
        "72120020",
        cep_services_loader=CepQueryServiceLoader(
            module=tests,
            walk_packages=lambda *args, **kwargs: [
                (None, "tests.helpers.fake_query_service", None)
            ],
        ),
    )
    assert sut.status == "waiting_query"


def test_load_method_from_cep_services_is_called_at_PyCEP_instantiation_time() -> None:
    cep_services_loader = FakeCEPServicesLoader()
    Cep("72120020", cep_services_loader=cep_services_loader)
    assert cep_services_loader.load_is_called
