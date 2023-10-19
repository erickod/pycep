from pycep import Cep


def test_cep_is_callalbe_passing_a_cep_as_string() -> None:
    sut = Cep("72120020")
    assert int(sut) == 72120020
