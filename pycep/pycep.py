from typing import Any


class PyCEP:
    def __init__(self, cep: str = "") -> None:
        self.__cep_number: str = cep

    def __call__(self, cep: str, *args: Any, **kwds: Any) -> "PyCEP":
        return PyCEP(cep)

    def __int__(self) -> int:
        return int(self.__cep_number)


Cep = PyCEP()
