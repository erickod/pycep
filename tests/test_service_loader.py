from unittest.mock import Mock

import pytest

import tests
from ceppy.cep_service_loader import CepQueryServiceLoader
from tests.helpers.fake_query_service import FakeQueryService


def test_CepQueryServiceLoader_loads_cep_query_services_modules() -> None:
    walk_packages = Mock()
    walk_packages.return_value = [(None, "tests.helpers.fake_query_service", None)]
    sut = CepQueryServiceLoader(module=tests, walk_packages=walk_packages)
    assert isinstance(sut.load()[0], FakeQueryService)


def test_CepQueryServiceLoader_raises_when_a_incompatible_module_is_found() -> None:
    walk_packages = Mock()
    walk_packages.return_value = [
        (None, "tests.helpers.incompatible_query_service", None)
    ]
    sut = CepQueryServiceLoader(module=tests, walk_packages=walk_packages)
    with pytest.raises(TypeError):
        sut.load()
