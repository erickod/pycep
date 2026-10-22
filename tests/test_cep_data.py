from pycep.cep_data import CepData

street = "Estrada do Portela - até 279 - lado ímpar"
state = "RJ"
city = "Rio de Janeiro"
district = "Madureira"
cep = "21351050"
provider = "CorreiosService"


def test_cep_data_instantiation_params() -> None:
    sut = CepData(
        street=street,
        city=city,
        state=state,
        district=district,
        cep=cep,
        provider=provider,
    )
    assert sut.street == street
    assert sut.state == state
    assert sut.city == city
    assert sut.district == district
    assert sut.cep == cep
    assert sut.provider == provider


def test_bool_evaluation_when_any_value_is_fullfilled() -> None:
    sut = CepData(cep=cep)
    assert bool(sut)


def test_none_values_are_normalized_to_empty_strings() -> None:
    sut = CepData(street=None, city=None, cep=cep)
    assert sut.street == ""
    assert sut.city == ""


def test_is_useful_requires_city_and_state() -> None:
    assert CepData(city=city, state=state).is_useful()
    assert not CepData(city=city).is_useful()
    assert not CepData(cep=cep, provider=provider).is_useful()
