from typing import Any

from pycep.cep_service_loader import CepQueryServiceLoader
from pycep.protocols.service_loader import CEPServicesLoader


class PyCEP:
    def __init__(
        self, cep: str = "", *, cep_services_loader: CEPServicesLoader
    ) -> None:
        self.__cep_number: str = cep
        self.__query_services = cep_services_loader.load()

    def __call__(self, cep: str, *args: Any, **kwargs: Any) -> Any:
        self.__cep_number = cep

    def __int__(self) -> int:
        return int(self.__cep_number)


class CepFactory:
    def __call__(
        self,
        cep: str,
        *,
        cep_services_loader: CEPServicesLoader = CepQueryServiceLoader()
    ) -> PyCEP:
        return PyCEP(cep, cep_services_loader=cep_services_loader)


Cep = CepFactory()
