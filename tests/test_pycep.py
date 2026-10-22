import time

import pytest

from pycep import Cep, CepQueryError
from pycep.pycep import PyCEP
from tests.helpers import FakeCEPServicesLoader
from tests.helpers.fake_query_service import (
    EmptyQueryService,
    FailingQueryService,
    FakeQueryService,
    SlowQueryService,
)


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
    assert sut[6] == ("provider", "FakeQueryService")


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


def test_given_fast_not_found_and_slow_found_when_query_then_returns_the_found() -> None:
    """
    GIVEN a provider that answers "not found" at once and another that finds 72120020 after 0.05s
    WHEN  the CEP 72120020 is queried
    THEN  the result is the slower provider's city 'Cidade Lateral'
    """
    services = [EmptyQueryService(), SlowQueryService(0.05, provider="SlowService")]
    sut = Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.city == "Cidade Lateral"
    assert sut.query_service == "SlowService"


def test_given_failing_fast_and_slow_found_when_query_then_failure_is_ignored() -> None:
    """
    GIVEN a provider that raises ConnectionError at once and another that finds the CEP after 0.05s
    WHEN  the CEP 72120020 is queried
    THEN  no error is raised and the slower provider's data is returned
    """
    services = [FailingQueryService(), SlowQueryService(0.05)]
    sut = Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.state == "GO"


def test_given_slow_provider_when_fast_one_finds_then_does_not_wait_for_the_slow() -> None:
    """
    GIVEN a provider that finds the CEP at once and another that takes 5 seconds
    WHEN  the CEP 72120020 is queried
    THEN  the result is returned in under 1 second from the fast provider
    """
    services = [SlowQueryService(5, provider="Slow"), FakeQueryService(provider="Fast")]
    started = time.monotonic()
    sut = Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services))
    assert time.monotonic() - started < 1
    assert sut.query_service == "Fast"


def test_given_two_found_answers_when_query_then_the_first_to_arrive_wins() -> None:
    """
    GIVEN provider A answering after 0.2s and provider B after 0.01s, both with data
    WHEN  the CEP 72120020 is queried
    THEN  the result comes from provider B
    """
    services = [SlowQueryService(0.2, provider="A"), SlowQueryService(0.01, provider="B")]
    sut = Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.query_service == "B"


def test_given_no_provider_finds_the_cep_when_query_then_returns_empty_data() -> None:
    """
    GIVEN two providers that answer "not found" for 99999999
    WHEN  the CEP 99999999 is queried
    THEN  status is 'query_done' and city, state and street are empty strings
    """
    services = [EmptyQueryService(), EmptyQueryService()]
    sut = Cep("99999999", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.status == "query_done"
    assert (sut.city, sut.state, sut.street) == ("", "", "")


def test_given_not_found_and_failure_when_query_then_returns_empty_data() -> None:
    """
    GIVEN one provider answering "not found" and another raising ConnectionError
    WHEN  the CEP 99999999 is queried
    THEN  no error is raised and city is an empty string
    """
    services = [EmptyQueryService(), FailingQueryService()]
    sut = Cep("99999999", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.city == ""


def test_given_every_provider_fails_when_query_then_raises_cep_query_error() -> None:
    """
    GIVEN two providers that raise ConnectionError
    WHEN  the CEP 72120020 is queried
    THEN  CepQueryError is raised
    """
    services = [FailingQueryService(), FailingQueryService()]
    with pytest.raises(CepQueryError):
        Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services))


def test_given_providers_slower_than_timeout_when_query_then_raises_cep_query_error() -> None:
    """
    GIVEN two providers that take 5 seconds and a timeout of 0.05 seconds
    WHEN  the CEP 72120020 is queried
    THEN  CepQueryError is raised after about 0.05 seconds
    """
    services = [SlowQueryService(5), SlowQueryService(5)]
    started = time.monotonic()
    with pytest.raises(CepQueryError):
        Cep("72120020", cep_services_loader=FakeCEPServicesLoader(services), timeout=0.05)
    assert time.monotonic() - started < 1


def test_given_cep_without_street_when_query_then_it_is_still_useful() -> None:
    """
    GIVEN a provider that finds a city-wide CEP with city 'Pequena' and state 'GO' but no street
    WHEN  the CEP 72000000 is queried
    THEN  the result has city 'Pequena' and an empty street
    """
    services = [FakeQueryService(street="", district="", city="Pequena")]
    sut = Cep("72000000", cep_services_loader=FakeCEPServicesLoader(services))
    assert sut.city == "Pequena"
    assert sut.street == ""
