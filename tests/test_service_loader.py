from unittest.mock import Mock

import tests
from pycep.cep_service_loader import CepQueryServiceLoader


def test_CepQueryServiceLoader_loads_cep_query_services_modules() -> None:
    walk_packages = Mock()
    walk_packages.return_value = [(None, "tests.helpers.fake_query_service", None)]
    sut = CepQueryServiceLoader(module=tests, walk_packages=walk_packages)
    assert sut.load() == ["FakeQueryService"]
